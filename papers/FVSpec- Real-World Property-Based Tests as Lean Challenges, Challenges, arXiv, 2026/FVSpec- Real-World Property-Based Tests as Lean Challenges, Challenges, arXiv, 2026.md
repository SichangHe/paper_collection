                                             FVSpec: Real-World Property-Based Tests as Lean
                                                              Challenges


                                                Quinn Dougherty∗, Max von Hippel†, Simon Henniger‡, Hazel Shackleton§, Mike Dodds§



                                                                                                Abstract
arXiv:2606.01008v4 [cs.SE] 14 Sep 2026




                                                     As AI systems generate an ever-growing share of the world’s code, formal verifica-
                                                     tion offers a principled way to ensure that code is correct, and AI itself may be able
                                                     to shoulder much of the verification burden. Yet we lack a clear picture of how well
                                                     today’s models and agents perform on verification tasks drawn from real-world
                                                     software, since existing benchmarks rely largely on curated or synthetic problems,
                                                     or focus on math rather than program verification. To close this gap, we present
                                                     a benchmark for evaluating AI on real-world formal software verification tasks.
                                                     We first scrape 7,413 distinct property-based tests (PBTs) from real-world Python
                                                     repositories, then automatically translate 2,623 of them (35%) into 9,415 Lean 4
                                                     specifications with sorry placeholders (≈3.5 formalizations/PBT). Translating
                                                     PBTs to Lean specs is challenging: it requires modeling Python in Lean, inferring
                                                     the property encoded in a PBT, and handling side effects. We describe an agentic
                                                     pipeline for transpiling PBTs into Lean, evaluate coverage and quality metrics, and
                                                     provide baselines for proof generation using several approaches. All code (scraper
                                                     and agents) and data (PBTs and Lean specs) are open source.


                                         1     Introduction
                                         Several AI safety proposals are premised on implementing safeguards by way of formal verification
                                         (FV)1 – that is, software systems that can produce and certify proofs [Dalrymple and Ammann, 2025,
                                         Dalrymple et al., 2024, von Hippel, 2026, Miyazono, 2024]. Software verification is therefore a
                                         key goal for AI safety, yet, currently, there is little evidence that AI can automate verification. To
                                         achieve this, we would first need high-quality benchmarks on which to train. Existing benchmarks
                                         are too small (e.g. Loughridge et al. [2024], Ravi and Coblenz [2025]), focused on math rather than
                                         software verification (e.g. Glazer et al. [2024]), or derived from expert-driven verification projects
                                         (as in Chakraborty et al. [2025]) that do not reflect the tasks involved in a typical software project:
                                         bootstrapping verification in real-world software is much more challenging than verifying software
                                         which was built to be verified from day one. For instance, the former, unlike the latter, often requires
                                         reasoning about black-box external systems and the interactions of several different components,
                                         potentially in different languages and architectures [Buro et al., 2020, Perconti and Ahmed, 2014].
                                         To reflect the needs of real-world verification, we propose a new benchmark, FVSpec, where we derive
                                         verification challenges from publicly available property-based tests (PBTs). PBT is a “close sibling”
                                         to FV which has seen significant adoption, sometimes called “lightweight formal methods” [Jackson
                                         and Wing, 1996]. In both FV and PBT, engineers write specifications: logical properties that the
                                         software must obey. For example, we might require that a Python function isort(lst) always
                                         returns a sorted permutation of its input lst. The difference lies in how this property is checked. In
                                             ∗ Forall R&D, work completed at Galois Inc, correspondence to quinn@for-all.dev
                                             † Some work completed at Benchify
                                             ‡ Harvard University
                                             § Galois Inc
                                             1 FV forms a subset of formal methods, which also include PBT, model checking, and abstract interpretation.




                                         In submission.
                                                                                                FVSpec:PBT


                                  Discovery          License filter          Extract         7,413 PBTs
                 GitHub
                                 18,494 repos       copyleft → drop    @given via ripgrep     497 repos




                                                                                                FVSpec:FV

                                                     Agentic tran-
                              Function discovery                        Post-production     9,415 samples
                                                      spilation
                                   tree-sitter                           merge / validate    2,623 PBTs
                                                    LSP repair loop




Figure 1: The full FVSpec generation pipeline (FVC = FV challenge). Top (FVSpec:PBT): the input
PBT corpus is scraped from public repos. Bottom (FVSpec:FV): each PBT is lifted to a Lean (Impl,
Spec) pair via tree-sitter–based function discovery, an agentic transpilation step (with LSP-repair),
and a post-production step that validates, deduplicates, and grades the output; 7,413 PBTs enter and
9,415 FVCs (from 2,623 distinct PBTs) emerge.

FV, the property is proved using mathematical techniques, resulting in almost-perfect confidence, but
requiring proof engineering by highly expert teams [Dodds, 2022] (or perhaps, in the future, agents).
In PBT, tests are randomly generated based on general rules that look like theorems.
First, we scrape 7,413 distinct PBTs written in Python’s Hypothesis framework [MacIver et al., 2019],
creating FVSpec:PBT. Each PBT can be seen as a conjecture about a piece of code, which the author
would like to prove or disprove. We translate code and PBTs to the prover Lean, which is becoming
the de-facto standard in AI verification. In the process of translation, each PBT becomes a conjecture.
We refer to our resultant corpus of conjectures and code as FVSpec:FV. Once the Lean version of the
conjecture is proven, it becomes a theorem. A similar approach was previously used by Dougherty
and Mehta [2025] on FVAPPS. In FVAPPS, source programs were taken from the APPS benchmark
[Hendrycks et al., 2021], then specs were inferred by an LLM and translated to Hypothesis PBTs,
and then lifted to theorems. We apply the same process to PBTs found in the wild.
Our main contributions are:
1. FVSpec:PBT — 7,413 deduplicated Python PBTs scraped from 497 open-source repositories,
   the first large PBT dataset drawn from ordinary software development2 .
2. FVSpec:FV — 9,415 Lean 4 FV challenge samples lifted from 2,623 of those PBTs by an agentic
   transpilation pipeline, with detailed metadata (8 FV challenges per PBT on average).
3. Baseline evaluations of Claude Sonnet 4.6, Claude Opus 4.7, and GPT 5.4 showing mean 70%
   success on easies and mean 49% on hards.
4. Open-source release of the full pipeline3 and datasets under MIT/Apache dual license.


2     Task Definition
Each problem consists of four components: (1) the original Python function under test and (2) PBT
testing it, (3) a Lean implementation of the same function, and (4) a Lean theorem corresponding
to the PBT, with a sorry placeholder where the proof should go. The AI’s task is to fill in every
sorry with a Lean proof (or a disproof) that compiles cleanly under lake build; submissions are
then scored by whether the proof retains any sorry or special-purpose axioms. Each problem also
includes a URL pointing to the original code and license information. As a running example, consider
isort(lst), illustrated in Figure 2. We encounter two issues when translating PBTs into Lean.

Nonsensical theorems pre-validation. Our pipeline can emit well-formed but useless statements
in the following three ways.
(i) Trivial Unit-typed conjectures. When the agent cannot recover a function’s return type, it falls
back on Unit. The resulting theorem is a tautology—e.g. theorem isort_check : isort lst
    2 Released on HuggingFace in January 2026, before the Hypothesis Corpus DeVoe [2026]; see Appendix B.
    3 (consisting of scraper, dependency extractor, agent, and post-production scripts)




                                                                  2
                                                                          FVSpec:FV

                          FVSpec:PBT                    Lean: Impl.lean
                                                            namespace Fvspec.Impl
                Python: implementation of isort             def insert (x : Int) : List Int → List Int
                   from bisect import insort                  | []      ⇒ [x]
                                                              | y :: ys ⇒ if x <= y then x :: y :: ys
                   def isort(lst):                                         else y :: insert x ys
                       out = []
                       for x in lst: insort(out, x)         def isort : List Int → List Int
                       return out                             | []      ⇒ []
                                                              | x :: xs ⇒ insert x (isort xs)

                                                            end Fvspec.Impl



                Python: Hypothesis PBT
                   from collections import Counter      Lean: Spec.lean
                   from hypothesis import given
                                                            import Fvspec.Impl
                   import hypothesis.strategies as st
                                                            open Fvspec.Impl
                   @given(st.lists(st.integers()))
                   def test_isort(lst):
                                                            theorem isort_sorted (l : List Int) :
                       out = isort(lst)
                                                              (isort l).Sorted LE.le := sorry
                       pairs = zip(out, out[1:])
                       assert all(a <= b for a, b in
                                                            theorem isort_perm (l : List Int) :
                        pairs)
                                                              (isort l).Perm l := sorry
                       assert Counter(out) ==
                        Counter(lst)




Figure 2: Each problem is partitioned into the PBT corpus (FVSpec:PBT, left)—the original Python
implementation and PBT we scrape from GitHub—and the formal-verification challenge (FVSpec:FV,
right) we transpile from it: a complete Lean re-implementation and theorem statement generalizing
the PBT. The AI must discharge both Lean sorry placeholders, one per theorem (or negations).


= () := by plausible, which holds for any total function into Unit and so carries no value. The
Unit is on the function under test in Impl.lean, and the conjecture is trivial as a result.
(ii) Ill-typed or unresolved-symbol theorems. The agent works from the Python source and writes Lean
by analogy. When it invents a Lean name that does not exist—e.g., writing theorem isort_perm
(l : List Int) : (isort l).permutationOf l := sorry, where permutationOf is
not a member of List4 —or attaches a type signature inconsistent with the surrounding code, the
Lean elaborator rejects the file with errors like unknown identifier, type mismatch, etc.
(iii) Spec theorems leaking into Impl.lean. Our first run used separate agents for Impl.lean
(definitions) and Spec.lean (theorems). The implementation agent is explicitly instructed
to emit no theorems, but occasionally it pre-empts the spec agent by inserting a namespace
Fvspec.Spec. . . theorem isort_sorted. . . end Fvspec.Spec block inside Impl.lean, which
violates our file split and would silently expand the proof obligation if left in.
We catch (i) by regex, drop (ii) at compile time, and strip (iii) with a namespace-aware filter that
removes namespace Fvspec.Spec blocks found in Impl.lean. A small residual (0.7% of samples)
carries naked theorem declarations in Impl.lean written outside any namespace; because grading
targets only Spec.lean, these do not expand the proof obligation, but they represent stray proof
activity that escaped the filter. A theorem that survives all three filters is a reasonable challenge
problem even if it has drifted from the original PBT.

Lean as a (nearly) perfect oracle. The Lean kernel arbitrates correctness, which is qualitatively
stronger than statistical sampling. But it is not adversarially perfect: an AI can satisfy the kernel
by changing the question—adding an axiom, weakening hypotheses, or exploiting a vulnerability
in Lean [Gopinathan, 2026, von Hippel and Dougherty, 2026]. To make gaming visible, every
submission is scored on two axes: a binary proved flag (the file compiles under lake build and
every original sorry has been discharged) and partial credit (fraction of original sorrys discharged).
We additionally record any axiom dependencies the proof introduces, since an AI can trivialize a goal
by quietly importing strong axioms; we do not currently auto-fail on extra axioms, but report them
so reviewers can flag suspicious solutions. Submissions can additionally be re-checked through the
independent leanprover/comparator Lean FRO [2026] kernel.

  4 (the correct name is List.Perm)




                                                        3
3     Methods
We had to solve two problems: first, how to scrape real-world PBTs, and seecond, how to convert
PBTs into FV challenges at scale.

3.1     Scraping the PBT Corpus

We scrape real-world PBTs from public GitHub repositories. To identify which repos are interesting
to us, we consider dependencies: if a package depends on Hypothesis MacIver et al. [2019], a
widely-used PBT library, it is of interest. Our scraper operates in three stages. (1) Discovery. We
crawl the Hypothesis dependency graph using PyGitHub Jacques et al. [2026]. (2) Licensing. We
skip repos with an explicitly non-permissive license (e.g. AGPL, GPL, LGPL, MPL), and record the
license string—including “unknown” for repositories with no detectable license—alongside the rest
of each repository’s metadata. Our thinking here is to avoid software that is licensed in a way that
would preempt using our benchmark in nonacademic environments. (3) Extraction. We shallow-clone
each accepted repository, locate PBTs via ripgrep, and parse the surrounding Python to recover the
transitive closure of locally-defined functions called therein. A 24-hour run produced 54,345 PBTs.

3.1.1    Deduplication
Most of those 54,345 PBTs are copies. Our first pass deduplicated by repository: we grouped
repos by the base name of their URL5 , kept the most-starred repo in each group, and dropped tests
from the others whose whitespace-normalized SHA-256 appeared in the kept one. That left 28,073
PBTs across 718 repositories, but only 8,314 distinct tests. Most of the non-distinct PBTs came
from PyTorch, whose Hypothesis suite appears, whole or in part, in at least 42 repositories holding
39,386 of the 54,345 PBTs. Only 24 of them are named pytorch; the rest have unrelated names
such as amd/ZenDNN-pytorch or fathnd/homomorphic. The copies come from different PyTorch
versions and carry 33 different sets of PBTs, with no PBT appearing in all 42. Other projects are
copied too: without the PyTorch copies, the remaining 14,959 PBTs contain only 6,567 distinct
PBTs. We therefore deduplicate on the PBT alone, keying on a SHA-256 of the PBT with comments
and blank lines removed and whitespace collapsed, and keep one canonical copy per key, chosen by
stars, then forks, then row id. The resulting corpus has 8,314 PBTs from 538 repos owned by 466
GitHub users, spanning 476 project names. The public release of FVSpec:PBT contains the 21,746
name-deduplicated PBTs whose dependencies we could re-extract from a fresh clone, covering 7,413
of the distinct tests, and we release code for the PBT-deduplication.

3.1.2    Diversity
A perennial concern with scraped benchmarks is concentration: SWE-bench Jimenez et al. [2024],
for instance, draws all 2,294 of its tasks from just 12 repositories, with django supplying 37% and
the top three (django, sympy, scikit-learn) supplying 64%. Our released corpus is far more
spread out—it draws from 497 repositories, no single one of which contributes more than 11.5% of
the PBTs and whose top ten together contribute 30.8%—and most of those repositories are unstarred
personal projects rather than curated showcase code. The median PBT is just 10 LoC, but exercises
around 2.8× its own length in project code.
To illustrate the diversity of our dataset, consider the result of drawing ten repositories from it
uniformly at random:6 flytekit (workflow SDK), landlab (earth-surface modelling toolkit),
onnx-embedding (ONNX-backed embedding library), ch-backup (ClickHouse backup tool),
logot (log-output assertion library), mlstacks (MLOps infrastructure provisioner), whenever
(datetime library), anls_star_metric (document-QA evaluation metric), jsondiff (JSON diffing
library), and sec-parser (SEC-filings parser). This is broadly representative of real-world software
engineering, as opposed to academic or competitive programming.
Figure 3 summarizes three code-quality metrics across the corpus. The source tests span a wide range
of complexity, from trivial single-assertion tests to multi-strategy tests exercising complex library
APIs—diversity inherited directly from real-world engineering practice and not curated for difficulty.
    5 (e.g., SunsetMkt/pytorch and njzjz/pytorch both reduce to pytorch)
    6 Reproduce with random.seed(13);     random.sample(sorted(r.name for r in repos if r.stars >= 10),
10) against the 497-repo deduplicated corpus; the star floor filters out personal forks.


                                                       4
                                                                 Source PBT size                                                           Python source complexity                                                                 Python source maintainability
                                 1200
                                                                                                                      2000                                                                                2000
                                 1000

                                  800                                                                                 1500                                                                                1500
Count




                                                                                                              Count




                                                                                                                                                                                           Count
                                  600
                                                                                                                      1000                                                                                1000
                                  400
                                                                                                                       500                                                                                 500
                                  200

                                       0                                                                                 0                                                                                   0
                                               0      20          40         60         80             100                    2          4      6       8        10      12     14                                       30        40      50     60       70    80       90       100
                                                        Lines of PBT code (clipped at 100)                                            Avg cyclomatic complexity (clipped at 15)                                                            Maintainability index


Figure 3: Python source characteristics. Code-quality metrics for the 7,413 deduplicated PBTs,
computed by Radon [Lacchia, 2026]. Left: lines of code. Center: cyclomatic complexity—the number
of linearly independent execution paths through the function, i.e. one plus the number of binary branch
points [McCabe, 1976]; higher values indicate more complex control flow. Right: maintainability
index—a 0–100 composite of Halstead volume [Halstead, 1977], cyclomatic complexity, and source
lines, where higher is more maintainable; the spike at 100 is an artefact of Radon capping the score.

                                                           PBT size vs. code under test                                               How much larger is the tested code?                                                         Direct local dependencies per PBT
                                 500                                                                                  140                                                  median=2.8×                                                                                         median=1
                                                                                                                                                                                                          1200

                                 400                                                                                  120
                                                                                                                                                                                                          1000
Total dep LOC (clipped at 500)




                                                                                                                      100




                                                                                                                                                                                         Number of PBTs
                                 300                                                                                                                                                                      800
                                                                                                                       80
                                                                                                              Count




                                                                                              PBT median=9
                                                                                              dep median=28
                                                                                                                                                                                                          600
                                 200                                                                                   60
                                                                                                                                                                                                          400
                                                                                                                       40
                                 100
                                                                                                                       20                                                                                 200
                                  0
                                                                                                                        0                                                                                   0
                                           0          20          40         60          80            100                   10
                                                                                                                                  1
                                                                                                                                               10
                                                                                                                                                 0
                                                                                                                                                              10
                                                                                                                                                                 1
                                                                                                                                                                              10
                                                                                                                                                                                   2                             0   1        2       3     4      5      6     7     8    9      10
                                                              PBT LOC (clipped at 100)                                                    Dep LOC / PBT LOC (log scale)                                                           Local dep functions called ( 10 grouped)



Figure 4: Three views of the relationship between PBT size and the size of the code being exercised,
over the n = 2,238 post-deduplication PBTs whose local dependencies were recoverable. (The
remaining 5,175 exercise only standard-library or external code, or had dependency extraction fail;
the figure is therefore a subset of the full 7,413-PBT corpus.) (a) Per-PBT scatter of PBT LoC against
the total LoC of the directly-called dependencies. (b) Histogram of the ratio between dependency
LoC and PBT LoC (log scale); the median PBT exercises code 2.8× its own length. (c) Histogram of
the number of direct local function calls per PBT.


3.2                                                Turning PBTs into Lean challenges

We lift each PBT in corpus (FVSpec:PBT) into a Lean (Impl.lean, Spec.lean) pair (Figure 1,
bottom) in three phases: function discovery, agentic transpilation, and post-production. We call the
resulting challenge corpus FVSpec:FV. The pipeline is modeled on FVAPPS [Dougherty and Mehta,
2025], except it starts from PBTs rather than programming puzzles, and adds LSP-repair.
Function discovery. For each PBT we use tree-sitter to extract the function under test and the transitive
closure of its local dependencies. Larger PBTs pull in tens to hundreds of lines of internal helpers.
When discovery fails—typically due to metaclasses, decorators, or other dynamic dispatch—we emit
a stub with generic type parameters so the formalization agent still receives well-formed input.
Agentic transpilation. A formalization agent translates each sample, producing both Impl.lean (a
computable port of the function under test and its dependencies, no sorry) and Spec.lean (one
theorem per Hypothesis assertion, with proofs left as sorry). After each generation step we type-
check the output via the Lean LSP and, on failure, feed the compiler output back to the agent. The
loop terminates on success or when a fixed budget runs out. The agents ran on claude-sonnet-4-5
in our first run (5,979 released samples), which used separate agents for the implementation and the
specification, and on claude-sonnet-4-6 in our second run (3,436 samples).
Post-processing. We first extract LLM turn counts from the raw .eval file archives produced by the
formalization agent, which runs as an Inspect AI [UK AI Security Institute, 2024] task. We then
collapse runs into a single JSONL, deduplicating by sample id and tie-breaking with a quality score


                                                                                                                                                     5
(structural faithfulness, theorem count, unit-tests, implementation success). Next, we re-run lake
build on each retained sample and drop failures, which we classify into nine families: timeouts, non-
wellfounded recursion, unknown identifiers, failures to synthesize, type mismatches, syntax errors,
missing functions, application errors, and declaration errors. We then run a custom AST analyzer
on the Lean artifacts to extract line counts, theorem and def counts, residual sorry and axioms.
Finally, conditioning on these metrics, we assign a binary easy/hard label using claude-haiku-4-5
as judge, together with a confidence score and a short rationale.7
Side effects. A particular design issue is how to handle side effect in code. PBTs in our corpus
come from messy real-world environments: production code routinely touches databases, sockets,
the filesystem, the wall clock, webhook queues, and so forth. The formalization agent handles this
by treating the effectful world as an uninterpreted interface. Parts of the source essential to the
property—the entities and operators it constrains—are translated into Lean structures and inductive
types. Parts that are pure plumbing—the database, the queue, the system clock—are introduced as
opaque axiom declarations and threaded through the theorem as parameters. The resulting theorem
holds over all interpretations of those axioms, which is exactly the contract the original PBT was
checking against the live environment.


4     Results

Our pipeline for the FVSpec:FV dataset yields 9,415 samples drawn from 2,772 distinct PBTs:
formalization succeeded for 2,623 of 7,413 distinct PBTs (35%; Figure 1, bottom right); a further
149 formalized PBTs are not traceable to the current public release. The mean sample carries 8
theorems (median 6, max 66) and median structural faithfulness 0.65 (Figure 5). A complete Lean
implementation was generated for 59% of samples; the remaining 41% ship against a stub Impl.lean,
so the theorem statement is well-typed but the body it constrains is opaque. The Claude Haiku grader
splits the dataset 62%/38% hard/easy. Where a PBT yields multiple compiling formalizations, all are
kept; the is_canonical field marks the highest-quality version per PBT.
The pipeline formalizes each of the 7,850 raw PBT records independently. Deduplicating those
records onto 2,772 unique PBTs by content (Section 3.1.1) collapses the PBTs but not their formal-
izations, leaving a mean of 3.4 formalizations per PBT (range 1–15). Among PBTs with multiple
formalizations, 32% have no single dominating attempt: for each formalization in the group there
exists another that scores higher on at least one sub-metric of our faithfulness metric. In practice,
this means for example, that the attempt with the best assertion coverage may have worse parameter
coverage than a sibling; keeping all formalizations and flagging the best one with is_canonical
therefore captures strictly more information than retaining only the top-scoring attempt.


4.1    Translation Quality

We evaluate translation quality using structural faithfulness. For this, we measure five sub-scores
(parameter coverage, type correspondence, strategy coverage, assertion coverage, and dependency
coverage) for both the original code and the translation, and we compute a weighted average of the
difference. Figure 5 shows the distribution of the overall score and the mean of each sub-score across
the dataset. The overall faithfulness distribution exhibits a clear mode above 0.5, indicating that
the majority of translations preserve the essential structure of the source PBT, though a long tail of
lower-quality translations remains.
In 59% of samples the agent generated a complete Lean implementation (Impl.lean contains a
computable definition); the remaining 41% use a signature-only placeholder. Structural faithfulness
is comparable across both groups (mean 0.67 vs. 0.68), confirming that specification quality is
largely independent of implementation recovery. The generated Lean artifacts span a wide range
of complexity (Figure 6): the median contains multiple theorems, and the sorry count tracks the
theorem count closely.


    7We confirmed judgment against real claude-sonnet-4-6 performance, and found approx. 70% correct predictions.




                                                         6
                           Structural faithfulness: overall                                              Faithfulness sub-scores (mean)
                                                                                                                                                                                      Difficulty: easy vs. hard                               Difficulty grader confidence distribution
                                                          median=0.65                                                                                                         6000     5869
        1750                                                                           Overall                                                 0.67                                                                               3500
        1500
                                                                          Dependency Coverage                                  0.48
                                                                                                                                                                              5000                                                3000
        1250                                                                                                                                                                  4000                                                2500
                                                                            Assertion Coverage                                                               0.97                                             3546
                                                                                                                                                                                                                                  2000




                                                                                                                                                                      Count




                                                                                                                                                                                                                          Count
Count
        1000                                                                                                                                                                  3000
                                                                             Strategy Coverage                                          0.61
                                                                                                                                                                                                                                  1500
         750
                                                                                                                                                                              2000
         500                                                               Type Correspondence                                                                 1.00                                                               1000
                                                                                                                                                                              1000                                                 500
         250                                                               Parameter Coverage                0.24

           0                                                                                                                                                                     0                                                   0
               0.2   0.3   0.4    0.5     0.6   0.7    0.8    0.9   1.0                          0.0   0.2           0.4              0.6             0.8    1.0                       hard                   easy                       0.70    0.75     0.80   0.85   0.90   0.95   1.00
                             Overall faithfulness score                                                               Mean score                                                                                                                          Grader confidence

                                                (a) Structural faithfulness                                                                                                                              (b) Difficulty grading
Figure 5: (a) Structural faithfulness: distribution of the composite score (left) and mean sub-scores
(right). (b) Difficulty grading: easy vs. hard counts (left) and grader confidence distribution (right).

                                                                    Lean output size                                                                    Theorems per sample                                             Sorry placeholders per sample
                                         600                                                                         1400
                                                                                                                                                                                                        800
                                         500                                                                         1200

                                         400                                                                         1000                                                                               600
                                                                                                                      800
                                 Count




                                                                                                             Count




                                                                                                                                                                                                Count
                                         300                                                                                                                                                            400
                                                                                                                      600
                                         200
                                                                                                                      400
                                                                                                                                                                                                        200
                                         100                                                                          200
                                           0                                                                               0                                                                              0
                                                0         100        200        300         400        500                        0                   5         10               15      20                     0          5             10          15          20
                                                                 Total Lean lines                                                               Theorems per sample                                                         sorry count per sample
                                                    (322 values >500 not shown; max=1,115)                                              (587 values >20 not shown; max=66)                                           (597 values >20 not shown; max=70)


Figure 6: Total lines (left), theorems per sample (center), and sorry placeholders per sample (right).


4.2                  Difficulty Grading

Figure 5 shows the results of our difficulty grading and the distribution of grader confidence. The
benchmark contains a substantial proportion of both easy and hard problems, and the grader expresses
high confidence for the majority of assessments. Difficulty is estimated here as a prediction, where
we ask the grader (haiku) to predict whether or not an agent would be able to complete the proofs.
Figure 7 examines the relationship between difficulty and two output characteristics: structural
faithfulness and Lean output size. Hard problems tend to produce longer Lean outputs, consistent
with the intuition that more complex source PBTs lead to more elaborate formalizations.

4.3                  Baselines

We evaluate three frontier models (Claude Sonnet 4.6, Opus 4.7, and GPT 5.4) on 100 randomly
sampled easy problems and 100 hard problems. Each model has access to the Lean LSP via MCP
tools and is scored on two metrics: a binary proved flag (zero sorry remaining and lake build
succeeds) and partial credit (fraction of sorry placeholders removed, clamped to [0, 1]). Figure 8
shows the models solved on average 49% of hard samples and 70% of easy ones.


5                Limitations

Specifications are translated rather than hand-written, so some may not faithfully represent the
original PBT. Our structural-faithfulness score is a heuristic: a high score does not guarantee semantic
equivalence, and a low score does not necessarily indicate a useless problem.
This especially goes for our axiomatization approach to side effects, which has some specific
limitations. If the property is fundamentally about timing, memory, ordering of side effects, or
wall-clock latency, an uninterpreted axiom cannot witness it. assert response_time < 100ms
cannot become a meaningful Lean theorem because the relevant semantics is precisely what the
axiomatization discards. Also, the agent identifies effectful boundaries via type signatures and call
patterns. When a function has a pure signature but performs side effects internally (e.g., a logger
called via a global, an lru_cache-style hidden state), the agent will inline it as if pure. The resulting
theorem may compile and even be true, but it is not guaranteed that its proof obligation always
corresponds to what the original’s code would have been.


                                                                                                                                                            7
                                                                                       Faithfulness by difficulty                                                                            Lean output size by difficulty
                                                                                                                                 hard                                  500                                                           hard
                                                                                                                                 easy                                                                                                easy
                                                       1000
                                                                                                                                                                       400
                                                        800
                                                                                                                                                                       300




                                               Count




                                                                                                                                              Count
                                                        600
                                                                                                                                                                       200
                                                        400

                                                        200                                                                                                            100

                                                          0                                                                                                              0
                                                              0.2         0.3     0.4     0.5     0.6    0.7     0.8      0.9     1.0                                        0         100         200        300         400         500
                                                                                         Overall faithfulness                                                                             Total Lean lines (clipped at 500)


                                  Figure 7: Overall faithfulness (left) and total Lean lines (right), stratified by difficulty.

                                                                                                    GPT-5.4 (k=5)                Opus 4.7 (k=5)                                       Sonnet 4.6 (k=5)
                           100                                                                                                                                         100




                                                                                                                                        Refusal rate (%) [per epoch]
Proved rate (%) [pass@k]




                            80    73%          70%
                                                                                                                                                                        80
                                        67%                                                             66%
                            60                                      59%                                          55%       57%                                          60
                                                                                43%      45%
                            40                                                                                                                                          40
                                                                                                                                                                                                                        25%
                            20                                                                                                                                          20                                                                        15%
                                                                                                                                                                                 4%      5%                      8%             5%          6%             4%
                                                                                                                                                                                                   3%
                             0                                                                                                                                           0
                                        Easy                                    Hard                            Overall                                                                 Easy                            Hard                     Overall


    Figure 8: Left: proved-ever rate by difficulty (best-of-k); right: baseline rate of the model giving up.


  Some formalizations are unfaithful in ways the score does not catch. Sample 30 (pbt_id 990),
  test_alert_collection_holds_unrelated_alerts from bjoern-reetz/cap-tools, has
  faithfulness 0.75 and is graded easy, and its theorem is true, but it misstates the property. AlertState
  is a dictionary keyed by each alert’s (sender, identifier, sent) reference, so ingesting an
  existing reference overwrites that entry, and UPDATE and CANCEL messages delete entries. The Lean
  version is an append-only list of contentless alerts, and the theorem says that folding ingest over
  a list returns that list. The agent saw neither the real AlertState, because dependency resolution
  found nothing for this test, nor the precondition that references never collide, which the test’s Hy-
  pothesis strategy enforces outside the test body. A faithful statement needs a keyed collection and an
  explicit Nodup hypothesis on the references. Dependency coverage, one component of the score, is
  1.0 whenever no dependencies are resolved, which is the case for 3,793 samples (40.3%).
    Our difficulty labels come from claude-haiku-4-5, itself a model whose judgments are imperfect
    and uncalibrated against human expert performance. We expose the grader’s confidence and rationale
    per sample so consumers can audit or override the labels.
   A complete Lean implementation is generated for 59% of samples; the remaining 41% ship against a
   stub, weakening the proof obligation: the theorem is well-typed but the body it constrains is opaque.
   These samples are tagged for easy filtering.
    Our scraper skips repositories with explicitly non-permissive licenses but accepts repositories where
    GitHub cannot detect a license at all.
  We do not measure human expert performance on FVSpec problems and therefore cannot calibrate
  the dataset’s difficulty against the proof effort required of skilled humans.

    6                            Related Work
    Our work extends FVAPPS [Dougherty and Mehta, 2025], which established AI-driven translation of
    coding problems into Lean. In FVAPPS, programs were taken from the APPS benchmark [Hendrycks
    et al., 2021], then specs were inferred and implemented as PBTs, then transpiled to Lean theorem
    statements. We apply the same process at scale to PBTs found in the wild, inferring specifications
    from natural language and source code. We enumerate related works below, and in Table 1.
   Lean verification benchmarks. A growing number of benchmarks target Lean. Lohn and Welleck
   [2024] provide 177 program specs translated from Tons of Inductive Programs, finding that current
   LLMs fail on medium and hard properties. Thakur et al. [2025] offer 161 curated problems sourced
   from HumanEval, testing end-to-end verified code generation. Wu et al. [2025b] cover all three


                                                                                                                                        8
foundational tasks—code generation, specification generation, and proof generation—across 189
manually curated coding tasks. Miranda et al. [2025] translate Python code with documentation
into Lean implementations, specifications, and unit tests (113 tasks). Bursuc et al. [2025] support
Lean, Rust/Verus, and Dafny, reporting success rates from 27% (Lean) to 82% (Dafny). Zeng
et al. [2026] use LeetCode transformations to evaluate verifiable agents on novel data without
contamination. These benchmarks are valuable but share a common limitation: their specifications
derive from synthetic coding problems or pedagogical exercises, not from properties written by
practicing engineers.
Other verification tool benchmarks. Loughridge et al. [2024] provide Dafny verification tasks. Beyer
[2025] provide the standard competition for software verifiers, with over 33,000 C tasks, but target
automated verification rather than interactive theorem proving8 . Wu et al. [2025a] focus specifically
on loop invariant synthesis. Chakraborty et al. [2025] explore neural synthesis for SMT-assisted
proof-oriented programming in F*.
Interactive theorem proving benchmarks. Hsiang et al. [2025] provide 122,517 theorems from
Mathlib4. Similarly, Thompson et al. [2024] collect 196,929 theorems from 2,226 GitHub Coq
repositories. These are primarily mathematical rather than software-oriented, and their theorems exist
in the training data of most frontier models.
Mathematics benchmarks. Glazer et al. [2024] evaluatet advanced mathematical reasoning. Although
FV and mathematics share proof infrastructure, the skills required differ substantially: software
verification demands modeling of program semantics, library APIs, and computational behavior,
rather than abstract mathematical reasoning.
FVSpec differs from each existing benchmark in at least one of the following three ways. First, our
specifications originate from real-world property-based tests written by practicing engineers, not
synthetic problems or pedagogical exercises. Second, the source PBTs were never formally verified,
so most theorems in our benchmark will not appear in any model’s training data. Third, we operate at
a larger scale than existing Lean verification benchmarks, with thousands rather than hundreds of
problems. Our work is motivated by the broader context of AI safety proposals premised on AI-driven
formal verification.


7     Conclusion

We present FVSpec, a benchmark of 9,415 Lean 4 formal verification challenges derived from
7,413 distinct real-world Python property-based tests scraped from 497 open-source repositories.
Unlike prior FV benchmarks—which draw from expert-written ITP code, competitive programming
problems, or curated verification exercises—FVSpec sources its specifications directly from practicing
engineers who had no formal verification intent, placing its problems genuinely out of distribution
relative to models’ training data. Our agentic formalization pipeline produced 9,415 challenges
from 2,623 of those PBTs (35%), with median structural faithfulness 0.65 and 62% of challenges
classified as hard by a difficulty predictor. Baseline evaluations of three frontier models confirm
that the benchmark is far from saturated, particularly on hard problems, leaving substantial room
for progress on AI-assisted formal verification of ordinary software. Our approach, which we have
described in depth, could easily be extended to PBTs from other languages (Haskell/QuickCheck,
C++/RapidCheck, TypeScript/fast-check) and other ITPs (Coq, Isabelle, F⋆ , Verus). Other potential
future work includes merging with the HC-2026 corpus to add runtime context, and using disproved
properties as seeds for program-repair challenges—bugs the original developer’s test harness missed,
now made precise in Lean.


References
Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad. Proofnet: Autofor-
   malizing and formally proving undergraduate-level mathematics. arXiv preprint arXiv:2302.12433,
   2023.

    8 These are completely different kinds of FV.




                                                    9
K. Bansal, S. Loos, M. Rabe, C. Szegedy, and S. Wilcox. Holist: An environment for machine
  learning of higher order logic theorem proving. In International conference on machine learning,
  pages 454–463. PMLR, 2019.

S. Barkallah, S. Daruru, B. Miranda, L. Aniva, A. Nie, and S. Koyejo. VeriBench-FTP: A formal
   theorem proving benchmark in Lean 4 for code verification. In The 5th Workshop on Mathematical
   Reasoning and AI at NeurIPS 2025, 2025.

D. Beyer. State of the art in software verification and witness validation: SV-COMP 2025. In
  Proceedings of the 31st International Conference on Tools and Algorithms for the Construction
  and Analysis of Systems (TACAS), 2025.

S. Buro, R. Crole, and I. Mastroeni. Equational logic and categorical semantics for multi-languages.
   Electronic Notes in Theoretical Computer Science, 352:79–103, 2020.

S. Bursuc, T. Ehrenborg, S. Lin, L. Astefanoaei, I. E. Chiosa, J. Kukovec, A. Singh, O. Butterley,
   A. Bizid, Q. Dougherty, et al. A benchmark for vericoding: formally verified program synthesis.
   arXiv preprint arXiv:2509.22908, 2025.

S. Chakraborty, G. Ebner, S. Bhat, S. Fakhoury, S. Fatima, S. Lahiri, and N. Swamy. Towards neural
   synthesis for SMT-assisted proof-oriented programming. In Proceedings of the 47th International
   Conference on Software Engineering (ICSE), 2025.

D. Dalrymple and N. Ammann. Safeguarded ai. https://aria.org.uk/opportunity-spaces/
  mathematics-for-safe-ai/safeguarded-ai/, 2025. Accessed 25 April 2026.

D. Dalrymple, J. Skalse, Y. Bengio, S. Russell, M. Tegmark, S. Seshia, S. Omohundro, C. Szegedy,
  B. Goldhaber, N. Ammann, A. Abate, J. Halpern, C. Barrett, D. Zhao, T. Zhi-Xuan, J. Wing, and
  J. Tenenbaum. Towards guaranteed safe AI: A framework for ensuring robust and reliable AI
  systems. arXiv preprint arXiv:2405.06624, 2024.

L.     DeVoe.     The Hypothesis corpus.          https://hypothesis.works/articles/
     hypothesis-corpus/, 2026. Accessed April 2026.

M. Dodds. Formally verifying industry cryptography. IEEE Security & Privacy, 20(3):65–70, 2022.
 doi: 10.1109/MSEC.2022.3153035.

Q. Dougherty and R. Mehta. Proving the coding interview: A benchmark for formally verified code
  generation. In Proceedings of the LLM4Code Workshop at the 47th International Conference on
  Software Engineering (ICSE), Ottawa, Ontario, Canada, 2025. doi: 10.48550/arXiv.2502.05714.

E. Glazer, E. Erdil, T. Besiroglu, D. Chicharro, E. Chen, A. Gunning, C. Falkman Olsson, J.-S.
  Denain, A. Ho, E. de Oliveira Santos, O. Järviniemi, M. Barnett, R. Sandler, M. Vrzala, J. Sevilla,
  Q. Ren, E. Pratt, L. Levine, G. Barkley, N. Stewart, B. Grechuk, T. Grechuk, S. Varma Enugandla,
  and M. Wildon. FrontierMath: A benchmark for evaluating advanced mathematical reasoning in
  AI. arXiv preprint arXiv:2411.04872, 2024.

K. Gopinathan. Lean proved this program was correct; then I found a bug. https://kirancodes.
  me/posts/log-who-watches-the-watchers.html, Apr. 2026. Blog post; reports a heap
  buffer overflow in lean_alloc_sarray in the Lean 4 runtime, found by AFL++ fuzzing of the
  verified lean-zip library. Accessed 26 April 2026.

M. H. Halstead. Elements of Software Science (Operating and Programming Systems Series). Elsevier
  Science Inc., 1977.

D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He,
  D. Song, and J. Steinhardt. Measuring coding challenge competence with APPS. In Proceedings
  of the 35th Conference on Neural Information Processing Systems (NeurIPS), 2021.

R. Hsiang, W. Adkisson, R. J. George, and A. Anandkumar. LeanDojo-v2: A comprehensive library
  for AI-assisted theorem proving in Lean. In The 5th Workshop on Mathematical Reasoning and AI
  at NeurIPS 2025, 2025.


                                                 10
J. Hu, T. Zhu, and S. Welleck. minictx: Neural theorem proving with (long-) contexts. arXiv preprint
   arXiv:2408.03350, 2024.
Y. Huang, X. Lin, Z. Liu, Q. Cao, H. Xin, H. Wang, Z. Li, L. Song, and X. Liang. Mustard: Mastering
   uniform synthesis of theorem and proof data. arXiv preprint arXiv:2402.08957, 2024.
D. Jackson and J. M. Wing. Lightweight formal methods. IEEE Computer, 29(4):21–22, 1996. doi:
  10.1109/2.491459.
V. Jacques, L. Wan, S. Kowalik, and E. Minack. PyGitHub. https://github.com/PyGithub/
  PyGithub, 2026. Accessed 26 April 2026.
J. Jiang, W. He, Y. Wang, G. Gao, Y. Hu, J. Wang, N. Guan, P. Wu, C. Dai, L. Xiao, and B. Dong.
   FATE: A formal benchmark series for frontier algebra of multiple difficulty levels. arXiv preprint
   arXiv:2511.02872, 2025.
C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan. SWE-bench: Can
  language models resolve real-world GitHub issues? In Proceedings of the 12th International
  Conference on Learning Representations (ICLR), 2024.
M. Lacchia. Radon: Python code metrics. https://radon.readthedocs.io/en/latest/, 2026.
Lean FRO. Comparator: A trustworthy judge for Lean proofs. https://github.com/
  leanprover/comparator, 2026. Sandboxes the build and replays proof terms, optionally cross-
  checking against an independently-implemented Rust kernel (nanoda). Accessed 26 April 2026.
S. Li, W. Lu, X. Shi, K. Weng, H. Sun, M. Yu, T. Zhang, G. Yu, H. Liu, and L. Du. MSC-180: A
   benchmark for automated formal theorem proving from mathematical subject classification. arXiv
   preprint arXiv:2512.18256, 2025.
C. Liu, J. Shen, H. Xin, Z. Liu, Y. Yuan, H. Wang, W. Ju, C. Zheng, Y. Yin, L. Li, et al. Fimo: A
  challenge formal dataset for automated theorem proving. arXiv preprint arXiv:2309.04295, 2023.
E. Lohn and S. Welleck. miniCodeProps: a minimal benchmark for proving code properties. arXiv
   preprint arXiv:2406.11915, 2024.
C. Loughridge, Q. Sun, S. Ahrenbach, F. Cassano, C. Sun, Y. Sheng, A. Mudide, M. R. H. Misu,
  N. Amin, and M. Tegmark. DafnyBench: A benchmark for formal software verification. arXiv
  preprint arXiv:2406.08467, 2024.
J. Lu, Y. Wan, Z. Liu, Y. Huang, J. Xiong, C. Liu, J. Shen, H. Jin, J. Zhang, H. Wang, et al.
   Process-driven autoformalization in lean 4. arXiv preprint arXiv:2406.01940, 2024.
P. Lu, J. Sheng, L. Lyu, J. Jin, T. Xia, A. Gu, and J. Zou. Solving inequality proofs with large
   language models. In The 39th Conference on Neural Information Processing Systems (NeurIPS),
   2025.
D. R. MacIver, Z. Hatfield-Dodds, and many other contributors. Hypothesis: A new approach to
  property-based testing. Journal of Open Source Software, 4(43):1891, 2019. doi: 10.21105/joss.
  01891.
T. J. McCabe. A complexity measure. IEEE Transactions on Software Engineering, (4):308–320,
  1976.
B. Miranda, S. Daruru, Z. Zhou, S. Barkallah, A. Nie, I. Mlauzi, L. Aniva, E. Obbad, W. Kirk, Y. Li,
  et al. Veribench: End-to-end formal verification benchmark for ai code generation in lean 4. 2025.
E. Miyazono. Formally scalable AI oversight through specifications. https://foresight.org/
  resource/evan-miyazono-formally-scalable-ai-oversight-through-specifications/,
  2024. Accessed 25 April 2026.
J. T. Perconti and A. Ahmed. Verifying an open compiler using multi-language semantics. In
   European Symposium on Programming Languages and Systems, pages 128–148. Springer, 2014.


                                                 11
A. Poiroux, G. Weiss, V. Kunčak, and A. Bosselut. Reliable evaluation and benchmarks for statement
  autoformalization. In Proceedings of the 2025 Conference on Empirical Methods in Natural
  Language Processing, pages 17958–17980, 2025.
S. Ravi and M. Coblenz. An empirical evaluation of property-based testing in python. Proc. ACM
   Program. Lang., 9(OOPSLA2), Oct. 2025. doi: 10.1145/3764068. URL https://doi.org/10.
   1145/3764068.
Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang, Z. Fu, Q. Zhu, D. Yang, et al.
  Deepseek-prover-v2: Advancing formal mathematical reasoning via reinforcement learning for
  subgoal decomposition. arXiv preprint arXiv:2504.21801, 2025.
C. Song, Z. Wang, F. Pu, H. Wang, X. Lin, J. Liu, J. Li, and Z. Liu. LeanGeo: Formalizing
  computational geometry problems in Lean. arXiv preprint arXiv:2508.14644v1, 2025.
A. Thakur, J. Lee, G. Tsoukalas, M. Sistla, M. Zhao, S. Zetzsche, G. Durrett, Y. Yue, and S. Chaud-
  huri. Clever: A curated benchmark for formally verified code generation. arXiv preprint
  arXiv:2505.13938, 2025.
K. Thompson, N. Saavedra, P. Carrott, K. Fisher, A. Sanchez-Stern, Y. Brun, J. F. Ferreira, S. Lerner,
  and E. First. Rango: Adaptive retrieval-augmented proving for automated software verification.
  arXiv preprint arXiv:2412.14063, 2024.
G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings, A. Thakur, and S. Chaudhuri. Put-
  nambench: Evaluating neural theorem-provers on the putnam mathematical competition. Advances
  in Neural Information Processing Systems, 37:11545–11569, 2024.
UK AI Security Institute. Inspect AI: Framework for large language model evaluations, 2024. URL
 https://github.com/UKGovernmentBEIS/inspect_ai.
M.   von  Hippel.        https://www.lesswrong.com/posts/SfhFh9Hfm6JYvzbby/
 the-scalable-formal-oversight-research-program, 2026.    Accessed 25 April
 2026.
M. von Hippel and Q. Dougherty.   Lies, damned lies, and proofs: Formal meth-
 ods are not slopless.   https://www.lesswrong.com/posts/rhAPh3YzhPoBNpgHg/
 lies-damned-lies-and-proofs-formal-methods-are-not-slopless,     Jan.  2026.
 Accessed 26 April 2026.
T.-Y. Wu et al. Quokka: Accelerating program verification with llms via invariant synthesis. arXiv
   preprint arXiv:2509.21629, 2025a.
W.-D. Wu, K. Wang, R. Mangal, and I. Dillig. Verina: Benchmarking formally verified code
  generation. arXiv preprint arXiv:2505.23135, 2025b.
Z. Wu, J. Wang, D. Lin, and K. Chen. Lean-github: Compiling github lean repositories for a versatile
   Lean prover. arXiv preprint arXiv:2407.17227, 2024.
H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen. Lean workbook: A large-scale lean problem
  set formalized from natural language math problems. Advances in Neural Information Processing
  Systems, 37:105848–105863, 2024.
Z. Yu, R. Peng, K. Ding, Y. Li, Z. Peng, M. Liu, Y. Zhang, Z. Yuan, H. Xin, W. Huang, et al.
  Formalmath: Benchmarking formal mathematical reasoning of large language models. arXiv
  preprint arXiv:2505.02735, 2025.
L. Zeng, F. Che, X. Huang, F. Ye, X. Xu, B. Yuan, and J. Fu. Veriequivbench: An equivalence
  score for ground-truth-free evaluation of formally verifiable code. In International Conference on
  Learning Representations, volume 2026, pages 146015–146063, 2026.
K. Zheng, J. M. Han, and S. Polu. Minif2f: a cross-system benchmark for formal olympiad-level
  mathematics. arXiv preprint arXiv:2109.00110, 2021.



                                                 12
A    Overview of other datasets

Benchmark                             Language                              Theorems Focus
Minif2f Zheng et al. [2021]           Lean, Isabelle, HOL Light, Metamath        488   math Olympiad
PutnamBench Tsoukalas et al. [2024]   Lean, Isabelle, Coq/Rocq                   640   math Olympiad
Fimo Liu et al. [2023]                Lean                                       149   math Olympiad
DafnyBench Loughridge et al. [2024]   Dafny                                      782   scraped Dafny
                                                                                       proofs
ProofNet Azerbayev et al. [2023]      Lean                                       371   U math
RLM25 Poiroux et al. [2025]           Lean                                       619   G math
Lean Workbook Ying et al. [2024]      Lean                                    57,000   HS, U, G math
FormalMATH Yu et al. [2025]           Lean                                     5,560   math Olympiad
LEAN-GitHub Wu et al. [2024]          Lean                                    28,597   scraped Lean
                                                                                       proofs
ProverBench Ren et al. [2025]         Lean                                       325   math Olympiad
MiniCTX Hu et al. [2024]              Lean                                       762   six Lean
                                                                                       projects
LeanGeo Song et al. [2025]            Lean                                       122   HS, U, G math
IneqMath Lu et al. [2025]             Lean                                     1,522   math Olympiad
FATE-{M,H,X} Jiang et al. [2025]      Lean                                       350   U, G math
VeriBench Barkallah et al. [2025]     Lean                                       857   software
                                                                                       verification
FVAPPS Dougherty and Mehta [2025]     Lean                                    17,931   software
                                                                                       verification
                                                                                       (from APPS)
CLEVER Thakur et al. [2025]           Lean                                       161   software
                                                                                       synthesis &
                                                                                       verification
Vericoding Bursuc et al. [2025]       Lean, Dafny, Verus                      12,504   software
                                                                                       synthesis &
                                                                                       verification
MUSTARD Huang et al. [2024]           Lean                                     5,866   HS, U math
FormL4 Lu et al. [2024]               Lean                                    14,510   U math
CoqStoq (Rango) Thompson et al.       Coq/Rocq                                10,396   software
[2024]                                                                                 verification
MSC-180 Li et al. [2025]              Lean                                       180   U, G math
HOList Bansal et al. [2019]           HOL Light                               29,462   U, G math
FVSpec:FV                             Lean                                    75,005   software
                                                                                       verification:
                                                                                       specs from the
                                                                                       wild
Table 1: Prior ITP benchmarks. HS = high-school, U = undergraduate, G = graduate. If one
benchmark improves upon another, we exclude the lesser.


Find an overview of prior ITP benchmarks in Table 1.

B    Comparison with the Hypothesis Corpus
We released our corpus on HuggingFace in January 2026. In April 2026, while we were finalizing this
work, the Hypothesis maintainers released their own scraped corpus DeVoe [2026] (HC-2026). The
two corpora target different downstream uses—HC-2026 is built to study Hypothesis runtime behavior
(entropy consumption, predicate firing, coverage), while ours is built to feed a Lean formalization
pipeline—which drives the design differences summarized in Table 3.
A consequence of HC-2026’s runtime focus is that it filters out as “invalid” any repository whose
PBTs may not be directly runnable without some custom setup: code that depends on external services,
API keys, environment variables, or live databases. Our pipeline imposes no such requirement, since
we only need a PBT’s source code to translate it into Lean. Of our 497 repositories, 67 (13%) appear
in HC-2026’s valid (executable) set and 195 (39%) appear in the pre-validity superset. HC-2026


                                                  13
  Table 2: PBT corpus statistics.              Table 3: Comparison with HC-2026 DeVoe [2026].

Metric                               Value                              FVSpec:PBT          HC-2026
PBTs (raw scrape)               54,345          Discovery                 dep. graph      GitHub search
PBTs (deduplicated)               8,314         Raw PBTs                    54,345            38,885
PBTs (public release)             7,413         Tests (deduped)              7,413            28,928
Unique repositories                 497         Repos                         497              1,529
Unique GitHub owners                431         Repo dedup                   none            is_fork
Upstream project names              453         Test dedup                SHA-256         parametrization
Top-1 / top-10 PBT share 11.5% / 30.8%          License filter           no copyleft           none
                                                Per-test data          source + metrics runtime + coverage
Per-repo (min / med / max):
 PBTs per repo                  1 / 4 / 852     Repo overlap (valid)            67 / 497 (13%)
 Stars                      0 / 0 / 81,185      Repo overlap (any)             195 / 497 (39%)
 Forks                      0 / 0 / 29,652
Per-PBT (min / med / max):
 PBT LoC                       2 / 10 / 174
 Direct fn deps                   0 / 0 / 12



rejected most of the other 128 because it found no Hypothesis tests after installing them (80) or
judged them near-duplicates of another repository (28).




                                                    14
