                                            Practical Rely/Guarantee Verification of an
                                         Efficient Lock for seL4 on Multicore Architectures

                                                        Robert J. Colvin1,2 , Ian J. Hayes2, Scott Heiner2 ,
                                                       Peter Höfner3 , Larissa Meinicke2 , and Roger C. Su3
arXiv:2407.20559v1 [cs.LO] 30 Jul 2024




                                                         1
                                                          Defence Science and Technology Group, Australia
                                                             2
                                                            University of Queensland, Brisbane, Australia
                                                    {r.colvin, ian.hayes, s.heiner, l.meinicke}@uq.edu.au
                                                       3
                                                         Australian National University, Canberra, Australia
                                                             {peter.hoefner, roger.su}@anu.edu.au



                                               Abstract. Developers of low-level systems code providing core function-
                                               ality for operating systems and kernels must address hardware-level fea-
                                               tures of modern multicore architectures. A particular feature is pipelined
                                               “out-of-order execution” of the code as written, the effects of which are
                                               typically summarised as a “weak memory model” – a term which includes
                                               further complicating factors that may be introduced by compiler opti-
                                               misations. In many cases, the nondeterminism inherent in weak memory
                                               models can be expressed as micro-parallelism, i.e., parallelism within
                                               threads and not just between them. Fortunately Jones’ rely/guarantee
                                               reasoning provides a compositional method for shared-variable concur-
                                               rency, whether that be in terms of communication between top-level
                                               threads or micro-parallelism within threads. In this paper we provide an
                                               in-depth verification of the lock algorithm used in the seL4 microkernel,
                                               using rely/guarantee to handle both interthread communication as well
                                               as micro-parallelism introduced by weak memory models.

                                               Keywords: Rely/Guarantee · Lock algorithms · Weak memory models


                                         1   Introduction

                                         The CLH lock [8,26,27] provides a space- and time-efficient method for ensuring
                                         mutual exclusion, and furthermore ensures that any thread attempting to acquire
                                         the lock will eventually succeed under reasonable fairness assumptions. CLH’s
                                         efficiency arises partly from its utilisation of the hardware-level cache system to
                                         minimise contention in main memory. It is used in the seL4 microkernel [16,40]
                                         to handle interrupts.
                                              In this paper, we formally verify the functional correctness of the CLH lock,
                                         and lay the foundation for proving progress properties. Additionally, we take into
                                         account the effects of weak memory models of possible target architectures for
                                         the deployment of seL4. We use rely/guarantee reasoning for this task, and find
                                         it especially suited for hardware-level algorithms which involve weak memory
                                         effects. We use the proof assistant Isabelle/HOL [31,34], and build on existing
2       R. Colvin et al.

library features (including a rely/guarantee encoding by Prensa Nieto [35]) to
automate some parts of the proof.
    The paper is structured as follows: Sect. 2 summarises Jones’ rely/guarantee
reasoning, with some specialisations for our context. Sect. 3 introduces the spec-
ification of a generic lock, and its specialisation to a queued lock. Sect. 4 proves
functional correctness of the CLH lock currently used in the seL4 microker-
nel. with respect to the specification of a queued lock. Sect. 5 analyses weak
memory effects on the CLH code, identifying the micro-parallelism that may be
introduced during execution on multicore architectures, and whether or not that
micro-parallelism may be retained or must be eliminated. Sect. 6 summarises
related work.


2     Rely/Guarantee Reasoning

Developed by Jones in the 1980s [19,20,21], rely/guarantee reasoning provides
a compositional framework for the verification of programs with shared-variable
concurrency. The key idea is to extend pre/postcondition reasoning of classic
Floyd-Hoare logic [12,18] by capturing the effect of the environment of a thread
in a rely relation on states; additionally, a thread summarises its own effects on
its environment via a guarantee relation on states.
    In the context of a lock, a thread i relies on the fact that if i currently holds
the lock then some resource x cannot be modified by the environment. This
is written as lock = held(i) ⇒ x ′ = x , a rely relation where lock and x are
shared variables, with primed instances (x ′ ) referring to their values in the post-
state (as opposed unprimed instances (x ) in the pre-state). The corresponding
guarantee relation is lock 6= held(i) ⇒ x ′ = x ; that is, thread i guarantees not
to change x if it does not hold the lock. In this work, pre/postconditions are
single-state predicates (where a state is a mapping from variables to values),
and relies and guarantees are binary relations on states (with primed as well
as unprimed variables). We allow the standard logical connectives to apply to
either predicates or relations under their usual interpretations.
    A rely/guarantee quintuple {p, r } c {g, q} states that the program c achieves
the postcondition q and guarantees each step satisfies g, provided that it starts
in a state satisfying p and each step of the environment satisfies the rely r . Infer-
ence using rely/guarantee takes place via the application of specialised syntax-
driven rules. The rules we apply are adaptations of some of the rules provided
by Coleman and Jones [1] and those encoded in Isabelle by Prensa Nieto [35].


2.1   Inference rules

The inference rules we apply in this paper are given in Fig. 1. Rule (1) states
that an atomic assignment x := e establishes q and guarantees g ∨ id under
precondition p and rely r , provided that neither p nor q is affected by the
environment, and executing x := e from a state satisfying p both establishes q in
the post state and implies the guarantee g. As an example, we may immediately
                Rely-guarantee verification of locks for multicore architectures                    3


  p, q stable under r                                                   {p0 , r0 } c {g0 , q0 }
                                     {p, r } c1 {g, pmid }
       phx ←ei ⇒ q                                                      p ⇒ p0 r ⇒ r0
                           (1)       {pmid , r } c2 {g, q} (2)                                    (3)
   p ⊳ (x ′ = e) ⇒ g                                                    g0 ⇒ g q0 ⇒ q
                                     {p, r } c1 ; c2 {g, q}
{p, r } x := e {g ∨ id, q}                                               {p, r } c {g, q}

                                                          {p1 , r1 } c1 {g1 , q1 }
       {p, r ∨ g2 } c1 {g1 , q1 }
                                                          {p2 , r2 } c2 {g2 , q2 }
       {p, r ∨ g1 } c2 {g2 , q2 }     (4)                                                     (5)
                                                          g1 ⇒ r2 ∧ g2 ⇒ r1
 {p, r } c1 k c2 {g1 ∨ g2 , q1 ∧ q2 }
                                            {p1 ∧ p2 , r1 ∧ r2 } c1 k c2 {g1 ∨ g2 , q1 ∧ q2 }

        ∀ i . {pi , ri } ci {gi , qi }                           p, q stable under r
  V      ∀Vi . ∀ j 6= i . gi W⇒ rj V     (6)                  id ⇒ g        p ∧ ¬b ⇒ q            (7)
 { i pi , i ri } ki . ci { i gi , i qi }                    {p, r } while b do skip {g, q}

              Fig. 1. Rely/guarantee inference rules adapted from [1,35].



derive {true, x ′ = x } x := 5 {x ← 5 ∨ id, x = 5}. The inclusion of the identity
relation id to the guarantee is a technical requirement that accounts for the fact
that the assignment statement inflicts no interference on the rest of the system
prior to executing – between steps of c in ‘c k x := 1’ either the assignment occurs
or nothing (id) occurs. We let phx ←ei be the predicate obtained by updating each
state in p so that x takes the value of e in the pre-state; p ⊳ r be the restriction
of the relation r to just the pre-states satisfying predicate p; and p stable under r
states that p is maintained by r .
    Rule (2) composes the properties of two commands in sequential composition
provided they agree on a mid-state, written pmid in the rule. The relies and
guarantees are identical across both components.
    Rule (3) is a general rule allowing the weakening of preconditions and re-
lies, and strengthening of postconditions and guarantees. We tend to leave the
application of this rule implicit where the implications are clear from the context.
    The significance of rely/guarantee lies in its handling of parallel composition.
There are two compositional rules typically found in the literature that apply
to two parallel processes, c1 k c2 . Rule (4) assumes some external environment
“inflicting” r on the local system (in this case, the local system is c1 k c2 ). The
compositionality of the rule requires that the additional interference g2 inflicted
on c1 by c2 must be handled (by c1 ), and vice-versa. Rule (5) instead insists
that the environment must already respect the relies of both threads c1 and c2 ,
and each thread must also respect each other’s relies. We found that each has its
application; in our case, micro-parallelism within a single thread (as addressed
in Sect. 5) is best handled by Rule (4), while at the system level, where a set of
threads interact via a shared contract, Rule (5) is more suitable. This is given by
the generalisation of Rule (5) to an arbitrary number of threads, written ki . ci ,
as shown in Rule (6).
    A common structure in lock implementations are spin loops, i.e., loops with an
empty body, while b do skip. We often abbreviate spin loops to await ¬b. Rule (7)
4        R. Colvin et al.

states that provided the precondition p and postcondition q are stable under r ,
and that p and the negation of the guard imply q, one can assume that q holds
if the loop terminates. A spin loop changes nothing, and hence guarantees the
identity relation, id.

2.2    Invariants
We define the following shorthand for a (single-state) data-type invariant I (or
any invariant), in the spirit of Morgan’s refinement calculus [29].

                             b {p ∧ I , r ∧ (I ⇒ I ′ )} c {g ∧ (I ⇒ I ′ ), q ∧ I }
         {p, r } c//I {g, q} =                                                       (8)

Definition (8) factors out the invariant, making specification more concise. It
states that if I holds in the pre-state, and the environment can be relied upon to
maintain the invariant, then c guarantees to maintain the invariant and establish
it in the post-state (the relation I ⇒ I ′ requires that I holds in the post-state
provided it holds in the pre-state).
    The use of an invariant helps to avoid the use of code-specific program-
counter-style variables, particularly when used on auxiliary concepts (essentially
forming the “specification” of a data type). Program-counters are preferably
avoided, as they are brittle with respect to the structure of the code, and become
cumbersome with complex programs, such as those with nested parallelisms.


3     Specification of Locks in Rely/Guarantee
In this section we discuss specifying locks in a rely/guarantee setting. The auxil-
iary variable lock ∈ LockStatus represents the status of the lock, which is either
free if no thread holds the lock, or held(i) if thread i holds the lock.

3.1    Properties of a generic lock
A lock is used by multiple threads (type T ) to ensure exclusive access to some
critical section of code, typically where some shared resource is accessed. That
is, from the viewpoint of each thread i ∈ T , the lock is used in the pattern1

                        acquirei () ; critical section ; releasei ().

The intention is that if modifying x in the critical section, a thread may rely
on the fact that no other thread concurrently modifies x , that is, in the calling
code, lock = held(i) ⇒ x ′ = x .
    The operation acquirei () is called to attempt to hold the lock, and releasei ()
to release the lock after the thread has finished accessing the shared resource.
The key properties required are the following.
1
    Note that acquire and release have no explicit parameters, but in some implementa-
    tions they may (usually some component of the lock data structure). They do have
    the thread identifier (i) as an implicit parameter.
               Rely-guarantee verification of locks for multicore architectures     5


                   {i 6∈ q} acquirei (); {i = hd(q)} releasei () {i 6∈ q}          (9)

                invariant =
                          b distinct(q)                                           (10)
                                             ′                ′
                          b (i ∈ q ⇔ i ∈ q ) ∧ (i ∈ q ⇒ q !i ≤ q!i)
                contracti =                                                       (11)
                     relyi =
                           b invariant ∧ contracti                                (12)
                          b invariant ∧ (∀ j 6= i . contractj )
                    guari =                                                       (13)
                          b lock = (if q = [ ] then free else held(hd(q)))
                     cinv =                                                       (14)


               Fig. 2. Rely/guarantee specification of the queued lock


 1. A call to acquirei () establishes the postcondition lock = held(i); and
 2. Thread i may rely on lock = held(i) ⇒ lock ′ = held(i).
The postcondition lock = held(i) is stable – maintained by the environment – if
the environment satisfies the rely, that is, if i holds the lock then it will never be
taken away. These conditions necessitate the converse guarantee, that thread i
will respect the lock if some other thread j holds it.

3.2   Queued lock

When multiple threads call acquirei () concurrently, a potentially desirable prop-
erty is that the lock is next obtained by the thread that has been waiting the
longest. To capture this refinement of the lock concept a generic lock can be
modelled via an abstract queue of waiting threads, q, as given in Fig. 2. We let
i ∈ q mean that i is an element of list q, and let hd(q) return q’s first element.
    To emphasise the different parts of a specification, we separate out the guar-
antees in guar and the relies in rely, and the pre- and postconditions are written
in green braces. Hence, Fig. 2 implies a quintuple of the form in (8),
             {i 6∈ q, relyi } acquirei () ; releasei ()// invariant {guari , i 6∈ q}.
The intermediate states are added to the structure of the program, in this case,
between acquirei () and releasei (), representing predicates that can be used to
fulfil the antecedents of Rule (2) during a proof of the full quintuple. For in-
stance, the postcondition for acquirei () also forms the precondition for releasei (),
which is apparent from the structure of code interspersed with states (similar
to an Owicki-Gries-structured proof [32,33]). The data type invariant, that each
thread identifier in q can appear at most once, is maintained throughout.
    The specification introduces a ‘contracti ’ for thread i, which is a relation
describing thread i’s assumption about how and when the state will be modified.
Then each thread guarantees to fulfil the contract for every other thread in the
system. In this case, the contract states that i cannot be entered or removed
from the queue by any other thread, and additionally, that once in the queue it
can only ever get closer to the head: i ∈ q ⇒ q ′ !i ≤ q!i. We use the notation q!i
to denote the index of the element i in the list q. This expression is undefined if
the list q does not contain i; we ensure throughout that such indexing is defined.
6       R. Colvin et al.

    The key part establishing that this specification meets that of a lock is the
coupling invariant cinv which derives the lock state from the queue: if the queue
is empty then the lock is free, and otherwise the first thread in the queue holds
the lock. Under this definition, the predicates and relations in Fig. 2 imply the
lock properties given in Sect. 3.1. We use a similar justification later for showing
that CLH implements an (abstract) lock.


4     Functional Correctness of CLH-seL4

The seL4 microkernel was the first operating system to be formally verified for
functional correctness [24], and its development continues [16], including formal
proofs of security criteria [30]. The original proof of correctness essentially as-
sumed execution on a single core, but recent developments have seen deployment
on multicore Arm, and potentially x86 and RISC-V, necessitating the need for
managing concurrent processors. This is addressed via a system-wide lock to han-
dle interrupts, and this lock is currently implemented via a version of CLH [40].
CLH is an interesting target for verification via rely/guarantee, because it is
efficient (used in practice) and involves fine-grained concurrency that cannot be
managed by programming language abstractions: it operates at the microkernel
level and therefore cannot assume access to library code, etc.
     We first present the acquire and release operations in a C-like language cor-
responding to the implementation currently in the release version of seL4. We
apply rely/guarantee reasoning to this code, augmented with auxiliary variables
capturing key concepts, and prove that it satisfies the conditions for a concur-
rent lock. We assume lines of code are executed in the order specified (sequential
consistency) – weak memory effects are addressed in Sect. 5.


4.1   CLH-seL4 implementation

Fig. 3 contains code similar to that used in the seL4 microkernel, with interrupt-
handling specifics stripped out (that code is separate to the locking mechanism;
we have also renamed some variables for consistency with other presentations of
CLH). Broadly speaking, the code maintains a “queue” of threads in a similar
fashion to a linked list structure through the local prev variables. We give a
brief description below, but defer a full explanation of the operation of the code
until we augment it with the key auxiliary concepts. The verification does not
need to be aware of cache line sizes, etc., as that is an efficiency concern.

Types and initialisation. The code assumes a fixed number of threads, N , and
each thread i is initially allocated a pointer to its own Node, which can be accessed
via procs[i].node. The node itself is simply a boolean which indicates whether
the next waiting node must continue to wait (Pending) or may take the lock
(Granted). There is one more Node than there are threads, with this extra node
effectively marking the head of the abstract queue. The array procs is initialised
so that each thread has a unique node, and tail is initialised to the unique
                Rely-guarantee verification of locks for multicore architectures       7


    type Status = Granted | Pending    type Node = struct{status : Status}
    type proc = struct{node : ∗Node; tmp : ∗Node}
    var procs : array N of proc := . . . ;   var tail : ∗Node := . . .
    tail → status := Granted;
 acquire(i : T ) =
  procs[i].node → status := Pending;      release(i : T ) =
  var prev := swap(&tail, procs[i].node); procs[i].node → status := Granted;
  procs[i].tmp := prev;                     procs[i].node := procs[i].tmp
  await prev → status = Granted ;


   Fig. 3. Excerpt of the seL4 CLH implementation (focussing on the logic) [40].


unused node (we omit these straightforward details). Initially, the status of tail
is set to Granted so that the first node to attempt to acquire the lock may do so.

Acquire. To acquire the lock a thread i initialises its node to have the status
Pending, indicating to the subsequent thread j that joins the queue that j cannot
(immediately) take the lock. An atomic swap operation is then called, which
reads and returns the current value of the tail pointer, and updates tail to
the node of the calling thread. Thus, the prev local variable records the previous
node in the queue, and this is then stored in procs[i].tmp for access in a call to
releasei (). This prev node will eventually be used by i the next time it calls
acquire. The thread then spins on the status of the previous node, waiting for it
to become Granted, at which point thread i takes the lock and enters its critical
section. Recall that the await b command abbreviates a while loop with an empty
body, i.e., while ¬b do skip.

Release. To release the lock, the thread sets the status of its own node to Granted,
signalling to the next waiting thread that it may proceed. It also now prepares
for its next call to acquirei () by copying the node saved in procs[i].tmp into
procs[i].node. Note that another thread may concurrently take the lock and
proceed to its critical section before thread i executes this second line of releasei ().

Efficiency. In terms of space efficiency, one Node is allocated per-processor ini-
tially, plus one additional node required to track the head of an empty queue.
Threads swap nodes between themselves during execution, but the complete set
of nodes never changes – there is no need for freeing/allocating memory during
execution (as long as the total number of threads that will access the lock is
known beforehand).
    The second aspect of efficiency involves a specific interaction with the mem-
ory (cache) system. Although the status of a node can be recorded in a single
bit, the status array is padded out so that each boolean takes up space equal to
a single cache line – this is the physical unit that processors may read from main
memory. Even if a single byte is requested from main memory, the entire cache
8       R. Colvin et al.

line in which that byte resides is read into the processor’s local cache. The size of
a cache line is processor-specific; 64 bytes is a typical size used in contemporary
architectures. As long as no process in the system changes any part of that 64
bytes, the local process can read from its copy of that chunk without accessing
shared memory, which would otherwise potentially slow down the entire system.
CLH exploits this so that each processor’s spin loop is effectively spinning on
its own local cache, completely separately to every other process in the system,
and avoiding repeated requests to main memory to retrieve a value. The only
time that main memory is accessed is precisely when the previous processor in
the queue flips the status from Pending to Granted, triggering a refresh of that
cache line.

4.2   Auxiliary variables, invariants and intermediate states of
      CLH-seL4
Fig. 4 outlines the proof of the CLH-seL4, including the invariant, pre/post-
condition conditions, rely/guarantees, and intermediate states. The proof uses
the following notation, where a # t represents a non-empty list with first (head)
element a, and ‘a’ is list concatenation.

                   injective(f ) =
                                 b ∀ i j ∈ dom f . i 6= j ⇒ f (i) 6= f (j )
                 a
           last(t [a]) = a               butlast(t a [a]) = t
                      f hh[ ]ii = [ ] f hha # t ii = f (a) # (f hht ii)
                       distinct(t ) =b length(t ) = size(set (t ))

Types, initialisation, and auxiliaries. We augment the code with several auxiliary
variables to capture key ideas. The structs are carried over from Fig. 3. There
is one local variable prev per thread, which we represent in the usual way as a
mapping from thread identifiers to the type of the local – in this case, ∗Node.
As such the prev for thread i is written previ , although there is otherwise no
distinction between a local variable and an array indexed by threads. Wherever
nodes are dereferenced – to access their status – we implicitly access the heap,
which is a mapping from ∗Node to Node.
    The most complex part of the algorithm is how nodes are shared between
threads. The auxiliary variable reserved , which by convention we write in red,
keeps track of the unique node currently marked by a process for its own use.
This auxiliary concept mostly corresponds to the concrete procs[i].node, except
for a brief period during release, where a thread’s reserved node may be found
in procs[i].tmp. In a symbiotic way, the auxiliary η variable records the lone
unreserved node in the system, which is always the previous (prev) node of the
thread holding the lock, or tail if the queue is empty.
    We also maintain an abstract list of the waiting threads in q. While this value
could be derived from the concrete state, making it explicit in the code also acts
as a type of abstract “program counter”, indicating which threads are currently
attempting to acquire the lock.
               Rely-guarantee verification of locks for multicore architectures          9


    var prev : T → ∗Node;            (uninitialised local )
    var reserved : array T of ∗Node; initially λ i . procs[i].node
    var η : ∗Node;                   initially tail
    var q : T list;                  initially [ ]


    acquirei () =
                b
        {i 6∈ q ∧ procs[i].node = reserved [i]}
     procs[i].node → status := Pending;
        {i 6∈ q ∧ procs[i].node = reserved [i] ∧ procs[i].node → status = Pending}
     hprev := tail; tail := procs[i].node; q := q a [i]i;
        {i ∈ q ∧ procs[i].node = reserved [i]}
     procs[i].tmp := prev;
        {i ∈ q ∧ procs[i].node = reserved [i] ∧ procs[i].tmp = prev}
     await prev → status = Granted ;
        {i ∈ q ∧ procs[i].node = reserved [i] ∧ procs[i].tmp = η ∧ i = hd(q)}
    releasei () =
                b
         {i ∈ q ∧ procs[i].node = reserved [i] ∧ procs[i].tmp = η ∧ i = hd(q)}
      hprocs[i].node → status := Granted ; η ⇋ reserved [i] ; q := tl(q)i ;
         {i 6∈ q ∧ procs[i].tmp = reserved [i]}
      procs[i].node := procs[i].tmp
         {i 6∈ q ∧ procs[i].node = reserved [i]}


            b distinct(q) ∧ injective(reserved ) ∧ η 6∈ ran reserved ∧
  invariant =
              η → status = Granted ∧ (∀ i ∈ q . reserved [i] → status = Pending) ∧
              η # reserved hhqii = prevhhqii a [tail]                            (15)
            b id(procs[i].node, procs[i].tmp, reserved [i], reserved [i] → status) ∧
  contracti =
              (i ∈ q ⇔ i ∈ q ′ ) ∧ (i ∈ q ⇒ q ′ !i ≤ q!i)                              (16)
      relyi : invariant ∧ contracti
     guari : invariant ∧ (∀ j 6= i . contractj )
      cinv : lock = (if q = [ ] then free else hd(q))


                            Fig. 4. seL4 CLH proof structure



Acquire. The atomic swap instruction is represented as an atomic sequence of
instructions enclosed in angled brackets, h. . .i.

 prev := swap(&tail, procs[i].node) ❀ hprev := tail; tail := procs[i].nodei

The prev local is updated to the current value of tail, which is then updated
to thread i’s node. Additionally, in Fig. 4, the abstract queue q is updated with
i appended to the end, indicating the concept of i joining the queue of waiting
threads. The rest of the code corresponds to that of Fig. 3.
10      R. Colvin et al.

Release. The relatively benign-seeming line of code to set the status of the node
of the releasing thread to Granted in fact holds much of the subtlety of the
data structure. This is reflected in the abstract swap of the reserved node for
thread i with what is currently the abstract η variable. Thus, thread i takes
the now-unused former head of the node queue for itself, to be used in its next
attempt to acquire the lock; and it simultaneously leaves behind its own node
to become the current head of the node queue. Abstractly, this is reflected in
the queue of threads by removing the first node – which is i – from q. The
reserved and η auxiliary variables are only modified at this key line of release,
which straightforwardly ensures that reserved remains injective, and that η is
not reserved.

Data type invariant. The invariant describes the relationships of the different
variables in the system; in particular, it outlines the auxiliaries η and reserved ,
properties of q, and the status of nodes. The key aspect in this regard is that
reserved nodes of threads currently in the queue are always Pending, while the η
node is always Granted. Additionally, the reserved mapping is always injective,
and η is never reserved by a thread. Finally, as shown in (15), the relationship
between the abstract queue q and the concrete state is that the list of nodes
obtained by reading from the auxiliary head through the reserved nodes in the
queue, η # reserved hhqii, is equal to taking the prev node of each thread in the
queue, with tail appended to the end, prevhhq ii a [tail]. This relationship gives
a direct, list-based approach to describing CLH’s pseudo-linked list, and could
form the “coupling invariant” in a data-refinement style proof [15,28,37].

Contract between threads. The contracti between threads describes changes that
may be made to the state. It is thus a relation, or two-state predicate, in contrast
to the single-state invariant. The contract amounts to not changing the variables
assigned to a particular thread i (we use id(x , y, . . .) for the relation that does
not alter x , y, etc.); and additionally, that the status of the reserved node is
never changed (establishing this key fact without an explicit reserved variable
proved cumbersome). The contract also contains those parts already described
in the specification of a queued lock from Fig. 2: a thread cannot be entered into
or removed from the queue by another thread, and a waiting thread only ever
gets closer to the front of the queue.

Properties of an abstract lock. The status of the system lock may be derived
from the auxiliary queue as in Fig. 2: if the queue is empty no thread holds the
lock, and otherwise the thread at the head of the queue holds the lock (cinv).

Relies and guarantees. Each thread i relies on its contract being fulfilled, and
that the invariant is maintained; and conversely, guarantees to fulfil the contract
for every other thread in the system and to maintain the invariant. Establishing
that the guarantee is maintained by each line of code is the most complex part of
the proof; establishing the postconditions is relatively straightforward by careful
choice of intermediate states.
               Rely-guarantee verification of locks for multicore architectures     11

Pre/postcondition and intermediate states for acquire. The precondition for
acquirei () is that i is not already in the queue, and that the concrete node entry
accurately holds i’s unique reserved node. The intermediate states in Fig. 4 are
relatively straightforward updates of this initial precondition based on the rele-
vant assignment. At each point we track the reserved node for i, which is kept
in procs[i].node. Implicitly, each intermediate state preserves the invariant. The
non-trivial part is establishing that the current thread is indeed the head of the
abstract queue when the loop terminates; this is derivable from the invariant,
specifically (15) and the status of waiting nodes.

               i ∈ q ⇒ (previ → status = Granted ⇔ i = hd(q))                     (17)

Pre/postcondition and intermediate states for release. The releasei () operation
assumes that i is at the head of the abstract queue, that procs[i].node holds the
reserved node, and that procs[i].tmp points to the auxiliary head of the queue.
After the first line of releasei (), thread i is no longer in the queue, and has taken
the former head of the queue as its reserved node; and this node may be found in
procs[i].tmp (one cannot access previ directly since it is local to acquirei ()). The
thread therefore updates procs[i].node to procs[i].tmp, ready for the next call to
acquirei (). As with acquirei (), at each state the invariant is implicitly maintained.

4.3   Thread and system proofs
We now state the top-level theorems showing that the CLH-seL4 implemen-
tation is correct. All proofs have been encoded and machine-checked using Is-
abelle/HOL. We include an invariant in the quintuple statements (8), which adds
the invariant to pre/postconditions and rely/guarantee relations.
Theorem 1 (Acquire).

   {i 6∈ q ∧ procs[i].node = reserved [i], contracti }
 acquirei ()// invariant
   {∀ j 6= i . contractj ,
    i ∈ q ∧ procs[i].node = reserved [i] ∧ procs[i].tmp = η ∧ i = hd(q)}

Theorem 2 (Release).

    {i ∈ q ∧ procs[i].node = reserved [i] ∧ procs[i].tmp = η ∧ i = hd(q),
     contracti }
 releasei ()// invariant
    {∀ j 6= i . contractj , i 6∈ q ∧ procs[i].node = reserved [i]}

   Proof. Individual lines of code are shown to satisfy their pre/post states
outlined in Fig. 4 using the inference rules for assignments (Rule (1)), and spin
loops (Rule (7)), and are joined using Rule (2) using the relevant mid-states.
The relies and guarantees are kept constant throughout. ✷
   The top-level property for a system of N threads calling acquire and release
repeatedly is given below. The initial state is derived from that given at the
12        R. Colvin et al.

top of Fig. 4. The overall postcondition (we leave unconstrained the condition
under which a thread may finish execution) shows that the queue is empty,
though the rest of the state could have arbitrary values. Note that the guarantee
∀ i . contracti is a simplification of ∀ i . ∀ j 6= i . contractj . These simplifications of
pre/postconditions and rely/guarantees follow from Rule (3).
Theorem 3 (Locking system).
          {q = [ ] ∧ reserved = . . . , ∀ i . contracti }
      ki . while do (acquirei () ; releasei ())// invariant
          {∀ i . contracti , q = [ ] ∧ . . .}
Proof. We apply Rule (6): each individual thread satisfies its own part from
Theorems 1 and 2 (and that the postcondition of acquirei () is the precondition
of releasei (), using Rule (2)); careful choice of relyi and guari from Fig. 4 ensure
that each thread’s guarantee fulfils the rely of every other thread. ✷
     For simplicity, Theorem 3 explicitly uses the contract between individual
threads; however, from the perspective of a system that incorporates the lock,
the rely of the lock system is simply that none of its variables are modified,
and conversely the lock system guarantees to change nothing other than its own
variables. These are both implied by ∀ i . contracti .
     That the lock itself is used in such a way as to guarantee mutual exclusion to
some system variable x is something that must be shown for each client system,
i.e., that x is only ever modified between calls to acquirei () and releasei ().

5     CLH-seL4 with Weak Memory
The CLH lock is an algorithm that may be deployed at the lowest level of the
software stack, and thus has little abstraction from hardware-level concerns.
Chief among these hardware-level factors is out-of-order execution, which has
been a feature of processors since the 1960s. Processors may execute machine
instructions out-of-order to make the best use of resources. For instance, given
consecutive, independent instructions – e.g., arithmetic operations accessing dif-
ferent sets of registers – it is more efficient to execute them in parallel than wait
for the first to complete before the second begins – e.g., if multiple arithmetic
units are available.
    The key principle of out-of-order execution is that accesses to the same vari-
able x must be kept in-order, while “independent” instructions (e.g., accessing
different parts of memory) may be reordered. On a single processor, this princi-
ple maintains the correctness of sequential code while improving performance by
eliminating unused processor cycles. However, the effects of parallelisation can
become apparent on modern multicore architectures, with potentially disastrous
effects on correctness.

5.1     Identifying Weak Memory Effects
We analyse the possible weak memory effects in a piece of code by searching
for instructions that may be executed out of order. For such instructions, we
                Rely-guarantee verification of locks for multicore architectures     13

either (1) transform the code to make this parallelism explicit, where it does not
affect correctness, or (2) insert fences or other ordering constraints to enforce
the required ordering.
    For a given memory model m (for instance, Arm, x86, RISC-V, or C), fol-
                         m
lowing [2], we write α ⇐ = β if instruction β may be reordered with instruction
                                                          m
α under memory model m. Conversely, we write α ⇐         /= β if they may not be
reordered, which may be because they access the same variables, or if either
instruction includes some sort of artificial ordering constraint, such as a fence.
    If a sequential program c is subject to a memory model m, its set of traces
is determined by the (weak memory) semantics given in [2] after transforming c
by interpreting each sequential composition “;” as a parallelized sequential com-
           m
position “ ;”, which makes the inclusion of the memory model m explicit.
    Following [2] we transform code that uses parallelized sequential composition
according to refinement rules based on trace equivalence. The two key rules are
the following:
                                m             m
                              /= β
                             α⇐        ⇒ α ; β = α; β                              (18)
                                m             m
                              =β
                             α⇐        ⇒ α;β=αkβ                                   (19)

If two instructions cannot be reordered according to m, then they are executed
in order, exactly as if familiar sequential composition was used (18). Conversely,
if two instructions may be executed out of order according to m, then effectively
they are executed in parallel (19).2 Note that this second rule may result in
nested parallelism within a process.
    Most weak memory models include some sort of barrier or fence instruction
“fence” that can be used to reinstate sequential order. This is summarised by
the following rule.
                                m       m
                             c1 ; fence ; c2 = c1 ; c2                       (20)
Note that we may eliminate both the fence and the top-level references to m,
reducing parallelized sequential composition to standard sequential composition.
Similar rules apply for other ordering constraints, such as C’s memory order type.
More complex rules can be derived for conditionals and loops [2,3].


5.2    Weak Memory Effects in Acquire

To address weak memory effects on CLH we consider the interactions between
different lines of code. At this level, we must consider the atomicity of instruc-
tions explicitly. To more realistically represent the code we make the loading of
procs[i].node into a local variable (register) r explicit, i.e., , we introduce a new
(atomic) action. The individual lines of acquire from Fig. 3 are repeated below
with potential reorderings between consecutive lines made explicit.
                                                                    arm
                r := procs[i].node                                  /=
                                                                   ⇐=              (21)
2
    Forwarding needs to be taken in account in general, but does not occur in CLH.
14      R. Colvin et al.

                                                                 arm
               r → status := Pending                            ⇐==             (22)
                                                                 arm
               prev := swap(&tail, r)                           ⇐=/=            (23)
                                                                 arm
               procs[i].tmp := prev                             ⇐==             (24)
               await prev → status = Granted                                    (25)

The first two instructions may not be reordered: the first modifies r, and the
second reads r. Note that the expression r → status implicitly dereferences r,
requiring an update of the location pointed to by r. The swap operation (which
we interpret according to the atomic statement in Fig. 4) modifies both the
local prev variable and the global tail variable, and also reads (but does not
modify) r. As above, the instruction r → status := Pending reads but does not
modify r. Since r is local, these instructions can reorder according to the natural
constraints of the Arm memory model (and indeed, almost any other). Treating
pointer dereferences as a load (of a variable) and a store (to a location) is covered
by the framework in [4].
    The swap operation cannot reorder with the initial update of r, that is,
                    arm
r := procs[i].node ⇐=/= prev := swap(&tail, r) (otherwise the sequential seman-
tics would be compromised). Hence the first three instructions, executing under
Arm, is trace equivalent to the following, by (18) and (19).

     r := procs[i].node ; (r → status := Pending k prev := swap(&tail, r))

If the swap occurs first, this could lead to a violation of the part of the invariant
requiring that nodes in the queue have status Pending, and invalidate the key
property (17). We must therefore enforce ordering between the setting of status
and the swap. For Arm (or C), ordering in this case can be enforced by inserting
a fence (such as dsb), or by placing a “release” (rel) ordering constraint on the
latter of the two stores [13].
    The instruction immediately following the swap, procs[i].tmp := prev, ac-
cesses local prev, and because prev is modified by the swap those two instruc-
tions remain strictly ordered.
    The succeeding await loop can be interpreted as a sequence of loads of the
global location prev → status. All such loads are independent of the previous
store to procs[i].tmp (but, since the store and the loop both access local prev,
they are dependent on the swap). As such, the loop and the preceding assignment
may effectively happen in parallel (including if a compiler decides to restructure
the assignment after the loop).

             procs[i].tmp := prev k await prev → status = Granted               (26)

This makes no difference to the correct functioning of the code and there is no
need to enforce this ordering, in contrast to the potential reordering involving
the swap above.

Theorem 4 (Parallelization of the while loop in acquire).
 {i ∈ q ∧ procs[i].node = reserved [i], contracti }
               Rely-guarantee verification of locks for multicore architectures    15

procs[i].tmp := prev k await prev → status = Granted// invariant
  {∀ j 6= i . contractj ,
   i ∈ q ∧ procs[i].node = reserved [i] ∧ procs[i].tmp = η ∧ i = hd(q)}

Proof. For such proofs involving nested parallelism we apply Rule (4) (as op-
posed to Rule (5)). In this case the left-hand side of the parallel composition,
procs[i].tmp := prev inflicts more interference on the while loop than we had
taken into account in Fig. 4. However, Rule (7) still applies – the extra interfer-
ence by the potential change to procs[i].tmp does not compromise the stability of
the pre or post condition. Furthermore, being a spin loop, the right-hand side of
the parallel composition does not inflict any more interference on the left-hand
side assignment than had previously been accounted for. ✷
    The pre and post conditions in Theorem 4 match the pre and post condi-
tions for the corresponding sequential composition in Fig. 4 – only the midstate
is missing. We can therefore replace the sequential composition with parallel
composition and maintain top-level correctness. Whether the assignment occurs
before or after the loop makes no difference, which is precisely the reason why
such reorderings are allowed by processors and compilers.
    We may therefore determine that the only necessary artificial ordering con-
straint that must be injected into the original sequential code for CLH-seL4
is to enforce ordering between the Pending status assignment and the swap.
All other possible reorderings allowed by the memory model are irrelevant to
correctness. We summarise this below, where for space we abbreviate wait =       b
await prev → status = Granted.

      acquiresel4
                                       arm                          arm
             i    =
                  b r := procs[i].node ; r → status := Pending ;                  (27)
                                             rel arm                      arm
                   prev := swap(&tail, r)         ; procs[i].tmp := prev ; wait
               k
        acquirei =
                 b r := procs[i].node ; r → status := Pending ;                   (28)
                   prev := swap(&tail, r) ; (procs[i].tmp := prev k wait)

Theorem 5 (Acquire under arm). By trace equivalence modulo fences and
                                               k
rel ordering constraints, acquiresel4
                                 i    = acquirei .

Proof. As described above, the rel constraint on the swap operation is suf-
ficient to enforce sequential ordering and may be replaced by strict sequential
composition, and in the absence of any other ordering constraints the assign-
ment before the loop and the loop itself may be parallelized. We have therefore
                              arm
reduced all the instances of ; to either sequential or parallel composition, in
                               k
line with that given in acquirei . ✷


5.3    Weak Memory Effects in Release

The two lines of code in release involve the loading of procs[i].node followed by
the modification of the same; hence the key parts of the two instructions are kept
strictly ordered by any memory model (breaking each of the two lines of code in
16       R. Colvin et al.

release into their atomic assembler instructions introduces some parallelism as
in acquire, but not for the key store and load to procs[i].node).
                                            arm
                                        /= procs[i].node := procs[i].tmp
     procs[i].node → status := Granted ⇐=                                         (29)

As such, the sequential composition in release may be treated as strict.

Theorem 6 (Release under arm). releasesel4
                                      i    = releasei (). ✷

Proof. Immediate from (29) and (18). ✷


5.4    Reordering with the critical section

The reasoning above is sufficient for considering the code of each operation in
isolation; however, further reorderings with code between the calls to acquire
and release are possible. Essentially any reading or writing to main memory
before acquire has fully completed (been flushed from the pipeline) or while
release is being executed is problematic from the perspective of maintaining
mutual exclusion in the critical section, as outlined in Sect. 3.1. For instance,
                                              arm                arm
in a calling context, the code acquirei () ; critical section ; releasei () could
allow parallelisation between the instructions of acquirei () and shared-variable
accesses in the critical section, and even with instructions of releasei (). If the
implementation of acquire includes a full fence (in Arm, the dsb instruction
would suffice) as the final instruction, and similarly the implementation of release
includes a fence as its first instruction, by (20) we may apply standard sequential
reasoning.
                      arm    arm
           acquirei () ; crit ; releasei () = acquirei () ; crit ; releasei ()    (30)

    In contrast, code prior to a call to acquire need not be fenced, under the rea-
sonable assumption that no code other than that of acquire and release modifies
the variables in Fig. 3. Similar reasoning holds for code after a call to release;
in both cases, under reasonable assumptions about access to the lock-specific
variables, no further barriers to reordering are necessary.
    A possible exception is if thread i makes a call to release immediately prior to
a call to acquire. Again, a simple analysis of the first instruction of acquire and the
last of release shows that both access procs[i].node and hence reordering is not
                                              arm
possible. Thus we may establish releasei () ; acquirei () = releasei () ; acquirei ().


5.5    Top-level proof

Theorem 7 (Correctness of CLH under arm). The implementation of CLH
in Fig. 3, updated with a rel constraint as in (27), and augmented with dsb
barriers (or equivalent) at the end of acquire and at the beginning of release,
works as a lock under arm.
               Rely-guarantee verification of locks for multicore architectures   17

Proof. By Theorem 1, Theorem 4, and Theorem 5, the implementation of acquire
satisfies the pre and postconditions of Fig. 4; and similarly for the implementa-
tion of release by Theorem 2 and Theorem 6. These may be composed identically
to Theorem 3. The definition and validity of the interpretation of the Arm mem-
ory model is taken from [2]. ✷
    Taking into account weak memory models (in this case, Arm, though the
reasoning applies to essentially any real model, such as RISC-V and x86-TSO
[2]), we find that artificial orderings must be inserted to enforce the order of the
initialisation of the status of the local node to Pending and the atomic swap;
however, the standard constraints of standard memory models either enforce
ordering of statements, or, in the case of the loop, the stated program order of
the statements is not strictly necessary for correctness. The required additional
reasoning is separate to the application of rely/guarantee reasoning.


6   Related work

The verification of concurrent algorithms, including locks [17,23,38], has a long
history comprising a variety of techniques and tools. Approaches that have been
applied specifically to CLH include several works which have focussed on ter-
mination/liveness properties using separation logics [11,25,36]. The application
of the Starling framework to CLH [41] focusses on functional correctness, with
an underlying technique based on Owicki-Gries reasoning [33]. It is unclear how
these works can be adapted to handle the extra complexity associated with
weak memory concerns, which must be taken into account when considering
deployment of CLH on modern devices. As we show in Sect. 5, some but not
all of the parallelism that multicore architectures introduce can be retained. A
verification approach that instead insists on restoring full sequential ordering
would therefore introduce unnecessary inefficiencies associated with the overuse
of fences. We have not addressed termination directly in this paper, however we
can use the results of Sect. 5 to enable the application of standard techniques;
we have made a step towards that by showing that every process is guaranteed
to only ever advance in the abstract queue (16). By basing our approach on
rely/guarantee reasoning we get compositionality – helpful for managing micro-
parallelism of weak memory effects – and an existing machine-checked theory
base in Isabelle/HOL [35].
    If we were instead to attempt to verify CLH directly using a weak-memory-
specific technique such as [9,10,22] we would typically need to rework the verifica-
tion conditions (pre/postconditions) into a technique-specific assertion language,
designed to capture weak memory effects, and apply technique-specific inference
rules. In our approach, weak memory effects are elucidated separately to the
main verification process. Furthermore, we may tackle other properties of CLH
– for instance, liveness and security, both of importance in the context of appli-
cations such as seL4 – by applying standard techniques to the transformed code;
otherwise, new assertion languages and inference systems need to be devised
to handle these additional concerns under the effects of weak memory models.
18     R. Colvin et al.

The approach of [6] is based on a similar semantic model to ours, but is, again,
specific to a particular verification technique; however, it has been adapted to
handle the Power architecture, which includes other micro-architectural features
that complicate correctness [7]. Our separation-of-concerns approach has a fur-
ther advantage in that the inclusion of auxiliary variables does not complicate
the reasoning about weak memory effects.


7    Conclusions

We have shown an end-to-end machine-checked verification of a complex, prac-
tical, in-use concurrent algorithm for multicore architectures such as Arm. The
approach is centred on Jones’ rely/guarantee concept, which is suitable for de-
scribing top-level specifications (Sect. 3), detailed proofs of individual threads
(Sect. 4), and compositional reasoning about inter- and intra-thread parallelism
(Sect. 5). We utilise and specialise mature tool support for theorem proving using
rely/guarantee concepts [35,31,34] (theory files available on request).
    In constructing the proof in Sect. 4 we also proved several simpler algorithms,
including: abstract versions of locks, one with only a single lock variable, and
one with an explicit q variable as in Sect. 3; two versions of an array-based
queue lock (which suffers from space considerations when multiple locks are
used within a system); and an alternative version of CLH given by Scott [39]. In
this last proof we were able to reuse many of the results from Sect. 4, and indeed
to show that both implementations are compatible, in the sense that different
threads could use the different implementations without clashing. This reuse
is owed in large part to abstracting the details in auxiliary variables and the
inherent compositionality of rely/guarantee reasoning, as well as separating the
weak memory effect reasoning (again, much of which was reused). A more typical
approach is to use program counters or the application of Owicki-Gries, both of
which would make proof reuse across different implementations much harder.
    We are currently working towards the automation of the program-level rea-
soning in Sect. 5 and tool support for derivational rely/guarantee proofs [14,5].
    Acknowledgements. This project was funded by the Department of De-
fence and administered through the Advanced Strategic Capabilities Accelerator.
We thank David Gwynne for help with understanding the efficiency implications
of CLH.


References

 1. Coleman, J.W., Jones, C.B.: A structural proof of the soundness
    of rely/guarantee rules. J. Log. Comput. 17(4), 807–841 (2007).
    https://doi.org/10.1093/logcom/exm030
 2. Colvin,    R.J.:    Parallelized    sequential  composition    and   hard-
    ware    weak     memory     models.   In:   SEFM.   pp.    201–221 (2021).
    https://doi.org/10.1007/978-3-030-92124-8_12
               Rely-guarantee verification of locks for multicore architectures      19

 3. Colvin, R.J.: Separation of concerning things: A simpler basis for defining and pro-
    gramming with the C/C++ memory model. In: ICFEM. pp. 71–89 (2022).
    https://doi.org/10.1007/978-3-031-17244-1_5
 4. Colvin,     R.J.:  A     fine-grained   semantics      for    arrays   and    point-
    ers under weak memory models. In: FM. pp. 301–320 (2023).
    https://doi.org/10.1007/978-3-031-27481-7_18
 5. Colvin, R.J., Hayes, I.J., Meinicke, L.A.: Designing a semantic model for a wide-
    spectrum language with concurrency. Form. Asp. Comput. 29(5), 853–875 (Sep
    2017). https://doi.org/10.1007/s00165-017-0416-4
 6. Coughlin, N., Smith, G.: Compositional noninterference on hardware
    weak memory models. Sci. Comput. Program. 217, 102779 (2022).
    https://doi.org/10.1016/j.scico.2022.102779
 7. Coughlin, N., Winter, K., Smith, G.: Compositional reasoning for non-
    multicopy atomic architectures. Form. Asp. Comput. 35(2) (2023).
    https://doi.org/10.1145/3574137
 8. Craig, T.S.: Building FIFO and priority-queuing spin locks from atomic swap.
    Tech. Rep. 93-02-02, University of Washington (1993)
 9. Dinsdale-Young, T., Birkedal, L., Gardner, P., Parkinson, M., Yang, H.: Views:
    Compositional reasoning for concurrent programs. In: POPL. p. 287–300 (2013).
    https://doi.org/10.1145/2429069.2429104
10. Doherty, S., Dalvandi, S., Dongol, B., Wehrheim, H.: Unifying operational weak
    memory verification: An axiomatic approach. ACM Trans. Comput. Log. 23(4)
    (2022). https://doi.org/10.1145/3545117
11. D’Osualdo, E., Sutherland, J., Farzan, A., Gardner, P.: TaDA Live: Compositional
    reasoning for termination of fine-grained concurrent programs. ACM Trans. Pro-
    gram. Lang. Syst. 43(4) (2021). https://doi.org/10.1145/3477082
12. Floyd, R.W.: Assigning meanings to programs. Math. Asp. Comput. Sci. 19, 19–32
    (1967)
13. Gharachorloo, K., Lenoski, D., Laudon, J., Gibbons, P., Gupta, A., Hennessy, J.:
    Memory consistency and event ordering in scalable shared-memory multiproces-
    sors. In: ISCA. pp. 15–26 (1990). https://doi.org/10.1145/325164.325102
14. Hayes, I.J., Colvin, R.J., Meinicke, L.A., Winter, K., Velykis, A.: An
    algebra of synchronous atomic steps. In: FM. pp. 352–369 (2016).
    https://doi.org/10.1007/978-3-319-48989-6_22
15. He, J., Hoare, C., Sanders, J.: Data refinement refined (resume). In: ESOP. pp.
    187–196 (1986). https://doi.org/10.1007/3-540-16442-1_14
16. Heiser, G., Klein, G., Andronick, J.: seL4 in Australia: From research
    to real-world trustworthy systems. Commun. ACM 63(4), 72–75 (2020).
    https://doi.org/10.1145/3378426
17. Hesselink,     W.H.:      Mechanical     verification      of    Lamport’s     Bak-
    ery algorithm.      Sci. Comput. Program.             78(9), 1622–1638       (2013).
    https://doi.org/10.1016/j.scico.2013.03.003
18. Hoare, C.A.R.: An axiomatic basis for computer programming. Commun. ACM
    12(10), 576–580 (1969). https://doi.org/10.1145/363235.363259
19. Jones, C.B.: Development Methods for Computer Programs including a Notion of
    Interference. Ph.D. thesis, Oxford University (1981)
20. Jones, C.B.: Specification and design of (parallel) programs. In: IFIP Congress.
    pp. 321–332 (1983)
21. Jones, C.B.: Tentative steps toward a development method for interfer-
    ing programs. ACM Trans. Program. Lang. Syst. 5(4), 596–619 (1983).
    https://doi.org/10.1145/69575.69577
20      R. Colvin et al.

22. Kang, J., Hur, C.K., Lahav, O., Vafeiadis, V., Dreyer, D.: A promising
    semantics for relaxed-memory concurrency. In: POPL. pp. 175–189 (2017).
    https://doi.org/10.1145/3009837.3009850
23. Kim, J., Sjöberg, V., Gu, R., Shao, Z.: Safety and liveness
    of MCS lock—layer by layer. In: APLAS. pp. 273–297 (2017).
    https://doi.org/10.1007/978-3-319-71237-6_14
24. Klein, G., Elphinstone, K., Heiser, G., Andronick, J., Cock, D., Derrin, P., Elka-
    duwe, D., Engelhardt, K., Kolanski, R., Norrish, M., Sewell, T., Tuch, H., Win-
    wood, S.: seL4: Formal verification of an OS kernel. In: SOSP. pp. 207–220 (2009).
    https://doi.org/10.1145/1629575.1629596
25. Liang, H., Feng, X.: A program logic for concurrent objects under fair scheduling.
    In: POPL. pp. 385–399 (2016). https://doi.org/10.1145/2837614.2837635
26. Magnusson, P., Landin, A., Hagersten, E.: Efficient software synchronization on
    large cache coherent multiprocessors. Tech. Rep. T94-07, Swedish Inst. C. S. (1994)
27. Magnusson,      P.,   Landin,     A.,    Hagersten,    E.:    Queue    locks     on
    cache     coherent   multiprocessors.     In:   IPPS.     pp.   165–171     (1994).
    https://doi.org/10.1109/IPPS.1994.288305
28. Morgan, C., Gardiner, P.: Data refinement by calculation. Acta Inform. 27, 481–
    503 (1990). https://doi.org/10.1007/BF00277386
29. Morgan, C.: Programming from Specifications. Prentice Hall, second edn. (1994)
30. Murray, T., Matichuk, D., Brassil, M., Gammie, P., Bourke, T., Seefried, S., Lewis,
    C., Gao, X., Klein, G.: seL4: From general purpose to a proof of information flow
    enforcement. In: SP. pp. 415–429 (2013). https://doi.org/10.1109/SP.2013.35
31. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL: A Proof Assistant for
    Higher-Order Logic, LNCS, vol. 2283. Springer (2002)
32. Nipkow, T., Prensa Nieto, L.: Owicki/Gries in Isabelle/HOL. In: FASE. pp. 188–
    203 (1999). https://doi.org/10.1007/978-3-540-49020-3_13
33. Owicki, S., Gries, D.: An axiomatic proof technique for parallel programs I. Acta
    Inform. 6(4), 319–340 (1976). https://doi.org/10.1007/BF00268134
34. Paulson, L.C.: Isabelle: a generic theorem prover. Springer (1994)
35. Prensa Nieto, L.: The rely-guarantee method in Isabelle/HOL. In: ESOP. pp. 348–
    362 (2003). https://doi.org/10.1007/3-540-36575-3_24
36. Reinhard, T., Jacobs, B.: Ghost signals: Verifying termination with busy waiting.
    In: CAV. pp. 27–50 (2021). https://doi.org/10.1007/978-3-030-81688-9_2
37. de Roever, W.P., Engelhardt, K.: Data Refinement: Model-Oriented Proof Methods
    and their Comparison. Cambridge University Press (2001)
38. Schellhorn, G., Travkin, O., Wehrheim, H.: Towards a thread-local
    proof technique for starvation freedom. In: IFM. pp. 193–209 (2016).
    https://doi.org/10.1007/978-3-319-33693-0_13
39. Scott,      M.L.:    Shared-Memory         Synchronization.     Synthesis      Lec-
    tures    on    Computer      Architecture,    Morgan     and   Claypool     (2013).
    https://doi.org/10.1007/978-3-031-01740-7
40. The seL4 Foundation: CLH lock in seL4. https://github.com/seL4/seL4/blob/
    master/include/smp/lock.h (2020)
41. Windsor, M., Dodds, M., Simner, B., Parkinson, M.J.: Starling: Lightweight
    concurrency verification with views. In: CAV. pp. 544–569 (2017).
    https://doi.org/10.1007/978-3-319-63387-9_27
