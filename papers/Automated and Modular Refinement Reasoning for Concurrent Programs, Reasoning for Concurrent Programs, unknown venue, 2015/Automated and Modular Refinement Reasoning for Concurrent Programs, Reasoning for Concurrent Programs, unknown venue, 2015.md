           Automated and Modular Refinement
           Reasoning for Concurrent Programs

    Chris Hawblitzel1 , Erez Petrank2 , Shaz Qadeer1 , and Serdar Tasiran3(B)
                               1
                                 Microsoft, Redmond, USA
                                   2
                                   Technion, Haifa, Israel
                            3
                              Koç University, Istanbul, Turkey
                                   stasiran@ku.edu.tr


       Abstract. We present civl, a language and veriﬁer for concurrent
       programs based on automated and modular reﬁnement reasoning. civl
       supports reasoning about a concurrent program at many levels of abstrac-
       tion. Atomic actions in a high-level description are reﬁned to ﬁne-grain
       and optimized lower-level implementations. A novel combination of auto-
       mata theoretic and logic-based checks is used to verify reﬁnement. Modu-
       lar speciﬁcations and proof annotations, such as location invariants and
       procedure pre- and post-conditions, are speciﬁed separately, indepen-
       dently at each level in terms of the variables visible at that level. We have
       implemented civl as an extension to the boogie language and veriﬁer.
       We have used civl to reﬁne a realistic concurrent garbage collection algo-
       rithm from a simple high-level speciﬁcation down to a highly-concurrent
       implementation described in terms of individual memory accesses.


1    Introduction
We present a technique for verifying a reﬁnement relation between two concur-
rent, shared-memory multithreaded programs. Our work is inspired by stepwise
reﬁnement [43], where a high-level description is systematically reﬁned, poten-
tially via several intermediate descriptions, down to a detailed implementation.
Reﬁnement checking is a classical problem in veriﬁcation and has been inves-
tigated in many contexts, including hardware veriﬁcation [11] and veriﬁcation
of cache-coherence protocols and distributed algorithms [32]. In the realm of
sequential software, notable successes using the reﬁnement approach include the
work of Abrial et al. [2] and the proof of full functional correctness of the seL4
microkernel [30]. This paper presents the ﬁrst general and automated proof sys-
tem for reﬁnement veriﬁcation of shared-memory multithreaded software.
    We present our veriﬁcation approach in the context of civl, an idealized
concurrent programming language. In civl, a program is described as a collec-
tion of procedures whose implementation can use the standard features such as
assignment, conditionals, loops, procedure calls, and thread creation. Each proce-
dure accesses shared global variables only through invocations of atomic actions.
A subset of the atomic actions may be reﬁned by new procedures and a new pro-
gram is obtained by replacing the invocation of an atomic action by a call to the
corresponding procedure reﬁning the action. Several layers of reﬁnement may

c Springer International Publishing Switzerland 2015
D. Kroening and C.S. Păsăreanu (Eds.): CAV 2015, Part II, LNCS 9207, pp. 449–465, 2015.
DOI: 10.1007/978-3-319-21668-3 26
450      C. Hawblitzel et al.

be performed until all atomic actions in the ﬁnal program are directly imple-
mentable primitives. Unlike classical program veriﬁers based on Floyd-Hoare
reasoning [20,28] that manipulate a program and annotations, the civl veriﬁer
manipulates multiple operational descriptions of a program, i.e., several layers
of reﬁnement are speciﬁed and veriﬁed at once.
    To prove reﬁnement in civl, a simulation relation between a program and
its abstraction is inferred from checks on each procedure, thus decomposing a
whole-program reﬁnement problem into per-procedure veriﬁcation obligations.
The computation inside each such procedure is partitioned into “steps” such
that one step behaves like the atomic speciﬁcation and all other steps have no
eﬀect on the visible state. This partitioning follows the syntactic structure of
the code in a way similar in spirit to Floyd-Hoare reasoning. To express the per-
procedure veriﬁcation obligations in terms of a collection of per-step veriﬁcation
tasks, the civl veriﬁer needs to address two issues. First, the notion of a “step”
in the code implementing a procedure must be deﬁned. The deﬁnition of a step
can deeply aﬀect the number of checks that need to be performed and the number
of user annotations. Second, it is typically not possible to show the correctness
of a step from an arbitrary state. A precondition for the step in terms of shared
variables must be supplied by the programmer and mechanically checked by the
veriﬁer.
    To address the ﬁrst problem, civl lets the programmer deﬁne the granularity
of a step, allowing the user to specify a semantics with larger atomic actions.
A cooperative semantics for the program is explicitly introduced by the pro-
grammer through the use of a new primitive yield statement; in this semantics a
thread can be scheduled out only when it is about to execute a yield statement.
The preemptive semantics of the program is sequentially consistent execution;
all threads are imagined to execute on a single processor and preemption, which
causes a thread to be scheduled out and a nondeterministically chosen thread
to be scheduled in, may occur before any instruction.1 Given a program P ,
civl veriﬁes that the safety of the cooperative semantics of P implies the safety
of the preemptive semantics of P . This veriﬁcation is done by computing an
automata-theoretic simulation check [24] on an abstraction of P in which each
atomic action of P is represented by only its mover type [17,35]. The mover
types themselves are veriﬁed separately and automatically using an automated
theorem prover [9].
    To address the second problem that reﬁnement veriﬁcation for each step
requires invariants about the program execution, civl allows the programmer
to specify location invariants, attached either to a yield statement or to a proce-
dure as its pre- or post-condition. Each location invariant must be correct for all
executions and must continue to hold in spite of potential interference from con-
currently executing threads. We build upon classical work [29,38] on reasoning
about non-interference with two distinct innovations. First, we do not require the
annotations to be strong enough to prove program correctness but only strong
1
    In this paper, we focus our attention on sequential consistency and leave considera-
    tion of weak memory models to future work.
    Automated and Modular Reﬁnement Reasoning for Concurrent Programs            451

enough to provide the context for reﬁnement checking. Program correctness is
established via a sequence of reﬁnement layers from an abstract program that
cannot fail. Second, to establish a postcondition of a procedure, we do not need
to propagate a precondition through all the yield annotations in the procedure
body. The correctness of an atomic action speciﬁcation gives us a simple frame
rule—the precondition only needs to be propagated across the atomic action
speciﬁcation. civl further simpliﬁes the manual annotations required for logical
non-interference checking by providing a linear type system [42] that enables
logical encoding of thread identiﬁers, permissions [7], and disjoint memory [31].
    Finally, civl provides a simple module system. Modules can be veriﬁed sep-
arately, in parallel or at diﬀerent times, since the module system soundly does
away with checks that pertain to cross-module interactions. This feature is signif-
icant since commutativity checks and non-interference checks for location invari-
ants are quadratic, whole program checks involving all pairs of yield locations
and atomic blocks, or all pairs of actions from a program. Using the module
system, the number of checks is reduced; they become quadratic in the number
of yields and atomic blocks within each module rather than the entire program.
    We have implemented civl as a conservative extension of the boogie veriﬁer.
We have used it to verify a collection of microbenchmarks and benchmarks from
the literature [6,13–15,19,27]. The most challenging case study with civl was
carried out concurrently with civl’s development and served as a design driver.
We veriﬁed a concurrent garbage collector, through six layers of reﬁnement,
down to atomic actions corresponding to individual memory accesses. The level
of granularity of the lowest-level implementation distinguishes this veriﬁcation
eﬀort, detailed in a technical report [23], from previous attempts in the literature.
    In conclusion, civl is the ﬁrst automated veriﬁer for shared-memory mul-
tithreaded programs that provides the capability to establish a multi-layered
reﬁnement proof. This novel capability is enabled by two important innovations
in core veriﬁcation techniques for reducing the complexity of invariants supplied
by the programmer and the veriﬁcation conditions solved by the prover.
– Reasoning about preemptive semantics is replaced by simpler reasoning about
  cooperative operational semantics by exploiting automata-theoretic simula-
  tion checking. This is a novel technique that combines automata-based and
  logic-based reasoning.
– A linear type system establishes invariants about disjointness of permission
  sets associated with values contained in program variables. These invariants,
  communicated to the prover as free assumptions, signiﬁcantly reduce the over-
  head of program annotations. We are not aware of any other veriﬁer that
  combines type-based and logic-based reasoning in this style.

2    Overview
We present an overview of our approach to reﬁnement on an example (Fig. 1)
inspired by the write barrier in our concurrent garbage collector (GC). In a con-
current GC, each object in the heap has a color: UNALLOC, WHITE, GRAY, or BLACK.
452     C. Hawblitzel et al.

The GC traverses reachable objects, marking the reached objects GRAY and then
BLACK. At the end of the traversal, reached objects are BLACK, unreached objects
are WHITE, and the GC deallocates the WHITE objects. The threads in the sys-
tem must cooperate with the GC to ensure that the collection creates no dangl-
ing pointers (i.e., if object A is reachable and A points to object B, then B should
var Color: int; // UNALLOC=0, WHITE=1,      not be deallocated). Therefore, before
                 // GRAY=2, BLACK=3
                                            a mutator thread mutates an object A
procedure WB(linear tid:Tid)                to point to an object B, the thread
atomic [if (Color == WHITE) Color := GRAY];
requires Color >= WHITE;
                                            executes a write barrier to check the
ensures Color >= GRAY;                      color of B. If B is WHITE, the write
{
  var cNoLock:int;
                                            barrier darkens B’s color to GRAY to
  yield Color >= WHITE;                     ensure that the GC does not deallo-
  cNoLock := GetColorNoLock(tid);
  yield Color >= cNoLock;
                                            cate B. WB implements the write bar-
  if (cNoLock <= WHITE)                     rier. The write barrier is only invoked
    call WBSlow(tid);
  yield Color >= GRAY;
                                            on allocated objects, thus, colors can-
}                                           not be UNALLOC when WB is called. To
procedure WBSlow(linear tid:Tid)
                                            simplify exposition, we consider a sin-
atomic [if (Color <= WHITE) Color := GRAY]; gle object whose color is stored in the
{
  var cLock:int;
                                            shared variable Color. WB ﬁrst reads
  call AcquireLock(tid);                    Color without holding a lock, to avoid
  cLock := GetColorLocked(tid);
  if (cLock <= WHITE)
                                            when possible, the cost of acquiring
    call SetColorLocked(tid, GRAY);         and releasing a lock for each object
  call ReleaseLock(tid);
}
                                            encountered by a mutator. If Color <=
                                            WHITE, WB calls the more expensive pro-
procedure GetColorNoLock(linear tid:Tid)
  returns (cl:int) atomic [...];
                                            cedure WBSlow to re-examine and pos-
procedure AcquireLock(linear tid:Tid)       sibly update Color while holding the
  right [...];
procedure ReleaseLock(linear tid:Tid)
                                            lock. The annotation yield Color >=
  left [...];                               cNoLock is a local invariant expected
procedure GetColorLocked(linear tid:Tid)
  returns (cl:int) both [...];
                                            to be preserved by the environment
procedure SetColorLocked(linear tid:Tid,    of WB. civl simpliﬁes reasoning about
  cl: int) atomic [...];
                                            WBSlow by allowing us to express its
                                            speciﬁcation as the following atomic
           Fig. 1. Write barrier            action:
[if (Color <= WHITE) Color := GRAY] This speciﬁcation indicates that regard-
less of how the environment interferes with its execution, to its caller it appears
as if WBSlow atomically executes the code above.
Per-procedure Simulation, Non-interference via Invariants. The veriﬁ-
cation of WB illustrates a combination of techniques. We ﬁrst explain how WB’s
post-condition is veriﬁed. To see that this task is not trivial, consider a scenario
in which WB, not holding a lock, reads Color and sets cNoLock to GRAY and then
yields. Another thread sets Color to WHITE. WB resumes, but because the local
variable cNoLock is GRAY, does nothing and exits with Color being WHITE, vio-
lating WB’s postcondition. But, in the GC this scenario is not possible. The yield
predicate (location invariant) Color >= cNoLock expresses the fact that other
threads can only modify Color to a higher (darker) value. civl veriﬁes the
   Automated and Modular Reﬁnement Reasoning for Concurrent Programs          453

correctness of this location invariant and rules out this undesirable scenario.
Using this location invariant, WB’s pre-condition, and WBSlow’s atomic speciﬁca-
tion, civl is able to verify WB’s post-condition.
    In Fig. 1, we suppose for illustration’s sake that WB and WBSlow have slightly
diﬀerent atomic speciﬁcations, one testing for Color == WHITE and the other for
Color <= WHITE. In this case, verifying that the implementation of WB reﬁnes
its atomic speciﬁcation relies on Color not being UNALLOC. Otherwise, WBSlow
would set Color to GRAY whereas WB would leave it unmodiﬁed, leading to a
reﬁnement violation. WB’s precondition Color >= WHITE and the location invari-
ant Color >= cNoLock imply that Color is never UNALLOC during the execution
of WB. Given this constraint, civl checks atomicity reﬁnement for WB by verifying
the existence of a particular simulation-relation. Each control path through WB is
analyzed as a sequence of code fragments, from one yield statement to the next.
For each control path through a procedure, exactly one code fragment must be
simulated by the atomic action speciﬁcation while others do not modify global
state. This reﬁnement proof for WB makes use of (1) correct modeling of envi-
ronment interference by the pre- and post-conditions, and the yield predicate,
and (2) the atomic action speciﬁcation for the called procedure WBSlow. The
civl veriﬁer automatically computes a logical veriﬁcation condition capturing
the proof obligations from the body and speciﬁcation of WB.
    Just as the veriﬁcation of WB builds on the speciﬁcation of WBSlow, the veriﬁ-
cation of WBSlow builds on other reﬁnement proofs (not shown) of the procedures
called in WBSlow; these procedures are shown at the bottom of the ﬁgure. This
example shows only one procedure at this layer. In programs with many proce-
dures with atomic speciﬁcations at each layer, civl combines the per-procedure
reﬁnement proofs soundly into a whole-program reﬁnement proof.
Preemptive vs Cooperative Semantics. The veriﬁcation of WBSlow high-
lights another important feature in civl. Reﬁnement checking is performed on
cooperative semantics in which a yield-to-yield execution fragment of code is
executed atomically. However, in a real execution, control can switch between
threads at any point in the code. A naive modeling of a real execution would
put a yield statement before every instruction in the code. The absence of a
yield statement before every instruction is justiﬁed by reasoning about mover
types [17]. The procedures called in WBSlow have the mover types claimed in their
declarations and veriﬁed by civl. For example, the mover type of AcquireLock
is right which indicates that it commutes later in time against concurrently
executing environment actions. These mover types are checked by constructing
veriﬁcation conditions from each pair of atomic actions.
                                               Given veriﬁed mover types for
                                           actions, civl veriﬁes the correctness
                                           of the placement of yield statements
                                           using a novel approach. A yield suﬃ-
    Fig. 2. Yield suﬃciency automaton      ciency automaton (Fig. 2) encodes all
sequences of atomic actions (of Right, Left, Both and Non-mover types)
and yields for which safety of cooperative semantics is suﬃcient for safety of
454      C. Hawblitzel et al.

preemptive semantics. Each “transaction” starts with a sequence of right movers
(or both movers) and ends with a sequence of left movers (or both movers). In
the middle, it can have at most one non mover. Transactions must be separated
by yield statements. civl then interprets the control-ﬂow graph of each pro-
cedure as an automaton with mover types as edge labels. This abstraction for
WBSlow is shown in Fig. 3. civl veriﬁes that this automaton is simulated by the
yield suﬃciency automaton using an existing algorithm for computing simulation
relations [24].
    The use of commutativity reasoning is optional in civl, but beneﬁcial in
our experience. Commutativity reasoning may be avoided by annotating atomic
action speciﬁcations with the mover type atomic and inserting a yield statement
                                   before every invocation of an atomic action.
                                   In our experience with civl, using more yield
                                   statements, each with an accompanying loca-
  Fig. 3. Abstraction of WBSlow    tion invariant, can make proofs diﬃcult in two
                                   ways. First, the annotation burden goes up
because sophisticated ghost variables may need to be introduced in the program
semantics.2 Second, the computational cost of the pairwise mover reasoning is
replaced by the cost of pairwise non-interference checks between yield predicates
and concurrently executing atomic actions.
Linear Variables. In Fig. 1, thread identiﬁer (tid) variables are declared linear
to indicate that two threads cannot possess the same thread identiﬁer simultane-
ously. We now explain this feature of civl in more detail using the program in
Fig. 4. This example contains a shared global array a indexed by an uninterpreted
type Tid;                             type Tid representing the set of thread iden-
procedure Allocate()
  returns (linear tid:Tid);
                                      tiﬁers. A collection of threads are executing
                                      procedure P concurrently. The identiﬁer of the
var a:[Tid]int;
                                      thread executing P is passed in as the para-
procedure main()                      meter tid. A thread with identiﬁer tid owns
{
  while (true) {
                                      a[tid] and can increment it without dan-
    var linear tid:Tid := Allocate(); ger of interference. The yield predicate t ==
    async call P(tid);
    yield true;
                                      a[tid] in P indicates this expectation, yet it
  }                                   is not possible to prove it unless the reason-
}
procedure P(linear tid: Tid)
                                      ing engine knows that the value of tid in one
  ensures a[tid] == old(a)[tid] + 1;  thread is distinct from its value in a diﬀerent
{
  var t:int := a[tid];
                                      thread.
  yield t == a[tid];                      Instead of building a notion of thread iden-
  a[tid] := t + 1;
}
                                      tiﬁers into civl, we provide a more primitive
                                      and general notion of linear variables. The
Fig. 4. Encoding thread identiﬁers civl type system ensures that values con-
                                      tained in linear variables cannot be dupli-
cated [42]. Consequently, the parameter tid of distinct concurrent calls to P
are known to be distinct; the civl veriﬁer exploits this invariant while checking
2
    Location invariants that cannot refer to the state of other threads are known to be
    incomplete, both in theory and in practice.
    Automated and Modular Reﬁnement Reasoning for Concurrent Programs               455

for non-interference and commutativity. Linearity is general enough to support
much more than just ﬁxed thread identiﬁers: civl also uses it to express separa-
tion of memory (as is done commonly in separation logic proofs [39]; see [31]) and
to express permissions [7] that may be transferred but not duplicated between
threads. Our veriﬁed GC, for example, expresses mutual exclusion during initial-
ization and root scanning by temporarily transferring permissions from mutator
threads to the GC thread.
Variable Hiding. The atomic action speciﬁcation of WBSlow makes no reference
to the lock variable, although its implementation involves a lock. When verifying
reﬁnement for WBSlow, the lock variable has been hidden. civl allows the pro-
grammer to both introduce and hide variables in each reﬁnement step, thereby
providing the capability to perform data reﬁnement. The ability to introduce
and hide variables and write yield predicates speciﬁc to each reﬁnement step
facilitates proofs spanning a large range of abstraction.

3    Verification
In this section, we present our veriﬁcation method on a core concurrent program-
ming language called civl (Fig. 5). Due to lack of space, we can only provide
an overview of the design of the civl veriﬁer. The full formalization of the lan-
guage and detailed rules for all veriﬁcation judgments is available in a technical
report [23].
       s ∈ Stmt ::= skip | yield e | call A |     A civl program Prog contains proce-
                     call P | async P |       dures  ps, atomic actions as, global state
                     ablock {e} s | s; s |                    →
                                                              −                       →
                                                                                      −
                     if le then s else s |    G, and threads T . Each thread T in T
                     while {e} le do s
                                              contains thread-local state TL and stack
     F ∈ Frame ::= (P, L, s)
                           →−                         →
                                                      −                         −
                                                                                →
     T ∈ Thread ::= (TL, F )                  frames F . Each stack frame F in F con-
                                 →
                                 −
Prog ∈ Program ::= (ps, as, G, T )            tains a procedure name P , procedure-
                                              local state L, and a statement s repre-
             Fig. 5. Syntax                   senting the code in P that remains to be
                                              executed. Thus, Prog contains all infor-
mation to represent not only the static program written by the programmer
but also the entire state of the program as it executes. The statements in civl
contain the usual constructs such as sequencing, conditional control ﬂow, and
looping. In addition, it contains invocation of procedures (call P ), execution
of atomic actions (call A), and thread creation (async P ). Each atomic action
has a single-state gate predicate and a two-state transition relation. If a thread
executes an atomic action in a state (disjoint union of global, thread-local, and
procedure-local state) where its gate predicate does not hold, the program fails;
otherwise, the state is modiﬁed according to its transition relation. The execution
of Prog is modeled as the usual preemptive semantics in which a nondetermin-
istically chosen thread may execute any number of steps. Prog is unsafe if some
execution fails the gate of an atomic action; otherwise, Prog is safe.
    Suppose a program Prog hi has been proved to be safe. However, it is imple-
mented using atomic actions that are too coarse to be directly implementable.
To carry over the safety of Prog hi to a realizable implementation Prog lo , these
456    C. Hawblitzel et al.

coarse atomic actions must be reﬁned down to lower-level actions. During reﬁne-
ment, a high-level atomic action A is implemented by a procedure P , which is
itself implemented using lower-level atomic actions. In civl, the programmer can
simultaneously reﬁne many atomic actions by specifying a partial function RS
from procedures to atomic actions; Prog hi is obtained from Prog lo by replacing
each occurrence of call P for P ∈ dom(RS ) with call RS (P ). The main contri-
bution of this paper is a veriﬁcation method that allows us to validate such a
reﬁnement from Prog hi to Prog lo (or abstraction from Prog lo to Prog hi ) so that
safety of Prog hi implies the safety of Prog lo as well.
    While abstracting Prog lo to Prog hi , it is often inconvenient to reason about
Prog lo using its preemptive semantics, which allows potential interference at
every control location in a thread from concurrently-executing threads. To make
reasoning more convenient, civl provides the statement yield e, an annotation
used to specify a cooperative semantics for the program. In this semantics, a
thread executes continuously until it reaches a yield statement, at which point
a diﬀerent thread may be scheduled. To ensure that any reasoning performed
on cooperative semantics is also sound for preemptive semantics, civl exploits
commutativity reasoning. It allows the programmer to specify the commuta-
tivity type of atomic actions in the program—B for both mover, R for right
mover, L for left mover, and N for non mover [17]. The civl veriﬁer checks
the correctness of these commutativity types by verifying each atomic action
pairwise against every atomic action in the program. While it is sound to put
a yield statement before and after every atomic action, the programmer may
omit certain yield statements, e.g., a yield after a right mover or a yield before
a left mover. In general, the Yield Suﬃciency Automaton from Fig. 2 encodes
all sequences of atomic actions and yield statements for which reasoning about
cooperative semantics is sound. Given the commutativity types of atomic actions
and the program code annotated with yield statements, the civl veriﬁer checks
modularly for each procedure that its implementation is connected to the yield
suﬃciency automaton via a simulation relation [24].
    In addition to introducing a control location where interference is allowed
to occur, a yield statement yield e also provides an invariant e to constrain the
environment interference. The invariant e is similar to the location invariant
in the method of Owicki and Gries [38]. It is expected to hold when the exe-
cuting thread reaches the yield statement (sequential correctness) and also be
preserved by concurrently-executing threads (non-interference). Each procedure
is equipped with a precondition, a postcondition, and a set of (potentially) mod-
iﬁed thread-local variables. civl uses these procedure annotations to verify the
sequential correctness of location invariants for each procedure separately. To
verify non-interference, it would suﬃce to check that each location invariant is
preserved by each atomic action in the program. civl increases the precision of
this check by allowing each location invariant to be preserved across an atomic
block, introduced as the statement ablock {e} s. The invariant e annotating the
atomic block is expected to hold when this statement begins execution and is
veriﬁed as part of sequential correctness. The civl type checker checks that the
   Automated and Modular Reﬁnement Reasoning for Concurrent Programs             457

statement s inside this atomic block does not have any yield statement or other
atomic blocks inside it. Thus, non-interference of a location invariant e against
ablock {e} s is achieved by proving the Floyd-Hoare triple {e ∧ e }s{e }.
    Having veriﬁed sequential correctness and non-interference for location invari-
ants, it remains to verify reﬁnement, i.e., if RS (P ) = A, then the atomic action
A is correctly reﬁned by the procedure P . This requirement means that any path
from entry to exit of P must contain exactly one atomic block that implements
the action A; all other atomic blocks on the path must leave global and thread-
local variables unchanged. To perform this check, the civl veriﬁer introduces
the following fresh local variables in P : (1) a Boolean variable b initialized to
false to track whether an atomic block along the current execution has modiﬁed
a global or thread-local variable, (2) variables to capture snapshot of global and
thread-local variables at the beginning of each atomic block. By updating these
auxiliary variables appropriately, the reﬁnement check is reduced to a collection
of assertions introduced into the body of P at the end of atomic blocks and at
the exit of P .
    Often, commutativity and non-interference checks require knowledge about
distinctness of local program variables in diﬀerent threads. For example, in Fig. 1,
to prove that AcquireLock commutes to the right of ReleaseLock, the veriﬁer
must know that the input parameter tid to these atomic actions is diﬀerent if
they are being executed by diﬀerent threads. A similar situation arises in Fig. 4,
when attempting to prove that the location invariant t == a[tid] is preserved
by the atomic action a[tid] := t + 1. Information about distinctness of pro-
gram variables in diﬀerent threads is diﬃcult to provide as a location invariant
whose scope is local to the context of the unique executing thread. As an alter-
native, we exploit reasoning based on a linear type system [42]. The programmer
declares certain variables as linear at input and output interfaces of procedures
and actions. Using this interface information, the civl type system computes
a set of available linear variables at each control location in a procedure. The
availability of a variable may change at an assignment or a procedure call, e.g.,
if y is available just before x := y, then y is not available and x is available
just afterwards. The civl type checker guarantees that the values contained in
available linear variables, across all threads at their respective control locations,
are distinct from each other. This fact is introduced as a logical assumption by
the veriﬁer when performing commutativity and non-interference checks.
    The interaction between the linear type system and logical reasoning in civl
is more general than the description above. In civl, the programmer may specify
an arbitrary function Perm from a value to a set of values; the set Perm(v) is
the set of permissions associated with v. The example described in the previous
paragraph corresponds to the special case when Perm(v) = {v}. The civl type
checker enforces a generalization of the distinctness invariant that the permission
sets corresponding to the values in available variables across all threads are
mutually disjoint.
458     C. Hawblitzel et al.

3.1   Safety Guarantee
We can combine the veriﬁcation techniques described above to verify the safety
of a program Prog lo . Speciﬁcally, we can guarantee that Prog lo is safe (i.e., all
atomic actions will satisfy their gates when run) if the following conditions hold:

1. Prog hi is safe when executed with preemptive semantics.
2. Prog lo is a valid reﬁnement of Prog hi , according to the rules for reﬁnement
   in civl. Speciﬁcally, for any atomic action A in Prog hi implemented by a
   procedure P in Prog lo , any path from entry to exit of P must contain exactly
   one atomic block that implements the action A; all other atomic blocks on the
   path must leave the global and thread-local state unchanged. Furthermore,
   all calls to A in Prog hi are replaced by calls to P in Prog lo .
3. The invariants of Prog lo satisfy sequential correctness and non-interference
   with respect to cooperative semantics.
4. Prog lo is well-typed with respect to linearity. Speciﬁcally, Prog lo does not try
   to duplicate any linear variables, and linear variables passed to procedures
   calls and atomic actions are available as expected by the type checker.
5. The atomic actions in Prog lo satisfy the pairwise commutativity checks.
6. The yield statements in Prog lo are suﬃcient, according to the yield suﬃciency
   automaton in Fig. 2.
7. Any inﬁnite execution of Prog lo must visit a yield statement inﬁnitely often.

    By themselves, conditions 1-4 guarantee that Prog lo will be safe when exe-
cuted with cooperative semantics. Conditions 5-7 then additionally ensure that
Prog lo will be safe when executed with preemptive semantics. The technical
report [23], which includes formal deﬁnitions of all the conditions for an exten-
sion of the language in Fig. 5, formalizes this safety guarantee into a sound-
ness theorem by establishing a simulation relation between Prog lo and Prog hi .
Since the theorem connects the safety of one program’s preemptive semantics to
another program’s preemptive semantics, multiple applications of the theorem
can be chained together to establish the safety of a low-level program: the low-
est level Prog 0 is safe because Prog 1 is safe, Prog 1 is safe because Prog 2 is safe,
and so on.


4     Modules
The technical report [23] describes a simple module system built on civl that
allows separate veriﬁcation of modules, allowing programmers to check a large
program by breaking it into smaller pieces and checking the pieces indepen-
dently. A key challenge for modular veriﬁcation in civl is the checking of non-
interference and commutativity. Naively, these are whole-program judgments,
quadratically checking all pairs of actions or all pairs of yields and atomic blocks
from an entire program. To check these judgments on a per-module basis rather
for a whole program, we observe that commutativity and non-interference are
trivially satisﬁed for operations that act on disjoint sets of global variables.
    Automated and Modular Reﬁnement Reasoning for Concurrent Programs           459

If an atomic block modiﬁes only variables g1 and g2 , it will not interfere with
a location invariant that refers only to variables g3 and g4 . More generally, let
each module M own a set of global variables, such that each global variable is
owned by exactly one module, and decree that only M ’s procedures and actions
can access M ’s global variables. Statements in M ’s procedures can only read
and write M ’s own global variables, and M ’s actions and location invariants can
only refer to M ’s own global variables. (On the other hand, procedure assertions
that are not checked for non-interference, such as the e in ablock {e} s, may
mention global variables from other modules, since these assertions can neither
interfere with other modules’ location invariants nor be interfered with by other
modules’ statements.)
    Note that ownership can change across reﬁnement layers. For example, a
library module implementing locks may deﬁne a variable to represent the abstract
state of a lock; after the lock module is veriﬁed at a low layer, another module can
take ownership of the lock variable in a higher layer (see [23] for a detailed exam-
ple of ownership transfer across three layers, from a lock module to a datatype
module to a client module).


5    Implementation

We have implemented the method described in this section as a conservative
extension of the Boogie [4] language and veriﬁer. Our implementation pro-
vides new language primitives for linear variables, asynchronous and parallel
procedure calls, yields, atomic actions as procedure speciﬁcations, expressing
reﬁnement layers, and hiding of global variables and procedures. At its core,
Boogie is an unstructured language comprising code blocks and goto statements.
Our implementation handles the complexity of unstructured control ﬂow. To
simplify the exposition, our formalization uses Floyd-Hoare triples to present
sequential correctness and annotated atomic code blocks to present reﬁnement
and non-interference checks. However, our implementation is considerably more
automated. All the annotations, except those at yields, loops, and procedure
boundaries, are automatically generated using the technique of veriﬁcation con-
ditions [5]. Annotated atomic code blocks are also inferred automatically. Non-
interference checks are collected as inlined procedures invoked at appropriate
places within the code of a procedure for increased precision.
    We automated the simulation relation check used for yield suﬃciency in
Sect. 3 by adapting an algorithm by Henzinger et al. [24] for computing the
similarity relation of labeled graphs. The complexity of the algorithm is O(n∗m),
where n and m are the number of control-ﬂow graph nodes and edges. In practice,
this part of the veriﬁcation is fast.
    A large proof usually comprises multiple layers of reﬁnement chained together.
Our implementation allows the speciﬁcation of multiple views of a program in
a single ﬁle by using the mechanism of layers. The programmer may attach a
positive layer number to each annotation and procedure; version i of the program
is constructed from annotations labeled i and procedures labeled at least i.
460     C. Hawblitzel et al.

We have implemented a type checker to make sure that layer numbers are used
appropriately, e.g., it is illegal for a procedure with layer i to call a procedure
with layer j greater than i.


6     Experience
The civl veriﬁer has been under development for around two years. Over that
period, we have developed a collection of 32 benchmarks, ranging in size from
17 to 539 LOC, to illustrate various features of civl and for regression testing
as we evolved the veriﬁer. In addition to microbenchmarks, this collection also
includes standard benchmarks from the literature such as a multiset implemen-
tation [14], the ticket algorithm [15], Treiber stack [27], work-stealing queue [6],
device cache [13], and lock-protected increment [19]. The civl veriﬁer is fast; the
entire benchmark set veriﬁes in 20 s on a standard 4-core Windows PC (2.8GHz,
8GB) with no benchmark requiring more than a few seconds.


6.1   Garbage Collector

We have used civl to design and verify a realistic concurrent mark-sweep garbage
collection (GC) algorithm (available at [22]). In particular, although our algo-
rithm is based on an earlier algorithm by Dijkstra et al. [10], it extends the ear-
lier algorithm with various modern optimizations and embellishments to improve
generality and performance. These extensions include lower write barrier over-
head, phase-based synchronization and handshaking, and coordination between
the GC and mutator threads during root scanning; our use of linearity aids the
proof of root scanning, while our rely-guarantee encoding aids management of
colors inside the write barrier (which is similar to the barrier in Sect. 2). Further-
more, our encoding of the algorithm in civl spans a wide range of abstraction,
from low-level memory operations all the way up to high-level speciﬁcations; we
used six layers of reﬁnement to help hide low-level details from the high-level
portions of the veriﬁcation.
    We believe that civl’s combination of features makes practical, for the ﬁrst
time, veriﬁcation across such a wide range of abstraction:

– The GC’s lowest layers relied primarily on reduction to prove that operations
  on concurrent data structures and synchronization operations appear atomic
  to higher layers.
– The GC’s higher layers relied primarily on invariant-based non-interference
  reasoning. This reasoning was simpliﬁed because reduction already made
  lower-layer operations atomic, reducing the amount of interference between
  higher-layer operations. In addition, the use of location invariants made cer-
  tain layers of the proof more manageable compared to an earlier eﬀort verifying
  the same GC where we used rely-guarantee reasoning and auxiliary variables
  to reason about non-interference.
      Automated and Modular Reﬁnement Reasoning for Concurrent Programs       461

– Linear variables were used throughout the proof to model the distinct thread
  identiﬁers for the garbage collector thread and mutator threads, but were
  most instrumental in expressing mutual exclusion during initialization and
  during root scanning. In initialization and root scanning, the mutator threads
  temporarily donate a fraction of their linear permissions to the GC thread.
  The distinctness invariant from Sect. 3 guarantees that the mutator threads
  and GC threads cannot simultaneously possess the same linear permissions; we
  leverage this guarantee to prove non-interference of mutator and GC actions
  during initialization and root scanning.

    civl’s support for reﬁnement also enabled concise speciﬁcations of the GC’s
correctness: a correct GC must implement Allocate, ReadField, and WriteField
actions that appear to act atomically, even though the implementations of these
operations actually execute concurrently with the GC thread and with other
program threads. The speciﬁcation states that Allocate atomically adds new
objects to the heap, while ReadField and WriteField read and write heap object
ﬁelds. Although the GC’s Mark and Sweep code constitutes most of the GC code,
they are hidden in the high-level speciﬁcation; they have detailed correctness
speciﬁcations in the middle layers of the proof, but the most important point
at the high level is that their work not interfere with Allocate, ReadField, and
WriteField. In particular, Mark must coordinate with WriteField’s write barrier,
and Sweep must not remove objects reachable by ReadField and WriteField.
    Overall, our GC implementation consists of about 2100 lines of Boogie code.
The veriﬁcation takes 60 s on the same PC used for microbenchmarks. The bulk
of this time, 54 s, is taken by the veriﬁcation of sequential correctness and non-
interference. The checks for linear variables, yield suﬃciency, and commutativity
take the rest of the time and are insigniﬁcant in comparison.

7      Related Work
Our work is the ﬁrst to provide a tool and theory to support automated, modu-
lar whole-program reﬁnement through multiple layers, as distinct from existing
work on single-layer atomicity reﬁnement between procedure implementations
and speciﬁcations. civl combines a number of techniques in a novel manner to
decompose the reﬁnement task following the syntactic structure of a program.
Below, we ﬁrst contrast civl with reﬁnement veriﬁcation techniques, and then
with tools and techniques for reasoning about concurrent programs in general.

7.1     Refinement-Oriented Verification
Atomic action speciﬁcations have been explored by the calvin [18,21] veriﬁer.
civl carries out reﬁnement veriﬁcation on a procedure body with cooperative
semantics as enabled by movers types and reduction. calvin attempts to ver-
ify reﬁnement directly on the preemptive semantics, making only limited use
of movers at the lowest-level representation. calvin, unlike civl, does not sup-
port location invariants and linear variables but incorporates rely-guarantee rea-
soning. civl supports both location invariants or rely-guarantee reasoning, and
462     C. Hawblitzel et al.

either technique can be used to prove non-interference. However, in certain cases,
rely-guarantee reasoning requires use of auxiliary (shared) variables and makes
interactive proofs diﬃcult as was the case in our GC proof.
    qed [13] is a simpliﬁer for concurrent programs and is close in spirit to the
reﬁnement-oriented approach of civl. A key distinction between civl and qed
is the fact that a proof step in qed is a small rewrite in the concurrent program
that must be justiﬁed by potentially expensive reduction and invariant reasoning.
In qed, procedures can be proven atomic only one procedure at a time, and only
by transforming their bodies by reduction to be yield free. The number of small
proof steps directly aﬀect both programmer and computer eﬀort. By contrast,
civl supports large proof steps, in each of which the bodies of several procedures
are automatically replaced by atomic actions, thereby lowering the cost of both
interaction and automation. The non-interference reasoning in qed is even more
limited than calvin. qed supports only global invariants and does not support
rely-guarantee reasoning or linear variables.
    Liang et al. [34] present a method for verifying that procedure bodies reﬁne
atomic speciﬁcations The key veriﬁcation approach is rely-guarantee reasoning
and the reﬁnement (simulation) relation between a procedure and its speciﬁca-
tion is constrained so it is preserved under parallel composition. No tool support
is provided. Authors present a (paper) GC proof, which is limited in scope com-
pared to ours, as their proof corresponds to a few layers of our proof. In particu-
lar, the GC is not reﬁned down to individual atomic memory accesses. Since this
work uses diﬀerent languages to describe the high-level and low-level programs, it
is not immediately possible to carry out a multi-level stepwise reﬁnement proof.
    Turon and Wand [40] use ownership disciplines and separation logic to verify
reﬁnement of atomic speciﬁcations by concurrent data structure implementa-
tions. Rely-guarantee reasoning is supported to provide compositionality and
non-interference arguments. This work targets a single reﬁnement step between
atomic speciﬁcations for methods and their implementations. No tool support
for this veriﬁcation method is provided.
    Verifying linearizability of concurrent data structures (see, e.g., [12,25]) can
be viewed as an instance of one-level of reﬁnement in our setting. civl can
be used for mechanical veriﬁcation of linearizability, as we did for the Treiber
stack. Tools and techniques speciﬁc to verifying linearizability cannot be easily
generalized for stepwise reﬁnement proofs through multiple levels.
    Reﬁnement proofs between implementations and speciﬁcations of protocols
have been investigated using the TLA+ [32] speciﬁcation language. Composi-
tional reﬁnement proofs [1] have also been investigated in this context. Modu-
lar reﬁnement proofs for hardware systems have been investigated extensively
(e.g., [11,26]) using the SMV [36] and Mocha [3] model checking tools. To verify
a concurrent, shared-memory program using such tools, one must encode the
program semantics as a state-transition system and express veriﬁcation goals
in terms of this system. For concurrent, shared-memory software, civl enables
reasoning on the structured, imperative multithreaded program text rather than
a logic description of the program’s state-transition relation.
      Automated and Modular Reﬁnement Reasoning for Concurrent Programs               463

7.2     Reasoning About Concurrency

In this section, we discuss foundational techniques for combating the complexity
of concurrent program veriﬁcation. civl and reﬁnement techniques discussed in
the previous section have common ideas with tools and formalisms discussed in
this section, however, the latter primarily target veriﬁcation of a single program
rather than reﬁnement. Reﬁnement in civl is orthogonal to these techniques,
which can be aided by civl’s ability to connect a complex concurrent program
to a simpler abstraction.
    VCC [8] is a tool for verifying concurrent C programs. Chalice [33] is a lan-
guage and modular veriﬁcation tool for concurrent programs. VCC does not
support reﬁnement and Chalice does so only for sequential programs. VCC and
Chalice base their invariant reasoning on objects, object ownership, and type
invariants. Invariant reasoning in civl is more primitive and based on predi-
cates in yield statements. Although the approach in VCC and Chalice is more
convenient when applicable, civl’s approach is more ﬂexible. VCC and Chal-
ice can reason sequentially about objects exclusively owned by a thread; civl
accomplishes the same using linear variables. Neither VCC nor Chalice support
movers and reduction reasoning.
    Concurrent separation logic [37] reasons about concurrency without explic-
itly checking for non-interference between threads. Recently, tools based on this
logic that blend in explicit non-interference reasoning (but without support for
reduction and mover reasoning) have been developed [16,41]. civl’s combination
of interference checking and linear variables is an extreme example of this trend,
is very general and technique-agnostic. We supply very primitive abstractions
and let programmers mix and match these abstractions freely to encode the
non-interference reasoning style of their choice.


References
 1. Abadi, M., Lamport, L.: Composing speciﬁcations. ACM Trans. Program. Lang.
    Syst. 15(1), 73–132 (1993)
 2. Abrial, J.-R., Butler, M., Hallerstede, S., Hoang, T.S., Mehta, F., Voisin, L.: Rodin:
    an open toolset for modelling and reasoning in Event-B. STTT 12(6), 447–466
    (2010)
 3. Alur, R., Henzinger, T.A., Mang, F.Y.C., Qadeer, S., Rajamani, S.K., Tasiran, S.:
    MOCHA: modularity in model checking. In: Computer Aided Veriﬁcation, 10th
    International Conference Proceedings, CAV 1998, pp. 521–525, Vancouver, June
    28 - July 2 (1998)
 4. Barnett, M., Chang, B.-Y.E., DeLine, R., Jacobs, B., Leino, K.R.M.: Boogie:
    a modular reusable veriﬁer for object-oriented programs. In: de Boer, F.S.,
    Bonsangue, M.M., Graf, S., de Roever, W.-P. (eds.) FMCO 2005. LNCS, vol. 4111,
    pp. 364–387. Springer, Heidelberg (2006)
 5. Barnett, M., Leino, K.R.M.: Weakest-precondition of unstructured programs. In:
    PASTE (2005)
 6. Blumofe, R.D., Leiserson, C.E.: Scheduling multithreaded computations by work
    stealing. J. ACM 46(5), 720–748 (1999)
464     C. Hawblitzel et al.

 7. Boyland, J.: Checking interference with fractional permissions. In: Static Analysis:
    10th International Symposium (2003)
 8. Cohen, E., Dahlweid, M., Hillebrand, M., Leinenbach, D., Moskal, M., Santen, T.,
    Schulte, W., Tobies, S.: VCC: a practical system for verifying concurrent C. In:
    Berghofer, S., Nipkow, T., Urban, C., Wenzel, M. (eds.) TPHOLs 2009. LNCS,
    vol. 5674, pp. 23–42. Springer, Heidelberg (2009)
 9. de Moura, L., Bjørner, N.S.: Z3: an eﬃcient SMT solver. In: Ramakrishnan, C.R.,
    Rehof, J. (eds.) TACAS 2008. LNCS, vol. 4963, pp. 337–340. Springer, Heidelberg
    (2008)
10. Dijkstra, E.W., Lamport, L., Martin, A.J., Scholten, C.S., Steﬀens, E.F.M.: On-
    the-ﬂy garbage collection An exercise in cooperation. Commun. ACM 21(11), 280–
    294 (1978)
11. Eirı́ksson, A.T.: The formal design of 1M-gate ASICs. Form. Methods Syst. Des.
    16(1), 7–22 (2000)
12. Elmas, T., Qadeer, S., Sezgin, A., Subasi, O., Tasiran, S.: Simplifying linearizabil-
    ity proofs with reduction and abstraction. In: Esparza, J., Majumdar, R. (eds.)
    TACAS 2010. LNCS, vol. 6015, pp. 296–311. Springer, Heidelberg (2010)
13. Elmas, T., Qadeer, S., Tasiran, S.: A calculus of atomic actions. In: POPL, pp.
    2–15 (2009)
14. Elmas, T., Tasiran, S., Qadeer, S..: VYRD: verifying concurrent programs by run-
    time reﬁnement-violation detection. In: Proceedings of the ACM SIGPLAN 2005
    Conference on Programming Language Design and Implementation, pp. 27–37,
    Chicago, 12–15 June 2005
15. Farzan, A., Kincaid, Z., Podelski, A.: Proofs that count. In: The 41st Annual ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL
    2014), San Diego, pp. 151–164, 20–21, January 2014
16. Feng, X., Ferreira, R., Shao, Z.: On the relationship between concurrent separation
    logic and assume-guarantee reasoning. In: De Nicola, R. (ed.) ESOP 2007. LNCS,
    vol. 4421, pp. 173–188. Springer, Heidelberg (2007)
17. Flanagan, C., Freund, S.N., Lifshin, M., Qadeer, S.: Types for atomicity: Static
    checking and inference for java. ACM Trans. Program. Lang. Syst. 30(4), 1–53
    (2008)
18. Flanagan, C., Freund, S.N., Qadeer, S., Seshia, S.A.: Modular veriﬁcation of mul-
    tithreaded programs. Theor. Comput. Sci. 338(1–3), 153–183 (2005)
19. Flanagan, C., Qadeer, S.: Thread-modular model checking. In: Ball, T., Rajamani,
    S.K. (eds.) SPIN 2003. LNCS, vol. 2648, pp. 213–224. Springer, Heidelberg (2003)
20. Floyd, R.: Assigning meaning to programs. In: Symposia in Applied Mathematics,
    vol. 19, pp. 19–32. American Mathematical Society (1967)
21. Freund, S.N., Qadeer, S.: Checking concise speciﬁcations for multithreaded soft-
    ware. J. Object Technol. 3(6), 81–101 (2004)
22. Hawblitzel, C., Petrank, E., Qadeer, S., Tasiran, S.: Veriﬁed concurrent garbage
    collector. http://singularity.codeplex.com/SourceControl/latest#base/Imported/
    Bartok/runtime/veriﬁed/GCs/concur/GC.bpl
23. Hawblitzel, C., Petrank, E., Qadeer, S., Tasiran, S.: Automated and modular
    reﬁnement reasoning for concurrent programs. Technical report MSR-TR-2015-8,
    Microsoft Research (2015). http://research.microsoft.com/apps/pubs/?id=238907
24. Henzinger, M.R., Henzinger, T.A., Kopke, P.W.: Computing simulations on ﬁnite
    and inﬁnite graphs. In: FOCS (1995)
25. Henzinger, T.A., Sezgin, A., Vafeiadis, V.: Aspect-oriented linearizability proofs.
    In: D’Argenio, P.R., Melgratti, H. (eds.) CONCUR 2013 – Concurrency Theory.
    LNCS, vol. 8052, pp. 242–256. Springer, Heidelberg (2013)
   Automated and Modular Reﬁnement Reasoning for Concurrent Programs                465

26. Henzinger, T.A., Liu, X., Qadeer, S., Rajamani, S.K.: Formal speciﬁcation and
    veriﬁcation of a dataﬂow processor array. In: Proceedings 1999 IEEE/ACM Inter-
    national Conference on Computer-aided Design, (ICCAD 1999), pp. 494–499. IEEE
    Press (1999)
27. Herlihy, M., Shavit, N.: The Art of Multiprocessor Programming. Morgan
    Kaufmann Publishers Inc., San Francisco (2008)
28. Hoare, C.A.R.: An axiomatic basis for computer programming. Commun. ACM
    12(10), 576–580 (1969)
29. Jones, C.B.: Tentative steps toward a development method for interfering pro-
    grams. ACM TOPLAS 5(4), 596–619 (1983)
30. Klein, G., Andronick, J., Elphinstone, K., Murray, T., Sewell, T., Kolanski, R.,
    Heiser, G.: Comprehensive formal veriﬁcation of an OS microkernel. ACM Trans.
    Comput. Sys. 32(1), 2:1–2:70 (2014)
31. Lahiri, S.K., Qadeer, S., Walker, D.: Linear maps. In: PLPV, pp. 3–14 (2011)
32. Lamport, L.: Specifying Systems: The TLA+ Language and Tools for Hardware
    and Software Engineers. Addison-Wesley, Boston (2004)
33. Leino, K.R.M., Müller, P.: A basis for verifying multi-threaded programs. In:
    Castagna, G. (ed.) ESOP 2009. LNCS, vol. 5502, pp. 378–393. Springer, Heidelberg
    (2009)
34. Liang, H., Feng, X., Fu, M.: Rely-guarantee-based simulation for compositional
    veriﬁcation of concurrent program transformations. ACM Trans. Program. Lang.
    Syst. 36(1), 3:1–3:55 (2014)
35. Lipton, R.J.: Reduction: A method of proving properties of parallel programs.
    Commun. ACM 18(12), 717–721 (1975)
36. McMillan, K.L.: A methodology for hardware veriﬁcation using compositional
    model checking. Sci. Comput. Program. 37(1–3), 279–309 (2000)
37. O’Hearn, P.W.: Resources, concurrency, and local reasoning. Theor. Comput. Sci.
    375(1–3), 271–307 (2007)
38. Owicki, S.S., Gries, D.: An axiomatic proof technique for parallel programs i. Acta
    Inf. 6, 319–340 (1976)
39. Reynolds, J.C.: Separation logic: a logic for shared mutable data structures. In:
    LICS, pp. 55–74 (2002)
40. Turon, A.J., Wand, M.: A separation logic for reﬁning concurrent objects. In: Pro-
    ceedings 38th ACM SIGPLAN-SIGACT Symposium on Principles of Programming
    Languages (POPL 2011), pp. 247–258. ACM, New York (2011)
41. Vafeiadis, V., Parkinson, M.: A marriage of rely/guarantee and separation logic. In:
    Caires, L., Vasconcelos, V.T. (eds.) CONCUR 2007. LNCS, vol. 4703, pp. 256–271.
    Springer, Heidelberg (2007)
42. Wadler, P.: Linear types can change the world!. In: Programming Concepts and
    Methods, North (1990)
43. Wirth, N.: Program development by stepwise reﬁnement. Commun. ACM 14(4),
    221–227 (1971)
