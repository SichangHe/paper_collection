                                               VS YNC: Push-Button Verification and Optimization for
                                               Synchronization Primitives on Weak Memory Models
                                                               (Technical Report)

                                          Jonas Oberhauser1,2 , Rafael Lourenco de Lima Chehab1,2 , Diogo Behrens1,2 , Ming Fu1,2 ,
arXiv:2102.06590v1 [cs.LO] 12 Feb 2021




                                         Antonio Paolillo1,2 , Lilith Oberhauser1,2 , Koustubha Bhat1,2 , Yuzhong Wen2 , Haibo Chen2,3 ,
                                                                       Jaeho Kim1,2 , and Viktor Vafeiadis4
                                                                             1 Huawei Dresden Research Center
                                                                                    2 Huawei OS Kernel Lab
                                                                               3 Shanghai Jiao Tong University
                                                               4 Max Planck Institute for Software Systems (MPI-SWS)




                                                                                                Abstract
                                                  This technical report contains material accompanying our work with same title published at ASPLOS’21 [24].
                                              We start in §1 with a detailed presentation of the core innovation of this work, Await Model Checking (AMC).
                                              The correctness proofs of AMC can be found in §2. Next, we discuss three study cases in §3, presenting bugs
                                              found and challenges encountered when applying VS YNC to existing code bases. Finally, in §4 we describe the
                                              setup details of our evaluation and report further experimental results.




                                                                                                    1
Contents
1   Await Model Checking in Detail                                                                                3
    1.1 Notations and Definitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     3
    1.2 Verifying Await Termination with AMC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .          4
    1.3 Implementing AMC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        7

2   Proving the Correctness of Await Model Checking                                                           8
    2.1 The tiny concurrent assembly-like language . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
         2.1.1 Syntax . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
         2.1.2 Semantics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
    2.2 Formalizing the Bounded-Effect principle . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
    2.3 Proving the main theorem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

3   Study Cases                                                                                                   27
    3.1 DPDK MCS lock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         27
    3.2 MCS lock of an internal Huawei product . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        29
    3.3 Linux qspinlock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     30

4   Optimized-code Evaluation                                                                                     33
    4.1 Setup details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   33
        4.1.1 Evaluation platforms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        33
        4.1.2 Environment setup . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         33
    4.2 Microbenchmark evaluation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .         34
        4.2.1 Experiment details . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        34
        4.2.2 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       36




                                                         2
   1      Await Model Checking in Detail
  AMC is an enhancement of stateless model checking (SMC) capable of handling programs with awaits on
  WMMs. SMC constructs all possible executions of a program, and filters out those inconsistent with respect
  to the underlying memory model. However, SMC falls short when the program has infinitely many or non-
  terminating executions (e.g., due to await loops) because the check never terminates. AMC overcomes this
  limitation by filtering out executions in which multiple iterations of an await loop read from the same writes.
      We start introducing basic notation and definitions, including execution graphs, which are used to represent
  executions. Next, we explain how awaits lead to infinitely many and/or non-terminating executions, and how
  AMC overcomes these problems. We present sufficient conditions under which AMC correctly verifies programs
  including await termination (AT) and safety. Finally, we show the integration of AMC into a stateless model
  checker from the literature.

   1.1      Notations and Definitions
  Executions as graphs. An execution graph G is a formal abstraction of executions, where nodes are events
  such as reads and writes, and the edges indicate (po) program order, (mo) modification order, and (rf) read-from
  relationships, as illustrated in Fig. 2. A read event Rm  T (x, v) reads the value v from the variable x by the thread T
  with the mode m, a write event WTm (x, v) updates x with v, and Winit (x, v) initializes. The short notations RT (x, v)
  and WT (x, v) represent the relaxed events Rrlx                   rlx
                                                   T (x, v) and WT (x, v) respectively. Note that the po is identical in
   a and b because it is the order of events in the program text. In contrast, mo and rf edges differ; e.g., in a ,

  WT1 (l, 1) precedes WT2 (l, 0) in mo, while in b it is the other way around. Furthermore, the rf edges indicate that
  WT1 (l, 1) is never read in a , while it is read by RT2 (l, 1) in b .

                                                                         a                                  b
                                                                              Winit (l, 0) Winit (q, 0)          Winit (l, 0) Winit (q, 0)
                                                                              mo                      rf                                     rf
                                                                                                acq                                    acq
                      locked = 0, q = 0;                                 WT1 (l, 1) moRT2 (q, 0) rf         WT1 (l, 1) moRT2 (q, 0) rf
                                                                              po                po               po                    po
                                                                                                acq                                    acq
           T1 : lock                            T2 : unlock              WTrel (q, 1)          RT2 (q, 0)   WTrel (q, 1)             RT2 (q, 0)
                                                                            1             rf                   1                rf
                                                                                                po                                     po
 locked = 1;                            while (q == 0);                                         acq                                    acq
 q = 1;                                 locked = 0;                           po               RT2 (q, 1)   rf po               moRT2 (q, 1)
                                                                                    mo          po                         mo          po
 while (locked == 1);                   assert (locked == 0);                             rf
 /* Critical Section */                                                      RT1 (l, 0)        WT2 (l, 0)       RT1 (l, 1)           WT2 (l, 0)
                                                                                                po rf            po                    po
Figure 1: Awaits in one path of a partial MCS lock. T1                                                                ..
                                                                                               RT2 (l, 0)              .             RT2 (l, 1) 7
signals q = 1 to notify T2 that it enqueued, and T2 waits
for the notification, then signals locked = 0 to pass the            Figure 2: Two execution graphs of Fig. 1 where l =
lock to T1 .                                                         locked.


  Consistency predicates. A weak memory model M is defined by a consistency predicate consM over graphs,
  where consM (G) holds iff G is consistent with M. For instance, the ‘IMM’ model used by VS YNC forbids the
  cyclic path1 of highlighted edges in b of Fig. 2 due to the rel and acq modes, as it forbids all cyclic paths
  consisting of edges in this order: 1) po ending in W rel , 2) rf ending in Racq , 3) po, 4) mo. Such a path is compactly
  written as “po; [W rel ]; rf; [Racq ]; po; mo”, and is never cyclic in graphs consistent with IMM. Thus consIMM ( b )
  does not hold. If say the rel barriers on the accesses to q would be removed, the graph would be consistent with
  IMM.
   Awaits. Intuitively, an await is a special type of loop which waits for a write of another thread. To make this
   intuition more precise, imagine a demonic scheduler that prioritizes threads currently inside awaits. Under such
   a scheduler, an await has two possible outcomes: either the write of the other thread is currently visible, and
   the await terminates immediately; or the write of the other thread is not visible. In the latter case, the scheduler
   continuously prevents the write from becoming visible by never scheduling the writer thread, and hence the
   await never terminates. A more precise definition for await is a loop that, for every possible value of the polled
       1 A path is cyclic if it starts and ends with the same node




                                                                     3
                                           /* lock acquire */
                                           do {
                                             atomic_await_neq (& lock , 1);
                                           } while( atomic_xchg (& lock , 1) != 0);

                                           x ++; /* CS */

                                           /* lock release */
                                           atomic_write (& lock , 0);

                                                    Figure 3: TTAS lock example.
variables2 , either exits immediately or loops forever when executed in isolation. We illustrate this with the two
loops of the TTAS lock from Fig. 3. The inner loop is an await; to show this, we need to consider every potential
value v of lock: for v = 0, the loop repeats forever, and for v 6= 0 the loop exits during the first iteration. The
outer loop is not an await; to show this, we need to find one value v of lock for which the loop is not executed
infinitely often but also not exited immediately. One such value is v = 1, for which the thread never reaches the
outer loop again after entering the inner loop.
Sets of execution graphs. Given a fair scheduler, awaits either exit after a number of failed iterations or
(intentionally) loop forever. We separate execution graphs that satisfy consM into two sets, GF and G∞ . GF is
the set of execution graphs where all awaits exit after a finite number of failed iterations. In Fig. 2, for example,
 a is in GF since cons ( a ) holds and the await of T exits after two failed iterations. Note GF consists exactly
                           M                               2
of the graphs in which all awaits terminate, but that does not imply that these graphs are finite: there may still be
infinitely many steps outside of the awaits. We will later state a sufficient condition that excludes such cases. G∞
is the set of the remaining consistent graphs. In each of these at least one await loops forever. We define:
Definition 1 (Await termination). AT holds iff G∞ is 0.       /
Due to the barriers on q, consIMM ( b ) does not hold, and hence b is not in G∞ . In fact, with these acq and rel
barriers, all graphs with an infinite number of failed iterations violate consistency, and hence G∞ is empty; AT is
not violated.
                                                                                           acq
     Note that we can splice an additional failed iteration into a by repeating RT2 (q, 0), resulting in a new
graph in GF . We generalize this idea. Let Gk ⊆ GF be the set of consistent execution graphs with a total3 of
k ∈ {0, 1, . . .} failed iterations. Thus, G0 is the set of consistent graphs with no failed iterations. With two failed
iterations of T2 ’s await and zero of T1 ’s await, a has a total of 2 + 0 = 2 failed iterations of awaits, and is thus in
G2 . Let now G ∈ Gk with k > 0, i.e., G has at least one failed iteration; we can always repeat one of its failed
iterations to obtain a graph G0 ∈ Gk+1 due to the      non-deterministic number of iterations of await loops. Since all
Gk are disjoint, their union (denoted by GF = k∈{ 0,1,... } Gk ) is infinite despite every set Gk being finite.
                                                     U


1.2     Verifying Await Termination with AMC
State-of-the-art stateless model checkers [15–17] cannot construct all execution graphs in GF or any in G∞ . In
order for SMC to complete in finite time, the user has to limit the search space to a finite subset of executions
graphs in GF . Consequently, SMC cannot verify AT (Definition 1) and can only verify safety within this subset
of executions graphs.
Key challenges. For SMC to become feasible in our problem domain, we need to solve three key challenges:
Infinity: We need to produce an answer in finite time without a user-specified search space, even though the
      search space GF ∪ G∞ is infinite.
Soundness: We need to make sure not to miss any execution graph that may potentially uncover a safety bug.
Await termination: We need to verify that G∞ is 0./
Under certain conditions specified later, AMC overcomes these challenges through three crucial implications:
   2 Polled variables refers the variables read in each loop iteration to evaluate the loop’s condition.
    3 We count here the sum of failed iterations of all executed instances of awaits, including multiple instances by the same thread, e.g., when

the inner await loop in the TTAS lock from Fig. 3 is executed multiple times.


                                                                       4
                    T
                                                                 rf                                rf                                rf
   /* lock acquire */                          B:
   do { d = 2;                                       WT (d, 2)        RT (d, 2)        WT (d, 1)        RT (d, 1)        WT (d, 0)        RT (d, 0)
                                                                 po               po               po               po               po
      while (d--);                                                                                                           rf
   } await_while
     (atomic_xchg(lock, 1) != 0);                  acq                acq                acq
                                               BpoRT (lock, 1) po BpoRT (lock, 1) po BpoRT (lock, 0)poWT (lock, 1) po RT (d, 0)
   assert (d==0);

Figure 4: Execution graph B represents the inner loop of T (marked yellow ). Failed await iterations are
indicated with dotted boxes, the final (non-failed) iteration with a solid box. The inner loop of T violates the
Bounded-Effect principle, as rf-edges (marked with ) leave failed await iterations. The outer loop obeys the
principle, as rf-edges only leave the final await iteration.
   1. The infinite set GF is collapsed into a finite set of finite executions graphs GF∗ ⊂ GF . Moreover, the infinite
      execution graphs in G∞ are collapsed into finite execution graphs in a (possibly infinite) set G∞     ∗ . AMC
      explores at most all graphs in GF∗ and up to one graph in G∞     ∗ .
   2. For all G ∈ GF , there exists G0 ∈ GF∗ such that G and G0 are equivalent. Thus, bugs present in GF are also
      in GF∗ .
  3. Detecting whether there exists a finite execution graph in G∞                                    ∞
                                                                 ∗ is sufficient to conclude whether G is empty.
                                                                 ∞
     Thus AMC can stop after exploring one graph in the set G∗ and report an AT violation, and if AMC does
     not come across such a graph, AT is not violated.
We now explain how AMC achieves these three implications, as well as the conditions under which it does so.
The key to AMC. In contrast to existing SMCs, AMC filters out execution graphs that contain awaits where
multiple iterations read from the same writes to the polled variables. This idea is captured by the predicate W(G)
which defines wasteful executions.
Definition 2 (Wasteful). An execution graph G is wasteful, i.e., W(G) holds, if an await in G reads the same
combination of writes in two consecutive iterations.
    AMC does not generate wasteful executions, as they do not add any additional information. For instance,
AMC does not generate execution graph α ∈ G2 from Fig. 5 because W( α ) holds: T1 reads from its own write
twice in the await. Similarly, AMC does not generate any of the infinitely many variations of α in which T1
reads even more often from that write. Instead, ifwe remove all references to q in the program of Fig. 1, AMC
generates only the two execution graphs in GF∗ = 1 , 2 , in which each write is read at most once by the await
of T1 . T1 can read from at most two differentUwrites, thus there is at most one failed iteration of the await in the
execution graphs in GF∗ , and we have GF∗ ⊆ k∈{ 0,1 } Gk ; in general, if there are at most n ∈ N writes each await
                                 α
                                        Winit (l, 0)                   β
                                                                                  Winit (l, 0)
                                      mo       mo                                        mo        mo
                                 WT1 (l, 1)         WT2 (l, 0)          WT1 (l, 1)            WT2 (l, 0)
                                 rf     po                             rf         po
                                  RT1 (l, 1)                            RT1 (l, 1)
                                        po          rf                            po
                                  RT1 (l, 1)                            RT1 (l, )
                                        po
                                  RT1 (l, 0)
                                 1                                     2
                                         Winit (l, 0)                             Winit (l, 0)
                                      mo       mo                            mo          mo
                                 WT1 (l, 1)         WT2 (l, 0)          WT1 (l, 1)            WT2 (l, 0)
                                 rf     po                                        po          rf
                                                rf
                                  RT1 (l, 1)                            RT1 (l, 0)
                                        po
                                  RT1 (l, 0)
                             Figure 5: Execution graphs of Fig. 1 where l = locked.


                                                                  5
                                                                       yes (AT violation)

        S.push(Ginit )
                                                 no              yes
                         no
                                         rf
                                    ∃r.⊥→r ∈ G        TG 6= 0/         Pick T ∈ TG
                                                                                        F: assertion      report G as a
                                                  yes                                                     counterexample
                                                                                      R: reads
                                                                            Next                        0                                 read
                                                                                      from x for all WUm (x, v) ∈ G:                             yes            rf
                            yes                   consM (G)            instruction of                                                   in await     S.push(G[⊥ → Rm
                                                                                                                                                                   T (x, )])
                  |S| > 0                                                                                     m0      rf m
           no
                                  G := S.pop()
                                                  ∧¬W(G)                     T                  S.push(G[W   U (x, v) → RT (x, v)])       loop
                                                                                                 for all G0 ∈ CalcRev.(G,WTm (x, v)):
 report success                                                               W: writes v to x      S.push(G0 )                             no
                                                          no

                                                                         Figure 6: AMC exploration
can read from, there are at most n − 1 failedUiterations of any await in graphs in GF∗ . If there are at most a ∈ N
executed instances of awaits, we have GF∗ ⊆ k∈{ 0,...,a·(n−1) } Gk which is a union of a finite number of finite sets
and thus finite. We will later define sufficient conditions to ensure this.
    We proceed to discuss how AMC discovers AT violations. Consider execution graph β . In the first iteration
of the await, T1 reads from WT1 (l, 1). In the next iteration, T1 ’s read has no incoming rf-edge; coherence forbids
T1 from reading an older write and the await progress condition forbids it from reading the same write. Since
there is no further write to the same location, AMC detects an AT violation and uses the finite graph β as the
evidence. In general, if the mo of every polled variable is finite, then AT violations from G∞ are represented by
graphs in G∞ ∗ where some read has no incoming rf-edge. AMC exploits this fact to detect AT violations.
Conditions of AMC. State-of-the-art SMC only terminates and produces correct results for terminating and
loop-free programs4 . AMC extends the domain of SMC to a fragment of looping and/or non-terminating
programs, on which AMC not only produces correct results but can also decide termination. With the generic
client code provided by VS YNC, all synchronization primitives we have studied are in this fragment, showing it
is practically useful. The fragment includes all programs satisfying the following two principles:
Bounded-Length Principle: There is a bound b (chosen globally for the program) so that all executions in G1
       of the program have length ≤ b.
Bounded-Effect Principle: Failed await iterations satisfy the bounded-effect principle, that the effect of the
       loop iteration is limited to that loop iteration.
    Informally, the Bounded-Length principle means that the number of execution steps outside of awaits is
bounded, and each individual iteration of a failed await is also bounded. Obviously, infinite loops in the client
code are disallowed by the Bounded-Length principle.
    The Bounded-Effect principle means that no side-effects from failed await iterations must be referenced by
either subsequent loop iterations, other threads, or outside the loop. The principle can be defined more precisely
in terms of execution graphs: rf-edges starting with writes5 generated by a failed await iteration must go to read
events that are generated in the same iteration. Figure 4 illustrates the principle: rf-edges from decrements in the
failed iterations of the loop body B go to subsequent iterations of the loop, but for the outer loop only the final
iteration has outgoing rf-edges. The Bounded-Effect principle allows removing any failed iteration from a graph
without affecting the rest of the graph since the effects of the failed iteration are never referenced outside the
iteration. This implies that any bugs in graphs from GF are also present in graphs in G1 . Furthermore, if the
Bounded-Effect principle and the Bounded-Length principle hold, then graphs in Gk are bounded for every k.
The bound for Gk can be computed as b + (k − 1) · x where b is the bound for G1 and x is the maximum number
of steps in a failed iteration of an await in G1 .
    The two principles jointly imply that mos and the number of awaits are bounded, thus, as discussed before,
GF∗ is a finite set and G∞∗ contains only finite graphs, and AMC always terminates. In synchronization primitives,
awaits either just poll a variable (without side effects) or perform some operation which only changes global
state if it succeeds, e.g., await_while(q==0); or await_while(!trylock(&L)); These awaits satisfy the
Bounded-Effect principle. The former does not have any side effects. The latter encapsulates its local side
   4 Exploration depths are often used to transform programs with loops into loop-free programs, potentially changing the behavior of the

program.
   5 Only writes that change the value of the variable matter here.




                                                                                             6
effects inside trylock(&L), which can therefore not leave failed iteration of the loop. A global side effect (i.e.,
acquiring the lock) only occurs in the last iteration of the await (cf. Fig. 4). When called in our generic client
code, synchronization primitives also satisfy the Bounded-Length principle: the client code invokes the functions
of the primitives only a bounded number of times, and each function of the primitives is also bounded.
AMC Correctness. For programs which satisfy the Bounded-Length principle and the Bounded-Effect principle,
1) AMC terminates, 2) AMC detects every possible safety violation, 3) AMC detects every possible non-
terminating await, and 4) AMC has no false positives. See Section 2 for the formal proof.

1.3     Implementing AMC
We implement AMC on top of GenMC [16, 17], a highly advanced SMC from the literature. The exploration
algorithm in Fig. 6 extends GenMC’s algorithm with the highlighted essential changes: 1) detecting AT violations
through reads with no incoming rf-edge; 2) checking if W(G) holds to filter out graphs G in which an await
reads from the same writes in multiple iterations. AMC builds up execution graphs through a kind of depth-first
search, starting with an empty graph Ginit , which is extended step-by-step with new events and edges. The search
is driven by a stack S of possibly incomplete and/or inconsistent graphs that is initialized to contain only Ginit .
     Each iteration of the exploration pops a graph G from S. If the graph G violates the consistency predicate
consM or is wasteful (i.e., W(G) holds), it is discarded and the iteration ends. Otherwise, a program state is
reconstructed by emulating the execution of threads until every thread executed all its events in G; e.g., if a thread
U executes a read instruction that corresponds to RU (x, 0) in G, the emulator looks into G for the corresponding
read event and returns the value read by the event, in this case 0. We denote the set of runnable threads in
the reconstructed program state by TG . Initially, all threads are runnable; a thread is removed from TG once it
terminates or if it is stuck in an await. If the set is not empty, we can explore further and pick some arbitrary
thread T ∈ TG to run next. We emulate the next instruction of T in the reconstructed program state. For the sake
of brevity, we discuss only three types of instructions: failed assertions6 , writes, and reads.
F: an assertion failed. We stop the exploration and report G.
If the instruction executes a read or write, a new graph with the corresponding event should be generated. Usually
there are several options for the event; for each option, a new graph is generated and pushed on a stack S. In
particular:
W: a write event w is added. In this case, for every existing read r to the same variable, a partial7 copy of G with
                    rf
        an edge w → r is generated and pushed into S.
                                                                                                                        rf
R: a read event r is added; for every write event w in G a copy of G with an additional edge w → r is generated
       and pushed into S.
Crucially, if the read event r is in an await, an additional copy of G is generated in which r has no incoming
                                             rf
rf-edge (we write this new graph as G[⊥ → r]). This missing rf-edge indicates a potential AT violation. It is
not an actual AT violation yet because a new write w to the same variable might be added by another thread
later during exploration. If such a write is added, it leads to the generation of two types of graphs: graphs in
                                                                 rf
which r is still missing an rf-edge, and graphs with the edge w → r where r no longer has a missing rf-edge (and
the potential AT violation got resolved). Otherwise, if a missing rf-edge is still present and no other thread can
be run, we know that such a write cannot become available anymore; the potential AT violation turns into an
actual AT violation. The algorithm detects the violation after popping a graph G in which no threads can be
                                                                     rf
run (TG = 0),
            / but a read without incoming rf-edge is present (⊥ → r ∈ G), and this missing rf-edge could not
be resolved except through a wasteful execution, i.e., every consistent graph G0 obtained by adding the missing
rf-edge and completing the await iteration is wasteful.
    6 The assertion expression assert(x==0) consists of at least two instructions: the first reads x, and the second just compares the result

to zero and potentially fails the assertion. Note that once the rf-edge for the event corresponding to the first instruction has been fixed,
whether the second instruction is a failed assertion or not is also fixed.
    7 For details we refer the reader to the function CalcRevisits from [16].




                                                                     7
2     Proving the Correctness of Await Model Checking
In this section we formally prove Theorem 1 to show that our AMC is correct. In order to formally prove this
theorem, first we define a tiny concurrent assembly-like language in §2.1, which follows our Bounded-Length
principle and allows us to map the execution graphs to the execution of instruction sequences. Then we formalize
the Bounded-Effect principle in §2.2. Finally we give the formal representation of Theorem 1 and prove it in
§2.3. Throughout this section we use the notation of [16].
Theorem 1 (AMC Correctness). For programs which satisfy the Bounded-Length principle and the Bounded
Effect principle, 1) AMC terminates, 2) AMC detects every possible safety violation, 3) AMC detects every
possible non-terminating await, and 4) AMC has no false positives.

2.1   The tiny concurrent assembly-like language
To have a formal foundation for these proofs we need to provide a formal programming language. Without such a
programming language, execution graphs just float in the air, detached from any program. Using the consistency
predicate consM we can state that an execution graph can be generated by the weak memory model, but not
whether it can be generated by a given program.

                                                     Winit x, 0

                                             Thread 1
                                                             rf
                                             Rrlx x, 0            rf
                                                                       rf
                                             Rrlx x, 0                      rf


                                             Rrlx x, 0

                                             Rrlx x, 0

                                               ..
                                                .
                                     Figure 7: Divergent execution graph

    For example, the non-terminating execution graph in Fig. 7 consisting only of reads from the initial store
is consistent with all standard memory models, but is obviously irrelevant to most programs. If we were only
to decide whether a non-terminating execution graph is consistent with the memory model or not, we could
simply always return true and be done with it. What we really want to decide is whether a given program
(which satisfies our two principles) has a non-terminating execution graph which is consistent with the memory
model. For this purpose we will in this section define a tiny assembly-like programming language, and define
whether a program P can generate an execution graph G through a new consistency predicate consP (G). This will
require formally defining an execution-graph driven semantics for the language, in which threads are executed in
isolation using values provided by an execution graph. After we define the programming language, we formally
define the Bounded-Effect principle. We then show that if the Bounded-Effect principle is satisfied, we can
always remove one failed iteration of an await from a graph without making the graph inconsistent with the
program. This will allow us to show that graphs in GF can always be “trimmed” to a graph in GF∗ which has the
same error events, and thus all safety violations are detected by AMC. Next we show that we can also add failed
iterations of an await; indeed, for graphs in G∞∗ we can add infinitely many such iterations. Thus these graphs
can be “extended” to graphs in G∞ which are consistent with the program. This implies that there are not false
positives. Finally we show that due to the Bounded-Length dance principle and the Bounded-Effect principle,
graphs in GF∗ and G∞ ∗ have a bounded number of failed iterations of awaits, and the remaining steps are bounded
as well. Thus the search space itself must be finite, and AMC always terminates.



                                                         8
    (Program) P := T0 k . . . k Ti k . . . k Tn        Composition of parallel threads Ti
        (Thread) T := S0 ; . . . ; Sn                  Sequence of statements Si
          (Stmts) S := await(n,κ) | step(ε,δ)          Await-loop and non-await-loop steps.
    (LoopCon) κ ∈ State → { 0, 1 }                     Loop condition
        (EvtGen) ε ∈ State → Events                    Event generator
        (StTrans) δ ∈ State × Value? → Update          State transformer
         (Events) e := Rm (x) | W m (x, v) | F m | E   Read, write, fence, error events. x ∈ Location, v ∈ Value.
        (Modes) m := rlx | rel | acq | sc              Barrier modes
          (State) σ ∈ Register → Value                 Set of thread-local states.
        (Update) µ ∈ Register * Value                  Updated register values.
         (Register)    ...                             Set of thread-local registers.
        (Location)     ...                             Set of shared memory locations.
            (Value)    ...                             Set of possible values of registers and memory locations.

                                 Figure 8: Compact Syntax and Types of our Language


         C-like program                                  Our toy language
                                                                 step(λ σ. Wrlx (x, σ(r1)), λ σ _. [ ]);
                             x = r1 ;                            step(λ σ. Rrlx (y),        λ σ v. [r1 → v ]);
                             r1 = y;                             step(λ σ. match σ(r1) with
                             if ( r1 == 0)                         0 → Rrlx (x)
                             r2 = x;
                                                                   _ → Frlx ,
                                                                 λ σ v. match σ(r1) with
                                                                   0 → [r2 → v]
                                                                   _ → [ ])

                 Figure 9: Using lambda functions inside step to implement different control paths

2.1.1    Syntax
Recall that the Bounded-Length principle requires that the number of steps inside await loops and the number of
steps outside awaits are bounded. We define a tiny concurrent assembly-like language which represents such
programs, but not programs that violate the Bounded-Length principle. The purpose of this language is to allow
us to prove things easily, not to conveniently program in it. Thus instead of a variety of statements, we consider
only two statements: await loops (await) and event generating instructions (step). The syntax and types of our
language is summarized in Fig. 8. The event generating instructions step use a pair of two lambda functions
to generate events and modify the thread local state. Thus the execution of the steps yields a sequence σ(t) of
thread-local states. We illustrate this at hand of the small example in Fig. 9, which we execute starting with the
(arbitrarily picked for demonstrative purposes) thread local state
                                                         (
                                                 0        5 r = r1
                                                σ (r) =
                                                          0 r = r2
in which the value of r1 is 5 and the value of r2 is 1. The first instruction of the program first evaluates
λ σ. Wrlx (x, σ(r1)) on σ0 to determine which event (if any) should be generated by this instruction. In this case,
the generated event is
                                          W rlx (x, σ0 (r1)) = W rlx (x, 5)


                                                            9
which writes 5 to variable x. Next, the function λ _ _. [ ] is evaluated on σ0 to determine the set of changed
registers and their new value in the next thread local state σ1 . This function takes a second parameter which
represents the value returned by the generated event in case the generated event is a read. Because the event in
this case is not a read, no value is returned, and the function simply ignores the second parameter. The empty list
[ ] indicates that no registers should be updated. Thus

                                                     σ1 = σ0

and execution proceeds with the next instruction. The second instruction generates the read event

                                                      Rrlx (y)

which reads the value of variable y. Assume for the sake of demonstration that this read (e.g., due to some other
thread not shown here) returns the value 8. Now the function λ σ v. [r1 → v] is evaluated on σ1 and v = 8. The
result [r1 → 8] indicates that the value of r1 should be updated to 8, and the next state σ2 is computed as
                                                     (
                                              2        8       r = r1
                                             σ (r) =
                                                       σ1 (r) o.w.

In this state, the third instruction is executed. Because in σ2 , the value of r1 is not 0, the match goes to the
second case, in which no event is generated (indicated by F(rlx ), i.e., a relaxed fence which indicates a NOP).
Thus again there is no read result of v, and the next state σ3 is computed simply as

                                                     σ3 = σ2


         normal code                                    encoding in toy language
                                                        event generators       state transformers

          r1 = x;                                        λ _. Rrlx (x)            λ _ v. [r1 → v]

          y = r1 +2;                                     λ σ. Wrlx (x, σ(r1)+2)   λ _ _. [ ]

                                                         λ _. Rrlx (x)            λ _ v. [r1 → v]
          if (x ==1){
                                                         λ σ. match σ(r1)         λ σ v. match σ(r1)
              y = 2;
              r2 = z;                                      with                     with
          } else {                                           1 → Wrlx (y, 2)          1. [ ]
              r2 = z;                                        _ → Rrlx (z)             _. [r1 → v]
              y = r2 ;                                   λ σ. match σ(r1)         λ σ v. match σ(r1)
          }                                                with                     with
                                                             1. Rrlx (z)              1. [r2 → v]
                                                             _. Wrlx (y, σ(r2))       _. [ ]

         for ( r1 = 0; r1 < 3; r1 ++)                    λ σ. Wrlx (x, σ(r1))     λ σ _. [r1 → σ(r1)+1]
         {                                               λ σ. Wrlx (x, σ(r1))     λ σ _. [r1 → σ(r1)+1]
             x = r1 ;                                    λ σ. Wrlx (x, σ(r1))     λ σ _. [r1 → σ(r1)+1]
         }

      Figure 10: Example Encodings of Language Constructs as Event-generator/State-transformer Pairs

    Note that each thread’s program text is finite, and the only allowed loops are awaits. Thus programs with
infinite behaviors or unbounded executions (which violate the Bounded-Length principle) can not be represented
in this language.
    Each statement generates up to one event that depends on a thread-local state, and modifies the thread-local
state based on the previous state and (in case a read event was generated) the result of the read. This is encoded


                                                        10
                      do_awaitwhile ({                   step(λ _. Rrlx (y), λ _ v. [r1 → v ]);
                           r1 = y;                       step(λ _. Rrlx (x), λ _ v. [r2 → v ]);
                      },x ==1)                           await(2, λ σ. σ(r2) == 1)
                     Figure 11: Encoding of Do-Await-While as a Program in our Language
using two types of lambda functions: the event generators that map the current state an event (possibly F rlx ), i.e.,
have type
                                                State → Event
and the state transformers that map the current state and possibly a read result to an update to thread-local state
representing the new value of all the registers that are changed by the instruction, i.e., have type

                                             State × Value? → Update

Here T ? is a so called option type, which is similar to the nullable types of C#: each value v ∈ T ? is either a
value of T or ⊥ (standing for “none” or “null”):

                                            v ∈ T ? ⇐⇒ v ∈ T ∨ v = ⊥

    Await loops are the only control construct in our language. Apart from awaits, the control of the thread only
moves forward, one statement at a time. Different conditional branches are implemented through internal logic
of the event generating instructions: the state keeps track of the active branch in the code, and the event generator
and state transformer functions do a case split on this state. Bounded loops have to be unrolled. See Fig. 10.
    We formalize the syntax of the language. There is a fixed, finite set of threads T and each thread T ∈ T has a
finite program text PT which is a sequence of statements. We denote the k-th statement in the program text of
thread T by PT (k). A statement is either an an event generating instruction or a do-await-while statement. We
assume that the set of registers, values, and locations are all finite.
Event Generating Instruction An event generating instruction has the syntax
                                                  step(ε,δ)
where
                                         ε : State → Event
is an event generator and
                                            δ : State × Value? → Update
is a state transformer. Note that the event generating instruction is roughly a tuple of two functions ε and δ.
When the statement is executed in a thread-local state s ∈ State, we first evaluate ε(σ) to determine which event
is generated. If this event is a read, it returns a value v (defined based on reads-from edges in an execution graph
G), which is then passed to δ to compute the new values for updated registers in the update δ(σ, v). The next
state is then defined by taking all new values from δ(σ, v) and the remaining (unchanged) values from s.
Do-Await-While A do-await-while statement has the syntax
                                                           await(n,κ)
where n ∈ { 0, 1, 2, . . . } is the number of statements in the loop, and the loop condition κ : State → { 0, 1 } is a
predicate over states telling us whether we must stay in the loop. If this statement is executed in thread-local
state s, we first evaluate κ(σ). In case κ(σ) evaluates to true, the control jumps back n statements, thus repeating
the loop; otherwise it moves one statement ahead, thus exiting the loop.
Syntactic Restriction of Awaits We add two syntactic restrictions of awaits: 1) no nesting of awaits and 2) an
await which jumps back n statements needs to be at least at position n in the program.

                    PT (k) = await(n,_)    →     n ≤ k ∧ ∀k0 ∈ [k − n : k). PT (k0 ) 6= await(_,_)

These restrictions will allow us to easily identify steps in an iteration of an await as steps in the range [k − n : k)



                                                          11
                                             T (t) − m
                                            kG
                                                                   ..         v
                                                                    .          n
                                           T (t) − m + v
                                          kG                 await(v,_);
                                                                   ..
                                                                    .
                                               T (t)
                                              kG             await(n,_);


                                          Figure 12: Two overlapping awaits
2.1.2   Semantics
The semantics of our language consist of two components: an execution graph G, which represents the concurrent
execution of the events, and local instruction sequences that generate and refer to these events. At first glance,
the instruction sequences and the event graph interlock like gears: the instruction sequences generate the events
in the event graph, e.g., the reads and writes, and the event graph generates the values that are returned by those
reads to the instruction sequences. Of course, the values returned by reads determine which events are generated
next by the instruction sequences. Unfortunately, it is a bit more complex than this: due to weak memory models,
the interlock is actually cyclical; a write event w of thread A can be generated based on a value returned by a
previous read of A, which reads from a write event of thread B, which is generated based on a previous read of B
which reads from w. Thus a simple step-by-step parallel construction of G and the instruction sequences is not
possible.
    Instead, we follow a more indirect (so called axiomatic) semantics: we take an arbitrary (potentially cyclical)
execution graph G and try to justify it ad-hoc by finding local instruction sequences that are consistent with the
events in the graph, i.e., 1) every event in G is generated by the instruction sequences, and 2) the instruction
sequences use read-results from the graph G. We define this in two steps: at first we ignore for simplicity the
consistency predicate consM (G) which states that G is consistent with the memory model, and only check that G
can be justified by the program text. We define this by a predicate consP (G) stating that G is consistent with
the program. Then we make the definition complete by combining the two consistency predicates into a single
predicate
                                        consPM (G) = consP (G) ∧ consM (G)
which states that the execution graph G is consistent with the program P under the weak memory model M. We
borrow the notation of execution graphs from the work of Vafeiadis et. al [16], with the minor change that our
events include barrier modes.
Defining consP (G) The semantics of our language is defined with relation to an execution graph G, which
provides the values individual reads read. With reference to these values, the local program text of each thread
can be executed locally. The graph is consistent with the program text if it contains exactly the events that occur
during this local execution. The local execution of thread T is described by four sequences, which are defined by
mutual recursion on the number of executed steps t ∈ { 0, 1, 2, . . . }: the thread local state σTG (t) after t steps, the
position of control kG T (t) after t steps, the (potential) event generated in the t-th step eT (t), and the (potential)
                                                                                                G
read result vG (t) of that event. The definitions of eTG (t) and vTG (t) are not themselves recursive but refer to σTG (t),
             T

while themselves being referenced in the definition of σTG (t + 1). For this reason, the four sequences do not all
have the same length. We denote the number of execution steps of thread T by NGT ∈ N ∪ { ∞ }, where NGT = ∞
indicates that the thread does not terminate and hence makes infinitely many steps. The number of steps NGT
coincides with the length |eTG (t)| and |vTG (t)| of the sequences eTG (t) of events and vTG (t) of read results of thread
T as every step generates up to one event and returns up to one read result

                                                |eTG (t)| = |vTG (t)| = NGT




                                                            12
As usual for these fence post cases, the number of states and positions of control is NGT + 1
                                             |σTG (t)| = |kG
                                                           T
                                                             (t)| = NGT + 1
Position of Control     The position of control
                                                 T
                                                kG (t) ∈ { 0, 1, 2, . . . }
                                        T (t)) to be executed by thread T after executing t steps. All programs start
is the index of the next statement PT (kG
at the first statement, i.e.,
                                                       T
                                                      kG (0) = 0
                                                                                       T (0)) = P (0). After t ≤ N T
and thus the first statement to be executed is the first statement of the program PT (kG         T                G
                                                                    T
steps, the position of control may leave the program text, i.e., kG (t) may no longer be an index in the sequence
PT ((k)) of statements of thread T
                                                   T
                                                  kG (t) ≥ |PT ((k))|
In this case, the computation of thread T ends:
                                            T
                                           kG (t) ≥ |PT ((k))| → NGT = t
                      T (t + 1) that needs to be defined. Otherwise, the execution of the t-th step changes the
and thus there is no kG
position based on the statement PT (kGT (t)) executed in that step. We abbreviate

                                                   T            T
                                                  SG (t) = PT (kG (t))
    If the this statement is an event generating instruction, we always move to the next statement, i.e.,
                                    T                               T            T
                               PT (kG (t)) = step(_,_)      →      kG (t + 1) = kG (t) + 1
For a do-await-while await(n,κ), k is either also incremented by 1 (the loop is exited) or decremented by n (the
loop is continued), depending on whether κ evaluates to false or true in the internal state σTG (t) of thread T after t
steps:                                                            (
                          T                            T            kT (t) + 1 κ(σTG (t)) = 0
                     PT (kG (t)) = await(n,κ) → kG (t + 1) = G       T (t) − n o.w.
                                                                    kG
Event Sequence This t-th step (with t < NGT ) generates the event
                                                    eTG (t) ∈ Event
which is either ε(σTG (t)) if the statement executed in this step is an event generating instruction step(ε,_)
                                      T
                                 PT (kG (t)) = step(ε,_)       →       eTG (t) = ε(σTG (t))
or, in case the statement is a do-await-while, a NOP event
                                        T
                                   PT (kG (t)) = await(_,_)        →      eTG (t) = F rlx
This event must be in G or G is not consistent with the program. Recall that G stores the event together with
meta data indicating the thread T and the event index t in the program order of T . If no event with this meta data
exists in the graph, the graph represents a partial execution of the program. In this case we stop execution of
thread T before the event is generated
                                          hT, t, −i 6∈ G.E       →       NT = t
Otherwise, the event and its meta data from the triplet hT, t, eTG (t)i. If some event with this meta data exists in
the graph, but not this particular event, then the program generated a different event than the one provided by the
graph; the graph is inconsistent with the program.
                                 hT, t, ei ∈ G.E ∧ e 6= eTG (t)        →      ¬consP (G)
Note that T and t already uniquely identify eTG (t) in a consistent execution graph. To avoid redundancy we
abbreviate
                                          hhT, tiiG = hT, t, eTG (t)i


                                                           13
Read Result The read result
                                                   vTG (t) ∈ Value?
is the value returned by a read event generated in step t < NGT of thread T . If no read event is generated, there is
no read result vTG (t)
                                        eTG (t) 6= R− (−) → vTG (t) = ⊥
Otherwise, the read reads from the write w = G.rf(hhT, tiiG i) and returns the value w.val written by that write.
Note that in the case of a missing rf-edge, w may be ⊥ even though eTG (t) is a read event. In such cases, we
return the read result ⊥. However, an instruction that generates a read event usually depends on the read result to
compute the next state. Thus we will define in the next section that the thread-local execution terminates in case
eTG (t) is a read event but the read result is ⊥. We collect the read result as the value vTG (t)
                                                     (
                      T        o               T       G.rf(hhT, tiiG ).val G.rf(hhT, tiiG i) 6= ⊥
                     eG (t) = R (x) → vG (t) =
                                                       ⊥                      o.w

State Sequence     The thread-local state of thread T after executing t steps

                                                   σTG (t) ∈ State

contains the values of all thread-local registers. We leave the initial state

                                                       σTG (0)

of thread T uninterpreted. Each step then updates the local state based on the executed statement. Do-await-whiles
never change the program state
                                     T
                                PT (kG (t)) = await(_,_)    →     σTG (t + 1) = σTG (t)

For event generating instructions, we consider two cases: the first (regular) case is that the value vTG (t) matches
the event eTG (t) in the sense that vTG (t) provides a value if eTG (t) is a read. In this case the event generating
instruction step(_,δ) with state transformer δ updates the state based on δ under control of the read result vTG (t):
                                 T
                            PT (kG (t)) = step(_,δ) ∧ (eTG (t) 6= R− (−) ∨ vTG (t) 6= ⊥)
                                          →     σTG (t + 1) = σTG (t)  δ(σTG (t), vTG (t))

Here  is the update operator which takes all the new (updated) register values from δ(σ, v) and the remaining
(unchanged) register values from s:
                                                   (
                                                     σ0 (r) r ∈ Dom(σ0 )
                                    (σ  σ0 )(r) =
                                                     σ(r) o.w.

In the second (irregular) case, step t generated a read event but no read-result was returned. In this case the
computation gets stuck. We define that t is the last step. Since steps 0, . . . , t have been executed the number of
steps is thus NGT = t + 1. Thus formally we need to define a state σTG (t + 1), despite the computation being stuck.
We arbitrarily define σTG (t + 1) = σTG (t).
            T
       PT (kG (t)) = step(_,δ) ∧ eTG (t) = R− (−) ∧ vTG (t) = ⊥       →     NGT = t + 1 ∧ σTG (t + 1) = σTG (t)

No Superfluous Events We have so far checked that every event generated by the program is also in G.
However, G is only consistent with a program if there is also no event in G that was not generated by the program,
i.e., there are no superfluous events. More precisely, G is consistent with the program P exactly when the set of
events G.E in G is exactly the set of events (plus meta data) generated by P:

                            consP (G) ⇐⇒ G.E = hhT, tiiG T ∈ T , t < NGT
                                                         


                                                           14
Register Read-From Recall that the Bounded-Effect principle states that there must not be a visible side effect
of a failed iteration of an await. Between threads, the only potentially visible side effects are the generated
stores. Within a thread, updates to registers can also be visible, provided these registers are not overwritten in the
mean-time. We define a register read-from relation within events of a single thread
                                                                 G.rrf ⊆ G.po
which holds between events e and e0 exactly when the statement that generated e0 “depends” on any registers
updated by the statement that generated e which have not been overwritten in the meantime. More precisely,
we put a register read-from edge in the graph between the t-th and u-th steps (with u ≥ t) if any function in the
               T (u))(G) executed by the u-th step depends on the visible output of the t-th to the u-th step:
statement PT (kG
                        rrf                                                    T
          hhT, tiiG −→ hhT, uiiG               ⇐⇒         u ≥ t ∧ ∃ f ∈ F(PT (kG (u))(G)). depends-on( f , visTG (t, u))
To define what it means to “depend” on these registers, we look at the functions ε, δ, κ of the statement and see
whether the registers can affect the functions. We collect the functions in statement S in a set F(S) defined as
follows                                        (
                                                { ε, δ } S = step(ε, δ)
                                       F(S) =
                                                {κ}      S = await(_, κ)
A function f ∈ F(S) depends on a set of registers R ⊆ Register if there are two states which only differ on
registers in R on which f produces different results8
                depends-on( f , R)           ⇐⇒         ∃σ, σ0 ∈ State. (∀r 6∈ R. σ(r) = σ0 (r)) ∧ f (σ) 6= f (σ0 )
To unify notation we define an update δTG (t) for each step t by
                       (
                                                 T (t)) = step(_, δ) ∧ (eT (t) 6= R− (−) ∨ vT (t) 6= ⊥)
                        δ(σTG (t), vTG (t)) PT (kG
             δTG (t) =                                                   G                  G
                        0/                  o.w.
where 0/ is the empty update (no registers changed). A straightforward induction shows:
Lemma 1.
                                           σTG (t + 1) = σTG (t)  δTG (t)
    We define the visible output of the t-th step the the u-th step to be the set of registers that are updated by the
t-th step but not by the steps before u
                                                                                           Dom(δTG (u0 ))
                                                                                 [
                                         visTG (t, u) = Dom(δTG (t)) \
                                                                               u0 ∈(t:u)

Iterations of Await In this section we define the steps that constitute iterations of await. These are steps that
execute statements with numbers k0 ∈ [k − n : k] where statement number k is a do-await-while statement that
jumps back n steps. We enumerate these steps k which are endpoints of await iterations.
                           endTG (0) = min t PT (kG  T
                                           
                                                       (t)) = await(_, _)
                           T                         T          T
                                           
                        endG (q + 1) = min t > endG (q) PT (kG    (t)) = await(_, _)
We denote the length of such an iteration, i.e., the number n of steps jumped back by the do-await-while-statement,
by
                             lenTG (q) = n where PT (kG     T
                                                              (endTG (q))) = await(n, _)
The start point (k − n) of the q-th iteration is defined by
                                                   startTG (q) = endTG (q) − lenTG (q)
    We show that the intervals [startTG (q) : endTG (q)] for all q do not overlap. For this it suffices to show that only
the last step in such an interval executes a do-await-while statement.
  8 For the sake of simplicity we use here curried notation for f = δ, i.e., δ(σ) 6= δ(σ0 ) iff there is a v such that δ(σ, v) 6= δ(σ0 , v).




                                                                        15
Lemma 2.
                            t ∈ [startTG (q) : endTG (q))   →     PGT (kG
                                                                        T
                                                                          (t)) 6= await(_, _)
Proof. Assume for the sake of contradiction that step t executes a do-await-while. W.l.o.g. t is the last step to do
so
                      t = max u ∈ [startTG (q) : endTG (q)) PGT (kGT
                               
                                                                     (u)) = await(_, _)
Since the remaining steps between t and endTG (q) are not do-await-while statements, they move the position of
control ahead one statement at a time. Thus the difference in the positions of control is equal to the difference in
the ste number.
                                  T
                                 kG (endTG (q)) − kG
                                                   T
                                                     (t + 1) = endTG (q) − (t + 1)
Furthermore, the loop condition of step t can not be satisfied since otherwise control would jump back and then
                        T (t) a second time; but this contradicts the assumption that no more do-await-while
have to cross position kG
statements are executed. Thus
                                                T             T
                                               kG (t + 1) = kG  (t)
and we conclude with simple arithmetic
                                        T        T
                                       kG (t) = kG (endTG (q)) − (endTG (q) − t)

Since t is in the interval [startTG (q) : endTG (q)) which by definition has length lenTG (q), we conclude first

                                                endTG (q) − t < lenTG (q)

and then that the await must be positioned in the last lenTG (q) statements before the q-th executed await
                                        T         T
                                       kG (t) ∈ [kG (end) − lenTG (q) : kG
                                                                         T
                                                                           (end))

but this contradicts the assumption that awaits are never nested.
   We conclude that interval number q + 1 starts after interval number q ends. Monotonicity then immediately
implies that the intervals are pairwise disjoint.
Lemma 3.
                                             endTG (q) < startTG (q + 1)
Proof. By definition, step endTG (q) executes a do-await-while statement
                                                T
                                           PT (kG (endTG (q))) = await(_, _)

By contraposition of Lemma 2, the step is not in interval number q + 1

                                      endTG (q) 6∈ [startTG (q + 1) : endTG (q + 1))

Due to monotonicity interval number q ends before interval number q + 1

                                                endTG (q) < endTG (q + 1)

and the claim follows
                                               endTG (q) < startTG (q + 1)


    Iteration q is failed if the loop condition in step endTG (q) evaluates to 1:

                failTG (q) ⇐⇒ κ(σTG (endTG (q))) = 1                   T
                                                            where PT (kG (endTG (q))) = await(_, κ)




                                                            16
We plan to cut all failed iterations from the graph which result in a wasteful graph. These are failed iterations q
in which the next failed iteration reads from exactly the same stores. We define this precisely through a predicate
WI TG (q):

 WI TG (q) ⇐⇒ failTG (q) ∧ ∀m ≤ lenTG (q). eTG (startTG (q) + m) = R− (−)
                                                           → G.rf(hhT, startTG (q) + miiG ) = G.rf(hhT, startTG (q + 1) + miiG )

Iff a graph has any such iterations, we say that is wasteful. Formally:

                                                    W(G) ⇐⇒ ∀T, q. ¬WI TG (q)

2.2     Formalizing the Bounded-Effect principle
The Bounded-Effect principle is now easily formalized. We define BE(G) to hold if in graph G no register
reads-from arrow leaves a failed iteration of an await. For the sake of simplicity we fully forbid generating write
events in failed iterations of awaits. This is unlikely to be a practical restriction9 ; as reads-from edges from such
writes that leave the iteration are anyways forbidden, this directly only affects loop-internal write-read pairs,
which can be simulated using registers.
Definition 3. Graph G satisfies the Bounded-Effect principle, i.e., BE(G), iff for all threads T , failed await
iterations q with failTG (q), and step numbers t ∈ [startTG (q) : endTG (q)) we have:
    1. no write event is generated in step t of thread T

                                                                eTG (t) 6= W − (−, −)

    2. if the event generated in step t of thread T is register read-from by the event generated in step u of thread
       T , then u is in the same failed iteration q
                                                     rrf
                                       hhT, tiiG −→ hhT, uiiG            →      u ∈ [startTG (q) : endTG (q))

    In the remainder of this text, we assume: all graphs that are consistent with the memory model and with P
satisfy the Bounded-Effect principle

                                                    ∀G. consPM (G)         →       BE(G)                                                     (1)

2.3     Proving the main theorem
We define the sets GF and G∞ of execution graphs with a finite resp. infinite number of failed await iterations by

                           GF = G consPM (G) ∧ ∀T. ∃q. ∀q0 ≥ q. ¬failTG (q0 )
                                 

                           G∞ = G consPM (G) ∧ ∃T. ∀q. ∃q0 ≥ q. failTG (q0 )
                                 

                              = G consPM (G) \ GF
                                 

Await-termination holds if G∞ is empty
                                                             AT ⇐⇒ G∞ = 0/
   We now show a series of lemmas that lead us to the main theorem:
Theorem 1.
     The set GF∗ = G ∈ GF ¬W(G) of non-wasteful execution graphs is finite, and every G ∈ G∞
                   
  1.                                                                                      ∗ =
       G ∈ GF∗ stagnant(G) which is stagnant is finite.
    2. if an error event E exists in a graph G ∈ GF , it also exists in a graph G0 ∈ GF∗
   9 It is possible to construct theoretical examples where this restriction changes the logic of the code, but we are not aware of any practical

examples. In any case, the restriction can be lifted with considerable elbow grease.


                                                                      17
   3. every graph G ∈ G∞ can be cut to a graph G0 ∈ G∞
                                                     ∗

   4. every graph G ∈ G∞                             0
                       ∗ can be extended to a graph G ∈ G
                                                          ∞


     In the proofs we ignore the memory model consistency. This can be easily proven on a case by case basis
(i.e., for concrete M) but a generic proof must rely on certain abstract features of the memory model which are
hard to identify in generic fashion. We leave a generic proof with appropriate conditions as future work.
     We first show that after a failed iteration, we return to the startof the await and immediately repeat the iteration
(possibly with a different outcome).
Lemma 4.

                               failTG (q)   →      T
                                                  kG (endTG (q) + 1) = kG
                                                                        T
                                                                          (startTG (q))
                                                    ∧ startTG (q + 1) = endTG (q) + 1
                                                     ∧ endTG (q + 1) = endTG (q) + 1 + n

Proof. By definition the loop condition κ in step endTG (q) is satisfied
                                   T
                              PT (kG (endTG (q))) = await(n,κ) ∧ κ(σTG (endTG (q))) = 1

Thus by the semantics of the language, control jumps back n = lenTG (q) steps
                                         T
                                        kG                    T
                                           (endTG (q) + 1) = kG (endTG (q)) − n

By Lemma 2 the previous n steps all do not execute do-await-while statements and thus moved control forward
linearly; the first part of the claim follows
                                T
                               kG (endTG (q)) − n = kG
                                                     T
                                                       (endTG (q) − n) = kG
                                                                          T
                                                                            (startTG (q))

We next prove the third part of the claim. Observe that the next n statements are exactly the same (non-await)
statements, and thus after an additional n steps we have again
                            T
                           kG (endTG (q) + 1 + n) = kG
                                                     T
                                                       (endTG (q) + 1) + n = kG
                                                                              T
                                                                                (endTG (q))

which is a do-await-while. Hence by the definition of endTG we have

                                            endTG (q + 1) = endTG (q) + 1 + n

which is the third part of the claim. For the remaining second part of the claim, note that the do-await-while still
jumps back n statements. Thus by definition of startTG and lenTG we have

                startTG (q + 1) = endTG (q + 1) − lenTG (q + 1) = endTG (q) + 1 + n − n = endTG (q) + 1

which is the claim.
    If the iteration is wasteful, then the next iteration repeats exactly the same events, positions of control, and
states (except that registers that were modified in the first iteration may have changed values)
Lemma 5. Let q be the index of an iteration that is wasteful, and m be the number of steps taken by the thread
inside the iteration (without leaving it)

                                                WI TG (q) ∧ m ≤ lenTG (q)

Then all of the following hold:
   1. the same events are generated in iterations q and q + 1 after m steps

                                        eTG (startTG (q) + m) = eTG (startTG (q + 1) + m)

                                                           18
   2. the same values are observed . . .

                                       vTG (startTG (q) + m) = vTG (startTG (q + 1) + m)

   3. the same position of control is reached . . .
                                        T
                                       kG (startTG (q) + m) = kG
                                                               T
                                                                 (startTG (q + 1) + m)

   4. if the value of register r is not the same after m steps in the two iterations

                                   σTG (startTG (q) + m)(r) = σTG (startTG (q + 1) + m)(r)

      then r must be an output of one of the steps u of the failed iteration q which is still visible after m steps

                                ∃u ∈ [startTG (q) : endTG (q)]. r ∈ vis(u, startTG (q + 1) + m)

Proof. We first show that claims 1 and 2 follow from claims 3 and 4. We know from claim 3 that the position of
control is the same. Thus also the executed statement is the same
                                   T
                              PT (kG (startTG (q) + m)) = PT (kG
                                                               T
                                                                 (startTG (q + 1) + m))

We split cases on the type of statement executed by the steps; in the case it is a do-await-while we are done as no
event or read-result is generated. In the other case, we have
                            T
                       PT (kG (startTG (q) + m)) = PT (kG
                                                        T
                                                          (startTG (q + 1) + m)) = step(ε, _)

From the Bounded-Effect principle we know that there is no register reads-from from a step u ∈ [startTG (q) :
endTG (q)] of the failed iteration q to step startTG (q + 1) + m which is outside that iteration (Lemma 3)
                                                 rrf
                                                6 hhT, startTG (q + 1) + miiG
                                     hhT, uiiG −→

and thus in particular ε does not depend on the visible outputs of step u to that step

                                     ¬depends-on(ε, vis(u, startTG (q + 1) + m)

From claim 4 we know that the only differences between the two states are on registers which are such visible
outputs. Thus with the definition of depends-on we know

                               ε(σTG (startTG (q) + m)) = ε(σTG (startTG (q + 1) + m))

and thus the generated events are the same, which is claim 1

                                   eTG (startTG (q) + m) = eTG (startTG (q + 1) + m)

For claim 2 we only consider read events

                                            eTG (startTG (q) + m) = R− (−)

We have by assumption that iteration q is wasteful, thus the two events read from the same store

                         G.rf(hhT, startTG (q) + miiG ) = G.rf(hhT, startTG (q + 1) + miiG )

and thus read the same value. Claim 2 immediately follows.
   Claims 4 and 3 are shown by joint induction on m. In the base case m = 0 claim 3 follows immediately from
Lemma 4
                             T
                            kG (startTG (q + 1)) = kG
                                                    T
                                                      (endTG (q) + 1) = kG
                                                                         T
                                                                           (startTG (q))

                                                          19
For claim 4 observe that every register r which differs before and after iteration q

                                       σTG (startTG (q))(r) 6= σTG (endTG (q) + 1)(r)

must have been modified by some u ∈ [startTG (q) : endTG (q)] in that iteration

                                                    r ∈ Dom(δTG (u))

W.l.o.g. u is the last such write, in which case the effect is still visible to step endTG (q) + 1

                                                r ∈ visTG (u, endTG (q) + 1)

and the claim follows as by Lemma 4, step endTG (q) + 1 is the start of iteration q + 1

                                              endTG (q) + 1 = startTG (q + 1)

    In the induction step m → m + 1, we know by the induction hypothesis that the position of control is the same
after m steps in the respective iteration and that the states are the same (modulo visible outputs). As we have
shown before, this implies that the read result is also the same

                                     vTG (startTG (q) + m) = vTG (startTG (q + 1) + m)

Analogous to the proof that ε produces the same event due to the Bounded-Effect principle, one can also conclude
that the new position of control must be the same (i.e., claim 3 holds)
                                  T
                                 kG (startTG (q) + m + 1) = kG
                                                             T
                                                               (startTG (q + 1) + m + 1)

and that the state transformer is the same (which apart from the state also depends on the read result)

                                 δTG (startTG (q) + m + 1) = δTG (startTG (q + 1) + m + 1)

Assume for the sake of showing the only remaining claim that register r has a different value in the new states

                             σTG (startTG (q) + m + 1)(r) 6= σTG (startTG (q + 1) + m + 1)(r)

By Lemma 1 the functions δTG determine the state change; since the states were updated in the same way, r can
not have been updated
                                     r 6∈ Dom(δTG (startTG (q) + m + 1))
and the difference was already present before the step

                                 σTG (startTG (q) + m)(r) 6= σTG (startTG (q + 1) + m)(r)

By the induction hypothesis this implies that r was a visible output of some step u from iteration q to the previous
step
                          ∃u ∈ [startTG (q) : endTG (q)]. r ∈ visTG (u, startTG (q + 1) + m)
and since it is not updated in this step, it is still visible to the next step

                           ∃u ∈ [startTG (q) : endTG (q)]. r ∈ visTG (u, startTG (q + 1) + m + 1)

which is the claim.
    Next we show that such a failed iteration can be safely removed. For this we define a deletion operation
G − (T, q) which deletes the q-th iteration of thread T from the graph. We only define this in case the q-th
iteration failed. In this case by the Bounded-Effect principle there are no write events that are deleted, and thus
we do not have to pay attention to deleting writes that are referenced by other reads. Events of other threads are


                                                            20
not affected at all. Neither are events generated before the start of the deleted iteration. For events started after the
deleted iteration we simply reduce the event index by the number of events in the deleted iteration (lenTG (q) + 1)

 (G − (T, q)).EU = G.EU if U 6= T
 (G − (T, q)).ET = hT, t, ei ∈ G.ET t < startTG (q) ∪ hT, t − (lenTG (q) + 1), ei ∈ G.ET t > endTG (q)
                                                    


This can also be defined by means of a partial, invertible renaming function

                                               r : G.E * (G − (T, q)).E

which maps each non-deleted event to its renamed event in G − (T, q):
                                   (
                                     hU, t, ei                   U 6= T ∨ t < startTG (q)
                    r(hU, t, ei) =
                                     hU, t − (lenTG (q) + 1), ei U = T ∧ t > endTG (q)

We have:
                                               (G − (T, q)).E = r(G.E)
For the reads-from relationship, we simply re-map the edges between the renamed events:

                                        (G − (T, q)).rf(e) = r(G.rf(r−1 (e)))

  We show that this graph still is consistent with the program.
Lemma 6.
                              consP (G) ∧ failTG (q) → consP (G − (T, q))
Proof. For threads other than T there is nothing to show as the event sequences and rf-edges are fully unchanged.
For T , we focus on the steps after the deletion, which may be affected by the change in registers. We will show:
any changes to registers after step startTG (q) were visible changes of a register by one of the deleted steps. Other
things have not changed. Thus any dependence on these changed registers would imply a register-read-from
relation in the original graph G, which is forbidden by the Bounded-Effect principle. For the sake of brevity we
define
                                                   G0 = G − (T, q)
Lemma 7. If t is a step behind the deleted parts in the new graph,

                                                      t ≥ startTG (q)

then both of the following hold:
   1. position of control in, event generated by, and read result seen in step t are unaffected by the deletion
      (relative to the original values of step t + lenTG (q) + 1)
              T          T         T             T         T         T             T         T         T
             kG 0 (t) = kG (t + lenG (q) + 1) ∧ eG0 (t) = eG (t + lenG (q) + 1) ∧ vG0 (t) = vG (t + lenG (q) + 1)



   2. if r is a register whose value was changed by the deletion

                                             σTG0 (t)(r) 6= σTG (t + lenTG (q) + 1)(r)

      then there is a step u in the original graph which still has a visible effect on r

                                  ∃u ∈ [startTG (q) : endTG (q)]. r ∈ visTG (u,t + lenTG (q) + 1)

Proof. The proof is analogous to the proof of Lemma 5 and omitted.



                                                            21
   Now to show that consP is preserved we simply consider the sets of events of the individual threads U ∈ T
and show that they are not affected:

                                     ∀U. G0 .EU = hhU, tiiG0 t < NGU0
                                                 
                                                                                                          (2)

We split cases on U 6= T . For threads U 6= T other than T , nothing has changed and the claim follows from the
consistency of G

                                           G0 .EU = G0 .EU
                                                  = hhU, tiiG t < NGU
                                                    

                                                  = hhU, tiiG0 t < NGU0
                                                    
                                                                                                                 (3)

For thread T , we split the set into those events generated before the cut (which have not changed)

                              hhT, tiiG t < startTG (q) = hhT, tiiG0 t < startTG (q)
                                                           
                                                                                                                 (4)

and the events generated after the cut, for which Lemma 7 shows that only indices have changed:

              hT, t − (lenTG (q) + 1), eTG (t)i t > endTG (q) ∧ t < NGT
            

         = hT, t − (lenTG (q) + 1), eTG (t)i t > startTG (q) + (lenTG (q) + 1) ∧ t < NGT
            

         = hT, t − (lenTG (q) + 1), eTG (t)i t − (lenTG (q) + 1) > startTG (q) ∧ t < NGT
            

         = hT, t, eTG (t + (lenTG (q) + 1))i t > startTG (q) ∧ t + (lenTG (q) + 1) < NGT
            
                                                                                            rebase t
         = hT, t, eTG0 (t)i t > startTG (q) ∧ t < NGT − (lenTG (q) + 1)
            
                                                                                                L7
                                   T              T
            
         = hhT, tiiG0 t > startG (q) ∧ t < NG0                                                                   (5)

Jointly with Eq. (4) this proves Eq. (2) for U := T :

  G0 .ET = r(G.ET )
         = hhT, tiiG t < startTG (q) ∪ hT, t − (lenTG (q) + 1), eTG (t)i t > endTG (q) ∧ t < NGT
                                      

         = hhT, tiiG0 t < startTG (q) ∪ hhT, tiiG0 i t ≥ startTG (q) ∧ t < NGT 0
                                      
                                                                                                        E (4), (5)
         = hhT, tiiG0 t < NGT 0
           

Together with Eq. (3) this shows Eq. (2). By Eq. (2) we conclude that the union over all threads U of events in
G0 .EU is equal to the events generated by all threads:

                                        G0 .EU =
                                    [               [ 
                                                        hhU, tiiG0 i t < NGT 0
                                     U∈T             U∈T

It immediately follows that the set of all events in G0 is equal to the set of events generated by all threads

                                     G0 .E = hhU, tiiG0 i U ∈ T , t < NGT 0
                                             

which is the definition of consP (G0 ), i.e., the claim.
   Next we iteratively eliminate all wasteful iterations of awaits. This takes us from any graph G ∈ GF to a
graph G0 ∈ GF∗ but preserves at least some error events.
Lemma 8.
                       G ∈ GF ∧ h−, −, Ei ∈ G.E → ∃G0 ∈ GF∗ . h−, −, Ei ∈ G0 .E
Proof. We construct a series G(i) of graphs in which i wasteful iterations have been eliminated from G. Since
G ∈ GF there are only finitely many failed iterations we need to remove, thus the sequence is finite. We begin
graph G in which 0 iterations have been deleted

                                                           G0 = G


                                                             22
and then progressively cut one additional arbitrary failed iteration at a time

                                       Gi+1 = Gi − ε (T, q) WI TG (q)
                                                      


The last graph GI−1 in the sequence with index I = |G(i) | by definition does not have any wasteful iterations

                                                   @T, q. WI TGI−1 (q)

and thus is not wasteful
                                                        ¬W(GI−1 )
By repeated application of Lemma 6 we conclude that all the graphs in the sequence, including GI−1 , are
consistent with the program
                                           consP (GI−1 )
and thus G0 := GI−1 is in GF∗
                                                        GI−1 ∈ GF∗
   It now suffices to show that the error event is preserved (although possibly generated by a different step).
Assume
                                               h−, −, Ei ∈ G.E
By definition we only delete events in wasteful iterations. By Lemma 5 every event in such an iteration is repeated
in the next iteration. The events outside the deleted iteration are maintained (cf. Lemma 7). We conclude: the
event E is generated in every graph in the sequence, in particular also in the last one

                                                 h−, −, Ei ∈ GI−1 .E

which is the claim.
   This shows that no bugs are missed by AMC. Our next goal is to show that AMC can terminate. We first
show that the number of writes generated in a graph is bounded.
Lemma 9.
                ∃b. ∀G. consPM (G) → | (T,t) eTG (t) = W − (−, −), T ∈ T ,t < NGT | ≤ b
                                           

Proof. The bound is equal to the sum of the program lengths of each thread

                                                     b := ∑ |PT |
                                                           T ∈T

The reason for this is that threads only repeat statements in case they fail a loop iteration; but these failed loop
iterations by the Bounded-Effect principle do not produce writes. We show: if step t of thread T generates a
write event, statement kGT (t) is never executed again.


                                 eTG (t) = W − (−, −)     →                T
                                                                  ∀u > t. kG        T
                                                                             (u) > kG (t)                        (6)
                                                                                 T (t) or before
Let u w.l.o.g. be the first step after t in which the position of control is at kG
                                         T        T        T            T
                                        kG (u) ≤ kG (t) ∧ kG (u − 1) > kG (t)

By the semantics of the language, step u − 1 must have been a failed await iteration
                                      T
                                 PT (kG (u − 1)) = await(n,κ) ∧ κ(σTG (u − 1)) = 1
                                                     T (u) and kT (u − 1) are not awaits
Since there are no nested awaits, all lines between kG          G

                                          T        T
                                   ∀k ∈ [kG (u) : kG (u − 1)). PT (k) 6= await(−,−)


                                                           23
Of course kGT (t) is in that interval; thus all steps between kT (t) and K T (u − 1) are not awaits. By the semantics of
                                                                G          G
the language, these steps moved control ahead one statement per step. Thus at most n steps have passed between
t and u − 1
                                                           T            T
                                           (u − 1) − t = kG  (u − 1) − kG (t) < n
Since step u − 1 ends an iteration q of an await of length n

                                           endTG (q) = u − 1 ∧ lenTG (q) = n

it follows that step t is one of the steps in that iteration

                                               t ∈ [startTG (q) : endTG (q)]

Because the loop condition is satisfied, the iteration is a failed iteration

                                                        failTG (q)

and we conclude from the Bounded-Effect principle: step t does not produce a write

                                                  eTG (t) 6= W − (−, −)

which is a contradiction. This proves Eq. (6), i.e., each statement can produce at most one write. Thus the total
number of writes produced by thread T is at most the size |PT | of the program text of thread T

                                  | t eTG (t) = W − (−, −), t < NGT | ≤ |PT |
                                   

The claim follows:

   | (T,t) eTG (t) = W − (−, −), T ∈ T , t < NGT | =           ∑ | t eTG (t) = W − (−, −), t < NGT | ≤ ∑ |PT |
                                                                     
                                                               T ∈T                                         T ∈T



    In a graph which satisfies the progress condition, each iteration of await reads from a different combination
of writes. Since the set of writes is bounded, the possible number of combinations is bounded as well. Thus the
number of failed iterations is also bounded.
Lemma 10.
                                                   GF∗ is finite
Proof. We show instead that each G ∈ GF∗ has bounded length (bounded by some constant B). This implies
that the graphs are finite as every G can then be encoded as a pair of a sequence of B events and a sequence
of B numbers in the range [0 : b − 1] indicating rf-edges. Since the set of events is finite, the number of such
encodings is finite, and so is GF∗ .
    Assume for the sake of contradiction that no such bound exists. Thus graphs in GF∗ can be arbitrarily large.
Since they are consistent with the program, this means that the program execution can become arbitrarily long.
Since there are only finitely many threads, one thread T can be executed for arbitrarily long. Since the program
text PT has finite length and thus only finitely many awaits, there has to be one await that can be made to fail
arbitrarily often. Let the line number of this await be k, and let G0 , G1 , G2 , . . . be graphs in which the await fails
zero times, once, twice, etc. The await jumps back some number n of statements

                                                  PT (k) = await(n,κ)

and thus produces at most n reads. By the progress condition, at least one of them must read from a new write
in each iteration. Coherence forbids going back to the previous writes. By Lemma 9 the number of available
writes in each graph Gi is at most b. Thus there can be at most n · b iterations of this loop. Consider Gn·b+1 , i.e.,
the graph in which one iteration beyond that has been executed. Note that after l iterations of the await, at most
n · b − l writes are still available to read from. Thus in the final iteration n · b + 1, the thread has at most −1 write
to read from, which is a contradiction. This shows that such a bound B must exist and thus GF∗ is finite.


                                                            24
  This proves our claims about GF /GF∗ . Next we consider the graphs in G∞
                                                                         ∗ which indicate await violations.
Lemma 11. Every graph G ∈ G∞  ∗ is finite.
Proof. Observe that every G ∈ G∞                                 F
                               ∗ is by definition an element of G∗ and thus finite.

    We proceed to show that graphs in G∞
                                       ∗ always indicate await terminations. This depends on the definition of
stagnancy which we have not shown yet. We define it as follows. Let

                                      VG = T ∈ T kGT (NGT ) < |PT |
                                           

be the set of threads which have not terminated (yet) in G. G is stagnant iff all of the following are true:
   1. Some threads have not terminated
                                                         VG 6= 0/
   2. All of those threads have just completed a failed await loop iteration

                                          ∀T ∈ VG . NGT = endTG (q) ∧ failTG (q)

   3. There is no extension G0 of G (with G.X ⊆ G0 .X for X ∈ { E, rf, mo }) where any threads in VG have
      terminated and threads read only from stores that are already available in G

                                    consPM (G0 ) ∧ Dom(G0 .rf) ⊆ G.E → VG = VG0

Lemma 12.
                                             G∞
                                              ∗ 6= 0
                                                   /     →     G∞ 6= 0/
                    ∗ is non-empty. Thus there is some stagnant graph G ∈ G∗
Proof. Assume that G∞                                                      ∞


                                                   stagnant(G)

The set of threads that have not completed their program in G

                                       VG = T ∈ T kGT (NGT ) < |PT |
                                             

is by definition of stagnancy non-empty.
    By definition of stagnancy, each of these threads in VG must be in the qT + 1-th iteration of an await, and 2)
iteration qT of the same await failed, and 3) there are no other writes to read from that would result in the thread
terminating. We extend the graph to an infinite graph G0 by adding failed await loop iterations in which each
load reads from the mo-maximal store to its location. Let for T ∈ VG the index of the previous (failed) iteration
of the await be qT
                                           failTG (qT ) ∧ NGT = endTG (qT )
    We add for T ∈ VG events for an infinite number of iterations, numbering each with an index n ∈ N, and each
step inside that iteration with an index m ≤ lenTG (q), replicating the same events over and over

             G0 .ET = G.E ∪ hT, NGT + n · lenTG (q) + m, eTG (startTG (q) + m)i n ∈ N, m ≤ lenTG (q)
                              

The newly added read events will read from the mo-maximal stores to their locations. Let

                               e = hT, NGT + n · lenTG (q) + m, eTG (startTG (q) + m)i

be such a read event. We define
                                            G0 .rf(e) = max G.Wloc(e)
                                                        G.mo
Other than that we change nothing. Obviously this repetition results in a wasteful execution. With Lemma 5 it
is easy to show that all of these new loop iterations are consistent with the program and are themselves failed
wasteful iterations
                                                   consPM (G0 )


                                                         25
This graph has infinitely many failed iterations of awaits and is thus in G∞ , which is the claim

                                                      G0 ∈ G ∞


  It only remains to show that every graph G ∈ G∞ can be cut to a graph in G∞
                                                                            ∗.
Lemma 13.
                                          G∞ 6= 0/ → G∞   ∗ 6= 0/
Proof. Assume that there are graphs which violate await termination and let G ∈ G∞ be such a graph. Analogous
to how we showed in Lemma 10 that there is some thread T which executes some await in line k an arbitrary
number of times, we can show that some thread executes infinitely many steps. Let V be the (non-empty) set of
these threads
                                            V = T NGT = ∞
                                                  

Each of these threads T ∈ V executes some await in line kT infinitely often
                                                                      T
                                 PT (kT ) = await(n,κ) ∧ ∀t. ∃u ≥ t. kG (u) = kT

By Lemma 9 the number of writes is bounded, thus (as also shown in Lemma 10) this loop have only finitely
many non-wasteful iterations. Starting from some iteration qT , the writes observed by the await never change;
iteration qT and all subsequent iterations are wasteful.

                                                ∀q0 ≥ qT . WI TG (q0 )

Due to fairness, this is only allowed if there is no possibility for the reads to read anything else: otherwise,
eventually one of the subsequent iterations would need to read from one of the other available writes and hence
not be a wasteful iteration. This allows us to construct a graph G0 ∈ G∞                                    0
                                                                          ∗ which stagnates. We generate G by
cutting down all failed wasteful iterations of threads in T . Assume w.l.o.g. that the iteration qT is the first
wasteful iteration of thread T (the finitely many preceding wasteful iterations can be deleted iteratively with
Lemma 7)
                                                  ¬WI TG (q0 − 1)
We define:
                                  G0 .ET = hT, t, ei ∈ G.ET t ≤ endTG (qT )
                                          

This ensures all conditions of stagnant: these threads have not terminated, by definition they just finished a failed
await loop iterationevent, and the only available writes force the thread to stay in the loop indefinitely. Thus we
have
                                                   stagnant(G0 )
Furthermore, the graph is still consistent with the program because the beginning of the thread-local execution is
exactly the same as for G
                                                     consP (G0 )
Since all wasteful iterations have been deleted, the graph G0 is not wasteful

                                                      ¬W(G0 )

and can thus in the set of graphs G∞
                                   ∗ that are searched by AMC

                                                      G0 ∈ G ∞
                                                             ∗

which proves the claim.
    The main theorem (Theorem 1) follows from Lemmas 8 and 11 to 13.


                                                         26
3       Study Cases
In this section, we discuss in detail three study cases: a bug in the MCS lock of the DPDK library, a bug in the
MCS lock of an internal Huawei product, and a comparison of expert-optimization and VS YNC-optimization of
the Linux qspinlock. We report about bugs found with VS YNC as well as limitations.

3.1      DPDK MCS lock
The Data Plane Development Kit (DPDK10 ) is a popular set of libraries used to develop packet processing
software in user space. VS YNC found a bug in the MCS lock of the current DPDK version (v20.05). Figure 13
shows the part of the implementation that concern us. At the end of the code, we added the bug scenario in
which two threads, Alice and Bob, are involved. Alice wants to acquire the lock (see run_alice() function),
and Bob currently holds the lock and is about to release it (see run_bob()). Note that we removed the slowpath
of rte_mcslock_unlock() since the bug only occurs in the fastpath. The core of the bug is a missing rel barrier
before or at Line 27, which causes Alice to hang and never enter the critical section.

 1   /* SPDX-License-Identifier: BSD-3-Clause                        29       /* The while-load of me->locked should not move above
 2    * Copyright(c) 2019 Arm Limited                                30        * the previous store to prev->next. Otherwise it will
 3    */                                                             31        * cause a deadlock. Need a store-load barrier. */
 4    typedef struct rte_mcslock {                                   32       __atomic_thread_fence(__ATOMIC_ACQ_REL);
 5     struct rte_mcslock *next;                                     33       while (__atomic_load_n(&me->locked, __ATOMIC_ACQUIRE))
 6     int locked; /* 1 if the queue locked, 0 otherwise */          34         rte_pause();
 7   } rte_mcslock_t;                                                35   }
 8                                                                   36
 9   static inline void                                              37   static inline void
10   rte_mcslock_lock(rte_mcslock_t **msl, rte_mcslock_t *me) {      38   rte_mcslock_unlock(rte_mcslock_t **msl, rte_mcslock_t *me) {
11     rte_mcslock_t *prev;                                          39     if (__atomic_load_n(&me->next, __ATOMIC_RELAXED) == NULL) {
12                                                                   40           // **ignore this branch**
13     /* Init me node */                                            41     }
14     __atomic_store_n(&me->locked, 1, __ATOMIC_RELAXED);           42
15     __atomic_store_n(&me->next, NULL, __ATOMIC_RELAXED);          43       /* Pass lock to next waiter. */
16                                                                   44       __atomic_store_n(&me->next->locked, 0, __ATOMIC_RELEASE);
17     /* If the queue is empty, the exchange operation is           45   }
18       * enough to acquire the lock. Hence, the exchange           46   //---------------------------------------------------------
19       * operation requires acquire semantics. The store to        47   // bug scenario
20       * me->next above should complete before the node is         48   //---------------------------------------------------------
21       * visible to other CPUs/threads. Hence, the exchange        49   // 2 threads: alice and bob.
22       * operation requires release semantics as well. */          50   rte_mcslock_t alice, bob;
23     prev = __atomic_exchange_n(msl, me, __ATOMIC_ACQ_REL);        51   // bob has the lock
24     if (prev == NULL) {                                           52   rte_mcslock_t *tail = &bob;
25        return;                                                    53
26     }                                                             54   void run_alice() { rte_mcslock_lock(&tail, &alice); }
27     __atomic_store_n(&prev->next, me, __ATOMIC_RELAXED);          55   void run_bob() { rte_mcslock_unlock(&tail, &bob); }
28

       Figure 13: Part of the DPDK MCS lock implementation describing the scenario in which Alice hangs.

The bug on IMM. Figure 14 shows an execution graph in which Alice hangs. AMC gives exactly this execution
graph as counter-example for await termination, but in the text form. The Usc pair of events are the “read part”
and “write part” of the atomic exchange (Line 23 of code in Fig. 13). To understand why exchange is modeled
with two events, remember that atomic exchange is implemented with load-linked/store-conditional instruction
pairs in many architectures. For example in ARMv8, atomic_exchange_n(msl, me, __ATOMIC_ACQ_REL) is
compiled to
     38: c85ffc02       ldaxr x2, [x0]
     3c: c803fc01       stlxr w3, x1, [x0]
     40: 35ffffc3       cbnz w3, 38 <run_alice+0x20>
Intuitively, the load instruction is the “read part” of the exchange, whereas the store instruction is “write part” of
the exchange. Also note that for the sake of this bug, __ATOMIC_ACQ_REL is equivalent to __ATOMIC_SEQ_CST,
i.e., even with the stronge sc barrier mode, the bug can still manifest.
     10 https://github.com/DPDK/dpdk




                                                                27
                                Winit locked, 0                                                         Winit locked, 0
                     Alice                                 Bob                           Alice                                Bob
        Wrlx alice->next, NULL             mo   Rrlx bob->next, alice           Wrlx alice->next, NULL mo             Racq bob->next, alice
                                                      hb

        Wrlx alice->locked, 1        mo         Wrel alice->locked, 0           Wrlx alice->locked, 1         mo     Wrel alice->locked, 0


                                      rf                                                                 hb   rf
        UscR tail, bob                                                          UscR tail, bob


        UscW tail, alice                                                        UscW tail, alice
rf              hb                                                      rf

        Wrlx bob->next, alice                                                   Wrel bob->next, alice
                                                                                                                     rf
         Fsc                                                                    Fsc


         Racq alice->locked, 1                                                  Racq alice->locked, 1


         Racq alice->locked, 1                                                  Racq alice->locked, 0
          ...




     Figure 14: IMM. Bug results in Alice hanging: Alice                     Figure 15: IMM. With the bug fixed, Alice writes
     writes to bob->next with rlx mode, and Bob reads rlx                    to prev->next with rel mode, and Bob reads with
     mode, which causes allows Bob’s write to before the                     acq mode, creating a synchronizes-with edge, which
     initialization of me->locked.                                           forces Bob’s write to occur after the initialization.
         Returning to the bug in IMM, Alice starts by initializing her node, in particular, setting alice->locked to 1.
     After exchanging the tail, Alice writes to bob->next. Although Bob reads from Alice’s write to bob->next,
     IMM allows Alice’s write to alice->locked to happen after Bob’s write to alice->locked because no happens-
     before relation is established between Alice and Bob. The mo relation shows this order of modifications. If that
     occurs, Alice’s fate is to await alice->locked to become 0 forever. To establish the correct happens-before
     relation between Alice and Bob, Alice’s write to bob->next has to be rel, and Bob’s read of bob->next has to be
     acq (see Fig. 15). That causes both events to “synchronize-with”, guaranteeing Alice’s write to alice->locked
     to happen before Bob’s. Note that in IMM the happens-before relation projected to one memory location, e.g.,
     alice->locked, implies the same order in the visible memory updates of that location, i.e., in the modification
     order mo of alice->locked. The happens-before relation does not, however, imply an ordering between the
     writes to distinct memory locations [25].
     The bug on ARM. The bug is not exclusive to the IMM model. Figure 16 shows an execution graph manually
     adapted to the ARM memory model (ARM for short). In this memory model, a global order of events exist;
     so, we number the events with one possible global order. ARM allows the write to alice->locked (event
     7) to happen after the read part of the atomic exchange UscR (event 3), but does not allow it happen after the
     write part Usc W (event 8). Moreover, since Alice’s write to bob->next is rlx (event 4), ARM allows the write

     to alice->locked (along with Usc       W ) to happen after it. As a consequence, although Bob reads (event 5) from

     Alice’s write to bob->next (event 4), the effect of setting alice->locked to 1 (event 7) happens after Bob has
     set it to 0 (event 6). In contrast to IMM, making Alice’s write to be rel is sufficient in ARM (see Fig. 17) because
     the control/address dependency between Bob’s events guarantees that writes that happen before the read event
     also happen before the subsequent dependent events.
     Validation of the bug. So far we were not able to reproduce the effect of the bug on real hardware. The
     situation that triggers the bug is very unlikely to happen, but nevertheless possible and still a potential problem
     for code using DPDK on ARM platforms. To have a higher confidence about the bug on ARM, we checked
     the scenario of Fig. 13 with Rmem [26], a stateful model checking tool capable of verifying small pieces of
     binary code compiled to ARMv8 architecture. Although Rmem cannot deal with the infinite loop of Alice, we
     can reproduce the bug by asserting Bob does not see alice->locked being reverted to 1 after he has set it to 0 –
     as expected, the assertion fails.


                                                                        28
                                      Winit locked, 0                                                                  Winit locked, 0
                     Alice        1                               Bob                                 Alice        1                            Bob
            Wrlx alice->next, NULL               mo       Rrlx bob->next, alice              Wrlx alice->next, NULL mo                  Rrlx bob->next, alice
        2                                             5                                  2                                         7
                                                                 ctrl+addr                                                                     ctrl+addr

            Wrlx alice->locked, 1          mo             Wrel alice->locked, 0              Wrlx alice->locked, 1          mo         Wrel alice->locked, 0
        7                                             6                                  4                                         10


            UscR tail, bob                  rf                                               UscR tail, bob                 rf
        3                                                                                3


            UscW tail, alice   ctrl+addr                                                     UscW tail, alice   ctrl+addr
        8                                                                                5
rf                                                                                rf

            Wrlx bob->next, alice                                                            Wrel bob->next, alice
        4                                                                                6
                                                                                                                                    rf
            Fsc                                                                               Fsc
        9                                                                                8


            Racq alice->locked, 1                                                             Racq alice->locked, 1
       10                                                                                9


            Racq alice->locked, 1                                                             Racq alice->locked, 0
       11                                                                                11
             ...




     Figure 16: ARM memory model. Bug results in                                       Figure 17: ARM memory model. To fix the bug,
     Alice hanging: Alice writes to bob->next with rlx                                 Alice has to writes to bob->next with rel mode, forc-
     mode causing the initialization of alice->locked to                               ing Bob’s write to occur after the initialization of
     be reordered after Bob’s write.                                                   alice->locked.
     Discussion. The DPDK MCS lock bug is a good example of how understanding WMMs can be challenging
     even for experts. Note the MCS lock has been contributed by ARM Limited to the DPDK project. In Fig. 13,
     Line 17, the developer considers exactly the situation observed in this bug: “The store to me->next above should
     complete before the node is visible to other CPUs/threads. Hence, the exchange operation requires release
     semantics as well.” However, making the exchange rel is not sufficient because the node can also become visible
     to another thread via the write at Line 27, and nothing stops the store of Line 14 and the write part of the exchange
     of Line 23 to be reordered after Line 27. Another interesting finding in this code is that, as far as we can verify,
     the explicit fence at Line 32 is useless and can be removed.

     3.2           MCS lock of an internal Huawei product
         Our next study case is concerned with the MCS lock implementation found in an internal Huawei product.
     In this implementation, VS YNC identified a missing acq barrier that causes serious data corruption problems.
     We were able to reproduce the problem on real hardware and reported the bug along with a simple fix to the
     maintainers. Here, we describe this issue to illustrate the challenges of porting x86 code to ARM, which is the
     reason why such a bug was introduced in the code base. With the recent increased demand of software for ARM
     servers, we believe that similar bugs are going to become more and more common in production.
     The bug on IMM. Figure 18 presents a slightly simplified version of the original MCS lock implementation.
     The bug is a missing acq barrier at the end of mcslock_acquire(). To understand the scenario, consider the
     execution graph in Fig. 19, where the critical section is a simple increment x++, Alice wants to enter, and Bob is
     inside the critical section. Similarly to the DPDK bug, Bob sees Alice’s node when releasing the lock and sets
     Alice’s spin = 0; this flag is called locked in DPDK. The first fence in Alice’s mcslock_acquire synchronizes
     with the fence in Bob’s mcslock_release due to the write and read of bob->next field. That establishes a
     happens-before relation marked with the dashed arrows in the figure. The happens-before relation, however,
     does not specify whether Bob’s critical-section execution happens before Alice’s critical-section execution, or
     vice-versa. In this execution graph, Alice and Bob run their critical sections concurrently and both read from the
     initial write to x, causing one of the increments to be lost. By introducing an acq barrier in the reads of me->spin
     or after them (Fig. 18, Line 19), Alice is guaranteed to execute her critical section after Bob. Note that, although
     the ARM model also introduces control dependencies, reads of me->spin and the read ofx inside the critical


                                                                                  29
 1   static inline void
 2   mcslock_acquire(volatile mcslock_t *tail,
 3                   volatile mcs_node_t *me)
                                                                Winit x, 0                                   rf
 4   {
 5     mcs_node_t *prev;
 6                                                                                               Alice                        Bob
 7       me->next = NULL;
                                                                                          Wrlx me->next, NULL               Rrlx x, 0
 8       me->spin = 1;




                                                                                                                                        x++;
 9
10       smp_wmb(); // ** consider to be SC fence **
11
                                                                                          Wrlx me->spin, 1                  Wrlx x, 1
12       // equivalent to xchg_acq
13       prev = __sync_lock_test_and_set(tail, me);
14       if (!prev)                                                                       Fsc                               Rrlx me->next, alice
15         return;                                                                                       hb




                                                                                                                                                   mcslock_release()
16
                                                                                           R m, bob
                                                                                          Uacq
17       prev->next = me;                                                                                                   Fsc




                                                                      mcslock_acquire()
18       smp_mb(); // ** consider to be SC fence **                                                               rf
19       while(me->spin);
         // BUG: Missing ACQ barrier, eg, smp_mb();                                        W tail, me
                                                                                          Uacq
20                                                             rf                                                           Rrlx me->next, alice
21   }
22
23
                                                                                          Wrlx bob->next, me                Wrlx alice->spin, 0
24   static inline void
25   mcslock_release(volatile mcslock_t *tail,            rf
26                   volatile mcs_node_t *me)
                                                                                          Fsc
27   {
28     if (!me->next) {
29       // SC cmpxchg                                                                                                 rf
30       if (__sync_val_compare_and_swap(                                                 Rrlx me->spin, 1
31                      tail, me, NULL) == me) {
32         return;
33       }                                                                                Rrlx me->spin, 0
34       while(!me->next);
35     }
36                                                                                        Rrlx x, 0
37       smp_mb(); // ** consider to be SC fence **
                                                                      x++;




38       me->next->spin = 0;
39   }                                                                                    Wrlx x, 1
40

                                                       Figure 19: In IMM, Alice’s read of x may happen before Bob’s
Figure 18: MCS implementation in a com-
                                                       write to x.
mercial OS. A barrier bug cases data races in
the critical section.
section of Alice, a reordering of these operations is not precluded because they are all read operations.
Discussion. Besides the barrier bug, some issues may be interesting to point out. The developers that imple-
mented this code opted in using compiler specific atomic operations. We do not recommend their use because they
hide the barrier mode used underneath. In particular, _sync_lock_test_and_set has an acq mode, whereas
_sync_val_compare_and_swap has an sc mode. Moreover, the developers overuse fences: the smb_mb() fence
in mcs_acquire(), Line 18, is redundant and can be eliminated.

3.3        Linux qspinlock
The qspinlock code was originally introduced in Linux version 4.2 as a new and faster spinlock [5]. Since
then experts have slightly improved the algorithm and carefully optimized the barriers, achieving an excellent
performance. Currently, qspinlock is the default spinlock inside the Linux kernel for many architectures include
x86 and ARM. We now describe how we used VS YNC to automate the barrier optimization process of the Linux
qspinlock and obtain similar barriers as the current code, at version 5.6 [21].
Baseline. Our optimization is based on Linux 4.4 [20], where the barriers were yet to be completely optimized,
but other (algorithm) optimizations were mainly done. Because our purpose is exclusively the barrier optimization,
we ported a few remaining algorithmic optimizations present on 5.6 back to version 4.4. Specifically, we
backported the prefetch instructions to receive the next node in the queue.
Code preparation. To optimize existing code with VS YNC, we may have to perform minor changes. In
particular, if the code uses custom atomics implemented in assembly, these have to be replaced with either


                                                               30
compiler builtin atomics or with VS YNC-atomics (which compile down to builtin atomics). In the case of
qspinlock, we replaced the Linux’s atomic operations with VS YNC-atomics. Because custom atomics do not
always follow the same model as IMM and compiler builtin atomics, some discrepancies may arise during
the replacement. We encountered one such case: The cmpxchg function in Linux is defined as having a full
memory barrier (i.e., an sc fence) before and after the operation only if it succeeds [2]. So we replace the Linux
cmpxchg with a wrapper that calls VS YNC’s atomic_cmpxchg and additionally an atomic fence in the success
case to mimic the original behavior (for reference, see Fig. 22) . Another issue we encountered were unions of
different-sized variables: The qspinlock code uses a union that allows the same memory location to be read and
written with either 8, 16 or 32 bits. Currently, AMC requires that accesses to the same memory locations always
have the same size – this limitation may be fixed in the future. To overcome this issue, we replaced accesses to
the qspinlock data structure always 32 bits.

               Version            acq      rel    sc           Time                  Correctness
               Linux 4.4 [20]       3      6     6     2015/09/11                  Not verified
               Linux 4.5 [19]       6      2     1     2015/11/09      Barrier bug, fixed in [6]
               Linux 4.8 [27]       6      3     0     2016/06/03      Barrier bug, fixed in [6]
               Linux 4.16 [6]       6      4     0     2018/02/13                  Not verified
               Linux 5.6 [21]       6      2     1     2020/01/07                  Not verified
               VS YNC               7      2     1     11 minutes              VS YNC-verified
                          Table 1: Barrier optimization results for Linux’s qspinlock

Optimization results. VS YNC recommended barrier modes similar to those used by the experts (see Table 1)
in roughly 11 minutes – in contrast, the expert optimization took several release cycles. The details of the
optimization can be seen in Fig. 20. The bold marked text refers the the optimization suggested by VS YNC. The
boxes 1 to 5 are the Linux cmpxchg function. We see that VS YNC removes all atomic fences and transfer their
barrier to atomic operations.
    We now relate the VS YNC optimization with the optimizations made by the Linux experts over the several
release cycles:
Version 4.5 – optimization of cmpxchg: The first optimization by the experts was exactly in the cmpxchg
      functions ( 1 to 5 ), changing it from sc to a more relaxed mode [19].
Version 4.8 – optimization of unlock function: Experts optimized the code in 6 , removing the fence and
      changing the atomic_sub to rel mode [27] – identically to VS YNC suggestion.
Version 4.16 – bug fix: The optimization from version 4.5 introduced a bug that was only found and fixed
      in version 4.16 [6]. The bug allowed the node initialization to occur after the update of prev->next,
      similarly to DPDK’s bug discussed in §3.1. In version 4.16, the experts used a rel barrier in the atomic
      write immediately after the decode_tail function, but finally replace that with an atomic sc-fence in the
      current version. Optimizations with VS YNC are verified and hence not affected by such bugs.
Version 5.6 – current version: Figure 21 shows the barrier modes used in the current version of qspinlock [21].
      The dotted lines connect our barriers in Fig. 20 with the equivalent barriers in the current version. The few
      different barrier modes are due to two reasons: First, there exists multiple maximally-relaxed combinations
      that are correct. Second, both optimizations are based on different memory models (LKMM and IMM).
      VS YNC extended with an LKMM module would likely suggest the same barriers as used in Linux.




                                                       31
lock
  atomic32_cmpxchg_rel --> acquire                                     lock
1
  atomic_fence --> remove                                                atomic32_cmpxchg_acq
  queued_spin_lock_slowpath                                              queued_spin_lock_slowpath
     atomic32_await_neq_rlx                                                atomic32_await_counter_neq_rlx
     atomic32_cmpxchg_rel --> acquire                                      atomic32_get_or_acq
  2
     atomic_fence --> remove                                               atomic32_sub_rlx
     atomic32_await_mask_eq_acq --> relaxed                                atomic32_await_mask_eq_acq
     atomic32_add_rlx --> acquire                                          atomic32_add_rlx
     encode_tail                                                           encode_tail
     atomic32_write_rlx                                                    grab_mcs_node
     atomicptr_write_rlx                                                   atomic32_write_rlx
     atomic32_read_rlx                                                     atomicptr_write_rlx
  3
     atomic32_cmpxchg_rel --> acquire                                      atomic32_read_rlx
     atomic_fence --> remove                                               atomic32_cmpxchg_acq
     atomic32_read_rlx                                                     atomic_fence
     atomic32_cmpxchg_rel --> seq_cst                                      atomic32_read_rlx
  4
     atomic_fence --> remove                                               atomic32_cmpxchg_rlx
     decode_tail                                                           decode_tail
     atomicptr_write_rlx                                                   atomicptr_write_rlx
     atomic32_await_neq_acq                                                atomic32_await_neq_acq
     atomicptr_read_rlx                                                    atomicptr_read_rlx
     atomic32_await_mask_eq_acq --> relaxed                                atomic32_await_mask_eq_acq
     atomic32_or_rlx --> acquire                                           atomic32_cmpxchg_rlx
  5
     atomic32_cmpxchg_rel --> acquire                                      atomic32_or_rlx
     atomic_fence --> remove                                               atomicptr_await_neq_rlx
     atomicptr_await_neq_rlx                                               atomic32_write_rel
     atomic32_write_rel                                                unlock
unlock                                                                   atomic32_sub_rel
6
  atomic_fence --> remove
  atomic32_sub_rlx --> release
Figure 20: Barrier modes in version 4.4 and                            Figure 21: Barrier mode information for qspin-
VS YNC optimizations in bold. Optimizations in                         lock in Linux version 5.6 (current version). Dot-
the red boxes are similar to version 4.5; those in                     ted lines connect related barrier optimizations
the blue box are identical to version 4.8.                             of VS YNC and the current version.


                       1   #define __linux_atomic_cmpxchg(mod1, mod2, l, a, b)     \
                       2   ({                                                      \
                       3           typeof(a) __r = atomic_cmpxchg##mod1(l, a, b)   \
                       4           if (__r == a) atomic_fence##mod2();             \
                       5           __r;                                            \
                       6   })
                       7
                       8   #define linux_cmpxchg(l, a, b)          __linux_atomic_cmpxchg(_rel,     , l, a, b)
                       9   #define linux_cmpxchg_rlx(l, a, b)      __linux_atomic_cmpxchg(_rlx, _rlx, l, a, b)
                      10   #define linux_cmpxchg_acq(l, a, b)      __linux_atomic_cmpxchg(_acq, _rlx, l, a, b)
                      11   #define linux_cmpxchg_rel(l, a, b)      __linux_atomic_cmpxchg(_rel, _rlx, l, a, b)
                      12   #define linux_cmpxchg_seq(l, a, b)      __linux_atomic_cmpxchg(    , _rlx, l, a, b)

           Figure 22: Using VS YNC atomics to implement code compatible with Linux’s cmpxchg.




                                                           32
4       Optimized-code Evaluation
In this section, we present details of the setup used in our “optimized-code evaluation” section. Moreover, we
discuss the results obtained with microbenchmarks in length. See the full paper for results with real-world
workloads [24].

4.1     Setup details
4.1.1    Evaluation platforms
We conduct our experiments in the following hardware platforms:
      • a Huawei TaiShan 200 (Model 2280)11 rack server that has 128 GB of RAM and 2 Kunpeng 920-6426
        processors, a HiSilicon chip with 64 ARMv8.2 64-bit cores12 , totaling 128 cores running at a nominal 2.6
        GHz frequency. The identifier to denote this machine in this document is taishan200-128c.

      • a GIGABYTE R182-Z91-0013 rack server that has 128 GB of RAM and 2 EPYC 7352 processors, an
        AMD chip with 24 x86_64 cores14 , totaling 48 cores (96 if counting hyperthreading) running at a nominal
        2.3 GHz frequency. The identifier to denote this machine in this document is gigabyte-96c.
   We installed on all these servers the Ubuntu 18.04.4 LTS (aarch64) operating system, with the following
Linux kernel version: 5.3.0-42-generic.
4.1.2    Environment setup
To produce stable benchmark results on a kernel as complex as Linux, we took some precautions in terms of
environment configuration of our experiment target platforms. We list here such precautions:
     1. Atomic types isolation. Linux and VS YNC each declare their own atomic types such as atomic_t and
        atomic64_t. When writing the kernel benchmark module, to avoid name conflicts between Linux kernel
        headers and VS YNC library headers, we separated into different translation units the benchmark “main”
        code (where the entry point lies and where the kernel threads are created) from the lock primitives function
        definitions and data structures instantiations (where the contention loops are executed, see Section 4.2.1).
        Therefore, the “main” code of the benchmark kernel module could use the classic Linux headers for its
        needs while the VS YNC test units could include the VS YNC library headers (that define the required atomic
        types) and use from Linux only the primitives types (such as uint32_t and the likes). This technique also
        enables the possibility to benchmark individually module from the Linux kernel, such as the qspinlock
        located in "linux/spinlock.h" header.
     2. Thread to core affinity assignment. The benchmark module spawns as many kernel threads as requested
        on the module invocation command. To measure the multi-core overheads of the locks, these threads must
        be pinned on individual cores (both within the same NUMA nodes and on different NUMA nodes). For
        this purpose, the Linux kthread_bind() function is used.
     3. Operating frequency fixing. To avoid suffering from thermal effects, and thus the OS dynamically
        changing the operating frequency while the benchmark were running (and by doing so skewing our results),
        we fixed the frequency to 1.5 GHz, a frequency point available on all the platforms used in our evaluations.
        For this purpose, we used the Linux cpufreq mechanism. We set the governor to userspace to be able to
        choose the frequency. We observed that using a fixed governor such as userspace instead of an adaptive
        one (such as ondemand) yields way better predictability in our results.
     4. Disable network. In the preliminary experiments we conducted for our work, we observed that network
        introduced lots of noise into the evaluations by widely spreading the distributions of results (more than
    11 https://e.huawei.com/uk/products/servers/taishan-server/taishan-2280-v2
    12 https://en.wikichip.org/wiki/hisilicon/kunpeng/920-6426
    13 https://www.gigabyte.com/Rack-Server/R182-Z91-rev-100
    14 https://www.amd.com/en/products/cpu/amd-epyc-7352




                                                         33
        10% difference between minimum and maximum observed throughput for a benchmark repeated with
        the same parameters). The simplest solution to avoid these interferences was to disable the network and
        therefore to operate the benchmarks directly on the machine workstation (on the server tty).

   5. Disable IRQ balancing. irqbalance is a Linux daemon in charge of distributing the hardware Interrupts
      Requests (IRQs) among the different processing cores of the platform for the purpose of overall system
      performance. However, sporadic IRQs and subsequent execution of Interrupt Service Routines (ISRs)
      occurring on an uncontrolled set of cores would bring unpredictability in the system response-time and
      interfere with our benchmark measurements. We simply disable this mechanism. Therefore, the Linux
      fallback strategy is to pin all IRQs to the first core, which we remove from our thread affinity assignment
      to completely avoid the issue of running ISRs and benchmarks concurrently on the same cores.
   6. Disable NUMA balancing. On platforms with a large number of cores such as the ones used in these
      experiments (see Section 4.1.1), the CPU cores are organized in NUMA nodes (for Non-Uniform Memory
      Access). This structure allows to palliate the unavoidable pressure on the memory bus due to the high
      amount of processing cores operating in parallel. Banks of memory are allocated per NUMA node,
      reflecting the cache hierarchy. NUMA balancing is a feature of Linux that periodically moves the tasks
      closer to the memory they use, i.e.in the right NUMA node. NUMA control is an additional tool allowing
      to configure NUMA-aware task scheduling and memory allocation in a fine-grain manner, this overriding
      the overall system NUMA balancing. We disable system NUMA balancing, and we enable task-local
      NUMA control, using this syntax:
        sudo numactl -- cpubind =0 -- membind =0 < cmd_to_insert_kernel_module >

        This goes one step further as task affinity assignment, as it forces memory allocation to be bound on NUMA
        node 0. Our benchmark being inherently concurrent, as soon as there will be more threads than cores per
        NUMA node, these threads will be allocated on the next NUMA node. For userspace benchmarks, we
        use libnuma directly in our pthread wrapper to pin threads to cores and control the allocation of context
        data structures. Therefore, the cross-node threads will suffer some performance loss when trying to access
        shared data (e.g. spinlock data structures).

   7. Completely isolate the cores. The Linux kernel provides the possibility to isolate a subset of the CPU
      cores. To do so, the parameter isolcpus must be filled with the list of CPU core identifiers to isolate.
      This parameter is given on the Linux boot argument command line (i.e.in Grub for our case, prior to
      the kernel boot). This has the effect of completely preventing the scheduling and other task balancing
      mechanisms (such as SMP balancing) to operate on these cores. Unless explicitly required with task
      affinity configuration (with the corresponding system calls or by using the taskset program), the OS will
      not schedule any task on these isolated cores. In our case, we decided to isolate all cores but the first, with
      the idea of running our benchmarks on the isolated cores, while the rest of the Linux processes would run
      on the Core 0 to avoid interfering with our results.
   8. Kernel threads priority. We tried several configurations of niceness for our kernel threads by calling
      the set_user_nice() Linux function, but this did not seem to impact the distribution of our results. This
      is to be expected with the precautions described above. The benchmark response time variability weren’t
      influenced by the priority of the kernel threads.

4.2     Microbenchmark evaluation
In this section, we present the microbenchmark experiments carried-out for the paper. We first describe the
experiment itself and then discuss the results obtained.
4.2.1    Experiment details
The microbenchmark works as follow: each thread repeatedly acquires a (writer) lock, increments a shared
counter, and releases the lock. This is summarized in pseudo-C in Listing 1.



                                                        34
                                                Listing 1: Pseudo-C code of microbenchmark
1    /* the tested lock is parameterized here */
2    # include < vsync /< chosen > lock .h >
3

4    /* lock variable */
5    static lock_s lock_var ;
6

7  /*
8   * supposedly already allocated,
 9  * we also take care of cacheline-alignment
10  * to avoid false sharing.
11  */
12 unsigned long long * shared_counter ;
13

14   /* ... */
15

16 unsigned long long run ()
17 {
18     * shared_counter = 0 ull ;
19     lock_init (& lock_var );
20

21            do {
22                    lock_acquire (& lock_var );
23

24                   (* shared_counter ) ++;
25

26                lock_release (& lock_var );
27            } while (! thread_should_stop () );
28

29            return * shared_counter ;
30   }
          The returned counter is used to compute the throughput (number of times the critical sections was accessed
     by any thread). We vary the number of threads in the following set 15 : {1, 2, 4, 8, 16, 23, 31, 63, 95, 127}. We run
     each experiment for a fixed period of time (30 seconds) and measure the throughput (number of critical sections
     per second). We run the experiments 5 times to ensure the stability of the results (for each case, we pick the
     median of these repeated runs).
          For spinlocks and reader-writer locks, the benchmark runs as a Linux kernel module. It means that we insert
     in the kernel a kernel module (*.ko file) that is linked with the code listed in Listing 1. When inserted, the
     module runs an initialization routine that consists in spawning as many kernel threads as requested (as explained
     above, this is a parameter of the experiment), and each thread runs the code listed in Listing 1, until interrupted
     by a timer (the 30-seconds execution). This timer is triggered externally, when removing the module from the
     kernel, as the exit routine of the module is requiring all the threads to finish their execution (it is not possible
     to kill a kernel thread with a kill signal). This kernel module is inspired by the previous work of Kashyap et
     al. [14], where they (nano-)benchmarked the behavior of a hash-table in kernel-mode to evaluate several locking
     primitives.
          For mutexes, we replace pthread_mutex using LD_PRELOAD, and the benchmark runs in Linux userspace.
          About the selected locking primitives, we compare two variants of each primitive: an sc-only variant, and a
     VS YNC-optimized variant with barriers.
         15 Obviously, the 127-thread case can only be run on platforms with 128 cores. It is omitted in the other cases.




                                                                           35
         architecture   algorithm                       seqopt      threads_nb        run_nb          atomics    count              duration   throughput
 0       ARMv8          array                           opt         1                 1               a64        957109580          30.0122    3.18907e+07
 1       ARMv8          array                           opt         1                 2               a64        957161287          30.0133    3.18913e+07
 2       ARMv8          array                           opt         1                 3               a64        957576858          30.025     3.18926e+07
 3       ARMv8          array                           opt         1                 4               a64        957238417          30.0143    3.18927e+07
 4       ARMv8          array                           opt         1                 5               a64        957129609          30.0141    3.18893e+07
 5       ARMv8          array                           opt         2                 1               a64        209273223          30.0116    6.97308e+06
 6       ARMv8          array                           opt         2                 2               a64        205836422          30.0118    6.85851e+06
 7       ARMv8          array                           opt         2                 3               a64        205883982          30.0119    6.86008e+06
 ...     ...            ...                             ...         ...               ...             ...        ...                ...        ...
 3697    x86_64         musl                            seq         63                3               a64        10917032           30.0052    363838
 3698    x86_64         musl                            seq         63                4               a64        12659470           30.0059    421900
 3699    x86_64         musl                            seq         63                5               a64        10882122           30.0047    362681
 3700    x86_64         musl                            seq         95                1               a64        11842053           30.0067    394647
 3701    x86_64         musl                            seq         95                2               a64        11655763           30.0056    388453
 3702    x86_64         musl                            seq         95                3               a64        13233013           30.0067    441002
 3703    x86_64         musl                            seq         95                4               a64        13896114           30.0062    463108
 3704    x86_64         musl                            seq         95                5               a64        13857038           30.0065    461801
                        Table 2: Raw captured records, with parameters and output values.

                                           120
                                                                                                                         Architecture
                                                                                                                           ARMv8
                                                                                                                           x86_64
                                           100



                                            80
                        Count of Records




                                            60




                                            40




                                            20




                                             0
                                                 1.00   1.16     1.32     1.48      1.64       1.80     1.96    2.12
                                                                          stability (binned)

Figure 23: Density of the stability of the different records, per architecture. The chart exhibits the fact that most
results are very stable (< 1.16 for stability).
4.2.2   Results
Grouping and filtering records. The raw experiment results look like a list of records as showed in Table 2.
The count column represents the value returned by the function run() of Listing 1, i.e.the number of times
a thread access the critical section. The duration column is the measured duration (even if it is fixed, some
                                                                     count
deviation may occur). Lastly, the throughput column is simply duration      , effectively capturing the number of
critical sections per second.
     The records then get grouped together by parameters, and throughput mean, median and stability are
computed, as reported on Table 3.
     As can be seen on the table, these values are computed for different versions of the algorithm. opt refers to
the VS YNC-optimized version of the algorithm, while seq refers to the sc-only variant.
     Mean, median and standard deviation are computed using the usual definitions, while the stability is computed
by dividing the maximum throughput by the minimum throughput, effectively giving an indication on the stability
of the data set. The closer the stability is to 1.00, the more stable the sample is for these fixed values of the
parameters. Figure 23 shows the repartition of the stability among the records of the above table. As can be
observed on the density chart, most observed values are stable.


                                                                                     36
                                                  mean            median           std        stability
 arch       algorithm    seqopt    threads_nb
 aarch64    array        opt       1              3.18913e+07     3.18913e+07      1436.94    1.00011
                                   2              6.87696e+06     6.85993e+06      54935.1    1.02047
                                   4              4.08881e+06     4.10817e+06      57940.8    1.03005
                                   8              3.91338e+06     3.90199e+06      49164.6    1.03246
                                   16             3.75618e+06     3.74699e+06      15217      1.00958
                                   23             2.48333e+06     2.41812e+06      105903     1.09302
                                   31             2.23512e+06     2.23639e+06      6561.7     1.00759
                                   63             1.74074e+06     1.74047e+06      8351.25    1.01191
                                   95             1.32026e+06     1.32048e+06      5805.31    1.01172
                                   127            1.11277e+06     1.10708e+06      11596.4    1.02398
                         seq       1              2.67509e+07     2.67693e+07      30079.4    1.0026
                                   2              5.66552e+06     5.69127e+06      62049.8    1.02652
                                   4              3.47092e+06     3.46877e+06      15011.9    1.01014
                                   8              3.10139e+06     3.10546e+06      7845.61    1.006
                                   16             3.05401e+06     3.05231e+06      4886.13    1.00395
                                   23             2.08272e+06     2.06173e+06      64897.5    1.07889
                                   31             1.92977e+06     1.92845e+06      10816.1    1.0132
                                   63             1.52597e+06     1.53138e+06      17730.6    1.02815
                                   95             1.11215e+06     1.10892e+06      13310.7    1.02923
                                   127            899750          898612           10382.7    1.02754
 ...        ...          ...       ...            ...             ...              ...        ...
 x86_64     ttas         seq       63             1.16617e+06     1.16119e+06      14598.2    1.03091
                                   95             1.16657e+06     1.16654e+06      9672.9     1.01849
            twa          opt       1              3.64516e+07     3.64537e+07      29737.1    1.00216
                                   2              6.02238e+06     6.02219e+06      1489.88    1.00069
                                   4              2.10028e+06     2.12157e+06      68586.1    1.09087
                                   8              2.27264e+06     2.28098e+06      34452.2    1.03792
                                   16             2.06737e+06     2.06864e+06      3631.41    1.00465
                                   23             1.85262e+06     1.85316e+06      1579.55    1.00227
                                   31             1.48692e+06     1.48739e+06      3060.34    1.00574
                                   63             1.23218e+06     1.23213e+06      3422.3     1.00665
                                   95             1.11774e+06     1.11715e+06      5174.11    1.01166
                         seq       1              1.39532e+07     1.39525e+07      8965.07    1.00157
                                   2              1.51132e+07     1.50894e+07      119766     1.02114
                                   4              3.3227e+06      3.31492e+06      13600.1    1.00948
                                   8              2.69598e+06     2.6822e+06       19174.8    1.0132
                                   16             2.09911e+06     2.10757e+06      17185.9    1.01866
                                   23             1.89835e+06     1.89785e+06      3783.31    1.00542
                                   31             1.71193e+06     1.7124e+06       5194.5     1.0076
                                   63             1.44299e+06     1.44049e+06      12048.1    1.01896
                                   95             1.09068e+06     1.08852e+06      8834       1.01751
Table 3: Records grouped by target platform, lock algorithm, sc-only/VS YNC-optimized version and number
of threads. Computed values are median, mean, standard deviation and stability of the throughput column of
Table 2.



                                                   37
                                                 Stability values        Amount (absolute)            Amount (%)
                                                              ≤ 1.1                           627            84.62%
                                                              > 1.1                           114            15.38%
                                                              > 1.2                            45             6.07%
                                                              > 1.3                            16             2.16%
                                                              > 1.4                             9             1.21%
                                                              Total                           741           100.00%
     Table 4: Number of experiments categorized by stability. The mentioned records are lines of Table 3.

                                          50
                                                                                                                    arch
                                                                                                                      aarch64
                                          45                                                                          x86_64

                                          40

                                          35
                       Count of Records




                                          30


                                          25

                                          20

                                          15

                                          10

                                          5


                                          0
                                               −0.650.15   0.95   1.75   2.55   3.35   4.15   4.95   5.75    6.55
                                                                     median-gain (binned)

                   Figure 24: Density of the speedups of the different locks, per architecture.
    Another way to see them is to group the lines of Table 3 by stability values as done in Table 4. We see than
more than 84% of the results have a stability inferior to 10% (value ≤ 1.1 in the table), which we believe is
satisfactory.
    In practice, we filter out all records with more than 20% stability to avoid skewing the results. Indeed,
sometimes the optimization speedup can be in the 0 to 20% improvement range. Therefore, statistically-speaking
computing speedups for unstable values would make little to no sense at all. For our evaluations, it means we
had to throw less than 7% of the results (see Table 4).
    Instead of simply dropping unstable records, an alternate method would be to redraw experiment samples
until it becomes stable (e.g.with a stability threshold value of 1.1). However, for time reasons, we did not use this
method. We believe the results obtained with this method and the method we actually used would be very similar.
Analysis of speedups of VS YNC-optimized over sc-only implementations. Then, we use the values in the
filtered table of records to compute the speedup TTos − 1, where To is median throughput of VS YNC-optimized and
Ts is the median throughput sc-only variants, respectively. Descriptive statistics aggregates about the observed
speedups are showed in Table 5 and the density of the speedup values is showed in Figure 24. In the paper,
for the sake of space, we only reported maximum observed speedups (the max column in Table 5). We can
observe on Figure 24 that most speedups are close to 0. This effect can mainly be observed on the plot because
of the highly-contended cases (number of threads from 8 and up), where the impact of optimizing barrier is
negligible. On the other hand, if we observe the same data but split for all measured contention levels (i.e.number
of threads) as depicted per architecture on Figures 25 and 26, we can analyze the results with finer-grain details.
For ARMv8 (taishan200-128c) (Fig. 25), good results are scattered across the different contentions levels, but
speedups tend to be better for low contention level (especially the 1 thread case). In the case of x86 (Fig. 26), the
tremendous low-contention speedup case (up to 7× for 1 thread) is emphasized. This is so big that it overshadows
the other cases. However, the qspinlock column is clearly better than the others, illustrating that in the x86
case, qspinlock has no negative speedup.



                                                                                  38
 Lock                 aarch64                                       x86_64
                           max       mean         min         std        max        mean         min         std
 ArrayQ lock [13]     0.256496    0.195695    0.136534   0.035925    3.704002    0.512900    0.050954   1.198285
 CertiKOS MCS [12]    0.741137    0.148102    0.014506   0.217878    0.711755    0.323380    0.184185   0.191676
 CLH lock [13]        0.326751    0.116884   -0.008331   0.090660    7.034888    0.767551   -0.150228   2.350886
 c-TKT-MCS [9]        0.633937    0.317441    0.046994   0.196817    1.379088    0.122309   -0.457079   0.497779
 c-TTAS-MCS [9]       0.538990    0.265129    0.063337   0.157456    1.388887    0.114989   -0.454959   0.502378
 c-MCS-TWA            0.610119    0.040497   -0.065989   0.201884    1.250191    0.121885   -0.282231   0.487366
 HCLH lock [13, 22]   0.297295    0.050683   -0.084593   0.105824    1.331446    0.201763   -0.019287   0.430856
 MCS lock [13, 23]    0.776025    0.111308   -0.031085   0.252447    3.605063    0.387545   -0.404894   1.216811
 musl mutex [3]       0.039510   -0.000101   -0.031193   0.026376    0.048818   -0.050181   -0.206353   0.110743
 3-state mutex [10]   0.000157   -0.013167   -0.025476   0.012847   -0.001148   -0.140026   -0.287827   0.143548
 qspinlock [5]        0.235271    0.117755   -0.148553   0.131182    3.966020    0.606631    0.085625   1.261861
 rec. CAS lock        0.078310    0.010387   -0.024441   0.037942    4.099000    1.950000   -0.338620   1.324669
 RW lock              0.546915   -0.007887   -0.405652   0.289225    1.194217    0.671709   -0.015319   0.462634
 Semaphore            0.112009   -0.001584   -0.089416   0.062090    0.004707    0.000205   -0.003467   0.002518
 CAS lock             0.045456   -0.007812   -0.060903   0.031734    4.099994    1.247507   -0.255443   1.175026
 Ticketlock [1]       0.162076    0.009903   -0.060949   0.059517    3.935485    0.633132   -0.392997   1.260925
 TTAS lock [13]       0.094544   -0.011786   -0.110472   0.057227    3.875872    1.322232   -0.286289   1.078801
 TWA lock [7]         0.337384    0.026431   -0.044020   0.112353    1.612696    0.023385   -0.600899   0.627365
Table 5: Speedups of VS YNC-optimized version of the algorithm over sc-only variant. This descriptive summary
must be read with care (especially for the values of mean), as they are only aggregated from our own experiment
samples (our arbitrary selected thread number, etc.).
MCS lock comparisons. Figure 27 compares the performance of several MCS lock implementations on
ARMv8 (taishan200-128c) and x86_64 (gigabyte-96c). As reported in the paper, the different MCS lock
implementations are: DPDK [11], Concurrency Kit (ck) [4], CertiKOS [12] and our VS YNC-optimized.
Critical and non-critical section sizes. We observed a few other things by conducting this campaign of
experiments. Our benchmark setting allows for additional parameters: cs_size and es_size (not reported in
the charts of this report).
    • The cs_size parameter (for “critical section size”) allows to artificially increase (and control) the size
      of the critical section. Instead of only touching one cache line by increasing a counter (as depicted in
      Listing 1), we can touch an arbitrary number of cache lines, which would corresponds to the value of the
      cs_size parameter.
    • The es_size parameter allows to set an arbitrary number of cache lines touched outside the critical section,
      to simulate different relative sizes of the critical section with regards to the size of the whole program.
We observed the following:
   1. The es_size parameter did not influence the results, meaning that the lock primitive performances and
      speedup obtained in VS YNC-optimized over sc-only are not affected by the size of the program that is not
      in the critical section.
   2. The cs_size parameter strongly influenced the results in the following way: the bigger the critical section
      was, the less was the impact of the barrier optimization. Additionally, overall, all locking primitives are
      converging towards the same performance value for an increasing critical section, which is expected as the
      entry/exit protocols are negligible relatively to a sufficiently large critical section.
From this, we can conclude that barrier optimizations and locking protocols make sense especially for small
critical sections and fine-grain locking. For the final results of the paper, we decided to set cs_size to 1 and
es_size to 0.
Hash table benchmarks. Linked to these last findings, prior running our custom-made kernel benchmark
module, we tried to use the work of Kashyap et al. [14] (which is publicly available on Github 16 ), but we were
  16 https://github.com/sslab-gatech/shfllock/tree/master/benchmarks/kernel-syncstress




                                                         39
                                    Speedups observed on ARMv8 target
                                     array                                                  Speedup

                               certikosmcs

                                       clh                                                    0.6

                                cmcsticket
                                                                                              0.4
                                 cmcsttas

                                 ctwamcs                                                      0.2
                                      hclh

                                      mcs                                                     0.0
                       Locks




                                     musl
                                                                                              −0.2
                                    mutex

                                    qspin
                                                                                              −0.4
                                   recspin
                                       rw
                               semaphore

                                      spin

                                    ticket
                                      ttas

                                      twa
                                                             16

                                                                  23
                                                                       31
                                                                            63

                                                                                 95
                                             1

                                                 2
                                                     4
                                                         8




                                                                                      127
                                                     Thread number
Figure 25: Heat map showing the speedups of the different locks on ARMv8 (taishan200-128c).
White squares correspond to data filtered-out for instability.
not able to produce predictable results. Indeed, the variability of such results was very high, and each time
we changed a small parameter it produced different output values. It happened even for details that should not
influence the results, such as changing the linking order of the object modules in the makefile. This was unusable
for our work, and could be explained in the following way: basically, the critical section in the kernel syncstress
module of Kashyap et al. is accessing nodes of a hash table. The data of this hash table is randomly populated.
However, accessing a hash table is not a predictable operation in terms of run-time, and different access can yield
very different execution times (especially if the hash table is seeded with different random values at each run).
This would lead to critical section size being very different for different runs (even with the same parameter
values), and was therefore not usable to compare different techniques. In comparison, our microbenchmark
framework, although being simpler in its structure, produce very predictable results (with very small deviations
and good stability, as showcased above in this section) and allow to precisely measure the overheads of barriers
and the performance of different locking primitive implementations.




                                                             40
                                Speedups observed on x86_64 target
                                   array                                             Speedup

                             certikosmcs
                                                                                       6
                                     clh

                              cmcsticket

                               cmcsttas
                                                                                       4
                               ctwamcs

                                    hclh

                                    mcs                                                2
                     Locks




                                   musl
                                  mutex
                                                                                       0
                                  qspin

                                 recspin
                                     rw

                             semaphore

                                    spin

                                  ticket

                                    ttas

                                    twa
                                                            16

                                                                 23

                                                                      31

                                                                           63

                                                                                95
                                           1

                                               2
                                                    4

                                                        8




                                                    Thread number
Figure 26: Heat map showing the speedups of the different locks on x86_64 (gigabyte-96c).
White squares correspond to data filtered-out for instability.

References
 [1] Linux ticketlock. https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/
     commit/?id=314cdbefd1fd0a7acf3780e9628465b77ea6a836, 2008.
 [2] Linux-Kernel Memory Model, 2018. http://www.open-std.org/jtc1/sc22/wg21/docs/papers/
     2018/p0124r6.html.
 [3] musl libc: an implementation of the C standard library, 2020. https://musl.libc.org.
 [4] Samy Al Bahra. Concurrency kit.               Retrieved November, 8:2018, 2015.       https://github.com/
     concurrencykit/ck.
 [5] Jonathan Corbet. locks and qspinlocks. https://lwn.net/Articles/590243/, 2014.
 [6] Will Deacon.   locking/qspinlock: Ensure node is initialized before updating prev->next, Feb
     13, 2018. https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/
     ?id=95bcade33a8a.
 [7] Dave Dice and Alex Kogan. Twa – ticket locks augmented with a waiting array. In European Conference
     on Parallel Processing, pages 334–345. Springer, 2019.
 [8] Dave Dice, Alex Kogan, Yossi Lev, Timothy Merrifield, and Mark Moir. Adaptive integration of hardware
     and software lock elision techniques. In Proceedings of the 26th ACM Symposium on Parallelism in
     Algorithms and Architectures, SPAA ’14, page 188–197, New York, NY, USA, 2014. Association for
     Computing Machinery.


                                                            41
 Performance of MCS lock implementations on ARMv8
                                     1 thread         2 threads         4 threads        8 threads       16 threads        23 threads         31 threads               63 threads               95 threads               127 threads
median throughput (M.iters/s)

                                                                                                                                          3                                               2.0
                                                                                                                                                                 2.5                                               1.5
                                                  5                 4                4
                                30                                                                   3                 3
                                                                                                                                                                 2.0                      1.5
                                                  4
                                                                    3                3                                                    2
                                                                                                                                                                                                                   1.0
                                20                3                                                  2                 2                                         1.5
                                                                                                                                                                                          1.0
                                                                    2                2
                                                  2                                                                                                              1.0
                                                                                                                                          1                                                                        0.5
                                10                                                                   1                 1
                                                                    1                1                                                                                                    0.5
                                                  1                                                                                                              0.5

                                0                 0                 0                0               0                 0                  0                      0.0                      0.0                      0.0



 Performance of MCS lock implementations on x86_64
                                     1 thread         2 threads         4 threads        8 threads       16 threads          23 threads             31 threads               63 threads               95 threads
median throughput (M.iters/s)




                                40                                  4                                3                                                                 2.0                      2.0
                                                  8                                                                    2.5                    2.0
                                                                                     3
                                30                                  3                                                                                                  1.5                      1.5
                                                                                                                       2.0                    1.5
                                                  6                                                  2
                                                                                     2
                                                                                                                       1.5
                                20                                  2                                                                                                  1.0                      1.0
                                                  4                                                                                           1.0
                                                                                                     1                 1.0
                                                                                     1
                                10                2                 1                                                                         0.5                      0.5                      0.5
                                                                                                                       0.5

                                0                 0                 0                0               0                 0.0                    0.0                      0.0                      0.0



                                       CertiKOS       ck     DPDK        own impl.

Figure 27: Comparisons of performance of different MCS lock implementations on ARMv8 (taishan-128c)
and x86_64 (gigabyte-96c).
          [9] David Dice, Virendra J. Marathe, and Nir Shavit. Lock cohorting: A general technique for designing numa
              locks. ACM Trans. Parallel Comput., 1(2), February 2015.
[10] Ulrich Drepper. Futexes are tricky. Futexes are Tricky, Red Hat Inc, Japan, 4, 2005.
[11] Linux Foundation. Data Plane Development Kit (DPDK), 2015.

[12] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan Wu, Jieung Kim, Vilhelm Sjöberg, and David Costanzo.
     Certikos: An extensible architecture for building certified concurrent os kernels. In Proceedings of the 12th
     USENIX Conference on Operating Systems Design and Implementation, OSDI’16, page 653–669, USA,
     2016. USENIX Association.
[13] Maurice Herlihy and Nir Shavit. The art of multiprocessor programming. Morgan Kaufmann, 2011.

[14] Sanidhya Kashyap, Irina Calciu, Xiaohe Cheng, Changwoo Min, and Taesoo Kim. Scalable and practical
     locking with shuffling. In Proceedings of the 27th ACM Symposium on Operating Systems Principles,
     SOSP ’19, page 586–599, New York, NY, USA, 2019. Association for Computing Machinery.
[15] Michalis Kokologiannakis, Ori Lahav, Konstantinos Sagonas, and Viktor Vafeiadis. Effective stateless
     model checking for c/c++ concurrency. Proceedings of the ACM on Programming Languages, 2(POPL),
     December 2017.
[16] Michalis Kokologiannakis, Azalea Raad, and Viktor Vafeiadis. Model checking for weakly consistent
     libraries. In Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design
     and Implementation, PLDI 2019, pages 96–110, New York, NY, USA, 2019. Association for Computing
     Machinery.

[17] Michalis Kokologiannakis and Viktor Vafeiadis. Hmc: Model checking for hardware memory models.
     In Proceedings of the Twenty-Fifth International Conference on Architectural Support for Programming
     Languages and Operating Systems, ASPLOS ’20, page 1157–1171, New York, NY, USA, 2020. Association
     for Computing Machinery.




                                                                                                                      42
[18] FAL Labs. Kyoto Cabinet: A straightforward implementation of DBM, 2011. http://fallabs.com/
     kyotocabinet.
[19] Waiman Long. locking/qspinlock: Use _acquire/_release() versions of cmpxchg() & xchg(), Nov
     10, 2015. https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/
     ?id=64d816cba06c.
[20] Waiman Long and Peter Zijlstra.  qspinlock code at version 4.4 of Linux Kernel, 2015.
     https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/kernel/
     locking/qspinlock.c?h=v4.4.

[21] Waiman Long and Peter Zijlstra.  qspinlock code at version 5.6 of Linux Kernel, 2020.
     https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/kernel/
     locking/qspinlock.c?h=v5.6.
[22] Victor Luchangco, Dan Nussbaum, and Nir Shavit. A hierarchical clh queue lock. In European Conference
     on Parallel Processing, pages 801–810. Springer, 2006.

[23] John M. Mellor-Crummey and Michael L. Scott. Algorithms for scalable synchronization on shared-memory
     multiprocessors. ACM Trans. Comput. Syst., 9(1):21–65, February 1991.
[24] Jonas Oberhauser, Rafael Lourenco de Lima Chehab, Diogo Behrens, Ming Fu, Antonio Paolillo, Lilith
     Oberhauser, Koustubha Bhat, Yuzhong Wen, Haibo Chen, Jaeho Kim, and Viktor Vafeiadis. VSync:
     Push-Button Verification and Optimization for Synchronization Primitives on Weak Memory Models.
     In Proceedings of the 26th ACM International Conference on Architectural Support for Programming
     Languages and Operating Systems, ASPLOS ’21, New York, NY, USA, 2021. Association for Computing
     Machinery.
[25] Anton Podkopaev, Ori Lahav, and Viktor Vafeiadis. Bridging the gap between programming languages and
     hardware weak memory models. Proceedings of the ACM on Programming Languages, 3(POPL), January
     2019.
[26] Christopher Pulte, Shaked Flur, Will Deacon, Jon French, Susmit Sarkar, and Peter Sewell. Simplifying
     arm concurrency: Multicopy-atomic axiomatic and operational models for armv8. Proceedings of the ACM
     on Programming Languages, 2(POPL), December 2017.

[27] Pan Xinhui. locking/qspinlock: Use atomic_sub_return_release() in queued_spin_unlock(), Jun
     3, 2016. https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/
     ?id=ca50e426f96c.




                                                   43
