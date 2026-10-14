                                             Automated Verification of CountDownLatch

                                                      Wei-Ngan Chin1         Ton Chanh Le1       Shengchao Qin2
                                                                  1
                                                                      National University of Singapore
                                                                           2
                                                                             Teesside University
arXiv:1908.09758v1 [cs.PL] 26 Aug 2019




                                               Abstract. The CountDownLatch (CDL) is a versatile concurrency mech-
                                               anism that was first introduced in Java 5, and is also being adopted into
                                               C++ and C#. Its usage allows one or more threads to exchange resources
                                               and synchronize by waiting for some tasks to be completed before others
                                               can proceed. In this paper, we propose a new framework for verifying the
                                               correctness of concurrent applications that use CDLs. Our framework is
                                               built on top of two existing mechanisms, concurrent abstract predicate
                                               and fictional separation logic, with some enhancements such as borrowed
                                               heap and thread local abstraction. In addition, we propose a new incon-
                                               sistency detection mechanism based on waits-for relation to guarantee
                                               deadlock freedom. Prior concurrency verification works have mostly fo-
                                               cused on data-race freedom. As a practical proof of concept, we have
                                               implemented this new specification and verification mechanism for CDL
                                               in a new tool, called HIPCAP, on top of an existing HIP verifier. We
                                               have used this new tool to successfully verify various use cases for CDL.



                                         1   Introduction

                                         One of the most popular techniques for reasoning about concurrent programs
                                         is separation logic [25, 29]. Originally, separation logic was designed to verify
                                         heap-manipulating sequential programs, with the ability to express non-aliasing
                                         in the heap [29]. Separation logic was also extended to verify shared-memory
                                         concurrent programs, e.g. concurrent separation logic [25], where ownerships of
                                         heap objects are considered as resource, which can be shared and transferred
                                         among concurrent threads. Using fractional permissions [2, 4], one can express
                                         full ownerships for exclusive write accesses and partial ownerships for concurrent
                                         read accesses. Ownerships of stack variables could also be considered as resource
                                         and treated in the same way as heap objects [3].
                                             Most existing solutions to verify the correctness of concurrent programs have
                                         focused on simpler concurrency primitives, such as binary semaphores [25], locks
                                         [11, 12] and first-class threads [22, 10]. Lately, some solutions are beginning to
                                         emerge for more complex concurrency mechanisms, such as barriers [14] and
                                         channels [8] (using only grant/wait). The former used multiple pre/post specifi-
                                         cations for every thread at each barrier point to capture resource exchanges, but
                                         this requires some non-local reasoning over each set of multiple pre/posts. The
                                         latter relied on higher-order concurrent abstract predicates (HOCAP) to provide
abstract predicates that are stable in the presence of interfering actions from con-
current threads. However, with the unrestricted use of higher-order predicates,
some concurrent abstract predicates proposed in [8] were unsound.
    Moreover, we are not aware of any formal verification solution that have been
applied to the more versatile CountDownLatch where multiple threads could be
involved in data exchanges. One new challenge is the need to handle two different
kinds of threads namely, (i) those that perform non-blocking countdown oper-
ations, and (ii) those that perform blocking await operations. We resolve them
through two new mechanisms (i) distinct abstract predicates can semantically
distinguish producers from consumers for concurrency synchronization mecha-
nisms; (ii) inconsistency lemma that can detect deadlocks by tracking when one
CDL command is to be completed before another. On correctness guarantees, we
show how to ensure both race-freedom and deadlock-freedom. Most existing solu-
tions on concurrency verification have focused on only race-freedom, whilst some
solutions [23, 21] have been proposed for verifying deadlock-freedom, mostly in
the context of mutex locks and channels.
    Our paper makes the following technical contributions:
  – We propose the first formal verification for CountDownLatch. We use two re-
    source predicates and one counting predicate to soundly track resource
    synchronization for our concurrent programs using CountDownLatch(s).
  – We provide a modular solution to the count down mechanism by supporting
    a thread-local abstraction on top of the usual global view on its shared counter.
    While this can be viewed as an instance of fictional separation logic [31], our
    use of thread-local abstraction goes beyond that by allowing the interference
    effects of parallel threads to be modularly and precisely aggregated.
  – We provide interpretations for our abstract predicates. This involves a novel
    use of septraction operator to capture the notion of borrowed heap.
  – We highlight two desired concurrency properties (i) race-freedom, and (ii)
    deadlock-freedom, that can be ensured by formally verifying our concurrent
    abstract predicates for CountDownLatch. A novel feature is the use of incon-
    sistency lemmas to help detect concurrency errors, after they occur.
  – We provide a prototype verifier for CountDownLatch. We use it to verify several
    applications and a library implementation of the CountDownLatch.


2   Motivation for CountDownLatch

The CountDownLatch protocol is a synchronization mechanism that allows one or
more threads to wait until a certain number of operations are completed by other
threads. A CountDownLatch instance is initialized with a non-negative count. A
call of the await primitive blocks the current thread until the count of its latch
reaches zero. At that point, all waiting threads are released and any subsequent
invocation of await returns immediately. Note that the count of each latch is only
decreased by one, down to zero for each invocation of the countDown primitive
and cannot be reset. The CountDownLatch is a versatile mechanism that can be
used for some non-trivial synchronization patterns.

                                         2
                                                                      cnt=2
                                                            await()
               c = create_latch(2);                   T3             2        awaiting . . .
                                                   
  # T1            # T2            # T3                   countDown()
 # h:=hs cos θ ; # r:=hs sin θ ;                    T1             1        T1 , continue
             2               2                     
 countDown(c); countDown(c); await(c);                 countDown()
                                                      T2             0        T2 , continue
                                  # V := 13 πr 2 h;
                                                                              T3 , resume
                                                                      cnt=0
                         Fig. 1. A use-case of CountDownLatch


    Our first use-case of CountDownLatch is when a thread must wait for other
threads to complete their work, so that all resources needed for its computation
are available. As a simple example, we show a program which calculates the
volume V of a circular cone given its slant height hs and aperture θ. In this
program, the height h and the radius r of the cone are concurrently computed
by two threads T1 and T2 . When both their computations have completed, these
threads separately invoke the countDown method to inform the thread T3 , via
awaiting on the latch to reach zero, to continue its computation for V based on
h and r, as illustrated in Fig. 1.
    In the second use-case, we leverage CountDownLatch to implement a copyless
multi-cast communication pattern, where a single send is being awaited by mul-
tiple receivers. As an example, let us assume that resource P*Q1 is being sent
by a thread, which are awaited by two other threads, receiving P and Q, respec-
tively. This copyless multi-cast communication can be modeled by the following
concurrent program with a CountDownLatch initialized to 1.

                                 c = create_latch(1);
                                                                       
                    # send P*Q         await(c);        await(c);
                   countDown(c);      # receive P      # receive Q
                    ...                ...              ...

The same pattern can be used to coordinate the starting of several threads,
in which the countDown action of the first thread is a starting signal for other
awaiting threads to start at the same time.
    Last but not least, a barrier synchronization can be implemented using
CountDownLatch. As another example, consider two threads, that own P and Q
respectively, but wish to exchange their respective resources at a barrier. We
may model this scenario by using one countDown immediately followed by await,
at each of the barrier point in the two threads, as follows:

                                 c = create_latch(2);

1
    P*Q is a separation logic formula formed by separation conjunction * [16, 29].


                                            3
                                                                   
              ...                           ...
             # owns P                       # owns Q              
                                                                  
             countDown(c); await(c);       countDown(c); await(c);
                                                                  
             # owns Q                       # owns P              
              ...                           ...

   As seen with these examples, the communication patterns here are non-trivial
and we shall see how resource predicates can help us perform formal reasoning
on CountDownLatch.


3   Concurrent Abstract Predicates for CountDownLatch

In this section, we propose a set of concurrent abstract predicates that can be
used to formally model the CountDownLatch. Apart from allowing its resources to
be more precisely tracked,another key challenge faced by the CountDownLatch
concurrency protocol is the ability to support thread modular reasoning for
its shared counter. We introduce two resource predicates LatchIn(c, P) and
LatchOut(c, P) to help track resource P precisely, and one counting predicate
CNT(c, n) to help track countdowns. Each set of three concurrent abstract predi-
cates is created to model a CountDownLatch, as follows:
   CountDownLatch create_latch(n) with P
      requires n>0
      ensures LatchIn(res, P)*LatchOut(res, P)*CNT(res,n) 1 ;
      requires n=0
      ensures CNT(res,-1)1 ;
Note the variable res denotes the return value of the method. We used two
pre/post specifications to describe this constructor. In case n=0, the latch cannot
be used for concurrency synchronization and is simply denoted by a final state of
CNT(res, -1)ǫ to denote an expired latch whose count is definitely 0. (We attach
fractional permission ǫ to CNT to help track sharing on the CountDownLatch. Such
a scenario would allow the latch itself to be de-allocated, where desired.) In case
n>0, the resource predicates, LatchIn(c, P) and LatchOut(c, P), are used to model
the inflow and outflow, respectively, of some resource P that are being exchanged
by the CountDownLatch. Specifically, the predicate LatchIn(c, P) shall be used for
the consumption of resource P into the CountDownLatch (at countDown call), while
the predicate LatchOut(c, P) shall be used to model the production of P from the
CountDownLatch (at each await call), as shown below.
  void countDown(CountDownLatch i)         void await(CountDownLatch i)
    requires LatchIn(i, P)*P*CNT(i,n)ǫ ∧n>0 requires LatchOut(i, P)*CNT(i,0)ǫ
    ensures CNT(i,n-1)ǫ ;                    ensures P*CNT(i,-1)ǫ ;
    requires CNT(i,-1)ǫ                      requires CNT(i,-1)ǫ
    ensures CNT(i,-1)ǫ ;                     ensures CNT(i,-1)ǫ ;
     The higher-order formula P denotes the logical resource added by our spec-
ifications for CountDownLatch to support race-free resource exchanges, as the

                                        4
underlying specification of CountDownLatch is focused exclusively on its count-
down counter and the blocking effects on threads from await calls. The predicate
CNT(c, n) does not capture any resources, but is used to provide an abstract view
of the counter inside CountDownLatch. A novel feature of this CNT predicate is that
it could be used to support both a global view and a thread local view. Note
that CNT(c, n)ǫ ∧n≥0 gives a thread-local view of the counter with a value of at
least n. As a special case, CNT(c, 0)ǫ denotes a shared counter that is at least 0,
while CNT(c, -1)ǫ denotes a shared counter that is definitely 0 (i.e. the counter has
reached its final state with value 0). In order to support resource consumption by
the first pre/post specification of countDown method, we require CNT(c, n)ǫ ∧n>0
to ensure race-free synchronization.
    The following normalization rules show how multiple CNT instances are com-
bined prior to each formal reasoning step to provide a sound view of the shared
counter. The first rule shows idempotence on the final state of CNT(c, -1). The
second rule combines multiple CNT instances, where possible. The third rule al-
lows resource trapped in each latch to be released at its final state. This rule
helps preserve (or release) unconsumed resources from each expired latch.
    [NORM−1] : CNT(c, n)ǫ1 *CNT(c, -1)ǫ1 ∧n≤0−→CNT(c, -1)ǫ1 +ǫ2
    [NORM−2] : CNT(c, n1)ǫ1 *CNT(c, n2)ǫ2 ∧ n=n1+n2 ∧ n1,n2≥0−→CNT(c, n)ǫ1 +ǫ2
    [NORM−3] : LatchOut(c, P)*CNT(c, -1)ǫ −→CNT(c, -1)ǫ *P

    To support distribution to multiple concurrent threads, we provide a set of
splitting lemmas for our abstract predicates, as follows:
    [SPLIT−1] : LatchOut(i, P*Q) −→ LatchOut(i, P)*LatchOut(i, Q)
    [SPLIT−2] : LatchIn(i, P*Q) −→ LatchIn(i, P)*LatchIn(i, Q)
    [SPLIT−3] : CNT(c, n)ǫ1 +ǫ2 ∧ n1,n2≥0 ∧ n=n1+n2 −→ CNT(c, n1)ǫ1 *CNT(c, n2)ǫ2

    Our splitting process is guided by the pre-condition expected for each concur-
rent thread. This split occurs at the start of fork/par operations. For example, if
an await call is in a thread, our split will try to ensure that a suitable thread-local
state, say LatchOut(i, P)*CNT(i, 0), is passed to this thread.
    We illustrate an example in Fig. 2 where splitting lemmas allow relevant
abstract predicates to be made available for the modular verification of each
thread. For simplicity in presentation, we shall omit fractional permissions for
the CNT predicate in the rest of this paper. As such permissions must be tracked
precisely, they are always conserved by lemmas and pre/post specifications.

                        c = create_latch(2) with P*Q;
                   # LatchOut(c, P*Q)*LatchIn(c, P*Q)*CNT(c, 2)
    # LatchOut(c, P*Q)*LatchIn(c, P)*LatchIn(c, Q)*CNT(c, 0)*CNT(c, 1)*CNT(c, 1)
                                                                                    
  ···                         · · · create P · · ·        · · · create Q · · ·
# LatchOut(c, P*Q)*CNT(c, 0) # P*LatchIn(c, P)*CNT(c, 1) # Q*LatchIn(c, Q)*CNT(c, 1)
                                                                                    
await(c);                    countDown(c);               countDown(c);              
                                                                                    
# P*Q*CNT(c, -1)             # CNT(c, 0)                 # CNT(c, 0)                
  · · · use P*Q · · ·         ···                         ···

             Fig. 2. A CountDownLatch with two threads counting down


                                          5
3.1     Ensuring Race Freedom
In the CountDownLatch protocol, we expect all countDown calls that are executed
concurrently to the await calls be completed before the latter. This is important
to ensure race-freedom, since resources that are generated from countDown oper-
ations must be completed (or used), before they are transferred to threads that
are blocked by the await calls. In order to ensure this, we require the precondition
of countDown method to be either CNT(c, n)∧n>0 or CNT(c, -1), but never CNT(c, 0).
Thus, each violation on the pre-condition of countDown2 would be signaled as a
potential race problem. Another situation where race problem can occur is when
resources that are required by await calls are not being synchronized by any
countDown call. Such an example is illustrated in Fig. 3.

                          c = create_latch(1) with P*Q;
                     # LatchOut(c, P*Q)*LatchIn(c, P*Q)*CNT(c, 1)
      # LatchOut(c, P*Q)*LatchIn(c, P)*LatchIn(c, Q)*CNT(c, 0)*CNT(c, 1)*CNT(c, 0)
                                                                                    
  ···                         · · · create P · · ·        · · · create Q · · ·
# LatchOut(c, P*Q)*CNT(c, 0) # P*LatchIn(c, P)*CNT(c, 1) # Q*LatchIn(c, Q)*CNT(c, 0)
                                                                                    
 await(c);                   countDown(c);               skip();                    
                                                                                    
# P*Q*CNT(c, -1)             # CNT(c, 0)                 # Q*LatchIn(c, Q)*CNT(c, 0)
  · · · use P*Q · · ·         ···                         ···

                # P*Q*CNT(c, -1) *CNT(c, 0) *Q*LatchIn(c, Q)*CNT(c, 0)
                         # P*Q*CNT(c, -1) *Q*LatchIn(c, Q)
                       # RACE-ERROR detected by [ERR−1]

                      Fig. 3. A CountDownLatch with a race error

    The third thread has the resource Q generated there but was not being syn-
chronized by any countDown call. As a consequence, Q was not properly trans-
ferred to its corresponding await call. We propose to detect such potential race
violations through the following inconsistency lemma:
    [ERR−1]: LatchIn(c, P)*CNT(c,-1) −→ RACE-ERROR
    The formula LatchIn(c, P)*CNT(c, -1) denotes a contradiction. The former pred-
icate requires the shared counter to be non-zero, while latter predicate is in a
final state with value 0 (see Sec B). Such contradictions are manifestations of
some concurrency synchronization errors. We identify this as a race problem.
3.2     Ensuring Deadlock Freedom
Deadlock may occur when blocking operations, such as await, are invoked and
then could wait forever, e.g., due to the shared counter never reaching zero.
   For a single CountDownLatch, this deadlock error can be signified by the fol-
lowing lemma:
   [ERR−2]: CNT(c,a)*CNT(c,-1)∧ a>0 −→ DEADLOCK-ERROR
Here, CNT(c, a)∧a>0 denotes a counter value of at least 1, while CNT(c, −1) denotes
2
    This violation occurs when skip() in the third thread of the example in Fig. 3 is
    replaced by countDown(c).


                                           6
a final counter with value 0. Such a contradiction is a manifestation of a deadlock
error which arose from the unreachability on precondition CNT(c, 0) ∨ CNT(c, -1)
that we impose on the await method. A simple example of this deadlock scenario
(omitting Latch predicates) is shown in Fig 4. This deadlock error occurs due to
the first thread not invoking a sufficient number of countDown calls. This lack of
countDown calls led to an error scenario when the conflicting states from the two
threads are being joined.
                                                For multiple latches, we will need
          c = create_latch(2);
                                            to track a wait-for graph [32], to help
  # CNT(c,2) −→ CNT(c,2)*CNT(c,0)
                                          detect deadlocks, where possible. Let
     # CNT(c,2)         # CNT(c,0)          us introduce a WAIT (S)ǫ relation that
   countDown(c);       await(c);  ;       is tracked inter-procedurally with its
     # CNT(c,1)         # CNT(c,-1)         wait-for graph S and its permission ǫ.
          # CNT(c,1)*CNT(c,-1)              Whenever we have a complete view of
# DEADLOCK-ERROR detected by [ERR−2] the waits-for relation (with full permis-
                                            sion, denoted as WAIT (S)1 ), we can al-
    Fig. 4. An intra deadlock scenario
                                            ways reset each acyclic wait-for graph
to {}, as follows: [WAIT−1]: WAIT (S)1 ∧¬isCyclic(S)−→ WAIT ({})1
Note that isCyclic(S) returns true when the wait-for graph S contains a cycle.
We add a wait-for arc via this lemma:
     [WAIT−2]: CNT(c1, a)*CNT(c2 , −1)* WAIT (S)ǫ ∧a>0 −→
                   CNT(c1, a)*CNT(c2 , −1)∧a>0 * WAIT (S∪{c2 →c1 })ǫ
An arc c2 →c1 is added into the WAIT relation to indicate that (the counting down
on) c2 will be completed before the CountDownLatch c1 or in other words, c1 is
waiting for c2 to complete. The wait-for predicates are split/normalized by:
     [WAIT−3]: WAIT (S1 )ǫ1 * WAIT (S2 )ǫ2 ←→ WAIT (S1 ∪S2 )ǫ1 +ǫ2
     We normalize where possible, and split the WAIT relation at fork/par locations.
Moreover, any occurrence of a cycle in the wait-for graph is immediately detected
as a potential deadlock by the following inconsistency lemma:
     [ERR−3]: WAIT (S)ǫ ∧ isCyclic(S) −→ DEADLOCK-ERROR
An example of deadlock detection for multiple latches is shown in Fig 5 where
the deadlock is detected by the cycle in WAIT ({c2→c1, c1→c2}).
                                                                Though deadlock de-
    c1 = create_latch(1); c2 = create_latch(1);            tection for locks and
       # WAIT ({})1 *CNT(c1,1) * CNT(c2,1) −→              channels have been pro-
# CNT(c1,1) * CNT(c2,0) * CNT(c2,1) * CNT(c1,0)            posed before [23], there
                                                           are at least two novel
                                                      
   # CNT(c1,1)*CNT(c2,0)       # CNT(c2,1)*CNT(c1,0)
 await(c2);                   await(c1);               ideas in our proposal.
                                                      
 # CNT(c1,1)*CNT(c2,-1) # CNT(c2,1)*CNT(c1,-1)  Firstly, we have now
                                                      
#      *WAIT ({c2→c1})ǫ1      #   *WAIT ({c1→c2})ǫ2 
                                                       shown how to formally
 countDown(c1);               countDown(c2);           ensure deadlock-freedom
                                                       

 # CNT(c1,0)*CNT(c2,-1) # CNT(c2,0)*CNT(c1,-1) 
                                                           for the more complex
   #    *WAIT ({c2→c1})ǫ1      #   *WAIT ({c1→c2})ǫ2
                                                           CountDownLatch protocol.
#     CNT(c1,-1)*CNT(c2,-1)*WAIT ({c2→c1, c1→c2})1 Sec-
       # DEADLOCK-ERROR detected by [ERR−3]                ondly, we have achieved
                                                           this through the use of
      Fig. 5. An example of inter-latch deadlock

                                         7
inconsistency lemmas. The wait-for arcs added are used for inconsistency de-
tection, since each arc c2 →c1 denotes a strict completion ordering c2 <c1 (for a
pair of latches) that is to be expected from its concurrent execution. Any cycle
from such an accumulated waits-for ordering denotes potential unsatisfiability.


3.3     Interpretations for Abstract Predicates

We have introduced three concurrent abstract predicates, namely LatchIn(c, P),
LatchOut(c, P) and CNT(c, n), for the specification of CountDownLatch. The first
two predicates are concerned with managing the flows of resource P through its
CountDownLatch. We can provide the following interpretations for them:
                     def
    LatchOut(i, P) = i7→0 −→ P
                   def
    LatchIn(i, P) = (P--⊛emp) * [DEC]ǫ * i7→m ∧m>0
    Each formula i7→m denotes a shared global location, while i7→m denotes
a fully-owned heap (local) location. Predicate LatchOut(i, P) is itself a pro-
ducer of resource P that is released once shared global counter becomes 0.
For the LatchIn(i, P) predicate, we use P--⊛emp with a septraction operator --⊛
([35]) to capture the consumption of resource P into the CountDownLatch via its
countDown(i) method. Unlike the septraction operator in [35] which works with
real heaps, our formula P--⊛emp is an extension to capture the concept of vir-
tual heap that denotes a borrowing of heap P. For example, (x7→_)--⊛emp is a
borrowing of (x7→_) such that ∀Q·(Q--⊛emp)*Q = emp. This simple (but novel) con-
cept allows us to capture notion of resource flows through the CountDownLatch.
The LatchIn(i, P) predicate also captures a partial permission for DEC action that
causes its shared global counter i7→m to be decreased by 1, as captured by:
    DEC : i7→n ∧ n>0     i7→n-1
    To support local reasoning with updates, we propose a thread-local view for
global counters based on fictional separation logic [18]. We introduce a new
thread-local formula {|i7→n|} to denote a shared counter whose value is at least n.
Such a thread-local abstraction is related to its global counter by the property:
    {|i7→n|} −→ i7→m ∧m≥n≥0
    While the formula i7→m provides a precise view of some shared global loca-
tion, the thread-local formula {|i7→m|}ǫ provides a fictional thread-local view of
the same counter that could be separately updated by each thread. This applies
even if fractional permission is being imposed for the thread-local predicate, as
long as such predicates can be shown to be stable.
   To support concurrency, we provide combine/split operations that can be
used to precisely handle multiple thread-local states from concurrent threads.
      {|i7→n|}ǫ1 +ǫ2 ∧a,b≥0∧n=a+b ←→ {|i7→a|}ǫ1 *{|i7→b|}ǫ2
Contrast this to the global view of a shared counter with trivial property:
      i7→a * i7→b ←→ i7→a ∧a=b
      With these two views, we provide the following intepretation for CNT(i, n):
               def
      CNT(i, n) = {|i7→n|}∧n≥0 ∨ i7→0 ∧n=-1
   To confirm soundness, we must determine that all three concurrent abstract
predicates are stable in the presence of interferring actions. Our use of {|i7→n|}

                                            8
remains stable since it is based on fictional separation logic, whose effect is not
affected by other concurrent threads. The shared global state i7→0 is stable,
since DEC operation does not modify such a final state of the shared counter.
The condition i7→m ∧m>0 of the shared global state in LatchIn(i, P) is stable
since it is always used with CNT(i, n) in the pre-condition of countDown method,
which results in i7→m ∧m>0*{|i7→n|}∧n>0. By itself the global view i7→m ∧m>0
would not be stable in the presence of concurrent [DEC]ǫ . However, the com-
bined state i7→m ∧m>0*{|i7→n|}∧n>0 remains stable since the thread-local view
of {|i7→n|}∧n>0 is not affected by [DEC]ǫ operations from other threads. Thus,
 i7→m ∧m>0 always hold since m≥n. Lastly, LatchOut(i, P) is also stable since it
only depends on a stable global formula i7→0 with final value 0.
    Comparing with Fictional Separation Logic Our use of thread-local
abstraction {|i7→n|}1 (equivalent to i7→n ) is an orthogonal enhancement for
fictional separation logic [18]. Though fictional abstraction can be used to rea-
son separately about updates to a shared resource amongst concurrent threads,
this abstraction is not truly thread-local since its split/aggregate rule does not
allow effects from strong-updates to be precisely propagated amongst concurrent
threads. For example, consider the monotonic (increasing) counter from [27].
Though fictional abstraction has the following split/aggregate rule to duplicate
or merge the predicate MC(c, i) of a monotonic counter c
    ∀i≤j · MC(c, j)e1+e2 ←→ MC(c, j)e1 *MC(c, i)e2
we do not consider it to be thread-local since each predicate in this rule may not
maintain a precise view of the shared global counter. Therefore, any update on a
predicate via local reasoning may cause other copies to become weaker. To make
this abstraction thread-local, we will need to utilize the following conversion:
   MC(c, n)1 ∧j≤n ←→ {|c7→n|}1 *MC′ (c, j)1
Here, {|c7→n|} is our precise thread-local abstraction, while MC’(c, j) is the mono-
tonic counter proposed from [18]. Adding such a thread-local abstraction permits
strong updates to be precisely tracked across concurrent threads.


4    Formalism of Language and Logic
                                                            We use the core lan-
 Prog ::= datat proc                                    guage in Fig. 6 to for-
 datat ::= data C { t f }                               malise our reasoning
 proc ::= t pn(t v) spec { e }                          with CountDownLatch. A
 spec ::= requires Φpr ensures Φpo ;                    program consists of data
   t ::= void | int | bool | CountDownLatch | C
                                                        declarations (datat), and
   e ::= v | v.f | k | new C(v) | e1 ; e2 | e1 ke2 | h ei
           create_latch(n) with κ∧π | countDown(v) |
                                                        procedure declarations
                                                        (proc). Each procedure
           await(v) | pn(v) | if v then e1 else e2 | . . .
                                                        declaration is annotated
    Fig. 6. Core Language with CountDownLatch           with   pairs of pre/post-
                                                        conditions (Φpr /Φpo ). A
(countdown) latch, created by create_latch (n), is initialized to a given count n
and can be passed in with a (logical) resource κ∧π. A countDown(v) operation
decrements the count of latch v. An await(v) operation blocks until the count

                                            9
of latch v reaches zero, after which all waiting threads are released and any sub-
sequent invocation of await returns immediately. The operation hei denotes an
atomic action. Other program constructs are standard as can be found in the
mainstream languages.


             FA Pred. rpred ::= pred R(self, V, v̄) [≡ Φ] [inv π]
                Action act ::= action
                                W         I ≡ ι1 ∧π1          ι2 ∧π2
         Disj. formula    Φ ::= (∃v̄ · η*κ∧π)
        Non-Resource      η ::= [I]ξ | WAIT ({v1 →v2 })ξ | v7→C(v̄) | η1 *η2
         Sep. formula     κ ::= ι | V | R(v, Φf , v̄) | κ1 *κ2
          Simple heap     ι ::= emp | v 7−
                                         → C(v̄) | {|v7→C(v̄)|} | ι1 *ι2
                 Perms    ξ ::= ǫ | 1
         Pure formula     π ::= α | π1 ∧π2 | π1 ∨π2 | ¬π | ∃v·π | ∀v·π
        Arith. formula    α ::= αt1 =αt2 | αt1 6=αt2 | αt1 <αt2 | αt1 ≤αt2
           Arith. term   αt ::= k | v | k × αt | αt1 + αt2 | −αt
         k∈integer constants v∈variables, v̄ ≡ v1 , .., vn C∈data names
         V∈resource variables R∈resource pred. names ǫ ∈ (0, 1]

                       Fig. 7. Core Specification Language


   Fig. 7 shows our specification language for concurrent programs supporting
CountDownLatch’s abstract resource predicates. A classical separation logic for-
mula Φ is in disjunctive normal form. Each disjunct in Φ consists of formulae
η, κ and π. A pure formula π includes standard equality/inequality and Pres-
burger arithmetic. π could also be extended to include other constraints such
as set constraints. The non-resource formula η may comprise action permission
assertions [I]ξ , (permission annotated) WAIT relations, or global views on shared
states v7→C(v̄) . The heap formula κ can be formed by simple heaps ι, resource
variables V, resource predicate instances R(x, Φf , v̄), or via separation conjunc-
tion * ([16, 29]). Note that a resource variable V is a place holder for a formula
Φf , used in a resource predicate declaration, while a resource predicate instance
R(x, Φf , v̄) encapsulates resources (Φf ) that are accessible via x. For precision
reasons, these resources are restricted to local entities that can be tracked pre-
cisely, such as heap nodes or abstract predicates, but must not include global
shared locations or WAIT relations. A simple heap ι is formed by data nodes
v 7−
   → C(v̄) (which can also appear in a thread-local view {|v7→C(v̄)|}).
     To allow us to focus on the essential issues, we include limited support on
permissions (namely on actions and WAIT relations) in our logic, but this aspect
can be relaxed to support more features of CSL [1]. Furthermore, instances of
WAIT relations are only permitted in pre/post specifications (and not in predicate
definitions). This is to allow every potential race/deadlock errors to be detected
by our lemmas, whenever it might occur. Note also that, different from CAP [7]
where each action is annotated with a region, for simplicity we do not explicitly
mention regions in our action definition and the shared region to be updated by
an action can be recovered from the root pointers in the action specification.

                                         10
5    Automated Verification

Our verification system is built on top of entailment checking:
                                    ∆A ⊢E ∆C ❀ (D, ∆R )
This entailment checks if antecedent ∆A is precise enough to imply consequent
∆C , and computes the residue ∆R for the next program state and resource
bindings D. D is a set of pairs (V, ΦV ) where V is a resource variable with its
definition ΦV . E is a set of existentially quantified variables from the consequent.
This entailment procedure is used for pre-condition and post-condition checking.
It is also used by assertion checking during automated verification.
    In this section, we focus on the main entailment rules for manipulating re-
source predicates. The rest of the entailment rules, such as those for manipulating
normal data predicates or those for combining/normalizing resource predicates
using lemmas introduced in Sec 3, are given in [5]. Note that for simplicity, we
omit fractional permissions from the predicates.
Resource Predicate Matching. Matching of two resource predicates
([RP−MATCH]) is the key of our approach, i.e. it allows resource predicates to
be split and identifies necessary resource bindings for later entailments. For sim-
plicity, we illustrate the rule with at most one resource per predicate and we can
handle predicates with multiple resources by splitting them.
                                         [RP−MATCH]
                  ρ = [v̄1 /v̄2 ] (V, Φ3 , ∆, b)=addVar(R(x, ρ(Φ2 ), v̄1 ))
                                  Φ1 ⊢δE∪{V} Φ3 ❀ (D, ρ1 )
          ∆1 =subst(D, κ1 ∧π1 ) ∆2 =subst(D, ∆) ∆3 =subst(D, ρ(κ2 ∧π2 ))
               ∆1 *∆2 ∧ freeEqn(ρ ∪ ρ1 , E) ⊢E−{v̄2 } ∆3 ❀ (D1 , ∆4 )
                            D2 = if b then D1 else D ∪ D1
               R(x, Φ1 , v̄1 )*κ1 ∧π1 ⊢E R(x, Φ2 , v̄2 )*κ2 ∧π2 ❀ (D2 , ∆4 )
                                       def
             addVar(R(x, V, v̄))   = (V, V, emp, false)
                                   def
             addVar(R(x, κ∧π, v̄)) = (V, κ*V∧π, R(x, V, v̄), true), fresh V

              [RP−UNIFY]                                     [RP−INST]
          D, ρ = unify(Φ1 , Φ2 )                               V∈E
          Φ1 ⊢δE Φ2 ❀ (D, ρ)                           Φ ⊢δE V ❀ ({(V, Φ)}, ∅)

    In the above [RP−MATCH] rule, we first apply the substitution ρ to unify
the components of the corresponding resource predicates in two sides of the
entailment. We then resort to an addVar method which either uses an existing
V (from the substituted RHS resource argument ρ(Φ2 )) for binding, or adds a
fresh variable to the RHS to facilitate the implicit splitting of resource predicates
(based on [SPLIT−1] and [SPLIT−2] rules). After that, we invoke a special resource
entailment Φ1 ⊢δE∪{V} Φ3 ❀ (D, ρ1 ) for resource predicate R, where the resource
variable V is added as an existential variable to discover the resource bindings D
which maps resource variables to resource predicates (if any). Note that if V is
a fresh variable, such a binding about V will not be kept in the final result. We

                                             11
also use two auxiliary functions: (i) subst for substituting a discovered resource
variable by its corresponding definition and (ii) freeEqn for transferring certain
equations (for existential variables from the consequent) to the antecedent for
subsequent entailments.
    Our resource entailment discovers resource bindings D based on classic rea-
soning (without any frame residue) via the rules [RP−UNIFY] and [RP−INST].
Given two resource formulae Φ1 and Φ2 , we first check if they are exact heaps
by the rule [RP−UNIFY] with unification where ρ is the bindings of first-order
variables. If there is any resource variable in the consequent formula, we instan-
tiate it by the rule [RP−INST] after all common heaps in both sides are unified.
An example of the combination of matching ([RP−MATCH]), followed resource
binding ([RP−INST]) is:

                    → cell(v1 )) ⊢ LatchIn(c, V) ❀ ({(V, x 7−
      LatchIn(c, x 7−                                       → cell(v1 ))}, emp)

    In many cases, resource predicates are not matched but are rather split. In
these cases, a resource predicate with remaining resources (i.e. added by addVar )
is returned. The predicate will be then added into the antecedent in the rule
[RP−MATCH]. For example:


     LatchOut(c, x 7−              → cell(v2 ))
                    → cell(v1 )*y 7−
      ⊢ LatchOut(c, x 7−                                  → cell(v2 )) ∧ v1 =v3 )
                        → cell(v3 )) ❀ (∅, LatchOut(c, y 7−

   In order to provide the most precise program states, we always perform nor-
malization after each reasoning step.


6     Prototype Implementation
We demonstrate the feasibility of our approach in supporting CountDownLatch
via concurrent abstract predicates by implementing it on top of HIP which
originally works for only sequential programs. In contrast, besides verifying
functional correctness, data-race freedom, deadlock freedom, our new implemen-
tation (called HIPCAP) is now capable of also verifying CountDownLatch and
beyond through its support for concurrent abstract predicates, shared local ab-
straction and wait-for relation. Our HIPCAP prototype implementation and a
set of verified programs (involving CountDownLatch and other concurrency mech-
anisms) are available for both online use and download.3

7     Related Work and Conclusion
Traditional works on concurrency verification such as Owicki-Gries [26] and Re-
ly/Guarantee reasoning [19] are focused on using controlled interference to for-
mally reason between each process against those that execute in the background.
Subsequent work on concurrency reasoning [25] are based mostly on race-freedom
3
    The URL is at http://loris-7.ddns.comp.nus.edu.sg/˜ project/hipcap/.


                                         12
for concurrent processes by allowing processes to share read accesses on some
locations, whilst having exclusive write accesses on others. These works were
conducted in the presence of thread fork operations [13, 10], and threads and
locks [11, 17, 23], and use reasoning machineries, such as RGSep [35], LRG [9],
CAP [7], and Views [6], but have not considered more advanced concurrency syn-
chronization, such as CountDownLatch. The closest to our work is a recent work
on barrier synchronization by Hobor and Gherghina [14] which requires extra
pre/post specifications for each thread that are involved in each barrier syn-
chronization to allow resources to be exchanged. This approach requires global
inter-thread reasoning to ensure that resources are preserved during each barrier
synchronization. In contrast, our use of flow-aware concurrent predicates (for
CountDownLatch) rely on only modular reasoning and would need a single set
of higher-order specifications for its concurrency primitives. Moreover, we also
ensure race-freedom and deadlock-freedom.
     Our resource predicates are based on Concurrent Abstract Predicates (CAP)
[7, 8, 34, 33]. The basic idea behind CAP [7] was to provide an abstraction of
possible interferences from concurrently running threads, by partitioning the
state into regions with protocols governing how the state in each region is allowed
to evolve. Dodds et al. [8] introduced a higher-order variant of CAP to give a
generic specification for a library for deterministic parallelism, making explicit
use of nested region assertions and higher-order protocols. Svendsen et al. [34]
presented a logic called Higher Order Concurrent Abstract Predicates (HOCAP),
allowing clients to refine the generic specifications of concurrent data structures.
HOCAP uses higher order (predicative) protocols to allow clients to transfer
ownership of additional resources to shared data structures.
    More recently, there have been a number of modern concurrency logics such
as iCAP [33], Iris [20], FCSL[24][30] and CoLoSL [28]. As an improved version
of [34], iCAP [33] allows the use of impredicative protocols parameterised on
arbitrary predicates and supports modular reasoning about layered and recur-
sive abstractions. Iris [20] combines partial commutative monoids (PCMs) and
invariants. Both Iris and iCAP leverage the idea of view shifts, originated by
Jacobs and Piessens [17]. FCSL [24, 30], incorporates a uniform concurrency
model, based on state-transition systems and PCMs, so as to build proofs about
concurrent libraries in a thread-local, compositional way. CoLoSL [28] allows
each thread to be verified with respect to its partial subjective view of the
global shared state, and uses overlapping conjunction [15] to reconcile the per-
missions and capabilities, residing in the shared state between concurrent threads.
Compared with these general frameworks, our abstract predicates are resource-
specific as they explicitly track resources that flow into and out of their abstrac-
tions and allow resources to be flexibly split and transferred across procedure
and thread boundaries. To deal with the shared counter mechanism, we have
now proposed a thread-local abstraction which makes it much more precise and
yet simpler to ensure stability of our concurrent abstract predicates. We have
also used inconsistency lemma support to ensure deadlock freedom and race-
freedom, and have used resource predicates to help ensure resource preservation

                                        13
– desirable properties that were not properly addressed by prior work on CAP.
In another research direction, deadlock avoidance by verification were recently
investigated for locks and channels [23, 21]. In comparison, we have provided a
new approach based on inconsistency lemma and wait-for set to ensure deadlock
freedom.
     In conclusion, we have proposed a framework to validate the correctness
of concurrent programs using CountDownLatch. We showed how to ensure race-
freedom and deadlock-freedom. To the best of our knowledge, this is the first
proposal on formal verification for the correctness of concurrent programs us-
ing CountDownLatch. We have made use of concurrent abstract predicates to
precisely track resources that are exchanged via CountDownLatch. Our proposal
allows tracked resources to be re-distributed, in support of sharing and syn-
chronization amongst a group of concurrent threads. We have also proposed
inconsistency lemmas to assist with deadlock and race detection. We have fol-
lowed the approach of [7] for verifying the correctness of an implementation for
CountDownLatch, but requires two new concepts (i) borrowed heap via P--⊛emp
whereby ∀Q·(Q--⊛emp)*Q = emp, and (ii) thread-local abstraction for precise track-
ing of shared counters. Lastly, proof of soundness of our verification framework
is still being developed. It is based the Views framework [6] for modular concur-
rency reasoning, but have to be extended to cater to several new features, namely
(i) inconsistency lemmas (ii) borrowed heap (iii) shared local abstractions, and
(iv) deadlock freedom guarantee.
Acknowledgement: We gratefully acknowledge Duy-Khanh Le who highlighted
this CountDownLatch problem to us and helped with our initial formulation based
on flow-aware predicates.


References
 1. A. Amighi, C. Haack, M. Huisman, and C. Hurlin. Permission-Based Separation
    Logic for Multithreaded Java Programs. CoRR, abs/1411.0851, 2014.
 2. R. Bornat, C. Calcagno, P. W. O’Hearn, and M. J. Parkinson. Permission Account-
    ing in Separation Logic. In POPL, 2005.
 3. R. Bornat, C. Calcagno, and H. Yang. Variables as Resource in Separation Logic.
    ENTCS, 155, 2006.
 4. J. Boyland. Checking Interference with Fractional Permissions. In SAS, 2003.
 5. W.-N. Chin, T. C. Le, and S. Qin.                     Automated Verification
    of    CountDownLatch.           Technical   report,   NUS,     February    2016.
    http://loris-7.ddns.comp.nus.edu.sg/˜ project/hipcap/hipcap-tr.pdf.
 6. T. Dinsdale-Young, L. Birkedal, P. Gardner, M. Parkinson, and H. Yang. Views:
    Compositional Reasoning for Concurrent programs. In POPL, 2013.
 7. T. Dinsdale-Young, M. Dodds, P. Gardner, M. J. Parkinson, and V. Vafeiadis.
    Concurrent abstract predicates. In ECOOP, 2010.
 8. M. Dodds, S. Jagannathan, and M. J. Parkinson. Modular reasoning for determin-
    istic parallelism. In POPL, 2011.
 9. X. Feng. Local Rely-Guarantee Reasoning. In POPL, 2009.
10. X. Feng and Z. Shao. Modular Verification of Concurrent Assembly Code with
    Dynamic Thread Creation and Termination. In ICFP, 2005.


                                        14
11. A. Gotsman, J. Berdine, B. Cook, N. Rinetzky, and M. Sagiv. Local Reasoning for
    Storable Locks and Threads. In APLAS, 2007.
12. C. Haack, M. Huisman, and C. Hurlin. Reasoning about Java’s Reentrant Locks.
    In APLAS, 2008.
13. A. Hobor. Oracle Semantics. PhD thesis, Princeton University, 2008.
14. A. Hobor and C. Gherghina. Barriers in Concurrent Separation Logic: Now With
    Tool Support! LMCS, 8(2), 2012.
15. A. Hobor and J. Villard. The ramifications of sharing in data structures. In POPL,
    2013.
16. S. S. Ishtiaq and P. W. O’Hearn. BI as an Assertion Language for Mutable Data
    Structures. In POPL, 2001.
17. B. Jacobs and F. Piessens. Expressive Modular Fine-grained Concurrency Specifi-
    cation. In POPL, 2011.
18. J. B. Jensen and L. Birkedal. Fictional Separation Logic. In ESOP, 2012.
19. C. B. Jones. Specification and Design of (Parallel) Programs. In IFIP Congress,
    1983.
20. R. Jung, D. Swasey, F. Sieczkowski, K. Svendsen, A. Turon, L. Birkedal, and
    D. Dreyer. Iris: Monoids and invariants as an orthogonal basis for concurrent
    reasoning. In POPL, 2015.
21. D.-K. Le, W.-N. Chin, and Y. M. Teo. An Expressive Framework for Verifying
    Deadlock Freedom. In ATVA, 2013.
22. K. R. M. Leino and P. Müller. A Basis for Verifying Multi-threaded Programs. In
    ESOP, 2009.
23. K. R. M. Leino, P. Müller, and J. Smans. Deadlock-Free Channels and Locks. In
    ESOP, 2010.
24. A. Nanevski, R. Ley-Wild, I. Sergey, and G. A. Delbianco. Communicating state
    transition systems for fine-grained concurrent resources. In ESOP, pages 290–310,
    2014.
25. P. W. O’Hearn. Resources, Concurrency and Local Reasoning. In CONCUR, 2004.
26. S. S. Owicki and D. Gries. Verifying Properties of Parallel Programs: an Axiomatic
    Approach. CACM, 19(5), 1976.
27. A. Pilkiewicz and F. Pottier. The essence of monotonic state. In TLDI, 2011.
28. A. Raad, J. Villard, and P. Gardner. CoLoSL: Concurrent Local Subjective Logic.
    In ESOP, 2015.
29. J. C. Reynolds. Separation Logic: A Logic for Shared Mutable Data Structures.
    In LICS, 2002.
30. I. Sergey, A. Nanevski, and A. Banerjee. Mechanized verification of fine-grained
    concurrent programs. In PLDI, 2015.
31. F. Sieczkowski, K. Svendsen, L. Birkedal, and J. Pichon-Pharabod. A separation
    logic for fictional sequential consistency. In ESOP, 2015.
32. A. Silberschatz, P. B. Galvin, and G. Gagne. Operating system concepts. Wiley,
    2013.
33. K. Svendsen and L. Birkedal. Impredicative concurrent abstract predicates. In
    ESOP, 2014.
34. K. Svendsen, L. Birkedal, and M. J. Parkinson. Modular Reasoning about Separa-
    tion of Concurrent Data Structures. In ESOP, 2013.
35. V. Vafeiadis and M. J. Parkinson. A Marriage of Rely/Guarantee and Separation
    Logic. In CONCUR, 2007.




                                         15
A     Additional Entailment Rules

Additional entailment rules are given in Fig 8.




                                               [EX−L]
                             fresh w [w/v]∆1 ⊢E ∆2 ❀ (D, ∆)
                                   ∃v·∆1 ⊢E ∆2 ❀ (D, ∆)


                                               [EX−R]
                                                                          def
                  fresh w    ∆1 ⊢E∪w [w/v]∆2 ❀ (D, ∆3 )                ∆ = ∃w·∆3
                                 ∆1 ⊢E ∃v·∆2 ❀ (D, ∆)


                                              [MATCH]
                                        ρ = [v̄1 /v̄2 ]
                   κ1 ∧π1 ∧freeEqn(ρ, E) ⊢E−{v̄2 } ρ(κ2 ∧π2 ) ❀ (D, ∆)
                   x 7−
                      → C(v̄1 )*κ1 ∧π1 ⊢E x 7−
                                             → C(v̄2 )*κ2 ∧π2 ❀ (D, ∆)


                                         [RP−COMBINE]
                    ι*κ ∧ π−→κ′ ∈ L         ρ = match(ι, R(x, Φf 1 , v̄1 ))
                             1
                      R(x, Φf , v̄1 )*κ1 ∧π1 ⊢E ρ(κ ∧ π) ❀ (D1 , ∆1 )
                             ρ(κ′ )*∆1 ⊢E κ2 ∧π2 ❀ (D2 , ∆)
                     R(x, Φf 1 , v̄1 )*κ1 ∧π1 ⊢E κ2 ∧π2 ❀ (D1 ∪ D2 , ∆)

                                                                 def
                                freeEqn([ui /vi ]n
                                                 i=1 , V) =
                let πi = (if vi ∈V then true else vi = ui ) in n
                                                              V
                                                                i=1 πi



                                                                 def
                 match(R(x1 , Φf 1 , v̄1 ), R(x2 , Φf 2 , v̄2 )) = [x1 /x2 , v̄1 /v̄2 ]


                          Fig. 8. Additional Entailment Rules




B    A Thread-Local Abstraction for CountDownLatch

We have introduced three concurrent abstract predicates, namely LatchIn(c, P),
LatchOut(c, P) and CNT(c, n), for the specification of CountDownLatch. The first
two predicates are concerned with managing the flows of resource P through its
CountDownLatch. We can provide the following interpretations for them:


                                                 16
                   def
    LatchOut(i, P) = i7→0 −→ P
                   def
    LatchIn(i, P) = (P--⊛emp) * [DEC]ǫ * i7→m ∧m>0
    Each formula i7→m denotes a shared global location, while i7→m denotes
a fully-owned heap (local) location. Predicate LatchOut(i, P) is itself a pro-
ducer of resource P that is released once shared global counter becomes 0.
For the LatchIn(i, P) predicate, we use P--⊛emp with a septraction operator --⊛
([35]) to capture the consumption of resource P into the CountDownLatch via its
countDown(i) method. Unlike the septraction operator in [35] which works with
real heaps, our formula P--⊛emp is an extension to capture the concept of vir-
tual heap that denotes a borrowing of heap P. For example, (x7→_)--⊛emp is a
borrowing of (x7→_) such that ∀Q·(Q--⊛emp)*Q = emp. This simple (but novel) con-
cept allows us to capture notion of resource flows through the CountDownLatch.
The LatchIn(i, P) predicate also captures a partial permission for DEC action that
causes its shared global counter i7→m to be decreased by 1, as captured by:
    DEC : i7→n ∧ n>0     i7→n-1
    To support local reasoning with updates, we propose a thread-local view for
global counters based on fictional separation logic [18]. We introduce a new
thread-local formula {|i7→n|} to denote a shared counter whose value is at least n.
Such a thread-local abstraction is related to its global counter by the property:
   {|i7→n|} −→ i7→m ∧m≥n≥0
    While the formula i7→m provides a precise view of some shared global loca-
tion, the thread-local formula {|i7→m|}ǫ provides a fictional thread-local view of
the same counter that could be separately updated by each thread. This applies
even if fractional permission is being imposed for the thread-local predicate, as
long as such predicates can be shown to be stable.
    To support concurrency, we provide combine/split operations that can be
used to precisely handle multiple thread-local states from concurrent threads.
   {|i7→n|}ǫ1 +ǫ2 ∧a,b≥0∧n=a+b ←→ {|i7→a|}ǫ1 *{|i7→b|}ǫ2
Contrast this to the global view of a shared counter with trivial property:
    i7→a * i7→b ←→ i7→a ∧a=b
   With these two views, we provide the following intepretation for CNT(i, n):
             def
    CNT(i, n) = {|i7→n|}∧n≥0 ∨ i7→0 ∧n=-1
    To confirm soundness, we must determine that all three concurrent abstract
predicates are stable in the presence of interferring actions. Our use of {|i7→n|}
remains stable since it is based on fictional separation logic, whose effect is not
affected by other concurrent threads. The shared global state i7→0 is stable,
since DEC operation does not modify such a final state of the shared counter.
The condition i7→m ∧m>0 of the shared global state in LatchIn(i, P) is stable
since it is always used with CNT(i, n) in the pre-condition of countDown method,
which results in i7→m ∧m>0*{|i7→n|}∧n>0. By itself the global view i7→m ∧m>0
would not be stable in the presence of concurrent [DEC]ǫ . However, the com-
bined state i7→m ∧m>0*{|i7→n|}∧n>0 remains stable since the thread-local view
of {|i7→n|}∧n>0 is not affected by [DEC]ǫ operations from other threads. Thus,
 i7→m ∧m>0 always hold since m≥n. Lastly, LatchOut(i, P) is also stable since it
only depends on a stable global formula i7→0 with final value 0.

                                         17
    Comparing with Fictional Separation Logic Our use of thread-local
abstraction {|i7→n|}1 (equivalent to i7→n ) is an orthogonal enhancement for
fictional separation logic [18]. Though fictional abstraction can be used to rea-
son separately about updates to a shared resource amongst concurrent threads,
this abstraction is not truly thread-local since its split/aggregate rule does not
allow effects from strong-updates to be precisely propagated amongst concurrent
threads. For example, consider the monotonic (increasing) counter from [27].
Though fictional abstraction has the following split/aggregate rule to duplicate
or merge the predicate MC(c, i) of a monotonic counter c
    ∀i≤j · MC(c, j)e1+e2 ←→ MC(c, j)e1 *MC(c, i)e2
we do not consider it to be thread-local since each predicate in this rule may not
maintain a precise view of the shared global counter. Therefore, any update on a
predicate via local reasoning may cause other copies to become weaker. To make
this abstraction thread-local, we will need to utilize the following conversion:
   MC(c, n)1 ∧j≤n ←→ {|c7→n|}1 *MC′ (c, j)1
Here, {|c7→n|} is our precise thread-local abstraction, while MC’(c, j) is the mono-
tonic counter proposed from [18]. Adding such a thread-local abstraction permits
strong updates to be precisely tracked across concurrent threads.


C     A Verified CountDownLatch Implementation

With the interpretations for the flow-aware predicates, we can now prove sound-
ness of our normalization, splitting and inconsistency lemmas.
   We must also verify the correctness of CountDownLatch implementation. A
more realistic implementation will make use of locks, wait and notifyAll op-
erations to implement blocking of await commands until the shared counter
reaches 0. For ease of presentation, we have used a simple version to illustrate
how thread-local abstraction was used, as shown below.
    CountDownLatch create_latch(int n) {return new CountDownLatch(n); }
    void countDown(CountDownLatch i) { h if (i.val>0) i.val = i.val-1;i }
    void await(CountDownLatch i) { while (i.val>0) skip; }



D     Proof of Lemmas for a CDL Library

With the interpretations for the flow-aware predicates, we can now prove sound-
ness of our normalization, splitting and inconsistency lemmas, as follows:

Proof ([SPLIT−1]).
                           LatchOut(i, (P*Q))
                           ⇔ i7→0 −→ (P*Q)
                           ⇔ i7→0 −→ P * i7→0 −→ Q
                           ⇔ LatchOut(i, P)*LatchOut(i, Q)


                                           18
Proof ([SPLIT−2]).
      LatchIn(i, (P*Q))
      ⇔ ((P*Q)--⊛emp)*[DEC]ǫ * i7→n ∧n>0
      ⇔ (P--⊛emp)*(Q--⊛emp)*[DEC]ǫ1 *[DEC]ǫ2 * i7→n * i7→n ∧n>0∧ǫ = ǫ1 +ǫ2
      ⇔ (P--⊛emp)*[DEC]ǫ1 * i7→n ∧n>0*(Q--⊛emp)*[DEC]ǫ2 * i7→n ∧n>0
      ⇔ LatchIn(i, P)*LatchIn(i, Q)
Proof ([SPLIT−3]).
                          CNT(i, n)∧n1,n2≥0∧n=n1+n2
                          ⇒ {|i7→n|}∧n1,n2≥0∧n=n1+n2
                          ⇒ {|i7→n1|}*{|i7→n2|}∧n1,n2≥0
                          ⇒ CNT(i, n1)*CNT(i, n2)
Proof ([NORM−1]).
               CNT(c, n)*CNT(c, -1)∧n≤0
               ⇔ ({|c7→n|}∧n≥0 ∨ c7→0 ∧n=-1)*CNT(c, -1)∧n≤0
               ⇔ ({|c7→n|}∧n=0 ∨ c7→0 ∧n=-1)*CNT(c, -1)
               ⇒ ( c7→m ∧m≥0 ∨ c7→0 ∧n=-1)* c7→0
               ⇒ c7→0
               ⇒ CNT(c, -1)
Proof ([NORM−2]).
                     CNT(c, n1)*CNT(c, n2) ∧ n=n1+n2 ∧ n1,n2≥0
                     ⇔ {|c7→n1|}*{|c7→n2|} ∧ n=n1+n2 ∧ n1,n2≥0
                     ⇔ {|c7→n|} ∧ n=n1+n2 ∧ n1,n2≥0
                     ⇒ CNT(c, n)
Proof ([NORM−3]).
                             LatchOut(c, P)*CNT(c, -1)
                             ⇔ ( c7→0 −→ P)* c7→0
                             ⇒ P* c7→0
                             ⇒ P*CNT(c, -1)
Proof ([ERR−1]).
                     LatchIn(c, P)*CNT(c,-1)
                     ⇔ (P--⊛emp)*[DEC]ǫ * c7→n ∧n>0*CNT(c,-1)
                     ⇔ (P--⊛emp)*[DEC]ǫ * c7→n ∧n>0* c7→0
                     ⇔ (P--⊛emp)*([DEC]ǫ * c7→n ∧n>0* c7→0 )
                     ⇔ (P--⊛emp)*false
                     ⇔ false //RACE-ERROR
Proof ([ERR−2]).
                           CNT(c,a)*CNT(c,-1)∧a>0
                           ⇔ {|c7→a|}*CNT(c,-1)∧a>0
                           ⇒ c7→m ∧m≥a* c7→0 ∧a>0
                           ⇒ false //DEADLOCK-ERROR
   The cycle detection lemma in [ERR−3] is a kind of contradiction detection
mechanism too, as explained in Sec 3.2.

                                        19
E    Verification Proofs for a CDL Library

For ease of presentation, we have used this simple version to illustrate how
thread-local abstraction are used. Our verification tool can automatically verify
this implementation of CountDownLatch. The detailed proof steps are re-produced
below.
    CountDownLatch create_latch(int n) with P
         requires n>0
         ensures LatchIn(res, P)*LatchOut(res, P)*CNT(res,n)
    {
        # n>0
        CountDownLatch i = new CountDownLatch(n);
        # i7→CountDownLatch(n)∧n>0
        # [DEC]1 *[KILL]1 * i7→n ∧n>0
        # [DEC]1 *{|i7→n|}* i7→n ∧n>0
        # [DEC]1 *{|i7→n|}*(P--⊛emp)*P* i7→n ∧n>0
        # (P--⊛emp)* [DEC]1 * i7→n *( i7→0 −→ P)*{|i7→n|}∧n>0
        # LatchIn(i, P)*LatchOut(i, P)*CNT(i, n)
        return i;
        # LatchIn(res, P)*LatchOut(res, P)*CNT(res, n)
    }
    CountDownLatch create_latch(int n) with P
         requires n=0
         ensures CNT(res,-1)
    {
        # n=0
        CountDownLatch i = new CountDownLatch(n);
        # i7→CountDownLatch(n)∧n=0
        # i7→n ∧n=0
        # CNT(i, -1)
        return i;
        # CNT(res, -1)
    }
    void countDown(CountDownLatch i)
          requires LatchIn(i, P)*P*CNT(i,n)∧n>0
          ensures CNT(i,n-1);
    {
        # LatchIn(i, P)*P*CNT(i,n)∧n>0
        # (P--⊛emp)*[DEC]ǫ * i7→m ∧m>0 * P * {|i7→n|} ∧n>0
        # [DEC]ǫ * i7→m ∧m>0 * {|i7→n|} ∧n>0
        h if (i.val>0) i.val=i.val-1;i
        # i7→m-1 ∧m>0 * {|i7→n-1|} ∧n>0
        # {|i7→n-1|} ∧n>0
        # CNT(i, n-1)
    }


                                       20
void countDown(CountDownLatch i)
      requires CNT(i,-1)
      ensures CNT(i,-1);
{
    # CNT(i,-1)
    # i7→0
    h if (i.val>0) i.val=i.val-1;i
    # i7→0
    # CNT(i,-1)
}
void await(CountDownLatch i)
     requires LatchOut(i, P)*CNT(i,0)
     ensures P*CNT(i,-1);
{
    # LatchOut(i, P)*CNT(i,0)
    # ( i7→0 −→ P)*{|i7→0|}
    # ( i7→0 −→ P)* i7→m ∧m≥0
    while (i.val>0) skip;
    # ( i7→0 −→ P)* i7→0
    # P*CNT(i,-1)
}
void await(CountDownLatch i)
     requires CNT(i,-1)
     ensures CNT(i,-1);
{
    # CNT(i,-1)
    # i7→0
    while (i.val>0) skip;
    # i7→0
    # CNT(i,-1)
}




                                 21
