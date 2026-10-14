                                                                                Pareto Optimal Code Generation


                                                               Gabriel Orlanski 1 Nicholas Roberts 1 Aws Albarghouthi 1 Frederic Sala 1


                                                                   Abstract                                 weight HumanEval (Chen et al., 2021) unit tests.
                                              Generate-then-rank is the dominant test-time scal-            Recent work discards neural reward models when reliable
                                              ing (TTS) paradigm for code generation, but scal-             test suites exist (DeepSeek-AI et al., 2025; Muennighoff
                                              ing accuracy by sampling and executing more can-              et al., 2025; Lambert et al., 2025), but this assumes verifi-
arXiv:2506.10056v2 [cs.SE] 24 Feb 2026




                                              didates makes comprehensive verification a major              cation cost is negligible relative to generation cost. As test
                                              computational bottleneck. This creates an inher-              suites grow more complex, this assumption breaks down.
                                              ent trade-off between accuracy and compute that,
                                                                                                            This cost creates a fundamental tradeoff. Full test
                                              despite its importance to TTS, is often ignored.
                                                                                                            suites maximize correctness but bottleneck throughput;
                                              Specifically, faster but noisier signals, such as
                                                                                                            lightweight checks like compilation and partial execution
                                              outcome reward models (ORMs), are dismissed
                                                                                                            maximize throughput but miss bugs. Outcome Reward Mod-
                                              as suboptimal. We frame verifier selection as a
                                                                                                            els (ORMs) offer a third option: neural rankers that score
                                              Pareto optimization problem and empirically map
                                                                                                            candidates in a single pass, with inference cost depending
                                              the accuracy-throughput frontier across signals,
                                                                                                            on candidate length rather than task complexity. These three
                                              including the full test suite, heuristics for selective
                                                                                                            approaches define a Pareto frontier of accuracy vs. through-
                                              execution, and ORMs, across four Python bench-
                                                                                                            put. However, where ORMs sit on this frontier relative to
                                              marks. We show that ORMs are most effective
                                                                                                            execution-based methods—and whether combining the two
                                              at optimizing the Pareto curve when pruning is
                                                                                                            shifts the frontier outward—has not been studied.
                                              used in the generate-then-rank pipeline–known
                                              as staged verification–where lightweight filters              The question is complicated by an asymmetry. Execution-
                                              remove obviously incorrect solutions, including               based tradeoffs are transparent: using fewer tests pre-
                                              candidates with small syntactic or character-level            dictably misses more bugs. ORM tradeoffs are opaque:
                                              bugs, before expensive verification. Our prun-                these models can assign high scores to candidates with ob-
                                              ing analysis shows that eliminating incorrect yet             vious defects, including arithmetic mistakes and logical er-
                                              highly ranked candidates (often character-level               rors in intermediate reasoning steps (Lightman et al., 2023;
                                              bugs) prevents wasted compute on incorrect to-                Wang et al., 2024). Cheap execution filters catch precisely
                                              kens. We find that ORMs with staged verification              these failure modes. Prior work evaluates verifiers in isola-
                                              shift the Pareto frontier outward, achieving 11.64x           tion, reporting accuracy or throughput but not both, leaving
                                              higher throughput at a cost of 8.26% accuracy rel-            the frontier unmapped (Inala et al., 2022; Zhang et al., 2022;
                                              ative to full test-suite verification.                        Ni et al., 2023; Cobbe et al., 2021; Snell et al., 2024).
                                                                                                            We empirically map the accuracy-throughput frontier
                                                                                                            for code verification. We focus on single-file Python bench-
                                         1. Introduction                                                    marks where verification cost already varies substantially;
                                         Generate-then-rank has become the dominant paradigm for            repository-scale tasks like SWE-Bench are future work.
                                         test-time scaling in code generation. The pipeline generates       Our investigation spans three verification signals across
                                         many candidates from a model, verifies each one against a          four benchmarks: full test suites, partial test execution, and
                                         test suite, and returns the highest-ranked correct solution.       ORMs. We evaluate both standard generate-then-rank and
                                         With hundreds or thousands of candidates, verification be-         staged verification, where lightweight filters remove obvi-
                                         comes the bottleneck. This is especially true for more com-        ous failures before ORM ranking (Figure 2). Staged verifi-
                                         prehensive SWE-Bench (Jimenez et al., 2024) test suites,           cation dominates naive ORM ranking across much of the
                                         which cost orders of magnitude more than the much lighter-         frontier: filtering eliminates candidates with syntactic
                                                                                                            bugs that ORMs systematically over-rank, preventing
                                            1
                                              University of Wisconsin-Madison. Correspondence to:           wasted compute on incorrect solutions (Figure 1).
                                         Gabriel Orlanski <gorlanski@cs.wisc.edu>.
                                                                                                            Our contributions are as follows:
                                         Preprint. February 26, 2026.

                                                                                                        1
                                                              Pareto Optimal Code Generation

                           500M                     1.5B                            3B                              7B          35
                                                                                                                                            14B
                                                                       16
                                           8
                 2.0                                                   14                         20                            30
                                           6                           12                                                       25
Best-of-64 (%)




                 1.5                                                                              15
                                                                       10                                                       20
                 1.0                       4                            8
                                                                                                  10                            15
                                                                        6
                 0.5                       2                                                                                    10
                                                                        4                          5                             5
                 0.0                       0                            2
                         102         104          102       104               102         104                 102         104         102         104
                        Prog/Sec (log)          Prog/Sec (log)               Prog/Sec (log)                  Prog/Sec (log)          Prog/Sec (log)
                                                          Non-Staged        Staged Verification         Full Tests

Figure 1. Staged Verification Shifts the Pareto Frontier. Each panel shows one generator size (500M to 14B) on CodeContests. Red
dashed: non-staged verification. Blue solid: staged verification, which filters before ORM ranking. Gold ×: full test suite. The shaded
region shows gains from staging; the frontier shifts outward across all generator sizes.


                 • We map the accuracy-throughput frontier: ORMs                     based verification; repository-scale tasks are future work.
                   are 8.60× faster than full test suites and 32.86% more
                   accurate than majority voting.                                    2.1. Problem Setup
                 • We show staged verification shifts the frontier out-
                   ward: Filtering before ranking is 11.64× faster and              Given a programming problem x, a generator produces
                   8.26% less accurate than full test suites.                       candidates C = {c1 , . . . , cn }. Each candidate is scored
                 • We characterize ORM failure modes and demon-                     by a verifier V, and the top-ranked candidate is returned.
                   strate that staged verification addresses them: Gains            We assume each problem is associated with test cases that
                   stem from removing incorrect candidates that ORMs                determine the correctness of a candidate, as is standard in
                   over-rank, particularly code with small syntactic bugs           competitive programming (Li et al., 2022; Jain et al., 2024)
                   that preserve overall structure.                                 and software engineering benchmarks (Jimenez et al., 2024).
                 • We show staged verification does not require careful
                   test curation: Random subsets of tests achieve false              Accuracy. We measure ranking quality using Best-of-
                   positive rates comparable to those of curated subsets,            k (Bofk; Hosseini et al., 2024): the probability that among
                   with low variance across selections.                              k random candidates, the highest-ranked one is correct. Let
                                                                                     ri denote the rank i candidate and 1[ri ] indicate correctness:
We have also released code reproducing our experiments.1                                                  n−k      
                                                                                                       1 X n−i−1
                                                                                         Bofk :=       n
                                                                                                                     · 1[ri is correct].               (1)
                                                                                                                k−1
2. The Verification Pareto Frontier                                                                    k i=0


This section formalizes the verification problem. We first de-                       Throughput. We measure the programs processed per
fine the metrics that characterize the Pareto frontier (subsec-                      second (PPS). Strong verifiers achieve high accuracy but low
tion 2.1), then introduce staged verification as a strategy for                      PPS; weak verifiers achieve high PPS but lower accuracy.
combining cheap filters with neural rankers (subsection 2.2),
and finally describe ORMs trained with the Bradley-Terry                             Verifiers. The strongest verifier Vall (full test suite) runs
objective as fixed-cost verifiers (subsection 2.3).                                  all test cases and admits no false positives as a candidate
Verification strategies occupy different points on an                                that passes is correct. Weak verifiers VSN (first-N -tests)
accuracy-throughput Pareto frontier. Strong verifiers (full                          check only a subset of tests; they are fast but admit false
test suites) maximize accuracy but bottleneck throughput;                            positives. An outcome reward model Vθ (neural ranker)
weak verifiers (syntax checks, partial execution) maximize                           scores candidates without execution, offering constant-time
throughput but sacrifice accuracy. ORMs offer fixed in-                              inference regardless of test suite size.
ference cost regardless of test suite complexity, but where
they sit on this frontier—and whether combining them with                            2.2. Staged Verification
lightweight filters can shift the frontier outward—remains
                                                                                     A program that fails any test is incorrect; a program that
unexplored. We focus on Python benchmarks with test-
                                                                                     passes all tests is correct. This asymmetry motivates staged
  1
    https://github.com/SprocketLab/                                                  verification: use a cheap filter to eliminate obviously incor-
orm-code-verifier                                                                    rect candidates before ranking survivors with an ORM. Re-

                                                                                2
                                                     Pareto Optimal Code Generation


      Normal Ranking                                                      Staged Verification
 Generate                                 Top 1              Generate                      Survivors                          Top 1

                                               1.0                                                                                 0.99
                        Full                                                     Weak                     ORM
                                               1.0                                                                                 0.85
                       Tests                                                    Verifier                 Ranking
                                               0.8                                                                                 0.42
   Unsorted                                    0.2            Unsorted
                                                                                                                                   0.00
                                               0.0                                         Failed (Bypasses ORM)
                                                                                                                                   0.00

Figure 2. Comparison of verification strategies. Normal ranking runs all tests to produce a high-quality ordering but is slow, especially
with a large test suite. Staged verification uses a weak verifier to filter obvious failures, then ranks survivors using an ORM.


moving candidates that can never be correct avoids wasted                3. Experimental Design
compute on ORM ranking and reduces possible spurious
correlations, so with a sufficiently large ORM we would                  We train ORMs on CodeContests and GSM8K, then mea-
expect both accuracy and throughput improvements.                        sure their accuracy and throughput across four benchmarks.
                                                                         In subsection 3.1 we describe the data, training, and eval-
We use deliberately simple filters—compilation, linting,                 uation protocol. In subsection 3.2 we detail the ranking
execution on the first N test cases—to isolate the interaction           strategies and weak filters under comparison.
between filtering and neural ranking from the complexity of
filter design. The pipeline is shown in Figure 2.                        3.1. Setup

2.3. ORMs as Verifiers                                                   Data. We train ORMs on CodeContests-Python (Li et al.,
                                                                         2022) and GSM8K (Cobbe et al., 2021) in PAL format (Gao
Let Vθ be the verifier that uses the ORM with parameters θ               et al., 2022). Training candidates are generated with Qwen
to predict if c is correct. We denote its output as:                     2.5 Coder Instruct 7B (Hui et al., 2024) using VLLM (Kwon
                                                                         et al., 2023), sampling 128 times per problem with tem-
           Vθ (c | x) = P (c passes all tests | x, c).         (2)       perature T =1.0 and topp =0.95 (Holtzman et al., 2020).
                                                                         We randomly sample up to 6 pairs per problem from 4.7K
We use a language model backbone with a scalar prediction                CodeContests and 7.3K GSM8K problems. For distribution
head that outputs scores in [0, 1]. Training uses pairs of               shift evaluation, we use HumanEval (Chen et al., 2021) and
candidates (cw , cℓ ) where cw is correct and cℓ is incorrect.           MBPP (Austin et al., 2021) via EvalPlus (Liu et al., 2023;
The Bradley-Terry objective (Bradley & Terry, 1952; Stien-               2024). All code is formatted using the Black formatter for
non et al., 2020) maximizes the margin between correct and               standardization and to handle whitespace requirements.
incorrect candidates. Formally, this objective is:
                                                                         To determine correctness, we follow existing works (Cas-
 LRM = −E(x,cw ,cℓ )∼D [log σ(Vθ (cw |x) − Vθ (cℓ |x))]. (3)             sano et al., 2022; Orlanski et al., 2023; Jain et al., 2024) in
                                                                         using the subprocess2 library to execute the programs with
At inference, the ORM scores each candidate in a single                  the test cases. For GSM8K, we check that the outputted
forward pass. Full training details are in Appendix A.                   scalar is correct using an assertion. In the case of CodeCon-
                                                                         tests, we check that the program prints the correct output to
Why not process reward models? Process reward mod-                       STDOUT and stop execution on the first error. We detail
els (PRMs) score individual reasoning steps rather than final            our training data in Table 4. We filter out any programs with
outcomes (Lightman et al., 2023; Uesato et al., 2022). We                syntax errors as these could be caused by the model hitting
exclude PRMs for two reasons. First, step-level annota-                  the token limit rather than a poor generation.
tions are expensive. PRM800K required extensive human
labeling (Lightman et al., 2023), and automated alterna-
                                                                         Training. An ORM does not necessarily need to be a lan-
tives remain an active research area (Wang et al., 2024).
                                                                         guage model, but given the strong overall results of prior
Second, PRMs require scoring each step, resulting in multi-
                                                                         work in using a language model as an ORM (Cobbe et al.,
ple forward passes per candidate, directly undermining the
                                                                         2021), we choose to use these. We train with the Bradley-
throughput advantage that makes learned verifiers attrac-
tive. ORMs require only pass/fail labels and a single pass,                2
                                                                             https://docs.python.org/3/library/
making them practical for high-throughput verification.                  subprocess.html

                                                                     3
                                                Pareto Optimal Code Generation

Terry objective (Equation 3), which models P (cw ≻ cℓ )                  1. Vc : Remove candidates failing the syntax checker.
for correct candidate cw and incorrect candidate cℓ . Intu-              2. VLint : Remove candidates with PyLint errors.
itively, this objective pushes Vθ (cw |x) higher than Vθ (cℓ |x)         3. VSN : Remove candidates failing the first N test cases
by maximizing the margin between correct and incorrect                      within a timeout of 3 seconds.
candidates. At inference, the ORM scores any new candi-
date based on how likely it is to be preferred over incorrect          We denote staged verification as Vx+θ where x is the fil-
solutions. We train using Adam (Kingma & Ba, 2017), co-                ter. For example, VS10 +θ filters with the first 10 tests, then
sine scheduling (peak 5e−6, 10% warmup), batch size 64,                ranks survivors with the ORM. For majority voting base-
and max sequence length 2048. We train for 2 epochs, use               lines, we rank by test cases passed with duplicate count as
the final checkpoint, and average results over six random              tiebreaker (Ehrlich et al., 2025; Li et al., 2022).
seeds. Both generators and ORM backbones are from the
Qwen family. While this ensures compatibility, it may fa-
                                                                       4. Results
vor the ORM through distribution matching; we partially
address this via distribution-shift evaluation on HumanEval            We first characterize when ORM-only ranking occupies
and MBPP. Full hyperparameters are in Appendix A.                      favorable frontier points (subsection 4.1), then show how
                                                                       test-based filtering shifts the frontier further outward (sub-
Evaluation. CodeContests and GSM8K programs exe-                       section 4.2). subsection 4.3 investigates why staging helps:
cute via subprocess with a 30s timeout (Cassano et al.,                ORMs systematically overrank candidates with subtle bugs
2022; Orlanski et al., 2023). HumanEval and MBPP use                   that tests catch. subsection 4.4 confirms that filtering effec-
EvalPlus (Liu et al., 2023; 2024). All verifiers are run across        tiveness is robust to test choice, and subsection 4.5 translates
5 independent trials to mitigate runtime noise. We measure             these findings into cost-accuracy trade-offs.
preprocessing, execution, and postprocessing time, exclud-
                                                                       Figure 1 shows that staged verification shifts the Pareto fron-
ing disk I/O. Vθ experiments use a single 48GB A6000 GPU
                                                                       tier outward across generator sizes. ORMs occupy favorable
with 16 cores and 64GB memory. Execution-only setups
                                                                       frontier points (8.60× faster than Vall , 32.86% more accurate
use 64 cores and 256GB for CodeContests. For the other
                                                                       than naive baselines) across datasets (Table 1) and genera-
datasets, we use 32 cores and 128GB memory. These config-
                                                                       tor sizes (Table 2). Staging improves on ORM-only points
urations are roughly cost-equivalent according to the current
                                                                       because lightweight filters remove incorrect candidates that
prices per hour on AWS. We deduplicate candidates via
                                                                       ORMs systematically overrank. This benefit does not de-
exact string match after Black formatting, then weight out-
                                                                       pend on specific test selection: random subsets achieve
comes by duplicate count for fair Best-of-k measurement.
                                                                       comparable false positive rates with low variance.
ORM Inference. We use dynamic batching akin to se-
quence packing (Raffel et al., 2020): rather than fixed batch          4.1. ORMs Occupy Favorable Frontier Points
sizes bounded by outlier-length programs, we construct a               Table 1 summarizes accuracy (Best-of-64) and throughput
batch by continuously adding candidates to the batch until             (PPS) across verification methods. Results are averaged over
the net tokens is over a threshold size. This establishes a            six random seeds with 95% confidence intervals; median CI
fairer comparison to CPU methods as we are properly uti-               width is 1.48 percentage points.
lizing GPU memory and FLOPs. For the 500M ORM we
set the max tokens per batch to 500,000 while for the 1.5B             When full-suite execution is the bottleneck, Vθ achieves
ORM we set the max tokens to 200,000.                                  8.60× higher throughput than Vall while remaining more
                                                                       accurate than naive baselines (Table 1), making ORM-only
3.2. Verification Methods                                              ranking a practical frontier choice. When even partial ex-
                                                                       ecution is inexpensive, however, running a small number
We evaluate the following three ranking strategies and three           of tests provides reliable signal at low cost, and ORM-only
filtering methods that can precede ranking:                            points become less competitive. Smaller ORMs sharpen
                                                                       this trade-off: the 500M variant is 1.44× faster than the
  1. Majority Voting: Select the most common candidate                 1.5B model with only a 4.99% accuracy loss. ORM-only
     after normalization with Black. Standard method for               ranking is most compelling when execution is expensive;
     ranking sequences generated (Ehrlich et al., 2025).               when even partial execution is cheap, ORM-only points
  2. Vθ : Score each candidate with the ORM and then                   become less competitive on the frontier.
     select the highest-scoring candidate.
  3. Vall : Select the candidate passing the most tests.               4.2. Staged Verification Shifts the Frontier
Next, for experiments involving staged verification, we use            Table 2 shows results across generators. Syntax and lint
the following heuristics as weak verifiers:                            filtering remove only 1.30% and 2.62% of candidates on

                                                                   4
                                                    Pareto Optimal Code Generation

Table 1. Overall results for the different pruning with a weak verifier then ranking methods. If Filter is “—” that means no pruning is done.
Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. Vall is the case
where all test cases are run. Rows with Ranker set to “MV” are verifier-only baselines that select using majority voting without ORM
inference. “Syntax” and “Lint” remove any programs with the respective errors. “N Test” prunes out any programs that do not pass the
first N test cases. The evaluation dataset is generated with Qwen 2.5 Coder 7B Instruct using T = 1.0, n = 128, topp = 0.95, and 1024
tokens. The results are averaged over six random seeds.

                                          CodeContests         GSM8K                 HumanEval                   MBPP
               Filter          Ranker   Bof64    PPS       Bof64   PPS            Bof64    PPS          Bof64       PPS
                               MV        2.55   64777.78    83.28    39596.93      84.21    48077.73     66.36     52179.55
               —               500M      5.33     52.49     84.13     264.94       79.31     144.84      66.04      303.14
                               1.5B      6.34     22.53     87.05     113.79       81.37      64.14      69.70      133.17
                               MV        2.55   6122.37     83.32     6256.05      84.22     6774.73     66.63     5679.06
               Syntax          500M      5.79    60.87      84.75      309.44      79.57      145.15     65.54      353.34
                               1.5B      6.58    25.09      88.09      127.63      82.37       66.88     70.92      149.13
                               MV        2.67    302.09     83.39        488.17    84.23     633.15      67.44      613.41
               Lint            500M      5.34     47.56     84.30        156.85    79.26     101.10      66.37      166.69
                               1.5B      6.60     22.64     87.05         90.24    82.23      55.19      70.36      100.38
                               MV       15.72    131.73      —            —        87.62     1020.54     76.07      930.69
               1 Test          500M     15.75     69.50      —            —        83.88      125.86     75.17      229.08
                               1.5B     16.86     58.35      —            —        85.98       63.32     77.04      132.52
                               MV       17.12    120.93      —            —        92.46     650.77      86.06      345.21
               10 Tests        500M     17.54     73.22      —            —        90.01     134.92      85.19      169.30
                               1.5B     18.06     65.80      —            —        90.05      72.83      86.57      121.29
                        Vall            20.69     2.95      97.96        88.21     95.97      22.19      90.04      15.01



average as shown in Table 8. The filtering overhead exceeds               ORMs remain most useful when partial execution has high
inference savings, decreasing throughput by 10.42× for the                fixed costs like environment setup or container launch, or
500M ORM and 4.24× for the 1.5B. Test-based filtering                     when filtering leaves a large ambiguous survivor set. We
changes the picture: on CodeContests, VS10 removes 90% to                 find that staged verification shifts the Pareto frontier
97% of candidates, shifting the cost balance so that VSN +θ               outward, with VS10 +θ achieving near-Vall accuracy at an
delivers 12.41× higher throughput than Vall . The best con-               order of magnitude higher throughput.
figuration, VS10 +θ with the 1.5B ORM, is 10.22× faster
than Vall while losing only 7.58% accuracy.                               4.3. ORMs Systematically Overrank Small Bugs
Staged verification is not purely a speed optimization, as                We do not retrain the ORM after filtering; the only way to
accuracy improves alongside throughput: the 500M ORM                      improve Best-of-k is to remove incorrect candidates that the
sees a 45.15% rise in Best-of-64 and the 1.5B a 38.09%                    ORM ranked too highly. In Figure 3 we show where the
rise over their unfiltered counterparts because test filtering            filtered candidates fall in the ORM ranking.
removes candidates the ORM would have misranked. On
CodeContests, the 1.5B ORM with VS10 +θ achieves 18.06%                   Syntax-filtered candidates cluster at the bottom (mean rank
with 95% CI of [17.67, 18.45]. These accuracy gains of 12+                96.72 out of 128, placing them in the lowest quartile). Re-
points over ORM-only exceed CI widths by roughly 15×.                     moving candidates the ORM already dislikes changes little.
                                                                          Test-filtered candidates tell a different story: mean rank
These patterns hold across generator sizes and sampling                   65.29, a shift of 31 positions toward the top. These are in-
temperatures. With the 14B generator, VS10 +θ yields 8.65×                correct candidates the ORM ranked in the middle or higher;
speedup at 7.64% accuracy loss. Temperature ablations                     removing them directly improves accuracy. Filtering also
show average throughput of 146.40 ±68.97 and 89.28                        stabilizes results: with VS10 +θ , Best-of-64 standard devia-
±33.49 PPS for the 500M and 1.5B ORMs, which is 13.44×                    tion drops by 23.23% (500M) and 31.23% (1.5B).
faster than Vall while accuracy degrades by only 8.80 points.
Throughput CIs are tight for CodeContests at less than 1%                 What bugs do ORMs miss? We analyze candidates the
of mean and moderate for HumanEval/MBPP at 3–10%.                         ORM ranked in its top-16 but VS1 filtered. Comparing
The latter use EvalPlus, which executes code via eval                     pattern prevalence in these “overrated” candidates versus
rather than subprocess, introducing additional runtime vari-              correct ones reveals which bugs ORMs fail to penalize.
ance. Reported speedups exceed CI widths by 10× or more.
                                                                          Three patterns are 20 to 46× more common in overrated can-

                                                                     5
                                                          Pareto Optimal Code Generation

Table 2. Results for the different pruning then ranking on only CodeContests as we scale the size of the generator model. If Filter is “—”
that means no pruning is done. Green backgrounds is higher performance while Red backgrounds is lower performance with respect to
the entire column. Vall is the case where all test cases are run. Rows with Ranker set to “MV” are verifier-only baselines that select using
majority voting without ORM inference. “Syntax” and “Lint” remove any programs with the respective errors. “N Test” prunes out any
programs that do not pass the first N test cases. The evaluation dataset is generated with Qwen 2.5 Coder Instruct models using T = 1.0,
n = 128, topp = 0.95, and 1024 tokens. The results are averaged over six random seeds.

                                          500M                   1.5B                      3B                    7B                    14B
        Filter          Ranker    Bof64       PPS        Bof64          PPS        Bof64        PPS      Bof64        PPS      Bof64         PPS
                        MV         0.00     65679.19      0.09     66369.90         1.87    64541.54      2.55    64777.78      2.21    62487.39
        —               500M       0.47       68.39       1.64       67.79          4.52      64.02       5.33      52.49      10.99      59.83
                        1.5B       0.61       26.42       2.62       26.63          5.76      25.14       6.34      22.53      12.86      23.52
                        MV         0.00     5642.49       0.09     5785.38          1.87    4972.95       2.55    6122.37       5.23     6432.92
        Syntax          500M       0.46      64.53        1.65      70.63           4.55     65.86        5.79     60.87       11.02      62.31
                        1.5B       0.58      27.16        2.67      28.25           5.68     25.56        6.58     25.09       13.03      24.61
                        MV         0.00      523.78       0.10      550.65          1.92        548.99    2.67        302.09    5.25     459.62
        Lint            500M       0.47       62.47       1.55       58.69          4.31         51.05    5.34         47.56    7.89      44.11
                        1.5B       0.67       31.28       2.62       27.19          5.47         23.45    6.60         22.64    8.90      20.01
                        MV         1.39      126.19       4.92      124.94          9.65        122.58   15.72        131.73   22.76     132.92
        1 Test          500M       1.71       79.64       5.64       74.06         10.93         66.69   15.75         69.50   24.47      66.16
                        1.5B       2.02       74.27       5.60       67.36         11.39         58.02   16.86         58.35   25.52      52.46
                        MV         1.65      125.65       5.73      122.34         12.16        116.15   17.12        120.93   25.83     120.53
        10 Tests        500M       1.76       87.47       5.95       79.18         12.67         70.78   17.54         73.22   28.02      67.14
                        1.5B       2.15       82.33       5.75       73.53         13.04         64.18   18.06         65.80   28.10      57.46
                 Vall              2.16       3.32        7.83          2.23       14.92         2.54    20.69         2.95    31.98         3.65


Table 3. Bug patterns the ORM fails to penalize. Freq is overall                    ness labels see similar token sequences and assign similar
pattern prevalence in problems with at least one passing solution;
Top-16 is the percentage of solutions in the top-16 ORM-rated
                                                                                    scores; a single test catches the runtime difference. Test-
selections containing the pattern.                                                  based filtering catches bugs the ORM misses, particu-
                                                                                    larly single-character errors that preserve surface form
                                 CodeContests                                       but fail at runtime. Filtered candidates sat 31 ranks too
               Pattern                      Freq       Top-16                       high on average; removing them shifts the frontier.
               sorted() w/o key             4.8%        2.5%
               / instead of //              2.9%        3.4%                        4.4. Robustness to Test Selection
               .remove() in loop            1.3%        2.1%
               Large number ops             1.1%        0.8%                        How sensitive is filtering effectiveness to which tests are se-
               while len()                  0.7%        0.8%                        lected? If there are large discrepancies between the discrim-
                                                                                    inative power of test cases, then using staged verification
                           HumanEval + MBPP                                         for code generation is not generalizable. We investigate the
                                                                                    false-positive rate (FPR) of test cases on CodeContests to de-
               Pattern                      Freq       Top-16
                                                                                    termine if our previously discussed results are an artifact of
               / instead of //              3.8%        3.3%                        lucky test selection. To do this, we profile the test execution
               sorted() w/o key             2.1%        3.7%
               /2 in binary search          1.5%        0.7%
                                                                                    time of generated solutions for CodeContests with the 1.5B
               (a+b)/2 midpoint             0.6%        0.3%                        and 3B Qwen 2.5 Coder Instruct generated solutions.3 We
                                                                                    run each test case five times with the solution and measure
                                                                                    its mean wall time to run in isolation.

didates: while len(x) loops (46× enrichment), large                                 In Figure 4 we show that test selection has minimal impact.
integer arithmetic (40×), and .remove() inside iteration                            At k = 1, mean FPR is 86.3% (1.5B) and 79.6% (3B), with
(22×). Table 3 confirms the mechanism: these patterns                               low variance across test choices (error bars). At k = 10,
appear at similar rates in the full candidate pool and in the                       mean FPR drops to 60.1% in 0.71 s (1.5B) and 51.2% in
ORM’s top-16 selections.                                                            0.62 s (3B). Incorrect LLM-generated code tends to fail
                                                                                    broadly rather than on specific edge cases—any single test
These bugs share a property: they preserve surface form.                            is roughly as effective as any other. We conclude that the
Float division (/) and integer division (//) differ by one
                                                                                       3
character. int(x/2) and x//2 look similar but behave                                     The 7B and 14B generated solutions continuously caused our
differently for negative numbers. ORMs trained on correct-                          64 core/256GB to hang indefinitely with the additional profiling.


                                                                               6
                                                                         Pareto Optimal Code Generation


                      0.7
                                     CodeContests                      1.0
                                                                                                    HumanEval                   1.4
                                                                                                                                                MBPP
                      0.5                                              0.7                                                      0.9
Lint


                      0.2                                              0.3                                                      0.5
                      0.0 0   25         50      75        100   125   0.0     80                        100        120         0.0 0    25    50    75    100     125
                       7                                                6                                                        7
      1 Test




                       4                                                4                                                        5
                       2                                                2                                                        2
                       0 0     25         50     75        100   125    0 0     25                  50     75    100      125    0 0     25    50    75    100     125
                       7                                                9                                                        9
      10 Tests




                       5                                                6                                                        6
                       2                                                3                                                        3
                       0 0     25         50     75        100   125    0 0     25                  50     75    100      125    0 0     25    50    75    100     125
                              Rank of Programs Removed                         Rank of Programs Removed                                 Rank of Programs Removed
Figure 3. Distribution of filtered candidates by ORM rank. Rank 1 is the top-ranked candidate; rank 128 is the lowest. Rows are filters;
columns are datasets. Results shown for the 1.5B ORM; the 500M ORM graph is in Figure 6.


                                                      1.5B                                               We find staged verification to not require careful test cu-
                      1.0                                                           4                    ration, as random test subsets achieve comparable false
                      0.8                                                                                positive rates with low variance.
False Positive Rate




                                                                                    3
                                                                                     Net Time (s)




                      0.6
                                                                                    2                    4.5. Practical Implications
                      0.4
                                                                                                         Our findings enable cost-accuracy Pareto frontiers based on
                      0.2                                                           1
                                                                                                         cloud provider pricing (Table 7); in Figure 5 we show this
                      0.0                                                           0                    frontier for CodeContests, where VS10 +θ is Pareto-optimal,
                                                                                                         achieving near-Vall accuracy at a fraction of the cost.
                                                      3B
                      1.0                                                           4                    We translate throughput to dollars using on-demand prices
                      0.8                                                                                (January 22, 2026) and the hardware configurations in sec-
False Positive Rate




                                                                                    3
                                                                                     Net Time (s)




                                                                                                         tion 3. For CodeContests (n=128), costs per 100k programs
                      0.6
                                                                                    2                    form three tiers: majority voting baselines cost $0.63–$0.69,
                      0.4                                                                                staged ORM verification costs $1.3–$2.4, and Vall costs $28.
                      0.2                                                           1                    Staged verification is 12–22× cheaper than Vall while recov-
                                                                                                         ering most of its accuracy. Moving from 1 to 10 tests adds
                      0.0 0         10        20        30         40         50 0                       only $0.06 but gains 1.40% absolute accuracy.
                                         Number of Random Tests (k)
                                                                                                         Costs are stable across generator sizes: verifier-only PPS
Figure 4. False positive rate and cumulative time for random test                                        ranges 122.6–132.9 for 1 test and 116.2–125.7 for 10 tests
subsets (top: 1.5B, bottom: 3B). Error bars show within-problem                                          (Table 2). Cost estimates have tight 95% CIs—the 10-test
standard deviation across subset selections.                                                             baseline costs $0.69 (CI: $0.68–$0.70)—indicating through-
                                                                                                         put variance contributes negligibly to cost uncertainty com-
                                                                                                         pared to provider choice. Staged verification is 12–22×
filtering benefit is not be an artifact of test ordering, but a                                          cheaper than full test-suite verification while recovering
generalizable property of LLM bug distributions.                                                         most of its accuracy, making it the Pareto-optimal choice
                                                                                                         for budget-constrained verification.
Our error bars show within-problem standard deviations
across five random subsets. For FPR, this is 3.3 and 3.1 per-
centage points (1.5B/3B) at k = 1, and 4.8 and 4.0 points                                                5. Related Work
at k = 10, corresponding to 95% confidence intervals of
                                                                                                         Verification cost in code generation. Execution-based
roughly ±4–6 points. This suggests more efficient test-suite
                                                                                                         evaluation is now standard in code benchmarks, from unit-
verification techniques than running a full test suite on all
                                                                                                         test style tasks such as HumanEval and MBPP to larger
candidates—e.g. filtering with a small random subset of
                                                                                                         suites such as APPS (Chen et al., 2021; Austin et al., 2021;
tests and running the full suite on the candidates that survive
                                                                                                         Hendrycks et al., 2021). More recently, repository-scale
the filter—which we leave as a promising future direction.

                                                                                                     7
                                                     Pareto Optimal Code Generation


        20 7B                                                           et al., 2023), and in work that reduces patch-validation cost
                                                                        or expensive test execution via prioritization and test selec-
        15                                                              tion (Benton et al., 2022; Chen & Zhang, 2020; Lou et al.,
Bof64


                                                                        2021; Yuan et al., 2022). Similar cost–accuracy trade-offs
        10                                                              also appear in multi-stage code generation systems that use
                                                                        cascades or budgeted selection (Chen et al., 2024; Ehrlich
         5                                                              et al., 2025). Our focus is on how combining lightweight
                                                                        execution filters with neural ranking shifts and optimizes
        30 14B                                                          the accuracy–throughput Pareto frontier.

        20                                                              6. Conclusion
Bof64




                                                                        Progress in verification for test-time scaling should be
        10
                                                                        measured by Pareto improvement: moving the accuracy–
                                                                        throughput frontier outward. Our results show that the
         10 3        10 2      10 1            100      101             most consistent Pareto gains come from a simple staged
                 Cost per 100k programs (USD, log scale)                verification pipeline of cheap filtering followed by ORM
                 Non-staged           1-Test         10-Test            ranking—which achieves 11.64× higher throughput with
                                                                        8.26% lower accuracy than full test-suite verification. The
Figure 5. Cost-accuracy Pareto frontier for Qwen 2.5 Coder              need for the filter comes from a recurring ORM error mode:
Instruct models on CodeContests. Top: 7B; bottom: 14B. Lines            ORMs over-score near-miss programs whose tokens look
show Pareto curves for non-staged, 1-test, and 10-test. Costs are
per 100k programs (log scale).                                          right but fail on basic runtime semantics, such as division
                                                                        operator slips and mutation during iteration, placing filtered
                                                                        failures about 31 ranks too high on average. Future work
                                                                        should target this failure mode directly and test whether the
settings such as SWE-Bench require environment setup and                same frontier shifts appear when verification is dominated
running a test suite per candidate, making verification a               by much more substantial repository-scale overhead.
dominant cost in test-time scaling (Jimenez et al., 2024; Li
et al., 2024; Miserendino et al., 2025; Orlanski et al., 2025).
                                                                        Limitations. While our motivation includes repository-
Learned verifiers for selection. Reward models, popu-
                                                                        scale verification such as SWE-Bench, our experiments
larized by RLHF, are widely used for test-time selection
                                                                        focus on single-file Python benchmarks. We therefore do not
(ORMs) and step-level evaluation (PRMs), and recent work
                                                                        measure costs that can dominate end-to-end verification at
also studies generative verification via LLM reasoning (Sti-
                                                                        much larger scales, including container startup, dependency
ennon et al., 2020; Ouyang et al., 2022; Lightman et al.,
                                                                        installation, and integration testing; we leave the evaluation
2023; Wang et al., 2024; Zhang et al., 2024). The closest
                                                                        of staged verification in such settings to future work.
work to ours is Singhi et al. (2025), which studies when to
sample more versus verify with an LLM; in contrast, we                  Our generators and ORMs also share a common model
map the accuracy–throughput frontier for code verification              family—Qwen—which may bias results. As additional
and study how execution filters and ORMs interact.                      powerful open weights models are released, the effects of
                                                                        varying the choice model family should be evaluated in
Ranking programs. A substantial line of work studies
                                                                        future work. Additionally, results may differ under larger
how to rank or rerank generated code candidates using ex-
                                                                        distribution shifts across languages, domains, or other as-
ecution signals, learned rankers, or auxiliary LLM-based
                                                                        pects of the training pipeline. The dollar-cost analysis in
reviewers (Inala et al., 2022; Ni et al., 2023; Sun et al., 2024;
                                                                        Table 7 depends on specific hardware and cloud pricing
Zhang et al., 2022; Zhong et al., 2024). Compared to these
                                                                        assumptions; while these affect absolute costs, the empirical
works, we emphasize the compute dimension by reporting
                                                                        accuracy–throughput frontier is measured directly.
accuracy and throughput across verifiers, and analyze how
lightweight execution filters complement neural rankers.
                                                                        Impact Statement
Staged filtering and budgeted verification. Staging
verification—using cheap checks to reduce the number of                 Staged verification reduces compute costs for large-scale
candidates that reach more expensive validation—is com-                 code generation by pruning incorrect candidates before ex-
mon in software engineering workflows. Related ideas ap-                pensive validation. However, treating lightweight filters as a
pear in automated program repair, where many candidate                  substitute for thorough testing could increase the risk of de-
patches are generated and validated against test suites (Jiang          ploying incorrect or insecure code, and lowering verification

                                                                    8
                                               Pareto Optimal Code Generation

costs may amplify harmful uses of high-volume generation.            Chen, L. and Zhang, L. Fast and precise on-the-fly patch val-
We emphasize that staged verification is a selection tool, not         idation for all. 2021 IEEE/ACM 43rd International Con-
a replacement for full test suites. Sandboxed execution and            ference on Software Engineering (ICSE), pp. 1123–1134,
human review remain essential before deployment.                       2020. URL https://api.semanticscholar.
                                                                       org/CorpusID:220687000.
References                                                           Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O.,
Allal, L. B., Muennighoff, N., Kumar Umapathi,                         Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brock-
  L. K., Lipkin, B., and von Werra, L.         bigcode-                man, G., Ray, A., Puri, R., Krueger, G., Petrov, M.,
  project/bigcode-evaluation-harness, April 2025. URL                  Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S.,
  https://github.com/bigcode-project/                                  Ryder, N., Pavlov, M., Power, A., Kaiser, L., Bavarian,
  bigcode-evaluation-harness. original-date:                           M., Winter, C., Tillet, P., Such, F. P., Cummings, D.,
  2022-08-09T12:58:56Z.                                                Plappert, M., Chantzis, F., Barnes, E., Herbert-Voss, A.,
                                                                       Guss, W. H., Nichol, A., Paino, A., Tezak, N., Tang,
Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,                J., Babuschkin, I., Balaji, S., Jain, S., Saunders, W.,
  H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q.,                Hesse, C., Carr, A. N., Leike, J., Achiam, J., Misra,
  and Sutton, C. Program Synthesis with Large Language                 V., Morikawa, E., Radford, A., Knight, M., Brundage,
  Models, August 2021. URL http://arxiv.org/                           M., Murati, M., Mayer, K., Welinder, P., McGrew, B.,
  abs/2108.07732. arXiv:2108.07732 [cs].                               Amodei, D., McCandlish, S., Sutskever, I., and Zaremba,
                                                                       W. Evaluating Large Language Models Trained on Code,
Benton, S., Xie, Y., Lu, L., Zhang, M., Li, X., and                    July 2021. URL http://arxiv.org/abs/2107.
  Zhang, L. Towards boosting patch execution on-the-                   03374. arXiv:2107.03374 [cs].
  fly. In Proceedings of the 44th International Confer-
                                                                     Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun,
  ence on Software Engineering, ICSE ’22, pp. 2165–2176,
                                                                       H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J.,
  New York, NY, USA, 2022. Association for Comput-
                                                                       Nakano, R., Hesse, C., and Schulman, J. Train-
  ing Machinery. ISBN 9781450392211. doi: 10.1145/
                                                                       ing Verifiers to Solve Math Word Problems, Novem-
  3510003.3510117. URL https://doi.org/10.
                                                                       ber 2021. URL http://arxiv.org/abs/2110.
  1145/3510003.3510117.
                                                                       14168. arXiv:2110.14168 [cs].
Bradley, R. A. and Terry, M. E. Rank Analysis of Incom-              Dao, T. FlashAttention-2: Faster Attention with Better Paral-
  plete Block Designs: I. The Method of Paired Com-                    lelism and Work Partitioning, July 2023. URL http://
  parisons. Biometrika, 39(3/4):324–345, 1952. ISSN                    arxiv.org/abs/2307.08691. arXiv:2307.08691
  0006-3444. doi: 10.2307/2334029. URL https:                          [cs].
  //www.jstor.org/stable/2334029. Publisher:
  [Oxford University Press, Biometrika Trust].                       DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J.,
                                                                       Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X.,
Cassano, F., Gouwar, J., Nguyen, D., Nguyen, S., Phipps-               Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z.,
  Costin, L., Pinckney, D., Yee, M.-H., Zi, Y., Ander-                 Li, Z., Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B., Feng,
  son, C. J., Feldman, M. Q., Guha, A., Greenberg, M.,                 B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai,
  and Jangda, A. MultiPL-E: A Scalable and Extensi-                    D., Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo, F., Hao,
  ble Approach to Benchmarking Neural Code Generation,                 G., Chen, G., Li, G., Zhang, H., Bao, H., Xu, H., Wang,
  December 2022. URL http://arxiv.org/abs/                             H., Ding, H., Xin, H., Gao, H., Qu, H., Li, H., Guo, J.,
  2208.08227. arXiv:2208.08227 [cs].                                   Li, J., Wang, J., Chen, J., Yuan, J., Qiu, J., Li, J., Cai,
                                                                       J. L., Ni, J., Liang, J., Chen, J., Dong, K., Hu, K., Gao,
Center for High Throughput Computing. Center for high                  K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L.,
  throughput computing, 2006. URL https://chtc.                        Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang,
  cs.wisc.edu/.                                                        M., Zhang, M., Tang, M., Li, M., Wang, M., Li, M., Tian,
                                                                       N., Huang, P., Zhang, P., Wang, Q., Chen, Q., Du, Q., Ge,
Chen, B., Zhu, M., Dolan-Gavitt, B., Shafique, M., and                 R., Zhang, R., Pan, R., Wang, R., Chen, R. J., Jin, R. L.,
  Garg, S. Model cascading for code: A cascaded                        Chen, R., Lu, S., Zhou, S., Chen, S., Ye, S., Wang, S., Yu,
  black-box multi-model framework for cost-efficient code              S., Zhou, S., Pan, S., Li, S. S., Zhou, S., Wu, S., Ye, S.,
  completion with self-testing. 2025 International Joint              Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W., Zhao, W.,
  Conference on Neural Networks (IJCNN), pp. 1–9,                      Liu, W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao,
  2024. URL https://api.semanticscholar.                              W. L., An, W., Liu, X., Wang, X., Chen, X., Nie, X.,
  org/CorpusID:276394952.                                              Cheng, X., Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su,

                                                                 9
                                             Pareto Optimal Code Generation

  X., Lin, X., Li, X. Q., Jin, X., Shen, X., Chen, X., Sun,          and Lin, J. Qwen2.5-Coder Technical Report, Novem-
  X., Wang, X., Song, X., Zhou, X., Wang, X., Shan, X.,              ber 2024. URL http://arxiv.org/abs/2409.
  Li, Y. K., Wang, Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li,         12186. arXiv:2409.12186 [cs].
  Y., Zhao, Y., Sun, Y., Wang, Y., Yu, Y., Zhang, Y., Shi,
  Y., Xiong, Y., He, Y., Piao, Y., Wang, Y., Tan, Y., Ma,          Inala, J. P., Wang, C., Yang, M., Codas, A., Encarnación, M.,
  Y., Liu, Y., Guo, Y., Ou, Y., Wang, Y., Gong, Y., Zou,             Lahiri, S. K., Musuvathi, M., and Gao, J. Fault-Aware
  Y., He, Y., Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y.,        Neural Code Rankers. October 2022. URL https:
  Zhu, Y. X., Xu, Y., Huang, Y., Li, Y., Zheng, Y., Zhu,             //openreview.net/forum?id=LtJMqnbslJe.
  Y., Ma, Y., Tang, Y., Zha, Y., Yan, Y., Ren, Z. Z., Ren,         Jain, N., Han, K., Gu, A., Li, W.-D., Yan, F., Zhang,
  Z., Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang, Z., Hao, Z.,          T., Wang, S., Solar-Lezama, A., Sen, K., and Sto-
  Ma, Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu, Z., Li, Z.,          ica, I. LiveCodeBench: Holistic and Contamination
  Xie, Z., Song, Z., Pan, Z., Huang, Z., Xu, Z., Zhang, Z.,           Free Evaluation of Large Language Models for Code,
  and Zhang, Z. DeepSeek-R1: Incentivizing Reasoning                 June 2024. URL http://arxiv.org/abs/2403.
  Capability in LLMs via Reinforcement Learning, Jan-                 07974. arXiv:2403.07974 [cs].
  uary 2025. URL http://arxiv.org/abs/2501.
  12948. arXiv:2501.12948 [cs].                                    Jiang, N., Lutellier, T., Lou, Y., Tan, L., Gold-
                                                                      wasser, D., and Zhang, X. Knod: Domain knowl-
Ehrlich, R., Brown, B., Juravsky, J., Clark, R., Ré,                 edge distilled tree decoder for automated program re-
  C., and Mirhoseini, A.     CodeMonkeys: Scaling                     pair. 2023 IEEE/ACM 45th International Confer-
  Test-Time Compute for Software Engineering, Febru-                  ence on Software Engineering (ICSE), pp. 1251–1263,
  ary 2025. URL http://arxiv.org/abs/2501.                            2023. URL https://api.semanticscholar.
  14723. arXiv:2501.14723 [cs].                                       org/CorpusID:256598113.
Frantar, E., Ashkboos, S., Hoefler, T., and Alis-                  Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K.,
  tarh, D. GPTQ: Accurate Post-Training Quantiza-                    Press, O., and Narasimhan, K. SWE-bench: Can
  tion for Generative Pre-trained Transformers, March                Language Models Resolve Real-World GitHub Issues?,
  2023.     URL http://arxiv.org/abs/2210.                           April 2024. URL http://arxiv.org/abs/2310.
  17323. arXiv:2210.17323 [cs].                                      06770. arXiv:2310.06770 [cs].
Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P.,                  Kingma, D. P. and Ba, J. Adam: A Method for Stochastic
 Yang, Y., Callan, J., and Neubig, G. PAL: Program-                  Optimization, January 2017. URL http://arxiv.
  aided Language Models.      ArXiv, abs/2211.10435,                 org/abs/1412.6980. arXiv:1412.6980 [cs].
  2022. URL https://api.semanticscholar.
  org/CorpusID:253708270.                                          Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L.,
                                                                    Yu, C. H., Gonzalez, J. E., Zhang, H., and Stoica,
Hendrycks, D., Basart, S., Kadavath, S., Mazeika, M.,               I. Efficient Memory Management for Large Lan-
  Arora, A., Guo, E., Burns, C., Puranik, S., He, H.,               guage Model Serving with PagedAttention, Septem-
  Song, D. X., and Steinhardt, J. Measuring Coding Chal-            ber 2023. URL http://arxiv.org/abs/2309.
  lenge Competence With APPS. ArXiv, abs/2105.09938,                06180. arXiv:2309.06180 [cs].
  2021. URL https://api.semanticscholar.
  org/CorpusID:234790100.                                          Lambert, N., Morrison, J., Pyatkin, V., Huang, S., Ivison,
                                                                     H., Brahman, F., Miranda, L. J. V., Liu, A., Dziri, N.,
Holtzman, A., Buys, J., Du, L., Forbes, M., and Choi, Y.             Lyu, S., Gu, Y., Malik, S., Graf, V., Hwang, J. D., Yang,
 The Curious Case of Neural Text Degeneration, Febru-                J., Bras, R. L., Tafjord, O., Wilhelm, C., Soldaini, L.,
  ary 2020. URL http://arxiv.org/abs/1904.                           Smith, N. A., Wang, Y., Dasigi, P., and Hajishirzi, H.
  09751. arXiv:1904.09751 [cs].                                      Tulu 3: Pushing Frontiers in Open Language Model Post-
                                                                     Training, February 2025. URL http://arxiv.org/
Hosseini, A., Yuan, X., Malkin, N., Courville, A., Sordoni,          abs/2411.15124. arXiv:2411.15124 [cs].
 A., and Agarwal, R. V-STaR: Training Verifiers for Self-
 Taught Reasoners, August 2024. URL http://arxiv.                  Lhoest, Q., Moral, A. V. d., Jernite, Y., Thakur, A., Platen,
  org/abs/2402.06457. arXiv:2402.06457 [cs].                         P. v., Patil, S., Chaumond, J., Drame, M., Plu, J., Tunstall,
                                                                     L., Davison, J., Šaško, M., Chhablani, G., Malik, B.,
Hui, B., Yang, J., Cui, Z., Yang, J., Liu, D., Zhang, L.,            Brandeis, S., Scao, T. L., Sanh, V., Xu, C., Patry, N.,
  Liu, T., Zhang, J., Yu, B., Lu, K., Dang, K., Fan, Y.,             McMillan-Major, A., Schmid, P., Gugger, S., Delangue,
  Zhang, Y., Yang, A., Men, R., Huang, F., Zheng, B.,                C., Matussière, T., Debut, L., Bekman, S., Cistac, P.,
  Miao, Y., Quan, S., Feng, Y., Ren, X., Ren, X., Zhou, J.,          Goehringer, T., Mustar, V., Lagunas, F., Rush, A. M., and

                                                              10
                                             Pareto Optimal Code Generation

  Wolf, T. Datasets: A Community Library for Natural                Muennighoff, N., Yang, Z., Shi, W., Li, X. L., Fei-Fei, L.,
  Language Processing, September 2021. URL http://                   Hajishirzi, H., Zettlemoyer, L., Liang, P., Candès, E.,
  arxiv.org/abs/2109.02846. arXiv:2109.02846                         and Hashimoto, T. s1: Simple test-time scaling, Febru-
  [cs].                                                              ary 2025. URL http://arxiv.org/abs/2501.
                                                                     19393. arXiv:2501.19393 [cs].
Li, J., Li, G., Zhao, Y., Li, Y., Liu, H., Zhu, H., Wang, L.,
  Liu, K., Fang, Z., Wang, L., Ding, J., Zhang, X., Zhu,            Ni, A., Iyer, S., Radev, D., Stoyanov, V., Yih, W.-t.,
  Y., Dong, Y., Jin, Z., Li, B., Huang, F., and Li, Y. Deve-          Wang, S. I., and Lin, X. V. LEVER: Learning to Verify
  val: A manually-annotated code generation benchmark                 Language-to-Code Generation with Execution, Septem-
  aligned with real-world code repositories. In Annual                ber 2023. URL http://arxiv.org/abs/2302.
  Meeting of the Association for Computational Linguistics,           08468. arXiv:2302.08468 [cs].
  2024. URL https://api.semanticscholar.
  org/CorpusID:270123562.                                           Orlanski, G., Xiao, K., Garcia, X., Hui, J., Howland, J., Mal-
                                                                      maud, J., Austin, J., Singh, R., and Catasta, M. Measur-
Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser,              ing The Impact Of Programming Language Distribution,
  J., Leblond, R., Eccles, T., Keeling, J., Gimeno, F.,               May 2023. URL http://arxiv.org/abs/2302.
  Lago, A. D., Hubert, T., Choy, P., d’Autume, C. d. M.,              01973. arXiv:2302.01973 [cs].
  Babuschkin, I., Chen, X., Huang, P.-S., Welbl, J., Gowal,
  S., Cherepanov, A., Molloy, J., Mankowitz, D. J., Rob-            Orlanski, G., Roy, D., Yun, A., Shin, C., Gu, A., Ge, A.,
  son, E. S., Kohli, P., Freitas, N. d., Kavukcuoglu, K.,             Adila, D., Albarghouthi, A., and Sala, F. SlopCodeBench:
  and Vinyals, O. Competition-Level Code Generation                   Measuring Code Erosion Under Iterative Specification
  with AlphaCode. Science, 378(6624):1092–1097, De-                   Refinement, December 2025. URL https://github.
  cember 2022. ISSN 0036-8075, 1095-9203. doi: 10.                    com/SprocketLab/slop-code-bench.
  1126/science.abq1158. URL http://arxiv.org/
  abs/2203.07814. arXiv:2203.07814 [cs].                            Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wain-
                                                                     wright, C. L., Mishkin, P., Zhang, C., Agarwal,
Lightman, H., Kosaraju, V., Burda, Y., Edwards, H.,                   S., Slama, K., Ray, A., Schulman, J., Hilton, J.,
  Baker, B., Lee, T., Leike, J., Schulman, J., Sutskever,             Kelton, F., Miller, L. E., Simens, M., Askell, A.,
  I., and Cobbe, K.        Let’s Verify Step by Step,                Welinder, P., Christiano, P. F., Leike, J., and Lowe,
  May 2023. URL http://arxiv.org/abs/2305.                            R. J. Training language models to follow instruc-
  20050. arXiv:2305.20050 [cs].                                       tions with human feedback. ArXiv, abs/2203.02155,
                                                                      2022. URL https://api.semanticscholar.
Liu, J., Xia, C. S., Wang, Y., and Zhang, L. Is Your Code
                                                                      org/CorpusID:246426909.
  Generated by ChatGPT Really Correct? Rigorous Eval-
  uation of Large Language Models for Code Generation,              Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang,
  June 2023. URL http://arxiv.org/abs/2305.                           S., Matena, M., Zhou, Y., Li, W., and Liu, P. J. Ex-
  01210. arXiv:2305.01210 [cs].                                       ploring the limits of transfer learning with a unified
Liu, J., Xie, S., Wang, J., Wei, Y., Ding, Y., and Zhang, L.          text-to-text transformer. Journal of Machine Learning
  Evaluating Language Models for Efficient Code Genera-               Research, 21(140):1–67, 2020. URL http://jmlr.
  tion, August 2024. URL http://arxiv.org/abs/                        org/papers/v21/20-074.html.
  2408.06450. arXiv:2408.06450 [cs].
                                                                    Singhi, N., Bansal, H., Hosseini, A., Grover, A.,
Lou, Y., Yang, J., Benton, S., Hao, D., Tan, L., Chen,                Chang, K.-W., Rohrbach, M., and Rohrbach, A.
  Z., Zhang, L., and Zhang, L. When automated pro-                    When To Solve, When To Verify: Compute-Optimal
  gram repair meets regression testing—an extensive                   Problem Solving and Generative Verification for
  study on two million patches. ACM Transactions on                   LLM Reasoning.     April 2025.    URL https:
  Software Engineering and Methodology, 33:1 – 23,                    //www.semanticscholar.org/paper/
  2021. URL https://api.semanticscholar.                              When-To-Solve%2C-When-To-Verify%
  org/CorpusID:234742364.                                             3A-Compute-Optimal-and-Singhi-Bansal/
                                                                      d170e69de7519e926bee6af648c9ffd625689600.
Miserendino, S., Wang, M., Patwardhan, T., and Hei-
 decke, J. Swe-lancer: Can frontier llms earn $1                    Snell, C., Lee, J., Xu, K., and Kumar, A. Scaling LLM Test-
 million from real-world freelance software engineer-                 Time Compute Optimally can be More Effective than
 ing? ArXiv, abs/2502.12115, 2025. URL https:                         Scaling Model Parameters, August 2024. URL http://
 //api.semanticscholar.org/CorpusID:                                  arxiv.org/abs/2408.03314. arXiv:2408.03314
 276421817.                                                           [cs].

                                                               11
                                             Pareto Optimal Code Generation

Stiennon, N., Ouyang, L., Wu, J., Ziegler, D., Lowe,             for Code Generation, November 2022. URL http://
   R., Voss, C., Radford, A., Amodei, D., and Chris-             arxiv.org/abs/2211.16490. arXiv:2211.16490.
   tiano, P. F. Learning to summarize with human
   feedback. In Advances in Neural Information Processing      Zhong, L., Wang, Z., and Shang, J. Debug like a Hu-
  Systems, volume 33, pp. 3008–3021. Curran Asso-                man: A Large Language Model Debugger via Ver-
   ciates, Inc., 2020. URL https://proceedings.                  ifying Runtime Execution Step by Step. In Find-
   neurips.cc/paper/2020/hash/                                   ings of the Association for Computational Linguis-
  1f89885d556929e98d3ef9b86448f951-Abstract. tics ACL 2024, pp. 851–870, Bangkok, Thailand
   html.                                                         and virtual meeting, 2024. Association for Computa-
                                                                 tional Linguistics. doi: 10.18653/v1/2024.findings-acl.
Sun, Z., Wan, Y., Li, J., Zhang, H., Jin, Z., Li, G., and Lyu,   49. URL https://aclanthology.org/2024.
   C. Sifting through the Chaff: On Utilizing Execution          findings-acl.49.
   Feedback for Ranking the Generated Code Candidates.
   2024. doi: 10.48550/ARXIV.2408.13976. URL https:
  //arxiv.org/abs/2408.13976. Publisher: arXiv
  Version Number: 3.

Uesato, J., Kushman, N., Kumar, R., Song, F., Siegel, N.,
 Wang, L., Creswell, A., Irving, G., and Higgins, I. Solv-
  ing math word problems with process- and outcome-
  based feedback, 2022. URL https://arxiv.org/
  abs/2211.14275. Publisher: arXiv Version Number:
 1.

Wang, P., Li, L., Shao, Z., Xu, R. X., Dai, D., Li, Y.,
 Chen, D., Wu, Y., and Sui, Z. Math-Shepherd: Verify
 and Reinforce LLMs Step-by-step without Human Anno-
 tations, February 2024. URL http://arxiv.org/
 abs/2312.08935. arXiv:2312.08935 [cs].

Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue,
 C., Moi, A., Cistac, P., Rault, T., Louf, R., Funtowicz,
 M., Davison, J., Shleifer, S., Platen, P. v., Ma, C., Jer-
 nite, Y., Plu, J., Xu, C., Scao, T. L., Gugger, S., Drame,
 M., Lhoest, Q., and Rush, A. M. HuggingFace’s Trans-
 formers: State-of-the-art Natural Language Processing,
 July 2020. URL http://arxiv.org/abs/1910.
 03771. arXiv:1910.03771 [cs].

Yuan, W., Zhang, Q., He, T., Fang, C., Hung, N. Q. V.,
  Hao, X., and Yin, H. Circle: continual repair across
  programming languages. In Proceedings of the 31st
  ACM SIGSOFT International Symposium on Software
  Testing and Analysis, ISSTA 2022, pp. 678–690, New
  York, NY, USA, 2022. Association for Computing
  Machinery. ISBN 9781450393799. doi: 10.1145/
  3533767.3534219. URL https://doi.org/10.
  1145/3533767.3534219.

Zhang, L., Hosseini, A., Bansal, H., Kazemi, M., Kumar, A.,
  and Agarwal, R. Generative Verifiers: Reward Modeling
  as Next-Token Prediction, October 2024. URL http://
  arxiv.org/abs/2408.15240. arXiv:2408.15240.

Zhang, T., Yu, T., Hashimoto, T. B., Lewis, M., Yih, W.-t.,
  Fried, D., and Wang, S. I. Coder Reviewer Reranking

                                                              12
                                                      Pareto Optimal Code Generation

A. Training Details Continued
Table 4. Details of our training datasets. “# Probs” is the number of problems in the dataset. “Prob. Tok” is the average number of tokens
in the problem description. “Tokens” is the average number of tokens in the problem and solutions when formatted with the prompt.
“Sols.” is the average number of unique non-syntax error solutions per problem. “# Passed” is the mean number of passing solutions per
problem. “% Passed” is the percentage of problems that had at least one passing solution. “# Pairs” is the average number of possible
pairs per problem, where a pair is 1 correct and 1 incorrect solution.

              Dataset            Split      # Probs    Prob. Tok    Tokens       Sols.    # Passed     % Passed      # Pairs
                                 Train      13,213        776.76     508.08    124.78        14.00         35.92       6.58
              CodeContests
                                 Val           117        921.66     625.66    126.31         4.36         23.08       3.61
                                 Train       7,373        160.16      59.55     83.50        67.03         98.87       9.26
              GSM8K
                                 Val           100        177.42      66.63    105.93        78.66        100.00      15.16


A.1. Hyperparameters
We use The Transformers Library (Wolf et al., 2020) with Hugging Face Datasets (Lhoest et al., 2021) for training our
models. We use FlashAttention 2.0 (Dao, 2023) and BFloat16 precision. We use the Adam optimizer (Kingma & Ba, 2017)
with β1 = 0.9, β2 = 0.999, ϵ = 1e − 8. We use a cosine learning rate schedule that peaks at 5e − 6 and 10% warmup steps.
We use a batch size of 64 with a maximum sequence length of 2048. We employ gradient checkpointing and accumulation
to be able to train our models on a single A6000 GPU. We train the ORM for 2 epochs on our dataset and use the last
checkpoint for evaluation. We train each setup six times across six random seeds (1, 1999, 2000, 2021, 2024, 2042) and
report the mean results.
To create our training data we first apply Black formatting to the generated code as mentioned in section 3. We then filter
out any programs with syntax errors and problems which do not have at least 1 correct and 1 incorrect solution. Then
we randomly sample at most six examples per problem. For our pairwise objectives this means we sample a total of 12
programs per problem. We use the CodeContests validation set along with 100 randomly sampled problems from the
GSM8K validation set to create our validation data.

B. Example Problem
                                         Listing 1. Example Problem Description From CodeContests
     1   A s t r i n g i s c a l l e d s q u a r e i f i t i s some s t r i n g w r i t t e n t w i c e i n a row .
             F o r example , t h e s t r i n g s ” a a ” , ” a b c a b c ” , ” a b a b ” and ” b a a b a a ” a r e
              s q u a r e . But t h e s t r i n g s ” a a a ” , ” a b a a a b ” and ” a b c d a b c ” a r e n o t s q u a r e .
     2
     3   For a given s t r i n g s d e t e r m i n e i f           i t is square .
     4
     5   Input
     6

     7   The f i r s t l i n e o f i n p u t d a t a c o n t a i n s an i n t e g e r t ( 1 <= t <= 1 0 0 ) − t h e
            number o f t e s t c a s e s .
     8
     9   T h i s i s f o l l o w e d by t l i n e s , e a c h c o n t a i n i n g a d e s c r i p t i o n o f one t e s t
                c a s e . The g i v e n s t r i n g s c o n s i s t o n l y o f l o w e r c a s e L a t i n l e t t e r s and
                h a v e l e n g t h s b e t w e e n 1 and 100 i n c l u s i v e .
    10
    11   Output
    12
    13   F o r e a c h t e s t c a s e , o u t p u t on a s e p a r a t e l i n e :
    14
    15         * YES i f t h e s t r i n g i n t h e c o r r e s p o n d i n g t e s t c a s e i s s q u a r e ,
    16         * NO o t h e r w i s e .
    17



                                                                    13
                                          Pareto Optimal Code Generation

18

19
20   You c a n o u t p u t YES and NO i n any c a s e ( f o r example , s t r i n g s yEs , yes , Yes
         and YES w i l l be r e c o g n i z e d a s a p o s i t i v e r e s p o n s e ) .
21
22   Example
23

24   Input
25
26
27 10
28 a
29 a a

30 a a a
31 a a a a
32 a b a b
33 a b c a b c
34 a b a c a b a
35 xxyy

36 xyyx
37 xyxy
38
39
40   Output
41

42
43 NO
44 YES
45 NO
46 YES
47 YES

48 YES
49 NO
50 NO
51 NO
52 YES



                                          Listing 2. Example Correct Solution
 1   import sys
 2

 3 # Read i n p u t from s t d i n
 4 input = sys . s t d i n . read
 5 data = input () . s p l i t ()
 6
 7   # The f i r s t e l e m e n t i s t h e number o f t e s t c a s e s
 8   t = int ( data [0])
 9
10 # I t e r a t e over each t e s t case
11 f o r i in range (1 , t + 1) :
12       s = data [ i ]
13       length = len ( s )
14       # Check i f t h e l e n g t h o f t h e s t r i n g i s e v e n
15       i f l e n g t h % 2 == 0 :
16               half = length / / 2

                                                          14
                                                 Pareto Optimal Code Generation

17             # Check i f t h e f i r s t h a l f i s e q u a l t o t h e s e c o n d h a l f
18             i f s [ : h a l f ] == s [ h a l f : ] :
19                     p r i n t ( ”YES” , end =” \ n ” )
20             else :
21                     p r i n t ( ”NO” , end =” \ n ” )
22        else :
23             p r i n t ( ”NO” , end =” \ n ” )

                                             Listing 3. Example Incorrect Solution
 1   import sys
 2
 3
 4 def i s s q u a r e ( s ) :
 5     n = len ( s )
 6     fo r i in range (1 , n / / 2 + 1) :
 7              i f n % i == 0 :
 8                   prefix = s [: i ]
 9                   i f p r e f i x * ( n / / i ) == s :
10                           r e t u r n ”YES”
11     r e t u r n ”NO”
12
13

14 d e f main ( ) :
15       input = sys . s t d i n . read
16       data = input () . s p l i t ()
17       t = int ( data [0])
18       results = []
19       fo r i in range (1 , t + 1) :
20            r e s u l t s . append ( i s s q u a r e ( d a t a [ i ] ) )
21       for r e s u l t in r e s u l t s :
22            print ( result )
23
24
25   if    name        == ”      main       ”:
26        main ( )




                                                               15
                                                  Pareto Optimal Code Generation

C. Bug Pattern Examples
Examples of each bug pattern from Table 3. All examples are from solutions ranked in the ORM’s top-16 but filtered by VS1 .

C.1. Float Division in Binary Search
Using / instead of // produces floats that cause TypeError on indexing or silent truncation bugs. A single character
difference.

                                           Listing 4. Wrong: float division (ORM Rank 2)
    1 while r i g h t − l e f t > 1e −9:
    2     mid = ( l e f t + r i g h t ) / 2 # Bug : r e t u r n s f l o a t 5 . 5 , n o t i n t 5
    3     i f c h e c k ( k , mid , p o i n t s ) :
    4           r i g h t = mid
    5     else :
    6           l e f t = mid

                                                  Listing 5. Correct: integer division
    1 w h i l e l e f t <= r i g h t :
    2         mid = ( l e f t + r i g h t ) / / 2         # Returns i n t 5
    3         i f c h e c k ( k , mid , p o i n t s ) :
    4               r i g h t = mid − 1
    5         else :
    6               l e f t = mid + 1


C.2. Int Cast of Float Division
Using int(x/y) instead of x//y. Appears correct but int() truncates toward zero while // floors, giving different
results for negative numbers.

                                        Listing 6. Wrong: int of float division (ORM Rank 3)
    1 prefix = [1]
    2 for x , y in zip ( a , b ) :
    3     i f y == ” * ” :
    4          p r e f i x . append ( p r e f i x [ −1] * x )
    5     else :
    6          p r e f i x . append ( i n t ( p r e f i x [ −1] / x ) )          # Bug : i n t ( − 3 / 2 ) = −1 , −3//2= −2

                                                   Listing 7. Correct: floor division
    1               p r e f i x . append ( p r e f i x [ −1] / / x )      # Correct floor division


C.3. Large Integer Arithmetic
Operations on large integers that lose precision or overflow intermediate values. Common in competitive programming
where results require modular arithmetic.

                                       Listing 8. Wrong: intermediate overflow (ORM Rank 3)
    1 def c o u n t p a t h s ( n , edges ) :
    2     MOD = 10 ** 9 + 7
    3     # Bug : a * b o v e r f l o w s b e f o r e modulo on some p a t h s
    4     r e s u l t = a * b * c % MOD # I n t e r m e d i a t e a * b * c e x c e e d s i n t p r e c i s i o n
    5     return result


                                                                  16
                                               Pareto Optimal Code Generation

                                              Listing 9. Correct: modulo at each step
   1 def c o u n t p a t h s ( n , edges ) :
   2     MOD = 10 ** 9 + 7
   3     r e s u l t = a * b % MOD
   4     r e s u l t = r e s u l t * c % MOD            # Keep i n t e r m e d i a t e v a l u e s bounded
   5     return result


C.4. Remove in Loop
Calling .remove() inside a loop modifies the collection while iterating, causing skipped elements or ValueError.

                                 Listing 10. Wrong: modifying set while iterating (ORM Rank 4)
   1 for i in range (1 , n ) :
   2     i f ( u , i ) i n E and ( v , i ) n o t i n E :
   3           T = min ( T , f ( u , i , t + 1 ) )
   4           E . remove ( ( u , i ) ) # Bug : m o d i f i e s E d u r i n g i t e r a t i o n
   5           E . remove ( ( v , i ) )
   6           E . add ( ( u , v ) )

                                             Listing 11. Correct: collect then remove
   1 to remove = [ ]
   2 for i in range (1 , n ) :
   3      i f ( u , i ) i n E and ( v , i ) n o t i n E :
   4             T = min ( T , f ( u , i , t + 1 ) )
   5             to remove . append ( ( ( u , i ) , ( v , i ) ) )
   6 for  p a i r in to remove :
   7      E. discard ( pair [0])
   8      E. discard ( pair [1])


C.5. While Len Condition
Using while len(x) > 0 instead of while x. Verbose and often indicates confused reasoning about the loop
invariant.

                                     Listing 12. Wrong: verbose length check (ORM Rank 5)
   1 while len ( h a b i t a t s ) > 0: # Unidiomatic
   2     i f i s i n s i d e ( ( center , radius ) , h a b i t a t s [ −1]) :
   3           h a b i t a t s . pop ( )
   4     else :
   5           r a d i u s += d i s t ( ( c e n t e r , r a d i u s ) , h a b i t a t s [ − 1 ] )
   6           # Bug : i n f i n i t e l o o p i f h a b i t a t c a n ’ t be c o v e r e d

                                      Listing 13. Correct: idiomatic check with termination
   1 while h a b i t a t s :
   2     h a b i t a t = h a b i t a t s [ −1]
   3     i f i s i n s i d e (( center , radius ) , habitat ) :
   4             h a b i t a t s . pop ( )
   5     e l i f r a d i u s >= m a x r a d i u s :
   6            break # E x p l i c i t termination condition
   7     else :
   8             radius = compute new radius ( center , h a b i t a t )


                                                                17
                                                 Pareto Optimal Code Generation

D. Prompts Used
                                          Listing 14. Prompt used for training and inference
       1 # Question
       2 Tom and Tim b o t h b r o u g h t 4 , s i x − s i d e d d i c e t o s c h o o l .
       3 How many t o t a l sides are there ?
       4
      # Proposed S o l u t i o n
       5
      ‘ ‘ ‘ python
       6
    7 def    solution () :
    8        dice per person = 4
    9        sides per die = 6
   10        total dice = dice per person * 2
   11        total sides = total dice * sides per die
   12        result = total sides
   13        return result
   14

   15      ‘‘‘
   16      <| e n d o f t e x t |>


E. Execution Details Continued
HumanEval tests function completion where the model must write the correct function given a docstring and signature.
MBPP, on the other hand, tasks the model with synthesizing a function given a single sentence specification and a single
test case. Then we use the execution framework provided by EvalPlus that executes the program from inside of a Python
process. In both of these cases, the evaluation relies on assertions that call a specific entrypoint function. Thus, we use
EvalPlus sanitize method to extract all relevant code and comments using treesitter4 to parse the AST. This does come
with the caveat that it heavily perturbs the whitespace of the original code in unnatural ways. Thus we use the Black
formatter5 to format both our evaluation and training data. We run all of our trials on a cluster designed for high throughput
computing (Center for High Throughput Computing, 2006).

F. Data Generation Details
To generate our training data for our ORMs, we use the training splits of CodeContests-Python (Li et al., 2022) and
GSM8K (Cobbe et al., 2021) in Program-aided Language Models (PAL) format (Gao et al., 2022). The CodeContests dataset
is a collection of competitive programming problems from platforms such as CodeForces.6 Each program requires taking in
STDIN inputs and printing the results to STDOUT. Most, but not all, problems have a few private test cases. We follow the
LiveCodeBench (Jain et al., 2024) prompts and formatting for generation. For GSM8K, we opt for the PAL format as it
allows us to have more programming training data from a different domain. We additionally use the BigCodeEval (Allal
et al., 2025) in context examples for GSM8K. We use Qwen 2.5 Coder Instruct 7B (Hui et al., 2024) with Int8 GPTQ
quantization (Frantar et al., 2023) to generate our training data. We sample a maximum of 1024 tokens 128 times per
problem with a temperature of T = 1.0 and top-p of 0.95. We use the VLLM (Kwon et al., 2023) library to generate our
data. Full details of our training data are found in Appendix A.

G. All result tables




   4
     https://github.com/tree-sitter/tree-sitter
   5
     https://github.com/psf/black
   6
     https://codeforces.com/

                                                                 18
                                                    Pareto Optimal Code Generation




Table 5. Breakdown of evaluation data. πG is the generator size, T is the temperature, and DS is the dataset. Prob Pass is the percentage of
problems where at least one solution passes at least one test. % Pass is the mean fraction of tests passed per solution. Net Sols is the total
number of solutions. Prob. Tok and Tok. are the average token counts for problem statements and solutions. # Pass is the average number
of fully correct solutions (passing all tests) per problem. Avg. Sols is the average number of solutions per problem.

  πG          T       DS             Prob Pass        % Pass        Net Sols       Prob. Tok          Tok.       # Pass       Avg. Sols
                      CC                68.48           2.75         21,014          620.74         878.31         0.04         127.36
                      GSM8K             80.36          18.75        151,608           71.31         155.68        18.31         114.94
  500M        1.0
                      HE               100.00          41.99        16,444           144.22         359.51        33.98         100.27
                      MBPP              95.77          40.42         40,187           60.51         156.05        39.50         106.31
                      CC                78.18           6.03         20,932          620.74         868.14         0.13         126.86
                      GSM8K             95.00          50.33        135,144           71.31         160.51        45.92         102.46
  1.5B        1.0
                      HE               100.00          57.90        16,643           144.22         320.82        51.06         101.48
                      MBPP              98.41          54.72         41,018           60.51         132.90        53.15         108.51
                      CC                88.48           9.83         21,108          620.74         921.48         0.47         127.93
                      GSM8K             97.80          66.16        129,375           71.31         163.22        59.09          98.09
  3B          1.0
                      HE               100.00          75.27        14,935           144.22         336.42        63.43         91.07
                      MBPP              99.47          58.99         44,896           60.51         138.26        65.64         118.77
                      CC                84.24          14.54         11,905          620.74         902.13         0.21          72.15
                      GSM8K             91.66          82.20         14,135           71.31         162.98         7.10          10.72
              0.2
                      HE                99.39          86.09         2,643           144.22         323.89        12.14          16.12
                      MBPP              96.83          72.24         10,281           60.51         144.11        14.60          27.20
                      CC                88.48          14.92         18,331          620.74         895.37         0.32         111.10
                      GSM8K             95.68          82.11         40,932           71.31         163.93        21.26          31.03
              0.4
                      HE                99.39          83.88         7,071           144.22         324.28        33.40          43.12
                      MBPP              97.88          71.08         24,167           60.51         144.51        37.24          63.93
                      CC                90.30          14.80         20,300          620.74         892.90         0.42         123.03
                      GSM8K             96.89          81.23         69,711           71.31         164.16        37.52          52.85
  7B          0.6
                      HE                99.39          83.23         11,127          144.22         319.59        52.44          67.85
                      MBPP              98.94          69.65         34,328           60.51         144.02        55.72          90.81
                      CC                93.33          14.47         20,834          620.74         893.17         0.38         126.27
                      GSM8K             97.88          80.62         94,225           71.31         164.30        52.23          71.44
              0.8
                      HE                99.39          81.76         14,241          144.22         315.55        67.17          86.84
                      MBPP              99.21          68.69         40,961           60.51         143.52        68.29         108.36
                      CC                92.12          14.11         21,022          620.74         897.16         0.32         127.41
                      GSM8K             98.56          79.44        114,882           71.31         165.06        64.48          87.10
              1.0
                      HE                99.39          80.98         16,625          144.22         310.11        78.46         101.37
                      MBPP              99.74          66.64         44,915           60.51         144.73        74.42         118.82
                      CC                92.73          18.76         19,852          620.74         988.10         0.10         120.32
                      GSM8K             98.94          87.69        129,548           71.31         170.84        83.86          98.22
  14B         1.0
                      HE               100.00          83.97        15,410           144.22         314.70        75.10         93.96
                      MBPP              98.94          70.23         24,411           60.51         142.26        38.29          64.58




                                                                     19
                                                   Pareto Optimal Code Generation




Table 6. Standard deviation of the results for the different pruning with a weak verifier then ranking methods. Green backgrounds is
higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—” that means no pruning
is done. Vall is the case where all test cases are run. “Syntax” and “Lint” remove any programs with the respective errors. “N Test” prunes
out any programs that do not pass the first N test cases. The evaluation dataset is generated with Qwen 2.5 Coder 7B Instruct using
T = 1.0, n = 128, topp = 0.95, and 1024 tokens. For the Non-ORM methods, there is no standard deviation for best-of-64 as the
ordering is the same

                                     CodeContests              GSM8K                 HumanEval                  MBPP
        Filter           Ranker     Bof64   PPS             Bof64  PPS              Bof64  PPS              Bof64  PPS
                         MV           —           —           —           —           —           —            —          —
        —                500M        0.74       14.45        0.99        71.70       1.05        37.57        1.06       76.28
                         1.5B        0.69        4.00        1.28        20.18       1.54        10.92        1.20       23.13
                         MV           —        399.40         —          445.70       —         517.91         —        742.06
        Syntax           500M        0.70       2.73         0.30        13.23       0.93        5.26         0.81      15.19
                         1.5B        0.76       1.76         0.43         8.23       1.80        4.19         0.83       9.72
                         MV           —         92.07         —           9.88        —           4.69         —          9.62
        Lint             500M        0.87       9.60         1.26        18.62       0.89        12.14        2.26       11.73
                         1.5B        0.82       2.75         1.98         7.56       1.41         5.02        1.74        7.12
                         MV           —          1.48         —           —           —         101.45         —        150.46
        1 Test           500M        0.34        0.28         —           —          1.03       27.92         1.42      48.73
                         1.5B        0.49        0.61         —           —          1.54        9.17         1.00      20.22
                         MV           —          2.27         —           —           —          54.43         —         44.48
        10 Tests         500M        0.15        0.01         —           —          0.76        0.27         0.39       0.03
                         1.5B        0.49        0.04         —           —          0.82        0.06         0.18       0.08
                  Vall                —          0.09         —          37.90         —         0.92          —          0.43




                                                                    20
                                                        Pareto Optimal Code Generation




       0.7
                        CodeContests                 1.3
                                                                    HumanEval                       1.2
                                                                                                                    MBPP
       0.5                                           0.9                                            0.8
Lint




       0.2                                           0.4                                            0.4
       0.0 0      25     50    75      100    125    0.0 20   40    60     80    100      120       0.0 0    25    50    75    100     125
            7                                           4                                            6
 1 Test




            4                                           3                                            4
            2                                           1                                            2
            0 0    25    50    75      100    125       0 0    25    50     75    100       125      0 0     25    50    75    100     125
            7                                           7                                            8
 10 Tests




            5                                           4                                            5
            2                                           2                                            2
            0 0    25    50    75      100    125       0 0    25    50     75    100       125      0 0     25    50    75    100     125
                  Rank of Programs Removed                    Rank of Programs Removed                      Rank of Programs Removed
Figure 6. Distribution of the failed candidates based on where Vθ had ranked them. A rank of 1 means the candidate was the top-ranked,
while 128 means it was the lowest-ranked. The rows are the individual verifiers while the columns are the datasets. This is for the 500M
Vθ .




Table 7. On-demand hourly prices for hardware-matched instances. Prices are Linux on-demand in AWS us-east-1, Azure eastus, and
GCP us-central1 (Jan 22, 2026).

                                             Provider     GPU (single ∼48GB)     CPU 64c/256GB
                                             AWS               $3.004/hr                $3.072/hr
                                             Azure             $3.673/hr                $3.072/hr
                                             GCP               $5.782/hr               $3.1078/hr




                                                                      21
                                                   Pareto Optimal Code Generation




Table 8. Information about the tokens filtered from the datasets by the 5 verifiers we look at on the 3B, 7B, and 14B models. The
percentage filtered is the percentage of tokens filtered from the dataset, the average sequence length is the average sequence length of the
tokens that were filtered, and the total tokens filtered is the total number of tokens filtered from the dataset.

                πG       V             DS             % Filtered       Avg. Seq Length          Total Tokens Filtered
                                       CC                    0.76                1,222.81                      1.89e+07
                                       GSM8K                 0.45                  201.33                      2.04e+07
                         Syntax
                                       HE                    0.00                  135.00                      5.47e+06
                                       MBPP                  0.00                   65.00                      6.63e+06
                                       CC                    5.36                1,131.51                      1.89e+07
                                       GSM8K                 1.33                  203.86                      2.04e+07
                         Lint
                                       HE                    1.00                  408.92                      5.47e+06
                                       MBPP                  1.05                  159.68                      6.63e+06
                7B                     CC                   88.90                  919.54                      1.89e+07
                         1 Test        HE                    8.44                  378.60                      5.47e+06
                                       MBPP                 22.88                  173.66                      6.63e+06
                                       CC                   92.85                  908.04                      1.89e+07
                         3 Tests       HE                   13.97                  364.37                      5.47e+06
                                       MBPP                 27.58                  170.55                      6.63e+06
                                       CC                   93.39                  906.89                      1.89e+07
                         10 Tests      HE                   18.84                  364.83                      5.47e+06
                                       MBPP                 37.92                  165.21                      6.63e+06
                                       CC                    4.87                1,610.94                      1.96e+07
                                       GSM8K                 0.16                  213.89                      2.35e+07
                         Syntax
                                       HE                    0.04                  130.29                      5.22e+06
                                       MBPP                  0.13                   61.49                      3.93e+06
                                       CC                    7.76                1,411.36                      1.96e+07
                                       GSM8K                 0.81                  216.55                      2.35e+07
                         Lint
                                       HE                    0.95                  315.97                      5.22e+06
                                       MBPP                  0.94                  135.12                      3.93e+06
                14B                    CC                   85.08                1,019.14                      1.96e+07
                         1 Test        HE                    5.99                  375.57                      5.22e+06
                                       MBPP                 21.93                  182.11                      3.93e+06
                                       CC                   89.01                1,005.72                      1.96e+07
                         3 Tests       HE                   11.18                  369.63                      5.22e+06
                                       MBPP                 26.60                  178.78                      3.93e+06
                                       CC                   89.95                1,003.10                      1.96e+07
                         10 Tests      HE                   15.53                  373.36                      5.22e+06
                                       MBPP                 38.54                  173.15                      3.93e+06




                                                                    22
                                                  Pareto Optimal Code Generation




Table 9. Information on filtered solutions for the 500M and 1.5B Vθ across the datasets when using the 7B Qwen 2.5 Coder Instruct πG
and a temperature of 1.0. “# Rem” is the average number of solutions removed per question. “Avg. Rank” is the average rank of the
solutions that were removed. “M1 Rank” is the average highest rank of the solutions that were removed. “M5 Rank” is the average rank
of the 5 top ranks of the solutions that were removed. “% Removed” is the total percentage of solutions removed across all questions. “%
Prob” is the percentage of problems where all solutions were removed. “Spread” is the average spread of the solutions that were removed
across the six seeds.

  Vθ         V                # Rem      Avg. Rank        M1 Rank          M5 Rank         % Removed          % Prob        Spread
             1 Test              51.38        82.90            38.87           51.04               40.14         6.86         20.00
             10 Tests            63.53        77.81            27.63           39.36               49.63        12.57         17.90
  500M
             Lint                 4.76       102.31            86.49           97.84                3.72         0.00         31.91
             Syntax               5.13       106.50            98.53          104.93                4.01         0.00         32.08
             1 Test              51.38        89.27           47.87            58.42               40.14         6.86         19.14
             10 Tests            63.53        83.47           35.41            45.89               49.63        12.57         17.14
  1.5B
             Lint                 4.76       108.70           96.02           104.91                3.72         0.00         30.16
             Syntax               5.13       112.99          107.00           111.73                4.01         0.00         30.28




Table 10. Results for the generation with Qwen 2.5 Coder 500M instruct with T = 1.0, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                     CodeContests            GSM8K                  HumanEval                 MBPP
         Filter           Ranker    Bof64   PPS           Bof64  PPS              Bof64   PPS             Bof64  PPS
                          500M       0.47      68.39       38.08        374.52     51.96      157.37       47.70      353.18
         —
                          1.5B       0.61      26.42       53.91        147.74     67.50       64.10       57.70      145.72
                          MV         1.39     126.19        —            —         64.05      851.41       61.41      870.83
         1 Test           500M       1.71      79.64        —            —         65.51      180.55       62.42      325.07
                          1.5B       2.02      74.27        —            —         74.18       91.64       66.59      200.19
                          MV         1.39     125.72        —            —         72.13      814.36       64.44      483.11
         3 Tests          500M       1.72      72.82        —            —         74.46      215.28       65.26      335.60
                          1.5B       2.05      69.09        —            —         78.73      116.20       67.90      213.38
                          MV         1.65     125.65        —            —         82.88      620.28       70.64      378.63
         10 Tests         500M       1.76      87.47        —            —         83.21      182.60       71.64      199.45
                          1.5B       2.15      82.33        —            —         83.67      114.91       72.36      154.63
                   Vall              2.16       3.32       73.63        391.53     86.79       19.09       73.73      13.99




                                                                   23
                                               Pareto Optimal Code Generation




Table 11. Results for the generation with Qwen 2.5 Coder 1.5B instruct with T = 1.0, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                   CodeContests          GSM8K                HumanEval                  MBPP
        Filter           Ranker   Bof64   PPS         Bof64  PPS            Bof64   PPS             Bof64   PPS
                         500M      1.64     67.79      63.63     348.16      64.78      169.35       58.72      394.16
        —
                         1.5B      2.62     26.63      75.01     137.80      71.85      69.56        65.72      162.73
                         MV        4.92    124.94       —           —        72.17      905.65       72.81     1195.51
        1 Test           500M      5.64     74.06       —           —        73.05      162.21       72.34     312.70
                         1.5B      5.60     67.36       —           —        77.90      80.87        74.26     186.30
                         MV        5.39    122.97       —           —        80.10     1026.14       76.22     1070.13
        3 Tests          500M      5.80     79.71       —           —        79.99      180.70       75.14     316.46
                         1.5B      5.61     73.83       —           —        83.29      93.31        76.07     193.02
                         MV        5.73    122.34       —           —        88.60      571.02       81.66      511.41
        10 Tests         500M      5.95     79.18       —           —        86.44      157.04       82.33      189.80
                         1.5B      5.75     73.53       —           —        88.15      91.79        82.47      142.11
                  Vall             7.83     2.23       92.72     173.71      94.06       20.09       85.64       20.97




Table 12. Results for the generation with Qwen 2.5 Coder 3B instruct with T = 1.0, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                   CodeContests          GSM8K                HumanEval                  MBPP
        Filter           Ranker   Bof64   PPS         Bof64  PPS            Bof64   PPS             Bof64   PPS
                         500M      4.52     64.02      75.48     339.96      75.50      159.60       60.70      387.75
        —
                         1.5B      5.76     25.14      81.89     134.53      79.90      65.21        67.54      159.58
                         MV       9.65     122.58       —           —        82.39     1057.72       74.99     1217.04
        1 Test           500M     10.93     66.69       —           —        79.15      142.54       72.22     294.73
                         1.5B     11.39     58.02       —           —        84.01      66.80        75.09     169.51
                         MV       11.34    118.91       —           —        85.78     1208.37       77.72     1074.66
        3 Tests          500M     12.40     64.03       —           —        85.29      153.96       74.96     301.64
                         1.5B     12.83     58.40       —           —        88.22      72.96        77.45     177.22
                         MV       12.16    116.15       —           —        89.54      684.03       84.10      509.97
        10 Tests         500M     12.67     70.78       —           —        89.01      137.37       83.04      178.20
                         1.5B     13.04     64.18       —           —        91.33      71.77        84.24      131.16
                  Vall            14.92     2.54       96.63     647.01      95.41       22.13       88.23       12.48




                                                               24
                                               Pareto Optimal Code Generation




Table 13. Results for the generation with Qwen 2.5 Coder 14B instruct with T = 1.0, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                   CodeContests          GSM8K                HumanEval                  MBPP
        Filter           Ranker   Bof64   PPS         Bof64  PPS            Bof64   PPS             Bof64   PPS
                         500M     10.99     59.83      90.53     323.74      83.23      172.96       68.85      328.09
        —
                         1.5B     12.86     23.52      91.49     127.83      85.44      70.92        73.28      137.09
                         MV       22.76    132.92       —           —        88.67     1197.05       79.82     1360.04
        1 Test           500M     24.47     66.16       —           —        85.08      143.42       75.26     264.22
                         1.5B     25.52     52.46       —           —        86.89      67.51        77.29     139.90
                         MV       24.32    127.07       —           —        90.36     1130.49       81.65     1127.35
        3 Tests          500M     26.07     59.08       —           —        88.10      148.71       77.00     267.42
                         1.5B     26.60     50.44       —           —        88.98      70.44        78.66     145.13
                         MV       25.83    120.53       —           —        91.62      662.39       87.72      349.60
        10 Tests         500M     28.02     67.14       —           —        90.47      128.04       85.83      157.48
                         1.5B     28.10     57.46       —           —        90.88      67.25        86.47      112.77
                  Vall            31.98     3.65       98.61     153.10      96.57       24.43       90.29       17.11




Table 14. Results for the generation with Qwen 2.5 Coder 7B instruct with T = 0.2, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                   CodeContests          GSM8K                HumanEval                  MBPP
        Filter           Ranker   Bof64   PPS         Bof64  PPS            Bof64   PPS             Bof64   PPS
                         500M      5.86     61.72      84.94     259.14      85.11      131.74       71.26      258.15
        —
                         1.5B      5.38     24.54      86.11     110.67      86.44      57.42        73.93      115.38
                         MV       10.82    173.82       —           —        88.41      961.83       78.24      316.36
        1 Test           500M     10.86     81.39       —           —        86.12      116.61       76.98      234.99
                         1.5B     11.72     66.73       —           —        88.01      56.21        77.42      128.61
                         MV       11.69    163.05       —           —        89.63     1196.20       79.63     1010.78
        3 Tests          500M     12.11     90.59       —           —        88.09      120.93       77.53     240.79
                         1.5B     12.38     80.77       —           —        89.52      59.52        78.31     135.70
                         MV       12.09    157.14       —           —        90.85      611.21       81.60      373.46
        10 Tests         500M     12.35     88.55       —           —        89.26      104.69       80.95      143.88
                         1.5B     12.40     80.12       —           —        90.38      56.36        81.31      104.77
                  Vall            12.40     3.09       91.17     504.11      91.46       11.63       82.40       6.97




                                                               25
                                               Pareto Optimal Code Generation




Table 15. Results for the generation with Qwen 2.5 Coder 7B instruct with T = 0.4, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                   CodeContests          GSM8K                HumanEval                  MBPP
        Filter           Ranker   Bof64   PPS         Bof64  PPS            Bof64   PPS             Bof64   PPS
                         500M      5.61     65.65      86.15     299.19      82.74      151.34       69.13      317.32
        —
                         1.5B      7.29     26.06      88.40     120.73      85.35      63.50        72.65      134.96
                         MV       13.11    163.12       —            —       87.80     1146.83       79.15     1257.67
        1 Test           500M     14.29     77.29       —            —       84.35      134.12       75.38     254.88
                         1.5B     14.91     64.04       —            —       86.96      62.73        76.75     138.36
                         MV       15.50    153.76       —            —       89.56     1143.86       80.52     1207.37
        3 Tests          500M     15.64     78.18       —            —       87.23      138.00       76.82     261.47
                         1.5B     16.18     69.93       —            —       88.85      65.37        78.44     144.88
                         MV       15.90    147.99       —            —       90.78      639.57       83.29      358.78
        10 Tests         500M     16.00     82.17       —            —       89.27      116.53       82.32      157.60
                         1.5B     16.29     73.83       —            —       90.03      61.52        83.10      112.16
                  Vall            16.74     3.83       95.21        60.02    92.57       15.11       84.55       14.80




Table 16. Results for the generation with Qwen 2.5 Coder 7B instruct with T = 0.6, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                   CodeContests          GSM8K                HumanEval                  MBPP
        Filter           Ranker   Bof64   PPS         Bof64  PPS            Bof64   PPS             Bof64   PPS
                         500M      6.00     66.83      85.73     317.18      83.09      163.23       67.14      351.91
        —
                         1.5B      7.21     26.53      88.19     127.31      84.78      67.77        71.45      146.91
                         MV       12.99    145.28       —            —       86.77     1280.37       77.83     1183.06
        1 Test           500M     13.46     74.06       —            —       84.87      140.68       74.82     264.62
                         1.5B     14.94     62.05       —            —       86.55      66.63        77.02     144.47
                         MV       14.76    142.47       —            —       89.71     1232.14       80.06     1011.88
        3 Tests          500M     14.84     78.82       —            —       87.75      150.36       76.82     268.41
                         1.5B     15.82     70.11       —            —       88.50      70.82        78.91     150.06
                         MV       15.63    136.34       —            —       90.93      504.65       85.36      362.63
        10 Tests         500M     15.30     80.81       —            —       89.52      125.36       84.09      159.63
                         1.5B     16.09     72.55       —            —       89.69      66.52        85.30      114.18
                  Vall            17.65     2.13       96.40     590.56      94.05       18.06       86.23       26.87




                                                               26
                                               Pareto Optimal Code Generation




Table 17. Results for the generation with Qwen 2.5 Coder 7B instruct with T = 0.8, n = 128, topp = 0.95, and 1024 tokens.
 Green backgrounds is higher performance while Red backgrounds is lower performance with respect to the entire column. If V is “—”
that means no pruning is done. Vall is the case where all test cases are run.

                                   CodeContests          GSM8K                HumanEval                  MBPP
        Filter           Ranker   Bof64   PPS         Bof64  PPS            Bof64   PPS             Bof64   PPS
                         500M      5.44     67.12      85.26     328.44      80.57      172.06       66.03      374.18
        —
                         1.5B      6.96     25.49      87.97     125.81      82.54      71.43        71.12      151.33
                         MV       13.54    137.85       —           —        87.43     1327.06       76.03     1097.09
        1 Test           500M     13.98     70.55       —           —        83.44      143.43       74.78     268.36
                         1.5B     14.92     59.29       —           —        84.53      67.50        77.26     145.59
                         MV       14.46    131.96       —           —        90.72     1178.13       79.32     1063.62
        3 Tests          500M     15.24     64.33       —           —        86.33      151.41       76.69     270.28
                         1.5B     15.60     57.96       —           —        87.06      71.48        79.00     150.07
                         MV       14.56    126.77       —           —        92.10      680.40       85.77      459.95
        10 Tests         500M     15.46     75.19       —           —        89.52      129.99       84.93      169.68
                         1.5B     15.70     67.22       —           —        89.56      68.03        86.31      118.63
                  Vall            17.98     3.35       97.30     582.08      95.65       19.81       89.03       19.55




                                                               27
