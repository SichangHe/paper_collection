                                         Accepted at MRL@EMNLP 2026




                                                                    Does CoT-Pass@k Really Check the CoT?
                                                                      A Multilingual Mathematical Audit

                                                      Tarık Tuna Taşaltı1,2 Burcu Hüdaverdi1 David Semedo2
                                                                  1
                                                                    Dokuz Eylül University, İzmir, Türkiye
                                         2
                                           NOVA School of Science and Technology, Universidade NOVA de Lisboa, Caparica, Portugal
                                                                   tasaltitariktuna@gmail.com



                                                                Abstract                             can reach under repeated sampling, and it anchors
                                                                                                     the current debate on whether reinforcement learn-
                                             Pass@k measures whether a model reaches a
arXiv:2609.32622v1 [cs.CL] 26 Sep 2026




                                             correct answer under repeated sampling, but             ing with verifiable rewards extends or merely sharp-
                                             never how: a lucky guess counts the same as             ens a base model’s reasoning. But Pass@k never
                                             sound reasoning. CoT-Pass@k was proposed                looks at how the answer was reached: a lucky guess
                                             to close that gap, adding an LLM-as-judge that          and sound reasoning count the same.
                                             must assess a solution’s reasoning chain before             CoT-Pass@k (Wen et al., 2026) was proposed
                                             it counts. Its value rests entirely on one assump-      to close exactly this hole. An LLM judge assesses
                                             tion: that the judge catches flawed reasoning.
                                                                                                     each correct solution and must approve the reason-
                                             That assumption has never been tested inside
                                             the metric that depends on it, and never outside        ing chain before the solution counts, so the met-
                                             English, though the metric’s claims concern             ric promises to separate models that reason from
                                             models used in many languages. We report the            models that guess. The promise rests entirely on
                                             first audit of that verification step, run under the    one assumption: the judge actually assesses the
                                             metric’s own protocol on a multilingual suite           chain. That assumption is testable; the literature
                                             of five mathematical benchmarks in English,             on reasoning-error detection gives ample reason to
                                             Turkish and Portuguese, two of them natively            doubt it: verifiers are weak at exactly the step-level
                                             written. We corrupt correct solutions with de-
                                                                                                     judgments the metric needs (Jacovi et al., 2024;
                                             terministic edits that damage the chain and the
                                             final answer separately. We observe that all            Zheng et al., 2025), step-level error identification
                                             three judges accept corrupted chains almost as          is generally harder than solution-level for every
                                             often as clean ones. V4-Flash and Qwen3.6               method tested (Xia et al., 2025), weaker still on
                                             reject a solution sharply only when its final an-       long chains (He et al., 2025), and prone to credit-
                                             swer is wrong and accept a wrong answer more            ing reasoning that merely looks valid (Wang et al.,
                                             readily when the chain agrees with it; the met-         2025b).
                                             ric’s own judge accepts most wrong answers as
                                                                                                         In this paper, we audit CoT-Pass@k under its
                                             well. Our study shows that chain–answer agree-
                                             ment dominates the two larger judges’ verdicts          own protocol, comprising the original judge prompt
                                             and that all three fail to reliably detect the tested   (Figure 3), three judgments per solution and the
                                             reasoning errors. Consequently the difference           original verification strategies, with controlled er-
                                             Pass@k − CoT-Pass@k averages 19.7 points                ror injection: deterministic edits that corrupt a so-
                                             on an earlier solver generation but only 4.1 on         lution’s reasoning chain and its final answer sepa-
                                             the current one. What little remains depends            rately (Section 4.2). The audit runs on five mathe-
                                             on the token budgets on both sides and on the           matical benchmarks in three languages, including
                                             generation mode; raising the generation bud-
                                                                                                     native Turkish and Portuguese sets (Section 3): the
                                             get moves Pass@64 by more than fifty points
                                             while the difference stays at zero. We close            metric is applied to models used far beyond En-
                                             with two checks any judged reasoning metric             glish, and its judge has only ever been measured in
                                             should pass before its numbers are read as evi-         it.
                                             dence about reasoning.                                      The audit returns a clear mechanism, and the
                                                                                                     mechanism predicts the metric’s behaviour. Ac-
                                         1   Introduction
                                                                                                     ceptance barely moves when we corrupt the chain
                                         Pass@k measures whether any of k sampled gener-             under any judge. Under V4-Flash and Qwen3.6
                                         ations answers a question correctly. It has become          it collapses when the final answer is wrong and
                                         the standard instrument for mapping what a model            rises again when that wrong answer is carried con-
Accepted at MRL@EMNLP 2026



sistently throughout the chain, so chain–answer           budget (Brown et al., 2024), which is why its critics
agreement dominates the verdicts and the judges           add a reliability threshold (Liu et al., 2025; Dragoi
fail to reliably detect the tested errors in the steps;   et al., 2025) or replace it with a posterior success es-
the metric’s own judge passes most wrong answers          timate (Hariri et al., 2026); none of these three met-
as well (Section 5.1). It follows that wherever an-       rics inspects the chain. CoT-Pass@k (Wen et al.,
swers are mostly right, CoT-Pass@k must collapse          2026) enters that debate as an instrument: an LLM
onto Pass@k, and it does: across two solver gener-        judge must approve the reasoning chain before a
ations, the average difference falls from 19.7 points     solution counts, so the metric should separate rea-
to 4.1 (Section 5.2). The original study’s solver was     soning from guessing. The original study supports
a Qwen2.5 base checkpoint, on which the metric            its judge by agreement with larger open-weights
does separate; on the solvers it would be applied to      judges; Section 5.1 shows why agreement is not
now, what it adds over Pass@k is close to nothing.        verification: two judges that both track the final
Switching the generation mode reverses which lan-         answer agree for the wrong reason.
guage the same solvers look stronger in, and rais-
ing the token budget moves Pass@64 by more than
                                                          Turkish and Portuguese benchmarks. Turkish
fifty points while the difference Pass@64 − CoT-
                                                          has TurkBench (Toraman et al., 2026) and Cetvel
Pass@64 stays at zero at every step (Section 5.3).
                                                          (Er et al., 2026) and Portuguese has MATH-PT
   Our contributions: (i) the first audit of CoT-
                                                          (Teixeira et al., 2026) and PHEB (Tavares et al.,
Pass@k’s verification step, under the metric’s own
                                                          2026), but none measures Pass@k, and only PHEB
protocol, where other error injection tests the judge
                                                          grades written solutions, against the official rubrics
but not a metric built on it (Sun et al., 2026; Mit-
                                                          of open-ended questions our suite does not use;
tal and Arike, 2026); (ii) a controlled, determinis-
                                                          TurkBench draws on TÜBİTAK olympiads but pre-
tic error-injection design whose conditions sepa-
                                                          dates the 2026 exam. MCLM (Son et al., 2025)
rate chain validity from answer correctness, includ-
                                                          translates AIME 2024 into 55 languages with GPT-
ing a consistency-preserving wrong-answer condi-
                                                          4o, Turkish among them, checks only that the an-
tion; (iii) a multilingual benchmark suite built for
                                                          swers and equations survive translation, and scores
this audit1 : translated AIME 2026 (MAA, 2026)
                                                          the final answer alone.
and native sets from the 2026 Turkish olympiad
(TÜBİTAK, 2026) and the Portuguese exams of
PHEB (Tavares et al., 2026). These carry, to our          Judge-free evaluation. Where gold step labels
knowledge, the first CoT-Pass@k results on na-            exist, reasoning can be scored without a judge (Ue-
tively written Turkish and Portuguese benchmarks;         sato et al., 2022; Lightman et al., 2024), and Pro-
(iv) a two-generation comparison of the metric’s          cessBench (Zheng et al., 2025) and PRMBench
collapse onto Pass@k, with question-level uncer-          (Song et al., 2025) score verifiers against known
tainty quantified; (v) an analysis showing that what      step errors and find existing process reward models
the metric reports depends on the token budgets,          weak at identifying the faulty step. These bench-
the generation mode and judgments stopped at the          marks measure judges in isolation; the verdict
max-token limit; and (vi) concrete recommenda-            never leaves the benchmark, so nothing connects
tions for reporting and auditing judged reasoning         a judge’s failure there to the numbers a deployed
metrics.                                                  metric reports. Sobhani et al. (2026) extends er-
                                                          ror injection to multilingual mathematics, Turkish
2       Related Work                                      among its languages, though its injected chains are
                                                          Bangla and English only; Zhao et al. (2026) corrupt
What Pass@k and CoT-Pass@k measure.                       chains across languages to measure the solver’s re-
Pass@k, adopted from program synthesis (Chen              liance on its own trace. In concurrent work, Garcia
et al., 2021), is the evidence base for the debate        (2026) shows that the effect in such studies tracks
on whether reinforcement learning with verifiable         where the answer is stated, not where the computa-
rewards extends a base model’s reasoning or only          tion happens. In all three, a corrupted chain scores
sharpens its sampling (Yue et al., 2025). Pass@k          a model against a known key, the gold answer or, in
is a coverage measure that rises with the sample          MathMist, the injected error; in none does a verdict
    1
   Code and the benchmark suite: https://github.          on a chain become the number a published metric
com/ttasalti/evalhub.                                     reports.
Accepted at MRL@EMNLP 2026



Judge-dependent evaluation. Where the judge               the translation audit, checked that each question
itself is the instrument, its failure modes are doc-      kept has a single ground-truth answer and can be
umented: preference biases, degradation on long           posed without its options. All Portuguese material
chains, credit for reasoning that only looks valid        in the suite is European Portuguese (the variety far
(Zheng et al., 2023; He et al., 2025; Wang et al.,        less represented in training corpora than Brazilian
2025b), weaker judges accept wrong answers more           Portuguese): the original exams, the translation
readily once a fluent chain is attached (Tu et al.,       by construction and native audit. The pairing is
2026), and a chain need not state the true reason for     deliberate: each non-English language gets one
its answer at all (Turpin et al., 2023). Two recent       translated benchmark, which isolates the language
studies come closest to ours in method. In con-           while holding the problems fixed, and one native
current work, Sun et al. (2026) build valid-answer,       benchmark, which removes any translation artifact.
invalid-reasoning solutions and find frontier judges         The suite spans a wide difficulty range: the
credit up to half of them as flawless, the verdicts       AIME sets and the Turkish olympiad are com-
tracking the answer. Mittal and Arike (2026) inject       petition mathematics, the Portuguese exams are
errors into PRM800K chains and find judges detect         high-school level and nearly saturated by current
that a chain is wrong far more reliably than where.       models. Contamination risk is limited for the com-
Both are English-only and stop at the judge. Our          petition material. The Turkish olympiad, held on
preliminary study (Taşaltı et al., 2026) benchmarks      16 May 2026, postdates the public release of ev-
both metrics on the three AIME 2026 versions and          ery model we use. AIME 2026, held in February,
raises, without testing, the question this audit starts   postdates the release of Qwen2.5 and R1-distill and
from, whether the judge catches subtle reasoning          the stated January 2025 training cutoff of Gemma
errors. Neither study, nor any other we know of,          4; Qwen3.5, Qwen3.6 and V4-Flash publish no
audits a published judged metric under the metric’s       training cutoff and appeared only three to eleven
own protocol, follows the judge’s verdicts into the       weeks after the first exam, little time for its prob-
number the metric reports, or ties what remains to        lems to reach their training data. The Portuguese
the token budgets and the generation mode: the            exams, written between 2006 and 2023, predate ev-
three steps this audit takes, in three languages.         ery model. AIME problems are mirrored in public
                                                          corpora within days of release, while we found nei-
3   Multilingual Benchmarks                               ther the 2026 Turkish olympiad nor the Portuguese
                                                          exam questions of PHEB on Hugging Face, and the
The suite holds five benchmarks in three typolog-         olympiad nowhere but in the organiser’s PDF, the
ically distant languages: Germanic English, Ro-           least exposed benchmark of the five.
mance Portuguese, and Turkic Turkish, the last ag-
glutinative and outside the Indo-European family          4     Method
altogether. The English core is the AIME 2026
competition set (MAA, 2026): thirty problems              4.1   Solvers, Judges and Metrics
with integer answers, on which none of our solvers        Solvers. We evaluate two model generations and
reaches the ceiling. Two translated benchmarks            a second current-generation family. The earlier gen-
carry the same thirty problems into Portuguese            eration is Qwen2.5-7B and Qwen2.5-32B (Qwen
and Turkish: the problems were first machine-             Team, 2024), run as base models and, through their
translated, then manually audited by native speak-        Instruct counterparts, in non-thinking mode. The
ers of each language, six for Portuguese and two for      current generation is Qwen3.5-4B and Qwen3.5-
Turkish, one of them an author. Two native bench-         9B (Qwen Team, 2026a) in base, non-thinking and
marks complete the suite: the thirty-two first-stage      thinking configurations, joined by Gemma-4-E2B-
problems of the 2026 Turkish TÜBİTAK mathemat-           it and Gemma-4-E4B-it (Gemma Team, 2026) in
ics olympiad (TÜBİTAK, 2026), and 166 problems           non-thinking and thinking mode. Base checkpoints
we draw from PHEB (Tavares et al., 2026), a multi-        run under their template’s default thinking setting,
subject benchmark of Portuguese national exams,           and every solver draws 64 generations per ques-
taking its multiple-choice mathematics questions          tion (16 on the Portuguese exams) at temperature
with ground-truth answers and converting them to          0.6 and top-p 0.95, with a 16,384-token genera-
open-ended form; two further graduate students,           tion budget unless a section states otherwise (the
native speakers of Portuguese and independent of          error-injection study raises it per benchmark, Sec-
Accepted at MRL@EMNLP 2026



tion 4.2). Serving templates and the sample-count       questions, where c of the n generations of a ques-
choice are given in Appendix A.2.                       tion are correct (Chen et al., 2021). CoT-Pass@k
                                                        (Wen et al., 2026) counts a generation as a success
Judges. Two open-weights judges cover the pa-           only if its final answer is correct and the judge ap-
per: Qwen3.6-35B-A3B (Qwen Team, 2026b)                 proves its reasoning chain: the same estimator with
and Gemma-4-26B-A4B-it, written Qwen3.6 and             c replaced by the number of generations that are
Gemma4; the error-injection study and the               both correct and approved. We write the difference
cross-generation replication add DeepSeek V4-           between them out as Pass@k − CoT-Pass@k; at
Flash (DeepSeek-AI, 2026), a far larger open-           k = n it is the share of questions with a correct
weights model from a third family that we run           solution but no approved one.
through a commercial API. A fourth judge cor-
roborates the earlier generation and scores the         4.2   Error Injection
error-injection study as well, DeepSeek-R1-0528-        We test whether the judge actually assesses chains
Qwen3-8B (DeepSeek-AI, 2025; Qwen Team,                 with error injection: we edit solutions so that the
2025), written R1-distill: it is the verifier of Wen    reasoning chain and the final answer are corrupted
et al. (2026) and the reason our earlier generation     separately, and we measure what the judge detects.
is the Qwen2.5 family, so one arm of our compari-          We use two current-generation solvers, Qwen3.5-
son reruns the metric on its own solver and its own     4B and Qwen3.5-9B, in thinking mode, with a gen-
judge rather than on a reconstruction of them.          eration budget of 65,536 tokens for English AIME,
Judging protocol. All judges run in thinking            32,768 for the AIME translations and the Turkish
mode at the same temperature 0.6 and top-p 0.95,        olympiad, and 16,384 for the Portuguese exams.
with a 16,384-token judgment budget, and judge          The original solutions are correctly answered gen-
every correct solution three times; Appendix A.2        erations to which all four error types can be applied
gives the two budget exceptions. A judgment that        (Appendix A.2). From every model×benchmark
reaches its own max-token limit without emitting        cell we randomly select 72 such solutions, giving
a verdict counts as neither an approval nor a rejec-    720 original solutions. Each is expanded into five
tion; the majority rule, used throughout the paper,     variants, the unedited clean control and one copy
compares approvals against rejections. Solvers are      per error type, for a total of 720 × 5 = 3,600 vari-
prompted in the language of the benchmark; their        ants. The intermediate numeric error replaces
chains, like those of the reasoning models stud-        one number drawn at random from between 40%
ied by Wang et al. (2025a) and Yong et al. (2025),      and 70% of the solution’s length, never one that ap-
are free to switch into English mid-solution, and       pears in the question or the answer, in the middle of
on the non-English benchmarks the Qwen3.5 base          the solution, where Mittal and Arike (2026) confine
checkpoints and every thinking-mode solver write        their injections so that a judge cannot find them by
nearly every chain in English or in a mixture, the      inspecting the first or last step, and leaves the final
instruction-tuned solvers in non-thinking mode al-      answer correct. The truncation error deletes the
most none (Figures 11 and 13 in Appendices C.5          last 25% of the reasoning chain and re-appends the
and D.4). Verification is therefore standardised: ev-   boxed final answer on a new line, leaving a visible
ery solution meets the same instrument, the original    seam. With these two error types the reasoning
English verification prompt of Wen et al. (2026), ex-   chain is corrupted but the final answer stays cor-
tended by two lines (Appendix A.1) that name the        rect. The final-answer error replaces only the final
problem’s language and direct the judge to score        answer and leaves the reasoning chain untouched.
the mathematics regardless of the chain’s language,     The consistent final-answer error replaces every
keeping the judging directly comparable to the orig-    occurrence of the correct final-answer value in the
inal study. The other two verification strategies of    reasoning chain with the same wrong number, so
the original metric are defined and ablated in Ap-      the chain stays consistent and supports the wrong
pendix B.                                               final answer. All edits are deterministic string ed-
                                                        its (no language model writes the corruptions), and
Metrics. Pass@k estimates the probability that at       every wrong number is a near miss of the value it re-
least one of k sampled generations reaches the cor-     places: shifted by one or two, two digits transposed,
rect final answer. We compute it nwith
                                    the standard       or a single digit changed. The chain edits adapt the
                         n−c
unbiased estimator 1 − k / k , averaged over            early-answering and adding-mistakes perturbations
Accepted at MRL@EMNLP 2026



of Lanham et al. (2023), which truncate a chain or        is dropped entirely, since a partial grid would open
insert one mistaken step into it, to a judge-side test    the comparison to selection effects (Appendix C.1
with deterministic edits and no regeneration, and         lists the models this removes). The Portuguese
the numeric edits adapt the rule-based numeric per-       exams are excluded (they have no non-thinking
turbations of Singh et al. (2025), tightened here to      runs, and even in the earlier generation the dif-
near misses. The design gives each error type one         ference there stays between 0 and 3.6 points, at
job. Models reading a chain are known to follow           that benchmark’s k=16), and thinking mode is
its stated final answer, most strongly at small scale     excluded because Qwen2.5 has no thinking coun-
(Garcia, 2026), and judges to confirm the answer          terpart; thinking-mode solvers are studied in Sec-
rather than check the steps (Sun et al., 2026); a re-     tion 5.1. Intervals on the difference resample ques-
jection under the first two error types can therefore     tions within a cell.
only come from assessing the chain, and extra ac-
ceptance under the consistent error can only come         4.4    Token-Budget Measures
from rewarding that consistency.                          Both the solver and the judge can run out of tokens,
   Three thinking-mode judges score every vari-           and in both cases the consequence is scored as a
ant, V4-Flash, Qwen3.6 and R1-distill, under the          failure that the model may not have committed.
three-judgment majority rule of Section 4.1. All             On the solver side, a generation still writing at
comparisons are paired: each judge is evaluated           the max-token limit is cut off before it states a
only on original solutions it judged in all five vari-    boxed final answer and is graded wrong; thinking
ants, the same 720 for all three judges. Accep-           mode makes this common, because the chain con-
tance rates carry 95% Wilson intervals (Wilson,           sumes the same budget the answer has to fit in.
1927); conditions are compared pairwise with an              On the judge side the same thing happens one
exact McNemar test (McNemar, 1947) on the same            level up. A judgment that spends its whole budget
solutions, and the paired difference between two          thinking emits no verdict, and under the major-
conditions is bounded by a bootstrap over those           ity rule it cannot contribute an approval: a solu-
solutions.                                                tion can lose its majority, and be counted against
                                                          CoT-Pass@k, without any judge having rejected
4.3   Cross-Generation Design
                                                          it. We count these stops per judgment and iso-
To measure whether the difference Pass@k − CoT-           late their effect with a counterfactual: recomputing
Pass@k still opens in current-generation models,          CoT-Pass@k with stopped judgments counted as
we compare two solver generations under one fixed         approvals. The band between the two curves is
setting: the anchor judge Qwen3.6 with a 16k              an upper bound on how much of the difference
generation budget, on the four 64-sample bench-           Pass@k − CoT-Pass@k the judge’s token budget,
marks, with every curve run to k = 64, under              rather than its verdicts, produced, since some of the
the majority rule. Throughout the paper genera-           stopped judgments would have ended in rejection
tion refers to the solvers being measured, never          had they finished.
to the judges, which are held fixed across both.             We also run a budget ladder that raises the gen-
Both generations enter as base checkpoints and,           eration budget itself (Section 5.3).
through their instruction-tuned counterparts, in non-
thinking mode (Section 4.1). The two arms hold            5     Results
different things fixed: in the non-thinking arm the
mode is matched exactly, with thinking explicitly         5.1    The Judges Miss the Injected Reasoning
disabled on both sides, while in the base arm each               Errors
family’s base checkpoint runs under its template’s        Figure 1 shows acceptance for the five variants
default thinking setting. The Gemma-4 solvers en-         under majority-correct. All three judges accept the
ter in non-thinking mode only, and Gemma4 joins           unedited clean control at high rates, 93% for V4-
the anchor judge on this grid; the two further judges     Flash, 98% for Qwen3.6 and 90% for R1-distill.
of Appendix C cover the earlier generation.                  The two error types that keep the final answer
   A model enters the comparison only if both             correct barely move them. Under the intermediate
judges returned verdicts for at least 30 of its correct   numeric error all three judges stay at their clean
solutions in every cell: both modes, all four bench-      rates, 93%, 98% and 92%, although every edited
marks; a model that misses the threshold anywhere         chain now carries a number that the steps around it
Accepted at MRL@EMNLP 2026




Figure 1: CoT acceptance under injected errors per benchmark and judge (rows), majority-correct strategy of
Section 4.1, 95% Wilson intervals; the dark grey bar is the rate pooled over the five benchmarks. Every judge
assesses the same 720 original solutions, 144 per benchmark and condition. R1-distill is the judge the metric
specifies.


no longer support: a paired McNemar test over the       the ordering can be tested pairwise: McNemar’s
same 720 solutions finds no evidence of a shift         test rejects equality for V4-Flash and Qwen3.6
from the clean control (p = 1, p = 0.55 and             (p = 2.4 × 10−3 and p = 2.6 × 10−14 ), with
p = 0.23), and the paired difference is bounded         the discordant pairs running the same way for each.
within 1.5 points in either direction for V4-Flash      R1-distill does not show the rise, accepting 62%
and Qwen3.6 and within 5 for R1-distill (95% boot-      of the consistent variants against 71% of the plain
strap intervals). The truncation error costs 8, 6 and   ones (p = 1.7 × 10−4 ; Appendix B). None of the
3 points.                                               three judges reliably detects the tested errors in
   Corrupting the final answer gives the opposite       the steps, and for V4-Flash and Qwen3.6 chain–
picture. The final-answer error leaves the chain        answer agreement dominates the verdicts.
untouched and replaces only the number at the              The verification strategy changes the rates, not
end, and acceptance collapses at once, to 18% for       the findings (Table 1 in Appendix B), and the size
V4-Flash and 34% for Qwen3.6, and only to 71%           of the edit matters only for the consistent wrong
for R1-distill. V4-Flash and Qwen3.6 can reject,        answer; the intermediate error is missed at every
sharply and in agreement with each other, but they      size (Figure 4).
did so only when the final answer was wrong. The           The pattern repeats on every benchmark (Fig-
metric’s own judge barely rejects even there, leav-     ure 1; Appendix B gives the rates per benchmark).
ing 71% of the wrong answers accepted. Changing         Under every judge the intermediate numeric error
a number inside the chain costs no judge a mea-         stays within four points of the clean control on all
surable share of its acceptance; changing only the      five, and the translated AIME sets behave like the
number at the end costs 75 and 64 points for V4-        English original. A wrong final answer costs V4-
Flash and Qwen3.6 and 20 for R1-distill.                Flash and Qwen3.6 47 to 98 points everywhere,
   The consistent final-answer error shows why. It      most on the short Portuguese exams, and R1-distill
corrupts strictly more of the reasoning than the        15 to 27, and the Turkish olympiad is where the
final-answer error, since the wrong value now runs      judges doubt correct chains too.
throughout the chain, yet acceptance rises instead
of falling: to 25% for V4-Flash and to 54% for          5.2   CoT-Pass@k Collapses onto Pass@k in
Qwen3.6, which accepts the majority of these vari-            Current Solvers
ants. A judge that verified the mathematics would       Section 5.1 predicts where CoT-Pass@k should
order the two the other way round. Both condi-          collapse onto Pass@k: the judge mostly approves
tions are built from the same 720 solutions, so         a chain that agrees with its final answer, so the
Accepted at MRL@EMNLP 2026



                                                         current-generation solvers, CoT-Pass@k stays
                                                         within a few points of Pass@k, and the judge
                                                         changes almost nothing of what Pass@k already
                                                         reports.
                                                            Nor does this depend on the anchor judge. Four
                                                         different judge models, among them the verifier
                                                         of the original study, reproduce the earlier genera-
                                                         tion’s average difference within two points of each
                                                         other; Gemma4, the only other judge that covers
                                                         both generations in full, reproduces the split be-
                                                         tween them (Tables 2 and 3 in Appendix C.1, per
                                                         judge and per model). Under both judges that span
                                                         the generations, the collapse is a property of the
                                                         metric, not of the judge we chose to anchor it on.
                                                            The divergence is not present from the start: at
                                                         k = 1 the generations are indistinguishable, 2.7
                                                         points against 2.0, and Figure 6 in Appendix C.2
                                                         follows them apart to 19.7 against 4.1. What sepa-
                                                         rates them is what repeated sampling adds: in the
                                                         earlier generation each new correct answer had a
Figure 2: CoT-Pass@64 (open) and Pass@64 (filled) per    growing chance of carrying a chain the judge would
solver and 64-sample benchmark under the anchor judge    reject; in the current one it does not.
Qwen3.6 at 16k; row-end numbers give the difference.        Per generation the verdicts do change. Aver-
Q2.5/Q3.5 = Qwen2.5/Qwen3.5, G4 = Gemma-4-it.            aged over the four benchmarks, the anchor judge
                                                         approves 61.6% of the earlier generation’s answer-
                                                         correct generations and 94.8% of the current gener-
difference Pass@k − CoT-Pass@k can come only             ation’s, and Gemma4 62.7% and 93.2% (Figure 8
from correct answers carrying chains the judge           in Appendix C.3). Two things therefore shrink the
rejects, and should vanish where those are rare.         difference. The judges reject far fewer of the cur-
Figure 2 confirms the prediction. Among the              rent generation’s correct chains, and the rejections
earlier-generation solvers (Qwen2.5), the differ-        that remain rarely reach CoT-Pass@64, because a
ence Pass@64 − CoT-Pass@64 is large for every            question keeps its CoT-Pass@64 as long as one of
model on every benchmark: 6.7–20 points on the           its c correct generations is approved, and the cur-
AIME benchmarks and 34–47 points on the Turkish          rent generation’s solved questions typically hold
olympiad, for both base and non-thinking models.         dozens (Appendix C.4). Comparing the genera-
   Among the current-generation solvers (Qwen3.5         tions at the same c leaves the gap in place (Fig-
and Gemma-4) the same judge and budget find              ure 9).
almost nothing. Qwen3.5-9B-Base ends at exactly             The collapse holds on all four benchmarks,
zero on all four benchmarks, Qwen3.5-4B-Base on          across three languages, and at every k we mea-
three of the four, and no Qwen3.5 model exceeds          sure, with the earlier-minus-current contrast car-
10 points anywhere in it; the Gemma-4 models stay        rying a 95% interval that excludes zero on each
at or below 6.7 on the AIME benchmarks and reach         benchmark separately. Three readings short of a
18.8 only on the Turkish olympiad, still well below      generational change do not survive the data. Higher
the smallest earlier-generation value there, 34.4.       accuracy alone does not produce it. At an identi-
Averaged over the four benchmarks, the difference        cal Pass@64 of 59.4 on the Turkish olympiad, the
is 19.7 points (95% CI [16.4, 23.0]) in the earlier      two earlier-generation solvers lose 43.8 and 46.9
generation against 4.1 ([2.7, 5.5]) in the current one   points where the current one loses 18.8 (Figure 2),
(per solver, 15.6–22.1 against at most 8.2), and the     and the acceptance rates above separate the gener-
contrast itself is 15.6 ([12.0, 19.3]). The intervals    ations at every level of accuracy (Figure 9). It is
are bootstrap intervals over questions, the sampled      not model size: scaling Qwen2.5 from 7B to 32B
unit in the framework of Miller (2024); Figure 7         leaves the difference as large, 34.4 against 43.8,
in Appendix C.2 gives one for every solver. On           while at the closest matched scale, Qwen2.5-7B
Accepted at MRL@EMNLP 2026



against the larger Qwen3.5-9B, the difference falls     that stop at the max-token limit from 27.9% to
from 15.6 to zero in the base arm and from 22.1         86.7% (the chains grow, the budget does not) while
to 3.3 in the non-thinking one. And it is not the       the Turkish rate rises only to 39.9% (Table 6 in
mode mix: the mode-matched arm alone, Qwen2.5-          Appendix D.4). Pass@64 inverts with it, English
Instruct against Qwen3.5 non-thinking, shows the        against Turkish: 91.7 to 88.3 in non-thinking mode,
collapse from 10–47 points down to at most 10.          40.0 to 85.0 with thinking on. Turning on the chain
The comparison remains observational, between           of thought that CoT-Pass@k exists to check re-
model families rather than a controlled intervention,   verses which of the two languages these models
and isolates none of what produces the change.          look stronger in. We therefore read language differ-
                                                        ences throughout as effects of the generation mode
5.3   Raising the Budget Moves the Scores, Not          and the token budget, not statements about ability
      the Difference                                    in a language; the mode even sets the language the
The residual that Section 5.2 leaves behind is small    chain is written in (Figure 13 in Appendix D.4).
under the anchor judge. Both sides of the metric           The benchmarks line up the same way: the Por-
spend token budget, the judge to take in the chain      tuguese exams, the easiest of the five and the least
and still reason, the solver to finish the chain and    bound by the max-token limit on either side (Ta-
still answer, and both move the numbers that get        ble 4), carry the smallest difference, 0.60 points
reported (Table 4 in Appendix D.1, at the shared        at most, at that benchmark’s k=16. Where solu-
16k budget).                                            tions fit the budgets, there is nothing left for the
    The judge’s side first. The two judges stop at      metric to report. The Turkish olympiad marks the
their own max-token limit at very different rates.      one residual the budget reading does not carry: the
Judging the Qwen3.5 solutions on the four compe-        largest difference the anchor judge reports here,
tition benchmarks, Gemma4 stops on 33 to 54%            9.38 points under the Gemma-4-E4B solver, sits
of its judgments; judging the Gemma-4 solutions         where essentially nothing stops at the max-token
on the same benchmarks, on 2 to 14%. Qwen3.6            limit, not one of that solver’s generations, and 0.1%
stays at or below 18% throughout, and most of its       of the anchor judge’s. Whatever it tracks, it is not
stops come after a verdict has already been writ-       the budget; we return to it in Section 6.
ten, while Gemma4’s stops rarely contain one. A            So far the budget has been held fixed and ev-
stopped judgment cannot contribute an approval,         erything else varied; moving it turns the reading
so it can only widen the difference (Section 4.4).      into an intervention. Table 5 in Appendix D.3 com-
And the two judges do report different differences      pares the two solvers of Section 4.2 at a low and a
on the same solutions: averaged over these four         high generation budget: the same problems, more
benchmarks at k = 64, 5.7 points under Gemma4           room to write. The high budget is 32k, except 64k
against 1.4 under the anchor. The counterfac-           on English AIME, whose chains still ran into the
tual of Section 4.4 measures how much of that           max-token limit at 32k.
is budget: counting Gemma4’s stopped judgments             The solver’s side of Table 5 responds exactly
as approvals removes 92.7% of its 5.7, an upper         as Table 4 predicts: the share of generations stop-
bound on the budget’s share, against 47.9% in non-      ping at the max-token limit collapses, from 84–
thinking mode, where the stops are rarer and the        90% to 9–18% on English AIME, and accuracy
two judges nearly agree to begin with, 5.9 against      climbs with it, Pass@1 from 10.5 and 16.2 to 75.4
5.8 (Figure 12 in Appendix D.2). Under Gemma4,          and 84.5 there, Pass@64 from 40.0 to 96.7 there
the judge’s token budget can account for most of        and by 3 to 17 points on the other benchmarks.
what the metric reports in thinking mode; under         What CoT-Pass@64 adds on top of Pass@64 never
Qwen3.6, on the very same solutions, there is al-       moves at all. The ladder’s solutions are judged
most nothing left to report. The collapse itself        as everywhere else, by the anchor judge at a bud-
shows under either judge (Section 5.2); what re-        get that rises with the solver’s, and the difference
mains on top of it can be an artifact of the judge      Pass@64 − CoT-Pass@64 is exactly zero in all
one happens to pick.                                    sixteen benchmark × solver × budget cells. The
    The solver’s side mirrors it one level down, and    anchor judge still rejects some solutions, but no
the cleanest view changes nothing but the genera-       question ever loses all of its correct ones. CoT-
tion mode. On the same thirty problems, enabling        Pass@64 follows Pass@64 point for point up
thinking raises the share of English generations        the ladder: whatever the budget produces, the
Accepted at MRL@EMNLP 2026



metric certifies. The ladder is reported under the        do not react to corrupted chains there either. What
anchor judge alone (Appendix D.3).                        the metric cannot carry is the debate it entered:
                                                          on current-generation solvers a conclusion drawn
6   Discussion and Conclusion                             from it inherits the Pass@k evidence it was meant
                                                          to go beyond, and whether verifiable rewards ex-
What the metric measures. A judgment that ap-
                                                          tend reasoning has to be settled with instruments
proves a corrupted chain, rejects it once its final
                                                          that measure the chain directly, such as the causal-
answer is wrong, and approves it again once that
                                                          importance and sufficiency metrics of Yu et al.
wrong value runs throughout the chain is a judg-
                                                          (2026), who find that verifiable rewards raise ac-
ment in which agreement between the chain and
                                                          curacy without reliably making the chain causally
the final answer dominates and the tested errors in
                                                          important or sufficient.
the mathematics count for little. The metric’s own
judge fits only the first clause, since it approves
most wrong answers too. That agreement is nearly          What the languages add. The verifier failure
free for a solver whose answers are usually right,        is not English-specific in the tested settings. On
which is why, on current-generation solvers, the          the same thirty AIME problems in three languages
metric returns what Pass@k already returns. What          the judges miss the injected errors, reject wrong
it reports is thus a property of the solver–judge pair:   answers and approve clean chains at rates at most
the same judge filters the two generations differ-        6.3 points below the English original’s, and some-
ently, and the same solvers score differently under       times above them (Section 5.1), and averaged
a judge that stops at the max-token limit.                over solvers the translations are approved within 3
                                                          points of the original or above it (Appendix C.3), so
Two checks. The question we put to CoT-                   we find no sign that Turkish or Portuguese makes
Pass@k is the one work on construct validity puts         verification harder for these judges. What moves
to any instrument, whether it captures the construct      the rates is the native benchmarks, the Turkish
it names (Bean et al., 2025), and our results turn        olympiad on the correct chains and the Portuguese
it into two checks that a judged reasoning metric         exams on the wrong answers, and the olympiad also
should pass before its numbers are read as evidence       carries the one difference the budget reading does
about reasoning. (i) Publish how the judge re-            not explain (Section 5.3), for which the Limitations
sponds to injected errors. Give it solutions whose        name the candidates. The language a chain is writ-
chains are corrupted while their final answers stay       ten in follows the solver rather than the benchmark,
correct; if approval does not move, nothing the met-      and its effect on the verdicts is small and inconsis-
ric reports separates a sound chain from a corrupted      tent: within 3 points for the Qwen3.5 base check-
one. The check is run once, by whoever proposes           points in every cell, 13 points in favour of English
the judge, on several hundred solutions; in our runs      for one earlier-generation solver on the olympiad,
the whole error-injection panel took about a sixth        and in favour of mixed chains under V4-Flash and
of the judge tokens the anchor judge spent on the         R1-distill there (Figures 10 and 5, Appendix C.5).
solutions of Section 5.2 (Appendix A.2). (ii) Re-
port the metric beside the judge-free metric it
wraps, under more than one token budget and               Conclusion. An instrument that promises to as-
generation mode. The difference between the two           sess reasoning has to be audited the way any in-
is all the judge adds, and publishing it per solver       strument is, against inputs whose correct verdict is
and per benchmark, at more than one token budget,         known by construction, as BLEU once was against
costs a column.                                           constructed variants that human judges would rank
                                                          far lower (Callison-Burch et al., 2006). Under
Where the metric still separates. None of this            that audit CoT-Pass@k’s verification step fails to
makes chain-level verification a bad idea; it makes       reliably detect the tested errors and, under V4-
an unaudited judge a bad instrument. The met-             Flash and Qwen3.6, its verdicts are dominated
ric does separate the earlier generation, and the         by chain–answer agreement, what the metric adds
original study itself observes that the separation        over Pass@k has collapsed on current-generation
it reports shrinks on benchmarks the base model           solvers, and what remains of it depends largely on
already solves (Wen et al., 2026), but harder prob-       the token budgets on both sides and on judgments
lems do not restore its meaning, since the judges         stopped at the max-token limit.
Accepted at MRL@EMNLP 2026



Limitations                                              nal judge’s behaviour off its acceptance rates and
                                                         did not audit the reasoning behind its verdicts, so
The injection is deterministic, and deliberately         whether it accepts on the form of a solution rather
so. String edits keep the correct verdict known by       than on its content remains open.
construction: no second model has to be trusted to
corrupt a chain, and every variant is reproducible.      The residual is observed, not explained. The
The cost is realism, and a lenient reader might treat    collapse is least complete on the Turkish olympiad:
an edited step as a slip rather than broken reasoning.   against earlier-generation differences of 34–47
That reading cannot explain the consistent final-        points there, the current-generation solvers fall far
answer error, which corrupts strictly more of the        under the anchor judge, the Qwen3.5 solvers to at
chain than the plain one yet is accepted more often      most 9.4 points and the Gemma-4 solvers to 18.8
by V4-Flash and Qwen3.6; and where our edits are         (Figure 2), but not to zero. That benchmark is at
too mild, the bias understates rather than overstates    once natively written, the least publicly exposed
how little the judges assess.                            of the five, and at olympiad level, and our suite
                                                         cannot separate these: the Portuguese exams are
What the edits cover. Truncation leaves a vis-
                                                         natively written too, but they are high-school level
ible seam, so the 3 to 8 points it costs are an up-
                                                         and nearly saturated, so they cannot isolate the ef-
per bound on what a chain that stops short costs
                                                         fect of native language. The multilingual reach
these judges. The injected solutions come from
                                                         is three languages in one domain, so the findings
two Qwen3.5 thinking-mode solvers, so the judges
                                                         are not English-specific in the tested settings, and
are audited on one family’s style of chain, and on
                                                         we claim nothing beyond those settings. The audit
the non-English benchmarks these chains are writ-
                                                         is also mathematical throughout, and whether the
ten in English or in a mixture rather than in the
                                                         same behaviour holds in code or in domains with
benchmark’s language (Appendix C.5), so outside
                                                         no single verifiable answer, our data cannot say.
English the judges are audited on non-English prob-
lems with English or mixed reasoning. We did not         Ethics Statement
check by hand whether each edited number carries
into the steps that follow; an edit in an auxiliary      This work evaluates publicly released language
line corrupts less of the mathematics than a broken      models on published mathematical exams, used for
derivation, and the consistent final-answer condi-       research evaluation only; no personal data and no
tion, whose corruption needs no such check, carries      human subjects are involved. The translations were
the ordering result.                                     audited by an author and volunteer native speakers,
                                                         and the corrupted solutions exist only as test inputs
Scale is bounded on both sides, solver and judge.        to the judges. The audit concerns a published met-
Our current-generation solvers reach 9B param-           ric, not its authors: we run it under its own prompt
eters, so the collapse is not directly verified on       and protocol and report where it still separates mod-
larger current models; within the earlier generation,    els. Generation and judging ran largely on H200
where we do scale, size does not produce it, since       GPUs, with part of the judging through commer-
7B to 32B leaves the difference as large. On the         cial APIs. The examination material belongs to its
judge side, the audit rests on three judges larger in    original sources; the AIME problems are credited
total parameters than the one the metric specifies       to the MAA AMC and used for non-commercial re-
(Qwen3.6, Gemma4 and DeepSeek V4-Flash) and              search, as are our translations of them. We used AI
on that original 8B judge itself (Wen et al., 2026),     assistants for code, figure scripts, literature checks
which in our error-injection study misses the chain-     and language editing.
level errors as they do but rejects a wrong final
answer far less often; it does not reach the flagship    Acknowledgments
tier of any lab. The judges differ in how much they
accept, and the weakest one also differs in what it      This work was supported by the AMALIA project
accepts. None of them reacts to the intermediate         under Measure RE-C05-i08 of the Portuguese na-
numeric error. V4-Flash and Qwen3.6 accept the           tional Programa de Recuperação e Resiliência. We
consistent wrong answer more often than the plain        also acknowledge the support of the NOVA LINCS
one, R1-distill does not, and it accepts 71% of the      project (UID/04516/2025).
plain wrong answers outright. We read the origi-
Accepted at MRL@EMNLP 2026



References                                                   Zhang, Zhicheng Zheng, Wenbo Su, and Bo Zheng.
                                                             2025. Can large language models detect errors in
Andrew M. Bean, Ryan Othniel Kearns, Angelika Ro-            long chain-of-thought reasoning? In Proceedings
  manou, Franziska Sofia Hafner, et al. 2025. Measur-        of the 63rd Annual Meeting of the Association for
  ing what matters: Construct validity in large language     Computational Linguistics (Volume 1: Long Papers),
  model benchmarks. In Proceedings of the 39th Con-          pages 18468–18489, Vienna, Austria. Association
  ference on Neural Information Processing Systems           for Computational Linguistics. ArXiv:2502.19361
  (NeurIPS 2025), Datasets and Benchmarks Track.             (DeltaBench).
  ArXiv:2511.04703.
                                                           Alon Jacovi, Yonatan Bitton, Bernd Bohnet, Jonathan
Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald         Herzig, Or Honovich, Michael Tseng, Michael
  Clark, Quoc V. Le, Christopher Ré, and Azalia Mirho-       Collins, Roee Aharoni, and Mor Geva. 2024. A
  seini. 2024. Large language monkeys: Scaling infer-        chain-of-thought is as strong as its weakest link: A
  ence compute with repeated sampling. arXiv preprint        benchmark for verifiers of reasoning chains. In Pro-
  arXiv:2407.21787.                                          ceedings of the 62nd Annual Meeting of the Asso-
                                                             ciation for Computational Linguistics (Volume 1:
Chris Callison-Burch, Miles Osborne, and Philipp
                                                             Long Papers), pages 4615–4634, Bangkok, Thai-
  Koehn. 2006. Re-evaluating the role of BLEU in ma-
                                                             land. Association for Computational Linguistics.
  chine translation research. In Proceedings of the 11th
                                                             ArXiv:2402.00559 (REVEAL).
  Conference of the European Chapter of the Associa-
  tion for Computational Linguistics, pages 249–256.       Amir Hossein Kargaran, Ayyoob Imani, François Yvon,
  ACL Anthology E06-1032.                                    and Hinrich Schütze. 2023. GlotLID: Language iden-
Mark Chen et al. 2021.    Evaluating large lan-              tification for low-resource languages. In Findings
 guage models trained on code. arXiv preprint                of the Association for Computational Linguistics:
 arXiv:2107.03374.                                          EMNLP 2023, pages 6155–6218, Singapore. Associ-
                                                             ation for Computational Linguistics.
DeepSeek-AI. 2025. DeepSeek-R1: Incentivizing rea-
  soning capability in LLMs via reinforcement learning.    Amir Hossein Kargaran, François Yvon, and Hinrich
  arXiv preprint arXiv:2501.12948.                          Schütze. 2024. MaskLID: Code-switching language
                                                            identification through iterative masking. In Proceed-
DeepSeek-AI. 2026. DeepSeek-V4: Towards highly              ings of the 62nd Annual Meeting of the Association
  efficient million-token context intelligence. arXiv       for Computational Linguistics (Volume 2: Short Pa-
  preprint arXiv:2606.19348.                                pers), pages 459–469, Bangkok, Thailand. Associa-
                                                            tion for Computational Linguistics.
Marius Dragoi, Ioana Pintilie, Florin Gogianu, and
 Florin Brad. 2025. Beyond pass@k: Breadth-depth           Tamera Lanham et al. 2023. Measuring faithful-
 metrics for reasoning boundaries. arXiv preprint            ness in chain-of-thought reasoning. arXiv preprint
 arXiv:2510.08325.                                           arXiv:2307.13702.

Yakup Abrek Er, Ilker Kesen, Gözde Gül Şahin, and         Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri
  Aykut Erdem. 2026. Cetvel: A unified benchmark for         Edwards, Bowen Baker, Teddy Lee, Jan Leike, John
  evaluating language understanding, generation and          Schulman, Ilya Sutskever, and Karl Cobbe. 2024.
  cultural capacity of LLMs for Turkish. In Proceed-         Let’s verify step by step. In The Twelfth Inter-
  ings of the 19th Conference of the European Chap-          national Conference on Learning Representations
  ter of the Association for Computational Linguistics       (ICLR). ArXiv:2305.20050 (PRM800K).
  (Volume 1: Long Papers), pages 1052–1085, Rabat,
  Morocco. Association for Computational Linguistics.      Junnan Liu, Hongwei Liu, Linchen Xiao, Ziyi
  ArXiv:2508.16431.                                          Wang, Kuikun Liu, Songyang Gao, Wenwei Zhang,
                                                             Songyang Zhang, and Kai Chen. 2025. Are your
Gabriel Garcia. 2026. The last word often wins: A for-       LLMs capable of stable reasoning?        In Find-
  mat confound in chain-of-thought corruption studies.       ings of the Association for Computational Lin-
  arXiv preprint arXiv:2605.10799.                           guistics: ACL 2025, pages 17594–17632, Vienna,
                                                             Austria. Association for Computational Linguistics.
Gemma Team. 2026. Gemma 4 technical report. arXiv            ArXiv:2412.13147 (G-Pass@k).
  preprint arXiv:2607.02770.
                                                           MAA. 2026. American invitational mathematics ex-
Mohsen Hariri, Amirhossein Samandar, Michael                amination (AIME) 2026. https://maa.org/
 Hinczewski, and Vipin Chaudhary. 2026. Don’t               maa-invitational-competitions/. Ad-
 pass@k: A Bayesian framework for large language            ministered by the Mathematical Association of Amer-
 model evaluation. In The Fourteenth International          ica. AIME I, 5 February 2026; AIME II, 11 February
 Conference on Learning Representations (ICLR).             2026. Accessed 2026-08-11.
 ArXiv:2510.04265.
                                                           Quinn McNemar. 1947. Note on the sampling error
Yancheng He, Shilong Li, Jiaheng Liu, Weixun Wang,           of the difference between correlated proportions or
  Xingyuan Bu, Ge Zhang, Z.Y. Peng, Zhaoxiang                percentages. Psychometrika, 12(2):153–157.
Accepted at MRL@EMNLP 2026



Evan Miller. 2024. Adding error bars to evals: A statis-   Tarık Tuna Taşaltı, David Semedo, and Burcu Hüdav-
  tical approach to language model evaluations. arXiv        erdi. 2026. Cross-lingual mathematical reasoning
  preprint arXiv:2411.00640.                                 in LLMs: Benchmarking base, non-think, and think
                                                             modes on multilingual AIME 2026 with pass@k and
Avni Mittal and Rauno Arike. 2026. C2-faith: Bench-          CoT-pass@k. In Proceedings Book of the VII. Inter-
  marking LLM judges for causal and coverage faith-          national Applied Statistics Congress (UYIK 2026),
  fulness in chain-of-thought reasoning. arXiv preprint      page 227, Istanbul, Türkiye. Tokat Gaziosmanpaşa
  arXiv:2603.05167. V2, June 2026.                           University.
Qwen Team. 2024. Qwen2.5 technical report. arXiv           Diogo Tavares, Rafael Ferreira, Afonso Simplício,
 preprint arXiv:2412.15115.                                  Gonçalo Vinagre, Ana Carolina Condez, Inês Calvo,
                                                             Inês Vieira, David Semedo, and João Magalhães.
Qwen Team. 2025. Qwen3 technical report. arXiv               2026. PHEB: An European Portuguese high school-
 preprint arXiv:2505.09388.                                  level LLM benchmark. In Proceedings of the Fif-
                                                             teenth Language Resources and Evaluation Confer-
Qwen Team. 2026a.     Qwen3.5.     https:                    ence (LREC 2026), pages 4673–4683, Palma, Mal-
 //huggingface.co/Qwen/Qwen3.5-4B,                           lorca, Spain. European Language Resources Associa-
 https://huggingface.co/Qwen/Qwen3.                          tion (ELRA).
 5-9B. Model cards; released 2 March 2026.
 Accessed 2026-09-25.                                      Tiago Teixeira, Ana Carolina Erthal, Juan Belieni, Beat-
                                                              riz Canaverde, Diego Mesquita, Miguel Faria, Eliezer
Qwen Team. 2026b.        Qwen3.6-35B-A3B.                     de Souza da Silva, and André F. T. Martins. 2026.
 https://huggingface.co/Qwen/Qwen3.                           MATH-PT: A math reasoning benchmark for euro-
 6-35B-A3B. Released 16 April 2026. Accessed                  pean and brazilian portuguese. In Proceedings of
 2026-09-25.                                                  the 17th International Conference on Computational
                                                              Processing of Portuguese (PROPOR 2026), Volume
Joykirat Singh, Akshay Nambi, and Vibhav Vineet.             1, pages 1005–1010, Salvador, Brazil. Association
  2025. Exposing the achilles’ heel: Evaluating LLMs          for Computational Linguistics. ArXiv:2604.25926.
  ability to handle mistakes in mathematical reasoning.
  In Proceedings of the 63rd Annual Meeting of the         Çağrı Toraman et al. 2026. Turkbench: A benchmark
  Association for Computational Linguistics (Volume 1:       for evaluating turkish large language models. In
  Long Papers), pages 27044–27065, Vienna, Austria.          Proceedings of the Second Workshop Natural Lan-
  Association for Computational Linguistics.                 guage Processing for Turkic Languages (SIGTURK
                                                             2026), pages 126–154, Rabat, Morocco. Association
Mahbub E Sobhani, Md. Faiyaz Abdullah Sayeedi, Tas-          for Computational Linguistics.
 nim Mohiuddin, Md. Mofijul Islam, and Swakkhar
 Shatabda. 2026. MathMist: A parallel multilingual         Minzhu Tu, Shiyu Ni, and Keping Bi. 2026. How
 benchmark dataset for mathematical problem solving          long reasoning chains influence LLMs’ judgment
 and reasoning. In Findings of the Association for           of answer factuality. In Proceedings of the 64th An-
 Computational Linguistics: EACL 2026, pages 2524–           nual Meeting of the Association for Computational
 2550. Association for Computational Linguistics.            Linguistics (Volume 1: Long Papers), pages 44957–
                                                             44972, San Diego, California, United States. Associ-
Guijin Son, Jiwoo Hong, Hyunwoo Ko, and James                ation for Computational Linguistics.
  Thorne. 2025. Linguistic generalizability of test-time
                                                           TÜBİTAK. 2026.         Ulusal bilim olimpiy-
  scaling in mathematical reasoning. In Proceedings
                                                             atları:  Geçmiş sınav soruları.    https:
  of the 63rd Annual Meeting of the Association for
                                                             //bilimolimpiyatlari.tubitak.gov.
  Computational Linguistics (Volume 1: Long Papers),
                                                             tr/tr/gecmis-sinav-sorulari.          2026
  pages 14333–14368, Vienna, Austria. Association
                                                             mathematics olympiad, first stage. Accessed
  for Computational Linguistics. ArXiv:2502.17407
                                                             2026-08-11.
  (MCLM).
                                                           Miles Turpin, Julian Michael, Ethan Perez, and
Mingyang Song, Zhaochen Su, Xiaoye Qu, Jiawei Zhou,          Samuel R. Bowman. 2023. Language models don’t
  and Yu Cheng. 2025. PRMBench: A fine-grained               always say what they think: Unfaithful explanations
  and challenging benchmark for process-level reward         in chain-of-thought prompting. In Advances in Neu-
  models. In Proceedings of the 63rd Annual Meeting          ral Information Processing Systems 36 (NeurIPS
  of the Association for Computational Linguistics (Vol-     2023).
  ume 1: Long Papers), pages 25299–25346, Vienna,
  Austria. Association for Computational Linguistics.      Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-
  ArXiv:2501.03124.                                          cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,
                                                             Geoffrey Irving, and Irina Higgins. 2022. Solving
Mingzhong Sun, Teresa Yeo, Armando Solar-Lezama,             math word problems with process- and outcome-
  and Tan Zhi-Xuan. 2026. An enigma of artifi-               based feedback. arXiv preprint arXiv:2211.14275.
  cial reason: Investigating the production-evaluation
  gap in large reasoning models. arXiv preprint            Mingyang Wang, Lukas Lange, Heike Adel, Yunpu
  arXiv:2606.01462.                                          Ma, Jannik Strötgen, and Hinrich Schütze. 2025a.
Accepted at MRL@EMNLP 2026



  Language mixing in reasoning language models: Pat-       Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan
  terns, impact, and internal causes. arXiv preprint         Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
  arXiv:2505.14815.                                          Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
                                                             Joseph E. Gonzalez, and Ion Stoica. 2023. Judging
Qian Wang, Zhenheng Tang, Zhanzhi Lou, Nuo Chen,             LLM-as-a-judge with MT-Bench and chatbot arena.
  Wenxuan Wang, and Bingsheng He. 2025b. Towards             In Advances in Neural Information Processing Sys-
  evaluating fake reasoning bias in language models.         tems 36 (NeurIPS 2023), Datasets and Benchmarks
  arXiv preprint arXiv:2507.13758. THEATER bench-            Track. ArXiv:2306.05685.
  mark.
Xumeng Wen, Zihan Liu, Shun Zheng, Shengyu Ye,             A     Experimental Setup
  Zhirong Wu, Yang Wang, Zhijian Xu, Xiao Liang,
  Junjie Li, Ziming Miao, Jiang Bian, and Mao Yang.        A.1    Prompts
  2026. Reinforcement learning with verifiable re-
  wards implicitly incentivizes correct reasoning in       Solver prompts. Every solver receives the prob-
  base LLMs. In The Fourteenth International Confer-       lem statement followed by one instruction sentence
  ence on Learning Representations (ICLR).
                                                           in the language of the benchmark:
Frank Wilcoxon. 1945. Individual comparisons by rank-
   ing methods. Biometrics Bulletin, 1(6).                       EN: Let’s think step by step and output the final
                                                                 answer within \boxed{}.
Edwin B. Wilson. 1927. Probable inference, the law of            TR: Adım adım düşün ve nihai cevabı
  succession, and statistical inference. Journal of the          \boxed{} içerisinde ver.
  American Statistical Association, 22(158):209–212.             PT: Vamos pensar passo a passo e apresentar a
                                                                 resposta final dentro de \boxed{}.
Shijie Xia, Xuefeng Li, Yixin Liu, Tongshuang Wu, and
  Pengfei Liu. 2025. Evaluating mathematical reason-
  ing beyond accuracy. In Proceedings of the AAAI            The Turkish line serves the AIME translation
  Conference on Artificial Intelligence, volume 39,        and the Turkish olympiad; the Portuguese line
  pages 27723–27730. ArXiv:2404.05692.
                                                           serves the AIME translation and the Portuguese
Zheng-Xin Yong, M. Farid Adilazuarda, Jonibek              exams.
  Mansurov, Ruochen Zhang, Niklas Muennighoff,
  Carsten Eickhoff, Genta Indra Winata, Julia Kreutzer,    Judge prompt. Figure 3 gives the English judge
  Stephen H. Bach, and Alham Fikri Aji. 2025.
                                                           prompt in full; it reproduces the verification
  Crosslingual reasoning through test-time scaling.
  arXiv preprint arXiv:2505.05408.                         prompt of Wen et al. (2026). The judge fills
                                                           {question} and {solution} and must end
Qinan Yu, Alexa Tartaglini, Peter Hase, Carlos Guestrin,   with \boxed{yes} or \boxed{no}.
  and Christopher Potts. 2026. Outcome rewards do
  not guarantee verifiable or causally important reason-
  ing. arXiv preprint arXiv:2604.22074.                    Multilingual variants. The Turkish and Por-
                                                           tuguese judge prompts are identical to the English
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai         one except for exactly two additions. First, the
  Wang, Yang Yue, Shiji Song, and Gao Huang. 2025.
  Does reinforcement learning really incentivize rea-      opening sentence tags the problem language: “a
  soning capacity in LLMs beyond the base model? In        given math problem (written in Turkish)” (respec-
  Advances in Neural Information Processing Systems.       tively Portuguese). Second, a fourth task is ap-
  ArXiv:2504.13837.                                        pended:
Raoyuan Zhao, Yihong Liu, Hinrich Schütze, and
  Michael A. Hedderich. 2026. A comprehensive eval-              4. **Language Consideration**:
  uation of multilingual chain-of-thought reasoning:             Ignore whether the solution is
  Performance, consistency, and faithfulness across              provided in Turkish, English, or
                                                                 a combination of both (language
  languages. In Findings of the Association for Compu-
                                                                 switching). Focus exclusively
  tational Linguistics: EACL 2026, pages 5223–5247.              on mathematical and logical
                                                                 correctness, disregarding the
Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji                 language used in the evaluation.
  Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jin-
  gren Zhou, and Junyang Lin. 2025. ProcessBench:
  Identifying process errors in mathematical reason-          Everything else (the task list, the error taxonomy,
  ing. In Proceedings of the 63rd Annual Meeting of        the output format, and the verdict convention) is
  the Association for Computational Linguistics (Vol-
  ume 1: Long Papers), pages 1009–1024, Vienna,
                                                           unchanged from Wen et al. (2026), so the multi-
  Austria. Association for Computational Linguistics.      lingual judgments are the same instrument as the
  ArXiv:2412.06559.                                        original English one up to these two additions.
Accepted at MRL@EMNLP 2026



You are an expert in mathematics and logical reasoning. Your task is to evaluate
 the correctness of a solution to a given math problem, with a **strong emphasis on
 the reasoning process**, not just the final answer.
 Below is the **Problem** and the **Solution (Provided by another AI model)**:
--
**Problem**:
{question}
**Solution (Provided by another AI model)**:
{solution}
--
 Please perform the following tasks:
1. **Analyze the solution step-by-step**, paying close attention to: -
 Computational accuracy - Logical consistency - Conceptual understanding - Whether
 the reasoning is valid and complete
 2. **Identify any issues or errors in the reasoning**, even if the final answer is
 correct. Classify them into the following categories (if applicable): -
**Calculation Error**: Mistakes in arithmetic, algebraic manipulation, or numerical
 computation. - **Logical Error**: Invalid reasoning, flawed logic, or incorrect
 inference. - **Conceptual Error**: Misunderstanding or misuse of mathematical
 concepts or definitions. - **Omission / Incompleteness**: Missing steps,
 incomplete justification, or not addressing all parts of the question. - **Other**:
Any other type of error that does not fit into the above categories.
 3. **Provide a final judgment** on whether the solution is logically sound and free
 of errors in reasoning.
 Please format your response as follows:
--
**Issues Identified:**
- [Issue 1]: [Classification] - [Brief explanation] - [Issue 2]: [Classification] -
 [Brief explanation] - ...
 Let’s think step by step and output your final judgment within \boxed{}
\boxed{yes} or \boxed{no}


Figure 3: The English judge prompt, reproduced from Wen et al. (2026). {question} and {solution} are
filled per judgment; the Turkish and Portuguese variants differ from it by the two additions given in Appendix A.1.


A.2   Configuration                                        Judge version. V4-Flash is the April 2026 pre-
                                                           view build of DeepSeek-V4-Flash, queried through
Serving and sampling. All models are served                the DeepSeek API before 31 July 2026, when the
with their family’s official chat templates: for the       same API name moved to re-trained builds; the
Qwen3.5 instruct models thinking is explicitly dis-        preview weights remain published.
abled or enabled, while base checkpoints run under
their template’s default thinking setting; sampling        Judging cost. Pass@k needs only the solver’s
parameters are set explicitly for every run. Ev-           generations, while CoT-Pass@k also sends ev-
ery solver draws 64 generations per question, and          ery answer-correct generation to the judge three
16 on the Portuguese exams, whose near-saturation          times. On the judge matrix of Section 5.2 the ten
makes larger samples uninformative and whose 166           solvers produced 78,080 generations with 416 mil-
questions keep the total sample count comparable           lion output tokens, of which 20,059 were answer-
to the other benchmarks. Our pipeline extends an           correct. Qwen3.6 and Gemma4 judged all of these,
open-source evaluation harness with these judging          60,177 judgments each, and V4-Flash and R1-
stages.                                                    distill, which cover the earlier generation only,
                                                           judged its 2,180 answer-correct generations, 6,540
                                                           judgments each, for 133,434 judgments and 797
Judge budgets. The judgment budget is 16,384               million judge output tokens in all. A judgment av-
tokens throughout, with two exceptions. V4-Flash           erages 3.5 thousand output tokens under V4-Flash
judges at 20,480 tokens wherever it appears, and           and 7.9 thousand under R1-distill, so judging one
in the error-injection study of Section 4.2 all three      correct solution costs 10 to 24 thousand tokens,
judges share that setting; the budget ladder of Sec-       and in the same cells Qwen3.6 and Gemma4 emit
tion 4.4 raises the anchor judge’s budget in step          0.82 and 0.92 tokens for every solver token, which
with the solver’s.                                         nearly doubles the output of a Pass@k evaluation.
Accepted at MRL@EMNLP 2026



    Variant                         any    majority   all    all-correct count a judgment that ends without a ver-
    V4-Flash                                                 dict as a rejection and majority-correct leaves it out,
    Clean                           96.2    92.9      89.2   which matters unevenly. Such judgments are 8.5%
    Intermediate numeric error      96.1    93.1      90.1   of Qwen3.6’s, touching one in five of its variants,
    Truncation error                89.3    85.1      78.8   reach fewer than one in a hundred of V4-Flash’s
    Final-answer error              47.2    18.1       6.4
    Consistent final-answer error   49.0    24.6      12.4   variants, and make up 16.5% of R1-distill’s, almost
    Qwen3.6
                                                             all ending without a boxed verdict rather than at the
    Clean                           99.4    97.8      81.2   token limit, which is why R1-distill’s all-correct
    Intermediate numeric error      99.2    98.2      81.0   rate falls to 36% on the clean control. Requiring
    Truncation error                93.9    92.1      69.2   two approvals outright would lower every Qwen3.6
    Final-answer error              67.2    34.3       7.8   rate by 1.7 to 5.3 points without reordering the five
    Consistent final-answer error   75.6    54.2      27.8
                                                             conditions, leave V4-Flash unchanged, and lower
    R1-distill
    Clean                           96.9    90.1      36.4
                                                             R1-distill’s rates by 2 to 11 points. R1-distill is also
                                                             unstable on identical input, splitting 22% of the
    Intermediate numeric error      96.0    91.9      42.2
    Truncation error                92.1    86.7      67.4   clean controls that received three verdicts between
    Final-answer error              91.9    70.6      28.3   approval and rejection, against 2% for Qwen3.6
    Consistent final-answer error   80.3    61.8      23.1   and 7% for V4-Flash.
                                                                Table 1 repeats the error injection experiment
Table 1: Acceptance rates (%) under the three verifi-
cation strategies of the original CoT-Pass@k judge: a
                                                             under all three strategies. No strategy detects the
variant is accepted when at least one of its three judge     intermediate numeric error, whose acceptance stays
generations approves it (any-correct), when more ap-         within 1 point of the clean control in all six com-
prove than reject (majority-correct), or when all three      binations of V4-Flash and Qwen3.6 and, for R1-
do (all-correct). The majority-correct column is the one     distill, falls at most 1 point below it, and in every
plotted in Figure 1. 720 original solutions per error type   combination of V4-Flash and Qwen3.6 the consis-
for each judge; R1-distill is the judge the metric speci-    tent final-answer error is accepted more often than
fies.
                                                             the plain one, while R1-distill orders the two the
                                                             other way under all three strategies. What the strate-
The error-injection study adds 32,400 judgments,             gies change is only how far apart they place the two
720 solutions in five variants, three judgments each,        groups. For V4-Flash and Qwen3.6, all-correct
under three judges. The jobs in our cluster’s ac-            separates them furthest, but relative to any-correct
counting add up to about 620 H200 GPU-hours of               it also rejects 7.1 points more of the unedited V4-
generation and open-weights judging, exploratory             Flash controls and 18.2 points more of the Qwen3.6
runs included; this is a lower bound, since runs out-        ones, so part of its strictness is disagreement be-
side that record, V4-Flash, which ran through the            tween generations of the same judge rather than
DeepSeek API, and the Qwen3.6 judgments of two               error detection.
error-injection cells, served through a commercial           Size and kind of the edit. Figure 4 splits the
API when the cluster was unavailable, are not in it.         same 720 solutions by how the wrong number was
Selecting solutions for error injection. The orig-           formed and by how far it moved. The intermediate
inal solutions of Section 4.2 are drawn from cor-            numeric error is missed whatever the edit, at 86 to
rectly answered generations that stopped before the          100% acceptance in every cell of every judge, and
max-token limit and are longer than 600 tokens,              its position between 40 and 70% of the chain moves
keeping only solutions to which all four error types         acceptance by at most 3 points. The plain final-
can be applied.                                              answer error is also insensitive to size, within 10
                                                             points across the four size bins. Only the consistent
B      CoT Verification Strategies                           final-answer error reacts to the size of the number.
                                                             A wrong answer within 1% of the correct one is
The original CoT-Pass@k judge turns the three
                                                             accepted 71% of the time by Qwen3.6, 34% by V4-
judgments of a solution into one verdict with a ver-
                                                             Flash and 69% by R1-distill, one more than double
ification strategy: any-correct accepts a variant if
                                                             the correct value 26, 9 and 49%.
at least one of its three judgments approves it, ma-
jority-correct if more of them approve than reject,          Rates per benchmark. Figure 1 gives the
and all-correct only if all three approve. Any- and          majority-correct rates per benchmark. The inter-
Accepted at MRL@EMNLP 2026




Figure 4: Acceptance (%, majority-correct) by the kind and the size of the injected edit, with 95% Wilson intervals,
for the three conditions that change a number (columns). Top, how the wrong number was formed; bottom, its
relative change |new − old|/|old|. Each row of panels partitions the same 720 solutions of every condition, and the
number of solutions in a category is given under its label.




Figure 5: Language of the error-injection study, by benchmark. Left, the 720 original solutions of Section 4.2
(Qwen3.5-4B and 9B, thinking mode), classed by the share of their letters, mathematics removed, in the benchmark’s
language (at least 80%, benchmark language), in English (at least 80%, English) or in between (mixed); the edits do
not change a chain’s language, so the five variants share the classification. Right, the judges’ output on the clean
controls, thinking and visible answer together, classed the same way. On English AIME every chain and every
judgment is English, so that benchmark is left out. Under the wrong-answer conditions Qwen3.6’s shares stay
within 1 point of these, R1-distill’s all-English share on the Turkish benchmarks falls from 36 to 37% to 19 to 26%,
and V4-Flash’s mixed share on the Portuguese exams falls from 10% to under 3%. Appendix C.5 gives the method.
Accepted at MRL@EMNLP 2026



mediate numeric error shifts no benchmark under                        Solver      Qwen3.6 Gemma4
any judge (exact McNemar on 144 solutions each,                        Q3.5-4B-B        0.8       1.6
smallest p = 0.30), and R1-distill’s loss of 15 to                     Q3.5-9B-B        0.0       0.8
                                                                       Q3.5-4B          4.9       6.6
27 points under a wrong final answer is significant                    Q3.5-9B          3.3       4.1
on every benchmark (p < 10−3 ). The Portuguese                         G4-E2B           8.2       8.2
exams carry the shortest solutions, a median of                        G4-E4B           7.4       4.9
3.7k tokens against 12k to 24k on the other four,                      Average          4.1       4.4
and every judge accepts their clean control at 99
to 100%. The Turkish olympiad gives each judge            Table 3: As Table 2, for the current-generation solvers
its lowest clean control and is the one benchmark         under the two judges that cover them. Q3.5 = Qwen3.5
                                                          (-B base), G4 = Gemma-4-it.
where V4-Flash accepts the consistent error less
often than the plain one; R1-distill does so there
and on the Portuguese exams as well (exact McNe-          C.2    The k Ladder and Question-Level
mar p ≤ 1.6 × 10−3 for all three reversals). On                  Uncertainty
the three AIME sets, the same problems in three
                                                          Figure 6 follows the same difference as the number
languages, the rates move together.
                                                          of sampled generations grows. Figure 7 reports the
C     Judges, Sampling and Uncertainty                    question-level bootstrap intervals quoted in the text,
                                                          per solver.
Two tables and six figures support Section 5.2, one          One row of Figure 7 needs a warning. Qwen3.5-
group per subsection.                                     9B-Base has a difference of exactly zero on each
                                                          of the four benchmarks, so every resample of its
C.1     The Judge Matrix                                  questions returns zero and its interval collapses to
Table 2 gives the difference Pass@64 − CoT-               a point. That is a structural limit of resampling an
Pass@64 for every earlier-generation solver un-           all-zero indicator, not a statement that the value is
der all four judges, and Table 3 for every current-       known without uncertainty, and the same applies
generation solver under the two judges that cover         to any cell-level interval of the form [0, 0].
both generations: together the per-model form of
the claim that the collapse does not depend on the
judge.
   The verdict threshold of Section 4.3 removes
from the comparison grid the Gemma-4 base check-
points (too few correct answers to support a rate),
Qwen3.5-0.8B (under the threshold on three of the
four benchmarks as a base checkpoint and on all
four in non-thinking mode) and Qwen3.5-2B (over
it only as a base checkpoint).

    Solver       Qwen3.6 Gemma4 V4-Flash R1-distill
    Q2.5-7B         15.6     13.9     18.0      15.6
    Q2.5-32B        20.5     22.1     23.0      21.3      Figure 6: The difference Pass@k − CoT-Pass@k
    Q2.5-7B-I       22.1     23.0     23.8      22.1      against the number of sampled generations, under the
    Q2.5-32B-I      20.5     20.5     21.3      21.3      anchor judge Qwen3.6 at 16k. Each solver is a weighted
    Average         19.7     19.9     21.5      20.1      mean over its four benchmarks, weighted by how many
                                                          questions each contributes; each curve is then the un-
Table 2: Pass@64 − CoT-Pass@64 per earlier-               weighted mean over the solvers of that generation. End-
generation solver (rows), averaged over the four 64-      points are labelled; Figure 7 gives the per-solver spread
sample benchmarks (weighted by how many questions         at k = 64.
each contributes, as in Figures 6 and 7) under all four
judges (columns). Judge generation budgets: 16,384 for
Qwen3.6, Gemma4 and R1-distill, 20,480 for V4-Flash;
                                                          C.3    Acceptance of Correct Generations
every judge runs in thinking mode with three judgments    Section 5.2 reports the collapse as the difference
per solution. The last row averages the solvers. Q2.5 =   Pass@64 − CoT-Pass@64, and at k=64 that dif-
Qwen2.5 (-I Instruct).                                    ference can shrink for a reason that has nothing
Accepted at MRL@EMNLP 2026



                                                           C.4   Saturation and Conditioning on c
                                                           The tick labels of Figure 9 give the number of
                                                           question and solver pairs in each bin of c. The
                                                           earlier generation’s solved questions sit at c ≤ 8,
                                                           where 80 of 116 pairs lose every correct generation,
                                                           and the current generation’s at c ≥ 33, where 1 of
                                                           287 does, so the saturation is real and it favours the
                                                           current generation. The figure then holds c fixed.
                                                           At every c the current generation keeps more of its
                                                           questions and more of its correct generations. At
                                                           c = 1–2 CoT-Pass@64 is 24 against 68 under the
                                                           anchor judge and the judge accepts 23% against
                                                           66% of the correct generations; at c = 33–64 it is
                                                           83 against 100 and 74% against 96%, so in both
Figure 7: Question-level bootstrap 95% intervals for       generations the judges reject most where a question
Pass@64 − CoT-Pass@64 under the anchor judge               holds few correct generations. The gap between
Qwen3.6 at 16k, in points, with the numeric interval       the generations therefore survives conditioning on
at the right of each row. Each solver is a weighted mean   c, and what saturation explains is only how the
over its four benchmarks, weighted by how many ques-       current generation’s remaining rejections, 4 to 34%
tions each contributes; mean is the unweighted mean
                                                           of its correct generations, turn into a difference of
over the solvers of a generation. 10,000 resamples of
questions, percentile intervals; cells are resampled in-   zero.
dependently. Q2.5/Q3.5 = Qwen2.5/Qwen3.5, G4 =
Gemma-4-it.                                                C.5   Language of the Chains
                                                           Solvers are prompted in the benchmark’s language
                                                           and their chains may switch into English (Sec-
                                                           tion 4.1). To measure how often, every answer-
                                                           correct generation of the judge matrix is stripped
to do with the judge. A question keeps its CoT-            of its mathematics (display and inline formulas,
Pass@64 as long as one of its correct generations          boxed answers, LaTeX commands, digits and op-
is approved, so where a question holds many cor-           erator symbols) and cut into lines and sentences of
rect generations the judge can reject most of them         at least twenty letters; each segment receives one
without moving the metric. Two figures, here and           label from GlotLID (Kargaran et al., 2023), and
in Appendix C.4, separate that saturation from the         segments that restate the question are dropped. A
verdicts. Figure 8 gives the quantity the difference       chain is target when at least 80% of its letters are
hides, the acceptance rate of answer-correct gener-        in the benchmark’s language, English when at least
ations, per solver and benchmark and under both            80% are English, and mixed otherwise. As a sec-
judges. The two generations never overlap, 57 to           ond layer, MaskLID (Kargaran et al., 2024), which
70% against 80 to 99% per solver, and on the na-           detects code switching by iterative masking, is run
tive Turkish olympiad the anchor judge approves            on the first 1,000 words of every earlier-generation
only 39 to 47% of the earlier generation’s correct         chain, of a fifth of the current generation’s chains
generations and 75 to 99% of the current gener-            and of every panel chain; the two layers agree on
ation’s. Averaged over the ten solvers the Turk-           whether a chain is mixed for 93% of the chains they
ish translation sits within 3 points of the English        share. Labels outside the three languages cover un-
original under both judges (Wilcoxon signed-rank           der 3% of the letters, and a threshold of 70 or 90%
test (Wilcoxon, 1945), p = 0.49), the Portuguese           changes the target share by at most one point.
translation runs 6 points above it under the anchor           The language of a chain is a property of the
judge (p = 0.004) and 3 above under Gemma4                 solver (Figures 10 and 11). The Qwen3.5 base
(p = 0.25), and the olympiad sits 15 and 14 points         checkpoints, which think by default, write 79 to
below the Turkish translation (p = 0.002), so the          93% of their chains on the non-English benchmarks
language of the problem does not lower the rate            in English and the rest mixed, while the instruction-
and the benchmark does.                                    tuned solvers of both generations answer in the
Accepted at MRL@EMNLP 2026




Figure 8: Acceptance rate of answer-correct generations per solver and benchmark, the share of a solver’s correct
generations whose reasoning chain the judge approved, under Qwen3.6 (top) and Gemma4 (bottom), for the solvers
of Section 5.2 at the 16k budget. The number above each bar is that rate in percent; the number at its base is the
count of answer-correct generations in the cell, given in parentheses after the rate where the bar is too short. The
rejected share is 100 minus the rate. The dark grey bar of each solver gives its rate pooled over the four benchmarks,
with the pooled count at its base, and the panel headers give the rate pooled over each generation. The vertical axis
starts at 30. Q2.5/Q3.5 = Qwen2.5/Qwen3.5 (-Inst instruct, -Base base), G4 = Gemma-4-it.


benchmark’s language at least 97% of the time;              benchmark’s language (Figure 5). There the ver-
only the Qwen2.5 base checkpoints split, and the            dicts move with the language under two judges on
Portuguese exams show the same division. Be-                the Turkish benchmarks. On the Turkish olympiad
cause the classes coincide with solvers, acceptance         V4-Flash accepts 94% of the mixed clean chains
by language cannot be read across solvers. Within a         against 69% of the all-English ones and R1-distill
solver the judges accept English and mixed chains           85 against 74%, and R1-distill also accepts the
alike, within 3 points for every Qwen3.5 base cell,         wrong final answer more often in a mixed chain, 72
and the one solver with enough chains of both               against 49% there and 73 against 63% on the Turk-
kinds, Qwen2.5-32B on the Turkish olympiad, is              ish AIME set; Qwen3.6 stays within 4 points on
accepted 48% of the time in English and 35% in              every clean control, and on the Portuguese bench-
Turkish.                                                    marks every judge’s clean controls stay within 7.

  The error-injection panel holds no chain in the              The judges themselves reason in English. On a
Accepted at MRL@EMNLP 2026




Figure 9: CoT-Pass@64 after conditioning on c, the number of a question’s 64 generations whose final answer is
correct, counted before judging, for the ten solvers of Section 5.2 at the 16k budget, pooled over the four benchmarks,
under both judges (rows), with 95% Wilson intervals. Left, the share of question and solver pairs in the bin in which
the judge approved at least one correct generation, which is CoT-Pass@64 for that bin since Pass@64 there is 100
by construction; right, the share of answer-correct generations in the bin that the judge approved, the acceptance rate
of Figure 8 at fixed c, so that the two generations can be compared at the same c. The tick labels give the number of
question and solver pairs in each bin, earlier | current. Per benchmark, the Turkish olympiad has the lowest value in
both panels in every bin of the earlier generation, and Figure 8 gives the acceptance rates per benchmark.


sample of 300 judgments per judge and benchmark
                                                                                        solver Gemma4       Qwen3.6
from the judge matrix, all four judges write 78 to
                                                              Benchmark        Solver   stops stops diff. stops diff.
100% of their judgments on the Turkish and Por-
tuguese benchmarks entirely in English and none in            AIME (EN)     Q3.5-4B      89.6   35.0 3.33 15.7 0.00
                                                                            Q3.5-9B      83.9   33.0 3.33 17.5 0.00
the benchmark’s language, whatever the language                             G4-E2B        0.2    2.1 6.67 6.5 3.33
of the chain (Figure 11). The error-injection panel                         G4-E4B        1.4    2.7 10.00 6.0 3.33
gives the same picture with one exception. On the             AIME (PT)     Q3.5-4B      47.7   53.5 13.33 5.2 0.00
                                                                            Q3.5-9B      44.0   49.8 0.00 3.6 0.00
two Turkish benchmarks R1-distill thinks mostly                             G4-E2B        0.1    9.8 3.33 1.4 3.33
in Turkish in 40 to 47% of its judgments while its                          G4-E4B        0.2    7.5 6.67 1.9 0.00
visible verdict stays in English, and the judgments           AIME (TR)     Q3.5-4B      44.2   51.0 0.00 10.0 0.00
it thinks through in Turkish approve more often, 78                         Q3.5-9B      35.6   53.8 10.00 8.3 0.00
                                                                            G4-E2B        0.5    7.6 3.33 3.0 3.33
against 64% of the clean controls on the Turkish                            G4-E4B        0.2    9.8 6.67 3.2 0.00
AIME set and 65 against 62% on the olympiad.                  TÜBİTAK (TR) Q3.5-4B      44.4   47.6 6.25 3.6 0.00
                                                                            Q3.5-9B      35.6   49.1 6.25 3.4 0.00
D     Token Budgets and Generation Mode                                     G4-E2B        0.8   13.6 3.12 0.2 0.00
                                                                            G4-E4B        0.0   10.3 9.38 0.1 9.38
D.1    Stops at the Max-Token Limit                           PT exams      Q3.5-4B       3.6    5.0 0.00 1.5 0.00
                                                                            Q3.5-9B       1.7    3.5 0.00 1.3 0.00
Table 4 supports Section 5.3 with the share of solver                       G4-E2B        0.1    0.7 0.00 0.2 0.60
                                                                            G4-E4B        0.0    0.4 0.00 0.2 0.00
generations and of judgments that stop at the max-
token limit, per benchmark and solver, with the              Table 4: Stops at the max-token limit on both sides, in
difference each judge reports.                               thinking mode at the 16k generation budget: the share
                                                             of solver generations that stop at the max-token limit
D.2    Judge Budgets and the Difference                      (stops, %), and per judge the share of its judgments that
Figure 12 decomposes the difference Pass@64 −                do, with the difference Pass@kmax − CoT-Pass@kmax
                                                             (diff.) under that judge. kmax is 64, or 16 for the Por-
CoT-Pass@64 that each judge reports, under the
                                                             tuguese exams; stop rates come from each generation’s
counterfactual of Section 4.4: judgments that stop           recorded finish state. Q3.5 = Qwen3.5, G4 = Gemma-4-
at the max-token limit are counted as approvals              it.
instead, and what survives is a lower bound on the
Accepted at MRL@EMNLP 2026




Figure 10: Language of the reasoning chains (left) and acceptance by language (right) for the answer-correct
generations of the ten solvers of Section 5.2 at the 16k budget, on the three non-English benchmarks pooled (top)
and on the Portuguese exams (bottom), where thinking runs stand in for the non-thinking runs they lack. A chain is
in the benchmark language when at least 80% of its letters, mathematics removed, are in that language, English
when at least 80% are English, mixed otherwise. Acceptance is the majority verdict of Qwen3.6 (filled) and Gemma4
(open); a class with fewer than 20 chains of a solver is not plotted, and n is the number of chains. The dotted line
separates the earlier generation from the current one. Pooling mixes benchmarks with different acceptance rates, so
within-solver comparisons are read per benchmark in Appendix C.5. Q2.5/Q3.5 = Qwen2.5/Qwen3.5 (-Inst instruct,
-Base base, -Think thinking mode), G4 = Gemma-4-it.


part carried by the judge’s verdicts, since a stopped       the anchor judge’s 19.7 points, 12.5 of Gemma4’s
judgment that would have rejected is credited as an         19.9, 18.6 of R1-distill’s 20.1, and 20.1 of V4-
approval. The scope is the fully crossed design of          Flash’s 21.5. Under the two judges that rarely stop
Section 5.3: the four current-generation solvers on         at their own limit the difference barely moves: the
the four 64-sample benchmarks, in both generation           earlier generation’s side of the generational contrast
modes, every cell scored by both judges at the 16k          is carried by verdicts, not by the judges’ budgets.
budget.
                                                            D.3    The Budget Ladder
  The same counterfactual applied to the earlier
generation certifies the other side of the contrast:        Table 5 supports Section 5.3: the two thinking-
the four Qwen2.5 solvers on the same four bench-            mode solvers of Section 4.2 at their low and raised
marks, every correct solution judged, at the same           generation budgets, row by row. The ladder is
16k solver budget. Crediting every stopped judg-            reported under the anchor judge alone: at the raised
ment as an approval leaves, of the average differ-          budgets Gemma4 stopped at its own max-token
ence each judge reports in Table 2, at least 15.2 of        limit so often that serving slowed and its runs could
Accepted at MRL@EMNLP 2026




Figure 11: Language of the answer-correct chains and of the judgments in the judge matrix of Section 5.2, per
benchmark. Top, the ten solvers at the 16k budget, earlier generation left of the dotted line and current generation
right of it (-Inst instruct, -Base base); bottom, a sample of 300 judgments per judge and benchmark. Classes as in
Figure 5. English AIME is left out, every chain and judgment there being English. Figure 10 gives the same shares
pooled over the three benchmarks together with acceptance by class.


                                                            not be completed, the instrument buckling under
                                                            the budgets it was given.

                                                            D.4   Generation Mode and Language
                                                            Table 6 supports Section 5.3: the same thirty AIME
                                                            problems in three languages, solved by the same
                                                            two solvers in both generation modes. Neither
                                                            reading of the language difference is more correct
                                                            than the other: both are conditional on a mode
                                                            and a budget a paper would ordinarily report in a
                                                            footnote.


Figure 12: The difference Pass@64 − CoT-Pass@64
per judge and solver mode, split into the part carried
by the judge’s verdicts (solid) and the part that disap-
pears when judgments stopped at the max-token limit
are counted as approvals (hatched). Cell means over
the four 64-sample benchmarks and the four current-
generation solvers, 16k budget on both sides.
Accepted at MRL@EMNLP 2026




Figure 13: Language of the answer-correct chains under the generation mode and the token budget of Section 5.3,
per benchmark. Top, the four current-generation solvers at the 16k budget in non-thinking and in thinking mode;
bottom, the two Qwen3.5 thinking-mode solvers at the low and the raised generation budget of the ladder (Table 5).
Classes as in Figure 5; English AIME left out. Turning thinking on moves every chain out of the benchmark’s
language, and raising the budget moves the mixed chains further toward English.



                       stops at max Pass@1 Pass@64
                        tokens (%)    (%)    (%)
Benchmark       Solver low    high low high low high         Mode         Lang. stops at max Pass@1 Pass@64
                                                                                 tokens (%)    (%)    (%)
AIME (EN)     4B       89.6   18.4 10.5 75.4 40.0 96.7
              9B       83.9    8.9 16.2 84.5 40.0 96.7       non-thinking EN            27.9     55.8      91.7
AIME (PT)     4B       47.7    7.6 51.0 71.0 83.3 93.3                    PT             2.4     54.7      95.0
              9B       44.0    3.8 55.3 78.2 80.0 96.7                    TR            16.6     35.7      88.3
AIME (TR)     4B       44.2    5.3 51.8 68.5 80.0 93.3       thinking     EN            86.7     13.4      40.0
              9B       35.6    2.9 62.6 76.0 90.0 93.3                    PT            45.8     53.2      81.7
TÜBİTAK (TR) 4B       44.4    6.0 45.4 65.5 87.5 93.8                    TR            39.9     57.2      85.0
              9B       35.6    3.0 55.4 75.4 90.6 93.8
                                                          Table 6: The same thirty AIME problems in English and
Table 5: The budget ladder: the same solver on the same   in the Portuguese and Turkish translations: Qwen3.5-
benchmark at its low and high generation budget. Low      {4B,9B} at the 16k generation budget, both modes.
is 16,384 tokens everywhere; high is 32,768, except       Columns give the share of generations that stop at the
65,536 on English AIME (the text explains the jump).      max-token limit, Pass@1 and Pass@64, averaged over
Share of solver generations stopping at the max-token     questions and over the two models.
limit, Pass@1 and Pass@64; thinking mode throughout.
4B/9B = Qwen3.5.
