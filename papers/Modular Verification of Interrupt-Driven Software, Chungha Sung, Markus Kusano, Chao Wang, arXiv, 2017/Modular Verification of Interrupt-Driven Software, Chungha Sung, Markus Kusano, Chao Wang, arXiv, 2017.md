                                            Modular Verification of Interrupt-Driven Software
                                                            Chungha Sung                           Markus Kusano                             Chao Wang
                                                   University of Southern California                 Virginia Tech                 University of Southern California
                                                      Los Angeles, CA, USA                      Blacksburg, VA, USA                   Los Angeles, CA, USA



                                            Abstract—Interrupts have been widely used in safety-critical       the sound approximation of complex constructs such as loops,
                                         computer systems to handle outside stimuli and interact with          recursions and numerical computations. However, although ab-
                                         the hardware, but reasoning about interrupt-driven software           stract interpretation techniques have been successfully applied
                                         remains a difficult task. Although a number of static verification
                                         techniques have been proposed for interrupt-driven software,          to sequential [6] and multithreaded software [27], they have not
                                                                                                               been able to precisely model the semantics of interrupt-driven
arXiv:1709.10078v1 [cs.PL] 28 Sep 2017




                                         they often rely on constructing a monolithic verification model.
                                         Furthermore, they do not precisely capture the complete ex-           software.
                                         ecution semantics of interrupts such as nested invocations of            At the high level, interrupts share many similarities with
                                         interrupt handlers. To overcome these limitations, we propose         threads, e.g., both interrupt handlers and thread routines may
                                         an abstract interpretation framework for static verification of
                                         interrupt-driven software that first analyzes each interrupt han-     be regarded as sequential programs communicating with others
                                         dler in isolation as if it were a sequential program, and then        via the shared memory. However, there are major differences
                                         propagates the result to other interrupt handlers. This iterative     in the way they interleave. For example, in most of the existing
                                         process continues until results from all interrupt handlers reach a   verification tools, threads are allowed to freely preempt each
                                         fixed point. Since our method never constructs the global model,      other’s execution. In contrast, interrupts often have various
                                         it avoids the up-front blowup in model construction that hampers
                                         existing, non-modular, verification techniques. We have evaluated     levels of priority: high-priority interrupts can preempt low-
                                         our method on 35 interrupt-driven applications with a total of        priority interrupts but not vice versa. Furthermore, interrupts
                                         22,541 lines of code. Our results show the method is able to          with the same level of priority cannot preempt each other. Thus,
                                         quickly and more accurately analyze the behavior of interrupts.       the behavior manifested by interrupts has to be viewed as a
                                                                                                               subset of the behavior manifested by threads.
                                                               I. I NTRODUCTION                                   To accurately analyze the behavior of interrupts, we develop
                                            Interrupts have been widely used in safety-critical embedded       IntAbs, an iterative abstract interpretation framework for
                                         computing systems, information processing systems, and mo-            interrupt-driven software. That is, the framework always
                                         bile systems to interact with hardware and respond to outside         analyzes each interrupt handler in isolation before propagating
                                         stimuli in a timely manner. However, since interrupts may arrive      the result to other interrupt handlers and the per interrupt
                                         non-deterministically at any moment to preempt the normal             analysis is iterated until results on all interrupt handlers
                                         computation, they are difficult for developers to reason about.       stabilize, i.e., they reach a fixed point. Thus, in contrast
                                         The situation is further exacerbated by the fact that interrupts      to traditional techniques, it never constructs the monolithic
                                         often have different priority levels: high-priority interrupts        verification model that often causes exponential blowup up front.
                                         may preempt low-priority interrupts but not vice versa, and           Due to this reason, our method is practically more efficient
                                         interrupt handlers may be executed in a nested fashion. Overall,      than these traditional verification techniques.
                                         methods and tools for accurately modeling the semantics of               The IntAbs framework also differs from prior techniques
                                         interrupt-driven software are still lacking.                          for statically analyzing interrupt-driven software, such as
                                            Broadly speaking, existing techniques for analyzing inter-         the source-to-source transformation-based testing approach
                                         rupts fall into two categories. The first category consists of        proposed by Regehr [31], the sequentialization approach used
                                         techniques based on testing [12], [30], which rely on executing       by Wu et al. [42], and the model checking technique imple-
                                         the program under various interrupt invocation sequences. Since       mented in iCBMC [18]. For example, none of these existing
                                         it is often practically infeasible to cover all combinations          techniques can soundly handle infinite loops, nested invocations
                                         of interrupt invocations, testing will miss important bugs.           of interrupts, or prove the absence of bugs. Although some
                                         The second category consists of static verification techniques        prior abstract interpretation techniques [28] over-approximate
                                         such as model checking [3], [18], [33], [36], [43], which             of the interrupt behavior, they are either non-modular or too
                                         rely on constructing and analyzing a formal model. During             inaccurate, e.g., by allowing too many infeasible store-to-
                                         the modeling process, interrupt-related behaviors such as             load data flows between interrupts. In contrast, our approach
                                         preemption are considered. Unfortunately, existing tools such         precisely models the preemptive scheduling of interrupts to
                                         as iCBMC [18] need to bound the execution depth to remain             identify apparently-infeasible data flows. As shown in Fig. 1,
                                         efficient, which means shallow bugs can be detected quickly,          by pruning away these infeasible data flows, we can drastically
                                         but these tools cannot prove the absence of bugs.                     improve the accuracy of the overall analysis.
                                            In this paper, we propose a static verification tool geared           IntAbs provides not only a more accurate modeling of the
                                         toward proving the absence of bugs based on abstract inter-           interrupt semantics but also a more efficient abstract interpre-
                                         pretation [5]. The main advantage of abstract interpretation is       tation framework. We have implemented IntAbs in a static
                                                                                     irq_H() {                irq_L() {                    irq_M() {

                                                                                         ...                       x = 0;                       y = 1;
 Interrupt Driven    Abstract Interpretation   Propagating Results                                                                              x = 1;
                                                                      Invariants
     Program           of Each Interrupt       to Other Interrupts                       assert(y==0);             assert(x==0);               assert(x==1);
                                                          Query                      }                        }                            }

                                                   Feasibility                      Fig. 2. An example program with three interrupt handlers and assertions.
                         Datalog Facts
                                                   Checking
                        Datalog Rules                (µZ)

                                                                                                           irq_H           irq_M   irq_L
Fig. 1. IntAbs – iterative verification framework for interrupt-driven programs.                  case0

                                                                                                                   irq_H

analysis tool for C/C++ programs, which uses Clang/LLVM [1]                                                irq_M                   irq_L
                                                                                                   case1
as the front-end, Apron [16] for implementing the numerical
abstract domains, and µZ [13] for checking the feasibility                                                         irq_H
of data flows between interrupts. We evaluated IntAbs on 35                                                irq_L                   irq_M
                                                                                                   case2
interrupt-driven applications with a total of 22,541 lines of C
code. Our experimental results show that IntAbs can efficiently                                                        irq_H
as well as more accurately analyze the behavior of interrupts                                                      irq_M
by removing a large number of infeasible data flows between                                                irq_L
interrupts.                                                                                        case3

   In summary, the main contributions of our work are:
   • A new abstract interpretation framework for conducting
      static verification of interrupt-driven programs.                               Fig. 3. Some possible interrupt sequences for the program in Fig. 2.
   • A method for soundly and efficiently identifying and
      pruning infeasible data flows between interrupts.
   • The implementation and experimental evaluation on a
                                                                                   Fig. 2, for example, since the interrupt handlers have different
      large number of benchmark programs to demonstrate the                        priority levels, we need to consider preemption while creating
      effectiveness of the proposed techniques.                                    the test sequences. Since a high-priority interrupt handler may
                                                                                   preempt, at any time, the execution of a medium- or low-
   The remainder of this paper is organized as follows. We first
                                                                                   priority interrupt handler, when irq_L is executing, irq_H
motivate our approach in Section II by comparing it with testing,
                                                                                   may be interleaved in between its instructions.
model checking, and abstract interpretation tools designed
                                                                                      Fig. 3 shows four of the possible interrupt sequences for
for threads. Then, we provide the technical background on
                                                                                   the program. Specifically, case0 is the sequential execution
interrupt modeling and abstract interpretation in Section III.
                                                                                   of the three handler functions; case1 shows that irq_H
Next, we present our new method for checking the feasibility
                                                                                   preempts irq_M, followed by irq_L; case2 is similar, except
of data flows between interrupts in Section IV, followed by our
                                                                                   that irq_L executes first and then is preempted by irq_H,
method for integrating the feasibility checking with abstract
                                                                                   followed by irq_M; and case3 is the nested case where irq_L
interpretation in Section V. We present our experimental
                                                                                   is preempted by irq_M and then by irq_H.
evaluation in Section VI. Finally, we review the related work
                                                                                      The main problem of testing is that there can be too many
in Section VII and conclude in Section VIII.
                                                                                   such interrupt sequences to explore. Even if we can somehow
                       II. M OTIVATION                                             guarantee that each interrupt handler is executed only once,
   We first use examples to illustrate the problems of prior                       the total number of test sequences can be enormously large,
techniques such as testing, model checking, and thread-modular                     even for small or medium-sized programs.
abstract interpretation. Then, we explain how our method
                                                                  B. Model Checking
overcomes these problems.
   Consider the example program in Fig. 2, which has three           Model checking tools such as CBMC [4] may be used to
interrupts irq_H, irq_L and irq_M. The suffix H is used search for erroneous interrupt sequences, e.g., those leading
to denote high priority, L for low priority, and M for medium to assertion violations. For instance, in the running example,
priority. Interrupts with higher priority levels may preempt all assertions hold under the sequences case0 and case2 in
interrupts with lower priority levels, but not vice versa. Inside Fig. 3. This is because, although irq_H preempts irq_L, they
the handlers, there are two variables x and y, which are set to access different variables and thus do not affect the assertion
0 initially. Among the three assertions, the first two may fail, conditions, while irq_M checks the value of x after assigning
while the last one always holds.                                  1 to x.
                                                                     In case1, however, the execution order of the three interrupt
A. Testing                                                        handlers is different, thus leading to an assertion violation inside
   Testing an interrupt-driven program requires the existence irq_H. More specifically, irq_M is preempted by irq_H at
of interrupt sequences, which must be generated a priori. In first. Then, after both completes, irq_L is executed. So, the
                                   y = 0; initialized value                            irq_M() {             irq_L() {             irq_H() {
            assert(y==0)                                                                   if (...)              ...                   if (...)
                                   y = 1; from irq_M     Feasible                            y = 0;                                      x = 0;
                                                                                                                 y = 1;
                                                                                           y = 1;                ...                   x = 1;
                                   x = 0; from irq_L
            assert(x==0)                                                                   assert(x==1);         assert(y==1);         assert(y==1);
                                   x = 1; from irq_M                                   }                     }                     }

                                   x = 0; from irq_L     Infeasible
                                                                                 Fig. 5. An example program with three interrupt handlers, where the first two
            assert(x==1)
                                                                                 assertions alway hold but the last assertion may fail.
                                   x = 1; from irq_M

                                                                                 Due to the different priority levels, certain store-to-load data
Fig. 4. Some possible store-to-load data flows during abstract interpretation.   flows are no longer feasible, as shown by the stores marked
                                                                                 by red boxes in Fig. 4: these two stores have lower priority
                                                                                 than the corresponding load in the assertions.
change of y may affect the read of y in irq_H, leading to
the violation.                                                                   D. Abstract Interpretation for Interrupts
   Finally, in case3, both of the first two assertions may be        Modeling the priority levels alone, however, is not enough
violated, because the check of x in irq_L and the check of        for proving all assertions because even without preemption,
y in irq_H can be affected by irq_M’s own assignments of          a low-priority interrupt may affect a high-priority interrupt.
x and y.                                                          Consider the first red box in Fig. 4. Although y=1 from irq_M
   Although bounded model checking can quickly find bugs,         cannot affect the load of y in irq_H through preemption, if
e.g., the assertion violations in Fig. 2, the depth of the execution
                                                                  irq_H is invoked after irq_M ends, y can still get the value
is often bounded, which means in practice, tools such as          1, thus leading to the assertion violation. Therefore, our new
iCBMC [18] cannot prove the absence of bugs.                      verification procedure has to consider all possible sequential
                                                                  interleavings of the interrupt handlers as well.
C. Abstract Interpretation                                           Now, consider the program in Fig. 5, which has three
   Abstract interpretation is a technique designed for proving interrupt handlers irq_M, irq_L and irq_H. In these handler
properties, e.g., assertions always hold. Unfortunately, existing functions, there are two global variables x and y, which
methods based on abstract interpretation are mostly designed are set to 0 initially. Among the three assertions, the first
for threads as opposed to interrupts. Since threads interact two always hold, whereas the last one may fail. For ease of
with each other more freely than interrupts, these methods are comprehension, we assume the computer hardware running
essentially over-approximated analysis. As such, they may still this program provides the sequentially consistent memory [20],
be leveraged to prove properties in interrupt-driven programs, [22], [45]. Note that irq_M has two stores of y, one inside
albeit in a less accurate fashion. That is, when they prove the conditional branch and the other outside, and irq_H has
an assertion holds, the assertion indeed holds; but when they two stores of x, one inside the conditional branch and the other
cannot prove an assertion, the result is inconclusive.            outside.
   For the running example in Fig. 2, for instance, existing         With prior thread-modular analysis [19], [24], [27], all three
abstract interpretation techniques such as Miné [24], [27], assertions may fail because the store y=0 in irq_M may be
designed for analyzing threads, cannot prove any of the three interleaved right before the assertions in irq_L and irq_H.
assertions. To see why, let us first assume that interrupt Furthermore, the store x=0 in irq_H executed before irq_M
handlers are thread routines. During thread-modular abstract may lead to the violation of the assertion in irq_M. In contrast,
interpretation, the verification procedure would first gather all with our precise modeling of the interrupt behavior, the new
possible pairs of load and store instructions with respect to method can prove that the first two assertions always hold.
the global variables, as shown in Fig. 4, where each assertion Specifically, the assertion in irq_L holds because, even if it is
has two possible loads. Specifically, the load of y in irq_H preempted by irq_M, the value of y remains 1. Similarly, the
corresponds to the initial value 0 and the store in irq_M. The assertion in irq_M holds because, even if it is preempted by
load of x in irq_L corresponds to the stores in irq_L and irq_H, the store x=1 post-dominates the store x=0, meaning
irq_M. The load of x in irq_M corresponds to the stores in the value of x remains 1 after irq_H returns.
irq_L and irq_M.                                                     In contrast, the assertion in irq_H may fail if irq_H
   Since these existing methods [24], [27] assume that all preempts irq_M right after the conditional branch that sets
stores may affect all loads, they would incorrectly report that y to 0. This particular preemption is feasible because irq_H
all three assertions may fail. For example, it reports that the has a higher priority than irq_M.
load of x in irq_M may (incorrectly) read from the store             Therefore, our new method has to consider not only the
x=0 in irq_L despite that irq_L has a lower priority and different levels of priority of all interrupts, but also the
thus cannot preempt irq_M. In contrast, our new method can domination and post-domination relations within each handler.
successfully prove the third assertion. Specifically, we model It decides the feasibility of store-to-load data flows based on
the behavior of interrupts with different levels of priorities. whether a load has a dominated store, whether a store has a
                                                                    TABLE I
                   C OMPARING I NTA BS WITH T ESTING AND P RIOR V ERIFICATION M ETHODS ON THE P ROGRAMS IN F IG . 2 AND F IG . 5.

  Property                           Testing [12], [30]   Model Checking (bounded) [18], [42]   Abs. Int. for Threads [19], [27]   IntAbs for Interrupts (new)
  assertion in Fig. 2: irq_H              violation                   violation                             warning                         warning
  assertion in Fig. 2: irq_L              violation                   violation                             warning                         warning
  assertion in Fig. 2: irq_M                                                                           (bogus) warning                       proof
  assertion in Fig. 5: irq_M                                                                           (bogus) warning                       proof
  assertion in Fig. 5: irq_L                                                                           (bogus) warning                       proof
  assertion in Fig. 5: irq_H             violation                     violation                            warning                         warning



                                                                               Consider the example program in Fig. 6, which has two
           run0() {              run1() {                                   functions named run0 and run1. If they were interrupts,
                stmt1;                    stmt3;                            where run1 has a higher priority level than run0, then after
                stmt2;                    stmt4;
                                                                            executing stmt1, there can only be two possible traces. The
              }                         }
                                                                            first one is for run1 to wait until run0 ends, and the second
           • Possible traces for interrupts:                                one is for run1 to preempt run0. If they were threads,
               – stmt1 → stmt2 → stmt3 → stmt4                              however, there can be three possible traces after executing
               – stmt1 → stmt3 → stmt4 → stmt2
           • Possible traces for threads:
                                                                            stmt1. In addition to the traces allowed by interrupts, we
               – stmt1 → stmt2 → stmt3 → stmt4                              can also execute stmt3 in run1, then execute stmt2 in
               – stmt1 → stmt3 → stmt4 → stmt2                              run0, and finally execute stmt4 in run1. The third trace is
               – stmt1 → stmt3 → stmt2 → stmt4
                                                                            infeasible for interrupts because the high-priority run1 cannot
 Fig. 6. The interleavings (after stmt1) allowed by interrupts and threads. be preempted by stmt2 of the low-priority run0.
                                                                               Since the interleaving behavior of interrupts is a strict subset
                                                                            of the interleaving behavior of threads, it is always safe to
post-dominated store, and whether a load-store pair is allowed apply a sound static verification procedure designed for threads
by the priority levels of the interrupts. We present the details to interrupts. If the verifier can prove the absence of bugs by
of this feasibility-checking algorithm in Section IV.                       treating interrupts as threads, then the proof is guaranteed to
   To sum up, the main advantages of IntAbs over state-of-the- be valid for interrupts. The result of this discussion can be
art techniques are shown in Table I. Specifically, testing and summarized as follows:
(bounded) model checking tools are good at detecting bugs
(e.g., assertion violations) but cannot prove the absence of bugs,             Theorem 1: Since the interleaving behavior of interrupts is a
whereas thread-modular abstract interpretation tools are good               subset   of the interleaving behavior of threads, proofs obtained
at obtaining proofs, but may report many false positives (i.e.,             by  any   sound abstract interpretation over threads remain valid
bogus warnings). In contrast, our new abstract interpretation               for  interrupts.
method is significantly more accurate. It can obtain more proofs               However, the reverse is not true: a bug reported by the
than prior techniques and, at the same time, can significantly verifier that treats interrupts as threads may not be a real bug
reduce the number of bogus warnings.                                        since the erroneous interleaving may be infeasible. In practice,
                                                                            there are also tricky corner cases during the interaction of
                             III. P RELIMINARIES                            interrupts, such as nested invocations of handlers, which call
   In this section, we describe how interrupt-driven programs for a more accurate modeling framework for interrupts.
are modeled in our framework by comparing their behavior to                    Interrupts may also be invoked in a nested fashion as shown
the behavior of threads. Then, we review the basics of prior                by  case3 in Fig. 3, which complicates the static analysis. Here,
abstract interpretation techniques.                                         we   say interrupts are nested when one’s handler function is
                                                                            invoked before another’s handler function returns, and the third
A. Modeling of Interrupts                                                   handler function is invoked before the second handler function
                                                                            returns. Such nested invocations are possible, for example, if the
   We consider an interrupt-driven program as a finite set T = corresponding interrupts have different priority levels, where
{T1 , . . . , Tn } of sequential programs. Each sequential program the inner most interrupt has the highest priority level. This
Ti , where 1 ≤ i ≤ n, denotes an interrupt handler. For ease of behavior is different from thread interleaving; with numerous
presentation, we do not distinguish between the main program corner cases, it requires the development of dedicated modeling
and the interrupt handlers. Globally, sequential programs in T and analysis techniques.
are executed in a strictly interleaved fashion. Each sequential
program may access its own local variables; in addition, it may B. Abstract Interpretation for Threads
access a set of global variables, through which it communicates                Existing methods for modular abstract interpretation are
with the other sequential programs in T .                                   designed almost exclusively for multithreaded programs [19],
   The interleaving behavior of interrupts is a strict subset of [24], [25], [27]. Typically, the analyzer works on each thread
the interleaving behavior of threads (c.f. [18]). This is because in isolation, without creating a monolithic verification model
concurrently running threads are allowed to freely preempt each as in the non-modular techniques [7], [42], to avoid the up-
other’s executions. However, this is not the case for interrupts. front complexity blowup. At a high level, the analyzer iterates
Algorithm 1 Local analysis of T with prior interferences I.                      Algorithm 2 Analysis of the entire program, i.e., a set of T ’s.
 1: function A NALYZE L OCAL(T = hN, n0 , δi, I)                                  1: function A NALYZE P ROG(P )
 2:   S←∅                                         . Map from nodes to states      2:   S ← map all nodes to ⊥
 3:   W ← {n0 }                                      . Set of nodes to process    3:   S0 ← S
 4:   while ∃n ∈ W do                                                             4:   repeat
 5:     W ← W \ {n}                                                               5:     S = S0
 6:     if n is a shared-memory read of variable v then                           6:     for all TU∈ P do
 7:        s ← TFUNC(n, S(n) t I(v))                                              7:         I ← I NTERF(T 0 , S) for each T 0 ∈ P, T 0 6= T
 8:     else                                                                      8:         S 0 ← S 0 ] A NALYZE L OCAL(T, I)
 9:        s ← TFUNC(n, S(n))                                                     9:   until S 0 = S
10:      for all hn, n0 i ∈ δ such that s 6v S(n0 ) do                           10: function I NTERF(T = hN, n0 , δi, S)
11:        S(n0 ) ← S(n0 ) t s                                                   11:   I←∅
12:        W ← W ∪ {n0 }                                                         12:   for all n ∈ N do
13:   return S                                                                   13:      if n is a shared memory write to variable v then
                                                                                 14:         I(v) ← I(v) t TFUNC(n, S (n))
                                                                                 15:   return I

through threads in two steps: (1) analyzing each thread in
isolation, and (2) propagating results from the shared-memory
writes of one thread to the corresponding reads of other threads.                all the (abstract) values stored into v by T . Each thread T is
                                                                                 analyzed in isolation by the loop at Lines 4–9. Here, we use
   Let the entire program P be a finite set of threads, where
                                                                                 ] to denote the join (t) of all memory-states on the matching
each thread T is represented by a control-flow graph hN, n0 , δi
                                                                                 nodes.
with a set of nodes N , an entry node n0 , and the transition
relation δ. Each pair (n, n0 ) ∈ δ means control may flow from                      This thread-modular abstract interpretation framework, while
n to n0 . Each node n is associated with an abstract memory-                     more efficient than monolithic verification, is potentially less
state over-approximating the possible concrete states at n. We                   accurate. For example, a load l may see any value written into
assume the abstract domain (e.g., intervals) is defined as a                     the shared memory by a store s even if there does not exist
lattice with appropriate top (>) and bottom (⊥) elements, a                      a path in the program where l observes s. This is why, as
partial-order relation (v), and widening/narrowing operators                     shown in Table I, techniques such as [19], [27] cannot obtain
to ensure that the analysis eventually terminates [5]. We also                   proofs for the programs in Fig. 2 and Fig. 5. In the context of
define an interference I that maps a variable v to the values                    interrupt handlers with priorities, it means that even infeasible
stored into v by some thread T .                                                 store-to-load flows due to priorities may be included in the
   Algorithm 1 shows how a thread-local analyzer works on T                      analysis, thus causing false alarms.
assuming some interferences I provided by the environment                           In the remainder of this paper, we show how to introduce
(e.g., writes in other threads). It treats T as a sequential program.            priorities into the propagation of data flows between interrupts
Let S(n) be the abstract memory-state at node n, n0 be the                       during the analysis, thereby increasing the accuracy while
entry node of T , and W be the set of nodes in T left to be                      retaining its efficiency.
processed. The procedure keeps removing node n from the
work-list W and processing it until W is empty (i.e., a fixed                    IV. F EASIBILITY OF DATA F LOWS BETWEEN I NTERRUPTS
point is reached).
   If node n corresponds to a shared-memory read of variable                        In this section, we present our method for precisely modeling
v, then the transfer function TFUNC (Line 7) assumes that n                      the priority-based interleaving semantics of interrupts, and
can read either the local value (from S) or the value written                    deciding the feasibility of store-to-load data flows between
by another thread (the interference I(v)). The transfer function                 interrupts. If, for example, a certain store-to-load data flow is
TFUNC of an instruction n takes some memory-state as input                       indeed not feasible, it will not be propagated across interrupts
and returns a new memory-state as output; the new memory-                        in Algorithm 2.
state is the result of executing the instruction in the given                       More formally, given a set of store-to-load pairs, we want
memory-state. Otherwise, if n is a local read, in which case the                 to compute a new M UST N OT R EAD F ROM relation, such that
transfer function TFUNC uses the local memory-state (Line 9)                     M UST N OT R EAD F ROM(l, s), for any load l and store s, means
as in the abstract interpretation of any sequential program. The                 if we respect all the other existing store-to-load pairs, then it
analysis result (denoted S) is an over-approximation of the                      would be infeasible for l to get the value written by s.
memory states within T assuming interferences I.                                    We have developed a Datalog-based declarative program
   The procedure that analyzes the entire program is shown                       analysis procedure for computing M UST N OT R EAD F ROM.
in Algorithm 2. It first analyzes each thread, computes the                      Toward this end, we first generate a set of Datalog facts
interferences, and then analyzes each thread again in the                        from the program and the given store-to-load pairs. Then,
presence of these interferences. The iterative process continues                 we generate a set of Datalog rules, which infer the new
until a fixed point on the memory-states of all threads is reached.              M UST N OT R EAD F ROM relation from the Datalog facts. Finally,
Initially, S maps each node in the program to an empty memory-                   we feed the facts together with the rules to an off-the-shelf
state ⊥. S 0 contains the analysis results after one iteration of                Datalog engine, which computes the M UST N OT R EAD F ROM
the fixed-point computation. The function I NTERF returns the                    relation. In our implementation, we used the µ-Z Datalog
interferences of thread T , i.e., a map from some variable v to                  engine [13] to solve the Datalog constraints.
A. Inference Rules
   Before presenting the rules, we define some relations:                     M UST N OT R EAD F ROM(l, s) ← C OVERED L OAD(l) ∧ L OAD(l, v)
   • D OM (a, b): statement a dominates b in the CFG of an                                          ∧ S TORE(s, v) ∧ I NTERCEPTED S TORE(s)
      interrupt handler function.                                           Second, we say a load l covered by a store s in a handler I
   • P OST D OM (a, b): statement a post-dominates b in the CFG          cannot read from any store s0 that cannot preempt I, because
      of an interrupt handler function.                                  the value of s0 will always be overwritten by s. That is, since
   • P RI (s, p): statement s has the priority level p.                  s0 cannot preempt I, it cannot execute in between s and l.
   • L OAD (l, v): l is a load of global variable v.
   • S TORE (s, v): s is a store to global variable v.
                                                                              M UST N OT R EAD F ROM(l, s) ← C OVERED L OAD(l) ∧ L OAD(l, v)
Dominance and post-dominance are efficiently computable [8]                                                ∧ S TORE(s, v) ∧ N O P REEMPT(s, l)
within each interrupt handler (not across interrupt handlers).
Priority information for each interrupt handler, and thus all               Third, we say that, if a store s is intercepted in a handler
its statements, may be obtained directly from the program.               I, then a load l of the same variable that cannot preempt s,
Similarly, L OAD and S TORE relations may be directly obtained           cannot read from the value stored by s. This is because the
from the program.                                                        store intercepting s will always overwrite the value.
   Next, we present the rules for inferring three new relations:
N O P REEMPT, C OVERED L OAD and I NTERCEPTED S TORE.                     M UST N OT R EAD F ROM(l, s) ← I NTERCEPTED S TORE(s) ∧ S TORE(s, v)
                                                                                                              ∧ L OAD(l, v) ∧ N O P REEMPT(l, s)
     a) N O P REEMPT: The relation means s1 cannot preempt
s2 , where s1 and s2 are instructions in separate interrupt              B. The Running Examples
handlers. From the interleaving semantics of interrupts, we                 To help understand how M UST N OT R EAD F ROM is deduced
know a handler may only be preempted by another handler                  from the Datalog rules and facts, we provide a few exam-
with a higher priority. Thus,                                            ples. For ease of comprehension, we show in Table II how
                                                                         M UST N OT R EAD F ROM may be deduced from I NTERCEPTED -
                                                                         S TORE, C OVERED L OAD and N O P REEMPT. Since all stores
 N O P REEMPT(s1 , s2 ) ← P RI(s1 , p1 ) ∧ P RI(s2 , p2 ) ∧ (p2 ≥ p1 )
                                                                         are either in or outside I NTERCEPTED S TORE, and all loads
Here, P RI(s1 , p1 ) means s1 belongs to a handler with priority         are either in or outside C OVERED L OAD, our rules capture the
p1 , and P RI(s2 , p2 ) means s2 belongs to a handler with priority      M UST N OT R EAD F ROM relation between all stores and loads.
p2 . If p1 is not higher than p2 , then s1 cannot preempt s2 .
                                                                                                       TABLE II
     b) C OVERED L OAD: The relation means a load l of a                      M UST N OT R EAD F ROM RULES BASED ON I NTERCEPTED S TORE ,
                                                                                             C OVERED L OAD AND P RIORITY
variable v is covered by a store s to v inside the same interrupt
handler; this is the case when s occurs before l along all                                         I NTERCEPTED S TORE(s)         N OT I NTERCEPTED S TORE(s)
program paths. This is captured by the dominance relation in              C OVERED L OAD(l)        M UST N OT R EAD F ROM(l, s)   1) Not N O P REEMPT(s, l) →
the corresponding control flow graph:                                                                                             Possibly R EAD F ROM(l, s)
                                                                                                                                  2) N O P REEMPT(s, l) →
                                                                                                                                  M UST N OT R EAD F ROM(l, s)
                                                                          N OT C OVERED L OAD(l)   1) N O P REEMPT(l, s) →        Possibly R EAD F ROM(l, s)
                                                                                                   M UST N OT R EAD F ROM(l, s)
   C OVERED L OAD(l) ← L OAD(l, v) ∧ S TORE(s, v) ∧ D OM(s, l)                                     2) Not N O P REEMPT(l, s) →
                                                                                                   Possibly R EAD F ROM(l, s)

    c) I NTERCEPTED S TORE: The relation is similar to C OV-
ERED L OAD. We say a store s1 is intercepted by another store s2            Specifically, if a store s is I NTERCEPTED S TORE and a load
if s2 occurs after s1 along all program paths in the same handler.       l is C OVERED L OAD, there is no way for the load to read from
Intuitively, the value written by s1 is always overwritten by s2         the store (Row 2 and Column 2).
before the handler terminates. Formally,                                    If a load l is not C OVERED L OAD and a store s is not
                                                                         I NTERCEPTED S TORE, the load may read from the store by
       I NTERCEPTED S TORE(s1 ) ← S TORE(s1 , v) ∧ S TORE(s2 , v)
                                                                         running sequentially or via preemption (Row 3 and Column
                                          ∧ P OST D OM(s2 , s1 )
                                                                         3).
                                                                            If a load l is C OVERED L OAD, a store s is not I NTER -
   Finally, the M UST N OT R EAD F ROM relation is deduced               CEPTED S TORE and the handler of the store can preempt the
using all aforementioned relations including N O P REEMPT,               handler of the load, the load may read from the store through
C OVERED L OAD and I NTERCEPTED S TORE. It indicates that,               preemption (the first case at Row 2 and Column 3). However,
under the current situation (defined by the set of existing store-       if the handler of the store cannot preempt the handler of the
to-load data flows), a load l cannot read from a store s in any          load, it is impossible for the load to read from the store; in
feasible interleaving. There are several cases:                          this case, the load always reads from the store in the same
   First, we say a load l covered by a store in a handler I              interrupt handler (the second case at Row 2 and Column 3).
cannot read from a store s intercepted by another store in a                Lastly, if a load l is not C OVERED L OAD, a store s is
handler I 0 , because l cannot read from s using any preemption          I NTERCEPTED S TORE, and the handler of the load cannot
or by running I and I 0 sequentially.                                    preempt the handler of the store, the load cannot read from
the store since the value of the store is always overwritten by       Algorithm 3 Analysis of the entire program (cf. Alg. 2).
another store in the same handler (the first case at Row 3 and        10: function I NTERF(T = hN, n0 , δi, T 0 = hN 0 , n00 , δ 0 i, S)
Column 2). However, if the handler of the load can preempt            11: I ← ∅
the handler of the store, then the load can read from the store       12: for all n ∈ N do
                                                                      13:     if n is a shared memory write to variable v then
through preemption in between two stores (the second case at          14:        I(v) ← I(v) ] {(n, TFUNC(n, S (n))}
Row 3 and Column 2).                                                  15:   return I

      irq0() { irq1() {                 irq0() { irq1() {
       store(x) store(x)                 store(x) ...                 Algorithm 4 Analysis of a single interrupt (cf. Alg. 1).
       load(x)  store(x)                 load(x)  store(x)             1: function A NALYZE L OCAL(T = hN, n0 , δi, I)
      }           }                     }            }                           ...
                                                                       6:   if n is aFshared-memory read of variable v then
   (a) C OVERED L OAD & I NTER -     (b) C OVERED L OAD & Not I N -
                                                                       7:      i ← {n | (st, s) ∈ I(v) ∧ ¬M UST N OT R EAD F ROM(l, st)}
   CEPTED S TORE                     TERCEPTED S TORE
                                                                       8:      s ← TFUNC(n, S(n) t i)
      irq0() {    irq1() {              irq0() {     irq1() {          9:   else
       ...         store(x)              ...          ...             10:      s ← TFUNC(n, S(n))
       load(x)     store(x)              load(x)      store(x)                   ...
      }           }                     }            }
   (c) Not C OVERED L OAD & I N -    (d) Not C OVERED L OAD & Not
   TERCEPTED S TORE                  I NTERCEPTED S TORE              attempt to identify all the infeasible pairs because the goal
                                                                      here is to quickly identify some infeasible pairs and skip them
              Fig. 7. Examples for each case in Table II.             during the more expensive abstract interpretation computation.
                                                                        Theorem 2: Whenever M UST N OT R EAD F ROM(l, s) holds,
   Fig. 7 shows concrete examples of the four cases presented
                                                                      the load l cannot read from the store s on any concrete
in Table II, where the figures correspond to the cases.
                                                                      execution of the program.
   Fig. 7(a) represents the case at Row 2 and Column 2 in
Table II and Fig. 7(b) represents the case at Row 2 and Column           The soundness of our analysis as stated above can be
3. In both programs, only the interference between bold-style         established in two steps. First, assume that each individual
statements are considered.                                            rule is correct, the composition is also correct. Second, while
   Fig. 7(a) shows an interference between C OVERED L OAD             presenting these rules, we have sketched the intuition behind
and I NTERCEPTED S TORE. Since the load in irq0 is always             the correctness of each rule. A more rigorous proof can be
overwritten by another store in it and a value of the first store     formulated via proof-by-contradiction in a straightforward
in irq1 is always updated by a store in it, the load cannot read      fashion, which we omit for brevity.
a value from the store by preemption or running sequentially.
                                                                                  V. T HE OVERALL A NALYSIS P ROCEDURE
   Fig. 7(b) shows an interference between C OVERED L OAD and
not I NTERCEPTED S TORE. In this case, if irq1 can preempt           We now explain how to integrate the feasibility checking
irq0, then the store from irq1 can occur between the store        technique into the overall procedure for iterative analysis, which
and the load in irq0. Otherwise, the load from irq0 cannot        leverages the M UST N OT R EAD F ROM relation to improve perfor-
read a value from the store from irq1.                            mance. Specifically, when analyzing each interrupt handler T ,
   Fig. 7(c) shows an interference between not C OVERED L OAD     we filter out any interfering stores from other interrupt handlers
and I NTERCEPTED S TORE. Similarly, if irq0 can preempt           that are deemed infeasible, thereby preventing their visibility
irq1, the load from irq0 can occur between the two stores         to T . This can be implemented in Algorithm 2 by modifying
from irq1. Thus, it is possible for the load to read a value      the function I NTERF, as well as the function A NALYZE L OCAL
from the first store in irq1. Otherwise, the load cannot read     defined in Algorithm 1.
a value from the store by preemption of irq1 or running              Our modifications to I NTERF are shown in Algorithm 3.
sequentially.                                                     That is, when computing the interferences of T , we choose to
   Fig. 7(d) shows an interference between not C OVERED L OAD     create a set of store–state pairs, instead of eagerly joining all
and not I NTERCEPTED S TORE. Here, the load in irq0 can           these states. By delaying the join of these states, we obtain
read a value from the store in irq1 by running sequentially       the opportunity to filter out the infeasible store-to-load pair
or through preemption. Therefore, it is possible for the load to  individually. For this reason, we overload the definition of ]
read a value from the store as described at Row 3 and Column      to be the join (t) of sets on matching variables.
3 in Table II.                                                       Next, we modify the abstract interpretation procedure for a
   To sum up, we can use the three inference rules to determine   single interrupt handler as shown in Algorithm 4. The process
infeasible store-to-load pairs for all these cases.               remains the same as A NALYZE L OCAL of Algorithm 1 except
                                                                  that, when a load l is encountered (Line 6), we join the state
C. Soundness of the Analysis                                      from all interfering stores while removing any that must not
   By soundness, we mean the M UST N OT R EAD F ROM rela- interfere with l, as determined by the M UST N OT R EAD F ROM
tion deduced from the Datalog facts and rules is an under- relation (Line 7).
approximation. That is, any pair (l, s) of load and store in this    The remainder of the modular analysis remains the same as
relation is guaranteed to be infeasible. However, we do not in Algorithm 2.
                                                                                           TABLE III
      irq0() {                        irq1() {
                                        while(...) {
                                                                    B ENCHMARK PROGRAMS USED IN OUR EXPERIMENTAL EVALUATION .
          b = x;                          x = 1;
                                          x = 0;                   Name     Description
          assert(b == 0);
                                       }                           test     Small programs created to conduct the sanity check of IntAbs’s
      }                                                                     handling of various interrupt semantics.
                                      }
                                                                   logger   Programs that model parts of the firmware of a temperature logging
                                                                            device from a major industrial enterprise. There are two major interrupt
                   Fig. 8. A small example with a loop.                     handlers: one for measurement and the other for communication.
                                                                   blink    Programs that control LED lights connected to the MSP430 hardware,
                                                                            to check the timer values and change LED blinking based on the timer
                                                                            values.
   For example, in Fig. 7(a), existing thread-modular abstract      brake   Programs generated from the Matlab/Simulink model of a brake-by-
interpretation methods would consider the two stores from                   wire system from Volvo Technology AB, consisting of a main interrupt
irq1 for the load of x in irq0. In contrast, we use                         handler and four other handlers for computing the braking torque based
                                                                            on the speed of each wheel.
Algorithm 4 to remove the pairing of the load in irq0 and           usbmouseUSB mouse driver from the Linux kernel, consisting of the device
the first store in irq1, since the load and the store satisfy the           open, probe, and disconnect tasks with interrupt handlers.
                                                                    usbkbd  USB keyboard driver from the Linux kernel, consisting of the device
M UST N OT R EAD F ROM relation. Similarly, the pairing of the              open, probe, and disconnect tasks with interrupt handlers.
load of x in irq0 and the store of x in irq1 is filtered out        rgbled  USB RGB LED driver from the Linux kernel. We use initialization
                                                                            of led and rgb functions and the led probe function, and check the
when irq1’s priority is not higher than irq0’s priority as                  consistency of the led and rgb device values using interrupts.
shown in Fig. 7(b).                                                 rcmain  Linux device driver for a remote controller core, including operations
                                                                            such as device register, free, check the device information, and update
   Our method can handle programs with loops. Fig. 8 shows                  protocol values. We check the consistency of the device information
an example, which has two interrupt handlers where irq1 has                 and protocol values using several interrupt handlers.
                                                                    others  Programs collected from Linux kernel drivers for supporting hardware
higher priority than irq0. Note that irq0 loads x and stores                such as ISA boards, TCO timer for i8xx chipsets, and watch dog.
the value into b. Since x is initialized to 0, the handler checks
whether the value of b is 0. irq1 has a loop containing two
stores of x. First, it stores the value 1 and then the value 0. Toward this end, we evaluated IntAbs on 35 interrupt-driven C
Using traditional thread-modular abstract interpretation, we programs, many of which are from real applications such
would assume that x=1 and x=0 are all possible stores to the as control software, firmware, and device drivers. These
load of x in irq0. This would lead to a bogus violation of benchmark programs, together with our software tool, have
the assertion in irq0.                                            been made available online [14]. The detailed description of
   However, in our analysis, this bogus violation is avoided by each benchmark group is shown in Table III. In total, there
using the post-dominate relation between statements. Inside the are 22,541 lines of C code.
while-loop of irq1, x=0 post-dominates x=1, meaning that
x=0 always occurs after x=1. Therefore, using our Datalog A. Results
inference rules presented in the previous section, we conclude       Table IV shows the experimental results. Columns 1-4 show
that the store x=1 cannot reach the load of x in irq0. Thus, the name, the number of lines of code (LoC), the number
it is impossible for the value 1 to be stored in b and then of interrupt handlers, and the number of assertions used for
cause the assertion violation.                                    each benchmark program. Columns 5-7 show the results of
                                                                  iCBMC [18], including the number of violations detected,
                       VI. E XPERIMENTS                           the number of proofs obtained, and the total execution time.
   We have implemented IntAbs, our new abstract interpretation Columns 8-10 show the results of Miné’s abstract interpretation
framework in a static verification tool for interrupt-driven method [24], [27]. Columns 11-13 show the results of IntAbs,
C programs. It builds on a number of open-source tools our new abstract interpretation tool for interrupts.
including Clang/LLVM [1] for implementing the C front-end,           Since iCBMC conducts bounded analysis, when it detects
Apron library [16] for implementing the abstract domains, and a violation, it is guaranteed to be a real violation; however,
µZ [13] for solving the Datalog constraints. We experimentally when it does not detect any violation, the property remains
compared IntAbs with both iCBMC [18], a model checker undetermined. Furthermore, since iCBMC by default stops as
for interrupt-driven programs and the state-of-the-art thread- soon as it detects a violation, we evaluated it by repeatedly
modular abstract interpretation method by Miné [24], [27]. We removing the violated property from the program until it could
conducted our experiments on a computer with an Intel Core no longer detect any new violation. Also note that since iCBMC
i5-3337U CPU, 8 GB of RAM, and the Ubuntu 14.04 Linux requires the user to manually set up the interrupt-enabled points
operating system.                                                 as described in [18], during the experiments, we first ordered
   Our experiments were designed to answer the following the interrupts by priority and then set interrupt-enabled points
research questions:                                               at the beginning of the next interrupt handler. For example,
   • Can IntAbs prove more properties (e.g., assertions) than     given three interrupts irq_L, irq_M and irq_H, we would
      state-of-the-art techniques such as iCBMC [18] and set the enabled point of irq_L in a main function, the enabled
      Miné [24], [27]?                                           point of irq_M at the beginning of irq_L, and the enabled
   • Can IntAbs achieve the aforementioned higher accuracy        point of irq_H at the beginning of irq_M.
      while maintaining a low computational overhead?                Overall, iCBMC found 88 violations while obtaining 0 proofs.
   • Can IntAbs identify and prune away a large number of         Miné’s method, which was geared toward proving properties
      infeasible store-load pairs?                                in threads, obtained 8 proofs while reporting 254 warnings,
                                                                     TABLE IV
                    R ESULTS OF COMPARING I NTA BS WITH STATE - OF - THE - ART TECHNIQUES ON 35 INTERRUPT- DRIVEN PROGRAMS .

                                                                iCBMC [18]                        Miné [24], [27]                    intAbs (new)
    Name            LOC      Interrupts   Assertions   Violations   Proofs   Time (s)   Warnings       Proofs    Time (s)    Warnings    Proofs      Time (s)
    test1            46          2            2            0          0        0.23        1             1            0.18      0           2          0.07
    test2            65          3            3            1          0        0.55        3             0            0.05      1           2          0.06
    test3            86          4            4            1          0        0.52        4             0            0.06      2           2          0.10
    test4            56          2            2            1          0        0.52        2             0            0.04      1           1          0.05
    test5            54          2            2            1          0        1.56        2             0            0.04      1           1          0.04
    logger1          161         2            1            0          0        0.45        1             0            0.22      0           1          0.27
    logger2          183         3            3            0          0        0.50        2             1            0.29      0           3          0.39
    logger3          195         4            4            0          0        0.46        1             3            0.31      0           4          0.43
    blink1           164         3            3            1          0        0.65        3             0            0.12      2           1          0.18
    blink2           174         4            3            1          0        0.67        3             0            0.16      2           1          0.30
    blink3           194         5            4            2          0        1.14        4             0            0.25      3           1          0.46
    brake1           819         2            5            1          0        0.87        3             2            0.66      1           4          0.98
    brake2           818         3            4            3          0        2.24        4             0            1.67      3           1          1.91
    brake3           833         4            5            2          0        2.38        5             0            2.58      4           1          3.48
    usbmouse1        426         2            8            2          0        0.79        7             1            0.11      2           6          0.13
    usbmouse2        442         4           16            2          0        0.69       16             0            0.31      5          11          0.69
    usbmouse3        449         5           20           11          0        4.00       20             0            0.52     11           9          1.28
    usbkbd1          504         2            8            3          0        0.91        8             0            0.23      4           4          0.39
    usbkbd2          512         3           12            2          0        1.20       12             0            0.51      4           8          1.09
    usbkbd3          531         5           20            3          0        1.19       20             0            1.86     12           8          4.44
    rgbled1          656         2           10            5          0        0.71       10             0            0.41      5           5          0.77
    rgbled2          679         3           15            5          0        1.11       15             0            0.99      5          10          2.39
    rgbled3          701         4           20            5          0        1.07       20             0            2.18     10          10          5.68
    rcmain1         2060         3            9            0          0        5.36        9             0            1.58      0           9          1.80
    rcmain2         2088         5           15            6          0       12.39       15             0            6.93      6           9          9.46
    rcmain3         2102         6           18            9          0        3.95       18             0           12.20      9           9         16.35
    i2c pca isa 1    321         4            6            0          0        0.41        6             0            0.14      0           6          0.29
    i2c pca isa 2    341         6           10            8          0        2.24       10             0            0.36      8           2          1.05
    i2c pca isa 3    363         8           14           12          0        4.98       14             0            0.85     12           2          2.48
    i8xx tco 1      757          3           2            0           0       0.30        2              0           0.28      0           2          0.35
    i8xx tco 2      949          4           2            1           0       0.96        2              0           0.43      1           1          0.54
    i8xx tco 3      944          6           3            0           0       0.52        3              0           0.81      0           3          1.04
    wdt pci 1       1239         4            2            0          0        0.41        2             0            0.40      0           2          0.61
    wdt pci 2       1290         6            3            0          0        0.43        3             0            0.78      1           2          1.45
    wdt pci 3       1339         8            4            0          0        0.39        4             0            1.41      3           1          3.21
    Total           22,541      136          262          88          0       56.75      (254)∗          8           39.92    (118)       144         64.21
∗
    indicates the results contain bogus warnings, because the technique was designed for threads, not for interrupts.


many of which turned out to be bogus warnings. In contrast,                   procedure only has to consider the remaining 31% of the load-
our new method, IntAbs, obtained 144 proofs while reporting                   store pairs. This allows IntAbs to reach a fixed point not only
118 warnings. This is significantly more accurate than the prior              quicker but also with significantly more accurate results.
techniques.
   In terms of the execution time, IntAbs took 64 seconds,                                               VII. R ELATED W ORK
which is slightly long than the 39 seconds taken by Miné’s                      We have reviewed some of the most closely-related work. In
method and the 56 seconds taken by iCBMC.                                     addition, Miné [28] proposed an abstract interpretation based
                                                                              technique for proving the absence of data-races, deadlocks,
B. Infeasible Pairs                                                           and other runtime errors in real-time software with dynamic
   Since IntAbs removes infeasible store-load pairs during                    priorities, which is an extension of his prior work [24], [26],
the iterative analysis of individual interrupt handlers, it tends             [27] by adding priorities while targeting the OSEK/AUTOSAR
to spend extra time checking the feasibility of these data                    operating systems. Specifically, it tracks the effectiveness of
flow pairs. Nevertheless, this is the main source of accuracy                 mutex, yield and scheduler state based on execution traces
improvement of IntAbs. Thus, to understand the trade-off,                     to figure out reachability, while using priorities to make the
we have investigated, for each benchmark program, the total                   analysis more accurate. However, the technique may not be
number of store-load pairs and the number of infeasible store-                efficient in terms of memory and speed since it needs to check
load pairs identified by our technique. Table V summarizes the                all mutex, yield, and scheduler state to determine spurious
results, where Column 3 shows the total number of store-load                  interference through trace history. Furthermore, it has not been
pairs, Column 4 shows the number of infeasible pairs, and                     thoroughly evaluated on practical benchmarks.
Column 5 shows the percentage.                                                   Schwarz and Müller-Olm [34] proposed a static analysis
   Overall, our Datalog-based method for computing the                        technique for programs synchronized via the priority ceiling
M UST N OT R EAD F ROM relation helped remove 69% of the load-                protocol. The goal is to detect synchronization flaws due
store pairs, which means the subsequent abstract interpretation               to concurrency induced by interrupts, especially for data
                            TABLE V                                            invocation of interrupts randomly. Higashi and Inoue [12]
 R ESULTS OF TOTAL AND FILTERED STORE - LOAD PAIRS USING I N T A B S .         leveraged a CPU emulator to systematically trigger interrupts
                                                                               to detect data races in interrupt-driven programs. However,
  Name            LOC      # of Pairs   # of Filtered Pairs   Filtered Ratio   it may be practically infeasible to cover all interleavings of
  test1             46          1                1                100%         interrupts using this type of techniques.
  test2             65          4                2                 50%
  test3             86         16                8                 50%            Wang et al. [39], [40] proposed a hybrid approach that
  test4             56          4                3                 75%         combines static program analysis with dynamic simulation to
  test5             54          4                3                 75%         detect data races in interrupt-driven programs. Although the
  logger1          161         18                2                 11%
  logger2          183         32                6                 18%         approach is useful for detecting bugs, it cannot be used to
  logger3          195         34                6                 17%         obtain proofs, i.e., proofs that assertions always hold.
  blink1           164         19               15                 78%
  blink2           174         56               32                 57%            There are also formal verification techniques for embedded
  blink3           194        120               63                 52%         software based on model checking [11], [15], [33], [36]–[38],
  brake1           819         34               24                 70%         [44]. For example, Schlich and Brutschy [33] proposed the
  brake2           818         82               58                 70%
  brake3           833        164              128                 78%         reduction of interrupt handler points based on partial order
  usbmouse1        426         12                8                 66%         reduction when model checking embedded software. Vórtler
  usbmouse2        442        168              136                 80%
  usbmouse3        449        288              208                 72%         et al. [36] proposed, within the Contiki system, a method for
  usbkbd1          504         40               20                 50%         modeling interrupts at the level of hardware-independent C
  usbkbd2          512        120               80                 66%         source code and a new modeling approach for periodically
  usbkbd3          531        400              280                 70%
  rgbled1          656         76               38                 50%         occurring interrupts. Then, they verify programs with interrupts
  rgbled2          679        228              152                 66%         using CBMC, which is again a bounded model checker. This
  rgbled3          701        456              304                 66%
  rcmain1         2060         84               84                100%
                                                                               means the technique is also geared toward detecting bugs and
  rcmain2         2088        560              476                 85%         thus cannot prove properties. Furthermore, since it models the
  rcmain3         2102        840              714                 85%         periodical interrupt invocation only, the approach cannot deal
  i2c pca isa 1    321         33               33                100%
  i2c pca isa 2    341        210              110                 52%         with non-periodic invocations.
  i2c pca isa 3    363        434              240                 55%            Datalog-based analysis techniques have been widely used in
  i8xx tco 1      757         14               12                 85%
  i8xx tco 2      949         28               20                 74%          testing and verification [2], [7], [9], [10], [21], [23], [29], [41],
  i8xx tco 3      944         39               33                 84%          but none of the prior techniques was designed for analyzing
  wdt pci 1       1239         60               40                 66%         the interleaving behavior of interrupts. For example, Kusano
  wdt pci 2       1290        150               82                 54%
  wdt pci 3       1339        288              139                 48%         and Wang [19], [20] used Datalog to obtain flow-sensitivity
  Total           22,541     5,116            3,560               69%          in threads to improve the accuracy of thread-modular abstract
                                                                               analysis for concurrent programs. Sung et al. [35] used Datalog-
                                                                               based static analysis of HTML DOM events to speed up a
                                                                               testing tool for JavaScript based web applications. However,
races and transactional behavior of procedures. However, it                    the Datalog rules used by these prior techniques cannot be
is not a general-purpose verification procedure and cannot                     used to reason about the behavior of interrupts with priorities.
prove the validity of assertions. Regehr et al. [32] proposed
to use context-sensitive abstract interpretation of machine                                          VIII. C ONCLUSIONS
code to guarantee stack-safety for interrupt-driven programs.                     We have presented an abstract interpretation framework
Kotker and Seshia [17] extended a timing analysis procedure                    for static verification of interrupt-driven software. It first
from sequential programs to interrupt-driven programs with                     analyzes each individual handler function in isolation and then
a bounded number of context switches. As such, it does not                     propagates the results to other handler functions. To filter out
analyze all behaviors of the interrupts. Furthermore, the user                 the infeasible data flows, we have also developed a constraint-
needs to come up with a proper bound of the context switches                   based analysis of the scheduling semantics of interrupts with
and specify the arrival time for interrupts.                                   priorities. It relies on constructing and solving a system of
   Wu et al. [43] leveraged (bound) model checking tools to                    Datalog constraints to decide whether a set of data flow pairs
detect data-races in interrupt-driven programs. Kroening et                    may co-exist. We have implemented our method in a software
al. [18] also improved the CBMC bounded model checker to                       tool and evaluated it on a large set of interrupt-driven programs.
support the verification of interrupt-driven programs. However,                Our experiments show the new method not only is efficient but
they only search for a bounded number of execution steps, and                  also significantly improves the accuracy of the results compared
thus cannot prove the validity of assertions. Wu et al. [42] also              to existing techniques. More specifically, it outperformed both
proposed a source-to-source transformation technique similar                   iCBMC, a bounded model checker, and the state-of-the-art
to Regehr [31]: it sequentializes interrupt-driven programs                    abstract interpretation techniques.
before feeding them to a verification tool. However, due to the
bounded nature of the sequentialization process, the method is                                   IX. ACKNOWLEDGMENTS
only suitable for detecting violations but not for proving the                   This material is based upon research supported in part by the
absence of such violations.                                                    U.S. National Science Foundation under grants CCF-1149454
   This limitation is shared by testing methods. For example,                  and CCF-1722710 and the U.S. Office of Naval Research under
Regehr [30] proposed a testing framework that schedules the                    award number N00014-17-1-2896.
                              R EFERENCES
                                                                                 [24] Antoine Miné. Static analysis of run-time errors in embedded critical
 [1] Vikram Adve, Chris Lattner, Michael Brukman, Anand Shukla, and                   parallel C programs. In Programming Languages and Systems, pages
     Brian Gaeke. LLVA: A Low-level Virtual Instruction Set Architecture.             398–418. 2011.
     In ACM/IEEE international symposium on Microarchitecture, 2003.             [25] Antoine Miné. Static analysis by abstract interpretation of sequential
 [2] Martin Bravenboer and Yannis Smaragdakis. Strictly declarative                   and multi-thread programs. In Proc. of the 10th School of Modelling
     specification of sophisticated points-to analyses. In ACM SIGPLAN                and Verifying Parallel Processes, pages 35–48, 2012.
     Conference on Object Oriented Programming, Systems, Languages, and          [26] Antoine Miné. Static analysis of run-time errors in embedded real-time
     Applications, pages 243–262, 2009.                                               parallel C programs. Logical Methods in Computer Science, 8(1), 2012.
 [3] Doina Bucur and Marta Kwiatkowska. On software verification for sensor      [27] Antoine Miné. Relational thread-modular static value analysis by
     nodes. Journal of Systems and Software, 84(10):1693–1707, 2011.                  abstract interpretation. In International Conference on Verification, Model
 [4] E. Clarke, D. Kroening, and F. Lerda. A tool for checking ANSI-C                 Checking, and Abstract Interpretation, pages 39–58, 2014.
     programs. In International Conference on Tools and Algorithms for           [28] Antoine Miné. Static analysis of embedded real-time concurrent software
     Construction and Analysis of Systems, pages 168–176, 2004.                       with dynamic priorities. Electr. Notes Theor. Comput. Sci., 331:3–39,
 [5] Patrick Cousot and Radhia Cousot. Abstract interpretation: A unified             2017.
     lattice model for static analysis of programs by construction or approxi-   [29] Mayur Naik, Alex Aiken, and John Whaley. Effective static race detection
     mation of fixpoints. In ACM SIGACT-SIGPLAN Symposium on Principles               for Java. In ACM SIGPLAN Conference on Programming Language
     of Programming Languages, pages 238–252, 1977.                                   Design and Implementation, pages 308–319, 2006.
 [6] Patrick Cousot, Radhia Cousot, Jérôme Feret, Laurent Mauborgne,           [30] John Regehr. Random testing of interrupt-driven software. In Interna-
     Antoine Miné, David Monniaux, and Xavier Rival. The ASTREÉ                     tional Conference on Embedded Software, pages 290–298, 2005.
     analyzer. In European Symposium on Programming Languages and                [31] John Regehr and Nathan Cooprider. Interrupt verification via thread
     Systems, pages 21–30, 2005.                                                      verification. Electron. Notes Theor. Comput. Sci., 174(9):139–150, 2007.
 [7] Azadeh Farzan and Zachary Kincaid. Verification of parameterized            [32] John Regehr, Alastair Reid, and Kirk Webb. Eliminating stack overflow
     concurrent programs by modular reasoning about data and control.                 by abstract interpretation. ACM Trans. Embedded Comput. Syst., 4(4):751–
     In ACM SIGACT-SIGPLAN Symposium on Principles of Programming                     778, 2005.
     Languages, pages 297–308, 2012.                                             [33] Bastian Schlich, Thomas Noll, Jörg Brauer, and Lucas Brutschy. Re-
 [8] Jeanne Ferrante, Karl J. Ottenstein, and Joe D. Warren. The program              duction of interrupt handler executions for model checking embedded
     dependence graph and its use in optimization. ACM Transactions on                software. In Haifa Verification Conference, pages 5–20, 2009.
     Programming Languages and Systems, 9(3):319–349, July 1987.                 [34] Martin D. Schwarz, Helmut Seidl, Vesal Vojdani, Peter Lammich,
 [9] Shengjian Guo, Markus Kusano, and Chao Wang. Conc-iSE: Incremental               and Markus Müller-Olm. Static analysis of interrupt-driven programs
     symbolic execution of concurrent software. In IEEE/ACM International             synchronized via the priority ceiling protocol. In ACM SIGACT-SIGPLAN
     Conference On Automated Software Engineering, 2016.                              Symposium on Principles of Programming Languages, pages 93–104,
[10] Shengjian Guo, Markus Kusano, Chao Wang, Zijiang Yang, and Aarti                 2011.
     Gupta. Assertion guided symbolic execution of multithreaded programs.
                                                                                 [35] Chungha Sung, Markus Kusano, Nishant Sinha, and Chao Wang. Static
     In ACM SIGSOFT Symposium on Foundations of Software Engineering,
                                                                                      DOM event dependency analysis for testing web applications. In ACM
     pages 854–865, 2015.
                                                                                      SIGSOFT Symposium on Foundations of Software Engineering, pages
[11] Shengjian Guo, Meng Wu, and Chao Wang. Symbolic execution of
                                                                                      447–459, 2016.
     programmable logic controller code. In ACM SIGSOFT Symposium on
     Foundations of Software Engineering, pages 326–336, 2017.                   [36] Thilo Vórtler, Benny H’”ockner, Petra Hofstedt, and Thomas Klotz.
[12] Makoto Higashi, Tetsuo Yamamoto, Yasuhiro Hayase, Takashi Ishio, and             Formal verification of software for the Contiki operating system
     Katsuro Inoue. An effective method to control interrupt handler for data         considering interrupts. In IEEE International Symposium on Design
     race detection. In Proceedings of the 5th Workshop on Automation of              and Diagnostics of Electronic Circuits & Systems, pages 295–298, 2015.
     Software Test, pages 79–86, 2010.                                           [37] Chao Wang and Kevin Hoang. Precisely deciding control state reacha-
[13] Krystof Hoder, Nikolaj Bjørner, and Leonardo de Moura. muZ - an                  bility in concurrent traces with limited observability. In International
     efficient engine for fixed points with constraints. In International             Conference on Verification, Model Checking, and Abstract Interpretation,
     Conference on Computer Aided Verification, pages 457–462, 2011.                  pages 376–394, 2014.
[14] The intAbs tool and benchmark programs for evaluating intAbs. URL:          [38] Chao Wang, Z. Yang, Franjo Ivancic, and Aarti Gupta. Disjunctive image
     https://github.com/sch8906/intAbs.                                               computation for emebedded software verification. In Proceedings of the
[15] Franjo Ivančić, I. Shlyakhter, Aarti Gupta, M.K. Ganai, V. Kahlon, Chao        Design, Automation & Test in Europe Conference, 2006.
     Wang, and Z. Yang. Model checking C program using F-Soft. In                [39] Yu Wang, Junjing Shi, Linzhang Wang, Jianhua Zhao, and Xuandong
     International Conference on Computer Design, pages 297–308, 2005.                Li. Detecting data races in interrupt-driven programs based on static
[16] Bertrand Jeannet and Antoine Miné. Apron: A library of numerical                analysis and dynamic simulation. In Proceedings of the 7th Asia-Pacific
     abstract domains for static analysis. In International Conference on             Symposium on Internetware, pages 199–202, 2015.
     Computer Aided Verification, pages 661–667, 2009.                           [40] Yu Wang, Linzhang Wang, Tingting Yu, Jianhua Zhao, and Xuandong Li.
[17] Jonathan Kotker, Dorsa Sadigh, and Sanjit A. Seshia. Timing analysis             Automatic detection and validation of race conditions in interrupt-driven
     of interrupt-driven programs under context bounds. In International              embedded software. In International Symposium on Software Testing
     Conference on Formal Methods in Computer-Aided Design, pages 81–90,              and Analysis, pages 113–124, 2017.
     2011.                                                                       [41] John Whaley and Monica S. Lam. Cloning-based context-sensitive
[18] Daniel Kroening, Lihao Liang, Tom Melham, Peter Schrammel, and                   pointer alias analysis using binary decision diagrams. In ACM SIGPLAN
     Michael Tautschnig. Effective verification of low-level software with            Conference on Programming Language Design and Implementation,
     nested interrupts. In Proceedings of the Design, Automation & Test in            pages 131–144, 2004.
     Europe Conference, pages 229–234, 2015.                                     [42] Xueguang Wu, Liqian Chen, Antoine Miné, Wei Dong, and Ji Wang.
[19] Markus Kusano and Chao Wang. Flow-sensitive composition of thread-               Static analysis of runtime errors in interrupt-driven programs via
     modular abstract interpretation. In ACM SIGSOFT Symposium on                     sequentialization. ACM Trans. Embedded Comput. Syst., 15(4):70:1–
     Foundations of Software Engineering, pages 799–809, 2016.                        70:26, 2016.
[20] Markus J. Kusano and Chao Wang. Thread-modular static analysis for          [43] Xueguang Wu, Yanjun Wen, Liqian Chen, Wei Dong, and Ji Wang. Data
     relaxed memory models. In ACM SIGSOFT Symposium on Foundations                   race detection for interrupt-driven programs via bounded model checking.
     of Software Engineering, pages 337–348, 2017.                                    In International Conference on Software Security and Reliability, pages
[21] Monica S. Lam, John Whaley, V. Benjamin Livshits, Michael C. Martin,             204–210, 2013.
     Dzintars Avots, Michael Carbin, and Christopher Unkel. Context-sensitive    [44] Z. Yang, Chao Wang, Franjo Ivančić, and Aarti Gupta. Mixed symbolic
     program analysis as database queries. In ACM SIGACT-SIGMOD-SIGART                representations for model checking software programs. In International
     Symposium on Principles of Database Systems, pages 1–12, 2005.                   Conference on Formal Methods and Models for Codesign, pages 17–24,
[22] Leslie Lamport. Time, clocks, and the ordering of events in a distributed        2006.
     system. Commun. ACM, 21(7):558–565, 1978.                                   [45] Naling Zhang, Markus Kusano, and Chao Wang. Dynamic partial order
[23] V. Benjamin Livshits and Monica S. Lam. Finding security vulnerabilities         reduction for relaxed memory models. In ACM SIGPLAN Conference
     in Java applications with static analysis. In USENIX Security Symposium,         on Programming Language Design and Implementation, pages 250–259,
     2005.                                                                            2015.
