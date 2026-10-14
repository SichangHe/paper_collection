                                                         Operator Packages, Proposer Strength, and
                                                             Construction-Family Plateaus in
                                                                Office-Scale Verified Search
                                                                         Roberto I. Ono Filho
                                                                        Independent researcher
                                                          ono.roberto@gmail.com ORCID 0009-0006-8650-629X
arXiv:2609.29636v1 [cs.CL] 28 Aug 2026




                                                                                           Abstract
                                                  Verified search, in which a language model proposes programs, a hard evaluator scores
                                              them, and selection keeps the best, has recently moved mathematical records; controlled
                                              ablations of the proposer-side components remain rare. We instrument a minimal FunSearch-
                                              style loop at office scale (a 30B local model on a laptop, 120–600 verified samples per
                                              run) with three operator packages: a schematic notebook the model writes and carries
                                              instead of verbatim elites, a named obstacle, and behavioural repulsion from constructions
                                              already found. On nine construction problems from a public repository, the complete 23
                                              factorial with two replicates favours the primary contrast in a nominal two-stage analysis:
                                              the composition closes more of the seed-to-record gap (+0.196 [+0.059, +0.343]; nominal
                                              pooled p = 0.023, stage-combination p ≈ 0.08; median per-problem effect +0.045; robust
                                              to removing the seed floor from the metric). Repulsion raises construction-hash diversity
                                              everywhere (+0.31, p = 0.0039; partly a manipulation check, since the operator optimizes a
                                              relative of this quantity). The factorial finds no positive memory-by-repulsion interaction and
                                              bounds any such interaction to about ±0.04: the gain decomposes additively, the notebook
                                              package carrying the largest descriptive share, and memory+repulsion is the only arm that
                                              never collapses (0 of 18 runs), with a mean 0.025 below the full composition’s, a difference
                                              unresolved at n = 9. A frontier proposer under the identical loop reaches in tens of samples
                                              what the local model does not in hundreds, and in single scoping runs its gains arrive without
                                              the operators (differences at most 0.003). The search stalls after closing ≈92% of the gap
                                              toward the best published construction on the flagship problem, and the registered family-hint
                                              test gives the stall its first reading: named in words, the reference family is adopted and
                                              loses; handed as code, it is optimized but its best tested finite-grid implementation remains
                                              below the plateau reached unaided. The loop transported and optimized the idea it was
                                              handed; no unaided run produced it. We release the harness, every candidate, and the dated
                                              pre-registrations.


                                         1    Introduction
                                         FunSearch [13] and AlphaEvolve [10] demonstrated that a language model inside an evolutionary
                                         loop with a hard evaluator can produce genuinely new mathematical constructions. The systems
                                         that followed improved the scaffolding: sample-efficient archives and novelty rejection [6], verbal
                                         reflections as search gradients [16], stronger databases and routing. Two questions have stayed
                                         unmeasured. First, which parts of what the proposer is asked to think (its memory of the lineage,
                                         its statement of the obstacle, its relation to what was already found) change the search, and
                                         by how much? The prompts of the published systems show elite programs verbatim and vary
                                         everything else. Second, how much of the outcome is the proposer itself, holding the loop fixed?
                                         Published systems change model and scaffold together.
                                             This paper measures both, at a scale any laboratory can afford, with the discipline our earlier
                                         studies [11] found necessary: every battery pre-registered before running, dated amendments,

                                                                                            1
exact paired tests, and negative results reported at the same volume as positive ones. The
operators we test are not arbitrary: they are the three interventions that survived a two-paper
program on open-ended generation: a schematic memory (the model’s own compressed recap
outperformed verbatim context on document-level integration), a standing question, and repulsion
from the already-produced, which in weight space collapsed without an anchor and in behaviour
space is the natural tail-preserving form.

Contributions. (1) A pre-registered program of cognitive operators inside a fixed verified-
search loop, grown from a 5×6×2 ablation to the complete 23 ×9×2 factorial: the composition
reaches +0.196 (nominal p = 0.023 over the two-stage sequence; robust to the metric’s seed
floor), behavioural repulsion buys construction-hash diversity in every problem and replicate
(p = 0.0039), and no single package avoids every failure mode. (2) A revision, by the com-
pleted factorial, of this program’s recurring anchoring pattern: the factorial finds no positive
memory×repulsion interaction and bounds any such interaction to about ±0.04 of frac; what
remains of anchoring is descriptive collapse prevention, not superadditive gain. Repulsion without
memory still breaks (three collapses in eighteen runs; four when paired with agenda), while
memory+repulsion never does, echoing unanchored preference optimization in weight space.
(3) A scaling inversion: from a 120-sample tie, the composed arm climbs to 0.3816 at 600
samples while repulsion alone stalls at 0.3514: diversity without accumulated direction does not
compound. (4) A controlled proposer comparison: local 30B versus a frontier model under the
identical loop and budget, on the same problem, locating the residual gap in the proposer rather
than in the loop, with a frontier-strength scoping run in which the single-run operator differences
are at most 0.001–0.003. (5) An honest calibration of office-scale verified search: the composed
arm closes a median 0.71 of the seed-to-reference gap (per-problem 0.10–0.99; two problems sit
at plateaus every arm shares), the tested grid and verifier-time changes did not improve the
result, a stronger proposer raised and accelerated the flagship plateau without closing the final
gap, and the construction family remains the leading suspect for the binding constraint.


2    Related work
Verified search systems. FunSearch evolved single functions with small code models and
millions of samples [13]; AlphaEvolve evolves whole files with frontier ensembles and thousands
[10], and its repository of 67 problems with official verifiers [3] is the substrate of our experiments.
ShinkaEvolve reports record-level results with ∼150 samples using novelty-based rejection and
bandit model selection [6]; ReEvo uses model-written reflections as “verbal gradients” [16]. Our
schematic notebook differs from ReEvo’s reflections in being a persistent, compressed lineage
memory that replaces verbatim elites rather than commenting on pairs. A recent wave adds
persistent memory to evolutionary code search: ε-MemEvo transfers compact strategy summaries
across tasks with an adaptive injection gate and reports gate ablations [8]; EvoMem reuses
mutation knowledge across runs [14]; MEMOIR shares algorithmic and failure-mode summaries
across search branches [5]. What remains absent, and what we contribute, is a complete factorial,
within one task suite and under a fixed local proposer, of a schematic-notebook package, an
obstacle line, and a construction-hash duplicate control. LoongFlow [15] composes planning,
hybrid memory and MAP-Elites niches into one system and reports large efficiency gains; it is
the closest architecture to our composed arm, and exactly the kind of system whose components
an ablation like ours aims to isolate.

Why diversity needs help. Without selection pressure, LLM mutation chains collapse
into attractor regions [4]; RL-tuned models lose pass@k coverage relative to their base [17];
and coverage under repeated sampling grows log-linearly only when a verifier exists [2]. Our


                                                   2
behavioural-repulsion operator is novelty search [7, 9] transplanted into the proposer’s prompt,
with the construction itself (not an embedding) as the behaviour descriptor.


3    The harness, the operators, the problems
Loop. A minimal FunSearch-style loop: K islands, each holding its best programs; per genera-
tion, per island, a prompt is built and S candidates sampled; each candidate runs in a sandbox
(time and memory limits) and is scored by the problem’s verifier; islands keep bounded elites and
migrate their best every third generation. The proposer is Qwen3-Coder-30B-A3B-Instruct
(8-bit, MLX, on a MacBook M5 Pro) prompted through its chat template; Section 5 swaps
in Claude Opus 5 through an API under the identical loop. Every candidate is logged: code,
score, error, generation, island, and a behaviour signature (a hash of the rounded construction it
outputs).

Operators. A (baseline): the prompt shows the statement and the island’s top-3 programs
with scores, FunSearch-style. B (schematic notebook): each generation the model writes a
≤12-line notebook (what worked, what failed and why, the open question) from the elites and
the recent failures; the prompt then shows the notebook and only the single best program. C
(agenda): one model-written line naming the structural obstacle of the current best, appended
to the prompt. D (behavioural repulsion): candidates whose construction duplicates an island
member’s are rejected, and the prompt lists already-found constructions as forbidden. E:
B+C+D. We refer to these as operator packages: each bundles several changes at once (B
replaces three verbatim elites with one, adds failure summaries and an open question, and
spends an extra call; D combines a prompt-level forbidden list with a post-verification duplicate
filter), so the factorial isolates packages, not single cognitive mechanisms; a finer within-package
decomposition is registered as future work.

Problems. Nine construction problems ported from the official repository notebooks, chosen
for cheap exact verification and known headroom. The original battery: circle packing (26 circles,
maximize the sum of radii), ring loading (m=15, exact 2m verification), beat-the-average (a
pmf maximizing P [X1 +X2 +X3 < 2X4 ]), the first autocorrelation inequality (minimize an upper
bound on C1 ), isosceles-free subsets of the 642 grid, and sum-difference III. A pre-registered
extension, run before any n=9 analysis, added three: the max–min pairwise-distance ratio for
16 points in the plane (minimize), the Heilbronn triangle problem for 11 points (maximize
the smallest triple area), and splitting 180! into 180 factors maximizing the smallest (exact
big-integer verification). Each run’s budget is 120 verified samples (10 generations × 2 islands
× 6); the primary metric frac is the fraction of the seed-to-record gap closed, auc its mean over
the budget (sample efficiency), div the share of distinct behaviours among valid candidates.


4    The factorial
Pre-registered contrasts (exact paired sign-flip over problems, cells = problems, pooled replicates).
The original six-problem battery put the primary contrast at the design’s resolution floor (+0.199,
p = 0.0625; with six cells and one adverse problem the exact test cannot go below 4/64); the
prospectively registered nine-problem extension supports it: F1 (primary), E vs A on frac:
+0.196 [+0.059, +0.343], p = 0.023 over the combined nine problems. We report the stages
separately, since the combination is a two-look sequence rather than an independent confirmation:
the three extension problems alone are positive but underpowered (+0.19 on average, p = 0.25,
carried mostly by max–min distance), and a Fisher combination of the stage p-values (0.0625,


                                                 3
frac (pooled over 2 replicates)        A        B          C       D       BC      BD      CD        E
circle packing 26                     0.703   0.974       0.976   0.000   0.989   0.752   0.980    0.992
ring loading 15                       0.444   0.767       0.808   0.808   0.731   0.808   0.808    0.808
beat-the-average                      0.181   0.384       0.519   0.608   0.661   0.789   0.540    0.709
autocorrelation C1                    0.059   0.156       0.041   0.202   0.014   0.212   0.000    0.104
isosceles-free 642                    0.560   0.560       0.560   0.399   0.560   0.560   0.560    0.560
sum-difference III                    0.392   0.329       0.253   0.158   0.314   0.327   0.069    0.362
max–min distance 16                   0.169   0.992       0.372   0.993   0.919   0.793   0.247    0.708
Heilbronn triangle 11                 0.672   0.431       0.507   0.540   0.371   0.477   0.619    0.700
180! into 180 factors                 0.774   0.774       0.774   0.774   0.774   0.774   0.774    0.774
mean frac                             0.439   0.596       0.534   0.498   0.592   0.610    0.511   0.635
mean construction-hash diversity       0.41    0.53        0.52    0.72    0.59    0.68    0.80     0.70
collapses (frac < 0.05, of 18 runs)     2        1           1      3       2       0        4       1

Table 1: The complete 23 factorial over nine problems, pooled over two independent replicates (120
verified samples per run). frac = fraction of the seed-to-record gap closed. E has the best mean and
is best or tied-best in five of nine problems; D alone is bimodal: best on wide valid manifolds (pmfs,
sequences), catastrophic where validity is fragile (packing geometry, constrained integer sets); BD is the
only arm that never collapses, CD the one that collapses most; two problems (isosceles-free, 180!) are
family plateaus where every arm meets the same wall.


0.25) gives p ≈ 0.08, so the pooled 0.023 should be read as nominal accumulated evidence. The
result is robust to the outcome definition: with the seed floor removed the contrast is unchanged
(+0.196, p = 0.023), and excluding the two problems where every arm meets the same plateau it
rises to +0.252 at the same p (n = 7). The effect is also heterogeneous (Figure 1): the median
per-problem effect is +0.045, leave-one-problem-out means span +0.153 to +0.224, with large
gains on four problems, little on four, and one small loss. F4, D vs A on construction-hash
diversity: +0.307 [+0.149, +0.477], p = 0.0039, the minimum attainable p, positive in all nine
problems in both replicates. F6 (the anchor), E vs D: +0.137 [-0.047, +0.382], p = 0.156:
not supported as a pairwise contrast; the factorial below resolves what it was measuring. F2
(auc): +0.115, p = 0.070: the composed arm’s advantage builds late. (The operators’ measured
overhead is small: one extra call per island-generation per operator, ∼220 characters each, 1–3%
of proposer output; Section 9 gives the accounting.)

The completed 23 . Three pairwise arms (memory+agenda, memory+repulsion,
agenda+repulsion) over the same nine problems and two replicates complete the cube (8
cells × 9 × 2; pre-registered before running). The effect-coded analysis (exact sign-flip over
problems, 29 ) finds no evidence for the primary interaction: memory×repulsion β = +0.003
[-0.039, +0.035], p = 0.47 one-sided; agenda×repulsion is null (−0.007, p = 0.79); and no
main effect survives BH correction: schematic memory is the largest single term (β = +0.057
[+0.014, +0.105], raw p = 0.047, q = 0.14), agenda (+0.016) and repulsion (+0.011) near zero
on frac. The decomposition is exact (E − A = 2 (βM + βA + βR + βM AR ) = 0.196): the nominal
pooled composite gain splits as roughly 58% notebook, 16% agenda, 12% repulsion and 14%
three-way (a descriptive decomposition with wide per-term intervals); at n = 9 the total total is
directionally supported, the parts remain unresolved. Two patterns in the cube are worth the
trip. First, each operator has one job (Table 1, Figure 2): the four memory-on cells hold the four
best mean fracs, while every repulsion-on cell sits at 0.68–0.80 construction-hash diversity against
0.41–0.59 without it; directionally, B-on cells hold the higher means and D-on cells the higher
hash diversity, with the caveat that no main effect survives correction. Second, the anchor lives
in the tail, not the mean: memory+repulsion is the only arm that never collapses (0 of 18 runs,
against 3 for repulsion alone and 4 for agenda+repulsion, the cube’s worst), so what memory
buys repulsion is insurance against starving the island, not superadditive mean gain. Agenda,

                                                      4
Figure 1: The primary contrast, problem by problem: E − A on the fraction of the seed-to-record gap
closed (pooled over two replicates). Small grey dots are the two replicates (lines join them); the large
dot is their mean. The pooled mean is +0.196; the median, +0.045; leave-one-problem-out means stay
between +0.153 and +0.224. Within-problem replicate spread is large on several problems (circle packing:
+0.01 and +0.56), which the problem-level test does not see.


decomposed at last, pays for neither: near-zero on frac alone, and the worst collapse count when
paired with repulsion. Exploratory pairwise contrasts back the parsimony reading: E vs BD
+0.025 (p = 0.55, median 0.000), E vs B +0.039 (p = 0.47), BD vs B +0.014 (p = 0.81), all null
at n = 9. The collapse asymmetry is robust to the threshold: at frac ≤ 0, < 0.01, < 0.05 and
< 0.10 the counts stay 3/3/3/3 for repulsion alone and 3/4/4/4 for agenda+repulsion against
0/0/0/0 for memory+repulsion, and no run anywhere produced zero valid candidates, so these
are performance collapses, not validity collapses.
     The heterogeneity is the finding the factorial adds to the literature: where the valid manifold
is wide (a pmf, a sequence of pairs), repulsion alone is the best single operator; where validity
is fragile (non-overlapping circles, exact integer constraints), it is associated with performance
collapses (both replicates of circle packing), and the composed arm inherits most of the benefit
with none of the catastrophes. No single package avoids every failure mode; memory+repulsion
was the only configuration that avoided all of them in these runs.


5    Scale, proposers, and the wall
We then took the problem with guaranteed headroom, beat-the-average, where AlphaEvolve’s
own reported value (0.3890) sits below the best known (0.400695), and ran a pre-registered
ladder. (i) Budget: at 600 samples the composed arm reaches 0.3816 while repulsion alone,
which had tied it at 120 samples, stalls at 0.3514: diversity without accumulated direction does
not compound. (The same 5× extension on max–min distance 16 left both local arms worse
than their own 120-sample runs on a fresh seed: seed variance dominates budget there too.) (ii)
Grid: refining the pmf grid from L=5000 to L=20000 at equal budget makes the local proposer
worse (0.3561): the limit was not resolution. (iii) Proposer: Claude Opus 5 under the identical
loop reaches 0.3897 within ∼100 samples (just above the repository’s published value, obtained
with 2025-era proposers; we read this as locating the wall, not as ranking systems across model
generations) and plateaus there for 17 generations. (iv) Verifier time: tripling the sandbox
budget to 60 seconds, so heavier optimizers can run, moves the plateau by +0.0002.
    The constructions are legible. The local model’s best is a bimodal sparse measure of 16 atoms
(half the mass on {0, 1, 2, 3}, geometrically spaced atoms at the top), with the strategy stated in
comments. Claude’s best implements an exact sparse-atom objective with an analytic gradient


                                                   5
Figure 2: The completed 23 at a glance (cell means over nine problems, two replicates). Memory-on cells
(blue) hold the four best gap fractions; D-on cells (circles) hold the highest construction-hash diversity;
the two axes barely interact (βM ×R ≈ 0). Collapse counts in parentheses: memory+repulsion is the only
arm that never collapses; agenda+repulsion collapses most.


and a multiplicative-weights refinement. The frontier proposer and AlphaEvolve’s published
value sit within 0.0007 of each other; the local model stalls about 0.008 behind them. All three
lie at 92–98% of the seed-to-reference gap toward a reference whose construction evidently lies
outside the sparse-atom family every language model proposes. More precisely: the candidates
of both proposers are small finitely supported measures found numerically, while the Bellec
and Fritz [1] construction is a multiscale, recursively structured sequence of discrete measures
whose analysis shows a finitely supported measure cannot be optimal; the family-hint conditions
below name that structure. Within the settings tested, grid and time changes did not move the
result and a stronger proposer moved it without closing the gap; these plateaus motivated the
hypothesis that what remained was the construction family, an idea. The family-hint experiment
below tests and qualifies that interpretation.
    A second problem sharpens where such ideas live. On max–min distance 16, the frontier
proposer under the same loop emits in generation zero, before any search feedback, a minimax
program (SLSQP on min t s.t. d2ij ≤ t, d2ij ≥ 1, analytic Jacobians) whose value lies marginally
below the repository’s published one; every valid sample across the run converges to the same
value. The loop verified this construction; it did not discover it. We treat the datum as scope,
not as a record claim: the operators structure search and protect its tails, but they do not
inject construction knowledge the proposer lacks. The pre-registered scoping runs make the
same point from the other side, on all three registered problems. On beat-the-average, the bare,
memory-only and repulsion-only arms land within 0.001 of one another (0.3871, 0.3866, 0.3876;
single runs, estimation only) and within 0.003 of the composed arm’s 0.3897. On max–min
distance and on the Heilbronn problem every arm converges to an identical value (12.889230
and 0.036530 respectively; the Heilbronn reference in our registry floors the reported figure, so
that value reaches the frozen reference and supports no exceedance claim). At frontier strength
the single-run operator differences are at most 0.001–0.003 everywhere we measured them: the
nominal gains are a local-proposer phenomenon, and whether the collapse insurance survives
at this strength remains untested (single runs; the frontier proposer’s own run-to-run noise is
unestimated).




                                                    6
Figure 3: Beat-the-average under the same loop (arm E): fraction of the seed-to-record gap closed per
verified sample. The local 30B at two grid resolutions; Claude Opus 5; dotted lines mark AlphaEvolve’s
reported value (0.3890) and the best known (0.400695, Bellec–Fritz).

                 condition               seed 11   seed 12   seed 13   mean     finals in-family
                 no hint                 0.3496    0.3607    0.3463    0.3522         0/3
                 generic hint            0.3512    0.3381    0.3086    0.3326         0/3
                 structural hint         0.3284    0.3383    0.3140    0.3269         3/3
                 crude in-family seed    0.3554    0.3679    0.3520    0.3584         2/3
                 strong in-family seed   0.3762    0.3739    0.3743    0.3748         3/3

Table 2: Family-hint test: final best per seed. In-family membership by the preregistered family-signature
classifier (at most 50 support atoms, mass ≥ 0.3 on {0..3}, atoms in ≥ 3 log10 distance-from-top bands;
the structural hint instructs exactly this structure, so the classifier is partly a manipulation check of
instruction-following). With three seeds per condition every contrast is descriptive (the smallest one-sided
sign-flip p at n=3 is 0.125).


6    The family-hint test: verbal specification versus executable
     seed
The registered family-hint experiment (five conditions × three seeds, 120 samples each, mem-
ory+repulsion arm, beat-the-average) asks what it takes to move the search into the Bellec and
Fritz [1] family: (a) no hint; (b) a generic hint; (c) a structural hint naming the family without
parameters; (d) a crude in-family seed program (initial score 0.2734); (e) a strong in-family seed,
our best tested finite-grid instantiation of the family (0.3742; on this grid with strict inequality,
notably below the 0.3816 sparse-atom plateau, a fact measured and registered before launch —
the condition supplies an author-implemented finite approximation, not the theoretical multiscale
construction itself).
    The answer came with a twist (Table 2). The structural hint worked as an instruction
and lost as a search: its final constructions carry the family signature, so the model obeyed,
entered a family that is inferior at this grid, and paid about 0.025 for it. Handed the family as
code, the loop optimizes it (+0.085 from the crude seed, above the no-hint endpoint in three of
three seeds) and stays loyal to it (no strong-seed run deserted to the better sparse family). No
unaided candidate in the three registered 120-sample runs matched the family signature. Two


                                                       7
caveats bound the reading: the historical 0.3816 comes from a different battery under strong
seed variance, so the strong seed’s 0.375 exceeds the contemporary no-hint 0.352 descriptively
while trailing the historical best; and the seed conditions enter with different initial scores, so
final values mix family advantage with starting-point advantage (matched-score sparse seeds
and paraphrased or deliberately wrong hints are the registered next controls). Within those
bounds the registered hypothesis was not supported: handing the idea, in words or in this finite
encoding, did not cross the last mile under this budget — our tested finite-grid encoding of the
idea was not sufficient to close the gap, which leaves open whether the theoretical family, a
richer encoding, or a larger budget would. What the experiment does establish is a division of
labour: under these runs the loop transported and optimized the idea it was handed and did
not produce its signature unaided, and instructing a construction is not inducing a competitive
implementation of it, the third appearance of that pattern in this program (the continuity
connective of the companion study; the frontier scoping runs; now the structural hint).


7    Discussion
What office scale buys. With 120–600 verified samples, a local model and one laptop: a
median 0.71 of the seed-to-reference gap closed by the composed arm across nine problems
(per-problem 0.10–0.99), legible programs, and, with a frontier proposer at ∼US$50 of API,
parity with the values the large systems report on this problem. The published record-movers
used frontier ensembles with thousands of samples [10], millions with small models [13], or
open-source loops with strong API models [6]; the band we measure (local proposer, hundreds of
samples, controlled operators) was unoccupied, and it is the band most laboratories can afford.

The operator ledger. E had the highest mean and one collapse; memory+repulsion was
the only zero-collapse arm, at a mean within 0.025 of E’s and without the agenda’s extra
call, so the parsimonious operational recipe these data support is memory+repulsion, with
the full composition as the highest-mean variant. The mechanism is visible in the notebooks:
the notebook package carries lineage information across generations and the duplicate control
spends the budget on genuinely different constructions. Alone, each fails somewhere: memory
and agenda are inert on problems the model already saturates; repulsion is associated with
performance collapses on fragile manifolds. This is a recurring collapse-prevention pattern,
consistent with the anchoring hypothesis, that this program has now observed across narrative
generation, weight-space preference optimization, and prompt-space search.

The proposer comparison and the plateau. On this one problem, the frontier proposer is
far more efficient in verifier evaluations (+0.008 absolute over the local model’s 600-sample best,
reached with roughly 20× fewer verified samples), and everything we tried after it moved little
(grid, time, more samples: +0.0002). This is a sample-efficiency comparison on one problem under
one harness, not yet a proposer-strength curve; replications on further problems are planned, and
reasoning effort, ensembles, alternative representations and thousand-sample budgets all remain
untested explanations. The shared plateau suggests, consistently with our consolidation results
[12], that search over a fixed prior rapidly collects what the prior’s construction families contain
and then stalls at the best family member, a hypothesis to test rather than assert. Section 6
put that hypothesis to a registered test; the short answer is that a verbal specification of the
reference family was followed and lost, while an executable in-family seed was optimized, and
no unaided run produced the family signature. This is the question Georgiev et al. [3] report
answering with an expert in the loop, from the other side.




                                                 8
Design rules. For verified search at small scale: pair memory with repulsion (the zero-collapse
arm; the full composition adds +0.025 of mean at the cost of the agenda’s extra calls, a difference
our data cannot distinguish from zero), and never run repulsion alone on fragile manifolds; keep
the behaviour descriptor construction-derived (a rounded construction hash, not an embedding;
no symmetry canonicalization); spend on the proposer before spending on samples; treat plateaus
as candidate family boundaries and test them (grid, time, proposer and hints in pre-registered
steps) rather than declaring them.


8    Experimental provenance
Every battery was registered before running; the combined analyses are sequential, and the table
makes the order of looks explicit.

 battery            registered   data already seen       primary                status
 F (5×6×2)          2026-08-22   none                    E>A frac               p = 0.0625 (floor)
 F-ext ladder       2026-08-23   F                       budget/grid/proposer   descriptive
 F-ext2 (n=9)       2026-08-24   F, ladder               E>A frac               p = 0.023 combined
 23 completion      2026-08-24   F, ext2 partial         M×R > 0                rejected (p = 0.47)
 Frontier scoping   2026-08-26   all above               estimation only        operators ≈ null
 Family hint        2026-08-27   all above               optimize-once-given    yes as code, no as words

Table 3: Order of registrations and looks. The nine-problem primary analysis is a two-look sequence
(discovery + prospective extension), not an independent confirmation.



9    Limitations
Nine problems is still a small universe of construction families; the full 23 isolates interactions, but
at n=9 no per-term effect survives correction, so the operator decomposition (memory largest)
is directional, not statistically resolved, and the collapse asymmetry is descriptive; budgets
are equalized in proposals and verifier evaluations (120 of each per run; duplicate rejection
in the repulsion arms happens after verification, since the signature requires the construction,
and discards 20–30 verified candidates per run from the islands); the operators’ extra calls are
measured at one per island-generation per operator (∼220 characters per call, an overhead
of 1–3% of proposer output characters; input-token accounting is incomplete, so budgets are
matched in proposals and verifications, not demonstrably in tokens), and the arms differ in
candidates surviving dedup into the islands (per run: A 108, B 95, C 93, D 72, BC 94, BD 65,
CD 73, E 63), so sample efficiency here means verifier-evaluation efficiency; the diversity metric
is related to the repulsion operator’s own filter; the behaviour signature is a hash of the returned
construction after rounding, with no canonicalization for symmetries (permutation, rotation,
reflection), so div can count symmetric variants as distinct, its rounding sensitivity is untested,
and the D filter and the div metric share this signature (a retrospective AST-structure metric,
invariant to renaming and independent of that signature, is directionally consistent on the runs
with logged code: D-on arms 0.67–0.87 distinct structures per valid candidate against 0.38–0.39
for A and B on the matched problems; paired D−A +0.27 at the n=3 resolution floor); the six
problems satisfy criteria fixed before any runs (cheap exact verifier, short-function candidates,
known headroom; the universe of 68 candidate problems and per-problem ratings are in the
released reconnaissance table) but were not sampled randomly, so the exact tests quantify sign
consistency within this selected suite and do not license random-sample generalization to the
repository or to construction problems generally; because the problems and their literature are
public, proposer performance does not distinguish retrieval of pretrained construction knowledge

                                                     9
from de novo discovery (the generation-zero minimax program is the extreme case); frac is
floored at the seed by construction, signs are harmonized for minimization, and reference values
are frozen at the repository commit recorded in the release; the scaling ladder is one domain;
the API proposer is not bitwise reproducible and its reasoning effort was fixed low; comparisons
against repository values compare a 2026 proposer with values obtained by 2025-era systems, so
they locate our wall and never rank systems: no system-level head-to-head with ShinkaEvolve
or AlphaEvolve is attempted, and the operators should be read as structuring search, not as a
substitute for construction knowledge the proposer lacks.


10     Conclusion
Inside a fixed verified-search loop at office scale, the operator packages our generation studies
isolated (a schematic notebook, a named obstacle, behavioural duplicate control) compose into
the arm with the highest mean, E, at one collapse in eighteen runs; memory+repulsion was
the only zero-collapse configuration, within 0.025 of E’s mean, and is the parsimonious recipe
these data support. Repulsion alone enforces behavioural non-duplication by construction and
was the best single package exactly where the valid manifold is wide; and on the one problem
where we compared them, a frontier proposer reached a higher value with roughly 20× fewer
verifier evaluations. On beat-the-average both proposers stalled inside one small finite-support
construction family, below a multiscale reference; the other plateaus are consistent with, but
do not establish, analogous family boundaries. Whether crossing that boundary requires what
we have informally called an idea was put to a registered test on the flagship problem: the
idea, handed in words, was followed and lost; handed as code, it was optimized, but our best
tested finite-grid instantiation remained below the plateau the models reach unaided. Under
the three registered runs the loop moved the idea it was handed and produced no candidate
matching its signature unaided; our finite encoding of the idea was not sufficient to close the gap
here. Whether the last mile of these searches is an idea, the question this program has carried
informally, remains open, now with its first measured answer.


A     Reproducibility
Code, run data, the dated laboratory notebook with every pre-registration and amendment, and
the analyses that generate every table are in the repository of the program (https://github.com/
RobertoOno/interrupting-the-loop): the search harness (scripts/frontier_search.py),
the problem verifiers (src/creative_machine/domains/), the batteries (run_f*.sh, run_hint.sh),
the analyses (frontier_analysis.py, analysis_23.py) and the generated appendices (docs/APPENDIX_F*.md,
APPENDIX_HINT.md). Every candidate of every reported run is logged in the released run data.
Proposing used Qwen3-Coder-30B-A3B-Instruct (8-bit, MLX) locally and anthropic.claude-opus-5
on Amazon Bedrock for the frontier comparison; every hypothesis, amendment and result is
dated in docs/PLANO.md.


References
 [1] Pierre C. Bellec and Tobias Fritz. Optimizing over iid distributions and the beat the average
     game, 2024. v5, 2025.

 [2] Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré,
     and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated
     sampling, 2024.



                                                10
 [3] Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner. Mathe-
     matical exploration and discovery at scale, 2025.

 [4] Can Gurkan, Forrest Stonedahl, and Uri Wilensky. Mutation without variation: Convergence
     dynamics in LLM-driven program evolution. In GECCO Companion (Workshop on LLMs
     for/with Evolutionary Computation), 2026. arXiv:2606.05408.

 [5] Fatemeh Haji, Javier Delarosa Quiros, and Peyman Najafirad. Memory-guided tree search
     with cross-branch knowledge transfer for llm solver synthesis, 2026.

 [6] Robert Tjarko Lange, Yuki Imajuku, and Edoardo Cetin. Shinkaevolve: Towards open-ended
     and sample-efficient program evolution, 2025.

 [7] Joel Lehman and Kenneth O. Stanley. Abandoning objectives: Evolution through the
     search for novelty alone. Evolutionary Computation, 19(2):189–223, 2011.

 [8] Aofan Liu, Shiyuan Song, and Yiyan Qi. ε-memevo: Adaptive cross-task memory transfer
     for llm program evolution, 2026.

 [9] Jean-Baptiste Mouret and Jeff Clune. Illuminating search spaces by mapping elites, 2015.

[10] Alexander Novikov et al. Alphaevolve: A coding agent for scientific and algorithmic
     discovery, 2025. Google DeepMind; arXiv:2506.13131.

[11] Roberto I. Ono Filho. Interrupting the loop: Periodic subject changes raise judged surprise
     and connection in base language models. arXiv:2608.19893 [cs.CL], 2026.

[12] Roberto I. Ono Filho. Moving the mean toward the known good, not beyond it: What
     inference-time interventions and weight consolidation buy in open-ended generation.
     Manuscript, under revision; to appear on arXiv, 2026.

[13] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
     M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming
     Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries
     from program search with large language models. Nature, 625(7995):468–475, 2024. doi:
     10.1038/s41586-023-06924-6.

[14] Viktor Volkov, Valentin Khrulkov, Andrey V. Galichin, Danil Sivtsov, Nikita Glazkov, Olga
     Volkova, Konstantin Pchelin, Iaroslav Bespalov, Dmitry V. Dylov, Petr Anokhin, and Ivan
     Oseledets. Evomem: Memory-augmented evolution for code optimization, 2026.

[15] Chunhui Wan et al. Loongflow: Directed evolutionary search via a cognitive plan-execute-
     summarize paradigm, 2025.

[16] Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo Hua, Haeyeon Kim,
     Jinkyoo Park, and Guojie Song. Reevo: Large language models as hyper-heuristics
     with reflective evolution. In Advances in Neural Information Processing Systems, 2024.
     arXiv:2402.01145.

[17] Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Yang Yue, Shiji Song, and
     Gao Huang. Does reinforcement learning really incentivize reasoning capacity in LLMs
     beyond the base model? In Advances in Neural Information Processing Systems, 2025.
     arXiv:2504.13837.




                                              11
