                                         Auditing and Decomposing Feedback-Driven Evolution in
                                         LLM Test Generation under the Oracle Problem
                                         YUNHAO LIANG, Chengdu Institute of Computer Applications, Chinese Academy of Sciences, China
                                         and University of Chinese Academy of Sciences, China
                                         CHENGGUANG GAN, Independent Researcher, Japan
                                         RUIXUAN YING, Institute of Multidisciplinary Research for Advanced Materials (IMRAM), Tohoku
                                         University, Japan
arXiv:2608.19626v1 [cs.SE] 20 Aug 2026




                                         HANJUN WEI, University of Chinese Academy of Sciences, China
                                         ZHE CUI, Chengdu Institute of Computer Applications, Chinese Academy of Sciences, China and University
                                         of Chinese Academy of Sciences, China
                                         SHIWEN NI, Artificial Intelligence Research Institute, Shenzhen University of Advanced Technology, China
                                         Execution feedback can make LLM test generation appear self-verifying even when generated inputs or
                                         outputs are invalid. A common shortcut executes each input on one accepted program and treats its output as
                                         ground truth, converting out-of-domain behavior into apparent fault detection and evolutionary progress.
                                            We audit this failure mode on 142 development, 114 locked external, and 138 held-out but qualification-
                                         amended tasks under two models, three seeds, and fault-cross-fitted real submissions. On external inputs
                                         where three accepted implementations agree, generated outputs match the panel only 27.79% and 50.12% of
                                         the time. A single reference inflates the apparent evolutionary gain by 9.46–14.85 percentage points; after
                                         audit, equal-budget independent resampling is 6.01–18.83 points better.
                                            We then compare a genuine three-round loop with a density-matched feedback placebo. External Real–
                                         Placebo contrasts are +0.13 and −0.50 points. An outcome-blind held-out follow-up, transparently amended
                                         from 20 to 18 faults after its original qualification gate stopped before model calls, yields +1.99 (95% CI
                                         [+0.08,+3.88]) and +0.28 points ([−1.41,+2.03]); neither meets the pre-specified equivalence or superiority
                                         rule within the amended cohort. Post-hoc matching of observed reference-valid yield changes them to −0.30
                                         and +0.78 points, both with zero-crossing intervals. The positive Qwen2.5 contrast is therefore not robust
                                         to usable-candidate opportunity. Because the external placebo is post hoc and held-out qualification was
                                         amended, RQ6 supplies diagnostic boundary evidence, not a pristine confirmation. A blinded human semantic
                                         audit conducted by two software engineering doctoral students jointly classifies 94.41% of panel-disconfirmed
                                         inputs as invalid but 3.60% as valid, making panel disagreement informative rather than semantic proof. We
                                         provide an audit-and-placebo protocol that separates verifier artifacts, interaction scaffolding, and grounded
                                         feedback credit.
                                         CCS Concepts: • Software and its engineering → Software testing and debugging.
                                         Additional Key Words and Phrases: LLM-based test generation, self-evolution, test oracle problem, differential
                                         testing, empirical software engineering

                                         1   Introduction
                                         Executable tests are attractive feedback for code models: they expose concrete failures and appear to
                                         turn generation into a verifiable objective. Recent systems use generated tests to rank programs [4],
                                         refine suites from execution feedback [3], or co-train code and test generators [13, 22]. Yet execution
                                         verifies a generated test only if its input is permitted by the natural-language specification and its
                                         expected output is correct. This is the test-oracle problem in a new feedback loop [2].
                                            Competitive-programming data offer a tempting shortcut: execute a generated input on one
                                         accepted program and treat its output as ground truth. That program may accept an out-of-domain
                                         input, fail on a valid corner case, or choose behavior the specification leaves undefined. Optimization
                                         can then reward tests that disagree with many wrong submissions for the wrong reason. The risk
                                         is amplified in self-evolution, where noisy feedback is repeatedly selected, distilled, or reinforced.

                                                                                               1
More search can discover more verifier-specific inputs and masquerade as learning unless the oracle
and the search budget are independently controlled.
   We audit this failure mode in natural-language-to-test generation. A model receives a problem
statement and up to three public examples and emits complete input–output tests. We compare
one call, one call plus six deterministic mutations, three independent calls with the same nine
candidate slots, and mutations of public inputs. A deterministically chosen accepted program builds
the initial oracle. Real faulty submissions are split so that one fold selects an archive and the other
evaluates it. Only after selection is frozen do the remaining accepted programs audit each selected
test; disconfirmed entries are removed without replacement.
   We also evaluate a genuine three-round loop. Later rounds receive prior inputs and opaque iden-
tifiers for search-fold faults detected or remaining, never held-out behavior. Besides independent
resampling, we introduce a density-matched placebo that preserves the iterative prompt, history
size, detected-set cardinality, and kill-count density while randomizing the input–fault correspon-
dence. Real–Placebo therefore tests whether behavior-aligned feedback adds value beyond iterative
scaffolding and coarse progress.
   The study covers 142 development tasks, a procedure-locked 114-task TestCase-Eval cohort [24],
and a 138-task held-out but qualification-amended follow-up, under two models and three seeds. It
further decomposes 2,836 real faults and conducts a blinded, stratified human semantic audit of 300
panel-disconfirmed inputs with two software engineering doctoral reviewers. Tasks, not individual
tests or executions, are the unit of inference.
   Single-reference evaluation inflates the estimated evolution gain by 9.46–14.85 pp. After audit,
equal-budget resampling is 6.01–18.83 pp better than mutation-based evolution in every model–
cohort condition. In the three-round study, the large model-dependent Plain–iterative shifts are
almost reproduced by the placebo. On the held-out qualification-amended cohort, Real–Placebo is
+1.99 pp (95% CI [+0.08,+3.88]) and +0.28 pp ([−1.41,+2.03]); neither meets the frozen equivalence
or practical- superiority rule. Yield-matched replay changes the contrasts to −0.30 and +0.78 pp, both
with zero-crossing intervals. Fine-grained feedback credit is therefore unresolved, not established
absent. The semantic audit jointly judges 94.41% of panel-disconfirmed inputs invalid but 3.60%
valid, so panel disagreement remains evidence rather than semantic proof.
   This paper contributes:
      • Oracle-induced gain inflation and a freeze-then-audit protocol using independently submitted
        accepted implementations.
      • Candidate-budget-matched, fault-cross-fitted experiments on 394 tasks, including a three-
        round execution-feedback loop under strict external execution isolation.
      • A density-matched feedback placebo, an outcome-blind but qualification-amended held-out
        follow-up, and an explicit evidence-status account separating interaction scaffolding from
        behavior-aligned attribution.
      • Mechanism evidence from 2,836 real faults and a hash-locked human semantic audit of 300
        stratified inputs, together with task-level evidence for independent reconstruction.
  The contribution is diagnostic rather than a new generator: feedback validity, equal-budget
search, and a suitable placebo must be established before a gain can be attributed to evolution or
execution feedback.

2     Background and Problem Formulation
2.1    Tests as feedback
For a programming task 𝑞, let 𝑆𝑞+ denote independently submitted programs that are accepted by
the benchmark and 𝑆𝑞− denote historical programs with wrong verdicts. A generated test 𝑡 = (𝑥, 𝑦)

                                                  2
contains an input 𝑥 and an expected output 𝑦. A suite is useful only if it accepts specification-
conforming programs and rejects faulty ones. Because membership in 𝑆𝑞+ is a platform verdict
rather than a proof, the following fidelity is operational with respect to the accepted-program panel.
We use the conventional fidelity and fault-detection quantities
                                                 1 ∑︁
                                  Fid𝑞 (𝑇 ) = +          1[𝑠 passes 𝑇 ],                           (1)
                                               |𝑆𝑞 |   +
                                                    𝑠 ∈𝑆𝑞
                                               1 ∑︁
                                 Kill𝑞 (𝑇 ) = −           1[𝑠 fails 𝑇 ].                            (2)
                                             |𝑆𝑞 | 𝑠 ∈𝑆 −
                                                         𝑞


The accepted-panel rejection rate is 1 − Fid𝑞 (𝑇 ). Kill rate is meaningless without fidelity because
an arbitrary expected output can reject every program. Unlike mutation testing [11], our faults are
real historical submissions.

2.2   Three notions of oracle validity
We separate three checks that are often conflated.
   Direct model oracle. For model output (𝑥, 𝑦𝑚 ), 𝑥 is panel-admissible when every available 𝑠 ∈ 𝑆𝑞+
completes and their normalized outputs agree on 𝑦𝐴 (𝑥). A direct oracle match is 𝑦𝑚 = 𝑦𝐴 (𝑥). This
post-generation diagnostic never affects selection and measures panel agreement, not semantic
truth.
  Single-reference oracle. A source hash selects 𝑟𝑞 ∈ 𝑆𝑞+ before generation. If 𝑟𝑞 (𝑥) completes, the
primary verifier sets 𝑦𝑟 = 𝑟𝑞 (𝑥) and discards the generated output. This removes direct output
hallucination but does not validate 𝑥.
  Multi-implementation audit. After freezing the primary archive, every remaining 𝑆𝑞+ program runs
each selected input. A test is panel-confirmed only if all complete and agree with 𝑦𝑟 ; otherwise it is
audit-disconfirmed and removed without replacement. The label denotes differential disagreement,
not semantic falsity: accepted programs may contain or share latent defects.

2.3   Oracle-induced gain inflation
Let 𝐾1 (𝑀) be method 𝑀’s held-out kill under one reference and 𝐾𝐴 (𝑀) the score of the same frozen
archive after panel audit. For evolution 𝐸 and its one-shot parent 𝑂,
                          𝐼 (𝐸, 𝑂) = [𝐾1 (𝐸) − 𝐾1 (𝑂)] − [𝐾𝐴 (𝐸) − 𝐾𝐴 (𝑂)].                         (3)
Positive 𝐼 is gain that does not survive audit. Comparing 𝐸 with equal-slot resampling 𝑅 under 𝐾𝐴
separates the operator from additional search.

2.4   Attributing value to execution feedback
A multi-round interface also adds an iterative prompt, history, and coarse progress. Real feedback
maps each input to the search faults it detects; placebo feedback preserves interaction structure and
density but destroys that mapping. For audited real and placebo scores 𝐾𝐴 (𝐹 ) and 𝐾𝐴 (𝑃),
                                      𝐴(𝐹, 𝑃) = 𝐾𝐴 (𝐹 ) − 𝐾𝐴 (𝑃)                                    (4)
measures aligned attribution. The placebo retains aggregate progress. Its contrast with resampling
therefore mixes scaffolding and coarse feedback. A zero-crossing interval detects no benefit but
does not establish equivalence.

                                                     3
                      Table 1. Cohorts are analyzed separately. Counts are per task.

          Cohort               Tasks   Accepted    Faulty   Seeds   Role
          Development IID         63       9–10     ≤ 20        3   Development
          Development OOD         79       3–10     ≤ 20        3   Development
          External               114          3       20        3   Procedure-locked evaluation
          Held-out E16-B         138          3       18        3   Qualification-amended



2.5    Scope of “evolution”
Self-evolving systems can change weights, memory, tools, or artifacts [7]. We study artifact-level
evolution: deterministic candidate mutation and a three-round loop in which search-fold outcomes
affect later prompts. This stage could supply data or reward to later training, but we do not claim
parameter-level self-improvement.

3     Study Design
We ask six questions: RQ1, how often model-generated outputs agree with the accepted-program
panel; RQ2, how much one reference inflates evolution gains; RQ3, whether audited evolution
beats one shot or equal-slot resampling; RQ4, which fault families concentrate disconfirmed
detections and whether rankings are robust; RQ5, whether blinded judgments support the invalid-
input mechanism; and RQ6, what incremental value behavior-aligned feedback shows beyond a
density-matched iterative placebo under exposed and qualification-amended cohorts.

3.1    Tasks and model conditions
Table 1 summarizes three non-pooled cohorts. Development uses 142 exact-output CodeContests-
family tasks previously exposed during method development. The external cohort was hash-
locked before fresh generation from TestCase-Eval [24]: 114 non-interactive tasks with a complete
statement, public examples, three accepted Python programs passing those examples, and 20
nonoverlapping faulty programs. The held-out cohort comes from a 200-task CodeContests test
bundle closed during earlier studies. Its frozen gate required 20 faults and at least 40 tasks per source,
but stopped before model calls because only 36 OOD tasks qualified. A separately frozen, outcome-
blind amendment changed only the fault panel and folds from 20/10–10 to 18/9–9, retaining 71 IID
and 67 OOD tasks. We report this cohort as qualification-amended, not pristine; the complete flow
is in the supplemental material. Python and exact-output tasks provide common, resource-limited
execution semantics and avoid special-checker ambiguity.
   The RQ6 evidence has deliberately different status across phases (Table 2). “Locked” therefore
refers to the stated procedure or decision rule, not automatically to a pristine confirmatory sample.
   The first model condition is a Qwen2.5-Coder-7B Instruct checkpoint [10] merged with a fixed
warm start (49 records, 33 tasks, LoRA rank 8, three epochs). The second is the released Qwen3.5-9B
checkpoint with thinking disabled [19]. They test replication, not a causal scale effect. For seeds
42–44, each receives the same statement and up to three public examples and returns at most three
strict JSONL tests. Generation uses temperature 0.7, top-𝑝 0.8, top-𝑘 20, repetition penalty 1.1, a
1,024-token completion limit, and a 4,096-token context.

3.2    Candidates, cross-fitting, and auditing
All primary branches share the first call (Table 3). One-shot retains its at-most-three parsed inputs.
Evolve adds six deterministic mutations without observing fault outcomes. Matched adds two calls

                                                    4
Table 2. RQ6 evidence status. No single phase is treated as a pristine confirmation of the fine-grained feedback
effect.

 Study     Timing and cohort                 Departure from a pristine test    Evidential role
 E14       Procedure locked before           Cohort already exposed            Prospective extension
           generation on exposed
           External tasks
 E15       Constructed after E14 on the      Post-hoc placebo                  Diagnostic control
           same tasks
 E16-A     Gate locked before opening        Qualification failed; no model    Stopped before generation
           200 held-out tasks                calls
 E16-B     Frozen before model outcomes      Fault threshold amended after     Outcome-blind boundary
                                             supply was observed               evidence
 Replay    Constructed after E16-B           Conditions on observed            Sensitivity analysis
           outcomes                          candidate yield


                                 Table 3. Per-task-repeat candidate budgets.

                          Variant          Calls   Slots   Additional candidates
                          One-shot             1      3    None
                          Evolve               1      9    6 deterministic mutations
                          Matched              3      9    2 independent calls
                          Public evolve        0      9    9 public-input mutations


under the identical prompt. Public evolution applies nine mutations to public inputs and uses no
model call. Failed mutations are not resampled, and every archive contains at most three tests.
   Generated outputs are used only for RQ1. For selection, a minimum-source-hash accepted
program executes each unique input and supplies its expected output; failures are rejected. A
content hash splits faults into balanced folds. In each direction, greedy selection covers one search
fold, while the other fold evaluates the at-most-three-test archive; the roles then swap.
   The archive is frozen before the other accepted programs execute its inputs. An entry is removed
without replacement if any auditor fails or disagrees. Thus single-reference and audited scores
describe the same selected archive. The primary outcome is task-macro held-out constrained kill.
Secondary outcomes are whether any held-out fault is detected and whether any test survives
audit. We call the latter audited task coverage; it is the fraction of tasks retaining a valid test, not
source-code line or branch coverage. Seeds are averaged within task before inference.

3.3    Real and placebo feedback
RQ6 compares three-call-per-direction interventions. Real feedback starts from the shared first call;
each of two later rounds sees bounded prior inputs, opaque identifiers for search faults detected per
input, and remaining search fault identifiers. It never sees sources, outputs, stack traces, held-out
behavior, or audit outcomes. The placebo uses the same template, rounds, history size, detected-set
cardinality, and multiset of the two largest per-input kill counts, but randomly reassigns history
inputs and fault identifiers. Independent resampling is the no-feedback baseline.
   E14 locked the real procedure on the already exposed external cohort; E15’s placebo was designed
after E14 and is post hoc. E16-B generated Plain, Real, and Placebo afresh on 138 held-out tasks. Per
task-repeat, Plain uses three calls; Real and Placebo each share round zero across directions and use

                                                       5
four direction-specific follow-ups. Real and Placebo are therefore matched in both calls and slots,
whereas Plain is slot- but not unique-call-matched. Across both models E16-B required 9,108 calls.
   Nominal slots can fail parsing, duplicate an input, or fail reference execution. After the frozen
analysis, an off-policy replay retained, within every task, seed, direction, and round, the earliest
equal number of reference-valid Real and Placebo candidates and repeated selection and audit. A
stricter diagnostic matched confirmed and disconfirmed yields separately. These post-treatment
analyses test sensitivity to usable opportunity; they are not counterfactual reruns because later
generations retain their original histories.

3.4    Mechanism and semantic sensitivity
For RQ4, each of 2,836 development faults is assigned one mutually exclusive, execution-grounded
trigger phenotype: public example, official exact-output anchor, safe local mutation family, unsafe-
public-mutation only, or hard residual. The categories identify triggers, not source-level causes.
Anchors are re-executed across accepted programs and family intervals remain exploratory.
   RQ5 samples 300 of 1,110 deduplicated, selected, reference-executable but panel-disconfirmed
inputs using locked strata (150 development, 150 external; construction and disagreement-mode
weights). Two software engineering doctoral students independently review each case using the
statement, public examples, and candidate input. They are blinded to task identity, generation
method, archived output, program behavior, fault detections, panel outcome, and the other re-
viewer’s judgment. Each chooses one of five labels: valid, out of domain, malformed, ambiguous, or
insufficient information. For a valid input, the reviewer also independently derives an expected out-
put. We report exact inter-rater agreement and Cohen’s 𝜅 [6], with design-weighted estimates and
10,000 within-stratum bootstraps. These are structured human judgments, not definitive semantic
ground truth. A 67-case packet (all reviewer disagreements and jointly valid cases plus consensus
quality controls) is reserved for consensus or third-reviewer specification adjudication.

3.5    Inference and integrity
Primary contrasts use paired task-level nonparametric bootstraps with 20,000 resamples and 95%
intervals. External gates were frozen: gain inflation must have a positive lower bound, and audited
Evolve–Matched must have an upper bound no greater than +2 pp. E15 had no equivalence margin,
so zero-crossing intervals mean no detectable incremental effect, not equivalence. E16-B pre-
specified ±2 pp as the smallest effect of interest: equivalence requires the whole interval inside that
range, superiority a lower endpoint above +2 pp, and inferiority an upper endpoint below −2 pp,
separately for both models.
   External programs run in bubblewrap namespaces with time, memory, process, and output limits;
unsafe fallback is forbidden. The older development runner saved limits and counts but lacks
equivalent per-row isolation attestations. Model artifacts, cohorts, folds, generated rows, analyses,
and paper summaries are linked by SHA-256 locks. The failed E16-A gate and E16-B amendment
are separately signed.

4     Results
4.1    RQ1: Direct expected outputs remain unreliable
Table 4 evaluates only generated inputs on which all available benchmark-accepted implementations
execute and agree. Even under that favorable conditioning, the model-proposed expected output
matches the panel for 44.16% of admissible development inputs in the Qwen2.5-Coder-7B condition
and 58.90% in the Qwen3.5-9B condition. The prospectively locked external rates are lower: 27.79%

                                                  6
Table 4. Direct-oracle reliability. “Admissible” counts tasks with at least one panel-admissible input. Rates
and 95% CIs are task-level bootstrap estimates.


               Cohort                                           Model           Tasks         Admissible                                       Matches panel (%)                 Panel-confirmed suite (%)
               Development                                      Qwen2.5            142                   138                                   44.16 [39.65, 48.80]              4.77 [3.36, 6.34]
               Development                                      Qwen3.5            142                   137                                   58.90 [54.82, 62.88]              11.50 [8.92, 14.16]
               External                                         Qwen2.5            114                   112                                   27.79 [22.93, 32.89]              2.53 [1.27, 4.09]
               External                                         Qwen3.5            114                    93                                   50.12 [43.81, 56.43]              5.07 [3.31, 7.02]

                                                       (a) Model-output agreement with accepted panel                                                      (b) Gain attenuation under accepted-panel audit
                                                                                                                                               20.0%
                                       70%                                                                                                                Single reference
                                                                                                                                                          Accepted-panel audit
Conditional accepted-panel agreement




                                       60%
                                                                                                                                               15.0%
                                                                                                                   Legacy gain over one-shot
                                       50%

                                                                                                                                               10.0%
                                       40%


                                       30%                                                                                                      5.0%



                                       20%
                                                                                                                                                0.0%

                                       10%

                                                                                                                                               −5.0%
                                       0%
                                               Dev                 Dev             External             External                                           Dev              Dev          External      External
                                             Qwen2.5             Qwen3.5           Qwen2.5              Qwen3.5                                          Qwen2.5          Qwen3.5        Qwen2.5       Qwen3.5




Fig. 1. Oracle quality and apparent-versus-audited evolution gains. Error bars are 95% task-bootstrap intervals;
cohorts are not pooled.

Table 5. Evolution minus one-shot held-out constrained kill before and after auditing the frozen archive. All
values are percentage points.


                  Cohort                                          Model             Apparent [95% CI]                                                  Audited [95% CI]                Inflation [95% CI]
                  Development                                     Qwen2.5           10.58 [8.41, 12.85]                                            −0.02 [−1.82, 1.80]                 10.60 [7.98, 13.47]
                  Development                                     Qwen3.5          13.38 [10.67, 16.39]                                            −1.47 [−3.74, 0.85]                14.85 [11.29, 18.60]
                  External                                        Qwen2.5           11.58 [8.71, 14.55]                                               2.12 [0.18, 4.09]                 9.46 [6.46, 12.76]
                  External                                        Qwen3.5           12.57 [9.46, 15.82]                                               2.18 [0.44, 4.08]                10.39 [7.24, 13.77]


(95% CI [22.93, 32.89]) and 50.12% [43.81, 56.43]. Requiring every test in a call to be panel-confirmed
is more demanding. Fully panel-confirmed suites occur in only 2.53% and 5.07% of external calls.
   The Qwen3.5-9B condition is consistently better, but its error rate remains too high for use as a
reward oracle. This is replication under a different fixed model, not evidence of a scaling law.

4.2                                          RQ2: One reference creates large apparent gains
Figure 1 contrasts the nominal single-reference gain of Evolve over One-shot with the gain remain-
ing after accepted-panel audit. On development, the apparent gains are 10.58 and 13.38 pp; the same
frozen archives yield −0.02 and −1.47 pp after audit. Externally, the apparent 11.58 and 12.57 pp
gains shrink to 2.12 and 2.18 pp. Consequently, estimated gain inflation is 9.46–14.85 pp across all
four conditions (Table 5), with every 95% interval strictly above zero.

                                                                                                                   7
Table 6. Accepted-panel-audited held-out constrained kill (%) and paired differences (percentage points).
“Public” mutates public examples and is a diagnostic rather than a call-matched model baseline.

 Cohort          Model      One-shot     Evolve    Matched    Public   Evolve–One           Evolve–Matched
 Development     Qwen2.5         20.43     20.41      39.24    42.39   −0.02 [−1.78,1.76]   −18.83 [−21.95,−15.78]
 Development     Qwen3.5         40.57     39.10      48.82    42.34   −1.47 [−3.79,0.83]   −9.72 [−12.44,−7.12]
 External        Qwen2.5         10.58     12.70      23.61    27.63   2.12 [0.18,4.08]     −10.91 [−14.91,−7.11]
 External        Qwen3.5         12.91     15.09      21.10    27.63   2.18 [0.45,4.08]     −6.01 [−9.15,−3.11]


Table 7. Selected fault-family results. Audit-disconfirmed share is the fraction of single-reference evolution
detections rejected by the accepted-program panel; it is not a semantic false-positive rate.

 Trigger phenotype                Faults (%)    Qwen2.5 audit-disconfirmed (%)    Qwen3.5 audit-disconfirmed (%)
 Public exposed                 1,180 (41.61)                             25.44                              17.35
 Official-oracle exposed          788 (27.79)                             43.26                              39.06
 Safe local mutation families     350 (12.34)                                —                                  —
 Unsafe-mutation only             320 (11.28)                             92.45                              84.52
 Hard residual                     198 (6.98)                             56.00                              44.12



  Adding only a second accepted implementation reduces apparent gains to 3.60–4.32 pp; three
reduce them to 1.11–2.38 pp. The full audit curves in the supplement show that most inflation is
detectable with one additional program.

4.3   RQ3: Auditing reverses the method ranking
Table 6 reports accepted-panel-audited held-out constrained kill. On development, Evolve is in-
distinguishable from or slightly below One-shot. On the external cohort it is 2.12–2.18 pp higher,
but this modest gain does not survive the equal-candidate-budget comparison. Matched exceeds
Evolve by 18.83 and 9.72 pp on development and by 10.91 and 6.01 pp externally; all four paired
intervals lie strictly below zero when expressed as Evolve minus Matched.
   Public-input mutation shows that in-domain seeds have potential, but its information source
and call cost differ. The conclusion concerns search quality at nine candidate slots, not token or
wall-clock efficiency.
   The external two-point Evolve gain over One-shot is metric-sensitive. Held-out task detection
changes by −1.02 pp for Qwen2.5 and +0.15 pp for Qwen3.5, with both intervals crossing zero.
Audited task coverage falls by 3.95 and 2.34 pp, respectively. The kill-rate gain does not broaden
audited task coverage, i.e., the fraction of tasks retaining a panel-confirmed test.

4.4   RQ4: Unsafe mutations concentrate audit-disconfirmed credit
Table 7 decomposes the 2,836 development faults. Public and official exact-output anchors already
expose 41.61% and 27.79%, respectively. Only 12.34% fall into the four safe local-mutation families
combined. A similarly sized 11.28% family is exposed only through public mutations that are
audit-disconfirmed by the accepted panel.
   The stronger condition reduces but does not eliminate disconfirmation. No family has a 95% lower
bound above zero for Evolve versus Matched in both models; the largest exploratory exception also
crosses zero. No stable subgroup reverses the ranking.
   The robustness appendix repeats the paired comparisons for each seed and for held-out kill,
task detection, and audited task coverage. All 12 model–cohort–seed gain-inflation intervals have

                                                         8
Table 8. Blinded human validity judgments for sampled audit-disconfirmed inputs. Rates are design-weighted;
only the overall row shows pre-specified stratified-bootstrap 95% CIs.

                 Group                  Sample 𝑛         Both invalid (%)    Both valid (%)
                 Overall                      300   94.41 [91.85, 96.51]    3.60 [2.23, 5.14]
                 Development                  150                  94.28                 4.89
                 External                     150                  94.61                 1.57
                 Native evolve                196                  96.25                 2.42
                 Matched resampling            50                  66.18                27.91
                 Public evolve                 50                  98.14                 0.00
                 One shot                       4                  75.00                25.00


positive lower bounds, and all 12 audited Evolve-minus-Matched intervals have negative upper
bounds. The same latter result holds for all 12 model–cohort–metric cells.

4.5   RQ5: Semantic review supports the dominant mechanism but preserves exceptions
The two blinded doctoral reviewers assign the same five-class label to 275 of 300 sampled inputs
(91.67%; inter-rater Cohen’s 𝜅 = .823). Collapsing the labels to valid versus other, they agree on
293 inputs (97.67%; 𝜅 = .825). Thus, 25 cases differ at the five-class level, but only seven cross the
valid–invalid boundary; the remaining disagreements concern the two invalidity subtypes.
   Both reviewers classify 275 inputs as invalid and 18 as valid; seven cross the valid–invalid
boundary. For jointly valid cases, derived outputs support the primary output in 13, an auditor
output in one, and neither unambiguously in four. Relaxed limits restore panel agreement in
three cases and fail to reproduce one primary output. These exceptions preclude treating panel
disagreement as semantic truth.
   Table 8 reports population estimates recovered using the locked sampling design. Overall, 94.41%
(95% stratified-bootstrap CI [91.85, 96.51]) are jointly judged invalid, while 3.60% [2.23, 5.14] are
jointly judged valid. Weighting sampled inputs by their held-out kill links gives the same qualitative
result: 94.91% [91.12, 97.62] invalid and 2.77% [1.34, 4.54] valid. Development and external estimates
are similar. The matched-resampling subgroup has a substantially larger jointly valid estimate than
native or public mutation, although this post-hoc subgroup comparison is descriptive and not a
method-selection result.
   The 67-case follow-up packet contains all inter-rater disagreements and jointly valid cases
plus consensus quality controls. It is a targeted adjudication set, not an error count; the reported
estimates do not force consensus or include a third-reviewer resolution.

4.6   RQ6: Available evidence does not isolate a robust aligned-feedback benefit
Table 9 separates the observed effect of entering a three-round interaction from the incremental
effect of behavior-aligned execution feedback. Against plain equal-candidate-slot resampling, real
feedback decreases audited held-out kill by 6.11 pp in the Qwen2.5 condition, but increases it by
2.73 pp in the Qwen3.5 condition. Read alone, E14 would suggest a model-dependent benefit from
feedback.
   The placebo reproduces that direction and nearly the same magnitude: it changes kill by −6.24
and +3.23 pp. Real feedback exceeds placebo by only +0.13 pp (95% CI [−1.56, +1.80]) for Qwen2.5
and is −0.50 pp [−2.13, +1.08] lower for Qwen3.5. The cross-model interaction in this real-minus-
placebo contrast is −0.63 pp [−2.92, +1.70]. None of these aligned-feedback intervals excludes
zero.

                                                     9
Table 9. External accepted-panel-audited held-out constrained kill. Levels are percentages; contrasts and 95%
paired task-bootstrap CIs are percentage points. The placebo analysis is post hoc.


 Model         Plain     Placebo       Real    Placebo–Plain [95% CI]          Real–Placebo [95% CI]
 Qwen2.5       23.63        17.38     17.51    −6.24 [−8.64,−3.93]             +0.13 [−1.56,1.80]
 Qwen3.5       21.18        24.42     23.92    +3.23 [0.85,5.76]               −0.50 [−2.13,1.08]


Table 10. E16-B accepted-panel-audited held-out constrained kill. Levels are percentages; contrasts and 95%
paired task-bootstrap CIs are percentage points. “Inc.” denotes the frozen inconclusive decision.


 Model        Plain    Placebo    Real    Placebo–Plain [95% CI]      Real–Placebo [95% CI]      Decision
 Qwen2.5      42.42      31.03   33.01    −11.39 [−14.44,−8.48]       +1.99 [+0.08,+3.88]        Inc.
 Qwen3.5      49.91      54.37   54.66    +4.47 [+2.28,+6.74]         +0.28 [−1.41,+2.03]        Inc.


Table 11. Post-hoc E16-B candidate-yield-matched replay. Entries are accepted-panel-audited Real–Placebo
held-out kill in percentage points with 95% task-bootstrap CIs.

                   Replay                      Qwen2.5               Qwen3.5
                   Frozen original             +1.99 [+0.08,+3.88]   +0.28 [−1.41,+2.03]
                   Reference-valid matched     −0.30 [−0.90,+0.30]   +0.78 [−0.62,+2.19]
                   Safety-stratified matched   −0.35 [−0.91,+0.20]   +0.13 [−1.03,+1.23]



   The placebo is intentionally conservative: it retains detected-set size and the largest per-input
kill-count density while randomizing the input–fault mapping. Consequently, real minus placebo
isolates the observed value of fine-grained attribution, whereas placebo minus plain combines
prompt/history scaffolding with coarse progress signals. The result does not show that all execution
feedback is useless, nor do zero-crossing intervals prove equivalence. This is the E15 post-hoc
diagnostic; E16-B supplies an outcome-blind but qualification-amended held-out boundary check.
   Table 10 reports E16-B. Placebo–Plain is −11.39 pp for Qwen2.5 and +4.47 pp for Qwen3.5. Real–
Placebo is much smaller: +1.99 pp [+0.08,+3.88] and +0.28 pp [−1.41,+2.03], respectively. The first
interval fails the frozen superiority threshold, and the second misses the equivalence boundary
by 0.03 pp. Both model-specific decisions are inconclusive; the amended cohort therefore neither
establishes equivalence nor a practically important advantage. The cross-model contrast is also
unresolved (−1.70 pp, 95% CI [−4.09,+0.67]).
   Source-interaction and secondary-outcome intervals cross zero (supplemental material). Per
direction-round, Qwen2.5 yields 0.837 confirmed Real candidates and 0.794 Placebo candidates.
Qwen3.5 is nearly matched at 1.874 and 1.882. Equal slots therefore do not guarantee equal usable
opportunity.
   Table 11 reports the post-hoc replay. Reference-valid matching changes the two contrasts to −0.30
and +0.78 pp; safety-stratified matching gives −0.35 and +0.13 pp. All intervals in the table cross
zero. Because truncation is post-treatment and later rounds retain original histories, this shows
non-robustness rather than a direct effect. In combination, E15 and E16-B narrow the plausible
claim but do not constitute a clean confirmatory test of feedback efficacy or ineffectiveness.

                                                     10
5     Discussion
5.1     Execution is conditional verification
Execution verifies a test only relative to a valid input domain and an adequate oracle. One accepted
program supplies neither. It can produce an output outside the specification, turning disagreement
with historical programs into apparent fault detection. Repeated optimization can then convert
this artifact into training data or reward. Better output generation does not remove the risk: larger
search can still find inputs on which the reference is permissive or idiosyncratic.
   The semantic audit triangulates this mechanism. Two blinded software engineering doctoral
reviewers jointly classify 94.41% of sampled panel-disconfirmed inputs as invalid, but 3.60% as valid
and one valid case supports an auditor-side output. Shared interpretation bias and reviewer error
remain possible. Panel execution is therefore a conservative consistency filter, not semantic ground
truth.

5.2     An iterative loop is not a feedback effect
Real feedback appears to hurt Qwen2.5 and help Qwen3.5 relative to resampling, but the density-
matched placebo reproduces both directions. On the amended held-out cohort, the Real–Placebo
contrast remains inconclusive under the pre-specified ±2 pp rule, and the Qwen2.5 contrast dis-
appears after equalizing observed valid yield. The stronger condition follows the richer interface
more reliably; the weaker one loses candidates through format failures.
  This does not show that execution feedback is universally useless. The placebo retains aggregate
progress and removes only fine-grained input–fault alignment. The supported conclusion is nar-
rower: scaffolding or coarse progress explains the dominant model-dependent shift observed on
the exposed external cohort, while the residual value of aligned attribution remains unresolved and
opportunity-sensitive. E15 is post hoc and E16-B changes qualification after seeing task supply;
together they provide triangulated diagnostic evidence, not confirmation that aligned feedback has
zero effect.

5.3     Evaluation safeguards
Future feedback-driven test studies should apply the following controls:

      (1) Freeze, then audit. Differentially execute selected tests on at least two independent
          accepted programs and remove disconfirmed entries without replacement. Report an audit-
          aware method separately if desired.
      (2) Match search and feedback interfaces. Compare evolution with independent generation
          at equal candidate slots, report call and execution costs, and add a placebo that preserves
          history and coarse feedback while breaking the claimed behavior alignment.
      (3) Separate selection from evaluation. Cross-fit real faulty programs, use tasks as the unit
          of inference, and report kill, task detection, audited task coverage, parse yield, and oracle
          accuracy together; distinguish this task-level validity yield from line or branch coverage.
      (4) Adjudicate disagreements. Resolve panel disagreement against the natural-language
          contract using executable constraints, bounded brute-force oracles, resource-limit replay,
          or independent human review; never equate disagreement with a false test by definition.

   These controls complement industrial pipelines that admit tests only after build, pass, reliability,
and coverage checks [1]. In natural-language-only algorithmic tasks, however, no trusted project
test suite serves as a final oracle.

                                                   11
5.4    Implications for self-evolving tests
Feedback-driven generation remains promising when search stays inside a defensible contract. One
direction is relational evolution: transform a public example under an executable precondition and
verify a metamorphic output relation [20]. Historical execution can then choose or rank supported
relations instead of overriding hard validity failures. This is future work, not a result of the present
study.
   The sampled disconfirmed population also suggests optimizing admissible hard-case yield rather
than raw disagreement. Jointly valid estimates are 27.91% for matched resampling, 2.42% for native
evolution, and 0% for public evolution, although these post-hoc subgroups are descriptive. A
prospective study should lock this objective and validate it with executable contracts before any
parameter update.

5.5    Cost and reproducibility
The four primary model–cohort conditions used 4,608 model calls and 555,610 unique program–
input executions. E14/E15 added 5,472 calls and 190,695 executions; E16-B added 9,108 calls and
197,642 executions. Two accepted programs capture most of the ranking change, so audits can
remain an offline evaluation standard rather than a deployment-time cost. Hash-locked manifests
and task-level rows allow alternative analyses without rerunning untrusted programs.
  Persistent model updates are meaningful only if their gains survive independent measurement.
Our contribution is therefore an audit and attribution protocol, not a new optimizer: establish a
deployable oracle contract and isolate the information in feedback before comparing SFT, preference
optimization, or reinforcement-learning updates.

6     Related Work
6.1    LLM-based test generation
LLMs generate tests for ranking code, improving structural coverage, and repairing existing suites.
CodeT ranks generated programs by agreement with generated tests [4]. CodaMOSA invokes a code
model when search-based generation reaches a coverage plateau [14], and CoverUp iteratively feeds
Python coverage gaps back to an LLM [18]. TestGen-LLM improves existing tests subject to build,
pass, reliability, and coverage filters [1]; IntUT makes test intentions explicit for industrial Java
projects [17]. These systems primarily study executable repository tests and structural adequacy;
broader evaluations find strong sensitivity to model, prompt, and project choices [23]. Their results
also show why validity cannot be reduced to coverage: data filtering materially affects both coverage
and bug detection [25].
   Algorithmic benchmarks instead make solution discrimination explicit. TestCase-Eval pairs 500
tasks with over 100,000 human submissions to measure fault coverage and targeted exposure [24];
we use a conservatively filtered Python exact-output subset. CodeContests-O iteratively refines tests
using execution on correct and incorrect solutions and optimizes fidelity and discriminability [3].
Our question is not whether an LLM can produce executable or discriminating tests, but whether a
reported improvement survives an oracle audit conducted only after selection and a comparison
with equal search opportunity.

6.2    Iterative feedback and self-evolution
Test-time refinement can improve outputs without weight updates. Self-Refine uses a model as
generator, critic, and refiner [15]; Reflexion stores verbal feedback from environmental trials [21];
and Self-Debugging conditions code revision on execution and explanation [5]. Conversely, con-
trolled reasoning experiments show that intrinsic self-correction can stagnate or degrade without

                                                   12
    Table 12. Positioning against representative adjacent work by objective and methodological emphasis.

 Work                      Setting                    Primary signal or           Main methodological
                                                      objective                   emphasis
 CodaMOSA / CoverUp        Repository tests           Structural coverage         Coverage-guided
                                                                                  generation
 Doc2OracLL                Java tests                 Documentation-              Oracle generation
                                                      grounded assertions         quality
 CodeContests-O            Algorithmic tasks          Fidelity and                Iterative test refinement
                                                      discriminability
 CURE / UTRL               Code-model training        Coder–tester reward         Persistent co-evolution
 This work                 Algorithmic tasks          Cross-fit real-fault kill   Post-selection audit,
                                                      after audit                 equal-slot control, and
                                                                                  feedback placebo



external feedback [9]. These findings motivate separating the effect of another interaction round
from the effect of grounded feedback content.
   Persistent adaptation raises the same attribution problem. Self-adapting language models generate
data and update directives [26]; surveys classify self-evolving agents by the component and timing
of adaptation [7]. In code, CURE co-evolves coder and tester without ground-truth solutions [22],
and UTRL adversarially trains unit- test and code generators [13]. Such methods make generated
tests part of a learning signal. Our study examines two prerequisites for crediting that signal: an
independently defensible oracle and a control that preserves interaction structure while breaking
the claimed behavior alignment.

6.3    Test-oracle validity and adequacy
The oracle problem asks how to decide whether observed behavior is correct [2]. Recent LLM
studies expose this as a distinct bottleneck. Doc2OracLL studies how API documentation affects
generated Java test oracles [8]; Konstantinou et al. ask whether generated oracles encode actual
rather than expected behavior [12]; and Molinelli et al. evaluate oracle usefulness on projects
created after likely training cutoffs [16]. These works evaluate assertions or expected behavior.
We study a complementary failure: an execution-derived oracle can be internally consistent yet
semantically unsafe because its input lies outside the natural-language contract.
   Differential implementations, formal contracts, and metamorphic relations can reduce depen-
dence on one absolute oracle [20]. Mutation testing measures whether suites distinguish seeded
faulty variants [11]; we instead cross-fit real historical faults so that selection and measurement
use disjoint fault folds. Agreement among accepted implementations remains a benchmark-specific
empirical oracle, not proof of specification conformance, which motivates the separate human
semantic audit.
   Accordingly, our contribution is neither a new generator nor another benchmark. It connects
three controls that adjacent work usually studies separately: freeze-then oracle audit, candidate-
budget matching, and a matched placebo for the feedback interface. The resulting protocol tests
whether apparent self-evolution reflects better tests, more search, or exploitation of the evaluator.

7     Threats to Validity
  Construct validity. Accepted-program agreement is stronger than one-reference execution but
does not prove that an input conforms to natural language. Accepted programs can contain or

                                                     13
share defects, and legal outputs may have multiple textual forms. We restrict the study to exact-
output tasks and normalize whitespace, but do not generalize to special checkers or floating-point
tolerance. Trigger phenotypes are execution-grounded categories, not source-level causes. The
human semantic audit is also not definitive ground truth: the two doctoral reviewers may share
training and interpretation biases, and neither used the allowed ambiguity labels. The 67-case
packet therefore remains for consensus or third-reviewer specification adjudication.
   The placebo preserves iterative structure, history size, detected-set cardinality, and leading
kill-count density. It does not remove all coarse feedback, nor exactly match prompt tokens. Real–
Placebo consequently estimates fine-grained input–fault attribution only, not the value of every
execution signal.
   Internal validity. Development tasks were exposed and the family analysis is post hoc. The
locked external study fixes tasks, models, budgets, folds, hypotheses, and analyses before fresh
generation, and archives are selected before auditor execution. Recorded infrastructure and provider
amendments preserve generated responses but can still affect execution or judgment behavior. E14
uses an already exposed cohort; E15 was designed after E14 and remains exploratory.
   E16-A froze before opening its 200 held-out tasks but failed its 20-fault gate. E16-B changed the
fault panel to 18 after observing qualification supply, before model outcomes. It is outcome-blind
but qualification-amended. Included tasks have more exact-compatible accepted programs than
excluded tasks, and no outcomes exist for excluded tasks, so profile analyses cannot eliminate
selection bias. Consequently, E16-B’s frozen analysis rules do not restore the evidential status of
the failed E16-A design, and RQ6 is not presented as a clean confirmatory experiment.
   Statistical conclusion validity. Tests and executions are dependent within task; we average seeds
within task and bootstrap paired tasks. Cohorts are not pooled, and exploratory family tests are not
multiplicity-corrected. Intervals describe the observed task populations, not arbitrary domains or
models. E15 lacked a smallest effect of interest, so zero-crossing intervals do not prove equivalence.
E16-B specified ±2 pp but neither model satisfies the frozen equivalence or superiority rule. Source
interactions cross zero. Yield-matched replay conditions on a post-treatment mediator and cannot
regenerate later rounds, so it demonstrates non-robustness, not a causal decomposition.
   External validity. All tasks are algorithmic, all executed submissions are Python-family, and
TestCase-Eval is a new source rather than a new application domain. Both model conditions are
from the Qwen family and differ in checkpoint provenance and warm start, so they neither establish
cross-family generality nor identify a scale effect. A size-matched code-instruction model from
an independent family is the highest-priority replication; repository tests, other languages, richer
checkers, and production systems also require study.
   Execution and reproducibility. External executions use strict namespace and resource-limit attes-
tations. The older development runner lacks equivalent per-row isolation evidence, and timeouts
or environmental differences may still alter classifications. Hashes link model shards, manifests,
sources, generations, and task-level summaries. The audit trail exposes the failed E16-A gate, E16-B
amendment, and subsequent runtime amendments, improving transparency without restoring
pristine prospective status.

8 Conclusion
One accepted implementation inflates apparent test-evolution gains by 9.46–14.85 pp. After indepen-
dent audit, equal-slot resampling is 6.01–18.83 pp better than mutation-based evolution. A genuine
three-round loop also does not establish a fine-grained feedback benefit: its model-dependent shift is
largely reproduced by a density-matched placebo, and qualification-amended held-out Real–Placebo

                                                  14
contrasts meet neither the pre-specified equivalence nor superiority rule. Equalizing observed valid
yield removes the positive Qwen2.5 contrast. These RQ6 analyses are diagnostic rather than pristine
confirmation. Blinded semantic judgments support invalid inputs as the dominant mechanism
while preserving a nonzero set of valid exceptions.
   Execution is useful feedback only inside a valid measurement contract. Future self-evolving test
generators should freeze selection before multi-program audit, cross-fit real faults, match search
budgets, report coverage and abstention, and compare aligned feedback with an interaction- and
density-matched placebo. These controls distinguish learning to test from learning to exploit a
verifier or merely follow a richer interface.

Data Availability
An anonymized replication package containing protocol locks, task-level derived metrics, analysis
code, figure builders, and integrity instructions is available at https://anonymous.4open.science/r/
llm-test-evolution-audit-8CF5/. Restricted model weights and source datasets are represented by
checksums and deterministic preparation instructions.

References
 [1] Nadia Alshahwan, Jubin Chheda, Anastasia Finogenova, Beliz Gokkaya, Mark Harman, Inna Harper, Alexandru
     Marginean, Shubho Sengupta, and Eddy Wang. 2024. Automated Unit Test Improvement Using Large Language
     Models at Meta. In Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software
     Engineering. Association for Computing Machinery, 185–196. doi:10.1145/3663529.3663839
 [2] Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo. 2015. The Oracle Problem in Software
     Testing: A Survey. IEEE Transactions on Software Engineering 41, 5 (2015), 507–525. doi:10.1109/TSE.2014.2372785
 [3] Jianfeng Cai, Jinhua Zhu, Ruopei Sun, Kangwen Zhao, Dongyun Xue, Mingxiao Feng, Wengang Zhou, and Houqiang
     Li. 2026. CodeContests-O: Powering LLMs via Feedback-Driven Iterative Test Case Generation. In Findings of the
     Association for Computational Linguistics: ACL 2026. Association for Computational Linguistics, 1054–1072. doi:10.
     18653/v1/2026.findings-acl.53
 [4] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. 2023. CodeT:
     Code Generation with Generated Tests. In International Conference on Learning Representations. https://openreview.
     net/forum?id=ktrw68Cmu9c
 [5] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2024. Teaching Large Language Models to Self-Debug.
     In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=KuPixIqPiq
 [6] Jacob Cohen. 1960. A Coefficient of Agreement for Nominal Scales. Educational and Psychological Measurement 20, 1
     (1960), 37–46. doi:10.1177/001316446002000104
 [7] Huan-ang Gao, Jiayi Geng, Wenyue Hua, Mengkang Hu, Xinzhe Juan, Hongzhang Liu, Shilong Liu, Jiahao Qiu, Xuan
     Qi, Yiran Wu, et al. 2025. A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence. arXiv preprint
     arXiv:2507.21046 (2025). doi:10.48550/arXiv.2507.21046
 [8] Soneya Binta Hossain, Raygan Taylor, and Matthew B. Dwyer. 2025. Doc2OracLL: Investigating the Impact of
     Documentation on LLM-Based Test Oracle Generation. Proceedings of the ACM on Software Engineering 2, FSE (2025),
     1870–1891. doi:10.1145/3729354
 [9] Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou.
     2024. Large Language Models Cannot Self-Correct Reasoning Yet. In The Twelfth International Conference on Learning
     Representations. https://openreview.net/forum?id=IkmD3fKBPQ
[10] Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Keming
     Lu, et al. 2024. Qwen2.5-Coder Technical Report. arXiv preprint arXiv:2409.12186 (2024). doi:10.48550/arXiv.2409.12186
[11] Yue Jia and Mark Harman. 2011. An Analysis and Survey of the Development of Mutation Testing. IEEE Transactions
     on Software Engineering 37, 5 (2011), 649–678. doi:10.1109/TSE.2010.62
[12] Michael Konstantinou, Renzo Degiovanni, and Mike Papadakis. 2024. Do LLMs Generate Test Oracles That Capture
     the Actual or the Expected Program Behaviour? arXiv preprint arXiv:2410.21136 (2024). doi:10.48550/arXiv.2410.21136
[13] Dongjun Lee, Changho Hwang, and Kimin Lee. 2026. Learning to Generate Unit Test via Adversarial Reinforcement
     Learning. In International Conference on Learning Representations. doi:10.48550/arXiv.2508.21107
[14] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K. Lahiri, and Siddhartha Sen. 2023. CodaMOSA: Escaping Coverage
     Plateaus in Test Generation with Pre-trained Large Language Models. In Proceedings of the 45th International Conference
     on Software Engineering. IEEE, 919–931. doi:10.1109/ICSE48619.2023.00085


                                                            15
[15] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri,
     Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean
     Welleck, Amir Yazdanbakhsh, and Peter Clark. 2023. Self-Refine: Iterative Refinement with Self-Feedback. In Advances
     in Neural Information Processing Systems 36. 46534–46594. doi:10.52202/075280-2019
[16] Davide Molinelli, Luca Di Grazia, Alberto Martin-Lopez, Michael D. Ernst, and Mauro Pezzè. 2025. Do LLMs Generate
     Useful Test Oracles? An Empirical Study with an Unbiased Dataset. In Proceedings of the 40th IEEE/ACM International
     Conference on Automated Software Engineering. 278–290. doi:10.1109/ASE63991.2025.00031
[17] Zifan Nan, Zhaoqiang Guo, Kui Liu, and Xin Xia. 2025. Test Intention Guided LLM-Based Unit Test Generation. In
     Proceedings of the 47th IEEE/ACM International Conference on Software Engineering. 1026–1038. doi:10.1109/ICSE55347.
     2025.00243
[18] Juan Altmayer Pizzorno and Emery D. Berger. 2025. CoverUp: Effective High Coverage Test Generation for Python.
     Proceedings of the ACM on Software Engineering 2, FSE (2025), 2897–2919. doi:10.1145/3729398
[19] Qwen Team. 2026. Qwen3.5-9B Model Card. Hugging Face model repository. https://huggingface.co/Qwen/Qwen3.5-
     9B Accessed 2026-08-15.
[20] Sergio Segura, Gordon Fraser, Ana Belén Sánchez, and Antonio Ruiz-Cortés. 2016. A Survey on Metamorphic Testing.
     IEEE Transactions on Software Engineering 42, 9 (2016), 805–824. doi:10.1109/TSE.2016.2532875
[21] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language
     Agents with Verbal Reinforcement Learning. In Advances in Neural Information Processing Systems 36. 8634–8652.
     doi:10.52202/075280-0377
[22] Yinjie Wang, Ling Yang, Ye Tian, Ke Shen, and Mengdi Wang. 2025. Co-Evolving LLM Coder and Unit Tester via
     Reinforcement Learning. In Advances in Neural Information Processing Systems 38. doi:10.52202/085713-4809
[23] Lin Yang, Chen Yang, Shutao Gao, Weijing Wang, Bo Wang, Qihao Zhu, Xiao Chu, Jianyi Zhou, Guangtai Liang,
     Qianxiang Wang, and Junjie Chen. 2024. On the Evaluation of Large Language Models in Unit Test Generation. arXiv
     preprint arXiv:2406.18181 (2024). doi:10.48550/arXiv.2406.18181
[24] Zheyuan Yang, Zexi Kuang, Xue Xia, and Yilun Zhao. 2025. Can LLMs Generate High-Quality Test Cases for Algorithm
     Problems? TestCase-Eval: A Systematic Evaluation of Fault Coverage and Exposure. In Proceedings of the 63rd Annual
     Meeting of the Association for Computational Linguistics (Volume 2: Short Papers). Association for Computational
     Linguistics, 1050–1063. doi:10.18653/v1/2025.acl-short.82
[25] Junwei Zhang, Xing Hu, Shan Gao, Xin Xia, David Lo, and Shanping Li. 2025. Less Is More: On the Importance of
     Data Quality for Unit Test Generation. Proceedings of the ACM on Software Engineering 2, FSE (2025), 1293–1316.
     doi:10.1145/3715778
[26] Adam Zweiger, Jyothish Pari, Han Guo, Ekin Akyürek, Yoon Kim, and Pulkit Agrawal. 2025. Self-Adapting Language
     Models. arXiv preprint arXiv:2506.10943 (2025). doi:10.48550/arXiv.2506.10943




                                                           16
A                                   Robustness Analyses
These analyses were specified after observing the primary results and are therefore robustness
checks, not new decision gates. They make no model calls, execute no programs, and do not
authorize method selection.

A.1                                   Audit depth
For depth 𝑘 ∈ {1, 2, 3}, we enumerate every size-𝑘 subset of available accepted implementations
within each task-repeat and average the result before averaging repeat seeds within task. “Full” uses
all 3–10 development implementations and all three external implementations. Depth one exactly
reconstructs the saved single-reference analysis; Full exactly reconstructs the saved accepted-panel
analysis.

                   Table 13. Evolve minus One-shot held-out constrained kill (percentage points) as audit depth increases.

                                                               Cohort               Model           1 ref.            2 refs.    3 refs.          Full
                                                               Development          Qwen2.5        10.58                4.32        2.38         −0.02
                                                               Development          Qwen3.5        13.38                3.66        1.11         −1.47
                                                               External             Qwen2.5        11.58                3.60        2.12          2.12
                                                               External             Qwen3.5        12.57                3.99        2.18          2.18



                                                       (a) Legacy minus one-shot                                                   (b) Legacy minus matched resampling
                                                                                                                                                          Dev Qwen2.5      External Qwen2.5
                                                                                                                                                          Dev Qwen3.5      External Qwen3.5
                                  15.0%                                                                        5.0%


                                  12.5%
Held-out constrained-kill delta




                                                                                                               0.0%

                                  10.0%

                                                                                                             −5.0%
                                   7.5%


                                   5.0%
                                                                                                             −10.0%

                                   2.5%
                                                                                                             −15.0%
                                   0.0%


                                  −2.5%                                                                      −20.0%



                                          1                2                   3                 Full                   1                    2                   3                     Full
                                              Number of correct implementations used for audit                                  Number of correct implementations used for audit




                                                   Fig. 2. Method differences as independent oracle references are added.

  Notably, the Qwen3.5 condition ranks Evolve slightly above Matched with one reference on
both cohorts, although the intervals cross zero. With only two references the differences become
−5.75 pp (95% CI [−8.17,−3.42]) on development and −4.24 pp [−7.46,−1.26] externally. Method
ranking therefore does not depend on auditing with a large ensemble.

A.2                                   Seed and metric sensitivity
Figure 3 reports seeds 42, 43, and 44 separately. In all 12 model–cohort–seed cells, the lower
confidence bound for gain inflation is positive. In all 12 cells, the upper bound for audited Evolve
minus Matched is negative. Individual external audited gains over one shot are small and often
uncertain, whereas the matched comparison is directionally stable.

                                                                                                        17
                                                            (a) Single-reference gain inflation                                                     (b) Audited legacy minus matched
                                                                                                                         0.0%

                                    15.0%
  Held-out constrained-kill delta




                                    12.5%                                                                              −5.0%



                                    10.0%

                                                                                                                       −10.0%
                                     7.5%


                                     5.0%
                                                                                                                       −15.0%


                                     2.5%
                                                                                                                                                                                                       seed 42
                                                                                                                                                                                                       seed 43
                                                                                                                       −20.0%
                                     0.0%                                                                                                                                                              seed 44

                                                 Dev               Dev             External            External                      Dev                  Dev                      External           External
                                               Qwen2.5           Qwen3.5           Qwen2.5             Qwen3.5                     Qwen2.5              Qwen3.5                    Qwen2.5            Qwen3.5




                                                                Fig. 3. Seed-wise gain inflation and audited method differences.


   Replacing held-out constrained kill with held-out task detection or archive task coverage yields
the same conclusion against matched resampling: all 12 model–cohort–metric upper confidence
bounds are negative. The external evolution-minus-one-shot kill gains of 2.12/2.18 pp correspond
to task-detection changes of −1.02/+0.15 pp and coverage changes of −3.95/−2.34 pp.

                                                          Constrained kill                                    Task detection                                                      Archive coverage
                                      5.0%
                                                                                                                                                                     Legacy-One
                                                                                                                                                       0.0%
                                                                                                                                                                     Legacy-Matched
                                                                                          0%
                                      0.0%
All-correct audited delta




                                                                                                                                                     −10.0%
                                                                                         −10%
                                    −5.0%


                                                                                                                                                     −20.0%
                                    −10.0%                                               −20%




                                    −15.0%                                                                                                           −30.0%
                                                                                         −30%



                                    −20.0%
                                                                                         −40%                                                        −40.0%


                                               D          D             E          E             D           D                   E            E                D                   D           E            E
                                              Q2.5       Q3.5          Q2.5       Q3.5          Q2.5        Q3.5                Q2.5         Q3.5             Q2.5                Q3.5        Q2.5         Q3.5




                                                         Fig. 4. Accepted-panel-audited method differences under three outcomes.



A.3                                          Cost accounting

Table 14. Observed historical costs. Evaluation hours are summed across executions and are not wall-clock
runtime.


                  Cohort                                        Model             Calls           Prompt tok.                   Completion tok.                        Executions                    Eval. h
                  Development                                   Qwen2.5           1,278                 796,311                                 208,781                           168,017             11.65
                  Development                                   Qwen3.5           1,278                 794,772                                 184,437                           200,234             13.62
                  External                                      Qwen2.5           1,026                 653,859                                 189,424                            94,025              4.49
                  External                                      Qwen3.5           1,026                 652,221                                 169,963                            93,334              4.69

                                                                                                                  18
  The total is 4,608 calls and 555,610 unique program–input executions. External rows attest strict
bubblewrap isolation; the older development rows record limits and counts but not equivalent
per-row isolation. The robustness reanalysis adds no generation or execution cost.

B   Three-Round Feedback Diagnostic
Table 15 reports both oracle views for the E14/E15 branches. The single-reference view makes the
apparent Qwen3.5 gain larger and the Qwen2.5 loss larger, but does not change the real-versus-
placebo conclusion. The audited cross-model interaction for real minus placebo is −0.63 pp (95% CI
[−2.92, +1.70]).

               Table 15. Held-out constrained kill (%) for the external three-round study.

                     Oracle view                Model      Plain   Placebo     Real
                     Single reference           Qwen2.5    31.04      21.49   22.69
                     Single reference           Qwen3.5    24.99      30.77   31.15
                     Accepted-panel audited     Qwen2.5    23.63      17.38   17.51
                     Accepted-panel audited     Qwen3.5    21.18      24.42   23.92


  Placebo parse rates in rounds one and two are 23.83% and 26.02% for Qwen2.5, and 77.49% and
83.33% for Qwen3.5. Real-feedback rates are 25.00% and 27.49%, and 78.95% and 82.46%, respectively.
This close tracking is a manipulation check: the placebo retains the interaction burden that plausibly
causes the Qwen2.5 degradation. It does not by itself prove which part of the iterative interface
causes the Qwen3.5 improvement.
  E14 and E15 each make 1,368 new calls per model. Combined, they add 5,472 calls, 4,893,942
prompt tokens, 911,550 completion tokens, and 190,695 unique program–input executions. E14’s
procedure was prospectively locked on the already exposed external cohort; E15 was designed after
E14 and is post hoc. Both bundles record strict bubblewrap isolation, source hashes, generated-row
hashes, and summary locks.

C   Qualification-Amended Held-Out Feedback Follow-up
E16-A opened 100 IID and 100 OOD tasks only after freezing the qualification rule, but stopped
before model calls because the 20-fault rule retained only 36 OOD tasks. The signed failure record
is preserved. E16-B was then frozen before model outcomes, changed the fault panel to 18 with
balanced 9/9 folds, and retained 138 tasks (71 IID, 67 OOD). One otherwise eligible task exceeded
the frozen 1,800-token prompt limit. This is an outcome-blind qualification amendment, not a
pristine confirmation.
   The complete qualification flow starts from 200 tasks and retains 138. The 62 excluded tasks
comprise 27 with accepted-program output disagreement alone, 18 with both disagreement and too
few exact-compatible references, 4 with too few references alone, 11 with too few faults alone, 1
with too few references and oracle cases, and 1 over the prompt limit. Thus, the nonexclusive reason
counts are 45 disagreements, 23 insufficient exact references, 11 insufficient faults, 1 insufficient
oracle case, and 1 prompt overflow.
   Changing the threshold therefore changes almost exclusively the OOD stratum. On the evaluated
nested subsets with at least 18, 19, and 20 available faults, Qwen2.5 Real–Placebo is +1.99, +1.79,
and +1.59 pp; Qwen3.5 is +0.28, +0.70, and +1.33 pp. The 19- and 20-fault intervals cross zero
for both models, and the point estimates do not share a monotone direction. This is a post-hoc
composition sensitivity, not evidence about unevaluated tasks below 18 faults.

                                                   19
   Table 16. E16-B qualification profiles. Means describe observables available before model generation.


 Group           Tasks      IID      OOD       Exact-compatible accepted                 Fault candidates
 Included           138      71         67                                    9.91                   19.68
 Excluded            62      29         33                                    4.98                   19.29

Table 17. Fault-threshold supply after all non-fault qualification filters but before prompt-length filtering.
Newly admitted tasks below 18 faults were not prompt-tokenized in the frozen run.

                                   Minimum faults     IID   OOD       Total
                                                 15    71      78      149
                                                 16    71      78      149
                                                 17    71      76      147
                                                 18    71      68      139
                                                 19    71      55      126
                                                 20    71      36      107


                   Table 18. E16-B held-out constrained kill (%) under both oracle views.

                       Oracle view                Model       Plain    Placebo   Real
                       Single reference           Qwen2.5     47.81      35.12   37.28
                       Single reference           Qwen3.5     51.92      57.58   57.50
                       Accepted-panel audited     Qwen2.5     42.42      31.03   33.01
                       Accepted-panel audited     Qwen3.5     49.91      54.37   54.66



   Under one reference, Real–Placebo is +2.16 pp for Qwen2.5 and −0.08 pp for Qwen3.5. Panel
auditing changes these to +1.99 and +0.28 pp, respectively; the main paper reports their confi-
dence intervals. Neither lies wholly inside the pre-specified ±2 pp equivalence region, and neither
has the lower bound above the +2 pp practical-superiority threshold. Both model-specific deci-
sions are therefore inconclusive within this qualification-amended cohort. E16-B uses 9,108 model
calls, 7,725,394 prompt tokens, 1,483,998 completion tokens, and 197,642 unique program–input
executions.
   Table 19 reports the secondary process measures omitted from the primary kill table. Audit
rejection is the ratio of selected single-reference archive entries removed by the accepted panel.
Candidate counts are per distinct model call; duplicate counts are candidates rejected because the
same normalized input appeared earlier in that branch. The final column divides audited held-out
faults killed by total tokens and is descriptive rather than an inferential efficacy estimand. For
arm-wise costing, the shared round-zero call is charged once to each arm; actual experiment-wide
totals above count it only once.
   The iterative arms have nearly identical token cost. Placebo and Real use 2.098 and 2.103 million
attributed tokens for Qwen2.5, and 2.166 and 2.170 million for Qwen3.5. Per direction-round,
Qwen2.5 Placebo and Real produce 0.827 and 0.874 reference-valid inputs, and 0.794 and 0.837
panel-confirmed inputs. Qwen3.5 produces 1.917 and 1.906 reference-valid inputs, and 1.882 and
1.874 confirmed inputs. This motivates the matched replay below.

                                                      20
                  Table 19. E16-B process, coverage, and descriptive efficiency diagnostics.

 Model      Arm        Audit reject (%)   Coverage (%)     Detect (%)    Tests/task   Safe/call   Dup./call   Kills/1K tok.
 Qwen2.5    Plain                 6.27           76.57           74.28         1.14      1.194       0.153           3.119
 Qwen2.5    Placebo               6.36           58.33           56.04         0.84      0.686       0.135           1.102
 Qwen2.5    Real                  6.62           60.63           58.82         0.89      0.738       0.136           1.170
 Qwen3.5    Plain                 2.57           84.42           82.85         1.38      1.515       0.537           3.753
 Qwen3.5    Placebo               3.92           90.34           88.53         1.51      1.857       0.534           1.871
 Qwen3.5    Real                  3.56           91.91           90.22         1.54      1.847       0.541           1.877



   The frozen arms had equal nominal slots but not equal realized candidate yield. Across task
repeats and cross-fit directions, Qwen2.5 Real and Placebo produced 0.837 and 0.794 panel-confirmed
reference-valid candidates per round; Qwen3.5 produced 1.874 and 1.882. We replayed all 828 saved
model–task–seed rows and first required exact reproduction of both frozen oracle views. We then
retained the earliest pairwise-minimum candidate count in each direction and round.

              Table 20. E16-B post-hoc yield-matched Real–Placebo sensitivity ( pp, 95% CI).

                  Matching policy                        Qwen2.5                  Qwen3.5
                  Reference-valid                        −0.30 [−0.90,+0.30]      +0.78 [−0.62,+2.19]
                  Panel-safe/disconfirmed strata         −0.35 [−0.91,+0.20]      +0.13 [−1.03,+1.23]


  This replay makes no model calls or program executions and leaves the frozen E16-B decision
unchanged. It is off-policy: later candidates were generated from the full original histories, not from
the truncated replay. The result therefore establishes sensitivity to observed candidate opportunity,
not a causal direct effect of semantic attribution.

D   Human Semantic Audit
Two software engineering doctoral students independently reviewed the 300 cases in separate
randomized blind orders. Both received the same frozen annotation schema and substantive instruc-
tions. For each case, a reviewer saw the problem statement, public examples, and candidate input,
but not the task identity, generation method, archived output, program behavior, fault detections,
panel outcome, or the other reviewer’s judgment. All 300 final rows from each reviewer passed the
same schema validator. Reviewer identities are withheld and replaced with A and B in Table 21
because direction is not substantively important.

Table 21. Five-class judgment confusion matrix. The two unused classes, ambiguous specification and insuffi-
cient information, have zero rows and columns and are omitted for space.

                                                                   Judge B
                             Judge A             Valid     Out of domain        Malformed
                             Valid                  18                     0               4
                             Out of domain           1                   195               0
                             Malformed               2                    18              62


  The raw five-class exact agreement is 275/300 = 91.67% and Cohen’s 𝜅 = .823. After collapsing
both invalid labels, agreement is 293/300 = 97.67% with 𝜅 = .825. These values measure inter-rater

                                                            21
agreement between the two human reviewers; they do not establish that a shared interpretation is
semantically correct.
  The specification-adjudication packet contains 67 unique cases. Its categories are not mutually
exclusive at selection time: 25 have inter-rater disagreement, 18 have reviewer consensus on
validity and therefore need expected-output review, 24 are a deterministic 10% quality sample from
otherwise unflagged consensus cases, and four of the jointly valid cases are resource-limit- sensitive.
The union is 67 because those four overlap the valid-output category. The packet is reserved for
consensus or third-reviewer adjudication, which would record a final validity label, output when
applicable, notes, and whether the evidence came from specification review, constraint checking,
brute force, or execution replay. Until then these cases are not force-resolved; the main analysis
uses the two frozen human ratings and preserves the audit-disconfirmed terminology.

E   Protocol Boundaries
The external protocol’s three claim checks concern the existence of the oracle problem, positive
gain inflation, and non-superiority to matched resampling within a +2 pp tolerance. All passed for
both model conditions. The protocol explicitly forbids using the external result to tune a generator
or choose an adapter. The development fault-family analysis is exploratory, and its confidence
intervals are descriptive. No cohort supports a causal model-scale claim or a semantic frequency
claim about source-level bug categories. E14 is a prospectively locked extension on the already
exposed external cohort, not a new untouched replication. E15 is a post-hoc diagnostic. Its real-
minus-placebo contrast identifies no detectable increment from fine-grained attribution under
the constructed placebo, but it does not establish equivalence or eliminate the possible value of
aggregate execution signals. E16-A is the pristine qualification attempt and failed before model
calls. E16-B is outcome-blind with respect to model results but follows a disclosed qualification
amendment; its two inconclusive decisions neither confirm equivalence nor establish practically
important superiority.




                                                  22
