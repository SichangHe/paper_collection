               Quantifying SMT Solver Instability for Formal
                              Verification∗
arXiv:2610.12649v1 [cs.SE] 8 Oct 2026




                                            Daniel Evans1 , Rylie Hansen1 , and John Shorter1
                                                    1
                                                      Computer Science Department
                                                             St. Olaf College
                                                             Northfield, MN
                                                       {evans11,hansen42,shorte1}@stolaf.edu



                                                                        Abstract
                                            Program verification has become commonplace in software develop-
                                        ment projects, and much of its feasibility can be attributed to the poten-
                                        tial of SMT solvers to automate model checking and other verification
                                        techniques. However, SMT instability, a phenomenon where semanti-
                                        cally equivalent permutations of source code take much longer to solve
                                        or timeout, has been found to interrupt workflows and make software
                                        engineers more likely to avoid verification. Previous efforts to measure
                                        SMT instability have had difficulty quantifying it due to the abnormal
                                        runtime distributions it produces. In this paper, we use the coefficient of
                                        variation to model instability across an extensive dataset of SMT queries
                                        from three software domains. Our results show that SMT instability is
                                        significant in each area, and that it increases for queries that take longer
                                        on average. However, using a novel method to quantify instability, we
                                        show that a different approach is possible: if a solution were to optimize
                                        the structure of queries for runtime, rather than variance, instability
                                        could be mitigated while also improving overall solver performance.


       1                                Introduction
       Satisfiable Modulo Theories (SMT) is a class of problems that seek to deter-
       mine whether or not a solution to a formula exists. As an expressive method
          ∗ Copyright ©2022 by the Consortium for Computing Sciences in Colleges. Permission to

       copy without fee all or part of this material is granted provided that the copies are not made
       or distributed for direct commercial advantage, the CCSC copyright notice and the title of
       the publication and its date appear, and notice is given that copying is by permission of the
       Consortium for Computing Sciences in Colleges. To copy otherwise, or to republish, requires
       a fee and/or specific permission.


                                                                             1
for representing formal logic problems, they are useful for software engineering
tools such as model checkers, symbolic executors, and proof-oriented program-
ming languages, which structure facts about software as SMT queries and solve
them using programs called SMT solvers [1], [2]. Solving an SMT query is an
NP-complete problem, and the solving process can be a time consuming step
for formal verification tools; thus, many solvers use heuristics to navigate the
solution space [3].
    Heuristics make the problem more feasible, but they also introduce a phe-
nomenon referred to as the butterfly effect, proof brittleness, or proof instability
[4]. Small changes to source code or logically equivalent permutations to an
SMT query can lead to significantly different runtimes for the solver [5]. This
is a widely recognized problem in academia and large-scale software produc-
tion because any small modification to a script—for example, editing a naming
convention—has the potential to make verification intractable [6].
    While the existence of proof instability has been well documented, the full
scope of the problem is not well known, and most methods of mitigating it are
either ad-hoc or incomplete [7]. In this work, we use the coefficient of variation
(CV) and other statistical methods to quantify instability within an extensive
benchmark study of 60,000 SMT query forms across three software domains.
We find that instability is significant for complete samples, and our results
provide strong evidence that instability continues to be a problem for distri-
butions with timeouts. Finally, we demonstrate that intelligently mitigating
instability—while optimizing for runtime—can reduce average solver runtime,
a step toward addressing instability.



2   Background
The phenomenon of instability (also called proof fragility or proof brittleness)
among SMT queries has been observed as a challenge in many large-scale,
industry verification-based projects [8], including those from Microsoft [9], [10]
and Amazon [11].
    In order to formally investigate the prevalence of instability in proofs gen-
erated by Dafne, a verification programming language, [5] developed the Mari-
posa tool and benchmark. They introduce the conception of a query as one
member of a distribution of equivalent queries that have been mutated in ways
that preserve semantic meaning, which we build off of in our work. Statistical
approaches to distributions of runtimes are made challenging by the reality
that the underlying distribution is not known—i.e. it is not normal and often
has very long tails—and frequently cannot be estimated due to timeout con-
straints. Success rate avoids some of these challenges by treating solver results


                                         2
as binary, rather than a continuous measure of time, but in doing so loses the
ability to quantify or compare the instability of one query set with another.
    This work was continued in Shake [7] and Cazamariposas [6], the former
a method that uses the empirically identified technique of context pruning to
reduce instability, and the latter a tool that identifies candidate qualifiers for
instability and suggests repairs. An important observation from these works is
the contribution of problematic axioms to instability, which is taken advantage
of by [8].
    [12] determined that, if a normalized or canonical form could be found
for each logically equivalent query, it would eliminate instability when making
irrelevant changes. While finding such a form is an NP-complete task in itself,
they produce a normalizing algorithm that works well in most cases. They
represent runtimes as a distribution of penalized runtime (PR-2) scores, where
a query-solver pair is evaluated by runtime where the solver succeeds, and twice
the timeout time where it fails. Then, Median Absolute Deviation (MAD) in
PR-2 scores is used to measure instability, which, unlike success rate, allows for
quantification and comparison. However, it is impossible to say how much the
true runtime would have deviated from the PR-2 score for queries that timeout,
so the statistical significance is unknown. Moreover, MAD does not quantify
instability relative to the difficulty of a query set, meaning that one query set
may appear to be more unstable than another simply because it takes longer
to compute, on average.

3     Methodology
3.1   Quantifying Instability
As in [5], we use the quality of semantic equivalence. Given SMT queries Q
and Q′ , we say that Q is semantically equivalent to Q′ if, for any assignment ϕ,
Q(ϕ) ⇐⇒ Q′ (ϕ). [12] identified several ways to mutate a query and preserve
semantics, including renaming variables, shuffling the clauses of commutative
operators, like conjunction or addition, and swapping symmetric operators, like
less than and greater than. Given some query Q and a semantic-preserving
mutation M , we define the mutation set of Q to be the set of all semantically
equivalent queries that can be derived by applying M to Q.
    By treating the mutant set of Q as a population to be sampled from, sta-
tistical analysis of the variance in runtimes that result from applying some
solver S to members of a query’s mutant set can describe proof instability.
Although instability in the field may involve non-equivalent queries, showing
it for equivalent ones suffices.
    Variance among a population of runtimes is often estimated using the stan-
dard deviation statistic, denoted σ, of a sample, and previous work has used


                                        3
standard deviation as a proxy for instability [5]. However, this makes queries
whose mutants typically take longer appear more unstable, when the difficulty
of a query and its instability should be considered independently. We use the
mean runtime, denoted µ, as a proxy for the difficulty of a query’s mutant set.
The coefficient of variation (CV) statistic, defined as
                                            σ
                                    CV =      ,
                                            µ
accounts for this by evaluating the variance of runtimes relative to the difficulty
of the mutant set [13].
    Constructing a confidence interval would indicate the trustworthiness of the
estimated CV, but the underlying distribution of runtimes is not consistent.
To overcome this, we use a nonparametric bootstrapping approach to estimate
the variability of the CV, as described in [14]. Randomly selecting from a
sample of mutant query runtimes with replacement produces what is called a
bootstrap, from which we calculate a resampled CV. By generating bootstraps
many times, we get a distribution of CVs and an estimation of variance, from
which we construct the desired confidence interval.
    In analyzing our results, we say that a query is unstable if the lower bound of
the 95% confidence interval around its CV is greater than or equal to one. That
is, a query is unstable when its mutant set has a standard deviation greater
than or equal to its mean, with 95% confidence. The choice of threshold is
arbitrary, but the ability to choose any threshold demonstrates the power of
this method, as it can be tailored to any desired amount in practice.
    Because it is necessary to impose a time limit on solvers, some samples have
missing runtime data. It is not possible to make good statistical estimations
about the variance of these distributions, so, in these cases, we resort to a
simplified version of the method used by [5]. That is, we define the success
rate (SR) of a sample to be the proportion of mutant queries for which the
solver does not timeout. Then, if a solver runs out of time on less than 5%
of the queries, the original query is considered unsolvable and not unstable,
while an SR greater than .95 is considered stable and not unstable. In order to
be statistically confident in concluding that an original query is unstable, we
perform a z-test of proportions for unsolvability and stability. This process is
summarized in Figure 1.

3.2     Study Design
3.2.1    Domain
We limit the scope of our analysis to the cvc5 [15] and Z3 [16] SMT solvers.
Both solvers are widely used in industry and academia, and previous work


                                        4
    Input                  Solvability Test     Reject H0    Stability Test    Reject H0   Ω is unstable
 Mutant set Ω,              H0 : SRΩ ≤ .05                   H0 : SRΩ ≥ .95                 with 95%
   n=100                    HA : SRΩ > .05                   HA : SRΩ < .95                 confidence

                 Failed to reject H0              Failed to reject H0

                          Ω may be unsolvable                Ω may be stable



             Figure 1: Categorization of Unstable When SR < 1


on instability has focused on them. The SMT queries we benchmarked were
pulled from three different sources: (i) bounded model checking, (ii) symbolic
execution, and (iii) competition.
    Bounded model checkers (BMCs) build finite state models of programs and
prove that they cannot reach states encoded as error states. They frequently
build these models using SMT queries [17]. Symbolic execution (SymEx) en-
gines use SMT queries to represent the end behavior of programs. Solving these
queries proves that a particular result—e.g. an error—is possible or impossible.
All of the BMC and SymEx queries used in this study were collected by [18] in
a public dataset, using the ESBMC model checker and KLEE symbolic execu-
tion engine on the GNU coreutils and other real world programs. In addition
to these two areas, we used SMT queries from the 2025 International Satis-
fiability Modulo Theories Competition (SMT-Comp), a yearly event that has
developers test SMT solvers on hundreds of thousands of competitions. Previ-
ous work has already demonstrated the existence of instability in SMT-Comp
queries [5], but BMC and SymEx have not been explored directly.

3.2.2     Query Selection
For BMC, SymEx, and SMT-Comp, we gathered two subsets of queries. The
process for BMC and SymEx differed from that of SMT-Comp because we
included queries from specific SMT-Comp logics.
    The first selection consisted of a random sample. We randomly chose 100
queries from both BMC and SymEx and 150 queries from SMT-Comp, equally
sourced across 15 logics. Every query was run using both solvers, and, if an
error occurred, it was replaced with a new randomly chosen query. SMT-Comp
has different subsets of query logics to fulfill, while BMC and SymEx contain
no such divisions.
    The second of our two selections consisted of difficult queries, which we
defined as queries that timed out for cvc5, Z3, or both. We selected 100 hard
queries from BMC and SymEx and 120 hard queries from 6 logics in SMT-
Comp. For SMT-Comp, the remaining queries were drawn from those timing
out on either solver. For BMC and SymEx, they were split evenly between


                                                     5
CVC5-only and Z3-only timeouts, with reallocation if needed.

3.2.3     Query Shuffling
For the purposes of this study, we modified the official SMT Query scrambler
used in the SMT-Comp by limiting its scope and implementing a basic nor-
malization process. The existing scrambler applies many different semantic-
preserving mutations, so we modified this behavior to only shuffle assertions,
thus limiting the scope of the data. Other works have analyzed instability
caused by other mutations, like shuffling the clauses of commutative functions
[12]. For the sake of consistency, we normalized variable names, which prevents
the effects of declarations from affecting instability.

4     Results
4.1     Prevalence of Instability
Table 1 contains the results of each solver, domain, and selection category.
For every original query in the SymEx hard category, CVC5 had an SR less
than one, so an accurate CV could not be calculated. In most categories, the
proportion of unstable queries is small, which is consistent with previous results
[5]. However, even a small percentage of inconsistent queries can cause enough
failure to limit the use of formal verification by software developers [6], so these
results are significant, particularly in categories with more than 10% unstable
queries like Z3 solving hard BMC queries.


                      Table 1: SMT Solver Benchmark Results
 Domain     Solver   Selection               Mean   CV     CV 95% CI     SR     Unstable Proportion
 BMC        cvc5     hard-scrambled          1114   0.06   [0.04,0.07]   0.09                  0.09
                     pure-random-scrambled    232   0.15   [0.07,0.18]   0.83                  0.06
            Z3       hard-scrambled           751   0.61   [0.38,0.72]   0.43                  0.29
                     pure-random-scrambled     72   0.22   [0.15,0.26]   0.95                  0.08
 SMT-Comp   cvc5     hard-scrambled          1133   0.24   [0.14,0.29]   0.08                  0.12
                     pure-random-scrambled    250   0.12   [0.08,0.15]   0.80                  0.06
            Z3       hard-scrambled          1111   0.04   [0.02,0.05]   0.11                  0.14
                     pure-random-scrambled    182   0.20   [0.1,0.24]    0.87                  0.05
 SymEx      cvc5     hard-scrambled          1101    NA    [NA,NA]       0.12                  0.07
                     pure-random-scrambled    157   0.13   [0.1,0.15]    0.96                  0.09
            Z3       hard-scrambled            11   0.19   [0.16,0.22]   0.99                  0.01
                     pure-random-scrambled      1   0.18   [0.15,0.21]   1.00                  0.00


   Moreover, comparing CV, our contribution, to SR, the previously used
method for measuring instability, provides various insights. In many cases, a
low SR is associated with high average runtimes and vice versa. This shows
how reliant SR is on the timeout threshold; easier queries may appear stable


                                               6
at twenty minutes, while having a high amount of variance that would lead
to them being considered unstable with some other time limit. CV gives a
more accurate indication of instability than the proportion of queries marked
as unstable for a given category. For example, among randomly selected BMC
queries, the average success rate of Z3 was about 95%, which makes the un-
stable proportion appear relatively low at 0.08. The CV, however, shows that
these queries still varied by about 22% on average, which could be very signif-
icant under a lower time limit.

4.2                  Relationship Between Query Difficulty and Instability
Another advantage of being able to quantify instability is being able to inves-
tigate its relationship to other variables. We applied linear regression to all
mutant sets with a success rate of one, and we found that the logarithm of
CV is a very significant positive predictor of the logarithm of average runtime
(t = 10.5, df = 263, p < .001), which provides strong evidence that, within the
domain of our analysis, more difficult queries tend to be more unstable. This
is further supported by the fact that CVs tended to be higher in the hard se-
lections as opposed to the randomly selected. Furthermore, difficult queries for
which the CV could not be estimated are likely to exhibit significant variation,
on average.

                                           Z3                                cvc5
              1200      BMC
                        SymEx
                        SMT-Comp
              1000      Average Runtime


              800
Runtime (s)




              600

              400

              200

                0
                               Queries (Ordered by Average)       Queries (Ordered by Average)


Figure 2: Difference Between Mean and Minimum Runtimes: Mutant
sets with average times of less than 10 or equal to 1200 seconds are excluded.
Z3 in particular exhibits high potential for time savings.




                                                              7
4.3   Leveraging Instability
When a software engineering tool generates an SMT query, that query is not
a random permutation within a broad set of semantically equivalent queries;
instead, the query is produced according to some internal algorithm. Natu-
rally, the concern of this algorithm is in generating rigorous proofs that verify
qualities of software, not in creating a particular structure that is well-suited
for the heuristics of SMT solvers. Thus, if the developer hasn’t considered this,
the query the tool produces may as well be truly random, and has previously
been treated as such.
    The prevalence of instability, particularly among difficult queries, suggests
that queries that are structured more intelligently could save time when they
reach the SMT solver. This is visualized in Figure 2, where minimum runtimes
within a query’s mutant set are plotted beneath the original runtime. In some
cases, a well-structured query’s runtime is negligible, while the original query
takes nearly sixteen minutes to solve.
    Quantifying instability using CV allows us to be more exact. For example,
we can say that, with a confidence level of 0.95, restructuring a hard BMC
query could decrease Z3 runtimes by as much as 38% on average. Previous
work suggests that the runtime of the original query typically correlates with
the center of its mutant set [5], which means that the average query runtime
is a good stand-in for the original runtime. Our results show that future work
should consider mitigating instability by optimizing query structure for run-
time, rather than just success rate or variance, as this would have a stabilizing
effect with the added benefit of decreased runtimes.

5     Conclusion
We investigated SMT instability in three relevant software development areas,
two of which had previously been unexplored. In addition to using the previous
metric of success rate, we applied the coefficient of variation to the runtimes
of 60,000 mutant queries, and our results show that instability is an issue for
both the cvc5 and Z3 solvers in every domain. By fitting a linear model to CV,
we demonstrate that it is possible to predict variation in queries and that the
difficulty of a query is a significant positive predictor of instability. Thus, it is
reasonable to expect that, for difficult queries where timeouts occur, we would
find significant instability as well.
    Finally, our results show that query instability may be an opportunity as
much as it is a challenge. If an efficient method could be developed for re-
structuring queries in a way that is better suited to the internal heuristics of
solvers, it could mitigate instability while also offering time savings. While
work is currently being done on developing bespoke methods identified in the


                                         8
field for mitigating instability [6], we conjecture that optimizing for runtime
would be a task well-suited for machine learning models that are capable of
reasoning about the complex structure of algorithms and program data.

6      Acknowledgments
The authors would like to express gratitude to Dr. Will Leeson, Professor of St.
Olaf College, and Nicholas Phair, PhD Student at the University of Virginia,
for supporting this research.


References
 [1]   M. Luckcuck, M. Farrell, L. A. Dennis, C. Dixon, and M. Fisher, “Formal
       specification and verification of autonomous robotic systems: A survey,”
       ACM Comput. Surv., vol. 52, no. 5, 100:1–100:41, Sep. 13, 2019, issn:
       0360-0300. doi: 10.1145/3342355
 [2]   A. Lattuada et al., “Verus: Verifying rust programs using linear ghost
       types,” in Proceedings of the ACM on Programming Languages, vol. 7,
       Apr. 6, 2023, 85:286–85:315. doi: 10.1145/3586037
 [3]   D. Kroening and O. Strichman, Decision Procedures: An Algorithmic
       Point of View, 1st ed. Springer Publishing Company, Incorporated, May
       2008, 304 pp.
 [4]   T. Bordis and K. R. M. Leino, “Free facts: An alternative to inefficient ax-
       ioms in dafny,” in Formal Methods, A. Platzer, K. Y. Rozier, M. Pradella,
       and M. Rossi, Eds., Cham: Springer Nature Switzerland, 2025, pp. 151–
       169. doi: 10.1007/978-3-031-71162-6_8
 [5]   Y. Zhou, J. Bosamiya, Y. Takashima, J. Li, M. Heule, and B. Parno,
       “Mariposa: Measuring SMT instability in automated program verifica-
       tion,” in 2023 Formal Methods in Computer-Aided Design (FMCAD),
       ISSN: 2708-7824, Oct. 2023, pp. 178–188.
 [6]   Y. Zhou, A. Shah, Z. Lin, M. Heule, and B. Parno, “Cazamariposas:
       Automated instability debugging in smt-based program verification,” in
       Automated Deduction – CADE 30, Berlin, Heidelberg: Springer-Verlag,
       Jul. 30, 2025, pp. 75–94. doi: 10.1007/978-3-031-99984-0_5
 [7]   Y. Zhou, J. Bosamiya, J. Li, M. Heule, and B. Parno, “Context prun-
       ing for more robust SMT-based program verification,” presented at the
       Formal Methods in Computer-Aided Design (FMCAD), Oct. 1, 2024.
 [8]   M. Dodds, “Formally verifying industry cryptography,” IEEE Security &
       Privacy, vol. 20, no. 3, pp. 65–70, May 2022, issn: 1558-4046.


                                         9
 [9]   C. Hawblitzel et al., “Ironclad apps: End-to-end security via automated
       full-system verification,” in Proceedings of the 11th USENIX conference
       on Operating Systems Design and Implementation, ser. OSDI’14, USA:
       USENIX Association, Oct. 6, 2014, pp. 165–181. Accessed: Mar. 27, 2026.
[10]   A. Lattuada et al., “Verus: A practical foundation for systems verifica-
       tion,” in Proceedings of the ACM SIGOPS 30th Symposium on Operating
       Systems Principles, ser. SOSP ’24, New York, NY, USA, Nov. 15, 2024,
       pp. 438–454. doi: 10.1145/3694715.3695952
[11]   A. Chakarov et al., “Formally verified cloud-scale authorization,” 2025.
       [Online]. Available: https : / / www . amazon . science / publications /
       formally-verified-cloud-scale-authorization
[12]   D. Amrollahi et al., “Towards SMT solver stability via input normaliza-
       tion,” in 2025 Formal Methods in Computer-Aided Design (FMCAD),
       ISSN: 2708-7824, Oct. 2025, pp. 84–93.
[13]   S. M. Ross, Introduction to Probability and Statistics for Engineers and
       Scientists. Amsterdam: Academic Press, 2020.
[14]   M.-T. Puth, M. Neuhäuser, and G. D. Ruxton, “On the variety of meth-
       ods for calculating confidence intervals by bootstrapping,” Journal of
       Animal Ecology, vol. 84, no. 4, pp. 892–897, 2015, issn: 1365-2656. doi:
       10.1111/1365-2656.12382
[15]   H. Barbosa et al., “Cvc5: A versatile and industrial-strength SMT solver,”
       in Tools and Algorithms for the Construction and Analysis of Systems,
       Cham: Springer International Publishing, 2022, pp. 415–442. doi: 10.
       1007/978-3-030-99524-9_24
[16]   L. de Moura and N. Bjørner, “Z3: An efficient SMT solver,” in Tools and
       Algorithms for the Construction and Analysis of Systems, C. R. Ramakr-
       ishnan and J. Rehof, Eds., Berlin, Heidelberg: Springer, 2008, pp. 337–
       340. doi: 10.1007/978-3-540-78800-3_24
[17]   D. Beyer and A. Podelski, “Software model checking: 20 years and be-
       yond,” in Principles of Systems Design, J.-F. Raskin, K. Chatterjee, L.
       Doyen, and R. Majumdar, Eds., Cham: Springer Nature Switzerland,
       2022, pp. 554–582. doi: 10.1007/978-3-031-22337-2_27
[18]   W. Leeson, M. B. Dwyer, and A. Filieri, “Sibyl: Improving software en-
       gineering tools with SMT selection,” in 2023 IEEE/ACM 45th Inter-
       national Conference on Software Engineering (ICSE), ISSN: 1558-1225,
       May 2023, pp. 2185–2197. doi: 10.1109/ICSE48619.2023.00184




                                       10
