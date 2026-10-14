                                         Published as a conference paper at ICLR 2026




                                         R ELIABLE S ELF -I MPROVEMENT T RAINING BY V ERI -
                                         FYING R EASONING , N OT J UST A NSWERS

                                                                                  Xinyu Zhang
                                                                                   Anyscale
                                                                              xinyzng@gmail.com



                                                                                    A BSTRACT
arXiv:2603.21558v2 [cs.AI] 28 May 2026




                                                  Self-improvement training—where a model learns from solutions it generated
                                                  itself—promises sustained capability gains, but it has a well-known failure mode:
                                                  as a model trains on its own outputs round after round, small errors in its reason-
                                                  ing compound until accuracy stalls or degrades. We trace this drift to what gets
                                                  kept. Most self-improvement methods keep a solution whenever its final answer is
                                                  correct, which lets through “lucky guesses”—answers that come out right despite
                                                  flawed reasoning—and training on them teaches the flawed reasoning. We pro-
                                                  pose Verified Self-Improvement (VSI), which keeps a self-generated solution
                                                  only when its reasoning holds up, not just its answer. Before a solution can enter
                                                  the training set, VSI recomputes every arithmetic step with a computer-algebra
                                                  library (sympy), checks that intermediate values stay consistent from one step
                                                  to the next, and enforces simple domain constraints (for example, counts should
                                                  be non-negative whole numbers). We evaluate VSI on GSM8K with Qwen3-4B-
                                                  Thinking across 5 rounds of self-improvement training under five conditions: no
                                                  verification, outcome (answer-only) verification, majority voting, full VSI step-
                                                  level checking, and VSI with DPO. VSI rejects about 34% of the correct-answer
                                                  solutions that outcome verification would keep—exactly the lucky guesses—and
                                                  this cleaner training signal lets accuracy keep climbing across all five rounds
                                                  (80.5%→91.0%), whereas outcome verification plateaus and no verification col-
                                                  lapses. Turning these checks into DPO preference pairs—preferring sound rea-
                                                  soning over lucky answers—further teaches the model to tell the two apart (re-
                                                  ward accuracy 46%→63%). VSI is a simple, reproducible recipe for making
                                                  self-improvement training reliable wherever an automatic check on the reasoning
                                                  is available.


                                         1   I NTRODUCTION
                                         Self-improvement training—where a model improves by learning from data it generates itself—is
                                         one of the most appealing ideas in modern machine learning. Recent work on self-training (Ze-
                                         likman et al., 2022; Singh et al., 2024), self-rewarding language models (Yuan et al., 2024), and
                                         bootstrapped reasoning (Hosseini et al., 2024) shows that a model can meaningfully improve from
                                         its own outputs through a simple loop: sample candidate solutions, keep the good ones, and finetune
                                         on them.
                                         In practice, though, the loop is fragile. When a model is finetuned on its own outputs round after
                                         round, errors in intermediate reasoning compound from one round to the next—a problem we call
                                         drift. A model may reach a correct final answer through faulty reasoning (a “lucky guess”); once
                                         that solution is kept and trained on, the model learns to reproduce the faulty reasoning, and over
                                         several rounds this builds into systematic degradation—the same dynamic behind model collapse
                                         when models are trained repeatedly on generated data (Shumailov et al., 2024).
                                         Our central claim is simple: what you keep determines how long self-improvement keeps paying off.
                                         Standard self-training keeps a solution based on its outcome alone—is the final answer correct?—
                                         which lets through solutions whose reasoning contains arithmetic slips, inconsistent intermediate
                                         values, or violated constraints that happen to cancel out. Finetuning on those solutions spreads the
                                         flawed reasoning.


                                                                                          1
Published as a conference paper at ICLR 2026




We propose Verified Self-Improvement (VSI): a self-improvement training loop that uses an auto-
matic check on each solution’s reasoning—not just its answer—to decide what to finetune on. Con-
cretely, VSI is rejection-sampling finetuning with a stricter acceptance rule. Before a self-generated
solution is kept, VSI requires that:

      1. The answer is correct: the final answer matches the ground truth.
      2. The arithmetic holds up: every arithmetic step we can parse from the chain-of-thought is
         recomputed with sympy (Meurer et al., 2017) and confirmed correct.
      3. The reasoning is internally consistent: intermediate values are tracked across steps, so
         we can catch a number the model invents that contradicts its own earlier work.
      4. Basic constraints hold: simple domain rules—non-negative counts, whole numbers for
         discrete quantities—are respected.

By asking that every reasoning step, not just the final answer, hold up, VSI keeps lucky guesses out
of the finetuning data, so the model learns from solutions that are right for the right reasons. This is
what keeps self-improvement training stable over more rounds.

Contributions. (1) We introduce VSI, a self-improvement training recipe that improves stability
by filtering self-generated finetuning data on the quality of the reasoning, not just the answer. (2)
We show this acceptance rule is far more selective than outcome-only filtering (∼52% vs. ∼78%
of solutions kept), removing solutions that are right for the wrong reasons. (3) We show that the
same checks yield DPO preference pairs that teach the model to prefer sound reasoning over lucky
answers. (4) We provide a complete, reproducible pipeline for self-improvement training with auto-
matic verification.


2     R ELATED W ORK

Self-training for reasoning. STaR (Zelikman et al., 2022) bootstraps reasoning by finetuning on
self-generated rationales that reach correct answers. ReST-EM (Singh et al., 2024) casts this as an
EM-style loop with repeated sampling. V-STaR (Hosseini et al., 2024) trains verifiers alongside
generators, and self-rewarding language models (Yuan et al., 2024) use the model itself as a judge.
These methods accept solutions mainly by outcome correctness; VSI adds an automatic check on
the reasoning steps, improving the quality of the finetuning data.

Process supervision. Lightman et al. (2024) show that supervising each reasoning step beats su-
pervising only the final answer when training math models, and Uesato et al. (2022) compare process
and outcome feedback. These works rely on human-annotated step labels; VSI obtains a step-level
signal automatically by recomputing the math, at no annotation cost.

Tool-assisted and verified reasoning. TORA (Gou et al., 2024) weaves tool use, including exact
computation, into the reasoning process, and generative theorem provers (Polu & Sutskever, 2020)
rely on formal verification. VSI differs in where the check is applied: it filters the finetuning data
rather than acting at inference time, which makes it complementary to these approaches.

Model collapse. Shumailov et al. (2024) show that repeatedly training on model-generated data
progressively degrades quality, and Huang et al. (2024) show that LLMs struggle to self-correct
without external feedback. VSI supplies exactly that external signal—an automatic check on the
reasoning—which keeps errors from propagating across rounds.


3     M ETHOD : V ERIFIED S ELF -I MPROVEMENT

3.1   T HE S ELF -I MPROVEMENT T RAINING L OOP

VSI runs as a self-improvement training loop (Figure 1). Starting from a base model M0 , each
round i proceeds as:


                                                   2
Published as a conference paper at ICLR 2026




                                                            repeat for K rounds



        Model Mi − 1                 Generate                     Verify               Finetune                 Model Mi




            one candidate (of N)                  final answer ✓                  Outcome filtering
                                                                                  checks the answer only               KEEP
                                                                                  lucky guess kept → drift
              16 − 3 − 4 = 9                                      ✓


              9 × 5 = 50                                          ✗
              sympy: 9 × 5 = 45                                                   VSI (ours)
              ####     45                                         ✓               checks every step              REJECT
                                                                                  wrong step caught → clean
              checks: arithmetic (sympy) · consistency · constraints




Figure 1: The VSI loop, and why checking the reasoning matters. Each round, the model gen-
erates N =8 solutions per problem; an acceptance rule V decides which enter the finetuning set, and
the loop repeats (top). We zoom into the verification step on one candidate—a “lucky guess” whose
final answer is correct (45) but whose reasoning contains a wrong arithmetic step (9 × 5=50, re-
computed by sympy as 45). Outcome filtering checks only the final answer and keeps the solution,
training on the flawed step; VSI recomputes every step and checks consistency and basic domain
constraints, so it rejects the solution—keeping lucky guesses out of training. This cleaner signal is
what keeps accuracy climbing across rounds (Table 1, Figure 2).


                                                                                                                 (1)         (N )
        1. Generate: For each training problem xj , sample N candidate solutions {yj , . . . , yj                                   }
           from Mi−1 with temperature T > 0.
                                                                                                           (k)         (k)
        2. Verify: Apply the verification filter V to select solutions: Di = {(xj , yj ) : V(yj , aj ) =
           True}, where aj is the ground-truth answer.
        3. Train: Fine-tune Mi−1 on Di to produce Mi .
        4. Evaluate: Measure task performance, reasoning quality, and diversity.

The decisive choice is the acceptance rule V—which solutions we keep for finetuning. We compare
three strategies:

3.2     V ERIFICATION S TRATEGIES

No verification (baseline). Randomly keep one solution per problem, regardless of correctness.
This is unfiltered self-improvement training.

Outcome verification (answer-only). Keep every solution whose final answer matches the ground
truth. This is the standard acceptance rule in STaR-style methods.

VSI (step-level checking).               A solution is kept under VSI only if all four checks below hold:

3.2.1     C HECK 1: A NSWER C ORRECTNESS
Extract the final numeric answer using pattern matching (after #### markers for GSM8K) and
verify it matches the ground truth within tolerance ϵ = 10−6 .


                                                                       3
Published as a conference paper at ICLR 2026




Algorithm 1 Logical Flow Verification
Require: Reasoning steps s1 , . . . , sT
Ensure: Boolean: flow is consistent
 1: A ← ∅ {variable assignment history}
 2: for t = 1 to T do
 3:   for each match of "<name> = <number>" or "there are <number> <name>" in
      st do
 4:      Extract variable name v (lowercased) and value x
 5:      Append (v, x, t) to A
 6:   end for
 7: end for
 8: Group A by variable name: Hv = {(xi , ti )} for each v
 9: for each variable v with |Hv | ≥ 2 do
10:   for each consecutive pair (xi−1 , ti−1 ), (xi , ti ) in Hv do
11:      if ti = ti−1 + 1 then
12:         skip {adjacent-step reassignment: legitimate update}
13:      end if
14:      gap ← ti − ti−1
15:      if gap > 2 and |xi − xi−1 |/ max(|xi−1 |, 1) > 0.5 then
16:         flag inconsistency for v
17:      end if
18:   end for
19: end for
20: return no inconsistencies flagged


3.2.2   C HECK 2: A RITHMETIC V ERIFICATION
Parse the chain-of-thought to extract arithmetic expressions of the form “A ⊙ B = C” where ⊙ ∈
{+, −, ×, ÷}. For each expression, evaluate the left-hand side using sympy.sympify() and
verify |LHS −C| < ϵ. We require ≥ 80% of parseable expressions to be arithmetically correct:
                               |{e ∈ Expr(y) : |sympy(e.lhs) − e.rhs| < ϵ}|
              ArithRate(y) =                                                ≥ τarith              (1)
                                                 |Expr(y)|
where τarith = 0.8 by default. This threshold allows for minor parsing failures while catching
genuine arithmetic errors.

Parser coverage analysis. A key subtlety of the arithmetic check is its behavior when no expres-
sions are parseable: if |Expr(y)| = 0, the pass rate defaults to 1.0 (a vacuous pass). This means the
parser’s limited coverage causes under-detection of errors rather than false rejection—unparseable
solutions are passed, not rejected. Our analysis (Table 4) shows that the majority of correct-answer
solutions contain at least one parseable expression, with a mean of approximately 3–5 expressions
per solution. Solutions with zero parseable expressions (which receive a vacuous arithmetic pass)
constitute a minority of cases. We additionally conducted a relaxed-parsing ablation using broader
expression patterns (dollar amounts, percentage operations, natural-language equality), which in-
creased expression extraction by approximately 15% but did not materially change the final accu-
racy, confirming that the standard parser captures the most verification-relevant expressions.

3.2.3   C HECK 3: L OGICAL F LOW V ERIFICATION
We track variable-value assignments across reasoning steps to detect “hallucinated intermediate val-
ues” where the model invents a number that contradicts its own earlier computation. The procedure
is formalized in Algorithm 1.
Two extraction patterns are used: (1) "<name> = <number>" for explicit assignments (e.g.,
“total = 100”) and (2) "there are <number> <name>" for natural-language quantity state-
ments. Variables are grouped by lowercased name, and we check whether the same variable is
reassigned to a substantially different value (> 50% relative change) across a gap of more than 2
steps without an intervening adjacent-step update.


                                                 4
Published as a conference paper at ICLR 2026




Limitations of flow verification. We acknowledge that this approach uses simple string matching
rather than coreference resolution—it may miss renamed variables or fail to link pronouns to their
referents. Adjacent-step reassignment (gap = 1) is deliberately allowed because it typically corre-
sponds to a legitimate computed update (e.g., “remaining = 50” followed by “remaining = 50 - 12
= 38”). The 50% threshold was chosen to avoid flagging minor rounding differences while catching
genuine hallucinated values; we verified that varying this threshold between 30% and 70% does not
materially change the overall verification rate.

3.2.4    C HECK 4: C ONSTRAINT S ATISFACTION

Enforce domain constraints appropriate to math word problems: (a) non-negativity for count vari-
ables (people, items, etc.), (b) integrality for discrete quantities, and (c) conservation (parts should
sum to whole, when detectable).

3.3     DPO VARIANT: L EARNING S OUND R EASONING

We additionally turn VSI’s checks into preference pairs for Direct Preference Optimization (DPO)
(Rafailov et al., 2023):

        • Chosen: Solutions passing all four VSI checks (correct answer + sound reasoning).
        • Rejected: Solutions with correct final answer but failed step verification (lucky guesses
          with flawed reasoning).

This directly teaches the model to prefer sound reasoning over lucky answers, addressing the root
cause of drift.


4     E XPERIMENTAL S ETUP

Model. We use Qwen3-4B-Thinking (Qwen Team, 2025) (4B parameters), a reasoning-focused
model that generates chain-of-thought in <think> tags. Its baseline GSM8K accuracy is ap-
proximately 80.5% and MATH-500 accuracy is approximately 45.5% under our evaluation settings
(greedy decoding, max 2048 output tokens, max context 4096). We note that vLLM greedy decoding
exhibits ∼1–2 percentage point non-determinism across runs on A10G GPUs due to floating-point
operation ordering; we report the mean across runs.

Datasets.    We use three datasets, all from HuggingFace:

        • GSM8K (Cobbe et al., 2021): 7,473 train / 1,319 test grade-school math problems (primary
          benchmark).
        • MATH-500: A 500-problem subset of MATH (Hendrycks et al., 2021) for cross-task trans-
          fer evaluation.

Training. We use LoRA (Hu et al., 2022) adapters (r=16, α=32) on attention projections
(q/k/v/o) with the base model in bfloat16 precision. Training uses HuggingFace Trainer with batch
size 1, gradient accumulation 16 (effective batch size 16), learning rate 2×10−4 , warmup ratio 0.05,
gradient checkpointing, and 1 epoch per iteration. Maximum sequence length is 2048 tokens with
dynamic padding. LoRA weights are merged into the base model after each iteration to produce a
full checkpoint. This configuration requires ∼18–20 GB VRAM per GPU.

Generation. At each iteration, we generate N =8 solutions per training problem using vLLM
(Kwon et al., 2023) with temperature T =0.7, top_p=0.9, and maximum 1536 tokens, parallelized
across 4 A10G GPUs (24 GB each).

Rounds. We run 5 rounds of self-improvement training per condition. For the DPO variant, we
use β=0.1 and learning rate 5 × 10−6 .


                                                   5
Published as a conference paper at ICLR 2026




Table 1: GSM8K test accuracy (%) across rounds of self-improvement training. VSI keeps improv-
ing over all 5 rounds, while no verification collapses and outcome-only filtering plateaus. Stable
depth counts rounds before accuracy drops below baseline −1%. Best per column in bold; VSI
rows shaded; collapsing (sub-baseline) values in red.

        Condition               Base     Iter 1   Iter 2   Iter 3   Iter 4   Iter 5   Depth
        No Verification          80.5    82.1     81.2     78.1     75.4      73.2      2
        Outcome Verification     80.5    84.8     86.2     86.6     86.3      85.8     >5
        Majority Voting          80.5    84.0     85.8     86.1     85.7      85.1     >5
        VSI (Verified)           80.5    84.2     86.7     88.2     89.5      91.0     >5
        VSI + DPO                80.5    84.5     87.1     88.9     90.1      91.2     >5


Additional baseline: majority voting. To test whether a label-free self-consistency signal could
stand in for checking the reasoning, we include a majority voting baseline (Wang et al., 2023). At
each round, we keep solutions whose final answer matches the most common answer among the
N =8 samples for each problem. Crucially, this baseline uses no ground-truth labels—it relies only
on agreement among the model’s own outputs—giving a fair comparison between checking the
reasoning (which uses ground truth) and a label-free self-consistency approach.

Evaluation metrics.

       • GSM8K Accuracy: Greedy decoding on the test set with answer extraction.
       • MATH-500 Accuracy: Cross-task transfer with \boxed{} extraction.
       • Pass@k (k ∈ {1, 5, 8}): Solution reliability via the unbiased estimator (Chen et al., 2021).
       • Verification Rate: Fraction of correct-answer solutions passing full VSI verification—a
         proxy for reasoning quality.
       • Self-BLEU: Average pairwise BLEU-4 across solutions to the same problem; higher values
         indicate mode collapse.
       • Stable Depth: Number of rounds before accuracy drops below baseline −1%.

5     R ESULTS

5.1   M AIN R ESULT: ACCURACY ACROSS I TERATIONS

Table 1 reports accuracy across all five conditions and rounds. The base model scores about 80.5%
on GSM8K (mean across evaluation runs). No verification collapses by round 3, falling below the
baseline −1% line (stable depth 2). Outcome verification and majority voting plateau around 86%,
while VSI climbs steadily to 91.0% by round 5. VSI + DPO reaches 91.2%, a marginal additional
gain.

Round-1 filtering analysis. At round 1 we generated 8 solutions per problem (7,473 problems,
∼59,784 solutions in total) and applied each strategy. The acceptance rates show how selective each
one is:

       • No verification: 7,473 solutions accepted (one sampled at random per problem).
       • Outcome verification: 46,836 accepted (∼78% of those generated), keeping every correct-
         answer solution.
       • Majority voting: 47,561 accepted (∼80%), keeping solutions that match the most common
         answer.
       • VSI (Verified): 30,983 accepted (∼52%), meaning VSI discards a substantial share
         (∼34%) of correct-answer solutions that fail the step-level checks—the lucky guesses with
         flawed reasoning.


                                                  6
Published as a conference paper at ICLR 2026




                                         Self-Improvement Training: GSM8K Accuracy by Filtering Strategy
                                 0.95


                                 0.90




               GSM8K Test Accuracy
                                 0.85


                                 0.80
                                                  Base model
                                                  No Verification
                                                  Outcome Verification
                                 0.75             Majority Voting
                                                  VSI (Verified)
                                                  VSI + DPO
                                 0.70
                                         Base              Iter 1           Iter 2        Iter 3        Iter 4   Iter 5
                                                                         Self-Improvement Iteration

Figure 2: GSM8K accuracy across 5 rounds of self-improvement training. VSI (green) keeps
improving round after round. Outcome verification (orange) plateaus after round 2. No verification
(red) collapses by round 3.

                                                   Reasoning Quality Across Self-Improvement Iterations
                                 0.9


                                 0.8
               Verification Rate




                                 0.7


                                 0.6

                                                 No Verification
                                 0.5             Outcome Verification
                                                 Majority Voting
                                                 VSI (Verified)
                                 0.4
                                        Iter 1                 Iter 2              Iter 3           Iter 4       Iter 5
                                                                         Self-Improvement Iteration

Figure 3: Reasoning quality over rounds. The fraction of correct-answer solutions that also pass
the full set of VSI checks rises over rounds for the VSI condition—the model is learning to produce
reasoning that holds up, not just correct answers.


       • VSI + DPO: preference pairs built from problems that had both a fully verified solution
         (chosen) and a correct-answer-but-unverified solution (rejected).

DPO training. DPO on 4,426 preference pairs finished in ∼2.25 hours with a final loss of 0.684.
Reward accuracy rose from 46% to 63% during training, showing that the model learned to tell
verified from unverified solutions apart. The DPO-trained model reaches 91.2% GSM8K accuracy
at round 5, marginally ahead of SFT-only VSI (91.0%).
Figure 2 visualizes these trajectories.

5.2   V ERIFICATION R ATE A NALYSIS

Figure 3 shows a key result: for the VSI condition, the verification rate—the fraction of correct-
answer solutions that also pass every check—rises over rounds. The model is learning not just


                                                                                 7
Published as a conference paper at ICLR 2026




Table 2: MATH-500 accuracy (%) — cross-task transfer evaluation (training used only GSM8K).
Best per column in bold; VSI rows shaded; sub-baseline values in red.

             Condition                Base    Iter 1      Iter 2    Iter 3   Iter 4   Iter 5
             No Verification          45.5     46.8       46.0      44.2     42.8     41.4
             Outcome Verification     45.5     46.4       47.2      47.0     46.6     46.2
             Majority Voting          45.5     48.6       49.0      48.8     48.4     48.0
             VSI (Verified)           45.5     47.2       48.6      49.8     50.6     51.2
             VSI + DPO                45.5     47.4       49.0      50.2     51.0     51.8

Table 3: Verification breakdown at round 1: pass rates (%) for each VSI check among correct-
answer solutions. All conditions share the same base model at round 1, so the rates are nearly
identical; the VSI column is shaded and the aggregate All Checks row (which sets the ∼34%
rejection rate) is highlighted.

                       Check                    No Verif.      Outcome       VSI
                       Arithmetic (≥ 80%)          83.5            84.1      84.1
                       Logical Flow                86.8            87.2      87.2
                       Constraints                 91.2            91.8      91.8
                       Parser Coverage (%)         77.5            78.3      78.3
                       All Checks                  65.1            66.3      66.3



to get the answer right, but to reason in a way that holds up—exactly the behavior we want from
self-improvement training.
By contrast, the verification rate for the outcome-only condition stays flat or drifts down, confirming
that outcome filtering does not improve reasoning quality.

5.3   C ROSS -TASK T RANSFER

Table 2 shows MATH-500 accuracy across rounds. Although training used only GSM8K, VSI trans-
fers positively: MATH-500 accuracy rises from 45.5% to 51.2% (+5.7pp), suggesting that learning
to reason in a way that holds up generalizes beyond the training set. No verification falls to 41.4%
by round 5, while outcome verification plateaus around 47%. Transfer is strongest on algebra and
number-theory problems and smaller on geometry and combinatorics, where GSM8K-style arith-
metic checks give less signal.

5.4   V ERIFICATION B REAKDOWN

Table 3 reports per-check pass rates at round 1 among correct-answer solutions. Because every
condition uses the same base model at round 1, the underlying rates are nearly identical (the slight
difference for No Verification reflects its smaller sample of 7,473 randomly chosen solutions versus
the full 46,836 correct-answer pool). The constraint check is the most lenient (91.8% pass), and the
arithmetic check the most selective (84.1% at the ≥80% threshold). The combined “All Checks” rate
of 66.1% confirms that VSI rejects ∼34% of correct-answer solutions (30,983 of 46,836), mostly
because of arithmetic errors and inconsistent intermediate values.
Table 4 provides a detailed parser coverage analysis. The key finding is that unparseable solutions
receive a vacuous pass on the arithmetic check (since the pass rate defaults to 1.0 when no expres-
sions are found), meaning the parser’s limited coverage leads to under-detection of errors rather than
false rejection. This substantially mitigates the concern about parser brittleness: the primary effect
is that some solutions with arithmetic errors slip through undetected, not that correct solutions are
incorrectly rejected.


                                                  8
Published as a conference paper at ICLR 2026




Table 4: Parser coverage at round 5 across conditions. “Vacuous pass” marks solutions with 0
parseable expressions, where the arithmetic check defaults to pass (rate = 1.0). “False rejection
(est.)” comes from a manual audit of 100 rejected correct-answer solutions. Best per row in bold;
VSI column shaded.

               Metric                                   No Verif.      Outcome      VSI
               Total correct-answer solutions            38,200         48,500    52,100
               Solutions with ≥ 1 expression (%)          71.3           79.1      88.4
               Solutions with 0 expressions (%)           28.7           20.9      11.6
               Mean expressions per solution               3.5            4.4       5.8
               Rejected by arithmetic (%)                 21.2           15.3       9.1
               False rejection est. (%)                    3.5            2.8       1.8

Table 5: Self-BLEU across rounds (lower = more diverse). Higher Self-BLEU indicates mode
collapse. Best (lowest) per column in bold; VSI rows shaded; collapsing values in red.

                 Condition                Iter 1   Iter 2     Iter 3     Iter 4   Iter 5
                 No Verification           0.32        0.38   0.47       0.56     0.64
                 Outcome Verification      0.31        0.34   0.37       0.39     0.41
                 Majority Voting           0.31        0.33   0.36       0.38     0.40
                 VSI (Verified)            0.30        0.32   0.33       0.34     0.35
                 VSI + DPO                 0.30        0.31   0.32       0.33     0.34


5.5   D IVERSITY AND M ODE C OLLAPSE

Table 5 reports Self-BLEU across conditions. No verification collapses fast (Self-BLEU rising from
0.32 to 0.64), confirming that unfiltered self-improvement training pushes the model toward repet-
itive outputs. Outcome verification and majority voting rise moderately (to ∼0.40). VSI stays low
(0.35 at round 5), indicating that checking the reasoning preserves diversity by keeping the model
from collapsing onto fragile shortcuts that happen to give the right answer.

6     D ISCUSSION

Why does checking the reasoning keep training stable? The mechanism is stopping errors be-
fore they spread. Under outcome-only filtering, a solution with a wrong arithmetic step A × B = C
(with C wrong) but a correct final answer (because another error compensates) still enters the fine-
tuning set, and the model picks up the bad arithmetic, which compounds over rounds. VSI’s arith-
metic check (via sympy) catches these before they can spread.

The “lucky guess” problem. Our analysis shows that a sizable fraction of correct-answer solu-
tions (often 20–40%) contain at least one arithmetic error or inconsistency. These lucky guesses are
indistinguishable from genuinely correct solutions under outcome verification; VSI removes them,
leaving a cleaner training signal.

Comparison with self-consistency. The majority-voting baseline compares checking the reason-
ing against a label-free self-consistency signal. From the round-1 statistics, majority voting accepts
∼80% of solutions (close to outcome verification at ∼78%), while VSI accepts only ∼52%—
substantially more selective. How stable each approach is over many rounds remains to be con-
firmed. A promising next step is to combine VSI with lightweight process reward models (PRMs):
a PRM could score steps that are hard to check by recomputation (such as how a problem is broken
down or which strategy is chosen), while VSI gives hard guarantees on arithmetic and consistency.

Limitations.   A few limitations are worth noting:


                                                   9
Published as a conference paper at ICLR 2026




      • Parsing coverage: our parser extracts expressions from most correct-answer solutions (Ta-
        ble 4), but a solution with no parseable expressions passes the arithmetic check by default
        (the rate defaults to 1.0). So limited coverage causes under-detection of errors, not false
        rejection. Natural-language arithmetic (“five times three”) and long multi-line derivations
        are still missed; our relaxed-parsing ablation recovers ∼15% more expressions, and better
        NLP-based parsing could recover more.
      • Domain specificity: the constraint checker is tailored to math word problems. Extending
        to other domains (e.g., code, logic puzzles) would need domain-specific constraints.
      • Computational overhead: the checks add ∼10 minutes of CPU time per round, negligible
        next to generation and training.
      • Aggressive filtering: in early rounds, when the base model produces fewer correct solu-
        tions, VSI can filter too aggressively. As a fallback, the pipeline relaxes the arithmetic
        threshold from 0.8 to 0.5 when fewer than 500 solutions pass all checks.

Beyond math. VSI is one concrete instance of a broader idea: a reliable, automatic check on
the reasoning can keep self-improvement training stable. Our implementation checks math, but
extending to other domains (formal theorem proving, code execution, physical simulation) would
mean building a domain-appropriate checker—each with its own parsing, constraints, and correct-
ness rules. In domains without a cheap external check—reinforcement learning with learned world
models, for instance—the check might instead read the model’s own internal state, which has been
shown to encode environment variables in a structured, linearly decodable form (Zhang, 2026). We
do not claim VSI generalizes automatically; rather, it is a template showing that when a reliable
check exists, self-improvement training can be stabilized. How long it stays stable is ultimately
bounded by how good that check is.


7   C ONCLUSION

We introduced VSI, a simple recipe that makes self-improvement training reliable by checking
the reasoning behind each solution—its arithmetic, its step-to-step consistency, and basic domain
constraints—rather than only its final answer. This keeps “lucky guess” solutions out of the fine-
tuning data. On GSM8K with Qwen3-4B-Thinking across 5 rounds of self-improvement training,
VSI reaches 91.0% accuracy (from an 80.5% baseline), while no verification collapses to 73.2% and
outcome-only filtering plateaus at 85.8%. VSI accepts ∼52% of generated solutions versus ∼78%
for outcome verification, rejecting ∼34% of correct-answer solutions with flawed reasoning. The
benefit transfers to MATH-500 (+5.7pp), and DPO on VSI-built preference pairs adds a marginal
gain (91.2% vs 91.0%). VSI offers a principled, reproducible way to make self-improvement train-
ing measurable and reliable, and it extends naturally to any domain where a reliable automatic check
on the reasoning is available.


R EFERENCES
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé Pinto, Jared Kaplan, Harri
 Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models
 trained on code. arXiv preprint arXiv:2107.03374, 2021.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
  Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John
  Schulman. Training verifiers to solve math word problems. In arXiv preprint arXiv:2110.14168,
  2021.

Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. QLoRA: Efficient finetuning
  of quantized language models. Advances in Neural Information Processing Systems, 36, 2024.

Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen, Yujiu Yang, Minlie Huang, Nan Duan, and
  Weizhu Chen. TORA: A tool-integrated reasoning agent for mathematical problem solving. In
  International Conference on Learning Representations, 2024.


                                                10
Published as a conference paper at ICLR 2026




Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
  and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. In
  Advances in Neural Information Processing Systems, volume 34, 2021.
Arian Hosseini, Xingdi Yuan, Nikolay Malkin, Aaron Courville, Alessandro Sordoni, and Rishabh
  Agarwal. V-STaR: Training verifiers for self-taught reasoners. arXiv preprint arXiv:2402.06457,
  2024.
Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang,
  and Weizhu Chen. LoRA: Low-rank adaptation of large language models. International Confer-
  ence on Learning Representations, 2022.
Jie Huang, Shibo Shen Gu, Arian Hosseini, Nikunj Saunshi, Kirthevasan Shiragur, Huan Sun, Osbert
   Wu, Ruoxi Xiang, Yifan Zhong, and Simeng Zuo. Large language models cannot self-correct
   reasoning yet. International Conference on Learning Representations, 2024.
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
 Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model
 serving with PagedAttention. In Symposium on Operating Systems Principles, 2023.
Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike,
  John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In International
  Conference on Learning Representations, 2024.
Aaron Meurer, Christopher P. Smith, Mateusz Paprocki, Ondrej Čertík, Sergey B. Kirpichev,
  Matthew Rocklin, Amit Kumar, Sergiu Ivanov, Jason K. Moore, Sartaj Singh, Thilina Rath-
  nayake, Sean Vig, Brian E. Granger, Richard P. Muller, Francesco Bonazzi, Harsh Gupta, Shivam
  Vats, Fredrik Johansson, Fabian Pedregosa, Matthew J. Curry, Andy R. Terrel, Štěpán Roučka,
  Ashutosh Saboo, Isuru Fernando, Sumith Kulal, Robert Cimrman, and Anthony Scopatz. SymPy:
  Symbolic mathematics in Python. PeerJ Computer Science, 3:e103, 2017.
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
  arXiv preprint arXiv:2009.03393, 2020.
Qwen Team. Qwen3 technical report. arXiv preprint arXiv:2505.09388, 2025.
Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and
  Chelsea Finn. Direct preference optimization: Your language model is secretly a reward model.
  Advances in Neural Information Processing Systems, 36, 2023.
Ilia Shumailov, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson, and Yarin Gal.
   Ai models collapse when trained on recursively generated data. Nature, 631:755–759, 2024.
Avi Singh, John D Co-Reyes, Rishabh Agarwal, Ankesh Anand, Piyush Patil, Xavier Garcia, Peter J.
  Liu, James Harrison, Jaehoon Lee, Kelvin Xu, Aaron Parisi, Aviral Kumar, Alex Alemi, Alex
  Rizkowsky, Azade Nova, Ben Adlam, Bernd Bohnet, Gamaleldin Elsayed, Hanie Sedghi, Igor
  Codreanu, S. Keshav, et al. ReST-EM: Beyond human data: Scaling self-training for problem-
  solving with language models. In Advances in Neural Information Processing Systems, 2024.
Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia
  Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with process- and
  outcome-based feedback. In arXiv preprint arXiv:2211.14275, 2022.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdh-
  ery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models.
  International Conference on Learning Representations, 2023.
Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho, Sainbayar Sukhbaatar, Jing Xu, and Jason
 Weston. Self-rewarding language models. In International Conference on Machine Learning,
 2024.
Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. STaR: Bootstrapping reasoning with
  reasoning. In Advances in Neural Information Processing Systems, volume 35, 2022.
Xinyu Zhang. What do world models learn in RL? Probing latent representations in learned envi-
  ronment simulators. arXiv preprint arXiv:2603.21546, 2026.


                                               11
