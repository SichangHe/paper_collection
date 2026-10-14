                                                         AgentEval: DAG-Structured Step-Level Evaluation
                                                      for Agentic Workflows with Error Propagation Tracking

                                                                  Dongxin Guo1 , Jikun Wu2 , Siu Ming Yiu1
                                                            1
                                                              The University of Hong Kong 2 Stellaris AI Limited
                                                       bettyguo@connect.hku.hk, hk950014@connect.hku.hk,
                                                                             smyiu@cs.hku.hk



                                                               Abstract                         As of early 2025, 62% of organizations are ex-
                                                                                                perimenting with AI agents and 23% are scaling
                                             Agentic systems that chain reasoning, tool use,
arXiv:2604.23581v1 [cs.SE] 26 Apr 2026




                                                                                                deployments (McKinsey & Company, 2025), en-
                                             and synthesis into multi-step workflows are
                                                                                                abled by advances in agent frameworks (Wu et al.,
                                             entering production, yet prevailing evaluation
                                             practices like end-to-end outcome checks and       2023; Schick et al., 2023; Patil et al., 2024). Yet
                                             ad-hoc trace inspection systematically mask        evaluation infrastructure has not kept pace: cur-
                                             the intermediate failures that dominate real-      rent approaches rely on end-to-end outcome met-
                                             world error budgets. We present AGENT E VAL,       rics that mask intermediate failures, ad hoc man-
                                             a framework that formalizes agent executions       ual inspection that does not scale, or static bench-
                                             as evaluation directed acyclic graphs (DAGs),      marks (Liu et al., 2024; Jimenez et al., 2024; Zhou
                                             where each node carries typed quality metrics
                                                                                                et al., 2024b) disconnected from deployment con-
                                             assessed by a calibrated LLM judge (GPT-4o),
                                             classified through a hierarchical failure taxon-   straints such as latency, cost, and continuous inte-
                                             omy (3 levels, 21 subcategories), and linked       gration. This evaluation gap has tangible conse-
                                             to upstream dependencies for automated root        quences: Gartner predicts that over 40% of agentic
                                             cause attribution. An ablation study isolates      AI projects will be canceled by 2027, partly due
                                             the impact of DAG-based dependency model-          to the inability to systematically evaluate deployed
                                             ing: it alone contributes +22 percentage points    agents (Gartner, Inc., 2025).
                                             to failure detection recall and +34 pp to root        Multi-step agent workflows create evaluation
                                             cause accuracy over flat step-level evaluation
                                             with identical judges and rubrics.
                                                                                                challenges absent from traditional NLP evalua-
                                                                                                tion. Agent executions follow DAG-structured de-
                                             Across three production workflows (450 test
                                                                                                pendencies where errors propagate and compound
                                             cases, two agent model families, predomi-
                                             nantly sequential architectures with a 12% non-
                                                                                                through downstream steps (Cemri et al., 2025;
                                             DAG trace rate), AGENT E VAL achieves 2.17×        Zhu et al., 2025), and workflows involve hetero-
                                             higher failure detection recall than end-to-end    geneous step types each requiring distinct qual-
                                             evaluation (0.89 vs. 0.41), Cohen’s κ = 0.84       ity metrics. Process supervision research demon-
                                             agreement with human experts, and 72% root         strates that intermediate-step assessment outper-
                                             cause accuracy against an 81% human ceiling.       forms outcome-only evaluation in the RL train-
                                             Cross-system evaluation on τ -bench and SWE-       ing setting where per-step ground truth is avail-
                                             bench traces confirms transferability (failure
                                                                                                able (Lightman et al., 2024; Uesato et al., 2022);
                                             detection recall ≥ 0.78) without taxonomy or
                                             rubric modification. A 4-month pilot with 18       we adapt this insight to inference-time assessment,
                                             engineers detected 23 pre-release regressions      where ground truth is constructed from expert anno-
                                             through CI/CD-integrated regression testing, re-   tation rather than learned from rewards, and where
                                             ducing median root-cause identification time       deployment infrastructure must operate continu-
                                             from 4.2 hours to 22 minutes and driving mea-      ously rather than as a one-time training signal.
                                             surable failure rate reductions in two work-          We present AGENT E VAL,1 an evaluation infras-
                                             flows.
                                                                                                tructure addressing these challenges through four
                                                                                                contributions:
                                         1   Introduction
                                                                                                 1. Evaluation DAG formalization: representing
                                         Agentic AI systems (autonomous agents that plan,           1
                                                                                                      The name “AgentEval” may have been used by other
                                         reason, and execute multi-step workflows using         unrelated projects; this work is independent and identified by
                                         external tools) are transforming NLP applications.     its GitHub repository (URL at the end of Section 7).
    agent workflows as DAGs where each node car-        tute, UK, 2024), and AgentOps (AgentOps, Inc.,
    ries typed quality metrics, enabling step-level     2024), provides monitoring for ML pipelines and
    evaluation with error propagation tracking.         emerging agent support. These tools differ from
 2. Step-level quality metrics: a metric suite          AGENT E VAL in one important way: none provides
    evaluated via calibrated LLM-as-judge scoring       formal DAG-based dependency modeling with er-
    (GPT-4o) with demonstrated human alignment          ror propagation tracking and root cause attribution
    (κ = 0.84).                                         (Table 7). AGENT E VAL’s root cause attribution
 3. Hierarchical failure taxonomy: a three-level        draws motivation from software engineering fault
    taxonomy with 21 subcategories derived from         localization (Jones and Harrold, 2005; Abreu et al.,
    523 agent traces, with quantitative error propa-    2007), operating as a practical greedy heuristic
    gation statistics.                                  rather than formal causal inference.
 4. Automated regression suite: evaluation infras-
    tructure integrated with CI/CD pipelines for        3     The AGENT E VAL Framework
    continuous quality monitoring.
                                                        AGENT E VAL comprises four integrated compo-
   On three production workflows with pre-
                                                        nents: (1) a formal DAG representation for agent
dominantly sequential architectures (using
                                                        workflows, (2) step-level quality metrics evaluated
Claude 3.5 Sonnet and Llama 3 70B as agents with
                                                        via calibrated LLM-as-judge, (3) a hierarchical fail-
GPT-4o as an independent judge), AGENT E VAL
                                                        ure taxonomy, and (4) an automated regression
achieves 2.17× higher failure detection recall
                                                        suite. Figure 1 provides an architectural overview.
than end-to-end evaluation, κ = 0.84 human
agreement, and 72% root cause accuracy. We              3.1    Agent Workflow as Evaluation DAG
explicitly characterize the approach’s boundaries
for more dynamic architectures in §5.5.                 We formalize agent workflows as evaluation DAGs
                                                        to enable structured step-level assessment.
2   Related Work                                        Definition 1 (Evaluation DAG). An evalua-
                                                        tion DAG is a tuple G = (V, E, τ, M) where
Agent Evaluation and Process Supervision.
                                                        V = {v1 , . . . , vn } is a set of evaluation nodes
Agent evaluation benchmarks have proliferated
                                                        corresponding to agent steps; E ⊆ V × V
(Liu et al., 2024; Jimenez et al., 2024; Zhou et al.,
                                                        defines directed dependency edges; τ : V → T
2024b; Yao et al., 2024; Ma et al., 2024), with
                                                        maps each node to a step type from T =
LATS (Zhou et al., 2024a) providing per-step value
                                                        {P LAN, T OOL S EL, PARAM G EN, E XEC, S YNTH};
estimates for planning. However, a recent survey
                                                        and M : V → 2M maps each node to applicable
(Yehudai et al., 2025) identifies a critical gap: ex-
                                                        quality metrics based on its type.
isting benchmarks evaluate agent capabilities in
                                                           Each node vi carries input context ci from parent
controlled settings, whereas deployment requires
                                                        nodes pa(vi ), agent output oi , and optional refer-
evaluation infrastructure with continuous moni-
                                                        ence ri . The step-level quality score is q(vi ) =
toring, regression detection, and CI/CD integra-
                                                        Eval(oi , ri , ci , M(vi )). The five-type classification
tion. The process supervision literature demon-
                                                        is extensible: the framework supports adding types
strates that evaluating intermediate steps outper-
                                                        (e.g., M EM R ETRIEVAL for RAG agents) by defin-
forms outcome-only evaluation (Lightman et al.,
                                                        ing new metric sets and rubrics.
2024; Uesato et al., 2022), while Cemri et al. (2025)
                                                           The DAG structure enables independent step
and Zhu et al. (2025) show that error propagation is
                                                        evaluation, error propagation tracking, counter-
the primary bottleneck in agent performance. The
                                                        factual analysis, and parallel evaluation of inde-
LLM-as-judge paradigm (Liu et al., 2023; Zheng
                                                        pendent branches. AGENT E VAL supports both
et al., 2023) enables scalable evaluation with >80%
                                                        schema-defined DAGs (expected workflow struc-
human agreement.
                                                        ture) and trace-inferred DAGs (actual execution
Production Infrastructure. The ML observ-               path), enabling detection of structural deviations
ability ecosystem, including MLflow, Weights            such as missing steps or unexpected branches. Non-
& Biases Weave (Weights & Biases, 2024),                DAG traces (∼12%) are handled via loop unrolling
LangSmith (LangChain, Inc., 2023), Arize                and timestamp-based branch resolution, with 0.8%
Phoenix (Arize AI, Inc., 2023), Braintrust (Brain-      falling back to flat evaluation (Appendix A). Dur-
trust Data, Inc., 2023), Inspect (AI Security Insti-    ing our pilot, structural deviation between schema-
                 Instrumentation                       Evaluation Engine                          Integration


            Agent              Trace        DAG             Step             Metric      Regression              CI/CD
            System            Collector     Parser        Evaluators        Aggregator    Detector              Pipeline


                                          Evaluation       Failure            Quality
                                           Rubrics        Taxonomy           Dashboard




Figure 1: AGENT E VAL architecture. Agent traces are collected via OpenTelemetry-compatible instrumentation,
parsed into evaluation DAGs, assessed by type-specific step evaluators using calibrated LLM-as-judge rubrics
and the failure taxonomy, aggregated into workflow-level metrics, and fed into regression detection and CI/CD
integration.


defined and trace-inferred DAGs proved a useful                   stream step that handles flawed upstream input
quality signal: deviant traces were associated with               gracefully (e.g., a tool call that retries on a mal-
2.1× higher failure rates than conformant traces.                 formed parameter) will not be flagged as a local
This is an observational pattern, not a causal claim;             failure, while a step that compounds the error will.
an agent may legitimately deviate from its expected               Downstream prompts include prior step outputs
DAG when the environment returns unexpected                       but not prior judge scores (Algorithm 1, line 4), so
output, and deviation alone does not imply mal-                   judges do not bias toward agreement with upstream
function.                                                         attributions.

3.2   Step-Level Quality Metrics                                  3.3      Hierarchical Failure Taxonomy

Each step type has dedicated metrics: P LAN                       We derive a three-level failure taxonomy from man-
steps are assessed for completeness and feasibil-                 ual analysis of 523 agent traces entirely disjoint
ity; T OOL S EL for selection accuracy and relevance;             from the 450 evaluation test cases (Table 1). The
PARAM G EN for parameter correctness and com-                     taxonomy is informed by prior work on multi-agent
pleteness; E XEC for success rate and result validity;            failures (Cemri et al., 2025; Zhu et al., 2025). The
and S YNTH for faithfulness, completeness, and co-                9 Level 2 categories are used for detection and
herence. We employ LLM-as-judge evaluation us-                    primary classification; 21 Level 3 subcategories
ing GPT-4o (gpt-4o-2024-08-06) with tem-                          (Appendix B) provide granular diagnostic detail.
perature = 0. The agent LLMs (Claude 3.5 Son-                     Taxonomy classification runs as a separate LLM-
net and Llama 3 70B) are from different model                     judge call after a step has already been flagged as a
families than the judge, addressing circular bias.                failure by score thresholding; it produces a diagnos-
Each metric uses a structured prompt with a 1–5                   tic label and does not interact with the propagation
rubric, chain-of-thought reasoning, and 5 few-shot                rule in Algorithm 1. Removing the taxonomy (Ta-
calibration anchors per metric (Appendix C). By                   ble 4) therefore degrades RCA primarily through
“calibration” we mean stratified few-shot anchor-                 loss of semantic grouping during error analysis, not
ing with 5 examples spanning the score range, not                 through changes to which steps are attributed as
iterative prompt optimization against a held-out                  root cause.
human-labeled set.
                                                                  3.4      Automated Regression Suite
Prompt design: absolute versus relative fram-                     The regression suite enables continuous quality
ing. The judge prompts use two intentionally dif-                 monitoring through: test case specification as
ferent framings depending on step type. P LAN is                  JSON with expected DAG structures and toler-
scored relative to the original user query, since plan-           ance thresholds, versioned evaluation tagged with
ning is the step that translates the query into work-             model/prompt/tool configurations, regression de-
flow structure and has no meaningful upstream con-                tection via paired bootstrap tests (p < 0.05) with
text (Appendix C, C.2). Subsequent steps such as                  dual-threshold alerting (historical 2σ and bootstrap
T OOL S EL are scored relative to the local context               significance), CI/CD integration via GitHub Ac-
they received from upstream nodes rather than re-                 tions that blocks deployment on critical regressions,
evaluated against the original query (Appendix C,                 and progressive evaluation where fast smoke tests
C.1). As a consequence of this asymmetry, a down-                 (10 cases, <5 minutes) gate full suites (100+ cases,
       Level 1        Level 2                    Freq.              Specification    CS      DA           DP
                      Goal misinterpretation       12%              Agent LLM        Claude 3.5 Sonnet Llama 3 70B
       Planning       Missing steps                 8%              Framework            LangChain       Custom
                      Incorrect ordering            5%              # Tools available 8         6           5
                                                                    Avg. steps/trace 6.1       5.2         3.8
                      Wrong tool selection         18%              # Test cases      150      150         150
       Execution      Parameter errors             22%              Edge case %      22%      18%         15%
                      API/tool failures             9%
                      Context loss                 11%        Table 2: Workflow specifications. Agent LLMs are from
       Integration    Output hallucination         10%
                                                              different model families than the GPT-4o judge.
                      Premature termination         5%

Table 1: Hierarchical failure taxonomy derived from 523
                                                              4     Experimental Setup
agent traces (disjoint from evaluation data). Context loss
has the highest downstream amplification factor (3.2×).       4.1    Agent Workflows
                                                              We evaluate on three agent workflows deployed in
                                                              customer service (CS), data analysis (DA), and doc-
                                                              ument processing (DP) pipelines (Table 2). Each
  Algorithm 1: AGENT E VAL Evaluation Procedure
                                                              uses the same tool set and prompt templates as its
   Input: Agent execution trace T , DAG schema S
              (optional)                                      production counterpart but operates on anonymized
   Output: Evaluation report R with step scores,              historical queries.
                 failures, root causes
 1 G ← ParseDAG(T, S) ; // Reconstruct DAG
                                                              4.2    Evaluation Dataset
 2 ⟨v1 , . . . , vn ⟩ ← TopologicalSort(G);
 3 for vi in ⟨v1 , . . . , vn ⟩ do                            We use two completely disjoint datasets: a taxon-
 4       ci ← AggregateContext(pa(vi ));
 5       q(vi ) ← LLMJudge(oi , ri , ci , M(τ (vi )));
                                                              omy development set of 523 traces (January–March
 6       if q(vi ) < θτ (vi ) then                            2025), and an evaluation dataset of 150 test cases
 7               fi ← ClassifyFailure(vi , Taxonomy);         per workflow (450 total, April–June 2025), sam-
                 // Greedy heuristic: select
                      lowest-scoring parent                   pled using stratified random sampling (∼80% typi-
 8               if ∃ vj ∈ pa(vi ) : q(vj ) < θτ (vj ) then   cal, ∼20% edge cases). Ground truth annotations
 9                     vj∗ ← arg minvj ∈pa(vi ) q(vj );       were produced by 5 domain experts (3+ years ex-
10                     Mark vi as propagated from vj∗ ;
                                                              perience), none of whom are paper authors. Each
11               else
12                     Mark vi as root cause;                 test case is a multi-step trace, and annotation is per-
13               end                                          formed at the step level: the human-evaluation sub-
14       end                                                  set of 150 traces yields 987 step annotations in total,
15 end
16 R ← Aggregate(G, {q(vi )}, {fi });
                                                              each rated 1–5 on the type-specific rubric. Of these,
17 return R;                                                  195 steps are rated ≤2 by the human majority and
                                                              constitute the failing-step set used as the Failure De-
                                                              tection Recall denominator (Section 4.2; full step
                                                              distribution in Appendix W). For human evaluation,
                                                              9 separate domain experts independently rated 150
<1 hour), reducing cost by 80% during develop-                cases on a 1–5 rubric (inter-annotator κ = 0.79,
ment.                                                         Fleiss’ κ = 0.76). Root causes were independently
                                                              annotated with inter-annotator κRCA = 0.74 (81%
   Algorithm 1 details the core evaluation proce-             pairwise agreement), which we treat as the human
dure. For each trace, the DAG is reconstructed,               ceiling.
nodes are processed in topological order, and each
step is evaluated with type-specific metrics via the          4.3    Baselines and Metrics
LLM judge. Failures are classified using the tax-             End-to-End Only (E2E): evaluates only final out-
onomy and attributed as either root-cause or prop-            put quality using GPT-4o with no intermediate as-
agated using a greedy heuristic: when multiple                sessment. Flat Step Evaluation (Flat): evaluates
parents have low scores, the parent with the lowest           each step independently using identical GPT-4o
quality score is selected as the propagation source.          judge and rubrics but without DAG structure. Rule-
This prioritizes simplicity and low false attribution         Based: 47 hand-crafted deterministic rules across
rates over formal causal reasoning (Appendix F).              the three workflows.
    Method            FDRec↑        FPR↓       HA (κ)↑       RCA↑         Configuration            FDRec↑          HA (κ)↑          RCA↑
    E2E Only    .41 [.35,.47] .08 [.05,.12] .52 [.45,.58]   N/A           Full AGENT E VAL         .89 [.84,.93]   .84 [.79,.88]   .72 [.64,.79]
    Flat Step   .67 [.61,.73] .15 [.11,.20] .71 [.65,.76] .38 [.30,.46]     − DAG structure        .67 [.61,.73]   .71 [.65,.76]   .38 [.30,.46]
    Rule-Based .58 [.52,.64] .05 [.03,.08] .63 [.57,.69] .45 [.37,.53]      − LLM judge            .62 [.56,.68]   .66 [.60,.72]   .51 [.43,.59]
    AGENT E VAL .89 [.84,.93] .07 [.04,.11] .84 [.79,.88] .72 [.64,.79]     (replaced w/ rules)
                                                                            − Failure taxonomy     .82 [.77,.87]   .79 [.74,.84]   .54 [.46,.62]
                                                                            − Calibration          .85 [.80,.90]   .76 [.70,.81]   .68 [.60,.75]
Table 3: Main results on 150 human-annotated test cases
with 95% bootstrap CIs. AgentEval vs. Flat Step: p <
                                                                          Table 4: Ablation study. DAG structure contributes the
0.001 (FDRec, HA, RCA).
                                                                          most (−22 pp FDRec, −34 pp RCA). All differences
                                                                          significant at p < 0.01.
  We measure Failure Detection Recall (FDRec),
False Positive Rate (FPR), Human Agreement
                                                                          formance degrades moderately (FDRec 0.82, RCA
(HA, Cohen’s κ), and Root Cause Accuracy
                                                                          0.58) but remains above flat evaluation.
(RCA). All metrics reported with 95% bootstrap
CIs (10,000 resamples).                                                   5.2     Ablation Study
5      Results and Analysis                                               Removing DAG structure causes the largest degra-
                                                                          dation (−22 pp FDRec, −34 pp RCA; p < 0.001),
5.1      Main Results
                                                                          confirming dependency modeling as the most im-
AGENT E VAL achieves FDRec 0.89, representing                             portant design decision. Replacing LLM-as-judge
2.17× higher recall than E2E (0.41) and outper-                           with rules causes the second-largest drop (−27 pp
forming Flat Step (0.67, +22 pp, p < 0.001).                              FDRec). Removing the failure taxonomy primarily
FDRec is computed against the 195 steps humans                            impacts RCA (−18 pp), and calibration anchors
labeled as failing; for each method, the question is                      primarily affect human agreement (−8 pp κ).
which of those 195 failing steps the method flags.                           Execution failures dominate across all work-
By construction, E2E only inspects the final syn-                         flows (42–55%), but integration failures are most
thesis step, so failures originating earlier in the                       impactful: context loss has an average downstream
workflow are detectable only when they cause the                          amplification factor of 3.2×, explaining why DAG-
final output to fail visibly. The 2.17× gap therefore                     based evaluation outperforms flat evaluation. Re-
quantifies the recall lost to that structural restric-                    sults are robust across four judge models (GPT-4o,
tion, not a difference in judge quality on equivalent                     Claude 3.5 Sonnet, GPT-4o-mini, Llama 3 70B),
inputs. Since the only difference from Flat Step is                       with the DAG advantage remaining significant for
DAG structure (identical judges and rubrics), the                         all (p < 0.01; Appendix I). Same-family judg-
+22 pp improvement over Flat Step further iso-                            ing (Claude judging Claude agents) produces com-
lates the contribution of dependency modeling on                          parable or slightly lower scores, ruling out self-
top of step-level evaluation. Across all 450 test                         evaluation inflation (Appendix J).
cases, 63% of step-level failures are propagated
from upstream errors rather than locally caused,                          Judge capability requirements. The judge does
underscoring why dependency tracking is essen-                            not need to solve the agent’s task in order to evalu-
tial. Human agreement reaches κ = 0.84 [0.79,                             ate it: verifying that a tool selection is reasonable,
0.88] (“almost perfect”), remaining strong on the                         that parameters match a schema, or that a synthesis
failure subset (κ = 0.76, Appendix D). Root cause                         step is grounded in retrieved context is in general
accuracy of 72% approaches the human ceiling                              easier than producing the action de novo. This
(∼81%), with 72% of incorrect attributions within                         asymmetry is what keeps the cost profile tractable,
1 DAG hop of the true root cause (Appendix E).                            since a cheaper-than-agent judge can still rate steps
Results are consistent across all three workflows                         usefully. Empirically, weaker judges preserve the
(Appendix H).                                                             DAG advantage in failure detection but degrade
   The DAG advantage holds on both typical (+23                           more sharply on root cause accuracy: GPT-4o-mini
pp FDRec) and edge cases (+19 pp), confirming                             retains FDRec 0.83 against 0.89 for GPT-4o, but
the benefit is not driven by edge case oversampling                       RCA drops from 0.72 to 0.65 (Appendix I). The
(Appendix G). The advantage grows with workflow                           practical implication is that the judge should be at
length: +15 pp FDRec for ≤3 steps vs. +28 pp                              least comparable to the weakest agent in the work-
for ≥6 steps. On non-DAG traces (∼12%), per-                              flow on relevant verification tasks; deployments
using judges substantially weaker than the agent              Setting     Domain          FDRec            RCA
should expect detection to remain useful while at-                        CS-Agent           .92             .75
tribution becomes less reliable.                              Internal    DA-Agent           .88             .78
                                                                          DP-Agent           .86             .64
Counterfactual Validation. To validate root                               Retail         .83 [.76,.89]   .61 [.52,.70]
                                                              τ -bench
cause identification, we replace identified root                          Airline        .79 [.71,.86]   .55 [.45,.64]
causes with gold-reference outputs and re-evaluate            SWE-bench   Code editing   .78 [.69,.86]   .52 [.42,.62]
downstream steps. Across 30 sampled failing
traces, counterfactual correction confirms AGEN -         Table 5: Cross-system generalization. Performance
T E VAL -identified root causes in 87% of cases
                                                          degrades on external benchmarks but remains above
                                                          E2E baselines (FDRec 0.38 on τ -bench, 0.35 on SWE-
(26/30), with downstream scores improving by an
                                                          bench).
average of 2.3 points. This procedure measures the
combined effect of correcting the upstream output
and the judge’s sensitivity to the improved con-          (−14 pp τ -bench, −20 pp SWE-bench), concen-
text that downstream steps then receive; it does not      trated in novel failure patterns not in our taxon-
isolate either component. The engineering implica-        omy. To assess potential annotator bias, 2 inde-
tion is that fixing the attributed root cause typically   pendent annotators (graduate students, not authors)
yields measurable improvement on downstream               re-annotated 40 τ -bench traces with comparable
steps the agent itself would re-execute, which is         agreement (κ = 0.74 step quality), suggesting lim-
precisely the intervention pattern engineers use dur-     ited confirmation bias. This pattern of robust de-
ing debugging. Cases where counterfactual correc-         tection with degraded attribution on novel domains
tion does not improve downstream scores (∼13%)            suggests the DAG-based approach generalizes as
are flagged for manual review rather than auto-           evaluation structure, while the taxonomy benefits
attributed.                                               from domain-specific extension.

5.3   Regression Detection                                5.5    Architecture Scope Analysis
We simulate six model update scenarios across 18          Our internal agents exhibit a 12% non-DAG rate.
scenario–workflow combinations. AGENT E VAL               Simulation of increasing non-DAG rates (Ap-
achieves 88% precision and 94% recall for regres-         pendix K) shows that the DAG advantage remains
sion detection, correctly identifying no regression       significant up to ∼60%, beyond which it becomes
for benign prompt rephrasing and correctly local-         marginal (<5 pp). The boundary is not a prop-
izing degradation for single-step tool deprecation.       erty of the architecture alone but of how much
E2E evaluation requires 4× more test cases for            execution structure can be reconstructed post hoc:
equivalent statistical power. During the pilot, 23 re-    retry loops are recoverable through unrolling, dy-
gressions were detected organically (8 genuine, 12        namic branches through timestamp resolution, and
borderline, 3 false positives). One illustrative case:    short reasoning loops through bounded iteration
a prompt template update for CS-Agent replaced            limits. Architectures that defeat reconstruction tend
a structured instruction with a free-form variant;        to share two properties: long unbounded reasoning
AGENT E VAL flagged a significant drop in PARAM -         loops, and parallel agent handoffs without explicit
G EN quality for the account-lookup step (p < 0.01,       dependency declaration. AGENT E VAL is there-
FDRec dropped 12 pp), which propagated to down-           fore most useful for the sequential and moderately-
stream steps, and the team reverted within hours.         branching tool-calling patterns that currently domi-
Additional case studies appear in Appendix L.             nate production deployments; we view extension to
                                                          cycle-aware and multi-agent settings as the natural
5.4   Cross-System Generalization                         next step (Section 7).
To assess generalization, we evaluate on τ -bench
                                                          6     Deployment Experience
(Yao et al., 2024) (120 traces) and SWE-bench
(Jimenez et al., 2024) (80 traces) without modify-        AGENT E VAL operates as a sidecar service with
ing the taxonomy or rubrics. AGENT E VAL suc-             OpenTelemetry-compatible trace collection (<2%
cessfully parses 90% of τ -bench and 89% of SWE-          latency overhead). Evaluation runs asynchronously
bench traces into valid DAGs. FDRec remains               with a tiered judge fallback: GPT-4o primary,
robust (≥0.78), while RCA degrades more sharply           GPT-4o-mini secondary, and locally deployed
Metric                                   Value Source




                                                                                                      th
                                                                                                   mi




                                                                                                                    tr.
Total traces evaluated                   12,847 System logs




                                                                                                                               t
                                                                                                  gS




                                                                                                                           pec
                                                                                                                   ain
                                                                                                           ize
Unique evaluation runs                      342 System logs




                                                                                                   n
                                                                                          AE




                                                                                                                          I ns
                                                                                                La


                                                                                                           Ar

                                                                                                                 Br
Pre-release regressions detected             23 Alerts + triage   Feature
  Genuine / Borderline / False        8 / 12 / 3 Team triage
Config. changes from findings                14 Git commits       DAG dependency model ✓           ∼       ✗       ✗        ✗
Failure rate reduction (CS)        31%→18% Eval suite             Error propagation     ✓          ✗       ✗       ✗        ✗
Failure rate reduction (DA)        27%→15% Eval suite             Root cause analysis   ✓          ✗       ✗       ✗        ✗
Root-cause time (before)          4.2 hr (med.) Survey (n=47)     Calibrated LLM judge  ✓          ∼       ∼       ∼        ✓
Root-cause time (with AE)        22 min (med.) Logs (n=156)       Failure taxonomy      ✓          ✗       ✗       ✗        ✗
                                                                  CI/CD regression      ✓          ✓       ∼       ✓        ∼
                                                                  Open-source          Avail.      ✓       ✓       ✓        ✓
Table 6: Pilot deployment outcomes (4 months, 18
engineers). Note: baseline and pilot measurements
                                                                  Table 7: Comparison with evaluation tools (public docu-
use different instruments; the magnitude of improve-
                                                                  mentation, January 2026; features evolving rapidly). ✓:
ment should be interpreted with caution (details in Ap-
                                                                  full; ∼: partial; ✗: not supported.
pendix M).


Llama 3 70B as an API-independent fallback. Step-                 and principled calibration anchor selection (Ap-
level evaluation takes ∼2 seconds per step; cost per              pendix N). Onboarding a new workflow requires
trace is ∼$0.02 with GPT-4o-mini. Multi-judge                     ∼20–30 person-hours, with same-domain work-
aggregation (3× cost) is recommended for release-                 flows requiring less (∼12–18 hrs) through partial
gating only. At scale (100K traces/day), daily cost               reuse.
is ≈$2K with GPT-4o-mini, motivating progressive
evaluation where fast smoke tests gate full suites.               7   Conclusion
   Over a 4-month pilot (September 2025–January
2026), three engineering teams used AGENT E VAL                   We presented AGENT E VAL, an evaluation infras-
to evaluate agents during active development (Ta-                 tructure that formalizes agent workflows as evalua-
ble 6). The most impactful outcome was the re-                    tion DAGs with step-level quality metrics, a hier-
placement of a previously manual root-cause in-                   archical failure taxonomy, and automated regres-
vestigation process with an automated propagation-                sion testing. On three production workflows with
aware analysis: median time to identify a root cause              predominantly sequential architectures, AGENT E-
moved from 4.2 hours under the prior workflow                     VAL achieves 2.17× higher failure detection recall
(self-reported survey) to 22 minutes with AGEN -                  than end-to-end evaluation, κ = 0.84 human agree-
T E VAL (system-logged). The two figures use dif-                 ment, and 72% root cause accuracy approaching
ferent measurement instruments and the precise                    the human ceiling (81%). The ablation study con-
magnitude should be read with that caveat (Ap-                    firms DAG-based dependency modeling as the sin-
pendix M); the directional improvement is consis-                 gle most impactful component, an advantage that
tent across all three teams. AgentEval’s error prop-              grows with workflow complexity and holds across
agation analysis revealed that 23% of CS-Agent                    four judge models. Cross-system evaluation on τ -
failures originated from a context truncation bug                 bench and SWE-bench demonstrates transferability
in the policy retrieval step; this single fix reduced             (FDRec ≥ 0.78), while architecture scope analy-
CS-Agent’s failure rate by 8 percentage points. For               sis characterizes the practical boundary at ∼60%
DA-Agent, taxonomy-guided analysis identified                     non-DAG traces. A 4-month pilot validated practi-
“parameter hallucination” (syntactically valid but                cal utility, with specific AgentEval-informed fixes
semantically incorrect SQL WHERE clauses) as                      driving measurable failure rate reductions. Future
31% of execution failures; targeted few-shot ex-                  work includes extending to multi-agent systems
amples reduced the parameter error rate from 27%                  via cycle-aware evaluation graphs, automated tax-
to 11%. Practitioner feedback highlighted error                   onomy evolution through trace clustering, and in-
propagation visibility as the primary benefit: “The               tegration of evaluation signals into agent training
DAG visualization made error propagation chains                   loops.
immediately visible. We found three cascading fail-
ure patterns that end-to-end testing had missed en-               Reproducibility. All materials are available at:
tirely.” (Senior Engineer). Key deployment lessons                https://github.com/bettyguo/Agen
include the importance of taxonomy-first design                   tEval.
Acknowledgments                                          AI Security Institute, UK. 2024. Inspect ai: Framework
                                                           for large language model evaluations. Zenodo.
We thank The University of Hong Kong and Stel-
                                                         Arize AI, Inc. 2023. Arize Phoenix: AI observability
laris AI Limited for their support of this work, and       and evaluation. https://github.com/Arize
the anonymous reviewers for constructive feedback         -ai/phoenix.
that improved the paper.
                                                         Braintrust Data, Inc. 2023. Braintrust: The AI ob-
                                                           servability platform for building quality AI products.
Limitations                                                https://www.braintrust.dev/.
Our evaluation covers predominantly sequential           Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A.
agent architectures; the DAG advantage diminishes         Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt
beyond ∼60% non-DAG trace rates, limiting ap-             Keutzer, Aditya G. Parameswaran, Dan Klein, Kan-
                                                          nan Ramchandran, Matei Zaharia, Joseph E. Gonza-
plicability to highly dynamic multi-agent systems         lez, and Ion Stoica. 2025. Why do multi-agent LLM
(§5.5). All core results are from a single orga-          systems fail? arXiv preprint, arXiv.2503.13657.
nization, though cross-system evaluation on two
                                                         Gartner, Inc. 2025. Gartner predicts over 40% of agentic
external benchmarks provides evidence of gener-            AI projects will be canceled by end of 2027. Gartner
alizability. LLM-as-judge evaluation introduces            Press Release, June 25, 2025. https://www.ga
model-dependent biases; our cross-family design            rtner.com/en/newsroom/press-relea
mitigates but does not eliminate these. The RCA            ses/2025-06-25-gartner-predicts-o
                                                           ver-40-percent-of-agentic-ai-proje
algorithm is a practical heuristic, not formal causal      cts-will-be-canceled-by-end-of-202
inference. The deployment comparison uses differ-          7.
ent measurement instruments and should be inter-
preted with caution. We evaluate English-language        Carlos E. Jimenez, John Yang, Alexander Wettig,
                                                           Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R.
workflows only. The commercial tool comparison             Narasimhan. 2024. Swe-bench: Can language mod-
is time-sensitive. Extended discussion of all limita-      els resolve real-world github issues? In The Twelfth
tions appears in Appendix O.                               International Conference on Learning Representa-
                                                           tions, ICLR 2024, Vienna, Austria, May 7-11, 2024.
                                                           OpenReview.net.
Ethical Considerations
                                                         James A. Jones and Mary Jean Harrold. 2005. Em-
Our evaluation uses anonymized historical queries          pirical evaluation of the tarantula automatic fault-
with no personally identifiable information; data          localization technique. In 20th IEEE/ACM Interna-
handling was reviewed under our organization’s in-         tional Conference on Automated Software Engineer-
                                                           ing (ASE 2005), November 7-11, 2005, Long Beach,
ternal data governance process. Human annotators           CA, USA, pages 273–282. ACM.
were domain experts compensated at standard pro-
fessional rates and informed of the study’s purpose.     LangChain, Inc. 2023. LangSmith: AI agent and LLM
                                                           observability platform. https://www.langch
LLM-as-judge evaluation introduces potential bi-
                                                           ain.com/langsmith.
ases from the judge model (GPT-4o); we mitigate
this through cross-family evaluation design but ac-      Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri-
knowledge residual model-dependent biases. The             son Edwards, Bowen Baker, Teddy Lee, Jan Leike,
                                                           John Schulman, Ilya Sutskever, and Karl Cobbe.
failure taxonomy was developed on internal data            2024. Let’s verify step by step. In The Twelfth In-
and may not capture failure modes relevant to all          ternational Conference on Learning Representations,
deployment contexts.                                       ICLR 2024, Vienna, Austria, May 7-11, 2024. Open-
                                                           Review.net.
                                                         Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu
References                                                 Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen
                                                           Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Ao-
Rui Abreu, Peter Zoeteweij, and Arjan J.C. van Gemund.     han Zeng, Zhengxiao Du, Chenhui Zhang, Sheng
  2007. On the accuracy of spectrum-based fault local-     Shen, Tianjun Zhang, Yu Su, Huan Sun, and 3 others.
  ization. In Testing: Academic and Industrial Confer-     2024. Agentbench: Evaluating llms as agents. In
  ence Practice and Research Techniques - MUTATION         The Twelfth International Conference on Learning
  (TAICPART-MUTATION 2007), page 89–98. IEEE.              Representations, ICLR 2024, Vienna, Austria, May
                                                           7-11, 2024. OpenReview.net.
AgentOps, Inc. 2024. AgentOps: Observability and
  DevTool platform for AI agents. https://gith           Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang,
  ub.com/AgentOps-AI/agentops.                             Ruochen Xu, and Chenguang Zhu. 2023. G-eval:
  NLG evaluation using gpt-4 with better human align-    Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  ment. In Proceedings of the 2023 Conference on           Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  Empirical Methods in Natural Language Process-           Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
  ing, EMNLP 2023, Singapore, December 6-10, 2023,         Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
  pages 2511–2522. Association for Computational           llm-as-a-judge with mt-bench and chatbot arena. In
  Linguistics.                                             Advances in Neural Information Processing Systems
                                                           36: Annual Conference on Neural Information Pro-
Chang Ma, Junlei Zhang, Zhihao Zhu, Cheng Yang,            cessing Systems 2023, NeurIPS 2023, New Orleans,
  Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng          LA, USA, December 10 - 16, 2023.
  Kong, and Junxian He. 2024. Agentboard: An an-
  alytical evaluation board of multi-turn LLM agents.    Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman,
  In Advances in Neural Information Processing Sys-        Haohan Wang, and Yu-Xiong Wang. 2024a. Lan-
  tems 38: Annual Conference on Neural Information         guage agent tree search unifies reasoning, acting, and
  Processing Systems 2024, NeurIPS 2024, Vancouver,        planning in language models. In Forty-first Interna-
  BC, Canada, December 10 - 15, 2024.                      tional Conference on Machine Learning, ICML 2024,
                                                           Vienna, Austria, July 21-27, 2024, volume 235 of
McKinsey & Company. 2025. The state of AI in 2025:         Proceedings of Machine Learning Research, pages
 Agents, innovation, and transformation. McKinsey          62138–62160. PMLR / OpenReview.net.
 Global Survey. https://www.mckinsey.com
 /capabilities/quantumblack/our-ins                      Shuyan Zhou, Frank F. Xu, Hao Zhu, Xuhui Zhou,
 ights/the-state-of-ai.                                    Robert Lo, Abishek Sridhar, Xianyi Cheng, Tianyue
                                                           Ou, Yonatan Bisk, Daniel Fried, Uri Alon, and Gra-
Shishir G. Patil, Tianjun Zhang, Xin Wang, and             ham Neubig. 2024b. Webarena: A realistic web
  Joseph E. Gonzalez. 2024. Gorilla: Large language        environment for building autonomous agents. In The
  model connected with massive apis. In Advances in        Twelfth International Conference on Learning Rep-
  Neural Information Processing Systems 38: Annual         resentations, ICLR 2024, Vienna, Austria, May 7-11,
  Conference on Neural Information Processing Sys-         2024. OpenReview.net.
  tems 2024, NeurIPS 2024, Vancouver, BC, Canada,
  December 10 - 15, 2024.                                Kunlun Zhu, Zijia Liu, Bingxuan Li, Muxin Tian, Yingx-
                                                           uan Yang, Jiaxun Zhang, Pengrui Han, Qipeng Xie,
Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta       Fuyang Cui, Weijia Zhang, Xiaoteng Ma, Xiaodong
  Raileanu, Maria Lomeli, Eric Hambro, Luke Zettle-        Yu, Gowtham Ramesh, Jialian Wu, Zicheng Liu, Pan
  moyer, Nicola Cancedda, and Thomas Scialom. 2023.        Lu, James Zou, and Jiaxuan You. 2025. Where LLM
  Toolformer: Language models can teach themselves         agents fail and how they can learn from failures.
  to use tools. In Advances in Neural Information Pro-     arXiv preprint, arXiv.2509.25370.
  cessing Systems 36: Annual Conference on Neural
  Information Processing Systems 2023, NeurIPS 2023,     A    Non-DAG Trace Handling
  New Orleans, LA, USA, December 10 - 16, 2023.
                                                         Approximately 12% of traces involve patterns that
Jonathan Uesato, Nate Kushman, Ramana Kumar,
  H. Francis Song, Noah Y. Siegel, Lisa Wang, An-        do not conform to strict DAGs, primarily retry
  tonia Creswell, Geoffrey Irving, and Irina Higgins.    loops (8%) and dynamic branching (4%). Retry
  2022. Solving math word problems with process-         loops are handled by unrolling into sequential at-
  and outcome-based feedback.        arXiv preprint,     tempts within the DAG, preserving the most re-
  arXiv.2211.14275.
                                                         cent attempt’s output as the step’s canonical result.
Weights & Biases. 2024. W&B Weave: A toolkit for         Dynamic branches are resolved using trace times-
 developing AI-powered applications. https://gi          tamps to reconstruct the executed path. For traces
 thub.com/wandb/weave.
                                                         where DAG reconstruction fails entirely (0.8%),
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu,         the system falls back to flat step evaluation and
  Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang,        flags the trace for manual review.
  Xiaoyun Zhang, and Chi Wang. 2023. Auto-
  gen: Enabling next-gen LLM applications via multi-     B    Full Failure Taxonomy
  agent conversation framework. arXiv preprint,
  arXiv.2308.08155.                                      Table 8 presents the complete three-level failure
Shunyu Yao, Noah Shinn, Pedram Razavi, and Karthik       taxonomy with Level 3 subcategories.
  Narasimhan. 2024. τ -bench: A benchmark for tool-
  agent-user interaction in real-world domains. arXiv    Construction methodology. The taxonomy was
  preprint, arXiv.2406.12045.                            developed through affinity diagramming. Three
                                                         authors independently coded the same 523 develop-
Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun
  Zhao, Roy Bar-Haim, Arman Cohan, and Michal
                                                         ment traces (entirely disjoint from the 450 evalua-
  Shmueli-Scheuer. 2025. Survey on evaluation of llm-    tion test cases), generating an initial pool of failure
  based agents. arXiv preprint, arXiv.2503.16416.        descriptors. These descriptors were then merged
into candidate categories through multiple consen-             D    Human Agreement by Score Subset
sus sessions. The resulting 9 Level 2 categories and
21 Level 3 subcategories were locked before any
                                                                       Subset                   n (steps)   κ
evaluation data was annotated; the evaluation set
was used only to confirm that the categories were                      All steps                     987    .84
                                                                       Failing (score ≤ 2)           195    .76
comprehensive enough to label observed failures,                       Borderline (score = 3)        146    .69
never to refine the taxonomy itself. During the pilot                  Passing (score ≥ 4)           646    .87
deployment, three additional subcategories were
proposed and merged through a propose-discuss-                 Table 9: Human agreement by score subset. Agreement
                                                               remains substantial on failures (κ ≥ 0.69), confirming
merge governance protocol (Appendix N); these
                                                               the overall κ = 0.84 is not inflated by majority-class
additions are reflected in the version reported here.          agreement.

C     LLM-as-Judge Prompt Templates                            E    RCA Error Analysis
All       prompts     use                        GPT-4o        Among the 28% of incorrect attributions, three pat-
(gpt-4o-2024-08-06) with                      temperature      terns dominate: (1) multi-branch convergence (41%
= 0 and max_tokens=1024.                                       of RCA errors), where independent upstream fail-
                                                               ures converge at a single step; (2) long propagation
C.1    Tool Selection (T OOL S EL)                             chains (33%), where the true root cause is ≥3 steps
                                                               upstream; and (3) threshold boundary cases (26%),
 System: You are an expert evaluator assessing the quality     where the root cause scores marginally above the
 of an AI agent’s tool selection in a multi-step workflow.     threshold.
 Evaluate strictly according to the rubric below. First pro-
 vide step-by-step reasoning, then your score on a separate
                                                                  The median distance between attributed and true
 line as “Score: N”.                                           root cause for incorrect attributions is 1 hop, with
 Task: Given the agent’s current context and the tool it       72% of errors within 1 hop and 91% within 2 hops.
 selected, rate the tool selection quality on a 1–5 scale.
 Rubric:                                                       This means most errors send engineers to a nearby
5: Optimal. Best available tool for the subtask.               step rather than a distant one, substantially reduc-
4: Acceptable. Valid tool but better alternative exists.       ing misattribution cost compared to random assign-
3: Partially correct. Correct category but suboptimal tool.
2: Poor. Wrong category but may produce some useful            ment (mean distance 2.8 hops).
    output.
1: Incorrect. Cannot accomplish the subtask.                   F   RCA Attribution Strategy Comparison
 Calibration Examples: [5 anchor examples omitted for
 space]
 Context: {agent_context}
 Available tools: {tool_list}                                  Attribution Strategy             RCA Acc.    False Attr.
 Selected tool: {agent_tool_selection}                         Greedy lowest-parent (default)     .72             .06
 Subtask description: {subtask}                                Full-path minimum                  .75             .14
                                                               Weighted propagation               .73             .09

C.2    Planning (P LAN)
                                                               Table 10: Comparison of RCA strategies. Full-path
                                                               minimum improves accuracy by 3 pp but doubles false
 System: You are an expert evaluator assessing the quality     attributions to distant ancestors.
 of an AI agent’s execution plan. First provide reasoning,
 then “Score: N”.
 Task: Rate the plan quality on a 1–5 scale given the user     Tradeoff discussion. The three strategies differ
 query and available tools.
 Rubric:                                                       in how aggressively they search upstream for a
5: Complete & optimal. All subtasks identified, feasible,      root cause when multiple parents have low scores.
    correctly ordered.                                         Greedy lowest-parent stops at the immediate parent
4: Mostly complete. Minor omission but critical steps
    present.                                                   with the lowest quality score. Full-path minimum
3: Partial. Covers main task but misses 1–2 important          walks the entire ancestor chain and selects the glob-
    subtasks.
2: Inadequate. Major gaps or infeasible steps.
                                                               ally lowest-scoring node. Weighted propagation
1: Incorrect. Plan would not address the user query.           interpolates between the two by weighting parent
 Calibration Examples: [omitted for space]                     scores by edge confidence.
 User query: {query}
 Available tools: {tool_list}                                     Full-path minimum achieves a 3 pp RCA im-
 Agent plan: {agent_plan}                                      provement, but at the cost of more than doubling
         Level 1         Level 2                      Level 3                   Description & Example
                                                      Scope error               Agent addresses wrong aspect of the query
                         Goal misinterpretation
                                                      Ambiguity failure         Agent selects wrong interpretation without
                                                                                clarification
         Planning
                                                      Tool omission             Required tool not included in plan
                         Missing steps                Verification gap          Plan lacks result verification
                                                      Prerequisite skip         Dependency step omitted
                                                      Dependency violation      Step executed before prerequisites
                         Incorrect ordering
                                                      Suboptimal sequence       Valid but inefficient ordering
                                                      Category error            Wrong tool category
                         Wrong tool selection
                                                      Granularity mismatch      Correct category but wrong specificity

         Execution                                    Type mismatch             Wrong data type
                         Parameter errors             Value error               Correct type but incorrect value
                                                      Missing required          Required parameter omitted
                                                      Timeout                   Tool call exceeds time limit
                         API/tool failures
                                                      Error response            Tool returns error, agent fails to handle
                                                      Truncation                Information dropped between steps
                         Context loss
                                                      Selective omission        Agent ignores relevant output parts
         Integration                                  Fabrication               Information not grounded in any result
                         Output hallucination
                                                      Conflation                Information from different steps incorrectly
                                                                                merged
                                                      Partial completion        Agent declares success prematurely
                         Premature termination
                                                      Loop exit                 Agent exits retry loop too early

                     Table 8: Complete three-level failure taxonomy with 21 Level 3 subcategories.


the false-attribution rate (.06 to .14) by reaching                              Steps     ∆FDRec          ∆RCA     n traces
for distant ancestors that may have been transient                               ≤3         +15 pp         +22 pp     127
or already compensated for by intermediate steps.                                4–5        +21 pp         +33 pp     198
                                                                                 ≥6         +28 pp         +42 pp     125
During pilot use, engineers reported that distant
misattributions were disruptive: the wasted inves-
                                                                             Table 12: DAG advantage by workflow length.
tigation time on a misattribution three hops up-
stream consistently exceeded the time saved by the
                                                                         H    Per-Workflow Breakdown
3 pp accuracy gain on cases where a distant attri-
bution was correct. We therefore selected greedy
lowest-parent as the default. Weighted propagation                              Wkfl Method FDRec FPR HA RCA
offers a smaller intermediate tradeoff (1 pp RCA                                         E2E         .35      .07   .48 N/A
improvement, +3 pp false attribution) and may suit                                       Flat        .63      .17   .68 .33
                                                                                CS




                                                                                         Rule        .54      .04   .60 .41
deployments with reliable edge-confidence signals,                                       AE          .92      .08   .86 .75
though our pilot did not require it.                                                     E2E         .43      .09   .54 N/A
                                                                                         Flat        .69      .14   .73 .42
                                                                                DA




                                                                                         Rule        .60      .05   .65 .49
                                                                                         AE          .88      .07   .85 .78
G    Stratified Results
                                                                                         E2E         .46      .08   .55 N/A
                                                                                         Flat        .70      .13   .72 .40
                                                                                DP




                                                                                         Rule        .61      .06   .64 .46
                                                                                         AE          .86      .06   .81 .64
Subset              Method          FDRec HA (κ)           RCA
                                                                                 Table 13: Per-workflow breakdown.
                    Flat Step      .64          .70         .36
Typical (∼80%)
                    AGENT E VAL .87 [.81,.92]   .83      .70 [.61,.78]
                    Flat Step      .76          .74         .44
                                                                         Performance on non-DAG traces (∼12%, 54 traces
Edge (∼20%)                                                              total): FDRec 0.82 [0.73, 0.90] and RCA 0.58
                    AGENT E VAL .95 [.89,.98]   .87      .78 [.67,.87]
                                                                         [0.46, 0.69], lower than overall results but above
Table 11: Results by case type. DAG advantage holds                      Flat Step (FDRec 0.64, RCA 0.35 on the same sub-
on both subsets.                                                         set). Degradation concentrates in retry-loop traces;
dynamic branching traces show smaller degrada-                         L   Regression Case Studies
tion (FDRec 0.85).
                                                                       Three illustrative cases from the pilot: (1) A prompt
                                                                       template update for CS-Agent replaced a structured
I     Judge Model Sensitivity                                          instruction with a free-form variant. AGENT E VAL
                                                                       flagged a drop in PARAM G EN quality for account-
                                                                       lookup (p < 0.01, FDRec dropped 12 pp), which
    Judge Model           FDRec       FPR      HA (κ)         RCA
                                                                       propagated downstream. The team reverted within
    GPT-4o                     .89    .07         .84         .72      hours. (2) DA-Agent’s SQL generation degraded
    Claude 3.5 Sonnet          .87    .09         .81         .69
    GPT-4o-mini                .83    .11         .77         .65      after an LLM provider-side update; AGENT E VAL
    Llama 3 70B                .80    .13         .73         .61      localized the regression to code generation steps,
                                                                       enabling a targeted fix. (3) A DP-Agent schema
Table 14: Judge sensitivity. DAG advantage over Flat                   change improved average-case performance by
Step remains significant (p < 0.01) for all judges.
                                                                       2 pp but degraded long-document handling by
                                                                       11 pp, detected only by the edge-case tier of pro-
J     Agent–Judge Independence                                         gressive evaluation.

                                                                       M    Deployment Methodology Details
Workflow                Judge                 FDRec HA RCA             Baseline: Self-reported surveys from 12 engineers
CS (Claude agent)
                  GPT-4o                       .92      .86    .75     covering 47 incidents before adoption. Median:
                  Claude 3.5 Sonnet            .90      .83    .73     4.2 hours; P25: 1.8 hours; P75: 8.5 hours; P90: 14
                        GPT-4o                 .88      .85    .78     hours. Self-reports may overestimate (recall bias)
DA (Claude agent)
                        Claude 3.5 Sonnet      .86      .82    .75
                                                                       and capture total time including communication
                        GPT-4o                 .86      .81    .64     overhead.
DP (Llama agent)
                        Claude 3.5 Sonnet      .85      .80    .63
                                                                          With AGENT E VAL: System-logged times from
Table 15: Same-family judging produces comparable or                   156 events. Median: 22 minutes; P25: 8 minutes;
lower scores, ruling out self-evaluation inflation.                    P75: 48 minutes; P90: 1.6 hours. Logged times
                                                                       capture alert-to-first-code-change interval and may
                                                                       underestimate by excluding initial investigation.
K      Architecture Scope Details                                         Both measurements consistently show substan-
                                                                       tial improvement across all three teams, but the
To characterize the practical boundary of DAG-
                                                                       exact magnitude should be interpreted with cau-
based evaluation, we simulate increasing non-DAG
                                                                       tion given measurement asymmetry and confounds
rates by randomly converting DAG traces to non-
                                                                       (failure severity, Hawthorne effects, concurrent im-
DAG (loop/branch) structures. At 30% non-DAG
                                                                       provements).
rate, FDRec remains 0.83 and RCA 0.63; at 50%,
                                                                          Additional deployment impact: For DA-Agent,
FDRec is 0.78 and RCA 0.55, still above flat evalu-
                                                                       taxonomy-guided analysis identified “parameter
ation but with diminished advantage. The practical
                                                                       hallucination” (syntactically valid but semantically
boundary is approximately 60% non-DAG rate, be-
                                                                       incorrect SQL WHERE clauses) as 31% of execu-
yond which the DAG advantage becomes marginal
                                                                       tion failures. Targeted few-shot examples reduced
(<5 pp). AGENT E VAL is most valuable for se-
                                                                       DA-Agent’s parameter error rate from 27% to 11%.
quential and moderately-branching architectures,
                                                                          Onboarding a new workflow requires ∼20–30
which represent the majority of current production
                                                                       person-hours. Same-domain workflows require
deployments (Table 16).
                                                                       less (∼12–18 hrs) through partial reuse. Prelim-
                                                                       inary experiments suggest GPT-4o-assisted DAG
Architecture Class               Est. Non-DAG %          Source
                                                                       schema proposals reduce setup time by approxi-
Sequential tool-calling               8–15%          Internal agents
Moderate branching                   20–30%             τ -bench       mately 40%.
SWE agents (edit-test loops)         25–35%           SWE-bench
Multi-agent collaboration            40–60%            Estimated†      N    Deployment Lessons Learned
Tree-of-thought / LATS               60–80%            Estimated†
                                                                       Five insights from deployment:
Table 16: Estimated non-DAG trace rates. † Based on                      First, taxonomy-first design is essential. After
architectural analysis, not empirically validated.                     the first month, 34% of CS-Agent failures were
“parameter hallucination” errors not captured by         P     Threshold Sensitivity Analysis
initial metrics. Lesson: Start with failure modes,
not metrics.                                                 Threshold shift               FDRec   FPR   RCA
   Second, calibration is critical and brittle. Uncal-       θ − 0.5 (more sensitive)       .92    .14   .69
                                                             θ (default)                    .89    .07   .72
ibrated judges showed 15% lower agreement. Five
                                                             θ + 0.5 (more conservative)    .85    .04   .67
stratified anchors per metric was the minimum; ran-
dom anchors underperformed due to skewed score           Table 17: Sensitivity to uniform threshold perturbation
distributions.                                           (±0.5).

   Third, schema-defined and trace-inferred DAGs
                                                         Per-type thresholds: θP LAN = 3.0, θTOOL S EL = 3.0,
serve complementary purposes. Structural devia-
                                                         θPARAM G EN = 2.5, θE XEC = 3.0, θS YNTH = 3.0, se-
tion proved a useful quality signal: deviant traces
                                                         lected by grid search on a held-out 52-trace subset.
were associated with 2.1× higher failure rates.
                                                         PARAM G EN thresholds are most sensitive: ±0.5
  Fourth, progressive evaluation changes behavior.       shifts FDRec by ±4 pp, compared to ±2 pp for
Teams that adopted smoke tests ran 3.4× more             other types.
evaluation cycles per sprint.
                                                         Aggregation Function. The workflow-level
  Fifth, taxonomy maintenance is a sociotechni-          score is the weighted harmonic mean:
cal challenge. We added 3 subcategories during                          P
                                                                             wi
the pilot and adopted a “propose-discuss-merge”           Q(G) = P i                , wi = |desc(vi )|+1 (1)
                                                                       i wi /q(vi )
protocol for governance.
                                                         where desc(vi ) is the set of descendants of vi .

                                                         Q      Counterfactual Analysis
O    Extended Limitations                                To demonstrate counterfactual analysis, we replace
                                                         a CS-Agent root cause (v2 , tool selection) with the
                                                         gold-reference output and re-evaluate downstream.
Methodological Boundaries. Our evaluation                Scores improve: v3 from 2.1 to 4.6, v4 from 1.8 to
dataset is sourced from anonymized logs using pro-       4.3, v5 from 2.3 to 4.1. Across 30 sampled failing
duction tools and prompts but does not reflect full      traces, counterfactual analysis confirms AGENT E-
live-system complexity. The reported κ = 0.84            VAL -identified root causes in 87% of cases. This
reflects agreement against majority-voted refer-         measures the combined effect of error correction
ences; per-annotator agreement (κ = 0.78–0.86,           and judge sensitivity to improved context.
Table 18) provides a more conservative estimate.
The 150 human-annotated cases provide adequate           R      Systematic Disagreement Patterns
power for aggregate metrics but wide per-workflow
                                                         Analyzing 156 step evaluations where AGENT E-
CIs. Ground truth for internal evaluation was pro-
                                                         VAL disagrees with human majority vote: (1) par-
duced by experts separate from authors; τ -bench
                                                         tial correctness (43%): steps with partially correct
and SWE-bench annotations were produced by au-
                                                         output that humans rate leniently but the judge rates
thors with independent validation on a subset. Cost
                                                         strictly, especially S YNTH steps; (2) context sen-
analysis assumes January 2026 API pricing.
                                                         sitivity (31%): cases where human evaluators use
                                                         external knowledge not in the trace; (3) borderline
                                                         thresholds (26%): steps near the pass/fail boundary
Generalization Scope. Our taxonomy was de-               where judgments diverge by exactly 1 point.
rived from three workflow types and may not
                                                         S     Parsing Failure Analysis
cover other domains; cross-system evaluation sug-
gests 76% taxonomy coverage on out-of-domain             Of 21 total parsing failures (12 τ -bench + 9 SWE-
agents. We evaluate English-language workflows           bench): multi-agent handoffs without explicit de-
only. The 5-type step classification covers common       pendency (8 traces), unbounded loops exceeding
tool-calling patterns but may need extension for         the 5-iteration unrolling limit (7 traces), and deeply
specialized architectures.                               nested conditional branches (6 traces).
T     Error Propagation Statistics                                                        Human
                                                                                                                 AgentEval
                                                                                                                                              Total
                                                                                                     1       2      3    4             5

Across all 450 test cases, 847 total step-level fail-                                     1          71       8        2   0  0                  81
                                                                                          2          4       93       15   2  0                 114
ures: 312 (36.8%) root cause failures, 535 (63.2%)                                        3          0       11      112 23   0                 146
propagated failures. Average propagation chain                                            4          0        2       28 228 25                 283
length: 2.1 steps. Context loss failures have the                                         5          0        0        4  37 322                363
longest average chain (3.2 steps); API/tool failures                                      Total      75 114 161 290 347                         987
the shortest (1.4 steps).
                                                              Table 21: Confusion matrix (987 step evaluations). Bi-
                                                              nary pass/fail agreement (threshold 3.0) is 94.0%.
U     Per-Annotator Agreement
                                                              X                         DAG Example Figure

    Annotator Pair      κ (vs. AgentEval)     κ (pairwise)                                    Root Cause             Propagated            Propagated    Propagated

    Annotator 1 (CS)          0.86                 0.81        v1 : Plan                      v2 : ToolSel         v3 : ParamGen           v4 : Exec     v5 : Synth
    Annotator 2 (CS)          0.83                 0.78          q=4.5                            q=1.2                q=2.1                 q=1.8        q=2.3

    Annotator 3 (CS)          0.82                 0.77
    Annotator 4 (DA)          0.85                 0.80
    Annotator 5 (DA)          0.84                 0.79                                                           Error propagation chain (length = 3)

    Annotator 6 (DA)          0.81                 0.76
    Annotator 7 (DP)          0.80                 0.78       Figure 2: DAG-based evaluation of a CS-Agent work-
    Annotator 8 (DP)          0.78                 0.75       flow. A wrong tool selection at v2 (root cause, q = 1.2)
    Annotator 9 (DP)          0.79                 0.77
                                                              propagates through v3 –v5 .
             Table 18: Per-annotator agreement.
                                                              Y                         Failure Mode Distribution

V     Per-Metric Human Agreement                                                                          Planning      Execution       Integration
                                                                                        100
                                                               Failure proportion (%)




                                                                                         80
        Step Type       Metric                     κ                                     60
        P LAN           Completeness              0.78                                   40
        P LAN           Feasibility               0.81
        T OOL S EL      Selection accuracy        0.92                                   20
        T OOL S EL      Tool relevance            0.85                                    0
        PARAM G EN      Param. correctness        0.89                                            CS-Agent            DA-Agent               DP-Agent
        PARAM G EN      Param. completeness       0.87
        S YNTH          Faithfulness              0.80
                                                              Figure 3: Failure mode distribution across workflows.
        S YNTH          Completeness              0.76
        S YNTH          Coherence                 0.82
        Average                                   0.83

Table 19: Per-metric human agreement (single-judge
GPT-4o).


W      Score Distribution and Confusion
       Matrix


     Score              1     2       3       4          5
     Human (%)         8.2   11.5    14.8   28.7       36.8
     AgentEval (%)     7.6   11.5    16.3   29.4       35.2

Table 20: Score distribution across 150 human-
annotated cases (step-level).
