                                                                  R E P OT: Recoverable Program-of-Thought
                                                                            via Checkpoint Repair*

                                                                                       Parsa Mazaheri
                                                                              University of California, Santa Cruz
                                                                                     pmazaher@ucsc.edu



                                                                Abstract                           Yao et al., 2023a). Neither is recoverable: a one-
                                                                                                   shot P OT plan with a mid-rollout error cannot re-
arXiv:2605.30052v1 [cs.SE] 28 May 2026




                                             One-shot Program-of-Thought (P OT) emits a            sume from where it succeeded; tree-search methods
                                             Python program that prints a primitive-action
                                                                                                   pay branching cost during generation regardless of
                                             plan; a single invalid action silently invalidates
                                             the trajectory. We introduce R E P OT (Recover-
                                                                                                   whether the first trajectory was already mostly cor-
                                             able P OT): a deterministic verified replay that      rect.
                                             walks the plan through the environment to its            We propose R E P OT— Recoverable Program-
                                             first invalid transition, then one LLM call that      of-Thought — a small modification of one-shot
                                             resumes from the verified prefix. R E P OT costs      P OT that adds checkpoint-based recovery without
                                             at most one extra LLM call on the ∼14% of             moving to tree search. R E P OT works in three steps
                                             problems where P OT fails. R E P OT beats P OT        (Algorithm 1):
                                             by +3 to +11pp across four closed-model con-
                                             figurations on P UZZLE Z OO-775 and peaks at            1. Run P OT once: emit a Python program, exe-
                                             96.9% vs 86.3% on gpt-5.4-mini-medium;
                                                                                                        cute it, parse the printed move list.
                                             against the matched-budget P OT-retry base-
                                             line, R E P OT wins decisively on Gemini (+3.8
                                                                                                     2. Verified replay: walk the proposed actions
                                             pp, 95% CI [+2.2, +5.4]), is within sampling
                                             noise on GPT-medium and Claude, and loses                  through the environment one step at a time, ac-
                                             on GPT-mini — a capability-scaling pattern                 cumulating a maximal verified prefix of valid
                                             we begin to address with A DAPTIVE R E P OT, a             transitions until the first failure (Eq. (1)).
                                             rule-based dispatcher that routes between suffix
                                             repair and a fresh P OT retry based on verified-        3. If the prefix already reaches the goal, return
                                             prefix length (preliminary; App. N). We repli-             success. Otherwise issue one suffix-repair
                                             cate on P LAN B ENCH B LOCKSWORLD (+1.1                    LLM call, conditioning on the verified pre-
                                             to +11.4pp) and on four open-weights models                fix, the verified state at the failure boundary,
                                             (+3.3 to +20.0pp on three of four). On D E -               and the verifier’s error message.
                                             RAIL-550, our controlled recovery benchmark,
                                             every condition with access to checkpoint in-         Novelty and positioning. R E P OT reframes one-
                                             formation clears ≥30% on GPT-medium and
                                                                                                   shot LLM reasoning as a recoverable execution:
                                             ≥70% on Gemini, vs ≤3.1% for error-only
                                             feedback — showing that checkpoint informa-           rather than all-or-nothing, the verifier owns the
                                             tion, not the specific verified-prefix tail, is the   trusted state and the model is only ever asked to
                                             load-bearing recovery signal.                         repair the unverified suffix. Three pieces compose:
                                                                                                   (i) a deterministic verified-replay primitive that
                                         1    Introduction                                         turns any P OT rollout into a checkpoint-resumable
                                                                                                   computation with no LLM calls; (ii) a suffix-repair
                                         Large language models can sketch impressive
                                                                                                   call conditioned on the verified state rather than a
                                         plans, then commit one illegal action and silently
                                                                                                   textual critique of the prior attempt — one well-
                                         fail the entire task. The dominant fix is to ei-
                                                                                                   typed task; (iii) a single repair budget (R = 1), so
                                         ther run a single sample through a tool (Program-
                                                                                                   cost stays at P OT baseline on the ∼86% of easy
                                         of-Thought, P OT Chen et al., 2023) or sample
                                                                                                   problems and only doubles on the rest. Where
                                         many independent rollouts and aggregate (Self-
                                                                                                   Reflexion-style (Shinn et al., 2023) verbal critique
                                         Consistency Wang et al., 2023, Tree of Thoughts
                                                                                                   asks the model to introspect its mistakes textu-
                                             * Code: https://github.com/parsa-mz/RePot             ally, R E P OT makes the verifier the source of truth.
Where ToT and LATS (Zhou et al., 2024) branch             trolled puzzle benchmark across four classical plan-
during generation, R E P OT branches only after a         ning environments (Tower of Hanoi, Checker Jump-
deterministic check identifies a real failure point.      ing, River Crossing, Blocksworld) at controllable
D ERAIL-550 (§7) shows the trusted checkpoint is          complexity, and report that frontier reasoning mod-
the load-bearing signal: 80.7% recovery of injected       els exhibit sharp accuracy collapse once complex-
errors versus 20.7% from error-only feedback.             ity exceeds a model-specific threshold, even when
                                                          given the algorithm. They further show that failures
Contributions.                                            concentrate early in the trace: the first invalid move
    • Algorithm. R E P OT— a recoverable exten-           often appears at a small fraction of the optimal-
      sion of P OT that combines deterministic veri-      plan length, and the remaining tokens are spent on
      fied replay (Eq. 1) with a single suffix-repair     a wrong-but-consistent continuation. Song et al.
      LLM call.                                           (2025) re-run a subset and argue some collapses
                                                          are artifacts of impossible River Crossing instances
    • Empirical. On P UZZLE Z OO-775, a verifier-         and prompt encoding; Scholten et al. (2024) frame
      backed suite, R E P OT improves over P OT by        the same phenomenon as “metacognitive myopia”.
      +3 to +11pp across three frontier models            Whatever the framing, the empirical pattern is ro-
      in four configurations, replicates on P LAN -       bust: most failed traces have a long valid prefix and
      B ENCH B LOCKSWORLD (Valmeekam et al.,              a single mid-rollout misstep. This is precisely the
      2023a) (+1.1 to +11.4pp), and beats a               regime in which checkpoint-based recovery should
      matched-budget P OT-retry baseline on the           help. R E P OT is a targeted fix for this recover-
      two reasoning-enabled models.                       able subset of failures: we do not claim to solve
                                                          reasoning collapse in general, only to mitigate re-
    • Mechanism. A controlled D ERAIL-550                 coverable execution collapse where a trusted inter-
      benchmark isolates which signal makes re-           mediate state can be preserved and resumed from.
      covery work: trusted checkpoint state sepa-
                                                          Prior work on one-shot brittleness. A large
      rates the recovery-capable conditions from
                                                          body of work has proposed remedies for the one-
      error-only feedback by ∼60pp; the explicit
                                                          shot failure mode; we group them into three fam-
      verified-prefix tail provides a smaller, model-
                                                          ilies. (i) Sample more: Self-Consistency (Wang
      dependent additional benefit.
                                                          et al., 2023) and best-of-k generate k trajectories
2    Background                                           and vote / pick the best by some scoring function.
                                                          Cost is O(k) LLM calls per problem regardless
Program-of-Thought planning. P OT (Chen                   of whether the first trajectory was nearly correct.
et al., 2023) prompts the model to write a Python         (ii) Branch during generation: Tree of Thoughts
program whose printed output is the plan, then runs       (Yao et al., 2023a) and LATS (Zhou et al., 2024)
the program in a sandbox and parses the printed           treat reasoning as search, expanding multiple con-
token list. The original work targeted arithmetic         tinuations and using a value model or verifier to
and symbolic reasoning, where the program is the          prune. They pay tree-search cost on every problem,
answer. In LLM planning, the printed plan is a            including easy ones. (iii) Iterate with critique:
sequence of primitive actions (a1 , . . . , an ) which    Reflexion (Shinn et al., 2023), ReAct (Yao et al.,
is then executed by an environment simulator, and         2023b), Self-Refine (Madaan et al., 2023), and Self-
the trajectory either reaches the goal or it does not.    Repair (Olausson et al., 2024) run a second LLM
P OT’s appeal in this setting is that it pushes the       call conditioned on a textual critique of the prior
brittle bookkeeping (state tracking, legal-action fil-    attempt. The critique can be wrong (the model that
tering, search) onto the model in code form, which        produced the failure now also produces the diag-
the model is good at (Wei et al., 2022; Wang et al.,      nosis), and there is no checkpoint mechanism: the
2023). The cost is also its weakness: a single ille-      second call re-plans from scratch given the critique.
gal action mid-rollout invalidates the entire trajec-
tory, and the trajectory’s verified prefix is discarded   Process verification and rewards. A separate
along with the invalid suffix.                            line uses process reward models (PRMs) (Light-
                                                          man et al., 2024) to score partial reasoning traces
The Illusion-of-Thinking finding. Shojaee et al.          and reject low-scored continuations. PRMs need a
(2025) (“The Illusion of Thinking”) run a con-            learned scorer and target mathematical reasoning
where ground-truth verification is hard. R E P OT          Algorithm 1 R E P OT— Recoverable Program-of-
sits in the complementary regime where the verifier        Thought
is the environment itself — exact, free, and imme-         Input: problem (s0 , g), env E, model M, repair
diately available — which lets us skip the learned             budget R
scorer entirely.
                                                                                                  
                                                            1: π ← M P OTP ROMPT(s0 , g) ▷ 1. one-shot
                                                               P OT
3     Related Work
                                                            2: (P, s, ϵ) ← R EPLAY (E, s0 , π)        ▷ 2. verified
Section 2 surveyed the main families that R E -                replay (Eq. 1)
P OT relates to. Here we position R E P OT against          3: if I S G OAL(s, g) then return P
three further adjacencies. Concurrent transac-              4: end if
tional/checkpoint work (Mohammadi et al., 2026;             5: for r = 1, . . . , R do     ▷ 3. suffix repair from
Chang and Geng, 2025; Li et al., 2025) targets                 checkpoint
                                                                     π ′ ← M R EPAIR P ROMPT(s0 , g, s, P, ϵ)
                                                                                                                  
multi-agent coordination rather than one-shot P OT.         6:
Decoupled reasoning–observation (ReWOO, Xu                  7:       (P ′ , s, ϵ) ← R EPLAY(E, s, π ′ )
et al., 2023; ThinkSwitcher, Liang et al., 2025)            8:       P ← P ++ P ′
routes between thinking modes per input; R E -              9:       if I S G OAL(s, g) then return P
P OT routes per-trajectory, conditioned on a ver-          10:       end if
ified failure boundary. Planning benchmarks                11: end for
P LAN B ENCH (Valmeekam et al., 2023a,b) provides          12: return P               ▷ partial; budget exhausted
PDDL-grounded LLM planning evaluation; we use
its Blocksworld split as external replication and
discuss the agentic-gap framing (Khan et al., 2025)        ary, and ϵk is the verifier’s error message at step k
in Discussion.                                             (or the empty string if k = n + 1). The function is
                                                           total, deterministic, and makes no LLM calls; its
4     Method                                               cost is O(n) environment steps.
4.1    Problem setting
                                                           4.3   R E P OT algorithm
We consider planning tasks of the form (s0 , g, E),
                                                           R E P OT composes P OT with verified replay and
where s0 is the initial state, g is the goal specifica-
                                                           a single suffix-repair call. The full algorithm is
tion, and E is a deterministic environment with a
                                                           shown in Algorithm 1. Two hyperparameters gov-
step function E : (s, a) 7→ (s′ , valid) that returns
                                                           ern its behaviour: the repair budget R (default
the next state and a validity flag. A plan is a se-
                                                           R = 1) and the verified-prefix tail length T shown
quence of primitive actions π = [a1 , a2 , . . . , an ].
                                                           to the model during repair (default T = 4). The
Success is I S G OAL(sn , g) where sn is the result of
                                                           model is otherwise sampled at τ = 0.
replaying π from s0 . We assume the environment
exposes a verifier (the same S TEP) and a goal predi-      A simple recovery model. For a problem in-
cate; we do not assume the model has direct access         stance, let p be the probability that P OT succeeds
to either.                                                 on the first sample, q the probability that P OT fails
4.2    Verified replay                                     but leaves a recoverable valid prefix, r the condi-
                                                           tional probability that suffix repair succeeds given
The core primitive is a deterministic verified-replay      a recoverable prefix, b the conditional probability
function that takes a candidate action sequence            that a fresh P OT resample succeeds given the first
and walks it through the environment. Given start          sample failed, and b′ ≤ b the fresh-retry success
state s0 and a plan π = (a1 , . . . , an ), define the     rate restricted to the unrecoverable subset. R E P OT
trajectory si = step(si−1 , ai ) if the transition is      beats P OT-retry iff
valid, else ⊥. Let k be the smallest index for which
the transition is invalid (or n + 1 if every action is             q (r − b) > (1 − p − q) (b − b′ ),          (2)
valid). Then

       R EPLAY(E, s0 , π) = P, sk−1 , ϵk , (1)
                                                          i.e. when verified-prefix repair beats the fresh-
                                                           sample marginal on the recoverable subset. Larger
where P = (a1 , . . . , ak−1 ) is the maximal verified     q (longer valid prefixes, scaling with capability)
prefix, sk−1 is the verified state at the failure bound-   makes the condition more favourable; §6.4 and
Figure 1: The R E P OT pipeline. (1) Problem provides initial state s0 and goal g. (2) P OT call (LLM call #1): the
model emits a Python program whose stdout encodes the action plan π. (3) Verified replay: walk π through the
environment one step at a time — deterministic, no LLM calls — producing the maximal valid prefix and the failure
boundary. If every action is valid, branch to (6) Final via the upper verified, goal reached arrow. Otherwise the
boundary is packaged as (4) Checkpoint: verified prefix P , verified state sk , and verifier error ε. The (5) Suffix
repair call (LLM call #2) sees the checkpoint and emits a suffix that resumes from sk . The lower arrow is the single
repair budget (R = 1): the suffix is itself sent through verified replay; on success we land at Final, on failure we
accept the partial verified plan.


Fig. 3 show this empirically. The adaptive variant              Three named ablations are used in §7: R E P OT
below dispatches per-problem to maximize Eq. 2.             full (Algorithm 1), R E P OT no-prefix (hides the prefix
                                                            tail; model sees only the current verified state +
4.4   Adaptive recovery policy
                                                            error), and R E P OT restart (repair call restarts from
Algorithm 1 always commits to the verified prefix.          s0 instead of the verified s, isolating “checkpoint”
When the prefix is empty or very short, the verified        from “extra call”). Definitions in App. L.
state s collapses to s0 and the repair call effectively
restarts from the initial state but with a (potentially     5     Experimental Setup
misleading) error anchor. Empirically, on weaker
                                                            5.1    Benchmarks
models P OT-retry’s fresh sample outperforms an-
choring on a short prefix (§6.1).                           P UZZLE Z OO-775. A stratified problem set
   As a preliminary extension, we introduce A DAP -         across four classical planning environments: Tower
TIVE R E P OT, a rule-based dispatcher with the             of Hanoi (8 complexities, 200 problems), Checker
same R = 1 budget. After verified replay, we read           Jumping (9 complexities, 225 problems), River
the prefix fraction ϕ = (k − 1)/n and route to              Crossing (4 complexities, 100 problems), and
a fresh P OT retry when n = 0 or ϕ < 0.15, oth-             Blocksworld (10 complexities, 250 problems).
erwise to suffix repair (Alg. 1). Thresholds were           Each environment exposes S TEP, I S G OAL, N OR -
fixed a priori (not tuned on test); a threshold sweep       MALIZE, and L EGAL ACTIONS interfaces.
and alternative dispatcher rules are left to future         P LAN B ENCH Blocksworld (378 problems).
work. The dispatcher realizes the optimal-branch            We use both subsets of P LAN B ENCH’s
prediction implied by Eq. 2: route to fresh sampling        Blocksworld split (Valmeekam et al., 2023a):
when the recoverable subset is empty, otherwise             generated_basic (189 4-block instances) and
exploit the verified prefix. Open-source results are        generated (189 instances spanning 3–12 blocks).
in App. N.                                                  We adapt the PDDL semantics into our S TEP in-
4.5   Repair prompt and ablations                           terface (predicate state, four-op action vocabulary
                                                            {pick-up, put-down, stack, unstack}, partial-goal
The repair call uses a verified-prefix-conditioned
                                                            subset check); see Appendix H for the adapter.
prompt: a stable block (problem statement, goal)
above a verifier-checkpoint marker, and a dy-               D ERAIL-550 (550 errors × 11 conditions). A
namic block (last T verified moves, current verified        controlled recovery-from-injected-error benchmark
state, legal actions, verifier error) below. Splitting      we build alongside P UZZLE Z OO-775. For each
along this boundary makes the stable block prefix-          problem, we run an oracle plan to a checkpoint
cacheable across repair calls; the full template is in      ∼1/3 of the way through, inject one randomly cho-
App. K (Fig. 12).                                           sen wrong action, and ask each recovery method to
take over. We compare 11 conditions (§7) includ-       6.2   Per-environment breakdown
ing R E P OT’s three prefix ablations.                 The R E P OT −P OT delta concentrates in
                                                       Blocksworld (+9.2 to +17.2pp on every reasoning
5.2    Models                                          model) and Checker Jumping (up to +15.6
We evaluate R E P OT on both closed-source             on gpt-5.4-mini-medium). Hanoi and River
and open-weights models.      The closed set           Crossing are saturated by P OT on most models
comprises three frontier models in four con-           (≥ 99%); the exception is gemini’s River Crossing
figurations:  gpt-5.4-mini-medium (reason-             collapsing to 76% P OT, which R E P OT recovers to
ing medium), gpt-5.4-mini (no reasoning),              100% (+24.0pp). Per-environment numbers are in
gemini-3.5-flash (thinking=MEDIUM), and                Appendix A (Table 5).
claude-sonnet-4.6 (no thinking). The open-
                                                       6.3   External replication: P LAN B ENCH
weights set comprises four models served on a
                                                             B LOCKSWORLD
single NVIDIA H100 80GB GPU via vLLM with
extended thinking disabled: Qwen3.6-35B-A3B            We repeat the P OT vs. R E P OT comparison on
(Qwen Team, 2026), gemma-4-26B-A4B-it                  P LAN B ENCH B LOCKSWORLD (378 instances, 3–
(Google DeepMind, 2025), gpt-oss-20b (Ope-             12 blocks). To keep cost low and avoid P OT saturat-
nAI, 2025), and Nemotron-3-Nano-30B-A3B                ing, we use the no-thinking variants of each model.
(NVIDIA, 2025). Sampling is deterministic              Table 2 reports the headline; the per-complexity
(τ = 0); full hyperparameters are in Table 4           breakdown is in Appendix A. R E P OT improves
(App. B).                                              over P OT on all three models. The biggest gains
                                                       land in the mid-complexity band (4–6 blocks),
5.3    Methods compared                                where P OT has both failure headroom and enough
                                                       structure to recover toward.
C OT, P OT, Self-Consistency (SC, k = 8), P OT-
retry, and our R E P OT (R = 1, T = 4). C OT and SC    Limitation: matched-budget control. The
emit prose plans; P OT, P OT-retry, and R E P OT all   P LAN B ENCH comparison reports P OT vs R E P OT
emit Python code. P OT-retry is a matched-budget       only; we do not run P OT-retry on P LAN B ENCH
control: run P OT once, and on verifier failure run    in this version. The external replication therefore
P OT once more from scratch with no prefix and no      validates only the raw lift, not the matched-budget
checkpoint — the same two-LLM-call worst-case          claim of Table 1.
budget as R E P OT, but with no checkpoint mech-       Multi-seed variance. R E P OT − P OT is positive
anism. The P OT vs P OT-retry vs R E P OT triple       on every seed for all three reasoning-thinking-on
lets us separate re-rolling from genuine checkpoint-   configurations (∆ ∈ [+1, +10]pp); per-seed num-
based recovery.                                        bers and lower run-to-run variance under R E P OT
                                                       are tabulated in Table 6 (App. D).
6     Results
                                                       6.4   Open-source replication and capability
6.1    Headline cross-model accuracy                         scaling
Table 1 reports success rate on P UZZLE Z OO-775       We replicate the headline comparison on a 120-
for the four closed models. R E P OT beats P OT        problem stratified subset with four open-weights
on every model with ∆ ∈ [+2.7, +10.6]pp; the           models served via vLLM with extended thinking
largest improvement is on gpt-5.4-mini-medium          disabled. Per-model rates appear in the bottom
(96.9% vs 86.3%). Against the matched-budget           block of Table 1 and visually in Fig. 2; R E P OT
P OT-retry baseline, R E P OT wins decisively on       improves over P OT on three of four open-source
Gemini (+3.8, 95% CI [+2.2, +5.4]), is statisti-       models (+3.3 to +20.0 pp). Nemotron-3 Nano
cally a tie on GPT-medium and Claude (CIs cross        30B FP8 underperforms P OT by 15 pp; with a
zero), and loses on GPT-mini (−6.6, [−9.4, −3.7]).     CoT baseline of 6.7% it sits near the instruction-
The result is consistent with our central claim that   following floor for this task family, the predicted
R E P OT’s mechanism contribution scales with the      failure mode of Eq. 2 when per-recoverable repair
validity of the first P OT plan, which itself scales   success r collapses. As a preliminary extension,
with model capability (§8). Per-method cost is in      A DAPTIVE R E P OT (App. N) further closes the gap
App. G (Fig. 9).                                       to P OT-retry on the weaker rows.
                      Model                    CoT    SCk=8    PoT    PoT-retry   RePoT    R−PR
                      Closed frontier models
                      GPT-5.4-mini (med)⋆      11.6    37.5    86.3       96.6      96.9   +0.3
                      Gemini 3.5 Flash⋆        83.0    96.6    81.3       84.1      87.7   +3.6
                      Claude Sonnet 4.6        44.1    75.9    83.1       87.5      86.1   −1.4
                      GPT-5.4-mini             17.9    24.4    58.7       68.0      61.4   −6.6
                      Open-source models
                      Gemma 4 26B-A4B          18.3    24.2    49.2       54.2      69.2   +15.0
                      GPT-OSS 20B              31.7    58.3    48.3       59.2      62.5    +3.3
                      Qwen 3.6 35B-A3B         36.7    59.2    55.0       61.7      58.3    −3.4
                      Nemotron-3 Nano 30B       6.7     8.3    25.8       34.2      10.8   −23.4

Table 1: Cross-model success rate (%). R−PR is RePoT−PoT-retry in percentage points. P OT- RETRY is a matched-
budget control: run P OT, on failure run P OT a second time from scratch (no checkpoint, no prefix). Paired bootstrap
95% CIs on R−PR (B = 10000). Closed: GPT-med [−1.4, +1.9], Gemini [+2.2, +5.4], Claude [−3.1, +0.3],
GPT-mini [−9.4, −3.7] — Gemini and GPT-mini are significant; GPT-med and Claude are within sampling noise.
Open-source: Gemma [+4.2, +25.0], GPT-OSS [−6.7, +13.3], Qwen [−10.8, +4.2], Nemotron [−31.7, −15.0] —
Gemma significant positive, Nemotron significant negative, GPT-OSS and Qwen within sampling noise. R E P OT’s
contribution scales with the validity of the first P OT plan, which itself scales with model capability (§8); A DAPTIVE
R E P OT is in App. N. ⋆ reasoning/thinking enabled at medium; unmarked closed rows run without reasoning.


     Model                 n PoT RePoT           ∆
     GPT-5.4-mini      756 55.0        64.3 +9.3
     Claude Sonnet 4.6 756 79.9        91.3 +11.4
     Gemini 3.5 Flash 756 98.9        100.0 +1.1

Table 2: External replication on P LAN B ENCH
B LOCKSWORLD (378 instances, 3–12 blocks). Suc-
cess rate (%); n = 756 records per row (378 problems
× 2 methods). All three models run without thinking
(no reasoning effort on GPT-5.4-mini; thinking off on
Claude Sonnet 4.6; thinking_level=NONE on Gemini              Figure 2: Open-source replication. R E P OT lift tracks
3.5 Flash) to keep cost low and avoid PoT saturation.         model capability: Gemma 4 (top) gains +20 pp over
RePoT beats PoT on every model. Paired bootstrap              P OT; Nemotron-3 Nano 30B FP8 (right) is the predicted
95% CIs (B = 10000) on ∆: GPT-mini [+3.5, +14.9],             capability-floor failure (Eq. 2).
Claude [+6.9, +15.9], Gemini [+0.3, +2.1] — all three
significant. P OT- RETRY is not run on P LAN B ENCH in
this version (limitation; the matched-budget claim of         7     Mechanism Analysis
Table 1 is not externally replicated here).
                                                              7.1     Checkpoint information is the
                                                                      load-bearing signal
                                                              D ERAIL-550 compares 11 recovery methods on
                                                              550 injected errors per model on two reasoning-
                                                              thinking-on configurations (Gemini, GPT (med)).
                                                              The decisive mechanism evidence is the gap be-
   Beyond per-model numbers, the open-source                  tween conditions that see checkpoint information
spread lets us test the prediction of Eq. 2 quan-             (verified state s, legal actions, and the verifier error
titatively. Across (model, environment) cells, the            ε) and conditions that see only an error message:
mean verified-prefix fraction on failed initial P OT          every checkpointed method clears 30% on GPT
plans (a model-level proxy for q in Eq. 2) correlates         (med) and 70% on Gemini, while error_only
positively with the R E P OT −P OT-retry success-             stays at 3.1% / 20.7% and no_feedback at 1.6%
rate delta: cells where the model leaves a long valid         / 3.8%. The ∼30–80pp gap is the headline find-
prefix before failing are exactly the cells where R E -       ing: checkpoint information — not textual er-
P OT’s verified-prefix repair beats fresh resampling          ror feedback or the specific verified-prefix tail
(Fig. 3, slope +35). This is the central qualitative          — is the decisive recovery signal (Fig. 4, Table 3).
claim of the paper made quantitative.                         Within the checkpointed conditions, the within-
                                                                  Recovery condition         Gemini GPT (med)
                                                                  No-checkpoint baselines
                                                                  no_feedback                   3.8         1.6
                                                                  error_only                   20.7         3.1
                                                                  Checkpointed baselines
                                                                  state_feedback               83.1        40.4
                                                                  state_plus_legal_actions     78.5        37.6
                                                                  stateguard_rollback          13.1         4.5
                                                                  RePoT prefix-conditioning ablation (ours)
                                                                  repot_full                  80.7          59.6
                                                                  repot_no_prefix             76.9          53.8
                                                                  repot_restart               82.4          94.5

                                                            Table 3: D ERAIL-550: success rate (%) on 550 in-
Figure 3: Capability scaling. Each point is one (model,     jected errors per condition, on two reasoning-thinking-
environment) cell across both closed and open-source        on configurations (Gemini = Gemini 3.5 Flash with
runs. x: mean verified-prefix fraction on failed initial    thinking_level=MEDIUM; GPT (med) = GPT-5.4-mini
P OT plans (a model-level proxy for q in Eq. 2); y: R E -   with reasoning at medium). Headline: a ∼30–
P OT −P OT-retry success delta in pp. The positive slope    80pp gap separates every checkpointed condition
confirms the mechanism: R E P OT’s lift scales with the     (state_feedback, repot_*) from non-checkpointed
validity of the first P OT plan, which itself scales with   baselines (error_only, no_feedback: ≤ 3% on GPT
model capability.                                           (med), ≤ 21% on Gemini). Trusted checkpoint state
                                                            is the load-bearing recovery signal, not textual er-
                                                            ror feedback alone. R E P OT operationalises that sig-
prefix ablation is mixed: R E P OT full beats R E P OT      nal inside P OT via verified replay. The within-R E P OT
no-prefix by +3.8 / +5.8pp on Gemini / GPT (med),           trio shows repot_restart>repot_full on both mod-
but R E P OT restart (which discards the verified state     els (more pronounced on GPT (med)) — the prefix-tail
and restarts from s0 with the same checkpoint in-           beyond the checkpoint is a model-dependent secondary
formation) beats R E P OT full on both models, with         effect, discussed in §7.1 and App. J.
a large gap on GPT (med) (94.5 vs 59.6). We read
this honestly: anchoring the repair on the verified-
                                                            predicts the matched-budget P OT-retry result in
prefix tail beyond the checkpoint can hurt, espe-
                                                            Table 1: on the two reasoning-enabled models
cially on weaker configurations; the checkpoint
                                                            (gpt-medium, gemini) R E P OT beats P OT-retry by
information itself is what matters, not the specific
                                                            +0.3 and +3.6pp; on the two non-reasoning rows
resumption point. A DAPTIVE R E P OT’s dispatcher
                                                            (claude no-thinking, gpt-mini no-reason) P OT-
operationalizes this: short prefixes route to fresh
                                                            retry beats R E P OT by 1.4 and 6.6pp. We read this
retry, only long prefixes anchor on the verified state.
                                                            as a scoped claim: R E P OT is the right move when
Cost. R E P OT averages 1.11–1.39× P OT LLM                 the model is capable enough to produce useful valid
calls across the four configurations. Per-method,           prefixes; when it is not, a fresh independent sam-
per-model breakdown in Table 8 (App. G).                    ple (P OT-retry) escapes wrong commitments more
                                                            effectively.
Failure modes. The dominant R E P OT failure is
repair_budget_exhausted on hard Blocksworld;                Future work. Empty-plan retry to close hand-
most hand-analyzed losses involve an empty initial          analyzed losses; adaptive repair budget conditioned
P OT plan with no prefix to anchor on (App. I).             on the verified-prefix fraction; open-source repli-
                                                            cation; broader benchmarks (PDDLGym, ALF-
8   Discussion                                              World).
When R E P OT helps and when it does not. R E -
                                                            9   Conclusion
P OT’s lift concentrates where P OT produces a long
valid prefix before failing: a mostly-correct plan          R E P OT is a small, structural addition to P OT: de-
whose suffix needs repair. Where P OT already suc-          terministic verified replay plus one bounded suffix-
ceeds (saturated easy regimes, gemini on Hanoi              repair call. Against the matched-budget P OT-retry
at 99.5%) R E P OT is no-op. Where P OT fails at            baseline on P UZZLE Z OO-775, R E P OT wins deci-
the first action, R E P OT’s replay degenerates to a        sively on Gemini (CI [+2.2, +5.4]), is within sam-
restart-from-s0 and lift is near zero. This shape           pling noise on GPT-medium and Claude, and loses
Figure 4: D ERAIL-550, headline conditions only. The ∼60pp gap between checkpointed and no-checkpoint
conditions is the load-bearing finding. The full 11-condition table is in Table 3.


on GPT-mini — a capability-scaling pattern that          Single-call repair budget. We use R = 1
D ERAIL-550 isolates: checkpoint information, not        as a cost-conservative choice; multi-call repair
the specific verified-prefix tail, is the load-bearing   (Alg. 1 line 4) likely closes the long-horizon
recovery signal. The cost is one extra LLM call          B LOCKSWORLD tail but is not evaluated here.
on the ∼14% of problems where P OT fails the
                                                         Within-prefix conditioning is model-dependent.
first time; the rest run at P OT cost. R E P OT is
                                                         On D ERAIL’s controlled mid-rollout error setting,
the cheapest viable middle between one-shot P OT
                                                         R E P OT restart beats R E P OT full on both configura-
and tree-search-based methods for verifier-backed
                                                         tions (more pronounced on GPT (med), 94.5 vs
planning, and a candidate primitive for any set-
                                                         59.6). The checkpoint-state contribution remains
ting where the environment exposes a deterministic
                                                         the load-bearing recovery signal, but anchoring the
step function and a goal predicate. Generalisation
                                                         repair on the verified-prefix tail can hurt on weaker
to verifier-backed agentic settings (coding, SQL,
                                                         configurations (App. J).
browser automation) is left to future work.
                                                         Negative-∆ cells in P LAN B ENCH. GPT (mini)
Limitations                                              at c = 8, 11 shows −8.3 and −9.1pp R E P OT vs
                                                         P OT, where single-call repair sometimes commits
Verifier-required scope. R E P OT assumes a de-          to a bad prefix at low P OT-base accuracy.
terministic verifier (puzzles, planning, tool use);
                                                         Statistical scope. P LAN B ENCH reports P OT vs
free-form reasoning would need a learned scorer
                                                         R E P OT only; we do not run P OT-retry on P LAN -
(Lightman et al., 2024). The evaluation in this
                                                         B ENCH in this version, so the matched-budget
paper is restricted to verifier-backed puzzle and
                                                         claim of Table 1 is not externally replicated. Open-
planning environments (P UZZLE Z OO-775, P LAN -
                                                         source results are on a 120-problem stratified sub-
B ENCH B LOCKSWORLD, D ERAIL-550). Whether
                                                         set, smaller than the closed-model headline.
the same recoverable-execution abstraction gener-
alizes to verifier-backed agentic settings (coding       Adaptive RePoT is preliminary. A DAPTIVE
agents with test suites, SQL agents with schema          R E P OT uses a hand-picked threshold (ϕ < 0.15); a
checks, browser automation with page-state val-          sensitivity sweep over ϕ and alternative dispatcher
idators) is an open empirical question we do not         rules (e.g., learned gating) are left to future work.
address.
References                                                 Qwen Team. 2026. Qwen3.6-35B-A3B: Agentic coding
                                                             power, now open to all.
Edward Y. Chang and Longling Geng. 2025. SagaLLM:
  Context management, validation, and transaction          Florian Scholten, Tobias R. Rebholz, and Mandy Hüt-
  guarantees for multi-agent llm planning. Preprint,         ter. 2024. Metacognitive myopia in large language
  arXiv:2503.11951.                                          models. Preprint, arXiv:2408.05568.
Wenhu Chen, Xueguang Ma, Xinyi Wang, and
                                                           Noah Shinn, Federico Cassano, Edward Berman, Ash-
 William W. Cohen. 2023. Program of thoughts
                                                             win Gopinath, Karthik Narasimhan, and Shunyu Yao.
 prompting: Disentangling computation from reason-
                                                             2023. Reflexion: Language agents with verbal rein-
 ing for numerical reasoning tasks. Transactions on
                                                             forcement learning. In Advances in Neural Informa-
 Machine Learning Research (TMLR).
                                                             tion Processing Systems (NeurIPS).
Google DeepMind. 2025. Gemma 4: Open multimodal
  models. Model card; Apache 2.0 license.                  Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh,
                                                             Maxwell Horton, Samy Bengio, and Mehrdad Fara-
Sheraz Khan, Subha Madhavan, and Kannan Natara-              jtabar. 2025. The illusion of thinking: Understanding
  jan. 2025. A comment on “the illusion of think-            the strengths and limitations of reasoning models
  ing”: Reframing the reasoning cliff as an agentic gap.     via the lens of problem complexity. In Advances in
  Preprint, arXiv:2506.18957.                                Neural Information Processing Systems (NeurIPS).

Peiran Li, Xinkai Zou, Zhuohang Wu, Ruifeng Li,            Zhao Song, Song Yue, and Jiahao Zhang. 2025. Think-
  Shuo Xing, Hanwen Zheng, Zhikai Hu, Yuping                 ing isn’t an illusion: Overcoming the limitations of
  Wang, Haoxi Li, Qin Yuan, Yingmo Zhang, and                reasoning models via tool augmentations. Preprint,
  Zhengzhong Tu. 2025. SafeFlow: A principled pro-           arXiv:2507.17699.
  tocol for trustworthy and transactional autonomous
  agent systems. Preprint, arXiv:2506.07564.               Karthik Valmeekam, Matthew Marquez, Alberto Olmo,
                                                             Sarath Sreedharan, and Subbarao Kambhampati.
Guosheng Liang, Longguang Zhong, Ziyi Yang, and              2023a. PlanBench: An extensible benchmark for
  Xiaojun Quan. 2025. Thinkswitcher: When to think           evaluating large language models on planning and
  hard, when to think fast. In Findings of the Associa-      reasoning about change. In Advances in Neural In-
  tion for Computational Linguistics: EMNLP 2025.            formation Processing Systems (NeurIPS).
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri        Karthik Valmeekam, Matthew Marquez, Sarath Sreed-
  Edwards, Bowen Baker, Teddy Lee, Jan Leike, John           haran, and Subbarao Kambhampati. 2023b. On the
  Schulman, Ilya Sutskever, and Karl Cobbe. 2024.            planning abilities of large language models – a criti-
  Let’s verify step by step. In International Conference     cal investigation. In Advances in Neural Information
  on Learning Representations (ICLR).                        Processing Systems (NeurIPS).
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler           Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V.
 Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,              Le, Ed H. Chi, Sharan Narang, Aakanksha Chowd-
 Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,               hery, and Denny Zhou. 2023. Self-consistency im-
 Shashank Gupta, Bodhisattwa Prasad Majumder,                proves chain of thought reasoning in language mod-
 Katherine Hermann, Sean Welleck, Amir Yazdan-               els. In International Conference on Learning Repre-
 bakhsh, and Peter Clark. 2023. Self-Refine: Iterative       sentations (ICLR).
 refinement with self-feedback. In Advances in Neu-
 ral Information Processing Systems (NeurIPS).             Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Bardia Mohammadi, Nearchos Potamitis, Lars Klein,             Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le,
  Akhil Arora, and Laurent Bindschaedler. 2026.               and Denny Zhou. 2022. Chain-of-thought prompt-
  Atomix: Timely, transactional tool use for reliable         ing elicits reasoning in large language models. In
  agentic workflows. Preprint, arXiv:2602.14849.             Advances in Neural Information Processing Systems
                                                             (NeurIPS).
NVIDIA. 2025.       Nemotron 3 Nano: Open,
 efficient mixture-of-experts hybrid Mamba–                Binfeng Xu, Zhiyuan Peng, Bowen Lei, Subhabrata
 Transformer model for agentic reasoning. Preprint,          Mukherjee, Yuchen Liu, and Dongkuan Xu. 2023.
 arXiv:2512.20848. Technical report.                         ReWOO: Decoupling reasoning from observations
                                                             for efficient augmented language models. Preprint,
Theo X. Olausson, Jeevana Priya Inala, Chenglong             arXiv:2305.18323.
  Wang, Jianfeng Gao, and Armando Solar-Lezama.
  2024. Is self-repair a silver bullet for code gener-     Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,
  ation? In International Conference on Learning             Thomas L. Griffiths, Yuan Cao, and Karthik
  Representations (ICLR).                                    Narasimhan. 2023a. Tree of thoughts: Deliberate
                                                             problem solving with large language models. In Ad-
OpenAI. 2025. gpt-oss-120b & gpt-oss-20b model card.         vances in Neural Information Processing Systems
  Preprint, arXiv:2508.10925.                                (NeurIPS).
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
  Shafran, Karthik Narasimhan, and Yuan Cao. 2023b.
  ReAct: Synergizing reasoning and acting in language
  models. In International Conference on Learning
  Representations (ICLR).
Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman,
  Haohan Wang, and Yu-Xiong Wang. 2024. Lan-
  guage agent tree search unifies reasoning, acting, and
  planning in language models. In International Con-
  ference on Machine Learning (ICML).
A   Per-environment success vs complexity               problems stratified across environment × complex-
    (curves)                                            ity, in JSONL format.
The main-text per-environment summary is the            Instance     schema. Each       row     carries:
table-form ∆ in Table 5. Figure 5 shows the             problem_id, environment, complexity, an
same data as a colour-coded heatmap, and Figure 6       explicit initial_state and goal_state (or
shows the underlying success-rate curves vs com-        goal predicate), an oracle_plan (action list,
plexity for gpt-5.4-mini-medium, the strongest          lower-bound length), the oracle_plan_length,
reasoning configuration.                                and a natural_language_prompt that the model
                                                        sees. Each environment supplies its own verifier
                                                        and goal predicate.

                                                        The controller. All methods (C OT, P OT, SC,
                                                        R E P OT) run through a common inference-time
                                                        controller (the Runner object). The controller me-
                                                        diates every interaction between the LLM and the
                                                        environment: it constructs the prompt, calls the
                                                        LLM, parses the output, then either submits the
                                                        entire plan to the environment (P OT, SC, C OT)
                                                        or steps actions one-at-a-time through the verifier
                                                        (R E P OT). This mirrors the pattern advocated by
                                                        Shojaee et al. (2025) and Scholten et al. (2024) of
Figure 5: ∆(RePoT−PoT) per environment, in per-
                                                        externalising state from the model’s hidden reason-
centage points, for all four models. Blocksworld is
R E P OT’s home environment (+5 to +17pp on every       ing into an authoritative simulator. The controller
model); Hanoi/Checker on strong models are saturated    logs:
by P OT at small N .
                                                           • the verbatim model prompt and completion
                                                             (prompt, output_text) for every LLM call;
B   Hyperparameters
                                                           • per-problem method metadata: number
C    Data generation and the controller                      of repair calls (repot_repair_calls),
     architecture                                            whether the initial P OT inside R E P OT
P UZZLE Z OO-775 (n = 775). Figure 7 shows                   succeeded (repot_initial_pot_success),
one example instance for each of the four classical          the verified-prefix length and total plan length,
planning environments we use, illustrated at small           the action where the first invalid transition
complexity. We generate problems with control-               was detected, and the verifier’s error message
lable complexity across Tower of Hanoi, Checker              at that boundary;
Jumping, River Crossing, and Blocksworld, in the
                                                           • end-to-end latency, prompt and completion
spirit of Shojaee et al. (2025). We do not redis-
                                                             token counts, and runtime exceptions if any
tribute Shojaee et al.’s instances; we generate fresh
                                                             (the runner_exception field, used to filter
problems following the same families and the same
                                                             poisoned runs as described in Appendix J).
controllable-complexity protocol.
   For each environment we generate problems              A failed LLM call (network, JSON parse, sand-
across a complexity range (e.g. Tower of Hanoi          box timeout) is recorded as a runner_exception
N ∈ [2, 14], Blocksworld N ∈ [3, 16] blocks). For       and the problem is treated as unsolved for that
every problem we additionally generate an oracle        method; we do not re-roll. The choice keeps the
plan from a domain solver (BFS for Hanoi/Checker,       per-method denominator stable across methods on
brute-force enumeration for small River Crossing,       the same problem.
FF-style stack reasoning for Blocksworld) and ver-
ify both that the oracle solves the instance and        Verifier semantics. The verifier is the environ-
that the instance is not trivially solved by greedy     ment’s transition function; for each proposed action
heuristics. Instances that fail either check are dis-   a at state s it returns (s′ , ok, ϵ): s′ is the next state,
carded. The released suite contains 775 verified        ok is a boolean validity flag, and ϵ is a one-line
Figure 6: Per-environment success rate vs problem complexity for gpt-5.4-mini-medium (thinking=medium).
Tower of Hanoi and Checker Jumping are nearly saturated by P OT at small N ; R E P OT’s lift concentrates on
Blocksworld and the mid-complexity dips of Checker and River.

           Hyperparameter                    Value                     Notes
           R E P OT
           Repair budget R                   1                         one suffix-repair call
           Verified-prefix tail T            4                         last 4 valid moves shown to model
           Sampling (all methods)
           Temperature                       0.0                       deterministic
           max_tokens (output)               16,384                    per LLM call
           Self-Consistency baseline
           k (samples)                       8                         majority vote on full plans
           Models
           gpt-5.4-mini-medium               reasoning=medium          OpenAI Responses API
           gpt-5.4-mini                      reasoning=none            OpenAI Responses API
           gemini-3.5-flash                  thinking_level=MEDIUM     Vertex AI
           gemini-3.5-flash (PlanBench)      thinking_level=NONE       no-thinking variant
           claude-sonnet-4.6                 no extended thinking      Anthropic API

Table 4: All hyperparameters used in this paper. Each row appears verbatim in our run configs; no tuning per-method
beyond what is listed. Defaults follow the public P UZZLE Z OO-775 config.


natural-language error message used by R E P OT’s           Environment        GPT (med) Gemini Claude GPT (mini)
repair prompt and by D ERAIL’s error_only con-              Blocksworld            +17.2     +10.4   +9.2        +5.2
dition. Goal achievement is checked by a problem-           Checker Jumping        +15.6      +0.0   -0.4        -1.3
                                                            River Crossing          +3.0     +24.0   +1.0        +9.0
specific is_goal predicate that accepts partial-goal        Tower of Hanoi          +0.5      +0.0   +0.0        +1.0
specifications (e.g. Blocksworld goal stacks need
not name every block).                                     Table 5: ∆(RePoT−PoT) per environment, in percent-
                                                           age points. Bold cells have |∆| ≥ 5pp. Blocksworld
Why an interactive controller is the right fram-           is RePoT’s home environment; Hanoi/Checker on the
ing. Shojaee et al. (2025)’s key empirical pat-            strongest models are saturated by PoT. Per-model think-
tern is that failures concentrate early in the trace,      ing config matches Table 1.
and the model spends the rest of the budget elab-
orating a wrong-but-consistent continuation. A
one-shot P OT setup makes this invisible: the only         D    Per-method, per-env, per-complexity
signal is a final pass/fail. A one-action-at-a-time             full table
controller exposes the failure boundary directly
(the first_failure_move_id, in their notation),            The full per-environment, per-complexity success
which is exactly what R E P OT’s verified-replay           rates for all 4 models × 5 methods on P UZZLE -
primitive depends on. The controller is therefore          Z OO-775 are released as part of the supplementary
not just a runtime convenience: it is the substrate        materials; the headline summary is in Table 1 and
that makes verified-prefix recovery well-defined.          the per-environment ∆ in Table 5.
Figure 7: One example per environment at small complexity. Each column is one environment (Tower of Hanoi,
Checker Jumping, River Crossing, Blocksworld); rows show initial state, an intermediate state after a few valid
actions, and the target state. Vertical arrows mark the per-step valid moves that the verifier accepts. Each environment
exposes a deterministic step function E.step(s, a) → (s′ , ok, ε) used by both the R EPLAY primitive (Eq. 1) and the
D ERAIL harness; complexity is controlled by the integer parameter named in column headers (# disks for Hanoi, #
blocks for Blocksworld, # checkers for Checker Jumping, # pairs for River Crossing).


 Model                     Seed    PoT    RePoT         ∆     E    Paired mechanism analysis
                           1       86.0      96.0   +10.0
                           2       85.0      94.0    +9.0    To isolate the verified-prefix mechanism from API
 gpt-5.4-mini-medium                                         sampling noise on trivial problems, we restrict
                           3       88.0      95.0    +7.0
                           mean    86.3      95.0    +8.7    to the matched-difficulty subset where both P OT-
                           1       79.0      88.0    +9.0    retry’s attempt-1 and R E P OT’s initial P OT call
                           2       81.0      88.0    +7.0    failed. On this subset we compare two strategies
 claude-sonnet-4.6
                           3       85.0      88.0    +3.0
                           mean    81.7      88.0    +6.3    that share the same matched budget: R E P OT’s
                           1       80.0      85.0    +5.0    verified-prefix suffix repair, and P OT-retry’s fresh
 gemini-3.5-flash
                           2       82.0      83.0    +1.0    independent sample. Table 7 reports the result
                           3       82.0      84.0    +2.0    and Fig. 8 shows the stacked-bar decomposition.
                           mean    81.3      84.0    +2.7
                                                             The pattern is heterogeneous: R E P OT recovers
Table 6: Multi-seed paired comparison (n = 100 strati-       +14.3pp more than fresh resampling on Gemini,
fied problems per seed, three seeds per model). R E P OT     is within noise on Claude, and loses on the two
− P OT is positive on every seed of every model.             GPT configurations. The pattern tracks capability
                                                             scaling (§6.4): R E P OT’s mechanism contribution
                                                             concentrates on configurations where the initial
                                                             P OT plan leaves a useful valid prefix, which is pre-
                                                             cisely the heterogeneity the adaptive policy (§4.4)
                                                             is designed to absorb.
Multi-seed raw numbers. Per-seed paired com-                  F    Multi-candidate “best-in-thought”
parisons of R E P OT vs P OT on the three reasoning-
                                                                   analysis
thinking-on configurations are reported in Table 6.
R E P OT − P OT is positive on every seed for all            We re-extract the highest-success candidate from
three configurations.                                        each P OT reasoning trace (Apple-paper proto-
 Model                 N    RePoT%    Retry%      ∆          than the initial P OT prompt (no examples, just
 GPT-5.4-mini (med)    23      60.9     73.9   −13.0         the verified-prefix tail and the verifier error),
 Gemini 3.5 Flash     112      17.9      3.6   +14.3         but the model spends additional reasoning on
 Claude Sonnet 4.6    103      12.6     13.6    −1.0
 GPT-5.4-mini         226       0.0      8.4    −8.4
                                                             resolving the failure boundary.

Table 7: Paired mechanism decomposition on prob-        Aggregated over all 100 problems, R E P OT aver-
lems where both P OT-retry’s attempt-1 and R E P OT’s   ages 1.06× P OT cost. Per-problem cost data is
initial P OT failed. RePoT% is R E P OT’s conditional   released alongside the trace files.
repair rate; Retry% the matched-budget fresh-sample
rate; ∆ = RePoT−Retry (pp).
                                                        Full per-method, per-model cost table. Aggre-
                                                        gated over all 775 closed-model traces, Table 8
                                                        reports mean and median prompt+completion to-
                                                        kens, mean LLM calls, and mean wall-clock per
                                                        problem for every (model, method) pair. R E P OT
                                                        and A DAPTIVE R E P OT average 1.11–1.39 LLM
                                                        calls per problem, matching the P OT-retry budget.

                                                        Cost vs accuracy Pareto. Figure 9 visualizes the
                                                        cost–accuracy trade-off mean-aggregated across
                                                        the four closed-model configurations.

Figure 8: Paired recovery decomposition on the
matched-difficulty subset (both methods’ initial P OT
failed). Stacks sum to 100% of N . “RePoT only” is
mechanism evidence; “PoT-retry only” is fresh-sample
evidence.


col) to defuse the “P OT baseline is weak” re-
view concern. On 100 stratified problems with
gpt-5.4-mini-medium: P OT final 89/100 vs P OT
best-in-thought 90/100 (a single problem). R E P OT
is unaffected: 93/100 on both protocols. The +4pp       Figure 9: Cost vs accuracy, mean across the four closed-
R E P OT −P OT delta is not an artifact of weak pars-   model configurations. P OT is the cost reference (1×).
ing.                                                    R E P OT achieves P OT-retry-class accuracy at essentially
                                                        the same mean cost (1.21×). SCk=8 ’s low mean reflects
G    Cost decomposition appendix                        its prose-plan format, which is more brittle than P OT’s
                                                        executable code.
We measured per-problem total token cost (prompt
+ completion) on gpt-5.4-mini-medium for the
100-problem stratified slice. The per-problem dis-
                                                        Recovery decomposition. Figure 10 decom-
tribution decomposes into two clean modes:
                                                        poses R E P OT’s wins into a second-attempt share
    • No-repair runs (86% of problems). R E -           (re-rolled P OT succeeds) and a mechanism share
      P OT’s verified replay confirmed the initial      (suffix repair rescues a doubly-failed P OT).
      P OT plan reaches the goal; cost is identical
      to P OT (n = 86, mean 1,820 tokens, median        H    P LAN B ENCH per-complexity
      1,540).
                                                        Figure 11 shows the per-complexity breakdown for
    • One-repair runs (14% of problems). The            all three PlanBench models. The complete cell-
      initial P OT plan failed; R E P OT issued one     level success rates (3 models × 10 complexities ×
      suffix-repair call. Per-problem cost is 1.4–      2 methods) are released as supplementary material.
      1.7× P OT (n = 14, mean 2,610 tokens, me-         The two negative-delta cells (gpt-5.4-mini at c =
      dian 2,180). The repair-call prompt is shorter    8 and c = 11, see Appendix J) appear in that file.
       Model                Method      Mean tokens (in/out) Median tokens (in/out) Mean calls Mean wall (s)
       GPT-5.4-mini (med) CoT                   193 / 13323             184 / 8212       1.00           93.1
                          SCk=8                 196 / 13277             184 / 7976       8.00           92.0
                          PoT                    216 / 4330             203 / 2294       1.00           29.9
                          PoT-retry              245 / 4788             203 / 2377       1.14           41.4
                          RePoT                  257 / 4297             205 / 2166       1.11           34.9
       Gemini 3.5 Flash     CoT                   155 / 961              142 / 321       1.00           19.2
                            SCk=8                 155 / 972              142 / 321       8.00           18.7
                            PoT                   210 / 497              197 / 510       1.00            6.5
                            PoT-retry             251 / 598              197 / 636       1.18            9.4
                            RePoT                 272 / 484              199 / 418       1.17            7.6
       Claude Sonnet 4.6    CoT                  182 / 2185             168 / 1422       1.00           27.0
                            SCk=8                182 / 2374             168 / 1511       8.00           29.4
                            PoT                   236 / 891              222 / 743       1.00           12.9
                            PoT-retry            274 / 1035              222 / 753       1.15           29.0
                            RePoT                 299 / 782              225 / 693       1.17           16.8
       GPT-5.4-mini         CoT                  197 / 1556              184 / 191       1.00            8.8
                            SCk=8                197 / 1209              184 / 191       8.00            6.9
                            PoT                   215 / 269              203 / 147       1.00            3.0
                            PoT-retry             302 / 357              209 / 273       1.39            7.3
                            RePoT                 424 / 288              211 / 240       1.39            3.9

Table 8: Per-method cost breakdown across the three frontier models in four configurations, aggregated over all
775 problems. Tokens are summed across all LLM calls for the problem. Mean calls counts each LLM invocation
(SC uses k = 8; R E P OT is 1+ repair calls; P OT-retry is 1 or 2). R E P OT and A DAPTIVE R E P OT average ∼1.1–1.4
LLM calls per problem, matching the P OT-retry budget. Wall-clock is end-to-end per problem.


I   Failure-mode case studies                                 actively harmful, but anchoring the repair on the
                                                              post-injection state appears to confuse the model
We hand-analyze the five problems where P OT                  in this controlled-error setting. The gap to non-
succeeded but R E P OT failed on the headline gpt-            checkpointed baselines (≥ 30pp on GPT (med),
5.4-mini-medium run (n = 100 slice). All five                 ≥ 60pp on Gemini) remains the load-bearing find-
share the same signature: R E P OT’s initial P OT call        ing. We hypothesise that the injected mid-rollout
returned an empty or non-goal-reaching plan, and              state is sometimes unreachable from the goal un-
the single repair call could not bridge the gap.              der a single repair call, while a fresh plan from s0
Taxonomy. PoT-call resampling loss (4/5): R E -               avoids that trap. Reporting as-is.
P OT’s initial P OT call returned an empty or un-
                                                              (ii) PlanBench gpt-5.4-mini at c = 8 and c = 11.
parseable plan while standalone P OT returned a
                                                              At these two complexities, R E P OT underperforms
goal-reaching plan — sampling variance, not a
                                                              P OT by −8.3pp and −9.1pp respectively. Both
mechanism weakness. Incomplete-plan stall (1/5):
                                                              points fall in the regime where P OT has very low
the initial P OT call emitted a 9-action plan that re-
                                                              base accuracy (33% and 18%) and the mid-rollout
played cleanly but did not reach the goal; the repair
                                                              state R E P OT resumes from is itself misleading.
call could not extend it within T = 4 — a genuine
                                                              The single repair call sometimes commits to ex-
single-call repair failure.
                                                              tending a bad prefix. A higher repair budget, or
                                                              a verifier-driven decision to restart from s0 when
J   Negative findings
                                                              the prefix-fraction is low, would mitigate; we treat
We report two findings that complicate the headline           both as future work and report the negative cells
narrative. We include them rather than buried them.           transparently.

(i) D ERAIL prefix-flip. On both Gemini and                   K Algorithm: full code listings and repair
GPT (med), R E P OT restart beats R E P OT full (82.4           prompt
vs 80.7 on Gemini; 94.5 vs 59.6 on GPT (med)
— a much larger gap than on Gemini). The in-                  The R E P OT agent’s run() method, the
equality R E P OT full >R E P OT no-prefix does hold          replay_until_failure()      primitive,     and
on both (+3.8 / +5.8pp), so the prefix tail is not            the code_prompt() repair template are released
Figure 10: Decomposition of R E P OT’s recovery on P UZZLE Z OO-775. Each row is one model; bars sum to 100%.
The teal segment is the share of problems where standalone P OT fails, R E P OT’s first P OT call also fails, and the
suffix repair call rescues (mechanism). The coral segment is the second-attempt contribution (standalone P OT fails
but R E P OT’s re-rolled P OT call succeeds without invoking the repair). On the strongest model most of R E P OT’s lift
is second-attempt; the verified-prefix repair contributes the harder tail. The matched-budget P OT-retry comparison
in Table 1 isolates the mechanism contribution under equal LLM-call budget.


alongside the paper. The full implementation is               no_feedback. The model sees the post-injection
approximately ∼25 lines for run(), ∼25 for the                    state only; no error message, no checkpoint
replay primitive, and ∼60 for the prompt; see the                 marker.
released source for verbatim listings. Figure 12
below shows the verified-prefix-conditioned repair            error_only. The model sees the post-injection
prompt template.                                                  state and a one-line verifier error; no check-
                                                                  point visualization.
L    Ablation conditions
The three named ablations referenced in §4.5 and              state_feedback. The model sees the last valid
used in §7:                                                       checkpoint state plus the wrong action that
                                                                  was attempted.
R E P OT full the algorithm of Algorithm 1.

R E P OT no-prefix same as full, but the dynamic-             state_plus_legal_actions. As above, plus the
     block prefix-tail and “|P| verified moves”                   legal action set from the checkpoint.
     counter are hidden; the model sees only the
     current verified state and the error message.            stateguard_rollback. A controller-based roll-
     Tests whether the prefix tail is what the model              back baseline: the controller proposes one
     uses, not just the checkpoint state.                         action at a time, the verifier accepts or rejects,
R E P OT restart same budget, but the repair call                 repeat until budget exhaustion.
     restarts from s0 instead of the verified state s.
     Tests whether the gain is the verified check-            R E P OT variants. Three   R E P OT  condi-
     point or just an extra LLM call.                              tions (repot_full,    repot_no_prefix,
                                                                   repot_restart) matching App. L.
M     D ERAIL condition definitions
D ERAIL measures recovery from one injected                      All conditions share the same per-problem injec-
wrong action at a ∼1/3 checkpoint of the oracle               tion seed; comparisons are paired across conditions
plan. We compare 11 conditions:                               on the same problem.
Figure 11: Per-complexity success rate on P LAN B ENCH B LOCKSWORLD. R E P OT’s lift concentrates in the
mid-complexity band where P OT has both failures to recover from and enough valid prefix to recover into. Two
negative-delta cells (gpt-5.4-mini at c = 8, 11) are reported in Appendix J.


Stable block (cacheable):                               (empty plan): the model emits an empty or near-
{problem.natural_language_prompt}
Goal state: {goal_state}
                                                        empty plan when it cannot solve, and the suffix-
Write Python code that prints exactly one line:         repair branch activates on only 1–3 problems out
moves = [...]                                           of 120. This is a different mechanism profile than
containing up to K primitive moves to apply
from the current verified state.                        closed thinking-on models, where suffix repair is
— verifier checkpoint below —                           the dominant value channel. Nemotron-3 Nano
Dynamic block:                                          30B FP8 routes mostly to short-prefix retries with
You have already executed |P| verified moves.           a low rescue rate (3%), confirming the capability-
Recent verified moves: {tail_T(P)}
Current verified state: {s}                             floor reading.
Legal moves: {legal_actions(s)}
Blocked: {blocked(s)}                                   Open-source cost. Mean total tokens per prob-
Verifier message: {ϵ}                                   lem (prompt + completion) under R E P OT are 1.5–
                                                        2× P OT on Gemma, GPT-OSS, and Qwen, in line
Figure 12: Verified-prefix-conditioned repair prompt.
                                                        with the 1.06–1.4× closed-model range. Wall-
The “verifier checkpoint” marker delimits the
cacheable problem description from the per-call dy-     clock per problem: P OT 25–60 s, R E P OT 40–110 s.
namic state.                                            Detailed per-method, per-model numbers are re-
                                                        leased alongside the trace files.

N    Open-source results: routing, cost, and            Capability scaling regression. The R E P OT
                                                        −P OT-retry success-rate delta regressed on the
     capability scaling
                                                        mean verified-prefix fraction of failed initial P OT
This appendix expands on §6.4 with the adaptive         plans across all (model, environment) cells appears
policy routing breakdown, per-model cost statis-        in Fig. 3 (§6.4).
tics, and the capability-scaling regression. Per-
model success rates for the five core methods are       O    Release
in the bottom block of Table 1; the A DAPTIVE R E -     Code is available at https://github.com/
P OT success rates are 60.0% (Gemma 4 26B-A4B),         parsa-mz/RePot (Apache-2.0): the R E P OT and
64.2% (GPT-OSS 20B), 62.5% (Qwen 3.6 35B-               A DAPTIVE R E P OT agents, the verified-replay
A3B), and 13.3% (Nemotron-3 Nano 30B FP8) on            primitive, the four environments, the D ERAIL har-
the same 120-problem stratified subset.                 ness, prompt templates, and a CLI with three sub-
                                                        commands (repot run / derail / judge). P UZ -
Adaptive policy routing. Figure 13 shows the            ZLE Z OO-775 and D ERAIL-550 ship under CC-BY-
routing distribution of A DAPTIVE R E P OT across       4.0; trace files are not redistributed but reproduce
the four open-source models. On the three work-         from the same CLI.
able models (Gemma, GPT-OSS, Qwen) about half
of problems trigger the initial PoT success branch
and most of the remainder route to fresh retry
Figure 13: Adaptive policy routing per open-source model. Bars sum to 120 problems. The three workable rows are
dominated by initial PoT success + fresh retry (empty plan); suffix repair is rare. Nemotron-3 (bottom) shows a
markedly different shape: few initial successes, many short-prefix retries.
