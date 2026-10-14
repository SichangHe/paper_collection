                                         The Verifier is the Curriculum: Precision Sets the Return on Search in
                                                                  Code Self-Distillation
                                                       Chenyu Zhou1            Qiliang Jiang2       Shuning Wu3        Xu Zhou3 *
                                                               1 School of Engineering, Institute of Science Tokyo, Japan
                                                       2 College of Control Science and Engineering, Zhejiang University, China
                                         3 Department of Electrical and Computer Engineering, National University of Singapore, Singapore

                                                              zhou.c.76d6@m.isct.ac.jp          jiangqiliang@zju.edu.cn
                                                                    shuningwu@u.nus.edu       zhouxu_nus@u.nus.edu


                                                            Abstract                            1    Introduction
                                          Post-training a code generator against a learned      Post-training a code-generation model requires
arXiv:2607.09709v2 [cs.AI] 15 Sep 2026




                                          judge can optimize proxy features that raise          a signal that says whether a candidate is good.
                                          the score without improving the artifact. We          The dominant choice for open-ended generation
                                          study the opposite signal: a deterministic,           is a learned judge, an LLM or multimodal model
                                          judge-free filter that asks only whether a gener-
                                                                                                prompted to score the output. This is convenient
                                          ated project launches cleanly under a headless
                                          engine (STRICT- LAUNCH). Under this gate,             and correlates with human preference, but it has a
                                          rejection-sampling self-distillation compounds        structural failure mode: a learned judge maps an
                                          out-of-family generalization: on GameCraft-           output to a score through whatever surface features
                                          Bench, a 14B model raises the per-candidate           drive its prediction, and if any of those features is
                                          clean-launch rate on four held-out families           cheap to manipulate without improving the artifact,
                                          from 8.8% to 42.2%, and coverage at 32 candi-         a model optimized against the judge will find it.
                                          dates from 84% to 100%, the gold references’
                                                                                                GameCraft-Bench’s official judge has exactly such
                                          own ceiling, beating the supervised model on
                                          every one of the 25 held-out tasks; retraining        a feature (§4): an agent lifts the judge’s art score to
                                          under three independent seeds reproduces the          1.8× by swapping solid-color placeholders for real
                                          three-round climb at 13.3, 26.4, and 43.7%.           assets with the game’s code frozen.
                                          The gate costs one engine invocation per candi-          This paper takes the opposite stance on which
                                          date: no reward model, no judge.                      signal to train against. Rather than chase a better
                                          At a fixed admitted count, what governs the           learned judge, we make the training filter a deter-
                                          loop is verifier precision. Swapping only             ministic, judge-free execution check that exposes
                                          the gate for a lenient BUILD check erases the         no scalar score to optimize, and make it the gate
                                          gain (p = 0.0012); a matched gold-duplication         of an iterative self-distillation loop. A candidate
                                          control regresses below the supervised model
                                                                                                passes only if the materialized project launches
                                          (p = 0.018). Under a semantic gate on APPS,
                                          dialing fuel precision π from 1.0 to 0.25 at
                                                                                                cleanly under a headless engine: the engine returns
                                          fixed candidate count prices that fuel linearly:      exit code 0 with no parse, load, or resource error
                                          over 23 training seeds, half-clean fuel returns       (STRICT- LAUNCH)—a property of the artifact un-
                                          +3.59 percentage points (pp) against the +3.69        der a fixed engine, not an opinion.
                                          a linear rate predicts.                                  The GameCraft-Bench task (Luo et al., 2026)
                                          Under count-matched rejection-SFT only one            maps a one-paragraph brief to a complete Godot
                                          direction of verifier error carries a measurable      project from scratch (§3). A scene referencing a
                                          cost. Masking three quarters of every prob-           missing script, or a script with a parse error, yields
                                          lem’s correct candidates moves held-out trans-        nothing that runs: an artifact must execute, not
                                          fer by −0.03pp [−0.74, +0.63], while admit-
                                                                                                merely look plausible.
                                          ting a quarter of false positives moves it by
                                          −1.58pp. Search obeys the same gate: qua-                Our central finding is that under the STRICT-
                                          drupling the harvest budget is worth +1.62pp          LAUNCH gate, rejection-sampling self-distillation
                                          behind a STRICT gate and nothing distinguish-         compounds: each round’s gain accrues on top of the
                                          able from zero behind a PARTIAL one. Recall is        last at a fixed harvest budget. Starting from a super-
                                          nearly free; search pays only through a precise       vised model that launches cleanly on held-out fam-
                                          gate: the verifier is the curriculum.                 ilies only 8.8% of the time, three rounds of “gen-
                                         * Corresponding author: zhouxu_nus@u.nus.edu           erate on the training families, keep what launches
cleanly, retrain” lift the per-candidate clean-launch      (Mahmoud et al., 2026), systematic RLVR verifier
rate to 42.2% and push coverage of the 25 held-out         error can collapse training (Egashira et al., 2026),
tasks, at the full 32-candidate budget, from 84%           and at test time verifier precision bounds rejection-
to 100%, the gold-reference ceiling. The gains are         sampling gain (Lu et al., 2025). We establish the
significant at every round and come from the self-         offline, training-time case, holding the optimizer
generated fuel rather than from mere duplication           fixed so that a matched filter swap identifies the
of gold: an exactly duplicated gold control hurts.         verifier’s precision as the causal variable.
In self-distillation the acceptance filter defines the
next training distribution, so what it certifies is what   How much precision is enough. Two concurrent
the model learns: the verifier is the curriculum.          lines put a number on verifier reliability from the
                                                           online side. Plesner et al. (2026) find RLVR within
Contributions. We introduce a deterministic,               2pp of a clean baseline at label noise up to 15%,
judge-free launch gate: one engine invocation, no          and Cai et al. (2025) model an unreliable verifier as
reward model to train, no judge to query. Under            a reward channel with asymmetric error rates. But
it self-distillation compounds out-of-family, beat-        a scalar rate cannot say which direction of error
ing the supervised model on every one of the 25            to spend a budget on: the noise in Plesner et al.
held-out tasks; an execution-grounding readout             (2026) is symmetric and resampled each epoch,
that the gate never optimizes rises over the same          and they name the missing piece themselves—their
rounds (§6). We identify verifier precision as the         precision-over-recall conclusion needs “a system-
causal variable under two verifier classes (execu-         atic controlled study varying FPR and FNR inde-
tion and semantic), and measure its conversion rate:       pendently, including fixed noise”. That study is
admitted correctness converts into held-out gain           what §8 reports, offline and on policy. On the
at an approximately constant rate over fuel preci-         online side the sharpest prediction is Rad et al.’s
sion π ∈ [0.25, 1] (§7, §8). And we give the error         (2026) bandit analysis of GRPO under noisy veri-
accounting for that axis. Under count-matched              fication, in which the drift on incorrect reasoning
rejection-SFT the cost is carried almost entirely by       modes is governed by the Youden index alone. Our
false positives, so a gate may spend three quarters        two corrupted arms sit at that same index yet do
of its recall for free as long as the surviving pool       not train alike (§8). Gureja et al. (2025) report the
still fills the quota. The harvest budget Kh , by con-     complementary regime of model-generated tests,
trast, pays only through a precise gate: STRICT at         where relaxing an all-tests-pass criterion recovers
Kh = 8 beats PARTIAL at 32 on a quarter of the             valuable training data that a rigid one discards.
generation and verification (§10). Finally, we lo-
cate that accounting in the learning interface: swap       Amplification versus reach. A distinct ques-
the optimizer for GRPO at a matched Youden in-             tion is whether self-training acquires capability
dex (TPR − FPR) and the training signal reverses,          beyond the base or only expresses what the base
the false-negative arm drawing more gradient and           already has. On a free-verifier synthetic domain,
spending it pushing away from trajectories that in         Strozzi (2026) report the latter and make the dis-
fact passed (§8).                                          tinction decidable through a pass@K crossover;
                                                           Qi et al. (2026) find a persistent gap between self-
2   Related work
                                                           generated and oracle supervision in closed-loop
Self-training and verifier quality. Bootstrap-             self-evolution. Both bear on the capability the loop
ping a model on its own filtered generations is            ends with; ours is about the curriculum it trains on.
well established, in STaR (Zelikman et al., 2022),         What we add is the precision axis both setups hold
V-STaR (Hosseini et al., 2024), ReST and ReST-             fixed: their verifiers are exact.
EM (Gulcehre et al., 2023; Singh et al., 2024),
and rejection-sampling fine-tuning for math (Yuan          Capacity versus verifier precision. Self-
et al., 2023), with recent on-policy, code, and            improvement has a capacity prerequisite (Song
consensus-gated variants (Zhao et al., 2026; Zhang         et al., 2025), but there the model verifies its own
et al., 2026; Stein et al., 2026). A concurrent line       outputs, coupling capacity to verifier precision. An
asks how the quality of the signal, rather than the        external, deterministic verifier decouples them: we
optimizer, governs the loop: weak rubric verifiers         vary precision at fixed capacity (§7) and capacity
yield proxy gains that fail a cross-family panel           at a fixed verifier (§9).
Gameable judges and verifiable game gener-                 benchmark’s visual judge is gameable: even ran-
ation. Automatic judges and benchmarks are                 domly chosen CC0 sprites lift its art score, though
known to be cheatable (Amodei et al., 2016; Zheng          it scores a fixed frame consistently (σ < 0.01; Ap-
et al., 2025; Zhong et al., 2025; Thaman, 2026;            pendix A).
Mahmoud et al., 2026; Helff et al., 2026), and a
growing line studies code/game generation against          A verification ladder. We order the available sig-
executable checks instead (Chi et al., 2026; Sun           nals by how much they certify (Appendix Fig. 4)
et al., 2026; Jiang et al., 2026; Zhang et al., 2025;      and train against the strongest rung that is still
Jia et al., 2026). We use GameCraft-Bench (Luo             a fixed engine predicate with no tunable score.
                                                           BUILD , the rung below STRICT- LAUNCH , only
et al., 2026) to ask how a judge-free execution filter
shapes what post-training transfers.                       opens the project headless and quits; parse errors
                                                           are not fatal. Read as verifiers, the rungs differ
3   Setup: the GameCraft-Bench task                        in precision: BUILD accepts 887 of the 888 candi-
                                                           dates the supervised model generates on the train-
GameCraft-Bench (Luo et al., 2026) poses end-to-           ing families; only 73 of those (8.2%) also pass
end game synthesis: given a short design brief, a          STRICT- LAUNCH . We test the consequence of a
model must emit a complete, runnable Godot 4               weaker rung in §7.
(Linietsky et al., 2014) project. A valid output
contains, at minimum, a project.godot en-                  5   Method: launch-gated iterative
gine configuration, one or more .tscn scene files,             self-distillation
the .gd scripts that implement behavior, and a             The procedure is rejection-sampling self-
demo_outputs/ trace of recorded input events               distillation (Zelikman et al., 2022; Gulcehre et al.,
that exercises the game. The benchmark’s official          2023; Yuan et al., 2023) with one deliberate
metric, OVERALL, is produced by a GPT-5.5 visual           choice: the acceptance filter is the deterministic
judge that renders the running game and scores it          STRICT- LAUNCH gate of the verification ladder of
on multiple qualitative axes.                              §4, applied only to training-family briefs. Matched
Why from-scratch projects are hard. Correct-               controls isolate that signal; Appendix Algorithm 1
ness is conjunctive across heterogeneous compo-            states one round.
nents (engine config ∧ scene graph ∧ scripts ∧             Rounds. Round 0 produces the supervised model
resources): the engine refuses to run if a scene ref-      M0 (SFT), trained on the 111 gold training-family
erences a script that fails to parse, if a resource path   projects; we write RFT-rt for the model after t
is malformed, or if an autoload errors at startup. A       rounds of this rejection-filtered training. Each sub-
snippet that almost works still resembles its target;      sequent round generates candidates with the previ-
a project that almost coheres does not run at all.         ous model, harvests its clean self-generated set (the
                                                           fuel), appends it to the gold pool, which remains
Families and the held-out split. The benchmark
                                                           the anchor, and retrains a fresh LoRA from the base.
groups its 140 tasks into 15 game families (plat-
                                                           The fuel grows every round (67 clean projects from
former, strategy, roguelike, simulation, . . . ). We
                                                           M0 , 123 from M1 , 186 from M2 ).
split the families three ways to measure cross-
family rather than in-distribution generalization:         Generation and training. Each round retrains
10 for training (111 gold projects), four held out,        a fresh LoRA (Hu et al., 2022) on Qwen3-14B
which the model never trains on (horror, rhythm,           (Qwen Team, 2025) and harvests Kh = 8 candi-
puzzle, shooter; 25 tasks), and one (4 tasks) ex-          dates per brief with vLLM (Kwon et al., 2023); the
cluded from both. The self-distillation harvest like-      full configuration is in Appendix C. For harvesting,
wise draws only from training-family briefs (Ap-           STRICT- LAUNCH is paired with a fixed three-file
pendix C).                                                 minimum, held constant in every control below.

4   Which signal to train against                          Evaluation protocol. The primary metric is the
                                                           per-candidate clean-launch rate, with all com-
We call a filter gameable if a cheap transforma-           parisons paired by task and tested by cluster-
tion of the artifact raises its score while leaving        permutation within each task (N = 25);
task-relevant executable behavior unchanged. The           coverage@K (a task is covered if any of its candi-
Table 1: Results on the four held-out families (25 tasks).   rates (Table 1, 3-seed column) are monotone in ev-
The per-candidate clean-launch rate (over four decod-        ery seed and end above the single-run trajectory.
ing seeds) carries a Wilson 95% CI describing each
                                                             Every family reaches full coverage by round 3 (Ap-
arm’s own candidate pool; all between-arm compar-
isons use the paired task-level tests of §5. The 3-seed      pendix Table 4).
column reports arms retrained under three training seeds
                                                             The gains are functional. The gains are not con-
(mean ± s.d.).
                                                             fined to the axis the gate reads. An execution-
model             per-candidate %     3-seed    cov.@32 %    grounding signal that steps the headless Scene-
                                                             Tree shows the number of held-out tasks with
SFT                8.8[7.0,10.9]        —          84
RFT-r1            13.6[11.4,16.2]    13.3±0.7      88        a grounded clean candidate (score ≥ 0.50; Ap-
RFT-r2            30.9[27.8,34.2]    26.4±1.6     100        pendix B) rising monotonically, 10 → 12 →
RFT-r3            42.2[38.9,45.7]    43.7±1.5     100
                                                             14 → 15 of 25 (Appendix Fig. 6). A blind brief-
CTRL (gold-dup)     5.6[4.2,7.4]        —           84       compliance judge, never a training signal, counts
BUILD -gated        8.6[6.9,10.8]       —           84
GEN - SWAP         22.4[19.6,25.4]      —          100       projects that both launch and implement their brief:
                                                             5.0 → 7.4 → 12.4 → 14.4 per 100 candidates (both
gold ceiling            100             —          100
                                                             signals and their controls in Appendix B).

dates launches cleanly) is
                                                             7   Mechanism: verifier precision is the
                     n−c
                         reported
                           n
                                  with the unbi-
                                                                 causal variable
ased estimator 1 − K / K (Chen et al., 2021)
at K = 32 (n candidates pooled per task, c of                Three matched controls at a fixed fuel budget locate
them clean). We write +a/−b for the numbers                  the gain.
of held-out tasks an arm improves and worsens.
Per-configuration budgets and coverage estimators            Exact duplication regresses (Appendix Fig. 3).
are in Appendix Table 5.                                     CTRL adds 67 exact duplicates of gold training
                                                             projects, matched per task to round 1’s fuel. It
6    Results                                                 regresses below SFT: 5.6% per-candidate against
                                                             8.8% (+7/−13, p = 0.018). It buys no cover-
Compounding to the gold ceiling. Table 1 gives               age: at K = 32 CTRL sits at SFT’s 84% (Table 1).
the main result (per-round trajectory in Appendix            The 67 copies fall on the 48 of 111 training tasks
Fig. 8). Under the STRICT- LAUNCH gate, three                round 1 already covers, doubling their weight. Self-
rounds of self-distillation lift the per-candidate           distilled round 1 at the same budget beats CTRL
clean-launch rate on the four held-out families from         +16/−5, p < 10−4 , in every leave-one-family-out
8.8% to 42.2%. Task-level coverage at the full 32-           fold (p ≤ 0.017).
candidate budget rises from 84% to 100%, the gold-
reference ceiling, with no crossover within the sam-         Each round’s fuel is better, not just larger.
pled budget (Appendix Fig. 7). Coverage saturates            Holding budget and coverage fixed, drawing
by round 2, so the round-over-round compounding              round 1’s count of fuel from a later generator (GEN -
is carried by the per-candidate rate rather than by          SWAP) isolates fuel quality: +8.8pp over round 1 it-
coverage. On the four tasks the supervised model             self (22.4 against 13.6), +20/−3, p < 10−4 , nearly
never solves within its full 32-candidate pool, it           twice round 1’s gain over SFT, so the loop com-
needs 25–35× as many draws to match a single                 pounds.
distilled draw (Appendix D).
                                                             A matched filter swap erases the gain. The
Significance at every round. The improve-                    BUILD -gated control reruns round 1’s loop with
ments survive paired, task-level testing (cluster-           the data source fixed and only the filter changed:
permutation, N = 25): round 1 over SFT gains                 STRICT- LAUNCH swapped for the lenient BUILD
+4.9pp (95% CI [+1.9, +8.1], p = 0.0017);                    rung (§4). Because BUILD accepts nearly ev-
round 3 gains +33.5pp (95% CI [+27.9, +39.6],                ery candidate while STRICT- LAUNCH accepts few,
p < 10−4 ) on every one of the 25 tasks (≥ +4/32             the count-matched BUILD fuel is 81% STRICT-
clean candidates each).                                      LAUNCH-broken (54/67). Trained on it, the model
                                                             reaches only 8.6% per-candidate clean-launch on
Robustness and per-family coverage. Under                    the held-out families: indistinguishable from SFT
three independent training seeds the round-wise              (8.8%, paired p = 1.0) and far below round 1’s
13.6% (+5/−16, p = 0.0012). Changing only the            We retrain M0 on each set under the same recipe;
verifier’s precision—nothing about the optimizer,        we evaluate pass@1 and coverage@8 over eight
the budget, or the task distribution—erases the en-      training seeds on the 470 held-out problems (three
tire first-round gain: what transfers depends on the     decoding seeds each), paired per problem.
acceptance signal. The supervised model’s candi-
                                                         Transfer rises sharply with gate strictness (Ap-
dates break exactly where the gate looks: 815 of
                                                         pendix Table 6). STRICT-gated self-distillation
888 fail STRICT- LAUNCH, every one on a parse
                                                         raises held-out pass@1 from 20.4% to 25.5%
error (Appendix B).
                                                         (+5.15pp [+4.14, +6.20], p = 0.0002) and
   Volume is not the binding constraint. Cut-
                                                         coverage@8 from 41.5% to 44.8% (+3.32pp
ting round 1’s fuel from 67 projects to 8 still
                                                         [+1.61, +5.06], p = 0.0002) on the same 470
lifts per-candidate clean-launch to 11.3% (+2.5pp
                                                         problems as Fig. 1. The controls separate by
[+0.4, +4.8] vs. SFT; −2.3pp [−5.3, +0.3] vs. full
                                                         gate strictness rather than by volume: LENIENT
fuel).
                                                         leaves pass@1 untouched (−0.10pp) while cut-
Precision buys coverage. Across rounds the self-         ting coverage@8 by 3.16pp (p = 0.0004); PAR -
distilled fuel covers 48, then 77, then 101 of the 111   TIAL moves pass@1 by +2.11pp (p = 0.0002);
training tasks (9 → 10 → 10 families) with almost        and STRICT beats PARTIAL in a direct paired test
no duplication, whereas the exact-duplication con-       (+3.04pp, p = 0.0002). At equal candidate count
trol re-covers the same 48 tasks and regresses (Ap-      this repeats the conclusion of Godot’s filter swap
pendix Fig. 3). High precision thus buys coverage        (§7), now under a semantic verifier and against
rather than costing it, inverting the usual trade-off    a graded ladder. The ordering is stable across
(Kynkäänniemi et al., 2019): a binary launch gate        eight independent training seeds that vary LoRA
certifies only that the project runs, so rounds har-     initialization and data order: STRICT beats every
vest novel working variants. The same widening           other arm in every training seed. At a fixed task
appears at 8B, where the fuel reaches 31 → 51 → 75       mix the ordering holds: on the 173 training prob-
of the 111 training tasks (Appendix C).                  lems that all three gates cover, STRICT still beats
                                                         PARTIAL (+3.3pp, p = 0.016); on the 96 held-
8   Pricing the fuel: a semantic gate in                 out problems that M0 never solves, STRICT gains
    competitive programming                              +3.4pp (p = 0.0002, cross-fitted on held-out de-
                                                         coding seeds). The ordering does not hinge on
The precision axis above is established with an ex-      the controls excluding all-pass candidates: against
ecution gate. We test it under a second class of ver-    a gate rebuilt to admit any candidate passing at
ifier, one that checks correctness rather than execu-    least half the tests, all-pass included, STRICT still
tion: APPS introductory competitive-programming          leads by +0.98pp [+0.49, +1.46] (p = 0.0004) in
problems (Hendrycks et al., 2021), where a can-          all eight seeds.
didate is accepted only if it passes all hidden unit
tests. Unlike the binary launch signal, a unit-test      A linear conversion rate. The ladder above
suite admits a graded verdict, so we can ask not         varies which rule admits a candidate. To isolate pre-
only whether a precise gate beats a lenient one but      cision itself with a constructed clean arm (frozen
whether the most precise gate is best.                   per-problem histogram; not Appendix Table 6’s
                                                         harvested STRICT), we hold the task set, gold pool,
Setup. We lightly supervise Qwen3-4B on 300              and candidate count fixed and vary only π, the frac-
APPS-introductory solutions (one epoch), giving          tion of the 1300 fuel candidates that actually pass
an APPS model, again M0 , that solves 20.4% of           all tests. Injected false positives displace clean can-
470 held-out problems at pass@1. From M0 we              didates on the problems the clean arm already cov-
harvest Kh = 8 candidates on each of 1500 training       ers. We measure this ladder over 23 training seeds
problems and score every candidate on the unit-test      and 470 held-out problems (150 as elsewhere, plus
ladder; 527 problems yield an all-pass candidate.        320 further APPS problems), under the crossed
We then build three count-matched fuel sets (1300        seed×task bootstrap defined in Appendix C. Trans-
candidates each, gold held fixed) differing only in      fer then tracks precision at a constant rate (Fig. 1):
the gate that admitted them: STRICT (all tests pass),    the arms gain +7.39, +6.32, +5.37, +3.59, and
PARTIAL (at least half the tests pass, but not all),     +1.89pp over M0 at π = 1.0, 0.875, 0.75, 0.5, and
and LENIENT (syntax-valid, but not all tests pass).      0.25, monotone across all five. Measured against
     held-out pass@1 gain (pp)
                                                                         other way. From a frozen Kh = 48 harvest we
                                 8
                                                                         build a second ladder that fixes the admitted count
                                 6                                       and varies the direction of the error: CLEAN (all-
                                                                         pass), FP 25 (a quarter of the slots replaced by same-
                                 4                                       problem, syntax-valid, non-all-pass completions),
                                 2                                       FN 25/ FN 50/ FN 75 (one quarter, one half, and three
                                                                         quarters of every problem’s true positives masked),
                                 0                                       and MIX (a 25% error budget split evenly between
                                 1
                                                                         the two directions). All six arms carry an identical
residual
  (pp)




                                 0                                       per-problem slot histogram at a common count-
                          −1                                             matched quota of 944 rows, over eight training
                                     0.25   0.50       0.75 0.875 1.00
                                            fuel precision π
                                                                         seeds, so they differ only in which kind of error the
                                                                         verifier makes.
Figure 1: Linear conversion of clean fuel into transfer.                    Removing three quarters of every prob-
Held-out gain over M0 (pp) against fuel precision π, the                 lem’s true positives moves the held-out rate
fraction of the admitted candidates that pass all tests.                 by −0.03pp (95% CI [−0.74, +0.63]), against
The APPS arms are controlled: π is set by construction
                                                                         −1.58pp [−2.23, −0.95] for a quarter of false posi-
at fixed task set, gold pool, and candidate count (1300).
Dashed: the linear rate π ∆(1), where ∆(1) is the gain                   tives; no false-negative rung is distinguishable from
from clean fuel. Lower panel: residuals from that rate.                  CLEAN, while every false-negative rung beats FP 25
Bars are 95% crossed seed×task bootstrap CIs over 23                     directly (+1.43, +1.74, +1.55pp; every interval
training seeds and 470 problems.                                         clear of zero).
                                                                            The MIX arm makes the accounting explicit.
                                                                         Splitting the error budget evenly moves the rate by
the linear rate π ∆(1), the residuals at π = 0.875,                      −0.87pp [−1.56, −0.18], while its false-positive
0.75, 0.5, and 0.25 are −0.14, −0.17, −0.10, and                         half alone predicts −0.79pp: the two agree within
+0.04pp, each with its own 95% CI covering zero                          0.08pp. At a fixed admitted count, then, the
and contained in ±0.55pp: halving the admitted                           damage is almost entirely a function of the false-
correctness returns +3.59pp where the rate predicts                      positive rate, and a gate’s recall is very nearly free,
+3.69. Precision therefore prices the fuel it admits:                    because it costs no problem coverage: the false-
a batch of precision π buys about π of what clean                        negative arms keep each problem’s slot count by
fuel buys. The price is steep. Every rung sits below                     construction. A larger harvest budget buys the other
clean fuel: the gap ∆(1) − ∆(π) has its interval                         thing: problems the loop did not cover before (§10).
clear of zero, from 1.07pp [0.84, 1.30] at π = 0.875                        Precision is the active variable, not a stand-in
up to 5.50pp [4.76, 6.29] at π = 0.25.                                   for how much correct data clears the gate: at a
   The rate also holds out of sample. The 320                            fixed admitted count and a fixed number of updates,
problems are disjoint from the 150 used elsewhere                        replacing a quarter of the true positives with copies
and entered only after the 150-problem analysis                          of the survivors costs nothing measurable, while
was fixed, so they are a held-out replication rather                     replacing them with false positives costs 2.57pp
than a larger sample. On that increment alone                            [1.75, 3.50] in all eight seeds (Appendix C).
the five arms gain +7.77, +6.66, +5.63, +3.82,
and +2.05pp, strictly monotone with every inter-                         The ordering belongs to the learning interface,
val clear of zero, and the four residual intervals                       not to the data (Appendix Table 3). That rank-
again all contain zero, within ±0.72pp. The rate                         ing is a statement about offline rejection sampling,
is not confined to constructed ladders. Two gates                        where the gate decides which rows enter a fixed-
built by thresholding the unit-test fraction, admit-                     size training set: a false positive writes a wrong tra-
ting at ≥ 25% and at ≥ 50% with all-pass included,                       jectory into the fuel, while a false negative merely
realize π = 0.44 and 0.58; over eight training seeds                     withholds one of many interchangeable right ones.
their gains land on π ∆(1) within 0.10pp.                                An on-policy learner meets the same two errors on
                                                                         different terms, because the verifier is the reward
Only false positives are paid for (Appendix                              rather than the filter: a false negative there does not
Fig. 5). The ladder above moves precision by                             withhold a row but penalizes a trajectory the model
injecting false positives; a gate can also err the                       in fact got right. We therefore repeat the contrast
with the optimizer swapped and everything else            we hold that recipe fixed—verifier and gold task
held fixed: the same two corruption directions at a       families unchanged—and ask only whether the fuel
25% dose of each, but GRPO (Shao et al., 2024) in         itself is Qwen-specific.
place of rejection-SFT, over eight training seeds per
arm as in the offline experiment (run configuration       Cross-scale: three rounds compound at 8B. At
in Appendix C). Each dose is a confusion-matrix           8B (Qwen3-8B+LoRA, identical recipe, five de-
rate; because each arm perturbs one direction only,       coding seeds) the loop runs the full three rounds
the two match the Youden index J = TPR − FPR              and compounds monotonically: per-candidate
to within 10−4 , as in Rad et al. (2026).                 clean-launch climbs 3.5 → 6.2 → 9.3 → 17.0%,
   Held at that index, the two directions do not          and coverage@32 (unbiased, same estimator as
train alike. A clean verifier leaves 48.8% of rollout     Table 1) rises 50.8 → 69.1 → 83.6 → 99.5%.
groups with no learning signal at all: every member       The per-candidate rate gains +13.5pp over the
earns the same reward, so the group-relative advan-       supervised model (bootstrap [+9.9, +17.7], p <
tage vanishes. Masking a quarter of the true posi-        10−4 ), with the third round alone worth +7.7pp
tives cuts that share to 14.1%, and false positives       ([+4.3, +11.3], p = 0.0004). One round buys
cut it to 36.7%. Both hold in all eight training seeds.   +2.7pp here against +4.9pp at 14B, so 1.75× the
The false-negative arm therefore receives more gra-       parameters is worth 2.2pp of one-round gain, under
dient than the clean one in every seed, not less          the same recipe, gate, and task families (per-scale
(Appendix Table 3), and spends it pushing away            evaluation budgets in Appendix C). The gate’s ad-
from trajectories that in fact passed: measured by        vantage persists at this scale: three launch-gated
the uncorrupted verifier, the policy’s own rollouts       rounds stand +12.3pp above one BUILD-gated
score 0.608 against the clean arm’s 0.696. Injected       round ([+8.3, +16.6], p < 10−4 ). The loop sur-
false positives push toward trajectories that in fact     vives a halving of scale: at 4B one launch-gated
failed, and push less, because a group in which           round lifts per-candidate clean-launch from 2.00%
every rollout already passes offers nothing to flip.      to 4.17% (+2.17pp, bootstrap [+0.67, +3.75], p =
What eight seeds resolve here is the training sig-        0.016 over six decoding seeds, and positive in all
nal, which separates in every one of them; held-out       six) and coverage@48 from 56.0% to 68.0%.
transfer points the same way (FN − FP = −1.90pp
                                                          Every base produces fuel once the recipe is con-
[−5.08, +0.96] over all 150 problems).
                                                          trolled. Every base we tried, across three lin-
The loop compounds under a semantic gate                  eages, produces STRICT- LAUNCH-clean fuel at 2.1–
too. A second STRICT-gated round continues the            9.6% per candidate on the canonical 111 training
climb: harvesting from round 1 and retraining             tasks (888 candidates per base, 8 per task), under a
from the base adds +2.6pp over round 1 (95% CI            recipe matched across bases in supervised data, se-
[+1.4, +3.9], p < 10−4 ; +7.9pp over M0 , on the          quence budget, and adapter placement (Appendix
150-problem set), with coverage@8 rising mono-            Table 2); the highest fuel rate in the sweep belongs
tonically (42.9 → 48.0 → 49.3%). The fuel com-            to Gemma-3-12B, above Qwen3-14B.
pounds too: the number of training problems yield-
ing all-pass fuel grows from 527 to 660 (+25%),           10   Search is a multiplier, not a substitute
outpacing the gain in pass@1. The gate widens             Back on APPS, raising only the candidates drawn
what the loop covers at a fixed harvest budget            per problem to Kh = 32, with model, adapter,
rather than polishing the part it already covers (Ap-     decoding, fuel selection, training, and evalua-
pendix C).                                                tion held fixed, gains +2.44pp ([+0.97, +4.03],
                                                          p = 0.0025). That invites the obvious econ-
9   How far this goes: scale
                                                          omy: sample more and check less. It does
The BUILD swap and the APPS precision ladder              not work. We cross the two knobs directly on
both hold the base fixed and vary the verifier. The       the same frozen APPS pool (Fig. 2): gate in
complementary swap, varying the base at a fixed           {STRICT, PARTIAL} crossed with Kh in {8, 32},
verifier, asks how far the loop travels. We rerun the     four count-matched arms at a common 900-row
full loop (supervised fine-tuning on the same 111         quota, eight training seeds, all built from prefixes
gold projects, then STRICT- LAUNCH-gated self-            of the same candidates, one round from M0 (a dif-
distillation) across model scale; across lineages         ferent estimand from the +2.44pp above). Quadru-
                           STRICT: +1.62 [+0.72, +2.60]                        our setting, precision is the cheapest of the three
                      28
held-out pass@1 (%)
                                                                               axes and the one that returns the most.
                      27
                      26                                                       11    Conclusion
                                                             +1.78pp
                      25                                     at 1/4 the cost   The verifier is the curriculum. Under a determin-
                      24                                                       istic, judge-free launch gate, rejection-sampling
                      23                                                       self-distillation compounds to the gold-reference
                           PARTIAL: +0.31 [−0.47, +1.17]
                                                                               coverage ceiling on held-out families. Precision
                           8                          32
                                                                               sets how high the loop climbs, at a rate one can mea-
                           harvest budget Kh (candidates per problem)
                                                                               sure: a lenient filter erases the gain (§7), and under
  Figure 2: Search is a multiplier, not a substitute. Held-                    a semantic gate admitted correctness converts into
  out pass@1 for the four count-matched APPS arms, as                          held-out gain at an approximately constant rate, so
  means over eight training seeds on 150 held-out prob-                        fuel of precision π retains about π of what clean
  lems; thin lines are the individual seeds. Every contrast                    fuel buys (§8).
  is paired by seed.
                                                                                  Every base we tried, across three lineages, sup-
                                                                               plies fuel (§9); on the four tasks the supervised
                                                                               model never solves within budget, the distilled
pling the harvest is worth +1.62pp [+0.72, +2.60]
                                                                               advantage is a 25–35× sampling-efficiency gain
of held-out pass@1 behind the STRICT gate, in
                                                                               (Appendix D). The gate needs no domain-specific
all eight seeds, and is indistinguishable from
                                                                               retuning: the same all-or-nothing rule applies to
zero behind PARTIAL (+0.31pp [−0.47, +1.17]);
                                                                               a launch check and to a unit-test check. Where a
the paired STRICT-minus-PARTIAL premium is
                                                                               verifiable predicate exists for the artifact, precision
+1.31pp [+0.85, +1.83] (all eight seeds positive).
                                                                               is what to buy first.
The STRICT gate at the low budget still beats the
PARTIAL gate at four times the budget, by +1.78pp                              Limitations
[+0.65, +2.94] (p = 0.0026, in all eight seeds).
And the gate’s own advantage widens as the budget                              Our main compounding loop is studied on a single
grows, from +2.09pp [+1.05, +3.15] at Kh = 8 to                                engine (N = 25 held-out tasks); the precision axis
+3.40pp [+2.17, +4.67] at Kh = 32: what a larger                               replicates in a second domain under a semantic
budget returns is set by the gate that reads what it                           gate (APPS, §8). At N = 25, only single-round
buys.                                                                          differences well above the per-task variability are
                                                                               resolvable, and because that variability is between
 The three axes, priced in one currency. We                                    tasks, drawing more candidates per task does not
 price the axes in what the loop spends: verifier invo-                        reduce it; the APPS comparisons, at 150–470 prob-
 cations and generated tokens. Sharpening the gate                             lems, are not so constrained. We therefore report
 is free in that currency, since STRICT and PARTIAL                            Godot effects as rates with intervals, always with
 each cost one unit-test run, and STRICT- LAUNCH                               the evaluation budget at which each clean-launch
 and BUILD each cost one engine invocation; qua-                               rate was measured. Execution grounding is a lower
 drupling the harvest costs 4× the generation and                              bound on functionality, covering runtime survival
 4× the verification; going from 8B to 14B costs                               and observable state change rather than brief com-
 1.75× as much compute per token. The one cost                                 pliance, which we measure separately with a blind
 precision does carry is yield: at a fixed admitted                            judge.
 count a stricter gate needs 1/yield times the gener-
                                                                               Ethical Considerations
 ation, and STRICT- LAUNCH admits 73 of 888 can-
 didates where BUILD admits 887. That cost falls as                            This work uses public code- and game-generation
 the loop runs, since the generator’s own clean rate                           benchmarks (GameCraft-Bench, APPS) and pub-
 rises 4.6 → 9.8 → 17.5% across rounds at 8B (Ap-                              licly available models, involves no human-subjects
 pendix C). Within each domain the returns then run                            data, and relies on deterministic execution checks
 inversely to price. On APPS the free axis returns                             rather than human annotation. Compute is reported
 the +2.09pp above against the 4× axis’s +1.62pp.                              in Appendix C; the artifacts we will release use
 On Godot the free axis returns 5.0pp of one-round                             only resources whose licenses permit research use
 gain against 2.2pp for the 1.75× axis (§7, §9). In                            and redistribution.
References                                                 Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan
                                                             Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
Dario Amodei, Chris Olah, Jacob Steinhardt, Paul             Weizhu Chen. 2022. LoRA: Low-rank adaptation of
  Christiano, John Schulman, and Dan Mané. 2016.             large language models. In International Conference
  Concrete problems in AI safety. arXiv preprint             on Learning Representations (ICLR).
  arXiv:1606.06565.
                                                           Chaobo Jia, Ruipeng Wan, Ting Sun, Weihao Tan, Borui
Xin-Qiang Cai, Wei Wang, Feng Liu, Tongliang Liu,            Wan, Yuxuan Tong, Guangming Sheng, and Hong Xu.
  Gang Niu, and Masashi Sugiyama. 2025. Re-                  2026. GameGen-Verifier: Parallel keypoint-based
  inforcement learning with verifiable yet noisy re-         verification for LLM-generated games via runtime
  wards under imperfect verifiers. arXiv preprint            state injection. arXiv preprint arXiv:2605.07442.
  arXiv:2510.00915.
                                                           Yilei Jiang, Jinyuan Hu, Qianyin Xiao, Yaozhi Zheng,
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,            Ruize Ma, Kaituo Feng, Jiaming Han, Tianshuo Peng,
 Henrique Ponde de Oliveira Pinto, Jared Kaplan,             Kaixuan Fan, Manyuan Zhang, and Xiangyu Yue.
 Harri Edwards, Yuri Burda, Nicholas Joseph, et al.          2026. OpenGame: Open agentic coding for games.
 2021. Evaluating large language models trained on           arXiv preprint arXiv:2604.18394.
 code. arXiv preprint arXiv:2107.03374.
                                                           Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
Wayne Chi, Yixiong Fang, Arnav Yayavaram, Sid-              Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gon-
 dharth Yayavaram, Seth Karten, Qiuhong Anna                zalez, Hao Zhang, and Ion Stoica. 2023. Efficient
 Wei, Runkun Chen, Alexander Wang, Valerie                  memory management for large language model serv-
 Chen, Ameet Talwalkar, and Chris Donahue. 2026.            ing with PagedAttention. In Proceedings of the 29th
 GameDevBench: Evaluating agentic capabilities              Symposium on Operating Systems Principles (SOSP).
 through game development. In International Confer-
                                                           Tuomas Kynkäänniemi, Tero Karras, Samuli Laine,
 ence on Machine Learning (ICML).
                                                             Jaakko Lehtinen, and Timo Aila. 2019. Improved
                                                             precision and recall metric for assessing generative
Kazuki Egashira, Mark Vero, Jasper Dekoninck, Flo-
                                                             models. In Advances in Neural Information Process-
  rian E. Dorner, Robin Staab, and Martin T. Vechev.
                                                             ing Systems (NeurIPS).
  2026. Delay, plateau, or collapse: Evaluating the im-
  pact of systematic verification error on RLVR. arXiv     Juan Linietsky, Ariel Manzur, and Godot Engine
  preprint arXiv:2605.02909.                                 contributors. 2014. Godot engine. https://
                                                             godotengine.org.
Caglar Gulcehre, Tom Le Paine, Srivatsan Srini-
  vasan, Ksenia Konyushkova, Lotte Weerts, Abhishek        Jack Lu, Ryan Teehan, Jinran Jin, and Mengye Ren.
  Sharma, Aditya Siddhant, Alex Ahern, Miaosen                2025. When does verification pay off? a closer
  Wang, Chenjie Gu, Wolfgang Macherey, Arnaud                 look at LLMs as solution verifiers. arXiv preprint
  Doucet, Orhan Firat, and Nando de Freitas. 2023.            arXiv:2512.02304.
  Reinforced self-training (ReST) for language model-
  ing. arXiv preprint arXiv:2308.08998.                    Tongxu Luo, Rongsheng Wang, Jiaxi Bi, Chenming Xu,
                                                             Zhengyang Tang, Jianlong Chen, Juhao Liang, Ke Ji,
Srishti Gureja, Elena Tommasone, Jingyi He, Sara             Shuqi Guo, Yuhao Du, Fan Bu, Wenyu Du, Xiaotong
   Hooker, Matthias Gallé, and Marzieh Fadaee. 2025.         Zhang, Kyle Li, Shaobo Wang, Linfeng Zhang, Yux-
   Verification limits code LLM training. arXiv preprint     uan Liu, Xin Lai, Chenxin Li, and 6 others. 2026.
   arXiv:2509.20837.                                         GameCraft-Bench: Can agents build playable games
                                                             end-to-end in a real game engine? arXiv preprint
Lukas Helff, Quentin Delfosse, David Steinmann,              arXiv:2606.17861.
  Ruben Härle, Hikaru Shindo, Patrick Schramowski,
  Wolfgang Stammer, Kristian Kersting, and Felix           Anas Mahmoud, MohammadHossein Rezaei, Zihao
  Friedrich. 2026. LLMs gaming verifiers: RLVR               Wang, Anisha Gunjal, Bing Liu, and Yunzhong He.
  can lead to reward hacking.       arXiv preprint           2026. Reward hacking in rubric-based reinforcement
  arXiv:2604.15149.                                          learning. arXiv preprint arXiv:2605.12474.
                                                           Andreas Plesner, Francisco Guzmán, and Anish Atha-
Dan Hendrycks, Steven Basart, Saurav Kadavath, Man-
                                                             lye. 2026. An imperfect verifier is good enough:
  tas Mazeika, Akul Arora, Ethan Guo, Collin Burns,
                                                             Learning with noisy rewards.      arXiv preprint
  Samir Puranik, Horace He, Dawn Song, and Jacob
                                                             arXiv:2604.07666.
  Steinhardt. 2021. Measuring coding challenge com-
  petence with APPS. In Advances in Neural Infor-          Zhenting Qi, Susanna Maria Baby, Stefanie Anna Baby,
  mation Processing Systems (NeurIPS) Datasets and           Kan Yuan, Andrew Tomkins, Tu Vu, Da-Cheng Juan,
  Benchmarks Track.                                          and Cyrus Rashtchian. 2026. On the generaliza-
                                                             tion gap in self-evolving language model reasoning.
Arian Hosseini, Xingdi Yuan, Nikolay Malkin, Aaron           arXiv preprint arXiv:2606.01075.
  Courville, Alessandro Sordoni, and Rishabh Agar-
  wal. 2024. V-STaR: Training verifiers for self-taught    Qwen Team. 2025. Qwen3 technical report. arXiv
  reasoners. arXiv preprint arXiv:2402.06457.               preprint arXiv:2505.09388.
Ali Rad, Khashayar Filom, Darioush Keivan, Pey-                   (a)
                                                                                                                             13.6
  man Mohajerin Esfahani, and Ehsan Kamalinejad.




                                                             clean-launch (%)
  2026. Rate or fate? RLVε R: Reinforcement learn-                              15




                                                               per-candidate
                                                                                                    8.6            8.8
  ing with verifiable noisy rewards. arXiv preprint                             10
  arXiv:2601.04411.                                                                     5.6
                                                                                5
Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
  Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan                                0
  Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.                                          CTRL       BUILD-           SFT      RFT-r1
  Deepseekmath: Pushing the limits of mathematical                                   (gold-dup)    gated          (base)    (ours)
  reasoning in open language models. arXiv preprint               (b)
  arXiv:2402.03300.




                                                          with clean fuel
                                                                            100




                                                          training tasks
Avi Singh, John D. Co-Reyes, Rishabh Agarwal, et al.                                                                       n=186
                                                                                75
  2024. Beyond human data: Scaling self-training for                                                      n=123
                                                                                50
  problem-solving with language models. Transac-
                                                                                25       n=67
  tions on Machine Learning Research (TMLR).
                                                                                0
Yuda Song, Hanlin Zhang, Carson Eisenach, Sham M.                                         r1               r2               r3
  Kakade, Dean Foster, and Udaya Ghai. 2025. Mind                                                 fuel entering round
  the gap: Examining the self-improvement capabili-
  ties of large language models. In International Con-    Figure 3: (a) Same 67-sample budget; the dashed line is
  ference on Learning Representations (ICLR).             the supervised model’s rate. Neither control improves
                                                          on it: exact gold duplication regresses (p = 0.018)
Alex Stein, Furong Huang, and Tom Goldstein.
                                                          and the lenient BUILD filter merely matches it. Only
  2026. GATES: Self-distillation under privileged
                                                          STRICT- LAUNCH -filtered self-distillation gains (p <
  context with consensus gating. arXiv preprint
  arXiv:2602.20574.                                       10−4 against CTRL, p = 0.0012 against BUILD-gated).
                                                          (b) What the precise gate buys: the training tasks, of 111,
Igor Lima Strozzi. 2026. Teacher-free self-training       whose fuel contains a clean project, with each round’s
  amplifies but does not compound: A pass@k               fuel size beside its point. The exact-duplication control
  crossover on a free-verifier domain. arXiv preprint     re-covers the 48 that round 1’s fuel already reaches.
  arXiv:2606.07856.
Jianwen Sun, Chuanhao Li, Zizhen Li, Yukang Feng,
   Fanrui Zhang, Yifei Huang, Yu Dai, and Kaipeng         Wei Zhang, Jack Yang, Renshuai Tao, Lingzheng Chai,
   Zhang. 2026. JAMER: Project-level code framework         Shawn Guo, Jiajun Wu, Xiaoming Chen, Ganqu
   dataset and benchmark on professional game engines.      Cui, Ning Ding, Xander Xu, Hu Wei, and Bowen
   arXiv preprint arXiv:2606.19830.                         Zhou. 2025. V-GameGym: Visual game genera-
                                                            tion for code large language models. arXiv preprint
Kunvar Thaman. 2026. Reward hacking benchmark:              arXiv:2509.20136.
  Measuring exploits in LLM agents with tool use.
  arXiv preprint arXiv:2605.02964.                        Siyan Zhao, Zhihui Xie, Mengchen Liu, Jing Huang,
                                                            Guan Pang, Feiyu Chen, and Aditya Grover.
Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting             2026.      Self-distilled reasoner: On-policy self-
  Dong, Keming Lu, Chuanqi Tan, Chang Zhou, and             distillation for large language models. arXiv preprint
  Jingren Zhou. 2023. Scaling relationship on learning      arXiv:2601.18734.
  mathematical reasoning with large language models.
  arXiv preprint arXiv:2308.01825.                        Xiaosen Zheng, Tianyu Pang, Chao Du, Qian Liu, Jing
                                                            Jiang, and Min Lin. 2025. Cheating automatic LLM
Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai          benchmarks: Null models achieve high win rates. In
  Wang, Shiji Song, and Gao Huang. 2025. Does re-           International Conference on Learning Representa-
  inforcement learning really incentivize reasoning ca-     tions (ICLR).
  pacity in LLMs beyond the base model? In Advances
  in Neural Information Processing Systems (NeurIPS).     Ziqian Zhong, Aditi Raghunathan, Nicholas Carlini,
                                                            et al. 2025. ImpossibleBench: Measuring LLMs’
Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D.             propensity of exploiting test cases. arXiv preprint
  Goodman. 2022. STaR: Bootstrapping reasoning              arXiv:2510.20270.
  with reasoning. In Advances in Neural Information
  Processing Systems (NeurIPS), volume 35, pages
  15476–15488.                                            A                 Diagnosis: the visual judge is gameable
Ruixiang Zhang, Richard He Bai, Huangjie Zheng,           The probe uses an agentic game-builder (a separate
  Navdeep Jaitly, Ronan Collobert, and Yizhe Zhang.
  2026.    Embarrassingly simple self-distillation
                                                          setting from the from-scratch generator studied in
  improves code generation.         arXiv preprint        the main text) and shares the benchmark’s exact
  arXiv:2604.01193.                                       evaluation stack: the official Godot 4.6.2 runtime,
headless replay, and the official GPT-5.5 OVERALL        projects pass STRICT- LAUNCH (the 25/25 gold
visual judge (the same judge used on the public          ceiling), and the BUILD-passing outputs that fail it
leaderboard, so scores are directly comparable).         do so with concrete parse or load errors.

The agentic pipeline and the asset lever. The            Execution grounding (EXEC - GROUND). It in-
companion agent constructs a project through a se-       jects an instrumentation probe into a temporary
quence of build passes; the one that matters here is     copy of the project and steps the headless Scene-
a material-grounding pass that retrieves real CC0        Tree for up to 180 frames in passive, synthetic, and
sprite assets and substitutes them for the solid-color   demo-replay modes, replaying up to three recorded
placeholder rectangles the agent otherwise emits.        demo_outputs traces per task. The score is
Enabling the material-grounding pass raises the          1[runtime-error-free] · (0.35 sstate + 0.25 spassive +
judge’s art score with the game’s code held fixed:       0.40 sactive ), thresholded at 0.50 for the grounded
the art score comes out 1.8× what the same code          call. The state term reads script-exposed member
earns with its original placeholders. The lever is       variables (so single-node procedural games still reg-
presentation, not fit: randomly chosen sprites of        ister state); the passive term measures state change
comparable provenance raise it as much as the re-        with no input at all; the active term subtracts that
trieved ones. The manipulated outputs move un-           baseline so autonomous animation is not counted as
der a judge that is self-consistent on a fixed frame     interaction. On the calibration set (15 gold projects
(σ < 0.01). Across generation seeds, one model’s         across families; 15 STRICT- LAUNCH-broken candi-
OVERALL moves by 0.08–0.33.                              dates plus one hand-built empty shell), gold scores
                                                         a median of 0.75 (minimum 0.58) and every neg-
B   Verification signals in detail                       ative scores near zero (empty shell 0.013): the
                                                         threshold at 0.50 separates the two sets with no
Why the lenient rung is near-vacuous. The le-
                                                         overlap.
nient BUILD check (open the project headless and
quit, godot --headless --quit-after)                     The brief-compliance negative control. As the
does not treat parse, project, or scene-resource         negative reference for the brief-compliance mea-
errors as fatal: the process can still exit 0. On        surement of §6, we wrote a single brief-agnostic
the held-out families, supervised-model outputs          project: one Node2D that drifts, one that follows
that pass this check are nonetheless non-functional      the pointer, and a bank of ticking member variables.
in concrete, diagnosable ways: scripts that fail         We submitted it verbatim for all 25 held-out briefs.
to parse (undeclared identifiers, calls to nonex-        It launches cleanly, and the blind judge rates it 0/25
istent methods) and so never load; malformed             against gold’s 19/25. The shell generator will be
project.godot files (unquoted values, bare               released with the code.
input-map identifiers) that cause the engine to open
its project manager instead of the game; and broken      C    Training, generation, and data
.tscn external-resource references. The same
engine renders the corresponding gold projects           Separating precision from fuel quantity. The
without error. Empirically this failure is parse-        count-matched ladder varies precision by replacing
dominated: of the 888 candidates the supervised          admitted slots, so a lower-precision arm also holds
model generates on the training families, 815 fail       fewer true positives. A four-arm ladder at the same
STRICT- LAUNCH , and every one of those contains         944-row quota and the same eight training seeds,
a GDScript or project.godot parse error.                 retrained and re-evaluated end to end on a differ-
                                                         ent accelerator, separates them: CLEAN; FP 25 (the
STRICT- LAUNCH .     A candidate passes STRICT-          same persisted fuel as Fig. 5, 708 true positives and
LAUNCH     if godot --headless --path                    236 false ones); C 708 (those 708 alone, at 708 rows
PROJECT --quit-after 5 returns exit                      and so a quarter fewer optimizer steps); and C 708 R
code 0 and emits no parse, load, or resource-            (those same 708, with 236 of them duplicated back
resolution error on stderr (we match patterns            to 944 rows). Against CLEAN: C 708 R +0.40pp
such as Parse Error, Failed to load                      [−0.18, +1.03], C 708 −0.91pp [−1.86, +0.06],
script, unresolved identifiers or calls, and failed      and FP 25 −2.17pp [−3.02, −1.46] with all eight
ext_resource lookups). The gate separates                seeds negative, which reproduces the −1.58pp
working from broken projects: all held-out gold          [−2.23, −0.95] of the original run on overlapping
                                                         increasing cost ⟶


       admits 887/888                    admits 73/888                  readout, not a gate            used by the benchmark
                                                                                                           multimodal
          BUILD                      STRICT-LAUNCH                     EXEC-GROUND
                                                                                                           visual judge
       open headless,                    exit-0, no parse,                    steps the                     renders and
            quit                      load or resource error                 SceneTree                         scores
          lenient:                  deterministic, judge-free                 functional                      gameable
        near-vacuous                    no score to raise                    lower bound                  (1.8 × art score)
                                 we train against this rung


                                                    increasing certification ⟶

Figure 4: The verification ladder, ordered by how much each signal certifies. BUILD is near-vacuous (it admits
887 of the supervised model’s 888 training-family candidates, of which only 73 also pass STRICT- LAUNCH);
STRICT- LAUNCH , our training gate, requires a clean headless launch (exit code 0, no parse/load/resource error),
deterministic and judge-free; execution grounding drives the running SceneTree and serves as a readout rather than
a gate; the top rung, a multimodal visual judge, certifies the most but is gameable.

                                            realized 1 − π / FNR
                                               0.250 / 0.000
                                                                     Algorithm 1: One round of launch-gated
FP25
                                                                     self-distillation.
FN25                                           0.000 / 0.252
                                                                      input :model Mt ; training-family briefs B;
FN50                                           0.000 / 0.499                     gold pool Dt ; harvest budget Kh :
FN75                                           0.000 / 0.748                     samples per brief
                                                                      for each brief b ∈ B do
MIX                                            0.125 / 0.128
                                                                           sample Kh candidate projects
          −2            −1      0           +1                              {c1 , . . . , cKh } ∼ Mt (· | b) ;
               held-out pass@1 vs. CLEAN (pp)                              for each candidate c with at least three
                                                                            files do
Figure 5: Only one direction of verifier error is
                                                                                materialize c to a project tree ;
paid for. Held-out pass@1 relative to the CLEAN
arm on APPS, in percentage points, with 95% crossed                             if STRICT- LAUNCH(c) then mark c
seed×task bootstrap intervals, at a common count-                                 as clean;
matched quota over eight training seeds. Realized, not                     keep up to two deduplicated clean
nominal: 1−π is the non-all-pass share of the admit-                        candidates for b ;
ted rows (the axis of Fig. 1); the FNR is masked true
positives over those available. FN arms mask true posi-
                                                                      Ft ← all kept clean candidates (the round’s
tives, FP 25 injects false ones, MIX splits the error budget            fuel) ;
evenly.                                                               Dt+1 ← Dt ∪ Ft ;
                                                                      Mt+1 ← FINE - TUNE(base, Dt+1 ) ;
                                                                      output :Mt+1 , Ft
intervals. Both paths land on that penalty: the
remaining step to FP 25 costs 1.27pp from C 708                    Table 2: STRICT- LAUNCH fuel rate per candidate, under
and 2.57pp from C 708 R. C 708 is handicapped                      a matched training recipe (8 epochs), measured on the
on updates and still ahead of FP 25; C 708 R cannot                canonical 111 training tasks (888 candidates per base).
reproduce the per-problem slot histogram exactly,
since a replaced slot on a problem with no surviv-                   Base                 STRICT- LAUNCH rate   Wilson 95% CI
ing sibling has nothing same-problem to duplicate.                   Qwen3-4B                         2.14%     [1.37, 3.32]
                                                                     Llama-3.1-8B                     2.93%     [2.01, 4.26]
GRPO arms of the error-direction ladder.                             Qwen3-8B                         4.62%     [3.42, 6.20]
Each run trains Qwen3-4B with LoRA for 300                           Qwen3-14B                        8.22%     [6.59, 10.21]
                                                                     Gemma-3-12B                      9.57%     [7.81, 11.69]
optimizer steps at group size G = 8 on 50 prob-
lems whose pass rate under the current policy lies
in [0.25, 0.75]. The two corrupted arms realize er-                Fuel expansion at 8B. The generator’s own yield
ror rates of 24.97% and 24.98%, giving Youden                      of STRICT- LAUNCH-clean candidates on the train-
indices of 0.7503 and 0.7502.                                      ing families covers 31 → 51 → 75 of the 111 tasks.
                                       (a) execution grounding                                                                (b) brief compliance




                                                                                                  (per 100 candidates)
                               25                                                                                        15




                                                                                                    brief-compliant
  grounded tasks



                               20
      (of 25)



                               15                                                                                        10
                               10
                                                                                                                         5
                                   5
                                   0                                                                                     0
                                        SFT             r1            r2                    r3                                    SFT        r1             r2       r3
                                                     self-distillation round                                                              self-distillation round

    Figure 6: Two readouts the gate never optimizes. (a) Execution grounding: tasks with at least one grounded
    (≥ 0.50) clean candidate, 10 → 12 → 14 → 15 of the same 25 held-out tasks; the score is validated by 15/15
    grounded gold against 0/16 known-bad projects. (b) Brief compliance under a blind judge that reads only the brief
    and the shipped GDScript: projects per 100 candidates that both launch and implement their brief.


                                                                                                                          50
coverage@K (% of 25 tasks)




                             100



                                                                                                      clean-launch (%)
                                                                                                                          40
                             75                                                                         per-candidate
                                                                                                                          30

                             50                                                                                           20

                                                                                    RFT-r3                                10
                             25                                                     RFT-r2
                                                                                    RFT-r1                                    0
                                                                                    SFT                                           SFT        r1             r2       r3
                              0                                                                                                            self-distillation round
                                   1          2         4         8            16            32
                                        sampling budget K (candidates per task)                        Figure 8: Three rounds compound. The per-candidate
                                                                                                       clean-launch rate on the four held-out families climbs
    Figure 7: The supervised model never closes the cov-
                                                                                                       8.8 → 13.6 → 30.9 → 42.2% with Wilson intervals.
    erage gap within the sampled budget.Coverage@K
                                                                                                       Task-level coverage is not co-plotted; at the full 32-
    under the unbiased estimator 1 − n−c       n
                                                 
                                         K / K , pooling                                               candidate budget it runs 84 → 88 → 100 → 100%, satu-
    four decoding seeds into n = 32 candidates per task, c
                                                                                                       rating at round 2. This series is the single-run trajectory
    of them clean, averaged over the 25 held-out tasks. The
                                                                                                       the matched controls are compared against; the three-
    supervised model is still 16.0pp short of full coverage
                                                                                                       seed means are in Table 1.
    at K = 32; round 3 has been above 97% since K = 8.


    Table 3: Training-signal diagnostics for the GRPO                                                  67 fuel projects, then 123 from M1 and 186 from
    arms over the same eight training seeds as Fig. 5, as                                              M2 ; these cover 48, 77, and 101 of the 111 training
    mean ± s.d. over those seeds; “clean reward” scores the                                            tasks across the three rounds, reaching all 10 train-
    policy’s own rollouts with the uncorrupted verifier.                                               ing families by round 2. Code, the harvested fuel,
                                                                                                       and one adapter per reported arm will be released
                                                   CLEAN          FP 25             FN 25
                                                                                                       upon publication.
    degenerate groups                             0.488±.023   0.367±.062      0.141±.037
    gradient norm                                 0.293±.027   0.318±.034      0.405±.057              Training. On Qwen3-14B we train for 8 epochs;
    clean reward                                  0.696±.036   0.629±.049      0.608±.028
                                                                                                       hyper-parameters follow. All training and inference
                                                                                                       ran on a single 96 GB GPU; a full three-round loop
                                                                                                       (generation, filtering, and retraining) took on the
    Data and split. The family partition is given                                                      order of tens of GPU-hours.
    in §3. We verified zero held-out leakage into
    any round’s fuel: every harvested brief carries a                                                  Generation. vLLM 0.11.2 serves the LoRA
    training-family label and matches no held-out brief.                                               adapter unmerged at bfloat16. We draw
    Per round, the harvest keeps, among candidates                                                     Kh = 8 candidates for each training-family brief.
    with at least three files, the STRICT- LAUNCH-clean                                                Prompts are rendered with each base model’s own
    ones, deduplicated, capped at two per task: of M0 ’s                                               chat template (apply_chat_template,
    73 STRICT- LAUNCH-clean candidates this yields                                                     add_generation_prompt=True,
enable_thinking=False), so each base is                   Table 4: Per-family coverage@16 at a single two-
queried in its native format. Decoding on Godot           decoding-seed budget, in task counts. Round 3
                                                          reaches full coverage in every family, while the exact-
uses Qwen3 non-thinking sampling: temperature
                                                          duplication control (CTRL) regresses in three of the four
0.7, top-p 0.8, top-k 20, repetition penalty 1.05,        families.
and a 24,576-token generation cap. The cap is set
above the longest gold reference (19,192 tokens).         family          SFT           r1         r2          r3      CTRL

                                                          horror          5/5           5/5        5/5      5/5        4/5
                                                          puzzle          5/8           5/8        7/8      8/8        2/8
                                                          rhythm          2/5           4/5        4/5      5/5        4/5
LoRA and optimization. Adapters use r =                   shooter         6/7           5/7        6/7      7/7        3/7
16, α = 32, dropout 0.05, no bias, task
type CAUSAL - LM. Target modules are resolved             Table 5: Evaluation protocol per configuration. Draws
from named_modules at run time, matching                  pool all decoding seeds (8 candidates per task per seed;
the {q,k,v,o,gate,up,down}_proj pro-                      APPS rows are labeled by held-out size). Table 4 instead
jections; if a base carries a vision tower, its projec-   uses one fixed seed pair, in task counts.
tions are excluded and only language-model pro-
                                                          configuration         seeds    draws      coverage
jections are adapted. Optimization is AdamW with
                                                          Godot 14B              4         800      coverage@32, unbiased
a cosine schedule and a 3% warmup ratio, learning         Godot 8B               5        1000      coverage@32, unbiased
rate 10−4 , batch size 1 with gradient accumulation       Godot 4B               6        1200      coverage@48, unbiased
8, sequence length 24,576, and scaled dot-product         APPS 4B /150           3        3600      coverage@8, task counts
                                                          APPS 4B /470           3       11280      coverage@8, task counts
attention, all in bfloat16. The prompt is masked
out of the loss (labels set to −100 over the prompt       Fig. 7 (14B)           4           800    unbiased, K ≤ 32
span). On APPS we reuse the same settings at
the smaller scale: r = 16, α = 32, learning rate          Table 6: APPS-introductory, Qwen3-4B. From a lightly
10−4 , sequence length 1536; held-out generation          supervised M0 (20.4%), only the STRICT (all-tests-pass)
                                                          gate produces decisive transfer; the count-matched PAR -
uses temperature 0.8 and top-p 0.95.
                                                          TIAL (≥ 50% but not all tests) control moves the rate
                                                          less; LENIENT (syntax-valid only) leaves pass@1 un-
                                                          touched while cutting coverage@8. Paired bootstrap
                                                          over 470 held-out problems, eight training seeds; rates
Evaluation and statistics. The 14B arms are
                                                          in %, ∆ in percentage points, p for the comparison with
evaluated with 8 candidates per held-out task across      M0 . ∗ p < 0.05, ∗∗ p < 0.01.
four decoding seeds (800 candidates per model,
pooled to K = 32 for coverage); the 8B and 4B             Fuel gate         pass@1             ∆        coverage@8     ∆
replications use five and six decoding seeds, re-         M0 (gold SFT)         20.4           —          41.5         —
spectively. The primary metric is the per-candidate       STRICT                25.5         +5.15∗∗      44.8       +3.32∗∗
clean-launch rate; comparisons between models are         PARTIAL               22.5         +2.11∗∗      41.0        −0.46
                                                          LENIENT               20.3          −0.10       38.3       −3.16∗∗
paired by task and tested with a cluster-permutation
test that permutes candidate labels within each task
(N = 25 tasks, 50,000 draws), with task-level boot-       D    Efficiency, not reach: what a zero at
strap confidence intervals on effect sizes (50,000 re-         K = 32 means
samples). The APPS ladders instead use a crossed
seed×task bootstrap: training seeds and held-out          Four of the 25 held-out tasks produced no clean
problems are resampled independently with re-             project anywhere in the supervised model’s full 32-
placement and the effect is recomputed over the           candidate pool, while the distilled model (RFT-r3)
crossed resamples (10,000 draws), with percentile         produced one on all four. We drew 512 fresh can-
intervals. Because candidates drawn for the same          didates per task from the same frozen supervised
task are strongly correlated (intraclass correlation      adapter, under the same gate and decoding config-
0.63), every comparison clusters on the task rather       uration. All four yielded clean projects: 15, 23,
than on the candidate. Wilson intervals are reported      3, and 5 successes out of 512, against 17, 25, 6,
per arm as a description of its candidate pool and        and 8 out of 32 for the distilled model. To reach,
are not used for between-arm inference. Table 5           with m supervised draws, the chance that a sin-
lists the evaluation budget and coverage estimator        gle distilled draw is clean (1 − (1 − q)m = qRFT ,
for every configuration.                                  where q and qRFT are the per-draw clean rates of the
supervised and distilled models), the supervised
model needs 25–35 draws, so under a multi-file
executable gate the separation is one of sampling
efficiency, placing this setting in the regime Yue
et al. (2025) report for RLVR in the language do-
main. The reading survives a larger budget: at 8B,
one launch-gated round covers 19/25 at K = 40,
against 14/25 for the supervised model and 15/25
for one BUILD-gated round.
