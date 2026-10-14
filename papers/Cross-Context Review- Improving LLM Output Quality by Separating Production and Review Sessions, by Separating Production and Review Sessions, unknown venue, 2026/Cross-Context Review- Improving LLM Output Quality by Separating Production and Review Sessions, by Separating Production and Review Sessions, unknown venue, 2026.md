                                              Cross-Context Review: Improving LLM Output Quality
                                                  by Separating Production and Review Sessions

                                                                                Song Tae-Eun
                                                                      Daejeon Jungang Cheonggua Co., Ltd.
                                                                              higheun@gmail.com



                                                           Abstract                        nitpick formatting or suggest minor improve-
                                                                                           ments, but it rarely catches the substantive
                                            Large language models struggle to catch        errors.
arXiv:2603.12123v2 [cs.CL] 1 Oct 2026




                                            errors in their own outputs when the re-          This is not just anecdotal.        The self-
                                            view happens in the same session that pro-     correction literature documents the problem
                                            duced them. This paper introduces Cross-
                                                                                           from multiple angles. LLMs cannot reliably
                                            Context Review (CCR), a straightforward
                                            method where the review is conducted in        correct their own reasoning without external
                                            a fresh session with no access to the pro-     feedback (Huang et al., 2024b; Kamoi et al.,
                                            duction conversation history. We ran a         2024). They anchor on their initial outputs
                                            controlled experiment: 30 artifacts (code,     (Lou and Sun, 2025). And RLHF-trained
                                            technical documents, presentation scripts)     models tend toward agreement rather than
                                            with 150 injected errors, tested under four    criticism, likely driven in part by human pref-
                                            review conditions — same-session Self-
                                                                                           erence judgments, and rate their own outputs
                                            Review (SR), repeated Self-Review (SR2),
                                            context-aware Subagent Review (SA), and        higher than others’ (Sharma et al., 2024; Pan-
                                            Cross-Context Review (CCR). The cen-           ickssery et al., 2024).
                                            tral result is that a second review helps         We hypothesize that these failures share a
                                            only when it happens in a fresh session:       root cause that is easy to overlook: the pro-
                                            CCR (F1 28.6%) outperforms a second re-        duction context itself. When the model re-
                                            view in the same session (SR2, 21.7%)          views its output in the same session, the entire
                                            robustly, both in the first run (paired
                                                                                           conversation history sits in the context window
                                            t, p<0.001) and in the three-run average
                                            (Holm-adjusted p=0.004). This version
                                                                                           — the instructions, the intermediate reason-
                                            updates the broader comparisons. Aver-         ing, the design trade-offs. All of this anchors
                                            aged across runs, and excluding one SR run     the model’s judgment. It does not scrutinize;
                                            whose records could not be verified, CCR       it rationalizes.
                                            is not significantly ahead of context-aware       The fix is correspondingly simple: start a
                                            subagent review (SA, 23.8%; p=0.057) or        new session. Give the model only the final ar-
                                            of a single same-session review (SR, 27.1%;    tifact, with no production history, and ask it
                                            p=0.26); the first version’s advantages over
                                                                                           to review. We call this Cross-Context Review
                                            these two baselines came from run 1. CCR
                                            needs no infrastructure and costs one extra    (CCR). The idea maps directly onto practices
                                            session.                                       that humans have relied on for centuries —
                                                                                           code review by someone who did not write the
                                        1   Introduction                                   code, peer review by scientists who did not
                                                                                           run the experiment, editorial review by editors
                                        Anyone who has used an LLM to write code           who did not draft the manuscript. These prac-
                                        or documentation has probably tried the ob-        tices exist because creators are biased toward
                                        vious next step: asking the same model to re-      their own work. Our claim is that this princi-
                                        view what it just produced. It seems reason-       ple transfers to LLM workflows, with “differ-
                                        able. The model knows what you asked for,          ent person” replaced by “different session.”
                                        remembers the constraints, and has the full           This paper makes four contributions:
                                        context. But a pattern emerges quickly — the
                                        model tends to approve its own work. It might       1. We define CCR as a verification method
       based on session separation, grounding it      14 open-source non-reasoning models, the av-
       in the self-correction, anchoring, and con-    erage blind spot rate was 64.5%, consistent
       text degradation literature.                   across model families and scales. This find-
                                                      ing is directly relevant to CCR: same-session
    2. We design an experiment with four con-         review presents the artifact as “own output,”
       ditions (SR, SR2, SA, CCR) that disen-         triggering the blind spot, while CCR presents
       tangles context separation from repetition     it as external input, which we hypothesize re-
       and context awareness — two confounds          moves the trigger; we do not measure the blind
       that could otherwise explain the results.      spot directly.
                                                         The takeaway is clear: asking a model to
    3. CCR robustly outperforms repeated
                                                      fix its own work within the same context is
       same-session review (SR2), in the run-1
                                                      unreliable at best and harmful at worst. If
       test and in the three-run average. Its
                                                      the context is the problem, then changing the
       advantages over single-pass SR and
                                                      context is the natural intervention.
       context-aware SA, significant in run 1,
       are not significant across runs (Section 6).   2.2   Anchoring Bias and Sycophancy

    4. The SR2 condition — same-session re-           Two biases make self-correction even harder
       peated review — shows no evidence of im-       than it needs to be. LLMs exhibit anchoring
       proving over single-pass SR (run 1, p =        bias — initial information disproportionately
       0.11), and CCR outperforms it robustly.        shapes later judgments (Lou and Sun, 2025).
       Together these suggest that a second look      In a production session, the model’s first out-
       helps when it is taken in a fresh session;     put becomes the anchor for everything that
       the CCR–SR2 comparison also differs in         follows. Self-review is biased toward confirma-
       review language (Section 6).                   tion before it even begins.
                                                         Sycophancy compounds this.            RLHF-
2     Related Work                                    trained models tend to agree rather than chal-
                                                      lenge (Sharma et al., 2024), and they rate
Four lines of research motivate why same-             their own generations higher than compara-
session review fails and why breaking the ses-        ble text from other sources (Panickssery et al.,
sion should help.                                     2024). In multi-agent debate, Choi et al.
                                                      (2025) found that removing identity mark-
2.1     Self-Correction in LLMs                       ers substantially reduced identity-driven bias
Huang et al. (2024b) demonstrated that                (e.g., a conformity–obstinacy gap of 0.608
LLMs cannot correct their own reasoning               falling to 0.024 for one model on MMLU).
without external feedback — and that cor-             CCR is analogous in that the reviewing ses-
rection attempts can actually make things             sion is not told that the artifact was produced
worse. Kamoi et al. (2024) surveyed the               by the same model, although debate between
broader self-correction literature and reached        agents is a different setting from reviewing an
a blunt conclusion: no prior work demon-              artifact.
strates successful self-correction with feedback
from prompted LLMs, except in tasks excep-            2.3   Context Degradation
tionally suited for self-correction. Zhang et al.     Even setting aside biases, there is a mechan-
(2025) added a troubling dimension, finding           ical problem with long contexts. Liu et al.
that self-correction sometimes flips correct an-      (2024) documented the “lost in the middle”
swers to incorrect ones through prompt bias           effect: models attend more to the beginning
and cognitive-like biases in the correction pro-      and end of long contexts, underweighting the
cess.                                                 middle. Hong et al. (2025) quantified what
   Most recently, Tsui (2026) identified a strik-     they call “context rot” — performance that
ing phenomenon called the “self-correction            degrades as input length increases, often in
blind spot”: LLMs fail to correct errors in their     non-uniform ways, observed across 18 mod-
own outputs while successfully correcting iden-       els. Production sessions routinely accumulate
tical errors presented as external input. Across      50K+ tokens. At that scale, the model loses
track of early decisions while remaining an-        and design decisions.
chored to recent ones. A fresh session avoids          In the export phase, the final artifact is ex-
this entirely: the reviewer works with just the     tracted. The conversation history is discarded.
artifact, typically 5K tokens or less.              Only the artifact text carries over.
                                                       In the review phase, a new Session B
2.4    Multi-Agent and Role-Based                   starts from scratch. The reviewer receives
       Approaches                                   the artifact and a prompt asking it to check
Others have tackled verification through            five things: factual accuracy (are the num-
multi-agent debate (Du et al., 2024; Liang          bers and claims right?), internal consistency
et al., 2024), role specialization (Huang et al.,   (are there contradictions?), contextual fitness
2024a; Qian et al., 2024), and iterative self-      (would this actually work in its intended en-
refinement (Madaan et al., 2023). These ap-         vironment?), audience perspective (could a
proaches work, but they are heavy — mul-            reader misinterpret something?), and com-
tiple agents, orchestration layers, specialized     pleteness (is anything important missing?).
prompts. Self-Refine (Madaan et al., 2023)             In the integration phase, the review find-
stays within a single session and therefore in-     ings feed back into improving the artifact —
herits all the context biases described above.      either in the original session or a new one.
Multi-agent debate introduces disagreement
but requires running multiple model instances       3.3   Theoretical Motivation
simultaneously.                                     CCR addresses several failure modes at once.
   Kim et al. (2025) show that multi-turn           A fresh session has no prior decisions to an-
interviewer-style evaluation reduces verbosity      chor to. Independent context prevents the
bias and improves robustness across runs, but       confirmation loops that Liang et al. (2024)
do not separate production and review con-          call Degeneration of Thought. The review
texts — the interviewer operates within a sin-      session works with a short context (∼5K to-
gle continuous conversation throughout the          kens) rather than the bloated production con-
evaluation.                                         text (∼50K+ tokens). And because the re-
   CCR sits in a different part of the design       viewer is not told that it produced the arti-
space. It achieves context independence with        fact, we expect sycophancy and self-preference
minimal overhead: one additional session, no        to weaken, although we do not measure them.
infrastructure changes, no prompt engineer-
                                                    3.4   Distinction from Incubation
ing. It is also complementary — there is noth-
                                                          Effects
ing stopping someone from combining CCR
with role-based or multi-agent methods.             One might argue that CCR is just the LLM
                                                    version of incubation — the well-documented
3     Method: Cross-Context Review                  human phenomenon where stepping away
                                                    from a problem and returning later leads to
3.1    Definition
                                                    insight (Wallas, 1926). We think this is a cat-
Cross-Context Review (CCR) is a verification        egory error.
method where an LLM reviews an artifact in             LLMs have no temporal continuity between
a fresh session containing only the artifact and    sessions. A new session has zero memory of
a standardized review prompt. The reviewing         prior sessions, whether one second or one year
session has no access to the production ses-        has passed. CCR is not “taking a break.” It is
sion’s conversation history, intermediate rea-      an information-theoretic intervention: remov-
soning, or generation instructions.                 ing the production context from the reviewer’s
                                                    input. The mechanism is not rest or uncon-
3.2    Protocol                                     scious processing — LLMs have neither — but
The protocol has four phases.                       the elimination of anchoring information.
  In the production phase, a user interacts            This distinction is testable. If incubation
with an LLM to produce an artifact — code, a        were the mechanism, a delay within the same
document, a script — in Session A. The con-         session should help. Our SR2 condition adds
versation accumulates instructions, iterations,     a second review pass within the same context
(no delay, same history) and shows no im-                        in the same session, with the first review visi-
provement — pointing to information removal,                     ble. SA tests whether knowing the generation
not temporal separation, as the operative fac-                   prompt helps or hurts when the review hap-
tor.                                                             pens in a fresh context. CCR gets only the
                                                                 artifact, nothing else.
4     Experimental Setup
                                                                 4.3   Execution
4.1     Artifacts and Error Injection
                                                                 All reviews used Claude Opus 4.6 (model ID:
We generated 30 artifacts using Claude Opus
                                                                 claude-opus-4-6) via the Claude Code Agent
4.6 in three categories:
                                                                 tool — a subprocess mechanism that launches
    • Code (C1–C10): Python functions for                        independent LLM sessions within the Claude
      CSV processing, date calculations, JSON                    Code CLI. This is functionally equivalent to
      parsing, database operations, validation,                  a fresh API session: each Agent subprocess
      deep merge, log parsing, async HTTP,                       gets its own context window with no carry-
      LRU cache, and markdown parsing.                           over. Temperature and sampling parameters
                                                                 followed the Agent tool’s defaults. We con-
    • Documents (D1–D10): Technical tutori-                      trolled for stochasticity by running each con-
      als covering REST APIs, Docker, CI/CD,                     dition 3 times independently.
      FastAPI, SQLAlchemy, virtual environ-                         Each condition was applied to all 30 ar-
      ments, JWT authentication, Pandas opti-                    tifacts across 3 runs, yielding 4 × 30 ×
      mization, WebSocket, and MCP servers.                      3 = 360 reviews. Reviews ran in paral-
                                                                 lel batches of 6 agents.        We had origi-
    • Scripts (S1–S10): Presentation scripts
                                                                 nally planned to use the Anthropic API di-
      about AI coding tools, MCP explanation,
                                                                 rectly with claude-sonnet-4-6 (as specified
      public data, Python vs JavaScript, AI
                                                                 in our experiment configuration), but insuf-
      agents, open source, wholesale market AI,
                                                                 ficient API credits forced a switch to the
      automation pipelines, CLAUDE.md, and
                                                                 Agent tool, which uses the host session’s model
      the Korean AI ecosystem.
                                                                 (Opus 4.6). We report this deviation transpar-
   We injected exactly 5 errors into each ar-                    ently.
tifact — one per error type (FACT, CONS,                            All artifacts, ground-truth annotations, re-
CTXT, RCVR, MISS) — at three severity lev-                       view prompts, result files, and analysis scripts
els (Critical, Major, Minor), for a total of 150                 are available from the author on request. The
ground-truth errors. The errors were designed                    result files are structured records transcribed
to be plausible: runtime bugs and off-by-one                     by the host session and do not include raw
errors in code, factual inaccuracies and inter-                  model output (Section 6). Exact reproduction
nal contradictions in documents, incorrect at-                   requires access to the Claude Code Agent tool;
tributions and wrong numbers in scripts.                         the supplementary experiment_runner.py
                                                                 provides an equivalent API-based implemen-
4.2     Review Conditions                                        tation for researchers with API access.
We tested four automated review conditions:
                                                                 4.4   Evaluation Metrics
 Condition         Abbr.   Context             Purpose
                                                                 Each review produces a set of findings. We
 Self-Review       SR      Full history        Baseline
 Self-Review ×2    SR2     Full + 1st review   Repetition ctrl   match findings to ground-truth errors using
 Subagent Review
 Cross-Context
                   SA
                   CCR
                           Prompt + artifact
                           Artifact only
                                               Context ctrl
                                               Our method
                                                                 a scoring function based on location overlap
                                                                 (line number proximity within ±5 lines), key-
Table 1: Review conditions and their available con-              word overlap (Jaccard similarity of description
text.                                                            terms), and a bonus for matching error type.
                                                                 A finding counts as a true positive if its match-
  SR is what most people do: “please review                      ing score exceeds 2.0. From TP, FP, and FN
what you just wrote.” SR2 controls for the                       counts we compute Precision, Recall, and F1
possibility that CCR’s advantage comes from                      per artifact per condition. Statistical signifi-
simply looking twice — it gets a second pass                     cance comes from paired t-tests on per-artifact
F1 scores (Run 1, N =30), with Cohen’s d for                          Condition    Critical    Major       Minor
effect size.                                                          CCR           40%         29%         18%
                                                                      SR†           32%         32%         22%
5     Results                                                         SA            30%         23%         16%
                                                                      SR2           31%         26%         16%
5.1    Overall Performance
                                                                Table 4: Detection rate by severity († SR runs 1–2
Table 2 shows results averaged across all re-                   only; v1: 29/27/19%).
views per condition: 90 (3 runs × 30 artifacts),
except SR with 60 after the exclusion in Sec-
                                                                5.3    Detection by Severity
tion 6.
                                                                CCR’s advantage over SR appears only for
 Cond.   Finds    TP      FP    FN    Prec.     Rec.     F1     critical errors (40% vs 32%, an 8-point gap);
 CCR      4.5     1.4     3.1   3.6   31.5      27.1     28.6   SR is ahead on major (32% vs 29%) and mi-
 SR†
 SA
          5.6
          4.3
                  1.4
                  1.1
                          4.2
                          3.2
                                3.6
                                3.9
                                      26.2
                                      27.4
                                                28.3
                                                21.8
                                                         27.1
                                                         23.8
                                                                nor (22% vs 18%) errors. These are descrip-
 SR2      5.5     1.1     4.4   3.9   21.0      22.7     21.7   tive rates without significance tests. Figure 2
                                                                illustrates the severity-dependent pattern.
Table 2: Overall results (N =90 per condition;
†
  SR uses runs 1–2 only, N =60, Section 6; v1                   5.4    Performance by Artifact Category
values with run 3: F1 24.5, Prec. 25.8, Rec.
24.2). Finds/TP/FP/FN are per-artifact averages;
                                                                  Category        CCR     SR          SA     SR2
Prec./Rec./F1 in %.
                                                                  Code          40.7%    37.0%      34.1%    31.9%
                                                                  Document      24.5%    22.3%      17.4%    19.2%
   CCR leads on F1 and precision; SR has                          Script        20.7%    22.1%      19.9%    14.0%
slightly higher recall. The SR2 numbers tell
an interesting story: the second review pass                    Table 5: F1 by artifact category (3-run average;
                                                                SR runs 1–2 only; v1 SR: 36.0/18.2/19.5%).
has substantially worse precision than single-
pass SR (21.0% vs 26.2%). The model is gen-
                                                                   CCR leads on code (+3.7 F1 points over
erating more noise, not more signal. Figure 1
                                                                SR) and documents (+2.2), and SR leads on
visualizes F1 across conditions and categories.
                                                                scripts (22.1% vs 20.7%). This makes sense:
5.2    Statistical Tests                                        code review benefits particularly from a “fresh
                                                                eyes” perspective that questions implementa-
Table 3 reports paired t-tests on per-artifact                  tion assumptions rather than accepting them
F1 from Run 1 (N =30), as in the first version;                 as given. SR2 performs notably poorly on
the robustness test on three-run averages is in                 scripts (14.0%), suggesting that repeated re-
Section 6.                                                      view within the same session is especially
                                                                counterproductive for subjective content.
 Comparison        t            p     Cohen’s d         Sig.
 SR vs CCR       −2.849      0.008       0.52          Yes**    5.5    Detection by Error Type
 SR2 vs CCR      −3.917     <0.001      0.72           Yes***
 SA vs CCR       −3.119      0.004      0.57           Yes**
 SR vs SR2       1.665       0.107      −0.30           No       Cond.   FACT     CONS    CTXT        RCVR    MISS
                                                                 CCR      48%      37%        13%      19%        19%
Table 3: Statistical comparisons (paired t-test,                 SR†      50%      35%        18%      18%        20%
Run 1). t is computed as the first minus the second              SA       41%      31%         9%      14%        13%
                                                                 SR2      40%      31%        16%      12%        14%
condition in each row; Cohen’s d is dz , the mean
paired difference (second minus first) divided by its
                                                                Table 6: Detection rate by error type (N =90
standard deviation.
                                                                per cell; † SR N =60, runs 1–2; v1 SR:
                                                                44/32/12/16/17%).
   In run 1, every comparison against CCR is
significant at p < 0.01, with medium-to-large                     Factual errors (FACT) are the easiest to
effect sizes (d = 0.52–0.72), and SR vs SR2                     catch across all conditions, which is unsurpris-
is not significant (p = 0.11). These run-1 re-                  ing — they are the most concrete. Contextual
sults do not hold across runs for SR and SA                     errors (CTXT) are the hardest, topping out at
(Section 6).                                                    18% (SR). CCR has the highest detection rate
                                                      The central SR2 result holds; two findings nar-
                                                      row the broader comparisons.
                                                         Provenance of SR run 3. The review
                                                      records were produced through the Claude
                                                      Code agent tool and transcribed into struc-
                                                      tured files by the host session; they do not
                                                      include raw model output. For SR run 3, 92%
                                                      of the finding descriptions appear verbatim in-
                                                      side the script that wrote the result files, so we
                                                      cannot confirm that they are unedited model
Figure 1: F1 scores by condition and artifact cate-   output. We exclude this run; the SR values
gory (3-run average; SR runs 1–2 only). CCR leads
                                                      in Tables 2–6 use runs 1 and 2 (N =60). Its
on code and documents; SR leads on scripts.
                                                      F1 (19.4%) was well below SR’s other runs
                                                      (25.7% and 28.6%). The other runs are un-
                                                      verified rather than known to be clean.
                                                         Run-to-run variation. The first version
                                                      tested run 1 only and stated that the ranking
                                                      held in all three runs. Table 7 shows that CCR
                                                      ranks first in run 1 only.

                                                          Cond.    Run 1     Run 2        Run 3
                                                          CCR       37.2      25.0          23.7
                                                          SR        25.7      28.6    (19.4, excluded)
                                                          SA        23.8      20.8          26.9
Figure 2: Detection rate by error severity (SR runs       SR2       18.7      22.5          23.9
1–2 only). CCR is ahead of SR only on Critical
errors (+8pp); SR is ahead on Major and Minor         Table 7: F1 (%) per run, averaged over 30 artifacts.
errors. Descriptive, not tested.
                                                         Robustness test. Averaging each arti-
for two of five types (CONS and RCVR), and            fact’s F1 over its available runs and compar-
SR for the other three; the differences between       ing with CCR by Wilcoxon signed-rank tests
CCR and SR are within 6 points on every type          (Holm-adjusted over three comparisons): SR2
and were not tested.                                  p=0.004, SA p=0.057, SR p=0.26. With SR
                                                      run 3 included, all three would be significant
  One anomaly: SR2 detects more CTXT er-
                                                      (p=0.004, 0.043, 0.043), which is why the ex-
rors than CCR (16% vs 13%) but has the low-
                                                      clusion matters.
est RCVR detection (12%). It appears that
                                                         What holds. Reviewing again in the same
repeated review within the same context shifts
                                                      session (SR2) is worse than reviewing in a
attention between error types rather than im-
                                                      fresh session (CCR), in the run-1 test and in
proving detection overall — a shuffling rather
                                                      the three-run average (in run 3 alone the two
than an amplification, although this is a hy-
                                                      are level). What is narrowed. Whether a
pothesis and we did not track individual errors
                                                      fresh-session review outperforms a single self-
across passes.
                                                      review is not established by these data, and
5.6    Reproducibility Across Runs                    the per-category, per-severity, and per-type
                                                      advantages over SR reported in the first ver-
The first version stated that the ranking CCR
                                                      sion do not hold after the update. The run-1
> SR ≈ SA > SR2 holds in all three runs.
                                                      tests in Table 3 are unchanged and reported
That statement was not accurate: CCR ranks
                                                      for continuity.
first in run 1 only (Table 7).
                                                         Citation corrections. We also checked ev-
6     Update in Version 2                             ery citation against its source. The first ver-
                                                      sion attributed to Tsui (2026) a rise in the
We re-examined the per-session records of this        blind-spot rate with task complexity (45.2% to
experiment while reusing them in later work.          79.2%); these figures do not appear in that pa-
per, which reports a 64.5% average that is con-    text (SR2) does not improve on a single re-
sistent across model families and scales, and      view (run 1, p=0.11), while a second review
we have removed them. We also corrected the        in a fresh session (CCR) robustly outperforms
description of Choi et al. (2025), added a qual-   SR2 (run 1 p<0.001; three-run Holm-adjusted
ifier to the summary of Kamoi et al. (2024),       p=0.004). The difference between SR2 and
and corrected author lists and publication de-     CCR is not repetition — both involve review-
tails in the bibliography.                         ing again — but context. However, CCR does
                                                   not robustly outperform a single same-session
7     Discussion                                   review (SR), so the data show that context
                                                   separation rescues a second look, not that it
7.1    Why Context Separation Works
                                                   beats looking once. Review language also dif-
The results line up with the prediction that       fers between CCR (English) and SR2 (Ko-
production context introduces systematic bias.     rean), so even this comparison is not a clean
But the SR2 result is what makes the argu-         isolation of context (see Limitations).
ment tight. Reviewing twice in the same ses-          This is a more limited claim than the first
sion shows no evidence of helping, and its pre-    version made.
cision is lower than single-pass SR (21.0% vs
26.2%), consistent with a second pass that         7.3   Practical Implications
adds findings rather than reconsidering the        CCR requires nothing special. No multi-
first assessment; we did not analyse the added     ple models, no orchestration framework, no
findings. The model “tries harder” by adding       prompt engineering. Start a new session, paste
noise. This is consistent with what Zhang          the artifact, ask for a review. That is the en-
et al. (2025) observed: self-correction within     tire method.
a fixed context can degrade initially correct         This makes it immediately applicable:
judgments.
   The SA result adds another dimension.            • In software development, review gener-
Knowing the generation prompt — under-                ated code in a new session before com-
standing what the user originally asked for —         mitting.
does not improve review quality. If anything,
it slightly hurts (SA F1 23.8% vs SR 27.1%;         • For content creation, verify articles or
not tested). One possible reading is that the         documentation independently of the ses-
anchoring effect operates through the presence        sion that produced them.
of production-related context rather than its       • In multi-agent pipelines, route artifacts
content, but SA and SR also differ in session         through an independent review agent as
and review language, so this is a hypothesis.         a standard stage.
Even well-intentioned context (“here is what
the user wanted”) triggers the same bias pat-        The cost overhead is small. A review session
terns.                                             processes ∼5K tokens (the artifact plus the re-
                                                   view prompt), compared to 50K+ tokens in a
7.2    The SR2 Result and Why It
                                                   typical production session. In many cases, the
       Matters
                                                   review session is actually cheaper than contin-
SR2 deserves its own subsection because it         uing in the production session would be.
serves a critical role as a confound control.
   Without SR2, a reader could reasonably at-      7.4   Connection to Human Review
tribute CCR’s advantage to a “two looks are              Practices
better than one” effect. After all, CCR ef-        The analogy to human review practices is not
fectively gives the model a second chance at       decorative — it is structural. Code review,
review, just in a different session. Maybe any     peer review, and editorial review all exist be-
second review would help, regardless of con-       cause the person who created something can-
text.                                              not evaluate it objectively. The creator knows
   Our data support a narrower version of this     too much: the intent behind ambiguous code,
argument. A second review in the same con-         the reasoning behind an unusual claim, the
context that makes a missing section seem ac-     guage), while CCR and SA reviewed in English
ceptable. A reviewer who lacks this context is    (the default for a fresh context with no prior
forced to engage with the artifact on its own     language cue). English-language reviews may
terms.                                            benefit from stronger reasoning in the model’s
   CCR reproduces this dynamic for LLMs.          dominant training language. We note, how-
The reviewing session does not know the in-       ever, that SA also reviews in English yet un-
tent, the reasoning, or the production context.   derperforms CCR, so language alone does not
It can only evaluate what is actually written.    explain the full effect.
Our results show this to be a better starting        Our artifacts span three types within a sin-
point than a second review in the same ses-       gle domain (software engineering tutorials in
sion; whether it beats a single self-review is    Korean). We have not tested legal documents,
not established.                                  medical reports, or scientific manuscripts. The
                                                  method should generalize — the theoretical
8   Limitations                                   basis applies to any context-dependent review
                                                  — but this remains to be shown.
We used a single model (Claude Opus 4.6).
                                                     Two further limitations were identified in
The theoretical motivation is model-agnostic
                                                  the audit for this version. First, the review
— anchoring, context rot, and sycophancy
                                                  records do not include raw model output, and
are documented across model families — but
                                                  one run was excluded for uncertain provenance
empirical validation on GPT-4, Gemini, and
                                                  (Section 6). Second, the matcher’s keyword
open-source models would strengthen the gen-
                                                  component compares findings with Korean
eralizability claim.
                                                  ground-truth text, so the English-language re-
   The errors were deliberately injected, not
                                                  views (CCR and SA) may be under-credited
naturally occurring. This allows precise mea-
                                                  relative to the Korean-language ones (SR and
surement but may not reflect real-world er-
                                                  SR2); the direction of the language confound
ror distributions. A preliminary case study
                                                  above is therefore uncertain.
with natural errors (supplementary Section
4A) provides some ecological validity.            9   Future Directions
   The absolute F1 numbers are moderate —
28.6% for the best condition. This may re-        CCR as presented here is a static, single-pass
flect the difficulty of the task, the matcher,    method: the reviewer examines the artifact
or the model; we did not separate these. All      once and produces findings. Two directions
conditions face the same task, so we focus on     extend this naturally.
relative differences.                                First, dynamic CCR could incorporate
   Our matching algorithm uses heuristic scor-    multi-turn interaction between reviewer and
ing (location proximity + keyword overlap).       author. Kim et al. (2025) demonstrate with
We validated the threshold empirically, but       LLM-as-an-Interviewer that dynamic, multi-
different matching methods would produce dif-     turn evaluation — where the evaluator asks
ferent absolute numbers. We did not report a      follow-up questions and probes weak points
threshold sensitivity analysis, and we have not   — reveals failure modes that static assess-
repeated one for this version.                    ment misses. Combining CCR’s context sepa-
   We did not run a human review baseline in      ration with interviewer-style follow-up (“Why
the quantitative experiment. Expert human         did you choose this approach? What happens
review across 30 diverse artifacts would be the   if the input is empty?”) could capture errors
ideal upper bound, but the labor cost was pro-    that a single-pass review misses while preserv-
hibitive for this study. Future work should in-   ing the independence that makes CCR effec-
clude it.                                         tive.
   There is a language confound. The arti-           Second, hierarchical CCR could scale the
facts and ground truth are in Korean, but the     method beyond pairwise review. Our meta-
review conditions produced output in differ-      validation (Appendix D) already shows that
ent languages: SR and SR2 reviewed in Ko-         successive independent reviews catch qualita-
rean (following the production session’s lan-     tively different error types. A layered architec-
ture — workers producing artifacts, indepen-       Yilun Du, Shuang Li, Antonio Torralba, Joshua B.
dent verifiers reviewing them, and integrators       Tenenbaum, and Igor Mordatch. 2024. Improv-
                                                     ing factuality and reasoning in language models
synthesizing findings — would formalize this
                                                     through multiagent debate. In Proceedings of
into a systematic verification pipeline. We ex-      the 41st International Conference on Machine
plore this direction in ongoing work.                Learning (ICML 2024), pages 11733–11763.

10   Ethics Statement                              Kelly Hong, Anton Troynikov, and Jeff Huber.
                                                     2025. Context rot: How increasing input to-
This research studies LLM behavior and does          kens impacts LLM performance. Technical re-
not involve human subjects. The artifacts are        port, Chroma Research.
synthetic. We note that CCR, like any auto-        Dong Huang, Jie M. Zhang, Michael Luck, Qing-
mated review method, can produce false pos-          wen Bu, Yuhao Qing, and Heming Cui. 2024a.
itives that might mislead users. We recom-           AgentCoder: Multi-agent-based code generation
                                                     with iterative testing and optimisation. arXiv
mend it as a supplement to human judgment,           preprint arXiv:2312.13010.
not a replacement, especially in safety-critical
applications.                                      Jie Huang, Xinyun Chen, Swaroop Mishra,
                                                      Huaixiu Steven Zheng, Adams Wei Yu, Xiny-
Use of AI Assistants                                  ing Song, and Denny Zhou. 2024b. Large lan-
                                                      guage models cannot self-correct reasoning yet.
The artifacts, injected errors, and all reviews       In Proceedings of the 12th International Confer-
were produced by Claude Opus 4.6 through              ence on Learning Representations (ICLR 2024).
the Claude Code agent tool, as described in        Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han,
Section 6. Claude Code was also used to write        and Rui Zhang. 2024. When can LLMs actu-
the analysis scripts, to recompute the numbers       ally correct their own mistakes? A critical sur-
                                                     vey of self-correction of LLMs. Transactions of
in this version from the per-session records,        the Association for Computational Linguistics
and to draft and revise text under the author’s      (TACL), 12:1417–1440.
direction. The author reviewed the final text
                                                   Eunsu Kim, Juyoung Suk, Seungone Kim, Niklas
and takes full responsibility for its content.       Muennighoff, Dongkwan Kim, and Alice Oh.
                                                     2025. LLM-as-an-interviewer: Beyond static
11   Conclusion                                      testing through dynamic LLM evaluation. In
                                                     Findings of the Association for Computational
We introduced Cross-Context Review, a                Linguistics: ACL 2025, pages 26456–26493.
method that improves LLM verification by
separating production and review into inde-        Tian Liang, Zhiwei He, Wenxiang Jiao, Xing
pendent sessions. In a controlled experiment,        Wang, Yan Wang, Rui Wang, Yujiu Yang,
                                                     Shuming Shi, and Zhaopeng Tu. 2024. Encour-
a second review in a fresh session robustly out-     aging divergent thinking in large language mod-
performed a second review in the same session,       els through multi-agent debate. In Proceedings
in the run-1 test and in the three-run average.      of the 2024 Conference on Empirical Methods
The first version’s broader advantages over          in Natural Language Processing (EMNLP 2024),
                                                     pages 17889–17904.
single-pass and subagent review came from one
run and are not significant across runs. Within    Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin
this setting (one model, synthetic Korean arti-      Paranjape, Michele Bevilacqua, Fabio Petroni,
                                                     and Percy Liang. 2024. Lost in the middle: How
facts, planted errors), the practical message is     language models use long contexts. Transac-
narrower: if a second review is wanted, a fresh      tions of the Association for Computational Lin-
session is the better place for it.                  guistics (TACL), 12:157–173.
   The method is simple to adopt: copy the
                                                   Jiaxu Lou and Yifan Sun. 2025. Anchoring bias
output into a new session and ask for a review        in large language models: An experimental
there.                                                study. Journal of Computational Social Science,
                                                      9(1):11.

References                                         Aman Madaan, Niket Tandon, Prakhar Gupta,
                                                    Skyler Hallinan, Luyu Gao, Sarah Wiegr-
Hyeong Kyu Choi, Xiaojin Zhu, and Sharon Li.        effe, Uri Alon, Nouha Dziri, Shrimai Prabhu-
  2025. When identity skews debate: Anonymiza-      moye, Yiming Yang, Shashank Gupta, Bod-
  tion for bias-reduced multi-agent reasoning.      hisattwa Prasad Majumder, Katherine Her-
  arXiv preprint arXiv:2510.07517.                  mann, Sean Welleck, Amir Yazdanbakhsh, and
    Peter Clark. 2023. Self-refine: Iterative refine-      environment?
    ment with self-feedback. In Proceedings of the      4. Audience perspective: Could the
    37th Conference on Neural Information Process-
                                                           target reader misinterpret any part?
    ing Systems (NeurIPS 2023).
                                                        5. Completeness: Is anything important
Arjun Panickssery, Samuel R. Bowman, and Shi               missing?
  Feng. 2024. LLM evaluators recognize and fa-
  vor their own generations. In Proceedings of the
  38th Conference on Neural Information Process-
                                                        For each issue found, provide:
  ing Systems (NeurIPS 2024).                           - Location (line number or section)
                                                        - Description of the error
Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen,            - Type (FACT/CONS/CTXT/RCVR/MISS)
  Yufan Dang, Jiahao Li, Cheng Yang, Weize
  Chen, Yusheng Su, Xin Cong, Juyuan Xu, Da-
                                                        - Severity (Critical/Major/Minor)
  hai Li, Zhiyuan Liu, and Maosong Sun. 2024.           - Suggested fix
  ChatDev: Communicative agents for software
  development. In Proceedings of the 62nd Annual        B    Error Taxonomy
  Meeting of the Association for Computational
  Linguistics (ACL 2024), pages 15174–15186.
                                                         Type           Code    Description
Mrinank Sharma, Meg Tong, Tomasz Korbak,                 Factual        FACT    Wrong numbers/claims
 David Duvenaud, Amanda Askell, Samuel R.                Consistency    CONS    Internal contradictions
 Bowman, Newton Cheng, Esin Durmus, Zac                  Contextual     CTXT    Environment issues
 Hatfield-Dodds, Scott R. Johnston, Shauna               Audience       RCVR    Reader misinterpretation
 Kravec, Timothy Maxwell, Sam McCandlish,                Completeness   MISS    Important omission
 Kamal Ndousse, Oliver Rausch, Nicholas
 Schiefer, Da Yan, Miranda Zhang, and Ethan             Table 8: Error taxonomy used in ground-truth an-
 Perez. 2024.    Towards understanding syco-            notation.
 phancy in language models. In Proceedings of
 the 12th International Conference on Learning
 Representations (ICLR 2024).                           C    Ground Truth Examples
Ken Tsui. 2026. Self-correction bench: Uncov-           Representative errors from each category,
  ering and addressing the self-correction blind        showing the injection methodology. See sup-
  spot in large language models. In Confer-             plementary materials for the complete set.
  ence on Language Modeling (COLM 2026).
  ArXiv:2507.02778v3.                                   Code (C2 — Korean Business Day
                                                        Calculator): GT-C2-1 (FACT, Critical):
Graham Wallas. 1926.         The Art of Thought.
  Jonathan Cape.                                        weekday() >= 6 checks Sunday only instead
                                                        of >= 5 (Saturday+Sunday).     Saturdays
Qingjie Zhang, Di Wang, Haoting Qian, Yiming            counted as business days.
  Li, Tianwei Zhang, Minlie Huang, Ke Xu, Hewu
  Li, Yan Liu, and Han Qiu. 2025. Understanding         Document (D7 — JWT Authen-
  the dark side of LLMs’ intrinsic self-correction.     tication): GT-D7-1       (FACT,       Criti-
  In Proceedings of the 63rd Annual Meeting of the
  Association for Computational Linguistics (ACL        cal):   create_refresh_token signs with
  2025).                                                SECRET_KEY instead of REFRESH_SECRET_KEY
                                                        — access and refresh tokens share the same
A      Review Prompt Template                           signing key.
Review the following [artifact type]                    Script (S2 — MCP Explained): GT-S2-
from a fresh perspective:                               1 (FACT, Critical): MCP attributed to Ope-
                                                        nAI instead of Anthropic — fundamental fac-
1. Factual accuracy: Are numbers,                       tual error about protocol creator.
   names, dates, and technical claims
                                                        D    Meta-Validation — Recursive
   correct?
                                                             CCR in Practice
2. Internal consistency: Are there
   contradictions or terminology                        This paper was itself produced and validated
   mismatches?                                          through multiple rounds of Cross-Context Re-
3. Contextual fitness: Would this work                  view — an unplanned but informative demon-
   correctly in its intended                            stration of the method in practice.
   The initial draft was written in one terminal
session (T1). A separate session (T2) reviewed
the draft without access to T1’s conversation
history and identified 15 errors: 2 critical (nu-
merical inconsistencies between the abstract
and results tables), 7 major, and 6 minor. The
critical errors were exactly the kind of consis-
tency errors that same-session review tends to
miss — the author “knows” the numbers are
right because they just wrote them.
   After incorporating T2’s corrections, a
fourth independent session (T4) performed a
second-level review focused on reference veri-
fication. T4 discovered that 7 of 15 reference
entries contained fabricated or incorrect au-
thor names — 3 with hallucinated co-authors
and 4 with wrong initials — plus 3 missing ref-
erences for works cited in the text. That is 10
reference-related errors that T2’s thorough re-
view had not caught. T2 checked the numbers,
the logic, and the structure, but did not ques-
tion whether the reference authors were real.
The specific failure mode — hallucinated refer-
ence authors surviving two prior review rounds
— is consistent with the possibility that mod-
els tend not to question the factual accuracy of
academic citations, likely because they cannot
verify them without external tools. Each inde-
pendent context brought a genuinely different
perspective.

 Round    Reviewer    Errors   Types
 CCR-1    T2            15     Numerical, sections
 CCR-2    T4            10     Authors, refs

Table 9: Meta-validation: recursive CCR on this
paper.

  The T4 round shows diminishing but non-
zero returns from additional CCR passes.
CCR-1 catches the most errors (15), but CCR-
2 catches a qualitatively different class of er-
rors (reference fabrication) that CCR-1 missed
entirely. This meta-validation chain mirrors
the recursive CCR depth experiment proposed
in our future work ; with no count of remain-
ing errors, it does not show how many rounds
are enough.
