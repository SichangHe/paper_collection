                                        Sketch-and-Verify: Structured Inference-Time Scaling
                                                      via Program Sketching


                                                                           Shan Jiang∗ Zijian Yi∗ Chenguang Zhu
                                                                               The University of Texas at Austin
                                                                                   shanjiang@utexas.edu
arXiv:2605.08658v1 [cs.LG] 9 May 2026




                                                                                          Abstract
                                                    We position S KETCH V ERIFY as a within-tier cost-performance policy, not a univer-
                                                    sal accuracy improvement. The operational question is: a practitioner constrained
                                                    to a small, cheap code model (in our experiments, Gemini 3.1 Flash Lite) for
                                                    latency, deployment, or budget reasons — how should they spend a small amount
                                                    of extra test-time compute? S KETCH V ERIFY factorizes the search space: the LLM
                                                    enumerates K distinct algorithmic strategies, writes a program sketch for each (a
                                                    partial program with ?? holes), and fills each sketch M times, producing K×M
                                                    structurally diverse candidates that are then verified by execution and selected by
                                                    fingerprint clustering. Each additional sketch is guaranteed to explore a different
                                                    algorithm; each additional flat sample likely duplicates an existing one.
                                                    Our central evidence is a cost-quality Pareto plot on HumanEval+ across three
                                                    Gemini tiers (Lite, Flash, Pro), and a reanalysis on the 19 problems where Lite
                                                    greedy fails. Two findings emerge. (1) Within-tier, sketching dominates flat sam-
                                                    pling at matched candidate count. On the hard subset, Lite Sketch K=2, M =5
                                                    recovers 11/19 problems (58%) vs. flat N =10 at 5/19 (26%, +32pp); Lite Sketch
                                                    K=10, M =10 recovers 15/19 (79%) vs. flat N =100 at 10/19 (53%, +26pp). Flat
                                                    sampling cannot close the gap even at ∼3× the budget: flat N =50 still loses to
                                                    Sketch K=2, M =5 by +11pp. (2) Cross-tier, sketching does not replace up-
                                                    grading. Pro greedy (89%) dominates Lite Sketch K=10, M =10 (79%) on both
                                                    pass@1 and dollar cost. The practitioner rule is: if a stronger tier is available, use
                                                    greedy on it; otherwise sketching is the cost-effective way to spend extra compute.
                                                    We characterize the K-vs-M trade-off via the Flash Lite scaling sweep, report
                                                    HumanEval+ saturation effects on Flash and Pro, and show the method composes
                                                    cleanly with execution-based selection from the concurrent Semantic Voting line
                                                    of work.


                                        1     Introduction
                                        Large code models are accurate but expensive; small code models are cheap but often miss because
                                        their first sampled solution follows a wrong modal strategy. The practitioner’s question is not
                                        which model is strongest in the abstract but a cost-performance policy: given a fixed model tier —
                                        chosen for latency, deployment, or budget reasons — how should I spend a small amount of extra
                                        test-time compute? The standard answer is to sample N candidate programs and select the best by
                                        execution [Chen et al., 2021, Li et al., 2022, Snell et al., 2025, Wang et al., 2023, Zhou et al., 2024,
                                        Inoue et al., 2025], but this leaves the diversity of the candidate pool to chance — and that chance is
                                        mostly wasted on cosmetic variants of the same two or three strategies.
                                        The result is predictable waste. When an LLM samples 100 programs at temperature 0.8, most
                                        variation is superficial — different variable names, loop styles, or formatting around the same handful
                                            ∗ Equal contribution, ordered by last name.



                                        Preprint.
of algorithmic approaches. A model that assigns 60% probability mass to a hash-map strategy will
produce approximately 60 hash-map solutions out of 100, regardless of temperature. The structural
diversity — how many fundamentally different strategies are explored — stays low, and no selection
rule can rescue a pool that never contained the right approach. This matters most for weak models,
which fail more often and produce less spontaneous strategic diversity.
We propose S KETCH V ERIFY, a method that restructures how inference-time compute is allocated.
Instead of drawing 100 i.i.d. samples, we ask the LLM to:

      1. Enumerate K fundamentally different algorithmic strategies for the problem.
      2. Sketch each strategy as a partial program with ?? holes for implementation details.
      3. Fill each sketch M times, producing K × M complete candidates.
      4. Verify all candidates by execution and select the best.

This decomposition is inspired by program sketching [Solar-Lezama, 2008, 2013], a technique from
programming languages where a programmer provides a structural template and a solver fills in
the details. OBsmith [Jiang et al., 2026b] demonstrated that LLM-powered sketching produces
structurally diverse programs for compiler testing. We generalize this insight to inference-time
scaling: if sketching increases structural diversity for testing, it should increase diversity among
candidate solutions—and more diverse candidates mean a better chance of finding the correct one.
The core idea is factorization of the search space. Flat sampling treats the program space as homoge-
neous; every sample has equal probability of exploring any region. S KETCH V ERIFY decomposes this
space into structural choices (which algorithm, data structures, control flow) and implementation
choices (expressions, conditions, edge cases). The K sketches guarantee breadth across strategies;
the M fills per sketch provide depth within each. This is directly analogous to stratified sampling in
statistics, which outperforms simple random sampling by ensuring coverage of all strata—but applied
to the space of programs rather than a probability distribution.

Headline result. On the 19 HumanEval+ problems where Gemini 3.1 Flash Lite greedy fails,
Lite Sketch K=2, M =5 recovers 11/19 problems at $3.8e-4 per problem; flat sampling at the same
candidate count recovers 5/19, and even at ∼3× the budget (flat N =50, $1.1e-3) flat recovers only
9/19. At the top end, Lite Sketch K=10, M =10 recovers 15/19 (79%) at $2.8e-3, while flat N =100
at the same candidate count plateaus at 10/19 (53%). The within-tier story is unambiguous; the
cross-tier story is not (Pro greedy dominates Lite+sketch on this benchmark), and we are explicit
about both.

Contributions.

      1. We introduce S KETCH V ERIFY, a within-tier cost-performance policy for code generation
         that applies program sketching as a structured way to spend test-time compute. By fac-
         torizing the search space into algorithmic strategy (K) and implementation detail (M ),
         S KETCH V ERIFY achieves a steeper pass@1 scaling curve than flat sampling within the
         same model tier on Gemini 3.1 Flash Lite.
      2. We report a cost-quality Pareto analysis (Section 4.2) and a hard-subset reanalysis on the
         19 HumanEval+ problems where Lite greedy fails. Within Lite, sketch dominates flat
         sampling at every budget on the hard subset — +32pp at matched candidate count between
         Sketch K=2, M =5 (58%) and flat N =10 (26%), and +11pp even when flat is given ∼3×
         more budget (flat N =50 at 47%). Across tiers, Flash greedy sits on the strict cost-quality
         Pareto frontier and dominates every Lite-with-sketch configuration on both axes; Pro greedy
         matches Flash greedy’s accuracy but is itself dominated on cost. Sketching is a complement
         to, not a substitute for, model upgrading.
      3. We propose category-first sketch generation: enumerate K algorithmic approaches as
         natural-language strategy names before writing any code, then commit each name to a
         code-level sketch with ∼4–8 expression-level holes. The two-step decomposition is what
         produces structural diversity rather than the cosmetic variants flat sampling yields.
      4. We characterize the K vs. M trade-off via the Flash Lite scaling sweep (Table 3). The
         sketch curve is non-monotone: K=2, M =5 (91%) outperforms K=5, M =10 (88%) despite


                                                  2
Algorithm 1 S KETCH V ERIFY Pipeline
Require: Problem π, LLM L, sketch budget K, fill budget M
Ensure: Selected solution s∗
 1: Stage 1 — Sketch:
 2:   {c1 , . . . , cK } ← E NUM C ATEGORIES(L, π, K)
 3: for k = 1, . . . , K do
 4:      σk ← G EN S KETCH(L, π, ck )
 5:      σk ← VALIDATE(σk )                                                          // discard if invalid
 6: end for
 7: Stage 2 — Fill:
 8: for each valid sketch σk do
 9:   for m = 1, . . . , M do
10:          sk,m ← F ILL(L, π, σk )
11:   end for
12: end for
13: Stage 3 — Verify:
14:   S ← {sk,m | sk,m compiles ∧ passes examples}                              // surviving candidates
15:   {x1 , . . . , xD } ← G EN I NPUTS(L, π)
16:   fi ← [si (x1 ), . . . , si (xD )] for each si ∈ S                                    // fingerprint
17: Stage 4 — Select:
18:   C ← C LUSTER B Y F INGERPRINT({(si , fi ) : si ∈ S})
19:   C ∗ ← arg maxC∈C |C|                                                              // largest cluster
20:   s∗ ← arg mins∈C ∗ |s|                                                 // shortest (Occam’s razor)
21: return s∗



         using 5× fewer candidates, and pure-flat (K=1) and pure-sketch (M =1) corners both
         underperform mixed allocations. Both axes matter; budget allocation is non-trivial.
      5. We show that S KETCH V ERIFY composes cleanly with execution-based selection: structured
         generation produces a candidate pool, fingerprint clustering selects among them. On near-
         saturated HumanEval+ the composition matches flat + Semantic Voting on Flash and Lite
         and edges it by +0.7pp on Pro. The two methods are stages of one pipeline (generate
         diversely, select on behavior), not competitors.

Background. A companion measurement on HumanEval+ at N =50 across nine Gemini config-
urations finds that flat sampling produces only 1.2–1.5 distinct execution-fingerprint clusters per
problem, with the dominant cluster covering 76–96% of candidates — temperature controls lexical,
not structural, diversity. Program sketching [Solar-Lezama, 2008, 2013] addresses this in synthesis by
fixing structure (algorithm, data structures, control flow) and leaving expression-level details as holes;
OBsmith [Jiang et al., 2026b] adapted sketching for LLM-powered compiler testing and showed that
sketch-generated programs are more structurally diverse than directly-generated ones. We bring the
same decomposition into inference-time scaling. Recent inference-time-scaling work [Snell et al.,
2025, Wu et al., 2025, Levi, 2024] characterizes flat pass@k curves; we add a structural axis (K)
that flat sampling does not have.

2     Method: S KETCH V ERIFY
2.1   Pipeline overview

Given a problem π and an LLM L, S KETCH V ERIFY proceeds in four stages (Algorithm 1). Note
that the fill budget M and the LLM L are deliberately distinct symbols: M ∈ N is a hyperparameter,
while L is the model.

2.2   Stage 1: Sketch generation via category-first prompting

The central technical challenge is generating sketches that are structurally diverse — not just
superficially different rewrites of the same approach. We propose a category-first strategy that
separates the “what approach” decision from the “how to code it” decision:


                                                    3
Step 1a: Category enumeration. We prompt the LLM: “List K fundamentally different algo-
rithmic strategies for this problem.” The LLM returns strategy names (e.g., “hash map lookup,”
“sorting + two pointers,” “dynamic programming”). This forces the model to reason about the space
of approaches before writing any code, preventing the common failure mode where it fixates on its
default strategy.

Step 1b: Per-category sketch generation. For each strategy name ck , we prompt: “Write a
program sketch using the ‘ck ’ strategy.” The sketch is a partial Python program where:

       • The algorithm, data structures, and control flow are fully specified.
       • Implementation details (expressions, conditions, loop bounds) are replaced with ?? place-
         holders. Each ?? represents a single expression or condition.
       • The sketch targets 4–8 holes: enough to allow meaningful variation in fills, not so many that
         the structural signal is lost.

Why two steps instead of one? Single-shot sketch generation tends to produce variants of the
same approach because autoregressive decoding gravitates toward the highest-probability strategy.
Committing to a strategy name first acts as a structural anchor. Sketch validation, the worked Two
Sum example, and the input-generation prompt are deferred to Appendix C.

2.3   Stages 2–4 in brief

Stage 2 (Fill). For each valid sketch we generate M completions at T =0.8 that replace the ?? holes;
every third fill is conditioned on the previous fill and asked for a different implementation, to push
past the modal fill. Stage 3 (Verify). Each candidate must compile, define the entry point, and not
crash (Tier 1 survival on HumanEval+ at K=10, M =10: 99.9% / 98.8% / 96.7% on Lite / Flash /
Pro). Surviving candidates are executed on D=50 diverse test inputs generated by LLM-powered
sketch-based input generation (Kin =10 categories × Min =5 instantiations), producing an execution
fingerprint: the vector of (status, output) pairs with floats rounded to 6 decimals, exception types
only, and timeouts as a distinct value. Identical fingerprints mean behavioral equivalence on the test
suite. Stage 4 (Select). Cluster passing candidates by fingerprint and return the shortest program
from the largest cluster (Occam’s razor among behavioral equivalents). This is the same selection
rule used by the concurrent Semantic Voting line of work; the only change relative to flat+SV is the
candidate pool. Holding the selector fixed makes any pass@1 difference attributable to structured
generation rather than a smarter selector.

2.4   Token budget

At K=10, M =10, S KETCH V ERIFY costs ∼86K tokens per problem (category enumeration ∼0.4K,
sketch generation ∼6K, fill ∼80K), ∼44% more than flat N =100 at ∼60K. Sketch overhead is ∼7%
of the total budget at this point and falls toward 0 as M grows; the per-candidate fill cost is identical
to flat sampling. We report cost-quality results in dollars at the published Gemini rates (Section 4.2);
a line-by-line breakdown is in Appendix C.

3     Experimental setup
3.1   Benchmarks

We evaluate on HumanEval+ [Liu et al., 2023]: 164 Python code-generation problems with 80×
augmented test suites (the EvalPlus extension of the original HumanEval). All results in this paper are
on HumanEval+. Cross-benchmark validation on MBPP+ [Liu et al., 2023] and LiveCodeBench [Jain
et al., 2025] is the natural follow-up (Section 6).

3.2   Models

We evaluate three Google Gemini models spanning capability tiers: Gemini 3.1 Pro (high), Gemini
3 Flash (medium), and Gemini 3.1 Flash Lite (low), each at the low thinking level. Holding the


                                                   4
model family fixed isolates the effect of S KETCH V ERIFY from confounds introduced by differences
in architecture or training data.

3.3   Baselines

We compare against four baselines:

       1. Greedy decoding (T =0, single sample). Lower bound.
       2. Best-of-N : N candidates at T =0.8; return the first that compiles and runs without crashing.
          Tests whether more candidates help without execution-based selection.
       3. Majority voting [Wang et al., 2023]: cluster candidates by string equality of outputs on the
          auto-generated test inputs and pick the largest group. Standard text-based selection baseline.
       4. Semantic Voting (flat): flat sampling + execution fingerprint clustering. The critical
          comparison — it shares the selection rule with S KETCH V ERIFY but generates candidates by
          flat sampling rather than sketches, so any gap is attributable to structured generation alone.

Reflexion-style sequential refinement [Shinn et al., 2023] is conceptually orthogonal (sequential,
single-strategy) and we discuss it as a complement in Section 5 rather than as an apples-to-apples
baseline.

3.4   Evaluation protocol

Matched candidate count. Our primary comparison matches candidate count (N = K × M )
so any pass@1 difference is attributable to allocation, not budget. At K=10, M =10, N =100.
S KETCH V ERIFY carries a ∼7% sketch-generation overhead at this point (Section 2.4), which we
report as a separate cost-quality axis rather than equalizing with extra flat samples.

Metrics. (1) Pass@1 on augmented test suites (EvalPlus evaluation). (2) Per-problem cost in dollars
at published Gemini rates, used for cost-quality plots.

3.5   Configuration

Default configuration: K=10 sketches, M =10 fills per sketch, temperature 0.8 for fills, 0.7 for
sketches. Test input generation: Kin =10 categories, Min =5 instantiations, yielding D=50 test inputs
per problem. Execution timeout: 5 seconds per candidate per input.


4     Results

4.1   Main results

Table 1 presents pass@1 on HumanEval+ across three Gemini models at the low thinking level. All
methods use N =100 candidates (flat sampling) or K=10 sketches × M =10 fills (S KETCH V ERIFY).
Execution-based methods share the same 50 sketch-generated test inputs per problem.
Two findings emerge from Table 1. First, on Gemini 3.1 Flash Lite, S KETCH V ERIFY reaches 92.1%
— a 6.7pp gain over greedy (85.4%) and 10.4pp over Best-of-N (81.7%) — but flat Semantic Voting
matches it at 92.7%. On HumanEval+, both recover the near-oracle ceiling for Lite, leaving the
within-tier improvement of S KETCH V ERIFY on this benchmark concentrated on the hard subset
(Section 4.2). Second, on Gemini 3.1 Pro, S KETCH V ERIFY reaches 98.1% vs. 97.4% for every flat
baseline, recovering one of the four problems that flat methods miss (152/155 vs. 151/155). On Flash
the two effects cancel: S KETCH V ERIFY matches greedy at 96.3% but trails flat Semantic Voting by
0.7pp.
Aggregate pass@1 on the full HumanEval+ is therefore not where the within-tier story lives. Both
Pro and Flash are near-saturated, and even on Lite the easy problems exhaust most of the gap between
N =1 and N =100. The cleanest comparison is on the subset where the model’s modal strategy is
actually wrong, which is what we turn to next.


                                                   5
                       Method                             Pro†    Flash    Lite
                       Greedy                             97.4     96.3    85.4
                       Best-of-N                          94.8     93.9    81.7
                       Majority Vote                      97.4     97.0    92.7
                       Semantic Voting (flat)             97.4     97.0    92.7
                       S KETCH V ERIFY (B: sem. vote)     98.1     96.3    92.1
Table 1: Pass@1 (%) on HumanEval+ with K=10, M =10. Pro, Flash, and Lite refer to Gemini 3.1
Pro, Gemini 3 Flash, and Gemini 3.1 Flash Lite, all at the low thinking level. † Pro results are on
155/164 problems; 9 problems failed due to API rate limits. On Pro, S KETCH V ERIFY achieves the
best result of all methods (+0.7 pp over flat Semantic Voting), demonstrating that structural diversity
is beneficial even on the near-saturated HumanEval+ when the model’s default strategy occasionally
misses.



4.2   Cost-quality Pareto analysis

The accuracy table above does not directly answer the practitioner’s question: at a given dollar
budget per problem, which (model, method) combination should I deploy? To address this, we plot
every (model, method) point on a cost-quality scatter, with cost computed from the per-call token
budget (Section 2.4) priced at published Gemini rates: $0.015/M input and $0.06/M output for Lite,
$0.075/$0.30 for Flash, and $1.25/$5.00 for Pro. Figure 1 shows the analysis on a 19-problem hard
subset where Lite greedy fails — the regime where extra compute can plausibly help.

Within-tier finding. On the hard subset, the Lite-only Pareto frontier traverses six points (greedy
→ Sketch K=1,M=1 → K=2,M=5 → K=5,M=10 → MV(N=100) → Sketch K=10,M=10) and is
monotone: each additional dollar of Lite compute buys more pass@1 if and only if it is spent on
sketching, not on flat sampling. Flat sampling at N = 100 recovers only 53% of the failures while
Sketch K=10, M =10 recovers 79% (+26pp) at the same candidate count. The dominance is robust:
Sketch K=2, M =5 ($3.8e-4, 58%) is cheaper and more accurate than flat N =50 ($1.1e-3, 47%), so
flat sampling cannot close the gap by buying more samples. Sketching is the cost-effective way to
spend extra compute on a weak model. Table 2 reports the per-configuration solve counts that drive
the Pareto plot.

Cross-tier finding. The strict cross-model Pareto frontier on the hard subset has only two points:
Lite flat N =1 ($2e-5, 16%) and Flash greedy ($1.1e-4, 89%). Pro greedy ($1.9e-3, 89%) is itself
off this frontier — Flash greedy matches its accuracy at ∼17× less cost — but it still dominates
every Lite-with-sketch configuration on both axes (e.g., it is cheaper and +10pp more accurate
than Lite Sketch K=10, M =10 at $2.8e-3 / 79%). Pro Sketch is dominated by Pro greedy. So
sketching is a within-tier complement to model upgrading, not a substitute. A counter-intuitive
corollary: Lite Sketch K=10, M =10 (79%) beats Flash Sketch K=10, M =10 (74%) on the hard
subset, because forcing alternative strategies on a strong model replaces a high-confidence default
with lower-confidence approaches, while on a weak model the default is wrong often enough that any
forced alternative is a net positive.

4.3   Scaling curves

The scaling curve—pass@1 as a function of total inference tokens—is our most direct test of whether
structured generation converts compute into accuracy more efficiently than flat sampling. Figure 3 and
Table 3 compare S KETCH V ERIFY at four budgets (K×M ) against flat sampling + Semantic Voting
at four matched-count budgets (N ) on Gemini 3.1 Flash Lite across 100 HumanEval+ problems.
Lite flat saturates at 89% — adding more candidates does not escape the modal-strategy trap —
while S KETCH V ERIFY crosses that ceiling and reaches 93%. The sketch curve is non-monotone
(K=5, M =10 at 88% slightly trails K=2, M =5 at 91%); both axes matter, and pure-flat (K=1)
and pure-sketch (M =1) corners both underperform mixed allocations. We replicated the sweep on
Gemini 3 Flash (50 HumanEval+ problems): flat greedy already reaches 96% and S KETCH V ERIFY
tops out at 94%, trailing every flat configuration — the factored-search benefit is not universal


                                                  6
                                                   HumanEval+ hard subset: problems where Lite greedy fails (19/152 common)
                                              90                      Flash greedy


    pass@1 (%) on hard subset (19 problems)   80
                                              70
                                              60
                                              50
                                              40
                                              30                                                       Lite                BoN
                                                                                                       Flash               MV / SV-flat
                                                                                                       Pro                 SketchVerify (all K, M)
                                              20                                                       greedy / flat-N=1   Cross-model frontier
                                                   Lite flat-N=1                                       flat-N (scaling)    Within-Lite frontier
                                                               10 4                    10 3               10 2                  10 1
                                                                                Cost per problem (USD, log scale)
Figure 1: Cost-quality Pareto plot on the hard subset of HumanEval+ (19 problems where Lite greedy
fails, intersected with the Lite scaling-curve subset). Each point is one (model, method) configuration.
Within Lite (blue), sketching dominates flat sampling at every budget: Sketch K=2, M =5 at $3.8e-4
/ 58% beats flat N =10 at $2.3e-4 / 26% (+32pp at matched candidate count) and also beats flat
N =50 at $1.1e-3 / 47% by +11pp despite costing 3× less; Sketch K=10, M =10 at $2.8e-3 / 79%
beats flat N =100 at $2.3e-3 / 53% (+26pp at matched candidate count). Across tiers, the cross-model
Pareto frontier (dashed) is just two points: Lite flat N =1 ($2e-5, 16%) and Flash greedy ($1.1e-4,
89%). Pro greedy ($1.9e-3, 89%) is itself off the strict frontier — Flash greedy matches its accuracy
at ∼17× less cost — but Pro greedy still dominates every Lite-with-sketch configuration on both axes.
The honest reading is: sketching is a within-tier complement to model upgrading, not a substitute for
it.


and emerges only when flat sampling’s modal-strategy prior is the binding constraint on accuracy.
Holding the selector fixed and swapping only the candidate pool, S KETCH V ERIFY + SV vs. flat+SV
on HumanEval+ in aggregate is 98.1 vs. 97.4 on Pro, 96.3 vs. 97.0 on Flash, 92.1 vs. 92.7 on Lite:
effectively a tie at the near-oracle ceiling. The within-tier gain is concentrated on the hard subset; full
Flash scaling, the diversity-mechanism discussion, and the composition table are in Appendix D.

5                         Analysis and related work
When does sketching help? S KETCH V ERIFY converts test-time compute into pass@1 more
efficiently than flat sampling when (a) the model’s modal strategy is wrong on a non-trivial fraction
of problems, and (b) it has latent knowledge of an alternative correct strategy. Both hold for
Lite on the hard subset; neither holds for Flash where greedy already reaches 96%. Three failure
modes mark the boundary: (i) overhead without benefit on easy problems where the K sketches
collapse to identical strategies; (ii) strategy-right, implementation-wrong problems (precise floating
point, off-by-one) where the error is upstream of the strategy choice — Reflexion-style sequential
refinement [Shinn et al., 2023] is the higher-leverage move and is complementary to S KETCH V ERIFY;
(iii) category blindness, when the correct approach is outside the model’s strategy distribution at any
tier (HumanEval/38 and HumanEval/50 are missed by every method at every tier we tested).

Related work. Inference-time scaling for code [Snell et al., 2025, Wu et al., 2025, Levi, 2024]
characterizes flat pass@k curves; we add a structural axis. Program sketching [Solar-Lezama, 2008,
2013] is the synthesis ancestor; OBsmith [Jiang et al., 2026b] brought it to LLM-powered compiler
testing, and we bring it to inference-time generation. Planning approaches [Jiang et al., 2024b,


                                                                                            7
             Model           Method                      Cost ($/prob)          Solved / 19           Pass@1     95% CI
             Lite            Flat N =1 (greedy)                    2.3e-5                    3          16%      [5.5, 37.6]
             Lite            Sketch K=1, M =1                      1.3e-4                    9          47%      [27.3, 68.3]
             Lite            Flat N =10                            2.3e-4                    5          26%      [11.8, 48.8]
             Lite            Sketch K=2, M =5                      3.8e-4                   11          58%      [36.3, 76.9]
             Lite            Flat N =50                            1.1e-3                    9          47%      [27.3, 68.3]
             Lite            Sketch K=5, M =10                     1.5e-3                   12          63%      [41.0, 80.9]
             Lite            Flat N =100                           2.3e-3                   10          53%      [31.7, 72.7]
             Lite            MV / SV-flat (N =100)                 2.3e-3                   13          68%      [46.0, 84.6]
             Lite            Sketch K=10, M =10                    2.8e-3                   15          79%      [56.7, 91.5]
             Flash           Greedy                                1.1e-4                   17          89%      [68.6, 97.1]
             Flash           SV-flat (N =100)                      1.2e-2                   16          84%      [62.4, 94.5]
             Flash           Sketch K=10, M =10                    1.4e-2                   14          74%      [51.2, 88.2]
             Pro             Greedy                                1.9e-3                   17          89%      [68.6, 97.1]
             Pro             SV-flat (N =100)                      1.9e-1                   17          89%      [68.6, 97.1]
             Pro             Sketch K=10, M =10                    2.3e-1                   16          84%      [62.4, 94.5]
Table 2: Pass@1 on the 19-problem hard subset of HumanEval+ (problems where Lite greedy fails,
intersected with the Lite scaling-curve subset). Per-problem cost is computed from input/output
tokens at published Gemini rates. CIs are Wilson 95% intervals; with n=19 they are wide on absolute
terms, so we lean on directional consistency across budgets: within Lite, every sketch configuration
beats the nearest flat configuration, and the within-tier Pareto frontier (bolded: K=2, M =5 and
K=10, M =10) is monotone in sketch budget. Across tiers, Flash and Pro greedy strictly dominate
Lite + sketch on both axes.



                                            Hard-subset solve matrix (Lite, low thinking): blue = solved
            Flat N = 1                                                                                                          3/19
           Flat N = 10                                                                                                          5/19
           Flat N = 50                                                                                                          9/19
          Flat N = 100                                                                                                          10/19
   Sketch K = 1, M = 1                                                                                                          9/19
   Sketch K = 2, M = 5                                                                                                          11/19
  Sketch K = 5, M = 10                                                                                                          12/19
 Sketch K = 10, M = 10                                                                                                          15/19
                         0     3   4   6   7     8     10    12    14   17     21    22    25    28    29   32   38   50   77
                                                      HumanEval+ task ID (hard subset, n = 19)

Figure 2: Per-problem solve matrix on the 19-problem hard subset for Gemini 3.1 Flash Lite at low
thinking. Blue cells are solved, gray are unsolved; the horizontal line separates flat from sketch
configurations. Two patterns drive the within-tier story: (a) the sketch block is denser than the
flat block at every matched-budget pair, so the +pp gaps in Table 2 are not concentrated on one or
two anomalous problems; and (b) problems 6, 8, 10, 14, 17, 29, and 32 are solved only by sketch
configurations, never by any flat sample budget, evidence that flat sampling’s modal-strategy prior
systematically misses on these problems. Problems 38 and 50 are unsolved by every method we
tested at every tier (see Section 5, failure mode 3).



Wen et al., 2025] produce a single plan; we generate K plans and M fills per plan. Selection-side
methods — CodeT [Chen et al., 2023], MBR-Exec [Shi et al., 2022], AlphaCode [Li et al., 2022],
Coder-Reviewer [Zhang et al., 2023] — improve selection from a candidate pool whose diversity is
left to chance; S KETCH V ERIFY changes what is generated and composes with any execution-based
selector. Concurrent Semantic Voting clusters flat samples by execution fingerprint; we reuse its
selector but replace the pool. Aytes et al. [2025], Jiang et al. [2024a], Jiang et al. [2026a], Zhong
et al. [2025a], Zhong et al. [2025b], and Hong et al. [2025] treat LLMs as program reasoners (oracle
generation, deobfuscation, API synthesis, formal-specification writing), supporting our use of LLMs
for both sketch generation and filling.


                                                                    8
       Pass@1 vs token budget: Gemini 3.1 Flash Lite (low thinking, HumanEval+)
                                                                        K=10,M=10

                     92                                                    K=2,M=5

                     90
                                                                                               K=5,M=10
                                                                                                   N=100
                     88
       Pass@1 (\%)

                                                                                        N=50
                     86
                                                                    N=10
                     84
                                                         K=1,M=1
                     82
                                                                    SketchVerify
                     80                                             Flat sampling + Semantic Voting
                              N=1
                                    103                            104                                105
                                          Total inference tokens per problem (log scale)
Figure 3: Pass@1 vs. total inference tokens per problem on HumanEval+ (Gemini 3.1 Flash Lite,
100 problems). The x-axis is log-scaled; each point is labeled with its (K, M ) or N configuration.
S KETCH V ERIFY (blue) lies above flat sampling + Semantic Voting (red) at every matched token
budget except the rightmost point, where flat saturates at 89% while S KETCH V ERIFY reaches 93% at
K=10, M =10. The gap is largest in the low-budget regime (∼10K tokens, 91% vs. 85%), where
flat sampling relies on a small number of i.i.d. samples that tend to share the same mode. The
non-monotonic point at K=5, M =10 (88%, below K=2, M =5 at 91%) is discussed in Appendix D.


                          S KETCH V ERIFY (factored)                                 Flat sampling + SV
    Config                      Tokens Pass@1 95% CI                Config              Tokens Pass@1       95% CI
    K=1, M =1                  ∼3.8K        82.0%    [73.3, 88.3]   N =1 (greedy)      ∼0.6K       80.0%    [71.1, 86.7]
    K=2, M =5                 ∼11.6K        91.0%    [83.8, 95.2]   N =10              ∼8.0K       85.0%    [76.7, 90.7]
    K=5, M =10                ∼45.4K        88.0%    [80.2, 93.0]   N =50             ∼32.0K       88.0%    [80.2, 93.0]
    K=10, M =10               ∼88.4K        93.0%    [86.3, 96.6]   N =100            ∼62.0K       89.0%    [81.4, 93.7]

Table 3: Scaling-curve data points on HumanEval+ (Gemini 3.1 Flash Lite, 100 problems). Token
counts are per-problem, summed across category enumeration, sketch generation, fill, and (for flat)
direct sampling. CIs are Wilson 95% intervals; with n=100 problems they are ±5–8pp wide, so
the consistent direction across budgets carries the argument rather than any single comparison. Key
comparisons: at a matched ∼10K-token budget, S KETCH V ERIFY K=2, M =5 reaches 91.0% while
flat sampling + SV at N =10 reaches 85.0% — a 6 pp gap. At ∼45K tokens the two are tied
(88%). At ∼62K tokens flat saturates at 89.0% (N =100), while S KETCH V ERIFY at ∼88K tokens
reaches 93.0% (K=10, M =10) — a 4 pp advantage at the top end despite the sketch-generation
overhead.



6     Conclusion

S KETCH V ERIFY is a within-tier cost-performance policy supported on the HumanEval+ hard subset
where Lite greedy fails: Sketch K=2, M =5 beats flat N =10 by +32pp and Sketch K=10, M =10
beats flat N =100 by +26pp. The cross-tier claim is not supported: Pro greedy dominates Lite Sketch
K=10, M =10 on both axes, so sketching complements model upgrading rather than replacing it.
Limitations: single model family (Gemini), single thinking level, single benchmark (Pro and Flash
near-saturated), coarse (K, M ) grid, sketch quality bounded by the model’s strategy distribution,
and ∼7% sketch-generation overhead. Clean follow-ups: adaptive-K, sketch-level tree search,
cross-family validation, and validation on harder benchmarks (LiveCodeBench, MBPP+).


                                                                9
References
Simon A. Aytes, Jinheon Baek, and Sung Ju Hwang. Sketch-of-thought: Efficient LLM reasoning
  with adaptive cognitive-inspired sketching. In Conference on Empirical Methods in Natural
  Language Processing, 2025.
Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu
  Chen. CodeT: Code generation with generated tests. In International Conference on Learning
  Representations, 2023.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
 language models trained on code. arXiv preprint arXiv:2107.03374, 2021.
Yang Hong, Shan Jiang, Yulei Fu, and Sarfraz Khurshid. On the effectiveness of large language
  models in writing Alloy formulas. arXiv preprint arXiv:2502.15441, 2025.
Yuichi Inoue, Kou Misaki, Yuki Imajuku, So Kuroki, Taishi Nakamura, and Takuya Akiba. Wider or
  deeper? scaling LLM inference-time compute with adaptive branching tree search. In Advances in
  Neural Information Processing Systems, 2025.
Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando
  Solar-Lezama, Koushik Sen, and Ion Stoica. LiveCodeBench: Holistic and contamination free eval-
  uation of large language models for code. In International Conference on Learning Representations,
  2025.
Shan Jiang, Chenguang Zhu, and Sarfraz Khurshid. Generating executable oracles to check
  conformance of client code to requirements of JDK Javadocs using LLMs. arXiv preprint
  arXiv:2411.01789, 2024a.
Shan Jiang, Pranoy Kovuri, David Tao, and Zhixun Tan. CASCADE: LLM-powered JavaScript
  deobfuscator at Google. In ICSE-SEIP, 2026a.
Shan Jiang, Chenguang Zhu, and Sarfraz Khurshid. OBsmith: LLM-powered JavaScript obfuscator
  testing. In ACM SIGPLAN International Conference on Object-Oriented Programming, Systems,
  Languages, and Applications (OOPSLA), 2026b.
Xue Jiang, Yihong Dong, Lecheng Wang, Zheng Fang, Qiwei Shang, Ge Li, Zhi Jin, and Wenpin
 Jiao. Self-planning code generation with large language models. ACM Transactions on Software
 Engineering and Methodology, 33(7), 2024b.
Noam Levi. A simple model of inference scaling laws. arXiv preprint arXiv:2410.16377, 2024.
Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom
  Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, et al. Competition-level code generation
  with AlphaCode. Science, 378(6624):1092–1097, 2022.
Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is your code generated by
   ChatGPT really correct? Rigorous evaluation of large language models for code generation. In
   Advances in Neural Information Processing Systems, 2023.
Freda Shi, Daniel Fried, Marjan Ghazvininejad, Luke Zettlemoyer, and Sida I Wang. Natural language
  to code translation with execution. In Conference on Empirical Methods in Natural Language
  Processing, 2022.
Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion:
  Language agents with verbal reinforcement learning. In Advances in Neural Information Processing
  Systems, 2023.
Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time compute optimally
  can be more effective than scaling parameters for reasoning. In International Conference on
  Learning Representations, 2025.
Armando Solar-Lezama. Program Synthesis by Sketching. PhD thesis, University of California,
  Berkeley, 2008.


                                                10
Armando Solar-Lezama. Program sketching. International Journal on Software Tools for Technology
  Transfer, 15:475–495, 2013.

Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdh-
  ery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models.
  In International Conference on Learning Representations, 2023.

Jiaxin Wen, Jian Guan, Hongning Wang, Wei Wu, and Minlie Huang. CodePlan: Unlocking reasoning
   potential in large language models by scaling code-form planning. In International Conference on
   Learning Representations, 2025.

Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang. Inference scaling laws:
  An empirical analysis of compute-optimal inference for LLM problem-solving. In International
  Conference on Learning Representations, 2025.

Tianyi Zhang, Tao Yu, Tatsunori Hashimoto, Mike Lewis, Wen-tau Yih, Daniel Fried, and Sida I
  Wang. Coder reviewer reranking for code generation. In International Conference on Machine
  Learning, 2023.

Hua Zhong, Shan Jiang, and Sarfraz Khurshid. An approach for API synthesis using large language
  models. arXiv preprint arXiv:2502.15246, 2025a.

Hua Zhong, Shan Jiang, and Sarfraz Khurshid. APRIL: API synthesis with automatic prompt
  optimization and reinforcement learning. arXiv preprint arXiv:2509.25196, 2025b.

Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. Language
  agent tree search unifies reasoning, acting, and planning in language models. In International
  Conference on Machine Learning, 2024.


A     Prompts

We provide the exact prompts used in all stages. All prompts are zero-shot.

A.1   Category enumeration prompt

Given this programming problem, list {K}
fundamentally different algorithmic STRATEGIES
that could solve it. Each strategy should use
a different core algorithm or data structure.

Problem:
{problem_description}

Function signature:
{function_signature}

Output a JSON array of strategy names, e.g.:
["hash map lookup", "sorting + two pointers",
 "brute force nested loops", ...]

List EXACTLY {K} strategies. Be creative ---
consider approaches from different algorithmic
paradigms (brute force, sorting, hashing, two
pointers, binary search, dynamic programming,
greedy, stack/queue, divide and conquer,
math/formula, graph-based, bit manipulation).

Return ONLY the JSON array, no other text.


                                                11
A.2   Sketch generation prompt

Write a Python program SKETCH using the
"{category}" strategy for this problem.

Problem:
{problem_description}

Function signature:
{function_signature}

A sketch is partial Python code where
implementation details are replaced with ??
placeholders. Rules:
- The overall structure (algorithm, data
  structures, control flow) must be fully
  specified
- Replace expressions, conditions, and short
  fragments with ??
- Each ?? should represent a single expression
  or condition (not multiple statements)
- The sketch must be syntactically valid Python
  EXCEPT for ?? tokens
- Include a one-line comment at the top naming
  the approach
- Target 4-8 holes (??) per sketch

Output ONLY the Python code block,
no explanations.

A.3   Sketch filling prompt

Complete this program sketch by replacing
every ?? with the correct Python expression
or code fragment.

Problem:
{problem_description}

Sketch ({category}):
‘‘‘python
{sketch_code}
‘‘‘

Rules:
- Replace each ?? with a single Python
  expression or condition
- The result must be a valid, complete,
  executable Python function
- Do NOT change the overall structure ---
  keep the same algorithm, loops, and
  data structures
- Output ONLY the completed function,
  no explanations

A.4   Diversity fill prompt

Used every 3rd fill to encourage variation:


                                              12
Complete this program sketch by replacing
every ?? with a DIFFERENT but still correct
Python expression compared to the previous
completion.

[same problem and sketch as above]

Previous completion (generate something
DIFFERENT):
‘‘‘python
{previous_fill}
‘‘‘

Rules:
- Replace each ?? differently from the
  previous completion
- The result must still be correct and
  executable
- Keep the same overall structure
- Output ONLY the completed function


B    Full configuration details


                            Parameter                        Value
                            Sketch budget K                  10
                            Fill budget M                    10
                            Sketch temperature               0.7
                            Fill temperature                 0.8
                            Category temperature             0.7
                            Test input categories Kin        10
                            Test input instantiations Min    5
                            Total test inputs D              50
                            Execution timeout                5 seconds
                            Max output tokens (fill)         2048
                            Max output tokens (sketch)       2048
                            Max output tokens (category)     1024
                 Table 4: Full hyperparameter configuration for S KETCH V ERIFY.




C    Method details

Sketch validation. Each generated sketch must (1) contain a function definition, (2) have at least
one ?? hole, (3) contain a return statement, and (4) parse as valid Python when holes are replaced
with a placeholder identifier ( ph ). We use a placeholder rather than None because ?? can appear in
assignment targets (e.g., for ?? in ??:), where None is syntactically invalid. Invalid sketches
are discarded.

Worked example. For a “two sum” problem, category-first generation with K=3 might produce
three sketches encoding hash table O(n), sorting + two pointers O(n log n), and brute force O(n2 )
strategies, each with 4–8 expression-level holes (??) for loop bounds, comparison conditions, and
return values; fills then concretize the holes while preserving the algorithmic skeleton.

Per-problem token cost.


                                                13
                 Step                         Calls      In/call    Out/call           Total
                 Category enumeration          1          ∼300            ∼100        ∼400
                 Sketch generation            K           ∼400            ∼200       ∼6,000
                 Sketch filling            K ×M           ∼500            ∼300      ∼80,000
                 S KETCH V ERIFY total                                             ∼ 86,400
                 Flat sampling (N =100)         100       ∼300            ∼300      ∼60,000


D    Additional results
Scaling on Gemini 3 Flash.


            S KETCH V ERIFY (factored)                                      Flat sampling + SV
 Config           Tokens Pass@1 95% CI                   Config                Tokens Pass@1          95% CI
 K=1, M =1          ∼3.8K      80.0%    [67.0, 88.8]     N =1 (greedy)        ∼0.6K          96.0%    [86.5, 98.9]
 K=2, M =5         ∼11.6K      90.0%    [78.6, 95.7]     N =10                ∼8.0K          96.0%    [86.5, 98.9]
 K=5, M =10        ∼45.4K      94.0%    [83.8, 97.9]     N =50               ∼32.0K          96.0%    [86.5, 98.9]
 K=10, M =10       ∼88.4K      94.0%    [83.8, 97.9]     N =100              ∼62.0K         pending   —

50-problem subset of HumanEval+; Wilson 95% CIs. Flash’s greedy already saturates at 96%, so the
sketch curve sits below the flat ceiling at every budget, with overlapping CIs. This is the operational
regime where factored search has nothing to factor and thus cannot help.

Diversity mechanism. The hard-subset gap is consistent with a simple mechanism: each category-
first sketch is a different algorithmic strategy by prompt design, so the sketch stage upper-bounds
behavioral diversity at K rather than at the model’s modal-strategy prior (Section 1). Direct mea-
surement of fingerprint-cluster counts under S KETCH V ERIFY on the same Lite scaling subset is in
progress.

K-vs-M trade-off. The four S KETCH V ERIFY points in Table 3 establish three patterns: (i) K=1
collapses toward flat sampling (K=1, M =1 at 82% sits within 2pp of flat N =1 at 80%); (ii) even
small K pays off (K=2, M =5 at 91% vs. flat N =10 at 85%, +6pp at matched candidate count,
attributable to K rather than M ); (iii) returns to scale are non-monotone (K=5, M =10 at 88% trails
K=2, M =5 at 91% despite using ∼4× the tokens, while K=10, M =10 at 93% is the best point). A
fixed-budget (K, M ) grid at N =100 is the cleanest follow-up.

Composition with Semantic Voting.

                     Generation         Selection                  Pro     Flash     Lite
                     Flat sampling      First passing (BoN)        94.8     93.9     81.7
                     Flat sampling      Semantic Voting            97.4     97.0     92.7
                     S KETCH V ERIFY    Semantic Voting            98.1     96.3     92.1

On HumanEval+ in aggregate, execution-based selection is the dominant improvement over Best-
of-N , and structured generation does not add further gains on top of Semantic Voting at the full-
benchmark level (consistent with the saturation ceiling). The within-tier value of S KETCH V ERIFY is
concentrated on the hard subset (Section 4.2, Table 2).

Released artifacts. Per-problem breakdowns, per-(K, M ) scaling data, and per-model results are
included in the released code repository under results/. Each run stores the selected candidate for
every problem, per-configuration metrics, and a cost-tracker log so that downstream analyses can be
re-derived without additional API calls.

E    Broader impacts
S KETCH V ERIFY reallocates LLM inference compute at test time; it does not train new models
or change what tasks an LLM can perform, only how candidates are generated and selected for


                                                    14
code-generation problems. The most plausible positive impact is making weaker, cheaper code
models more accurate for budget- or latency-constrained users (educational settings, low-resource
deployments), which lowers the cost barrier to capable AI-assisted coding. The most plausible
negative impact is amplifying existing risks of LLM-generated code: confidently-wrong solutions
selected by the consensus-based selector, propagation of insecure or biased code patterns from training
data, and over-reliance on automated suggestions in domains where human review is essential. Two
structural features of S KETCH V ERIFY bear directly on these risks: (i) execution-based selection filters
out crashes but not silent semantic errors, so users should still treat selected candidates as suggestions
rather than verified solutions; and (ii) the diversity-of-strategies design surfaces alternative algorithms,
which can help users notice when the model’s modal solution is wrong but does not guarantee
any candidate is correct. We did not introduce new generative capabilities, so the harm surface of
S KETCH V ERIFY is bounded by the base models it wraps; standard mitigations (sandboxed execution,
human review, security audits of generated code) apply unchanged.




                                                    15
