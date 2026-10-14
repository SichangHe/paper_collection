                                         PolyQEnt: A Polynomial Quantified Entailment
                                                           Solver

                                              Krishnendu Chatterjee1 , Amir Kafshdar Goharshady2 , Ehsan Kafshdar
                                             Goharshady1 , Mehrdad Karrabi1 , Milad Saadat3 , Maximilian Seeliger4 , and
                                                                         Ðorđe Žikelić5
                                                 1
arXiv:2408.03796v3 [cs.LO] 29 Jan 2025




                                                     Institute of Science and Technology Austria, Klosterneuburg, Austria
                                                                      2
                                                                         University of Oxford, Oxford, UK
                                                               3
                                                                  Sharif University of Technology, Tehran, Iran
                                                                       4
                                                                         Vienna University of Technology
                                                         5
                                                            Singapore Management University, Singapore, Singapore


                                                 Abstract. Polynomial quantified entailments with existentially and
                                                 universally quantified variables arise in many problems of verification
                                                 and program analysis. We present PolyQEnt which is a tool for solving
                                                 polynomial quantified entailments in which variables on both sides of
                                                 the implication are real valued or unbounded integers. Our tool provides
                                                 a unified framework for polynomial quantified entailment problems that
                                                 arise in several papers in the literature. Our experimental evaluation over
                                                 a wide range of benchmarks shows the applicability of the tool as well
                                                 as its benefits as opposed to simply using existing SMT solvers to solve
                                                 such constraints.


                                         1     Introduction

                                         Polynomial constraint solving in verification. A fundamental
                                         computational task that arises in several contexts of verification and static
                                         analysis of programs is constraint solving over polynomials. The most prominent
                                         example of an application in program analysis is template-based synthesis [26].
                                         Given a program and a property, a classical approach to proving that the
                                         program satisfies the property is to compute a certificate (i.e. a formal proof)
                                         of the property [21]. This can be achieved by fixing a suitable symbolic
                                         template for the certificate, which allows reducing the program verification
                                         problem to computing values of symbolic template variables that together give
                                         rise to a correct certificate [42]. Such an approach with symbolic templates
                                         being linear or polynomial functions has found extensive applications in
                                         static analysis of programs with linear or polynomial arithmetic, including
                                         termination analysis [13,36,6], invariant generation [12,20,7], reachability [2],
                                         cost analysis [31,27,44], program synthesis [25,23] and probabilistic program
                                         analysis [5,6,10]. This approach has also found extensive applications in other
                                         domains of computer science, e.g. controller verification and synthesis [1,38,37].
                                         Polynomial Quantified Entailments. In all cases mentioned above, the
                                         goal of template-based synthesis is to compute a certificate for the property
2        K. Chatterjee et al.

of interest, where the certificate is computed in the form of a symbolic linear or
polynomial function. The computation is achieved by a reduction to solving a
system of polynomial entailments, i.e. a system of K ∈ N constraints of the form
                                K 
                                ^                                      
                   ∃t ∈ Rm .          ∀x ∈ Rn . Φi (x, t) =⇒ Ψ i (x, t) .
                                i=1

Here, the variables t ∈ Rm present real-valued template coefficients of the
symbolic linear or polynomial function that together define the certificate, and
each Φi and Ψ i is a boolean combination of polynomial inequalities over a vector
x ∈ Rn of program variables. The entailments ∀x ∈ Rn . Φi (x, t) =⇒ Ψ i (x, t)
together encode the necessary properties for the symbolic template polynomial
to define a correct certificate. Hence, any valuation of the variables t ∈ Rm
that gives rise to a solution to the system of constraints above also gives rise
to a concrete instance of the correct certificate. We refer to each entailment
∀x ∈ Rn . Φi (x, t) =⇒ Ψ i (x, t) as a polynomial quantified entailment (PQE), and
to the problem of solving a system of PQEs in eq. (1) as PQE solving.
Solving PQEs via positivity theorems. Initial work on template-based
synthesis has focused on linear programs and linear certificate templates. A
classical approach to solving this problem is to use Farkas’ lemma that considers
implications over linear expressions [16], which has been applied in several
works related to program analysis, e.g. [12,30,5,8]. However, this method was
insufficient for analyzing programs described by polynomials, e.g. programs that
may contain program variable multiplication. A generalization of Farkas’ lemma-
style reasoning to the setting of polynomial constraints and PQEs is achieved by
using positivity theorems, such as Handelman’s [29] and Putinar’s theorem [39].
It was shown in [6,2] that they can be applied towards effectively solving
systems of PQEs, with applications in static analysis of polynomial programs
for termination [6], reachability [2], invariant generation [7], non-termination [9]
properties and for probabilistic program analysis [10,43].
PolyQEnt. PQE solving via positivity theorems is becoming increasingly
popular in static program analysis, however tool support for its integration
into these analyses is non-existent and researchers have relied on their
own implementations. In this work, we present our tool PolyQEnt which
implements methods for solving systems of PQEs over the theories of polynomial
real or unbounded integer arithmetic, based on Handelman’s theorem, Putinar’s
theorem and Farkas’ lemma. We provide efficient implementations of each of
these methods together with practical heuristics that we observed to improve
their performance. At the same time, our tool preserves soundness and relative
completeness guarantees of these translations as established in the previous
results in the literature [2,7]. We envision that PolyQEnt will allow future
research to focus on the design of appropriate certificate templates, whereas
the constraint solving part can be fully delegated to our tool. PolyQEnt is
implemented in Python and publicly available on GitHub 6 . It allows users to
6
    https://github.com/ChatterjeeGroup-ISTA/polyqent
                    PolyQEnt: A Polynomial Quantified Entailment Solver          3

provide constraints as input in the SMT-LIB syntax [4], which is a standard
and widely used input format. PolyQEnt also automates the selection of
the positivity theorem to be used (Handelman’s theorem, Putinar’s theorem
or Farkas’ lemma) in order to achieve most efficient constraint solving while
providing the soundness and relative completeness guarantees.
Experimental evaluation. We experimentally evaluate PolyQEnt on several
benchmarks collected from the literature on termination and non-termination
analysis in polynomial programs, termination of probabilistic programs and
polynomial program synthesis. While all these problems could also be directly
solved using off-the-shelf SMT solvers that support quantifier elimination,
e.g. Z3 [14], our experimental results show significant improvements in runtime
when positivity theorems are used to eliminate quantifier alternation.
Comparison to constrained Horn clauses. The problem of PQE solving
syntactically resembles the more studied problem of constrained Horn clause
(CHC) solving. CHC solving is a classical approach to program verification [24]
with many readily available tools, e.g. [28,32,33,15,18]. However, the goal of
the PQE solving problem is fundamentally different from CHC solving, and
methods for one problem are not readily applicable to the other problem. In CHC
solving, the focus is on computing boolean predicates that together make the
CHC valid. In contrast, template-based synthesis applications discussed above
require computing values of template variables that together define a certificate
conforming to a given template, where the template is specified as a boolean
combination of symbolic linear or polynomial inequalities over program variables.
Hence, what would be viewed as an uninterpreted predicate in CHC solving,
becomes a fixed boolean combination of polynomial inequalities of a specified
maximal polynomial degree in PQE solving. The existing CHC solvers are thus
not applicable to the problem of PQE solving.
    Finally, FreqHorn [19] is a CHC solver that is able to generate interpretations
for uninterpreted predicates in the form of polynomial inequalities. Once
predicate interpretations are generated, the satisfiability of the resulting
interpreted formula is checked by performing quantifier elimination via a
technique based on Model-Based Projections [18], after which the resulting
quantifier-free formula is solved via Gauss-Jordan elimination. Hence, the last
step of FreqHorn’s methodology is also applicable to our problem. The novelty
provided by our PolyQEnt is twofold. First, our quantifier elimination procedure
is based on positivity theorems, which have recently been extensively utilized in
program analysis and verification but for which tooling support is inexistent.
Second, while the methodology of FreqHorn is in principle applicable to our
problem setting, the tool itself only supports CHC solving over uninterpreted
predicates. Hence, we could not perform a direct comparison.


2   Tool Overview
In this section we provide an overview of our tool and discuss details of the
considered problem, the tool’s architecture and its backend design.
4        K. Chatterjee et al.

2.1    Problem Statement

The problem of polynomial quantified entailment (PQE) solving is concerned
with computing a valuation of existentially quantified variables t1 , . . . , tm that
make the following logical formula true
                                  K 
                                  ^                                      
                     ∃t ∈ Rm .          ∀x ∈ Rn . Φi (x, t) =⇒ Ψ i (x, t) .                       (1)
                                  i=1

Here, each Φi and Ψ i is a boolean combination of polynomial inequalities of the
form p(t1 , . . . , tm , x1 , . . . , xn ) ▷◁ 0, with p a polynomial function and ▷◁ ∈ {≥, >}.
We refer to each entailment ∀x ∈ Rn . Φi (x, t) =⇒ Ψ i (x, t) as a polynomial
quantified entailment (PQE), and to the formula in eq. (1) as a system of PQEs.
    In what follows, we consider systems of PQEs defined over the background
theory of real arithmetic. However, our PolyQEnt is also applicable to PQEs
defined over unbounded integer arithmetic (i.e. mathematical integers). While
our presentation will mostly focus on PQEs defined over real arithmetic, in
Section 2.3 we discuss differences that arise in considering unbounded integer
arithmetic and how PolyQEnt addresses them.
Canonical form of PQEs. We say that a PQE ∀x ∈ Rn . Φ(x, t) =⇒
Ψ (x, t) is in the canonical form, if Φ is a conjunction of finitely many
polynomial    inequalities and Ψ is a single polynomial inequality, i.e. if Φ ≡
Vn 
  j=1 pj (t1 , . . . , tm , x1 , . . . , xn ) ▷◁ 0 and Ψ ≡ p(t1 , . . . , tm , x1 , . . . , xn ) ▷◁ 0.
Each PQE can be translated into an equisatisfiable PQE in the canonical form,
defined over the same set of free variables t ∈ Rm and universally quantified
variables x ∈ Rn . This is an important result, as this translation presents the
preprocessing step of our PolyQEnt. The following proposition formally proves
this claim. The proof, together with the procedure employed by PolyQEnt to
achieve this translation, is provided in the Appendix.

Proposition 1. Each PQE can be translated into an equisatisfiable PQE in the
canonical form, defined over the same sets of quantified variables.


2.2    Tool Architecture

Architecture. The tool takes as input a system of PQEs in the form as in
eq. (1). The input is provided in the SMT-LIB format [4], alongside with an
optional config file in the .json format (see the following paragraph for details).
Examples are provided in the tool’s repository. Note that we do not assume
any logical structure of the polynomial inequalities in the PQEs, i.e. polynomial
predicates in each PQE can have arbitrary and/or logical connectives.
    The input files are then parsed and the PQEs are translated to their
equisatisfiable canonical forms as in Proposition 1. PolyQEnt then applies
the appropriate positivity theorem to reduce the problem of PQE solving to
solving a fully existentially quantified system of polynomial constraints (see
                     PolyQEnt: A Polynomial Quantified Entailment Solver              5

Section 2.3 for details). The resulting fully existentially quantified system of
polynomial constraints is then fed to an SMT-solver. In case when the “UNSAT
Core" heuristic is used, PolyQEnt will further process the output of the SMT-
solver (see Section 2.3 for details). Finally, the output of PolyQEnt is either (1)
SAT with a valuation of existentially quantified variables for which the system of
PQEs is valid, (2) UNSAT if the SMT-solver proves unsatisfiability, or (3) Unknown
if the SMT-solver returns unknown.
Configuration file (optional). PolyQEnt has a default (and recommended)
configuration, which does not require the user to provide the config file. However,
we also allow the user to change some of the parameter values used by
PolyQEnt (e.g. the positivity theorems used, the technical parameters, the
SMT-solver, or the heuristics) by providing a .json config file. The technical
details can be found in the tool’s readme file and Appendix C.

Remark 1. We integrated the commands for running Z3 and MathSAT5
into PolyQEnt. However, PolyQEnt also stores the obtained system of
existentially quantified polynomial inequalities in an SMTLIB format output
file which can then be fed to other SMT-solvers.

2.3   Backend Algorithms and Heuristics
We now overview the backend of our tool. Observe that the system of PQEs in
eq. (1) contains quantifier alternation with existential quantification preceding
universal quantification. As mentioned in Section 1, constraints involving such
quantifier alternation can in principle be solved directly by using an off-the-shelf
SMT solver that supports quantifier elimination, e.g. Z3 [14]. However, decision
procedures for solving such constraints are known to be highly unscalable and
a major source of inefficiency [40]. PQE solving can be made significantly more
efficient by first using positivity theorems to eliminate universal quantification
and reduce the problem to solving a purely existentially quantified system of
polynomial constraints. Our experiments in Section 3 support this claim. In what
follows, we describe an overview of positivity theorems and also how PolyQEnt
uses them for quantifier elimination.
Overview of positivity theorems. All three positivity theorems implemented
in PolyQEnt, namely Handelman’s theorem, Putinar’s theorem and Farkas’
lemma, consider constraints of the form
                                                                      
               ∀x ∈ Rn . f1 (x) ▷◁ 0 ∧ · · · ∧ fm (x) ▷◁ 0 =⇒ g(x) ▷◁ 0 ,        (2)

where f1 , . . . , fm , g are polynomials over real-valued variables x1 , . . . , xn and
each ▷◁ ∈ {≥, >} (we discuss the unbounded integer variables case in the
following paragraph). These theorems provide sound translations of the
implication in eq. (2) into a purely existentially quantified system of polynomial
inequalities over newly introduced auxiliary symbolic variables. Translations are
sound in the sense that, if the obtained purely existentially quantified system of
constraints is satisfiable, then the implication in eq. (2) is valid. Moreover, these
6          K. Chatterjee et al.

theorems provide additional sufficient conditions under which the translation
is also complete, i.e. the implication in eq. (2) and the resulting existentially
quantified system are equisatisfiable:
    – Farkas’ lemma. Farkas’ lemma [16,35] provides a sound and complete
      translation if all fi ’s and g are linear expressions.
    – Handelman’s theorem. Handelman’s theorem [29] provides a sound
      translation if all fi ’s are linear expressions and g is a polynomial expression.
      Moreover, the translation can be made complete if in addition all inequalities
      fi (x1 , . . . , xn ) ▷◁ 0 are non-strict, the inequality g(x1 , . . . , xn ) ▷◁ 0 is strict
      and the set {(x1 , . . . , xn ) | ∀1 ≤ i ≤ n. fi (x1 , . . . , xn ) ≥ 0} ⊆ Rn is bounded.
    – Putinar’s Theorem. Putinar’s theorem [39] provides a sound translation
      if all fi ’s and g are polynomial expressions. Moreover, the translation can
      be made complete if in addition all inequalities fi (x1 , . . . , xn ) ▷◁ 0 are non-
      strict, the inequality g(x1 , . . . , xn ) ▷◁ 0 is strict and the set {(x1 , . . . , xn ) |
      ∀1 ≤ i ≤ n. fi (x1 , . . . , xn ) ≥ 0} ⊆ Rn is bounded.
Polynomial unbounded integer arithmetic. While positivity theorems
consider polynomials over real-valued variables, the resulting translations remain
sound under unbounded integer arithmetic. In this case, strict inequalities can
always be treated as non-strict by incrementing the appropriate side of the
inequality by 1, and the above yield sound but incomplete translations. The
usage of positivity theorems in polynomial unbounded integer arithmetic was
discussed in [9]. PolyQEnt provides support for unbounded integer arithmetic
PQEs.
Positivity theorems in PolyQEnt. PolyQEnt implements the
translations via Farkas’ lemma, Handelman’s theorem and Putinar’s theorem,
and uses them to eliminate quantifier alternation in the system of PQEs.
When applied to a PQE in the canonical form, the translation yields a purely
existentially quantified system of polynomial constraints. Hence, the system
of PQEs is translated into a purely existentially quantified formula, with the
first-order variables being the existentially quantified variables t ∈ Rm as in
eq. (1) as well as new symbolic variables introduced by the translation. For
each PQE, the default configuration of PolyQEnt automatically chooses the
positivity theorem that leads to a most efficient translation, while satisfying the
soundness and relative completeness requirements of each theorem listed above,
with Farkas’ Lemma being the most efficient, followed by Handelman’s theorem,
and finally Putinar’s Theorem. Alternatively, by providing the .json config file
as described in Section 2.2, the user can opt for a different positivity theorem to
be used.
    In Appendix D, we provide formal statements of each positivity theorem that
PolyQEnt implements. When invoked in PolyQEnt each theorem has some
input parameters which are set to default values, that can be modified in the
config file (See Appendix D for details).
Heuristics. We conclude by outlining two heuristics that we implemented in
PolyQEnt and that we observed to improve the tool’s performance. The effect
of each heuristic is studied in our experimental evaluation in Section 3:
                   PolyQEnt: A Polynomial Quantified Entailment Solver            7

1. Assume-SAT. For a PQE to be valid, either (1) the left-hand-side of the
   entailment needs to be satisfiable and to imply the right-hand-side at all
   satisfying points, or (2) the left-hand-side of the entailment needs to be
   unsatisfiable. Positivity theorems translate a system of PQEs into a purely
   existentially quantified system of polynomial constraints, whose satisfiability
   implies either (1) or (2). The Assume-SAT heuristic instead collects a system
   of constraints whose satisfiability only implies (1). This heuristic is sound
   but it leads to incompleteness, as (2) also implies that the system of PQEs
   is satisfiable. However, we observed that the Assume-SAT heuristic can
   sometimes considerably reduce the size of the obtained system of constraints,
   which can make the subsequent SMT solving step significantly more efficient.
2. UNSAT core. This heuristic was proposed in [23], a work which uses
   positivity theorems for program synthesis. Since the positivity theorem
   translations introduce a large number of fresh symbolic variables that are
   now existentially quantified, the idea behind the heuristic is to first try to
   solve the resulting system of constraints while adding additional constraints
   that set the values of some of these newly introduced symbolic variables to
   0. If the SMT-solver returns SAT, then the original system is satisfiable as
   well. Otherwise, SMT solvers such as Z3 [14] and MathSAT [11] can return an
   unsatifsiability core, a subset of constraints that are unsatisfiable themselves.
   If the core contains none of the newly added constraints, it implies that the
   original system was unsatifiable. Otherwise, PolyQEnt removes the newly
   added t = 0 constraints that are in the core and repeats this procedure.


3     Experimental Evaluation
We evaluate the performance of our tool on three benchmark sets in the following
three subsections. The goal of our experiments is to illustrate (1) soundness of
the tool, (2) its ability to solve PQEs that arise in program analysis literature,
(3) the necessity of using positivity theorems for quantifier elimination as
opposed to feeding PQEs to an SMT solver directly, and (4) to study the
performance of different combinations of our two heuristics and different SMT
solvers. Benchmarks are provided in the .smt2 format. All the experiments were
conducted on a Debian 11 machine with AMD EPYC 9654 2.40 GHz CPU and
6 GB RAM with a timeout of 180 seconds.
Baselines. In order to illustrate the necessity of using positivity theorems
for quantifier elimination, on all three benchmark sets we compare
PolyQEnt against baseline methods which directly use Z3(v4.13.4) [14] and
CVC5(v1.2.0) [3] to solve the system of PQEs, i.e. without separately performing
quantifier elimination.

3.1   Termination and Non-Termination
The first benchmark set consists of systems of PQEs that arise in termination
analysis of programs. We consider TermComp’23 [22], C-Integer category,
8         K. Chatterjee et al.

benchmark suite that consists of 335 non-recursive programs written in C. Initial
value of every program variable is assumed to be in the range [−1024, 1023]. The
goal is to either prove termination or non-termination of each program.
Extraction of PQEs. We extract PQEs for termination and non-termination
proving as follows:
    For termination proving, we use the template-based synthesis method for
computing ranking functions [2]. For each program, as is common in termination
analysis, we first used ASPIC [17] to generate a supporting invariant with respect
to which ranking function is to be computed. We then use the method of [2] to
extract two systems of PQEs that each encode the ranking function synthesis
problem – one for the linear (polynomial degree 1) and one for the quadratic
(polynomial degree 2) templates. Finally, we run PolyQEnt with Farkas’ lemma
to solve the first system of PQEs, and with Putinar’s theorem to solve the second
system of PQEs, respectively.
    For non-termination proving, we use the template-based synthesis method for
computing a non-termination certificate of [9]. We use the same parameters as in
the ‘best config’ setting of the artifact of [9] to define the template for the non-
termination certificate. We run the method of [9] to generate the system of PQEs
that encodes the non-termination certificate synthesis problem. Finally, to solve
the resulting system of PQEs, we run PolyQEnt with Farkas’ lemma in 101/103
cases where ‘best config’ prescribes linear templates, and with Putinar’s theorem
in 2/103 cases where it prescribes polynomial templates. Results. Table 1 shows
a summary of our results on PolyQEnt’s performance on PQEs coming from
termination analysis. Clearly, PolyQEnt performs far better than using Z3 or
CVC5 directly for quantifier elimination. Comparing performance of different
heuristics, we observe several interesting points:

    – Applying heuristic H1 (Assume-SAT) helps PolyQEnt greatly, especially
      when using MathSAT as the backend solver.
    – Applying heuristic H2 (UNSAT Core) does not prove any unique cases that
      other configurations of PolyQEnt could not prove. However, Z3 solves more
      instances than MathSAT when both are equipped with this heuristic.
    – While Z3 solves more instances of PQEs coming from termination analysis,
      MathSAT outperforms it in solving PQEs coming from non-termination
      analysis. This suggests running several SMT solvers in parallel in order to
      achieve the best results.


Runtime comparison. Fig. 1 plots the number of instances solved by each
tool against runtime. For several benchmarks the direct-Z3 method terminates
nearly instantly. Apart from them, it can be seen that Z3 is faster than MathSAT
in settings where H1 heuristic is not applied, but applying H1 makes MathSAT
slightly more efficient than Z3. Moreover, compared to not using any heuristics,
applying H1 and H2 results in a speed-up in 220 and 32 benchmarks, respectively.
                         PolyQEnt: A Polynomial Quantified Entailment Solver                                       9

                         Base              Base+H1           Base+H2         Base+H1+H2
  Specification                                                                              Dir. Z3   Dir. CVC5
                  MS 5    Z3    U.    MS 5 Z3       U.   MS 5 Z3     U.    MS 5 Z3    U.
    Termination    44    154    154    148 153 153        43   109 113     125 132 145         103        9
  Non-Termination 72      76    78     101    87   103    61    75   76     81   82   89       39         9
  Avg. Time (s)   4.4    3.9    1.6   0.5   2.5   0.5    4.3   3.5   3.4   2.7   3.7   3.6     1.6       19.4
Table 1: Summary of our results on TermComp benchmarks. The Base column
shows the results of PolyQEnt without any heuristics. The next 3 columns
enable heuristics H1(Assume-SAT) and H2(UNSAT Core). The ‘Dir. Z3’ and
‘Dir. CVC5’ columns summarize the results obtained by applying Z3 and CVC5
directly. For each setting, we show the number of instances solved by MathSAT
5 (MS 5), Z3 and their union (U.).




Fig. 1: Performance of PolyQEnt with different settings in comparison to
baselines. Both axes are scaled logarithmically for better visualization. The
leftmost four plots demonstrate the effect of using different solvers and heuristic
settings, and the rightmost plot unionizes solvers to just compare heuristics.


3.2    Almost-Sure Termination
The second benchmark set comes from almost-sure termination proving in
probabilistic programs. We collected benchmarks from two sources: i) 10
benchmarks from [43] (Table 3) and ii) 7 benchmarks from [34]. We choose
these benchmarks because both works consider probabilistic program models of
different applications which are required to be almost-surely terminating.
Extraction of PQEs. To prove almost-sure termination, we use the template-
based synthesis method for computing ranking supermartingales [6]. For each
program, as is common in termination analysis, we used ASPIC [17] and
StInG [41] to generate supporting invariants with respect to which ranking
supermartingale is to be computed. We then fix a quadratic (polynomial
degree 2) template for the ranking supermartingale and use the method of [6] to
extract a system of PQEs that encodes the synthesis problem. Finally, we use
PolyQEnt with Handelman’s theorem to solve the system of PQEs.
Results. Table 2 shows a summary of our results on PolyQEnt’s performance
on PQEs coming from almost-sure termination analysis. Applying Z3 or CVC5
directly is not successful on any of the benchmarks. On the other hand,
10         K. Chatterjee et al.

                            Base              Base+H1           Base+H2          Base+H1+H2
     Benchmark set                                                                                Dir. Z3   Dir. CVC5
                     MS 5    Z3     U.    MS 5 Z3     U.    MS 5 Z3     U.     MS 5 Z3    U.
      From [43]       7      6      7       7    6    7      7     6     7      7    5     7         0         0
      From [34]       6      5      6       5    6    6      5     4     5      6    4     6         0         0
     Avg. Time (s)   10.4   6.1    10.4   9.5   3.5   9.7   10.1   3.4   10.1 10.9   2.0   10.9     NA         NA
                       Table 2: Results on the second benchmark set.
                            Base              Base+H1           Base+H2          Base+H1+H2
     Benchmark Set                                                                                Dir. Z3   Dir. CVC5
                     MS 5    Z3     U.    MS 5 Z3     U.    MS 5 Z3     U.     MS 5 Z3    U.
      From [23]       28     30     30     28    29   29     28    30   30      28   29   29        24         0
     Avg. Time (s)   3.2    2.6    2.6    2.4   2.4   2.4   2.9    2.7   2.6   2.6   2.5   2.5     14.0        NA
                        Table 3: Results on the third benchmark set.

PolyQEnt successfully solves 13 out of 17 instances. Moreover, it can be seen
that in most of the settings, running one SMT-solver alone does not provide the
best results. This again suggests running several SMT solvers in parallel.


3.3      Synthesis

The third benchmark set comes from polynomial program synthesis, where
we collect 32 benchmarks from PolySynth [23]. Each benchmark is a non-
deterministic program that contains holes and a desired specification. PolySynth
uses a template-based technique to synthesize suitable polynomial expressions
for the holes such that the specification is satisfied.
Extraction of PQEs. We first use the method of [23] to extract a system
of PQEs for polynomial program synthesis. For each benchmark, we ran
PolyQEnt using Farkas lemma as well as Handelman’s and Putinar’s theorem
with polynomial degree 2 templates. For brevity, we present a union of these
runs, where we consider the faster setting whenever several of them worked.
Results. Table 3 shows a summary of our results on PolyQEnt’s
performance on PQEs coming from program synthesis. We note
that for two benchmarks (namely, positive_square_with_holes and
positive_square_with_number_holes) the Direct Z3 method could find a
solution while PolyQEnt equipped with Farkas and Handelman could not.
However, using Putinar with polynomial degree 2, PolyQEnt can solve those
instances as well. Other than that, PolyQEnt outperforms the Direct Z3 and
Direct CVC5 approaches both in terms of the number of solved instances and
runtime. Comparing the performance of heuristics, it can be seen that the
UNSAT Core heuristic slightly outperforms the Assume-SAT heuristic.
Concluding Remarks. We presented our tool PolyQEnt for solving systems
of polynomial quantified entailments, a problem that arises in many template-
based synthesis methods for program analysis and verification. The significance
of PolyQEnt is that, for template-based synthesis, it separates the task of
certificate design, which future research can focus on, and the task of polynomial
constraint solving, for which PolyQEnt provides an efficient tool support.
Future work includes studying further heuristics towards making PolyQEnt
even more efficient for solving systems of polynomial quantified entailments.
                     PolyQEnt: A Polynomial Quantified Entailment Solver             11

References

 1. Ahmadi, A.A., Majumdar, A.: Some applications of polynomial optimization in
    operations research and real-time decision making. Optim. Lett. 10(4), 709–729
    (2016)
 2. Asadi, A., Chatterjee, K., Fu, H., Goharshady, A.K., Mahdavi, M.: Polynomial
    reachability witnesses via stellensätze. In: PLDI. pp. 772–787. ACM (2021)
 3. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M.,
    Mohamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A versatile and industrial-
    strength SMT solver. In: Fisman, D., Rosu, G. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 13243, pp. 415–442. Springer (2022).
    https://doi.org/10.1007/978-3-030-99524-9_24, https://doi.org/10.1007/
    978-3-030-99524-9_24
 4. Barrett, C., Fontaine, P., Tinelli, C.: The Satisfiability Modulo Theories Library
    (SMT-LIB). www.SMT-LIB.org (2016)
 5. Chakarov, A., Sankaranarayanan, S.: Probabilistic program analysis with
    martingales. In: CAV. Lecture Notes in Computer Science, vol. 8044, pp. 511–526.
    Springer (2013)
 6. Chatterjee, K., Fu, H., Goharshady, A.K.: Termination analysis of probabilistic
    programs through positivstellensatz’s. In: CAV (1). Lecture Notes in Computer
    Science, vol. 9779, pp. 3–22. Springer (2016)
 7. Chatterjee, K., Fu, H., Goharshady, A.K., Goharshady, E.K.: Polynomial invariant
    generation for non-deterministic recursive programs. In: PLDI. pp. 672–687. ACM
    (2020)
 8. Chatterjee, K., Fu, H., Novotný, P., Hasheminezhad, R.: Algorithmic analysis of
    qualitative and quantitative termination problems for affine probabilistic programs.
    ACM Trans. Program. Lang. Syst. 40(2), 7:1–7:45 (2018)
 9. Chatterjee, K., Goharshady, E.K., Novotný, P., Zikelic, D.: Proving non-
    termination by program reversal. In: PLDI. pp. 1033–1048. ACM (2021)
10. Chatterjee, K., Novotný, P., Zikelic, D.: Stochastic invariants for probabilistic
    termination. In: POPL. pp. 145–160. ACM (2017)
11. Cimatti, A., Griggio, A., Schaafsma, B.J., Sebastiani, R.: The mathsat5 smt solver.
    In: International Conference on Tools and Algorithms for the Construction and
    Analysis of Systems. pp. 93–107. Springer (2013)
12. Colón, M., Sankaranarayanan, S., Sipma, H.: Linear invariant generation using non-
    linear constraint solving. In: CAV. Lecture Notes in Computer Science, vol. 2725,
    pp. 420–432. Springer (2003)
13. Colón, M., Sipma, H.: Synthesis of linear ranking functions. In: TACAS. Lecture
    Notes in Computer Science, vol. 2031, pp. 67–81. Springer (2001)
14. De Moura, L., Bjørner, N.: Z3: An efficient smt solver. In: International conference
    on Tools and Algorithms for the Construction and Analysis of Systems. pp. 337–
    340. Springer (2008)
15. Dietsch, D., Heizmann, M., Hoenicke, J., Nutz, A., Podelski, A.: Ultimate
    treeautomizer (CHC-COMP tool description). In: HCVS/PERR@ETAPS.
    EPTCS, vol. 296, pp. 42–47 (2019)
12      K. Chatterjee et al.

16. Farkas, J.: Theorie der einfachen ungleichungen. Journal für die reine und
    angewandte Mathematik (Crelles Journal) 1902(124), 1–27 (1902)
17. Feautrier, P., Gonnord, L.: Accelerated invariant generation for C programs with
    aspic and c2fsm. In: Proceedings of the Tools for Automatic Program AnalysiS,
    TAPAS@SAS 2010, Perpignan, France, September 17, 2010. Electronic Notes in
    Theoretical Computer Science, vol. 267, pp. 3–13 (2010)
18. Fedyukovich, G., Prabhu, S., Madhukar, K., Gupta, A.: Solving constrained horn
    clauses using syntax and data. In: FMCAD. pp. 1–9. IEEE (2018)
19. Fedyukovich, G., Prabhu, S., Madhukar, K., Gupta, A.: Quantified invariants
    via syntax-guided synthesis. In: Dillig, I., Tasiran, S. (eds.) Computer Aided
    Verification - 31st International Conference, CAV 2019, New York City, NY,
    USA, July 15-18, 2019, Proceedings, Part I. Lecture Notes in Computer
    Science, vol. 11561, pp. 259–277. Springer (2019). https://doi.org/10.1007/
    978-3-030-25540-4_14, https://doi.org/10.1007/978-3-030-25540-4_14
20. Feng, Y., Zhang, L., Jansen, D.N., Zhan, N., Xia, B.: Finding polynomial loop
    invariants for probabilistic programs. In: ATVA. Lecture Notes in Computer
    Science, vol. 10482, pp. 400–416. Springer (2017)
21. Floyd, R.W.: Assigning meanings to programs. In: Program Verification:
    Fundamental Issues in Computer Science, pp. 65–81. Springer (1993)
22. Frohn, F., Giesl, J., Moser, G., Rubio, A., Yamada, A., et al.: Termination
    competition 2023 (2023), https://termination-portal.org/wiki/Termination_
    Competition_2023
23. Goharshady, A.K., Hitarth, S., Mohammadi, F., Motwani, H.J.: Algebro-geometric
    algorithms for template-based synthesis of polynomial programs. Proc. ACM
    Program. Lang. 7(OOPSLA1), 727–756 (2023)
24. Grebenshchikov, S., Lopes, N.P., Popeea, C., Rybalchenko, A.: Synthesizing
    software verifiers from proof rules. In: PLDI. pp. 405–416. ACM (2012)
25. Gulwani, S., Jha, S., Tiwari, A., Venkatesan, R.: Synthesis of loop-free programs.
    In: PLDI. pp. 62–73. ACM (2011)
26. Gulwani, S., Srivastava, S., Venkatesan, R.: Program analysis as constraint solving.
    In: PLDI. pp. 281–292. ACM (2008)
27. Gulwani, S., Zuleger, F.: The reachability-bound problem. In: PLDI. pp. 292–304.
    ACM (2010)
28. Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The seahorn verification
    framework. In: CAV (1). Lecture Notes in Computer Science, vol. 9206, pp. 343–
    361. Springer (2015)
29. Handelman, D.: Representing polynomials by positive linear functions on compact
    convex polyhedra. Pacific Journal of Mathematics 132(1), 35–62 (1988)
30. Heizmann, M., Hoenicke, J., Leike, J., Podelski, A.: Linear ranking for linear lasso
    programs. CoRR abs/1401.5347 (2014)
31. Hoffmann, J., Aehlig, K., Hofmann, M.: Multivariate amortized resource analysis.
    ACM Trans. Program. Lang. Syst. 34(3), 14:1–14:62 (2012)
32. Hojjat, H., Rümmer, P.: The ELDARICA horn solver. In: FMCAD. pp. 1–7. IEEE
    (2018)
33. Komuravelli, A., Gurfinkel, A., Chaki, S.: Smt-based model checking for recursive
    programs. Formal Methods Syst. Des. 48(3), 175–205 (2016)
34. Kura, S., Urabe, N., Hasuo, I.: Tail probabilities for randomized program runtimes
    via martingales for higher moments. In: TACAS (2). Lecture Notes in Computer
    Science, vol. 11428, pp. 135–153. Springer (2019)
35. Matoušek, J., Gärtner, B.: Understanding and using linear programming, vol. 1.
    Springer (2007)
                     PolyQEnt: A Polynomial Quantified Entailment Solver            13

36. Podelski, A., Rybalchenko, A.: A complete method for the synthesis of linear
    ranking functions. In: VMCAI. Lecture Notes in Computer Science, vol. 2937,
    pp. 239–251. Springer (2004)
37. Prajna, S., Jadbabaie, A.: Safety verification of hybrid systems using barrier
    certificates. In: HSCC. Lecture Notes in Computer Science, vol. 2993, pp. 477–
    492. Springer (2004)
38. Prajna, S., Papachristodoulou, A., Parrilo, P.A.: Introducing sostools: A general
    purpose sum of squares programming solver. In: Proceedings of the 41st IEEE
    Conference on Decision and Control, 2002. vol. 1, pp. 741–746. IEEE (2002)
39. Putinar, M.: Positive polynomials on compact semi-algebraic sets. Indiana
    University Mathematics Journal 42(3), 969–984 (1993)
40. Renegar, J.: On the computational complexity and geometry of the first-
    order theory of the reals. part iii: Quantifier elimination. Journal of Symbolic
    Computation 13(3), 329–352 (1992). https://doi.org/https://doi.org/10.
    1016/S0747-7171(10)80005-7
41. Sankaranarayanan, S., Sipma, H.B., Manna, Z.: Constraint-based linear-relations
    analysis. In: Static Analysis, 11th International Symposium, SAS 2004, Verona,
    Italy, August 26-28, 2004, Proceedings. Lecture Notes in Computer Science,
    vol. 3148, pp. 53–68. Springer (2004)
42. Srivastava, S., Gulwani, S., Foster, J.S.: Template-based program verification and
    program synthesis. Int. J. Softw. Tools Technol. Transf. 15(5-6), 497–518 (2013)
43. Wang, P., Fu, H., Goharshady, A.K., Chatterjee, K., Qin, X., Shi, W.: Cost analysis
    of nondeterministic probabilistic programs. In: PLDI. pp. 204–220. ACM (2019)
44. Zikelic, D., Chang, B.E., Bolignano, P., Raimondi, F.: Differential cost analysis
    with simultaneous potentials and anti-potentials. In: PLDI. pp. 442–457. ACM
    (2022)
14         K. Chatterjee et al.

A    Proof of Proposition 1
Proposition 1. Each PQE can be translated into an equisatisfiable PQE in the
canonical form, defined over the same sets of quantified variables.
Proof. Consider a system of PQEs as in eq. (1)
                                       K 
                                       ^                                       
                        ∃t ∈ Rm .             ∀x ∈ Rn . Φi (x, t) =⇒ Ψ i (x, t) ,
                                       i=1

with each Φi and Ψ i being an arbitrary boolean combination of polynomial
inequalities over x and t. It is a classical result that every formula in propositional
logic can be translated into an equivalent formula in conjunctive normal form
(CNF). Hence, we can translate each Φi (x, t) =⇒ Ψ i (x, t) into an equisatisfiable
formula of the form
                                                   mi _
                                                   ^  ni
                                  Θi (x, t) =              (pij,l (x, t) ▷◁ij,l 0),
                                                   j=1 l=1

where each pij,l (x, t) ▷◁ij,l 0 is a polynomial inequality. We then have
                 K 
                 ^                                       
  ∃t ∈ Rm .             ∀x ∈ Rn . Φi (x, t) =⇒ Ψ i (x, t)
                 i=1
                                 K 
                                 ^                            
≡∃t ∈ Rm . ∀x ∈ Rn .                   Φi (x, t) =⇒ Ψ i (x, t)
                                 i=1
                                     mi _
                                 K  ^
                                 ^      ni                                
            m             n
≡∃t ∈ R . ∀x ∈ R .                                 (pij,l (x, t) ▷◁ij,l 0)
                                 i=1   j=1 l=1
                                   mi  _
                                 K ^
                                 ^      ni                                
≡∃t ∈ Rm . ∀x ∈ Rn .                               (pij,l (x, t) ▷◁ij,l 0)
                                 i=1 j=1     l=1
                                   mi
                                 K ^
                                 ^
≡∃t ∈ Rm . ∀x ∈ Rn .
                                 i=1 j=1
                                                                                                     
         (−pij,1 (x, t) ▷◁ij,l   0) ∧ · · · ∧ (−pij,1 (x, t) ▷◁ij,ni −1 0) =⇒ (pij,1 (x, t) ▷◁ij,ni 0) .

The last formula yields an equisatisfiable system of PQEs with each PQE in
the canonical form. Note that the above also yields a procedure for translating
individual PQEs into their canonical forms. This concludes the proof.         ⊔
                                                                              ⊓


B    Example
Example 1. To illustrate how the problem of solving a system of PQEs arises
in template-based synthesis for program analysis, we consider an example of
                    PolyQEnt: A Polynomial Quantified Entailment Solver            15

                       ∃t1 , t2 , t3 , t4 ∈ R
Invariant :                                                           
     -1024 ≤ x ≤ 1023 ∀x ∈ R, − 1024 ≤ x ≤ 1023 ⇒ t1 x + t2 ≥ 0
                      
l1 : while x ≥ 1 do 
                      
                                  
                       ∀x ∈ R, − 1024 ≤ x ≤ 1023 ∧ x ≥ 1
                      
                      
         x := x -1    
                      
                                                                                   
      done                  ⇒ t1 (x − 1) + t2 ≥ 0 ∧ t1 (x − 1) + t2 ≤ t1 x + t2 − 1
lt :                  
                                  
                       ∀x ∈ R, − 1024 ≤ x ≤ 1023 ∧ x < 1
                      
                      
                      
                      
                      
                                                                       
                            ⇒ t3 x + t4 ≥ 0 ∧ t3 x + t4 ≤ t1 x + t2 − 1
                      
                      

Fig. 2: A simple program (left) and the corresponding system of polynomial Horn
clauses for computing ranking function that proves termination (right).


proving termination of programs by computing ranking functions. Consider
the program in Fig. 1 (left) and termination as a specification. We describe
the three steps of the classical template-based method for synthesizing linear
ranking functions [12]. We consider linear programs and ranking functions
for the simplicity of the example, however this method was extended to the
setting of polynomial programs and ranking functions in [6] and is supported in
PolyQEnt:
 1. To find a linear ranking function, we first fix a symbolic linear expression
    template for each cutpoint location in the program:
                                    (
                                     t1 x + t2 if l = l1
                           Tl (x) =
                                     t3 x + t4 if l = lt

    where t1 , t2 , t3 and t4 are the symbolic template variables.
 2. A system of PQEs in Fig. 1 (right) encodes that T is a ranking function.
 3. Hence, any valuation of template variables t1 , t2 , t3 , t4 that makes all PQEs
    valid gives rise to a correct ranking function for the program in Fig. 1 (left).



C    Config File
PolyQEnt has a default (and recommended) configuration, which does not
require the user to provide the config file. However, we also allow the user to
change some of the parameter values used by PolyQEnt and the set of heuristics
used by providing a .json config file:

 1. Positivity theorem to be used (farkas, handelman or putinar). The
    default configuration of PolyQEnt automatically chooses the most efficient
    positivity theorem to be applied while preserving soundness and relative
    completeness guarantees (see Section 2.3 for details). However, this optional
    parameter allows the user to opt for a different positivity theorem whose
    application is sound but not relatively complete, but may sometime lead to
    a more efficient constraint solving.
16     K. Chatterjee et al.




                       Fig. 3: Architecture of PolyQEnt


2. Parameters of the positivity theorem to be used. See Appendix D for details.
   The default parameter values are also specified in Appendix D.
3. The set of heuristics (if any) to be applied. The default configuration applies
   the Assume-SAT heuristic (see Section 2.3 for details).
4. An SMT-solver to be used to solve the fully existentially quantified system
   of polynomial constraints resulting from applying the positivity theorem.
   The default configuration uses z3 [14], however PolyQEnt also supports
   mathsat [11].
5. Background theory to be considered. The default is real arithmetic, however
   the config file allows the user to choose unbounded integer arithmetic.


D    Positivity Theorems

We now present the formal details behind the positivity theorems implemented
in PolyQEnt. Provided are theorem statements, their use in PolyQEnt and
tool parameters, the default configuration parameter values and how to change
parameter values. All theorem claims are adopted from [2], and we refer the
reader to [2] for more details. Reading this section is optional for the users
interested solely in running PolyQEnt with the default configuration.
Farkas’ lemma. We start by presenting Farkas’ lemma, which is utilized by
PolyQEnt when both the left-hand-side (LHS) and the right-hand-side (RHS)
of PQEs in canonical form are specified in terms of linear inequalities.

Theorem 1 (Farkas’ lemma [16]). Consider a set V = {x1 , . . . , xn } of real-
valued variables and the following system of m linear inequalities over V
                     
                       a + a1,1 · x1 + . . . + a1,n · xn ▷◁1 0
                      1,0
                     
                     
                                            ..
                Φ :=                         .
                     
                     
                     a
                        m,0  + am,1 · x1 + .  . . + am,n · xn ▷◁m 0

where each ▷◁i ∈ {>, ≥}. Exactly one of the following is true
                    PolyQEnt: A Polynomial Quantified Entailment Solver            17

F1) Φ is satisfiable. Then, Φ entails the linear inequality

                          ψ := c0 + c1 · x1 + · · · + cn · xn ≥ 0

    if and only if ψ can be written as non-negative linear combination of the
    inequalities in Φ and 1 ≥ 0, i.e. if and only if there exist non-negative real-
    valued coefficients y0 , . . . , ym such that:
                                           Pm
                                         + i=1 yi · ai,0
                                c0 = y 0 P
                                          m
                                   c1 = i=1 yi · ai,1
                                           ..
                                        Pm.
                                  cn = i=1 yi · ai,n .

F2) Φ is unsatisfiable and −1 ≥ 0 can be derived as above.
F3) Φ is unsatisfiable and 0 > 0 can be derived as above, with at least one of the
   strict inequalities having strictly positive coefficient yi > 0.

    If the inequality ψ := c0 + c1 · x1 + · · · + cn · xn > 0 is strict, then the case
(F1) should be modified by requiring at least one coefficient yi with ▷◁i = {>} to
be strictly positive, i.e. yi > 0.

    Given a PQE in canonical form where both the LHS and the RHS are specified
in terms of linear inequalities, Farkas’ lemma specifies the necessary and sufficient
conditions for the LHS of the PQE to be unsatisfiable, i.e. (F2) and (F3), as
well as for the LHS to be satisfiable and to entail the RHS, i.e. (F1). Hence,
PolyQEnt translates each such PQE into a system of constraints defined by
the Farkas’ lemma. The application of Farkas’ lemma in PolyQEnt introduces
no new parameter values.
Handelman’s theorem. Next, we present Handelman’s theorem. PolyQEnt
utilizes this theorem when all inequalities on the LHS of a PQE in canonical
form are linear, but the inequality on the RHS contains a polynomial of degree
at least 2. In order to formally present Handelman’s theorem, we first need to
define the notion of a monoid of a system of linear inequalities. Consider a set
V = {x1 , . . . , xn } of real-valued variables and the following system of linear
inequalities over V
                             Φ := {f1 ▷◁1 0, . . . , fm ▷◁m 0},

where each fi = ai,0 + ai,1 · x1 + . . . + ai,n · xi and each ▷◁i ∈ {>, ≥}. The monoid
of Φ of degree d, denoted Monoid(Φ, d), is the set of all polynomials over V of
degree at most d that can be expressed as a product of linear expressions in Φ,
i.e.
                                  nY  m                        m
                                                               X        o
             Monoid(Φ, d) :=              fiki |∀i : ki ∈ N0 ∧    ki ≤ d .
                                   i=1                     i=1

We are now ready to formally state Handelman’s theorem.
18      K. Chatterjee et al.

Theorem 2 (Handelman’s theorem [29]). Consider a set V = {x1 , . . . , xn }
of real-valued variables and the following system of m linear inequalities over V
                     
                       a + a1,1 · x1 + . . . + a1,n · xn ▷◁1 0
                      1,0
                     
                     
                                            ..
                Φ :=                         .                     .
                     
                     
                         m,0 + am,1 · x1 + . . . + am,n · xn ▷◁m 0
                     a

where each ▷◁i ∈ {>, ≥}. Suppose that Φ is satisfiable. Then, Φ entails polynomial
                                                                     ¯ non-negative real
inequality g(x1 , . . . , xn ) ▷◁ 0 if there exist a natural number d,
                                                            ¯
numbers y0 , y1 , . . . yu and h1 , . . . , hu ∈ Monoid(Φ, d) such that
                                                  u
                                                  X
                                      g = y0 +          yi · hi .
                                                  i=1

Moreover, if the satisfiability set of Φ is bounded in Rn , the linear inequalities
▷◁1 , . . . , ▷◁m are all non-strict and the polynomial inequality ▷◁ is strict, then
Φ entails polynomial inequality g(x1 , . . . , xn ) > 0 if and only if there exist
a natural number d,      ¯ non-negative real numbers y0 , y1 , . . . yu and h1 , . . . , hu ∈
                  ¯                    Pu
Monoid(Φ, d) such that g = y0 + i=1 yi · hi .
     Given a PQE in canonical form where inequalities on the LHS are linear
but the inequality on the RHS is at least a degree 2 polynomial, Handelman’s
theorem specifies the sufficient conditions for the LHS to be satisfiable and to
entail the RHS. On the other hand, the conditions for the LHS to be unsatisfiable
are as in the Farkas’ Lemma, i.e. conditions (F2) and (F3) in Theorem 1. Hence,
PolyQEnt translates each such PQE into a system of constraints defined by
Handelman’s theorem as well as (F2) and (F3) in Farkas’ lemma.
     The translation is sound. The translation is also relatively complete, subject
to the assumptions stated in Theorem 2, i.e. that the satisfiability set of the
inequalities on the LHS is bounded, the inequalities on the LHS are non-strict
and the inequality on the RHS is strict.
PolyQEnt parameters for Handelman’s theorem. PolyQEnt defines
a parameter for the maximal polynomial degree d¯ of the monoid to be used
in the translation. The value used by the PolyQEnt default configuration is
the maximal polynomial degree appearing in the system of PQEs. In the config
file, this value can be changed by setting a new value of the degree_of_sat
parameter.
Putinar’s theorem. Finally, we present Putinar’s theorem, and its extension
for the case when the LHS of the entailment is unsatisfiable which was proved
in [2]. PolyQEnt utilizes these theorems when both the LHS and the RHS of
a PQE in canonical form contain at least one polynomial of degree at least 2. In
what follows, we sayPthat a polynomial h is sum-of-squares, if it can be written
as a finite sum h = h2j for squares of polynomials hj .
Theorem 3 (Putinar’s theorem [39]). Consider a set V = {x1 , . . . , xn } of
real-valued variables and the following system of m polynomial inequalities over V
               Φ := {f1 (x1 , . . . , xn ) ▷◁1 0, . . . , fm (x1 , . . . , xn ) ▷◁m 0}.
                      PolyQEnt: A Polynomial Quantified Entailment Solver                19

where each ▷◁i ∈ {>, ≥}. Suppose that Φ is satisfiable. Then, Φ entails a
polynomial inequality g(x1 , . . . , xn ) ▷◁ 0 if there exist positive real number y0
and sum-of-squares polynomials h0 , . . . , hm such that
                                                    m
                                                    X
                                 g = y0 + h0 +             hi · fi .
                                                     i=1

Moreover, if the satisfiability set of at least one fi ≥ 0 is topologically compact
(i.e. closed and bounded), the linear inequalities ▷◁1 , . . . , ▷◁m are all non-strict
and the polynomial inequality ▷◁ is strict, then Φ entails polynomial inequality
g(x1 , . . . , xn ) > 0 if and only if there exist positive real P
                                                                 number y0 and sum-of-
                                                                   m
squares polynomials h0 , . . . , hm such that g = y0 + h0 + i=1 hi · fi .

Theorem 4 (Unsatisfiability theorem [2]). Consider a set V                        =
{x1 , . . . , xn } of real-valued variables and the following system of m polynomial
inequalities over V

              Φ := {f1 (x1 , . . . , xn ) ▷◁1 0, . . . , fm (x1 , . . . , xn ) ▷◁m 0}.

where each ▷◁i ∈ {>, ≥}. Then Φ is unsatisfiable if and only if at least one of the
following two conditions holds:
U1) There exist a positive real number y0 and sum-of-square polynomials
   h0 , . . . , hm such that
                                            m
                                            X
                             −1 = y0 + h0 +   hi · fi
                                                           i=1

U2) There exist d ∈ N0 and polynomials h′1 , . . . ,P
                                                    h′m over V ∪{w1 , . . . , wm }, such
                                                      m
   that for some j in which ▷◁j ∈ {>}, wj = i=1 h′i · (fi − wi2 ).
                                        2·d


    Given a PQE in canonical form where both the LHS and the RHS contain
a polynomial of degree at least 2, Putinar’s theorem specifies the sufficient
conditions for the LHS to be satisfiable and to entail the RHS. On the other
hand, the conditions for the LHS to be unsatisfiable are given by conditions
(U1) and (U2) in Theorem 4. Hence, PolyQEnt translates each such PQE into
a system of constraints defined by Putinar’s theorem and Theorem 4.
    The translation is sound. The translation is also relatively complete, subject
to the assumptions stated in Theorem 3, i.e. that the satisfiability set of at least
one inequality on the LHS is topologically compact, that the inequalities on the
LHS are non-strict and the inequality on the RHS is strict.
PolyQEnt parameters for Putinar’s theorem. PolyQEnt defines
the following parameters when invoking Putinar’s theorem. In the default
configuration, the values of all these parameters are set to the maximal
polynomial degree appearing in the system of PQEs, and the values of these
parameters can be changed by modifying the config file:
 – Maximum degree of hi ’s in Theorem 3. In the config file, degree_of_sat
   represents this parameter.
20     K. Chatterjee et al.

 – Maximum degree of hi ’s in Theorem 4 (condition (U1)). In the config file,
   degree_of_nonstrict_unsat represents this parameter.
 – Maximum degree of hi ’s in Theorem 4 (condition (U2)). In the config file,
   degree_of_strict_unsat represents this parameter.
 – Value of d in Theorem 4 (condition (U2)). In the config file,
   max_d_of_strict represents this parameter.

Remark 2 (Assume-SAT). Heuristic Assume-SAT removes the conditions that
consider the case when the LHS of a PQE is unsatisfiable in all the previous
theorems. If Farkas’ lemma or Handelman’s theorem is applied, PolyQEnt
omits the conditions (F2) and (F3) in Theorem 1. If Putinar’s theorem is applied,
PolyQEnt omits the conditions (U1) and (U2) in Theorem 4.
