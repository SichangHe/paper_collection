                                                                                Inference-Time Diversity in
                                                                             RL-Trained Lean Theorem Provers:
                                                                                    A Diagnostic Study


                                                                                                 Zachary Burton 1


                                                                  Abstract                                      2025).1 The prevailing paradigm assumes that sufficient RL
                                                                                                                training and inference-time compute will cause models to
arXiv:2601.16172v3 [cs.AI] 26 Jun 2026




                                              RL-trained Lean theorem provers mode-collapse
                                              at inference time: on miniF2F-test with DeepSeek-                 internalize the structural priors required for formal proofs.
                                              Prover-V1.5-RL, doubling the i.i.d. sampling bud-                 We present evidence that this assumption is flawed. RL-
                                              get from k=32 to k=64 produces zero addi-                         trained provers suffer from mode collapse at inference time:
                                              tional solved theorems (42/244 in both cases).                    they converge on a narrow set of proof strategies and fail to
                                              A fixed schedule of 15 tactic skeletons breaks                    explore alternatives even when given additional sampling
                                              this plateau and recovers a +45% relative im-                     budget. On miniF2F-test with DeepSeek-Prover-V1.5-RL,
                                              provement at k=16 (mean ∆ = +12.3 ± 4.2                           i.i.d. sampling at temperature 0.6 solves 38 theorems at
                                              theorems across n=3 seeds, sign preserved in                      k=16, 42 at k=32, and still 42 at k=64—32 additional
                                              every seed). A controlled diversity ablation rules                stochastic samples find zero new proofs.
                                              out the prompt-diversity confound: tactic skele-
                                              tons help, paraphrases match the baseline, and                    A fixed prompt schedule of 15 common tactic skeletons
                                              irrelevant Lean comments actively degrade. A                      (simp, intro, constructor, . . . ) breaks the plateau,
                                              leave-one-out formalization-difficulty stratifica-                yielding a +45% relative improvement at k=16 (55 vs.
                                              tion reveals a structural-content gradient across                 38) and continuing to find new proofs through k=64. A
                                              the three perturbations. The phenomenon is RL-                    controlled diversity ablation (skeleton vs. paraphrase vs.
                                              specific: V1.5-Base proves zero theorems regard-                  irrelevant comment) confirms the gains are structural, not
                                              less of intervention, identifying RL as the stage that            an artifact of prompt diversity. Stratifying by an empirical
                                              creates the proof capability which subsequently                   formalization-difficulty score grounded in baseline solv-
                                              collapses; extending to two additional 7B Lean                    ability across our experimental matrix further localizes the
                                              provers, RL-trained DeepSeek-Prover-V2-7B con-                    effect.
                                              tributes +3 frontier solves no i.i.d. baseline can                A recent line of work has examined whether RL with veri-
                                              reach despite a flat aggregate, while SFT-trained                 fiable rewards (RLVR) genuinely expands a base model’s
                                              Goedel-Prover does not (−10.0 ± 4.4 theorems,                     reasoning capacity (Yue et al., 2025; Wu et al., 2025). We
                                              n=3, sign preserved every seed). Inference-time                   study a different question—inference-time collapse within an
                                              structural diversity is a cheap, complementary                    RL-trained policy in an exact-verifier domain—and discuss
                                              axis for RL-trained provers, orthogonal to scaling                the relationship in detail in Section 2.
                                              model size or training compute.
                                                                                                                1.1. Contributions
                                         1. Introduction                                                           • We diagnose mode collapse in RL-trained Lean provers
                                                                                                                     via two complementary signatures: an i.i.d. sampling
                                         Recent neural theorem provers combine large language                        plateau at k=32 → 64 on V1.5-RL that a fixed 15-
                                         models with reinforcement learning and tree searches to                     skeleton schedule breaks, and a controlled diversity
                                         achieve strong results on formal proof benchmarks (Xin                      ablation (skeleton vs. paraphrase vs. irrelevant com-
                                         et al., 2024; Chen et al., 2025; Trinh et al., 2024; Lin et al.,            ment) showing the gain comes from structural guidance,
                                           1
                                             Massachusetts Institute of Technology, Cambridge, MA, USA.              not prompt diversity. A dedicated NL-only ablation
                                         Correspondence to: Zachary Burton <zacburton@alum.mit.edu>.                 (C3) further isolates the natural-language hint contri-
                                                                                                                  1
                                         The 3 rd AI for Math Workshop at the 43rd International Confer-            Code, prompts, and per-attempt logs: https://github.
                                         ence on Machine Learning (ICML), Seoul, South Korea, 2026.             com/zacn04/icml_hints_for_provers.
                                         Copyright 2026 by the author(s).

                                                                                                            1
                                            Inference-Time Diversity in Lean Provers

     bution from the tactic-prefix contribution.                       Entropy collapse and the limits of RL post-training.
                                                                       RL post-training narrows the output distribution of the un-
   • A leave-one-out empirical-difficulty stratification,              derlying base model, trading diversity against best-of-N
     grounded in cross-prover baseline solvability, local-             performance (Kirk et al., 2024). Two recent works study
     izes the structural gain to the easy/trivial buckets where        whether RL with verifiable rewards (RLVR) expands a base
     V1.5-RL’s gap to other open-source provers concen-                model’s reasoning support: Yue et al. (2025) find that base
     trates, and reveals a clean structural-content gradient           models surpass their RL-trained variants at large k on math
     across the three perturbations.                                   and coding benchmarks with answer-string verification, and
                                                                       Wu et al. (2025) argue more generally that the contraction
   • We establish RL-specificity in two ways. A within-                of output support induced by RLVR can outweigh its expan-
     architecture base-vs-RL contrast on V1.5 shows the                sion of high-reward modes. Our setting differs from those
     non-RL base has zero proof capability, so RL is both the          measurements in two relevant ways: the Lean kernel verifies
     source of the capability and the source of its collapse.          proofs exactly rather than by string-match or unit-test (so
     A cross-model contrast on two additional 7B provers               V1.5-Base proves zero theorems at any k, Section 4.4), and
     shows that RL-trained DeepSeek-Prover-V2-7B gains                 our cross-model comparison includes an SFT-trained control
     +3 frontier theorems unreachable by any i.i.d. baseline           (Goedel-Prover) absent from those setups.
     despite a flat aggregate, while SFT-trained Goedel-
     Prover loses −10.0 ± 4.4 theorems across n=3 seeds
                                                                       3. Method
     (sign preserved every seed).
                                                                       3.1. Skeleton Schedule and Ablations
2. Related Work                                                        A structured query is the pair (x, s) of theorem statement
                                                                       x and tactic skeleton s. The schedule is a deterministic
Neural theorem provers. The integration of language
                                                                       15×8=120 grid: 15 hand-selected Lean tactic skeletons
models with formal proof assistants has progressed quickly.
                                                                       (Appendix A, including the empty skeleton) crossed with
Early systems like GPT-f (Polu & Sutskever, 2020) and
                                                                       8 goal-hint comments (the first being empty). Schedule ad-
PACT (Han et al., 2022) demonstrated that transform-
                                                                       vances tactic-first, hint-second; each of the 120 attempts is a
ers could generate tactic scripts, and LeanDojo with Re-
                                                                       distinct (skeleton, hint) prompt configuration with no repeats
Prover (Yang et al., 2023) added retrieval to handle Lean’s
                                                                       within k≤120. Our tested budgets k ∈ {16, 32, 64} sample
large premise library. More recent provers combine rein-
                                                                       the first 16, 32, and 64 grid entries. The schedule is fully
forcement learning with tree search to push miniF2F perfor-
                                                                       deterministic; stochasticity comes only from temperature
mance above 60%: the DeepSeek-Prover family (V1.5 (Xin
                                                                       sampling.
et al., 2024) and V2 (Ren et al., 2025)) and the supervised-
fine-tuned Goedel-Prover (Lin et al., 2025). We deliber-               To isolate structural content from prompt diversity per se, we
ately anchor our analysis on V1.5-RL: it is the only widely            add two ablations (Appendix B): C1 (paraphrase)—16 se-
benchmarked RL-trained Lean prover that also releases a                mantically equivalent rephrasings of the instruction injected
non-RL base variant, which is what makes the clean within-             as Lean comments, with empty tactic prefix; and C2 (com-
architecture isolation of RL’s effect possible in Section 4.4.         ment)—16 content-free Lean comments (/- approach
                                                                       alpha -/, . . . ) prepended to the theorem.
Tree search and hint-based methods. HyperTree Proof
Search (Lample et al., 2022) and COPRA (Thakur et al.,                 3.2. Experimental Setup
2023) build proof trees one tactic at a time with explicit             Models. The primary within-architecture analysis (Sec-
backtracking; our skeleton schedule can be viewed as fixing            tions 4.1–4.4) uses DeepSeek-Prover-V1.5-RL together with
only the first node of the proof tree and letting the model            its non-RL base variant V1.5-Base—same pretraining cor-
complete the rest in a single forward pass with no proof-state         pus, no RL fine-tuning stage. V1.5 is the only widely
feedback. Draft-Sketch-Prove (Jiang et al., 2023), Conjec-             benchmarked RL-trained Lean prover that releases a paired
tureBench (Sivakumar et al., 2025), and Aristotle (Achim               non-RL checkpoint, which is what enables the clean within-
et al., 2025) intervene at a higher level of abstraction (infor-       architecture isolation of RL’s effect. The cross-model study
mal sketches, conjecture generation, intermediate semantic             in Section 4.5 extends the pass@16 comparison to two addi-
lemmas), whereas we operate at the syntactic tactic-stem               tional 7B provers: DeepSeek-Prover-V2 (Ren et al., 2025),
level and focus on diagnosing RL-induced underexplo-                   RL-trained and emitting chain-of-thought before the Lean
ration rather than proposing a new proving architecture.               output; and Goedel-Prover-SFT (Lin et al., 2025), which is
Lean 4 (de Moura & Ullrich, 2021) and Mathlib (The                     supervised-fine-tuned with no RL stage and emits Lean code
mathlib Community, 2020) form our verification stack and               directly. Neither additional model releases a paired non-
miniF2F (Zheng et al., 2022) is our benchmark throughout.

                                                                   2
                                           Inference-Time Diversity in Lean Provers

RL or non-SFT base checkpoint, so the within-architecture                                                            Mode-collapse plateau on miniF2F-test (V1.5-RL)
RL-vs-no-RL contrast remains possible only on V1.5.                                             65          A-RL (i.i.d. baseline)
                                                                                                            B-RL (skeleton schedule)                                               60
                                                                                                60                                58
                                                                                                     55




                                                                     Theorems solved (of 244)
Skeleton delivery. We deliver the structural intervention                                       55
in each model’s native interaction modality. For completion-                                    50
mode provers (V1.5-RL, V1.5-Base, Goedel-Prover) this                                           45
is a literal Lean tactic prefix injected after := by. For                                       40                                42                                               42
the reasoning-mode prover (V2) it is a natural-language                                              38
                                                                                                35                                                         plateau (k=32 -> k=64
instruction in the chat prompt: “Begin the proof with:                                                                                                      adds zero theorems)
                                                                                                30
<tactic>.” Both delivery mechanisms operationalize
                                                                                                25
the same underlying hypothesis—that the model should                                                 k=16                        k=32                                              k=64
                                                                                                                                        Sampling budget
commence the proof from a specific tactic stem—adapted to
the prompting paradigm each model was trained for. Forcing           Figure 1. A-RL i.i.d. sampling flatlines at 42/244 from k=32
a literal Lean prefix on a chat-mode reasoning model would           onward; B-RL with the 15-skeleton schedule keeps climbing.
conflict with its native chain-of-thought process and conflate
the structural-guidance claim with a separate question about
cross-paradigm prompt-format robustness.                             available at https://github.com/zacn04/icml_
                                                                     hints_for_provers.
Search procedure. Both conditions execute exactly k
LLM calls per theorem and the search exits on the first
attempt that produces a Lean-verified proof. Pass@k is               4. Results
reported in the strict sense: any of the k attempts succeeds.        4.1. Scaling Analysis: Mode Collapse in i.i.d. Sampling
Sample mode (A) holds the prompt fixed (empty) and varies
the random seed across attempts; structured mode (B)                 Table 1 presents our main finding. The baseline (i.i.d.
holds the seed fixed and varies the prompt across attempts           sampling) plateaus at k=32: doubling the budget to k=64
according to the schedule. Both modes consume an identical           produces zero additional solved theorems. In contrast, the
LLM-call budget at k=16, making the comparison an apples-            skeleton-guided approach continues to find new proofs at
to-apples test of two sources of diversity. Model outputs are        each budget level.
post-processed before Lean verification (theorem-signature           The baseline’s plateau from k=32 to k=64 is striking: 32
stripping, markdown-fence removal, re-indentation); see              additional samples—each with different random seeds—
Appendix C for the exact pipeline.                                   fail to find a single new proof. This indicates that the
                                                                     model is trapped in a narrow region of the proof strategy
Benchmark and environment. We evaluate on miniF2F-                   space. Temperature sampling alone cannot break this mode
test (244 theorems, Lean 4 split), with the Lean toolchain           collapse.
pinned to v4.9.0-rc1 and Mathlib pinned to commit
7fa489a5. This pinning matches the environment used                  4.2. Diversity Ablation: Structure vs. Diversity
to train DeepSeek-Prover-V1.5 and is critical for clean at-
tribution: newer Lean versions ship substantially more               Table 2 compares four conditions at k=16 to isolate the
powerful built-in tactic solvers (notably simp, aesop, and           source of improvement.
nlinarith), and running on those toolchains would con-
                                                                     The C2 result is interesting. We observe that irrelevant
flate the gain from our intervention with the gain from Lean’s
                                                                     Lean comments injected before the theorem actually de-
own evolution.
                                                                     grade performance, suggesting that surface-level prompt
                                                                     perturbations that lack tactic-level structure interfere with
Decoding and inference. Sampling uses temperature                    the model’s collapsed policy. The C1 topline equality with
0.6 and top-p 0.95 for all conditions. Completion-mode               A-RL is suggestive but, by itself, ambiguous: it is consis-
provers use a 1024-token generation budget per attempt;              tent with both “C1 has no effect” and “C1 helps on some
reasoning-mode provers use 8192 tokens to accommo-                   theorems while hurting an equal number on others.” We
date their chain-of-thought before the Lean code block.              disambiguate these in Section 4.3 by stratifying solves by
Inference runs on a single A100 GPU per experiment                   empirical formalization difficulty.
(80GB for the V1.5 runs, 40GB for V2 and Goedel-Prover;
both sufficient). Lean verification uses lake env lean
                                                                     4.3. Empirical Difficulty Stratification
--json with a 120-second per-attempt timeout, and we
shard theorems 8-way across parallel workers (i mod 8).              Mathematical difficulty (e.g., IMO vs. textbook) is a poor
Full code, prompt templates, and per-attempt logs are                proxy for the difficulty a neural prover actually faces in

                                                                 3
                                                                                                       Inference-Time Diversity in Lean Provers

                                                               Condition                                                 Pass@16                     Pass@32               Pass@64
                                                               A-RL (i.i.d. baseline)                               38/244 (15.6%)                42/244 (17.2%)       42/244 (17.2%)
                                                               B-RL (skeleton schedule)                             55/244 (22.5%)                58/244 (23.8%)       60/244 (24.6%)
                                                               Absolute gap                                               +17                          +16                   +18
                                                               Relative improvement                                      +44.7%                       +38.1%                +42.9%
Table 1. Scaling analysis on miniF2F-test with DeepSeek-Prover-V1.5-RL. The i.i.d. baseline plateaus at k=32 while the skeleton schedule
continues to find new proofs. The gap is persistent across all budget levels.



                                        Condition                                        Solved          Pass@16                                                  Bucket              #
                                        C2 (irrelevant comments)                            25               10.2%                                                Frontier (σ=0)     117
                                        A-RL (i.i.d. baseline)                              38               15.6%                                                Hard (σ=1)         24
                                        C1 (instruction paraphrases)                        38               15.6%                                                Medium (σ=2)        13
                                        B-RL (skeletons)                                    55               22.5%                                                Easy (σ=3)         53
Table 2. Diversity ablation at k=16 (all /244). Skeletons improve;                                                                                                Trivial (σ=4)      37
paraphrases match baseline at topline; comments degrade. Sec-                                                                                                     Total              244
tion 4.3 shows C1’s match hides redistribution.
                                                                                                                                             Table 3. Leave-one-out difficulty distribution of miniF2F-test for
                                                                                                                                             V1.5-RL analyses. σ = σ−V1.5-RL counts how many of four non-
                                                    Diversity ablation: structural content drives the gain
                                                                                                                                             V1.5-RL sample baselines (Goedel ×2, V2 ×2) solve the theorem.
                                                                                                                                             48% are in the frontier bucket.
                                   60                                                                           55
                                                                                                             (22.5%)
                                                                                              48
Theorems solved at k=16 (of 244)




                                   50                                                      (19.7%)
                                                               38              38
                                   40                       (15.6%)         (15.6%)                                      baseline (38)       every tested k; theorems with σ−M =N−M (the maximum,
                                   30        25                                                                                              4 for V1.5-RL) are solved by every other baseline. The
                                          (10.2%)
                                                                                                                                             distribution under σ−V1.5-RL is reported in Table 3.
                                   20

                                   10                                                                                                        Where the perturbations operate. For each condition C,
                                    0                                                                                                        let NEW(C) denote the set of theorems solved by C but not
                                             C2              A-RL              C1            C3                B-RL
                                         irrelevant           i.i.d.       instruction     NL goal             tactic                        by V1.5-RL sample at k=16, and let LOST(C) denote the
                                         comments           baseline      paraphrases     hints only         skeletons
                                                                                                                                             set solved by sample but not by C. Stratifying these sets by
Figure 2. Structural-content gradient at k=16: C2 < A-RL = C1                                                                                σ−V1.5-RL yields Table 4.
< C3 < B-RL. Irrelevant tokens hurt; pure paraphrase matches the
baseline; NL goal hints alone (C3) recover most of the A–B gap;
tactic stems go furthest.                                                                                                                    What the stratification reveals. The skeleton intervention
                                                                                                                                             specifically remediates V1.5-RL’s gap to the rest of the field.
                                                                                                                                             Of its 17 net wins, 15 fall in the easy (+9) and trivial
Lean, because the choice of formalization can materially                                                                                     (+6) buckets—that is, on theorems where three or four of
shift the proof difficulty independently of the under-                                                                                       the four other-model baselines already solve without any
lying mathematics. We therefore define an empirical                                                                                          intervention. This is the operational signature of mode
formalization-difficulty score per theorem, grounded in what                                                                                 collapse: V1.5-RL is failing on problems that other RL-
current ML provers can actually do on these specific Lean                                                                                    and SFT-trained provers solve routinely, and the skeleton
formalizations.                                                                                                                              intervention recovers precisely those problems.
                                                                                                                                             The two non-structural perturbations behave very differently.
Difficulty score (leave-one-out). For each theorem τ and
                                                                                                                                             Paraphrase (C1) reshuffles wins within the easy and trivial
a target model M under analysis, we define σ−M (τ ) as the
                                                                                                                                             buckets without producing any net gain, and comment (C2)
number of hint-free i.i.d. sampling baselines from other mod-
                                                                                                                                             degrades performance uniformly across those same buckets.
els that solve τ . This leave-one-out construction prevents
                                                                                                                                             The structural-content gradient is sharpest in the easy-plus-
the score from being contaminated by M ’s own sample runs,
                                                                                                                                             trivial column, where the three perturbations sit at +15
which also serve as the reference for the “NEW” analysis.
                                                                                                                                             (skeleton), 0 (paraphrase), and −14 (comment).
For analyses of V1.5-RL, the four baselines used to com-
pute σ−V1.5-RL are Goedel-Prover sample at k∈{16, 32} and                                                                                    Higher sample budgets do not change the frontier picture.
V2-7B sample at k∈{16, 32}. (An equivalent leave-one-out                                                                                     Replicating the stratification at k=32 and k=64 on V1.5-
score is used for the V2 analysis in Section 4.5.) Theorems                                                                                  RL, no perturbation unlocks a single σ−V1.5-RL =0 frontier
with σ−M =0 are beyond the reach of every other baseline at                                                                                  theorem at any tested budget. Some fraction of the 117

                                                                                                                                         4
                                              Inference-Time Diversity in Lean Provers

                            Condition            Frontier    Hard       Medium     Easy    Trivial    NET
                            Skeleton (B-RL)         0         +1           +1       +9       +6       +17
                            Paraphrase (C1)         0          0            0       +3       −3        0
                            Comment (C2)            0         +1            0       −6       −8       −13
Table 4. NET effect (NEW − LOST) of each V1.5-RL perturbation at k=16, stratified by σ−V1.5-RL . The skeleton intervention’s +17 net
is dominated by recoveries in the easy (+9) and trivial (+6) buckets—theorems that other open-source provers routinely solve via sample
but that V1.5-RL sample misses, exactly the population we would expect a mode-collapsed model to fail on. Paraphrase (C1) shows only a
small redistribution between easy and trivial; comment (C2) shows uniform degradation across easy and trivial. No perturbation moves
any theorem out of the σ−V1.5-RL =0 frontier.



       Attempt class                      Wins     NEW                  content gradient hypothesized in Section 3.2: NL hints alone
       Attempt 0 (truly empty)              16        0                 recover roughly 58% of the A→B gap (+10 solves of the
       Attempt 15 (hint comment only)        9       8                  +17 B-A topline), and tactic stems contribute the orthogonal
       Tactic prefix (attempts 1–14)        30       12                 remainder (+7). Skeleton guidance is therefore not reducible
       Total                                55       20                 to either modality alone—both layers contribute, and the
Table 5. V1.5-RL structured k=16 wins by attempt class. “NEW”           two effects compose.
= wins not in V1.5-RL sample k=16. The hint-comment slot
contributes +8 NEW, tactic prefixes contribute +12. Dominant            4.4. Base vs. RL: The Origin of Mode Collapse
tactic prefixes: intros (+6), norm num (+3).
                                                                        The base model result is unambiguous and somewhat surpris-
                                                                        ing: DeepSeek-Prover-V1.5-Base proves zero theorems
                                                                        on miniF2F-test, regardless of sampling budget or whether
frontier theorems likely reflect known formalization issues             tactic skeletons are provided. Inspection of the generated
in miniF2F-test—missing hypotheses or ambiguous state-                  outputs across all 244 theorems and all 64 attempts reveals
ments on specific competition problems—rather than pure                 that the base model produces sorry in 58.8% of its outputs,
capability limits, but we cannot disentangle the two with the           or echoes the theorem statement verbatim without attempting
data we have.                                                           a proof. By contrast, the RL model almost never generates
                                                                        explicit sorry tokens (<0.2% under i.i.d. sampling); its
Decomposing the skeleton win. The k=16 schedule                         mode collapse manifests instead as persistent generation of
includes one wrap attempt (attempt 15) where the tac-                   failing but syntactically valid tactic sequences—repeated
tic prefix is empty but a natural-language goal-hint com-               rw or apply attempts that do not close the goal.
ment (e.g., /-- Hint: Start by simplifying                              This reframes our hypothesis. We had originally predicted
using simp. --/) is prepended. We count V1.5-RL                         that the base model would show a smaller skeleton-induced
structured wins by attempt class (Table 5).                             improvement, providing graded evidence that RL exacerbates
The 0/16 NEW count for attempt-0 confirms V1.5-RL is                    collapse. Instead, the base model shows no improvement
effectively deterministic at our inference settings—the +17             because it has no proof capability to collapse: the RL fine-
topline cannot be attributed to vLLM sampling variance. The             tuning stage is what teaches the model to generate valid Lean
structural intervention works through two delivery layers:              4 tactic proofs in the first place. Skeletons cannot substitute
natural-language hint comment (+8 NEW) and literal tactic               for this capability, nor goad out theorem proving knowledge
prefix (+12 NEW), both contributing additively to the +20               where it is non-existent.
total.                                                                  The implication is sharper than an earlier framing we posited:
                                                                        mode collapse is not merely exacerbated by RL training,
Dedicated NL-only ablation (C3). The attempt-class                      it is caused by it. RL creates a useful but narrow proof
decomposition pins the NL hint contribution to a single                 policy; without the structural intervention provided by tactic
slot of the composite schedule, leaving open whether the                skeletons, the model cannot escape the policy learned at
effect generalizes when the entire budget is spent on NL                training time, even when it may benefit. The base model
comments. We therefore ran a dedicated condition C3 in                  demonstrates that the underlying language model has no
which all 16 attempts on V1.5-RL use empty tactic prefixes              useful tactic-level prior: the RL stage is the locus of both
and cycle through the 7 distinct natural-language goal-hint             proof capability and the inference-time collapse that limits
comments (Appendix A), with no tactic stem injected at any              it.
attempt. C3 solves 48/244 (19.7%)—intermediate between
sample-only A (15.6%) and structured-skeleton B (22.5%).
The clean ordering A < C3 < B confirms the structural-

                                                                    5
                                               Inference-Time Diversity in Lean Provers

                          Condition                     Pass@16              Pass@32              Pass@64
                          A-BASE (i.i.d.)             0/244 (0.0%)         0/244 (0.0%)         0/244 (0.0%)
                          B-BASE (skeletons)          0/244 (0.0%)         0/244 (0.0%)         0/244 (0.0%)
                          A-RL (i.i.d.)             38/244 (15.6%)       42/244 (17.2%)        42/244 (17.2%)
                          B-RL (skeletons)          55/244 (22.5%)       58/244 (23.8%)        60/244 (24.6%)
Table 6. Base model vs. RL model on miniF2F-test. The base model proves zero theorems across all conditions and budgets—inspection
of generated outputs shows it almost always produces sorry or echoes the theorem statement back, indicating it has not learned to
generate valid Lean 4 proofs at all. Mode collapse is therefore an RL-specific phenomenon: RL is what creates proof capability in the first
place, and our intervention recovers proofs that the RL-collapsed model fails to find on its own.



4.5. Generalization Across Models                                       meaningful gain that the topline metric hides. Goedel-
                                                                        Prover (SFT-trained) shows a small negative aggregate. We
The V1.5 RL-vs-Base contrast in Section 4.4 pins mode
                                                                        read these together as evidence that RL-trained provers are
collapse to the RL stage within one model family. To
                                                                        reachable through structural intervention in a way SFT-only
test whether the same A-vs-B pattern generalizes across
                                                                        provers are not, while acknowledging that the size of the
architectures and training pipelines, we extend the pass@16
                                                                        gain is contingent on the specifics of the post-training recipe
comparison to two additional 7B Lean provers: a further RL-
                                                                        and likely on how much capability the i.i.d. baseline has
trained model (DeepSeek-Prover-V2-7B) and one SFT-only
                                                                        already saturated.
model (Goedel-Prover).
                                                                        V2 frontier solves. The +1 aggregate hides the most theo-
The Goedel-Prover null is diagnostic, not contradictory.                retically interesting outcome in the cross-model matrix. We
Goedel-Prover-SFT achieves the highest absolute pass@16                 compute σ−V2 (τ ) on the same leave-one-out construction
of any open-source prover in our study (36.9% seed=1;                   as Section 3.2, dropping all V2 baselines from the diffi-
mean 97.7 ± 6.7 theorems across n=3 seeds, Section 4.6)                 culty score. Three theorems with σ−V2 =0—imo 1960 p2,
using purely supervised fine-tuning on a large synthetic                imo 1962 p2, and numbertheory x5neqy2p4—are
Lean corpus, with no RL stage. Despite this capability                  solved by V2 structured at k=16 but by none of the other
advantage over V1.5-RL, structured hints do not improve its             six sample baselines in our matrix (V1.5-RL, Goedel, V2-
performance—they cost it −10.0 ± 4.4 theorems on average                sample, at multiple k). Two are IMO problems. These are
across the three seeds, with the sign preserved in every seed.          theorems where structured guidance is the only known route
Goedel also shows the same k-scaling plateau we observed                to a solution at this compute scale, and they are exactly the
for V1.5-RL: pass@16 and pass@32 are identical at 36.9%                 kind of frontier finding that the aggregate metric obscures
for the i.i.d. baseline, and the structured condition scales            and that V1.5-RL’s structured condition does not produce
similarly (34.8% → 36.1%). The plateau itself thus appears              (Section 4.3). V2 structured is therefore the first condition
to be a general property of i.i.d. sampling from these models,          in our matrix that opens up the σ=0 frontier, even though its
but the remediability of the plateau via structured hints is            aggregate is flat. We refrain from inferring a general pattern
specific to RL-trained models.                                          from n=3, but flag this as evidence that the aggregate ∆
                                                                        metric is a lossy summary of where structural guidance
A plausible interpretation. SFT and RL induce different                 actually pays off, and as a concrete falsifier for the strong
modes of underexploration. SFT pattern-matches a model                  version of our hypothesis: if frontier theorems were beyond
onto a fixed distribution of training proofs; mode collapse             reach of all current models in this size class, V2 structured
for such a model manifests as tactic-local exploration that             should not have unlocked any.
already starts from a broad set of stems—skeletons add
nothing because the model would have tried those stems                  Solved-set overlap. A paired view of A-RL vs. B-RL at
anyway. RL reward-shapes a model onto a narrower set of                 k=16 further constrains the “more compute would suffice”
high-reward strategies and abandons alternative tactic stems            objection (Figure 3): of the 38 theorems solved by A-RL,
entirely; skeletons help because they force commencement                B-RL solves 35 of them and adds 20 new ones (only 3
from stems the RL policy has been trained away from. The                A-RL solves are lost, consistent with stochastic variation in
asymmetry we observe is consistent with this account, but               shard scheduling). The intervention is therefore near-Pareto-
the magnitude varies with the RL training pipeline. V1.5-RL             dominant on this benchmark and accesses a different region
shows the cleanest aggregate gain (+17); V2-7B is flat on               of the proof space rather than reproducing the baseline’s hits
the aggregate but contributes +3 frontier solves that no i.i.d.         with a different prompt—the 20 unique solves are concen-
baseline of any model in our matrix reaches—a structurally              trated in mathd algebra and mathd numbertheory

                                                                    6
                                                    Inference-Time Diversity in Lean Provers

                              Model            Post-Training                 A pass@16          B pass@16         ∆
                              V1.5-Base        none (pre-train only)      0/244 (0.0%)         0/244 (0.0%)       0
                              Goedel-Prover    SFT                       90/244 (36.9%)       85/244 (34.8%)     −5
                              V1.5-RL          RL                         38/244 (15.6%)     55/244 (22.5%)      +17
                              V2-7B            RL                        126/244 (51.6%)     127/244 (52.0%)     +1
Table 7. Cross-model A vs. B comparison at k=16 on miniF2F-test. The aggregate ∆ varies by model: V1.5-RL shows the largest lift
(+17), V2-7B is flat on aggregate (+1) but solves +3 frontier theorems that no i.i.d. baseline reaches (Section 4.5), and SFT-trained
Goedel-Prover shows −5. Together with V1.5-Base (which has no proof capability with or without hints), the pattern is consistent with
the hypothesis that structured hints remedy the underexploration induced by RL fine-tuning; the magnitude of remediation varies with the
post-training recipe.



           Solved-set overlap on miniF2F-test (V1.5-RL, k=16)                 the prompt varies (B: ±5.6); Goedel retains generation
                                                                              diversity on a fixed prompt (A: ±6.7) and converges when
                                                                              the schedule constrains its openings (B: ±2.5). This second,
                                                                              distinct signature of the RL-vs-SFT distinction is consistent
                                                                              with the broader account in Section 4.5.

                                                                              4.7. Direct Measurement of First-Tactic Collapse
                   20                   35               3                    The plateau in Section 4.1 is behavioural evidence of mode
                                                                              collapse. We now operationalize the phenomenon as a direct
                                                                              distributional measurement on the same per-attempt logs.
                                                                              For each miniF2F theorem we collect the 64 raw outputs
                                                                              produced by V1.5-RL i.i.d. sampling at k=64, extract the
                                                                              first tactic head (the leading identifier on the first line of
                                                                              the proof body), and count its distinct values across the 64
           B-RL                                              A-RL             samples per theorem.
      (skeleton)                                             (i.i.d.)
                                                                              This converts “mode collapse” from a behavioural metaphor
       B-RL: 55/244 (22.5%)                       A-RL: 38/244 (15.6%)
                                                                              into a direct distributional statement. Aggregated across
                                                                              all 244 theorems and 13,159 samples, three tactic heads—
Figure 3. Solved-set overlap of A-RL vs. B-RL at k=16 on V1.5-
                                                                              have (37.2%), rw (14.1%), norm num (14.0%)—account
RL. 20 theorems are solved only by B-RL, 3 only by A-RL, 35 by                for 65.3% of every strategic opening V1.5-RL ever takes.
both.                                                                         The structured schedule injects 15 distinct first-tactic heads
                                                                              by construction, so at the same k=64 LLM-call budget B
                                                                              explores ∼7.5× the strategic-opening surface that the i.i.d.
problems that no i.i.d. sampling at this budget reaches.                      policy actually exercises.

4.6. Seed Variance and Robustness of the Asymmetry                            5. Discussion
The single-seed numbers above could in principle be artifacts                 Mode collapse as the central finding. Our results reframe
of stochastic sampling. To check this, we replicate the A and                 the narrative from “tactic skeletons improve performance” to
B conditions at k=16 across n=3 seeds (seed ∈ {1, 2, 3},                      “RL-trained provers severely underexplore the tactic space at
temperature 0.6) on both V1.5-RL and Goedel-Prover-SFT—                       inference time.” The skeleton schedule is a probe that reveals
the two models that anchor the RL-vs-SFT asymmetry claim.                     this underexploration, not a novel proving architecture. The
Table 8 reports per-seed solve counts and aggregate statistics.               baseline’s plateau at k=32—where 32 additional stochastic
The sign of ∆ is preserved in every one of the six (model,                    samples find zero new proofs—is the most striking evidence
seed) cells—3/3 positive on V1.5-RL, 3/3 negative on                          of this phenomenon.
Goedel—so the cross-model asymmetry is not an artifact of
any individual seed. The two ∆ means separate by ∼ 3.7                        Implications for inference-time scaling. The mode col-
standard deviations of the combined variance, well clear of                   lapse we observe has direct implications for the common
zero. The within-model variance pattern is also informative:                  practice of scaling inference compute. If i.i.d. sampling has
V1.5-RL collapses onto a near-deterministic proof on a                        diminishing returns far earlier than assumed, then simply
fixed prompt (A: ±1.5) and only acquires variance when                        increasing k is wasteful. Our results suggest that structural

                                                                         7
                                               Inference-Time Diversity in Lean Provers

                                       V1.5-RL (RL-trained)                         Goedel-Prover (SFT-trained)
               Seed                A                B       ∆=B−A                  A             B        ∆=B−A
               1              38 (15.6%)       55 (22.5%)       +17            90 (36.9%)    85 (34.8%)       −5
               2              35 (14.3%)       44 (18.0%)       +9            102 (41.8%)    90 (36.9%)       −12
               3              37 (15.2%)       48 (19.7%)       +11           101 (41.4%)    88 (36.1%)       −13
               mean ± std      36.7 ± 1.5      49.0 ± 5.6   +12.3 ± 4.2       97.7 ± 6.7     87.7 ± 2.5   −10.0 ± 4.4
Table 8. Seed-variance study at k=16. The asymmetry is preserved in every seed: ∆ > 0 √   in 3/3 V1.5-RL seeds and ∆ < 0 in 3/3
Goedel seeds. The means separate by +12.3 − (−10.0) = 22.3 theorems with combined std 4.22 + 4.42 ≈ 6.1, a ∼ 3.7σ separation
of V1.5-RL ∆ from Goedel ∆. Note the cross-model variance pattern: on the RL-trained model the A condition is near-deterministic
(±1.5) while B varies (±5.6); on the SFT-trained model the pattern flips (A: ±6.7, B: ±2.5).



           Unique first-tactic heads        theorems                    one-shot decision procedures, which raises the concern that
           1 (deterministic opening)    120 (49.2%)                     the structural gain might just be V1.5-RL underusing Lean’s
           2                             69 (28.3%)                     built-in automation rather than a true distributional shift in
           3                             34 (13.9%)                     its tactic policy. We can check this directly. We classify
           4                             12 (4.9%)                      each of the 24 NEW B-RL k=16 solves (theorems that B-RL
           5–7                            9 (3.7%)                      solves and matched-shard A-RL does not) by whether (i)
           median / mean / max              2 / 1.9 / 7                 the injected tactic was one of the closers above and the
Table 9. Distinct first-tactic heads per theorem across 64 V1.5-        model’s continuation was effectively empty (a no-op like
RL i.i.d. samples at k=64. The median theorem receives only 2           done/rfl or fewer than eight non-trivial tokens), or (ii)
strategic openings; nearly half (49.2%) receives a deterministic        the model produced a substantive continuation beyond the
single opening. Median Shannon entropy is 0.27 bits per theorem
(mean 0.48), versus log2 64 = 6.0 bits under uniform sampling—          skeleton. Only 3 of 24 NEW solves (12.5%) fall in category
observed entropy is ≤ 8% of capacity.                                   (i); the remaining 21 (87.5%) require the model to extend the
                                                                        skeleton with real tactics. The skeleton schedule therefore
                                                                        primarily acts as a prompt prefix that perturbs the model out
                                                                        of its collapsed sampling head, not as a Mathlib-automation
diversity—varying the proof strategy, not just the random               top-up.
seed—is a more efficient axis for scaling inference compute.
This is complementary to tree-based methods like Hyper-
Tree (Lample et al., 2022), which achieve diversity through             RL as both cause and prerequisite. The base model result
explicit search rather than prompt perturbation.                        imposes an unexpected constraint on any account of mode
                                                                        collapse in this domain. Because DeepSeek-Prover-V1.5-
Structural content as a gradient. The bucket-stratified ab-             Base proves zero theorems regardless of skeletons, mode
lation (Section 4.3, Table 4) refines the structural-vs-diversity       collapse cannot be attributed to a pre-existing limitation of
dichotomy into a continuous gradient. The three perturba-               the underlying language model that RL merely amplifies.
tions differ in how much tactic-level structural content they           Instead, RL plays a dual role: it is the stage at which proof
carry: skeleton (literal Lean tactic prefix or a comment                capability is created (the base model has none), and it is
naming a tactic), paraphrase (paraphrased general-purpose               also the stage at which that capability is collapsed onto a
instruction without tactic specifics), comment (a content-free          narrow policy. Any future intervention—whether at training
token marker). The combined easy+trivial NET tracks this                time (e.g., entropy-regularized RL) or inference time (e.g.,
gradient cleanly—+15/0/ − 14 for skeleton, paraphrase,                  learned skeleton retrieval)—must navigate this trade-off
and comment respectively—because that is where V1.5-                    rather than treat collapse as a separable problem.
RL’s gap to other open-source provers concentrates. Equally
informative is the within-skeleton decomposition (Table 5)              Saturation vs. RL-specificity. The cross-model ∆ pattern
and the dedicated C3 ablation: a natural-language tactic-               at k=16 is monotone in baseline headroom: V1.5-RL (A =
suggestion comment alone produces +8 new solves at the                  38) gains +17, V2-7B (A = 126) gains +1, Goedel (A =
attempt-level breakdown and 48/244 (vs. 38 baseline) when               90) loses −10. A pure saturation account predicts this
run as a standalone 16-attempt schedule, while literal Lean             ordering with no appeal to RL vs. SFT, and with only one
tactic prefixes contribute the remaining +12 NEW. Both are              SFT model in the matrix—which is also the highest-baseline
forms of tactic-stem-level structural guidance delivered at             prover—the labels “SFT” and “saturated” are not statistically
different abstraction layers, and both contribute additively.           separable. We take this objection seriously, and the cross-
Several of the 15 skeletons (simp, aesop, norm num,                     model evidence in Section 4.5 is best read as compatible
ring, linarith, nlinarith, ring nf) function as                         with both accounts rather than as decisive for the RL-specific

                                                                    8
                                           Inference-Time Diversity in Lean Provers

reading. What the cross-model data can’t explain on its              shown that the collapse it reveals is RL-specific in two distinct
own is the V1.5-Base control: a non-RL prover at the                 senses: it is absent in the non-RL V1.5-Base variant (which
same pretrained scale with A = 0 and B = 0 at every                  has no proof capability at all), and it is partially remediated by
tested k (Section 4.4). The within-architecture base-vs-RL           structural guidance only on RL-trained models in our cross-
contrast is the cleanest evidence we have that RL is what            model matrix—never on the SFT-trained Goedel-Prover. The
creates the policy whose collapse we are diagnosing. We              magnitude of the remediation varies sharply by post-training
frame the cross-model results as a consistency check on              recipe (+17 on V1.5-RL; +1 aggregate but +3 frontier
top of this within-architecture result, not as an independent        solves on V2-7B; −10.0 ± 4.4 on Goedel-Prover-SFT across
confirmation; a matched-capability SFT control at lower              n=3 seeds), which we read as evidence that the underlying
baseline pass@k would be the natural next experiment.                phenomenon is real but pipeline-contingent rather than
                                                                     universal. The most natural follow-ups are (i) converting
Static inference vs. agentic systems. The setup studied              the diagnostic from a sampling-plateau metaphor into a
here is deterministic, zero-shot, single-pass: each attempt is       direct first-tactic-distribution measurement on the existing
a single forward pass of the model on a prompt with no com-          logs; (ii) replacing the hand-designed 15-skeleton schedule
piler feedback, proof-state reflection, or interactive repair.       with a learned, per-theorem skeleton retriever, which the
This is a deliberate design choice—we want to isolate the            gradient in Section 4.3 suggests should outperform the
model’s intrinsic sampling behavior from the orchestrator’s.         fixed grid; and (iii) closing the loop at training time via
Modern Lean systems built around agentic loops (interac-             entropy-regularized or skeleton-conditioned RL, since the
tive compiler diagnostics, retrieval over Mathlib lemmas,            V1.5-Base control implies that any training-time intervention
multi-pass proof repair) already mitigate this collapse in           will be constrained by the dual role RL plays in creating and
practice, and the diagnostic we present is most useful to that       collapsing the proof policy.
line of work as a measurement of the underlying model that
the harness is layered on top of. Extending our schedule +           References
first-tactic-distribution measurement to (i) reasoning provers
with longer trajectories and (ii) interactive harnesses around       Achim, T. et al. Aristotle: Imo-level automated theorem
closed-weight frontier models is the next obvious step, but is         proving. arXiv preprint arXiv:2510.01346, 2025.
out of scope for a single-model diagnostic study at this size.
                                                                     Chen, L., Gu, J., Huang, L., et al. Seed-prover: Deep and
                                                                       broad reasoning for automated theorem proving. arXiv
Other limitations. The cleanest within-architecture iso-               preprint arXiv:2507.23726, 2025.
lation of RL’s effect (Section 4.4) is only possible on V1.5
because no other Lean prover in our matrix releases a                de Moura, L. and Ullrich, S. The Lean 4 theorem prover
paired non-RL base checkpoint. A third RL replication on               and programming language. In Automated Deduction –
Kimina-Prover (Wang et al., 2025) was attempted but cut                CADE 28, pp. 625–635. Springer, 2021.
for compute reasons after an output-extractor fix; a partial
sample-baseline produced 20/35 trials (57%) and is de-               Han, J. M., Rute, J., Wu, Y., Ayers, E., and Polu, S. Proof arti-
ferred to future work. Cross-model k-scaling beyond k=16               fact co-training for theorem proving with language models.
is currently established on V1.5-RL (k ∈ {16, 32, 64}) and             International Conference on Learning Representations
Goedel-Prover (k ∈ {16, 32}); extending V2 to k ≥ 32, eval-            (ICLR), 2022.
uating on ProofNet/PutnamBench, exploring constrained
                                                                     Jiang, A. Q., Welleck, S., Zhou, J. P., Li, W., Liu, J.,
decoding beyond the first tactic, and replacing the hand-
                                                                        Jamnik, M., Lacroix, T., Wu, Y., and Lample, G. Draft,
selected 15×8 grid with a learned per-theorem retriever
                                                                        sketch, and prove: Guiding formal theorem provers with
are all natural next steps. Multi-seed coverage at k=16 is
                                                                        informal proofs. In International Conference on Learning
n=3 (Section 4.6); the headline k=32 → k=64 plateau is
                                                                        Representations (ICLR), 2023.
single-seed and would benefit from replication. The first-
tactic-distribution measurement (Section 4.7) is currently           Kirk, R., Mediratta, I., Nalmpantis, C., Luketina, J., Hambro,
V1.5-RL only; extending it to V2-7B and Goedel would                   E., Grefenstette, E., and Raileanu, R. Understanding the
let us test whether first-tactic-head concentration tracks the         effects of RLHF on LLM generalisation and diversity. In
RL-vs-SFT asymmetry we already observe at the solve-rate               International Conference on Learning Representations
level (Section 4.6).                                                   (ICLR), 2024. arXiv:2310.06452.

6. Conclusion                                                        Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A.,
                                                                       Roziere, B., and Szafraniec, M. HyperTree proof search
We have used a deterministic 15-skeleton schedule as a probe           for neural theorem proving. Advances in Neural Informa-
to diagnose mode collapse in RL-trained Lean provers, and              tion Processing Systems, 35:26337–26349, 2022.

                                                                 9
                                          Inference-Time Diversity in Lean Provers

Lin, Y., Tang, S., Lyu, B., et al. Goedel-prover: A frontier         A. Skeleton Schedule (Tactics × Goal Hints)
  model for open-source automated theorem proving. arXiv
  preprint arXiv:2502.07640, 2025.                                   The structured-skeleton schedule is a deterministic 15 ×
                                                                     8 = 120 grid: 15 tactic skeletons crossed with 8 goal-hint
Polu, S. and Sutskever, I. Generative language model-                comments (one of which is empty). At budget k, the schedule
  ing for automated theorem proving. arXiv preprint                  advances by tactic-index first and by hint-index second:
  arXiv:2009.03393, 2020.                                            attempts 0 . . . 14 use the 15 distinct skeletons paired with
                                                                     hint index 0 (empty); attempts 15 . . . 29 repeat the skeletons
Ren, Z., Shao, Z., Song, J., et al. DeepSeek-Prover-V2:
                                                                     paired with hint index 1; and so on. Each of the 120 attempts
  Advancing formal mathematical reasoning via reinforce-
                                                                     is a distinct (skeleton, hint) prompt configuration.
  ment learning for subgoal decomposition. arXiv preprint
  arXiv:2504.21801, 2025.
                                                                     Tactic skeletons (15 total). The Python-source ordering
Sivakumar, J. A., Borchert, P., Cardenas, R., et al. Con-            used by the perturbation function is reproduced below; index
  jecturing: An overlooked step in formal mathematical               i in this list is TACTIC SKELETONS[i] in the schedule.
  reasoning. arXiv preprint arXiv:2510.11986, 2025.
Thakur, A., Tsoukalas, G., Wen, Y., Xin, J., and Chaudhuri,            0. (empty) — no tactic prefix
  S. COPRA: In-context learning for proving theorems with
                                                                       1. simp
  llms. arXiv preprint arXiv:2310.04353, 2023.
The mathlib Community. The Lean mathematical library.                  2. intro
  Proceedings of the 9th ACM SIGPLAN International                     3. intros
  Conference on Certified Programs and Proofs, pp. 367–
  381, 2020.                                                           4. constructor
Trinh, T., Wu, Y., Le, Q. V., He, H., and Luong, T. Solv-              5. refine ?
  ing olympiad geometry without human demonstrations.
  Nature, 625(7995):476–482, 2024.                                     6. refine ⟨? , ? ⟩

Wang, H., Unsal, M., Lin, X., et al. Kimina-prover preview:            7. aesop
 Towards large formal reasoning models with reinforce-
 ment learning. arXiv preprint arXiv:2504.11354, 2025.                 8. norm num

Wu, F., Xuan, W., Lu, X., Liu, M., Dong, Y., Harchaoui, Z.,            9. linarith
 and Choi, Y. The invisible leash: Why RLVR may or may
                                                                     10. nlinarith
 not escape its origin. arXiv preprint arXiv:2507.14843,
 2025.                                                               11. ring
Xin, H. et al. Deepseek-prover-v1.5: Harnessing proof                12. ring nf
  assistant feedback for reinforcement learning and monte-
  carlo tree search. arXiv preprint arXiv:2408.08152, 2024.          13. simp followed by try aesop
Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P., Yu,            14. simp followed by try nlinarith
  S., Godil, S., Prenger, R., and Anandkumar, A. Leandojo:
  Theorem proving with retrieval-augmented language mod-
                                                                     Goal-hint comments (8 total). Goal hints are short
  els. Advances in Neural Information Processing Systems,
                                                                     natural-language tactic suggestions injected as Lean
  36:10065–10081, 2023.
                                                                     comments (/-- Hint: <hint text> --/) before
Yue, Y., Chen, Z., Lu, R., Zhao, A., Wang, Z., Yue, Y., Song,        the theorem statement.       Index j corresponds to
  S., and Huang, G. Does reinforcement learning really               GOAL HINTS[j]; the hint at index 0 is empty (no comment
  incentivize reasoning capacity in LLMs beyond the base             is prepended).
  model? arXiv preprint arXiv:2504.13837, 2025. ICML
  2025 Workshop AI4Math Best Paper; NeurIPS 2025 Best                  0. (empty) — no goal-hint comment
  Paper Runner-Up.
                                                                       1. “Start by simplifying the goal and hypotheses using
Zheng, K., Han, J. M., and Polu, S. miniF2F: a cross-system               simp.”
  benchmark for formal Olympiad-level mathematics. Inter-
  national Conference on Learning Representations (ICLR),              2. “If the goal is an implication or forall, introduce vari-
  2022.                                                                   ables.”

                                                                10
                                            Inference-Time Diversity in Lean Provers

  3. “If the goal is a conjunction or existence, build it using        B.2. C2: Irrelevant Comment Prefixes
     constructor or refine.”
                                                                       Each comment is prepended before the theorem statement:
  4. “If arithmetic is involved, try norm num, then
     linarith or nlinarith.”                                            1. /- approach alpha -/
  5. “If the goal looks routine, try aesop after simplifica-            2. /- strategy beta -/
     tion.”
                                                                        3. /- method gamma -/
  6. “If the proof requires rewriting, look for a lemma in the
     context and rewrite.”                                              4. /- path delta -/

  7. “If the goal involves recursion on naturals, consider              5. /- route epsilon -/
     induction.”
                                                                        6. /- attempt zeta -/

Pairing rule. Attempt i in the schedule uses tactic index               7. /- angle eta -/
i mod 15 and hint index ⌊i/15⌋ mod 8. Consequently, at
k=16 the only repeated tactic-index is the wraparound to                8. /- direction theta -/
tactic 0 (empty) at attempt 15, now paired with hint 1 (“Start
                                                                        9. /- variant iota -/
by simplifying. . . ”); this is the empty-tactic + hint-comment
configuration analyzed in Table 5.                                     10. /- form kappa -/

                                                                       11. /- mode lambda -/
B. Diversity Ablation Prompts
B.1. C1: Instruction Paraphrases                                       12. /- plan mu -/

Each paraphrase is injected as a Lean block comment before             13. /- way nu -/
the standard header. The 16 variants are:
                                                                       14. /- style xi -/

  1. “Prove the following theorem in Lean 4:”                          15. /- view omicron -/

  2. “Complete this Lean 4 proof:”                                     16. /- take pi -/

  3. “Find a formal proof for the following:”
                                                                       C. Environment
  4. “Show that the following statement holds:”
                                                                         • Lean: v4.9.0-rc1 (matching DeepSeek-Prover-V1.5
  5. “Write a tactic proof for this theorem:”                              training environment)

  6. “Construct a formal proof of the following:”                        • Mathlib:                       commit
                                                                           7fa489a5cbf3c4f08d36e1e0b5dee4d761fdbd9b
  7. “Provide a Lean 4 proof for:”
                                                                         • Models:
  8. “Demonstrate the following result formally:”
                                                                              – deepseek-ai/DeepSeek-Prover-V1.5-RL,
  9. “Give a complete tactic proof:”                                            deepseek-ai/DeepSeek-Prover-V1.5
                                                                                (V1.5-Base)
10. “Prove this result using Lean 4 tactics:”
                                                                              – deepseek-ai/DeepSeek-Prover-V2-7B
11. “Formalize a proof of the following theorem:”                             – Goedel-LM/Goedel-Prover-SFT
12. “Establish the following in Lean 4:”                                 • Inference: vLLM, single A100 per run. V1.5 ran on
                                                                           v0.18 / A100 80GB; V2 and Goedel ran on v0.10.2 /
13. “Derive a proof for the following statement:”                          A100 40GB with --enforce-eager (sufficient in
14. “Supply a formal tactic proof for:”                                    both cases).

15. “Verify the following theorem in Lean 4:”                            • Decoding (V1.5, Goedel; completion mode): temper-
                                                                           ature 0.6, top-p 0.95, max 1024 tokens per attempt; no
16. “Prove the following:”                                                 chat template.

                                                                  11
                                    Inference-Time Diversity in Lean Provers

• Decoding (V2; reasoning mode): temperature 0.6,
  top-p 0.95, max 8192 tokens per attempt; apply model
  chat template; extract last ‘‘‘lean4 fenced block
  from response.
• Verification: lake env lean --json, 120s
  timeout, sorry rejection.




                                                         12
