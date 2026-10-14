                                         A flexible specification approach for verifying total
                                         correctness of fine-grained concurrent modules
arXiv:2312.15379v2 [cs.PL] 19 Dec 2024




                                         JUSTUS FASSE, KU Leuven, Belgium
                                         BART JACOBS, KU Leuven, Belgium
                                         A well-established approach to proving progress properties such as deadlock-freedom and termination is to
                                         associate obligations with threads. For example, in most existing work the proof rule for lock acquisition
                                         prescribes a standard usage protocol by burdening the acquiring thread with an obligation to release the lock.
                                         The fact that the obligation creation is hardcoded into the acquire operation, however, rules out non-standard
                                         clients e.g. where the release happens in a diﬀerent thread.
                                            We overcome this limitation by instead having the blocking operations take the obligation creation op-
                                         erations required for the speciﬁc client scenario as arguments. We dub this simple instance of higher-order
                                         programming with auxiliary code Sassy. To illustrate Sassy, we extend HeapLang, a simple, higher-order,
                                         concurrent programming language with erasable code and state. The resulting language gets stuck if no
                                         progress is made. Consequently, we can apply standard safety separation logic to compositionally reason
                                         about termination in a ﬁne-grained concurrent setting.
                                            We validated Sassy by developing (non-foundational) machine-checked proofs of representative locks—an
                                         unfair spinlock (competitive succession), a fair ticketlock (direct handoﬀ succession) and the hierarchically
                                         constructed cohortlock that is starvation-free if the underlying locks are starvation-free—against our speciﬁ-
                                         cations using an encoding of the approach in the VeriFast program veriﬁer for C and Java.

                                         1   INTRODUCTION

                                                                                          (* conﬁrm handoﬀ *)
                                                     acquire lk;                                                       acquire lk;
                                                                                          if !f then exit;
                                                     (* Critical section *)                                            (* Critical section *)
                                                                                          (* Critical section *)
                                                     f ≔ false (* handoﬀ *)                                            release lk
                                                                                          release lk

                                         Fig. 1. The lock handoﬀ between the left and middle thread is challenging for the modular verification of
                                         progress. This example reflects the key challenge also encountered when verifying a starvation-free cohort-
                                         lock. Here, we simplify the handoﬀ by “synchronizing” via the exit statement, guarded by the dereference
                                         (!) of flag f initialized to true (not shown).

                                            Consider the program in Figure 1. We consider acquire non-primitive e.g. implemented as a
                                         simple busy-waiting spinlock (Figure 2). Naturally, acquire (the spinlock module) is developed
                                         independently from speciﬁc client scenarios. It is therefore oblivious to the non-standard usage
                                         pattern by the left and middle thread: the lock acquired by the left thread is released by the middle
                                         thread. Nevertheless, termination of the right thread’s acquire crucially depends on the left and
                                         middle thread’s correct synchronization (simulated via exit). One application of this pattern are
                                         cohortlocks [Dice et al. 2012]. In a cohortlock the threads are partitioned into groups (cohorts)
                                         competing for a top-level lock. When releasing, a thread prefers passing ownership of the top-
                                         level lock directly to another member of the same cohort without calling release . Such handoﬀs
                                         are synchronized via additional per-cohort locks (see Section 9).
                                            We believe the cohortlock is a good, self-contained, benchmark for compositional total correct-
                                         ness veriﬁcation approaches. Importantly, its starvation-freedom depends both on its bounded
                                         unfairness and the starvation-freedom of the underlying locks.
                                         Authors’ addresses: Justus Fasse, KU Leuven, Department of Computer Science, Celestijnenlaan 200A box 2402, Leuven,
                                         3001, Belgium, justus.fasse@kuleuven.be; Bart Jacobs, KU Leuven, Department of Computer Science, Celestijnenlaan 200A
                                         box 2402, Leuven, 3001, Belgium, bart.jacobs@kuleuven.be.
2                                                                                       Justus Fasse and Bart Jacobs


    let acquire lk =                                           let acquire lk 𝜂 𝜅 =
      while not                                                  while not
        h if !lk then Expect lk.ob                                 h if !lk then 𝜂 ()
          else lk.ob := CreateOb CurrentThread;                      else 𝜅 ();
          CAS lk false true i                                        CAS lk false true i
      do () done                                                 do () done
    let release lk =                                           let release lk 𝜅 =
      hDestroyOb lk.ob; lk ≔ false i                             h𝜅 (); lk ≔ false i
(a) Classic obligation handling. The spinlock mod-            (b) Parameterized (Sassy) obligation handling. The
ule creates an obligation when the lock is acquired,          client controls which obligations are created when
which can only be destroyed by calling release.               acquiring the lock (𝜅) and which can be relied upon
                                                              to justify the blocking (𝜂).

Fig. 2. Spinlock implementation with two approaches to obligation-handling expressed as auxiliary (pseudo)
code. The angle brackets indicate the atomic execution of the contained expression to associate auxiliary
code with the two cases of CAS x y z (compare-and-set). If ! 𝑥 = 𝑦, CAS assigns 𝑦 to 𝑥 and return true.
Otherwise false is returned, leaving 𝑥 unchanged.


   In this paper we propose a two-step veriﬁcation approach for such programs. First, based on
the Ghost Signals constructs of Reinhard and Jacobs [2021a,b], we instrument the program-under-
veriﬁcation in a terminating (fuel-based) language with obligations-based auxiliary1 constructs to
soundly generate fuel, thereby supporting busy-waiting. In this language, inﬁnite fairly scheduled
executions are impossible (they would run out of fuel and get stuck). Consequently, proving safety
of the instrumented program establishes termination of the erased program under fair scheduling.
   Classic modular obligations-based veriﬁcation approaches for blocking programs [Kobayashi
2006; Leino et al. 2010; Boström and Müller 2015; Jacobs et al. 2018; Reinhard and Jacobs 2021a,b]
require a lock to be released by the thread that acquired it and therefore do not support the program
in Figure 1. Speciﬁcally, the acquiring thread is charged with an obligation which it can only get rid
of by releasing the lock (Figure 2a). We lift this restriction by applying the higher-order program-
ming speciﬁcation approach of Jacobs and Piessens [2011] to the problem of modularly generating
fuel. This is possible since grounding the fuel-generation in the language sidesteps the open prob-
lem of reasoning about the fair scheduling assumption in a higher-order, step-indexed, logic (see
Section 10). Concretely, when an operation’s progress depends on the client, we parameterize it
with the auxiliary function 𝜂 (e.g. Figure 2b). While blocked on the client, invoking 𝜂 must gener-
ate fuel. The other auxiliary parameter 𝜅 (Figure 2b) directly corresponds to Jacobs and Piessens
[2011]’s auxiliary parameter and permits the manipulation of auxiliary state when the operation
takes eﬀect (cf. linearization point [Herlihy and Wing 1990; Birkedal et al. 2021], see Section 4) e.g.
the moment the lock is acquired. Equipped with 𝜂 and 𝜅 it is quite simple to express the client-
dependent progress argument (see Figure 3).
   We gradually introduce Sassy, beginning with its operational perspective. First, we introduce
the fuel-based, terminating, language we use in the remainder of the paper (Section 2). Next, mod-
ular programming in this language allows us to complete the sketch of Figure 3 (Section 3).
   Afterwards, we turn towards the issue of expressive, modular speciﬁcations. We begin by re-
calling prior work on such speciﬁcations to compositionally prove partial correctness of ﬁne-
grained concurrent data structures (Section 4). The next section introduce our total correctness
speciﬁcations for unfair blocking modules (Section 5). Before deﬁning our speciﬁcations for fair
1We distinguish logic-level ghost operations and erasable auxiliary code from now on.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules          3


      acquire lk                                                                acquire lk
        (𝝀. (* expect o2 *))                                                      (𝝀. (* expect o1 *))
        (𝝀. (* create obligation                                                  (𝝀. (* create obligation
        o1 in middle thread *));              if !f then exit;                    o2 in current thread *));
      (* Critical section *)                  (* Critical section *)            (* Critical section *)
      f ≔ false (* handoﬀ *)                  release lk                        release lk
                                                (𝝀. (* destroy o1 *))             (𝝀. (* destroy o2 *))

Fig. 3. The pieces of auxiliary code passed to acquire and release encapsulate the client-dependent part
of the progress proof: 𝜅 is executed at the point of lock acquisition/release; 𝜂 justifies acquire ’s blocking.
The left thread’s blocking is justified by obligation o2 held by the right thread; the right thread’s blocking
is justified by obligation o1 held by the middle thread. Threads must destroy their obligations before they
finish.


         𝑣, 𝑤 ∈Val ::= 𝑧 | true | false | () | ℓ | 𝑠 |                         (𝑧 ∈ Z, ℓ ∈ Loc, 𝑠 ∈ SigLoc)
                          𝝁 v f x. 𝑒 | (𝑣, 𝑤)v | . . .
          𝑒 ∈ Expr ::= 𝑣 | x | 𝑒 ⊚ 𝑒 | if 𝑒 then 𝑒 else 𝑒 | (𝑒, 𝑒)e | 𝝅 1 𝑒 | 𝝅 2 𝑒 | AllocN 𝑒 𝑒 |
                          free 𝑒 | 𝑒 ≔ 𝑒 | ! 𝑒 | CmpXchg (𝑒, 𝑒, 𝑒) | FAA 𝑒 𝑒 | let 𝑥 = 𝑒 in 𝑒 |
                          𝝁 e f x. 𝑒 | (𝑒 𝑒) | . . . |
                          h𝑒i | NewSignal 𝑒 𝑒 | SetSignal 𝑒 𝑒 | Finish | exit |
                          NewExpectPerm 𝑒 𝑒 𝑒 𝑒 | Expect 𝑒 𝑒 𝑒 | lower 𝑒 to 𝑒 times 𝑒 at 𝑒 | fork 𝑒 𝑒
                   ⊚ ::= + | − | = | . . .

Fig. 4. Syntax of HeapLang< . Diﬀerences to HeapLang are highlighted in blue and are introduced in Section 2.
We write 𝜆x. 𝑒 , 𝝁 e x. 𝑒, 𝜆. 𝑒 , 𝝁 e . 𝑒, and ref 𝑒 , AllocN 1 𝑒.


blocking modules (Section 7) we discuss modular programming of fair modules in Section 6. To
illustrate these speciﬁcations, we apply them to several case studies: an unfair spinlock, a fair tick-
etlock and the hierarchically constructed cohortlock (Section 9). Section 8 brieﬂy discusses the
non-foundational mechanization of these case studies. Lastly, we discuss related work (Section 10)
and conclude the paper (Section 11).

2 A TERMINATING LANGUAGE
In this section we present our approach, based on Ghost Signals [Reinhard and Jacobs 2021a,b], for
extending a programming language with auxiliary constructs to obtain a language that always ter-
minates under fair scheduling. The auxiliary constructs are erasable in the sense that if a program
instrumented with these constructs does not get stuck, the original program under the original lan-
guage’s semantics also terminates under fair scheduling and also does not get stuck. We present
our approach by applying it to HeapLang [Iris contributors 2024, § 12], a simple imperative lan-
guage with unstructured concurrency (fork) and a higher-order store, to obtain HeapLang< .
   The syntax, small-step semantics of our extensions, and state of HeapLang< are shown in Figs. 4,
                                                                                        −𝜃 h (𝑒 ′ , 𝜎 ′ , 𝜖)
5, and 6 respectively. The “head step” ([Iris contributors 2024, § 12]) relation (𝑒, 𝜎) →
denotes that in state 𝜎, expression 𝑒, executed by thread 𝜃 , can step to expression 𝑒 ′ with new
state 𝜎 ′ and no forked threads (𝜖). Adopting the notation of Iris’ technical documentation, we
4                                                                                       Justus Fasse and Bart Jacobs


              BetaS
                                                 0 ∈ 𝜎.CallPerms(𝜃 )
              ((𝝁 v f x. 𝑒) 𝑣 , 𝜎) →
                                   −𝜃 h (𝑒 [(𝝁 e f x. 𝑒)/f ] [𝑣/x], 𝜎 : CallPerms[𝜃 \←↪ {0}], 𝜖)

    LowerS
                                𝛿 ∈ 𝜎.CallPerms(𝜃 ′ )          𝛿′ < 𝛿        0≤𝑛
                                  ′        ′
                                     −𝜃 h (𝑒, 𝜎 : CallPerms[𝜃 \←↪ {𝛿}] [𝜃 ′ ⊎←↪[𝑛 · 𝛿 ′ ]], 𝜖)
    ( lower 𝛿 to 𝑛 times 𝛿 at 𝜃 , 𝜎) →                                   ′


    NewSignalS
                               𝑠 ∉ 𝜎.Signals         𝜎.Obligations(𝜃 ′ ) ≠ Finished
                      ′
                        −𝜃 h (𝑠, 𝜎 : Obligations[𝜃 ′ ∪←↪ {(𝑠, l)}] : Signals[𝑠 ← (l, false)], 𝜖)
    ( NewSignal 𝜃 l, 𝜎) →

    SetSignalS
                           𝜎.Signals(𝑠) = (l, 𝑏)        𝜎.Obligations(𝜃 ′ ) ≠ Finished
    ( SetSignal 𝜃 ′ 𝑠, 𝜎) →
                          −𝜃 h ((), 𝜎 : Obligations[𝜃 ′ \←↪ {(𝑠, l)}] : Signals[𝑠 ← (l, true)], 𝜖)

                 AtomicBlockS
                           𝑒, 𝜎 ⇓ 𝑣, 𝜎 ′                   CurrentThreadS
                                                           ( CurrentThread, 𝜎) →
                                                                               − h (𝜃, 𝜎, 𝜖)
                                                                                    𝜃
                          −𝜃 h (𝑣, 𝜎 ′ , 𝜖)
                 (h𝑒i, 𝜎) →

             FinishS
                                       𝜎.Obligations(𝜃 ) = ∅
             ( Finish, 𝜎) →
                          −𝜃 h ((), 𝜎 : Obligations[𝜃 ← Finished], 𝜖)

NewExpectPermS
                                𝑠 ∈ 𝜎.Signals        𝛿 ∈ 𝜎.CallPerms(𝜃 ′ )         𝛿′ < 𝛿
                           ′       ′
                             −𝜃 h ((), 𝜎 : CallPerms[𝜃 \←↪ {𝛿}] : ExpectPerms[𝜃 ′ ∪←↪(𝑠, 𝛿 ′ )], 𝜖)
( NewExpectPerm 𝜃 𝑠 𝛿 𝛿 , 𝜎) →                                      ′


      ExpectS
      𝜎.Signals(𝑠) = (l, false)                l ≺ 𝜎.Obligations(𝜃 ′ )        (𝑠, 𝛿) ∈ 𝜎.ExpectPerms(𝜃 ′ )
                           ( Expect 𝜃 ′ 𝑠 𝛿, 𝜎) →
                                                −𝜃 h ((), 𝜎 : CallPerms[𝜃 ′ ⊎←↪ {𝛿}], 𝜖)

ForkS
                                         𝑠 = 𝑜.0          CP = 𝜎.CallPerms(𝜃 )
                          EP = 𝜎.ExpectPerms(𝜃 )          𝜃 ′ = min{𝜃 ′ ∈ Θ | 𝜃 ′ ∉ 𝜎.Obligations}
                                                       ( fork 𝑠 𝑒, 𝜎) →
                                                                      −𝜃 h
((), 𝜎 : Obligations[𝜃 \←↪ 𝑜] : Obligations[𝜃 ′ ← 𝑜] : CallPerms[𝜃 ′ ← CP] : ExpectPerms[𝜃 ′ ← EP],
                                          (𝜃 ′ , (𝑒; Finish)))

                 Fig. 5. HeapLang< operational semantics. l ≺ 𝑂 means ∀(𝑠, l′ ) ∈ 𝑂. l < l′ .
A flexible specification approach for verifying total correctness of fine-grained concurrent modules            5


                             
                             
                                                         fin
                                                                                                       
                                                                                                       
                             
                             
                                          Heap : Loc −⇀Val,                                            
                                                                                                       
                             
                                                                                                      
                                                                                                       
                             
                                                                                                      
                                                                                                       
                                                A        fin
                                                                                                      
                                         Heap : Loc −⇀Val
                             
                                                                                                      
                                                                                                       
                             
                                                              fin
                                       Signals : SigLoc −⇀ Lev × B                                     
                                                                                                       
                              Obligations : Θ −⇀ Multiset(SigLoc × Lev) ∪ {Finished} 
              𝜎 ∋ State ,
                                                                                     
                                               fin
                             
                                                                                     
                                                                                      
                             
                                                                                     
                                                                                      
                             
                                                                                     
                                                                                      
                                               fin
                                               −
                             
                                                   Multiset(Deg)
                                                                                      
                                 CallPerms : Θ  ⇀
                             
                              ExpectPerms : Θ −⇀ Multiset(SigLoc × Deg)              
                                                                                      
                                                                                     
                                               fin



Fig. 6. HeapLang< ’s state extends HeapLang’s state with an auxiliary heap, a signals heap mapping allocated
signal locations to their level l ∈ Lev = Val and state (unset or set), and three maps that map each live or
finished thread’s id 𝜃 ∈ Θ = N+ to the thread’s finite multiset of obligations (redundantly including each
signal’s level), its finite multiset of call permissions (each qualified by a degree 𝛿 ∈ Deg =Val), and its finite
multiset of expect permissions (each associated with a signal and a degree). The semantics is parameterized
by a well-founded order on Lev and a well-founded order on Deg. In the appendix we discuss how these can
be constructed modularly.


write 𝜎 : Heap[ℓ ← 𝑣] to designate the state identical to 𝜎 with the exception of 𝜎.Heap(ℓ) which
stores 𝑣. Moreover we use the in-place update notation 𝑚[𝜄 ⊚←↪ 𝜔] to denote 𝑚[𝜄 ← (𝑚(𝜄) ⊚ 𝜔)]
for a binary operation ⊚. We introduce the various constructs below.
   HeapLang’s sole facility for synchronization, and non-termination, are recursive function calls.
Thus the ﬁrst step to convert HeapLang into our terminating language HeapLang< is to con-
sume some (trans-)ﬁnite resource (fuel) at every function call.2 Concretely we use call permis-
sions [Jacobs et al. 2018] as fuel. Call permissions are qualiﬁed by a degree 𝛿 taken from a well-
founded universe of degrees Deg. At each function application a call permission at the dedicated,
minimal degree 0 is consumed (Figure 5, BetaS). If no call permission of degree 0 is available
the program gets stuck. The command lower 𝛿 to 𝑛 times 𝛿 ′ at 𝜃 replaces a call permission at
degree 𝛿 of thread 𝜃 with 𝑛 call permissions of of lower degree 𝛿 ′ (LowerS). Notice that despite
creating new call permissions at degree 𝛿 ′ , this command lowers the multiset of call permissions
under multiset order [Dershowitz and Manna 1979; Coupet-Grimal and Delobel 2006]. We assume
that every other degree is greater than 0 and omit the lowering to 0 if it is clear from context. Addi-
tionally, we drop the at clause if 𝜃 is the current thread. Each thread has its own call permissions.
After a fork, the forkee starts oﬀ with a stock of call permissions equal to that of the forker at
fork-time.
   Call permissions scale to sequential and non-blocking ﬁne-grained concurrent programs [Jacobs et al.
2018] but fail to address blocking concurrency. The following program illustrates the problem.
let f = ref true in fork (while !f do () done); f ≔ false
After initializing the ﬂag to true and forking, the main thread unsets the ﬂag. Meanwhile, the forkee
busy-waits until the ﬂag is unset. Under any fair scheduler the main thread will eventually unset
the ﬂag, allowing the program to terminate. Nonetheless, no amount of call permissions suﬃces
to fuel this program. Following Reinhard and Jacobs [2021b] we address this issue by generating
fuel.
   Naturally, fuel must not be generated arbitrarily. A thread may generate fuel only if some un-
set signal exists whose setting it can legitimately expect. Speciﬁcally, NewSignal 𝜃 l creates an
unset signal, returning its identiﬁer 𝑠, and assigns the obligation to set 𝑠 to thread 𝜃 (Figure 5,
NewSignalS). The obligation and signal are associated with the level l ∈ Lev (l is pronounced
2We will often write while loops, which can easily be converted into recursive functions.
6                                                                                  Justus Fasse and Bart Jacobs


Cyrillic “𝑙”), where Lev is a well-founded universe of levels that ensures acyclicity. SetSignal 𝜃 𝑠
sets 𝑠’s state to 𝑡𝑟𝑢𝑒, thus fulﬁlling (destroying) the associated obligation to set 𝑠 held by thread 𝜃 .
We omit 𝜃 if it is equal to the current thread. If a thread still has obligations when it ﬁnishes, the
program gets stuck (Figure 5, FinishS). Obligations can be passed to the forkee at thread creation
time. The division of obligations is expressed as a list of signal identiﬁers passed as extra erasable
argument to fork: fork 𝑠 𝑒.
   Finally, we need the operation that generates fuel: Expect . Consider a simpliﬁed step rule:
                        UnsoundExpect
                           𝜎.Signals(𝑠) = (l, false)           l ≺ 𝜎.Obligations(𝜃 )
                         ( Expect 𝜃 𝑠 𝛿, 𝜎) →
                                            −𝜃 h ((), 𝜎 : CallPerms[𝜃 ⊎←↪ {𝛿}], 𝜖)
If 𝑠 is unset and its level is less than those of all obligations held by 𝜃 , Expect 𝜃 s 𝛿 generates a
call permission of degree 𝛿 for 𝜃 . Once again, we omit 𝜃 if it is the current thread.
   With Expect in hand we can annotate the program with auxiliary code to fuel the busy-waiting.
let f = ref true in let s = NewSignal 0 in
fork ∅ (while h if !f then Expect s 0; !f i do () done);
f ≔ false; SetSignal s; Finish

The main thread pre-creates the signal 𝑠. At fork-time, the two auxiliary arguments express that
the main thread keeps the obligation to set 𝑠 and all its call permissions. In order to Finish 3 , it
has to set 𝑠, which it does just after unsetting the ﬂag. As a result, the Expect s in the forkee
generates the call permissions necessary to justify the busy-waiting while the main thread is (le-
gitimately) expected to set the ﬂag. We use atomic blocks—indicated via the angled brackets h𝑒i
(AtomicBlockS)—to execute Expect in the same step the ﬂag is read. In our examples atomic
blocks include exactly one real, atomic, expression. Consequently they erase to that real atomic
expression.
   This fuel-generation scheme, however, is unsound; see the appendix for a counterexample. In-
deed, it generates fuel out of thin air. We follow Reinhard and Jacobs [2021b] and force fuel-generation
to be prepaid. In addition to the acyclicity requirement already introduced, executing Expect 𝜃 s 𝛿
requires thread 𝜃 to have an expect permission for 𝑠 and 𝛿.4 NewExpectPerm 𝜃 𝑠 𝛿 ′ 𝛿 spawns this
expect permission by consuming a call permission of degree 𝛿 ′ (𝛿 < 𝛿 ′ ). If no call permission of de-
gree 𝛿 ′ is available to thread 𝜃 the program gets stuck. We write Expect s if 𝜃 is the current thread
and there is a single expect permission for signal 𝑠. Like call permissions, expect permissions are
inherited by the forkee at fork-time (ForkS). With the additional expect permission requirement
for Expect , HeapLang< is sound i.e. it does not admit inﬁnite fair executions.
  Theorem 2.1 (Absence of infinite fair executions). A HeapLang< program of the form 𝑒; Finish
does not have inﬁnite fair executions.
  Proof. See appendix. Due to the setup’s similarity, the proof is similar to that of Reinhard and Jacobs
[2021a,b].                                                                                          
   Corollary 2.2 (Safe termination). A safe HeapLang< program of the form 𝑒; Finish reduces
to a value under fair scheduling.
   Proof. By Theorem 2.1 we know that, under an arbitrary fair scheduler, HeapLang< programs
must either reduce to a value or get stuck. A safe HeapLang< program cannot get stuck by deﬁni-
tion.                                                                                        
3 The instrumented fork implicitly inserts a Finish at the end of the forkee.
4“Wait permissions” in Reinhard and Jacobs [2021b].
 A flexible specification approach for verifying total correctness of fine-grained concurrent modules                      7


  let lk = new_lock () in let f = ref true in
  let l 2 = ref 0 in let l 3 = ref 0 in lower 𝛿 1 into 4 times 𝛿 2 ; lower 𝛿 2 into 4 times 𝛿 3 ;
let started = ref false in                     if !f then exit;               let started = ref false in
acquire lk                                     (* Critical section *)         acquire lk
  (𝝀.(if not !started then                                                      (𝝀.(if not !started then
     NewExpectPerm !l 3 𝛿 2 𝛿 3 ;                                                  NewExpectPerm !l 2 𝛿 2 𝛿 3 ;
     started ≔ true);                                                              started ≔ true);
     Expect !l 3 )                                                                 Expect !l 2 )
  (𝝀.l 2 ≔ NewSignal 2 l1 );                                                    (𝝀.l 3 ≔ NewSignal l1 );
(* Critical section *)                                                        (* Critical section *)
f ≔ false                                      release lk                     release lk
                                                (𝝀.SetSignal !l 2 )             (𝝀.SetSignal !l 3 )

 Fig. 7. Safe HeapLang< program that erases to the motivating example of Figure 1, using the spinlock module
 of Fig. 2 (b). We elide the straightforward lowering of call permissions to 0 to justify function calls.


 3   MODULAR PROGRAMMING IN HEAPLANG<
 This section tackles consider the problem of modular programming in HeapLang< : given a Heap-
 Lang program consisting of multiple modules, such as the program of Fig. 1 built on top of a
 spinlock module, how can we instrument it to obtain a safe HeapLang< program, without breaking
 modularity?
    The main challenge lies in instrumenting modules that oﬀer operations whose termination de-
 pends on liveness properties of the client, such as lock modules where termination of an invoca-
 tion of acquire depends on the client eventually calling release after each conﬂicting invocation
 of acquire.
    Two approaches may generally be adopted in this case, as illustrated in Fig. 2. One approach, il-
 lustrated in Fig. 2 (a), is for the module to burden the calling thread with suﬃcient obligations such
 that suﬃcient Expect commands can be inserted into the module to fuel its busy-waiting loops.
 This yields the type of contract between module and client that has been enforced by most ex-
 isting obligations-based modular veriﬁcation approaches for blocking programs [Kobayashi 2006;
 Leino et al. 2010; Boström and Müller 2015; Jacobs et al. 2018; Reinhard and Jacobs 2021a,b]. How-
 ever, it imposes a particular usage pattern and generally rules out some subset of legitimate clients,
 such as the client of Fig. 1 and the modular construction of cohortlocks (Section 9).
    Therefore, in this paper, we propose a more ﬂexible and general approach, illustrated in Fig. 2 (b),
 where the job of generating fuel for the busy-waiting loops whose termination depends on the
 client is relegated to the client. Speciﬁcally, each operation whose termination depends on the
 client eventually performing some action takes, as an auxiliary argument 𝜂, a piece of auxiliary
 code that must produce call permissions whenever it is invoked before the client has performed
 the action. In the case of acquire, for example, 𝜂 must produce a call permission whenever it is
 invoked while the client has not invoked a release operation after a conﬂicting acquire invocation.
    This approach correspondingly also leaves it up to the client to create whatever obligations, in
 whatever threads, it needs to be able to do so. For this purpose, each module operation also takes,
 as an auxiliary argument 𝜅, a piece of auxiliary code that is invoked at the operation’s linearization
 point [Herlihy and Wing 1990].5
 5 This revives [Jacobs and Piessens 2011] which, for partial correctness veriﬁcation, has been superseded by viewshift-based

 approaches (e.g. Jung et al. [2015]).
8                                                                                 Justus Fasse and Bart Jacobs


    let x = ref 1 in                  let x = ref 1 in                      let x = ref 1 in
    let y = ref 1 in                  fork (                                fork (
    fork (1 / !y; y ≔ 0);               while not CAS x 0 1                   acquire x;
    1 / !x; x ≔ 0                       do () done;                           1 / !x; release x);
                                        1 / !x; x ≔ 0);                     1 / !x; release x
                                      1 / !x; x ≔ 0

(a) The threads work with dis-       (b) Location 𝑥 is concurrently        (c) Forker and forkee synchro-
joint state.                         accessed by both threads. The         nize the division by 𝑥’s content
                                     forkee’s division by 𝑥’s content      using a spinlock.
                                     is guarded by the busy-waiting
                                     CAS-loop

                        Fig. 8. Safe programs dividing by the value of a reference.



    Figure 7 shows how, given this parameterization of the spinlock module, the client program of
Figure 1 can be instrumented.
    First, the client sets up two auxiliary locations l2 and l3 that will store the signals whose obli-
gations will be held by threads 2 (middle) and 3 (right), respectively. Because creating an expect
permission consumes a call permission, threads 1 and 3’s 𝜂 argument to acquire only creates one
the ﬁrst time it is invoked. Thread 3 uses the 𝜅 argument to acquire to burden itself with the obli-
gation to release upon acquiring the lock. In contrast, thread 1 burdens thread 2 instead, allowing
it to ﬁnish without releasing the lock (which will happen in thread 2 instead).
    Instantiating the degrees. The example client program is parameterized by the degree 𝛿 3 of the
call permission expected by the lock module’s acquire implementation, both when it is invoked
and after it invokes its 𝜂 argument, as well as by degrees 𝛿 1 and 𝛿 2 such that 𝛿 3 < 𝛿 2 < 𝛿 1 . In the
appendix we discuss how to pick these degrees modularly.

4     BACKGROUND: PARTIAL CORRECTNESS OF POSSIBLY DIVERGING PROGRAMS
In this paper, we propose a two-step approach to modularly verify termination of busy-waiting
programs: ﬁrst, modularly instrument the program with auxiliary constructs from a terminating
language such that safety of the instrumented program implies termination under fair scheduling
of the original program; second, modularly verify safety of the instrumented program using any
existing logic for partial correctness veriﬁcation of higher-order ﬁne-grained concurrent programs.
   We show how to do the latter in Iris [Jung et al. 2015, 2016, 2018; Krebbers et al. 2017; Spies et al.
2022], a state-of-the-art logic in this category. First, this section recalls key notion of Iris to verify
partial correctness of uninstrumented ﬁne-grained concurrent programs in Iris. Beginning with
monolithic programs, this section builds up to Jung et al. [2015]’s logically atomic triples speciﬁ-
cation formalism for ﬁne-grained concurrent modules. The next section then shows how to adapt
this approach to verify instrumented programs following the programming pattern of Section 3,
yielding total correctness logically atomic triples.

4.1 Separation logic
Consider the three concurrent programs in Figure 8. We will use Iris to prove safety/partial cor-
rectness for them; in particular, that they do not divide by zero. Iris is a separation logic [Reynolds
2000; O’Hearn et al. 2001; O’Hearn 2019], a Hoare-style [Hoare 1969] logic where assertions assert
ownership of resources, in addition to asserting the truth of logical propositions.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                   9


      {True}
      let x = ref 1 in                              hoare-conseq
      {𝑥 ↦→ 1}                                      𝑃 ⇛ 𝑃′           {𝑃 ′ } 𝑒 {𝑄 ′ }    𝑄′ ⇛ 𝑄
      let y = ref 1 in
                                                                      {𝑃 } 𝑒 {𝑄 }
      {𝑥 ↦→ 1 ∗ 𝑦 ↦→ 1}
      fork (                                 points-to-exclusivity                     hoare-alloc
           {𝑦 ↦→ 1}                          ℓ ↦→ _ ∗ ℓ ↦→ _ =⇒ False                  {True} ref 𝑣 {ℓ. ℓ ↦→ 𝑣 }
           1 / !y;
           {𝑦 ↦→ 1}                                           hoare-load’
           y ≔ 0                                              {ℓ ↦→ 𝑣 } ! ℓ {𝑤 . 𝑣 = 𝑤 ∗ ℓ ↦→ 𝑣 }
           {𝑦 ↦→ 0}
                                                                                          hoare-fork
      );                                        hoare-store’                                 {𝑃 } 𝑒 {True}
      {𝑥 ↦→ 1}                                  {ℓ ↦→ 𝑣 } ℓ ≔ 𝑤 {ℓ ↦→ 𝑤 }
      1 / !x;                                                                             {𝑃 } fork 𝑒 {True}
      {𝑥 ↦→ 1}                               hoare-frame
      x ≔ 0                                       {𝑃 } 𝑒 {𝑣. 𝑄 }                hoare-def’
      {𝑥 ↦→ 0}                                                                  {𝑃 } 𝑒 {𝑄 } , (𝑃 −∗ wp 𝑒 {𝑄 })
                                             {𝑃 ∗ 𝑅} 𝑒 {𝑣. 𝑄 ∗ 𝑅}
  (a) Local reasoning about dis-
  joint state.                                                     (b) Selected reasoning rules.

Fig. 9. Separation logic enables local reasoning. The persistence modality 𝑃 expresses that 𝑃 does not assert
ownership.


  Figure 9a shows an Iris proof outline for the program in Figure 8a, constructed using the proof
rules shown in Figure 9b. The points-to assertion ℓ ↦→ 𝑣 asserts exclusive ownership of the memory
cell at location ℓ and that it currently stores the value 𝑣; the separating conjunction 𝑃 ∗ 𝑄 asserts
ownership of separate resources 𝑟 1 and 𝑟 2 such that 𝑃 holds for 𝑟 1 and 𝑄 holds for 𝑟 2 . The proof of
the fork command uses hoare-frame to frame oﬀ 𝑥 ↦→ 1 and hoare-conseq, where, as we will
see, the viewshift operator ⇛ generalizes implication.
  Iris’ Hoare triples are not primitive; rather, they are encoded in terms of its weakest precondition
wp [Dijkstra 1975], separating implication (also known as magic wand) −∗ [Ishtiaq and O’Hearn
2001] and persistence modality  [Jung et al. 2015, 2018]; see hoare-def’. wp 𝑒 {𝑄 } asserts own-
ership of suﬃcient resources to ensure expression 𝑒 executes safely and satisﬁes postcondition 𝑄;
𝑃 −∗ 𝑄 asserts ownership of some resources that, composed with any separate resources for which
𝑃 holds, satisfy 𝑄: 𝑃 ∗ (𝑃 −∗ 𝑄) ⊢ 𝑄; 𝑃 asserts that 𝑃 holds persistently: 𝑃 ⊢ 𝑃 ∗ 𝑃.

4.2     Sharing resources
   Figure 10a shows a proof outline for the program of Figure 8b, using the proof rules shown in
Figure 10b. In this program, both threads read from and write to the same location 𝑥. To support
the sharing of resources among threads, Iris has invariants. In Iris, all resources are owned either
                                                      N
by threads or by invariants. Creating an invariant 𝑃 in a namespace N transfers ownership of
                                                                                 N
some resources satisfying 𝑃 from the current thread to the invariant: 𝑃 ⇛ 𝑃 .6 The knowledge
                                                 N     N      N
of the existence of an invariant is persistent: 𝑃 ⊢ 𝑃 ∗ 𝑃 , and can therefore be shared freely
among threads.
6 The viewshift 𝑃 ⇛ 𝑄 states that resources satisfying 𝑃 can be transformed into resources satisfying 𝑄 by updating ghost

state. Iris’s invariants are constructed from (higher-order) ghost state.
10                                                                                                  Justus Fasse and Bart Jacobs


 {True}
 let x = ref 1 in
                                                                               hoare-def
 {𝑥 ↦→ 1}
                                                                               {𝑃 } 𝑒 {𝑄 } E , (𝑃 −∗ wp E 𝑒 {𝑄 })
 {𝑥 ↦→ 1 ∗ 𝑅} where 𝑅 ∗ 𝑅 =⇒ False
               N                                                         hoare-csq
 {𝑅 ∗ 𝐼             } where 𝐼 , ∃𝑛. 𝑥 ↦→ 𝑛 ∗ (𝑛 = 1 ∨ (𝑛 = 0 ∗ 𝑅))
 fork (                                                                  𝑃 ⇛E 𝑃′             {𝑃 ′ } 𝑒 {𝑄 ′ } E      𝑄′ ⇛E 𝑄
            N
      {𝐼        }                                                                             {𝑃 } 𝑒 {𝑄 } E
      while not
           {(𝑥 ↦→ 1) ∨ (𝑥 ↦→ 0 ∗ 𝑅)}                                                          inv-alloc’
                                                                                                           N
           CAS x 0 1                                                                          𝑃 ⊢ |⇛ 𝑃
           {𝑏. (𝑏 = true ∗ 𝑥 ↦→ 1 ∗ 𝑅) ∨ (𝑏 = false ∗ 𝑥 ↦→ 1)}
                                                                             hoare-inv
      do () done;                                                                            N
                    N                                                                    𝐼          atomic(𝑒)
      {𝑅 ∗ 𝐼            }
                                                                             N ⊆E             {⊲ 𝐼 ∗ 𝑃 } 𝑒 {⊲ 𝑃 ∗ 𝑄 } E\N
      1 / !x; x ≔ 0 (* see main thread *)
 );                                                                                           {𝑃 } 𝑒 {𝑄 } E
               N
 {𝑅 ∗ 𝐼             }                                                          hoare-load
 let v =                                                                       {ℓ ↦→ 𝑣 } ! ℓ {𝑤 . 𝑣 = 𝑤 ∗ ℓ ↦→ 𝑣 } ∅
      {𝑅 ∗ 𝑥 ↦→ 1}
      !x                                                                           hoare-store
      {𝑤 . 𝑤 = 1 ∗ 𝑅 ∗ 𝑥 ↦→ 1}                                                     {ℓ ↦→ 𝑣 } ℓ ≔ 𝑤 {ℓ ↦→ 𝑤 } ∅
 in
                            N                                            hoare-cas-succ
 {𝑣 = 1 ∗ 𝑅 ∗ 𝐼                 }                                        {ℓ ↦→ 𝑣 } CAS ℓ 𝑣 𝑤 {𝑏. 𝑏 = true ∗ ℓ ↦→ 𝑤 } ∅
 1 / v;
               N                                                         hoare-cas-fail
 {𝑅 ∗ 𝐼 }
   {𝑅 ∗ 𝑥 ↦→ 1}
                                                                                                  𝑣 ≠ 𝑣′
   x ≔ 0                                                                 {ℓ ↦→ 𝑣 } CAS ℓ 𝑣 ′ 𝑤 {𝑏. 𝑏 = false ∗ ℓ ↦→ 𝑣 } ∅
   {𝑅 ∗ 𝑥 ↦→ 0}
       N
 {𝐼        }
                                                                         (b) Selected Iris rules [Jung et al.                2018;
               (a) Concurrent reads of, and writes to, x.                Iris contributors 2024].

Fig. 10. The location x is shared between the threads. The load, store, and compare-and-swap commands
are atomic.


   A thread can open an invariant; this temporarily transfers ownership of the invariant’s resources
to the thread. However, a thread must close all invariants it opened before the end of the current
step of execution. Also, it must not open an invariant that is already open. Both constraints are
enforced by tracking the current mask, the set of namespaces7 that can currently be opened. Specif-
ically, the mask E in {𝑃 } 𝑒 {𝑄 } E means that, if 𝑒 takes at most one step, invariants in mask E may
be opened to prove the triple; see hoare-inv.8 If a mask is omitted, the default mask ⊤, which
includes all namespaces, is assumed.
7 Actually, namespaces and masks are both sets of invariant names; if the current mask is E, an invariant in namespace N

can be opened if N ⊆ E.
8 In order to be able to assign meaning to higher-order ghost state such as invariants, Iris is step-indexed: Iris propositions are

predicates over a resource and a step index 𝑛, i.e. the number of steps left in the partial execution trace under consideration.
⊲ 𝑃 asserts that 𝑃 holds later, i.e. after another step of execution. For points-to assertions and other ﬁrst-order assertions
𝑃 , which are timeless, the modality can be ignored: ⊲ 𝑃 ⇛ 𝑃 .
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                                        11


 let deref = 𝝀 l.


                                            ∗∗
 { ⊤ |⇛∅ ∃𝑤 . 𝑙 ↦→ 𝑤 ∗ (𝑙 ↦→ 𝑤 ∅ ≡
                                 − ⊤ Φ(𝑤))}
    {∃𝑤 . 𝑙 ↦→ 𝑤 ∗ (𝑙 ↦→ 𝑤 ∅ ≡− ⊤ Φ(𝑤))}                                                                    inv-alloc
                                                                                                                                 N
                                                                                                            ⊲ 𝑃 ⊢ |⇛∅ 𝑃
                                              ∗
      !l
   {𝑣. 𝑣 = 𝑤 ∗ 𝑙 ↦→ 𝑤 ∗ (𝑙 ↦→ 𝑤 ∅ ≡
                                  − ⊤ Φ(𝑤)}
   {𝑣. ∅ |⇛⊤ Φ(𝑣)}                                                                    inv-open
                                                                                                            N ⊆E

                                                                                                                                ∗
 {Φ(𝑣)}
                                                                                           N
                                                                                               E ⇛ E\N ⊲ 𝑃 ∗ (⊲ 𝑃 E\N ≡
                                                                                                                      −              E True)
 in                                                                                    𝑃


                                                                                                    ∗
 let x = ref 1 in
           N
 {𝑅 ∗ 𝐼            } where 𝐼 , ∃𝑛. 𝑥 ↦→ 𝑛 ∗ (𝑛 = 1 ∨ (𝑛 = 0 ∗ 𝑅))                              𝐴 E1 ≡−    E2 𝐵 , 𝐴 −∗ E1 |⇛E2


                                                                                                                               ∗
 fork (
           N                                                                               𝐴 E1 ⇛ E2 𝐵 , (𝐴 E1 ≡−
      {𝐼       }                                                                                                                   E2 𝐵)
      while not CAS x 0 1 do () done;
      {𝑅 ∗ 𝐼
                   N
                       }
                                                                                                  𝐴 ⇛ E 𝐵 , 𝐴 E ⇛E 𝐵

                                                                                                                         
   1 / deref x; x ≔ 0 (* See main thread *)                                             hoare-atomic
 )                                                                                                              {𝑃 } 𝑒
                                                                                         atomic(𝑒)                           E2 |⇛E1 𝑄 E2
 let v =                                                                                        
           N                                                                                        E1 |⇛E2 𝑃       𝑒 {𝑄 } E1
 {𝑅 ∗ 𝐼 }
 { ⊤ |⇛∅ 𝑥 ↦→ 1 ∗ (𝑥 ↦→ 1 ∅ ≡
      deref x
                                          ∗
                            − ⊤ Φ(1))} where Φ(𝑢) , 𝑅 ∗ 𝑢 = 1
                                                                                                  ⊲(𝑃 ∗ 𝑄) ⊣⊢ ⊲ 𝑃 ∗ ⊲ 𝑄
 {𝑤 . Φ(𝑤)}
                                                                                                         𝜏 is inhabited
 in
                           N                                                                    ⊲(∃𝑥 : 𝜏 . 𝑃) ⊣⊢ ∃𝑥 : 𝜏 . ⊲ 𝑃
 {𝑣 = 1 ∗ 𝑅 ∗ 𝐼 }
 1 / v; x ≔ 0 (* See Figure 10a *)
                                                                                           timeless(£𝑛)              ⊲ 𝑃 ∗ £1 ⊢ |⇛ 𝑃
(a) Proof outline for the program in Figure 8b with the
atomic ! replaced by deref.                                                                       (b) Selected proof rules.

                                           Fig. 11. Specifying fine-grained concurrent functions


   Central to the proof outline in Figure 10a is the purely ghost, exclusive, resource 𝑅 9 , initially
owned by the main thread and, through the invariant, providing exclusive permission to set 𝑥
from 1 to 0.
   Fancy updates. In fact, rule hoare-inv is a special case of rule hoare-atomic (Figure 11b). The
fancy update E1 |⇛E2 𝑃 [Jung et al. 2018, § 7.2] asserts ownership of suﬃcient resources to enable
changing the current mask from E1 to E2 (which involves closing the invariants in E2 \ E1 and
opening the invariants in E1 \E2 ) and otherwise updating ghost state to obtain resources satisfying
𝑃. In particular, if N ⊆ E, we have 𝐼
                                      ∗
                                         N
                                            ⊢ E |⇛E\N ⊲ 𝐼 ∗ (⊲ 𝐼 E\N ≡− E True) (inv-open), where
linear viewshift 𝑃 E1 ≡− E2 𝑄 is a shorthand for 𝑃 −∗ E1 |⇛E2 𝑄.
                                                                                                 ∗
4.3     Fine-grained concurrent functions
Figure 11a shows a proof outline for the program from Figure 8b with ! 𝑥 replaced by deref 𝑥,
deﬁned as let deref l = !l. Unlike ! ℓ, deref ℓ is not atomic since the function application itself
takes a step too. The proof of deref uses hoare-atomic; the proof of the call site uses inv-open.

9 For example                  𝛾                                                                            𝛾
                     ex()          [Iris contributors 2024, § 4.6]. Speciﬁcally, we have True ⇛ ∃𝛾 . ex()       .
12                                                                                            Justus Fasse and Bart Jacobs


                 z       }|       {         z        }|     {
             Logically atomic triple                   AU

                 h®
                  𝑥 . 𝑃i 𝑒 h®
                            𝑦. 𝑄i E ′ , ∀Φ. h®      ® 𝑄 ⇛ Φi E −∗ wp 𝑒 {Φ} where E = ⊤ \ E ′ and
                                             𝑥. 𝑃 | 𝑦.

                                       z }| { z           }|                            {
                                                     VSabort               VScommit
                                                                                        
             AU , gfp(𝑋 . E |⇛∅ ∃®
                                                      ∗
                                 𝑥. 𝑃 ∗ 𝑃 ∅ ≡− E 𝑋 ∧ ∀®
                                                      𝑦. 𝑄 ∅ ≡−
                                                                               ∗      E Φ )

            (a) Encoding of logically atomic triples. Presentation adapted from Mulder and Krebbers
            [2023].
      let x = ref 1 in
            N
       {𝐼         ∗ 𝑅}
      fork (
                  N                                    h𝑏. lk ↦→ 𝑏i acquire lk hlk ↦→ true ∗ 𝑏 = falsei ∅
            {𝐼        }
            acquire x;                                 hlk ↦→ truei release lk hlk ↦→ falsei ∅
                  N                                                  𝛾
            {𝐼        ∗ 𝑅}                             𝑅 , ex() , 𝐼 , ∃𝑛. 𝑥 ↦→ 𝑛 ∗ (𝑛 = 1 ∨ (𝑛 = 0 ∗ 𝑅))
            1/ !x; release x
                                                            N
      )                                                𝐼        ⊢ h𝑛. 𝑥 ↦→ 𝑛 | 𝑥 ↦→ 1 ∗ 𝑛 = 0 ⇛ 𝑅i ∅
            N                                               N
       {𝐼         ∗ 𝑅}                                 𝐼        ∗ 𝑅 ⊢ h𝑥 ↦→ 1 | 𝑥 ↦→ 0 ⇛ Truei ∅
      1 / !x;
                                                            N
      release x                                        𝐼        ⊢ {𝑅} 𝑥 ≔ 0 {True}
            N                                               N
       {𝐼        }                                     𝐼        ⊢ {𝑅} ! 𝑥 {𝑣. 𝑣 = 1 ∗ 𝑅}
      (b) Proof outline for client of concrete (c) Client invariant and atomic updates. Because the
      spinlock.                                spinlock implementation in Figure 2 uses booleans we
                                               implicitly add the constraint 𝑛 ∈ {0, 1}.

                                   Fig. 12. Jung et al. [2015]’s logically atomic triples.


 Verifying spinlock Spinlock release can be speciﬁed analogously:
                                    − ⊤ Φ) release lk {Φ}. Specifying spinlock acquire, however,
  ⊤ |⇛∅ lk ↦→ true ∗ (lk ↦→ false ∅ ≡      ∗
is slightly trickier: we need a mechanism to allow the function to retry (busy-wait) while it is
blocked (marked in green):10 { AU } acquire lk {Φ} where                                  
                                                            ∗        Ô
AU , gfp(𝑋 . ⊤ |⇛∅ ∃𝑏. lk ↦→ 𝑏 ∗ ( lk ↦→ 𝑏 ∅≡− ⊤ 𝑋 ) ∧ (𝑏 = false −∗ lk ↦→ true ∅≡− ⊤ Φ) ) and
gfp(𝑋 . 𝐹 (𝑋 )) is the greatest ﬁxpoint of 𝐹 , i.e. gfp(𝑋 . 𝐹 (𝑋 )) , 𝑃. (𝑃 ⊢ 𝐹 (𝑃)).
                                                                                                         ∗
4.4    Logically atomic triples
The speciﬁcation derived for spinlock’s acquire is a special case of Jung et al. [2015]’s logically
atomic triples.11 Using their notation12 we specify acquire in terms of its atomic pre- and postcon-
dition: h𝑏. lk ↦→ 𝑏i acquire lk hlk ↦→ true ∗ 𝑏 = falsei ∅ . Figure 12 shows the general encoding of
logically atomic triples (12a) and their application to the program of Figure 8c (12b, c).

4.5 Data abstraction
This usage of the lock exposes the underlying boolean reference all but dictating the implemen-
tation as spinlock. We achieve data abstraction by letting the lock module deﬁne a lock predicate
10 AU stands for “atomic update”.
11 Birkedal et al. [2021] have shown that logical atomicity implies linearizability [Herlihy and Wing 1990].
12 Inspired by da Rocha Pinto et al. [2014]’s atomic triples.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules         13


𝐿(lk, 𝑏,𝛾) of three arguments, whose deﬁnition is opaque to the client. To lessen the proof burden
for the client, in particular because 𝐿 may not be timeless, only ⊲ 𝐿(. . .) is required in the atomic
precondition.
                                     {True} create () {lk. ∃𝛾 . 𝐿(lk, false, 𝛾)}
                          h𝑏. ⊲ 𝐿(lk, 𝑏, 𝛾)i acquire lk h𝐿(lk, true, 𝛾) ∗ 𝑏 = falsei E
                          h⊲ 𝐿(lk, true, 𝛾)i release lk h𝐿(lk, false, 𝛾)i E
Now, lk is an opaque reference and 𝑏 represents the abstract lock state, false for unlocked and true
for locked. The third argument 𝛾 is new and can be used by the module to keep track of internal
ghost state across function calls. Because of its irrelevance to the client we usually omit it. Finally,
E is the module mask reserved for operations (module internal invariants) on the lock.

5 TOTAL CORRECTNESS LOGICALLY ATOMIC TRIPLES FOR UNFAIR MODULES
Equipped with this background on verifying partial correctness of uninstrumented programs we
now turn towards instrumented ones. In particular, we consider programs following the higher-
order programming pattern of Section 3. Clients of blocking modules pass auxiliary code wrapped
in auxiliary functions to blocking modules to abstract over the client-speciﬁc manipulation of
auxiliary state. Previously we reasoned informally about 𝜂—required to produce fuel when the
module is blocked on the client—and 𝜅, allowing the client to change auxiliary state the moment
the blocking operation takes eﬀect. In this section we concretize these intuitions with precise
contracts.

5.1 Spinlock-specific total correctness specification
We want a modular yet expressive speciﬁcation for the instrumented spinlock of Figure 2b. Recall
that we use atomic blocks to bundle the execution of 𝜂 and 𝜅 with real, atomic, expressions. For
example executing 𝜅 the moment the spinlock is released h𝜅 (); lk ≔ false i (Figure 2b). If
the sequential expression 𝑒 is executed in a big-step—i.e. as part of an atomic block—wp⇓E 𝑒 {Φ}
describes the weakest precondition of 𝑒 such that Φ holds afterwards.
   The logically atomic triples of Figure 12c do not work for two reasons. First, VScommit needs to
say that it is safe to execute 𝜅, that 𝜅 terminates, and that after running 𝜅 the invariants can be
closed again. Therefore we adapt VScommit as follows.
                         𝑏 = false −∗ lk ↦→ true ∅ ≡−
                                                       ∗    ⊤ Φ                   partial correctness
                𝑏 = false −∗ wp⇓∅ 𝜅 {lk ↦→ true ∅ ≡−
                                                       ∗    ⊤ Φ}                     total correctness
   Second, VSabort needs to say that if the lock is already held, it is safe for the module to run 𝜂, 𝜂
terminates, and after running 𝜂 the invariants can be closed again. Separately, upon return, 𝜂 must
guarantee that a call permission to fuel the busy-waiting loop is available. Therefore, we adapt
VSabort as follows.
                                         lk ↦→ 𝑏 ∅≡−
                                                          ∗    ⊤ AU                   partial correctness
                          ⇓
            𝑏 = true −∗ wp ∅ 𝜂 {cp(0) ∗ (lk ↦→ 𝑏 ∅≡−
                                                          ∗    ⊤ TAU)}                   total correctness
The important addition is the call permission in the postcondition.Note that acquire consists of a
simple busy-waiting CAS-loop so that a call permission of minimal degree 0 per iteration suﬃces.
We use cp𝜃 (𝛿) to represent ownership of a call permission of degree 𝛿 associated with thread 𝜃 . If
𝜃 is the current thread we omit it.
14                                                                                          Justus Fasse and Bart Jacobs



l
         1                        2                       3          
𝛿 h®
   𝑥 ։ 𝑋 . 𝑃i 𝑒 h®
                 𝑦. 𝑄i E ′ , ∀Φ, 𝜂, 𝜅, 𝑂.      cp(𝛿) ∗ obs(𝑂) ∗ l ≺ 𝑂 −∗

     z            }|                {
                TAU

             𝜂      𝜅
     l;𝑂
     𝛿
                      ® 𝑄 ⇛ Φi E −∗ wp 𝑒 𝜂 𝜅 {Φ} where E = ⊤ \ E ′ and
          𝑥 ։ 𝑋 . 𝑃 | 𝑦.
         h®
                                                            n 6                     z }| { o  ª
                                                                                       VSabort
                             ©                  
                             ­ obs(𝑂) ∗ 𝑥® ∉ 𝑋 −∗ wp⇓ 𝜂 () cp(𝛿) ∗ obs(𝑂) ∗ 𝑃 ≡−
                             ­
                     𝑥. 𝑃 ∗ ­­
TAU , gfp(𝑍 . E |⇛∅ ∃®
                                     4        5

                                                      ∅
                                                                             7

                                                                                      ∅      E 𝑍 ∧ ®®
                                                                                                    ®)
                                                                                                    ®
                                                                                                        ∗
                             ­  8                           n z      }|       { o                 ®
                                                                    VScommit
                             ­                                                                     ®
                             «
                                             9
                                 𝑥® ∈ 𝑋 ∗ obs(𝑂) −∗ wp⇓∅ 𝜅 () ∀®𝑦. 𝑄 ∅ ≡− E Φ
                                                                                      ∗             ¬

                 Fig. 13. Total correctness logically atomic triple for unfair, blocking, modules.


     A spinlock-speciﬁc total correctness speciﬁcation thus looks as follows.
h𝑏 ։ false. lk ↦→ 𝑏i acquire lk hlk ↦→ true ∗ 𝑏 = falsei ∅ , ∀Φ, 𝜂, 𝜅. TAU −∗ wp acquire lk 𝜂 𝜅 {Φ}
                                                                                               !
where TAU , gfp(𝑋 . ⊤|⇛∅ ∃𝑏. lk ↦→ 𝑏 ∗
                                          (𝑏 = true −∗ wp⇓∅ 𝜂 cp(0) ∗ (lk ↦→ 𝑏 ∅ ≡− ⊤ 𝑋 ) ) ∧
                                                               
                                          (𝑏 = false −∗ wp⇓∅ 𝜅 lk ↦→ true ∅ ≡− ⊤ Φ )
                                                                                             ∗ ∗  )

The eventually arrow13 ։ expresses the liveness requirement imposed on the client. If unsatisﬁed,
the module can legitimately expect the client to eventually put the module in a satisfying state.
This summarizes the core idea of our total correctness logically atomic triples.

5.2      Total correctness logically atomic triples
Figure 13 generalizes this speciﬁcation approach to arbitrary unfair blocking operations. To start
with, we generalize the eventually arrow notation to handle sequences of variables: 𝑥® ։ 𝑋 (Fig-
ure 13, 1 ). It engenders the preconditions 𝑥® ∉ 𝑋 5 and 𝑥® ∈ 𝑋 8 for 𝜂 and 𝜅, respectively (cf.
𝑏 ։ false).
   Operations may generally wish to block internally i.e. without involvement of the client. In
HeapLang< , this requires that the levels of the signals they expect be below the levels of the thread’s
obligations. The exclusive resource obs𝜃 (𝑂) 3 asserts that thread 𝜃 ’s set of obligations is exactly
O. Once again we omit 𝜃 if it matches the current thread.
  Total correctness speciﬁcation for unfair locks.
  We characterize unfair locks with the following speciﬁcation.
                                            {True} create () {lk. 𝐿(lk, false)}
                     l
                     𝛿 h𝑏 ։ {false}. ⊲ 𝐿(lk, 𝑏)i acquire lk h𝐿(lk, true) ∗ 𝑏 = falsei E
                                                                           l
                               𝛿 h⊲ 𝐿(lk, true)i release lk h𝐿(lk, false)i E

  Note that the triple for release is slightly diﬀerent than the one for acquire . For one, release ’s
speciﬁcation lacks the eventually arrow. This means it is only passed 𝜅. Moreover, l is positioned to
the right for release and to the left for acquire . The distinction drawn here is whether the module
has access to l ≺ 𝑂 ∗ obs(𝑂) before (left) or after (right) running 𝜅. Consequently, release ’s
postcondition is Φ ∗ l ≺ 𝑂 ∗ obs(𝑂) as opposed to just Φ.
13 This notation is inspired by TaDA Live [D’Osualdo et al. 2021] where it describes a constraint on the environment that

always eventually the atomic precondition is satisﬁed.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules          15


                             let f = ref true in let lk = create () in
                             let sf = NewSignal 2 in let s = ref nil in
                                                                     NewExpectPerm sf 𝛿 '' 𝛿 ';
                                                                     let r = ref nil in
                                                                     let b = ref true in
                                                                     while !b do
    let r = ref nil in
                                                                       acquire lk
    acquire lk
                                                                          (𝝀. if !r ≠ !s then (
      (𝝀. if !r ≠ !s then (
                                                                              NewExpectPerm !s ⊤eta ⊥eta;
          NewExpectPerm !s ⊤eta ⊥eta;
                                                                              r ≔ !s);
          r ≔ !s);
                                                                            Expect !s)
        Expect !s);
                                                                          (𝝀. s ≔ NewSignal 0);
      (𝝀. (s ≔ NewSignal 0));
                                                                       b ≔ !f;
    f ≔ false;
                                                                       release lk
    release lk (𝝀. SetSignal !s; SetSignal sf)
                                                                          (𝝀. SetSignal !s;
                                                                            if !f then (Expect sf;
                                                                              lower 𝛿 ' into 2 times 𝛿 ))
                                                                     done

Fig. 14. Instrumented version of D’Osualdo et al. [2021, § 4]’s distinguishing client. If lk is fair, the program
is guaranteed to terminate under any fair schedule. Otherwise, the program may diverge. Notice that in this
program the right thread can be bypassed at most once.



6    MODULAR PROGRAMMING OF FAIR MODULES
The programming and speciﬁcation patterns proposed in Sections 3 and 5 are appropriate when the
responsibility for ensuring that the blocking operation eventually ﬁnds the atomic precondition
satisﬁed, is delegated entirely to the client. In many cases, however, the distribution of responsi-
bilities is more intricate.
    Consider, for example, the erasure of the program in Figure 14. In this program, there is no
way for the client to guarantee, on their own, that the left thread will eventually ﬁnd itself able
to acquire the lock. Indeed, this is only the case if the left thread’s acquire cannot be starved by
the lock implementation. We say that an acquire operation is bypassed if during its execution the
lock is released and subsequently acquired by another acquire . A lock is starvation-free if each
acquire can only be bypassed ﬁnitely many times. We call such locks fair. Concretely, if the lock
is unfair, e.g. the spinlock in Figure 2, this program may diverge. But if it is a fair lock, e.g. the
ticketlock in Section 6.1, it terminates under any fair scheduler.
    The division of responsibilities between module and client in case of fair locks, then, is as follows.
It is the client’s responsibility to ensure that all bypassing acquire operations are eventually paired
with a corresponding release. The module, in turn, must ensure a ﬁnite number of bypasses before
a given acquire operation succeeds.
    In terms of our instrumentation, this distinction manifests as the program in Figure 14 being safe
or not. With an unfair lock, the left thread’s 𝜂 has to guarantee possibly inﬁnitely many release s—
one for each bypass. To do so, it would need to create inﬁnitely many expect permissions which
is impossible (Section 2). Conversely, the auxiliary code is safe if a fair lock module ensures that
for every bypass—of which there can be only ﬁnitely many—there exists a compensatory call per-
mission.
16                                                                                 Justus Fasse and Bart Jacobs


       let acquire lk 𝜂 𝜅 =
         let t =
         h if !(lk.next) = !(lk.owner)
           then (* Acq-LP-1 *) 𝜅 ()                           let release lk 𝜅 =
           else (FAIRNESS;                                      h (* Rel-LP *) 𝜅 ();
             lk.𝜅 s[!(lk.next)] ≔ 𝜅 );                           FAA lk.owner 1;
           FAA lk.next 1 i                                       if !(lk.owner) < !(lk.next)
         in                                                      then (* Acq-LP-2 *)
         while                                                     lk.𝜅 s[!(lk.owner)] () i
         h if !(lk.owner) ≠ t then 𝜂 () else ();
           !(lk.owner) ≠ t i
         do () done

Fig. 15. Instrumented ticketlock implementation. The ticket t is the old value returned when lk.next is
bumped. fairness is a placeholder for the auxiliary code to satisfy the fair lock contract with respect to 𝜂.


6.1    Ticketlock
   Figure 15 shows a ticketlock [Mellor-Crummey and Scott 1991] implementation instrumented
in the style of Section 3. The ticketlock is a simple fair lock consisting of two ﬁelds: owner ticket
and next available ticket, both initialized to zero. During acquire , the next ﬁeld is atomically
incremented with the fetch-and-add (FAA) instruction. FAA returns the old value which becomes
the ticket. Thereafter, the owner ﬁeld is read in a busy-waiting loop until the read value matches
the ticket. Releasing the lock simply increments the owner counter by one.14
   Before revealing the auxiliary code that fairness stands-in for, we discuss the placement of 𝜂
and 𝜅 as application of the programming pattern of Section 3. First, acquire and release ’s 𝜅s must
be executed at their respective linearization points. Let 𝑡 be a ticket and 𝑜 and 𝑛 be the contents
of owner and next, respectively. The ticketlock is held by the thread owning ticket 𝑡 iﬀ 𝑡 = 𝑜.
This implies two linearization points for ticketlock acquire : (1) An internal one if FAA lk.next 1
returns the ticket 𝑜. Because FAA returns the old value, 𝑡 = 𝑛 = 𝑜, while next’s new value is 𝑛 + 1.
Therefore the lock linearizes at this moment, transitioning from not held to held. This situation
is detected in the auxiliary code, executing 𝜅 accordingly (Figure 15, Acq-LP-1). (2) An external
one if the returned ticket 𝑡 < 𝑜. In this case, acquire linearizes at the FAA of release when owner
equals 𝑡 − 1 (Acq-LP-2). Regardless of whether release linearizes an acquire or not, its own
linearization point happens with the increment of owner .
   Second, 𝜂 is called when acquire establishes that it is blocked on the client because its ticket 𝑡
does not equal the contents of owner . Notice that if acquire linearizes at Acq-LP-1, 𝜂 will not be
called. Otherwise, acquire will see itself bypassed by all preceding ticket holders.
   Indeed, the ticket regime enforces a ﬁrst-in-ﬁrst-out (FIFO) direct handoﬀ succession policy [Dice
2017; Guerraoui et al. 2018]. The auxiliary code placeholder thus compensates exactly that many
bypasses. (* FAIRNESS , *) lower 𝛿 into !(lk.next) - !(lk.owner) times ⊤eta In the ap-
pendix we describe how to pick 𝛿 and ⊤eta modularly.

7 TOTAL CORRECTNESS LOGICALLY ATOMIC TRIPLES FOR FAIR MODULES
To match the extended programming pattern of Section 6 we adapt the notion of total correctness
logically atomic triples to fair modules, here locks. We say that every time the client fulﬁlls its duty

14 For simplicity we use FAA for this operation too.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                 17


by calling release a new round starts: h𝐿(lk, true, 𝑟 )i release lk h𝐿(lk, true, 𝑟 + 1 )i E . Otherwise
the speciﬁcation for a fair release is identical to an unfair one.
  At the notation-level the impact of fairness on acquire is similarly minimal. h(𝑏, 𝑟 ) ։ 𝑟 {false}×
N. 𝐿(lk, 𝑏, 𝑟 )i TL_acquire lk h𝐿(lk, true, 𝑟 ) ∗ 𝑏 = falsei E . The addition of the rounds subscript to
the eventually arrow ։𝑟 indicates which part of the atomic precondition evolves to indicate new
rounds. All but one competing acquire operation will see themselves bypassed for each new round
and must thus be compensated with a call permission. To show the diﬀerence with respect to the
unfair encoding, we ﬁrst recall the deﬁnition of our total correctness logically atomic triple for
unfair locks e.g. spinlock.15

h𝑏 ։ false. 𝐿(lk, 𝑏)i SL_acquire lk h𝐿(lk, true) ∗ 𝑏 = falsei E ,
      ∀Φ, 𝜂, 𝜅. (cp(⊤SL ) ∗ TAU) −∗ wp SL_acquire lk {Φ}
                                                                  n                                  o
                                           ©
where TAU , gfp(𝑍 . ⊤\E |⇛∅ ∃𝑏. 𝐿(lk, 𝑏) ∗ ­
                                             (𝑏 = true −∗ wp ⇓
                                                                𝜂
                                                                   n
                                                                    cp(⊤SL ) ∗ (𝐿(lk, 𝑏)  ≡
                                                                                          −
                                                                                         ∅ o ⊤\E
                                                                                                 𝑍 )
                                                                                                       ∗
                                                                                                       )∧ª
                                                                                                         ®)
                                                                                               ∗
                                                             ∅
                                                              ⇓
                                           «                                                             ¬
                                             (𝑏 = false −∗ wp ∅ 𝜅 𝐿(lk, true) ∅ ≡− ⊤\E Φ )

We use the round resource 𝑅 to encode that 𝜂 requires one-time compensation per round.

h(𝑏, 𝑟 ) ։ 𝑟 {false} × N. 𝐿(lk, 𝑏, 𝑟 )i TL_acquire lk h𝐿(lk, true, 𝑟 ) ∗ 𝑏 = falsei E ,
      ∀Φ, 𝜂, 𝜅, 𝑅 . (cp(⊤TL ) ∗ 𝑅(_) ∗ TAU) −∗ wp TL_acquire lk {Φ}
TAU , gfp(𝑍 . ⊤\E |⇛∅ ∃𝑏, 𝑟 . 𝐿(lk, 𝑏, 𝑟 ) ∗
                                                                 n                                                      o
©
­
  (𝑏 = true ∗ ( ∃𝑟 0 . 𝑅(𝑟 0 ) ∗ (𝑟 0 = 𝑟 ∨ cp(⊤
                                             n
                                                𝐶 )) ) −
                                                       ∗ wp ⇓
                                                               𝜂   cp( ⊥𝐶 ) ∗ 𝑅(𝑟 ) ∗ (𝐿(lk, 𝑏, 𝑟 ) ∅ ≡−
                                                                         o                                ∗        𝑍 )    ª
                                                                                                                           ®)
                                                                   ∗
                                                            ∅                                                   ⊤\E
                                           ⇓
«                                                                                                                          ¬
  ∧ (𝑏 = false ∗ ( ∃𝑟 0 . 𝑅(𝑟 0 ) ) −∗ wp ∅ 𝐿(lk, true, 𝑟 ) ∅ ≡− ⊤\E Φ

 Notice that 𝑅 has to be treated “linearly” by the module. Initially passed to the module at an
unknown round, every call to 𝜂 takes and returns 𝑅 in its pre- and postcondition until 𝜅 consumes
it at the linearization point. Calling 𝜂 at round 𝑟 returns 𝑅(𝑟 ). Future calls to 𝜂 are free if the module
can prove to 𝜂 that it has already been called for the current round: ∃𝑟 0 . 𝑅(𝑟 0 ) ∗ 𝑟 0 = 𝑟 (recall that
𝑟 always expresses the current round). Otherwise 𝜂 requires a compensatory call permission.
    Internal waiting. Figure 16 generalizes this encoding to our encoding of total correctness logi-
cally atomic triples for fair modules. To support internal blocking we again require the caller to
pass obs(𝑂) with the lower bound determined by a set of module degrees L𝑀 ( A , B , E ). In Sec-
tion 5.2 all changes to the thread’s obligations had to be opaque to the client: 𝜂 and 𝜅 require
obs(𝑂) in their precondition. For fair modules16 we relax this restriction for 𝜂 and allow any set
of obligations 𝑂 ′ with L𝑀  𝑂 ′ ( C , D ). This permits calling 𝜂 while holding internal obligations
whose level is above or in L𝑀 . Section 9 discusses how the proof for a fair cohortlock uses this
aﬀordance.
    Total correctness speciﬁcation for fair locks.

             {True} create () {lk. 𝐿(lk, _, false)}
             LFL
                   h(𝑏, 𝑟 ) ։𝑟 {false} × N. ⊲ 𝐿(lk, 𝑟 , 𝑏)i acquire lk h𝐿(lk, 𝑟 , true) ∗ 𝑏 = falsei E
             h⊲ 𝐿(lk, 𝑟 , true)i release lk h𝐿(lk, 𝑟 + 1, false)i L
                                                                  E
                                                                    FL



15We defer the treatment of obligations (i.e. the L annotation) because both spinlock and ticketlock’s blocking behavior
                                                   𝑀
is entirely justiﬁed by the client.
16We could also view unfair modules as fair modules with a constant round.
18                                                                                         Justus Fasse and Bart Jacobs


       A
      L𝑀 h®
                                                                                               B  
          𝑥 ։𝑟 𝑋 . 𝑃i 𝑒 h®
                         𝑦. 𝑄i E𝑀 ,            ∀Φ, 𝜂, 𝜅, 𝑂, 𝑅. 𝑅(None) ∗ cp(⊤𝑀 ) ∗ obs(𝑂) ∗ L𝑀 ≺ 𝑂 −∗
                                                 z               }|             {
                                                                 TAU

                                                     𝜂       𝜅
                                                                          𝑀 ;𝑂
                                                 h®            ® 𝑄 ⇛ Φi L
                                                  𝑥 ։𝑟 𝑋 . 𝑃 | 𝑦.       E
                                                                               −∗ wp 𝑒 𝜂 𝜅 {Φ}
     where E = ⊤ \ E𝑀 and TAU , gfp(𝑍 . E |⇛∅ ∃®
                                               𝑥. 𝑃 ∗

     © ©              C
                                                                                                 ª ª
     ­ ­ ∀𝑂 ′ . obs(𝑂 ′ ) ∗ L𝑀  𝑂 ′ ∗ ∃𝑟 0 . 𝑅(𝑟 0 ) ∗ (𝑟 0 = 𝑟 ∨ cp(⊤𝐶 )) ∗ 𝑥® ∉ 𝑋 −∗            ® ®
     ­ ­                                                                                           ® ®
     ­ ­                                                                                           ®∧ ®
     ­ ­                 n                                 z }| { o
                                                              VSabort
                                                                                                   ® ®
     ­ ­                                                                                           ® ®
     ­
     ­ «
     ­
     ­ 
     ­
                   ⇓
                                               D
               wp ∅ 𝜂 () 𝑅(𝑟 ) ∗ cp(⊥𝐶 ) ∗ obs(𝑂 ′ ) ∗ 𝑃 ∅ ≡− E 𝑍

                                                nz         }|
                                                        VScommit
                                                                   ∗{o 
                                                                                                      ®)
                                                                                                   ¬ ®®
                                                                                                      ®
                                                                                                      ®
     ­
     «
                             E
                                        ⇓
         (𝑅(_) ∗ 𝑥® ∈ 𝑋 ∗ obs(𝑂)) −∗ wp ∅ 𝜅 () ∀®   𝑦. 𝑄 ∅ ≡− E Φ
                                                                  ∗                                   ®
                                                                                                      ¬

                    Fig. 16. Total correctness logically atomic triple for fair blocking modules.


8    TOOL SUPPORT
In this paper we used Iris17 to verify safety of instrumented programs. However, any other ap-
proach for verifying safety of higher-order ﬁne-grained concurrent programs can be used as well,
such as that implemented by the VeriFast tool for separation logic-based modular symbolic execu-
tion of concurrent C or Java programs [Vogels et al. 2015]. We used the existing encoding of Ghost
Signals into VeriFast by Reinhard and Jacobs [2021a] to modularly verify termination of Java ver-
sions of the examples of this paper18 , including the cohortlock described in the next section. While
non-foundational—bugs in the axiomatization of Ghost Signals or in VeriFast itself could lead to
unsoundness—these machine-checked example proofs dramatically increase our conﬁdence that
our approach can in fact be applied to modularly verify termination of highly non-trivial concur-
rent algorithms.19

9    COHORTLOCK
Lock cohorting [Dice et al. 2012, 2015] is a design pattern to construct non-uniform memory access
(numa) aware locks from numa unaware locks. On a numa architecture, threads can be grouped
into cohorts belonging to the same node. While all threads share a logical address space, access to
memory last accessed by a thread from the same cohort is much faster than otherwise. Therefore,
if there are threads of multiple cohorts competing for a lock, it is preferable to pass the lock to a
thread of the same cohort to improve throughput.
   Figure 17 shows an implementation in HeapLang. Speciﬁcally, cohortlocks employ one top-level
lock shared by all cohorts, plus a local lock per cohort. To own a cohortlock, both the local lock
and the top-level lock must be owned. In addition to acquire and release , the local lock must
support an alone operation that only returns false if there is a thread waiting to acquire the lock.20
For the ticketlock this is easy: let alone lk = !(lk.owner) + 1 = !(lk.next). Thus, to prefer
passing ownership within the same cohort, the cohortlock’s release queries the underlying local
17 On paper only, not in Coq; a Coq mechanization of our metatheory is future work.
18 See the artifact [Fasse and Jacobs 2024].
19 A mechanization of the example proofs in Iris in Coq would give even much greater conﬁdence; this is future work.
20 alone may return false positives but never false negatives.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules     19


                                                        let release lk =
                                                          let LL = lk.LLs[CC] in
 let acquire lk =
                                                          if ticketlock_alone LL
   let LL = lk.LLs[CC] in
                                                            || lk.passCount[CC] ≥ MAX then
   ticketlock_acquire LL;
                                                            lk.passCount[CC] ≔ 0;
   if lk.passing[CC] then
                                                            ticketlock_release TL;
     (* Handoﬀ *)
                                                            ticketlock_release LL
     lk.passing[CC] ≔ false
                                                          else
   else
                                                            lk.passCount[CC]++;
     ticketlock_acquire TL
                                                            lk.passing[CC] ≔ true;
                                                            ticketlock_release LL

Fig. 17. Cohortlock. CC means current cohort. If there are waiting threads from the same cohort, the cohort-
lock will pass ownership directly to the next thread of the cohort by releasing the local lock LLs[CC] but
not the top-level lock TL. To avoid starvation, such handoﬀs are performed a maximum of MAX times. The
cohortlock is fair if its underlying locks are fair.



lock whether the releasing thread is alone. If so both the top-level and local lock are released (in
that order). Otherwise, the cohortlock release can choose to only release the local lock while
passing ownership of the top-level lock to the next thread in the cohort (cf. Figure 1). To prevent
starvation of other cohorts, it only does so until a threshold is reached. Moreover, the cohortlock
is only fair if the underlying locks are fair.
   We proved that this lock implementation satisﬁes total correctness per our fair lock speciﬁca-
tion, assuming only that the ticketlocks used in turn satisfy our fair lock speciﬁcation. We (non-
foundationally) machine-checked our proof using VeriFast; see the artifact [Fasse and Jacobs 2024].
   A core design decision of the proof is that acquire creates a signal (which we call the acquire sig-
nal) during the ticketlock_acquire LL call’s linearization point (LP), but only if lk.passing[CC]
is false, and discharges it during ticketlock_acquire TL’s LP. Similarly, release creates a signal
(the release signal) during the ticketlock_release TL call’s LP (again, if not passing) and dis-
charges it during the ticketlock_release LL call’s LP. If the 𝜂 passed into ticketlock_acquire LL
is executed, some other thread in the cohort holds LL, and either 1) has not yet acquired TL, 2) holds
TL, or 3) has released TL. Correspondingly, this 𝜂 expects either this thread’s acquire signal, calls
the client’s 𝜂, or expects the thread’s release signal. If the 𝜂 passed into ticketlock_acquire TL
is executed, some other cohort holds TL. At most MAX number of successive threads of that cohort
own the lock, so at most MAX rounds of the client’s 𝜂 have to be called.

10 RELATED WORK
We propose the ﬁrst approach for expressive modular termination veriﬁcation of busy-waiting
programs in a higher-order separation logic like Iris or that of VeriFast. This means that it beneﬁts
from the existing metatheory development and tool support for those logics, and furthermore that
it is compatible with the other features and many of the other applications and extensions of those
logics proposed in the literature, and is more accessible to the communities already familiar with
those logics.
    TaDA Live. D’Osualdo et al. [2021]’s TaDA Live is a bespoke ﬁrst-order separation logic to com-
positionally reason about termination of ﬁne-grained concurrent programs. We believe the clear
distinction between module and client responsibilities for termination advocated for—and demon-
strated by—TaDA Live set a new standard for modular termination veriﬁcation.
20                                                                                             Justus Fasse and Bart Jacobs


   In contrast to Sassy, however, it does not support unstructured concurrency or external lin-
earization points. Another notable diﬀerence is the interpretation of “։”: in TaDA Live it expresses
that the client must always eventually fulﬁll the atomic precondition. Since this is insuﬃcient to
prove termination of unfair locks their unfair lock speciﬁcation requires an impedance budget, an
ordinal that bounds the number of acquire invocations. By contrast, our ։ requires the client to
justify progress in terms of call permissions whenever the atomic precondition is not in the module-
desired state. As a result, in contrast to TaDA Live, Sassy supports program C2 [D’Osualdo et al.
2021, p. 79].21
   A more serious limitation of TaDA Live is that, like our approach, it associates a level (called
a layer in TaDA Live) with each lock and requires that only environment obligations at levels
below the lock’s level are used to justify blocking. Unlike our approach, however, it also does
not support asynchronously burdening another thread with obligations. We believe that, together,
these limitations mean it does not support a variant of the client program of Figure 1 where the
middle thread busy-waits for the left thread to clear the ﬂag, whereas our approach does.22
   Iris. Although Iris [Jung et al. 2015, 2016, 2018; Spies et al. 2022] is fundamentally limited to
safety properties due to its use of step-indexing, many approaches have been developed to work
around this limitation. The Iris developments discussed below have been foundationally mech-
anized in Iris’ Coq-framework. Transﬁnite Iris [Spies et al. 2021] uses ordinals as step-index in-
stead of natural numbers. This solves the biggest issue of a naive fuel-based approach in Iris at the
logic level, obviating the need for auxiliary code. Spies et al. [2021] prove program termination
via reﬁnement of an ordinal in addition to termination-preserving reﬁnement of another program.
Transﬁnite Iris does not, however, address blocking concurrent programs under fair scheduling.
Tassarotti et al. [2017] proved termination-preserving reﬁnement for concurrent programs, but
with the rather severe limitation that stuttering in the reﬁnement must be bounded by a ﬁxed nat-
ural number. Trillium [Timany et al. 2024] considers a more general form of reﬁnement between
traces of a program and a model. Fairis, an instantiation of Trillium for reasoning about concur-
rent programs under fair scheduling, allows them to reason about liveness properties, including
termination. Their approach requires a terminating model, which is then proven to be reﬁned by
the program. Modular composition of models is mentioned as future work.

11 CONCLUSION AND FUTURE WORK
We propose the ﬁrst approach for expressive modular veriﬁcation of termination of busy-waiting
programs in a higher-order separation logic like Iris. We demonstrate its expressiveness and amenabil-
ity to tool support by reporting on a (non-foundational) machine-checked proof that a cohortlock—
built on top of other locks and using lock handoﬀ internally (where a lock is acquired by one
thread and released by another)—satisﬁes our fair lock speciﬁcation, assuming only that the un-
derlying locks it is built on also satisfy our fair lock speciﬁcation. It is a two-step approach. First,
the program is instrumented modularly with auxiliary constructs from a fuel-based terminating
programming language that has the property that if an instrumented program is safe, the original
program is also safe and terminates under fair scheduling. Secondly, any logic for veriﬁcation of
safety of higher-order ﬁne-grained concurrent programs is used to modularly verify safety of the
instrumented program. We propose auxiliary code patterns for modularly instrumenting unfair
and fair blocking modules, and corresponding speciﬁcation patterns for modularly verifying the
instrumented programs’ safety.


21 See our proof in the artifact [Fasse and Jacobs 2024].
22 For more details and our proof of this program, see the artifact [Fasse and Jacobs 2024].
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                  21


   We identify three key directions for future work. First, in this paper we presented how Iris can
be used to reason about HeapLang< programs. The implementation and proof of the ticketlock
leveraged HeapLang’s higher-order nature and Iris’ ability to reason about helping. Another key
strength of Iris with respect to the veriﬁcation of concurrent modules is its support for erasable
prophecy variables to reason about future-dependent linearization points. HeapLang< inherits sup-
port for prophecy variables but cannot read them in erasable code. To enable verifying total cor-
rectness of concurrent modules with future-dependent linearization points, we plan to modify
prophecy variables, allowing auxiliary code to read them. We suspect that this might additionally
enable attaching prophecy resolutions to logically atomic operations, not just atomic operations, a
current limitation [Jung et al. 2020]. Second, a natural next step would then be to integrate the pre-
sented work and this extension into a Coq mechanization. This would give foundational backing
to our approach.

ACKNOWLEDGMENTS
This research is partially funded by the Research Fund KU Leuven, and by the Cybersecurity Re-
search Program Flanders.

REFERENCES
Lars Birkedal, Thomas Dinsdale-Young, Armaël Guéneau, Guilhem Jaber, Kasper Svendsen, and Nikos Tzevelekos.
   2021. Theorems for free from separation logic speciﬁcations. Proc. ACM Program. Lang. 5, ICFP (2021), 1–29.
   https://doi.org/10.1145/3473586
Pontus Boström and Peter Müller. 2015. Modular Veriﬁcation of Finite Blocking in Non-terminating Programs.
   In 29th European Conference on Object-Oriented Programming, ECOOP 2015, July 5-10, 2015, Prague, Czech Re-
   public (LIPIcs, Vol. 37), John Tang Boyland (Ed.). Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 639–663.
   https://doi.org/10.4230/LIPIcs.ECOOP.2015.639
Solange Coupet-Grimal and William Delobel. 2006. An eﬀective proof of the well-foundedness of the multiset path ordering.
   Appl. Algebra Eng. Commun. Comput. 17, 6 (2006), 453–469. https://doi.org/10.1007/S00200-006-0020-Y
Pedro da Rocha Pinto, Thomas Dinsdale-Young, and Philippa Gardner. 2014. TaDA: A Logic for Time and Data Ab-
   straction. In ECOOP 2014 - Object-Oriented Programming - 28th European Conference, Uppsala, Sweden, July 28 - Au-
   gust 1, 2014. Proceedings (Lecture Notes in Computer Science, Vol. 8586), Richard E. Jones (Ed.). Springer, 207–231.
   https://doi.org/10.1007/978-3-662-44202-9_9
Nachum Dershowitz and Zohar Manna. 1979. Proving Termination with Multiset Orderings. Commun. ACM 22, 8 (1979),
   465–476. https://doi.org/10.1145/359138.359142
Dave Dice. 2017. Malthusian Locks. In Proceedings of the Twelfth European Conference on Computer Systems, EuroSys
   2017, Belgrade, Serbia, April 23-26, 2017, Gustavo Alonso, Ricardo Bianchini, and Marko Vukolic (Eds.). ACM, 314–327.
   https://doi.org/10.1145/3064176.3064203
David Dice, Virendra J. Marathe, and Nir Shavit. 2012. Lock cohorting: a general technique for designing NUMA
   locks. In Proceedings of the 17th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming,
   PPOPP 2012, New Orleans, LA, USA, February 25-29, 2012, J. Ramanujam and P. Sadayappan (Eds.). ACM, 247–256.
   https://doi.org/10.1145/2145816.2145848
David Dice, Virendra J. Marathe, and Nir Shavit. 2015. Lock Cohorting: A General Technique for Designing NUMA Locks.
   ACM Trans. Parallel Comput. 1, 2 (2015), 13:1–13:42. https://doi.org/10.1145/2686884
Edsger W. Dijkstra. 1975. Guarded Commands, Nondeterminacy and Formal Derivation of Programs. Commun. ACM 18,
   8 (1975), 453–457. https://doi.org/10.1145/360933.360975
Emanuele D’Osualdo, Julian Sutherland, Azadeh Farzan, and Philippa Gardner. 2021. TaDA Live: Compositional Reason-
   ing for Termination of Fine-grained Concurrent Programs. ACM Trans. Program. Lang. Syst. 43, 4 (2021), 16:1–16:134.
   https://doi.org/10.1145/3477082
Justus Fasse and Bart Jacobs. 2023–2024. Expressive modular termination veriﬁcation for busy-waiting programs (Ver-
   iFast proofs).      https://github.com/verifast/verifast/tree/master/examples/busywaiting/ﬂexiblespecs/ticketlock-java
   https://zenodo.org/records/13620299.
Rachid Guerraoui, Hugo Guiroux, Renaud Lachaize, Vivien Quéma, and Vasileios Trigonakis. 2018. Lock-Unlock: Is
   That All? A Pragmatic Analysis of Locking in Software Systems. ACM Trans. Comput. Syst. 36, 1 (2018), 1:1–1:149.
   https://doi.org/10.1145/3301501
22                                                                                             Justus Fasse and Bart Jacobs


Maurice Herlihy and Jeannette M. Wing. 1990. Linearizability: A Correctness Condition for Concurrent Objects. ACM
    Trans. Program. Lang. Syst. 12, 3 (1990), 463–492. https://doi.org/10.1145/78969.78972
C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. Commun. ACM 12, 10 (1969), 576–580.
    https://doi.org/10.1145/363235.363259
Iris contributors. 2024. The Iris 4.2 Reference. https://plv.mpi-sws.org/iris/appendix-4.2.pdf
Samin S. Ishtiaq and Peter W. O’Hearn. 2001. BI as an Assertion Language for Mutable Data Structures. In Conference
    Record of POPL 2001: The 28th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages , London,
    UK, January 17-19, 2001, Chris Hankin and Dave Schmidt (Eds.). ACM, 14–26. https://doi.org/10.1145/360204.375719
Bart Jacobs, Dragan Bosnacki, and Ruurd Kuiper. 2018. Modular Termination Veriﬁcation of Single-Threaded and Multi-
    threaded Programs. ACM Trans. Program. Lang. Syst. 40, 3 (2018), 12:1–12:59. https://doi.org/10.1145/3210258
Bart Jacobs and Frank Piessens. 2011. Expressive modular ﬁne-grained concurrency speciﬁcation. In Proceedings of the 38th
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2011, Austin, TX, USA, January 26-28,
    2011, Thomas Ball and Mooly Sagiv (Eds.). ACM, 271–282. https://doi.org/10.1145/1926385.1926417
Ralf Jung, Robbert Krebbers, Lars Birkedal, and Derek Dreyer. 2016. Higher-order ghost state. In Proceedings of the 21st ACM
    SIGPLAN International Conference on Functional Programming, ICFP 2016, Nara, Japan, September 18-22, 2016, Jacques
    Garrigue, Gabriele Keller, and Eijiro Sumii (Eds.). ACM, 256–269. https://doi.org/10.1145/2951913.2951943
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
    ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
    https://doi.org/10.1017/S0956796818000151
Ralf Jung, Rodolphe Lepigre, Gaurav Parthasarathy, Marianna Rapoport, Amin Timany, Derek Dreyer, and Bart Jacobs.
    2020. The future is ours: prophecy variables in separation logic. Proc. ACM Program. Lang. 4, POPL (2020), 45:1–45:32.
    https://doi.org/10.1145/3371113
Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
    Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning. In Proceedings of the 42nd Annual ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2015, Mumbai, India, January 15-17, 2015,
    Sriram K. Rajamani and David Walker (Eds.). ACM, 637–650. https://doi.org/10.1145/2676726.2676980
Naoki Kobayashi. 2006. A New Type System for Deadlock-Free Processes. In CONCUR 2006 - Concurrency Theory, 17th
    International Conference, CONCUR 2006, Bonn, Germany, August 27-30, 2006, Proceedings (Lecture Notes in Computer
    Science, Vol. 4137), Christel Baier and Holger Hermanns (Eds.). Springer, 233–247. https://doi.org/10.1007/11817949_16
Robbert Krebbers, Ralf Jung, Ales Bizjak, Jacques-Henri Jourdan, Derek Dreyer, and Lars Birkedal. 2017. The Essence
    of Higher-Order Concurrent Separation Logic. In Programming Languages and Systems - 26th European Symposium on
    Programming, ESOP 2017, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2017,
    Uppsala, Sweden, April 22-29, 2017, Proceedings (Lecture Notes in Computer Science, Vol. 10201), Hongseok Yang (Ed.).
    Springer, 696–723. https://doi.org/10.1007/978-3-662-54434-1_26
K. Rustan M. Leino, Peter Müller, and Jan Smans. 2010. Deadlock-Free Channels and Locks. In Programming Languages
    and Systems, 19th European Symposium on Programming, ESOP 2010, Held as Part of the Joint European Conferences on
    Theory and Practice of Software, ETAPS 2010, Paphos, Cyprus, March 20-28, 2010. Proceedings (Lecture Notes in Computer
    Science, Vol. 6012), Andrew D. Gordon (Ed.). Springer, 407–426. https://doi.org/10.1007/978-3-642-11957-6_22
Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: a semantic foundation
    for functional veriﬁcation of Rust programs with unsafe code. In PLDI ’22: 43rd ACM SIGPLAN International Conference
    on Programming Language Design and Implementation, San Diego, CA, USA, June 13 - 17, 2022, Ranjit Jhala and Isil Dillig
    (Eds.). ACM, 841–856. https://doi.org/10.1145/3519939.3523704
John M. Mellor-Crummey and Michael L. Scott. 1991. Algorithms for Scalable Synchronization on Shared-Memory Multi-
    processors. ACM Trans. Comput. Syst. 9, 1 (1991), 21–65. https://doi.org/10.1145/103727.103729
Ike Mulder and Robbert Krebbers. 2023. Proof Automation for Linearizability in Separation Logic. Proc. ACM Program.
    Lang. 7, OOPSLA1 (2023), 462–491. https://doi.org/10.1145/3586043
Peter W. O’Hearn. 2019. Separation logic. Commun. ACM 62, 2 (2019), 86–95. https://doi.org/10.1145/3211968
Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data Structures.
    In Computer Science Logic, 15th International Workshop, CSL 2001. 10th Annual Conference of the EACSL, Paris, France,
    September 10-13, 2001, Proceedings (Lecture Notes in Computer Science, Vol. 2142), Laurent Fribourg (Ed.). Springer, 1–19.
    https://doi.org/10.1007/3-540-44802-0_1
Tobias Reinhard and Bart Jacobs. 2021a. Ghost Signals: Verifying Termination of Busy Waiting - Verifying Termination
    of Busy Waiting. In Computer Aided Veriﬁcation - 33rd International Conference, CAV 2021, Virtual Event, July 20-23,
    2021, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 12760), Alexandra Silva and K. Rustan M. Leino (Eds.).
    Springer, 27–50. https://doi.org/10.1007/978-3-030-81688-9_2
Tobias Reinhard and Bart Jacobs. 2021b. Ghost Signals: Verifying Termination of Busy-Waiting (Technical Report).
    https://zenodo.org/records/4775181
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                  23


John C Reynolds. 2000. Intuitionistic reasoning about shared mutable data structure. Millennial perspectives in computer
   science 2, 1 (2000), 303–321.
Amr Sabry and Matthias Felleisen. 1992. Reasoning About Programs in Continuation-Passing Style. In Proceedings of the
   Conference on Lisp and Functional Programming, LFP 1992, San Francisco, California, USA, 22-24 June 1992, Jon L. White
   (Ed.). ACM, 288–298. https://doi.org/10.1145/141471.141563
Simon Spies, Lennard Gäher, Daniel Gratzer, Joseph Tassarotti, Robbert Krebbers, Derek Dreyer, and Lars Birkedal. 2021.
   Transﬁnite Iris: resolving an existential dilemma of step-indexed separation logic. In PLDI ’21: 42nd ACM SIGPLAN
   International Conference on Programming Language Design and Implementation, Virtual Event, Canada, June 20-25, 2021,
   Stephen N. Freund and Eran Yahav (Eds.). ACM, 80–95. https://doi.org/10.1145/3453483.3454031
Simon Spies, Lennard Gäher, Joseph Tassarotti, Ralf Jung, Robbert Krebbers, Lars Birkedal, and Derek Dreyer. 2022.
   Later credits: resourceful reasoning for the later modality. Proc. ACM Program. Lang. 6, ICFP (2022), 283–311.
   https://doi.org/10.1145/3547631
Joseph Tassarotti, Ralf Jung, and Robert Harper. 2017. A Higher-Order Logic for Concurrent Termination-Preserving
   Reﬁnement. In Programming Languages and Systems - 26th European Symposium on Programming, ESOP 2017, Held
   as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2017, Uppsala, Sweden, April
   22-29, 2017, Proceedings (Lecture Notes in Computer Science, Vol. 10201), Hongseok Yang (Ed.). Springer, 909–936.
   https://doi.org/10.1007/978-3-662-54434-1_34
Amin Timany, Simon Oddershede Gregersen, Léo Stefanesco, Jonas Kastberg Hinrichsen, Léon Gondelman, Abel Nieto, and
   Lars Birkedal. 2024. Trillium: Higher-Order Concurrent and Distributed Separation Logic for Intensional Reﬁnement.
   Proc. ACM Program. Lang. POPL (2024).
Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2015. Featherweight VeriFast. Log. Methods Comput. Sci. 11, 3 (2015).
   https://doi.org/10.2168/LMCS-11(3:19)2015
24                                                                            Justus Fasse and Bart Jacobs


Appendices
A MODULAR PICKING OF DEGREES AND LEVELS
A.1 Unfair modules
All modules of a HeapLang< program are generally parameterized by some degrees among which
some order must hold. If we assume the dependency relation on modules forms a tree, we can
pick these degrees modularly as follows. Each module 𝑀 deﬁnes a local domain of degrees Δ𝑀 ⊆
Val, equipped with a well-founded order <Δ𝑀 . In deﬁning its local domain of degrees, a module
may refer to those of its dependencies. It also deﬁnes any named degrees relevant to clients as
elements of that local domain. For a client to obtain a module’s code (which includes the code of
its dependencies), it must supply a degree embedding 𝜖𝑀 , an order-preserving function that maps
the module’s local domain of degrees to the global universe of degrees Deg.
    Instantiating the degrees. Recall that the example client program (Figure 7 in the main text)
is parameterized by the degree 𝛿 3 of the call permission expected by the lock module’s acquire
implementation, both when it is invoked and after it invokes its 𝜂 argument, as well as by degrees
𝛿 1 and 𝛿 2 such that 𝛿 3 < 𝛿 2 < 𝛿 1 .
    Let’s apply this approach to our example program (Figure 7 in the main text). The spinlock
module simply deﬁnes ΔLK = {0} with < ΔLK = ∅. It deﬁnes named degree ⊤LK = 0. The client
program deﬁnes its ΔC = {0} × ΔLK ∪ {(1, 0), (2, 0)}, ordered lexicographically. It also deﬁnes
named degree ⊤C , the degree of the call permission it needs to run, as equal to (2, 0). Given a
degree embedding 𝜖C , the client module builds its code by ﬁrst obtaining the code for the lock
module by passing embedding 𝜖LK = 𝜆𝛿. 𝜖C ((0, 𝛿)) and then instantiating its own code with 𝛿 1 =
𝜖C ((2, 0)), 𝛿 2 = 𝜖C ((1, 0)), 𝛿 3 = 𝜖C ((0, ⊤LK )).
    We can now use the client program’s local order <ΔC as the order on Deg and instantiate the
client program with 𝜖C = 𝜆𝛿. 𝛿 to obtain fully instantiated HeapLang< code that we can run, start-
ing with a call permission of degree ⊤C .
    Instantiating the levels. We can apply the exact same approach to modularly determine a pro-
gram’s levels: LC = {0} × LLK ∪ {(0, 0), (1, 0)}, ordered lexicographically, with l1 = 𝜖C ((0, 0)) and
⊤C = (1, 0). The client program requires that the caller’s obligations are above (or equal to) ⊤C .

A.2   Fair modules
Instantiating the degrees. In Section 6 of the main text we discuss modular programming of fair
modules. Since in the case of fair modules, call permissions ﬂow from the client to the module, then
back to the client’s 𝜂, and then ﬁnally back to the module, we extend the approach for modularly
determining a program’s degrees to support this. A fair blocking module’s local domain of degrees
                                                                         eta , a subset of Val equipped
is no longer ﬁxed; it now depends on the client’s eta domain of degrees Δ𝑀
with a well-founded order as well as a distinguished top element and bottom element. Given a
client’s eta domain, the module provides a local domain as well as an embedding from the eta
domain into the local domain. The client then provides an embedding of the local domain into the
global universe to obtain the module’s code, as before.
   Applying this approach to the ticketlock of Section 6.1 in the main text:
      • The ticketlock module is paramterized by the client’s eta domain of degrees Δ𝐶eta with
        named degrees ⊤𝐶eta and ⊥𝐶eta
      • The module deﬁnes its module-local degrees Δ𝑀 , {0} × Δ𝐶eta ∪ {(1, 0)}, ordered lexico-
        graphically. The named degree ⊤𝑀 = ⊤TL ( = 𝛿 in Section 6.1 of the main text) = (1, 0).
      • Additionally, the module deﬁnes the embedding 𝜖𝑀 , 𝜆𝛿. (0, 𝛿).
      • Finally, the client provides the embedding 𝜖𝐶 into the universe of degrees.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules   25


Thus 𝛿 and ⊤eta in lower 𝛿 into !(lk.next) - !(lk.owner) times ⊤eta refer to 𝜖𝐶 (⊤TL ) and
𝜖𝐶 (𝜖𝑀 (⊤𝐶eta )), respectively.

B HEAPLANG< : A TERMINATING LANGUAGE
B.1 Absence of infinite fair executions
We prove Theorem 2.1 of the main text. Due to the setup’s similarity, the proof is similar to that
of Reinhard and Jacobs [2021a,b].
  Theorem B.1 (Absence of infinite fair executions). A HeapLang< program of the form 𝑒; Finish
does not have inﬁnite fair executions.
   Proof. By contradiction. Thus, throughout this section—including the auxiliary deﬁnitions and
lemma below—we assume an inﬁnite fair execution of a HeapLang< program 𝑒; Finish, i.e. an
inﬁnite sequence of machine conﬁgurations related by machine steps where, if in a conﬁguration
at index 𝑖 a thread 𝜃 has not ﬁnished, then at some index 𝑗 ≥ 𝑖 that thread takes a step. Additionally,
let 𝑆 ∞ be the set of signals Expect ed inﬁnitely often in this execution.
   Deﬁnition B.2 (Program order graph). We construct the inﬁnite program order graph (in fact, a
tree) as follows. Each step in the inﬁnite sequence, identiﬁed by its position 𝑖, corresponds to a
node in the tree. Each node is connected with a directed edge to the next step of the same thread,
and if the step is a fork, to the ﬁrst step of the child.
   Deﬁnition B.3 (Path fuel). Consider an inﬁnite path in the program order graph starting at some
index 𝑖 that never Expects a signal in 𝑆 ∞ . We deﬁne the path fuel for this path at each machine
step 𝑗 ≥ 𝑖 as the multiset of degrees obtained by combining the path’s multiset of call permissions
at conﬁguration 𝑗 with 𝑛 − 𝑗 + 1 copies of degree 𝛿 for each of the path’s expect permissions at
conﬁguration 𝑗 for signal 𝑠 at degree 𝛿 where signal 𝑠 is last Expect ed on the path at step 𝑛:
          PF( 𝑗 ) , 𝜎.CallPerms(𝜃 ) ⊎
                                                  (
                               Ú                      [(𝑛 − 𝑗 + 1) · 𝛿]   𝑠 last Expect ed at step 𝑛
                     (𝑠,𝛿 ) ∈𝜎 .ExpectPerms(𝜃 )
                                                      ∅                   otherwise, i.e. 𝑠 ∈ 𝑆 ∞
             where
                𝜃 is the thread id of the ﬁrst step on the path whose index is not less than 𝑗 .
                𝜎 is the machine state before step 𝑗 .
Notice that 𝑛 − 𝑗 + 1 constitutes an upper bound on the number of times the path will Expect this
expect permission. Notice that if the path owns any expect permissions for signals in 𝑆 ∞ , they are
ignored, since, by our assumption, the path will not use them anyway.
  Like other multisets, we order path fuel values by the well-founded Dershowitz-Manna or-
der [Dershowitz and Manna 1979; Coupet-Grimal and Delobel 2006].
   Lemma B.4 (Finite paths). A path that never Expects a signal in 𝑆 ∞ is ﬁnite.
  Proof. Suppose otherwise. Let 𝐹 be the set of nodes on the path that are function calls. Since
HeapLang< ’s only source of divergence are function calls, 𝐹 must be inﬁnite. All steps in 𝐹 decrease
the path fuel due to function calls consuming a call permission. All steps—on or oﬀ the path—also
decrease the path fuel or leave it unchanged. Thus, the inﬁnite path implies an inﬁnite descending
chain. A contradiction.                                                                             
  We now continue the proof of Theorem 2.1 by case splitting on whether the execution Expect s
any signals inﬁnitely often or not.
26                                                                                Justus Fasse and Bart Jacobs


                                    let x = ref true in
                                    let l 1 = ref NewSignal 0 in
                                    let y = ref true in
                                    let l 2 = ref NewSignal 0 in
        acquire y                                      acquire x
          (𝝀.SetSignal !l 1 ; Expect !l 2 𝛿 ;            (𝝀.SetSignal !l 2 ; Expect !l 1 𝛿 ;
           l 1 ≔ NewSignal 0) (𝝀.())                      l 2 ≔ NewSignal 0) (𝝀.())
        release x ()                                   release y ()

Fig. 18. Livelocked program admitting infinite fair executions given the unsound step-rule for Expect . Here
we assume that acquire is the simple spinlock (hence the degree 0).


Case 1: 𝑆 ∞ = ∅. By Lemma B.4, all paths of the program order graph must be ﬁnite. However,
applying Kőnig’s lemma we conclude that the inﬁnite program order graph of the inﬁnite fair
execution must have at least one inﬁnitely long path. A contradiction.
Case 2: 𝑆 ∞ ≠ ∅. Let 𝑠 min ∈ 𝑆 ∞ be a signal of minimal level in 𝑆 ∞ . Such a signal must exist since
the universe of levels is well-founded. Let 𝑝 be the path that carries the obligation to set 𝑠 min i.e.
the path constituted by the set of steps by a thread while holding the obligation for 𝑠 min . This
path must be inﬁnite: because signal 𝑠 min is Expect ed inﬁnitely often it can never be set. Thus, 𝑝
can never Finish. Moreover, since the execution is fair, the thread holding 𝑠 min ’s obligation will
always eventually be scheduled. Finally, recall that a thread can only Expect a signal whose level
is below the levels of the obligations held by that thread. Holding the obligation for 𝑠 min , whose
level is minimal in 𝑆 ∞ , 𝑝 can never Expect a signal in 𝑆 ∞ . Applying Lemma B.4 again, we arrive
at the desired contradiction.                                                                       

B.2 Unsound Expect counterexample
Recall the unsound step-rule for Expect in Section 2 of the main text:
                        UnsoundExpect
                        𝜎.Signals(𝑠) = (l, false)        l ≺ 𝜎.Obligations(𝜃 )
                          Expect 𝜃 𝑠 𝛿, 𝜎 →
                                          − h (), 𝜎 : CallPerms[𝜃 ⊎←↪ {𝛿}]
                                            𝜃

Figure 18 gives a counterexample using UnsoundExpect i.e. a program which admits an inﬁnite
fair execution.
   The left (main) thread holds lock 𝑥 while the right thread (forkee) holds lock 𝑦. Both threads try
to acquire the other thread’s lock before releasing their own, resulting in a livelock.
   Notice that the issue is not only that UnsoundExpect is allowed to pick the degree at which to
generate a call permission arbitrarily. Additionally, the two threads could “juggle” obligations by
spawning and destroying signals arbitrarily. This is prevented by requiring an expect permission
in order to Expect .

C    PROVING SAFETY FOR HEAPLANG< PROGRAMS
C.1 Weakest precondition
We adapt the weakest precondition of Iris 4.0 [Spies et al. 2022; Iris contributors 2024] in Figure 19.
Important changes:
     • We assume a ﬁxed state interpretation (Figure 20) suitable for HeapLang< .
     • We always prove non-stuckness.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                    27



      wp(𝑆, 𝛷 𝐹 , 𝑠) , 𝜇wp rec. 𝜆E, 𝑒 , 𝜃 ,𝛷.
                        (∃𝑣. expr to val(𝑒) = 𝑣 ∧ |⇛E 𝛷 (𝑣)) ∨
                        

                                                                                           𝜅®
                                                                                                  ∗
                          expr to val(𝑒) = ⊥ ∧ ∀𝜎, 𝑛𝑠 , 𝜅®, 𝜅®′, 𝑛𝑡 . 𝑆 (𝜎, 𝑛𝑠 , 𝜅® ++ 𝜅®′, 𝑛𝑡 ) E ≡−   ∅

                              (𝑠 = NotStuck ⇒ red(𝑒, 𝜎 , 𝜃 )) ∗ ∀𝑒 ′ , 𝜎 ′ , 𝑒®. (𝑒, 𝜎 −→t 𝑒 ′ , 𝜎 ′ , 𝑒®) −∗ £ (𝑛 ⊲ (𝑛𝑠 ) + 1) −∗
                                                                                        𝜃
                                                                                            𝑒 |) ∗ wp rec(E, 𝑒 ′ , 𝛷 , 𝜃 ) ∗
                                    (|⇛∅ ⊲ |⇛∅ )𝑛⊲ (𝑛𝑠 )+1 ∅ |⇛E 𝑆 (𝜎 ′ , 𝑛𝑠 + 1, 𝜅®′, 𝑛 + |®
                                                                               
                                              ∗   wp rec(⊤, 𝑒 ′′ ,𝛷 𝐹 , 𝜃 ′ )
                                           (𝜃 ′,𝑒 ′′ ) ∈𝑒®

wp𝑆;𝛷 𝐹 𝑒 {𝑣. 𝑃 } , wp(𝑆, 𝛷 𝐹 , 𝑠) (E, 𝑒 , 𝜃 , 𝜆𝑣. 𝑃)
  𝑠;E , 𝜃


Fig. 19. We adapt Iris’ weakest precondition [Iris contributors 2024, p. 35], specializing it to HeapLang< . We
add a notion of thread ids that is built into the operational semantics to support our auxiliary constructs.
We fix 𝑠 = NotStuck, 𝑛 ⊲ (𝑛𝑠 ) = 0, and the state interpretation 𝑆 of Figure 20.



      • Our deﬁnition of reducibility red(𝑒, 𝜎, 𝜃 ) (Figure 21) accepts None, which we use to support
        the exit command. Notice that red(𝑒, 𝜎, 𝜃 ) admits exit and that None—the expression
        stepped to by exit—vacuously satisﬁes the weakest precondition (see also the proof rule
        of exit in Figure 22).

C.2 State interpretation
Our ﬁxed state interpretation (Figure 20) to tie the state of Figure 41 to the proof state follows
the general pattern of tying the physical state to the ghost state of Iris. Iris’ authoritative cam-
era [Iris contributors 2024, 4.8] is used to store the authoritative fragment in the state interpre-
tation, itself kept by the weakest precondition. This still permits fragments to be given out for
modular proofs. Nevertheless, the authoritative part in the state interpretation makes sure that at
every step the ghost state matches the physical state.

C.3    Proof rules for HeapLang< extensions
Figure 22 gives proof rules for our extensions of HeapLang. They directly reﬂect the step rules of
the operational semantics of these extensions (main text Figure 45, reproduced in this appendix in
Figure 45) and can be derived from the weakest precondition (Figure 19).

C.4    Proving deref
Figure 23 proves deref against the speciﬁcation given in Section 4 of the main text.

C.5 Big-step weakest precondition
To reason about big-steps (see Section G), we deﬁne the big-step weakest precondition Figure 25.
This weakest precondition admits the expected reasoning rules (Figure 26).

C.6    Inlined spinlock
Figure 27 shows a simple HeapLang< program with the bodies of acquire and release inlined.
28                                                                                                     Justus Fasse and Bart Jacobs


                                              fin                            𝛾Heap
𝑆 (𝜎, 𝑛𝑠 , 𝜅®, 𝑛𝑡 ) , •𝜎.Heap : Auth(Loc −⇀ (Frac × Ag(Val))                         ∗                                     cf. Jung et al. [2018]
                                       𝛾StepCount
                  •𝑛𝑠 : Mono(N)           ∗                                                                    cf. Matsushita et al. [2022]
                              Prophs                       
                    ∃Π. •Π            ∗ dom(Π) = 𝜎.Prophs ∗ ∗                                                                  Jung et al. [2020]
                          ∀{𝑝 ← vs} ∈ Π. vs = filter(𝑝, 𝜅))
                                                        ® ∗
                  Our extensions for HeapLang< :
                                                   fin                         𝛾HeapA
                   •𝜎.HeapA : Auth(Loc −⇀ (Frac × Ag(Val)))                              ∗
                                                          fin                   𝛾Signals
                   •𝜎.Signals : Auth(SigLoc −⇀ Ex(Lev × B))                                ∗
                                                           fin                                              𝛾Obligations
                   •𝜎.Obligations : Auth(Θ −⇀ Ex(Multiset(SigLoc × Lev)))                                                  ∗
                                                         fin                    𝛾CallPerms
                   •𝜎.CallPerms : Auth(Θ −⇀ Multiset(Deg))                                     ∗
                                                               fin                           𝛾ExpectPerms
                   •𝜎.ExpectPerms : Auth(Θ −⇀ Set(SigLoc × Deg))

                                      Fig. 20. Extended state interpretation.

                                               𝜅®                                              𝜖
                        ∃®
                         𝜅, 𝑒 2 , 𝜎2, 𝑒®. 𝑒, 𝜎 →
                                               − t 𝑒 2, 𝜎2, 𝑒®                       𝑒, 𝜎 →
                                                                                          − t None
                                               𝜃                                               𝜃
                                   red(𝑒, 𝜎, 𝜃 )                                         red(𝑒, 𝜎, 𝜃 )

                          Fig. 21. Adaption of red(𝑒, 𝜎) to admit the exit command.


                                                                       obs𝜃 (𝑂) ∗
                ⊲(∀𝑠. sig(𝑠, l, false) ∗ obs𝜃 (𝑂 ∪ {(𝑠, l)}) −∗ Φ(𝑠)) ⊢ wp NewSignal 𝜃 l {Φ}
                              sig(𝑠, l, false) ∗ obs𝜃 (𝑂 ∪ {(𝑠, l)}) ∗
                                 ⊲(sig(𝑠, l, true) ∗ obs𝜃 (𝑂) −∗ Φ())) ⊢ wp SetSignal 𝜃 𝑠 {Φ}
                                             CP 𝜃 ∗ obs𝜃 (𝑂) ∗ EP 𝜃 ∗
                                                                 
⊲ ∀𝜃 ′ . obs𝜃 (𝑂 \ 𝑠) ∗ obs𝜃 ′ (𝑠) ∗ CP 𝜃 ∗ CP 𝜃 ′ ∗ EP 𝜃 ∗ EP 𝜃 ′ ≡−
                                                                             ∗
                                               ⊲ Φ() ∗ ⊲ wp 𝑒 {obs𝜃 ′ (∅)} ⊢ wp fork 𝑠 𝑒 {Φ}
                                                                     True ∗ ⊲ Φ(𝜃 ) ⊢ wp𝜃 CurrentThread {Φ}
                                                                     obs(∅)𝜃 ∗ ⊲ Φ ⊢ wp𝜃 Finish {Φ}
                                                                     wp⇓ 𝑒 {𝑥 . Φ} ⊢ wp h𝑒i {𝑥 . Φ}
                          cp(0) ∗ ⊲(wp 𝑒 [(𝝁 e f x. 𝑒)/f ] [𝑣/x] {Φ}) ⊢ wp (𝝁 v f x. 𝑒) 𝑣 {Φ}
                                      cp𝜃 ′ (𝛿) ∗ ⊲(cp𝜃 ′ ( [𝑛 · 𝛿 ′ ]) −∗ Φ) ⊢ wp lower 𝛿 to 𝑛 times 𝛿 ′ at 𝜃 ′ {Φ}
     cp𝜃 ′ (𝛿) ∗ sig(𝑠, _, _) ∗ 𝛿 ′ < 𝛿 ∗ ⊲(cp𝜃 ′ (𝛿) −∗ ep𝜃 ′ (𝑠, 𝛿 ′ ) −∗ Φ) ⊢ wp NewExpectPerm 𝜃 ′ 𝑠 𝛿 𝛿 ′ {Φ}
sig(𝑠, l, false) ∗ obs𝜃 ′ (𝑂) ∗ l ≺ 𝑂 ∗ ep𝜃 ′ (𝑠, 𝛿) ∗ ⊲(cp𝜃 ′ (𝛿) −∗ Φ) ⊢ wp Expect 𝜃 ′ 𝑠 𝛿 {Φ}
                                                                             True ⊢ wp exit {False}

                                Fig. 22. Proof rules for HeapLang< ’s extensions.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                  29

                                                                                     
                                 (ℓ ↦→ 𝑤) −∗ wp ∅ ! ℓ {𝑣. Φ(𝑣) ∗ ℓ ↦→ 𝑤 }
                                                                                     wp-frame (not shown)
                     (ℓ ↦→ 𝑤 ∗ VSclose ) −∗ wp ∅ ! ℓ {𝑣. Φ(𝑣) ∗ ℓ ↦→ 𝑤 ∗ VSclose }
                                                                                    wp-mono (not shown)
                       (ℓ ↦→ 𝑤 ∗ VSclose ) −∗ wp ∅ ! ℓ 𝑣. Φ(𝑣) ∗ ∅ |⇛⊤ True
                                                                                     fup-frame (not shown)
                            (ℓ ↦→ 𝑤 ∗ VSclose ) −∗ wp ∅ ! ℓ 𝑣. ∅ |⇛⊤ Φ(𝑣)
                                                                                      apply VSopen
                         (VSopen ∗ VSclose ) −∗ ⊤ |⇛∅ wp ∅ ! ℓ 𝑣. ∅ |⇛⊤ Φ(𝑣)
                                                                                        wp-atomic
                               (VSopen ∗ VSclose ) −∗ wp ! ℓ {𝑣. Φ(𝑣)}
                                                                                         pure step
                             (VSopen ∗ VSclose ) −∗ wp deref ℓ {𝑣. Φ(𝑣)}


                              VSopen
                                      } |           {z      ∗
                       {( ⊤ |⇛∅ ℓ ↦→ 𝑤) ∗ (ℓ ↦→ 𝑤 ∅ ≡− ⊤ Φ(𝑤)) } deref ℓ {𝑣. Φ(𝑣)}
                        |      {z                           }
                                                        VSclose
                                                                                                        hoare-def




                     Fig. 23. Proof of deref (main text, Section 4) against its specification.

                                                 BigStep
                                                            𝜖
                                                        − ∗t- (𝑣, 𝜎 ′ , 𝜖)
                                                 (𝑒, 𝜎) →
                                                            𝜃
                                                    (𝑒, 𝜎) ⇓𝜃 (𝑣, 𝜎 ′ )

Fig. 24. Definition of big-step relation as finite number (∗ ) of modified thread steps (t- ) to a value by the
                                                    𝜖
same thread. The modified thread-step relation −   →t- uses duplicates of the regular thread- and head-step
                                                        𝜃
relations but disallows forks and atomic blocks.


                                   wp⇓ , 𝜆E, 𝑒, 𝛷.∀𝜎, 𝑛𝑠 , 𝜅®, 𝑛𝑡 . 𝑆 (𝜎, 𝑛𝑠 , 𝜅,
                                                                               ® 𝑛𝑡 ) E ≡−
                                            ∃𝜎 ′, 𝑣. p𝑒, 𝜎 ⇓ 𝑣, 𝜎 ′ q ∗ 𝑆 (𝜎 ′ , 𝑛𝑠 , 𝜅,
                                                                                             ∗  E
                                                                                      ® 𝑛𝑡 ) ∗ 𝛷 (𝑣)
                        wp⇓E 𝑒 {𝑣. 𝑃 } , wp⇓ (E, 𝑒, 𝜆𝑣. 𝑃)

Fig. 25. Our weakest precondition for big-step evaluation. Unlike Iris’ general weakest precondi-
tion [Iris contributors 2024, p. 35], the big-step weakest precondition is specialized to HeapLang< and in
particular a fixed state interpretation. Moreover, it directly uses the big-step relation defined on a subset of
HeapLang< that notably excludes the fork command. Finally, wp⇓ does not allow stuck computations.

                                               
                                 Big-step-atomic
                                            ⇓
                                  E1 |⇛E2 wp E2 𝑒    𝑥 . E2 |⇛E1 𝑃 ⊢ wp⇓E1 𝑒 {𝑥 . 𝑃 }

Big-step-bind
                         𝐾 is a context                                              Big-step-AtomicBlock
       n                                   o                                             ⇓
                                                                                     wp E 𝑒 {𝑥 . 𝑃 } ⊢ wp E h𝑒i {𝑥 . 𝑃 }
 wp⇓E 𝑒 𝑥 . wp⇓E 𝐾 (val to expr(𝑥)) {𝑦. 𝑃 } ⊢ wp⇓E 𝐾 (𝑒) {𝑦. 𝑃 }


Fig. 26. Reasoning rules for wp⇓ . Here, “context” really refers to a list of HeapLang< -specific context items
(cf. [Iris contributors 2024, p. 36]).
30                                                                                               Justus Fasse and Bart Jacobs


                     {obs1 (∅) ∗ cp(1)}
                 let lk = ref true in (* init. locked *)
                 let s = NewSignal 0 in
                 NewExpectPerm s 1 0;
                     {obs({(𝑠, 0)}) ∗ lk ↦→ true ∗ sig(𝑠, 0, false) ∗ ep1 (𝑠, 0) ∗ tok𝛾 }
                                                                                                       N
                     𝐼 , ∃𝑏. lk ↦→ 𝑏 ∗ (𝑏 = true ∗ (sig(𝑠, 0, false) ∨ tok𝛾 )) ∨ (𝑏 = false ∗ 𝑅)
                          N
                     {𝐼       ∗ 𝑅 ∗ tok𝛾 }
                 (* forker: keep obligation *)
                                                                                  N
                                             {obs2 (∅) ∗ ep2 (𝑠, 0) ∗ tok𝛾 ∗ 𝐼 }
                                             (* inlined acquire lk 𝜂 𝜅 *)
                                             while not
                                                                                  N
                               N             {obs2 (∅) ∗ ep2 (𝑠, 0) ∗ tok𝛾 ∗ 𝐼 }
 {obs1 ({(𝑠, 0)}) ∗ 𝑅 ∗ 𝐼 }
                                                  {obs2 (∅) ∗ ep2 (𝑠, 0) ∗ tok𝛾 ∗ 𝐼 } ∅
 (* inlined release lk 𝜅 *)
                                                                        z }| {              z}|{
                                                                          𝜂                  𝜅
   {obs1 ({(𝑠, 0)}) ∗ 𝑅 ∗ 𝐼 } ∅
                                                  h if !lk then Expect s else () ;
                          z     }|     {
                                 𝜅

                                                                                                                           
                                                    CAS lk false true i
 h lk ≔ false; SetSignal s i                        
                                                                                                                             
                                                                                                                              
    {obs1 (∅) ∗ lk ↦→ false ∗ 𝑅} ∅                   𝑣. lk ↦→ true ∗ (𝑣 = false ∗ 𝑏 = true ∗ sig(𝑠, 0, false) ∗ cp2 (0)) ∨
                                                                                                                             
                                                                                                                              
                                                                                                                             
                                                                        (𝑣 = true ∗ 𝑏 = false ∗ 𝑅)
    {obs1 (∅) ∗ 𝐼 } ∅                                ∗ ep (𝑠, 0) ∗ tok𝛾                                                      
                 N                                         2                                                                 ∅
 {obs1 (∅) ∗ 𝐼       }
                                                                          z }| { z                  }|          {
                                                                              acquired                retry
                                                                                                                        N
                                             {𝑣. obs2 (∅) ∗ ep2 (𝑠, 0) ∗ (𝑣 = true ∗ 𝑅 ∨(𝑣 = false ∗ cp(0) ∗ tok𝛾 )) ∗ 𝐼 }
                                             do () done
                                                             N
                                             {obs2 (∅) ∗ 𝐼       ∗ 𝑅}

Fig. 27. Inlined spinlock acquire and release . Recall that compare-and-swap (CAS) returns true if the
                                                                                    𝛾
swap is succesfully executed and false otherwise.). We use the shorthand tok𝛾 , ex() to represent an
exclusive ghost token.




D MOTIVATING EXAMPLE
We give a proof outline for the instrumented (HeapLang< ) version of the motivating example. The
explanation proceeds in four steps:
   (1) We show the proof outline for the spinlock operations against the general unfair speciﬁca-
       tion given in the paper.
   (2) We show the client’s invariant and highlight key aspects of it.
   (3) We show proof outlines for the client’s auxiliary functions 𝜂 and 𝜅.
   (4) We explain how the invariant and thread-local resources let us derive the necessary total
       correctness logically atomic updates to invoke acquire and release .

D.1 Spinlock proof
First, Figures 28b, 29 and 30 show proof outlines for the instrumented spinlock against our total
correctness unfair lock speciﬁcation.

D.2   Client invariant
Figure 31 shows the (client) invariant we use to verify the instrumented motivating example.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules         31


                                                               let new_lock = 𝝁 e _ _ _.
                                                                   {True}
                                                                   ref false
                                                                   {ℓ. ℓ ↦→ false}
           𝐿(𝑥, 𝑏) , 𝑥 ↦→ 𝑏                                        {ℓ. 𝐿(ℓ, false)}
                  (a) Lock predicate for spinlock.                       (b) Create new spinlock.

                                   Fig. 28. Spinlock representation and creation.


                       let release = 𝝁 e lk 𝜅 .
                         {cp(⊤SL ) ∗ TAU} where TAU = ⊤SL h𝐿(lk, true) | 𝐿(lk, false)i l∅
                                                                                  𝜅
                          h
                                                      n                       o
                          {TAU}
                             {𝐿(lk, true) ∗ (wp⇓ 𝜅 () 𝐿(lk, false) ∅ ≡
                                                                        ∗
                                                                      − ⊤ Φ) )} ∅



                                                                       ∗ ∗
                             𝜅 ();
                             {𝐿(lk, true) ∗ obs(𝑂) ∗ l ≺ 𝑂 ∗ (𝐿(lk, false) ∅ ≡
                                                                             − ⊤ Φ)} ∅
                             {lk ↦→ true ∗ obs(𝑂) ∗ (𝐿(lk, false) ∅ ≡− ⊤ Φ)} ∅
                             lk ≔ false
                             {lk ↦→ false ∗ obs(𝑂) ∗ (𝐿(lk, false) ∅ ≡
                                                                       ∗∗
                                                                      − ⊤ Φ)} ∅
                             {𝐿(lk, false) ∗ obs(𝑂) ∗ (𝐿(lk, false) ∅ ≡
                                                                      − ⊤ Φ)} ∅
                             {Φ ∗ obs(𝑂)} ∅
                          i
                          {Φ ∗ obs(𝑂) ∗ l ≺ 𝑂 }

                                              Fig. 29. Release spinlock.


   The protocol enforced by the invariant encompasses two aspects controlled by 𝑏 and 𝑑:
      • Progress: When the lock is held (𝑏 = true), there exists an unset signal to justify busy-
                                                                                          1/2
         waiting. Speciﬁcally, if the left or middle thread own the lock (𝛾 o ↦−→ LM) the middle thread
                                                                                                       1/2
        must hold the obligation for signal 𝑠 2 . If the right thread owns the lock 𝛾 o ↦−→ R it must
        hold the obligation for signal 𝑠 3 .
      • Handoﬀ: When the ﬂag f has been unset (𝑑 = false) the middle thread can complete the
        handoﬀ between itself and the left thread—obtaining ownership.
                                                               𝛾
   This invariant uses the shorthand tok𝛾 , ex() for exclusive tokens again. Moreover, we use
                                                                                  𝛾
the oneshot camera [Jung et al. 2018] with the shorthands pending𝛾 , pending , and shot(𝑣)𝛾 ,
          𝛾
 shot(𝑣) . The exclusive resource pending𝛾 is required to set the value to 𝑣 and obtain the persis-
tent resource shot(𝑣)𝛾 . This ensure that l1 and l2 can only be set once to a signal.

D.3    Client-specific auxiliary code
      • Figure 32 shows the proof outline for the auxiliary code of the left thread’s 𝜅 (acquire ).
      • Figure 33 shows the proof outline for the auxiliary code of the left thread’s 𝜂 (acquire ).
      • Figure 34 show the proof outline for the auxiliary of the middle thread’s 𝜅 (release ). This
        is the 𝜅 for the release matching the lock acquisition by the left thread.
32                                                                                                       Justus Fasse and Bart Jacobs


  let acquire = 𝝁 e acq lk 𝜂 𝜅 .
                                                                                𝜂
     {cp(⊤SL ) ∗ obs(𝑂) ∗ l ≺ 𝑂 ∗ TAU} where TAU = l⊤SL h𝑏 ։ {false} . 𝐿(lk, 𝑏) | 𝐿(lk, true) ∗ 𝑏 = falsei ∅
                                                                                                        𝜅
     {cp(⊤SL ) ∗ obs(𝑂) ∗ l ≺ 𝑂 ∗ TAU ∗ ⊲((cp(⊤SL ) ∗ TAU) −∗ wp acq lk 𝜂 𝜅 {Φ})}
     lower ⊤SL into 1 times 0
     {cp(0) ∗ obs(𝑂) ∗ l ≺ 𝑂 ∗ TAU ∗ ⊲((cp(⊤SL ) ∗ TAU) −∗ wp acq lk 𝜂 𝜅 {Φ})}
     if
     h
     {TAU}
       
                                                                                      
                                                                                       
       
       
         ∃𝑏. 𝐿(lk, 𝑏) ∗                      n                    o                    
                                                                                       
       
       
       
                                      ⇓
         (((𝑏 = false ∗ obs(𝑂)) −∗ wp ∅ 𝜅 () (𝐿(lk, true) ∅ ≡
                                           n
                                                            − ⊤ Φ) ) ∧
                                                                           ∗       o
                                                                                       
                                                                                       
                                                                                       
       
       
        ((𝑏 = true ∗ obs(𝑂)) −∗ wp ∅ 𝜂 () cp(⊤SL ) ∗ obs(𝑂) ∗ (𝐿(lk, 𝑏) ∅ ≡
       
        (if !lk then
                                    ⇓                                                  
                                                                           − ⊤ TAU) )) 
                                                                                       
                                                                                       ∅     ∗
                                                    ∗
          𝜂 ()
          {cp(⊤SL ) ∗ obs(𝑂) ∗ (𝐿(lk, true) ∅ ≡
                                              − ⊤ TAU)} ∅
        else


                          ∗
            𝜅 ()
          {𝐿(lk, true) ∅ ≡
                         − ⊤ Φ} ∅
        );
        CAS lk false true
     {𝑣. (𝑣 = true ∗ Φ) ∨ (𝑣 = false ∗ cp(⊤SL ) ∗ obs(𝑂) ∗ TAU)}
     i
     then
          {Φ}
       () (* return *)
     else
          {cp(0) ∗ cp(⊤SL ) ∗ obs(𝑂) ∗ l ≺ 𝑂 ∗ TAU ∗ ((cp(⊤SL ) ∗ TAU) −∗ wp acq lk 𝜂 𝜅 {Φ})}
        acq lk 𝜂 _ 𝜅
          {Φ}

                                                    Fig. 30. Acquire spinlock.


𝐼 (𝑙𝑘, 𝑓 , 𝑙 2, 𝑙 3, 𝛾 o, 𝛾 h, 𝛾𝑙2 , 𝛾𝑙3 ) = ∃𝑏, 𝑑, 𝑠 2, 𝑠 3 . 𝐿(lk, 𝑏) ∗ 𝑓 ↦→ 𝑑 ∗ 𝑙 2 ↦→ 𝑠 2 ∗ 𝑙 3 ↦→ 𝑠 3 ∗

                                        ©                                                                             ª
                                           (𝑏 = false ∗ 𝛾 o ↦→ None) ∨
                                        ­                                                                             ®
                                        ­ ©                © (𝛾 o ↦−→ LM ∗ sig(𝑠 2, 0, false) ∗ shot(𝑠 2 )𝛾l2 ) ∨ ª ª ® ∗
                                                                    1/2


                                        ­ ­ (𝑏 = true ∗ ­                                                         ® ® ®
                    Progress
                                                                    1/2

                                        « «                « (𝛾 o ↦−→ R ∗ sig(𝑠 3 , 0, false) ∗ shot(𝑠 3 )𝛾l3 )   ¬ ¬ ¬
                                          𝑑 = true ∨                                                ª
                                        ©
                    Handoﬀ              ­                               1/2
                                                                                                             ®
                                            𝑑 = false ∗ tok𝛾h ∨ 𝛾 o ↦−→ LM ∗ obs2 ({(𝑠 2 , 0)})
                                        «                                                                    ¬

                                                                                                                               𝛾
Fig. 31. Inspired by the appendix of Spies et al. [2022], we use the shorthands tok𝛾name , ex() name ,
                           𝛾                                   𝛾
pending𝛾name , pending name , and shot(𝑣)𝛾name , shot(𝑣) name . The exclusive and one-shot cameras are
described by Jung et al. [2018] and in Iris’ technical reference [Iris contributors 2024]. Thread 1 is the left
thread, thread 2 the middle thread and thread 3 the right thread.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                     33

                                                                ⇓
                                       {𝑙 2 ↦→ _ ∗ obs2 (∅)} ∅
                                       l 2 ≔ NewSignal 2 0
                                                                                          ⇓
                                        {𝑙 2 ↦→ 𝑠 2 ∗ obs2 ((𝑠 2, 0) ∗ sig(𝑠 2, false, 0)} ∅

                           Fig. 32. Big-step weakest precondition of the left thread’s 𝜅.


                                                                                                                   ⇓
           {sig(𝑠 3, 0, false) ∗ 𝑙 3 ↦→ 𝑠 3 ∗ started ↦→ 𝑏 ∗ ((𝑏 = false ∗ cp(𝛿 2 )) ∨ (𝑏 = true ∗ ep(𝑠 3, 𝛿 3 )))} ∅
           if not !started then (
                                       ⇓
           {started ↦→ 𝑏 ∗ cp(𝛿 2 )} ∅
              NewExpectPerm !l 3 𝛿 2 𝛿 3 ;
              started = true
                                              ⇓
           {started ↦→ true ∗ ep(𝑠 3, 𝛿 3 )} ∅
           );
                                                                               ⇓
           {sig(𝑠 3, false, 0) ∗ ep(𝑠 3, 𝛿 3 ) ∗ 𝑙 3 ↦→ 𝑠 3 ∗ started ↦→ true} ∅
           Expect !l 3
                                                                                          ⇓
           {cp(𝛿 3 ) ∗ sig(𝑠 3, false, 0) ∗ ep(𝑠 3, 𝛿 3 ) ∗ 𝑙 3 ↦→ 𝑠 3 ∗ started ↦→ true} ∅

                              Fig. 33. Big-step weakest precondition of left thread’s 𝜂.


                                                                                          ⇓
                                        {𝑙 2 ↦→ 𝑠 2 ∗ obs((𝑠 2, 0)) ∗ sig(𝑠 2, false, 0)} ∅
                                        SetSignal !l 2
                                                                                   ⇓
                                        {𝑙 2 ↦→ 𝑠 2 ∗ obs(∅) ∗ sig(𝑠 2, true, 0)} ∅

                            Fig. 34. Big-step weakest precondition of 𝜅 (middle thread)



   Notice that these do not yet correspond to the big-step weakest preconditions required for the
total correctness logically atomic update (TAU). What is missing are the linear view shift to close
the invariant.

D.4 Deriving the total correctness logically atomic update
Recall that TAU is deﬁned as greatest ﬁxpoint. We use gfp-intro to introduce it.
                                                     gfp-intro
                                                           𝑃 ⊢ 𝐹 (𝑃)
                                                      𝑃 ⊢ gfp(𝑃. 𝐹 (𝑃))

Thus, for acquire we’re looking for wait invariant resource WI such that:

                                           n                                                                o
                                      WI ⊢ ⊤\E |⇛∅ ∃𝑏. ⊲ 𝐿(lk, 𝑏) ∗
     ©
     ­
                                    ⇓
         ((𝑏 = true ∗ obs(𝑂)) −∗ wp ∅ 𝜂 () cp(⊤SL ) ∗ obs(𝑂) ∗ (𝐿(lk, true) ∅ ≡−
                                            n                       o                           ∗       WI)   )∧ ª
                                                                                                                 ®
                                                                          ∗
                                                                                                    ⊤\E

         ((𝑏 = false ∗ obs(𝑂)) −∗ wp⇓∅ 𝜅 () (𝐿(lk, true) ∅ ≡− ⊤\E Φ) )
     «                                                                                                           ¬
                                  𝜂                                                                                     gfp-intro
                      WI ⊢ l;𝑂
                           ⊤SL h𝑏 ։ {false} . 𝐿(lk, 𝑏) | 𝐿(lk, true) ∗ 𝑏 = false ⇛ Φi E
                                                       𝜅
34                                                                                                      Justus Fasse and Bart Jacobs


D.4.1 Left thread acquire . The client picks Φ and WI as follows:
                                               1/2
Φ , obs(∅) ∗ obs2 ({(𝑠 2, 0)}) ∗ 𝛾 o ↦−→ LM
           N
WI , 𝐼         ∗ pending𝛾l ∗ obs2 (∅) ∗ (∃𝑐. started ↦→ 𝑐 ∗ ((𝑐 = false ∗ cp(𝛿 2 )) ∨ (𝑐 = true ∗ ep(𝑠 3, 𝛿 3 )))
                           2

     Thus we derive acquire ’s TAU as follows:
                                         N
       • Atomic precondition: 𝐼        is part of WI. Opening the invariant we obtain (among other
         resources) ⊲ ∃𝑏. 𝐿(lk, 𝑏). Later and exists commute since B is inhabited giving us ⊲ 𝐿(lk, 𝑏).
       • 𝜂: To run 𝜂, the module must show that 𝑏 is true. Therefore the Progress part of the invariant
                                                                                                                1/2
         simpliﬁes and—given that WI includes pending𝛾l —the disjunct with 𝛾 o ↦−→ R must hold.
                                                              2
         At this point deriving the precondition of 𝜂 (Figure 33) is relatively straightforward.
         The local resources of WI can be established from the expect permission and the fact that
         started ↦→ true. Moreover, restoring 𝐼 is easy since 𝐼 ’s resources were not modiﬁed. Thus,
         given ⊲ 𝐿(lk, true) we can close the invariant again.
       • 𝜅: To run 𝜅, the module must show that 𝑏 is false. Its precondition (Figure 32) can be derived
         from the local resource obs2 (∅) of WI, and 𝑙 2 ↦→ _ as given by 𝐼 . Assuming the postcondition
                                                                                                  1/2
         of 𝜅, we turn pending𝛾l into shot(𝑠 2 )𝛾l2 , 𝛾 o ↦→ None into 𝛾 o ↦−→ LM and deposit these
                                     2
                                                                                                 1/2
         together with sig(𝑠 2, false, 0) to restore 𝐼 . The other half of 𝛾 o ↦−→ LM and obs2 ({(𝑠 2, 0)})
         are equal to Φ. Thus, together with ⊲ 𝐿(lk, true) it is now possible to close the invariant.
D.4.2 Handoﬀ between left and middle thread. The left thread opens the invariant, set f to false,
and deposits the right conjunct of Handoﬀ with 𝑑 = false. Either the middle thread reads f and
discovers it to be set. In that case the program exits completing the proof trivially. Otherwise, it
exchanges its token tok𝛾h for the right part of that disjunction.
D.4.3 Middle thread release . We do the same for 𝜅 of the middle thread’s release . That is we
derive ⊤SL h𝐿(lk, true) | 𝐿(lk, false) ⇛ Φi l;𝑂
                                            E with WI and Φ deﬁned as follows.
                          𝜅

                                   Φ , True
                                                              1/2
                                                     N
                                   WI , 𝐼                ∗ 𝛾 o ↦−→ LM ∗ obs({(𝑠 2 , 0)})
                                                                                           1/2
       • Atomic precondition: From the invariant 𝐼 and separately 𝛾 o ↦−→ LM we can conclude that
         ⊲ 𝐿(lk, true) must hold.
                                         1/2
       • 𝜅: Moreover, because 𝛾 o ↦−→ LM is part of the local resources of WI we can conclude that the
               1/2
         𝛾 o ↦−→ LM part of Progress holds. Therefore 𝜅’s precondition holds (Figure 34). Assuming
                                                                                                                           1/2
         its postcondition, we can close the invariant by combining the local fraction 𝛾 o ↦−→ LM
         with the one from the invariant. This allows us to obtain 𝛾 o ↦→ None. 𝛾 o ↦→ None forces
         𝐿(lk, false). Thus ⊲ 𝐿(lk, false) is required to close up the invariant; as desired.
       • Notice that 𝜅 gives the module obs(∅), which trivially satisﬁes l ≺ ∅. Recall, that the
         obligations returned from release (Section 5) must exactly be those returned from 𝜅 i.e.
         obs(∅).
D.4.4 Right thread. The calls to acquire and release can be justiﬁed in the same manner.

D.5 Erasure of instrumented motivating example
Figure 35 shows the erasure of the instrumented motivating example.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules   35


                                           let lk = new_lock () in
                                           let f = ref true in
                                           fork (
                                              if !f then exit;
                                              release lk
                                           );
                                           fork (
                                              acquire lk;
                                              release lk
                                           );
                                           acquire lk;
                                           f ≔ false

                                    Fig. 35. Erasure of the motivating example.


E TICKETLOCK
Figure 37 shows the ticketlock’s predicate, invariant and a proof outline for acquire and release .

E.1 Ticketlock predicate and invariant
A key idea of the lock predicate 𝐿 and invariant 𝐼 are the fractional permissions split between
them. This forces the lock predicate and invariant to be kept in sync. More speciﬁcally, in order
to modify these shared points-to’s, both the client’s invariant (opaque to the module) and the lock
invariant (opaque to the client) need to be opened, updated, and closed.
   Other key details include:
      • Matching the ticketlock’s implementation, the lock is held iﬀ the owner ﬁeld is less than
        the next (available ticket) ﬁeld. Note that this enforces the execution of the external lin-
        earization point at release if threads are queued on the ticketlock.
      • Concretely, the ghost map 𝑀 keeps track of the helping exchange [Jung et al. 2015; Spies et al.
        2022]. For each ticket 𝑘 and current value of the owner ﬁeld 𝑜, 𝑀 holds one of:
          – The total correctness logically atomic update to linearize the 𝑘’th acquire if 𝑘 < 𝑜.
             The later credit accompanying the total correctness logically atomic update (see TAU′ )
             allows stripping the later from (the not timeless) TAU.
          – The 𝑘’th linearization’s Φ if 𝑘 = 𝑜.
          – An exclusive token picked by the 𝑘’th acquire so that it can take out Φ.
   Finally, the given ticketlock predicate nests the module’s invariant inside the lock predicate.
This makes the lock’s speciﬁcation more concise, only requiring the lock predicate. Spies et al.
[2022]’s addition of later credits to Iris make this nesting quite manageable. Notice the auxiliary
dummy step taken at the beginning of acquire and release in Figure 37a. These generate a later
credit that let us strip the later from the invariant23 nested inside the lock predicate. Since the lock
invariant can be duplicated, acquire can keep a copy of the invariant. This way checking the loop
condition after acquire ’s linearization (giving up 𝐿(lk, true)) is permitted.
   An alternative approach is to deﬁne a persistent lock predicate is_lock(lk)—also returned at
lock creation time—that is additionally required for acquire and release . The machine-checked
VeriFast proof in the artifact [Fasse and Jacobs 2024] follows this approach.

23 Invariants are not timeless.
36                                                                                               Justus Fasse and Bart Jacobs


     {obs(∅) ∗ cp(𝛿 1 )}
     let lk = new_lock () in
     let f = ref true in
     let l 2 = ref 0 in let l 3 = ref 0 in

                                                                                                                    
     lower 𝛿 1 into 4 times 𝛿 2 ; lower 𝛿 2 into 4 times 𝛿 3 ; lower 𝛿 2 into 4 times 0 ;
         obs(∅) ∗ 𝐿(lk, false) ∗ 𝑓 ↦→ true ∗ 𝑙 2 ↦→ 0 ∗ 𝑙 3 ↦→ 0 ∗ [2 · cp(𝛿 2 )] ∗ [4 · cp(𝛿 3 )] ∗ [4 · cp(0)] ∗
         𝛾 o ↦→ None ∗ tok𝛾h ∗ pending𝛾l ∗ pending𝛾l
                                                       2           3
           N
     {𝐼        ∗ tok𝛾h ∗ pending𝛾l ∗ pending𝛾l }
                                         2                 3
     fork ∅ ( (* Middle thread *)
          {tok𝛾h ∗ cp(𝛿 3 ) ∗ cp(0)}
          if !f then exit; (* See Section D.4.2 *)
                                   1/2
          {obs({(𝑠 2, 0)}) ∗ 𝛾 o ↦−−→ LM ∗ cp(𝛿 3 ) ∗ cp(0)}
          {WI ∗ cp(𝛿 3 ) ∗ cp(0)}
          release lk (* See Section D.4.3 *)
            (𝝀. SetSignal !l 2 )
          {Φ ∗ obs(∅)}
     );
     fork ∅ ( (* Right thread *)
          {obs(∅) ∗ pending𝛾l ∗ cp(𝛿 2 ) ∗ [2 · cp(𝛿 3 )] ∗ [2 · cp(0)}
                               3
          let started = ref false in
          acquire lk
            (𝝀. if not !started then (NewExpectPerm !l 2 𝛿 2 𝛿 3 ; started ≔ true);
              Expect !l 2 )
          (𝝀 l 3 ≔ NewSignal l1 );
          release lk
            (𝝀. SetSignal !l 3 )
          {obs(∅)}
     );
     {obs(∅) ∗ obs2 (∅) ∗ pending𝛾l ∗ pending𝛾l ∗ cp(𝛿 2 ) ∗ cp(𝛿 3 ) ∗ cp(0)}
                                             2                 2
     let started = ref false in
     {WI ∗ cp(𝛿 3 ) ∗ cp(0)}
     acquire lk (* see Section D.4.1 *)
       (𝝀. if not !started then (NewExpectPerm !l 3 𝛿 2 𝛿 3 ; started ≔ true);
         Expect !l 3 )
       (𝝀 l 2 ≔ NewSignal 2 l1 );
     {Φ}
                                                 1/2
     {obs(∅) ∗ obs2 ({(𝑠 2, 0)}) ∗ 𝛾 o ↦−−→ LM}
     f ≔ false (* See Section D.4.2 *)
     obs(∅)

Fig. 36. Proof outline for motivating example. 𝛿 3 is the embedding of ⊤SL into the client degrees (see Section 3
of main text).
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                                  37


                                                                              let release lk 𝜅 =
                                                                                let _ = () in (* Get later credit *)
                                                                                {cp(⊤TL ) ∗ TAU ∗ £ 1}
 let acquire lk 𝜂 𝜅 =
                                                                                h
                                                                                                                                          
    {cp(⊤TL ) ∗ obs(𝑂) ∗ LTL ≺ 𝑂 ∗ TAU}
    let _ = () in (* Get later credit *)                                        
                                                                                 lk.owner ↦→ 𝑜 ∗ lk.next ↦→ 𝑛 ∗ 𝛾 held ↦→ true ∗
                                                                                                                                          
                                                                                                                                           
                                                                                                                                           

                                                                                                          ∗
                                                                                  . . . Rest of I ∗
    { £ 1 ∗ cp(⊤TL ) ∗ obs(𝑂) ∗ LTL ≺ 𝑂 ∗ TAU}                                  
                                                                                 (𝐿(lk, false, 𝑜 + 1) ≡                                   
                                                                                                                                           
    let t = (* Ticket *)                                                                             ∅
                                                                                                        − ⊤\E Φ)                           ∅
                                                                                 (* Rel-LP *) 𝜅 ();
    h if !(lk.next) = lk.owner
                                                                                 FAA lk.owner 1;
                                                                                                                             
      then (* Acq-LP-1 *) 𝜅 ()
                                                                                                                             
                                                                                              1    /2
     else (fairness;                                                             lk.owner
                                                                                           1/2
                                                                                                ↦−−→ 𝑜 + 1 ∗ lk.next ↦→ 𝑛 ∗   
                                                                                                                              
                                                                                                                             
                                                                                  𝛾 held ↦−−→ false ∗ . . . Rest of I ∗
       lk.TAUs[!(lk.next)] ≔ 𝜅 );                                                ∗Φ                                          
     FAA lk.next 1 i                                                                                                          ⊤\E
                                                                                 if !(lk.owner) < !(lk.next)
    in
                  E       𝛾𝑀                                         𝛾𝑡          then (* Acq-LP-2 *)
    { 𝐼 (lk, 𝛾)       ∗ 𝑡 ↩−−→ (𝜃, 𝑂, LTL, 𝜂, 𝜅, Φ, 𝛾𝑡 ) ∗ ex()           }     {TAU′ for 𝑘 = 𝑜 + 1} ⊤\E
    while
                                                                                    lk.TAUs[!(lk.owner)] ()
    h if !(lk.owner ≠ t) then 𝜂 () else ();                                     {Φ𝑘 ∗ 𝑘 = 𝑜 + 1} ⊤\E
      !(lk.owner) ≠ t i
                                                                                 else
    do () done
    {Φ}
                                                                                {𝑜 + 1 = 𝑛 outside domain of     ∗ }⊤\E
                                                                                  ()
                                                                                i
                                                                                {Φ ∗ obs(𝑂) ∗ LTL ≺ 𝑂 }
                  (a) Ticketlock implementation. The proof outline references definitions of 37b.

      TAU′ (𝜃, 𝑂, LTL, 𝜂, 𝜅, Φ) , obs𝜃 (𝑂) ∗ LTL ≺ 𝑂 ∗
                               𝜂                                                  𝑂,LTL
             £ 1 ∗ h𝑏, 𝑜 ։𝑜 {false} × N. 𝐿(lk, 𝑏, 𝑜) | 𝐿(lk, true, 𝑜) ∗ 𝑏 = falsei𝜃,⊤\E
                                                                 𝜅
                                                           1/2                         1/2
                                                                                                          E
      𝐿(lk, 𝑏, 𝑜, 𝛾) , 𝛾 ↦→ (𝛾 held , 𝛾𝑀 ) ∗ 𝛾 held ↦−→ 𝑏 ∗ lk.owner ↦−→ 𝑜 ∗ 𝐼 (lk, 𝛾)
      𝐼 (lk, 𝛾) , ∃𝑏, 𝑜, 𝑛, 𝑀. (𝑜 ≤ 𝑛) ∗ (𝑏 ↔ 𝑜 < 𝑛) ∗ dom(𝑀) = [0, 𝑛) ∗
                             1/2             1/2
                                                                                 𝛾𝑀
             lk.owner ↦−→ 𝑜 ∗ 𝛾 held ↦−→ 𝑏 ∗ lk.next ↦→ 𝑛 ∗ 𝑀                         ∗
                                                                                                                               
                           ∗             ′
                                   (TAU (𝜃, 𝑂, LTL, 𝜂, 𝜅, Φ) ∗ 𝑜 < 𝑘) ∨ (Φ ∗ 𝑜 = 𝑘) ∨ ( ex()
             𝑘↦→ (𝜃,𝑂,LTL,𝜂,𝜅,Φ,𝛾𝑘 ) ∈𝑀
                                                                                                               𝛾𝑘
                                                                                                                    ∗ 𝑜 ≥ 𝑘)


(b) Lock predicate for ticketlock implementation. Parts highlighted in green mark additions necessary to
satisfy the fair specification.

                                   Fig. 37. Ticketlock implementation and proof outline.



F COHORTLOCK
F.1 𝜂s
We brieﬂy recall key details from Section 9 of the main text.

  Top-level lock (TL). The cohortlock is held by the client whenever TL is held. Thus, TL’s 𝜂 can
use the client 𝜂 whenever TL is held. Recall that TL can be passed without competition from other
cohorts MAX number of times. This means the TL round does not change while the cohortlock
38                                                                                    Justus Fasse and Bart Jacobs

                                                                                                          
                                                     (𝑣 = false ∗ notAlone(lk, 𝑟 + 1)) ∨
      h𝐿(lk, true, 𝑟 ) | 𝑅, 𝑣. 𝐿(lk, true, 𝑟 ) ∗ 𝑅 ∗
                                                     (𝑣 = true ∗ (𝑅 ∗ notAlone(lk, 𝑟 + 1) ⇛ ∅ False)
            ⇛ Φ(𝑣) ∗ 𝑅i⊤\E −∗ wp alone lk {𝑣. Φ(𝑣)}
      𝐿(lk, false, 𝑟 ) ∗ notAlone(lk, 𝑟 ) ⇛ E False

Fig. 38. Specification of ticketlock’s alone . It ensures two properties. First, if alone returns false, the next
lock release will be a direct handoﬀ i.e. linearize the acquire of the next thread in line. It follows that the
client will at no point observe the lock not being held in the next round. Second, if alone has returned false
for the current round, it will not return true for that same round.



round does. Thus, for each TL round, TL’s 𝜂 may need to call the cohortlock client’s 𝜂 up to MAX
times.

  Local lock (LL). For each local lock round, acquire may be blocked on the “client” (here the
cohortlock implementation) if:
      • The TL, and thus the cohortlock, is held by the same cohort as the LL acquire : 𝜂 can invoke
        the cohortlock client’s 𝜂 to justify progress.
      • The LL is held but TL has not yet been acquired by a member of the cohort: the LL 𝜂 can
        expect the acquire signal.
      • The LL is held, the TL has been released by a member of the cohort but LL’s release has
        not yet occurred: the LL 𝜂 can expect the release signal.

F.2 Levels
Let LFL be the set of levels for a fair lock module used for the top-level lock (TL) and the local
locks (LLs).

                                 LCL , {0} × LFL ∪ {(1, 0)} ∪ {2} × LFL

The embedded levels are ordered lexicographically. We use {0} × LFL for the TL, (1, 0) for the
acquire and release signals, and {2} × LFL for the LLs.

F.3    Degrees
Let Δ𝐶eta be the client’s eta domain of degrees (cf. Section 6.1 of the main text) with the named
degrees ⊤𝐶eta and ⊥𝐶eta . We deﬁne Δeta     eta
                                    TL and ΔLL in terms of their local domain of degrees:

                                  Δeta         eta
                                   TL , {0} × Δ𝐶 ∪ {(1, 0)}
                                        ⊤eta           𝑒𝑡𝑎       eta
                                         TL , (1, 0), ⊥TL , (0, ⊥C )
                                  Δeta         eta
                                   LL , {0} × Δ𝐶 ∪ {(1, 0)} ∪ {(2, 0)}
                                        ⊤eta           𝑒𝑡𝑎       eta
                                         LL , (2, 0), ⊥LL , (0, ⊥C )

F.4    alone
Figure 38 shows the speciﬁcation to ticketlock’s alone operation. This speciﬁcation enforces that if
the current owner is not alone, then the next release directly transfers ownership of the ticketlock
to the next waiting thread.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules               39


G HEAPLANG<
The main text presents our extensions to HeapLang: the auxiliary code, and function application—
instrumented to consume a call permission at every call. The following ﬁgures complete Heap-
Lang< ’s deﬁnition.
     • HeapLang< ’s syntax is deﬁned in Figure 39 with additional syntactic sugar deﬁned in Fig-
        ure 40.
     • HeapLang< ’s state is deﬁned in Figure 41.
     • HeapLang< ’s pure and boxed reduction rules are deﬁned in Figure 42.
     • HeapLang< ’s impure reduction steps are shown in Figure 43.
     • HeapLang< ’s evaluation contexts are deﬁned in Figure 44.
     • HeapLang< ’s big-step evaluation relation is deﬁned in Figure 24. Its deﬁnition uses copies
        of the regular thread-step (Figure 42) and head-step relations that exclude fork-statements
        and atomic blocks.


𝑣, 𝑤 ∈Val ::= 𝑧 | true | false | () | h | ℓ | 𝑠 | 𝑝 |                       (𝑧 ∈ Z, ℓ ∈ Loc, 𝑝 ∈ ProphId, 𝑠 ∈ SigLoc)
              𝝁 v f x. 𝑒 | (𝑣, 𝑤)v | inlv 𝑣 | inrv 𝑣
 𝑒 ∈ Expr ::= 𝑣 | x | 𝝁 e f x. 𝑒 | (𝑒 1 𝑒 2 ) | ⊚1𝑒 | 𝑒 1 ⊚2 𝑒 2 | if 𝑒 then 𝑒 1 else 𝑒 2 |
                (𝑒 1 , 𝑒 2 )e | 𝝅 1 𝑒 | 𝝅 2 𝑒 | inle 𝑒 | inre 𝑒 | match 𝑒 with inl ⇒ 𝑒 1 | inr ⇒ 𝑒 2 end |
                AllocN 𝑒 1 𝑒 2 | free 𝑒 | ! 𝑒 | 𝑒 1 ≔ 𝑒 2 | CmpXchg 𝑒 1 𝑒 2 𝑒 3 | Xchg 𝑒 1 𝑒 2 | FAA 𝑒 1 𝑒 2 |
                newproph | resolve with 𝑒 1 at 𝑒 2 to 𝑒 3
                fork 𝑒 1 𝑒 2 | let 𝑥 = 𝑒 1 in 𝑒 2 | Finish | exit | h𝑒i | lower 𝑒 1 to 𝑒 2 times 𝑒 3 at 𝑒 4
                NewSignal 𝑒 1 𝑒 2 | SetSignal 𝑒 1 𝑒 2 | NewExpectPerm 𝑒 1 𝑒 2 𝑒 3 𝑒 4 | Expect 𝑒 1 𝑒 2 𝑒 3 |
        ⊚1 ::= − | . . . (list incomplete)
        ⊚2 ::= + | − | +L | = | . . . (list incomplete)

Fig. 39. HeapLang< ’s syntax, mostly identical to HeapLang [Iris contributors 2024]. Auxiliary code added by
HeapLang< is highlighted in blue. Note the additional arguments to fork, explained in Figure 45. Syntactic
sugar for some constructs is defined in Figure 40.



                                                     𝜆x. 𝑒 , 𝝁 e x. 𝑒
                                                       𝜆. 𝑒 , 𝝁 e      .𝑒
                                                     skip , (); ()
                                                 𝑒 1 && 𝑒 2 , if 𝑒 1 then 𝑒 2 else false
match 𝑒 with inl (x) ⇒ 𝑒 1 | inr (y) ⇒ 𝑒 2 end , match 𝑒 with inl ⇒ 𝜆x. 𝑒 1 | inr ⇒ 𝜆y. 𝑒 2 end
                                                    ref 𝑒 , AllocN 1 𝑒
                                             CAS 𝑒 1 𝑒 2 𝑒 3 , 𝝅 2 CmpXchg 𝑒 1 𝑒 2 𝑒 3
                                      resolve 𝑒 1 to 𝑒 2 , resolve with skip at 𝑒 1 to 𝑒 2



                                        Fig. 40. HeapLang< syntactic sugar.
40                                                                                   Justus Fasse and Bart Jacobs



                ℓ ∋ Loc , Z
           𝑝 ∋ ProphId , Z
               𝛿 ∋ Deg , Val
               l ∋ Lev , Val
            𝑠 ∋ SigLoc , N
                 𝜃 ∋ Θ , N+
                            
                                                                                                  
                                                                                                   
                                                     fin
                                                                                                  
                                        Heap : Loc −⇀Val
                            
                                                                                                  
                                                                                                   
                            
                                                                                                  
                                                                                                   
                                                                                                  
                                      Prophs : ℘(ProphId)
                            
                                                                                                  
                                                                                                   
                            
                            
                                                     fin                                           
                                                                                                   
                            
                            
                            
                                       HeapA : Loc −⇀Val                                           
                                                                                                   
                                                                                                   
                                                           fin
                                                                                    
              𝜎 ∋ State ,          Signals : SigLoc −⇀ Lev × B
                            
                                                                                    
                            
                             Obligations : Θ −⇀ Multiset(SigLoc × Lev) ∪ {Finished} 
                                                                                     
                                                                                     
                                                fin
                            
                                                                                    
                                                                                     
                            
                                                                                    
                                                                                     
                                                                                    
                                                fin
                                                                                    
                                CallPerms : Θ −⇀ Multiset(Deg)
                            
                             ExpectPerms : Θ −                                      
                                                                                     
                                                                                    
                                                fin
                                                 ⇀ Multiset(SigLoc × Deg)
               𝜅 ∋ Obs , ProphId × (Val ×Val)

Fig. 41. HeapLang< ’s state. This figure is adapted from [Iris contributors 2024, p. 52]. The additions for aux-
iliary state are shown in blue. The well-founded orders on levels (Lev) and degrees (Deg) can be modularly
constructed (see main text, Section 7).



H ERASABLE HEAPLANG<
To simplify the erasure argument, we adapt HeapLang< in a few ways. Figure 48 shows the most
important changes. The duplicated constructs let us easily distinguish between real and auxiliary
code.

H.1 Syntactic constraints
A safe HeapLang< program satisfying the following syntactic constraints is erasable if:
     • The program is in A-normal form (ANF) [Sabry and Felleisen 1992].
     • The auxiliary let (letA ) is the only auxiliary code embedded in real code. The other aux-
       iliary constructs must appear in the val-body of the auxiliary let expression. Note that we
       consider atomic blocks to be real but that all our uses contain a single, real, atomic expres-
       sion.
     • We distinguish between real (instrumented) functions 𝝁 v f x 𝑦. 𝑒 2 and purely auxiliary
       functions 𝝁 Av f x. 𝑒.
     • An auxiliary let bound variable does not appear free in real code. It may, however, appear
       inside auxiliary let expressions inside real code. Moreover, our the real (instrumented) 𝜇
       construct always takes a second argument where auxiliary let bound variables may appear.
     • In the val-body of an auxiliary let, there are no assignments to the real heap i.e. ≔ does not
       occur. The auxiliary assignment ≔A may appear and gets stuck on real locations.
     • Real functions may not be called in auxiliary code. This check is syntactic because real
       (instrumented) functions always take two arguments while auxiliary functions only take
       on.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                                 41



                                                                                                                       𝜅®
Per-thread reduction                                                                                         𝑒 1 , 𝜎1 →
                                                                                                                      − t 𝑒 2 , 𝜎2, 𝑒®
                                                                                                                       𝜃

                                     𝜅®                                                        𝜖
                            𝑒 1 , 𝜎1 →
                                     −𝜃 h 𝑒 2 , 𝜎2, 𝑒®                                𝑒 1 , 𝜎1 →
                                                                                               −𝜃 h None
                                     𝜅®                                                             𝜖
                       𝐾 [ 𝑒 1 ], 𝜎1 →
                                     − t 𝐾 [ 𝑒 2 ], 𝜎2, 𝑒®                          𝐾 [ 𝑒 1 ], 𝜎1 →
                                                                                                  − t None
                                     𝜃                                                              𝜃


                                                                                                                      𝜅®
“Head” reduction (pure)                                                                                      𝑒 1 , 𝜎1 →
                                                                                                                      −𝜃 h 𝑒 2 , 𝜎2, 𝑒®

                                     “Boxing” reductions
                                                                                𝜖
                                                             (𝝁 e f x. 𝑒, 𝜎) →
                                                                             −𝜃 h (𝝁 v f x. 𝑒, 𝜎, 𝜖)
                                                                                𝜖
                                                              ((𝑣 1, 𝑣 2 )e, 𝜎) →
                                                                                −𝜃 h ((𝑣 1 , 𝑣 2 )v, 𝜎, 𝜖)
                                                                                𝜖
                                                             ( inle (𝑣), 𝜎) →
                                                                            −𝜃 h ( inlv (𝑣), 𝜎, 𝜖)
                                                                                𝜖
                                                             ( inre (𝑣), 𝜎) →
                                                                            −𝜃 h ( inrv (𝑣), 𝜎, 𝜖)
                                     Pure reductions
                                    Modiﬁed function application is deﬁned in Figure 45.
                                                                                𝜖
                                                                   (−⊚𝑧, 𝜎) →
                                                                            −𝜃 h (−𝑧, 𝜎, 𝜖)
                                                                                𝜖
                                                              (𝑧 1 +⊚ 𝑧 2, 𝜎) →
                                                                              −𝜃 h (𝑧 1 + 𝑧 2, 𝜎, 𝜖)
                                                                                𝜖
                                                              (𝑧 1 −⊚ 𝑧 2, 𝜎) →
                                                                              −𝜃 h (𝑧 1 − 𝑧 2, 𝜎, 𝜖)
                                                                                𝜖
                                                                 (ℓ +L 𝑧, 𝜎) →
                                                                             −𝜃 h (ℓ + 𝑧, 𝜎, 𝜖)
                                                                                𝜖
                                                             (𝑣 1 =⊚ 𝑣 2, 𝜎) →
                                                                             −𝜃 h ( true, 𝜎, 𝜖)                      if 𝑣 1  𝑣 2
                                                                                𝜖
                                                             (𝑣 1 =⊚ 𝑣 2, 𝜎) →
                                                                             −𝜃 h ( false, 𝜎, 𝜖)                     if 𝑣 1  𝑣 2
                                                                                𝜖
                                  ( if true then 𝑒 1 else 𝑒 2, 𝜎) →
                                                                  −𝜃 h (𝑒 1 , 𝜎, 𝜖)
                                                                                𝜖
                                ( if false then 𝑒 1 else 𝑒 2, 𝜎) →
                                                                 −𝜃 h (𝑒 2 , 𝜎, 𝜖)
                                                                                𝜖
                                                         (𝝅 1 (𝑣 1, 𝑣 2 v ), 𝜎) →
                                                                                −𝜃 h (𝑣 1 , 𝜎, 𝜖)
                                                                                𝜖
                                                         (𝝅 2 (𝑣 1, 𝑣 2 v ), 𝜎) →
                                                                                −𝜃 h (𝑣 2 , 𝜎, 𝜖)
                                                                                𝜖
    ( match inlv (𝑣) with inl ⇒ 𝑒 1 | inr ⇒ 𝑒 2 end, 𝜎) →
                                                        −𝜃 h (𝑒 1 (𝑣), 𝜎, 𝜖)
                                                                                𝜖
    ( match inrv (𝑣) with inl ⇒ 𝑒 1 | inr ⇒ 𝑒 2 end, 𝜎) →
                                                        −𝜃 h (𝑒 2 (𝑣), 𝜎, 𝜖)


    Fig. 42. HeapLang pure and boxed reduction rules. This figure is taken from [Iris contributors 2024].
    42                                                                                       Justus Fasse and Bart Jacobs



                                                                                                              𝜅®
    “Head” reduction (impure)                                                                        𝑒 1 , 𝜎1 →
                                                                                                              − h 𝑒 2 , 𝜎2, 𝑒®
Heap reductions
                              𝜖
           ( AllocN 𝑧 𝑣, 𝜎) →
                            − h (ℓ, 𝜎 : Heap[[ℓ, ℓ + 𝑧) ← 𝑣] , 𝜖)               if 𝑧 > 0 and ∀𝑖 < 𝑧. 𝜎.Heap(ℓ + 𝑖) = ⊥
                              𝜖
               ( free ℓ, 𝜎) →
                            − h ((), 𝜎 : Heap[ℓ ← ⊥] , 𝜖)                       if 𝜎.Heap(𝑙) = 𝑣
                              𝜖
                     (! ℓ, 𝜎) →
                              − h (𝑣, 𝜎, 𝜖)                                     if 𝜎.Heap(𝑙) = 𝑣
                              𝜖
                (ℓ ≔ 𝑤, 𝜎) →
                           − h ((), 𝜎 : Heap[ℓ ← 𝑤] , 𝜖)                        if 𝜎.Heap(𝑙) = 𝑣
                              𝜖
    ( CmpXchg ℓ 𝑤 1 𝑤 2, 𝜎) →
                            − h ((𝑣, true), 𝜎 : Heap[ℓ ← 𝑤 2 ] , 𝜖)             if 𝜎.Heap(𝑙) = 𝑣 and 𝑣  𝑤 1
                              𝜖
    ( CmpXchg ℓ 𝑤 1 𝑤 2, 𝜎) →
                            − h ((𝑣, false), 𝜎, 𝜖)                              if 𝜎.Heap(𝑙) = 𝑣 and 𝑣  𝑤 1
                              𝜖
                ( Xchg ℓ 𝑤 →
                           − h (𝑣, 𝜎 : Heap[ℓ ← 𝑤] , 𝜖)                         if 𝜎.Heap(𝑙) = 𝑣
                              𝜖
                  ( FAA ℓ 𝑧 2 →
                              − h (𝑧 1 , 𝜎 : Heap[ℓ ← 𝑧 1 + 𝑧 2 ] , 𝜖)          if 𝜎.Heap(𝑙) = 𝑧 1
Special reductions
            fork is modiﬁed and deﬁned in Figure 45.
                              𝜖
           ( newproph, 𝜎) →
                          − h (𝑝, 𝜎 : Prophs ⊎ {𝑝 } , 𝜖)                        if 𝑝 ∉ 𝜎.Prophs
                                                          𝜅®
                                                         − h (𝑣, 𝜎 ′, 𝑒®′ )
                                                  (𝑒, 𝜎) →
                                                                    ® +[ (𝑝,(𝑣,𝑤 ) ) ]
                                                                    𝜅+
                           ( resolve with 𝑒 at 𝑝 to 𝑤, 𝜎) −−−−−−−−−−−→h (𝑣, 𝜎 ′, 𝑒®′ )

    Fig. 43. HeapLang’s impure head reduction rules. Taken from Iris’ technical documentation [Iris contributors
    2024].


    H.2 Erasure
      Theorem H.1 (Erasure). erase(𝑒 ′ ) does not admit inﬁnite fair executions if the augmented pro-
    gram 𝑒 ′ ; Finish is safe.
       Proof. Assume to the contrary an arbitrary inﬁnite fair execution of erase(𝑒 ′ ). In contradiction
    of Theorem 2.1 we construct an inﬁnite fair execution of 𝑒 ′ ; Finish.
      Lemma H.2 (Augmented infinite fair execution). Let 𝑇 ′ ; 𝜎 ′ be an arbitrary, safe, augmented
    conﬁguration and Σ a fair inﬁnite execution starting from erase(𝑇 ′ ); erase(𝜎 ′ ). Then, there exists an
    inﬁnite fair execution starting from 𝑇 ′ ; 𝜎 ′ .
       Proof. Let 𝑇 be the erased list of expression representing the threads and 𝑖 be the index in 𝑇
    of the thread taking the ﬁrst step of Σ. We compare the head redexes of 𝑇 ′ [𝑖] and 𝑇 [𝑖] before that
    step.
        Base case:
    If they are the same, we execute the real step in the augmented execution as well. Notice that real
    code does not interfere with auxiliary state so that the we can apply the same logic to the following
    step. Thus, we apply the lemma coinductively on the resulting two new conﬁgurations.
       Inductive case:
    Otherwise, 𝑇 [𝜃 ] and𝑇 ′ [𝜃 ] do not correspond.𝑇 ′ [𝜃 ] has the shape of ﬁnitely many nested auxiliary
    let statements before reaching the head redex of 𝑇 [𝜃 ]. By the safety of 𝑇 ′ ; 𝜎 ′ we know that all
A flexible specification approach for verifying total correctness of fine-grained concurrent modules   43



          𝐾 ∈ Ctx ::= • | Ctx>
       𝐾> ∈ Ctx> ::= (𝑒 𝐾) | (𝐾 𝑣) |
                          ⊚1 𝐾 | 𝑒 ⊚2 𝐾 | 𝐾 ⊚2 𝑣 | if 𝐾 then 𝑒 1 else 𝑒 2 |
                         (𝑒, 𝐾) | (𝐾, 𝑣) | 𝝅 1 𝐾 | 𝝅 2 𝐾 |
                         inl 𝐾 | inr 𝐾 | match 𝐾 with inl ⇒ 𝑒 1 | inr ⇒ 𝑒 2 end |
                         AllocN 𝑒 𝐾 | AllocN 𝐾 𝑣 | free 𝐾 | ! 𝐾 | 𝑒 ← 𝐾 | 𝐾 ← 𝑣 |
                         CmpXchg 𝑒 1 𝑒 2 𝐾 | CmpXchg 𝑒 1 𝐾 𝑣 3 | CmpXchg 𝐾 𝑣 2 𝑣 3 |
                         Xchg 𝑒 𝐾 | Xchg 𝐾 𝑣 | FAA 𝑒 𝐾 | FAA 𝐾 𝑣 |
                         resolve with 𝑒 1 at 𝑒 2 to 𝐾 | resolve with 𝑒 1 at 𝐾 to 𝑣 3 |
                         resolve with 𝐾> at 𝑣 2 to 𝑣 3
                         let 𝑥 = 𝐾 in 𝑒 |
                         NewSignal 𝑒 𝐾 | NewSignal 𝐾 𝑣 | SetSignal 𝑒 𝐾 | SetSignal 𝐾 𝑣 |
                         NewExpectPerm 𝑒 1 𝑒 2 𝑒 3 𝐾 | NewExpectPerm 𝑒 1 𝑒 2 𝐾 𝑣 4 |
                         NewExpectPerm 𝑒 1 𝐾 𝑣 3 𝑣 4 | NewExpectPerm 𝐾 𝑣 2 𝑣 3 𝑣 4 |
                         Expect 𝑒 1 𝑒 2 𝐾 | Expect 𝑒 1 𝐾 𝑣 3 | Expect 𝐾 𝑣 2 𝑣 3 |
                         lower 𝑒 1 into 𝑒 2 times 𝑒 3 at 𝐾 | lower 𝑒 1 into 𝑒 2 times 𝐾 at 𝑣 4 |
                         lower 𝑒 1 into 𝐾 times 𝑣 3 at 𝑣 4 | lower 𝐾 into 𝑣 2 times 𝑣 3 at 𝑣 4 |
                         fork 𝐾 𝑒



Fig. 44. HeapLang< evaluation contexts. The let construct is added but not auxiliary code. Auxiliary code
added by HeapLang< is highlighted in blue.


auxiliary steps are safe and terminating. The ﬁnite number of lets are executed until the base case
is reached.                                                                                       
   Recall that we assume by contradiction that [erase(𝑒 ′ )], ∅ (i.e. starting from an empty heap) is
an inﬁnite fair execution. Moreover, we know that 𝑒 ′ is safe given some state 𝜎 ′ (with 𝜎 ′ .Heap = ∅)
satisfying the weakest precondition of 𝑒 ′ ; Finish i.e. equipped with suﬃcient initial call permis-
sions. By deﬁnition erase( [𝑒 ′ ; Finish], 𝜎 ′ ) = [erase(𝑒 ′ )], ∅. Applying Lemma H.2 we obtain an
inﬁnite fair execution, for 𝑒 ′ ; Finish, reaching the desired contradiction.                        
44                                                                                        Justus Fasse and Bart Jacobs


               BetaS
                                                   0 ∈ 𝜎.CallPerms(𝜃 )
                                    𝜖
               ((𝝁 v f x. 𝑒) 𝑣 , 𝜎) →
                                    −𝜃 h (𝑒 [(𝝁 e f x. 𝑒)/f ] [𝑣/x], 𝜎 : CallPerms[𝜃 \←↪ {0}], 𝜖)

     LowerS
                             𝛿 ∈ 𝜎.CallPerms(𝜃 ′ )             𝛿′ < 𝛿          0≤𝑛
                                               𝜖
     ( lower 𝛿 to 𝑛 times 𝛿 ′ at 𝜃 ′, 𝜎) →
                                         −𝜃 h (𝑒, 𝜎 : CallPerms[𝜃 ′ \←↪ {𝛿}] [𝜃 ′ ⊎←↪[𝑛 · 𝛿 ′ ]], 𝜖)

 NewSignalS
                             𝑠 ∉ 𝜎.Signals             𝜎.Obligations(𝜃 ′ ) ≠ Finished
                              𝜖
     ( NewSignal 𝜃 ′ l, 𝜎) →
                           −𝜃 h (𝑠, 𝜎 : Obligations[𝜃 ′ ∪←↪ {(𝑠, l)}] : Signals[𝑠 ← (l, false)], 𝜖)

     SetSignalS
                         𝜎.Signals(𝑠) = (l, 𝑏)            𝜎.Obligations(𝜃 ′ ) ≠ Finished
                              𝜖
     ( SetSignal 𝜃 ′ 𝑠, 𝜎) →
                           −𝜃 h ((), 𝜎 : Obligations[𝜃 ′ \←↪ {(𝑠, l)}] : Signals[𝑠 ← (l, true)], 𝜖)

                  AtomicBlockS
                                                             CurrentThreadS
                         𝑒, 𝜎 ⇓ 𝑣, 𝜎 ′                                           𝜖
                             𝜖
                                                             ( CurrentThread, 𝜎) →
                                                                                 − h (𝜃, 𝜎, 𝜖)
                                                                                      𝜃
                            −𝜃 h (𝑣, 𝜎 ′, 𝜖)
                   (h𝑒i, 𝜎) →

              FinishS
                                  𝜎.Obligations(𝜃 ) = ∅
                             𝜖
              ( Finish, 𝜎) →
                           −𝜃 h ((), 𝜎 : Obligations[𝜃 ← Finished], 𝜖)

NewExpectPermS
                             𝑠 ∈ 𝜎.Signals             𝛿 ∈ 𝜎.CallPerms(𝜃 ′ )         𝛿′ < 𝛿
                                         𝜖
( NewExpectPerm 𝜃 ′ 𝑠 𝛿 𝛿 ′ , 𝜎) →
                                 −𝜃 h ((), 𝜎 : CallPerms[𝜃 ′ \←↪ {𝛿}] : ExpectPerms[𝜃 ′ ∪←↪(𝑠, 𝛿 ′ )], 𝜖)

       ExpectS
       𝜎.Signals(𝑠) = (l, false)               l ≺ 𝜎.Obligations(𝜃 ′ )          (𝑠, 𝛿) ∈ 𝜎.ExpectPerms(𝜃 ′ )
                                                   𝜖
                         ( Expect 𝜃 ′ 𝑠 𝛿, 𝜎) →
                                              −𝜃 h ((), 𝜎 : CallPerms[𝜃 ′ ⊎←↪ {𝛿}], 𝜖)

ForkS
                                       𝑠 = 𝑜.0              CP = 𝜎.CallPerms(𝜃 )
                        EP = 𝜎.ExpectPerms(𝜃 )              𝜃 ′ = min{𝜃 ′ ∈ Θ | 𝜃 ′ ∉ 𝜎.Obligations}
                                                                        𝜖
                                                         ( fork 𝑠 𝑒, 𝜎) →
                                                                        −𝜃 h
((), 𝜎 : Obligations[𝜃 \←↪ 𝑜] : Obligations[𝜃 ′ ← 𝑜] : CallPerms[𝜃 ′ ← CP] : ExpectPerms[𝜃 ′ ← EP],
                                          (𝜃 ′ , (𝑒; Finish)))

Fig. 45. Operations of HeapLang< that extend or modify HeapLang. Reproduction of Figure 5 in the main
text.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules                   45



                                                                                                             𝜅®
Machine reduction                                                                                          − tp 𝑇 ′ ; 𝜎 ′
                                                                                                       𝑇;𝜎 →
                                                               𝜅®
                                                      𝑒 1 , 𝜎1 →
                                                               − t 𝑒 2 , 𝜎2, 𝑒®
                                                               𝜃
 𝜃 = length(𝑇 )          𝑛 = length(𝑇 ) + length(𝑇 ′ ) + 1                  𝑚 = length(𝑒®)       map 𝜋1 𝑒® = [𝑛, 𝑛 + 𝑚)
                                                      𝜅®
                            𝑇 ++ [𝑒 1 ] ++ 𝑇 ′ ; 𝜎1 →
                                                    − tp 𝑇 ++ [𝑒 2 ] ++ 𝑇 ′ ++ (map 𝜋2 𝑒®); 𝜎2
                                                      𝜃

                                              𝜖
                                        𝑒, 𝜎 →
                                             − t None                 𝜃 = length(𝑇 )
                                              𝜃
                                                  𝜖
                             𝑇 ++ [𝑒] ++ 𝑇 ′ ; 𝜎 →
                                                 − tp map((𝜆. ()), (𝑇 ++ [𝑒] ++ 𝑇 ′ )); 𝜎
                                                  𝜃


                 Fig. 46. Adapted from iris’ technical documentation [Iris contributors 2024].


Value (in)equality                                                                                        𝑣  𝑤, 𝑣  𝑤
                    𝑣  𝑤 , 𝑣 = 𝑤 ∧ (val_compare_safe(𝑣) ∨ val_compare_safe(𝑤))
                    𝑣  𝑤 , 𝑣 ≠ 𝑤 ∧ (val_compare_safe(𝑣) ∨ val_compare_safe(𝑤))
       lit_compare_safe(𝑧)                lit_compare_safe( true)                      lit_compare_safe( false)

                   lit_compare_safe(ℓ)                              lit_compare_safe(())

     lit_compare_safe(𝑣)                    lit_compare_safe(𝑣)                            lit_compare_safe(𝑣)
    val_compare_safe(𝑣)                 val_compare_safe( inl (𝑣))                     val_compare_safe( inr (𝑣))

            Fig. 47. HeapLang value comparison judgment. Copied from [Iris contributors 2024].
46                                                                                                              Justus Fasse and Bart Jacobs


                                                 0 ∈ 𝜎.CallPerms(𝜃 )                 𝑒 1 , 𝜎 ⇓𝜃 𝑣 ′ , 𝜎 ′
                                            𝜖
                                       −𝜃 h (𝑒 [(𝝁 e f x 𝑦. 𝑒 2 )/f ] [𝑣/x] [𝑣 ′ /𝑦], 𝜎 ′ : CallPerms(𝜃 ) \←↪ {0} , 𝜖)
          ((𝝁 v f x 𝑦. 𝑒 2 ) 𝑣 𝑒 1, 𝜎) →

                               𝑒 2 , 𝜎 ⇓𝜃 𝑣, 𝜎 ′          𝑒 1 [𝑣/x], 𝜎 ′ ⇓𝜃 𝑣 ′ , 𝜎 ′′
                                                                𝜖
                                                             −𝜃 h (𝑣 ′ , 𝜎 ′′ , 𝜖)
                                  ((𝝁 Av _ x. 𝑒 1 ) 𝑒 2 , 𝜎) →

                     𝑧>0           ∀𝑖 < 𝑧. 𝜎.Heap(ℓ + 𝑖) = ⊥                    ∀𝑖 < 𝑧. 𝜎.HeapA (ℓ + 𝑖) = ⊥
                                        𝜖
                                   −𝜃 h (ℓ, 𝜎 : Heap[[ℓ, ℓ + 𝑧) ← 𝑣] : HeapA [[ℓ, ℓ + 𝑧) ← 0], 𝜖)
                  ( AllocN 𝑧 𝑣, 𝜎) →

                     𝑧>0           ∀𝑖 < 𝑧. 𝜎.Heap(ℓ + 𝑖) = ⊥                    ∀𝑖 < 𝑧. 𝜎.HeapA (ℓ + 𝑖) = ⊥
                                                           𝜖
                               ( AllocNA 𝑧 𝑣, 𝜎) →
                                                 −𝜃 h (ℓ, 𝜎 : HeapA [[ℓ, ℓ + 𝑧) ← 𝑣], 𝜖)

                                    𝜖                                                          𝑒 1 , 𝜎 ⇓𝜃 𝑣, 𝜎 ′
         ( let 𝑥 = 𝑣 in 𝑒, 𝜎) →
                              −𝜃 h (𝑒 [𝑣/𝑥], 𝜎, 𝜖)                                                          𝜖
                                                                                                    −𝜃 h (𝑒 2 [𝑣/𝑥], 𝜎 ′ , 𝜖)
                                                                         ( letA 𝑥 = 𝑒 1 in 𝑒 2 , 𝜎) →

       𝜎.Heap(ℓ) = 𝑣                            𝜎.HeapA (ℓ) = 𝑣                                        𝜎.Heap(ℓ) = 𝑣
              𝜖                                       𝜖                                            𝜖
     (! ℓ, 𝜎) →
              −𝜃 h (𝑣, 𝜎, 𝜖)            (!A ℓ, 𝜎) →
                                                  −𝜃 h (𝑣, 𝜎, 𝜖)                (ℓ ≔ 𝑤, 𝜎) →
                                                                                           −𝜃 h ((), 𝜎 : Heap[ℓ ← 𝑤], 𝜖)

                                                            𝜎.HeapA (ℓ) = 𝑣
                                                           𝜖
                                        (ℓ ≔A 𝑤, 𝜎) →
                                                    −𝜃 h ((), 𝜎 : HeapA [ℓ ← 𝑤], 𝜖)


Fig. 48. Step rules of HeapLang< extensions with adapted definitions compared to the main text to simplify
the erasure proof.


                               erase(𝜎) = {Heap ← 𝜎.Heap; Prophs ← 𝜎.Prophs}

                        Fig. 49. Store erasure, i.e. removing the auxiliary state of HeapLang< .


                                            erase(𝑇 ; 𝜎) = map erase() 𝑇 ; erase(𝜎)

Fig. 50. A machine configuration consisting of a list expressions, one per thread, 𝑇 and the state 𝜎 erases to
the erasure of the every expression and the erased state.
A flexible specification approach for verifying total correctness of fine-grained concurrent modules   47



                                                   erase( letA 𝑥 = 𝑒 1 in 𝑒 2 ) = erase(𝑒 2 )
                                                erase(𝝁 e f x 𝑦. 𝑒) = 𝝁 v f x (). erase(𝑒)
                                 erase( AtomicBlock 𝑒) = AtomicBlock erase(𝑒 1 )
                                       erase((𝑒 1 𝑒 2 𝑒 3 )) = (erase(𝑒 1 ) erase(𝑒 2 ) ())
                         Other cases by straightforward structural recursion, e.g.:
                         erase( let 𝑥 = 𝑒 1 in 𝑒 2 ) = let 𝑥 = erase(𝑒 1 ) in erase(𝑒 2 )

                                             Fig. 51. Expression erasure.
