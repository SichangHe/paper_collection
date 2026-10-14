                                             Multi-Threaded Software Model Checking via
                                               Parallel Trace Abstraction Refinement

                                                             Max Barth      and Marie-Christine Jakobs

                                                                         LMU Munich, Germany
arXiv:2509.13699v2 [cs.LO] 15 Jan 2026




                                                Abstract. Automatic software verification is a valuable means for soft-
                                                ware quality assurance. However, automatic verification and in particu-
                                                lar software model checking can be time-consuming, which hinders their
                                                practical applicability e.g., the use in continuous integration. One solu-
                                                tion to address the issue is to reduce the response time of the verification
                                                procedure by leveraging today’s multi-core CPUs.
                                                In this paper, we propose a solution to parallelize trace abstraction, an
                                                abstraction-based approach to software model checking. The underly-
                                                ing idea of our approach is to parallelize the abstraction refinement.
                                                More concretely, our approach analyzes different traces (syntactic pro-
                                                gram paths) that could violate the safety property in parallel. We realize
                                                our parallelized version of trace abstraction in the verification tool Ulti-
                                                mate Automizer and perform a thorough evaluation. Our evaluation shows
                                                that our parallelization is more effective than sequential trace abstrac-
                                                tion and can provide results significantly faster on many time-consuming
                                                tasks. Also, our approach is more effective than DSS, a recent parallel
                                                approach to abstraction-based software model checking.


                                         1    Introduction
                                         Software failures can have severe consequences. In particular for safety-critical
                                         systems, it is therefore important to not only detect software failures but also
                                         prove their absence. While software testing may reveal failures, it typically fails to
                                         prove their absence. In contrast, formal software verification techniques support
                                         both, the detection of specification violations (i.e., bugs) and the proof that a
                                         program is correct wrt. its specification. However, formal verification needs to
                                         become less time-consuming to fit into the software development process.
                                             One solution is to leverage today’s multi-core CPUs and reduce the response
                                         time via parallelization. Parallel portfolio approaches, e.g., [20,34,14,7], which
                                         run different software verifiers in parallel, facilitate easy parallelization. Unfor-
                                         tunately, they also waste a lot of resources because they only use the result
                                         of the first verifier that finishes successfully. Other parallelization approaches,
                                         e.g. [6,27,8], split the verification task (program plus property) into several sub-
                                         tasks and analyze them in parallel. Still, finding a good splitting is difficult.
                                             In this paper, we follow an orthogonal approach and aim to achieve the
                                         reduction in response time by parallelizing the verification algorithm itself. Many
                                         approaches in this category, e.g., [26,22,42,49,56], parallelize the computation of
2         M. Barth, M.-C. Jakobs

             0: if x>0                            x>0          x=-x;    x!=0
                                             ℓ0           ℓ1         ℓ5      ℓ6
             1:    x=-x;                                        )




                                                                        !(x
                                                            1 0
                                                         >-




                                                                         !=
             2: else                    !(x>0)      !(x




                                                                           0)
             3:    while x>-10                        x>-10
             4:       x=x-1;                 ℓ3                    ℓ4          ℓe
             5: assert x!=0;                            x=x-1;

    Fig. 1. Source code (left) and program automaton (right) of our example NotZero



the state space, which requires complicated synchronization. In contrast, we
pursue a similar idea as Yin, Dong, Liu, and Wang [59] and aim to parallelize
abstraction refinement. While Yin, Dong, Liu, and Wang target bounded model
checking for concurrent programs, we consider abstraction-based software model
checking, more concretely trace abstraction [30,31].
    Trace abstraction [30,31] is an automata-based software model checking ap-
proach for safety properties like assertions. It maintains an automaton (the
abstraction), which describes those syntactical program paths that lead to a
property violation and whose feasibility still needs to be analyzed. During verifi-
cation, trace abstraction alternates between (a) selecting a path from the current
abstraction, (b) checking the feasibility of the selected path, and when proven
infeasible (c) determining an automaton that describes the infeasible path and
paths with similar reasons of infeasibility before (d) refining the abstraction, i.e.,
removing the determined paths from the abstraction.
    We observe that step (b) and (c) can be done independently when given the
selected path and the program. Hence, our parallelization uses several worker
instances for step (b) and (c), which all consider different paths. In addition, a
single coordinator is responsible for steps (a) and (d) as well as the communica-
tion with the workers.
    We demonstrate our parallelization for two worker threads on the program1
shown in Fig. 1. First, the coordinator selects the two paths π1 = x > 0, x =
−x, !(x! = 0) and π2 =!(x > 0), !(x > −10), !(x! = 0), one following the if
and the other the else branch. Note that both paths are semantically infeasible.
The coordinator assign paths π1 and π2 to separate workers. Assume that the
coordinator first gets the result for path π1 . Thus, it excludes π1 from its current
abstraction. For demonstration purposes, we assume that after the abstraction
refinement the result for path π2 is not yet available. Hence, the coordinator
selects a third path π3 =!(x > 0), x > −10, x = x − 1; , !(x > −10), !(x! = 0) and
assigns it to the free worker. Next, we assume that the coordinator receives the
result for π2 and gets to know that it can exclude all paths following the else
branch. After removing the paths from the else branch from the abstraction,
the coordinator detects that there are no further paths to check and reports
the program is proven safe. While this example wastes CPU time on processing

1
    For more details on the program automaton, we refer to the next section.
                                       Parallel Trace Abstraction Refinement        3

path π3 , the response time of the verification should still be shorter because it
processes paths π1 and π2 in parallel.
    We implement the demonstrated idea of parallel trace abstraction refinement
in the tool Ultimate Automizer and thoroughly evaluate it on verification tasks
of the SVBenchmark. Our evaluation shows that parallelization can be beneficial
wrt. effectiveness and response time.
    In summary, our paper makes the following contributions.
  – We conceptually develop a parallel version of the trace abstraction algorithm
     (Sec. 3), an abstraction-based algorithm for software model checking target-
     ing safety properties, and integrate it into the tool Ultimate Automizer.
  – We perform a rigorous experimental evaluation of parallel trace abstraction
     (Sec. 4) considering 14 560 C verification tasks of the SVBenchmark and
     four different numbers of workers. Also, we compare against a state-of-the-
     art parallelization approach.


2     Sequential Trace Abstraction
In this paper, we aim to parallelize trace abstraction [30,31], a software verifica-
tion technique to analyze whether a program adheres to a given safety property.
Trace abstraction, which is also known as automata-based software model check-
ing, maintains and iteratively refines (i.e., reduces the size of) a set of traces,
a subset of the syntactical program paths that may cause a property violation.
During verification, the set of traces forms the current (trace) abstraction of
the program and is represented via an automaton. In the following, we formally
introduce the notion of traces, define the initial trace abstraction, and explain
the sequential verification procedure that iteratively refines trace abstractions.

2.1    Traces and Initial Trace Abstraction
Our goal is to use traces to represent (syntactic) program paths. To this end,
a trace describes the order in which a (syntactic) program path performs its
operations. In our presentation, we consider two types of program operations:
assignments and assume statements (Boolean expressions), which both operate
on a set V of integer variables2 . The set Σ describes the set of all possible
program operations. Hence, traces are sequences π ∈ Σ ∗ of program operations.
We order these traces based on their prefix relation. More concretely, we write
π ′ ⪯ π if there exists π ′′ ∈ Σ ∗ such that π = π ′ π ′′ .
    During verification, we consider sets Sπ of traces that represent syntactic
program paths that will violate the safety property of interest if they are seman-
tically feasible. For the efficient representation of a set Sπ of traces, we use a
finite automaton A with alphabet Σ. The automaton’s language is exactly the
set of traces, i.e., L(A) = Sπ . The verification starts with the set SI of all traces
that model a syntactic program path that potentially violates the safety prop-
erty of interest. Since one may encode safety properties as the unreachability of
2
    Our implementation supports C statements.
4      M. Barth, M.-C. Jakobs

Algorithm 1 Sequential trace abstraction procedure [30]
Input: program automaton AP
 1: A = AP ;
 2: while True do
 3:   if L(A) == ∅ then return SAFE;
 4:   select π ∈ L(A)
 5:   (result, interpolants) = checkSAT(φπ );
 6:   if result == SAT then return UNSAFE;
 7:   Aπ = generateAutomaton(π, interpolants, A);
 8:   A = A \ Aπ



certain program locations (named error locations) [32], we restrict ourselves to
safety properties encoded by error locations. Thus, the set SI contains all traces
that model a syntactic program path that may end in an error location.
    To describe the set SI , we need to model the program as an automaton
that accepts the traces from the set SI . To this end, we use a (program) auto-
maton AP = (L, δP , ℓ0 , FP ) [30]. Its set L of states represents the program
locations, which are closely related to the program counter values. The initial
location ℓ0 ∈ L relates to the program counter value at the start of the program.
Furthermore, the transition relation δP ⊆ L × Σ × L models the program’s
control-flow. Transitions (ℓ, op, ℓ′ ) ∈ δP describe which operations op may be
executed at a given program location ℓ and where to proceed (ℓ′ ) after the
execution of operation op. Finally, the set FP ⊆ L contains the accepting states,
which correspond to the program’s error locations and determine the safety
property. Hence, a program automaton accepts exactly the traces in SI .
    Figure 1 shows the source code (left) and the resulting program automaton
(right) of our example program NotZero. Except for the error location ℓe , the
index of a location in the program automaton refers to the corresponding line
number in the source code of the program. Furthermore, the automaton con-
tains one edge per assignment and two assume statement edges per if, while, or
assert statement, namely one for each evaluation of their condition. To let the
violation of the assertion result in a property violation, the false evaluation of
the assertion’s condition leads to the error location ℓe .


2.2   Iterative Trace Abstraction Refinement

Next, we describe the iterative verification procedure, namely the sequential
trace abstraction algorithm. The verification procedure employs counterexample-
guided abstraction refinement (CEGAR) [17] and is shown in Alg. 1.
    The algorithm gets a program automaton, which accepts the traces that rep-
resent syntactic program paths that lead to a property violation (i.e., an error
location). During verification, the algorithm maintains automaton A to represent
the current trace abstraction, which contains all traces that model a syntactic
program path to an error location for which the semantic feasibility has not yet
                                         Parallel Trace Abstraction Refinement     5

                    {true}       {x ≤ 0}         {x ≤ −10}     {false}
                      q0            q3              q5             qe
                           !(x>0)        !(x>-10)        !(x!=0)
                             x>-10, x = x − 1;

      Fig. 2. An interpolant automaton for trace !(x > 0), !(x > −10), !(x! = 0)


been checked. Line 1 initializes the trace abstraction with the program automa-
ton AP . Lines 2–8 perform the iterative refinement of the trace abstraction. The
verification will end with result SAFE (i.e., property proven) in line 3 if the
language of the automaton A is empty, i.e., there does not exist a trace that
models a feasible program path that ends in an error location. If the language is
non-empty, there still exist syntactic program paths to error locations for which
the semantic feasibility has not yet been checked. Hence, line 4 uses breadth-first
search to select a trace π ∈ L(A) representing one such path. Thereafter, line 5
checks the semantic feasibility of that path. To this end, it first constructs an
SSA-based formula encoding φπ of π and subsequently checks φπ ’s satisfiability
with an SMT solver. For example, for trace !(x > 0), !(x > −10), !(x! = 0) we
check formula ¬(x0 > 0)∧¬(x0 > −10)∧¬(x0 ̸= 0) and for trace x > 0, x = −x; ,
!(x! = 0) we check formula x0 > 0 ∧ x1 = −x0 ∧ ¬(x1 ̸= 0). If the result of the
satisfiability check is SAT, we proved that the syntactic program path repre-
sented by trace π is semantically feasible. Since all program paths represented
by a trace π ∈ L(A) end in an error location, we found a feasible counterexam-
ple and line 6 returns UNSAFE (i.e., property violation detected). Otherwise,
we refine the trace abstraction in lines 7 and 8. First, we construct an inter-
polant automaton Aπ [30] that accepts π and other traces with similar reasons
of semantic infeasibility. Note that the construction of Aπ uses abstraction A to
focus on traces that are still relevant and, thus, to make the construction more
efficient. Figure 2 shows a possibly interpolant automaton for trace !(x > 0),
!(x > −10), !(x! = 0). The automaton encodes the trace and extends it with an
additional loop. Also, the automaton records the infeasibility argument for its
accepted traces by annotating its states with assertions. Typically, we use in-
terpolation to derive the assertions from the unsatisfiability proof of the trace’s
formula encoding. Given the interpolant automaton, which by construction only
accepts traces that are semantically infeasible, line 8 refines our current trace
abstraction. More concretely, it removes the traces accepted by the interpolant
automaton from the current trace abstraction by computing the difference of our
current abstraction (automaton A) and the interpolant automaton Aπ .


3   Towards Parallel Trace Abstraction
Next, we describe how we parallelize the iterative trace abstraction procedure,
which we described in the previous section. The idea is to parallelize the loop
performing the iterative refinement of the trace abstraction.
6       M. Barth, M.-C. Jakobs

Algorithm 2 Coordinator that directs parallel trace abstraction
Input: program automaton AP
 1: A = AP ; Sπex = ∅;
 2: while True do
 3:   if L(A) == ∅ then return SAFE;
 4:   while idleWorkerAvailable() ∧ L(A) \ Sπex ̸= ∅ do
5:      select π ∈ L(A) \ Sπex
6:       Sπex = Sπex ∪ {π};
7:       giveTaskToWorker(π, A);
8:    waitUntilAtLeastOneWorkerResultAvailable();
9:    while workerResultAvailable() do
10:      (Aπ , result) = getWorkerResult();
11:     if result == SAT then return UNSAFE;
12:     A = A \ Aπ ;



3.1   Preliminary Considerations
Looking at the loop (lines 2–8 of Alg. 1), we observe that the only dependency
between loop iterations is the trace abstraction represented by automaton A.
The update of the abstraction in line 8 aggregates the results of the different
iterations and therefore, should not be done in parallel. Nevertheless, the aggre-
gation itself is commutative, i.e., for the abstraction itself it does not matter in
which order we use the interpolant automata to refine it. Furthermore, we notice
that the check in line 5, which inspects the feasibility of trace π, is independent
of abstraction A. In addition, when generating the interpolant automaton we
only use the abstraction to make the generation more efficient. Hence, using an
older, out-of-date abstraction, which accepts more traces, is sound but may not
be as efficient as using the latest one. For the emptiness check in line 3 and the
search of a trace π ∈ L(A), it is also sound to use an out-of-date abstraction.
However, using an out-of-date abstraction may likely result in performing unnec-
essary work, e.g., more refinement iterations, which one could avoid when using
the latest abstraction. Further taking into account that we experienced that the
feasibility check (line 5) and the interpolant automaton generation (line 7) are
the most expensive tasks in each iteration, we decide to consider those two tasks
for parallel execution. Thereby, we concede that different threads may need to
maintain memory-expensive out-of-date copies of the abstraction. This is accept-
able because from our experience sequential trace abstraction much more often
runs out of time than it runs out of memory.

3.2   Procedure of Parallel Trace Abstraction
To realize our parallelization, we use a central coordinator (Alg. 2) in com-
bination with several workers (Alg. 3). The coordinator directs the verification
                                         Parallel Trace Abstraction Refinement          7

Algorithm 3 Worker for trace processing
Input: trace π, trace abstraction A with π ∈ L(A)
 1: (result, interpolants) = checkSAT(φπ );
 2: if result = UNSAT then
 3:    Aπ = generateAutomaton(π, interpolants, A);
 4: else Aπ = ({q0 }, ∅, q0 , ∅);
5: publishResult(Aπ , result);



procedure. To this end, it runs a modified version of the sequential trace abstrac-
tion procedure (Alg. 1). Differences are highlighted in gray and mainly represent
synchronization with workers. In addition, it maintains a set Sπex , which tracks
the traces already assigned for analysis, and uses it to avoid exploring the same
trace π twice.3 Like the sequential procedure, the coordinator (Alg. 2) initializes
and iteratively updates the trace abstraction (lines 1 and 12). Also, it checks
the stopping criteria of the verification procedure (lines 3 and 11). To maintain
the set Sπex , Alg. 2 initializes it with an empty set of already analyzed traces in
line 1 and updates it in line 6 after selecting a trace to analyze. Furthermore, we
adapt the trace selection (line 5) such that it only selects traces that are in the
current trace abstraction and have not been assigned for analysis yet, i.e., are
not in set Sπex . In contrast to the sequential procedure, Alg. 2 distributes the
selected traces to the available workers for analysis and relies on the workers’
results to update its trace abstraction.
    The workers (Alg. 3) process the traces. They perform the feasibility check of
the traces (line 1). For traces proven infeasible, they also compute the interpolant
automaton (line 3) required for refinement. Hence, they perform the steps in line
5 and 7 of the sequential verification procedure (Alg. 1). In addition, they make
the result (the result of the feasibility check and the interpolant automaton)
available for the coordinator (line 5). To ensure that they provide a structurally
valid result, they construct an automaton accepting the empty language in line 4
if the trace is feasible, i.e., no interpolant automaton is required.
    To coordinate with the workers, each iteration of the coordinator contains
a phase to distribute the work to the workers (lines 4–7) followed by a phase
to collect and process the workers’ results (lines 8–12). Each phase is realized
with a while loop. The loop distributing work stops when no further worker or
trace to analyze is available, while the loop considering worker results stops if
no result is available. Furthermore, we avoid busy waiting by explicitly waiting
until some result becomes available in line 8.
    Using the coordinator together with one worker basically performs sequential
trace abstraction, but distributed on two threads. When we use more than one
3
    Note that in contrast to sequential trace abstraction, which either stops exploration
    when detecting that a trace is feasible or removes the infeasible trace from the trace
    abstraction before selecting the next trace, our parallel trace abstraction selects
    traces while the analysis of traces selected earlier may not have finished.
8       M. Barth, M.-C. Jakobs

Algorithm 4 Recursive algorithm search to select diverse traces from a trace
abstraction
Input: trace abstraction A = (Q, δ, q0 , F ), search state q, selected prefix π, relevant
    set of analyzed traces Srt
 1: if Srt = ∅ then
 2:    if acceptingStateReachableFrom(q, A) then
 3:       return π ◦ shortestPathToAcceptingStateFrom(q, A);
 4:    else return null;
 5: succ = list({(q, ·, ·) ∈ δ});
 6: sort(succ, (q, op, q ′ ) → |{π ′ ∈ Srt | π ◦ op ⪯ π ′ }|);
 7: while !empty(succ) do
 8:    (q, op, q ′ ) = dequeue(succ);
 9:    if π ◦ op ∈  / Srt then
10:       πr = search(A, q ′ , π ◦ op, {π ′ ∈ Srt | π ◦ op ⪯ π ′ });
11:       if πr != null then return πr ;
12: return null;



worker, we need to take particular care of the trace selection. To avoid redundant
work, we already ensure that a trace is only selected once. Ideally, we would like
to select diverse traces, e.g., traces with different reasons for infeasibility. We
discuss trace selection in more detail in the next section.


3.3   Procedure for Diverse Trace Selection

Now, we discuss our trace selection (i.e., line 5 of Alg. 3). The selection must
ensure that it does not select a trace from Sπex and ideally it should select a trace
with a new reason for infeasibility. The more the newly selected trace differs
from the previously selected traces Sπex , the likelier it will be that it provides a
different reason for infeasibility. With this in mind, we aim to steer our selection
such that it selects traces that diverge early from previously selected traces.
     Algorithm 4 shows our selection procedure, which implements a recursive
search procedure through the abstraction. The algorithm gets the trace abstrac-
tion A to search through, the state q where in the abstraction to continue the
search, the already selected prefix π, and the set of relevant analyzed traces Srt ,
i.e., the previously selected traces with prefix π that are not yet known to be in-
feasible. Thus, line 5 of Alg. 3 calls the algorithm with the current trace abstrac-
tion, the abstraction’s initial state q0 , an empty prefix trace ε, and set Sπex ∩L(A)
of traces already assigned for analysis but not yet known to be infeasible.
     To select traces that diverge early from previously selected traces, Alg. 4
prioritizes successor transitions that have been reached less often via the prefix π
currently considered by the search procedure. If no traces have been selected yet
that use the currently considered prefix π, i.e., Srt is empty, lines 1–4 return the
shortest trace with prefix π that is in the language of the abstraction or null
if none exist. The prioritization itself is realized in lines 5–12 of Alg. 4. First,
line 5 builds a list of all transitions that start in the current search state q. Next,
                                      Parallel Trace Abstraction Refinement        9

the algorithm sorts these transitions by how likely they lead to a new trace. We
approximate the likelihood with the number of previously selected traces that
are continuations of the trace built from the currently selected prefix π and the
transition’s operation. Thereby, a higher number indicates a smaller likelihood.
Thereafter, the while loop realizes the actual prioritized search. In each iteration,
line 8 removes the transition with the largest likelihood (smallest number of
continuations) that has not yet been explored. The check in line 9 ensures that
we skip the transition whenever the transition’s operation together with the
currently selected trace results in a previously selected trace. In all other cases,
line 10 recursively searches for a trace not previously selected. The recursive call
searches for a continuation of prefix trace π extended with the current transition’s
operation. Therefore, it continues the search with the successor q ′ of the currently
considered transition and adapts the search to those relevant traces that agree
with the new prefix. If the recursive call detects a new trace (πr ̸= null), we
return it in line 11. However, if the current transition cannot lead us to a new
trace, the next loop iteration tries the next transition. If we fail to generate a
new trace with any available transition outgoing of the current search state q,
we return null in line 12 and backtrack. Note that Alg. 4 terminates with a
non-null result as long as there exists a trace accepted by trace abstraction A,
which is not in the initial set Srt of analyzed traces. Algorithm 3 guarantees this
whenever it selects a new trace.

3.4   Implementation
We integrate our approach for parallel trace abstraction into Ultimate Auto-
mizer [50], a Java-based software verification tool that already supports sequen-
tial trace abstraction. Following our conceptual approach, our implementation of
parallel trace abstraction reuses the components of the existing sequential trace
abstraction and mainly adds the parallelization and adapts the trace search.
    To realize the parallelization, we use the Runnable interface to implement
Alg. 3, which processes a given trace π. Furthermore, we realize the work-
ers with a fixed thread pool, which is provided as an ExecutorService. Note
that the user can configure the number of threads in the pool via a parame-
ter. To start new trace processing and to retrieve their results, we combine the
ExecutorService instance with a CompletionService instance. The coordina-
tor uses the CompletionService instance to initiate a new trace processing and
to retrieve the results from finished trace processing without busy waiting.
    To allow for a better comparison between sequential and parallel trace ab-
straction, our implementation of parallel trace abstraction aims to include all
traces π in its analysis that the sequential trace abstraction analyzes. To this
end, we use a slightly modified search for diverse traces. In the first iteration
of each execution of the loop in lines 4–7 of Alg. 2, we first apply breadth-first
search, the search strategy of sequential trace abstraction, to detect a trace π ac-
cepted by the current trace abstraction (i.e., π ∈ L(A)). If π has not been found
before (i.e., π ∈
                / Sπex ), we distribute π to a worker and continue with the next
iterations of the loop, which all perform our proposed search (Alg. 4). Otherwise,
10      M. Barth, M.-C. Jakobs

we apply our proposed search. However, we do not compute Sπex ∩ L(A) when
calling the search but overapproximate it. To this end, we remove a trace π from
Sπex when we process the result of its analysis. Another improvement we employ
is that we limit the search for a trace π to 5 seconds4 instead of performing the
expensive non-emptiness check in line 4 of Alg. 2 and treat a timeout of the
search as a failed non-emptiness check. Note that this is sound because we never
use the non-emptiness check to determine the result of the verification.


4     Evaluation
The goal of our parallelization is to reduce the response time and to increase the
effectiveness of the approach. Therefore, our evaluation investigates the effect of
our parallelization on response time and solved tasks. Furthermore, we compare
our parallelization with a recent parallelization technique that uses software
model checking techniques similar to trace abstraction.

4.1   Experimental Setting
Tool Configurations. In our evaluation, we consider four different configura-
tions of our parallel trace abstraction, namely PAR-1-UA, PAR-2-UA, PAR-4-
UA and PAR-6-UA. They differ in the size of the fixed thread pool. PAR-1-UA
uses one worker thread and describes the sequential baseline of our approach.
The other three configurations use two, four, and six worker threads. Since even
the sequential configuration PAR-1-UA uses a coordinator and worker thread,
we also run Ultimate Automizer with the sequential configuration SEQ-UA
used in the latest competition on software verification (SV-COMP25). For all
five configurations, we use Ultimate Automizer version 0.3.0-474959ed5 . Fur-
thermore, we use DSS, a recent state-of-the-art technique for parallel model
checking, which employs distributed summary synthesis [8]. For DSS, we use the
version provided in artifact [9] accompanying the paper.
    Verification Tasks. For our evaluation, we consider verification tasks from
the software verification benchmark6 (SVBenchmark), which is used by the in-
ternational competition on software verification (SV-COMP) [11]. A verification
task in SV-COMP consists of a program and a property. We restrict our eval-
uation to all tasks from SV-COMP 2025 that consider (a) sequential C pro-
grams, the programs supported by trace abstraction in Ultimate Automizer,
and (b) property unreach-call, a safety property which states that certain error
locations (encoded as calls to the function reach_error) must not be reached.
In total, we consider 14 560 tasks, 11 158 of them fulfill the property while 3 402
of them violate the property.
4
  This limit proved useful in practice. Our observation is that the search typically
  finishes within one second.
5
  Note that SEQ-UA solves slightly more tasks in this version than in its version
  submitted to SV-COMP 2025.
6
  https://gitlab.com/sosy-lab/benchmarking/sv-benchmarks/-/tree/svcomp25-final
                                       Parallel Trace Abstraction Refinement       11

Table 1. Per tool configuration, number of correctly and incorrectly reported property
violations (alarms) and property adherence (proofs)

                         SEQ-UA PAR-1-UA PAR-2-UA PAR-4-UA PAR-6-UA DSS

      correct alarms       1128     1140       1241       1243      1245 291
      correct proofs       3377     3695       3747      3860        3858 1263
      incorrect alarms        0        0          0          0          1 317
      incorrect proofs        0        0          0          0          0   62



   Evaluation Environment. The machines, we use, contain 33 GB of memory
and an Intel Xeon E3-1230 v5 CPU with 8 processing units and a frequency of
3.40 GHz. Their operating system is a 64-bit Ubuntu 24.04 with Linux kernel 6.8
and the installed Java version is OpenJDK 21.0.7. We limit each run of any tool
configuration on a verification task to 8 CPU cores, 15 min of wall time and
30 GB of memory and enforce the limits with BenchExec [10] (version 3.18).


4.2   Impact of Parallelization on Effectiveness

In this section, we study the impact of our parallelization on effectiveness, i.e.,
the number of (correctly) solved tasks. To this end, let us first look at Tab. 1,
which shows for every tool configuration (column) the number of correctly and
incorrectly reported alarms (property violations) and proofs (property satisfac-
tions). When studying the trace abstraction configurations (first five columns),
we observe that PAR-1-UA performs better than the SV-COMP 2025 configu-
ration SEQ-UA. One reason is that our new search strategy allows us to recover
from exceptions that occur during trace processing. Due to worse effectiveness,
we do not further consider SEQ-UA in the remaining evaluation. Furthermore,
we observe that only PAR-6-UA reports incorrect results, namely one incorrect
alarm. Studying the incorrect result, we observe that all other configurations
fail to solve this task. A more detailed manual inspection of the incorrect analy-
sis result lets us believe that the unsoundness is caused by the reused Ultimate
Automizer functionality and not our parallelization. Further studying Tab. 1, we
observe that with increasing number of threads the number of solved alarms and
proofs typically increases. The only exception is PAR-6-UA, which solves less
proofs than PAR-4-UA. We investigated this further and observe that PAR-
1-UA can correctly solve 2 219 of 4 835 by analyzing less than six traces, i.e.,
PAR-6-UA does not provide any benefits while causing additional overhead,
which may cause timeouts. When restricting the set of tasks for which PAR-1-
UA analyzes at least six traces, i.e., all configurations have its worth, PAR-6-UA
has the largest number of correct proofs.


 Effectiveness typically increases when the number of workers increases.
     12                     M. Barth, M.-C. Jakobs



wall time PAR-1-UA [s]




                                                     wall time PAR-1-UA [s]




                                                                                                          wall time PAR-1-UA [s]
                     102                                                  102                                                  102


                     101                                                  101                                                  101
                           101         102                                      101         102                                      101        102
                            wall time PAR-2-UA [s]                               wall time PAR-4-UA [s]                              wall time PAR-6-UA [s]

     Fig. 3. Scatter plot that compares the wall time of PAR-2-UA (left), PAR-4-UA (mid-
     dle), and PAR-6-UA (right) with the wall time of PAR-1-UA (y-axes) on tasks solved by
     both configurations. Additionally, points outside the rectangle represent tasks either
     not solved by PAR-1-UA (top) or PAR-2-UA, PAR-4-UA, and PAR-6-UA (right)



     4.3                   Effect of Parallelization on Response Time

     Next, we study whether parallelization may reduce the response time (i.e., wall
     time). To observe the immediate effect of parallelization on response time, we aim
     to compare configurations for trace abstraction that only differ in the number
     of worker threads. Hence, we compare the wall time of our approach with one
     worker (PAR-1-UA) with the configurations PAR-2-UA, PAR-4-UA, and PAR-
     6-UA that utilize 2, 4, and 6 workers. Figure 3 shows one scatter for each of the
     parallel configurations PAR-2-UA, PAR-4-UA, and PAR-6-UA. Each scatter
     plot compares the wall time of the respective parallel configuration with the wall
     time of PAR-1-UA. Thereby, it contains data points (x, y) for all tasks correctly
     solved by at least one of the two compared configurations, i.e., 5 036 tasks for
     PAR-2-UA, 5 178 tasks for PAR-4-UA, and 5 203 tasks for PAR-6-UA. One
     point (x, y) in the scatter plot compares the wall time used by PAR-2-UA,
     PAR-4-UA, and PAR-6-UA, respectively, with the wall time used by PAR-1-
     UA (y) for one particular task. (Black) points above the top border show tasks
     that PAR-1-UA does not solve. Similarly, tasks right of the right border show
     tasks that the respective configuration using multiple worker threads does not
     solve. Depending on the scatter plot, PAR-1-UA fails to solve between 201 and
     368 tasks, while PAR-2-UA, PAR-4-UA, and PAR-6-UA fail to solve 48, 75, and
     100 tasks, respectively. Sometimes, a configuration with multiple worker threads
     fails while PAR-1-UA solves the tasks close to the timeout. Thus, the overhead
     for parallelization may cause the failure. In other cases, we observe that the
     configuration with multiple worker threads analyzes more traces and still fails.
     Hence, we believe that the order in which the trace abstraction is refined may
     differ. This may lead to different trace abstractions such that the relevant traces
     that need to be analyzed to succeed will not be selected and analyzed early
     enough. Still, the number of failures of PAR-1-UA for which the parallelization
     succeeds are much larger than vice versa.
          Next, let us look at tasks solved by both of the compared configurations,
     i.e., the points in the rectangle. All three scatter plots contain points below the
     diagonal, i.e., PAR-1-UA responds faster, and above the diagonal, i.e., PAR-1-
                                                                                             Parallel Trace Abstraction Refinement                                                        13

                                          6                    alarms                                                                                       proofs
                                                                                                                                     4.0




          wall time PAR-1 / wall time x




                                                                                                     wall time PAR-1 / wall time x
                                          5                                                                                          3.5

                                          4                                                                                          3.0
                                                                                                                                     2.5
                                          3
                                                                                                                                     2.0
                                          2
                                                                                                                                     1.5
                                          1                                                                                          1.0
                                              [0, [10, [100, [0, [10, [100, [0, [10, [100,                                                 [0, [10, [100, [0, [10, [100, [0, [10, [100,
                                              10) 100) ) 10) 100) ) 10) 100) )                                                             10) 100) ) 10) 100) ) 10) 100) )
                                                 PAR-2          PAR-4          PAR-6                                                          PAR-2          PAR-4          PAR-6


Fig. 4. Speed up on tasks for which PAR-1-UA responds more slowly. Grouped by the
wall time of PAR-1-UA into the intervals [0, 10), [10, 100), and [100, ∞). On the left,
we only consider tasks with property violations (alarms) while on the right we only
consider tasks that adhere to the specification (proofs).



UA responds slower. More importantly, there are points in each plot that are
above the line parallel to the diagonal. This line represents the upper bound for
the speedup achievable according to Amdahl’s law.7 For a point to be above that
upper bound, the parallelization needs to skip some work done by PAR-1-UA.
For example, due to parallelization we may find a property violation earlier, find
a better loop abstraction earlier, or in general get to a smaller abstraction earlier,
which may allow us to skip processing some traces considered by PAR-1-UA.
In detail, PAR-2-UA responds faster for 49% (2 369 of 4 787) of the commonly
solved tasks and achieves a speedup larger than 3 for 67 tasks. Furthermore,
PAR-4-UA responds faster for 43% (2 002 of 4 760) of the commonly solved tasks
and achieves a speedup larger than 5 for 42 tasks. PAR-6-UA responds faster
34% (1 619 of 4 735) of the commonly solved tasks and achieves a speedup larger
than 7 for 31 tasks. Moreover, we observe that if parallelization is slower, it will
typically not take that much longer. Indeed, it only takes between 0.68 and 1.99
additional seconds in the median and between 9.58 and 14.59 additional seconds
on average. When not profiting from parallelization, we do not lose much.
    Next, let us study those tasks for which PAR-2-UA, PAR-4-UA, and PAR-
6-UA respond faster, respectively. Our goal is to investigate whether the benefit
of parallelization is different for proof and alarm detection as well as for more
difficult tasks, i.e., tasks for which PAR-1-UA takes longer. Figure 4 shows two
plots, the left considers alarms and the right considers proofs. Each plot con-
tains three combined violin and box plots per configuration using multiple worker
threads considering tasks solved by both, the respective configuration with mul-
tiple worker threads and PAR-1-UA. However, the combined plots only consider
those commonly solved tasks for which PAR-1-UA is slower wrt. wall time and
show the distribution of the speedup (i.e., wall time of PAR-1-UA divided by
wall time of the other configuration) for tasks which PAR-1-UA solves in less
than 10s of wall time, in 10-100s of wall time, and more than 100s of wall time.
For each group, we observe that from left to right the violins and boxes become
7
    The upper bound of the speedup is identical with the thread number.
14      M. Barth, M.-C. Jakobs

larger and the whiskers become higher, i.e., we may be able to save more wall
time when the verification is complex and takes longer. However, the variance
for more complex tasks is also higher. Furthermore, we observe that the vari-
ance increases when using more worker threads. It seems that with more worker
threads the possible speedup depends more and more on the benchmark. When
comparing the left and right plots in Fig. 4, we observe that the violins on the
left are larger. It seems easier to achieve high speedups from parallelization when
detecting property violations.


 Parallelization can significantly reduce response time, particularly for time-
 consuming tasks, while exhibiting negligible negative effects when no improve-
 ments are achieved.



4.4   Comparison Against Existing Parallelization Techniques

Finally, we compare our parallelization to state-of-the-art parallelization ap-
proaches. We are aware of two recent, relevant parallelization approaches: ranged
program analysis [27] and distributed summary synthesis (DSS) [8]. Like us, both
may use a verification procedure based on predicates, CEGAR, and interpola-
tion. Since we technically failed to port ranged program analysis to Ubuntu 24.04
(the OS environment for our experiments), we only compare our approach to
DSS. Since DSS makes use of all 8 available cores, we decide to compare DSS to
our configuration PAR-6-UA, which uses the most threads.
    Effectiveness. First, we compare the number of solved tasks. To this end,
we first compare the columns of Tab. 1 that are labeled with PAR-6-UA and
DSS. We observe that DSS correctly detects significantly fewer alarms and proofs
while reporting much more incorrect results, both alarms and proofs. One reason
for the higher number of incorrect results is DSS’s limited support for pointers
and arrays, which is known to cause incorrect results.
    Efficiency. To compare the efficiency in
terms of response time (wall time), we restrict     103
our comparison to the 1 395 tasks correctly
                                                 wall time DSS [s]




solved by our approach (i.e., PAR-6-UA) and         102
DSS. Figure 5 shows a scatter plot that con-
tains one (x, y) for each of 1 395 tasks that       101
compares the wall time of our approach (x)
                                                    100 0
with the wall time of DSS (y). We observe that         10     101       102     103
                                                          wall time PL-6-UA [s]
there exist points above and below the diag-
onal, i.e., our approach solves the task faster
                                                  Fig. 5. Comparing the wall time of
than DSS and vice versa. A detailed analysis
                                                  our approach PAR-6-UA (x-axis)
reveals that DSS uses less time for 66% (915 and competitor DSS (y-axis)
of 1 395) of the tasks. For these 915 tasks, DSS
is faster by 7.1s in the median. A large pro-
                                     Parallel Trace Abstraction Refinement     15

portion of the 7.1s are caused by the larger startup time of Ultimate Automizer
and, thus, of PAR-6-UA, which is about 4.7s larger.

 Our approach is more effective and regularly more efficient than DSS.


4.5   Threats to Validity
Our implementation of the parallelization may contain bugs. We think it is un-
likely since we only observed one incorrect result when using six worker threads.
Still, our results may not generalize. Despite using all sequential C tasks from
SV-COMP that consider the unreach-call safety property, which encode differ-
ent safety properties, the set may not reflect all real-world sequential programs
and safety properties. Also, results may differ with other resource limits.


5     Related Work
We are aware of one other software verification approach [59] that parallelizes
the CEGAR refinement step. The approach performs scheduling constraint based
abstraction refinement, a verification approach for concurrent programs, which
is based on bounded model checking (BMC). Its parallelization runs multiple
instances of the verification procedure in parallel and lets each instance use
a random search strategy parameterized by the process ID to detect different
counterexamples (i.e., syntactic paths to property violations). The refinement
results (i.e., scheduling constraints) are exchanged via a shared data structure.
In contrast, we consider a different verification technique, only parallelize the
analysis of the counterexample but perform a more sophisticated search.
    Instead of parallelizing the refinement steps, Lopes and Rybalchenko [42] par-
allelize the exploration of the abstract state space in predicate-abstract model
checking. Also, there are approaches [26,33,22] that parallelize the state-space
construction in explicit model checking. Parallelized state-space construction
may even use GPUs [21,4,57]. In context of static analysis, e.g., dataflow analy-
ses, some approaches parallelize the computation of abstract facts [49,18,39,56]
while in LTL model checking, several approaches [13,3,23] parallelize the empti-
ness check of the language described by the product of system automaton and
negated specification. Also, some approaches run complete algorithmic blocks of
an analysis in parallel like base- and step-case in k-induction [38] or invariant
generation for k-induction [5]. Furthermore, verifiers may use implementations of
decision diagrams [19] or SAT and SMT solvers [36] that can operate in parallel,
e.g., use multiple threads to perform an operation.
    Parallelizing the verification algorithm itself may be complex. Thus, another
class of approaches splits the verification task into several subtasks and ana-
lyzes them in parallel. One option is to split the set of program paths, which is
e.g., applied to dataflow analyses [51], BMC [25,45,37], software model check-
ing [27,29,28,48], and symbolic execution [53,54,47]. Another strategy is to de-
compose the program into code blocks, as e.g., done in dataflow analyses [52,55],
16      M. Barth, M.-C. Jakobs

verifiers like Bolt [2], Coverity [44], BAM [6], or DSS [8], and static application se-
curity testing [16]. When one needs to analyze multiple properties, e.g., different
assertions, one can also analyze the individual properties in parallel [58,40,43].
    Even simpler than splitting the verification task is it to run different verifiers
or different verifier configurations in parallel. Approaches like PredatorHP [46],
Nacpa [41], or CoVeriTeam’s parallel portfolio [7] run different approaches in
parallel but in isolation. In contrast, some approaches [1,14,15,24,12] that run
multiple SAT or SMT based verification instances in parallel may share informa-
tion, e.g., perform lemma sharing. Finally, swarm verification [34,35] and parallel
randomized state-space search [20] aim to diversify the search through the state
space, e.g., by letting various instances use different search orders.
    While it is not straightforward to combine our approach with other algorith-
mic parallelization techniques, splitting the verification task or running different
verifier instances on a verification task is orthogonal to our parallelization ap-
proach and can easily be combined with our approach.


6    Conclusion

Trace abstraction is an automata-based software verification technique, which
checks safety properties of software. Its original verification algorithm imple-
mented in Ultimate Automizer has not been designed to work in parallel. To
let trace abstraction benefit from modern compute hardware, in particular multi-
threading, we therefore propose a parallelization approach for trace abstraction.
Our approach parallelizes the abstraction refinement, i.e., our approach analyzes
multiple, distinct syntactic paths, which lead to an error location, in parallel.
Thereby, each analysis checks the feasibility of the respective path and in case of
infeasibility computes an interpolant automaton to refine the trace abstraction.
A coordinator uses a specialized search procedure to find diverse paths that lead
to an error location, distributes the found paths to available workers, and ap-
plies the refinement to the global trace abstraction. Since our parallelization is
orthogonal to parallel portfolio approaches, which run multiple verifiers in par-
allel, or parallelization approaches that split the verification task, we can freely
combine it with those approaches.
    We evaluated the implementation of our parallel trace abstraction in Ulti-
mate Automizer on a large set of C verification tasks from the SVBenchmark.
Thereby, we observe that parallelization increases the effectiveness, i.e., typically,
we solve more tasks with more workers. Nevertheless, parallelization will only
make sense if the number of traces analyzed by sequential trace abstraction
is at least as large as the number of workers. Furthermore, we observe that
in particular for longer running tasks parallelization may reduce the wall time
significantly. For several tasks, the speedup for the wall time is significantly
larger than the upper bound given by Amdahl’s law for task parallelization, i.e.,
parallel trace abstraction may allow us to skip some of the verification steps
performed by sequential trace abstraction. This further confirms the value of
parallel trace abstraction.
                                        Parallel Trace Abstraction Refinement        17

References
 1. Ábrahám, E., Schubert, T., Becker, B., Fränzle, M., Herde, C.: Parallel SAT solving
    in bounded model checking. In: Proc. FMICS. pp. 301–315. LNCS 4346, Springer
    (2006). https://doi.org/10.1007/978-3-540-70952-7_21
 2. Albarghouthi, A., Kumar, R., Nori, A.V., Rajamani, S.K.: Parallelizing top-down
    interprocedural analyses. In: Proc. PLDI. pp. 217–228. ACM (2012). https://doi.
    org/10.1145/2254064.2254091
 3. Barnat, J., Cerná, I.: Distributed breadth-first search LTL model checking.
    Formal Methods Syst. Des. 29(2), 117–134 (2006). https://doi.org/10.1007/
    S10703-006-0009-Y
 4. Bartocci, E., DeFrancisco, R., Smolka, S.A.: Towards a GPGPU-parallel SPIN
    model checker. In: Proc. SPIN. pp. 87–96. ACM (2014). https://doi.org/10.1145/
    2632362.2632379
 5. Beyer, D., Dangl, M., Wendler, P.: Boosting k-induction with continuously-refined
    invariants. In: Proc. CAV. pp. 622–640. LNCS 9206, Springer (2015). https://doi.
    org/10.1007/978-3-319-21690-4_42
 6. Beyer, D., Friedberger, K.: Domain-independent multi-threaded software model
    checking. In: Proc. ASE. pp. 634–644. ACM (2018). https://doi.org/10.1145/
    3238147.3238195
 7. Beyer, D., Kanav, S., Richter, C.: Construction of verifier combinations based on
    off-the-shelf verifiers. In: Proc. FASE. pp. 49–70. LNCS 13241, Springer (2022).
    https://doi.org/10.1007/978-3-030-99429-7_3
 8. Beyer, D., Kettl, M., Lemberger, T.: Decomposing software verification using dis-
    tributed summary synthesis. Proc. ACM Softw. Eng. 1(FSE), 1307–1329 (2024).
    https://doi.org/10.1145/3660766
 9. Beyer, D., Kettl, M., Lemberger, T.: Reproduction package for FSE 2024 article
    ’Decomposing software verification using distributed summary synthesis’ (version
    FSE24-proceedings) (2024). https://doi.org/10.5281/ZENODO.11563223
10. Beyer, D., Löwe, S., Wendler, P.: Reliable benchmarking: Requirements and solu-
    tions. STTT 21(1), 1–29 (2019). https://doi.org/10.1007/s10009-017-0469-y
11. Beyer, D., Strejcek, J.: Improvements in software verification and witness vali-
    dation: SV-COMP 2025. In: Proc. TACAS. pp. 151–186. LNCS 15698, Springer
    (2025). https://doi.org/10.1007/978-3-031-90660-2_9
12. Blicha, M., Hyvärinen, A.E.J., Marescotti, M., Sharygina, N.: A cooperative paral-
    lelization approach for property-directed k-induction. In: Proc. VMCAI. pp. 270–
    292. LNCS 11990, Springer (2020). https://doi.org/10.1007/978-3-030-39322-9_13
13. Brim, L., Cerná, I., Krcál, P., Pelánek, R.: Distributed LTL model checking based
    on negative cycle detection. In: Proc. FST TCS. pp. 96–107. LNCS 2245, Springer
    (2001). https://doi.org/10.1007/3-540-45294-X_9
14. Chaki, S., Karimi, D.: Model checking with multi-threaded IC3 portfolios. In:
    Proc. VMCAI. pp. 517–535. LNCS 9583, Springer (2016). https://doi.org/10.1007/
    978-3-662-49122-5_25
15. Champion, A., Mebsout, A., Sticksel, C., Tinelli, C.: The Kind 2 model checker.
    In: Proc. CAV. pp. 510–517. LNCS 9780, Springer (2016). https://doi.org/10.1007/
    978-3-319-41540-6_29
16. Christakis, M., Cottenier, T., Filieri, A., Luo, L., Mansur, M.N., Pike, L., Rosner,
    N., Schäf, M., Sengupta, A., Visser, W.: Input splitting for cloud-based static
    application security testing platforms. In: Proc. FSE. pp. 1367–1378. ACM (2022).
    https://doi.org/10.1145/3540250.3558944
18      M. Barth, M.-C. Jakobs

17. Clarke, E.M., Grumberg, O., Jha, S., Lu, Y., Veith, H.: Counterexample-guided
    abstraction refinement. In: Proc. CAV. pp. 154–169. LNCS 1855, Springer (2000).
    https://doi.org/10.1007/10722167_15
18. Dewey, K., Kashyap, V., Hardekopf, B.: A parallel abstract interpreter for
    JavaScript. In: Proc. CGO. pp. 34–45. IEEE (2015). https://doi.org/10.1109/CGO.
    2015.7054185
19. van Dijk, T., van de Pol, J.: Multi-core decision diagrams. In: Hamadi, Y., Sais, L.
    (eds.) Handbook of Parallel Constraint Reasoning, pp. 509–545. Springer (2018).
    https://doi.org/10.1007/978-3-319-63516-3_13
20. Dwyer, M.B., Elbaum, S.G., Person, S., Purandare, R.: Parallel randomized state-
    space search. In: Proc. ICSE. pp. 3–12. IEEE (2007). https://doi.org/10.1109/
    ICSE.2007.62
21. Edelkamp, S., Sulewski, D.: External memory breadth-first search with delayed du-
    plicate detection on the GPU. In: Proc. MoChArt. pp. 12–31. LNCS 6572, Springer
    (2010). https://doi.org/10.1007/978-3-642-20674-0_2
22. Evangelista, S., Kristensen, L.M., Petrucci, L.: Multi-threaded explicit state space
    exploration with state reconstruction. In: Proc. ATVA. pp. 208–223. LNCS 8172,
    Springer (2013). https://doi.org/10.1007/978-3-319-02444-8_16
23. Evangelista, S., Petrucci, L., Youcef, S.: Parallel nested depth-first searches for
    LTL model checking. In: Proc. ATVA. pp. 381–396. LNCS 6996, Springer (2011).
    https://doi.org/10.1007/978-3-642-24372-1_27
24. Gacek, A., Backes, J., Whalen, M., Wagner, L.G., Ghassabani, E.: The JKind
    model checker. In: Proc. CAV. pp. 20–27. LNCS 10982, Springer (2018). https:
    //doi.org/10.1007/978-3-319-96142-2_3
25. Ganai, M.K., Gupta, A.: Tunneling and slicing: Towards scalable BMC. In: Proc.
    DAC. pp. 137–142. ACM (2008). https://doi.org/10.1145/1391469.1391507
26. Garavel, H., Mateescu, R., Smarandache, I.M.: Parallel state space construction
    for model-checking. In: Proc. SPIN. pp. 217–234. LNCS 2057, Springer (2001).
    https://doi.org/10.1007/3-540-45139-0_14
27. Haltermann, J., Jakobs, M., Richter, C., Wehrheim, H.: Parallel program analysis
    via range splitting. In: Proc. FASE. pp. 195–219. LNCS 13991, Springer (2023).
    https://doi.org/10.1007/978-3-031-30826-0_11
28. Haltermann, J., Jakobs, M., Richter, C., Wehrheim, H.: Ranged program analysis
    via instrumentation. In: Proc. SEFM. pp. 145–164. LNCS 14323, Springer (2023).
    https://doi.org/10.1007/978-3-031-47115-5_9
29. Haltermann, J., Jakobs, M., Richter, C., Wehrheim, H.: Parallel program analysis
    on path ranges. Science of Computer Programming 238, 103154 (2024). https:
    //doi.org/10.1016/J.SCICO.2024.103154
30. Heizmann, M., Hoenicke, J., Podelski, A.: Refinement of trace abstraction. In:
    Proc. SAS. pp. 69–85. LNCS 5673, Springer (2009). https://doi.org/10.1007/
    978-3-642-03237-0_7
31. Heizmann, M., Hoenicke, J., Podelski, A.: Software model checking for people who
    love automata. In: Proc. CAV. pp. 36–52. LNCS 8044, Springer (2013). https:
    //doi.org/10.1007/978-3-642-39799-8_2
32. Henzinger, T.A., Jhala, R., Majumdar, R., Necula, G.C., Sutre, G., Weimer, W.:
    Temporal-safety proofs for systems code. In: Proc. CAV. pp. 526–538. LNCS 2404,
    Springer (2002). https://doi.org/10.1007/3-540-45657-0_45
33. Holzmann, G.J.: A stack-slicing algorithm for multi-core model checking. In: Proc.
    PDMC@CAV. Electronic Notes in Theoretical Computer Science, vol. 198, pp.
    3–16. Elsevier (2007). https://doi.org/10.1016/J.ENTCS.2007.10.017
                                        Parallel Trace Abstraction Refinement        19

34. Holzmann, G.J., Joshi, R., Groce, A.: Swarm verification. In: Proc. ASE. pp. 1–6.
    IEEE (2008). https://doi.org/10.1109/ASE.2008.9
35. Holzmann, G.J., Joshi, R., Groce, A.: Swarm verification techniques. IEEE Trans.
    Software Eng. 37(6), 845–857 (2011). https://doi.org/10.1109/TSE.2010.110
36. Hyvärinen, A.E.J., Wintersteiger, C.M.: Parallel satisfiability modulo theories. In:
    Hamadi, Y., Sais, L. (eds.) Handbook of Parallel Constraint Reasoning, pp. 141–
    178. Springer (2018). https://doi.org/10.1007/978-3-319-63516-3_5
37. Inverso, O., Trubiani, C.: Parallel and distributed bounded model checking of
    multi-threaded programs. In: Proc. PPoPP. pp. 202–216. ACM (2020). https:
    //doi.org/10.1145/3332466.3374529
38. Kahsai, T., Tinelli, C.: PKind: A parallel k-induction based model checker. In:
    Proc. PDMC. EPTCS, vol. 72, pp. 55–62 (2011). https://doi.org/10.4204/EPTCS.
    72.6
39. Kim, S.K., Venet, A.J., Thakur, A.V.: Deterministic parallel fixpoint computation.
    Proc. ACM Program. Lang. 4(POPL), 14:1–14:33 (2020). https://doi.org/10.1145/
    3371082
40. Kumar, R., Ball, T., Lichtenberg, J., Deisinger, N., Upreti, A., Bansal, C.:
    CloudSDV enabling static driver verifier using Microsoft Azure. In: Proc.
    IFM. pp. 523–536. LNCS 9681, Springer (2016). https://doi.org/10.1007/
    978-3-319-33693-0_33
41. Lemberger, T., Wachowitz, H.: Nacpa: Native checking with parallel-portfolio anal-
    yses - (competition contribution). In: Proc. TACAS. pp. 236–241. LNCS 15698,
    Springer (2025). https://doi.org/10.1007/978-3-031-90660-2_18
42. Lopes, N.P., Rybalchenko, A.: Distributed and predictable software model check-
    ing. In: Proc. VMCAI. pp. 340–355. LNCS 6538, Springer (2011). https://doi.org/
    10.1007/978-3-642-18275-4_24
43. Marescotti, M., Gurfinkel, A., Hyvärinen, A.E.J., Sharygina, N.: Designing parallel
    PDR. In: Proc. FMCAD. pp. 156–163. IEEE (2017). https://doi.org/10.23919/
    FMCAD.2017.8102254
44. McPeak, S., Gros, C., Ramanathan, M.K.: Scalable and incremental software bug
    detection. In: Proc. FSE. pp. 554–564. ACM (2013). https://doi.org/10.1145/
    2491411.2501854
45. Nguyen, T.L., Schrammel, P., Fischer, B., La Torre, S., Parlato, G.: Parallel bug-
    finding in concurrent programs via reduced interleaving instances. In: Proc. ASE.
    pp. 753–764. IEEE (2017). https://doi.org/10.1109/ASE.2017.8115686
46. Peringer, P., Soková, V., Vojnar, T.: PredatorHP revamped (not only) for interval-
    sized memory regions and memory reallocation (competition contribution). In:
    Proc. TACAS. pp. 408–412. LNCS 12079, Springer (2020). https://doi.org/10.
    1007/978-3-030-45237-7_30
47. Qiu, R., Khurshid, S., Pasareanu, C.S., Wen, J., Yang, G.: Using test ranges to
    improve symbolic execution. In: Proc. NFM. pp. 416–434. LNCS 10811, Springer
    (2018). https://doi.org/10.1007/978-3-319-77935-5_28
48. Richter, C., Chalupa, M., Jakobs, M., Wehrheim, H.: Cooperative software verifi-
    cation via dynamic program splitting. In: Proc. ICSE. pp. 2087–2099. IEEE (2025).
    https://doi.org/10.1109/ICSE55347.2025.00092
49. Rodriguez, J., Lhoták, O.: Actor-based parallel dataflow analysis. In: Proc.
    CC. pp. 179–197. LNCS 6601, Springer (2011). https://doi.org/10.1007/
    978-3-642-19861-8_11
50. Schüssele, F., Bentele, M., Dietsch, D., Heizmann, M., Jiang, X., Klumpp, D.,
    Podelski, A.: Ultimate automizer and the abstraction of bitwise operations - (com-
20      M. Barth, M.-C. Jakobs

    petition contribution). In: Proc. TACAS. pp. 418–423. LNCS 14572, Springer
    (2024). https://doi.org/10.1007/978-3-031-57256-2_31
51. Sherman, E., Dwyer, M.B.: Structurally defined conditional data-flow static anal-
    ysis. In: Proc. TACAS. pp. 249–265. LNCS 10806, Springer (2018). https://doi.
    org/10.1007/978-3-319-89963-3_15
52. Shi, Q., Zhang, C.: Pipelining bottom-up data flow analysis. In: Proc. ICSE. pp.
    835–847. ACM (2020). https://doi.org/10.1145/3377811.3380425
53. Siddiqui, J.H., Khurshid, S.: Scaling symbolic execution using ranged analysis.
    In: Proc. SPLASH. pp. 523–536. ACM (2012). https://doi.org/10.1145/1831708.
    1831732
54. Staats, M., Pasareanu, S.S.: Parallel symbolic execution for structural test genera-
    tion. In: Proc. ISSTA. pp. 183–194. ACM (2010). https://doi.org/10.1145/1831708.
    1831732
55. Stiévenart, Q., Es, N.V., der Plas, J.V., Roover, C.D.: A parallel worklist algorithm
    and its exploration heuristics for static modular analyses. J. Syst. Softw. 181,
    111042 (2021). https://doi.org/10.1016/J.JSS.2021.111042
56. Sun, Z., Xu, D., Zhang, Y., Qi, Y., Wang, Y., Zuo, Z., Wang, Z., Li, Y., Li, X.,
    Lu, Q., Peng, W., Guo, S.: BigDataflow: A distributed interprocedural dataflow
    analysis framework. In: Proc. FSE. pp. 1431–1443. ACM (2023). https://doi.org/
    10.1145/3611643.3616348
57. Wijs, A., Bosnacki, D.: GPUexplore: Many-core on-the-fly state space exploration
    using GPUs. In: Proc. TACAS. pp. 233–247. LNCS 8413, Springer (2014). https:
    //doi.org/10.1007/978-3-642-54862-8_16
58. Yang, G., Do, Q.C.D., Wen, J.: Distributed assertion checking using symbolic exe-
    cution. ACM SIGSOFT Softw. Eng. Notes 40(6), 1–5 (2015). https://doi.org/10.
    1145/2830719.2830729
59. Yin, L., Dong, W., Liu, W., Wang, J.: Parallel refinement for multi-threaded pro-
    gram verification. In: Proc. ICSE. pp. 643–653. IEEE (2019). https://doi.org/10.
    1109/ICSE.2019.00074
