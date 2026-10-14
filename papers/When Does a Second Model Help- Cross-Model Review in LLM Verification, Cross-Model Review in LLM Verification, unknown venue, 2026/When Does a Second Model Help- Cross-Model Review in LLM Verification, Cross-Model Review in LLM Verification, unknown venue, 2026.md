                                                                     When Does a Second Model Help?
                                                                  Cross-Model Review in LLM Verification

                                                                                      Song Tae-Eun
                                                                           Daejeon Jungang Cheonggua Co., Ltd.
                                                                                 higheun@gmail.com



                                                              Abstract                              has motivated the use of LLMs themselves as re-
                                                                                                    viewers, an approach that is already gaining indus-
                                            Large language models now generate code,                trial traction, as evidenced by the recent release of
arXiv:2610.01471v1 [cs.CL] 1 Oct 2026




                                            documentation, and analyses, and are in-                cross-model review tooling integrated directly into
                                            creasingly used to review such output. We
                                                                                                    AI coding assistants (OpenAI, 2026). Two ques-
                                            ask when a second review by a different
                                            model helps. Building on the author’s ear-              tions are open: what makes AI review of AI out-
                                            lier preprints, which varied context, repetition,       put independent, and does cross-model review im-
                                            and role structure within one model, we test            prove defect detection?
                                            model independence in a controlled experi-                 Verification is only as useful as it is independent
                                            ment: 30 artifacts with 150 planted errors,             of what produced the output. In human contexts,
                                            10 review conditions, and 900 review sessions           peer review, double-blind evaluation, and indepen-
                                            with three reviewer models from two develop-
                                                                                                    dent auditing all derive their value from ensuring
                                            ers. In this experiment, (1) a top-tier cross-
                                            model reviewer is not significantly different
                                                                                                    that the verifier’s judgment is not contaminated by
                                            in F1 from same-model review in a fresh ses-            the same biases that produced the original output.
                                            sion (CCR), which does not establish equiv-             When the same LLM reviews its own generation
                                            alence; (2) the two find partly different er-           within the same conversational context, it shares
                                            rors (Jaccard 41.2%); and (3) at two review             its training data, parameters, and conversational
                                            calls, one CCR plus one cross-model review              context, and in-context self-correction without ex-
                                            matches more planted errors than two CCR re-            ternal feedback has been found to degrade accu-
                                            views (56.7% vs. 42.7%; Holm-adjusted p =
                                                                                                    racy (Huang et al., 2024).
                                            .006), but not significantly more than two re-
                                            views by the top-tier cross-model reviewer, so             A series of earlier studies by the author ex-
                                            model difference and reviewer capability are            plored individual dimensions of independence
                                            not separated. A lightweight cross-model re-            within one model. Cross-Context Review (CCR;
                                            viewer scores no higher than same-model re-             Song, 2026a) reported that context independence
                                            view. Withholding requirements from the re-             (removing the generation conversation before re-
                                            viewer raises F1 for the two lower tiers but            view) improves defect detection; in the data reused
                                            not the top tier, in untested point estimates
                                                                                                    here, after excluding one baseline run of un-
                                            whose pattern depends on how failed sessions
                                            are scored. Before analysis we audited all ses-
                                                                                                    certain provenance, CCR exceeds same-context
                                            sion records, excluding one baseline run of             self-review by only 1.5pp in F1, which is not
                                            uncertain provenance and 14 failed calls; re-           significant (Section 5.1). Diachronic CCR (D-
                                            sults with all sessions are also reported. A par-       CCR; Song, 2026c) reported that temporal in-
                                            tial check on public detector outputs from an-          dependence (adding repeated review rounds) is
                                            other benchmark neither replicates nor contra-          counterproductive, increasing false positives by
                                            dicts the main comparison. Records, artifacts,          62% without improving recall. In a study whose
                                            and scripts are available from the author on re-
                                                                                                    main subject is benchmark-contamination detec-
                                            quest.
                                                                                                    tion, the Hierarchical Cross-Context Architecture
                                        1   Introduction                                            report (HCCA; Song, 2026b) also describes a pi-
                                                                                                    lot in which a multi-stage pipeline (worker, ver-
                                        Large language models (LLMs) now generate                   ifier, director) whose later stages could see ear-
                                        code, documentation, data analyses, and research            lier conclusions produced only sycophantic confir-
                                        artifacts faster than people can review them. This          mation, and identify information restriction rather

                                                                                                1
than structural complexity as the key mechanism.          2     Background
These three reports are the author’s own single-
                                                          2.1    Context Independence
author preprints that have not been peer reviewed,
so we do not rely on their conclusions: every base-       Cross-Context Review (CCR; Song, 2026a) con-
line number below is recomputed from the per-             ducts review in a fresh session, so the reviewer re-
session data, the benchmark and matching proce-           ceives only the artifact, not the conversation that
dure are specified in Appendix A, and where our           produced it. Across 360 sessions over 30 artifacts
test disagrees with an earlier report we say so.          with 150 ground truth errors, the original report
                                                          found CCR ahead of same-context review, testing
   All three studies stayed within one model. The
                                                          run 1 alone (paired t, p = 0.008); among the
most intuitive form of independence, using a dif-
                                                          four same-model conditions, CCR ranks first in
ferent model, remained untested. This paper ad-
                                                          that run only (run-level F1 in Appendix D). In the
dresses that gap.
                                                          data used here, after excluding one same-context
   We introduce a four-dimensional framework for          run of uncertain provenance (Section 4.1), CCR’s
independence in LLM verification, encompassing            F1 is 28.6% versus 27.1%, and the artifact-level
context, temporal, structural, and model indepen-         test finds no significant difference (unadjusted p =
dence. Through a controlled experiment with 900           0.26; Table 2). The original report attributed the
review sessions across 10 conditions, we system-          gap to removing the conversational anchoring that
atically evaluate model independence and its in-          biases a model toward defending its own output.
teraction with other dimensions. Our key findings
are:                                                      2.2    Temporal Independence
                                                          Diachronic CCR (D-CCR; Song, 2026c) tested re-
   We use complementary to mean partially non-
                                                          peated review rounds: counter-intuitively, a sec-
overlapping detection, not super-additive cover-
                                                          ond round decreased performance, with false pos-
age. (1) Complementary detection: cross-model
                                                          itives increasing by 62%. The report attributes this
review (XMR) and CCR find partly different de-
                                                          to the same model amplifying its existing false-
fects (Jaccard 41.2%), with CCR ahead on code
                                                          confidence patterns rather than gaining new per-
(F1 40.7%) and XMR on documents (F1 up to
                                                          spectives, which would suggest that repeating re-
42.1%); (2) call-matched coverage: one CCR
                                                          view in the same session is not a path to indepen-
plus one XMR review matches 56.7% of planted
                                                          dence.
errors against 42.7% for two CCR reviews, while
the gain over two top-tier XMR reviews is not             2.3    Structural Independence
significant; (3) reviewer capability appears to
                                                          The HCCA report (Song, 2026b) assigns special-
shape the effect—a top-tier reviewer shows no
                                                          ized analytical roles under intentional information
significant difference from CCR, but a lightweight
                                                          restriction. In a pilot extending this to a multi-
model scores numerically below even baseline
                                                          stage pipeline (worker, verifier, director) in which
same-context review, so the value of model in-
                                                          later stages could see earlier conclusions, the re-
dependence appears to depend on reviewer qual-
                                                          port observes only sycophantic confirmation and
ity; and (4) information restriction raises cross-
                                                          attributes the benefit of its main design to informa-
model F1 for the two lower tiers (+2.2 and +3.0pp)
                                                          tion restriction rather than to structural complex-
but not the top tier (−0.2pp; untested point esti-
                                                          ity.
mates).
   These results suggest tentative guidance: pair-        2.4    The Remaining Dimension: Model
ing a same-model review with a cross-model one                   Independence
gave more coverage than two same-model re-                The three prior studies explored three ways of
views, though not significantly more than two top-        varying review within a single model: context can
tier cross-model reviews; for resource-constrained        be reset, timing varied, and roles restructured, but
settings, a single cross-model review with a top-         the model’s training data, weights, and systematic
tier reviewer had the highest F1 of any single con-       biases remain constant. The natural next question
dition in our data (not significantly above CCR);         is whether a different model, trained on different
and lightweight cross-model reviewers offered no          data with different objectives, provides a funda-
advantage over same-model review.                         mentally different form of independence.

                                                      2
   Indirect evidence suggests it should. LLMs                 Software review and blind spots. LLMs are
differ in measured capability across tasks (Zheng          increasingly applied to code review (Li et al.,
et al., 2023; Chiang et al., 2024), and cross-model        2022; Pornprasit and Tantithamthavorn, 2024; Ci-
review has already been integrated into production         han et al., 2025); in a related setting, Shin et al.
developer tools (OpenAI, 2026). However, we are            (2025) find that LLM-generated reviews of re-
not aware of prior work that systematically mea-           search papers over-focus on technical validity and
sures whether these differences translate into com-        overlook novelty compared with human experts.
plementary defect detection.                               Doddapaneni et al. (2024) probe five evaluator
                                                           LLMs with 2,400 perturbed answers and report
2.5   Related Work                                         that they miss quality drops in over 50% of cases
LLM self-correction and self-preference. In-               on average. We use “blind spot” in a narrower
context self-correction without external feedback          sense (defects one reviewer model misses and
degrades accuracy (Huang et al., 2024); Kamoi              another catches) and quantify it through Jaccard
et al. (2024b) attribute the failure to the feedback       overlap.
(error-detection) stage and recommend analysing               Hallucination detection, ensembles, and N-
the quality of generated feedback directly. They           version. Consistency-based methods exploit the
also note that cross-model correction is unsuitable        intuition that disagreement across independent
for testing whether a model can improve its own            samples signals unreliability, via semantic en-
responses, and recommend comparisons against               tropy (Farquhar et al., 2024) or reference checking
baselines of comparable computational cost; our            (Manakul et al., 2023). Ensemble and mixture-
two-review-call analysis matches the number of             of-agents methods show that model diversity im-
review calls, not compute. LLMs also favor                 proves aggregate performance (Dietterich, 2000;
their own generations (Panickssery et al., 2024).          Wang et al., 2024a; Tekin et al., 2024), echoing N-
Neither line compares a same-conversation re-              version programming (Chen and Avizienis, 1978);
viewer against a fresh-context or different-model          we extend these principles to across-model defect
reviewer: the axis we vary.                                detection.
   Sycophancy and evaluation bias. LLMs ad-                   Correlated errors and frontier blind spots.
just outputs to match perceived user preferences           Kim et al. (2025) analyze over 350 LLMs, largely
(Sharma et al., 2024) and, as judges, exhibit po-          on multiple-choice benchmarks; on one leader-
sitional and other judgement biases (Wang et al.,          board (HELM), pairs of models that both err
2024b; Chen et al., 2024).                                 choose the same wrong answer about 60% of the
   Multi-agent systems and LLM-as-judge.                   time, and larger, more accurate models have more
Multi-agent frameworks structure multiple LLM              highly correlated errors. This result raises con-
instances to debate answers or assume special-             cerns about naive multi-model ensembles and mo-
ized roles (Du et al., 2024; Liang et al., 2024;           tivates our measurement of pairwise finding over-
Chan et al., 2024; Hong et al., 2024; Qian et al.,         lap (52.2% within the same model vs. 37–46%
2024), while LLM-as-judge approaches use LLMs              across models; Section 5.3), a descriptive compar-
to score or rank outputs (Zheng et al., 2023;              ison rather than a test of error correlation.
Li et al., 2024; Kim et al., 2024). These sys-
tems primarily manipulate structural and context           3     A Framework for Independence in
independence but typically use a single under-                   LLM Verification
lying model, leaving model independence unex-
                                                           3.1    Dimensions of Independence
plored. Error-detection benchmarks: ReaLMis-
take (Kamoi et al., 2024a) and BIG-Bench Mis-              We define four binary dimensions characterizing
take (Tyen et al., 2024) report low detection              the relationship between a generator LLM (which
rates even for strong models, and CriticBench              produces the artifact) and a reviewer LLM (which
(Lin et al., 2024) finds that stronger models cri-         verifies it):
tique weaker ones better while weaker models can              Context independence (C): the reviewer has no
sometimes surpass stronger ones in self-critique;          access to the generation conversation, operating
but none of these analyses is organised around a           with P (findings | artifact) rather than P (findings |
model inspecting its own output versus another             artifact, G), where G is the generation transcript.
model’s.                                                      Temporal independence (T): the review occurs

                                                       3
in a single pass, with no memory of prior review               We additionally explore two non-directional hy-
rounds on the same artifact.                                potheses:
   Structural independence (S): the reviewer op-               H4 (Dimension Interaction). The combination
erates without hierarchical subordination to the            of context and model independence exhibits inter-
generator, avoiding deference or sycophancy.                action effects (synergistic or antagonistic) beyond
   Model independence (M): the reviewer is a dif-           the sum of individual effects. This hypothesis is
ferent model, typically from a different developer.         not identifiable in our design, which has no con-
This does not guarantee different training data or          dition with model independence but no context in-
uncorrelated errors; whether cross-model errors             dependence; we state it for completeness.
are less correlated is an empirical question (Sec-             H5 (Error-Type Specialization). Different in-
tion 5.3).                                                  dependence dimensions are differentially effective
   We additionally define information restriction           across error types (FACT, CONS, CTXT, RCVR,
(R) as a cross-cutting modifier: the reviewer               MISS) and artifact categories (code, document,
receives only the artifact, without the original            script).
prompt or requirements, forcing assessment on in-
trinsic merits rather than compliance with stated           4     Experimental Setup
goals.
                                                            4.1    Experiment A: Controlled Code Review
3.2   Experimental Conditions as Dimension                  Artifacts. We reuse the 30 software artifacts
      Combinations                                          and 150 ground truth errors from Song (2026a).
Our 10 conditions map onto the framework as                 The artifacts span three categories: code mod-
shown in Table 1. All XMR conditions inherently             ules (C1–C10), technical tutorials (D1–D10), and
include context independence, because in our de-            presentation scripts (S1–S10). Each artifact con-
sign the cross-model reviewer never receives the            tains 5 planted defects across 5 error types: fac-
generation conversation; comparing CCR (C only)             tual errors (FACT), internal consistency violations
against XMR conditions (C + M) therefore esti-              (CONS), missing context handling (CTXT), re-
mates the effect of replacing the reviewer model,           coverability gaps (RCVR), and missing function-
which also changes reviewer capability and other            ality (MISS). Error severities range from Critical
model characteristics, rather than an isolated effect       to Minor. Reusing identical artifacts enables di-
of model independence.                                      rect comparison with prior results.
                                                               Generator model. All 30 artifacts were gener-
3.3   Hypotheses                                            ated by a single frontier-class LLM, Claude Opus
Based on our framework, we test the following hy-           4.6 according to our run logs; the artifact files
potheses:                                                   themselves do not record the generating model.
   H1 (Unique Finding). Cross-model review dis-             The same-model baselines (SR, SR2, SA, CCR)
covers defects that cross-context review misses,            were run with that model, subject to the same
and vice versa. Formally: UFR(XMR → CCR) >                  caveat. Reviewer model identifiers denote the re-
0 and UFR(CCR → XMR) > 0, where                             quested API parameter rather than a confirmed
UFR(A → B) is the proportion of A’s true posi-              served checkpoint, as the endpoints do not return
tives not found by B.                                       a served model identifier. Using a single gener-
   H2 (Union Superiority).        The union of              ator ensures that all reviewer conditions evaluate
CCR and XMR findings achieves higher re-                    identical artifacts, removing generator variation;
call than either alone (implied by H1 under                 it does not separate reviewer independence from
a fixed matcher; we report it for its magni-                other reviewer characteristics such as capability.
tude).     Formally: Recall(CCR ∪ XMR) >                       Dependence on prior work. The four base-
max(Recall(CCR), Recall(XMR)).                              line conditions (SR, SR2, SA, CCR), the C/T/S
   H3 (Bias Orthogonality). The overlap be-                 dimensions, and the artifacts with their ground
tween CCR and XMR findings is lower than                    truth come from the earlier preprints; only the
the overlap between independent sessions within             XMR conditions and the unifying taxonomy are
the same model, which would be consistent with              new. Appendix A specifies the artifacts, error in-
systematically different blind spots. Formally:             jection, and matching so that the claims here can
Jaccard(CCR, XMR) < Jaccard(CCRA , CCRB ).                  be checked without those reports. The baselines

                                                        4
               Condition        C    M    R   Reviewer Model              Description
               SR               −    −    −   Generator (same session)    Baseline: self-review
               SR2              −    −    −   Generator (2nd pass)        Repeated review (T=0)
               SA               −    −    −   Generator (sub-agent)       Role separation (S varied)
               CCR              +    −    −   Generator (new session)     Context independence only
               XMR-Ge           +    +    −   Gemini 2.5 Flash            Cross-model (lightweight)
               XMR-Ge-R         +    +    +   Gemini 2.5 Flash            + information restriction
               XMR-GePro        +    +    −   Gemini 2.5 Pro              Cross-model (capable)
               XMR-GePro-R      +    +    +   Gemini 2.5 Pro              + information restriction
               XMR-GPT          +    +    −   GPT-5.4                     Cross-model (top-tier)
               XMR-GPT-R        +    +    +   GPT-5.4                     + information restriction

Table 1: Experimental conditions mapped to independence dimensions. Temporal (T) and structural (S) dimen-
sions are held constant across most conditions; SR2 uniquely lacks temporal independence (repeated review), and
SA uniquely varies structural independence (sub-agent role). See Sections 2.2–2.3 for detailed analysis of these
dimensions.


were collected before the XMR conditions under               sitioning at the time of the experiment, not a ca-
the same protocol, a temporal asymmetry noted in             pability we measured, and GPT-5.4 is also a later
Limitations.                                                 model generation than Gemini 2.5:
   Data provenance and exclusions. We audited                   • GPT-5.4 (top-tier): a model from a different
all 900 session records against the raw files before              developer than the generator.
the analysis reported here. The 540 cross-model
records carry the reviewer model identifier, call               • Gemini 2.5 Pro (capable): a strong model
duration, and a per-session timestamp. The 360                    from a third developer.
same-model baseline sessions were run through                   • Gemini 2.5 Flash (lightweight): a cost-
the Claude Code agent tool and transcribed into                   optimized model from the same developer as
structured files by the host session; they carry no               Gemini 2.5 Pro, testing whether model inde-
raw model output, and in several runs all 30 files                pendence helps even with reduced capability.
share one timestamp. For one run (SR, run 3), 92%
                                                                For each family, we test both unrestricted (full
of the finding descriptions appear verbatim inside
                                                             artifact + requirements) and information-restricted
the script that wrote the files, so we cannot con-
                                                             (artifact only) conditions.
firm that they are unedited model output, and we
                                                                Procedure. Each session proceeds identi-
exclude this run from all analyses. Fourteen cross-
                                                             cally: the reviewer receives the artifact (and
model sessions failed (five timeouts or crashes and
                                                             requirements, unless information-restricted) and
nine unparseable outputs; eight of the fourteen
                                                             produces a structured list of findings (location,
were XMR-Ge-R sessions) and had been scored
                                                             description, severity, error type). Findings are
as reviews with no findings; because a failed call
                                                             matched against the ground truth by location- and
is not a review, we exclude them as well. The anal-
                                                             keyword-overlap scoring, each finding assigned to
yses therefore describe cross-model review when
                                                             at most one ground-truth error and each ground-
the call succeeds; Appendix D reports the main
                                                             truth error credited at most once per review (Ap-
values with failures scored as zero. The exclu-
                                                             pendix A).
sion rules followed from the audit and were fixed
                                                                Statistical testing. We use the Wilcoxon
before the full recomputation, although a partial
                                                             signed-rank test for paired comparisons at the arti-
check of their effect on cross-model F1 was run
                                                             fact level (averaging the available runs per artifact
during the audit. The remaining baseline records
                                                             per condition after the exclusions of Section 4.1;
are unverified rather than known to be clean.
                                                             every artifact keeps at least one run in every con-
   Conditions and scale. We evaluate 10 condi-               dition, so each test uses 30 paired observations),
tions (Table 1), each with 90 sessions (3 runs per           with Holm-Bonferroni correction over the nine
artifact × 30 artifacts), yielding 900 sessions total.       comparisons against CCR. For comparison with
  Reviewer models. We employ three external                  the original CCR report, Table 2 also gives paired
reviewer models from two developers at different             t-tests on run 1 alone without correction; our con-
capability tiers. The tiers reflect the vendors’ po-         clusions use the former. Union analysis computes

                                                         5
Rank Condition          n   F1 Prec. Rec. pW         pt          over baseline self-review.
     1   XMR-GPT     86 32.3     28.6   38.4 1.00 .478              The difference between the best XMR condition
     2   XMR-GPT-R 89 32.1       27.5   39.8 1.00 .524           (XMR-GPT, 32.3%) and CCR (28.6%) is not sta-
     3   XMR-GePro-R 90 29.0     29.2   29.3 1.00 .176
     4   CCR         90 28.6     31.5   27.1 —     —
                                                                 tistically significant (adjusted pW = 1.00; run-1
     5   SR          60 27.1     26.2   28.3 1.00 .008           pt = 0.478). We therefore detect no F1 differ-
     6   XMR-Ge-R    82 27.0     34.2   23.9 1.00 .232           ence between model independence with a top-tier
     7   XMR-GePro   90 26.8     30.6   24.9 1.00 .083
     8   XMR-Ge      89 24.0     35.1   20.0 1.00 .017           reviewer and context independence alone; without
     9   SA          90 23.8     27.4   21.8 .228 .004           an equivalence test, this is not evidence that the
    10   SR2         90 21.7     21.0   22.7 .011 <.001          two are equal.
                                                                    The spread across reviewer models is larger.
Table 2: Performance across 10 conditions (900 ses-
sions; n = sessions analysed after excluding SR run 3
                                                                 XMR-GPT (32.3%) exceeds XMR-Ge (24.0%) by
and 14 failed cross-model sessions, Section 4.1; Ap-             8.3 percentage points, more than the gap between
pendix D gives the values with failures scored as zero).         CCR and SR (1.5pp). This single comparison is
Values are percentages. pW : Wilcoxon signed-rank test           outside the nine-comparison family; its unadjusted
against CCR on per-artifact means over the available             Wilcoxon p is 0.020 with failed sessions excluded
runs, Holm-adjusted over nine comparisons (only SR2              and 0.071 with them scored as zero, and it would
differs); pt : paired t-test on run 1 only, unadjusted, as       not survive correction if added to the family. The
in the original CCR report.
                                                                 data are consistent with reviewer capability mat-
                                                                 tering more than independence per se, but do not
the unique ground truth errors detected by at least              establish it.
one session per condition, yielding Union Recall,
                                                                 5.2   Complementary Detection (H1, H2)
Unique Finding Rate (UFR), and Jaccard similar-
ity.                                                             While individual F1 scores are similar between
                                                                 CCR and top XMR conditions, their coverage pat-
4.2      Reproducibility                                         terns differ meaningfully.
The artifacts, ground-truth annotations, review                     Union Recall (Figure 1): under the existing
prompts, per-session review records, and analy-                  automated matcher, a two-review-call comparison
sis scripts are available from the author on re-                 yields 85/150 (56.7%) matched ground-truth er-
quest. Raw API outputs and per-session model                     rors for one CCR plus one XMR-GPT-R review
identifiers exist only for the cross-model condi-                versus 64/150 (42.7%) for two CCR reviews, a
tions; the same-model baseline records were tran-                14.0pp gain (artifact-level bootstrap 95% CI [6.7,
scribed into structured files by the host session and            22.0]; signed-rank p = .006, Holm-adjusted over
do not include raw model output (Section 4.1). We                the three union comparisons). These are set-level
note that exact reproduction is limited by the non-              recalls over run 1 (singles 56 and 64; 56 + 64 −
deterministic nature of LLM outputs, and the 90                  35 = 85), not the per-session means of Table 2.
sessions per condition are repeated measurements                 Across the three runs per condition, mixed unions
on 30 artifacts, so our tests use 30 artifact-level              cover 44.7–56.7% and CCR-only unions 30.0–
pairs.                                                           42.7% (reused runs, not independent replications).
                                                                 Against two XMR-GPT-R reviews, on the 29 arti-
5     Results                                                    facts without a failed session (76/145 vs. 82/145
                                                                 for the mixed pair), the gain is 4.1pp (95% CI
5.1      Overall Performance                                     [−2.1, 10.3]; adjusted p = .184). The third com-
Table 2 presents the main results across all 10 con-             parison in the family uses self-review as the same-
ditions, ranked by F1 score, and Figure 2 (Ap-                   model partner: SR plus XMR-GPT-R matches
pendix) visualizes this ranking.                                 77/150 against 53/150 for SR plus SR2 in run 1
   The top three conditions are all cross-model                  (+16.0pp, 95% CI [6.7, 26.0]; adjusted p = .008).
configurations, and the bottom three are the                     These retrospective results are conditional on the
lightweight cross-model condition (XMR-Ge), the                  matcher; condition-specific matching bias remains
sub-agent baseline (SA), and the repeated base-                  unmeasured.
line (SR2). XMR-Ge-R (27.0%) is level with                          The Jaccard similarity between CCR and XMR-
SR (27.1%), so model independence with a                         GPT-R is 41.2% (35 of 85 unique errors found
lightweight reviewer shows no clear advantage                    by either), indicating moderate overlap: the ap-

                                                             6
                                                                Category   CCR    GePro-R    GPT     GPT-R
                                                                Code       40.7     23.4     37.2     29.8
                                                                Document   24.5     38.1     42.1     40.7
                                                                Script     20.7     25.6     15.4     25.8

                                                          Table 3: F1 (%) by artifact category. Bold indicates
                                                          best condition per category.


                                                          arise from differences in detection rates or find-
Figure 1: Planted errors matched by CCR and by            ing counts, and the run pairs share artifacts, so this
XMR-GPT-R (run 1 of each condition; 150 errors in         is descriptive support rather than a test.
total).                                                      CCR vs. SR overlap (59.9%) is comparable to
                                                          within-condition overlaps: we see no clear sign
                                                          that changing the context alone changes which er-
proaches share a substantial core, but ∼59%               rors the model finds, whereas changing the model
of unique findings come from only one ap-                 is accompanied by lower overlap, which matters
proach, supporting H1 (each finds defects the             given that high-capability LLMs exhibit strongly
other misses). The 14.0pp union gain is con-              correlated errors (Kim et al., 2025).
sistent with H2 (union superiority) in the narrow
sense that the union covers more than either review       5.4    Domain Specialization (H5)
alone. Any two imperfect, non-identical detec-            The aggregate F1 scores mask a reversal at the cat-
tors raise union recall mechanically; the observed        egory level (Table 3).
unions in fact fall below both pooled and within-            For code artifacts, CCR outperforms all XMR
artifact independence reference values (rA + rB −         conditions; one possible explanation is that the
rA rB ). These descriptive comparisons do not es-         generating model shares an understanding of pro-
tablish synergy or its absence; we do not claim           gramming patterns and code structure that an ex-
synergy (super-additive coverage beyond indepen-          ternal model lacks. For documents, the pattern re-
dent expectation)—complementarity here refers to          verses, and it holds for every condition, not only
non-overlap (Jaccard 41.2%).                              those in the table: all six cross-model conditions
                                                          (F1 30.1–42.1%) score above all four same-model
5.3   Bias Orthogonality (H3)
                                                          conditions (17.4–24.5%). XMR conditions per-
To test whether cross-model overlap is lower than         form better, suggesting a different model brings
within-model overlap (which would be consistent           different expectations about consistency and com-
with systematically different blind spots), we com-       pleteness, shaped by different training corpora.
puted pairwise Jaccard similarity at the finding          This category reversal is our clearest descriptive
level across all run pairs.                               support for H5, although the category estimates
   Within-condition overlap (same model, dif-             carry no uncertainty intervals and the explanations
ferent sessions): CCR 52.2% (90 run pairs),               above are conjectures; it suggests that the choice
SR 61.8% (30 pairs, runs 1–2 only), XMR-                  between CCR and XMR should depend on artifact
GPT 59.3% (84), XMR-Ge 55.1% (88). Cross-                 type.
condition overlap (all run combinations): CCR vs.
XMR-GPT 46.1% (258 pairs), CCR vs. XMR-Ge                 5.5    Error Type Analysis
36.5% (267), and CCR vs. SR 59.9% (180; same              Breaking down results by error type reveals further
model, different context). Pairs involving an ex-         specialization (Table 4). Detection rates are per-
cluded session are dropped, so the pair counts dif-       session recall for each error type, averaged over
fer.                                                      the analysed sessions (n as in Table 2).
   Within-model session pairs share 52–62% of                Several patterns emerge. The top-tier cross-
findings, while cross-model pairs share 37–46%.           model reviewer is higher than CCR on FACT
The difference between CCR intra-condition over-          (58% vs. 48%) and CONS (53% vs. 37%). On
lap (52.2%) and CCR-vs-XMR cross-model over-              CTXT, where operational context matters, the two
lap (average 41.3%) is 10.9 percentage points,            top-tier conditions reach 26–31%, against 9–18%
consistent with H3. Lower overlap can also                for every other condition (XMR-GPT-R and SR

                                                      7
      Error Type   CCR   XMR-Ge     GePro    GPT             5.7   Reviewer Model Capability
      FACT         48       35        48      58             Within each restriction setting, F1 increases
      CONS         37       33        38      53
      CTXT         13        9         9      26             with reviewer tier: top-tier 32.1–32.3% (above
      RCVR         19        7        16      34             CCR’s 28.6%, not significantly), capable 26.8–
      MISS         19       17        14      21
                                                             29.0% (approaching CCR with restriction), and
                                                             lightweight 24.0–27.0% (at or below the SR base-
Table 4: Detection rate (%) by error type (recall per
type). Bold indicates best condition per type.               line of 27.1%). The spread between the best
                                                             and worst XMR conditions (8.3pp) is larger than
                                                             the total spread among all same-model conditions
are not shown in the table). Across all six cross-           (6.9pp), although ranges over different sets of con-
model conditions (including three not shown in               ditions are not directly comparable effect sizes.
Table 4), RCVR varies most (7–38%), followed
by FACT (35–58%) and CTXT (9–31%), consis-                   5.8   Model Bias False Positives
tent with these types being sensitive to reviewer            Cross-model review introduces a new category of
capability.                                                  false positive: model bias errors, where the re-
   The apparent tension between Tables 3 and                 viewer flags issues based on its own training data
4, namely CCR’s higher F1 on code (40.7% vs.                 rather than actual defects. Classifying all XMR
37.2%) despite XMR-GPT’s comparable or higher                false positives via keyword-based analysis, 187
per-type recall, is consistent with precision: on            of 1,995 (9.4%) were model bias; the most com-
code, CCR’s precision is 46.9% versus 35.6%                  mon subcategory (72.7%, 136/187) involved flag-
for XMR-GPT, while its recall is 36.7% versus                ging generator-specific features or tools as non-
40.0%. The analyses also operate at different                existent, which may reflect differences in training
granularities, so dominance at one level need not            data between model families (the classification is
imply it at the other.                                       keyword-based and was not validated). Informa-
                                                             tion restriction partially mitigates this (lightweight
                                                             13%→10%, capable 10%→8%), and the top-tier
5.6     Information Restriction Effect
                                                             model shows the lowest rate (9% unrestricted, 8%
Restricting the information available to the re-             restricted).
viewer, by providing only the artifact without the
original requirements, changes cross-model F1 by             5.9   Case Studies
tier as follows: top-tier 32.3→32.1 (−0.2), capa-            We ran five case studies outside software review—
ble 26.8→29.0 (+2.2), and lightweight 24.0→27.0              agricultural anomaly detection (B1), recession
(+3.0). The two sides of each comparison are not             identification (B2), news fact-checking (B3), a
the same session sets after exclusions, and with             meta-review of this paper’s own analysis code
failed sessions scored as zero the changes are +0.9,         (B4), and a security audit (B5). Because their ev-
+2.2, and +0.9 (Appendix D).                                 idential value varies sharply, we summarize them
   This pattern is consistent with the earlier HCCA          here and report them in full in Appendix F.
report (Song, 2026b) that less information pro-                 Only B3 (news fact-checking) is informative
motes more independent judgment; the per-tier                for our hypotheses: the top-tier cross-model re-
gains are untested point estimates, and the account          viewer again has the highest F1, and the union
that follows is a hypothesis. When the reviewer              of CCR and XMR-GPT findings reaches 86.0%
cannot simply check the artifact against stated re-          recall against 76.7% for XMR-GPT alone (CCR
quirements, it must assess the artifact on its intrin-       55.8%), with a Jaccard of 54.1%; each condition’s
sic quality, detecting inconsistencies, logical gaps,        recall here pools its three runs, so the union pools
and errors that requirement-checking might over-             six reviews against three and is descriptive, not a
look. After the exclusions the top-tier reviewer             matched comparison. B1 and B2 reached 100%
shows no gain (+0.9 with failures scored as zero),           accuracy under every condition; a ceiling leaves
and the size of the lightweight tier’s gain depends          no room to discriminate between conditions, so we
on how failed sessions are handled, so the relation-         draw no comparative conclusion from them and
ship between reviewer capability and the benefit of          report them only as evidence that the task fram-
restriction is unclear.                                      ing transfers. B4 and B5 lack independent ground

                                                         8
truth and are qualitative demonstrations, not tests.        views (56.7% vs. 42.7%). Most other compar-
We therefore rest the cross-domain claim on B3              isons are descriptive; in our primary test, only
alone, with the caveat that 12 articles from a sin-         SR2 differs significantly from CCR. A facto-
gle source is a small sample.                               rial design that varies generator, reviewer model,
                                                            and context independently, and evaluation on es-
6     Discussion                                            tablished benchmarks such as FEVER (Thorne
6.1    Why Different Models Find Different                  et al., 2018), AVeriTeC (Schlichtkrull et al., 2023),
       Things                                               CUAD (Hendrycks et al., 2021), or LegalBench
                                                            (Guha et al., 2023), would test these patterns more
The partial non-overlap is consistent with several          directly.
explanations, though our design does not establish
causal mechanisms: training-data divergence (dif-           Limitations
ferent corpora, different standards), different capa-
bility profiles (the category reversal suggests code        Design. All artifacts came from a single generator,
review benefits from shared programming context,            and each capability tier is represented by one re-
document review from diverse perspectives), and             viewer model (three models from two developers),
model-specific knowledge gaps (cross-model re-              so reviewer capability and model identity are con-
viewers also flag non-errors from their own gaps;           founded. All cross-model conditions also include
Section 5.8).                                               context independence, so H4 (an interaction be-
   Kim et al. (2025) find strongly correlated errors        tween context and model independence) cannot be
on closed-ended benchmarks; our unions also fall            identified; a factorial design is left to future work.
below the independence reference (Section 5.2),                Data and measurement. The ground truth con-
so the partial non-overlap we observe should not            sists of planted errors written at injection time
be read as independent errors. Perspective diversi-         and was not independently annotated, and the
fication (B5) and three-model unions are discussed          matcher was not audited by hand. The same-
in Appendix E.1.                                            model baselines reuse data collected before the
                                                            cross-model conditions; their records cannot be
6.2    Practical Guidelines
                                                            checked against raw model output, and we treat
Based on our findings, we offer the following ten-          them as unverified rather than clean (Section 4.1).
tative guidance, limited to this sample of artifacts        The union comparison is retrospective: CCR runs
and reviewers. For maximum coverage, combine                differ widely (56, 37, and 29 matched errors),
same-model and cross-model review (56.7% vs.                the headline pairing is among the higher of the
42.7% for two same-model reviews at the same                reused run combinations, and whether the matcher
number of review calls; not significantly above             treats the reviewers’ output styles equally is un-
two top-tier cross-model reviews). For a sin-               measured. The per-error-type and per-category
gle best approach, use cross-model review with              comparisons are descriptive and were not tested
a top-tier reviewer (F1 32.1–32.3%; not signifi-            for significance.
cantly above CCR) at single-review cost. Prior-                Language. All artifacts and ground-truth an-
itize same-model review for code-heavy projects             notations are in Korean, and review output lan-
(F1 40.7% vs. 37.2% on code) and cross-model                guage was not fixed across conditions: in run 1,
review for documentation/consistency (F1 42.1%              20 of 30 CCR reviews are in English while the
vs. 24.5% on documents); avoid cross-model re-              other conditions’ reviews are mostly in Korean.
view with lightweight models (F1 24.0–27.0% vs.             Because the matcher’s keyword component com-
CCR 28.6%).                                                 pares findings with Korean ground-truth text (Ap-
                                                            pendix A), it may under-credit English-language
7     Conclusion
                                                            reviews. Other languages are untested.
We presented a four-dimensional framework for                  Generalization. The case studies are small: B1
independence in LLM verification and new ex-                and B2 showed ceiling effects, B3 has 12 arti-
periments on model independence. Across 900                 cles from a single source, and in B5 one model
sessions, CCR leads on code and XMR on docu-                returned no findings for one target. Our results
ments, and one CCR plus one XMR review cov-                 are a snapshot of early-2026 models. A partial
ers more ground-truth errors than two CCR re-               external-data check on ReaLMistake detector out-

                                                        9
puts (Appendix B) neither replicates nor contra-             business-day calculation, an LRU cache), ten tech-
dicts our main comparison.                                   nical tutorials (D1–D10; e.g., Docker Compose, a
                                                             FastAPI CRUD service, JWT authentication), and
Ethical Considerations                                       ten presentation scripts (S1–S10; talks on AI tool-
Improved verification can catch errors in AI-                ing, open data, and automation).
generated code and analysis before they cause                   Error injection and ground truth. Into each
harm, but over-reliance is a risk: even our union            artifact, exactly five errors were injected, one of
approach matches only 56.7% of the planted er-               each type (FACT, CONS, CTXT, RCVR, MISS),
rors under our automated matcher. We empha-                  giving 150 errors: 30 Critical, 60 Major, and 60
size that our framework is intended to augment,              Minor. According to our run logs, injection was
not replace, human review; the undetected planted            performed by the generator model in dedicated in-
errors and the model-bias false positives (Sec-              jection sessions. Each ground-truth record stores
tion 5.8) underscore the continued importance of             the location, the original and injected text, the
human judgment for high-stakes applications.                 type, the severity, a description, and the correct an-
                                                             swer. The records were written at injection time;
Use of AI Assistants                                         we did not run an independent annotation study,
                                                             so the ground truth is a set of planted errors rather
AI tools were used throughout this work, and
                                                             than an exhaustive list of all defects in each arti-
we report their use as part of the method.
                                                             fact.
The artifacts, the injected errors, and the same-
                                                                Matching. Each finding is scored against every
model baseline reviews were produced by Claude
                                                             ground-truth error of its artifact and assigned to
Opus 4.6 through the Claude Code agent tool;
                                                             the highest-scoring one if the score is at least 2.0:
the cross-model reviews were produced by the
                                                             +3 if a line number in the finding’s location equals
listed reviewer models through their APIs. Claude
                                                             one in the error’s location, otherwise +1 if any are
Code was also used to write the analysis and audit
                                                             within five lines; plus 4× the fraction of ground-
scripts, to recompute every reported number from
                                                             truth keywords (tokens of three or more characters
the per-session records, to check the manuscript
                                                             from the description, injected text, and correct an-
against the raw data (which led to the corrections
                                                             swer) that appear in the finding’s description; plus
described in Section 4.1), and to draft and revise
                                                             1 if the finding’s error type matches. Within one
substantial parts of the text under the author’s di-
                                                             review, each ground-truth error is credited at most
rection. Every reference was checked for exis-
                                                             once, in the order findings are listed. Unmatched
tence against bibliographic databases, and unre-
                                                             findings are counted as false positives, so preci-
solved entries were checked by hand. The author
                                                             sion and F1 are measured against the planted er-
reviewed the final text and takes full responsibility
                                                             rors only; a finding that correctly identifies a pre-
for all of its content.
                                                             existing defect also counts as a false positive. A lo-
Data and Code Availability                                   cation match alone (3 points) clears the threshold,
                                                             so the matcher can credit a finding that does not
The per-session review records, the 30 artifacts             identify the error; we did not audit match accuracy
with their 150 ground-truth defect annotations,              by hand. The keyword component is language-
and the matching, aggregation, and audit scripts             sensitive (see Limitations).
are available from the author on request. They in-              Statistics. Per-condition means in Table 2 av-
clude the per-session sets of detected ground-truth          erage the analysed sessions (n in the table). The
identifiers, which are what the union and Jaccard            primary test compares per-artifact means over the
figures in Section 5.2 are computed from, so every           available runs against CCR (Wilcoxon signed-
set-level number in this paper can be recomputed             rank, 30 pairs, Holm over nine comparisons); run-
independently.                                               1 paired t-tests are shown for comparison with the
                                                             original CCR report. Precision, recall, and F1 are
A   Benchmark, Ground Truth, and
                                                             computed per session and then averaged, so the
    Matching
                                                             reported F1 is not the harmonic mean of the re-
Artifacts. The generator produced 30 artifacts               ported precision and recall. Per-type recall uses
from fixed prompts, all in Korean: ten Python                each session’s single planted error of that type, so
functions or classes (C1–C10; e.g., CSV statistics,          no session has an empty denominator.

                                                        10
                                                               D     Values With Failed Sessions Scored as
                                                                     Zero
                                                               Table 5 compares the main per-condition F1 val-
                                                               ues with and without the exclusions of Section 4.1.
                                                               “All sessions” keeps SR run 3 and scores the 14
                                                               failed cross-model sessions as reviews with no
                                                               findings, which is how the values are computed
                                                               without the exclusions.
                                                                  Run-level F1 for the same-model conditions (30
Figure 2: F1 scores for all 10 conditions (ranked). The        artifacts each; runs 1/2/3) is: CCR 37.2/25.0/23.7,
asterisk marks the only condition significantly differ-        SR 25.7/28.6/(19.4, excluded), SA 23.8/20.8/26.9,
ent from CCR (SR2; Wilcoxon signed-rank on per-                and SR2 18.7/22.5/23.9. CCR ranks first among
artifact means over the available runs, Holm-adjusted          them in run 1 only, which is the run the original
p = 0.011); full statistics in Table 2.                        CCR report tested.

                                                                   Condition      All sessions   Excluded   n excl.
B    External-Data Check on ReaLMistake
                                                                   XMR-GPT            30.9         32.3       86
As a partial external-data check, we recomputed                    XMR-GPT-R          31.8         32.1       89
                                                                   XMR-GePro-R        29.0         29.0       90
the two-review-call comparison on the public de-                   CCR                28.6         28.6       90
tector outputs of ReaLMistake (Kamoi et al.,                       SR                 24.5         27.1       60
2024a), without new model calls. There, a “same-                   XMR-Ge-R           24.6         27.0       82
                                                                   XMR-GePro          26.8         26.8       90
model review” is the responder model detecting                     XMR-Ge             23.7         24.0       89
errors in its own responses, the two same-model                    SA                 23.8         23.8       90
reviews differ only in prompt wording (tempera-                    SR2                21.7         21.7       90
ture 0), and the cross-model partner is Claude 3
                                                               Table 5: F1 (%) with all 900 sessions and after the
Opus. The analysis plan was committed to our                   exclusions. With all sessions, the primary test against
version-controlled repository before the results               CCR (Holm over nine comparisons) finds only SR2 dif-
were computed (available on request). Pooled                   ferent (p = 0.011); SR’s unadjusted p is 0.021 (0.26
over three tasks and two responder models (649                 after excluding its run 3), and XMR-GPT vs. XMR-Ge
erroneous and 251 correct responses), union recall             has unadjusted p = 0.071 (0.020 after excluding fail-
of the mixed pair was not detectably different from            ures).
two same-model reviews (+0.5pp, 95% CI [−1.2,
2.2]; item bootstrap stratified by cell). In a post
hoc split by responder, mixing raised recall for
                                                               E     Additional Discussion
GPT-4 responses and lowered it for Llama-2-70B                 E.1    Beyond Two Models: Diminishing
responses, and in every cell the false-positive rate                  Returns
moved in the same direction as recall, so the split
                                                               Our primary analysis is pairwise, but adding a
is consistent with a shift in operating point rather
                                                               third reviewer model yields diminishing returns.
than with added coverage alone. Two Claude 3
                                                               In Experiment A, the three-model union (CCR ∪
Opus reviews did not consistently trail the mixed
                                                               XMR-GPT-R ∪ XMR-GePro-R) reaches 58.0%
pair, so the check does not separate model differ-
                                                               recall (run 1), only 1.3pp over the two-model
ence from reviewer capability. Because the unit
                                                               union (56.7%). In this setting, a third reviewer
(response-level binary labels), the source of vari-
                                                               adds little.
ation between same-model reviews, the domain,
and the detector generation (early 2024) all differ            E.2    Perspective Diversification
from our setting, this check neither replicates nor
                                                               Our B5 case study further shows that prompt
contradicts our main result.
                                                               perspective diversification produces partly non-
C    Additional Figure                                         overlapping findings even within one model,
                                                               though model diversification yields greater nov-
This figure presents the same data as Table 2 in               elty (Table 6); the architect perspective yields
graphical form.                                                the lowest inter-model overlap, suggesting that

                                                          11
design-level assessment may benefit most from                 B2: Economic recession identification. Simi-
different models. One model’s anomalous zero-              larly, all conditions reached 100% accuracy across
finding behavior cautions, however, that not all           6 tasks, correctly identifying all officially desig-
models respond uniformly to perspective varia-             nated recession periods; timing error was 0 months
tion.                                                      (same-model) and 0.2 months (cross-model).
                                                              B3: News fact-checking. To test generalization
F     Case Studies in Full                                 beyond software artifacts, we conducted a fact-
                                                           checking case study with 12 PolitiFact-verified ar-
F.1    Setup                                               ticles (43 ground-truth errors, 108 reviews). The
To assess generalizability beyond code review, we          reviewer conditions achieved F1 of 20.7% (CCR),
conduct five case studies (B5’s setup is given with        24.4% (XMR-GPT), and 23.8% (XMR-Ge), with
its results):                                              XMR-GPT highest in recall (76.7%, vs. 55.8%
   B1: Agricultural price anomaly detection.               for CCR and 51.2% for XMR-Ge); precision was
From national open-data agricultural auction               low (12.7–15.5%) in all conditions. The union re-
records (2022–2026, 1,155 trading days, 15 com-            call of CCR and XMR-GPT reached 86.0% (Jac-
modities), we flagged 15 candidate anomalies via           card 54.1%; 3-way union 88.4%). Because each
Z-score (|z| > 3) and IQR intersection and added           condition’s recall already pools its three runs, this
3 normal-range controls; one annotator labeled the         union pools six reviews against three and is not
candidates by hand (14 true anomalies, 1 uncer-            a matched-call comparison; we report it descrip-
tain). Both same-model and cross-model review-             tively.
ers analyzed each.                                            The fact-checking results resemble Experi-
                                                           ment A’s key patterns in a non-software domain:
   B2: Economic recession identification. Us-
                                                           in both settings the top-tier cross-model reviewer
ing macroeconomic time series (GDP growth, un-
                                                           has the highest individual F1 (Experiment A over-
employment, yield-curve spread, Sahm Rule in-
                                                           all 32.3% vs. CCR 28.6%, not significant; fact-
dicator; 1960–2025), we designed six tasks re-
                                                           check 24.4% vs. 20.7%, untested), and neither
quiring recession-period identification, with offi-
                                                           shows ceiling effects. The higher Jaccard in fact-
cial government-designated dates as ground truth.
                                                           checking (54.1% vs. 41.2%) may indicate that
   B3: News fact-checking. Using 12 PolitiFact-
                                                           some errors are detectable across models; the fact-
verified articles across six topic areas (ratings:
                                                           checking union (pooled over runs) is not compara-
Half True 4, Mostly False 3, False 3, Pants
                                                           ble with Experiment A’s call-matched union, and
on Fire 2), the generator analyzed each article’s
                                                           sample composition, detection rates, and match-
claims; three reviewer conditions (CCR, XMR-
                                                           ing also differ between the two settings, and B3
GPT, XMR-Ge) each reviewed all 12 three times
                                                           has only 12 articles.
(108 reviews total), against 43 ground-truth errors
                                                              Interpretation of B1, B2, and B3. B1 and
from PolitiFact’s analyses.
                                                           B2 do not discriminate between conditions. One
   B4: Meta case study—reviewing this paper’s
                                                           untested possibility is that differences appear only
code. We applied same-model review (fresh ses-
                                                           on judgment-intensive tasks; we did not manip-
sion) and cross-model review to the visualization
                                                           ulate or measure task difficulty. In these two
code written for this paper’s figures, providing
                                                           cases, where the signal was strong (extreme price
a qualitative illustration of the non-overlap mea-
                                                           spikes, well-documented recessions), every condi-
sured quantitatively in Experiment A.
                                                           tion we tested succeeded. The differences mea-
                                                           sured in Experiment A and B3, where review re-
F.2    Results
                                                           quires nuanced judgment about correctness, con-
B1: Agricultural anomaly detection. All condi-             sistency, and completeness, may represent the
tions classified all 17 cases with a definite label        regime where independence dimensions matter.
correctly (14 true anomalies and 3 normal con-             B3 suggests that this regime is not specific to soft-
trols); the one case the annotator marked uncertain        ware artifacts: fact-checking of news claims pro-
was treated the same way by every condition and is         duces similar qualitative patterns.
not scored. The anomalies involved extreme price              B4: Meta case study. Same-model and cross-
spikes (z > 3, increases of 42–138%) unambigu-             model review independently examined our visual-
ous to any capable model.                                  ization code (2 Python files, ∼600 lines): same-

                                                      12
 Comparison axis                  Mean Jaccard     Range            tive the highest (wren 0.208, cgltf 0.157), sug-
 Inter-perspective (same model)      0.228       0.143–0.331        gesting that exploit-oriented analysis follows rel-
 Inter-model (same perspective)      0.152       0.057–0.259
                                                                    atively standardized patterns across models while
Table 6: Perspective vs. model diversification Jaccard              design-level reasoning is more model-specific. In
overlap (lower means less overlap).                                 finding counts, perspective diversification within a
                                                                    single model yielded +98–118% additional find-
                                                                    ings via union, and model diversification within
model review found 15 issues (2 P1, 8 P2, 5 P3)                     a single perspective yielded +117%. These are
and the cross-model reviewer 6 (3 P1, 3 P2), with                   counts of findings, not validated defects, and we
4 in common (Jaccard = 4/17 = 23.5%). Same-                         did not measure the union across all nine model–
model review excelled at depth (subtle logic in-                    perspective combinations.
consistencies, convention violations), while the                       One anomaly limits generality: one model pro-
cross-model reviewer caught critical edge cases,                    duced zero findings for the smaller target (cgltf,
including a crash-inducing path missed entirely by                  3.1K lines) under the defender and architect per-
same-model review.                                                  spectives while functioning normally otherwise,
   In a second round reviewing this paper’s draft                   indicating that some models’ responsiveness to
text, same-model review found 27 issues and the                     perspective variation depends on target charac-
cross-model reviewer 15; we no longer have the                      teristics. Overall, perspective diversification is a
cluster-level records for this round and do not                     complementary, not competing, axis to model di-
report an overlap figure for it. The qualitative                    versification; while two targets are a limited sam-
pattern held: same-model review caught cross-                       ple, the consistent patterns suggest their combina-
referencing and framework-consistency errors, the                   tion may offer richer coverage than either alone.
cross-model reviewer flagged overclaiming and
source-traceability gaps. The code-review overlap
(23.5%), below the 41.2% in Experiment A, sug-                      References
gests overlap may vary with task characteristics,
                                                                    Chi-Min Chan, Weize Chen, Yusheng Su, Jianxuan Yu,
though B4 is a qualitative demonstration rather                       Wei Xue, Shanghang Zhang, Jie Fu, and Zhiyuan
than a statistical test.                                              Liu. 2024. ChatEval: Towards better LLM-based
   B5: Security audit perspective diversifica-                        evaluators through multi-agent debate. In Proceed-
tion. To test whether varying the perspective                         ings of ICLR 2024.
(rather than the model) produces independent
                                                                    Guiming Hardy Chen, Shunian Chen, Ziche Liu, Feng
value even within the same model, we conducted a                      Jiang, and Benyou Wang. 2024. Humans or LLMs
security audit on two C libraries (wren, 8.9K lines;                  as the judge? A study on judgement biases. In Pro-
cgltf, 3.1K lines) reviewed by three frontier mod-                    ceedings of EMNLP 2024.
els from distinct families under three perspectives:
                                                                    Liming Chen and Algirdas Avizienis. 1978. N-version
attacker (exploit-focused), defender (mitigation-
                                                                      programming: A fault-tolerance approach to reli-
focused), and architect (design-level). Findings                      ability of software operation. In Proceedings of
were matched by file, function, and CWE cate-                         FTCS-8, pages 3–9.
gory.
   Both diversification axes produce low overlap                    Wei-Lin Chiang, Lianmin Zheng, Ying Sheng, Anasta-
                                                                      sios N. Angelopoulos, Tianle Li, Dacheng Li, Hao
(Table 6), below the 41.2% CCR–XMR over-                              Zhang, Banghua Zhu, Michael Jordan, Joseph E.
lap observed in Experiment A, indicating partly                       Gonzalez, and Ion Stoica. 2024. Chatbot arena: An
non-overlapping findings; low overlap alone does                      open platform for evaluating LLMs by human pref-
not show that the additional findings are correct.                    erence. In Proceedings of ICML 2024.
Mean inter-model overlap is about a third lower
                                                                    Umut Cihan, Vahid Haratian, Arda İçöz, Mert Kaan
than inter-perspective overlap (J = 0.152 vs.                        Gül, Ömercan Devran, Emircan Furkan Bayendur,
0.228), consistent with changing the model pro-                      Baykal Mehmet Uçar, and Eray Tüzün. 2025. Au-
ducing more distinct findings than changing the                      tomated code review in practice. In Proceedings of
prompt alone.                                                        ICSE 2025 (SEIP).
   The architect (design-level) perspective pro-                    Thomas G. Dietterich. 2000. Ensemble methods in ma-
duces the lowest inter-model Jaccard (J = 0.075;                      chine learning. In Multiple Classifier Systems, pages
wren 0.082, cgltf 0.068) and the attacker perspec-                    1–15. Springer.


                                                               13
Sumanth Doddapaneni, Mohammed Safi Ur Rahman                  Haitao Li, Qian Dong, Junjie Chen, Huixue Su, Yu-
  Khan, Sshubam Verma, and Mitesh M. Khapra.                    jia Zhou, Qingyao Ai, Ziyi Ye, and Yiqun Liu.
  2024. Finding blind spots in evaluator LLMs with              2024. LLMs-as-judges: A comprehensive survey
  interpretable checklists. In Proceedings of EMNLP             on LLM-based evaluation methods. arXiv preprint
  2024, pages 16279–16309.                                      arXiv:2412.05579.

Yilun Du, Shuang Li, Antonio Torralba, Joshua B.              Zhiyu Li, Shuai Lu, Daya Guo, Nan Duan, Shailesh
   Tenenbaum, and Igor Mordatch. 2024. Improving                Jannu, Grant Jenks, Deep Majumder, Jared Green,
   factuality and reasoning in language models through          Alexey Svyatkovskiy, Shengyu Fu, and Neel Sun-
   multiagent debate. In Proceedings of ICML 2024.              daresan. 2022. Automating code review activi-
                                                                ties by large-scale pre-training. In Proceedings of
Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, and             ESEC/FSE 2022. ArXiv:2203.09095.
  Yarin Gal. 2024. Detecting hallucinations in large
  language models using semantic entropy. Nature,             Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang,
  630:625–630.                                                   Yan Wang, Rui Wang, Yujiu Yang, Shuming Shi,
                                                                 and Zhaopeng Tu. 2024. Encouraging divergent
Neel Guha, Julian Nyarko, Daniel E. Ho, and 1 others.            thinking in large language models through multi-
  2023. LegalBench: A collaboratively built bench-               agent debate. In Proceedings of EMNLP 2024.
  mark for measuring legal reasoning in large lan-
  guage models. In Proceedings of NeurIPS 2023.               Zicheng Lin, Zhibin Gou, Tian Liang, Ruilin Luo,
                                                                Haowei Liu, and Yujiu Yang. 2024. CriticBench:
Dan Hendrycks, Collin Burns, Anya Chen, and                     Benchmarking LLMs for critique-correct reasoning.
  Spencer Ball. 2021. CUAD: An expert-annotated                 In Findings of ACL 2024, pages 1552–1587.
  NLP dataset for legal contract review. In Proceed-
  ings of NeurIPS 2021.                                       Potsawee Manakul, Adian Liusie, and Mark J. F. Gales.
                                                                2023. SelfCheckGPT: Zero-resource black-box hal-
Sirui Hong, Mingchen Zhuge, Jiaqi Chen, Xiawu                   lucination detection for generative large language
   Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang,               models. In Proceedings of EMNLP 2023.
   Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang
   Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu,              OpenAI. 2026. codex-plugin-cc: Use Codex from
   and Jürgen Schmidhuber. 2024. MetaGPT: Meta                 Claude Code to review code or delegate tasks.
   programming for a multi-agent collaborative frame-           GitHub repository. GitHub repository. Accessed:
   work. In Proceedings of ICLR 2024.                           2026-09-30.

Jie Huang, Xinyun Chen, Swaroop Mishra,                       Arjun Panickssery, Samuel R. Bowman, and Shi Feng.
   Huaixiu Steven Zheng, Adams Wei Yu, Xiny-                    2024. LLM evaluators recognize and favor their
   ing Song, and Denny Zhou. 2024. Large language               own generations. In Proceedings of NeurIPS 2024.
   models cannot self-correct reasoning yet.   In
   Proceedings of ICLR 2024.                                  Chanathip Pornprasit and Chakkrit Tantithamthavorn.
                                                                2024. Fine-tuning and prompt engineering for large
Ryo Kamoi, Sarkar Snigdha Sarathi Das, Renze Lou,               language models-based code review automation. In-
  Jihyun Janice Ahn, Yilun Zhao, Xiaoxin Lu, Nan                formation and Software Technology, 175:107523.
  Zhang, Yusen Zhang, Ranran Haoran Zhang, Su-
  jeeth Reddy Vummanthala, Salika Dave, Shaobo                Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan
  Qin, Arman Cohan, Wenpeng Yin, and Rui Zhang.                 Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng
  2024a. Evaluating LLMs at detecting errors in LLM             Su, Xin Cong, Juyuan Xu, Dahai Li, Zhiyuan Liu,
  responses. In Proceedings of COLM 2024.                       and Maosong Sun. 2024. ChatDev: Communicative
                                                                agents for software development. In Proceedings of
Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han, and              ACL 2024.
  Rui Zhang. 2024b. When can LLMs actually cor-
  rect their own mistakes? A critical survey of self-         Michael Schlichtkrull, Zhijiang Guo, and Andreas Vla-
  correction of LLMs. Transactions of the Association           chos. 2023. AVeriTeC: A dataset for real-world
  for Computational Linguistics, 12.                            claim verification with evidence from the web. In
                                                                Proceedings of NeurIPS 2023.
Elliot Kim, Avi Garg, Kenny Peng, and Nikhil Garg.
   2025. Correlated errors in large language models.          Mrinank Sharma, Meg Tong, Tomasz Korbak, David
   In Proceedings of ICML 2025. ArXiv:2506.07962.               Duvenaud, Amanda Askell, Samuel R. Bow-
                                                                man, Newton Cheng, Esin Durmus, Zac Hatfield-
Seungone Kim, Juyoung Suk, Shayne Longpre,                      Dodds, Scott R. Johnston, Shauna Kravec, Timo-
  Bill Yuchen Lin, Jamin Shin, Sean Welleck, Graham             thy Maxwell, Sam McCandlish, Kamal Ndousse,
  Neubig, Moontae Lee, Kyungjae Lee, and Minjoon                Oliver Rausch, Nicholas Schiefer, Da Yan, Miranda
  Seo. 2024. Prometheus 2: An open source language              Zhang, and Ethan Perez. 2024. Towards understand-
  model specialized in evaluating other language mod-           ing sycophancy in language models. In Proceedings
  els. In Proceedings of EMNLP 2024.                            of ICLR 2024.


                                                         14
Hyungyu Shin, Jingyu Tang, Yoonjoo Lee, Nayoung
  Kim, Hyunseung Lim, Ji Yong Cho, Hwajung Hong,
  Moontae Lee, and Juho Kim. 2025. Mind the blind
  spots: A focus-level evaluation framework for LLM
  reviews. In Proceedings of EMNLP 2025.
Tae-Eun Song. 2026a. Cross-context review: Im-
  proving LLM output quality by separating pro-
  duction and review sessions.       arXiv preprint
  arXiv:2603.12123. Version 2 corrects version 1.
Tae-Eun Song. 2026b. Cross-context verification: Hi-
  erarchical detection of benchmark contamination
  through session-isolated analysis. arXiv preprint
  arXiv:2603.21454v2.
Tae-Eun Song. 2026c. More rounds, more noise: Why
  multi-turn review fails to improve cross-context ver-
  ification. arXiv preprint arXiv:2603.16244v1.
Selim Furkan Tekin, Fatih Ilhan, Tiansheng Huang, Si-
  hao Hu, and Ling Liu. 2024. LLM-TOPLA: Effi-
  cient LLM ensemble by maximising diversity. In
  Findings of EMNLP 2024.
James Thorne,      Andreas Vlachos,      Christos
  Christodoulopoulos, and Arpit Mittal. 2018.
  FEVER: A large-scale dataset for fact extraction
  and VERification. In Proceedings of NAACL-HLT
  2018.
Gladys Tyen, Hassan Mansoor, Victor Cărbune, Peter
  Chen, and Tony Mak. 2024. LLMs cannot find rea-
  soning errors, but can correct them given the error
  location. In Findings of ACL 2024, pages 13894–
  13908.
Junlin Wang, Jue Wang, Ben Athiwaratkun, Ce Zhang,
  and James Zou. 2024a. Mixture-of-agents enhances
  large language model capabilities. In Proceedings
  of ICLR 2025.
Peiyi Wang, Lei Li, Liang Chen, Zefan Cai, Dawei
  Zhu, Binghuai Lin, Yunbo Cao, Lingpeng Kong,
  Qi Liu, Tianyu Liu, and Zhifang Sui. 2024b. Large
  language models are not fair evaluators. In Proceed-
  ings of ACL 2024.
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
  Joseph E. Gonzalez, and Ion Stoica. 2023. Judg-
  ing LLM-as-a-judge with MT-Bench and Chatbot
  Arena. In Proceedings of NeurIPS 2023.




                                                          15
