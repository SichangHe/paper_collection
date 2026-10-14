                                              SqueezeBench: Saturation-Resilient Evaluation of
                                                        Mathematical Capability
                                                             Pablo Manrique                Hai Xia           Stefan Szeider
                                                                          Algorithms and Complexity Group
                                                                             TU Wien, Vienna, Austria
                                                                     {pmanriqu,hxia,sz}@ac.tuwien.ac.at
arXiv:2610.13461v1 [cs.AI] 9 Oct 2026




                                                                                          Abstract
                                                  AI systems are making rapid progress in mathematics, but this progress is hard to measure.
                                              Benchmarks of solved problems saturate, and in benchmarks of open problems each problem can
                                              be resolved for the first time only once. We present SqueezeBench, a benchmark that is resilient
                                              to saturation: a success raises the bar instead of removing the problem. Each problem fixes an
                                              integer function f (n) whose values are known only for small n, and the benchmark keeps a lower
                                              and an upper record on it. A record is a computable Lean function with a machine-checked proof
                                              that it bounds f . A submission proposes a new function and proves that it bounds f , that it is
                                              no worse than the current record at any n, and that it is strictly better at some n. Once accepted,
                                              it becomes the record that the next submission has to beat. The system thus chooses the bound
                                              as well as its proof, and it may improve the record at a single n or improve its growth rate. At
                                              every n, the gap between the two records shows how far the certified bounds are from determining
                                              f (n). Every proof is checked by two independent Lean kernels, so no referee needs to check the
                                              mathematics. The checks also reject a function that computes f by exhaustive search at small n,
                                              and a maintainer only reads the submitter’s report and looks for such a search at larger n. We
                                              release ten problems from extremal combinatorics with twenty proved initial records, together
                                              with the admission tools. As a baseline, agents based on a frontier language model, with at most
                                              one hour per record, had 82 submissions accepted and improved every record, without going
                                              beyond the published literature. Agents based on two newer models then started from these
                                              records, had 60 more submissions accepted and improved 19 of the 20 records again. For eight
                                              of the ten problems, at least one record is still asymptotically behind the best published bound.


                                        1    Introduction
                                        AI systems have made rapid progress in mathematics. On miniF2F, a benchmark of formalized
                                        olympiad problems, the best prover solved 29.2% of the test problems when the benchmark appeared
                                        in 2021 [Zheng et al., 2022], and 99.6% four years later [Chen et al., 2025]. In 2025, a system reached
                                        a gold-medal score at the International Mathematical Olympiad, certified by the competition’s
                                        coordinators [Luong and Lockhart, 2025], and AI systems have since resolved a few open problems
                                        posed by Erdős [Feng et al., 2026].
                                             This progress is hard to measure. A benchmark of solved problems has a maximum score,
                                        and as the best systems approach it, their scores can no longer be told apart [Akhtar et al., 2026].
                                        Four systems have reported solving all 672 problems of PutnamBench [Tsoukalas et al., 2024,
                                        PutnamBench maintainers, 2026], and the maintainers of FrontierMath consider its hardest tier
                                        saturated [Stewart, 2026]. The answers of such benchmarks are often public, so they may also end up
                                        in the training data of the systems they evaluate. Benchmarks of open problems, such as FrontierMath
                                        Erdős [Adamczewski and Bloom, 2026], avoid known answers, but each problem yields at most one
first resolution. After that, its solution is public, and a later system that solves it may be reproducing
a published solution, so the set of informative problems shrinks as the systems improve. Their scores
count resolved problems, and intermediate progress, such as a better bound, earns little or no credit.
In both kinds of benchmark the statement to be proved is given, and the system is not asked to
find it. Record archives such as EinsteinArena [Bianchi et al., 2026] and Optimization Constants in
Mathematics [Davis et al., 2026] keep improvable records, but a record there is a number for a fixed
problem, checked by running a witness or by citing a paper, and no kernel checks a bound’s proof.
     We propose SqueezeBench, a benchmark designed to avoid these difficulties. Each problem
fixes a function f : N → N whose values are known only for small n, such as the size of the largest
cap set in Fn3 or the diagonal Ramsey number R(n, n). For each problem the benchmark keeps two
records, a lower bound and an upper bound on f . A record is a computable function written in
Lean 4 [de Moura and Ullrich, 2021] together with a proof that it bounds f . A submission proposes
a new function and proves three obligations: it bounds f , it is no worse than the current record at
any n, and it is strictly better at some n. An accepted submission becomes the new record, and the
next submission has to beat it, so a success leaves the problem in the benchmark with a stronger
record. We call this property resilience. It does not guarantee that systems remain distinguishable,
since the benchmark stagnates when no system improves any record. At each n the two records
enclose the unknown value f (n), and the distance between them shows how far the certified bounds
are from determining f (n) (Figure 2). We include only problems with no known closed formula
for f .
     Each accepted submission is stored with its author and date. At any time each record has a holder,
and the record history of a problem shows who held which bound, when, and by how much each
submission moved it. This history is the leaderboard. We do not reduce it to a single score, since
progress on twenty records, each a function of n, has many dimensions. To compare systems in a
controlled way, we start each of them from the same snapshot of records with the same budget and
compare the records they reach, value by value, not the number of accepted submissions. Replaying
a bound that the current record already matches earns nothing, and a bound beyond the published
literature cannot have been copied from it. Our initial records are elementary bounds weaker than
the published ones, so the first steps can draw on the literature, and we report this catch-up phase as
such.
     The system proposes the bound itself, and only the three obligations are fixed. An improvement at
a single n is accepted, and so is an improvement of the asymptotic growth. This freedom has a catch.
The function f is itself a correct bound, and a record that computes f by exhaustive search could
never be improved. The checks therefore evaluate each new record at every n ≤ 100 within a fixed
budget, which rejects such a search below n = 100, and a maintainer reads the submitter’s report
and looks for a search placed above it. Otherwise admission needs no mathematical referee. The
proofs are verified by two independent Lean kernels against statements fixed before the submission,
and the other checks also run mechanically. Once per problem, a maintainer also checks that the
formal definition matches the intended question.
     As a baseline, we ran agents based on a frontier language model, Opus 5 in Claude Code, one
per record, with at most one hour each and 18.9 hours in total, starting from the initial records. They
had 82 submissions accepted and improved every record at least once, for example the upper bound
for the Ruzsa–Szemerédi problem from n3 to ⌊n(n + 3)/18⌋. Nearly all accepted submissions use
general arguments and explicit constructions, not exhaustive search. None goes beyond the published
literature, and for every problem at least one record stays asymptotically behind the literature.
     We then ran agents based on two newer models from the baseline’s records, Fable 5.1 on 19
records and Opus 5.5 on the lower record for Golomb rulers, in one run of up to about two hours per
record, and the agents could consult a second language model. This continuation is not a controlled
comparison of models but a test of resilience. The records left by one system were the starting point
of the next, and the newer agents had 60 submissions accepted and improved 19 of the 20 records
again. The number of records that match the leading term of the best published bound rose from


                                                    2
four to ten, for example through the Ellenberg–Gijswijt bound for cap sets and Shearer’s bound for
R(3, k), both formalized by the agent itself. All agents could search the web. One of them found a
public Lean formalization of a published construction and adapted it, which the benchmark accepts
as part of the catch-up phase when the license allows it and the source is credited. Neither run
exhausted the problems. For eight of the ten problems, at least one record is still asymptotically
behind the best published bound (Table 2).
    Our contributions are as follows.
    • A benchmark design that measures mathematical progress without a fixed target: lower and
      upper records that are functions of the parameter, replaced only by submissions that prove the
      three obligations (Section 2).

    • Ten problems from extremal combinatorics, formalized in Lean 4 on top of Mathlib, each with
      proved initial lower and upper records (Section 4).
    • An admission pipeline that checks a submission mechanically against statements fixed in
      advance, with two independent kernels, the three standard axioms and a computation budget,
      together with tools to prepare, verify and accept submissions (Section 2).

    • An evaluation of agents based on three frontier language models on all twenty records, a
      baseline from the initial records and a continuation from the baseline’s records, with the
      harness that runs the baseline (Section 5).
All problems, records and tools are publicly available at:

                            https://github.com/leansolving/SqueezeBench


2    Framework
As part of our benchmark, we formalize ten problems in the field of extremal combinatorics. This
branch of mathematics studies how large or how small a finite object can be, subject to certain
conditions. For instance, as we will further explain in Section 4.2, SqueezeBench includes the
Golomb ruler problem [Bloom and Golomb, 1977], which asks the following question: for every
natural number n, what is the smallest possible length of a set of n integers whose pairwise differences
are all distinct, where the length is the difference between the largest and the smallest integer? In
other words, these are rulers with n marks that measure no distance twice. For small values of n,
one could even solve this problem by hand: for n = 3, the ruler {0, 1, 3} has length 3, but no ruler
of length 2 exists, since {0, 1, 2} measures the distance 1 twice. Thus, the smallest possible length
is 3. For n = 4, one can find rulers of length 6, such as {0, 1, 4, 6}, but not of length 5, since the six
pairwise differences would be distinct positive integers no larger than 5. Therefore, the shortest ruler
has length 6. However,  as the value of n increases, finding such shortest rulers becomes intractable,
since there are L−1n−2 candidate rulers of length L. Although there is no known solution for the
Golomb ruler problem for all possible values of n, researchers have proved upper and lower bounds
on these numbers [Singer, 1938, Erdős and Turán, 1941, Lindström, 1969]. This problem is typical
of the problems in SqueezeBench. For each of them, the exact answer is known only for a small
number of values of the parameter, or for special families of them, and no closed formula is known
for the general case. In contrast, we consider bounds that are explicit: each has to be a computable
function that can be evaluated at every value of the parameter. They can be closed formulas, tables
or programs that build explicit constructions. The task is to narrow the gap between these known
functions and the unknown answer. Note that our requirement on bounds is stronger than what the
literature typically provides, where the best bounds are often asymptotic, with unspecified constants
or valid only for sufficiently large values.


                                                    3
                                                                                     squeeze verify
 Challenge Vk
                          squeeze
                                      Submission Vk                                  1 only its own directory
 import Vk−1 /Def.lean
                            new       Def.lean        the new record            PR   2 plain definitions
 record            open
                                      Proof.lean      valid, improves, strict        3 Comparator, 2 kernels
 valid           sorry                metadata.toml   author, witness n0             4 proof budget
 improves        sorry                REPORT.md       how the bound was found        5 computable, no f
 strict          sorry
                                                                                     6 cheap for n ≤ 100

                                          Def.lean becomes trusted
                                                                                                  all pass

  Challenge Vk+1
                                                                                      maintainer review
  import Vk /Def.lean                        squeeze accept


Figure 1: One version step: trusted files written by squeeze (solid), untrusted submission (dashed).


   In short, SqueezeBench keeps the best lower and upper bounds on each f proved so far and
accepts a submission only if it provably improves one of them. The rest of this section covers how a
problem is formalized, what counts as a bound, how records are kept, what a submission consists of
and how it is verified.

Problems. We have formalized each problem in Lean 4, building on its mathematical library,
Mathlib [The mathlib Community, 2020]. The answer to each problem is a function f : N → N,
where f (n) is the optimal value for the parameter n. In Lean, f is defined by its combinatorial
meaning, typically as a maximum or minimum over a finite set, but no closed form for f is known.
This is what makes the benchmark resilient to saturation: if f had a closed form, the lower and upper
bounds could meet at every n, and the problem would be solved. This could eventually happen—and
we would welcome a submission that settles an open problem—but we select problems for which it
is not expected soon. Each problem also fixes a smallest parameter value nmin , in practice 1, 2 or 3,
below which f is set to 0. Some definitions degenerate at such small values, and pinning them lets a
bound be stated for every n without side conditions.

Bounds and records. A lower bound on f is a function l : N → N with l(n) ≤ f (n) for all n,
and an upper bound is a function u with f (n) ≤ u(n) for all n. For each problem, SqueezeBench
keeps a lower and an upper record, the best bound proved so far in each direction, as a sequence of
versions that starts from an elementary seed (Figure 2). The record gap u(n) − l(n) measures how
far the records are from determining f (n); for Golomb rulers, 536 ≤ f (28) ≤ 585. A submission
that replaces a lower record l consists of a new Lean function l′ and proofs of three theorems: valid
(l′ ≤ f ), improves (l ≤ l′ ), both for all n, and strict (l(n0 ) < l′ (n0 ) for some n0 ≥ nmin ).
For upper records, the inequalities are reversed. The valid theorem is usually the one that requires
most of the proof effort in a submission. The other two are more easily automatable: we provide
idioms that allow defining a new bound from the current record by improving it at a single point or
taking the pointwise maximum with another valid bound, so the improves requirement is trivial
in these cases. For proving strict, the bounds are evaluated and compared at a witness point n0 .

Challenges and submissions. A submission must be checked without trusting the person who
wrote it. For this, we use Comparator [Lean FRO, 2026a], a tool from the Lean FRO for judging
Lean proofs, which is also used by other projects such as lean-eval [Lean FRO, 2026b] and
Palomar [Palomar, 2026]. Comparator takes a trusted challenge, which states theorems with their
proofs left as sorry and may leave some definitions open, and an untrusted solution, which fills
them in. It checks that the solution proves exactly the statements of the challenge and uses no
axioms beyond a given list. We allow only the three standard axioms propext, Quot.sound


                                                  4
and Classical.choice, so sorry and native_decide are rejected. It then checks the
proofs with the Lean kernel and, in our setup, also with nanoda [Bailey, 2026], an independent
implementation of the kernel. Our design follows this interface. For every new version of a record,
SqueezeBench provides a Challenge: a trusted Lean file in which the new record definition is
left open, and valid, improves and strict are stated in terms of f and the current record.
The solution is split into two Lean files: Def.lean defines the new function, and Proof.lean
imports it and proves the three theorems. The split matters because the next Challenge imports
Def.lean to refer to this record, which makes that file trusted; keeping the proofs out of it keeps
the trusted part small. Two more files complete the submission: metadata.toml gives the author
name and the witness n0 , and REPORT.md explains how the bound and its proofs were obtained
and the setup used, including the models or agents. SqueezeBench is hosted in a public GitHub
repository, and a submission is a pull request that adds these four files.

Verification and acceptance. Every step is run by squeeze, a command-line tool that we
implemented in Lean (Figure 1). A submitter runs squeeze new, which creates the four files of a
submission with the statements copied from the open Challenge, and opens a pull request that adds
them. squeeze verify checks the submission in six gates, both locally and on the pull request.
    • Gates 1–2. They run before any submitted code is built. The pull request may change only
      files inside the new record’s directory, and Def.lean must be at most 64 KiB and contain
      only plain definitions, since later Challenges import it and anything else could alter them.
    • Gate 3. Comparator, as described above.
    • Gates 4–6. They check what Comparator does not. (4) The proofs in Proof.lean stay
      within a computation budget, per declaration and in total, so that they argue instead of making
      the kernel search by brute force. (5) The new record is computable, and its definition does not
      refer to f . (6) The kernel evaluates the new record at every n from nmin to 100, and at n0 if it
      is larger, each within a fixed budget.

Gate 6 lets the next submitter evaluate the record to beat it. It also rejects a record that computes f
by exhaustive search, such as a brute-force computation of f under another name, which passes
every other gate; such a record is a correct bound that no later submission could improve. No known
algorithm computes f (n) within the budget for n near 100, while every record accepted so far passes.
Budgets are counted in heartbeats, Lean’s measure of work, so for fixed Lean and Mathlib versions
they do not depend on the machine. Once all gates pass:

    • Review. A maintainer reads the submission, including its report, and merges it. The maintainer
      also rejects a search that starts above n = 100.
    • Next Challenge. squeeze accept writes the next Challenge, stated against the new record.
      If two submissions answer the same Challenge, the first one merged wins, and squeeze
      verify rejects the other until it is restated against the new record.
    • Audit and history. Since Challenges are never edited, squeeze audit can re-check every
      past version against the Challenge that admitted it. Each problem’s page in the repository lists
      every accepted version with its date, author and witness.



3    Related Work
SqueezeBench lies between mathematical reasoning benchmarks, archives of best known results
and formal theorem proving, and Table 1 compares it with benchmarks and archives.



                                                  5
                                                  (a) lower records                                       (b) upper records

                8000 80            gain lk (n) − l1 (n)                                       V000           V001
                                         V008
                                                                V001–V008
                                                                                                                      V002
 ruler length          40                                                          1000

                           0
                               1             50           100                                                          V006
                4000                                                                                                               V013
                                                                      V000         500



                   0                                                                 0
                       1                    28            50                 100          1          10          20           28          40
                                                number of marks n                                         number of marks n

Figure 2: Every accepted record for the Golomb ruler problem. Colors run from light for the oldest
version to dark for the newest, the standing record is drawn thick, and each version is at least as good
as its predecessor at every n, which its submission proved. (a) The lower records for n ≤ 100: the
seed n2 (dashed) and versions V001–V008, which differ only in lower-order terms and overlap at
         

this scale. Writing lk for version V00k of the lower record, the inset shows the gain lk (n) − l1 (n)
of each later version over V001, for k = 2, . . . , 8 (k = 8 drawn thick). (b) The upper records for
n ≤ 40, from the seed (dashed) to the standing record V013.


    Benchmarks of solved problems, such as miniF2F [Zheng et al., 2022] and ProofNet [Azerbayev
et al., 2023], hold out known answers, which can leak into training data, and they saturate. Bench-
marks of open problems avoid known answers. FrontierMath Erdős [Adamczewski and Bloom,
2026] asks for Lean proofs or disproofs of 68 Erdős problems, and Formal Conjectures [Firsching
et al., 2026] collects open conjectures from many areas, such as number theory and spectral theory,
and HorizonMath [Wang et al., 2026] scores programs that compute values for open problems against
fixed baselines.
    Archives of best known results track moving targets, such as the surveys of small Ramsey num-
bers [Radziszowski, 2026] and of cages [Exoo and Jajcay, 2013]. Their updates rest on human
checking, and each covers its own problems. Newer collections gather many problems in one place,
such as Leaps in Bounds (LoB) [Munro, 2026], FrontierShift [AItonomy Foundation, 2026] and
Optimization Constants in Mathematics [Davis et al., 2026], which Terence Tao started1 . They are
updated semi-automatically and accept a claim backed by a citation, without a formal proof. Fun-
Search [Romera-Paredes et al., 2024], AlphaEvolve [Novikov et al., 2025] and PatternBoost [Charton
et al., 2024] find constructions by search and check each with a program; FunSearch’s cap sets of
growth 2.2202 exceed our lower record. These systems are potential submitters, not competitors,
since a construction enters the benchmark once proved in Lean. SqueezeBench is not a search
method: it adds a Lean proof valid at every n and keeps a lower and an upper record.
    Progress on such problems rarely comes as a single proof. In combinatorics in particular,
the bounds on an extremal function are tightened step by step by many researchers, and even an
improvement at a single value can matter. A benchmark that asks for a proof of a fixed statement
or for a better scalar cannot credit such steps on a function whose values are unknown, and a single
proof of a conjecture does not credit the earlier work it builds on.
    The columns of Table 1 record whether the answers are Known, whether a better submission
replaces the incumbent (Moves), whether the incumbent can never get worse (Non-reg.), the Target (a
proposition, a scalar or a function of n), whether a lower and an upper bound are both kept (2-sided),
whether trust rests on a citation (Cited), what performs the Check (a kernel, or a program run on a
witness), whether the check is automatic or human (Mode), and the submission (Sub.).
       1 https://terrytao.wordpress.com/2026/01/22/a-crowdsourced-repository-for-optimization-constants/




                                                                             6
Table 1: Mathematical benchmarks and record archives. NA marks a system that maintains no
standing record. Only where a submission replaces a total function can a replacement be tighter at
one n and looser at another, and only SqueezeBench both replaces functions and proves that the re-
placement never regresses. Notes: a Formal Conjectures’ function-valued bound goals are unproved
(:= by sorry) and asymptotic, so improving a single n earns no credit. b HorizonMath compares
against a fixed value in data/baselines.json; beating it does not replace it. c SorryDB and
ArXivLean refresh the task stream: an answer key exists, but is kept fresh. d Formal Conjectures’
anchors c1a_lower_bound and c1a_upper_bound both carry sorry while tagged as solved.
e
  FrontierShift shows a gap on some pages, but only its upper side is a maintained record. Sources.
PutnamBench [Tsoukalas et al., 2024], FormalMATH [Yu et al., 2025], Lean Workbook [Ying et al.,
2024], CombiBench [Liu et al., 2025], SorryDB [Letson et al., 2026], ArXivLean [Gehrunger et al.,
2026], FM: Open Problems [Epoch AI, 2026], Covering [Acerbi, 2026], Grassl [Grassl, 2026], Ein-
steinArena [Bianchi et al., 2026]. The remaining systems are cited above.

                           Known Moves Non-reg. Target         2-sided Cited Check Mode Sub.
      Benchmarks: A system is scored against mathematical problems
      miniF2F, ProofNet, yes        no     NA        prop.      NA    NA     proof auto     proof
      PutnamBench,
      FormalMATH, Lean
      Workbook
      CombiBench            yes     no     NA        prop.      NA    NA     proof   auto   answer + proof
      SorryDB, ArXivLean yesc       no     NA        prop.      NA    NA     proof   auto   proof
      FrontierMath Erdős no         no     NA        prop.      NA    NA     proof   auto   proof
      Formal Conjectures no         no     no        functiona yes    yesd   proof   auto   answer terma
      HorizonMath           no      nob    NA        scalar     no    yes    exec.   auto   Python program
      FM: Open Problems no          no     NA        scalar     no    yes    exec.   auto   real value
      Records: An archive of the community’s best known results
      Ramsey, Cages         no      yes    yes       table      yes   yes    none human citation
      LoB, Covering,        no      yes    yes       table      yes   yes    exec. human construction
      Grassl
      Opt. Constants        no      yes    yes       scalar     yes   yes    none    human a claim + link
      EinsteinArena         no      yes    yes       scalar     no    yes    exec.   auto a witness
      FrontierShift         no      yes    yes       scalare    no    yes    exec.   human a witness
      SqueezeBench          no      yes    yes       function yes     no     proof   auto function +
                                                                                           proofs



4     Problems
We include ten problems in SqueezeBench, but the list is not closed. We will keep adding problems
that meet the same requirements as the current ones (Section 2), and we welcome proposals of new
problems from the community. Appendix A describes how a new problem could be added.

4.1   The ten problems
The ten problems come from three areas of extremal combinatorics (Table 2): additive combinatorics
(cap sets, Roth numbers, the Ruzsa–Szemerédi problem and Golomb rulers), extremal graph theory
(graphs without a 4-cycle, graphs without cycles of length 3 or 4, and subgraphs of the hypercube
without a 4-cycle), and Ramsey theory (the diagonal Ramsey numbers R(n, n), the Ramsey numbers
R(3, k) and the Schur numbers). Each problem has a single integer parameter, and its exact values
are known only up to a small size, for example n ≤ 4 for R(n, n), k ≤ 5 for the Schur numbers,
n ≤ 6 for cap sets and for the hypercube, and n ≤ 28 for Golomb rulers.




                                                       7
Table 2: The ten problems and their standing records after the runs of Section 5. Seed records are
omitted; each is the simplest provable bound, and several are trivial. Golomb is a minimization
problem, and its upper record and lower record are the construction and impossibility argument,
respectively. For all other problems, constructions give the lower record. ⋆ matches the leading term
of the best published bound, or its base if the bound is exponential, in that direction. † matches the
best elementary bound; the published frontier uses the triangle removal lemma. Unmarked records
are asymptotically behind the literature.

 Problem            f counts                          Domain Standing lower record                Standing upper record
 Additive combinatorics
 Cap set           largest subset of Fn3 with no        n≥1         growth 1121/6 ≈ 2.196         O(2.756n )
                   three collinear points                           (extended products of caps)   (Ellenberg–Gijswijt) ⋆
 Roth              largest subset of {0, . . . , n − 1} n ≥ 1       Θ(n0.638 ); exact for         4n/11 + O(1) (Moser)
                   with no 3-term progression                       n ≤ 209
 Ruzsa–            most triangles in an n-vertex        n≥3         Θ(n1.716 ) (from cap sets)    n2 /18 + O(n), smaller for
 Szemerédi         graph whose every edge lies in                                                 n ≥ 33 (counting) †
                   exactly one triangle
 Golomb            shortest ruler with n marks and n ≥ 1            n2 − 2n3/2 + O(n) ⋆           ≈ n2 (Singer) ⋆ ; best known
                   all differences distinct                                                       for n ≤ 100
 Extremal graph theory
                                                                                                                     √
 C4 -free          most edges in an n-vertex graph n ≥ 1            ≈ 12 n3/2 (sub-polarity       Reiman’s bound − O( n) ⋆
                   with no 4-cycle                                  graphs) ⋆
 Girth five        most edges in an n-vertex graph n ≥ 1            Θ(n3/2 ) for all n            Moore bound + O(1) ⋆
                   with no 3- or 4-cycle                            (sub-planes of projective
                                                                    planes)
                                                                             √
 Hypercube C4       most edges in a C4 -free          n≥1           (n + Θ( n)) 2n−2              ≈ 0.623 of the edges
                    subgraph of the n-cube                          (Brass–Harborth–              (Chung)
                                                                    Nienborg) ⋆
 Ramsey theory
                                                                               √
 Ramsey             least N such that every             n≥2         (1 + o(1)) e2 n 2n/2          Erdős–Szekeres with
                    2-coloring of KN has a                          (Spencer) ⋆ ; best known at   Walker’s step
                    monochromatic Kn                                n = 5, 6
 R(3, k)            least N such that every N -vertex k ≥ 2         ≈ (k/2)3/2 (ordered           (1 + o(1)) k2 / log k
                    graph has a triangle or k                       point–line incidences)        (Shearer) ⋆
                    independent vertices
 Schur              largest N such that {1, . . . , N } k ≥ 1       growth 3801/5 ≈ 3.28          ⌊e k!⌋ − k for odd k
                    has a k-coloring with no                        (template constructions) ⋆
                    monochromatic x + y = z



4.2      Running example: Golomb rulers
The values of f (n) for the Golomb ruler problem of Section 2 are known for n ≤ 28; the last five
weresettled by exhaustive      searches by distributed.net [OEIS Foundation Inc., 2026]. The lower seed
is n2 , since its n2 distances are distinct and at most the length. The upper seed is the shorter of the
                    

binary ruler {0, 1, 3, . . . , 2n−1 − 1} and a ruler of length about 2n3 , patched at n = 5, 6.
    Figure 3 shows how f is formalized. Like every problem, it builds on Mathlib [The mathlib Com-
munity, 2020], and four problems reuse a Mathlib definition of f directly, such as rothNumberNat
for Roth numbers. The ruler condition is stated through sums: in a Sidon set, a+b = c+d determines
the pair, which for a finite set of integers is equivalent to all positive differences being distinct. Since f
is an infimum and the infimum of the empty set is 0 in Lean, the file proves that the binary ruler above
is a ruler; without it, no lower bound on f could be proved. The definition is noncomputable:
nothing in the pipeline evaluates f , and a record may not refer to f or RulerLengths, since it
would compute f under another name.




                                                                8
 def IsSidon (S : Finset N) : Prop :=
   ∀ a ∈ S, ∀ b ∈ S, ∀ c ∈ S, ∀ d ∈ S,
     a + b = c + d → (a = c ∧ b = d) ∨ (a = d ∧ b = c)
 def RulerLengths (m : N) : Set N :=
   {L | ∃ S : Finset N, S ⊆ range (L + 1) ∧ S.card = m ∧
         IsSidon S ∧ L ∈ S}
 noncomputable def f (m : N) : N :=
   if m < nMin then 0 else sInf (RulerLengths m)

          Figure 3: The Lean definition of f for Golomb rulers (parameter m, nmin = 1).


5     Evaluation
On the ten problems included as part of SqueezeBench, we performed an agent-based evaluation
that provides a baseline and a continuation from its records. It has two phases:

    1. We obtained preliminary bounds using Claude Code agents with the model Opus 5, starting
       from elementary seeds under a budget of one hour (or until two idle sessions in a row) and 16
       GiB of memory. They ran in parallel on an AMD Ryzen 9 5900X machine with 24 threads at
       3.7 GHz and 125 GiB of memory under Ubuntu 22.04.5 LTS.
    2. From the bounds of the first phase, we launched Fable 5.1 agents at maximum effort on 19
       of the 20 records, and an Opus 5.5 agent on the lower record for Golomb rulers, with the
       possibility of consulting GPT-6 Astra through its API. Each agent had at most 32 GiB of
       memory, and each run took up to about two hours. We sent a stop notice after 80 minutes
       or at 55% of the context, and a notice to continue when an agent stopped earlier; the first six
       runs ended before this rule existed. The prompt changed slightly over the runs, and a rule on
       outside sources was added during them. The agents ran on two AMD EPYC 9274F CPUs (96
       threads) with 755 GiB of memory under Ubuntu 24.04.

    In both phases, one agent was used per track (10 problems × 2 directions). They were all
prompted to first read the documentation about the problem and the current records, possibly search
the literature and choose a bound. Then they had to develop a Lean proof of the valid, improves
and strict theorems, run squeeze verify and, if it passed, accept the bound as a new record
and repeat the loop. The agents accepted records in their own copies of the repository. We re-verified
every record of the second phase independently before merging it, and later re-ran squeeze audit
on every record of both phases. The prompt also asks for improvements at infinitely many n and
discourages many tiny submissions. The repository contains the full prompt.
    Every one of the twenty records improved on its seed. In the first phase, the Opus 5 agents had
82 submissions accepted in 18.9 hours, and sixteen of the twenty tracks were stopped by the time
limit rather than by two idle sessions. In the second phase, the Fable 5.1 and Opus 5.5 agents had
60 more submissions accepted and improved 19 of the 20 records again. Table 2 lists the standing
records: ten match the leading term or the growth rate of the best published bound, one matches the
best elementary bound, and nine are asymptotically behind. Nearly all accepted proofs are general
arguments, such as explicit algebraic constructions, products of smaller constructions, and counting
arguments; decide only checks explicit witnesses. Gate 6 was added during the second phase,
and it rejected one record that had passed the earlier checks in an agent’s copy of the repository but
was not yet merged. The first formalization of the Ellenberg–Gijswijt bound computed its values
by a recursion over lists and exceeded the budget at every n from 59 to 100, so the next submitter
could not have evaluated it. The agent resubmitted the bound with a computation that needs fewer
than 100 heartbeats per n. One record may go beyond the literature at concrete values. For the
Ruzsa–Szemerédi problem, a Fable 5.1 agent localized a counting argument of Fox et al. [2017],
suggested by the second model it consulted, and combined it with the degree bounds of earlier
versions. The resulting upper record gives f (50) ≤ 140 and f (100) ≤ 529, where the best bounds


                                                  9
we could derive from the literature are 144 and 566. We found no published bound that gives these
values; asymptotically, the record is still far from the o(n2 ) bound of the triangle removal lemma.
    The running example shows the difference between the two phases (Figure 2). Opus 5 reached
the Erdős–Turán ruler, of length about 2n2 , with the optimal rulers for n ≤ 17, and refined counting
arguments over the distances of a ruler to n2 − 2n3/2 + O(n), the form of Lindström’s bound [Lind-
ström, 1969]. Fable 5.1 brought in constructions from the literature, down to length about n2 [Singer,
1938, Bose and Chowla, 1962, Ruzsa, 1993], and tables of explicit rulers, the optimal ones for n ≤ 28
and the best known ones up to n = 100 [Rokicki and Dogon, 2016]; the kernel checks each ruler. The
upper record went from 1570 to the optimum 585 at n = 28, and from 20,002 to 8831 at n = 100.
Three submissions by Opus 5.5 refined the lower-order terms of the lower record, from 529 to 536
at n = 28 and from 8143 to 8210 at n = 100. In total, 13 upper and 8 lower versions were accepted.
The records now determine f (n) for n ≤ 5, and the gap is 49 at n = 28 and 621 at n = 100, where
the seeds left 42,687 and 1,984,851. Both records match the leading term n2 of the best published
bounds and go no further; the published lower bound has a better second-order term [Balogh et al.,
2023].
    Apart from possibly the Ruzsa–Szemerédi record, no record goes beyond the published literature.
Both records match the leading term of the best published bounds only for C4 -free graphs and
Golomb rulers; for the other eight problems at least one record stays behind (Table 2). For example,
the upper record for the diagonal Ramsey numbers gives R(5, 5) ≤ 58, while the published bound
is 46 [Radziszowski, 2026]. Some of the best bounds rest on results that Mathlib lacks, or whose
explicit constants are far too weak at these n, such as the triangle removal lemma. Others were
obtained by computer, and there the two directions differ. A construction found by a search comes
with a witness, which is cheap to check once it is published: the agents imported the best known
Golomb rulers up to 100 marks and a Schur coloring that shows S(7) ≥ 1696. An impossibility
result found by an exhaustive search has no short certificate and exceeds the computation budget, as
for f (28) = 585, so it can enter a record only through an argument that is not known yet. Published
but unformalized bounds leave room for further submissions. Beyond them, the records reach values
of f that nobody knows, and formalizing the literature alone cannot saturate the benchmark.


6    Conclusions
SqueezeBench measures mathematical progress by records rather than by solved statements. A
record is a computable function with a proof that it bounds f , and a submission replaces it only
by proving that it is valid, no worse at any n and better at some n, checked by two kernels against
statements fixed in advance. In our evaluation the records left by one system became the starting
point of the next. After 82 accepted submissions of the baseline, agents based on newer models had
60 more accepted and improved 19 of the 20 records again, and eight of the ten problems still have
a record behind the literature. The record history is the leaderboard.
    The benchmark has limits. Its ten problems come from one area of mathematics and have one
parameter each. Our runs were not a controlled comparison of models from one snapshot with equal
budgets, which is how we intend the benchmark to be used. A maintainer still reads each report for
a search above n = 100. Bounds known only from exhaustive computer searches cannot enter a
record within the budget. Future work will add problems with several parameters and admit proofs
that rely on a verified checker for SAT certificates, marked as such, as a route for these bounds.
SqueezeBench is open to submissions from people and AI systems alike.




                                                 10
Acknowledgements
This research was funded in whole or in part by the Austrian Science Fund (FWF) within the Cluster
of Excellence Bilateral Artificial Intelligence (10.55776/COE12).
         This project is also partially supported by the European Union’s Horizon 2020 research and
         innovation programme under the Marie Skłodowska-Curie grant agreement No. 101034440.


Use of AI assistants
We used generative AI tools to implement the benchmark tools and the Lean formalizations, to give
feedback on the design of the admission checks, and to compare the records with the literature.
The records of Section 5 were produced by the AI agents under evaluation. The other tasks with
required disclosure do not apply to this work. We also used AI tools to draft and edit text and figures,
search the literature and format references. We reviewed all AI-assisted work. Code and proofs are
checked by tests and the Lean kernel, and every cited source was checked against its original. We
take responsibility for the final content of this paper, including text, claims and artifacts produced
with the aid of generative AI.


References
G. Acerbi. Covering Repository. https://www.coveringrepository.com/, 2026. Incorporates the
  data of D. Gordon’s La Jolla Covering Repository up to March 2026; updates dating to November
  1996; distributes validation software. Accessed 2026-09-21.
T. Adamczewski and T. F. Bloom. FrontierMath Erdős, 2026. URL https://arxiv.org/abs/2609.25050.
   68 Erdős problems open as of August 2026; resolution required in Lean.
AItonomy Foundation. FrontierShift: Open problems. https://aitonomy.org/projects/open-problems,
  2026. 167 problems; incumbent-beating submission rule; per-problem lower/upper bounds and
  gap. Accessed 2026-09-21.
M. Akhtar, A. Reuel, P. Soni, S. Ahuja, P. S. Ammanamanchi, R. Rawal, V. Zouhar, S. Yadav,
 C. Whitehouse, D. Ki, J. Mickel, L. Choshen, M. Suppa, J. Batzner, J. Chim, J. Sania, Y. Long,
 H. A. Rahmani, C. Q. Knight, Y. Nan, J. Raj, Y. Fan, S. Singh, S. Sahoo, E. Habba, U. Gohar, S. M.
 Pawar, R. Scholz, A. Subramonian, J. Ni, M. Kochenderfer, S. Koyejo, M. Sachan, S. Biderman,
 Z. Talat, A. Ghosh, and I. Solaiman. When AI benchmarks plateau: A systematic study of
 benchmark saturation. In Forty-third International Conference on Machine Learning, 2026. URL
 https://openreview.net/forum?id=YC1Otscjbs.
Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad. ProofNet:
  Autoformalizing and formally proving undergraduate-level mathematics. CoRR, abs/2302.12433,
  2023. doi: 10.48550/ARXIV.2302.12433. URL https://doi.org/10.48550/arXiv.2302.12433.
C. Bailey. nanoda_lib: a type checker for Lean 4. https://github.com/ammkrn/nanoda_lib, 2026.
  Accessed 2026-09-25.
J. Balogh, Z. Füredi, and S. Roy. An upper bound on the size of Sidon sets. Am. Math. Mon., 130
   (5):437–445, 2023. doi: 10.1080/00029890.2023.2176667. URL https://doi.org/10.1080/000298
   90.2023.2176667.
F. Bianchi, Y. Kwon, A. Pappu, and J. Zou. Harnessing the collective intelligence of AI agents in
   the wild for new discoveries. CoRR, abs/2606.10402, 2026. doi: 10.48550/ARXIV.2606.10402.
   URL https://doi.org/10.48550/arXiv.2606.10402.


                                                  11
G. S. Bloom and S. W. Golomb. Applications of numbered undirected graphs. Proceedings of the
  IEEE, 65(4):562–570, 1977. doi: 10.1109/PROC.1977.10517.
R. C. Bose and S. Chowla. Theorems in the additive theory of numbers. Commentarii Mathematici
  Helvetici, 37(1):141–147, 1962. doi: 10.1007/BF02566968.
F. Charton, J. S. Ellenberg, A. Z. Wagner, and G. Williamson. PatternBoost: Constructions in
   mathematics with a little help from AI. CoRR, abs/2411.00566, 2024. doi: 10.48550/ARXIV.2
   411.00566. URL https://doi.org/10.48550/arXiv.2411.00566.
L. Chen, J. Gu, L. Huang, W. Huang, Z. Jiang, A. Jie, X. Jin, X. Jin, C. Li, K. Ma, C. Ren,
  J. Shen, W. Shi, T. Sun, H. Sun, J. Wang, S. Wang, Z. Wang, C. Wei, S. Wei, Y. Wu, Y. Wu,
  Y. Xia, H. Xin, F. Yang, H. Ying, H. Yuan, Z. Yuan, T. Zhan, C. Zhang, Y. Zhang, G. Zhang,
  T. Zhao, J. Zhao, Y. Zhou, and T. H. Zhu. Seed-Prover: Deep and broad reasoning for automated
  theorem proving. CoRR, abs/2507.23726, 2025. doi: 10.48550/ARXIV.2507.23726. URL
  https://doi.org/10.48550/arXiv.2507.23726.
D. Davis, P. Ivanisvili, and T. Tao. Optimization Constants in Mathematics. https://teorth.github.io
  /optimizationproblems/, 2026. Announced 22 January 2026. Accessed 2026-09-21.
L. de Moura and S. Ullrich. The Lean 4 theorem prover and programming language. In A. Platzer
  and G. Sutcliffe, editors, Automated Deduction - CADE 28 - 28th International Conference on
  Automated Deduction, Virtual Event, July 12-15, 2021, Proceedings, volume 12699 of Lecture
  Notes in Computer Science, pages 625–635. Springer, 2021. doi: 10.1007/978-3-030-79876-5\_
  37. URL https://doi.org/10.1007/978-3-030-79876-5_37.
Epoch AI. FrontierMath: Open problems. https://epoch.ai/frontiermath/open-problems, 2026. Pilot
  January 2026; expanded to 50 problems 31 July 2026. Accessed 2026-09-21.
P. Erdős and P. Turán. On a problem of Sidon in additive number theory, and on some related
   problems. Journal of the London Mathematical Society, s1-16(4):212–215, 1941. doi: 10.1112/
   jlms/s1-16.4.212.
G. Exoo and R. Jajcay. Dynamic cage survey. The Electronic Journal of Combinatorics, 2013. doi:
  10.37236/37. Dynamic Survey DS16; first published 2008, revision 26 July 2013.
T. Feng, T. H. Trinh, G. Bingham, J. Kang, S. Zhang, S. Kim, K. Barreto, C. Schildkraut, J. Jung,
   J. Seo, C. Pagano, Y. Chervonyi, D. Hwang, K. Hou, S. Gukov, C. Tsai, H. Choi, Y. Jin,
   W. Li, H. Wu, R. Shiu, Y. Shih, Q. V. Le, and T. Luong. Semi-autonomous mathematics
   discovery with Gemini: A case study on the Erdős problems. CoRR, abs/2601.22401, 2026. doi:
   10.48550/ARXIV.2601.22401. URL https://doi.org/10.48550/arXiv.2601.22401.
M. Firsching, P. Lezeau, S. Mercuri, M. Z. Horváth, Y. Dillies, C. Sönne, E. Wieser, F. Zhang,
 T. Hubert, B. A. y Arcas, and P. Kohli. Formal Conjectures: An open and evolving benchmark
 for verified discovery in mathematics. CoRR, abs/2605.13171, 2026. doi: 10.48550/ARXIV.260
 5.13171. URL https://doi.org/10.48550/arXiv.2605.13171.
J. Fox, H. Huang, and B. Sudakov. On graphs decomposable into induced matchings of linear sizes.
   Bulletin of the London Mathematical Society, 49(1):45–57, 2017. doi: 10.1112/blms.12005.
T. Gehrunger, J. Dekoninck, and M. Vechev. ArXivLean: How well can LLMs formally prove
   research math? https://matharena.ai/arxivlean/, 2026. First public release 21 April 2026.
   Accessed 2026-09-21.
M. Grassl. Bounds on the minimum distance of linear codes and quantum codes. http://www.code
 tables.de, 2026. Accessed 2026-09-21.


                                                12
Lean FRO. Comparator. https://github.com/leanprover/comparator, 2026a. Accessed 2026-09-25.
Lean FRO. lean-eval. https://github.com/leanprover/lean-eval, 2026b. Accessed 2026-09-25.
A. Letson, L. Sarra, A. Poiroux, O. Dressler, P. Lezeau, D. Aranha, F. Pu, A. Hill, M. C. Hidalgo,
  J. Berman, G. Tsoukalas, and L. Taelman. SorryDB: Can AI provers complete real-world Lean
  theorems? CoRR, abs/2603.02668, 2026. doi: 10.48550/ARXIV.2603.02668. URL https:
  //doi.org/10.48550/arXiv.2603.02668.
B. Lindström. An inequality for B2 -sequences. Journal of Combinatorial Theory, 6(2):211–212,
  1969. doi: 10.1016/S0021-9800(69)80124-9.
J. Liu, X. Lin, J. Bayer, Y. Dillies, W. Jiang, X. Liang, R. Soletskyi, H. Wang, Y. Xie, B. Xiong,
   Z. Yang, J. Zhang, L. Zhi, J. Li, and Z. Liu. CombiBench: Benchmarking LLM capability for
   combinatorial mathematics. CoRR, abs/2505.03171, 2025. doi: 10.48550/ARXIV.2505.03171.
   URL https://doi.org/10.48550/arXiv.2505.03171.
T. Luong and E. Lockhart. Advanced version of Gemini with Deep Think officially achieves gold-
   medal standard at the International Mathematical Olympiad. Google DeepMind blog, 2025. URL
   https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieve
   s-gold-medal-standard-at-the-international-mathematical-olympiad/. Accessed 2026-09-24.
D. Munro. Leaps in Bounds. https://leapsinbounds.org/, 2026. Per-parameter histories of lower and
  upper bounds. Accessed 2026-09-21.

A. Novikov, N. Vu, M. Eisenberger, E. Dupont, P. Huang, A. Z. Wagner, S. Shirobokov, B. Kozlovskii,
  F. J. R. Ruiz, A. Mehrabian, M. P. Kumar, A. See, S. Chaudhuri, G. Holland, A. Davies, S. Nowozin,
  P. Kohli, and M. Balog. AlphaEvolve: A coding agent for scientific and algorithmic discovery.
  CoRR, abs/2506.13131, 2025. doi: 10.48550/ARXIV.2506.13131. URL https://doi.org/10.485
  50/arXiv.2506.13131.
OEIS Foundation Inc. Sequence A003022: Length of shortest (or optimal) Golomb ruler with
 n marks. The On-Line Encyclopedia of Integer Sequences, https://oeis.org/A003022, 2026.
 Accessed 2026-09-25.
Palomar. Palomar: A registry of Lean-verified mathematics. https://palomar-registry.org/about,
  2026. Accessed 2026-09-25.

PutnamBench maintainers. PutnamBench leaderboard, 2026. URL https://trishullab.github.io/Put
  namBench/leaderboard.html. Accessed 2026-09-24.
S. P. Radziszowski. Small Ramsey numbers. The Electronic Journal of Combinatorics, 2026. doi:
   10.37236/21. Dynamic Survey DS1; first published 1994, revision #18, 24 April 2026.
T. Rokicki and G. Dogon. Possibly optimal Golomb rulers calculated for 160 to 40,000 marks.
   https://cube20.org/golomb/, 2016. Accessed 2026-09-25.
B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. R. Ruiz,
  J. S. Ellenberg, P. Wang, O. Fawzi, P. Kohli, and A. Fawzi. Mathematical discoveries from program
  search with large language models. Nat., 625(7995):468–475, 2024. doi: 10.1038/S41586-023-0
  6924-6. URL https://doi.org/10.1038/s41586-023-06924-6.

I. Z. Ruzsa. Solving a linear equation in a set of integers I. Acta Arithmetica, 65(3):259–282, 1993.
   doi: 10.4064/aa-65-3-259-282.




                                                 13
J. Singer. A theorem in finite projective geometry and some applications to number theory. Transac-
   tions of the American Mathematical Society, 43(3):377–385, 1938. doi: 10.1090/S0002-9947-1
   938-1501951-4.
E. Stewart. The Epoch Brief, September 12, 2026. Epoch AI newsletter, 2026. URL https:
  //epochai.substack.com/p/the-epoch-brief-september-12-2026. Accessed 2026-09-24.
The mathlib Community. The Lean mathematical library. In J. Blanchette and C. Hritcu, editors,
  Proceedings of the 9th ACM SIGPLAN International Conference on Certified Programs and
  Proofs, CPP 2020, New Orleans, LA, USA, January 20-21, 2020, pages 367–381. ACM, 2020.
  doi: 10.1145/3372885.3373824. URL https://doi.org/10.1145/3372885.3373824.
G. Tsoukalas, J. Lee, J. Jennings, J. Xin, M. Ding, M. Jennings, A. Thakur, and S. Chaudhuri.
  PutnamBench: Evaluating neural theorem-provers on the Putnam Mathematical Competition.
  In A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang,
  editors, Advances in Neural Information Processing Systems 37: Annual Conference on Neural
  Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 -
  15, 2024, 2024. URL http://papers.nips.cc/paper_files/paper/2024/hash/1582eaf9e0cf349e1e5a6
  ee453100aa1-Abstract-Datasets_and_Benchmarks_Track.html.
E. Y. Wang, S. R. Motwani, J. V. Roggeveen, E. Hodges, D. Jayalath, C. London, K. Ramakrishnan,
   F. Cipcigan, P. Torr, and A. Abate. HorizonMath: Measuring AI progress toward mathematical
   discovery with automatic verification. CoRR, abs/2603.15617, 2026. doi: 10.48550/ARXIV.260
   3.15617. URL https://doi.org/10.48550/arXiv.2603.15617.
H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen. Lean Workbook: A large-scale Lean problem
  set formalized from natural language math problems. In A. Globersons, L. Mackey, D. Belgrave,
  A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, editors, Advances in Neural Information
  Processing Systems 37: Annual Conference on Neural Information Processing Systems 2024,
  NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, 2024. URL http://papers.nips.
  cc/paper_files/paper/2024/hash/bf236666a2cc5f3ae05d2e08485efc4c-Abstract-Datasets_and_
  Benchmarks_Track.html.
Z. Yu, R. Peng, K. Ding, Y. Li, Z. Peng, M. Liu, Y. Zhang, Z. Yuan, H. Xin, W. Huang, Y. Wen,
  G. Zhang, and W. Liu. FormalMATH: Benchmarking formal mathematical reasoning of large
  language models. CoRR, abs/2505.02735, 2025. doi: 10.48550/ARXIV.2505.02735. URL
  https://doi.org/10.48550/arXiv.2505.02735.
K. Zheng, J. M. Han, and S. Polu. miniF2F: a cross-system benchmark for formal Olympiad-level
  mathematics. In The Tenth International Conference on Learning Representations, ICLR 2022,
  Virtual Event, April 25-29, 2022. OpenReview.net, 2022. URL https://openreview.net/forum?id=
  9ZPegFuFTFv.



A      Adding a problem
To add a new problem to SqueezeBench, the following steps must be followed.
    1. Define the problem. Problems/<P>/Def.lean defines nmin and f by its combinatorial
       meaning, pinned to 0 below nmin , reusing a definition from Mathlib where one exists. It also
       provides, for each direction, a lemma that reduces a bound to its combinatorial content, such
       as the existence of a witness of a given size. Where f can be evaluated, its smallest values are
       checked by decide on every build. If f is a least element, the file also proves that the set is
       nonempty; without this, no lower record can be proved.


                                                  14
   2. Seed both records. Each direction gets a version V000 in Records/<Dir>/V000/, with
      the same four files as a submission: the record in Def.lean, a proof of valid alone in
      Proof.lean, metadata.toml and REPORT.md. A seed should be simple and quick to
      formalize, and it may not be taken from the known values.
   3. Configure the checks. A trusted file Challenges/<P>/problem.toml sets nmin , the
      directions, the budget of gate 6 and the oracles, the constants that a record may not refer to: f
      and the definitions it is built from.
   4. Write the first Challenges. squeeze accept, run once per direction, writes the statement
      of the seed and the first open Challenge, which asks to beat the seed.

   5. Check the seeds. squeeze audit checks that the seeds pass their own Challenges, with
      the three standard axioms only.
   6. Describe the problem. A README.md gives the statement, the known values with their
      sources, and the literature; squeeze accept later adds the record history to it.
   7. Review. A maintainer checks that the definition of f denotes the intended object, including
      any reused Mathlib definition, and admits the problem. From then on it appears in squeeze
      like every other problem.
The repository also contains a tutorial problem that is not part of the benchmark, the largest subset
of {1, . . . , m} that contains no element together with its double. Its f is computable, so a newcomer
can check values of f by decide and practice the submission workflow on it.




                                                  15
