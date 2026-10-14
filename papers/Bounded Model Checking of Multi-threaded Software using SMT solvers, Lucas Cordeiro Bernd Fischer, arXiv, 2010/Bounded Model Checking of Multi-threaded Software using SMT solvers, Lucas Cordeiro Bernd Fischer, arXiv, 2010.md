                                                Bounded Model Checking of Multi-threaded Software
                                                               using SMT solvers

                                                                         Lucas Cordeiro                                                      Bernd Fischer
                                                                   University of Southampton                                            University of Southampton
                                                                 lcc08r@ecs.soton.ac.uk                                              b.fischer@ecs.soton.ac.uk
arXiv:1003.3830v1 [cs.LO] 19 Mar 2010




                                        ABSTRACT                                                                             Keywords
                                        The transition from single-core to multi-core processors has                         Formal Software Verification, SAT Modulo Theories, Multi-
                                        made multi-threaded software an important subject in com-                            core systems
                                        puter aided verification. Here, we describe and evaluate an
                                        extension of the ESBMC model checker to support the veri-                            1. INTRODUCTION
                                        fication of multi-threaded software with shared variables and
                                                                                                                                Embedded computer systems are used in a wide range of
                                        locks using bounded model checking (BMC) based on Sat-
                                                                                                                             sophisticated applications, such as mobile phones or set-top
                                        isfiability Modulo Theories (SMT). We describe three ap-
                                                                                                                             boxes providing internet connectivity. The functionality de-
                                        proaches to model check multi-threaded software and our
                                                                                                                             manded in such applications has increased significantly and
                                        modelling of the synchronization primitives of the Pthread
                                                                                                                             an increasing number of functions are implemented in soft-
                                        library. In the lazy approach, we generate all possible in-
                                                                                                                             ware rather than hardware. Thus, multi-core processors with
                                        terleavings and call the BMC procedure on each of them
                                                                                                                             scalable shared memory have become popular in embedded
                                        individually, until we either find a bug, or have systemat-
                                                                                                                             systems. In turn, the verification of the software design and
                                        ically explored all interleavings. In the schedule recording
                                                                                                                             the correctness of its multi-threaded implementations has
                                        approach, we encode all possible interleavings into one sin-
                                                                                                                             become increasingly difficult.
                                        gle formula and then exploit the high speed of the SMT
                                                                                                                                Bounded model checking (BMC) has already been success-
                                        solvers. In the underapproximation-widening approach, we
                                                                                                                             fully applied to verify embedded software and discover subtle
                                        reduce the state space by abstracting the number of state
                                                                                                                             errors in real designs [6]. BMC generates verification condi-
                                        variables and interleavings from the proofs of unsatisfiabil-
                                                                                                                             tions (VCs) that reflect the exact path in which a statement
                                        ity generated by the SMT solvers. In all three approaches,
                                                                                                                             is executed, the context in which a given function is called,
                                        we use partial-order reduction (POR) techniques to reduce
                                                                                                                             and the bit-accurate representation of the expressions. Prov-
                                        the number of interleavings explored. Experiments show
                                                                                                                             ing the validity of these VCs remains a major performance
                                        that our approaches can analyze larger problems and sub-
                                                                                                                             bottleneck in verifying embedded software, despite attempts
                                        stantially reduce the verification time compared to state-of-
                                                                                                                             to cope with increasing system complexity by applying SMT
                                        the-art techniques that combine classic POR methods with
                                                                                                                             (Satisfiability Modulo Theories) [5, 9, 13].
                                        symbolic algorithms and others that implement the Counter-
                                                                                                                                Recently, there have been attempts to extend BMC to
                                        Example Guided Abstraction Refinement technique.
                                                                                                                             the verification of multi-threaded software [14, 17, 18, 24].
                                                                                                                             The main challenge is the state space explosion problem,
                                                                                                                             as the number of interleavings grows exponentially with the
                                        Categories and Subject Descriptors                                                   number of threads and program statements. However, two
                                        D.2.4 [Software/Program Verification]: Model check-                                  important observations help us: (i) SMT-based BMC finds
                                        ing; F.3.1 [Specifying and Verifying and Reasoning                                   counter-examples very quickly [9] and (ii) SMT solvers pro-
                                        about Programs]: Mechanical verification                                             duce unsatisfiable cores that allow us to remove logic that is
                                                                                                                             not relevant to a given property [20]. Grumberg et al. [16]
                                                                                                                             realized that the unsatisfiable cores generated by the solvers
                                                                                                                             can also be used to control the number of allowed interleav-
                                        General Terms                                                                        ings of the given set of processes. They propose an algorith-
                                        Computer-Aided Verification                                                          mic method based on Boolean Satisfiability (SAT) and BMC
                                                                                                                             to model check a multi-process system based on a series of
                                                                                                                             under-approximated models. However, this method does not
                                                                                                                             combine classic partial-order reduction (POR) methods with
                                                                                                                             symbolic algorithms, which limits its usefulness for analyz-
                                        Permission to make digital or hard copies of all or part of this work for            ing and verifying multi-threaded software. It has also not
                                        personal or classroom use is granted without fee provided that copies are            been applied in conjunction with SMT solvers.
                                        not made or distributed for profit or commercial advantage and that copies              In our prior work [9], we extended the encodings from
                                        bear this notice and the full citation on the first page. To copy otherwise, to      previous SMT-based bounded model checkers [5, 13] to pro-
                                        republish, to post on servers or to redistribute to lists, requires prior specific
                                        permission and/or a fee.                                                             vide more accurate support for variables of finite bit width,
                                        Copyright 200X ACM X-XXXXX-XX-X/XX/XX ...$10.00.                                     bit-vector operations, arrays, structures, unions and point-
ers. Here, we develop three approaches to tackle complexity           18) before terminating. If we continue exploring the remain-
problems in model checking multi-threaded C software. In              ing interleavings, we schedule TY first, and the execution of
the lazy approach, we extend the BMC procedure of single-             Y1 makes the test x > 2 in line 7 true, thus enabling TX
threaded software to multi-threaded software by wrapping it           to progress and transition through X0 and X1 , i.e., we ex-
inside a straightforward generate-and-test loop, which gen-           ecute program statements x = 3, a[i] = ∗((int∗)arg), and
erates all possible interleavings and calls the BMC proce-            assert(i >= 0 && i < N )). Note that, as in [14] we do
dure on each of them individually. We stop this loop either           not model context switches inside the execution of individ-
when we find a bug, or have systematically explored all inter-        ual statements, to avoid exploring additional interleavings.
leavings. In the scheduling recording approach, we explore            This approach is safe as long as statements only read or write
systematically the control-flow graph (CFG) of each thread            a single global variable, but is an under-approximation to
and encode all the possible execution paths into one single           programs that contain statements involving multiple global
formula, which is then fed into the back-end SMT solver.              variables. However, with the benchmarks that are publicly
In our third approach, we extend the under-approximation              available, we have not encountered any problems in practice.
and widening (UW) algorithm proposed in [16] with the pur-
pose of addressing the verification of real-world C code using      1 #include         <p th r e a d . h>
different background theories and SMT solvers.                      2 #define        N 10
   We also implement partial order reduction algorithms [3]         3 i n t a [N] , i ,        j =1 , x =2;
in our three approaches and propose a comprehensive SMT-            4 int nondet uint ( ) ;
                                                                    5 void ∗Tx( void ∗ a r g )
based BMC procedure to support the checking of multi-
                                                                    6 {
threaded programs that utilize the synchronization primi-           7     i f ( x>2)
tives of the POSIX Pthread Library [21]. To our knowl-              8     {
edge, this work marks the first application of the UW algo-         9         a [ i ]=∗(( int ∗) arg ) ;         //X0
rithm combined with POR techniques to model check non-             10         a s s e r t ( i >=0 && i <N ) ;    //X1
trivial multi-threaded C software. Experiments obtained            11     }
                                                                   12 }
with ESBMC show that our approaches can analyze larger
                                                                   13 void ∗Ty( void ∗ a r g )
problems and substantially reduce the verification time com-       14 {
pared to state-of-the-art techniques that combine classic POR      15     i f ( x>3)
methods with symbolic algorithms and others that imple-            16         a [ j ]=∗(( int ∗) arg ) ;        //Y0
ment the Counter-Example Guided Abstraction Refinement             17     else
(CEGAR) technique.                                                 18         x =3;                             //Y1
                                                                   19 }
                                                                   20 i n t main ( )
                                                                   21 {
2.   BOUNDED MODEL CHECKING OF                                     22     pthr ead t id1 , id2 ;
     MULTI-THREADED SOFTWARE                                       23     i n t a r g 1 =10 , a r g 2 =20;
                                                                   24     i=n o n d e t u i n t ( ) ;
   In BMC, the program to be analyzed is modelled as a state       25     p t h r e a d c r e a t e(& i d 1 , NULL, Tx , &a r g 1 ) ;
transition system, which is built by extracting its behaviour      26     p t h r e a d c r e a t e(& i d 2 , NULL, Ty , &a r g 2 ) ;
from the CFG. This graph is used as part of a translation          27 }

process from program text to single static assignment (SSA)
form. Each thread is modelled as a CFG where nodes rep-
resent program statements and edges represent transitions.            Figure 1: A multi-threaded C program with violated
A state transition system M = (S, R, S0 ) is an abstract ma-          property.
chine that consists of a set of states S (where S0 ⊆ S rep-
resents the set of initial states) and transitions R between
states, i.e., for each γ ∈ R, γ ⊆ S × S. A state s ∈ S con-                         START_THREAD                     START_THREAD

sists of the value of the program counter pc and the values of
all program variables. An initial state s0 assigns the initial
program location of the CFG to the pc. We identify each                                  Tx0: x>2                         Ty0: x>3

transition γ = (si , si+1 ) between two states si and si+1 with          FALSE
                                                                                               TRUE               TRUE                FALSE
a logical formula γ(si , si+1 ) that captures the constraints on
the values of the program counter and the program variables.                           Tx1: a[i]=10;
                                                                                                                                     Ty2: x=3;
   As a running example, we consider the C program in Fig-                                                      Ty1: a[j]=20;

ure 1, which consists of two threads that are created using
the Pthread library [21]. Note that our example contains a                       Tx2: assert(i>=0 && i<N);
subtle bug (array lower bound) in line 9, because function
nondet uint() might return non-deterministically a negative                                                              END_THREAD

integer number and as a result the assert macro (line 10)                            END_THREAD
fails. Figure 2 shows the CFG representation of the two
threads TX and TY . After creation, they are at the con-
trol points TX0 and TY0 respectively, and since x == 2 (see                Figure 2: Control-flow graph of two threads.
line 3 of Figure 1), both tests x > 2 and x > 3 are false.
If we schedule TX first, it will not be enabled, and we can              Formally, given a transition system M, a property φ, and
transition to the next state only by switching to TY and ex-          a bound k, BMC unrolls the system k times and translates
ecuting only the program statement Y1 (i.e., x = 3, see line          it into a verification condition ψ such that ψ is satisfiable iff
φ has a counterexample of depth less than or equal to k. The             search space. Second, we obviously do not need to gener-
model checking problem associated with SMT-based BMC                     ate the source code of all possible interleavings. Instead, we
for checking linear-time temporal logic (LTL) properties is              keep in memory the nodes of all unexplored execution paths
then formulated by constructing the logical formula:                     and expand them one path at a time. We then construct the
                                                                         VCs for the chosen execution path according to formula (1)
                         constraints                 property            and feed it into the SMT solver to check for satisfiability.
               z               }|                 { z }| {
                         n k−1                        n
                                                                         Third, and most important, we can use information from
                         ^ ^                          ^
       ψ k = I (s0 ) ∧              γj (si , si+1 ) ∧   Pj (sk )   (1)   the front-end to reduce both the number of interleavings to
                         j=1 i=0                    j=1
                                                                         be explored and the size of the formulas sent to the SMT
                                                                         solver. In particular, during the symbolic execution we ex-
where Pj (sk ) represents a LTL property φ in step k of                  ploit which transitions are enabled in a given state to drive
thread j, I is the function for the set of initial states of             the exploration of the interleavings.
M and γj (si , si+1 ) is the function of the transition relation            In our running example, the transitions from TX0 to TX1
of
Vnthread
       Vk−1j at time steps i and i + 1. Hence, the formula               and from TY 0 to TY1 are disabled because we initially have
   j=1  i=0 γj (si , si+1 ) represents the set of all executions         x = 2. This rules out all interleavings that start with ei-
of n threads up to the length k or less. Pj (sk ) is derived             ther X0 or Y0 and only leaves those that bypass TX entirely,
from the property being checked and represents the condi-                or start with Y1 . Assuming that we explore the thread TX
tion that it is violated by a bounded execution of thread j of           first, in the first iteration we thus build the VCs only for
length k or less. Note that formula (1) encodes all allowed              the program statement Y1 . We then pass the formula (1)
interleavings of the given threads.                                      to the SMT solver and check its satisfiability. If it is satis-
                                                                         fiable, we have found a property violation and we can stop
2.1 Lazy Approach                                                        the process. Here, however, it is not satisfiable and we con-
  Conceptually, the simplest way to extend a bounded model               tinue to the next iteration by selecting an unexplored path.
checker for single-threaded software to the multi-threaded               In the second iteration, we explore TY first, and select pro-
case is to wrap it inside a straightforward generate-and-test            gram statement Y1 , and after that we explore TX and select
loop: we just need to generate all possible interleavings and            program statements X0 and X1 . Again, we pass the corre-
call the BMC procedure on each of them individually, until               sponding version of formula (1) to the SMT solver. Since
we either find an error, or have systematically explored all             this is now satisfiable, we can stop the exploration of the
interleavings.                                                           execution paths.
                                                                            In summary, we guide the symbolic execution between the
                                           Y0                            threads and systematically explore all the possible execution
                          X1
                                                                         paths in a lazy way. This approach can find bugs fast, but
          X0                               Y1                            as the front-end might invoke the SMT solver repeatedly,
                                                                         once for each possible execution path, it can suffer perfor-
               Y1         X0              X1
                                                                         mance degradation, in particular for correct programs where
                                                                         we need to explore all possible interleavings. The invocation
                                                                         procedure itself is slow and the formula needs to be passed
          Y0              X0                   X1                        from front-end to back-end several times. Moreover, exe-
                                                                         cution paths that share the same program statements will
                                    (a)                                  be unnecessarily checked several times. However, as each
                                                                         formula corresponds to one possible path only, its size is rel-
                                     Y1
                                                                         atively small compared to the schedule recording approach
                                                                         described in the next section and can thus be handled easily
                    Y1              X0              X1                   by the SMT solver without requiring too much memory.

                                    (b)                                  2.2 Schedule Recording Approach
                                                                            State-of-the-art SMT solvers are built on top of SAT solvers
Figure 3: (a) All possible thread interleavings in                       to speed up the performance by exploiting the support for
Figure 2 (b) The actual thread interleavings after                       “conflict clauses” and non-chronological backtracking [25].
using information from the front-end.                                    In the schedule recording approach we leverage this and
                                                                         avoid invoking the SMT solver multiple times. We use the
  On the face of it, this seems to be naive: the number of               symbolic execution engine as before to systematically ex-
interleavings can grow very quickly (see Figure 3(a) for all             plore the interleavings, but now we add schedule guards to
possible interleavings in the running example), and we need              record in which order the scheduler has executed the pro-
to invoke the model checker several times, which might slow              gram. We then encode all execution paths into one for-
down the verification process.                                           mula, which is finally fed into the SMT solver. However,
  However, there are several observations that make this                 the number of threads and context switches can grow very
approach worthwhile. First we can obviously generate each                large quickly, and easily “blow-up” the solver. Given this,
interleaving, model check it, and stop the generation when               there is a clear trade-off between usage of time and memory
we find the first error. In practice, if the program contains            resources to model check multi-threaded software.
any errors, they will be exhibited in a substantial fraction of             Figure 4 illustrates our schedule recording encoding ap-
the interleavings, if not all (experience of [23] for real appli-        plied to the example in Figure 2. Since control-flow tests
cations), so that we only need to explore a small part of the            cannot influence the state (as the front-end hoists side-effects
out of the tests), we only need to add guards to effective          duce only two different interleavings as follows: {Y1 } and
statements, i.e., assignments and assertions. Similarly, we         {Y1 , X0 , X1 } (cf. Figure 3(b)).
only need to record effective context switches (ECS), i.e.,           Given this, we can define a schedule SCH to determine
context switches to an effective statement. These are shown         which interleavings will be considered and encode the guards
as dashed arrows in Figure 4. Finally, we define an ECS block       in formula (1) as:
as a sequence of program statements that are executed with
no intervening ECS, and give each block a number. Each                                constraints                property        schedule
effective program statement is then prefixed by a schedule                z               }|                   { z }| { z            }|     {
                                                                                      n k−1                        n            k−1
guard tsi = j where i is the ECS block number and j is                                ^ ^                          ^            ^
the thread identifier. Its intuitive interpretation is that the     ψ k = I (s0 ) ∧             γj′ (si , si+1 ) ∧   Pj (sk ) ∧     SCH (si )
                                                                                      j=1 i=0                  j=1            i=0
guarded statement can only be executed if thread j is sched-
uled in the i-th ECS block. The value of tsi is set by the                                                                     (2)
SMT solver, and determines the order in which the program           where γj′ represents the modified transition relation incor-
statements are executed. For example, the guard at TY 2             porating the schedule guards added by the front-end and
thus encodes that Y1 can only be executed if TY runs in the         SCH (si ) represents a constraint on the schedule. If we do
                                                                                                   V
first ECS block. Note that schedule guards are only nec-            not add any constraints, then k−1i=0 SCH (si ) = true and all
essary but not sufficient conditions for the execution of a         possible interleavings are considered. However, if we want
statement. For example, TY 1 has the same guard as TY 2 ,           to apply more aggressive POR techniques, we can add con-
but Y0 cannot be executed using any viable schedule. The            straints to SCH in order to force the removal of interleavings
guards can also be combined conjunctively and disjunctively         that do not contribute to checking a given property. In our
to encode more involved schedules. For example, the guard           running example, we can add the constraint ts1 = 2 and
of both TX1 and TX2 corresponds to a schedule in which TY           ts2 = 1 to remove the interleaving {Y1 } (see Figure 3(b)),
ran before switching to TX .                                        which does not contribute to check the assertion in line 10
                                                                    of Figure 1.
          START_THREAD                    START_THREAD
                                                                    2.3 UW Approach
                                                                        The core idea of the under-approximation and widening
                                                                    (UW) approach is to consider a series of under-approximations
               Tx0: x>2                        Ty0: x>3             of a given model by encoding additional literals into the
                                         TRUE         FALSE
                                                                    verification condition ψ and by extracting the proof objects
                    TRUE
         FALSE
                                                                    generated from an SMT solver [11]. We define ψ ′ as an un-
                                                                                                                           V
                     ECS block 1                                    derapproximated model of ψ, i.e., ψ ′ = ψ ∧ i=0           n   li where
                                     Ty1: ts1==2      Ty2: ts1==2
                                                                    l1 , l2 , . . . , ln are additional literals that guard the program
                                      -> a[j]=20;       -> x=3;     statements of each thread. Similar to the schedule guards
                                                                    described in the previous section, these literals also control
                     ECS block 2                                    the symbolic execution: a program statement is executed
                                                                    only if the literal and its corresponding guard are enabled.
        Tx1: ts1==2 && ts2==1                                       Therefore, we can see that if ψ is unsatisfiable, then ψ ′ is
               -> a[i]=10;
                                            END_THREAD              also unsatisfiable, i.e., there is no assignment to the literals
                                                                    l1 , l2 , . . . , ln that make ψ ′ satisfiable. However, it is possible
                                                                    that ψ is satisfiable while ψ ′ is not, due to the additional lit-
        Tx2: ts1==2 && ts2==1
        -> assert(i>=0 && i<N);
                                                                    erals. Thus, ψ ′ can be thought of as an underapproximation
                                              control-flow
                                                                    of ψ and each satisfying assignment of ψ ′ is also a satisfying
                                              effective context     assignment to ψ. These additional literals then allow us to
            END_THREAD                        switch (ECS)          guide the widening process according to the variables that
                                                                    participate in the proof of unsatisfiability produced by the
                                                                    SMT solver. In the formal description, we rewrite formula
Figure 4: Schedule encoding of the example in Fig-                  (1) as
ure 2.
                                                                                      constraints                property
   The schedule guards are added by the front-end when pro-                z              }|                  { z }| {          U W model
gram statements are executed symbolically and become part                             n k−1
                                                                                      ^ ^                         n
                                                                                                                  ^            z^ }|^ {
of the produced verification conditions. The thread selec-          ψ k = I (s0 ) ∧              ′
                                                                                                γj (si , si+1 ) ∧   Pj (sk ) ∧          lij
tion variable is a free variable that the SMT solver will try                         j=1 i=0                  j=1            ∀i∈T ∀j∈I
to instantiate with all possible concrete values. The thread                                                                       (3)
number value is a constant that corresponds to the thread           where lij ∈ L are literals that encode the program state-
identifier. As an example, if the SMT solver chooses ts1 = 2        ments of each thread. We denote the set of threads by T ,
and ts2 = 1, then the program statement X0 , X1 , Y0 , and          the set of program statements S, and the set of control lit-
Y1 are all enabled in principle, but which ones are executed        erals by L. In the example of Figure 2, T = {TX , TY },
depends on the values of the control-flow tests x > 2 and           S = {X0 , X1 , Y0 , Y1 }, and L = {lX0 , lY0 }. Note that the way
x > 3. Note that the ordering of statements within a thread         that we encode the underapproximation differs from [16].
is of course still ensured by the program order semantics, so       The authors in [16] encode an underapproximation using
that X1 will not be executed before X0 . Consequently, all          m × n control literals, where m is the number of control
the combinations of the thread selection variables will pro-        points that guard each program statement and n is the num-
ber of processes. In our encoding, we use the same guards           Access Relations      Read-read     Read-write       Write-write
as in the schedule recording approach as control literals, we         Same variable       Equivalent   Non-equivalent   Non-equivalent
use lX0 = (ts1 = 2) && (ts2 = 1) and lY0 = (ts1 = 2). We            Different variables   Equivalent    Equivalent       Equivalent
also use information from the front-end (as described in Sec-
tion 2.1) to reduce substantially the number of control liter-     Table 1: Read-write analysis of interleavings equiv-
als required. If we were to include a control literal for each     alence between visible instructions.
statement as in [16], then our solution might not scale in
practice to large software systems.
   The main difference between the schedule recording and          safely merged into one. In order to implement RW-POR, we
the UW approaches is that schedule remains fixed and is by         compute the sets of variables written
                                                                                                       S(W Rj ) and read (RD
                                                                                                                             j)
default set to true while the UW model is updated based            by each of the threads. If W Rj ∩            RD k ∪ W R k = ∅
                                                                                                           k6=t
on the information extracted from the proof and is initially                    S
set to false. The widening process then works as follows.          and RDj ∩ k6=t W Rk = ∅, i.e., if the intersection between
Initially, each literal in L is set to be false, because we aim    the set of visible variables that are written and read by
to minimize the number of interleavings. At every state, we        thread j and all other threads is empty, then we only ex-
only consider the thread with the smallest index that has          plore the successors generated by executing j and all other
enabled transitions and only expand those. In our running          transitions can be safely ignored.
example, we first execute program statement Y1 because the            There are six possible combinations of visible instructions
tests x > 2 and x > 3 are false and consequently no other          of different threads, as shown in Table 1. There are three
thread has enabled transitions. As the global variable x           particular situations to consider when we generate the inter-
is set initially to 2 (line 3), at the first step we consider      leavings: (i) two read operations will not modify the state,
that only program statement Y1 is expanded from the ini-           so they will always generate equivalent interleavings, (ii)
tial state and build formula (3) by encoding Y1 statement as       two program statements accessing different variables are in-
lY0 ⇒ (x = 3). After that, we invoke the SMT solver to ex-         dependent w.r.t. their execution states, thus these two pro-
tract the unsatisfiable core and check that lY0 participated       gram statements always generate equivalent interleavings
in the proof of unsatisfiability. In the second iteration of our   with both execution orders, (iii) two instructions access-
algorithm, we remove lY0 from L in order to continue to the        ing same variable (i.e., with read-write and write-write re-
next iteration so that lY0 can now become either true or false     lations) will generate non-equivalent interleavings. In these
(while the others must remain false). Afterwards, we exe-          cases, the read-write relation actually causes read-write races
cute symbolically program statements X0 ; X1 ; Y0 and build        and the write-write relation causes the write-write races.
formula (3). We check that lX0 participated in the proof of        In summary, only two types of relations will generate non-
unsatisfiability. At the next iteration, we remove lX0 from        equivalent interleavings, while all other four types of rela-
L, execute symbolically program statements Y0 ; X0 ; X1 and        tions generate equivalent interleavings. Those redundant
build formula (3). At this iteration, we have found a vio-         interleavings are simply removed in our approach.
lation of the property and the UW procedure terminates;               Both PORs described above work best in conjunction with
otherwise the procedure would continue until none of the           an alias analysis. However, at this point in our work, we
additional literals in L participate in the proof of unsatis-      do not have one implemented. We thus assume that the
fiability. It means that the procedure does not rely on the        actual thread parameters are not aliased to global variables
underapproximation itself and concludes that the property          or to each other. In addition, we do not remove redundant
holds.                                                             interleavings originating from pointer aliasing.


2.4 Partial Order Reduction                                        3. MODELLING SYNCHRONIZATION
   In the modelling of multi-threaded software, we consider           PRIMITIVES IN PTHREAD
that any of the threads j ∈ T is able to make a transition            This section presents our modelling of the synchronization
and then we have V to compute all states for which a thread        primitives of the Pthread library [21]. We assume that the
j exists, (i.e., n j=1 γj (si , si+1 )). The problem is that the   library function implementations are correct and focus our
number of states to be explored can grow dramatically with         effort only on verifying client programs that use them. We
the number of program statements and threads. The pur-             thus provide an instrumented model of the Pthread func-
pose of the Partial-Order Reduction (POR) technique [1, 8,         tions and use this to model check the client code. We show,
15, 22] is to reduce the number of states that have to be          in our experiments, that our modelling is able to detect in-
explored. This is done in a way that if the property holds         correct use of the functions and is also able to detect blocking
on the reduced model, it also holds on the original model.         operations that can lead to global deadlocks.
   In our SMT-based BMC framework, as threads communi-
cate only through global variables, we apply partial order re-     3.1 Modelling Mutex Locking Operations
duction (POR) techniques at two levels in our algorithm. At          The Pthread library supports two functions to implement
the first level, we apply the visible instruction analysis POR     mutual exclusion between threads, pthread mutex lock and
(VI-POR) [22], which removes the interleavings of instruc-         pthread mutex unlock. The argument to these functions is
tions that do not affect the global variables, i.e., we remove     a C data structure called mutex that, in our modelling, has
transitions which are independent from transitions made by         two states, “locked” and “unlocked”. The pthread mutex lock
any other thread. An instruction is visible if it accesses a       locks the mutex if it is unlocked; otherwise it blocks the
global variable, and it is invisible otherwise. At the second      current thread until the mutex is released and can then be
level, we apply the read-write analysis POR (RW-POR) [8]           locked successfully again. The pthread mutex unlock un-
in which two (or more) independent interleavings can be            locks the mutex that was locked previously by the same
thread.                                                             1 #define         mutex lock field (a)
   Execution paths are considered to be blocked on a mu-            2                     (( a ) . data . l ock )
tex when the thread tries to lock a mutex that has already          3 #define m u t e x c o u n t f i e l d ( a )

been locked by other threads. Such blocking paths are also          4                     (( a ) . data . count )
                                                                    5 i n t p t h r e a d m u t e x l o c k ( p t h r e a d m u t e x t ∗ mutex )
called non-wait-free paths. In order to model mutex oper-           6 {
ations, we apply the notion of wait-free paths as proposed          7     s t a t i c Bool unlocked = 1 ;
initially in [24]. However, in contrast to [24], our approach is    8     extern unsigned i n t t r d s i n r u n ;
able to model check multi-threaded programs that make use           9     i f ( ! deadlock )
of mutexes, can handle more than two threads, can detect           10     {
deadlocks, and does not require the user to run the model          11         atomic begin ( ) ;
                                                                   12         u n l o c k e d = ( m u t e x l o c k f i e l d (∗ mutex )==0);
checker twice in order to detect different types of bugs (“reg-    13         i f ( unlocked )
ular” and concurrency bugs).                                       14             m u t e x l o c k f i e l d (∗ mutex )=1;
   To explain how mutexes are encoded in our SMT-based             15         else
BMC framework, we consider the example in Figure 5. In             16             m u t e x c o u n t f i e l d (∗ mutex)++;
this example, both threads TA and TB lock and unlock the           17         a to m i c e n d ( ) ;
same mutex m. The execution paths A0 ; A1 ; B0 ; B1 and            18
                                                                   19        atomic begin ( ) ;
B0 ; B1 ; A0 ; A1 are unblocked while the others are blocked       20        i f ( ! unlocked )
paths. However, instead of blocking the execution paths            21        {
starting with A0 ; B0 and B0 ; A0 , we simple ignore the state     22           i f ( ! m u t e x l o c k f i e l d (∗ mutex ) )
of the mutex, so that we do not block the remaining instruc-       23               m u t e x c o u n t f i e l d (∗ mutex)−−;
tions, and just lock it (again). In pthread mutex unlock,          24           d e a d l o c k = ( m u t e x c o u n t f i e l d (∗ mutex )
we simply check if the mutex is already locked and if so, we       25                               <t r d s i n r u n ) ;
                                                                   26           assert ( deadlock ) ;
release the lock; otherwise, we have detected an error.            27        }
                                                                   28        a to m i c e n d ( ) ;
START_THREAD      START_THREAD                                     29     }
                                         A1      B0
                                                                   30     return 0 ;
                                                            B1
                                                                   31 }
   A0: lock(m)      B0: lock(m)    A0
                                                                   32 i n t p t h r e a d m u t e x u n l o c k ( p t h r e a d m u t e x t ∗ mutex )
                                        B0         A1
                                                                   33 {
                                        A0             B1          34     atomic begin ( ) ;
  A1: unlock(m)    B1: unlock(m)   B0
                                                  A0        A1     35     a s s e r t ( m u t e x l o c k f i e l d (∗ mutex ) ) ;
                                         B1                        36     m u t e x l o c k f i e l d (∗ mutex )=0;
                                                                   37     a to m i c e n d ( ) ;
 END_THREAD        END_THREAD                                      38     return 0 ;
                                                                   39 }


  Figure 5: Execution paths blocking on a mutex.
                                                                        Figure 6: Modelling mutex lock and unlock opera-
   This modelling is sufficient to find bugs related to data            tions to detect global deadlock.
races. However, it is not able to detect deadlocks. In order
to detect global deadlock situations caused by the wrong use
of the mutexes, we need to look in more detail at the possible          count field, allow context switches, check if the mutex was
states that a thread can be in with our modelling: (i) Join             unlocked, and then assert count < trds in run. If the as-
state: The thread is waiting for thread termination; (ii) Lock          sertion fails, a global deadlock was detected (i.e., a thread
state: The thread is waiting for a mutex to be unlocked; (iii)          is blocked by a lock operation on a mutex and the required
Wait state: The thread is waiting for a signal or broadcast             mutex never gets unlocked by the thread that owns it, either
to wake up; (iv) Exit state: The thread has already exited;             because the locking thread has exited or because it has been
(v) Free state: The thread is not in any of the above four              blocked by another operation). If the assertion holds, we
states and is free to execute its instructions. A thread is             then eliminate this execution as described above. The mod-
blocked if it is in one of the join, lock or wait states, and           elling of the pthread mutex unlock, which is similar to [24],
is supposed to be running if it is not in exit state. Global            is shown at the bottom of Figure 6.
deadlock occurs if there is no running thread in the free state,
i.e., the number of blocked threads is equal to the number              3.2 Modelling Conditional Waiting
of running threads. In order to model deadlock, counts of                  In the Pthread library, we consider functions from con-
both blocked threads and running threads are maintained                 ditional waiting: pthread cond wait, pthread cond signal,
with global variables. Figure 6 presents our modelling of               and pthread cond broadcast. The arguments to the func-
pthread mutex lock to detect global deadlock with mutexes.              tion pthread cond wait are two data structures called cond
We define mutex lock f ield and mutex count f ield as a C               and mutex where, in our modelling, cond has also two states,
macro in lines 1 and 3 respectively.                                    “locked” and “unlocked”. The others functions have only
   We use the count field of the pthread mutex t data struc-            the argument cond. Our modelling of the conditional wait-
ture to count the number of threads that are in the lock                ing operation also employs the notion of wait-free execution
state due to this mutex, and trds in run to check the global            paths. The function pthread cond wait is used to block the
number of threads that are currently running. Initially, the            thread on a condition variable and the blocked thread is
mutex is unlocked and we only lock it after the first call to           awakened only if another thread calls signal or broadcast.
pthread mutex lock. In subsequent calls, we increase the                If there are several threads that are blocked on a condition
     variable, then the pthread cond signal call unblocks at least                  current thread, an assertion checks if a broadcast operation
     one of them (but there is no guarantee of which one will be                    has occurred by checking whether the current value of vari-
     woken up due to the scheduling policy) while the function                      able broadcast id is greater than the recorded broadcast id.
     pthread cond broadcast call unblocks all threads currently                     The deadlock is detected if there is no execution path with
     blocked on the specified condition variable.                                   broadcast operations.
        Figure 7 shows our modelling for the wait operation prim-
     itive. We consider that initially there is no deadlock (see line
     4) and whenever a thread calls pthread cond wait, we atom-
                                                                                    4. EXPERIMENTAL EVALUATION
     ically lock the condition variable cond, assert that the mutex                    We have implemented the lazy, schedule recording, and
     is currently locked, and then release the mutex so that other                  UW approaches described in Section 2 in our ESBMC1 (Ef-
     threads that access that mutex can make progress (i.e., wait-                  ficient SMT-Based Bounded Model Checker) tool that sup-
     free execution). Afterwards, we allow context switches and                     ports the SMT logics QF AUFBV as well as QF AUFLIRA
     we then check whether the number of threads in wait state                      from the SMT-LIB [26]. In our experiments, we have used
     (i.e., threads that are waiting for a signal or broadcast to                   ESBMC v1.3 together with the SMT solver Z3 [11].
     wake up) is less than the total number of the threads that                        The experimental evaluation of our work consists of two
     are currently running.                                                         parts. In Section 4.1, we compare our approaches against
                                                                                    the Monotonic Partial Order Reduction (MPOR) [18] and
                                                                                    Peephole Partial Order Reduction (PPOR) [27] that are im-
 1 i n t p t h r e a d c o n d w a i t ( p t h r e a d c o n d t ∗ cond ,
                                                                                    plemented in a SMT-based bounded model checker using
 2                                             p t h r e a d m u t e x t ∗mutex )
 3 {
                                                                                    the Yices SMT solver [12]. In Section 4.2, we compare our
 4     s t a t i c B o o l d e a d l o c k =0;                                      approaches against SATABS version 2.4 [7] connected to Ca-
 5     extern unsigned i n t t r d s i n r u n ;                                    dence SMV [19], which is a state-of-the-art C model checker
 6     i f ( ! deadlock )                                                           and supports the verification of multi-threaded software with
 7     {                                                                            shared variables using the CEGAR technique. All experi-
 8         atomic begin ( ) ;
                                                                                    ments were conducted on an otherwise idle Intel Xeon 5160,
 9         c o n d l o c k f i e l d (∗ cond )=1;
10         a s s e r t ( m u t e x l o c k f i e l d (∗ mutex ) ) ;                 3GHz server with 4 GB of RAM running Linux OS. For all
11         m u t e x l o c k f i e l d (∗ mutex )=0;                                benchmarks, the time limit has been set to 3600 seconds for
12         c o n d n w a i t e r s f i e l d (∗ cond )++;                           each individual property. All times given are wall clock time
13         a to m i c e n d ( ) ;                                                   in seconds as measured by the unix time command through
14         atomic begin ( ) ;                                                       a single execution.
15         i f ( c o n d l o c k f i e l d (∗ cond ) )
16         {                                                                        4.1 Comparison to MPOR and PPOR
17             d e a d l o c k = ( c o n d n w a i t e r s f i e l d (∗ cond ) <
18                                    trds in run );                                  We use the dining philosophers model to evaluate our
19             assert ( deadlock ) ;                                                approaches against MPOR and PPOR. Since the bench-
20         }                                                                        marks used in [18] are not available, we re-implemented
21         assume ( d e a d l o c k &&                                              them as described there. An implementation is available
22                         c o n d l o c k f i e l d (∗ cond )==0);
23         a to m i c e n d ( ) ;                                                   at users.ecs.soton.ac.uk/lcc08r/esbmc. Each philoso-
24         m u t e x l o c k f i e l d (∗ mutex )=1;                                pher has its own local variables, and they communicate only
25     }                                                                            through a global shared array of forks. This version guar-
26 }                                                                                antees the absence of deadlocks. As in [18], we also check
27 i n t p t h r e a d c o n d s i g n a l ( p t h r e a d c o n d t ∗ cond )       two properties: (i) whether all philosophers can eat simul-
28 {
                                                                                    taneously (this property does not hold, i.e., the verification
29     atomic begin ( ) ;
30     c o n d l o c k f i e l d (∗ cond )=0;                                       condition is unsatisfiable) and (ii) whether all philosophers
31     c o n d n w a i t e r s f i e l d (∗ cond )−−;                               have eaten at least once (this property holds, i.e., the verifi-
32     a to m i c e n d ( ) ;                                                       cation condition is satisfiable). The authors in [18] run their
33     return 0 ;                                                                   experiments on a workstation with 2.8 GHz Xeon processor
34 }                                                                                and 4GB of RAM memory running Linux OS. In order to
                                                                                    make the results comparable, we scale their times in Table 2.
                                                                                    We give both original (in brackets) and scaled timings.
     Figure 7: Modelling conditional waiting and signal                               Table 2 shows the detailed results of the comparison be-
     operations to detect global deadlock.                                          tween MPOR, PPOR, and the three ESBMC approaches.
                                                                                    The first column #L gives the number of lines of code, while
        In order to model signal operations, we simply release the                  the second column #T reports the total number of threads.
     condition variable and decrement the number of threads that                    The Time column provides the time in seconds while the col-
     were locked due to the specified condition variable. The                       umn #I provides the total number of generated interleavings
     modelling of the conditional signal operation is shown in                      and the column #IF the total number of failed interleavings.
     Figure 7 as well.                                                              The column Iter gives the number of iterations to prove or
        In order to model broadcast operations, we create an addi-                  disprove the property in the UW approach.
     tional global variable called broadcast id, which records the                    As we can see in Table 2, our approaches perform equiva-
     number of broadcast operations that have executed and also                     lently to MPOR to check the first property of the model until
     gets incremented inside the function pthread cond broadcast.                   we set the number of philosophers to 5. If we continue in-
     In the wait operation the thread firstly records the current                   creasing the number of philosophers, MPOR performs better
     broadcast id and is then forced to make context switches to
                                                                                    1
     other threads. When the context is switched back to the                            Available at http://users.ecs.soton.ac.uk/lcc08r/esbmc/
                                                MPOR            PPOR               Lazy        Schedule      UW
                  Module            #L #T        Time            Time        Time    #I/#IF     Time      Time Iter
             1    din phil2 unsat   63  2      0.2 (0.2)       0.1 (0.1)      0.2       2/0       0.2      0.2   1
             2    din phil3 unsat   63  3      0.8 (0.9)       1.0 (1.1)      0.5       6/0      0.4       0.5   1
             3    din phil4 unsat   63  4      5.0 (5.3)      41.9 (44.9)      2       24/0      1.6       1.6   1
             4    din phil5 unsat   63  5     21.4 (22.9)    138.7 (148.6)   11.1     120/0      8.3       8.7   1
             5    din phil6 unsat   63  6     48.8 (52.3)    470.4 (504.4)    74      720/0     115.8     115.4  1
             6    din phil7 unsat   63  7    150.8 (161.6)        TO         574.1    5040/0     TO        TO    0
             7    din phil2 sat     63  2      0.1 (0.1)       0.1 (0.1)      0.2       2/2       0.2      0.4   3
             8    din phil3 sat     63  3      1.2 (1.3)       0.3 (0.3)      0.2       6/6       0.5      1.6   4
             9    din phil4 sat     63  4      8.9 (9.5)       3.6 (3.8)      0.2     24/24       1.8      2.6   5
             10   din phil5 sat     63  5     88.4 (94.7)     57.6 (61.7)     0.3    120/120      8.8      33    6
             11   din phil6 sat     63  6    294.4 (315.4)   2130.8 (2283)    0.3    720/720    105.6     105.2  1
             12   din phil7 sat     63  7    1136.8 (1218)        TO          0.3 5040/5040      TO        TO    0


        Table 2: Results of the comparison between MPOR, PPOR, lazy, schedule, and UW ESBMC


than our approaches. However, our three approaches per-             erties of a given program and Failed indicates how many
form better than PPOR to check the first property. In ad-           properties failed during the verification process. Here, prop-
dition, our lazy ESBMC scales significantly better than the         erties can fail for two reasons: either due to a time out (TO)
other approaches to check the second property of the dining         or due to memory out (MO).
philosophers model, i.e., whether all philosophers have eaten          As we can see in Table 3, our lazy ESBMC approach
at least once. We also show in column #I/#IF that all inter-        performs significantly better than the other approaches on
leavings generated by our lazy ESBMC are satisfiable. Our           benchmarks that contain bugs (i.e., the formula sent to the
UW and schedule ESBMC also performs better than MPOR                SMT solver is satisfiable). However, if there is no bug in the
and PPOR until we set the number of philosophers to 6. In           benchmark, then our schedule ESBMC approach performs
summary, our lazy approach outperforms both MPOR and                better than the UW and lazy ESBMC, but not as good as
PPOR for those benchmarks that generate satisfiable for-            SATABS for the dining philosophers benchmark. This indi-
mulae and is still comparable to MPOR and PPOR when                 cates that our SMT-based BMC procedures do not scale well
the generated formulae are unsatisfiable.                           for problems of increasing complexity, i.e., for a large num-
                                                                    ber of threads and data dependencies among the threads.
4.2 Comparison to SATABS                                            However, SATABS times out for programs 17 and 18, and
   In order to evaluate our approaches against SATABS, we           provides false results for programs 7-12, 15, 23, and 24, of
used a number of multi-threaded programs taken from stan-           which the last two contain deadlocks due to the incorrect use
dard benchmark suites (see Table 3). Programs 1-12 are an           of lock and unlock operations. Based on that, we conclude
implementation of the dining philosophers as described in           that SATABS does not seem to explore all interleavings and
Section 4.1. In the dining philosophers implementation, we          also does not add additional checks for detecting deadlocks,
set the number of philosophers (threads) to 2, 3, . . . , 7 and     which explains the better scaling for the dining philosophers
compare the runtime performance of the three approaches             benchmark.
against SATABS. The programs 13-22 are taken from the                  We can see that our UW ESBMC algorithm outperforms
benchmark suite of the INSPECT tool [28]. This suite con-           SATABS in most of the multi-threaded programs from Ta-
tains programs with two or more threads as well as mutex            ble 3, except for the programs 5, 6, 10, 11, and 12. How-
and condition synchronization primitives from the Pthread           ever, in these programs SATABS provides false results as
library. The programs 23 and 24 are taken from the Helgrind         discussed above. In any case, it is important to note that
benchmark suite [2] and they contain concurrency bugs re-           when we enabled the proof generation feature of the SMT
lated to lock and unlock operations. It is important to note        solver to extract the unsatisfiable cores, we always observed
that most of these benchmarks contain data dependencies             memory overhead and corresponding slowdowns, as also re-
among the threads (i.e., the threads access the global vari-        ported previously in [10]. Additionally, we observed that
ables).                                                             the performance of the UW ESBMC procedure can be sig-
   Table 3 shows the detailed results of the comparison be-         nificantly improved if we use heuristics to update the set of
tween UW, Lazy, and schedule ESBMC as well as SATABS.               additional literals in L to be used at the next iteration of
We do not run the programs 19-22 with SATABS because                the algorithm. However, at this point in time, we do not
it does not support the condition synchronization primitive.        investigate further alternative ways of updating the set L.
It is also important to point out that the verification times       We set the maximum size of the unsatisfiable core to contain
of the programs 1-12 in Table 3 differ from Table 2 because         500 control literals since the SMT solver Z3 fails with a seg-
instead of checking a single property, here we check prop-          mentation fault when there are thousands of literals. This
erties related to mutex operations and array bounds, which          situation occurs only with the dining philosophers model
can be automatically generated by both tools, SATABS and            when we set the number of philosophers to 6 or more. We
ESBMC. Hence, the column #P gives the number of prop-               reported this bug to the Z3 developers and they were already
erties to be verified for each multi-threaded C program. The        aware of this problem.
Time column provides the time in seconds to check all prop-
                                          SATABS                                        UW                                   Schedule                                              Lazy
                                       Time   #P                             Time        #P                               Time    #P                            Time              #P                     #I




                                                                                                                                                                                                         #I / #IF
                                                         Violated




                                                                                               Violated




                                                                                                                                            Violated




                                                                                                                                                                                  Violated
                                                Passed




                                                                                      Passed




                                                                                                                                   Passed




                                                                                                                                                                         Passed
                                                                    Failed




                                                                                                          Failed




                                                                                                                                                       Failed




                                                                                                                                                                                             Failed
                                        Total




                                                                              Total




                                                                                                                           Total




                                                                                                                                                                 Total
                                                                                                                   Iter
          Module              #L #T
      1   din phil2 unsat     63  2      26     13        0          0        0.3     28        0  0               1        0.2    28        0  0                 0.3    28          0        0             2/0
      2   din phil3 unsat     63  3      26     13        0          0        0.6     28        0  0               1        0.5    28        0  0                 0.7    28          0        0             6/0
      3   din phil4 unsat     63  4      26     13        0          0        2.3     28        0  0               1        1.7    28        0  0                 2.7    28          0        0            24/0
      4   din phil5 unsat     63  5    26.2     13        0          0       12.3     28        0  0               1        9.4    28        0  0                  14    28          0        0           120/0
      5   din phil6 unsat     63  6    26.4     13        0          0        142     28        0  0               1      123.8    28        0  0                91.7    28          0        0           720/0
      6   din phil7 unsat     63  7    27.1     13        0          0        TO       0        0 28               0       MO       0        0 28               719.2    28          0        0          5040/0
      7   din phil2 sat       63  2    30.1     18        0          0        0.5     28        1  0               3        0.3    28        1  0                 0.2    28          1        0             2/2
      8   din phil3 sat       63  3    28.4     18        0          0        2.2     28        1  0               4        0.7    28        1  0                 0.2    28          1        0             6/6
      9   din phil4 sat       63  4    28.4     18        0          0       3.05     28        1  0               5        2.4    28        1  0                 0.2    28          1        0           24/24
     10   din phil5 sat       63  5    28.6     18        0          0       42.5     28        1  0               6       14.4    28        1  0                 0.3    28          1        0         120/120
     11   din phil6 sat       63  6    27.8     18        0          0        180     28        1  0               1      177.5    28        1  0                 0.3    28          1        0         720/720
     12   din phil7 sat       63  7    28.9     18        0          0       MO       28        1  0               0       MO      28        1  0                 0.3    28          1        0       5040/5040
     13   carter01 ok         58   2     25       2       0          0        0.3       4       0           0      1       0.3       4       0           0       0.3       4         0        0                     2/0
     14   lazy01 ok           48   3      3       1       0          0        0.2       4       0           0      1       0.2       4       0           0       0.3       4         0        0                     6/0
     15   phase01 ok          34   1     23       0       1          0        0.2       4       0           0      1       0.2       4       0           0       0.2       4         0        0                     2/0
     16   stateful01 ok       47   2      2       1       0          0        0.2       4       0           0      1       0.2       4       0           0       0.2       4         0        0                     2/0
     17   stateful06 ok       59   2    TO        0       0          2        0.2       5       0           0      1       0.2       5       0           0       0.2       5         0        0                     2/0
     18   stateful20 ok       61   3    TO        0       0          2        5.7       5       0           0      1       3.3       5       0           0       0.7       5         0        0                     6/6
     19   sync01 ok           62   2      -       -       -          -        0.2       4       0           0      1       0.3       4       0           0       0.3       4         0        0                     2/0
     20   sync01 bad          62   2      -       -       -          -        0.3       3       1           0      1       0.3       3       1           0       0.3       3         1        0                     2/1
     21   sync02 ok           73   2      -       -       -          -        0.3       4       0           0      1       0.3       4       0           0       0.3       4         0        0                     2/0
     22   sync02 bad          73   2      -       -       -          -        0.3       3       1           0      1       0.3       3       1           0       0.3       3         1        0                     2/1
     23   tc10 rec lock bad   49   1    0.3  7            0          0        0.3       8       2  0               1       0.3       8       2  0                0.3  8            2          0            1/1
     24   tc14 laog bad       45   5     20 17            0          0        TO        0       0 28               2       TO        0       0 28                0.8 10           18          0        120/120


               Table 3: Results of the comparison between SATABS, UW, schedule, and lazy ESBMC


5.        RELATED WORK                                                                             context-switches, as described in [4]. This approach, how-
   SMT-based BMC is gaining popularity in the formal veri-                                         ever, is limited to two threads and it requires additional
fication community due to the advent of sophisticated SMT                                          constraints to bound the number of context switches and
solvers built over efficient SAT solvers [11]. Ganai and Gupta                                     allowed interleavings into the formula to be sent to a SAT
describe a verification framework for BMC which extracts                                           solver.
high-level design information from an extended finite state                                           Ganai and Gupta describe a lazy method for modelling
machine (EFSM) and apply several techniques to simplify                                            multi-threaded concurrent systems using shared variables [14],
the BMC problem [13]. However, the authors use only the                                            but this method is restricted to two threads. Gupta et al. [18]
theory of integer and real arithmetic, which does not re-                                          extend [14, 17] by supporting more than two threads and
flect precisely the ANSI-C semantics. Armando et al. also                                          by combining dynamic partial order reduction with sym-
propose a BMC approach using SMT solvers for ANSI-C                                                bolic state space exploration. However, this method is in-
programs [5], but they only make use of linear arithmetic,                                         complete since it considers the concurrency semantics up to
arrays, records and restricted bit-vectors arithmetic and, as                                      the bounded depth as in [4, 24]. Grumberg et al. propose
a consequence, their SMT-CBMC prototype does not ad-                                               an algorithmic method based on SAT and BMC to model
dress important constructs of the ANSI-C language.                                                 check a multi-process system based on a series of under-
   Qadeer and Rehof present a pragmatic method to discover                                         approximated models [16]. This approach, however, does not
bugs in concurrent software in which the program analysis is                                       integrate partial order reduction algorithms to reduce redun-
restricted to executions with a bounded number of context                                          dant interleavings and it does not address the problem of
switches [23]. However, this method is incomplete since it                                         model checking real-world embedded software in multi-core
considers the verification up to a given fixed context bound.                                      environments.
In addition, the authors do not apply it to realistic and large                                       To the best of our knowledge, there is no work that consid-
concurrent software benchmarks and the integration of this                                         ers a comprehensive SMT-based BMC formulation to verify
context-bounded model checking algorithm into the explicit                                         multi-threaded software using a set of under-approximations
state model checker ZING [4] is left for future work. Ra-                                          and widening models as well as the integration of partial
binovitz and Grumberg describe an extension of CBMC to                                             order reduction algorithms into the UW framework. In con-
concurrent C programs [24], which translates C threads into                                        trast to [14, 24], our method can handle more than two
SSA form and adds constraints for a bounded number of                                              threads and can detect deadlock caused by the mutexes and
conditions operations. Our main contribution is an algo-             [10] L. M. de Moura and N. Bjørner. Proofs and
rithmic method and corresponding tools to verify multi-                   refutations, and z3. In LPAR, 2008.
threaded software using SMT in order to combat the ver-              [11] L. M. de Moura and N. Bjørner. Z3: An efficient SMT
ification complexity.                                                     solver. In TACAS, LNCS 4963, pp. 337–340, 2008.
                                                                     [12] B. Dutertre and M. L. d. The Yices SMT solver. Tool
6.   CONCLUSIONS AND FUTURE WORK                                          paper, http://yices.csl.sri.com/documentation.shtml.
                                                                     [13] M. K. Ganai and A. Gupta. Accelerating high-level
   Despite the large body of (theoretical) research in the ver-
                                                                          bounded model checking. In ICCAD, pp. 794–801,
ification of concurrent systems, there are only few tools that
                                                                          2006.
analyze multi-threaded programs with shared variables. In
this work, we presented an extension of the ESBMC model              [14] M. K. Ganai and A. Gupta. Efficient modeling of
checker to support the verification of multi-threaded soft-               concurrent systems in BMC. In SPIN, LNCS 5156, pp.
ware with shared variables, mutexes and conditions using                  114–133, 2008.
an SMT-based BMC framework. We also described three                  [15] P. Godefroid. Partial-order Methods for the
approaches UW, lazy and eager SMT-based BMC imple-                        Verification of Concurrent Systems: An Approach to
mented with partial-order reduction methods in which the                  the State-explosion Problem. PhD thesis, 1995.
final formula is well suited for using with the SMT solvers.         [16] O. Grumberg, F. Lerda, O. Strichman, and
Our experimental results show that our UW ESBMC ap-                       M. Theobald. Proof-guided
proach outperforms the CEGAR approach implemented in                      underapproximation-widening for multi-process
the SATABS model checker. With the addition of deadlock                   systems. In POPL, pp. 122–131, 2005.
detection in our modelling, we can find bugs that other pre-         [17] V. Kahlon, S. Sankaranarayanan, and A. Gupta.
vious approaches are not able to find. Moreover, our lazy                 Semantic reduction of thread interleavings in
ESBMC, which adds concurrency constraints lazily and in-                  concurrent programs. In TACAS, LNCS 5505, pp.
crementally, is able to find bugs quickly in non-trivial bench-           124–138, 2009.
marks. In future, we would like to explore in more depth             [18] V. Kahlon, C. Wang, and A. Gupta. Monotonic
the partial-order reduction methods, configure ESBMC for                  partial order reduction: An optimal symbolic partial
compatibility with any given compiler to break statements                 order reduction technique. In CAV, pp. 398–413, 2009.
with multiple global variables, and investigate heuristics to        [19] K. McMillan. The Cadence SMV Model Checker.
update the set of additional literals in our UW ESBMC al-                 http://www.kenmcmil.com/smv.html.
gorithm.                                                             [20] K. L. McMillan and N. Amla. Automatic abstraction
Acknowledgments. We thank D. Kroening for the fruitful dis-               without counterexamples. In TACAS, LNCS 2619, pp.
cussions about the starting point of this work and J. Rathke for          2–17, 2003.
many helpful discussions about multi-process systems. We also        [21] F. Mueller. A library implementation of posix threads
thank S. Yiu for his work in his MSc Thesis [29] on model checking        under unix. In USENIX, pp. 29–41, 1993.
concurrent programs with SAT. We thank J. Colley, D. Nicole,
                                                                     [22] D. Peled. All from one, one for all: on model checking
R. Silva, and R. Quigley for their comments on a draft version.
                                                                          using representatives. In CAV, pp. 409–423, 1993.
                                                                     [23] S. Qadeer and J. Rehof. Context-bounded model
7.   REFERENCES                                                           checking of concurrent software. In TACAS, LNCS
                                                                          3440, pp. 93–107, 2005.
 [1] E. Clarke, O. Grumberg, and D. Peled. Model
     Checking. The MIT Press, Cambridge, MA, 2000.                   [24] I. Rabinovitz and O. Grumberg. Bounded model
                                                                          checking of concurrent programs. In CAV, LNCS 3576,
 [2] Helgrind: a thread error detector. http://valgrind.org/.
                                                                          pp. 82–97, 2005.
 [3] R. Alur et al. Partial-order reduction in symbolic
                                                                     [25] J. P. Marques-Silva and K. A. Sakallah. Grasp - a new
     state-space exploration. FMSD, 18(2):97–116, 2001.
                                                                          search algorithm for satisfiability. In ICCAD, pp.
 [4] T. Andrews et al. Zing: Exploiting program structure                 220–227, 1996.
     for model checking concurrent software. In CONCUR,
                                                                     [26] SMT-LIB. The Satisfiability Modulo Theories Library.
     pp. 1–15, 2004.
                                                                          http://combination.cs.uiowa.edu/smtlib.
 [5] A. Armando, J. Mantovani, and L. Platania. Bounded
                                                                     [27] C. Wang, Z. Yang, V. Kahlon, and A. Gupta. Peephole
     model checking of software using SMT solvers instead
                                                                          partial order reduction. In TACAS, pp. 382–396, 2008.
     of SAT solvers. Int. J. Softw. Tools Technol. Transf.,
     pp. 69–83, 2009.                                                [28] Y. Yang. Inspect: A Framework for Dynamic
                                                                          Verification of Multithreaded C Programs.
 [6] A. Biere. Bounded model checking. In Handbook of
                                                                          http://www.cs.utah.edu/∼yuyang/inspect/.
     Satisfiability, pp. 457–481. 2009.
                                                                     [29] S. Yiu. Model Checking Concurrent Programs with
 [7] E. Clarke, D. Kroening, N. Sharygina, and K. Yorav.
                                                                          SAT. MSc thesis, Southampton, 2009.
     SATABS: SAT-based predicate abstraction for
     ANSI-C. In TACAS 2005, LNCS 3440, pp. 570–574,
     2005.
 [8] B. Cook, D. Kroening, and N. Sharygina. Symbolic
     model checking for asynchronous boolean programs. In
     SPIN, pp. 75–90, 2005.
 [9] L. Cordeiro, B. Fischer, and J. Marques-Silva.
     SMT-based bounded model checking for embedded
     ANSI-C software. In ASE, pp. 137–148, 2009.
