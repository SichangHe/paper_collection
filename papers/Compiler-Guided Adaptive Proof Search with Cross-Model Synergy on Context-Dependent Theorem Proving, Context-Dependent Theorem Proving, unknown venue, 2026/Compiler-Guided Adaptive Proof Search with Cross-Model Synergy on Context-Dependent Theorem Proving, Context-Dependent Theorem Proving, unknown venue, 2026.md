                                            Compiler-Guided Adaptive Proof Search with Cross-Model Synergy on
                                                          Context-Dependent Theorem Proving

                                                    Zhuo Liu                              Ding Yu               Hangfeng He
                                              University of Rochester              University of Rochester  University of Rochester
                                            zhuo.liu@rochester.edu                dyu18@ur.rochester.edu hangfeng.he@rochester.edu



                                                               Abstract                         project-level Lean projects introduces additional
                                                                                                challenges. Real-world project-level proofs of-
                                             Theorem proving in real-world Lean 4 projects
                                                                                                ten depend on local definitions, project-specific
arXiv:2608.18084v2 [cs.CL] 4 Sep 2026




                                             is challenging because proofs often depend
                                             on project-specific context. While iterative       lemmas, naming conventions, and proof patterns
                                             refinement can use compiler errors to re-          spread across the surrounding context (Tooby-
                                             pair failed proofs, reusing failed attempts re-    Smith, 2025). Recent efforts on project-level Lean
                                             quires careful search control: some proofs         theorem proving (Hu et al., 2024; Kumarappan
                                             provide better starting points than others, and    et al., 2024; Poiroux et al., 2025a) show that even
                                             later revisions may degrade a partially cor-       strong provers still struggle in this setting.
                                             rect proof. We propose a compiler-guided
                                                                                                   Most existing methods rely on independent
                                             proof search framework that balances explo-
                                             ration and exploitation. It explores diverse       sampling: a prover generates multiple complete
                                             starting points through dual-model generation      proof candidates, and success is measured by
                                             and stagnation-triggered resampling, while ex-     pass@k (Chen et al., 2021; Ren et al., 2025), which
                                             ploiting promising proof states through current-   counts whether any candidate verifies. However,
                                             best refinement guided by compiler-grounded        this paradigm treats the compiler as a final filter
                                             pairwise comparison. Experiments on seven          rather than a source of feedback for guiding later
                                             real-world Lean 4 projects from miniCTX-
                                                                                                attempts. As a result, failed proofs are discarded
                                             v2 show that our method achieves a better
                                             effectiveness–efficiency tradeoff than pass@k      even when they contain useful partial progress.
                                             baselines. Within the pass@32 budget, our          In context-dependent formal proving, this partial
                                             method improves average pass rate by 12.8 per-     progress may include a relevant project-specific
                                             centage points while reducing LLM calls by         lemma, a promising proof outline, or a nearly cor-
                                             21.9%.                                             rect tactic sequence. This forces later samples to
                                                                                                start largely from scratch.
                                        1    Introduction
                                                                                                   Compiler-guided refinement (First et al., 2023;
                                        Large language models (LLMs) are increasingly           Zhou et al., 2025) offers a natural way to reuse
                                        used as agents that revise their outputs based on       failed proofs, but effective refinement is not guaran-
                                        feedback from external environments (Yang et al.,       teed. Execution feedback can improve code genera-
                                        2023; Chen et al., 2023; First et al., 2023). Formal    tion and agentic problem solving (Chen et al., 2021;
                                        theorem proving is well suited for studying this        Yang et al., 2023; First et al., 2023), but prior work
                                        process: in Lean (Moura and Ullrich, 2021), every       also shows that self-correction is not reliably ben-
                                        candidate proof can be checked by a compiler, and       eficial in general (Kamoi et al., 2024; Adnan and
                                        failed attempts receive structured feedback from        Kuhn, 2025). Similarly, in compiler-guided proof
                                        the compiler (Chen et al., 2023; First et al., 2023).   refinement, additional revision does not necessarily
                                           Recent neural theorem provers have made sub-         improve the proof state. A revision may fix one er-
                                        stantial progress on formal reasoning problems.         ror while introducing another, or degrade a partially
                                        Systems such as DeepSeek-Prover-v2 (Ren et al.,         correct proof. Moreover, refinement is also sensi-
                                        2025) and AlphaProof (Hubert et al., 2026) show         tive to the starting proof: some failed attempts are
                                        that neural provers can generate strong proof at-       close to repairable, while others lead to stuck trajec-
                                        tempts, especially on olympiad-style and library-       tories even after many refinements. These observa-
                                        based benchmarks (Zheng et al., 2021; Tsoukalas         tions suggest an exploration–exploitation tradeoff
                                        et al., 2024). However, proving theorems inside         between trying new proofs and improving existing
ones. An effective prover should therefore explore        2     Related Work
diverse starting proofs, preserve useful intermedi-
                                                          2.1    Context-Dependent Theorem Proving
ate proofs during refinement, and restart when the
current path stops improving. In practice, Lean-          Context-dependent theorem proving studies prob-
specialized provers and general-purpose reasoning         lems where the proof depends on surrounding
models exhibit complementary strengths on project-        project context. miniCTX (Hu et al., 2024)
level problems: the former generate precise tactic        introduces a benchmark built from seven real-
sequences but underutilize surrounding project con-       world Lean projects, highlighting the difficulty of
text, while the latter better leverage this context but   theorem proving with long project-level context.
more often produce ill-typed tactics (Wang et al.,        RLMEval (Poiroux et al., 2025a) evaluates neu-
2024).                                                    ral theorem proving and proof autoformalization
    To this end, we propose a compiler-guided adap-       on research-level theorems from Lean Blueprint
tive proof search framework for context-dependent         formalization projects. LeanAgent (Kumarappan
Lean theorem proving. The framework combines              et al., 2024) further studies this setting across di-
cross-model exploration with controlled refine-           verse Lean repositories. Our work targets this real-
ment. For exploration, it draws candidates from           world setting and focuses on how to reuse failed
two complementary models: a Lean-specialized              proof attempts.
prover that provides tactic-level precision and a
                                                          2.2    Whole-Proof Generation
general-purpose reasoning model that can better
use long project context. A compiler-grounded             Whole-proof generation produces a complete proof
pairwise comparison selects the more promising            in one pass, rather than predicting the proof tac-
candidate as the current-best proof state. For ex-        tic by tactic. Recent formal reasoning systems
ploitation, the system refines this current-best proof    have shown strong progress. AlphaProof (Hubert
using compiler feedback, but accepts a revision           et al., 2026) and AlphaGeometry (Trinh et al.,
only when pairwise comparison indicates improve-          2024) demonstrated that AI systems can reach
ment. When refinement stops making progress,              medal-level performance on International Math-
it returns to exploration and resamples candidates        ematical Olympiad (IMO) problems, while neu-
from both models.                                         ral provers (Wang et al., 2025; Ren et al., 2025;
                                                          Chen et al., 2025; Lin et al., 2025) have achieved
    Our contributions are as follows:
                                                          strong results on olympiad-style benchmarks such
                                                          as miniF2F (Zheng et al., 2021) and Putnam-
   • We introduce a hybrid proof search frame-            Bench (Tsoukalas et al., 2024). Other systems use
     work that uses complementary specialist and          verifier or compiler feedback to repair failed com-
     generalist models for exploration, and com-          plete proofs (Zhou et al., 2025; First et al., 2023;
     bines them with current-best refinement and          Lu et al., 2025; Wang et al., 2026), showing that
     stagnation-triggered resampling.                     failed attempts can provide useful information for
                                                          later refinement. Our work builds on whole-proof
   • We analyze proof search trajectories in              generation, but focuses on search over failed proofs:
     context-dependent Lean theorem proving,              we use complementary models to find diverse start-
     showing that success depends strongly on the         ing points and compiler-grounded comparison to
     starting proof and on preserving useful inter-       preserve promising proof states.
     mediate proof states.
                                                          2.3    Tactic Search-Based Proving
                                                          A complementary line of work studies tactic-level
   • We evaluate our framework on seven Lean 4
                                                          proof search, where a model predicts the next tactic
     projects from miniCTX-v2 and 84 formaliza-
                                                          from the current proof state. Many systems guide
     tion problems from RLMEval-FLT3, showing
                                                          this process with best-first search (Xin et al., 2025;
     that it achieves a better pass rate–LLM call
                                                          Wu et al., 2024; Polu and Sutskever, 2020) or re-
     tradeoff.
                                                          lated tree-search methods (Coulom, 2006). For ex-
                                                          ample, Lample et al. (2022) propose an AlphaZero-
Code. The code is available at https://github.            style hypertree proof-search algorithm to improve
com/joeliuz6/lean_proof_search.                           search efficiency. LeanProgress (George et al.,
                                   stagnation ≥ N (Section 3.4)


                                      candidate A                                refined candidate
                                                                                   s*
                                                              Judge

                                      candidate B
                                                                  VS



                                                                                 Current best s*
                Dual Generation                       Pairwise Comparison                               Refinement
                 Section 3.2                               Section 3.3                                   Section 3.3


                      >_ Lean 4 Compiler                   Errors             Auto tactics           verified ✓
        Input                                 Verification & Feedback (Section 3.1)                                    Verified proof



Figure 1: Overview of our framework. Exploration (left) generates two diverse candidates via a generalist and
a specialist. Exploitation (right) maintains a single current-best proof s∗ and drives it toward verification: each
repair produces a proposal, and an LLM judge decides whether to accept it. When refinement stagnates for N
consecutive rounds, the system re-enters exploration and draws fresh candidates from both models. The Verification
& Feedback layer (bottom) provides structured error feedback, tactic suggestions and verification signals.


2025) trains a model to predict proof progress and                           as a proposal that may or may not replace s∗
uses this signal to guide search. BFS-Prover (Xin                            (§3.3).
et al., 2025) introduces a scalable best-first search
framework with preference optimization over state–
                                                                       Pairwise comparison serves as the search con-
tactic pairs and length normalization. Our work
                                                                       troller in the whole process: it selects the stronger
is different in granularity: rather than searching
                                                                       initial proof during exploration, decides whether a
over individual tactics, we search over whole-proof
                                                                       refined proposal should replace s∗ during exploita-
candidates. This allows us to combine exploration
                                                                       tion, and chooses a new starting point after resam-
from multiple proof generators with refinement of
                                                                       pling (§3.3).
promising proof states.
                                                                          Algorithm 1 in Appendix A shows the full search
3    Compiler-Guided Adaptive Proof                                    procedure.
     Search
                                                                       3.1   Compiler-Grounded Feedback
Overview. Given a theorem statement s and its
surrounding Lean 4 project context C, the system                       We use the Lean 4 compiler not only as a verifier,
generates a verified proof p. C is the source content                  but also as a source of structured error feedback
before the target theorem in the project file. We                      and lightweight automatic tactics.
design a compiler-guided search procedure that or-
chestrates two complementary off-the-shelf models                      Structured error feedback. When a proof fails,
with comparison-based refinement.                                      we extract structured errors: the error position, and
   We view whole-proof generation as a search                          the error message, aligned to the specific tactic
problem over proof candidates. The system main-                        line that produced it. This gives models precise
tains a single current-best proof state s∗ and alter-                  line-level grounding instead of file-level noise. The
nates between two phases, as illustrated in Figure 1:                  error message is used by both the repair model and
                                                                       the pairwise comparison controller.
    • Exploration proposes diverse starting points
      by drawing candidates from two models with                       Lightweight automatic solving. In our work, an
      complementary strengths: a generalist and a                      AUTO S OLVE module tries a small set of auto tac-
      specialist (§3.2), and re-invoking both when-                    tics: deterministic closing tactics and Lean’s built-
      ever the search stagnates (§3.4).                                in lemma search to close trivial goals. More details
                                                                       can be found in Appendix C. Proofs solved this
    • Exploitation refines the current-best proof                      way exit the search without any model call, saving
      using compiler feedback, treating each repair                    budget for harder goals.
                                                                   R1       R2     R3        R4   R5               R1   R2        R3   R4   R5
3.2   Exploration: Dual-Model Candidate
      Generation                                         WP0        1       1      22        1     1    WP5                       27   26
A single model often produces similar errors across      WP1                1      2         1     1    WP6                                 26
repeated failed samples. Therefore, we generate          WP2                2      1         6     1    WP7                       18        14
one candidate from each of two complementary
                                                         WP3        2       1      5         1     1    WP8             21        25   11   30
models to add meaningful diversity.
                                                         WP4       11       2                     12    WP9             12        24   18   17
Generalist. We use a strong general-purpose rea-
soning model as the generalist, e.g., GPT-5 (Singh
                                                               1        5               10        15          20             25        30        35
et al., 2025). Its long-context capacity makes it                  Iterations to success          ( = no verified proof within 32 iterations )
suitable for using project-specific definitions and
dependencies, although it may still produce invalid      Figure 2: Empirical refinement results of one the-
Lean syntax or tactic usage (Wang et al., 2024).         orem with different initial attempts. One theo-
                                                         rem, 10 wrong proofs (WP) as starting points (rows),
Specialist. We         use    a   Lean-specialized       each evaluated with 5 independent refinement runs
prover (Wang et al., 2025; Ren et al., 2025)             (columns) with a 32-iteration budget. Cells show
as the specialist, e.g., Deepseek Prover (Ren et al.,    iterations to success; × marks failure. Theorem:
2025). Because it is trained on large-scale Lean         Set_EAnnulus_oc_subset_co in CARLESON. More
proof data, it is better aligned with Lean syntax,       examples can be found in Figure 9 and Figure 10 in
                                                         Appendix B.1.
tactics, and common proof patterns, but may be
less effective at using long project-level context.
The two models often perform in different ways:          steps, while others (WP5, WP6) rarely succeed
the generalist is stronger at context understanding,     under the same budget. We further verify in Ap-
while the specialist is stronger at formal proof syn-    pendix B.1 that this effect is not only due to sam-
tax. As a result, they tend to produce different kinds   pling randomness: variation across different start-
of proof attempts rather than repeated variations of     ing proofs is larger than variation across repeated
the same mistake. In our method, each candidate          runs from the same starting proof. Second, the ef-
is verified immediately after generation; if either      fect of refinement is not consistent across different
proof succeeds, the system returns without refine-       runs. Even when starting from the same wrong
ment. Otherwise, pairwise comparison selects the         proof, different runs can follow different trajecto-
more promising proof as the initial s∗ .                 ries: some quickly reach a correct proof, while
                                                         others drift away and fail.
3.3   Exploitation: Comparison-Based
      Current-Best Refinement                            Propose-then-accept refinement. Instead of al-
                                                         ways replacing the current proof with a new revi-
Why refinement needs search control. Stan-
                                                         sion, we use a propose-then-accept strategy. At
dard iterative refinement (First et al., 2023) treats
                                                         each step, the repair model generates a revised
each revision as an unconditional state update:
                                                         proof s̃t+1 from the current-best proof s∗t and its
              st+1 = R EFINE(st , et ),           (1)    compiler errors e∗t :

using compiler error feedback et , and overwrit-                                 s̃t+1 = R EFINE(s∗t , e∗t ),                                    (2)
ing st regardless of whether st+1 is actually better.                            s∗t+1 = B ETTER(s∗t , s̃t+1 ).                                  (3)
However, refinement is not always an improvement.
A revised proof may fix one error but introduce new      If the new proof verifies, the search stops. Other-
ones, or move away from a previously promising           wise, B ETTER decides whether the new proof is
strategy. While a single bad revision may not mat-       more promising than the current-best proof.
ter much, these mistakes can accumulate over many
rounds and gradually push the search away from a         Pairwise comparison. B ETTER is an LLM judge
correct proof.                                           that compares two proofs together with their com-
   Figure 2 illustrates two important patterns. First,   piler errors. It chooses the proof that looks more
the choice of starting proof matters a lot. For the      likely to succeed after future refinement, based on
same theorem, some wrong proofs (WP0–WP3)                factors such as current progress, error severity, and
can usually be repaired within a few refinement          overall proof strategy. If the new proof is accepted,
                                   carleson                                 foundation                                                     mathlib                                                                   Seymour
                                                              65                                           60                                                                             90
                55                                                                                         55
                50                                            60                                           50                                                                             80
Pass Rate (%)



                45                                                                                         45                                                                             70
                                                              55
                40                                                                                         40
                                                                                                                                                                                          60
                                                              50                                           35
                35
                                                                                                           30                                                                             50
                30                                            45                                           25                                                                             40
                25
                     0    5   10    15    20   25        30        0   5   10     15     20   25    30           0             5      10       15         20        25         30              0        5       10      15      20       25        30
                                   LLM Calls                                    LLM Calls                                                  LLM Calls                                                                 LLM Calls
                                   ConNF                                           FLT                     70
                                                                                                                                           HepLean                                        65
                                                                                                                                                                                                                     Average
                50                                            60
                45                                                                                                                                                                        60
                                                              50                                           60
                40                                                                                                                                                                        55
Pass Rate (%)




                                                              40                                           50                                                                             50
                35
                                                                                                                                                                                          45
                30                                            30                                           40
                                                                                                                                                                                          40
                25                                            20
                                                                                                           30                                                                             35
                20
                                                              10                                                                                                                          30
                15                                                                                         20
                     0        10         20         30             0       10          20          30            0             5      10       15         20        25         30              0        5       10      15      20       25        30
                                   LLM Calls                                    LLM Calls                                                  LLM Calls                                                                 LLM Calls
                                                     Generalist                 Specialist               Dual_model                                   React-style                                   Ours

  Figure 3: Pass rate (%) vs. LLM calls across seven Lean 4 projects from miniCTX-v2. Gray dashed line is pass@32.


  it becomes the new current-best proof s∗ . Oth-                                                                            3.5
                                                                                                                                           Ours: Generalist proof
                                                                                                                                           Ours: Specialist proof                                                    $3.32

  erwise, the system keeps the old one. Rejected                                                                             3.0
                                                                                                                                           Ours: pairwise comparison
                                                                                                                                           GPT-5-mini pass@32
                                                                                                                                                                                            $3.07
                                                                                                                                                                                                                $3.26
                                                                                                                                                                                                                                 $2.70
  proposals increase a stagnation counter nstag , while                                                                      2.5
                                                                                                                                                                                     $2.54                                   $2.49              $2.43
                                                                                                                Cost (USD)




                                                                                                                                                            $2.20
  accepted proposals reset it to zero.                                                                                       2.0             $1.81
                                                                                                                                                                             $1.98                      $1.95                            $1.96
                                                                                                                                                      $1.73
                                                                                                                                                                    $1.63
                                                                                                                                                                                                    $1.44
                                                                                                                             1.5
  3.4                    Returning to Exploration:                                                                           1.0
                         Stagnation-Aware Resampling                                                                         0.5
                                                                                                                                       $0.65




  Pairwise comparison helps preserve promising                                                                               0.0
                                                                                                                                         r              n                n             ib             T           n       F                 g
                                                                                                                                      ou             ea         at
                                                                                                                                                                    io               hl             FL         so      nN                Av
  proof states, but it cannot fix a fundamentally bad                                                                             ym
                                                                                                                                               ep
                                                                                                                                                  L          d                  at                       a rle      Co
                                                                                                                               Se          H              un                 M                         C
  proof strategy. Sometimes the current proof gets                                                                                                    Fo

  stuck in a region where local refinement no longer
                                                                                                            Figure 4: Total LLM cost breakdown per project under
  helps: new revisions keep getting rejected for sev-
                                                                                                            32 average LLM calls. Specialist DeepSeek-Prover-v2-
  eral iterations, and there are increasing errors in                                                       7B is self-hosted; its cost is estimated at the generalist’s
  refinement. Resampling serves as a fallback mech-                                                         per-token price (higher than the specialist) for a conser-
  anism in this situation.                                                                                  vative comparison.

  Trigger and restart. When the stagnation
  counter nstag reaches a threshold N , the system                                                          Lean 4 projects. The projects differ in mathemati-
  returns to exploration. It generates fresh candidates                                                     cal domain, proof style and dependency structure,
  from both models, verifies them, and uses B ETTER                                                         making miniCTX-v2 a useful benchmark for eval-
  to choose a new current-best proof s∗ . Refinement                                                        uating whether proof search methods generalize
  then continues from this new starting point. We re-                                                       across different Lean environments. We report our
  sample from both models instead of only the model                                                         results on the test split.
  that produced the stagnated proof. This allows dif-
  ferent proof strategies and helps avoid repeatedly                                                        RLMEval-FLT3. We also evaluate our method
  exploring the same bad region of proof space.                                                             on the FLT3 subset of RLMEval (Poiroux et al.,
                                                                                                            2025a), which studies real-world formalization
  4                  Experimental Setup                                                                     problems. FLT3 contains 84 theorems from a
                                                                                                            Lean 4 formalization of Fermat’s Last Theorem
  4.1                    Benchmark                                                                          for n = 3, each paired with a natural language
  miniCTX-v2. Our main benchmark is miniCTX-                                                                proof. Following RLMEval, we evaluate in the
  v2 (Hu et al., 2024), a context-dependent theorem                                                         easy setting, where all project lemmas are available
  proving benchmark built from seven real-world                                                             during proof generation.
                                                   Pass rate (%) per project
           Method                                                                                                                Avg.
                                Carleson ConNF   FLT     Foundation HepLean Mathlib Seymour
           Gemini-2.5-Flash      44.00   28.00   35.29     52.00                    38.00        40.00          72.00            44.18
           DeepSeek-Prover-v2    42.00   30.00   47.06     54.00                    42.00        42.00          70.00            46.72
           Ours                  48.00   34.00   50.00     60.00                    54.00        46.00          78.00            52.86
             avg calls           14.86   16.46   15.03     12.28                    14.92        16.12            8.98           14.09


Table 1: Pass rate (%) on miniCTX-v2 across seven projects with Gemini-2.5-Flash as the Generalist. Results of
full proof generation are pass@16. Our method additionally reports average LLM calls per theorem (gray).


4.2   Models                                                                                         Generalist 15.0 + Specialist 2.2 + Cmp 14.5
                                                                           50
Unless otherwise noted, we choose DeepSeek-                                                                     Generalist 8.4 + Specialist 1.4 + Cmp 8.0




                                                           Pass rate (%)
                                                                           40                             Generalist 6.3 + Specialist 1.3 + Cmp 5.9
Prover-v2-7B (Ren et al., 2025) as the specialist
and GPT-5-mini (Singh et al., 2025) as the gen-                            30
eralist, which also serves as the repair model and                         20                                                             Generalist
pairwise judge.                                                                                                                           Specialist
                                                                           10                                                             Ours
4.3   Baselines                                                                 0    5      10           15         20          25          30         35
                                                                                                         LLM calls
Single-model generation (Generalist / Special-
ist). We follow the standard pass@k (Chen et al.,          Figure 5: Pass rate (%) vs. LLM calls on RLMEval-FLT3
2021) protocol: each model draws k independent             with informal proof guidance. Text labels show average
                                                           calls from the generalist, specialist, and pairwise com-
candidates and succeeds if any verifies, consistent        parison (Cmp).
with prior evaluations (Ren et al., 2025).
Dual-model generation (Dual_Model). Both
                                                           For a fair comparison, we use low reasoning ef-
models sample independently, and their outputs
                                                           fort for the generalist model. For the specialist,
are combined into a single candidate set. At a bud-
                                                           we set temperature 1 with top-p 0.95 to encourage
get of 2k calls, each model contributes k samples;
                                                           diverse proofs. Full details are in Appendix C.
it succeeds if any candidate verifies.
Agentic baseline (ReAct-Style). We implement               5                Results
a ReAct-style agent (Yao et al., 2022) under the           5.1                  Main Results on miniCTX-v2
same model access, AutoSolve, compiler feedback,
and verification harness as our method. The agent          We evaluate all methods by plotting pass rate
maintains a bank of proof candidates, each paired          against the average number of LLM calls per the-
with its compiler errors. At each turn, an LLM             orem. For our method, we vary the max refine-
controller (GPT-5-mini) observes the current proof         ment budget K ∈ {8, 12, 16, 20, 24, 28} and set
bank and recent action history, then selects one of        the stagnation threshold to N = ⌈K/4⌉ following
three actions: (1) sample from generalist, (2) sam-        the analysis in Table 3. For each baseline, we vary
ple from specialist, or (3) refine an existing candi-      its call budget up to an average budget of 32 calls.
date by specifying its index.                              Our method achieves the best effectiveness–
4.4   Metrics                                              efficiency tradeoff. As shown in Figure 3, our
                                                           method is consistently at or near the top of the pass
We report pass rate (fraction of theorems verified)        rate curve across projects. Within the pass@32 bud-
against average LLM calls per theorem. The                 get (left to the gray line), our method improves the
pass-rate vs. LLM-call curve is our main evaluation,       average pass rate by 12.8 percentage points over
capturing the effectiveness–efficiency tradeoff. We        the average pass@32 performance of the two base
additionally break down cost in dollars (Figure 4).        models, while reducing LLM calls by 21.9%.
4.5   Implementation Details                               Our method balances exploration and exploita-
Our method interacts with Lean 4 through the               tion. Dual-model generation and stagnation-
lean-interact library (Poiroux et al., 2025b).             triggered resampling serve as exploration: they
                65.0                                                                                                     (a) Pass rate                      (b) Call breakdown                                                              (c) Cost breakdown
                                                                                                                    62                                 16
                                                                                                                                                                                   Ours
                62.5                                                                                                                                                               w/o comparison
                                                                                                                                                                                                         13.84
                                                                                                                                                                                                                                      1.2
                                                                                                                    61                                 14                                                                                                                         $1.10
                                                                                                                                                                                                                                                                                       $1.14
                                                                                                                                                                                                                                                 $1.09
                                                                                                                           59.28
                60.0                                                                                                60                                 12                                                                             1.0
                                                                                                                                                                                                                 11.05
Pass rate (%)




                                                                                                                                                                     10.08




                                                                                                    Pass rate (%)
                                                                                                                    59                                 10




                                                                                                                                                                                                                         Cost (USD)
                57.5




                                                                                                                                           LLM calls
                                                                                                                                                                                                                                      0.8
                                                                                                                                   57.16                                                                                                     $0.70

                55.0                                                                                                58                                  8
                            Ours                                                                                                                              6.54                                                                    0.6
                                                                                                                                                                                           6.11
                            w/o Specialist                                                                          57                                  6
                52.5        w/o autosolve
                                                                                                                                                                                                                                      0.4                             $0.33
                            w/o resample                                                                            56                                  4
                50.0        w/o comparison
                                                                                                                    55                                  2                                                                             0.2
                                                                                                                                                                             1.20 0.97
                                                                                                                                                                                                                                                         $0.07
                47.5                                                                                                                                                                                                                                          $0.05
                                                                                                                                                                                                  0.00                                                                    $0.00
                                                                                                                    54                                  0                                                                             0.0
                          10.0      12.5      15.0     17.5       20.0     22.5     25.0     27.5                            Pass rate                       Generalist      Specialist   Generalist     Total LLM                          Generalist Specialist Generalist        Total
                                                      LLM calls                                                                                                Proof           Proof       compare          calls                             proof      Proof     compare          cost



                (a) Ablation study of different components.                                                                   (b) Effect of pairwise comparison on call allocation and cost.

                                                                                             Figure 6: Ablation study results.


                                   (a) Keep-Current Rate on Solved Trajectories                                                            Cost. Figure 4 and Figure 11 (Appendix B.2)
                                                                     avg=50.4%
                         HepLean                                                           67.3                                            break down the per-project LLM cost and the av-
                           ConNF                                                    62.2                                                   erage number of calls per theorem for the points
                         carleson                                            56.9                                                          under 32 average LLM calls (left to the gray dashed
                       foundation                                   50.0
                                                                                                                                           line in Figure 3). We count three types of LLM
                              FLT                                 47.6
                          mathlib                      40.6                                                                                calls: generalist proof calls, including initial proof
                         Seymour                     37.9                                                                                  generation and refinement; specialist proof calls;
                                                                                                                                           and pairwise comparison calls. On average, our
                                 (b) Final Verification from Preserved Proof States                                                        method spends $1.96, compared with $2.43 for
                                                                  avg=39.5%
                         HepLean                                                            66.7
                                                                                                                                           GPT-5-mini pass@32, while achieving a higher
                           ConNF                                                    57.1
                         carleson                                  40.0                                                                    pass rate. Although comparison calls occur at a
                       foundation                                           50.0                                                           similar frequency to generalist proof calls, they
                              FLT                                           50.0                                                           are cheaper due to short decision output. See Ap-
                          mathlib             20.0                                                                                         pendix B.2 for more detailed token comparison.
                         Seymour               22.2
                                             20                40                   60              80                                     5.2                 Results on RLMEval-FLT3
                                                              Percentage (%)
                                                                                                                                           We also test on RLMEval-FLT3, where each theo-
                                                                                                                                           rem comes with an informal proof. We provide the
Figure 7: Pairwise comparison behavior on solved
refinement trajectories. (a) Keep-current rate macro-                                                                                      informal proof to the generation, refinement, and
averaged over trajectories during successful refine-                                                                                       pairwise comparison modules. As Figure 5 shows,
ment. (b) Final verification from preserved proof states.                                                                                  our method remains effective in this setting: at just
Dashed lines are pooled over all comparison steps.                                                                                         13.5 calls per theorem, it already reaches 39.3%
                                                                                                                                           pass rate, higher than both Generalist pass@32
                                                                                                                                           (36.9%) and Specialist pass@32 (28.6%).
produce diverse proof candidates. As shown in Fig-
ure 3, dual-model generation already outperforms                                                                                           5.3                 Robustness to Model Choice
either single model. Compiler-guided refinement                                                                                            We test whether our gains depend on a specific
serves as exploitation: it improves the current-best                                                                                       model pairing by replacing the generalist with
proof using structured error feedback. At higher                                                                                           Gemini-2.5-Flash and rerunning the full pipeline.
call budgets, the dual-model generation flattens                                                                                           As Table 1 shows, our method outperforms both
(e.g., CARLESON plateaus at 0.50 after about 16                                                                                            base models on every project, reaching 52.86%
calls), while our method continues to improve.                                                                                             average pass rate under a budget of 16 calls. Re-
                                                                                                                                           sults with an additional generalist-specialist pair in
Structured control outperforms open-ended ac-                                                                                              Appendix B.3 further confirm this finding.
tion selection. As shown in Figure 3, our method
outperforms the ReAct-style baseline on every                                                                                              6                Analysis
project, despite a simpler controller. This sug-
gests that, reliable search benefits from an explicit                                                                                      6.1                 Ablation Study
exploration–exploitation schedule rather than leav-                                                                                        Figure 6(a) shows the pass rate–LLM calls tradeoff
ing search decisions entirely to an LLM controller.                                                                                        for four ablations: w/o specialist, w/o autosolve,
 Component               Fraction (%)   Subtotal (%)                      K/12    K/6     K/4     K/3     K/2
 AutoSolve                  28.36          28.36          Pass Rate (%)   48.00   56.00   60.00   54.00   60.00
 Init (Generalist)          30.34                         LLM Calls       30.24   27.12   24.42   27.60   27.76
 Init (Specialist)          9.44           39.78
                                                         Table 3: Effect of stagnation threshold N on mathlib-
 Resample (Generalist)       0.49
 Resample (Specialist)       1.01           1.50         valid.
 Refine (Generalist)        18.91
 Refine (Specialist)        11.46          30.37
                                                         jectories whose final verification follows a pair-
                                                         wise comparison step, 39.5% are verified after the
Table 2: Fraction of theorems proved by each compo-
nent.                                                    comparison chooses the existing current-best proof
                                                         state rather than the newest refinement proposal.
                                                         This means that these successes come from a state
w/o resample, and w/o comparison. In the w/o com-        preserved by comparison, not from immediately
parison setting, pairwise comparison is replaced by      accepting the latest refinement.
a random selector. The ablation shows that the              Together, these results suggest that successful re-
gain does not come from more model calls alone;          finement is not just about generating new revisions,
it comes from how the calls are allocated across         but also about preserving useful proof states.
generation, refinement, comparison, and restart.
                                                         6.3   Complementary Sources of Success
Every component contributes to performance.
                                                         Table 2 decomposes verified proofs by the stage
Removing any single component shifts the curve
                                                         where they are first found. The key observation
downward, indicating that specialist generation, au-
                                                         is that our framework succeeds through comple-
tosolve, resampling, and pairwise comparison each
                                                         mentary search stages rather than a single source
improve the search process. Since w/o comparison
                                                         of success. The generalist and specialist contribute
removes comparison calls by design, we further
                                                         different solved cases, consistent with their dif-
analyze its call allocation and cost in Figure 6(b).
                                                         ferent strengths. Beyond initial generation, refine-
Pairwise comparison improves proof state se-             ment accounts for 30.37% of solved theorems. This
lection. Without comparison, the system relies           shows that failed proofs often contain recoverable
more on proof generation: generalist proof calls         partial progress and that post-failure search is es-
increase from 6.54 to 10.08 per theorem. Pairwise        sential. AutoSolve closes simple goals at zero LLM
comparison improves proof state selection in two         cost to improve efficiency. Appendix B.4 further
ways: it chooses a better starting point after initial   shows that our method still outperforms the base-
dual-model generation, and it preserves stronger         lines when AutoSolve is disabled. Resampling
intermediate states during refinement. This pre-         rarely solves proofs directly, but serves as a fallback
vents useful proof trajectories from being overwrit-     mechanism when refinement stagnates, providing
ten by weaker proposals. As a result, our method         a new starting point for subsequent refinement. Ap-
achieves a higher pass rate (59.28% vs. 57.16%)          pendix B.5 gives an example how resampling helps
with slightly lower total cost ($1.10 vs. $1.14).        later refinement.

6.2   Proof Search Trajectory Analysis                   6.4   Sensitivity to Stagnation Threshold
Refinement proposals are frequently rejected.               Table 3 shows that too small N triggers prema-
Figure 7(a) shows that, even on successful trajecto-     ture restarts, wasting calls on unnecessary resam-
ries, about half of refinement proposals are rejected    pling, while too large N delays necessary restarts,
on average (50.4%). This suggests that refinement        spending calls on exhausted trajectories. N = K/4
does not consistently move toward a correct proof:       achieves the best balance, reaching 60.00% pass
new revisions often introduce new errors or move         rate with 24.42 calls.
away from a previously promising direction. With-        6.5   Context Usage and Trade-offs
out comparison, these unstable updates would over-
write the current proof state at every step.             We use the full context in our method, which makes
                                                         all local definitions, lemmas, and proof examples
Successful proofs often come from preserved              available to the model without an additional re-
states. Figure 7(b) shows that among solved tra-         trieval component. Figure 8 shows how the source
Relevant source context:                                    Target theorem:
lemma z_spec : S . a + eta ^ 2 * S . b = lambda * S . z      lemma lambda_not_dvd_z : not lambda | S . z := by
     := ...
                                                            Generated proof:
lemma lambda_not_dvd_y : not lambda | S . y := by
  intro h                                                      intro h
  replace h := mul_dvd_mul_left ( eta - 1) h                   replace h := mul_dvd_mul_left ( eta - 1) h
  rw [<- y_spec ] at h                                         rw [ < - z_spec ] at h
  rw [<- pow_two ] at h                                        rw [ < - pow_two ] at h
  exact S. lambda_sq_not_dvd_a_add_eta_mul_b h                 exact S . lambda_sq_not_dvd_a_add_eta_sq_mul_b h



Figure 8: Example of context usage. The generated proof explicitly uses z_spec and also follows the proof structure
of the nearby theorem lambda_not_dvd_y, while using the corresponding facts for S.z.


context is used. Appendix B.6 provides a broader           work could combine our trajectory-level control
analysis of how different stages of our method use         with tactic-based search.
source context. The main drawbacks of full con-
                                                           Reliance on pretrained inference-time models.
text are higher input cost and potentially irrelevant
                                                           Our framework uses pretrained LLMs at inference
context. Retrieval could reduce context length, but
                                                           time. We do not train models to improve through
may fail to retrieve a necessary local fact or use-
                                                           multi-turn interaction with Lean feedback. Future
ful proof. Online learning could instead adapt the
                                                           work could explore reinforcement learning or other
model to project-specific information, but requires
                                                           training methods for verifier-guided interaction.
additional training and updates. These alternatives
are complementary to our framework, since the              Toward verifier-grounded process rewards.
search procedure does not depend on how the con-           Our comparison uses an LLM judge to decide
text is provided.                                          whether to keep or replace a proof. This is flexible,
                                                           but it may not always reflect true proof progress.
7   Conclusion                                             An LLM judge is a practical starting point for proof
                                                           selection. Learning verifier-grounded process re-
This work studies adaptive proof search for context-       ward models, or using an independent judge, could
dependent theorem proving. Our framework com-              provide more reliable guidance for keeping, refin-
bines exploration from dual-model generation with          ing, or restarting proof trajectories.
exploitation from current-best refinement, allowing
it to preserve and improve better proof states. More       Acknowledgments
broadly, our results suggest that whole-proof gener-
ation can be extended from independent sampling            We thank the anonymous reviewers for their help-
to adaptive proof search. Rather than only train-          ful suggestions. This work was supported in part
ing stronger provers, future provers may benefit           by computational resources provided through the
from compiler-grounded process signals that can            National Artificial Intelligence Research Resource
help decide which proof states to keep, refine, or         (NAIRR) Pilot under Award NAIRR250254.
abandon.
                                                           References
Limitations
                                                           Muntasir Adnan and Carlos CN Kuhn. 2025. Measuring
Extending complementary generation and re-                  and mitigating debugging effectiveness decay in code
                                                            language models. Scientific Reports, 15(1):44120.
finement. Our framework uses two models for
initial proof generation and a generalist model for        Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu,
refinement. Future work could explore larger or               Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin,
more specialized model pools, and study how dif-              Chenggang Li, Wenlei Shi, Zhihong Wang, Mingx-
                                                              uan Wang, Chenrui Wei, Shufa Wei, Huajian Xin,
ferent models should be assigned to generation,               Fan Yang, Weihao Gao, Zheng Yuan, Tianyang Zhan,
refinement, comparison, and resampling.                       and 3 others. 2025. Seed-prover 1.5: Mastering
                                                              undergraduate-level theorem proving via learning
Limited use of tactic-level search. Our method                from experience. arXiv preprint arXiv:2512.17260.
works at the whole-proof level. It generates, refines,     Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan,
and compares complete proofs, but does not explic-          Henrique Ponde de Oliveira Pinto, Jared Kaplan,
itly search over tactic-level proof states. Future          Harri Edwards, Yuri Burda, Nicholas Joseph, Greg
  Brockman, Alex Ray, Raul Puri, Gretchen Krueger,           Goedel-prover-v2: Scaling formal theorem proving
  Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela        with scaffolded data synthesis and self-correction.
  Mishkin, Brooke Chan, Scott Gray, and 39 others.           arXiv preprint arXiv:2508.03613.
  2021. Evaluating large language models trained on
  code. arXiv preprint arXiv:2107.03374.                   Minghai Lu, Zhe Zhou, Danning Xie, Songlin Jia, Ben-
                                                             jamin Delaware, and Tianyi Zhang. 2025. Adaptive
Xinyun Chen, Maxwell Lin, Nathanael Schärli, and             proof refinement with llm-guided strategy selection.
  Denny Zhou. 2023. Teaching large language models           arXiv preprint arXiv:2510.25103.
  to self-debug. arXiv preprint arXiv:2304.05128.
                                                           Leonardo de Moura and Sebastian Ullrich. 2021. The
Rémi Coulom. 2006. Efficient selectivity and backup          lean 4 theorem prover and programming language. In
  operators in monte-carlo tree search. In International     International Conference on Automated Deduction,
  conference on computers and games, pages 72–83.            pages 625–635. Springer.
  Springer.
                                                           Auguste Poiroux, Antoine Bosselut, and Viktor Kunčak.
Emily First, Markus N Rabe, Talia Ringer, and Yuriy          2025a. RLMEval: Evaluating research-level neu-
  Brun. 2023. Baldur: Whole-proof generation and             ral theorem proving. In Findings of the Association
  repair with large language models. In Proceedings of       for Computational Linguistics: EMNLP 2025, pages
  the 31st ACM Joint European Software Engineering           10946–10957, Suzhou, China. Association for Com-
  Conference and Symposium on the Foundations of             putational Linguistics.
  Software Engineering, pages 1229–1241.
                                                           Auguste Poiroux, Viktor Kuncak, and Antoine Bosselut.
Robert Joseph George, Suozhi Huang, Peiyang                  2025b. Leaninteract: A python interface for lean 4.
  Song, and Anima Anandkumar. 2025.          Lean-
  progress: Guiding search for neural theorem prov-        Stanislas Polu and Ilya Sutskever. 2020. Generative
  ing via proof progress prediction. arXiv preprint           language modeling for automated theorem proving.
  arXiv:2502.17925.                                           arXiv preprint arXiv:2009.03393.

Jiewen Hu, Thomas Zhu, and Sean Welleck. 2024.             Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
   minictx: Neural theorem proving with (long-) con-          Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,
   texts. arXiv preprint arXiv:2408.03350.                    Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-
                                                              rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,
Thomas Hubert, Rishi Mehta, Laurent Sartran, Mik-             Daya Guo, and Chong Ruan. 2025. Deepseek-prover-
  lós Z. Horváth, Goran Žužić, Eric Wieser, Aja              v2: Advancing formal mathematical reasoning via
  Huang, Julian Schrittwieser, Yannick Schroecker,            reinforcement learning for subgoal decomposition.
  Hussain Masoom, Ottavia Bertolli, Tom Zahavy,               arXiv preprint arXiv:2504.21801.
  Amol Mandhane, Jessica Yung, Iuliya Beloshapka,
  Borja Ibarz, Vivek Veeriah, Lei Yu, Oliver Nash, and     Aaditya Singh, Adam Fry, Adam Perelman, Adam Tart,
  19 others. 2026. Olympiad-level formal mathemati-          Adi Ganesh, Ahmed El-Kishky, Aidan McLaughlin,
  cal reasoning with reinforcement learning. Nature,         Aiden Low, AJ Ostrow, Akhila Ananthram, Akshay
  651(8106):607–613.                                         Nathan, Alan Luo, Alec Helyar, Aleksander Madry,
                                                             Aleksandr Efremov, Aleksandra Spyra, Alex Baker-
Ryo Kamoi, Yusen Zhang, Nan Zhang, Jiawei Han,               Whitcomb, Alex Beutel, Alex Karpenko, and 467 oth-
  and Rui Zhang. 2024. When can llms actually cor-           ers. 2025. Openai gpt-5 system card. arXiv preprint
  rect their own mistakes? a critical survey of self-        arXiv:2601.03267.
  correction of llms. Transactions of the Association
  for Computational Linguistics, 12:1417–1440.             Joseph Tooby-Smith. 2025. Heplean: Digitalising high
                                                              energy physics. Computer Physics Communications,
Adarsh Kumarappan, Mo Tiwari, Peiyang Song,                   308:109457.
  Robert Joseph George, Chaowei Xiao, and Anima
  Anandkumar. 2024. Leanagent: Lifelong learn-             Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He,
  ing for formal theorem proving. arXiv preprint              and Thang Luong. 2024. Solving olympiad ge-
  arXiv:2410.06209.                                           ometry without human demonstrations. Nature,
                                                              625(7995):476–482.
Guillaume Lample, Timothee Lacroix, Marie-Anne
  Lachaux, Aurelien Rodriguez, Amaury Hayat,               George Tsoukalas, Jasper Lee, John Jennings, Jimmy
  Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.        Xin, Michelle Ding, Michael Jennings, Amitayush
  2022. Hypertree proof search for neural theorem            Thakur, and Swarat Chaudhuri. 2024. Putnambench:
  proving. Advances in neural information processing         Evaluating neural theorem-provers on the putnam
  systems, 35:26337–26349.                                   mathematical competition. Advances in Neural In-
                                                             formation Processing Systems, 37:11545–11569.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-
  Hui Chung, Haoyu Zhao, Lai Jiang, Yihan Geng,            Evan Wang, Simon Chess, Daniel Lee, Siyuan Ge,
  Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing       Ajit Mallavarapu, Jarod Alper, and Vasily Ilin. 2026.
  Lu, David Acuna, Kaiyu Yang, Hongzhou Lin, Yejin           Learning to repair lean proofs from compiler feed-
  Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. 2025.        back. arXiv preprint arXiv:2602.02990.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
  Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao
  Lu, Hugues de Saxcé, Bolton Bailey, Chendong Song,
  Chenjun Xiao, Dehao Zhang, Ebony Zhang, Fred-
  erick Pu, Han Zhu, and 21 others. 2025. Kimina-
  prover preview: Towards large formal reasoning
  models with reinforcement learning. arXiv preprint
  arXiv:2504.11354.
Ruida Wang, Jipeng Zhang, Yizhen Jia, Rui Pan, Shizhe
  Diao, Renjie Pi, and Tong Zhang. 2024. Theoreml-
  lama: Transforming general-purpose llms into lean4
  experts. In Proceedings of the 2024 Conference on
  Empirical Methods in Natural Language Processing,
  pages 11953–11974.

Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan
  Ying, Zheng Yuan, Wenwei Zhang, Dahua Lin, and
   Kai Chen. 2024. Internlm2. 5-stepprover: Advancing
   automated theorem proving via critic-guided search.
   arXiv preprint arXiv:2410.15700.
Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang
  Wu, Xia Xiao, Yifan Sun, Shen Zheng, and Ming
  Ding. 2025. Bfs-prover: Scalable best-first tree
  search for llm-based automatic theorem proving. In
  Proceedings of the 63rd Annual Meeting of the As-
  sociation for Computational Linguistics (Volume 1:
  Long Papers), pages 32588–32599.
John Yang, Akshara Prabhakar, Karthik Narasimhan,
  and Shunyu Yao. 2023. Intercode: Standardizing and
  benchmarking interactive coding with execution feed-
  back. Advances in Neural Information Processing
  Systems, 36:23826–23854.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
  Shafran, Karthik Narasimhan, and Yuan Cao. 2022.
  React: Synergizing reasoning and acting in language
  models. arXiv preprint arXiv:2210.03629.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  2021. Minif2f: a cross-system benchmark for for-
  mal olympiad-level mathematics. arXiv preprint
  arXiv:2109.00110.
Yichi Zhou, Jianqiu Zhao, Yongxin Zhang, Bohan Wang,
  Siran Wang, Luoxin Chen, Jiahui Wang, Haowei
  Chen, Allan Jie, Xinbo Zhang, Haocheng Wang, Lu-
  ong Trung, Rong Ye, Phan Nhat Hoang, Huishuai
  Zhang, Peng Sun, and Hang Li. 2025. Solving for-
  mal math problems by decomposition and iterative
  reflection. arXiv preprint arXiv:2507.15225.
                                                                R1       R2   R3        R4   R5               R1   R2        R3   R4   R5
A   Algorithm
                                                      WP0       32       10   27             20    WP5    12                      3
Algorithm 1 shows the full search procedure. Dur-
                                                                10       23   12                                   18
ing refinement, the current-best proof s∗ changes
                                                      WP1                                          WP6



only when a new proposal is accepted (lines 29–31).   WP2                     12             14    WP7    28       15        7         13
During resampling, s∗ is replaced by a fresh proof    WP3                     3         17         WP8    27       12        4    4    3
generated during exploration (lines 16–22). The
                                                      WP4       25       22   16        6     9    WP9        5    7         5    14
threshold N controls how often the search switches
between exploration and refinement: smaller N en-
courages more exploration, while larger N spends            1        5             10        15          20             25        30        35
                                                                Iterations to success        ( = no verified proof within 32 iterations )
more budget on refinement.
                                                      Figure   9:       Refinement   heatmap                                                for
Algorithm 1 Compiler-Grounded Refinement              _isBigO_deriv_ofReal_cpow_const_atTop                                                  in
Search with Dual-Model Exploration                    mathlib.
Require: Theorem s, context C, max iters K,
                                                                R1       R2   R3        R4   R5               R1   R2        R3   R4   R5
    stagnation threshold N
 1: E ← VALIDATE C ONTEXT(C)                          WP0                13                   6    WP5             3         3    3    3
 2: if AUTO S OLVE(s, E) succeeds then                WP1                4    14                   WP6


 3:    return proof                                   WP2                     28        8    17    WP7    22
 4: end if
                                                      WP3                7                         WP8                            9
 5: pgen ← G ENERALIST (C, s)
 6: if V ERIFY (pgen ) then                           WP4                                          WP9        9    6         8    7    9
 7:    return pgen
 8: end if
                                                            1        5             10        15          20             25        30        35
 9: pspec ← S PECIALIST(C, s)                                   Iterations to success        ( = no verified proof within 32 iterations )
10: if V ERIFY (pspec ) then
11:    return pspec                                   Figure   10:       Refinement                                      heatmap            for
                                                      eLpNorm_toReal_le in Carleson.
12: end if
13: s∗ ← B ETTER(pgen , pspec )
14: nstag ← 0                                         B         Additional Analysis
15: for k = 1 to K do
16:    if nstag ≥ N then                              B.1         Analysis of Randomness in Iterative
17:       r1 ← M ODELwinner (C, s)                                Refinement
18:       r2 ← M ODELother (C, s)                     To understand how much the choice of starting
19:       if V ERIFY(r1 ) or V ERIFY(r2 ) then        wrong proof affects refinement outcomes versus
20:          return verified proof                    inherent stochasticity, we run five independent re-
21:       end if                                      finement runs for each wrong proof and measure
22:       s∗ ← B ETTER(r1 , r2 ); nstag ← 0           two sources of variation:
23:       continue
24:    end if                                               • Intra-WP std: the standard deviation of suc-
25:    s̃ ← R EFINE(C, s∗ , E RRORS(s∗ ))                     cess iterations across multiple reruns of the
26:    if V ERIFY(s̃) then                                    same wrong proof, capturing run-to-run ran-
27:       return s̃                                           domness.
28:    end if
                                                            • Inter-WP std: the standard deviation of suc-
29:    if B ETTER(s∗ , s̃) = s̃ then
                                                              cess iterations across different wrong proofs
30:       s∗ ← s̃; nstag ← 0
                                                              within the same theorem, capturing the effect
31:    else
                                                              of starting point selection.
32:       nstag ← nstag + 1
33:    end if                                         Failed runs (no verified proof within 32 iterations)
34: end for                                           are assigned a value of 32.
35: return failure                                       Figures 9 and 10 visualize the iteration counts
                                                      for two theorems. Each row corresponds to a wrong
                                                                                                                                                                   70.8K
                                                      Intra-WP std                 Inter-WP std                                                           70                                                       Ours (15.84 calls)
                                                                                                                                                                                                                   GPT-5-mini pass@16




                                                                                                                         Average Tokens per Theorem (K)
                                        T1                       1.86                     5.59                                                            60                   55.4K
                                        T2                       0.80                     2.58
                                                                                                                                                          50
                                        T3                       7.02                     8.66
                                        T4                       0.00                     0.00                                                            40
                                        T5                       0.08                     0.49
                                                                                                                                                          30
                                        T6                       5.42                     6.54
                                        T7                       1.22                     0.49                                                            20
                                                                                                                                                                                                                   11.7K        13.5K
                                        T8                       4.06                     4.85                                                            10                                7.8K    9.1K
                                        T9                       1.24                     1.00
                                                                                                                                                           0
                                        Avg                      2.41                     3.36                                                                         Input                 Reasoning                Output


Table 4: Intra-WP std vs. inter-WP std for theorems in                                                                Figure 12: Average token consumption per theorem on
the mathlib-valid.                                                                                                    HepLean under nearly matched LLM call budgets.


                                   Generalist proof
                                                                                                      31.7
                                                                                                                                                          55
                                                                                             31.3
                                   Specialist proof                       29.9
                                                                                                                                                          50
Number of LLM calls




                      30           Pairwise comparison                             28.6




                                                                                                                      Pass rate (%)
                                                                                                                                                          45
                                                                                                               25.1
                                               23.2        22.7

                      20                                                                                                                                  40
                                                                                                                                                          35
                      10          8.4                                                                                                                     30                                     Generalist
                                                                                                                                                                                                 Specialist
                                                                                                                                                          25                                     Ours
                       0
                               r             an              n          ib         T           n       F        g                                              0           5           10   15       20       25           30           35
                         y m
                             ou
                                        ep
                                          Le       d  at
                                                        io
                                                                  at
                                                                     hl          FL
                                                                                      a rle
                                                                                            so
                                                                                                 Co
                                                                                                    nN       Av                                                                             LLM calls
                      Se          H             un               M                  C
                                             Fo
                                                                                                                      Figure 13: Pass rate (%) vs. LLM calls on HepLean with
Figure 11: LLM calls breakdown under 32 average                                                                       GPT-5.4-mini as the Generalist and Goedel-Prover-V2-
LLM calls on miniCTX-v2 test.                                                                                         8B as the Specialist.


proof starting point, and each column to an indepen-                                                                  where many theorems are resolved early, to over 31
dent rerun. The prevalence of entire rows marked                                                                      on Carleson and ConNF, showing greater need for
with × (e.g., WP4, WP6 in Figure 10) indicates that                                                                   refinement on harder projects.
certain starting points consistently fail regardless                                                                     Figure 12 shows the average token usage per
of random seed, while others (e.g., WP9) succeed                                                                      theorem on HepLean project under similar num-
reliably. This pattern suggests that starting point                                                                   ber of LLM calls. Our method uses more input
quality is a stronger determinant of success.                                                                         tokens because it includes compiler feedback, but
   Table 4 confirms this quantitatively. Across 9                                                                     fewer reasoning and output tokens because compar-
randomly chosen theorems with non-trivial vari-                                                                       ison call outputs short answers. At the same time,
ance, the average inter-WP std (3.36) exceeds the                                                                     our method achieves better performance than the
average intra-WP std (2.41), indicating that the                                                                      baseline (64% vs. 56%).
variation due to different starting points is larger
than the variation from repeated runs of the same                                                                     B.3 Additional Model Pair: GPT-5.4-mini and
starting point. This supports the conclusion that                                                                         Goedel-Prover-V2-8B
selecting a good wrong proof as the refinement                                                                        We further evaluate robustness by replacing both
starting point matters more than simply rerunning                                                                     the generalist and the specialist, using GPT-5.4-
the same starting point multiple times.                                                                               mini as the generalist and Goedel-Prover-V2-8B as
                                                                                                                      the specialist. Figure 13 plots pass rate against
B.2                          LLM Calls Breakdown and Token                                                            LLM calls on HepLean. Both individual mod-
                             Comparison                                                                               els plateau quickly, the generalist at 48% and the
Figure 11 shows the average number of LLM calls                                                                       specialist at 44%, while our method continues to
per theorem. Pairwise comparison calls account                                                                        improve with additional calls, reaching over 56%.
for the largest part across all projects, but their cost                                                              This confirms that the complementary exploration
is low as the judge produces only a short binary de-                                                                  strategy benefits from model diversity in general,
cision. The total varies from 8.4 calls on Seymour,                                                                   rather than relying on the specific strengths of any
                                                             Pass rate (%) per project
           Method                                                                                             Avg.
                                          Carleson ConNF   FLT     Foundation HepLean Mathlib Seymour
           GPT-5-mini (pass@32)            40.00   34.00   38.24       56.00      56.00     44.00     80.00   49.75
           DeepSeek-Prover-v2 (pass@32)    46.00   34.00   50.00       56.00      50.00     48.00     78.00   51.71
           Ours w/o AutoSolve              52.00   46.00   52.94       66.00      64.00     54.00     90.00   60.71
             avg calls                     23.50   27.92   24.24       17.94       18.56    24.20      8.58   20.71


Table 5: Pass rate (%) on miniCTX-v2 across seven projects without AUTO S OLVE. The two baselines use pass@32.
Our method additionally reports average LLM calls per theorem (gray).


single model pair.                                                     Proof source           Ref. rate (%)    Avg. # refs
                                                                       AutoSolve                    3.51              0.04
B.4   Results Without AutoSolve                                        Initial Specialist           42.11             0.53
To separate the effect of AUTO S OLVE from our                         Initial Generalist           60.66             0.93
                                                                       Refinement                   62.30             1.11
adaptive search, we run our method with AUTO -
                                                                       Resampling                   33.33             0.33
S OLVE disabled. Table 5 compares this setting with
                                                                       Full method                  42.79             0.69
the pass@32 baselines. Without AUTO S OLVE, our
                                                                       Ground-truth proof           40.30             0.57
method reaches an average pass rate of 60.71%,
compared with 49.75% for GPT-5-mini and 51.71%                   Table 6: Explicit use of declarations from the source
for DeepSeek-Prover-v2. It also achieves the high-               context. We count a reference when a verified proof
est pass rate on all seven projects while using 20.71            names a declaration that appears in the preceding source
LLM calls per theorem on average. These results                  context but not in the target theorem statement. Ref.
show that the main performance gain and the lower                rate is the percentage of proofs with at least one such
call usage are not from AUTO S OLVE. Proofs found                reference. Avg. # refs is the average number of distinct
                                                                 references per proof. Results are pooled over theorems
by AUTO S OLVE can be solved by LLMs within
                                                                 from all seven projects.
very few calls.

B.5   Resampling Example                                            We report two measures. The reference rate is
We give an example to show the indirect                          the percentage of verified proofs that use at least
role of resampling in the search process. On                     one such declaration. The average number of refer-
TileStructure.Forest.exists_p_of_mem_σ                           ences is the average number of different source con-
from Carleson project, four refinement steps failed              text declarations used each proof. Table 6 shows
to improve the current proof, and resampling was                 that 42.79% of the proofs found by our method use
triggered at iteration 5. The new proof was selected             at least one additional declaration from the source
but was still not valid. After one more refinement               context. The rate is 40.30% for the ground-truth
step, the theorem was solved. This success is                    proofs. Refinement has the highest reference rate
counted as refinement rather than resampling in                  at 62.30% and also the highest average number of
Table 2. This example shows that resampling can                  references. AutoSolve has a much lower reference
help the search leave a stuck state and give later               rate, which is expected because it mainly handles
refinement a better starting point.                              simpler proofs with built-in tactics. Initial proofs
                                                                 from the Generalist also make frequent use of the
B.6 Analysis of Explicit Use of Source Context                   source context, with a reference rate of 60.66%. In
We conduct an additional experiment to understand                comparison, initial proofs from the Specialist use
how our method uses information from the source                  fewer explicit references. One possible reason is
context. For each theorem, we extract the names of               that the Generalist is better at reasoning over the
declarations in the provided source context before               provided context, while the Specialist focuses more
the target theorem. We then use lexical matching to              on Lean proof generation.
check whether the verified proof explicitly refers to
any of these declarations. We only count declara-                B.7     Analysis of Judge Model Preference
tion names that appear directly in the proof. Thus,            Table 7 reports the model selection rate across
this analysis does not capture implicit use through            all pairwise comparisons in which both GPT-5-
tactics such as simp or aesop.                                 mini and DeepSeek-Prover-V2 successfully pro-
    Project      #Comparisons   GPT-5-mini (%)   DeepSeek-Prover-V2 (%)   the context length to 8192 for the specialist, and
    Carleson          49             53.1                 46.9
    ConNF             73             54.8                 45.2            increasing it further does not improve performance.
    FLT               32             78.1                 21.9
    Foundation        47             55.3                 44.7
    HepLean           45             71.1                 28.9
    Mathlib          122             55.7                 44.3
                                                                          Lean version. We use v4.16.0 for miniCTX-v2
    Seymour           23             52.2                 47.8            and v4.7.0-rc2 for RLMEval-FLT3.
    Total            391             58.6                 41.4


Table 7: Model selection rate in pairwise comparisons,                    AutoSolve. The AUTO S OLVE module attempts
pooled over all theorems. Each comparison occurs when                     to close the theorem before any LLM call using
both GPT-5-mini and DeepSeek-Prover-V2 produce a                          two classes of tactics:
candidate proof and the judge selects the better starting
                                                                             (i) deterministic closers (rfl, simp, omega,
point.
                                                                          linarith, norm_num, ring, decide, etc.) that
                                                                          close the goal directly, and
duce a candidate proof during initial generation                             (ii) search-based tactics (exact?, hint) that
or stagnation-triggered resampling. These com-                            query Lean’s library search, return “Try this: . . . ”
parisons are counted over all theorems, including                         suggestions, and verify each suggestion against the
unsolved ones. Across 391 total comparisons, GPT-                         compiler.
5-mini is selected 58.6% of the time, indicating a
moderate but consistent preference. This advantage                        Parsing Pairwise Decisions. The pairwise judge
is most pronounced on FLT (78.1%) and HepLean                             is prompted to return {“choice”:              “A”} or
(71.1%), where GPT-5-mini’s candidates are sub-                           {“choice”: “B”}. Responses are parsed with cas-
stantially favored. On other projects such as Car-                        cading fallbacks: JSON parsing, regex extraction,
leson, Seymour, and Foundation, the selection rates                       single-character detection, and if all fail, defaulting
are closer, suggesting that the relative strength of                      to the current proof (choice A).
the two models is task dependent. These results
indicate that employing a multi-model generation
                                                                          Error Extraction. When a proof fails verifica-
strategy is beneficial: although GPT-5-mini is pre-
                                                                          tion, compiler errors are matched to specific tactic
ferred overall, DeepSeek-Prover-V2 is still selected
                                                                          lines by aligning error positions with proof source
in over 40% of comparisons, confirming that it pro-
                                                                          lines. Each error is formatted with one line of sur-
vides complementary proof candidates.
                                                                          rounding context and the error message, producing
                                                                          a compact line-level report used by both the repair
C       Implementation Details
                                                                          model and the comparison judge.
We use lean-interact (Poiroux et al., 2025b) to
interact with the Lean 4 REPL. For each theorem,                          Hardware. We run the self-hosted specialist
the surrounding source context is validated by run-                       model on a server with two NVIDIA L40S GPUs,
ning it through the REPL (timeout = 360), produc-                         each with 48GB of memory. The generalist model
ing a cached environment E against which all proof                        is accessed through an API.
attempts are verified (timeout = 120). Unless other-
wise specified, all main results are reported from a
                                                                          D    Prompt Templates
single run for each method and budget.

Context Use. Following miniCTX (Hu et al.,                                This section lists the prompt templates used for
2024) and RLMEval (Poiroux et al., 2025a), C                              proof generation, refinement, and pairwise compar-
is the source content before the target theorem in                        ison. Each prompt includes the theorem statement
the project file. It includes imports, local defini-                      and the surrounding Lean project context. Refine-
tions, project-specific lemmas, namespaces, and                           ment and comparison prompts also include com-
notation. It comes directly from the original Lean                        piler feedback from failed proof attempts.
repository. The generalist receives the full context                         For RLMEval-FLT3, each theorem is paired with
because it can handle long inputs. The specialist                         a natural language proof. We include this natural
has a shorter context window, so we keep the begin-                       language proof in the generation, refinement, and
ning and the end of C and remove the middle part,                         pairwise comparison prompts, while keeping the
following RLMEval (Poiroux et al., 2025a). We set                         rest of the search procedure unchanged.
                                           Number of theorems proved per project
        Component                                                                             Avg.
                                Carleson ConNF FLT Foundation HepLean Mathlib Seymour
        AutoSolve                  0      7     11       20           4       10        5     8.14
        Init (Generalist)         16      2      0        5          10        3       25     8.71
        Init (Specialist)          4      1      3        1           4        3        3     2.71
        Resample (Generalist)      0      0      0        0           1        0        0     0.14
        Resample (Specialist)      0      0      0        0           1        0        1     0.29
        Refine (Generalist)       5       5     4        3           7        8        6      5.43
        Refine (Specialist)       2       7     1        1           5        3        4      3.29
        Total                     27      22    19       30          32       27       44     28.71

         Table 8: Detailed breakdown of theorems proved by each component on miniCTX-v2 test.


D.1   Specialist Proof Generation                      D.4      Pairwise Proof Comparison

                                                              You are an expert in Lean 4. Your task
  Complete the following Lean 4 code with                     is to compare two proofs that both failed
  explanatory comments preceding each line                    verification, select the one that has
  of code:                                                    better quality and is more suitable as the
  ```lean4                                                    starting point for refinement.
  {context}                                                Here is the Lean 4 context:
  {declaration}                                            ```lean4
                                                           {context}
                                                           ```
                                                           Here is the theorem declaration:
D.2   Generalist Proof Generation                          ```lean4
                                                           {declaration}
                                                           ```
  Here is the Lean 4 context:                              — Proof A —
  ```lean4                                                 ```lean4
  {context}                                                {proof_A}
  ```                                                      ```
  Using this context, prove the following                  Errors for Proof A:
  theorem in Lean 4.                                       {errors_A}
  Theorem statement:                                       — Proof B —
  {declaration}                                            ```lean4
  Start your response like this:                           {proof_B}
  ```lean4                                                 ```
  := by                                                    Errors for Proof B:
                                                           {errors_B}
                                                              Compare the two proofs above. Consider the
D.3   Error-Guided Repair                                     following criteria:
                                                              Fixability: Which error message is easier
                                                              to resolve?
                                                              Progress: Which proof leaves fewer or
  Here is the Lean 4 context:
                                                              simpler remaining subgoals?
  ```lean4
                                                              Strategy: Which proof uses a sounder
  {context}
                                                              overall approach?
  ```
                                                              Respond with ONLY this JSON: {"choice":
  Here is the target theorem statement:
                                                              "A"} or {"choice": "B"}, no other text.
  {declaration}
  Here is an attempted Lean 4 proof body but
  contains errors:
  ```lean4
                                                       E       Effect of Context Length on Success
  {wrong_proof}                                                Rate
  ```
  The proof has the following errors:                  To understand how the surrounding Lean context
  {errors}                                             influences proving difficulty, we analyze the rela-
  Based on the context and errors, provide a           tionship between source context length and proof
  new corrected Lean 4 proof.                          success rate across all seven projects with max re-
  Please output a new lean4 proof ONLY, no
  other explanations.                                  finement K = 16. Figure 14 shows the distribution
                                                       of solved and failed theorems as a function of con-
text length (in characters) for each project.
   The seven projects have different context length
distributions. FLT and Seymour have the shortest
contexts, with almost all theorems below 20k char-
acters. Carleson is the main outlier, with some
contexts longer than 140k characters. In most
projects, longer contexts are more often linked to
failed proofs. This pattern is strongest in Carleson,
where most theorems above 40k characters are not
solved. A similar trend appears in Foundation and
ConNF. In FLT and Seymour, the results are more
balanced because the contexts are generally short.
Overall, longer source contexts are often associ-
ated with harder proofs. They may include more
irrelevant information and also tend to appear in
more complex theorems.

F   Artifact Use
Licenses and terms of use. We use pub-
licly available benchmarks and tools, including
miniCTX-v2, RLMEval-FLT3, Lean 4, and lean-
interact, under their released terms of use and li-
censes. We use the associated Lean projects only
for research evaluation and do not redistribute mod-
ified project artifacts. For API-based generalist
models and self-hosted specialist models, we fol-
low the corresponding provider terms and model
licenses.
Intended use. Our use of these artifacts is con-
sistent with their intended research and evaluation
use. We use theorem proving benchmarks to eval-
uate proof search systems, Lean projects as proof
environments, and models for proof generation, re-
finement, and comparison.
Privacy and offensive content. The artifacts
used in this work are theorem proving benchmarks,
Lean source files, compiler feedback, and informal
mathematical proofs. They are not datasets about
individual people and are not expected to contain
personally identifying information or offensive con-
tent.
                                          carleson                                                                                                                            ConNF
                                                                                                  Failed              8                                                                                                  Failed
        8                                                                                         Solved              7                                                                                                  Solved
                                                                                                                      6
        6                                                                                                             5
Count




                                                                                                              Count
                                                                                                                      4
        4
                                                                                                                      3
        2                                                                                                             2
                                                                                                                      1
        0                                                                                                             0
             0k     20k      40k        60k                 80k     100k         120k               140k                  0k               5k              10k               15k         20k     25k               30k
                                     Context length (chars)                                                                                                      Context length (chars)
                                         foundation                                                                                                                          HepLean
        16                                                                                        Failed              5                                                                                                  Failed
        14                                                                                        Solved                                                                                                                 Solved
                                                                                                                      4
        12
        10                                                                                                            3
Count




                                                                                                              Count




         8
         6                                                                                                            2
         4
                                                                                                                      1
         2
         0                                                                                                            0
              0k        5k     10k        15k                 20k      25k            30k               35k               0k                     5k                   10k                15k           20k                     25k
                                     Context length (chars)                                                                                                      Context length (chars)
                                              mathlib                                                                                                                              FLT
        7                                                                                         Failed                                                                                                                 Failed
        6                                                                                         Solved              8                                                                                                  Solved
        5
                                                                                                                      6
        4
Count




                                                                                                              Count




        3                                                                                                             4
        2
                                                                                                                      2
        1
        0                                                                                                             0
                   5k        10k         15k                  20k          25k              30k                            0k         2k              4k         6k                8k    10k   12k           14k         16k
                                     Context length (chars)                                                                                                      Context length (chars)
                                                                                                           Seymour
                                                        6                                                                                                        Failed
                                                        5
                                                                                                                                                                 Solved

                                                        4
                                                Count




                                                        3
                                                        2
                                                        1
                                                        0
                                                              0k     2k          5k                8k          10k              12k             15k        18k              20k
                                                                                                  Context length (chars)


 Figure 14: Distribution of proof success and failure by source context length across seven miniCTX-v2 projects.
