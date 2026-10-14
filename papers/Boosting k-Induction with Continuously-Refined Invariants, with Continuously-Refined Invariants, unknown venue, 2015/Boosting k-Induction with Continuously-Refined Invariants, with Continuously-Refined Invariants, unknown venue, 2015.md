                  Boosting k-Induction
           with Continuously-Refined Invariants

                 Dirk Beyer, Matthias Dangl, and Philipp Wendler

                         University of Passau, Passau, Germany




        Abstract. k-induction is a promising technique to extend bounded
        model checking from falsiﬁcation to veriﬁcation. In software veriﬁcation,
        k-induction works only if auxiliary invariants are used to strengthen the
        induction hypothesis. The problem that we address is to generate such
        invariants (1) automatically without user-interaction, (2) eﬃciently such
        that little veriﬁcation time is spent on the invariant generation, and
        (3) that are suﬃciently strong for a k-induction proof. We boost the
        k-induction approach to signiﬁcantly increase eﬀectiveness and eﬃciency
        in the following way: We start in parallel to k-induction a data-ﬂow-
        based invariant generator that supports dynamic precision adjustment
        and reﬁne the precision of the invariant generator continuously during
        the analysis, such that the invariants become increasingly stronger. The
        k-induction engine is extended such that the invariants from the invariant
        generator are injected in each iteration to strengthen the hypothesis. The
        new method solves the above-mentioned problem because it (1) automat-
        ically chooses an invariant by step-wise reﬁnement, (2) starts always with
        a lightweight invariant generation that is computationally inexpensive,
        and (3) reﬁnes the invariant precision more and more to inject stronger
        and stronger invariants into the induction system. We present and eval-
        uate an implementation of our approach, as well as all other existing
        approaches, in the open-source veriﬁcation-framework CPAchecker.
        Our experiments show that combining k-induction with continuously-
        reﬁned invariants signiﬁcantly increases eﬀectiveness and eﬃciency, and
        outperforms all existing implementations of k-induction-based veriﬁca-
        tion of C programs in terms of successful results.


1     Introduction

Advances in software veriﬁcation in recent years have lead to increased eﬀorts
towards applying formal veriﬁcation methods to industrial software, in par-
ticular operating-systems code [3, 4, 34]. One model-checking technique that is
implemented by half of the veriﬁers that participated in the 2015 Competition
on Software Veriﬁcation [7] is bounded model checking (BMC) [16,17,22]. For
unbounded systems, BMC can be used only for falsiﬁcation, not for veriﬁca-
tion [15]. This limitation to falsiﬁcation can be overcome by combining BMC
    A preliminary version of this article appeared as technical report [8].


c Springer International Publishing Switzerland 2015
D. Kroening and C.S. Păsăreanu (Eds.): CAV 2015, Part I, LNCS 9206, pp. 622–640, 2015.
DOI: 10.1007/978-3-319-21690-4 42
                   Boosting k-Induction with Continuously-Reﬁned Invariants     623

with mathematical induction and thus extending it to veriﬁcation [26]. Unfor-
tunately, inductive approaches are not always powerful enough to prove the
required veriﬁcation conditions, because not all program invariants are induc-
tive [2]. Using the more general k-induction [38] instead of standard induction is
more powerful [37] and has already been implemented in the DMA-race analy-
sis tool Scratch [27] and in the software veriﬁer Esbmc [35]. Nevertheless,
additional supportive measures are often required to guide k-induction and take
advantage of its full potential [25]. Our goal is to provide a powerful and com-
petitive approach for reliable, general-purpose software veriﬁcation based on
BMC and k-induction, implemented in a state-of-the-art software-veriﬁcation
framework.
    Our contribution is a new combination of k-induction-based model check-
ing with automatically-generated continuously-reﬁned invariants that are used to
strengthen the induction hypothesis, which increases the eﬀectiveness and eﬃ-
ciency of the approach. BMC and k-induction are combined in an algorithm
that iteratively increments the induction parameter k (iterative deepening). The
invariant generation runs in parallel to the k-induction proof construction, start-
ing with relatively weak (but inexpensive to compute) invariants, and increasing
the strength of the invariants over time as long as the analysis continues. The
k-induction-based proof construction adopts the currently known set of invari-
ants in every new proof attempt. This approach can verify easy problems quickly
(with a small initial k and weak invariants), and is able to verify complex prob-
lems by increasing the eﬀort (by incrementing k and searching for stronger invari-
ants). Thus, it is both eﬃcient and eﬀective. In contrast to previous work [35], the
new approach is sound. We implemented our approach as part of the open-source
software-veriﬁcation framework CPAchecker [12], and we perform an extensive
experimental comparison of our implementation against the two existing tools that
use k-induction and against other common software-veriﬁcation approaches.
Contributions. We make the following contributions:
• a novel approach for providing continuously-reﬁned invariants from data-ﬂow
  analysis with precision adjustment in order to repeatedly inject invariants to
  k-induction,
• an eﬀective and eﬃcient tool implementation of a framework for software
  veriﬁcation with k-induction that allows to express all existing approaches to
  k-induction in a uniform, module-based, conﬁgurable architecture, and
• an extensive experimental evaluation of (a) all approaches and their imple-
  mentations in the framework, (b) the two existing k-induction tools Cbmc
  and Esbmc, and (c) the two diﬀerent approaches predicate analysis and value
  analysis; the result being that the new technique outperforms all existing
  k-induction-based approaches to software veriﬁcation.
Availability of Data and Tools. Our experiments are based on benchmark
veriﬁcation tasks from the 2015 Competition on Software Veriﬁcation. All bench-
marks, tools, and results of our evaluation are available on a supplementary web
page1 .
1
    http://www.sosy-lab.org/∼dbeyer/cpa-k-induction/
    (successfully evaluated by the CAV 2015 Artifact Evaluation Committee)
624           D. Beyer, M. Dangl, and P. Wendler

 1    int main() {                                  1   int main() {
 2      unsigned int x1 = 0, x2 = 0;                2     unsigned int x1 = 0, x2 = 0;
 3      int s = 1;                                  3     int s = 1;
 4                                                  4
 5        while (nondet()) {                        5       while (nondet()) {
 6          if (s == 1) x1++;                       6         if (s == 1) x1++;
 7          else if (s == 2) x2++;                  7         else if (s == 2) x2++;
 8                                                  8
 9            s++;                                  9           s++;
10            if (s == 5) s = 1;                   10           if (s == 5) s = 1;
11                                                 11       }
12            if ((s == 1) && (x1 != x2)) {        12
13              // Valid safety property           13       if (s >= 4) {
14              ERROR: return 1;                   14         // Violation: s may be 4
15            }                                    15         ERROR: return 1;
16        }                                        16       }
17    }                                            17   }


Fig. 1.   Safe    example     program              Fig. 2. Unsafe example program
example-safe, which cannot be                      example-unsafe,   where   some
proven with existing k-induction-based             approaches may produce a wrong
approaches                                         proof
Example. We illustrate the problem of k-induction that we address, and the
strength of our approach, on two example programs. Both programs encode an
automaton, which is typical, e.g., for software that implements a communication
protocol. The automaton has a ﬁnite set of states, which is encoded by variable s,
and two data variables x1 and x2. There are some state-dependent calculations
(lines 6 and 7 in both programs) that alternatingly increment x1 and x2, and a
calculation of the next state (lines 9 and 10 in both programs). The state variable
cycles through the range from 1 to 4. These calculations are done in a loop with
a non-deterministic number of iterations. Both programs also contain a safety
property (the label ERROR should not be reachable). The program example-safe
in Fig. 1 checks that in every fourth state, the values of x1 and x2 are equal; it
satisﬁes the property. The program example-unsafe in Fig. 2 checks that when
the loop exits, the value of state variable s is not greater or equal to 4; it violates
the property.
    First, note that the program example-safe is diﬃcult or impossible to prove
with many classical software-veriﬁcation approaches other than k-induction:
(1) BMC cannot prove safety for this program because the loop may run
arbitrarily long. (2) Explicit-state model checking fails because of the huge
state space (x1 and x2 can get arbitrarily large). (3) Predicate analysis with
counterexample-guided abstraction reﬁnement (CEGAR) and interpolation is
able to prove safety, but only if the predicate x1 = x2 gets discovered. If
the interpolants contain instead only predicates such as x1 = 1, x2 = 1,
x1 = 2, etc., the predicate analysis will not terminate. Which predicates
get discovered is hard to control and usually depends on internal interpola-
tion heuristics of the satisﬁability-modulo-theory (SMT) solver. (4) Traditional
1-induction is also not able to prove the program safe because the assertion
is checked only in every fourth loop iteration (when s equals 1). Thus, the
induction hypothesis is too weak (the program state s = 4, x1 = 0, x2 = 1
is a counterexample for the step case in the induction proof).
                  Boosting k-Induction with Continuously-Reﬁned Invariants       625

    Intuitively, this program should be provable by k-induction with a k of at
least 4. However, for every k, there is a counterexample to the inductive-step
case that refutes the proof. For such a counterexample, set s = −k, x1 = 0,
x2 = 1 at the beginning of the loop. Starting in this state, the program would
increment s k times (induction hypothesis) and then reach s = 1 with property-
violating values of x1 and x2 in iteration k + 1 (inductive step). It is clear that s
can never be negative, but this fact is not present in the induction hypothesis,
and thus, the proof fails. This illustrates the general problem of k-induction-
based veriﬁcation: safety properties often do not hold in unreachable parts of the
state space of a program, and k-induction alone does not distinguish between
reachable and unreachable parts of the state space. Therefore, approaches based
on k-induction without auxiliary invariants will fail to prove safety for program
example-safe.
    This program could of course be veriﬁed more easily if it were rewritten to
contain a stronger safety property such as s ≥ 1∧s ≤ 4∧(s = 2 ⇒ x1 = x2 +1)∧
(s = 2 ⇒ x1 = x2 ) (which is a loop invariant and allows a proof by 1-induction
without auxiliary invariants). However, our goal is to automatically verify real
programs, and programmers usually neither write down trivial properties such
as s ≥ 1 nor more complex properties such as s = 2 ⇒ x1 = x2 .
    Our approach of combining k-induction with invariants proves the program
safe with k = 4 and the invariant s ≥ 1. This invariant is easy to ﬁnd auto-
matically using an inexpensive data-ﬂow analysis, such as an interval analysis.
For larger programs, a more complex invariant might be necessary, which might
get generated at some point by our continuous strengthening of the invariant.
Furthermore, stronger invariants can reduce the k that is necessary to prove a
program. For example, the invariant s ≥ 1 ∧ s ≤ 4 ∧ (s = 2 ⇒ x1 = x2 ) (which
is still weaker than the full loop invariant above) allows to prove the program
with k = 2. Thus, our strengthening of invariants can also shorten the inductive
proof procedure and lead to better performance.
    An existing approach tries to solve this problem of a too-weak induction
hypothesis by initializing only the variables of the loop-termination condition
to a non-deterministic value in the step case, and initializing all other vari-
ables to their initial value in the program [35]. However, this approach is not
strong enough for the program example-safe and even produces a wrong proof
(unsound result) for the program example-unsafe. This second example pro-
gram contains a diﬀerent safety property about s, which is violated. Because
the variable s does not appear in the loop-termination condition, it is not set
to an arbitrary value in the step case as it should be, and the inductive proof
wrongly concludes that the program is safe because the induction hypothesis is
too strong, leading to a missed bug and a wrong result. Our approach does not
suﬀer from this unsoundness, because we add only invariants to the induction
hypothesis that the invariant generation has proven to hold.
Related Work. The use of auxiliary invariants is a common technique in soft-
ware veriﬁcation [2, 9, 10,18,19,20,23, 30,36], and techniques combining data-ﬂow
analysis and SMT solvers also exist [28, 31]. In most cases, the purpose is to
speed up the analysis. For k-induction, however, the use of invariants is crucial
626    D. Beyer, M. Dangl, and P. Wendler

in making the analysis terminate at all (cf. Fig. 1). There are several approaches
to software veriﬁcation using BMC in combination with k-induction.
Split-Case Induction. We use the split-case k-induction technique [26,27], where
the base case and the step case are checked in separate steps. Earlier versions of
Scratch [27] that use this technique transform programs with multiple loops
into programs with only one single monolithic loop using a standard approach [1].
The alternative of recursively applying the technique to nested loops is discarded
by the authors of Scratch [27], because the experiments suggested it was less
eﬃcient than checking the single loop that is obtained by the transformation.
We also experimented with single-loop transformation, but our experimental
results suggest that checking all loops at once in each case instead of checking
the monolithic transformation result (which also encodes all loops in one) has
no negative performance impact, so for simplicity, we omit the transformation.
Scratch also supports combined-case k-induction [25], for which all loops are
cut by replacing them with k copies each for the base and the step case, and
setting all loop-modiﬁed variables to non-deterministic values before the step
case. That way, both cases can be checked at once in the transformed program
and no special handling for multiple loops is required. When using combined-
case k-induction, Scratch requires loops to be manually annotated with the
required k values, whereas its implementation of split-case k-induction supports
iterative deepening of k as in our implementation. Contrary to Scratch, we do
not focus on one speciﬁc problem domain [26, 27], but want to provide a solution
for solving a wide range of heterogeneous veriﬁcation tasks.
Auxiliary Invariants. While both the split-case and the combined-case
k-induction supposedly succeed with weaker auxiliary invariants than for
example the inductive invariant approach [5], the approaches still do require
auxiliary invariants in practice, and the tool Scratch requires these invariants
to be annotated manually [25,27]. There are techniques for automatically gen-
erating invariants that may be used to help inductive approaches to succeed
(e.g. [2, 9, 20]. These techniques, however, do not justify their additional eﬀort
because they are not guaranteed to provide the required invariants on time,
especially if strong auxiliary invariants are required. Based on previous ideas of
supporting k-induction with invariants generated by lightweight data-ﬂow analy-
sis [24], we therefore strive to leverage the power of the k-induction approach
to succeed with auxiliary invariants generated by a data-ﬂow analysis based on
intervals. However, to handle cases where it is necessary to invest more eﬀort
into invariant generation, we increase the precision of these invariants over time.
Invariant Injection. A veriﬁcation tool using a strategy similar to ours is
PKind [28, 33], a model checker for Lustre programs based on k-induction. In
PKind, there is a parallel computation of auxiliary invariants, where candi-
date invariants derived by templates are iteratively checked via k-induction and,
if successful, added to the set of known invariants [32]. While this allows for
strengthening the induction hypothesis over time, the template-based approach
lacks the ﬂexibility that is available to an invariant generator using dynamic
precision reﬁnement [11], and the required additional induction proofs are
                  Boosting k-Induction with Continuously-Reﬁned Invariants       627

potentially expensive. We implemented checking candidate invariants with
k-induction as a possible strategy of our invariant generation component.
Unsound Strengthening of Induction Hypothesis. Esbmc does not require addi-
tional invariants for k-induction, because it assigns non-deterministic values only
to the loop-termination condition variables before the inductive-step case [35]
and thus retains more information than our as well as the Scratch implemen-
tation [25, 27], but k-induction in Esbmc is therefore potentially unsound. Our
goal is to perform a real proof of safety by removing all pre-loop information in
the step case, thus treating the unrolled iterations in the step case truly as “any
k consecutive iterations”, as is required for the mathematical induction. Our
approach counters this lack of information by employing incrementally-reﬁned
invariant generation.
Parallel Induction. PKind checks the base case and the step case in parallel,
and Esbmc supports parallel execution of the base case, the forward condition,
and the inductive-step case. In contrast, our base case and inductive-step case
are checked sequentially, while our invariant generation runs in parallel to the
base- and step-case checks.

2   k-Induction with Continuously-Refined Invariants
Our veriﬁcation approach consists of two algorithms that run concurrently.
One algorithm is responsible for generating program invariants, starting with
an imprecise invariant, continuously reﬁning (strengthening) the invariant. The
other algorithm is responsible for ﬁnding error paths with BMC, and for con-
structing safety proofs with k-induction, for which it periodically picks up the
new invariant that the former algorithm has constructed so far. The k-induction
algorithm uses information from the invariant generation, but not vice versa.
In our presentation, we assume that each program contains at most one loop;
in our implementation, we handle programs with multiple loops by checking all
loops together.
Iterative-Deepening k-Induction. Algorithm 1 shows our extension of the
k-induction algorithm to a combination with continuously-reﬁned invariants.
Starting with an initial value for the bound k, e.g., 1, we iteratively increase the
value of k after each unsuccessful attempt at ﬁnding a speciﬁcation violation or
proving correctness of the program using k-induction. The following description
of our approach to k-induction is based on split-case k-induction [25], where
for the propositional state variables s and s within a state-transition system
that represents the program, the predicate I(s) denotes that s is an initial state,
T (s, s ) states that a transition from s to s exists, and P (s) asserts the safety
property for the state s.

Base Case. Lines 3 to 5 implement the base case, which consists of running BMC
with the current bound k. This means that starting from an initial program state,
all paths of the program up to a maximum path length k − 1 are explored. If an
error path is found, the algorithm terminates.
628         D. Beyer, M. Dangl, and P. Wendler

      Algorithm 1 Iterative-Deepening k-Induction
      Input:
          the initial value kinit ≥ 1 for the bound k,
          an upper limit kmax for the bound k,
          a function inc : N → N with ∀n ∈ N : inc(n) > n for increasing the bound k,
          the initial states defined by the predicate I,
          the transfer relation defined by the predicate T , and
          a safety property P
      Output: true if P holds, false otherwise
       1: k := kinit
       2: while k ≤ kmax do                                     
                                         
                                        k−1    
                                              n−1
       3:     base_case := I(s0 ) ∧                 T (si , si+1 ) ∧ ¬P(sn )
                                        n=0   i=0
       4:     if sat(base_case) then
       5:         return false
                                                 
                                                k−1
       6:     forward_condition := I(s0 ) ∧            T (si , si+1 )
                                                i=0
       7:     if ¬ sat(forward_condition) then
       8:        return true
                               
                              n+k−1
       9:     step_casen :=           (P(si ) ∧ T (si , si+1 )) ∧ ¬P(sn+k )
                               i=n
      10:    repeat
      11:       Inv := get_currently_known_invariant()
      12:       if ¬ sat(Inv(sn ) ∧ step_casen ) then
      13:          return true
      14:    until Inv = get_currently_known_invariant()
      15:    k := inc(k)
      16: return unknown


      Algorithm 2 Continuous Invariant Generation using Configurable Program Analysis
      Input:
          a configurable program analysis with dynamic precision adjustment D,
          the initial states defined by predicate I,
          a coarse initial precision π0 ,
          a safety property P
      Output: true if P holds
       1: π := π0
       2: Inv := true
       3: loop
       4:    reached := CPAAlgorithm(D, I, π)
       5:    if ∀s ∈ reached : P(s) then
       6:       return true
                               
       7:    Inv := Inv ∧            s
                          s ∈ reached
       8:     π := RefinePrec(π, reached)
                 Boosting k-Induction with Continuously-Reﬁned Invariants       629

Forward Condition. Otherwise we check whether there exists a path with length
k  > k − 1 in the program, or whether we have already fully explored the state
space of the program (lines 6 to 8). In the latter case the program is safe and
the algorithm terminates. This check is called the forward condition [29].
Inductive Step. Checking the forward condition can, however, only prove safety
for programs with ﬁnite (and short) loops. Therefore, the algorithm also attempts
an inductive proof (lines 9 to 14). The inductive-step case checks if, after every
sequence of k loop iterations without a property violation, there is also no prop-
erty violation before loop iteration k+1. For model checking of software, however,
this check would often fail inconclusively without auxiliary invariants [8]. In our
approach, we make use of the fact that the invariants that were generated so far
by the concurrently-running invariant-generation algorithm hold, and conjunct
these facts to the induction hypothesis. Thus, the inductive-step case proves a
program safe if the following condition is unsatisﬁable:
                             n+k−1
                              
               Inv (sn ) ∧           (P (si ) ∧ T (si , si+1 )) ∧ ¬P (sn+k )
                              i=n

where Inv is the currently available program invariant, and sn , . . . , sn+k is any
sequence of states. If this condition is satisﬁable, then the induction check is
inconclusive, and the program is not yet proved safe or unsafe with the current
value of k and the current invariant. If during the time of the satisﬁability check
of the step case, a new (stronger) invariant has become available (condition in
line 14 is false), we immediately re-check the step case with the new invariant.
This can be done eﬃciently using an incremental SMT solver for the repeated sat-
isﬁability checks in line 12. Otherwise, we start over with an increased value of k.
    Note that the inductive-step case is similar to a BMC check for the presence
of error paths of length exactly k + 1. However, as the step case needs to consider
any consecutive k + 1 loop iterations, and not only the ﬁrst such iterations, it
does not assume that the execution of the loop iterations begins in an initial
state. Instead, it assumes that there is a sequence of k iterations without any
property violation (induction hypothesis).
Continuous Invariant Generation. Our continuous invariant generation
incrementally produces stronger and stronger program invariants. It is based on
iterative reﬁnement, each time using an increased precision. After each strength-
ening of the invariant, it can be used as injection invariant by the k-induction
procedure. It may happen that this analysis proves safety of the program all by
itself, but this is not its main purpose here.
    Our k-induction module works with any kind of invariant-generation pro-
cedure, as long as its precision, i.e., its level of abstraction, is conﬁgurable.
We implemented two diﬀerent invariant-generation approaches: KI and DF,
described below.
630     D. Beyer, M. Dangl, and P. Wendler

    We use the design of Fig. 3                injects
                                                       Invariant Generation
to explain our ﬂexible and mod-
ular framework for k-induction:
k-induction is a veriﬁcation tech- k-induction (KI)                Data-Flow Analysis (DF)
                                      Algorithm 1                  Algorithm 2
nique, i.e., an invariant gener-
ation. In this paper, the main
algorithm is thus the k-induction, Fig. 3. Conﬁgurable design of a k-induction
as deﬁned in Algorithm 1. framework
We denote the algorithm by KI. If invariants are generated and injected into
KI, we denote this injection by KI←. Thus, the use of generated invariants that
are produced by a data-ﬂow analysis (DF) are denoted by KI←DF. If the invari-
ant generator continuously reﬁnes the invariants and repeatedly injects those
invariants into KI, this is denoted by KI←−, more speciﬁcally, if data-ﬂow analy-
sis with dynamic precision adjustment (our new contribution) is used, we have
KI←−DF,
           and if the PKind approach is used, i.e., KI is used to construct invari-
ants, we have KI←−KI.
                           Now, since the second KI, which constructs invariants
for injection into the ﬁrst KI, can again get invariants injected, we can further
build an approach KI←−KI      ←−DF
                                     that combines all approaches such that the
invariant-generating KI beneﬁts from the invariants generated with DF, and
the main KI algorithm that tries to prove program safety beneﬁts from both
invariant generators.
KI. PKind [33] introduced the idea to construct invariants for injection in par-
allel, using a template-based method that extracts candidate invariants from the
program and veriﬁes their validity using k-induction [32]. If the candidate invari-
ants are found to be valid, they are injected to the main k-induction procedure.
We re-implemented the PKind approach in our framework (KI←−KI),           using a
separate instance of k-induction to prove candidate invariants. Being based on
k-induction, the power of this technique is continuously increased by increas-
ing k. We derive the candidate invariants by taking the negations of assump-
tions on the control-ﬂow paths to error locations. Similar to our Algorithm 2,
each time this k-induction algorithm succeeds in proving a candidate invari-
ant, the previously-known invariant is strengthened with this newly generated
invariant. In our tool, we used an instance of Algorithm 1 to implement this app-
roach. We are thus able to further combine this technique with other auxiliary
invariant-generation approaches.
DF. As a second invariant-generation approach (our contribution), we use the
reachability algorithm CPAAlgorithm for conﬁgurable program analysis with
dynamic precision adjustment [11]. Algorithm 2 shows our continuous invari-
ant generation. The initial program invariant is represented by the formula true.
We start with running the invariant-generating analysis once with a coarse ini-
tial precision (line 4). After each run of the program-invariant generation, we
strengthen the previously-known program invariant with the newly-generated
invariant (line 7, note that the program invariant Inv is not a safety invariant)
and announce it globally (such that the k-induction algorithm can inject it).
                  Boosting k-Induction with Continuously-Reﬁned Invariants         631

If the analysis was able to prove safety of the program, the algorithm
terminates (lines 5 to 6). Otherwise, the analysis is restarted with a higher preci-
sion. The CPAAlgorithm takes as input a conﬁgurable program analysis (CPA), a
set of initial abstract states, and a precision. It returns a set of reachable abstract
states that form an over-approximation of the reachable program states. Depend-
ing on the used CPA and the precision, the analysis by CPAAlgorithm can be
eﬃcient and abstract like data-ﬂow analysis or expensive and precise like model
checking.
    For invariant generation, we choose an abstract domain based on expressions
over intervals [8]. Note that this is not a requirement of our approach, which
works with any kind of domain. Our choice is based on the high ﬂexibility of
this domain, which can be fast and eﬃcient as well as precise. For this CPA, the
precision is a triple (Y, n, w), where Y ⊆ X is a speciﬁc selection of important
program variables, n is the maximal nesting depth of expressions in the abstract
state, and w is a boolean specifying whether widening should be used. Those
variables that are considered important will not be over-approximated by joining
abstract states. With a higher nesting depth, more precise relations between
variables can be represented. The use of widening ensures timely termination
(at the expense of a lower precision), even for programs with loops with many
iterations, like those in the examples of Figs. 1 and 2. An in-depth description
of this abstract domain is presented in a technical report [8].


3    Experimental Evaluation

We implemented all existing approaches to k-induction, compare all conﬁgura-
tions with each other, and the best conﬁguration with other k-induction-based
software veriﬁers, as well as to two standard approaches to software veriﬁcation:
predicate and value analysis.
Benchmark Verification Tasks. As benchmark set we use veriﬁcation tasks
from the 2015 Competition on Software Veriﬁcation (SV-COMP’15) [7]. We took
all 3 964 veriﬁcation tasks from the categories ControlFlow, DeviceDrivers64,
HeapManipulation, Sequentialized, and Simple. The remaining categories were
excluded because they use features (such as bit-vectors, concurrency, and recur-
sion) that not all conﬁgurations of our evaluation support. A total of 1 148 ver-
iﬁcation tasks in the benchmark set contain a known speciﬁcation violation.
Although we cannot expect an improvement for these veriﬁcation tasks when
using auxiliary invariants, we did not exclude them because this would unfairly
give advantage to the new approach (which spends some eﬀort generating invari-
ants, which are not helpful when proving existence of an error path).
Experimental Setup. All experiments were conducted on computers with two
2.6 GHz 8-Core CPUs (Intel Xeon E5-2560 v2) with 135 GB of RAM. The operat-
ing system was Ubuntu 14.04 (64 bit), using Linux 3.13 and OpenJDK 1.7. Each
veriﬁcation task was limited to two CPU cores, a CPU run time of 15 min, and
632    D. Beyer, M. Dangl, and P. Wendler

a memory usage of 15 GB. The benchmarking framework BenchExec2 ensures
precise and reproducible results.
Presentation. All benchmarks, tools, and the full results of our evaluation are
available on a supplementary web page.3 All reported times are rounded to two
signiﬁcant digits. We use the scoring scheme of SV-COMP’15 to calculate a score
for each conﬁguration. For every real bug found, 1 point is assigned, for every
correct safety proof, 2 points are assigned. A score of 6 points is subtracted
for every wrong alarm (false positive) reported by the tool, and 12 points are
subtracted for every wrong proof of safety (false negative). This scoring scheme
values proving safety higher than ﬁnding error paths, and signiﬁcantly punishes
wrong answers, which is in line with the community consensus [7] on diﬃculty
of veriﬁcation vs. falsiﬁcation and importance of correct results. We consider
this a good ﬁt for evaluating an approach such as k-induction, which targets at
producing safety proofs.
    In Figs. 4 and 5, we present experimental results using a plot of quantile
functions for accumulated scores as introduced by the Competition on Soft-
ware Veriﬁcation [6], which shows the score and CPU time for successful results
and the score for wrong answers. A data point (x, y) of a graph means that
for the respective conﬁguration the sum of the scores of all wrong answers
and the scores for all correct answers with a run time of less than or equal
to y seconds is x. For the left-most point (x, y) of each graph, the x-value shows
the sum of all negative scores for the respective conﬁguration and the y-value
shows the time for the fastest successful result. For the right-most point (x, y)
of each graph, the x-value shows the total score for this conﬁguration, and the
y-value shows the maximal run time. A conﬁguration can be considered better,
the further to the right (the closer to 0) its graph begins (fewer wrong answers),
the further to the right it ends (more correct answers), and the lower its graph
is (less run time).
Comparison of k-Induction-Based Approaches. We implemented all
approaches in the Java-based open-source software-veriﬁcation framework
CPAchecker [12], which is available online4 under the Apache 2.0 License.
For the experiments, we used version 1.4.5-cav15 of CPAchecker, with
SMTInterpol [21] as SMT solver (using uninterpreted functions and linear
arithmetic over integers and reals). The k-induction algorithm of CPAchecker
was conﬁgured to increment k by 1 after each try (in Algorithm 1, inc(k) = k+1).
The precision reﬁnement of the DF-based continuous invariant generation (Algo-
rithm 2) was conﬁgured to increment the number of important program variables
in the ﬁrst, third, ﬁfth, and any further precision reﬁnements. The second preci-
sion reﬁnement increments the expression-nesting depth, and the fourth disables
the widening.
2
  https://github.com/dbeyer/benchexec
3
  http://www.sosy-lab.org/∼dbeyer/cpa-k-induction/
4
  http://cpachecker.sosy-lab.org
                       Boosting k-Induction with Continuously-Reﬁned Invariants         633

Table 1. Results of k-induction-based conﬁgurations in CPAchecker for all 3 964 ver-
iﬁcation tasks with diﬀerent approaches for generating auxiliary invariants

                                        KI←DF
Approach          KI                                             KI←−KI
                                                                       KI←−DF
                                                                              KI←−KI
                                                                                   ←−DF
                                                                                      
                         (0, 1,t) (8, 2,t) (16, 2,t) (16, 2, f )
Score           2 246    3 944    4 117    4 062    3 992    3 535    4 249    4 282
Correct results 1 531    2 377    2 462    2 428    2 392    2 169    2 507    2 519
Wrong proofs        1        1        2        1        1        1        1        1
Wrong alarms       30       30       30       30       30       30       26       25
CPU time (h) 530           330      330      340      340      380      320      320
Wall time (h) 440          240      210      210      210      270      190      170
Times for correct results only:
CPU time (h)       17      32       39       36       36       28       36       41
Wall time (h)      13      19       22       20       20       18       20       22
k-Values for correct safe results only:
Max. final k     101      101      100      100      126      101      112      111
Avg. final k        1.7      1.4     1.7      1.8      1.8      1.8      1.8      1.9



    We evaluated the following groups of k-induction approaches: (1) without
any auxiliary invariants (KI), (2) with auxiliary invariants of diﬀerent precisions
generated by the DF approach (KI←DF), and (3) with continuously-reﬁned
invariants (KI←−).
                 
    The k-induction-based conﬁguration using no auxiliary invariants (KI) is an
instance of Algorithm 1 where get currently known invariant() always returns true
as invariant and Algorithm 2 does not run at all.
    The conﬁgurations using generated invariants (KI←DF) are also instances
of Algorithm 1. Here, Algorithm 2 runs in parallel, however, it terminates after
one loop iteration. We denote these conﬁgurations with triples (s, n, w) that
represent the precision (Y, n, w) of the invariant generation with s being the
size of the set of important program variables (s = |Y |). For example, the ﬁrst
of these conﬁgurations, (0, 1, true), has no variables in the set Y of important
program variables (i.e., all variables get over-approximated by the merge opera-
tor), the maximum nesting depth of expressions in the abstract state is 1, and the
widening operator is used. The remaining conﬁgurations we use are (8, 2, true),
(16, 2, true), and (16, 2, false). These conﬁgurations were selected because they
represent some of the extremes of the precisions that are used during dynamic
invariant generation. It is impossible to cover every possible valid conﬁguration
within the scope of this paper.
    There are three conﬁgurations using continuously-reﬁned invariants: (1) using
the k-induction approach similar to PKind to generate invariants, reﬁning by
increasing k, denoted as KI←−KI,       (2) using the DF-based approach to gen-
erate invariants, reﬁning by precision adjustment, denoted as KI←−DF,         and
(3) using both approaches in parallel combination, denoted as KI←−KI      ←−DF.
                                                                            
All conﬁgurations using invariant generation run the generation in parallel to the
main k-induction algorithm, an instance of Algorithm 1.
634     D. Beyer, M. Dangl, and P. Wendler

Score and Reported Results. The conﬁguration KI with no invariant generation
receives the lowest score of 2 246, and (as expected) can verify only 1 531 pro-
grams successfully. This shows that it is indeed important in practice to enhance
k-induction-based software veriﬁcation with invariants. The conﬁgurations
KI←DF using invariant generation produce similar numbers of correct results
(around 2 400), improving upon the results of the plain k-induction without auxil-
iary invariants by a score of 1 700 to 1 800. Even though these conﬁgurations solve
a similar number of programs, a closer inspection reveals that each of the con-
ﬁgurations is able to correctly solve signiﬁcant amounts of programs where the
other conﬁgurations run into timeouts. This observation explains the high score of
4 249 points achieved by our approach of injecting the continuously-reﬁned invari-
ants generated with data-ﬂow analysis into the k-induction engine (conﬁguration
KI←−DF
          ). By combining the advantages of fast and coarse precisions with
those of slow but ﬁne precisions, it correctly solves 2 507 veriﬁcation tasks, which
is 45 more than the best of the chosen conﬁgurations without dynamic reﬁnement.
Using a k-induction-based invariant generation as done by PKind (conﬁguration
KI←−KI)
          is also a successful technique for improving the amount of solvable ver-
iﬁcation tasks, and thus, combining both invariant-generation approaches with
continuously reﬁning their precision and injecting the generated invariants into
the k-induction engine (conﬁguration KI←−KI      ←−DF)
                                                          is the most eﬀective of all
evaluated k-induction-based approaches, with a score of 4 282, and 2 519 correct
results. The few wrong proofs produced by the conﬁgurations are not due to con-
ceptual problems, but only due to incompleteness in the analyzer’s handling of
certain constructs such as unbounded arrays and pointer aliasing.

Performance. Table 1 shows that by far the largest amount of time is spent by
the conﬁguration KI (no auxiliary invariants), because for those programs that
cannot be proved without auxiliary invariants, the k-induction procedure loops
incrementing k until the time limit is reached. The wall times and CPU times for
the correct results correlate roughly with the amount of correct results, i.e., on
average about the same amount of time is spent on correct veriﬁcations, whether
or not invariant generation is used. This shows that the overhead of generating
auxiliary invariants is well-compensated.
    The conﬁgurations with invariant generation have a relatively higher CPU
time compared to their wall time because these conﬁgurations spend some
time generating invariants in parallel to the k-induction algorithm. The results
show, however, that the time spent for the continuously-reﬁned invariant gen-
eration clearly pays oﬀ as the conﬁguration using both data-ﬂow analysis and
k-induction for invariant generation is not only the one with the most correct
results, but at the same time one of the two fastest conﬁgurations with only 320 h
in total. Even though they produced much more correct results, the conﬁgura-
tions KI←−KI
                ←−DF
                       and KI←−DF
                                        did not exceed the times of the chosen
conﬁgurations using invariant generation without continuous reﬁnement. The
conﬁguration KI←−KI     using only k-induction to continuously generate invari-
ants is slower, but produces results for some programs where the conﬁguration
                 Boosting k-Induction with Continuously-Reﬁned Invariants          635

     Table 2. Results of k-induction-based tools for all 3 964 veriﬁcation tasks

              Tool             C BMC          E SBMC          CPACHECKER
              Configuration             sequential parallel KI←−KI
                                                                ←−DF
                                                                   
              Score          −4 372      1 674     1 716       4 282
              Correct results 1 949      2 050     2 059       2 519
              Wrong proofs      666        156       152           1
              Wrong alarms        5          9        13          25
              CPU time (h)      360        290       370         320
              Wall time (h)     360        290       200         170
              Times for correct results only:
              CPU time (h)          3.9      16        26         41
              Wall time (h)         3.9      16        13         22
              k-Values for correct safe results only:
              Max. final k         50     2 048     1 952        111
              Avg. final k          1.1        5.3      7.1        1.9




KI←−DF
          fails. The results show that the combination of the techniques reaps
the beneﬁts of both.
    These results show that the additional eﬀort invested in generating auxil-
iary invariants is well-spent, as it even decreases the overall time due to the
fewer timeouts. As expected, the continuously-reﬁned invariants solve many
tasks quicker than the conﬁgurations using invariant generation with high pre-
cisions and without reﬁnement.
Final value of k. The bottom of Table 1 shows some statistics about the ﬁnal val-
ues of k for the correct safety proofs. There are only small diﬀerences between
the maximum k values of most of the conﬁgurations. Interestingly, the con-
ﬁguration using non-dynamic invariant generation with high precision has a
higher maximum ﬁnal value of k than the others, because for the veriﬁcation
task afnp2014 true-unreach-call.c.i, a strong invariant generated only with
this conﬁguration allowed the proof to succeed. This eﬀect is also observable in
the continuously-reﬁned conﬁgurations using invariants generated by data-ﬂow
analysis: They are also able to solve this veriﬁcation task, and, by dynami-
cally increasing the precision, ﬁnd the required auxiliary invariant even earlier
with loop bounds 112 and 111, respectively. There is also a veriﬁcation task in
the benchmark set, gj2007 true-unreach-call.c.i, where most conﬁgurations
need to unroll a loop with bound 100 to prove safety, while the strong invariant
generation technique allows the proof to succeed earlier, at a loop bound of 16.
The continuously-reﬁned conﬁgurations beneﬁt from the same eﬀect: KI←−DF   
and KI←−KI
             ←−DF
                     solve this task at loop bounds 22 and 19, respectively.
636     D. Beyer, M. Dangl, and P. Wendler

Comparison with Other
Tools. For comparison
with other k-induction-
based tools, we evalu-
ated Esbmc and Cbmc,
two software model check-
ers with support for
k-induction. For Cbmc, we
used version 5.1 in com-
bination with a wrapper
script     for     split-case
k-induction provided by
M. Tautschnig. For Esbmc Fig. 4. Quantile functions of k-induction-based tools
we used version 1.25.2 (CPAchecker in conﬁguration KI←−KI                  ←−DF)
                                                                                      for
in combination with a accumulated scores showing the CPU time for the suc-
wrapper       script     that cessful results; linear scale between 0 s and 1 s, logarith-
enables k-induction (based mic scale beyond
on     the    SV-COMP’13
submission [35]). We also provide results for the experimental parallel k-induction
of Esbmc, but note that our benchmark setup is not focused on parallelization
(using only two CPU cores and a CPU-time limit instead of wall time). The
CPAchecker conﬁguration in this comparison is the one with continuously-
reﬁned invariants and both invariant generators (KI←−KI        ←−DF).
                                                                         Table 2 gives
the results; Fig. 4 shows the quantile functions of the accumulated scores for each
conﬁguration. The results for Cbmc are not competitive, which may be attributed
to the experimental nature of its k-induction support.

Score. CPAchecker in conﬁguration KI←−KI          ←−DF
                                                           successfully veriﬁes al-
most 500 tasks (20 %) more than Esbmc. Furthermore, it has only 1 missed bug,
which is related to unsoundness in the handling of some C features, whereas
Esbmc has more than 150 wrong safety proofs. This large number of wrong
results must be attributed to the unsound heuristic of Esbmc for strengthen-
ing the induction hypothesis, where it retains potentially incorrect information
about loop-modiﬁed variables [35]. We have previously also implemented this
approach in CPAchecker and obtained similar results [8]. The large number of
wrong proofs reduces the conﬁdence in the soundness of the correct proofs. Con-
sequently, the score achieved by CPAchecker in conﬁguration KI←−KI          ←−DF
                                                                              
is much higher than the score of Esbmc (4 282 compared to 1 674 points). This
clear advantage is also visible in Fig. 4. The parallel version of Esbmc performs
somewhat better than its sequential version, and misses fewer bugs. This is due
to the fact that the base case and the step case are performed in parallel, and the
loop bound k is incremented independently for each of them. The base case is
usually easier to solve for the SMT solver, and thus the base-case checks proceed
faster than the step-case checks (reaching a higher value of k sooner). Therefore,
the parallel version manages to ﬁnd some bugs by reaching the relevant k in
the base-case checks earlier than in the step-case checks, which would produce
                 Boosting k-Induction with Continuously-Reﬁned Invariants      637

a wrong safety proof at reaching k. However, the number of wrong proofs is still
much higher than with our approach, which is conceptually sound. Thus, the
score of the new, sound approach is more than 2 500 points higher.

Performance. Table 2 shows that our approach needs only 10 % more CPU time
than the sequential version of Esbmc for solving a much higher number of tasks,
and even needs less CPU and wall time than the parallel version of Esbmc.
This indicates that due to our invariants, we succeed more often with fewer
loop unrollings, and thus in less time. It also shows that the eﬀort invested for
generating the invariants is well spent.
Final Value of k. The bottom of Table 2 contains some statistics on the ﬁnal value
of k that was needed to verify a program. The table shows that for safe programs,
CPAchecker needs a loop bound that is (on average) only about one third of
the loop bound that Esbmc needs. This advantage is due to the use of generated
invariants, which make the induction proofs easier and likely to succeed with
a smaller number of k. The veriﬁcation task array true-unreach-call2.i is
solved by Esbmc after completely unwinding the loop, therefore reaching the
large k-value 2 048. In the parallel version, the (quicker) detached base case hits
this bound while the inductive step case is still at k = 1 952.
Comparison with Other Approaches. We also compare our combination of
k-induction with continuously-reﬁned invariants with other common approaches
for software veriﬁcation. We use for comparison two analyses based on CEGAR,
a predicate analysis [13] and a value analysis [14]. Both are implemented in
CPAchecker, which allows us to compare the approaches inside the same tool,
using the same run-time environment, SMT solver, etc., and focus only on the
conceptual diﬀerences between the analyses.
    Figure 5 shows a quan-
tile plot to compare the
conﬁguration KI←−KI     ←−
DF with CPAchecker
predicate analysis and
value analysis. The pred-
icate analysis solves 2 463
veriﬁcation tasks in a total
of 280 CPU hours, and
achieves a score of 4 201.
The value analysis solves
2 367 veriﬁcation tasks in
a total of 303 CPU hours,
and achieves a score of 4 216
because it has a few wrong Fig. 5. Quantile functions of diﬀerent approaches
results less. The higher num- implemented in CPAchecker (k-induction in conﬁgu-
ber of solved tasks (2 519) ration KI←−KI
                                           ←−DF)
                                                   for accumulated scores showing
and the higher score (4 282) the CPU time for the successful results
638     D. Beyer, M. Dangl, and P. Wendler

of the k-induction-based conﬁguration show that k-induction is clearly competi-
tive with the state-of-the-art in software veriﬁcation, if it is boosted by injecting
continuously-reﬁned invariants.


4     Conclusion
We have presented the novel idea of injecting invariants into k-induction that
are generated using data-ﬂow analysis with dynamic precision adjustment, and
contribute a publicly available implementation of our idea within the software-
veriﬁcation framework CPAchecker. Our extensive experiments show that the
new approach outperforms all existing implementations of k-induction for soft-
ware veriﬁcation, and that it is competitive compared to other, more mature tech-
niques for software veriﬁcation. We showed that a sound, eﬀective, and eﬃcient
k-induction approach to general-purpose software veriﬁcation is possible, and that
the additional resources required to achieve these combined beneﬁts are negligible
if invested judiciously. At the same time, there is still room for improvement of
our technique. An interesting improvement would be to add an information ﬂow
between the two cooperating algorithms in the reverse direction. If the k-induction
procedure could tell the invariant generation which facts it misses to prove safety,
this could lead to a more eﬃcient and eﬀective approach to generate invariants
that are speciﬁcally tailored to the needs of the k-induction proof. Already now,
CPAchecker is parsimonious in terms of unrollings, compared to other tools.
The low k-values required to prove many programs show that even our current
invariant generation is powerful enough to produce invariants that are strong
enough to help cut down the necessary number of loop unrollings. k-induction-
guided precision reﬁnement might direct the invariant generation towards provid-
ing weaker but still useful invariants for k-induction more eﬃciently.

Acknowledgments. We thank M. Tautschnig and L. Cordeiro for explaining the opti-
mal available parameters for k-induction, for the veriﬁers Cbmc and Esbmc, respectively.


References
 1. Aho, A.V., Sethi, R., Ullman, J.D.: Compilers: Principles, Techniques, and Tools.
    Addison-Wesley, Reading (1986)
 2. Awedh, M., Somenzi, F.: Automatic invariant strengthening to prove properties
    in bounded model checking. In: Proceedings of DAC, pp. 1073–1076. ACM/IEEE
    (2006)
 3. Ball, T., Cook, B., Levin, V., Rajamani, S.K.: SLAM and static driver veriﬁer: tech-
    nology transfer of formal methods inside microsoft. In: Proceedings of IFM, LNCS,
    vol. 2999, pp. 1–20. Springer (2004)
 4. Ball, T., Levin, V., Rajamani, S.K.: A decade of software model checking with SLAM.
    Commun. ACM 54(7), 68–76 (2011)
 5. Barnett, M., Leino, K.R.M.: Weakest-precondition of unstructured programs. In:
    Proceedings of PASTE, pp. 82–87. ACM (2005)
                   Boosting k-Induction with Continuously-Reﬁned Invariants            639

 6. Beyer, D.: Second competition on software veriﬁcation. In: Proceedings of TACAS,
    LNCS, vol. 7795, pp. 594–609. Springer (2013)
 7. Beyer, D.: Software veriﬁcation and veriﬁable witnesses. In: Proceedings of TACAS,
    LNCS, vol. 9035, pp. 401–416. Springer (2015)
 8. Beyer, D., Dangl, M., Wendler, P.: Combining k-induction with continuously-
    reﬁned invariants. Technical Report MIP-1503, University of Passau, January 2015.
    arXiv:1502.00096
 9. Beyer, D., Henzinger, T.A., Majumdar, R., Rybalchenko, A.: Invariant synthesis
    for combined theories. In: Proceedings of VMCAI, LNCS, vol. 4349, pp. 378–394.
    Springer (2007)
10. Beyer, D., Henzinger, T.A., Majumdar, R., Rybalchenko, A.: Path invariants. In:
    Procedings of PLDI, pp. 300–309. ACM (2007)
11. Beyer, D., Henzinger, T.A., Théoduloz, G.: Program analysis with dynamic precision
    adjustment. In: Proceedings of ASE, pp. 29–38. IEEE (2008)
12. Beyer, D., Keremoglu, M.:CPAchecker: A tool for conﬁgurable software veriﬁca-
    tion. In: Proceedings of CAV, LNCS, vol. 6806, pp. 184–190. Springer (2011)
13. Beyer, D., Keremoglu, M.E., Wendler, P.: Predicate abstraction with adjustable-
    block encoding. In: Proceedings of FMCAD, pp. 189–197. FMCAD (2010)
14. Beyer, D., Löwe, S.: Explicit-state software model checking based on CEGAR and
    interpolation. In: Proceedings of FASE, LNCS, vol. 7793, pp. 146–162. Springer
    (2013)
15. Biere, A.: Handbook of Satisﬁability. IOS Press, Amsterdam (2009)
16. Biere, A., Cimatti, A., Clarke, E.M., Strichman, O., Zhu, Y.: Bounded model check-
    ing. Adv. Comput. 58, 117–148 (2003)
17. Biere, A., Cimatti, A., Clarke, E., Zhu, Y.: Symbolic model checking without BDDs.
    In: Proceedings of TACAS, LNCS, vol. 1579, pp. 193–207. Springer (1999)
18. Bjørner, N., Browne, A., Manna, Z.: Automatic generation of invariants and inter-
    mediate assertions. Theor. Comput. Sci. 173(1), 49–87 (1997)
19. Blanchet, B., Cousot, P., Cousot, R., Feret, J., Mauborgne, L., Miné, A., Monniaux,
    D., Rival, X.: A static analyzer for large safety-critical software. In: Proceedings of
    PLDI, pp. 196–207. ACM (2003)
20. Bradley, A.R., Manna, Z.: Property-directed incremental invariant generation. FAC
    20(4–5), 379–405 (2008)
21. Christ, J., Hoenicke, J., Nutz, A.: SMTInterpol: An interpolating SMT solver. In:
    Proceedings of SPIN, LNCS, vol. 7385, pp. 248–254. Springer (2012)
22. Cordeiro, L., Fischer, B., Silva, J.P.M.: SMT-based bounded model checking for
    embedded ANSI-C software. In: Proceedings of ASE, pp. 137–148. IEEE (2009)
23. Cousot, P., Halbwachs, N.: Automatic discovery of linear restraints among variables
    of a program. In: Procedings of POPL, pp. 84–96 (1978)
24. Donaldson, A.F., Haller, L., Kroening, D.: Strengthening induction-based race
    checking with lightweight static analysis. In: Proceedings of VMCAI, LNCS, vol.
    6538, pp. 169–183. Springer, Heidelberg (2011)
25. Donaldson, A.F., Haller, L., Kroening, D., Rümmer, P.: Software veriﬁcation using
    k -induction. In: Proceeding of Static Analysis. LNCS, vol. 6887, pp. 351–368.
    Springer (2011)
26. Donaldson, A.F., Kroening, D., Rümmer, P.: Automatic analysis of scratch-pad
    memory code for heterogeneous multicore processors. In: Proceedings of TACAS,
    LNCS, vol. 6015, pp. 280–295. Springer (2010)
27. Donaldson, A.F., Kröning, D., Rümmer, P.: Automatic analysis of DMA races using
    model checking and k-induction. FMSD 39(1), 83–113 (2011)
640     D. Beyer, M. Dangl, and P. Wendler

28. Garoche, P.-L., Kahsai, T., Tinelli, C.: Incremental invariant generation using logic-
    based automatic abstract transformers. In: Proceedings of NFM, LNCS, vol. 7871,
    pp. 139–154. Springer (2013)
29. Große, D., Le, H.M., Drechsler, R.: Proving transaction and system-level properties
    of untimed SystemC TLM designs. In: Proceedings of MEMOCODE, pp. 113–122.
    IEEE (2010)
30. Gupta, A., Rybalchenko, A.: InvGen: an eﬃcient invariant generator. In: Proceedings
    of CAV, LNCS, vol. 5643, pp. 634–640. Springer (2009)
31. Albarghouthi, A., Gurﬁnkel, A., Li, Y., Chaki, S., Chechik, M.: UFO: veriﬁcation
    with interpolants and abstract interpretation. In: Proceedings of TACAS, LNCS,
    vol. 7795, pp. 637–640. Springer (2013)
32. Kahsai, T., Ge, Y., Tinelli, C.: Instantiation-based invariant discovery. In: Proceed-
    ings of NFM, LNCS, vol. 6617, pp. 192–206. Springer (2011)
33. Kahsai, T., Tinelli, C.: Pkind: a parallel k-induction based model checker. In: Pro-
    ceedings of International Workshop on Parallel and Distributed Methods in Veriﬁ-
    cation, EPTCS 72, pp. 55–62 (2011)
34. Khoroshilov, A., Mutilin, V., Petrenko, A., Zakharov, V.: Establishing linux driver
    veriﬁcation process. In: Proceedings of PSI, LNCS, vol. 5947, pp. 165–176. Springer
    (2010)
35. Morse, J., Cordeiro, L., Nicole, D., Fischer, B.: Handling unbounded loops with
    ESBMC 1.20. In: Proceedings of TACAS, LNCS, vol. 7795, pp. 619–622. Springer
    (2013)
36. Sankaranarayanan, S., Sipma, H.B., Manna, Z.: Scalable analysis of linear systems
    using mathematical programming. In: Proceedings of VMCAI, LNCS, vol. 3385,
    pp. 25–41. Springer (2005)
37. Sheeran, M., Singh, S., Stålmarck, G.: Checking safety properties using induc-
    tion and a SAT-solver. In: Proceedings of FMCAD, LNCS, vol. 1954, pp. 108–125.
    Springer (2000)
38. Wahl, T.: The k-induction principle (2013). http://www.ccs.neu.edu/home/wahl/
    Publications/k-induction.pdf
