                                                                        VERITAS: Verifier-Guided Proof Search
                                                                        for Zero-Shot Formal Theorem Proving


                                                    Manish Acharya 1 Zhenyu Liao 2 Yueke Zhang 1 Kevin Leach 1 Yu Huang 1 Yifan Zhang 1


                                                                  Abstract                                    explore the combinatorial space of partial proofs (Kocsis &
                                                                                                              Szepesvári, 2006; Silver et al., 2018; Lample et al., 2022;
                                              LLM-based formal provers often collapse rich
                                                                                                              Google DeepMind, 2024). Most modern systems combine
arXiv:2606.19399v1 [cs.LG] 17 Jun 2026




                                              verifier signals (syntax errors, type mismatches,
                                                                                                              the two: an LLM proposes, search disposes.
                                              partial goal progress) into a binary pass/fail bit.
                                              We present VERITAS, a zero-shot framework                       What is striking about this combination is how thinly the
                                              that routes every verifier signal back into proof               two components communicate. In a typical pipeline, the LM
                                              search through a two-phase protocol: Best-of-N                  emits a batch of candidate tactics, the verifier checks each
                                              sampling first, then a critic-guided MCTS pass                  one, and the search algorithm updates value estimates from
                                              that ingests Phase 1 failures as explicit negative              the resulting pass-or-fail outcomes. Anything richer that
                                              examples. The protocol preserves every theorem                  the verifier produces along the way (a parse error pointing
                                              solved by its own Phase 1 sweep, so Phase 2’s                   at a malformed token, a type mismatch naming the offend-
                                              additional solves are attributable to feedback-                 ing hypothesis, a partial goal that has been simplified but
                                              driven exploration. VERITAS reaches 40.6% on                    not closed) is summarised into a scalar reward or thrown
                                              miniF2F (vs. an independently run Best-of-5 at                  away entirely. Yet these intermediate signals are exactly the
                                              36.9%, Portfolio 26.2%) and 7.3% on VERITAS-                    artefacts a human prover attends to: collapsing them into a
                                              CombiBench, a 55-theorem combinatorics bench-                   single bit forces the search to relearn what the verifier has
                                              mark we release on which Best-of-5 (1.8%) falls                 already told it explicitly. The cost is most visible on proofs
                                              below Portfolio (3.6%), exposing that unguided                  that require a chain of dependent tactics, where each step’s
                                              sampling hurts when correct lemma names must                    correctness hinges on the previous step’s effect on the goal.
                                              be recovered iteratively from verifier feedback.                Recent rich-feedback methods in RL (Hübotter et al., 2026)
                                              Artifacts are available on GitHub.                              make the same observation in the post-training regime; we
                                                                                                              explore the dual at inference time.
                                                                                                              We present VERITAS, a zero-shot framework built around
                                         1. Introduction
                                                                                                              a single design commitment: the verifier’s structured feed-
                                         Formal theorem proving, the construction of machine-                 back should reach every generation decision. We factor
                                         checkable proofs in interactive proof assistants such as Lean,       proof search into four specialised agents sharing a unified
                                         Coq, and Isabelle, has become a flagship benchmark for eval-         proof state. A Strategist chooses a high-level approach
                                         uating AI systems on multi-step formal thought, because              (direct computation, induction, rewriting, contradiction)
                                         success admits a crisp definition: a candidate proof is ei-          before any tactics are emitted, narrowing the search to a
                                         ther accepted by the verifier or it is not. This property has        strategy-relevant subspace. A Tactician (Claude Sonnet)
                                         driven a steady stream of progress, pushing solve rates on           proposes tactic candidates conditioned on the current goal,
                                         miniF2F (Zheng et al., 2022) from below 30% to above                 retrieved Mathlib premises, and crucially the explicit list of
                                         80% (Polu & Sutskever, 2020; Yang et al., 2023; Wu et al.,           tactics that have already failed earlier in the search, with
                                         2024b; Ren et al., 2025). Two complementary families drive           their Lean error messages attached as negative examples.
                                         this progress: language models that generate candidate tac-          A Critic (Claude Haiku) scores partial proof states, replac-
                                         tics (Polu & Sutskever, 2020; Han et al., 2022; Yang et al.,         ing MCTS’s random rollouts with a value estimate that
                                         2023; Azerbayev et al., 2024), and tree-search methods that          integrates Lean’s four-way feedback signal. A Retriever
                                            1
                                                                                                              grounds generation in Mathlib by surfacing relevant lemmas.
                                              Department of Computer Science, Vanderbilt University,          These agents are coordinated by a deliberately conservative
                                         Nashville, TN, USA 2 Amazon, Seattle, WA, USA. Correspon-
                                         dence to: Yifan Zhang <yifan.zhang.2@vanderbilt.edu>.                two-phase protocol: Phase 1 is identical to a Best-of-N
                                                                                                              sweep, and Critic-guided MCTS in Phase 2 runs only on
                                         Accepted at the 3rd AI for Math Workshop (AI4Math), ICML 2026,       theorems Phase 1 failed. This yields a monotonicity guaran-
                                         Seoul, South Korea. Workshop proceedings are non-archival.

                                                                                                          1
                        VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

tee: VERITAS preserves every theorem solved by its own                  the hypothesis set, τ1:t the tactic history, and the four σ
Phase 1 attempts. The reported Best-of-5 baseline is an                 values are Lean’s structured signals: σA syntax validity, σB
independent stochastic run, so its overlap with VERITAS                 type correctness, σC goal progress (e.g. subgoal reduction),
need not be a subset; within a VERITAS run, however, ev-                and σD proof completion (no remaining goals or sorry).
ery Phase 2-only solve is attributable to MCTS with verifier            Every agent’s output conditions the next agent’s input within
feedback. A batched Lean validation trick further cuts per-             an iteration.
expansion verification from O(K) to O(1) proof-checker
invocations.                                                            Agents. The Strategist maps a proof state to one
                                                                        of six high-level strategies (direct, induction,
Across two Lean 4 benchmarks the experiments give a con-
                                                                        contradiction, cases, rewrite, apply_lemma)
sistent picture: tightly coupling the verifier with genera-
                                                                        together with a depth estimate, restricting subsequent search
tion matters more than scaling either component alone. On
                                                                        to a strategy-relevant subspace. The Tactician (Claude Son-
miniF2F, VERITAS reaches 40.6% (99/244), above Best-
                                                                        net 4.6, temperature 0.8) generates K tactic candidates con-
of-5 Claude (36.9%) and a handcrafted Portfolio (26.2%);
                                                                        ditioned on the strategy, retrieved premises, Critic guidance,
a phase-wise decomposition identifies 11 theorems no
                                                                        and crucially the failure set F of tactics rejected earlier (in-
flat-sampling budget can reach. The picture sharpens on
                                                                        jected into the system prompt as negative examples). The
VERITAS-CombiBench: there, Best-of-5 (1.8%) falls be-
                                                                        Critic (Claude Haiku 4.5, temperature 0.3) returns a value
low the Portfolio (3.6%) because unguided sampling hallu-
                                                                        V (s) ∈ [0, 1], suggested next tactics, and a pruning recom-
cinates Mathlib lemma names Lean rejects on sight, while
                                                                        mendation, providing low-latency guidance for selection.
VERITAS reaches 7.3% by correcting those names itera-
                                                                        The Retriever surfaces the top k=5 Mathlib premises by
tively from Lean’s errors. We read these results as evidence
                                                                        weighted keyword overlap over goal tokens, lemma names,
for a general design principle: when a deterministic verifier
                                                                        and statement signatures (matching type names such as
emits structured intermediate signals, folding them back
                                                                        Nat/Finset, operators +, ∗, ≤, and connectives ∧, ∨); re-
into generation amplifies the LLM substantially more than
                                                                        sults are appended to the Tactician’s prompt and passed to
additional sampling does.
                                                                        the Critic as context.

Contributions. (i) A zero-shot four-agent framework that                2.1. Critic-Guided MCTS
routes Lean’s structured feedback (syntax/type/progress/-
completion) into every generation decision; (ii) a two-phase            Selection. We extend standard UCB with Critic value and
Best-of-N → Critic-MCTS protocol with an internal mono-                 strategy
                                                                         p        alignment, scoring an action a at state s as Q(s, a)+
tonicity guarantee that isolates the search contribution; (iii) a       c ln N (s)/N (s, a) + wv Vcritic (s′ ) + ws align(a, π), where
batched Lean validation trick that reduces verification cost            align(a, π) ∈ {0, 1} equals 1 iff the leading token of a be-
by 10×; (iv) VERITAS-CombiBench, a benchmark of 55                      longs to the strategy-specific tactic vocabulary Vπ (e.g.,
hard, author-verified Lean 4 combinatorics theorems we re-              Vinduction = {induction, cases, rcases}), biasing se-
lease; and (v) a phase-wise attribution showing 11 miniF2F              lection toward strategy-aligned subtrees. Expansion runs the
theorems uniquely solvable by MCTS, plus a failure-mode                 four agents in sequence (Strategist → Retriever → Critic
taxonomy that locates the next frontier for verifier-in-the-            → Tactician), validates all K generated candidates in a
loop search.                                                            single batched Lean call (Section 2.3), and creates child
                                                                        nodes for the syntactically valid ones. Simulation replaces
                                                                        random rollouts with the Critic’s value augmented by the
2. The VERITAS Framework                                                structured signals, V (s) = Vcritic (s) + α1 σA + α2 σB +
VERITAS coordinates four specialized agents (Strategist,                α3 σC + β/(1+N (s)), with α1 =α2 =0.1 and α3 =0.2 as-
Tactician, Critic, and Retriever) through a shared proof state          signing increasing weight to increasingly informative sig-
and a Critic-guided MCTS loop, with all agents observing                nals (goal progress is the strongest intermediate signal short
the same structured verification signals from Lean. Figure 1            of completion) and β=0.1 providing an exploration bonus
shows the full pipeline and Algorithm 1 gives the protocol              that decays with visit count. Backpropagation carries the
in pseudo-code. The division of labor separates strategic               structured A–B–C–D signal upward rather than collapsing
choice, tactic synthesis, state valuation, and premise re-              to binary win/loss; this preserves credit for partial-progress
trieval while keeping all roles grounded in the same verifier           states (σC ) that would otherwise be pruned: the critical case
state.                                                                  for multi-step theorems.

                                                                        2.2. Two-Phase Design and Monotonicity Guarantee
Proof state and verifier signals. All agents operate on a
shared ProofState s = (T , g, H, τ1:t , σA , σB , σC , σD ),            Phase 1 (Best-of-N sweep) generates N tactics in one
where T is the theorem statement, g the current goal, H                 Claude API call and validates them in one batched Lean

                                                                    2
                        VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

Algorithm 1 VERITAS Two-Phase Search                                      speedup at K=6 and approaching 20× at K=16 where
Require: Theorems T ; budgets N (Best-of-N ), I (MCTS), K                 Lean’s per-file overhead dominates.
    (candidates per node)
 1: S1 , S2 ← ∅                               // Phase 1: Best-of-N
 2: for T ∈ T do                                                          3. Experiments
 3:    {τi }N1 ← Claude(T ); (ok, err) ← L EAN BATCH (T, {τi })
 4:    if ∃i : ok[i] then                                                 We evaluate whether verifier feedback improves zero-shot
 5:       S1 ← S1 ∪ {T }                                                  proof search under realistic inference budgets. The section
 6:    else                                                               first reports aggregate solve rates, then decomposes where
 7:       FT ← {(τi , err[i])}N i=1                                       the gains come from by benchmark family, search phase,
 8:    end if                                                             compute budget, and deepest verifier signal.
 9: end for
10:                                 // Phase 2: Critic-guided MCTS
11: for T ∈ T \ S1 do                                                     3.1. Setup
12:    Init root s0 from T with cache FT
13:    for i = 1, . . . , I do                                            Benchmarks. miniF2F (Zheng et al., 2022): 244 competi-
14:       Select leaf s via UCB-with-Critic score; run Strate-            tion mathematics theorems (AIME, AMC, IMO, MATH) in
          gist/Retriever/Critic                                           Lean 4 with Mathlib. The test split contains 201 “hard” prob-
15:       {τk }K 1 ← Tactician(s, FT ); (ok, err) ← L EAN BATCH           lems and 43 problems annotated with sorry. VERITAS-
16:       Expand valid children; append errors to FT ; backpropa-
          gate V (s)                                                      CombiBench: a benchmark of 55 verified-solvable com-
17:       if any child closes T then                                      binatorics problems in Lean 4, sourced from IMO short-
18:           S2 ← S2 ∪ {T }; break                                       lists (22), the Brualdi Introductory Combinatorics text-
19:       end if                                                          book (29), and online repositories (4). All 55 have author-
20:    end for                                                            confirmed Lean 4 proofs (no sorry), released under CC-
21: end for
22: return S = S1 ∪ S2                                                    BY 4.0.

call; if any succeeds, return immediately. Phase 2 (Critic-               Methods. We evaluate four methods spanning a 2×2 abla-
guided MCTS) activates only if Phase 1 fails, with the                    tion on LLM × MCTS: Portfolio (36 handcrafted tactics in
Phase 1 failure set F injected into the Tactician’s system                one batched call, no LLM, no search); Best-of-1 and Best-
prompt.                                                                   of-5 Claude (1 or 5 tactics from Claude Sonnet, no search);
                                                                          VERITAS Two-Phase (Phase 1 Best-of-5 + Phase 2 Critic-
Proposition 2.1 (Monotonicity). For any fixed VERITAS                     guided MCTS, 50 iterations × 6 candidates per node).
run on problem set T and Phase 1 budget N , the final                     Two further ablations on the 201-problem miniF2F sub-
VERITAS solve set is a superset of that run’s own Phase 1                 set isolate component contributions: VERITAS-Heuristic
solve set: S(T ) ⊇ S1 (T ).                                               (MCTS with rule-based agents, no LLM) and VERITAS-
                                                                          MCTSonly (Phase 2 without the Phase 1 sweep).
Proof. If VERITAS’s Phase 1 solves a theorem, that proof
is immediately kept and Phase 2 is never invoked for that                 Hyperparameters and infrastructure. c=1.4, wv =0.6,
theorem. If Phase 1 fails, Phase 2 may or may not succeed,                ws =0.2, β=0.1, max depth 10.              Time budgets:
but it cannot remove a theorem already in S1 .                            300s (miniF2F), 600s (VERITAS-CombiBench). All
                                                                          proofs verified via lake env lean -json against
This guarantee is an internal attribution property: every the-            Lean 4 (de Moura & Ullrich, 2021) and Mathlib (The
orem in S2 is a Phase 2 contribution. It does not imply that              mathlib Community, 2020) with pre-built .olean files
a separately sampled Best-of-5 baseline must be a subset of               (1–5s per theorem after warmup). All experiments are
VERITAS, because the baseline is an independent stochastic                single-run, consistent with standard practice in inference-
run.                                                                      only Lean theorem proving where stochasticity arises only
                                                                          from Claude’s temperature sampling and per-run cost is
2.3. Batched Lean Validation                                              prohibitive (∼$150–200 per benchmark sweep). 95% confi-
                                                                          dence intervals throughout use the Wilson score interval for
Rather than invoking Lean separately for each of K can-                   binomial proportions.
didates, we compile them into one .lean file as pri-
vate theorems with distinct names (private theorem
                                                                          3.2. Main Results: LLMs and Guided Search Are Both
_p0 ... := by <tactic_0>, etc.) and run a sin-
                                                                               Necessary
gle lake env lean -json call. Successful tactics are
identified by the absence of errors on their line ranges. This            Table 1 (and Figure 2) report our main results. On miniF2F,
reduces validation cost from O(K) to O(1) Lean calls per                  VERITAS Two-Phase achieves 40.6% (99/244), outper-
MCTS expansion, yielding approximately 10× wall-clock                     forming Best-of-5 by +3.7pp, Best-of-1 by +11.5pp, and

                                                                      3
                      VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving




Figure 1. VERITAS two-phase protocol. Phase 1: Best-of-N dispatch; failures feed corpus F1 . Phase 2: Critic-guided MCTS on U1
with Lean signals σA –σD ; final S = S1 ∪ S2 satisfies S ⊇ S1 .


Portfolio by +14.4pp. Because the Best-of-5 comparison is                        (a) Main results                               (b) Category deltas
                                                                     Portfolio              26.2%                         60%
an independent stochastic run, we treat this gap as descrip-




                                                                                                         Solve rate (%)
tive and report paired attribution separately.                       Best-of-1                29.1%                       40%
The two single-component ablations close the 2×2 grid.               Best-of-5                   36.9%
                                                                                                                          20%
MCTS without LLM: VERITAS-Heuristic (12.4%) is worse
                                                                     VERITAS                         40.6%
than Portfolio (26.2%) despite using 218× more Lean calls;                                                                0%
all 25 problems it solves are a strict subset of Portfolio’s.                0% 10%20%30%40%50%                                 Bo5                 VERITAS
Phase 2 without Phase 1: VERITAS-MCTSonly (19.4%)                                   Solve rate (%)                                    Alg. +4   AIME +0
                                                                                                                                      Num. +4   IMO -5
underperforms Best-of-5 (25.8% on the 201-set) because                                                                                AMC +2    Other +20
it expends MCTS budget on easy problems flat sampling
                                                                    Figure 2. Main results on miniF2F. (a) Solve rates with 95%
solves trivially. Together these confirm that LLM and search        Wilson CIs; dashed line: ReProver (26.5%). (b) Per-category Best-
contributions are synergistic, and the two-phase design en-         of-5→VERITAS deltas (see Table 1).
sures Phase 1 handles easy theorems efficiently while leav-
ing Phase 2’s full budget for the hard ones.
                                                                    negative examples and partial goals into high-value states.
This also clarifies the monotonicity claim. The full sys-           All four successes are Brualdi problems (4/29); Portfolio
tem improves by +3.7 pp over the independent Best-of-5              (6.9%) still beats Best-of-5 (3.4%) on that subset.
baseline, while Proposition 2.1 guarantees the narrower in-
ternal property that VERITAS preserves its own Phase 1              Flat Best-of-N spends all computation at the root, so an
solves. The result is therefore not merely “more search”: it        unknown constant or type mismatch is discarded af-
is the structured pass through Best-of-N first, followed by         ter failure; VERITAS spends computation where Lean has
verifier-guided expansion only where Phase 1 fails.                 already revealed structure, downweighting tactic families
                                                                    that repeatedly produce σA errors.
3.3. VERITAS-CombiBench: When LLM Sampling
     Actively Hurts                                                 3.4. MCTS Adds Most Value for Multi-Step Inductive
                                                                         Problems
Portfolio (3.6%) outperforms both Best-of-1 and Best-of-5
(1.8% each): more LLM samples make things worse.                    Figure 2(b) visualises the per-category Best-of-5 → VERI-
Combinatorics in Lean 4 requires exact Mathlib names                TAS deltas using the numbers in Table 1. MCTS adds largest
(Nat.choose_symm, Finset.card_powerset);                            gains on algebra (+4.5pp) and “other” (+20pp), consistent
flat LLM prompts hallucinate lexically wrong names                  with our hypothesis that iterative Lean feedback most helps
(σA = 0), while Portfolio’s norm_num/omega cover a                  when the proof requires a sequence of dependent tactics.
valid slice. VERITAS reaches 7.3% (4/55) by feeding Lean            VERITAS drops by 5.2pp on IMO relative to Best-of-5: at
errors back into the Tactician. Flat Best-of-N discards             competition-creativity scale, the MCTS budget (50 × 6) is
failures at the root; VERITAS turns failed names into               insufficient, and stochastic generation can let Phase 1 find a
                                                                    proof Phase 2 fails to rediscover.

                                                                4
                                 VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

Table 1. Main zero-shot results. Solve rates on miniF2F (per-category and total) and VERITAS-CombiBench, with inference budget per
theorem. Bold = best within the zero-shot regime. Best-of-1 shares Best-of-N’s per-category breakdown (subsumed at N =1); the ablation
rows are evaluated on the 201-problem hard miniF2F subset (sorry-annotated theorems excluded). Counts in parentheses are solved/total.
Cost approximated from Anthropic API list prices for the full miniF2F run.

                                                                   miniF2F per category (%)                      miniF2F combiB        Inference cost
       Method                                           Alg. NumT. AMC AIME IMO Other                             Total     Total     Lean/thm API ($)
                                                        n=88           67          45         15    19      10     244        55                        total

       Portfolio (heuristic)                            30.7        46.3      11.1           6.7   0.0     0.0    26.2       3.6             1          <1
       Best-of-1 Sonnet                                             subsumed by Best-of-N at N =1                 29.1       1.8             1            7
       Best-of-5 Sonnet                                 53.4        44.8      17.8          13.3 10.5     10.0    36.9       1.8             5           35
       VERITAS Two-Phase                                57.9        49.3      20.0          13.3 5.3      30.0    40.6       7.3            27          150
       Component ablations on 201-problem hard miniF2F subset
       VERITAS-Heuristic (no LLM)                MCTS without any LM guidance                                     12.4        —            218          <1
       VERITAS-MCTSonly (no Phase 1)            MCTS without the Best-of-N sweep                                  19.4        —             60          60


           (a) Phase attr.                         (b) Easy/hard                             Table 2. Solve attribution on the 201 hard miniF2F theorems.
                                                                        65                   VERITAS uniquely contributes 11 solves (+5.5pp) not found by
                                             Port. 19
     Bo5           47              +5 52                                                     the independent Best-of-5 baseline or by 5× more flat samples
                                             Bo1 22                          81              (N =25, separately verified, finds none of the 11).
                                              Bo5 26                          88
 VERITAS           47             +11    58                                                              Outcome set                Count % of 201
                                          VERITAS 29                              95
                                                                                                         Solved by both               47         23.4
           0     20        40       60                  20 40 60 80 100
                                                         Solve rate (%)
                                                                                                         Best-of-5 only (indep.)       5
                                                                                                                                      11
                                                                                                                                                  2.5
                                                                                                                                                  5.5
               Solved (of 201 hard)                                                                      VERITAS only
                                                                                                         Unsolved by either          138         68.7
                  Shared   Bo5   MCTS                       Hard     Easy
                                                                                                         Best-of-5 reference          52         25.9
                                                                                                         VERITAS Two-Phase            58         28.9
Figure 3. Phase attribution and difficulty split. (a) Solved
theorems on 201 hard problems (47 shared; orange: 11 VERITAS-
only; blue: 5 Best-of-5-only). (b) Easy (sorry, n=43) vs. hard
(non-sorry, n=201) solve rates by method.
                                                                                             nal Phase 1. In contrast, the 11 VERITAS-only solves clus-
                                                                                             ter among theorems with visible intermediate state changes:
Difficulty stratification. The 43 sorry-annotated prob-                                      after a first tactic simplifies hypotheses, the next useful tactic
lems are uniformly easier: Portfolio solves 65.1%, Best-                                     depends on the new goal.
of-5 solves 88.4%, VERITAS solves 95.3%. On the 201
non-sorry problems the rates are 18.9%, 25.9%, and 28.9%,                                    3.6. Sample Efficiency vs. Verification Budget
confirming that VERITAS’s largest gains are on hard prob-
lems.                                                                                        Figure 4(a) plots solve rate against verification budget,
                                                                                             and Table 3 gives the precise compute numbers. Among
                                                                                             inference-only methods, VERITAS dominates the frontier:
3.5. Phase 2 MCTS Reaches Theorems Beyond Flat
                                                                                             it converts ∼6,500 Lean calls (27/theorem) into 40.6%
     Sampling
                                                                                             solve rate at ∼$150 API spend, which Best-of-5 cannot
Table 2 attributes each of the 201 hard miniF2F theorems                                     reach within 5× the Lean budget, and which VERITAS-
to the method that solved it. The independent Best-of-5                                      MCTSonly fails to approach even with 10× the LLM-free
baseline and VERITAS share 47 solves; the baseline alone                                     MCTS budget. The marginal-solve column quantifies the
solves 5 more due to sampling variation; VERITAS uniquely                                    trade-off: each method’s solves beyond Portfolio per 1k
solves 11 additional theorems (5.5% of 201).                                                 extra Lean calls.
The 11 MCTS-unique theorems each require 2–4 dependent                                       The compute curve also explains why the gain is modest in
tactics where each step depends on the previous step’s effect                                absolute percentage points despite being consistent. VER-
on the goal. Flat sampling cannot generate the complete se-                                  ITAS spends most of its extra calls on the hard tail, af-
quence by chance, but iterative Lean feedback allows MCTS                                    ter Best-of-5 has already solved many one-step theorems.
to discover it incrementally (∼47 Lean calls on average).                                    The resulting marginal return is lower than the jump from
The five Best-of-5-only solves are also informative. They                                    Best-of-1 to Best-of-5, but qualitatively different: additional
are not a violation of monotonicity, because the baseline is                                 sampling buys independent attempts, while Phase 2 buys
an independent stochastic run rather than VERITAS’s inter-                                   dependent proof continuations (Figure 4(a)).

                                                                                        5
                                         VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

Table 3. Inference budget per method. Lean calls per theorem,                                  5. Related Work
API cost (Anthropic list prices), and marginal solves over Portfolio
per 1k extra Lean calls. † : 201 hard subset.                                                  VERITAS combines LLM proof generation, proof-state
                                                                                               search, and verifier feedback. Prior systems rarely feed
                      Method           Lean/thm Cost ($) Solve %                    ∆/k
                                                                                               structured errors into each generation.
                      Portfolio                    1              <1         26.2 (ref.)
                      Best-of-1                    1                7        29.1    —
                      Best-of-5                    5               35        36.9 26.6         LLM-based theorem proving. GPT-f (Polu & Sutskever,
                      VERITAS                     27              150        40.6 5.5          2020), PACT (Han et al., 2022), and ReProver (Yang et al.,
                      V-Heur.†                  218               <1         12.4     —        2023) established tactic generation and retrieval. Trace-
                      V-MCTSonly†                60               60         19.4    0.2       trained systems, including InternLM-StepProver (Wu et al.,
                                                                                               2024b), Goedel-Prover (Lin et al., 2025), DeepSeek-Prover-
                                                                                               V2 (Ren et al., 2025), Llemma (Azerbayev et al., 2024),
                      (a) Efficiency                              (b) Failure modes            LEGO-Prover (Wang et al., 2024), and Baldur (First et al.,
                                    Pareto frontier
                                    Portfolio Complete ( D )
                                    Bo1
                                                                             99 (41%)          2023), explore fine-tuning, pretraining, lemma libraries, and
                 40                 Bo5
Solve rate (%)




                                    V-Heur.
                                    V-MCTS          Syntax ( A)          78 (32%)              repair. They are not direct zero-shot baselines, but they
                                    VERITAS
                 30                               Type ( B)        41 (17%)                    motivate the same question VERITAS asks at inference
                 20                            Progress ( C)    24 (10%)                       time: how much of the proof assistant’s dense signal can be
                                                                                               used before trace training?
                                                      Other 2 (1%)
                 10
                         103 104 105 106                          0     25 50 75 100
                          Lean calls (log)                              Theorems (/244)        Tree search and execution feedback. Our loop builds
                                                                                               on UCB/UCT (Auer et al., 2002; Kocsis & Szepesvári,
Figure 4. Compute efficiency and failure modes. (a) Solve rate                                 2006) and AlphaZero (Silver et al., 2018). HyperTree Proof
vs. total Lean calls (log); VERITAS on the inference-only Pareto                               Search (Lample et al., 2022), Thor (Jiang et al., 2022), and
frontier. (b) Deepest verifier signal at termination; 24 σC near-
misses (10%).                                                                                  DeepSeek-Prover-V1.5 (Xin et al., 2025) combine search
                                                                                               with proof-assistant feedback; COPRA (Thakur et al., 2024)
                                                                                               is the closest inference-only method. VERITAS differs
3.7. Failure-mode Analysis Locates the Next Frontier                                           by role decomposition, Critic-guided MCTS, monotonic
                                                                                               two-phase routing, and injecting failed tactic text plus Lean
Stratifying the 244 theorems by deepest verifier signal (Fig-
                                                                                               errors into generation rather than using outcomes only as
ure 4(b)): 99 proofs (σD =1); 24 (10%) reach σC with-
                                                                                               rewards or pruning signals.
out closing—the most promising near-misses for a learned
critic or larger budget; 41 (17%) are type-correct but wrong;
78 (32%) never escape syntax failures. Syntax-level fail-                                      Process supervision and rich feedback. Step-level super-
ures reflect hallucinated tactic names (retrieval/templates);                                  vision improves math reasoning (Lightman et al., 2024;
type-correct-but-wrong states suit a learned Critic; σC near-                                  Uesato et al., 2022) and informal self-correction (Fang
misses already expose useful intermediate goals.                                               et al., 2025; Shinn et al., 2023; Zhang et al., 2026b; 2025);
                                                                                               SDPO (Hübotter et al., 2026) distills such feedback during
4. Discussion                                                                                  training. VERITAS is the inference-time dual with deter-
                                                                                               ministic Lean feedback. Its roles align with multi-agent
VERITAS supports a narrow principle: deterministic verifier                                    reasoning (Hong et al., 2024; Wu et al., 2024a; Li et al.,
signals should feed generation rather than collapse into ter-                                  2023; Zhang et al., 2026a), but failed tactics are checked
minal rewards. It helps most on structurally close failures,                                   facts, not model opinions, so they can be remembered while
such as unknown constants, wrong arity, and σC partial                                         completed proofs are preserved.
goals, and least on syntactically valid but semantically un-
helpful states. The idea extends beyond Lean: SMT unsat                                        6. Conclusion
cores, Coq/Agda goals, symbolic-execution counterexam-
ples, and model-checking traces provide similar structure,                                     VERITAS shows that structured Lean feedback can guide
though soft verifiers require calibrated thresholds. VER-                                      zero-shot proof search without trace fine-tuning. Phase 1
ITAS is not a cure for IMO-level creativity or interactive                                     preserves easy proofs, while Phase 2 turns Lean errors,
latency (5 to 10 min/theorem); its main contribution is rout-                                  failed tactics, and partial goals into guidance, reaching
ing. Phase 1 collects easy proofs and failures, Phase 2                                        40.6suggests deterministic verifier signals can serve as
spends budget only where failures can guide the next tac-                                      inference-time state, not just final checks. Better retrieval,
tic, and a learned retriever is the clearest next gain for σA                                  cheaper critics, and distilled Phase 2 traces can scale this
failures (Figure 4(b)).                                                                        routing principle to the remaining hard tail.

                                                                                           6
                      VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

References                                                          Lample, G., Lachaux, M.-A., Lavril, T., Martinet, X., Hayat,
                                                                      A., Ebner, G., Rodriguez, A., and Lacroix, T. HyperTree
Auer, P., Cesa-Bianchi, N., and Fischer, P. Finite-time
                                                                      proof search for neural theorem proving. In Advances in
  analysis of the multiarmed bandit problem. Machine
                                                                      Neural Information Processing Systems (NeurIPS), 2022.
 Learning, 47(2–3):235–256, 2002.
                                                                    Li, G., Hammoud, H. A. A. K., Itani, H., Khizbullin, D., and
Azerbayev, Z., Schoelkopf, H., Paster, K., Dos Santos, M.,
                                                                       Ghanem, B. CAMEL: Communicative agents for “mind”
  McAleer, S., Jiang, A. Q., Deng, J., Biderman, S., and
                                                                       exploration of large language model society. In Advances
 Welleck, S. Llemma: An open language model for math-
                                                                       in Neural Information Processing Systems (NeurIPS),
  ematics. In International Conference on Learning Repre-
                                                                       2023.
  sentations (ICLR), 2024.
                                                                    Lightman, H., Kosaraju, V., Burda, Y., Edwards, H., Baker,
de Moura, L. and Ullrich, S. The Lean 4 theorem prover                B., Lee, T., Leike, J., Schulman, J., Sutskever, I., and
  and programming language. In Automated Deduction –                  Cobbe, K. Let’s verify step by step. In International
  CADE 28, pp. 625–635. Springer, 2021.                               Conference on Learning Representations (ICLR), 2024.
Fang, Z., Zhang, Y., Zhang, Y., Leach, K., and Huang, Y.            Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li,
  DPO-F+: Aligning code repair feedback with developers’              J., Xia, M., Chen, D., Arora, S., and Jin, C. Goedel-
  preferences. arXiv preprint arXiv:2511.01043, 2025.                 Prover: A frontier model for open-source automated the-
First, E., Rabe, M. N., Ringer, T., and Brun, Y. Baldur:              orem proving. arXiv preprint arXiv:2502.07640, 2025.
  Whole-proof generation and repair with large language             Polu, S. and Sutskever, I. Generative language model-
  models. In Proceedings of the 31st ACM Joint European               ing for automated theorem proving. arXiv preprint
  Software Engineering Conference and Symposium on the                arXiv:2009.03393, 2020.
  Foundations of Software Engineering (ESEC/FSE), pp.
  1229–1241, 2023.                                      Ren, Z. Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao,
                                                          W., Zhang, L., Fu, Z., Zhu, Q., Yang, D., Wu, Z. F., Gou,
Google DeepMind. AI solves IMO problems at silver medal   Z., Ma, S., Tang, H., Liu, Y., Gao, W., Guo, D., and
  level. Google DeepMind blog, 2024. URL https:           Ruan, C. DeepSeek-Prover-V2: Advancing formal math-
 //deepmind.google/discover/blog/                         ematical reasoning via reinforcement learning for subgoal
  ai-solves-imo-problems-at-silver-medal-level/.          decomposition. arXiv preprint arXiv:2504.21801, 2025.
Han, J. M., Rute, J., Wu, Y., Ayers, E. W., and Polu, S.            Shinn, N., Cassano, F., Berman, E., Gopinath, A.,
  Proof artifact co-training for theorem proving with lan-            Narasimhan, K., and Yao, S. Reflexion: Language agents
  guage models. In International Conference on Learning               with verbal reinforcement learning. In Advances in Neu-
  Representations (ICLR), 2022.                                       ral Information Processing Systems (NeurIPS), 2023.
Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Zhang,         Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai,
  C., Wang, J., Wang, Z., Yau, S. K. S., Lin, Z., Zhou, L.,            M., Guez, A., Lanctot, M., Sifre, L., Kumaran, D., Grae-
  Ran, C., Xiao, L., Wu, C., and Schmidhuber, J. MetaGPT:              pel, T., Lillicrap, T., Simonyan, K., and Hassabis, D. A
  Meta programming for a multi-agent collaborative frame-              general reinforcement learning algorithm that masters
  work. In International Conference on Learning Repre-                 chess, shogi, and Go through self-play. Science, 362
  sentations (ICLR), 2024.                                            (6419):1140–1144, 2018.
Hübotter, J., Lübeck, F., Behric, L., Baumann, A., Bagatella,       Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., and Chaud-
  M., Marta, D., Hakimi, I., Shenfeld, I., Kleine Buening,            huri, S. An in-context learning agent for formal theorem-
  T., Guestrin, C., and Krause, A. Reinforcement learning             proving. In First Conference on Language Modeling
  via self-distillation. arXiv preprint arXiv:2601.20802,             (COLM), 2024.
  2026.
                                                                    The mathlib Community. The Lean mathematical library.
Jiang, A. Q., Li, W., Tworkowski, S., Czechowski, K.,                 In Proceedings of the 9th ACM SIGPLAN International
   Odrzygóźdź, T., Miłoś, P., Wu, Y., and Jamnik, M. Thor:         Conference on Certified Programs and Proofs (CPP), pp.
   Wielding hammers to integrate language models and au-              367–381, 2020.
   tomated reasoning. In Advances in Neural Information
   Processing Systems (NeurIPS), 2022.                              Uesato, J., Kushman, N., Kumar, R., Song, F., Siegel, N.,
                                                                     Wang, L., Creswell, A., Irving, G., and Higgins, I. Solv-
Kocsis, L. and Szepesvári, C. Bandit based Monte-Carlo                ing math word problems with process- and outcome-
  planning. In 17th European Conference on Machine                    based feedback. In arXiv preprint arXiv:2211.14275,
  Learning (ECML), pp. 282–293, 2006.                                 2022.

                                                                7
                       VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

Wang, H., Xin, H., Zheng, C., Li, L., Liu, Z., Cao, Q.,               com/manishacharya60/veritas; all reported suc-
 Huang, Y., Xiong, J., Shi, H., Xie, E., Yin, J., Li, Z., Liao,       cesses are Lean 4/Mathlib verified.
 H., and Liang, X. LEGO-Prover: Neural theorem proving
 with growing libraries. In International Conference on               B. Comparison to Fine-Tuned Systems
 Learning Representations (ICLR), 2024.
                                                                      Table 4 gives the broader miniF2F context. We place this
Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang,        table in the appendix because these methods are not directly
 L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White,          comparable: they train on large Lean traces, while VERI-
 R. W., Burger, D., and Wang, C. AutoGen: Enabling next-              TAS is zero-shot and inference-only.
 gen LLM applications via multi-agent conversation. In
 Conference on Language Modeling (COLM), 2024a.                       Table 4. Context (not directly comparable): miniF2F solve rates
                                                                      of fine-tuned proof models that train on Lean traces.
Wu, Z., Huang, S., Zhou, Z., Ying, H., Wang, J., Lin, D., and                  Method (regime)                            miniF2F (%)
 Chen, K. InternLM2.5-StepProver: Advancing automated
                                                                                Zero-shot, inference-only
 theorem proving via expert iteration on large-scale LEAN                        VERITAS (this work)                         40.6
 problems. arXiv preprint arXiv:2410.15700, 2024b.                              Fine-tuned on Lean traces
                                                                                 ReProver (Yang et al., 2023)                26.5
Xin, H., Ren, Z. Z., Song, J., Shao, Z., Zhao, W., Wang, H.,                     COPRA-GPT-4 (Thakur et al., 2024)           30.7
                                                                                 InternLM-StepProver (Wu et al., 2024b)      65.9
  Liu, B., Zhang, L., Lu, X., Du, Q., Gao, W., Zhang, H.,                        DeepSeek-V2 (Ren et al., 2025)              88.9
  Zhu, Q., Yang, D., Gou, Z., Wu, Z. F., Luo, F., and Ruan,
  C. DeepSeek-Prover-V1.5: Harnessing proof assistant
  feedback for reinforcement learning and Monte-Carlo                 C. Implementation Details and
  tree search. In International Conference on Learning                   Hyperparameters
  Representations (ICLR), 2025.
                                                                      Table 5 lists every hyperparameter used by VERITAS. We
Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,                  make four design choices explicit: (i) the Tactician runs at
  P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.              T =0.8 to encourage diverse candidates while the Strategist
  LeanDojo: Theorem proving with retrieval-augmented                  and Critic use T =0.3 for deterministic
                                                                                                        √ role-playing; (ii) the
  language models. In Advances in Neural Information                  MCTS UCB constant c=1.4 ≈ 2 matches AlphaZero;
  Processing Systems (NeurIPS), 2023.                                 (iii) the value combination weights wv =0.6, ws =0.2 were
                                                                      fixed once on a 30-theorem development split (held out
Zhang, Y., Zhang, Y., Leach, K., and Huang, Y. CodeGrad:              from miniF2F) and never re-tuned; (iv) the four σA –σD
  Integrating multi-step verification with gradient-based             signal weights (0.1, 0.1, 0.2) encode that σC (partial goal
  LLM refinement. arXiv preprint arXiv:2508.10059, 2025.              progress) is the most informative intermediate signal short
                                                                      of completion.
Zhang, Y., Ganapavarapu, G., Jayaraman, S., Agrawal, B.,
  Patel, D., and Fokoue, A. SPIRAL: Symbolic LLM plan-
  ning via grounded and reflective search. In Proceedings             Software       environment. Lean            4       toolchain
  of the Fortieth AAAI Conference on Artificial Intelligence,         leanprover/lean4:v4.14.0, Mathlib commit
  2026a.                                                              e9f8a37 (frozen for the entire experiment). Python
                                                                      harness 3.11, anthropic-sdk 0.62, asyncio concur-
Zhang, Y., Li, J., Pei, K., Huang, Y., and Leach, K. SynthFix:        rency capped at 8 in-flight requests per agent role to respect
  Adaptive neuro-symbolic code vulnerability repair. arXiv            rate limits.
  preprint arXiv:2604.17184, 2026b.
                                                                      Hardware. A single 8-core machine with no GPU; all
Zheng, K., Han, J. M., and Polu, S. miniF2F: A cross-system           heavy lifting is on the Anthropic API and the Lean kernel.
  benchmark for formal Olympiad-level mathematics. In                 miniF2F (244 theorems) completes in ∼22 h wall-clock with
  International Conference on Learning Representations                8 worker processes; VERITAS-CombiBench (55 theorems)
  (ICLR), 2022.                                                       completes in ∼5 h.

                                                                      D. Prompts
A. Impact and Reproducibility
                                                                      D.1. Strategist
This work advances automated formal reasoning; the main               SYSTEM:
risk is over-trusting unchecked generated proofs. Code,               You are a Lean 4 proof strategist. Read the current
                                                                      goal
VERITAS-CombiBench, prompts, hyperparameters, and                     and produce ONE of six high-level strategies and a
per-theorem outcomes are available at https://github.                 depth


                                                                  8
                          VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

         Table 5. All VERITAS hyperparameters.                      - If a previous failure says "unknown constant
                                                                  ‘foo‘",
        Component Parameter          Value                            NEVER repeat ‘foo‘. Look in the Premises section
                                                                  for
        Strategist   model           Sonnet 4.6                       the closest valid name.
                     temperature     0.3                            - If a previous failure says "type mismatch", change
                     max_tokens      256                          the
        Tactician    model           Sonnet 4.6                       expected term, not the lemma name.
                     temperature     0.8                            - If a previous failure says "no goals", you
                     top_p           0.95                         over-closed;
                     max_tokens      512                              drop the trailing tactic.
                     K cands/node    6                              - Prefer atomic tactics over combinators on first
                     N Best-of-N     5                            attempt.

        Critic       model           Haiku 4.5                    INPUT:
                     temperature     0.3                            Goal       : {goal}
                     max_tokens      128                            Hypotheses : {hypotheses}
                                                                    Strategy   : {strategy}
        Retriever    corpus          Mathlib 4 (∼200k)              Premises   : {top-5 Mathlib lemmas, names +
                     k premises      5                            statements}
                     scoring         weighted overlap               Failures   : [(tactic_1, lean_error_1),
                     token weights   types 3, ops 2, conn 1                       (tactic_2, lean_error_2), ...]
        MCTS         UCB c           1.4
                     value wv        0.6                          OUTPUT: K=6 newline-separated tactic blocks, e.g.
                     strat ws        0.2
                     sig α1 , α2     0.1                          induction n with
                     sig α3          0.2                            | zero => norm_num
                     explor. β       0.1                            | succ n ih =>
                     iterations I    50                                 simp [ih, Nat.succ_eq_add_one]
                     budget          300 s/theorem
                                                                  rcases n with _ | n
        Lean batch   solver          lake env lean -json          . norm_num
                     batch size      K=6                          . simp [Nat.succ_eq_add_one]; omega
                     timeout         60 s/batch                   ...


estimate (1-5). Do NOT produce tactic code.                       D.3. Critic
                                                                  SYSTEM:
STRATEGIES (pick exactly one):                                    You are a Lean 4 proof-state critic. Read a partially
   DIRECT       - close in one tactic (rfl, decide,               completed proof state, the four-way verifier signal
omega,                                                            (sigma_A applied; sigma_B type-correct; sigma_C goal
                  norm_num, simp, ring, ...).                     progress; sigma_D proof-complete), and a short tactic
   INDUCTION    - induction over a Nat / List / Finset.           history; return a value in [0, 1] and at most 3 ranked
   CONTRADICTION- exfalso + manipulate hypotheses.                next-tactic suggestions for the Tactician.
   CASES        - case-split on a hypothesis or a
Decidable.                                                        VALUE GUIDELINES:
   REWRITE      - apply rw / simp_rw using known lemmas.            1.0 - state is closed (sigma_D = 1).
   APPLY_LEMMA - apply a named Mathlib lemma; needed                0.7..0.9 - clear partial progress (sigma_C = 1) and
when                                                                           only one or two tactics from closure.
                  the goal matches a known statement up             0.4..0.6 - state is type-correct but goal unchanged.
to                                                                  0.1..0.3 - state has type errors but is reachable.
                  unification.                                      0.0      - state is unreachable / contradictory.
DEPTH ESTIMATE: integer 1..5; 1 means a single closing            PRUNE:
tactic suffices, 5 means deep multi-step reasoning.                 Set "prune": true if no further expansion can reach
                                                                    closure (e.g. wrong induction split, exhausted lemma
INPUT:                                                              options).
  Theorem statement : {statement}
  Imports / context : {imports}                                   INPUT:
  Hypotheses        : {hypotheses}                                  Goal           : {current_goal}
  Goal              : {goal}                                        Hypotheses     : {hypotheses}
                                                                    Recent tactics : last 5 tactics applied
OUTPUT (JSON):                                                      Signals        : (sigma_A, sigma_B, sigma_C, sigma_D)
{"strategy": "INDUCTION", "depth": 3,
 "rationale": "one short sentence"}                               OUTPUT (JSON):
                                                                  {"value": 0.72,
                                                                   "next_tactics": ["simp [Nat.succ_eq_add_one]",
D.2. Tactician                                                                      "omega",
SYSTEM:                                                                             "linarith"],
You are a Lean 4 + Mathlib theorem-proving assistant.              "prune": false,
Given a current goal, retrieved premises, a high-level             "rationale": "near-miss; one rewrite from closure"}
strategy, and a list of previously-attempted tactics
with
their Lean errors, output K candidate tactics (one per
line) that are likely to make progress. Each candidate
                                                                  E. Retriever Implementation
must be a complete tactic block that compiles in ‘by‘
mode in Lean 4. Do NOT add prose, comments, or                    The Retriever scores each Mathlib lemma ℓ against the cur-
markdown.
                                                                  P goal g by a weighted keyword-overlap score s(ℓ, g) =
                                                                  rent
CRITICAL CORRECTION RULES (always apply):                            t∈tok(g)∩tok(ℓ) w(type(t)), with weights w(type) = 3


                                                              9
                       VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

(e.g. Nat, Finset, Real), w(op) = 2 (e.g. +, ·, ≤, <,                 fully checked by sorry-free reference proof exists
mod), and w(conn) = 1 (e.g. ∧, ∨, →). Token extrac-                   in our private solutions file; (iii) no statement uses
tion normalises Unicode and Mathlib’s namespace dots (e.g.            Decidable.decide as the closing tactic; (iv) the names-
Finset.sum_pow_choose_eq contributes the tokens                       pace is combiBench.<source>.
Finset, sum, pow, choose). The top-k premises by
score are returned to both the Tactician (as candidate lemma          Worked example. A representative theorem from the
names) and the Critic (as context for value estimation). We           Brualdi subset: given the number of subsets of an n-element
index Mathlib once per session and reuse the sparse map.              set, prove
We did not tune weights; defaults gave the highest recall on                                 n  
                                                                                            X     n
a 50-lemma held-out probe set.                                                                       = 2n ,
                                                                                                  k
                                                                                           k=0

F. Batched Lean Validation                                            formalised in Lean 4 over Finset.range
                                                                      (n+1)        with     the    expected      proof     simp
Construction. For a state s with goal g, the Tactician                [Finset.sum_pow_choose_eq, pow_succ].
returns K=6 candidate tactics {τ1 , . . . , τK }. The harness         Phase 1 with Best-of-5 hallucinated Nat.choose_sum
emits a single .lean file containing K private theorems               (does not exist) and Finset.sum_choose_pow (wrong
sharing the same imports and hypotheses:                              arity), neither of which the Tactician corrects without the
import Mathlib                                                        verifier’s unknown constant ‘Nat.choose_sum‘
private theorem _p0 ({hyps}) : {goal} := by                           error feedback. VERITAS solves it on iteration 14 after the
  {tactic_0}                                                          Tactician, conditioned on the accumulated failure history,
private theorem _p1 ({hyps}) : {goal} := by                           emits the correct Finset.sum_pow_choose_eq
  {tactic_1}                                                          lemma name.
...
                                                                      License. The supplementary material includes the the-
Compilation. A single lake env lean -json call                        orem statements, reference proofs, and per-theorem out-
returns one JSON line per Lean message, each carrying                 comes. VERITAS-CombiBench is released publicly under
(file, line_start, line_end, severity,                                CC-BY 4.0. Statements derived from competition short-
message). The harness maps each message back to the                   lists are public domain (problem statements, not solutions);
corresponding τi by line range and classifies it into σA –σD :        Brualdi-derived problems are paraphrased to avoid exact
an empty error set with kind=ok on τi ’s line is σD ; an              verbatim re-use.
unsolved goals message is σC ; a type mismatch
or application type mismatch is σB ; everything                       H. Detailed Failure Case Studies
else (parse errors, unknown constants) is σA . Successful
tactics on different τi lines are independent because of the          We expand the three case studies summarised in Section 3,
private modifier.                                                     with condensed Lean traces.

Cost reduction. Lean’s per-file overhead (Mathlib im-                 (i) Feedback-driven syntax correction. On miniF2F-test
port, namespace setup, elaboration of shared hypotheses)              theorem induction_sum_pow_choose, Phase 1 gen-
is amortised across K candidates instead of paid K times.             erates induction n with zero => norm_num
Empirically the cost ratio is K=6 candidates in ∼1.05× the            | succ n ih => ...           (missing the leading |).
wall-clock of a single tactic check, vs. K×1.0 ≈ 6× for the           Lean 4 returns expected ‘|’, got identifier
sequential baseline (a 5.7× speed-up that grows to ∼20×               ‘zero’ (σA =0). The Tactician, conditioned on this error,
at K=16).                                                             emits the corrected induction n with | zero
                                                                      => norm_num | succ n ih => simp [ih,
                                                                      Nat.succ_eq_add_one] on the next iteration, which
G. VERITAS-CombiBench Construction                                    closes the goal (σD =1).
Sources                  (55                      theorems).
IMO / IMO Shortlist (combinatorics)        22                         (ii) Critic-guided intermediate lemma. On VERITAS-
Brualdi, Intro. Combinatorics (5th ed.)    29                         CombiBench problem brualdi_3_4, Phase 1 attempts
Online problem repositories                 4                         the direct closure omega repeatedly. The verifier re-
                                                                      turns σB (type mismatch on Int vs. Nat). The Critic
Statement curation. Each problem was hand-formalised                  value drops below 0.2 for any state whose recent tactic is
by the authors in Lean 4 over Mathlib. We require:                    omega; MCTS expansion under the APPLY_LEMMA strat-
(i) a theorem statement (no def, no example); (ii) a                  egy produces have h : (n : Int) = ... :=

                                                                 10
                      VERITAS: Verifier-Guided Proof Search for Zero-Shot Formal Theorem Proving

by push_cast; ring, which unblocks a subsequent                     Paired outcome reporting. Because Best-of-5 is sam-
omega closure.                                                      pled independently of VERITAS Phase 1, we report paired
                                                                    overlap counts rather than using the baseline gap as a signif-
(iii) Strategy-guided field arithmetic. On miniF2F-                 icance claim.
test theorem algebra_field_simp_ex, the Strategist
outputs REWRITE with depth 2. The Tactician emits                   K. Per-Category miniF2F Breakdown
field_simp; ring; the verifier returns σB (unsolved
denominator). The Tactician’s next iteration, prompted              Table 1 is the authoritative category breakdown used for all
with the type-mismatch error and the strategy bias, emits           deltas in Section 3.4. We avoid duplicating alternate tables
field_simp [hx, hy]; ring, closing the goal.                        because miniF2F variants differ in naming and theorem
                                                                    grouping.
I. Cost and Compute Breakdown                                       The only negative delta is IMO, where the independent
                                                                    Best-of-5 run solves two more theorems than VERITAS.
Table 6 decomposes the per-theorem cost on miniF2F. The             This reflects stochasticity and the fixed MCTS budget, not a
Tactician dominates token spend (K=6 candidates per node            violation of internal monotonicity.
at T =0.8); Critic and Strategist each contribute ≤ 5%. Lean
validation is the dominant wall-clock component but con-            Algebra and “other” show the clearest positive deltas, match-
tributes zero API cost.                                             ing the claim that MCTS helps most when proofs require
                                                                    dependent simplifications rather than a single lucky tactic.
Table 6. Per-theorem cost decomposition (miniF2F). Averages
over 244 theorems; both phases included.
                                                                    L. Additional Negative Results
        Component          Calls Tokens (k)   USD
                                                                    Things we tried that did not help. These ablations were
        Strategist          1.0         0.6   0.001
        Tactician           7.4        18.2   0.504                 retained to make the final configuration less arbitrary and to
        Critic              6.4         1.7   0.011                 clarify which forms of extra modeling capacity were useful.
        Retriever           8.4           –   0.000
        Lean batch         27.3           –   0.000                 Larger K=12 gave only +0.4pp, within Wilson CI, at 2×
                                                                    API cost. We therefore kept K=6 as the better efficiency
        Total / theorem   50.5         20.5 0.516
        Total / sweep   12,300        5,010 125.7                   point.
                                                                    Critic-only without four-way signals collapsed to −2.1pp:
                                                                    σA –σD structure is necessary, not just sufficient, because
CombiBench cost. VERITAS-CombiBench’s smaller (55                   the Critic otherwise loses the distinction between syntax
theorems) but harder profile yields ∼$0.83 per theorem              failure, type failure, and genuine goal progress.
(more Phase-2 iterations on average; Lean calls average 41
per theorem) and ∼$45 per full sweep.                               Multiple Strategists added 1.3,s/theorem and −0.8pp, sug-
                                                                    gesting that strategy diversity was less useful than consistent
                                                                    state routing.
Carbon estimate. Anthropic’s reported Sonnet inference
uses ∼0.5 Wh per 1 k tokens; total LM tokens for one full           Chain-of-thought in the Tactician raised token cost 1.7×
miniF2F sweep (∼5 M tokens) corresponds to ∼2.5 kWh,                without solve-rate gain. In all four cases, extra modeling
or roughly 1 kg CO2 e under the EU average grid mix (com-           capacity helped less than preserving the verifier signal in a
parable to a one-hour video call).                                  compact, stateful form.

J. Statistical Methodology                                          M. Future Directions
Confidence intervals. We report Wilson 95% intervals                VERITAS shows that structured Lean feedback can guide
with z=1.96 and benchmark size n. At p=0.4, half-                   zero-shot proof search without trace fine-tuning. By pre-
widths are ±6.2pp on miniF2F (n=244) and ±13.0pp on                 serving easy Phase 1 proofs and routing Lean errors, failed
VERITAS-CombiBench (n=55).                                          tactics, and partial goals into Phase 2 search, it reaches
                                                                    40.6% on miniF2F and 7.3% on VERITAS-CombiBench.
Variance under reseeding. We re-ran a 50-theorem strati-            These results suggest that deterministic verifier signals can
fied miniF2F subset (10 per category) under three Tactician         serve as inference-time state, not just final checks; better
seeds. Standard deviations were ±1.4pp solve rate and               retrieval, cheaper critics, and distilled Phase 2 traces can
±2.1 Lean calls/theorem, so one full sweep is a reasonable          scale the same principle to the remaining hard tail.
estimator.

                                                               11
