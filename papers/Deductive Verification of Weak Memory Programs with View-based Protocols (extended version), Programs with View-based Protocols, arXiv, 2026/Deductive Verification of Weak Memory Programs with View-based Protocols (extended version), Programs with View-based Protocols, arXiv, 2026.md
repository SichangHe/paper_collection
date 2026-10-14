                                                 Deductive Verification of Weak Memory
                                                  Programs with View-based Protocols
                                                          (extended version)⋆

                                         Ömer Şakar1[0000−0003−3457−5446] , Soham Chakraborty2[0000−0002−4454−2050] ,
                                         Marieke Huisman1[0000−0003−4467−072X] , and Anton Wijs3[0000−0002−2071−9624]
arXiv:2604.21084v1 [cs.LO] 22 Apr 2026




                                                                 1
                                                                  University of Twente, The Netherlands
                                                                {o.f.o.sakar, m.huisman}@utwente.nl
                                                                     2
                                                                       TU Delft, The Netherlands
                                                                    s.s.chakraborty@tudelft.nl
                                                         3
                                                           Eindhoven University of Technology, The Netherlands
                                                                           a.j.wijs@tue.nl



                                                 Abstract. Concurrent programming under weak memory concurrency
                                                 faces substantial challenges to ensure correctness due to program behav-
                                                 iors that cannot be explained by thread interleaving, a.k.a. sequential
                                                 consistency. While several program logics are proposed to reason about
                                                 weak memory concurrency, their usage has been limited to intricate man-
                                                 ual proofs. On the other hand, the VerCors verifier provides a rich toolset
                                                 for automated deductive verification for sequential consistency.
                                                 In this paper, we bridge this gap for automated deductive verification of
                                                 weak memory concurrent programs with the VerCors deductive verifica-
                                                 tion tool. We propose an approach to encode weak memory concurrency
                                                 in VerCors. We develop VerCors-relaxed, where we extend the VerCors
                                                 atomics support and bring concepts from several protocol automata to
                                                 encode permission-based separation logics for weak memory concurrency
                                                 models. To demonstrate the effectiveness of our approach, we encode
                                                 the relaxed fragment of the SLR program logic, a recent state-of-the-
                                                 art permission-based separation logic for weak memory concurrency in
                                                 VerCors-relaxed, our extension of VerCors. We use the SLR encoding
                                                 on VerCors-relaxed to automatically verify several examples from the
                                                 literature within realistic performance.

                                                 Keywords: Weak Memory· Deductive Verification · VerCors · Con-
                                                 current Programs


                                         1     Introduction

                                         Reasoning about programs with weak memory models is challenging, but nec-
                                         essary, as modern compilers apply a range of optimisations depending on the
                                         ⋆
                                             This is a preprint. The Version of Record is published in Model Checking Software
                                             (SPIN 2026) and is available at TBD.
2       Ö. Şakar et al.

targeted hardware. The challenge is that weak memory models allow program
executions that are not explainable by a sequentially-consistent (SC) interleaving
of thread instructions, and may cause program outcomes that are unexpected.
    To formally reason about weak memory models, several program logics such
as Relaxed Separation Logic (RSL) [39], GPS [36] and FSL [16] have been de-
veloped. These logics tackle different (parts of) weak memory models. However,
all these logics require proving manually whether or not an execution is allowed
by a given weak memory model.
    In this work, we focus on the deductive verification of weak memory pro-
grams. Previous work in this direction [6,7,36] used protocols per location to
specify the possible writes to a location in the entire program. We take a slightly
different approach, and use protocols to specify the possible writes per thread-
location combination, more specifically, for a thread and a location it intends to
write to. We combine this with thread-local views that capture the progress of
all threads. These two ingredients are combined into view-based protocols.
    Concretely, we propose VerCors-relaxed as an approach to encode relaxed
memory accesses using view-based protocols in VerCors, a deductive verifier
for concurrent programs using permission-based separation logic (PBSL) with
support for SC atomics [6,7]. The proposed encoding focuses on usability and
automation in modular verification, as it reasons about threads one by one,
considering their instructions in SC order. We demonstrate that our encoding
with view-based protocols provides an elegant way to reason about reordered
writes to different locations for all threads in the program, and thus gives the
possibility to reason about speculative writes.
    To demonstrate the effectiveness of our approach, we encode the relaxed frag-
ment of the SLR program logic [35], a recent state-of-the-art logic using PBSL
for weak memory concurrency, in VerCors-relaxed. SLR suits our approach well
since both use PBSL. We use the SLR encoding in VerCors-relaxed to automat-
ically verify several examples from the literature with realistic performance.
Outline & Contributions. Section 2 introduces a small programming language
and VerCors’ PVL language. Section 3 explains the first contribution of the pa-
per, namely the concept of view-based protocols and the reasoning with them,
using examples. Section 4 explains SLR, its rules and its encoding using the view-
based protocols. Section 5 then explains the second contribution, the encoding of
protocols and thread-local views into VerCors. Several examples from the litera-
ture are encoded into VerCors-relaxed, discussed in Section 6. Section 7 discusses
related work. Finally, Section 8 concludes the paper and discusses future work.


2   Preliminaries

Programming language. To keep our examples general and not restricted to
a particular programming language, we use a basic language to express how
registers and shared variables are updated. First of all, a parallel program is
executed by a set of threads T that access a set of atomic locations A and a set
                          Deductive Verification of Weak Memory Programs         3

 1   class ArraySum {
 2     int sum;
 3     /*@ context (∀ int i=0..N; Perm(xs[i], 1\2)) ** Perm(sum, write);
 4       requires (∀ int i=0..N; 0 <= xs[i]) ** sum == 0;;
 5       ensures sum >= 0; @*/
 6     void parSum(int[] xs) {
 7       invariant Inv(/*@ Perm(sum, write) ** sum >= 0 @*/) {
 8         par (int tid=0..N)
 9         /*@ context Perm(xs[tid], 1\2) ** xs[tid] >= 0; @*/
10         {
11           atomic(Inv) {
12             sum = sum + xs[tid]; }}}}}


               Fig. 1: A PVL program summing an array in parallel.



of register variables Reg. Without loss of generality, we assume that all variables
in A ∪ Reg are of a generic type V, and v ∈ V is a value from this domain.
    There are three ways to interact with atomic memory:
 1. Writing of the value v ∈ V to atomic location x ∈ A by thread t ∈ T,
    corresponding to a relaxed write instruction, e.g., the store operation x := 1.
 2. Reading of the value v ∈ V from atomic location x ∈ A by thread t ∈ T,
    corresponding to a relaxed read instruction, e.g., the load operation a := x
    where a is a register/local variable.
 3. A RWM operation of thread t ∈ T that atomically reads the value v ∈ V from
    atomic location x ∈ A and writes the value w ∈ V to x if v is the expected
    value, corresponding to a relaxed read-modify-write, e.g., rmw (x,0,2).
VerCors. VerCors is a deductive verifier aimed at concurrent software [8]. Ver-
Cors uses PBSL (Permission-based Separation Logic) [10,11,13], which allows it
to reason about data-race freedom, memory safety, and functional correctness of
sequential and concurrent programs. VerCors supports multiple input languages
such as Java, C/C++, OpenCL and its language PVL (Prototypal Verification
Language), which is mainly used to prototype verification features. It supports
classes and methods similar to Java and verification-related concepts. The rest
of this section introduces the PVL constructs needed for the work in this paper.
    An example PVL program is shown in Fig. 1. It uses parallel blocks, invariants
and atomics. We use a slightly modified syntax of PVL for readability. In the
example, we verify that the sum over positive integers is also positive.
    The parSum method in the ArraySum class (l.6) has a pre-/postcondition style
contract (l.3–5). The keywords requires and ensures specify pre- and postcon-
ditions, respectively and context is short for both a pre- and postcondition.
    The context statement (l.3) specifies permission over the array xs. In PBSL,
permissions capture which threads can access which memory locations. To spec-
ify permissions, the Perm(L, p) predicate is used where L is a shared heap
4       Ö. Şakar et al.

location and p a fractional in interval (0,1], where read permission is in (0,1)
and write permission is 1 (also written as write).
    Note that ∗∗ and && denote separating (in separation logic) and logical con-
junction, respectively and that ∀* and ∀ denote the separating [30] and standard
universal conjunction, respectively. Permissions can be split and joined, e.g.,
Perm(L,1\2) ** Perm(L,1\2) ⇔ Perm(L,1), to distribute permissions over
threads. VerCors, using the underlying theory, can prove absence of data races
(thread safety) by proving that the total permission per memory location does
not exceed 1 at any point in time.
    The method contains an invariant block (l.7–12). The invariant Inv is a
statically scoped invariant. It can only be used in the scope of its declaration.
It has to hold where it is defined (l.7) and is used for reasoning about atomic
operations (l.11–12), explained below. It specifies write permission over the field
sum (l.2) and that sum always contains a positive value (including zero).
    The body of the invariant block (l.7–12) contains a parallel block (l.8), which
models the spawning of N threads that execute the body concurrently, with
unique identifiers tid. The parallel block has a thread contract (l.9), which
specifies the contract for a single thread. The thread contract in Fig. 1 specifies
half (i.e. read) permission for the location xs[tid] and that xs[tid] is positive.
    The parallel block consists of an atomic block (l.11), which is executed in
one step, i.e., atomically. The atomic invariant Inv captures the shared state
that is accessed by the atomic instructions, corresponding to the atomic rule in
Concurrent Separation Logic [37]. The body of the atomic block increments sum
by xs[tid]. This is allowed since the invariant Inv contains write permission.


3   Proposed Approach: Protocols and Thread-local views

This section introduces weak memory programs using examples. Next, the con-
cepts of single-thread protocols and thread-local views are explained. The pro-
tocols and the thread-local views are used in the encoding of SLR in Section 4.
Finally, the verification procedure is explained, by which we reason about coher-
ence properties. This procedure is encoded into VerCors-relaxed in Section 5.

Examples of Weak Memory Programs. Fig. 2 shows example programs
rerevisited throughout this paper. Register variables are named a, b, . . . ∈ Reg,
and atomically accessible (shared) locations are named x, y, . . . ∈ A. Threads
are labeled T0 , T1 , . . . ∈ T. All atomic reads and writes use the relaxed memory
ordering, on which only SC-per-location is imposed. We assume that all vari-
ables have been initialized to 0. Allowed results are written in blue comments,
while inconsistent results are in red comments. For instance, in the 2+2W (i.e.,
2 writes per-thread, 2 in parallel) example [23], both a and b may be assigned
the value 2 in the same execution, which is due to the fact that the writes to x
and y can be reordered. However, in the COH (i.e., coherence) program [23], if
a is assigned 2, then b cannot be 1, as that would violate SC-per-location since
the write actions would be observed in different orders. Both examples can be
                            Deductive Verification of Weak Memory Programs              5

                          (2+2W)
                                                       (COH)
                  x := 2      y := 2
                                               x := 1     x := 2
                  y := 1      x := 1
                                               a := x //2 b := x //1
                  a := y //2 b := x //2
                                                    T0        T1
                       T0         T1

        Fig. 2: Two example programs using atomics with relaxed orderings.




             Fig. 3: Protocols for the 2+2W and COH examples in Fig. 2.


automatically reasoned about with view-based protocols using VerCors-relaxed.

Protocols. A protocol is a tree that models the stores to an atomic location for
a particular thread. The concept comes from GPS [36], in which all writes of a
program to an atomic location are modeled in one protocol. The current work
differs by defining a protocol per thread and atomic location combination.
Definition 1. A protocol Pxt is a tuple (Sxt , ŝtx , →t,x , Fxt , Vxt ), where x ∈ A with
type V is an atomic location and t ∈ T a thread identifier, Sxt is a finite set
of states, ŝtx ∈ Sxt is the initial state, Fxt ⊆ Sxt is the set of accepting states,
→t,x : Sxt × V × Sxt is the transition relation between states in Sxt with labels
v ∈ V. The labels represent the values that are written to x, and doing so leads
to the target state of the corresponding transition. Finally, Vxt : Sxt → V is
a function that maps states to values, with ∀(s, v, s′ ) ∈→t,x .Vxt (s′ ) = v, and
Vxt (ŝtx ) = v0 , with v0 the predefined initial value of x.
         v
With s −  →t,x s′ , we express that (s, v, s′ ) ∈→t,x . With →∗t,x , we refer to the tran-
sitive, reflexive closure of →t,x . A protocol can be interpreted as a graph, with
the states being the vertices and →t,x defining the edges. We restrict protocols to
                                       v
trees, i.e., 1) ∀s, s′ ∈ Sxt , v ∈ V.s −
                                       →t,x s′ =⇒ s′ ̸→∗t,x s (→t,x is cycle-free) and
2) ∀s, s ∈ Sx .(s ̸→t,x s ∧ s ̸→t,x s) =⇒ ¬∃s′′ ∈ Sxt .s →∗t,x s′′ ∧ s′ →∗t,x s′′ (for
         ′     t       ∗   ′     ′   ∗

every two states between which no path defined by →∗t,x exists, no state is reach-
able from both via →∗t,x ). Since protocols are trees, we can define a partial-order
of the states using →∗t,x : for two states s, s′ ∈ Sxt , we have s ≤ s′ iff s →∗t,x s′ .
    For the 2+2W program in Fig. 2, Fig. 3 shows four protocols, used to spec-
ify writing behavior. The protocols are used for speculative load operations,
explained in the next section. A protocol Pxt exists for each t ∈ T and x ∈ A
to which t writes to. In the example, both threads write to x and y, therefore
we have Px0 , Px1 , Py0 and Py1 . States are labeled si,j
                                                        x , where i refers to thread Ti
6        Ö. Şakar et al.

associated with it, j serves to differentiate states, and x refers to the associ-
ated atomic location. Initial states ŝi,j
                                       x are indicated by an incoming transition
without a source state. Edges between states are part of →t,x , where the label
signifies the written value. The values associated with the states are written in
blue between curly brackets. The accepting states are indicated by double circles.
    At the start of the parallel program, the protocols for all threads start in
their initial states. At the end of the program, all protocols must have reached
an accepting state for the execution to be valid w.r.t. the memory model.
    In the following, with S, we refer to the set of all states of all protocols
together for a given program, and with Sx , we refer to the set of all states of all
protocols for location x. Similarly, with Ŝ, we refer to the set of all initial states
of all protocols, and with Ŝx to the set of all initial states of protocols for x.
Thread-local views.
Definition 2. Each thread t has for every atomic location x a thread-local view
Ltx : T → S ∪ {⊥}. The thread-local view maps each thread t′ ∈ T to a state of
                ′
its protocol Pxt . If the protocol does not exist, then t′ maps to ⊥.
Each thread t uses for each location x that it intends to access, the local view of
its own protocol Pxt , i.e., Ltx (t), to keep track of its own write operations to x,
                                          ′
and its local view of the protocols Pxt of other threads t′ , i.e., Ltx (t′ ), to speculate
about the writes that those threads can perform to x.
     Initially, each thread-local view points to the initial states, i.e., ∀t,t′ ∈T Ltx (t′ ) =
  t′
ŝx . The set of all possible views for a program is called W. For a given program
with threads T and atomic locations A, the function L : T × A → W maps each
pair (t ∈ T, x ∈ A) to thread-local view Ltx .
     The SOS rules in Fig. 5 define how thread-local views evolve as load and
store operations are executed. The contracts of load and store follow the SOS
rules. Prior to discussing the rules, we need to define which values a thread can
read when a load operation is executed, as determined by a thread’s local view.
     The values that can be read from location x are the values that are associated
with states from the protocols for x that are reachable from the respective current
states as defined by the view. There are, however, two conditions: first, from its
own protocols, a thread can only select the value associated with the current
state, not a value associated with a reachable state, i.e., it cannot speculate about
its write operations, and second, as soon as one write to x has occurred, the initial
value of x cannot be read anymore. In Fig. 4, the functions PReadtx : W → 2S
map views to sets of reachable states, and the functions Readtx : W → 2S use this
to involve the condition related to initial values. Note the use of π and τ , which
are there to keep track of the observed modification order of writes, to guarantee
write and read coherence. The most recently observed store operation, for every
x ∈ A, represented by a protocol state, is stored by the function π : A → S, and
the function τ : A → S × S maps locations to relations that store the observed
modification order for that location. In PReadtx , these are used to ensure that a
state s is selected only if it is not τ + -before (i.e. the transitive closure over τ )
the most recently observed store operation for that location.
                                  Deductive Verification of Weak Memory Programs                        7


 PReadtx (L, π, τ ) = {s | ∃t′ ∈ T. t ̸= t′ ∧ Ltx (t′ ) →∗t′ ,x s ∧ ¬τ (x)+ (s, π(x)) } ∪ {π(x)}
                    ∧
                                                                                           

                         
                             PReadtx (L, π, τ ),                                     , if π(x) = ŝtx
   Readtx (L, π, τ ) =
                     ∧
                                                       ′
                             PReadtx (L, π, τ ) \ {ŝtx | ∃t′ ∈ T.Ltx (t′ ) ̸= ⊥}    , else

                            Fig. 4: The Readtx and PReadtx functions.


                                                             v
                                            t∈T      Ltx (t) −
                                                             →t,x s
(Write)              x:=v
          ⟨L, π, τ ⟩ −−−→t,x ⟨L[(t, x) 7→ Ltx [t 7→ s]], π[x 7→ s], τ [x 7→ τ (x) ∪ {(π(x), s)}]⟩
                                                                      ′          ′
                             t, t′ ∈ T   s ∈ Readtx (L, π, τ ) ∩ Sxt      x = Vxt (s)
(Read)              a:=x
          ⟨L, π, τ ⟩ −−−→t,x ⟨L[(t, x) 7→ Ltx [t′ 7→ s]], π[x 7→ s], τ [x 7→ τ (x) ∪ {(π(x), s)}]⟩

 Fig. 5: Operational semantics for protocol views with load and store operations.




    In Fig. 5, the Write-rule expresses that a store operation can be executed
when from the current state Ltx (t) of Pxt , a transition labeled v exists to a state
s ∈ Sxt . When this operation has been executed, the thread-local view is updated
to indicate that the new current state of Pxt is s. Also, π(x) is updated to s, and
τ (x) is updated to indicate that the old π(x) is before s. Program verification
states are represented by tuples ⟨L, π, τ ⟩.
   The Read-rule expresses that a load operation can be executed when a state
       ′
s ∈ Sxt can be read from according to Readtx (L, π, τ ). We can then select s,
which means that after execution of the load operation, the thread-local view
and π(x) are updated, and τ (x) is extended by mapping the old π(x) to s.
    Consider the COH example in Fig. 2. The thread-local view L0x is in its initial
                                            0
state with π(x) = ŝ0,0                                     0,0 1,0 1,1
                    x , τ = {} and PReadx (L, π, τ ) = {ŝx , ŝx , sx }, since both
           1                            1 0        ∗
states of Px are reachable, i.e., ∀s ∈ Sx .Lx (1) →t′ ,x s holds and τ is empty.
    After the write of 1 to x by T0 , L0x (0) = s0,1x  and L0x (1) = ŝ1,0
                                                                       x . Suppose
T0 reads the value 2 from sx and τ is updated such that (sx0,1 , s1,1
                                 1,1
                                                                        x ) ∈ τ . Af-
ter the write of 2 to x by T1 , L1x (0) = ŝx0,0 and L1x (1) = s1,1
                                                                 x . In this state,
PRead1x (L, π, τ ) = {ŝ0,0  1,1                            0
                        x , sx }, since the both states of Px are reachable, how-
ever only for state ŝx it holds that ¬τ (x) (s, π(x)), since (s0,1
                       0,0                   +                        1,1
                                                                x , ŝx ) ∈ τ .

     The case distinction in Readtx is to differentiate a local view from which the
initial state is observable. If some thread t has observed any non-initial state,
i.e., ∃t′ ∈ T.Ltx (t′ ) ̸= ŝtx , it means that the initial state can never be observed
anymore, since for any non-initial state s it holds that ŝtx ≤ s. This corresponds
to the second case in Readtx , where the initial states are removed if π(x) ̸= ŝtx .
Do note here that all initial states essentially represent the same starting value
for an atomic location, e.g., ŝ0,0          1,0
                                     x and ŝx in Fig. 3 both represent the initial state
8        Ö. Şakar et al.

of x. Although they represent the same starting value, they are differentiated
since they are associated with different threads.
The Verification Procedure. This section explains the verification procedure
of parallel programs using the view-based protocols. The encoding of the pro-
cedure into VerCors-relaxed is explained in Section 5 and Appendix A. At the
start, for all threads t ∈ T, an initial thread-local view Ltx is created for each
x ∈ A, the function π is initialized to the respective initial states for each atomic
location and the function τ is created, initially undefined. Then, repeatedly, the
SOS rules are applied in all possible ways, to obtain a state space of executions.
For the construction of an execution, first, the operations of one thread t are
considered in program order, having first defined π(x) = ŝtx for all x ∈ A, or
π(x) = ⊥, if the protocol does not exist. The Ltx for all relevant x ∈ A, π(x) and
τ (x) are updated according to the SOS rules as the corresponding operations are
executed. Once this has been done, the operations of another thread t′ ̸= t are
                                                                              ′
considered, after π has been reset, this time reading and updating the Ltx views.
When all threads have been processed in this way, a final consistency check is
performed to determine whether an execution speculated a value that was never
written to: if this is the case, the execution is ignored. An execution is consistent
iff:
                      ∀t ∈ T, x ∈ A.Ltx (t) ̸= ⊥ =⇒ Ltx (t) ∈ Fxt                    (CC1)
                                                              ′
                           ∀t, t′ ∈ T, x ∈ A.Ltx (t′ ) →∗ Ltx (t′ )                  (CC2)

Condition CC1 expresses that in each protocol, we have reached a final state in
the view of the thread owning that protocol. A violation of this would mean that
the thread has not completely behaved as specified by the protocol. The condi-
tion CC1 has to hold at the end of the program. The condition CC2 expresses
that any speculations done by a thread t about writes of a thread t′ have been
                           ′
valid, i.e., the state Ltx (t′ ), representing the actual writes of t′ , is reachable from
Ltx (t′ ), representing the writes that t assumed t′ would perform. The condition
CC2 has to hold throughout the execution.
     To demonstrate this procedure, we consider again the examples in Fig. 2.
Consider the 2+2W example, for which the protocols given in Fig. 3. Initially,
we have L0x (0) = ŝ0,0      0          1,0 0        0,2       0        1,2
                       x , Lx (1) = ŝx , Ly (0) = ŝy and Ly (1) = ŝy . Views Lx and
                                                                                      1
   1
Ly are defined similarly. When verifying T0 ’s instructions, we first have π(x) =
ŝ0,0
  x    and π(y) = ŝ0,2                                                        0
                       y , and then encounter "x := 2", resulting in Lx (0) = sx ,
                                                                                        0,1
             0,1                    0,0 0,1
π(x) = sx and τ (x) = {(ŝx , sx )}. Next, "y := 1" is encountered, resulting
in L0y (0) = s0,3              0,3                 0,2 0,3
                 y , π(y) = sy , and τ (y) = {(ŝy , sy )}. After that, a load opera-
tion from y is encountered. The possible values are represented by L0y (0), plus all
states reachable from L0y (1), minus the latter’s initial state, as a write to y has
been observed (see the definition of Readtx ). This means that the possible val-
ues are Vy0 (s0,3                  1 1,3
                 y ) = 1 and Vy (sy ) = 2. Hence, operations "y := 1" and "y := 2"
by T0 are both enabled. We set π(y) = s1,3                          0,2 0,3      0,3 1,3
                                                y and τ (y) = {(ŝy , sy ), (sy , sy )}.
Next, we consider T1 . The first two store operations lead to Ly (1) = s1,31
                                                                                    y   and
L1x (1) = s1,1
             x    (and appropriate     updates of π and  τ ). In a similar   way as for  T0 ,
                               Deductive Verification of Weak Memory Programs                      9
                                             ϕ(v) is pure
                                                                                             (w−rlx)
                                                              ∃ts′ > ts.
                                                                                      
                       W p (x, X) ∗ ϕ(v) ∗
               ⊢                                 x := v
                                                              W p x, {(v, ts′ )} ∪ X
                                                                                     
                        O(x, −, ts)

                                  Fig. 6: The w−rlx rule



the next two possible load operations are associated with sx0,1 and s1,1       x , meaning
that both 1 and 2 can be read. Hence, the result indicated in Fig. 2 is consistent.
    Consider the COH example in Fig. 2, and its protocols in Fig. 3. Initially,
we have L0x (0) = L1x (0) = ŝ0,0 x    and L0x (1) = L1x (1) = ŝ1,0x . After "x := 1" by
T0 , Lx (0) = sx , π(x) = sx , and τ (x) = {(ŝ0,0
       0         0,1              0,1
                                                          x , s0,1
                                                               x   )}. Next, according to
Readtx , a load operation can access the results represented by both s0,1           x   and
s1,1
 x   . We select s1,1
                  x   , to check whether    the  result indicated   in Fig. 2 is consistent,
and set π(x) = ŝ1,1 x   and τ (x) = {(ŝ0,0     0,1    0,1 1,1
                                            x , sx ), (sx , sx )}. Next, after π(x) has
been reset to ŝx , "x := 2" by T1 leads to L1x (1) = sx1,1 , π(x) = ŝx1,1 , and
                  1,0

τ (x) = {(ŝ0,0   0,1      0,1 1,1      1,0 1,1             + 0,1 1,1
             x , sx ), (sx , sx ), (ŝx , sx )}. As τ (x) (sx , sx ), the next load
                                     1,1
operation can only read from sx , meaning that only "x := 2" by T1 is enabled,
and hence the result in Fig. 2 is inconsistent since it violates read coherence.


4     Relating View-based Protocols to SLR

SLR is a program logic for reasoning about concurrent programs under weak
memory models. Its key feature is its reasoning about relaxed memory accesses
by tracking the reads and writes of the program and the order of observation of
values. Using this information, invalid executions can be shown to be impossible.
    We relate our view-based protocols to the relaxed fragment of the SLR logic
rules, namely the w−rlx, r−rlx and r−rlx∗ rules, which are introduced below4 .
    Besides the standard operators in first order logic and separation logic, the
assertion language of SLR introduces two novel assertions, namely O(l, v, ts)
and W p (l, X). The assertion O(l, v, ts) signifies the observation of value v from
location l at time ts. The timestamp ts is used to order observations where the
timestamps are densely totally ordered.
    The assertion W p (l, X) signifies permission to write to a location l, where X
is a set of pairs (v, ts) where a value v is written at timestamp ts. The fractional
permission p signifies whether the permission is exclusive (i.e., p = 1) or shared
(i.e., 0 < p < 1). This assertion is encoded using the protocols and views. In the
proposed approach, the p is not explicitly encoded, but encoded implicitly by
the protocols. The case where there is only one thread writing, meaning there
is only one protocol with an edge, implies exclusive access, i.e., p = 1. In the
case where multiple threads write, meaning multiple protocols in a local view
can progress, implies shared accesses, i.e., 0 < p < 1.
4
    Details pertaining to other memory orderings such as Rel and Acq assertions and
    modalities are omitted to focus on the relaxed memory ordering.
10         Ö. Şakar et al.



The w−rlx rule. The w − rlx rule in Fig. 6 states that the threads need to
have permission to write to x (i.e., W p (x, X)) and a previously observed value at
time ts (i.e., O(x, −, ts)) where the observed value is irrelevant. Also, ϕ(v) has to
hold, where ϕ is a pure predicate over v. It has to be pure, since relaxed memory
operations cannot by themselves be used for synchronization5 . This predicate
can then be communicated to a thread that observes the written value. After
the write operation, the set of writes X is updated with the newly written pair
(v, ts′ ) where the timestamp ts′ is chosen such that it is strictly larger than the
timestamp ts of the previously observed value.
      SLR uses timestamps in its W and O assertions. The timestamps are used to
record the order of writes and observations, where the concrete timestamps are
irrelevant. For this reason, the view-based protocols do not encode the times-
tamps explicitly, but model the modification order using τ . This relation defines
an order between store operations where there is a concrete order. For example,
the τ relation is used in the PReadx function to only read values that are not
τ -before the most recently observed store operation, i.e., a value is observed
that is not followed by a store operation with a larger timestamp. This is also
used to order the store operations per-thread, using the protocols to define the
program order per-thread, where every edge (s →∗t,x s′ ) defines (s, s′ ) ∈ τ (x)+ .
      The SOS Write rule (in Fig. 5) explains how the local views change when a
value is written to an atomic location. To explain the link with the w−rlx rule,
we must first discuss the encoding of the assertions W p (x, X) and O(x, v, ts).
The set X in the W p (x, X) assertion is conceptually a history of the observed
store operations for location x which are ordered by timestamps. This is in
essence the same concept as τ (x), however encoded differently.
      The set X is updated in the postcondition of the w − rlx rule by adding
(v ′ , ts′ ) to X, where v ′ is the value to write and ts′ is a timestamp that is later
than the most recent observation O(x, −, ts). This corresponds to the update
of local views in the Write-rule, where for the thread t and a reachable state s
(with Vxt (s) = v), the local view is updated, i.e., Ltx [t 7→ s]. Also, π is updated,
i.e., π[x 7→ s], where π(x) corresponds to the store operation associated with
O(x, v, ts). The order between the state of the most recently observed store π(x)
and the state of the current store operation is added to τ (x). This encodes the
coherence property Writes-Ordered in Fig. 7, where the order beforehand was
left undefined and after the store operation, the order is established.
      The O(x, v, ts) assertion is encoded mainly using π, where the most recently
observed store operation is recorded. The order between observations O(x, v, ts)
and O(x, v ′ , ts′ ) is encoded using τ (x), where for two states s and s′ with Vx (s) =
v and Vx (s′ ) = v ′ , if ts < ts′ , then (s, s′ ) ∈ τ (x).
The r−rlx and r−rlx∗ rules. The r −rlx rule in Fig. 8 states that a thread
again needs a previously observed value at time ts (i.e., O(x, −, ts)). After read-
5
     In SLR’s release/acquire fragment, ϕ is used for resource sharing, since release/ac-
     quire semantics can be used for synchronization. This work focuses on SLR’s relaxed
     fragment, so the encoding of ϕ is not shown to focus on the W and O assertions.
                             Deductive Verification of Weak Memory Programs                11


            W p (x, X) ∗ (−, ts)∈X ∗ (−, ts′ )∈X ⇒
               W p (x, X) ∗ (ts < ts′ ∨ ts = ts′ ∨ ts′ < ts)                (Writes-Ordered)

            W 1 (x, X) ∗ O(x, v, ts) ⇒
               W 1 (x, X) ∗ O(x, v, ts) ∗ (v, ts′ ) ∈ X                   (Reads-from-Write)
               p                             ′   ′                ′
            W (x, X) ∗ (v, ts) ∈ X ∗ (v , ts ) ∈ X ∗ v ̸= v           ⇒
                   p                 ′
               W (x, X) ∗ ts ̸= ts                                          (Different-Writes)

                            Fig. 7: The coherence properties

      ⊢{ O(x, −, ts) } r := x { ∃ts′ ≥ ts. O(x, v, ts′ ) ∗ r = v ∗ ϕ(v) }            (r−rlx)

      ⊢{ W 1 (x, X) }
         r := x
       { ∃ts. (v, ts) = max(X) ∗ W 1 (x, X) ∗ r = v ∗ O(x, v, ts) ∗ ϕ(v)}           (r−rlx∗ )


                          Fig. 8: The r−rlx and r−rlx∗ rules



ing from x, the value v is observed at a timestamp ts′ > ts, and the predicate
ϕ(v) can be established (dually from the w−rlx rule).
    In the Read-rule (in Fig. 5), the state s is observed and the local view con-
sequently updated, i.e., Ltx [t′ 7→ s], along with π and τ (x). Remember that the
local view represents the most recently observed store operation of each thread,
which implies that if state s is the result of the load operation, then the local
view has observed a thread writing the value associated with s. This encodes
the Reads-from-Write property in Fig. 7, since the result of the load operation
must have the associated store operation in the local view. The property Reads-
from-Write states that an observation (i.e. a read) of value v at time ts implies
that there is a write before where v has been written to x at time ts′ < ts.
    When a thread has exclusive write permission, more conclusions can be drawn
from an observation, expressed in the r −rlx∗ rule. Before the load operation,
exclusive write permission is required (i.e., W 1 (x, X)). Afterwards, again, the
observation of value v is made at time ts and the predicate ϕ(v) can be estab-
lished. Moreover, since the write permission is exclusive, it is established that
the value v with timestamp ts is the maximum value of X, i.e., the latest write.
    The encoding of this rule is subtle. The Read rule returns a value associated
                                                     ′
with state s, where s ∈ Readtx (L, π, τ ) ∩ Sxt . The PRead function (which is called
by the Read rule) returns the set of possibly observable states where the state s
is in the set iff Ltx (t′ ) →∗t′ ,x s, i.e., it is reachable from the current thread-local
view. If there is only one writing thread t, i.e., one protocol Pxt , the conclusion
can be drawn that the only reachable state is in Pxt . If thread t then performs
a load operation, it can conclude that the result stems from the most recent
12      Ö. Şakar et al.

store of itself, which is equivalent to the maximum of the set X. If there are
multiple writers, this cannot be deduced as with the r−rlx rule.

Coherence. SLR allows to reason about coherence with the rules Reads-from-
Write, Writes-Ordered and Different-Writes. The first two rules were mentioned
above. The property Different-Writes in Fig. 7 is captured by the protocols.
The protocol states represent store operations by different threads, even if two
threads write the same value. SLR defines this using the written values, where
given the assertion W p (x, X), two store operations in the set X with differ-
ent values happen at different times. The protocol states make this explicit by
associating distinct states with both store operations. This property is main-
tained by the Write-rule by tracking the latest observed store operation π(x)
and establishing the order of the current store operation and π(x).

Soundness. Soundness in this context of this work means that if a program
encoded using the view-based protocols verifies, then the program also verifies
with the SLR logic. The argument is made as follows:

1. For the program verification state ⟨L, π, τ ⟩, it initially holds that π(x) = ŝx ,
                            ′
   ∀t,t′ ∈T Ltx (t′ ) = ŝtx , and τ is undefined. This corresponds with SLR’s initial
                  ∧



   W (x, X) where X = {(ŝx , 0)}.
2. For a thread t and location x, the SOS Write rule updates the program state
   by 1) L[(t, x) 7→ Ltx [t 7→ s]], updating the view to point to the next state s
   that corresponds with the store operation and 2) τ [x 7→ τ (x) ∪ {(π(x), s)}],
   establishing the order between the most recently observed write operation
   and s. This corresponds to the addition of the pair (v, ts′ ) to the set X in
   SLR’s W assertion, i.e, W (x, {(v, ts′ )} ∪ X) where Vxt (s) = v and ts′ > ts.
3. For a thread t and location x, the SOS Read rule updates Ltx [t′ 7→ s], where
   s is a state representing a possibly observable write operation (of thread t′ ).
   The order of the previously observed operation π(x) and s is added to the τ
   relation. This corresponds to the O(x, v, ts′ ) assertion in SLR’s r −rlx and
   r−rlx∗ rules, where ts′ > ts corresponding to the update to τ .
   The case where there is only one writing thread, i.e., one protocol, the set
                               ′
   Readtx (L, π, τ ) ∩ Sxt from which s is chosen, is limited to the states of the
   writing protocol. This corresponds to the additional postcondition in the
   r−rlx∗ rule where (v, ts) = max(X).
4. From an initial program state ⟨L, π, τ ⟩ and corresponding W (x, X) and
   O(x, −, ts) assertions, we can repeated apply the SOS rules and SLR rules to
   end up in a final program state ⟨L′ , π ′ , τ ′ ⟩. Throughout the application of the
   rules, we can maintain a correspondence between ⟨L, π, τ ⟩ and the W (x, X)
   and O(x, −, ts) assertions, as explained above. From this we conclude that if
   the final program state ⟨L′ , π ′ , τ ′ ⟩ is reached, the W (x, X ′ ) and O(x, −, ts′ )
   assertions are updated accordingly, implying that if a program verifies with
   the view-based protocols approach, then also the program verifies with the
   SLR logic. Thus, we conclude that our approach is sounds w.r.t. SLR.
                           Deductive Verification of Weak Memory Programs          13

 1   adt ps {
 2     pure ps sx0(int t); // State definitions
 3     pure ps sx1(int t);
 4     ... // ∀ states
 5     pure V val(ps s);
 6     axiom val(sx0(0)) == a && val(sx1(0)) == b && ...; // ∀ states
           with concrete a and b
 7     pure boolean isF(int t, ps s);
 8     axiom isF(0, s) == (s == sx1(0)) && .. ; // ∀ threads
 9     pure ps next(V val, ps s);
10     pure int intra(ps s);
11     axiom next(b, sx0(0)) == sx1(0) && ...; // ∀ transitions
12     axiom (∀ int i, ps s; intra(s) < intra(next(i, s))); }


                   Fig. 9: Skeleton code for a protocol encoding.



5    Encoding Protocols and Views into VerCors-relaxed

In this section, we explain parts of the encoding of the protocols and thread-
local views into VerCors-relaxed. For presentation purposes, we omit the contract
template for parallel programs (see Appendix A). Furthermore, we leave out the
encoding for τ in the method contracts for load and store, addressing the SOS
Read and Write rules, respectively.
    Protocols are encoded using VerCors’ ADTs (axiomatic data types). The
states and transitions of the protocols are defined axiomatically because VerCors’
ADT support allows the modeling of abstract concepts, similar to how (concrete)
lists are modeled as an abstract ordered collection. The ADT consists of three
elements: a type name, abstract functions and axioms.
    Fig. 9 shows skeleton code of the ADT encoding named ps (for protocol
states, l.1). This introduces the ps type. For a given protocol Pxt , and for each
state in Sxt , a unique abstract function is defined (l.2–4) that acts as the con-
structor for that state, with a thread identifier the state belongs to. Vxt is encoded
as a function val (l.5). For each state, the associated value is defined (l.6). The
accepting states Fxt are encoded as a function isF, taking a thread identifier
and a state (l.7). At (l.8), the accepting states in Fxt are defined, e.g., sx1(0) is
accepting for thread t. For all states in Fxt , the result of isF is defined. For the
other states, the result is undefined, resulting in a failing verification.
    Finally, →t,x is encoded using two functions. First, the next function (l.9)
takes a state and a value and returns the next state. Each transition is defined
at l.11, e.g., the next state of sx0(0) is sx1(0) when writing the value b.
    The intra function (l.10) defines a mapping of states to integers, used to
define the partial order between states. For each state s, the intra-value of any
next state of s is greater than the intra-value of s. Note that since the next
function is not total, the result of intra is also not total.
14       Ö. Şakar et al.

 1   class a_V {
 2     ps[] G;
 3     seq<ps>[] L;
 4     /*@ ensures Perm(G[*], write) ** Perm(L[*], write);
 5         ensures (∀ int t1,t2=0..N; L[t1][t2] == s0(t2));
 6         ensures (∀* int t1=0..N; G[t1] == s0(t1)); @*/
 7     constructor(int N); }


                      Fig. 10: The contract of the constructor.


 1   /*@ given seq<ps> oldLV;
 2      yields seq<ps> newLV;
 3      given int N, t;
 4      given ps prevPi;
 5      yields ps nextPi;
 6    1)context Perm(G[*], 1\2);
 7      ensures (∀* int t1=0..N; G[t1] == \old(G[t1]));
 8    2)ensures newLV[t] == \old(oldLV[t]);
 9      requires (∀ int t1,t2=0..N; intra(oldLV[t1][t2]) <= intra(G[t2])
10                               || intra(G[t2]) <= intra(oldLV[t1][t2])));
11      ensures(∀ int t1,t2=0..N; intra(newLV[t1][t2]) <= intra(G[t2])
12                            || intra(G[t2]) <= intra(newLV[t1][t2])));
13      ensures (∀ int t1=0..N; intra(oldLV[t1]) <= intra(newLV[t1]));
14    3)ensures \result \in Read(newLV) && ps.val(nextPi) == \result;
15      ensures (prevPi != nextPi) ==> ps.tau(prevPi, nextPi);@*/
16   int load();


                     Fig. 11: The contract of the load method.



    Figs. 10 to 12 shows contracts for the atomic methods. Here, a global view
G is used, which is an array of ps, where ∀t ∈ T.L[t][t] = G[t]. G is used as
a shorthand to simplify notation. The atomic location is represented by a class
a_V (Fig. 10, l.1). The constructor returns the permissions over the global and
local views (l.4) and initializes the global and local views (l.5–6).
    The contract of the load method (Fig. 11) defines the relations between
the local view before the method call, the view after the method call and the
global view. To express these, load takes four ghost arguments (i.e., the given
arguments) and returns two ghost results (i.e., the yields results). These are
specification-only variables that are not part of the program, but help to reason
about the problem. The pre-/postconditions regarding protocol adherence of
the views are omitted due to space limitations. The t and N specify the thread
accessing the atomic location and the number of threads, respectively. The oldLV
and newLV are the local view before and after the load method. The prevPi and
nextPi ghost variables are discussed later.
    The contract of the load method is split into three parts:
                          Deductive Verification of Weak Memory Programs        15

 1   /*@ given int N, t;
 2      given seq<ps> oldLV;
 3      yields seq<ps> newLV;
 4      given ps prevPi;
 5      yields ps nextPi;
 6    1)context Perm(G[t], 1\2) ** Perm(G[t], 1\2);
 7    2)requires ps.val(ps.next(val, oldLV[t])) == val;
 8    3)ensures G[t] == ps.next(val, oldLV[t]);
 9      ensures newLV == oldLV[t -> ps.next(val, oldLV[t])];
10      ensures ps.intra(newLV[t]) <= ps.intra(G[t]);
11    4)ensures \result == val ** ps.val(nextPi) == val;
12      ensures ps.tau(prevPi, nextPi); @*/
13   int store(int val);


                    Fig. 12: The contract of the store method.



 1. Permission annotations: To read from the protocol of a different thread,
    load requires thread read permission to all global views (l.6). A thread
    acquires this permission from a global invariant (at the call site of load). It
    is specified that the global view does not change (l.7), since the load method
    only requires read permission and does not change the global view.
 2. Relation between global view and the local views: First, l.8 specifies
    that the old and new local views of the accessing thread are consistent.
    Next, l.9–12 maintain the invariant between global view and oldLV/newLV,
    respectively. Finally, l.13 specifies how newLV can change w.r.t. oldLV, where
    each state in newLV has to be reachable from the respective state in oldLV.
 3. Relation between local views and the result: The Read function (l.14)
    corresponds to Readtx from Section 3. The set of possible values for newLV
    must contain the returned result corresponding to the value of most recently
    observed state nextPi. The order between the most recently observed state
    nextPi and the previously observed state prevPi is also established (l.15).
    The contract for the store method (Fig. 12) has similar ghost arguments/re-
sults as load, where the load method mainly changes its local view of the
progress of other threads, the store method only records its own progress. The
contract consists of four parts:
 1. Permission annotations: Only write permission is needed to t’s global
    view. Half of the permission comes from a global invariant (at the call site
    of store) and the other half from the thread itself (l.6).
 2. Valid transition: The argument val must be the value of a next state of
    the protocol (l.7).
 3. Update local view and global view: The global view for t is set to the
    next state (l.8), and newLV is copied from oldLV, with newLV[t] changed
    accordingly (l.9). Finally, it is maintained that the global view and new local
    view uphold the partial order without speculations (l.10).
16      Ö. Şakar et al.


Table 1: The average verification times and number of lines for various examples.
Example       Source           #         Avg.     Nr. of      Nr. of Total nr.
                           accesses     Verif.  lines for lines for of lines
                                      Time (s) protocols program
ARM-weak        [23]            6        81.14     206          133        751
   COH      [23],Fig. 2         4        55.52     100          167        480
 COH-c     Based on [23]        4        56.95     100          161        474
 COH-V          [38]            4        49.61     100          160        473
 COH-p1    Based on [38]        4        52.01      95          160        468
 COH-p2    Based on [38]        4        48.30      94          160        467
  COH2     Based on [38]        6        75.52     121          199        533
  COH3     Based on [38]        9        91.68     163          183        559
 CoRR2          [35]            6        75.42     127          143        483
  dCAS        Fig. 16           2        57.16     100          172        619
    LB        [23,38]           4        69.40     143          138        693
    SB        [23,38]           4        69.41     131          130        673
  2+2W      [23],Fig. 2         6        80.88     156          143        711



 4. Relation between local state and result: The relation between the local
    state and result is similar to the same relation in the load method.
A contract of the rmw operation can be proven by combining the contracts for
load and store. Due to space limitations, the section on rmw operations has
been moved to Appendix B.


6    Evaluation

Thirteen examples have been encoded using the approach, showing different
aspects of the encoding. Seven examples have been selected from different papers.
Since this work only focuses on the relaxed memory order, all examples with
only relaxed memory accesses were picked. Five more examples are based on
the examples from the papers. First, COH-c is based on the COH example
from [23], reasoning that both threads read 1 instead of 1 and 2 respectively.
COH2 and COH3 are also based on the COH example, with more accesses and
threads. The examples COH-p1 and COH-p2 are based on COH from [38]. Both
examples show incorrect protocols w.r.t the program, where the first protocol
misses a transition and the second protocol specifies the wrong value to write.
In all the examples, the type for the values V is an integer type.
    The examples, including the executions that are reasoned about, can be found
in Fig. 13. Similar to Fig. 2, the allowed results are shown in blue, while incon-
sistent results are shown in red. The evaluation verifies that the executions (as
described by the comments) are consistent or inconsistent. The cases COH-p1
and COH-p2 use the same program as COH-V, where COH-p1 has a wrong edge
for T0 from value 0 to value 2 and COH-p2 has a protocol state with 3 (instead
of 2). These cases show that the protocol is also checked against the program.
                              Deductive Verification of Weak Memory Programs          17

            (ARM-weak)                         (COH)                       (COHc)
    a := x //1 y := x x := y           x := 1     x := 2           x := 1      x := 2
    x := 1                             a := x //2 b := x //1       a := x //2 b := x //2
         T0       T1    T2                  T0        T1                T0         T1
     (COH-V)                       (COH2)                            (COH3)
x := 1 a := x //2          x := 1      x := 3         x := 1        x := 3       x := 5
x := 2 b := x //1          x := 2      x := 4         x := 2        x := 4       x := 6
                           a := x //3 b := x //2      a := x //3    b := x //5   c := x //2
     T0        T1               T0         T1              T0            T1          T2
                         (CoRR2)                                   (dCAS)
      x := 1   x := 2     a := x //2   c := x //1    rmw(x, 0, 1) //1 rmw(x, 0, 1) //1
                          b := x //1   d := x //2
          T0        T1         T2          T3               T0              T1
                                                                    (2+2W)
                 (LB)                      (SB)
                                                            x := 2      y := 2
          a := x //1 x := y       x := 1      y := 1
                                                            y := 1      x := 1
          y := 1                  a := y //0 b := x //0
                                                            a := y //2 b := x //2
               T0      T1              T0         T1
                                                                 T0         T1

                     Fig. 13: The examples, including their executions



    Table 1 shows the results of VerCors’ verification times, a reference to the
source of the example, the number of load/store accesses, and the number of lines
in the encoding.6 The verification time includes the verification of the protocol
against the program and the reasoning about the consistent and inconsistent
executions as found in Fig. 13. The numbers of lines to formalise the protocols,
the main program, excluding protocols and atomic variables, and the complete
encoding, including the atomic variables are given. The experiments were per-
formed on a MacBook Pro 2020 (macOS 15.7.3) with a 2.0GHz Intel Core i5.
Each experiment was performed ten times, after which the average time of those
executions was recorded. The time has been measured using the time command.
    The verification times for the examples are reasonable, around 1/1.5 minutes.
The examples are of similar size, with between 2 and 9 relaxed loads/stores per
example, which explains the similar verification times. The number of lines for
four protocol states is around 100, e.g., the COH example of which 60 lines is
boilerplate code for the protocol (including newlines and comments). It grows
exponentially with the number of states, due to having to specify that states
are distinct, e.g., the ARM-weak protocol. The number of lines of the examples
depends on the number of atomic accesses and lemmas to help the prover. The
number of lines per atomic variable is common across all examples, which is 203
lines including helper methods and lemmas, except for the dCAS example which
includes the rmw method, where the atomic variable encoding requires 333 lines.

6
    The encodings of the examples can be found at [32]
18      Ö. Şakar et al.

7    Related Work
There are numerous memory models that define different semantics for weak
atomics and fences. The most notable is the C11/C++11 memory model, which
can be translated into hardware memory models. Variants have been made to
improve C11, such as RC11 [25], RC20 [29] and the ’promising’ semantics [23,27].
     The research around weak memory is mainly centered around program logics
and semantics that express weak atomics and fences of different weak mem-
ory models. These program logics extend and build on top of each other. RSL
(Relaxed Separation Logic) [39] is an extension of CSL (Concurrent Separation
Logic) to reason about programs under the C11 memory model. FSL (Fenced
Separation Logic) and FSL++ [16,17] extend RSL with fence support. GPS
(Ghost state, Protocols, and Separation) [36] uses per-location protocols. Basic
coherence properties can be established using these protocols [38]. GPS+ [20]
and GPS++ [19] extend GPS with support for fences. SLR [35] is a separation
logic for the memory model using a ‘promising’ semantics [23]. SLR integrates
the different features from RSL (and extensions) and GPS (and extensions) to
tackle programs under weak-memory while avoiding out-of-thin-air values. Most
of these logics have been formalized in Rocq and their soundness has been proven.
Our approach differs from the approach with Rocq mainly in the automization
of proofs where the proofs with the logics are manual.
     Weak-memory reasoning by means of static analysis has been considered nu-
merous times, e.g. [3,4,5,14,18,26,34]. While this is suitable to approximate which
executions are inconsistent, they do not address the subsequent verification of
consistent executions. Our approach allows verifying that methods adhere to
their contracts, considering all consistent executions.
     Model checking has also been used to verify programs w.r.t. weak memory
models [1,2,9,12,15,22,24,28,31]. Compared to deductive verification approaches,
they do not allow modular verification, and are focussed on verifying temporal
logic formulae, as opposed to pre- and postcondition contracts.
     There are also works on encoding weak memory reasoning in a deductive ver-
ifier. Jacobs encoded the TSO memory model in the VeriFast tool [21]. Summers
and Müller [33] encoded large fractions of RSL, FSL and FSL++ in Viper [30].
With Viper, they reason about programs under the C11 model automatically.
Both the VeriFast and Viper approaches use a tool that employs separation
logic, but they encode different memory models. Summers and Müller left the
encoding of GPS as future work, which is required to encode coherence prop-
erties. However, per-location coherence, or SC-per-location, i.e., the fact that all
threads observe the writes to a specific location in a single total order, can-
not explicitly be reasoned about with the logics they support. Our approach is
mainly different from this by the fact that it uses view-based protocols to encode
coherence properties and support write speculations.
     VerCors has support for SC atomics. The work of Amighi [7,6] explains how
protocols and state invariants allow for transference. Amighi describes the gen-
eral contracts for the load, store and read-modify-write operations on SC atom-
ics. The current work extends the support for atomics by encoding the behavior
                            Deductive Verification of Weak Memory Programs            19

of relaxed memory accesses and introduces per-thread protocols and more gran-
ular local views to allow reasoning about coherence properties.


8    Conclusion

We presented an approach to verify weak memory programs using view-based
protocols in VerCors-relaxed. The approach allows us to reason about execu-
tions of programs, with support for speculative reads using view-based protocols
in VerCors-relaxed. We discussed how SLR program logic is encoded using the
view-based protocols and verified examples using VerCors-relaxed. Future work
involves generating protocol encodings of more examples, since the current proto-
col generation is tailored towards the set of examples. Other future work involves
investigating the scalability of this method to larger programs, adding support
for release/acquire fences, and targeting other weak memory models.


Data Availability. An artifact containing our implementation, our test cases,
and scripts that reproduce our experiments and the results presented in Section 6
is archived and available at [32].


References
 1. Abdulla, P.A., Atig, M.F., Chen, Y.F., Leonardsson, C., Rezine, A.: Memorax,
    a precise and sound tool for automatic fence insertion under TSO. In: TACAS.
    LNCS, vol. 7795, pp. 530–536. Springer (2013)
 2. Abdulla, P.A., Atig, M.F., Ngo, T.P.: The best of both worlds: Trading efficiency
    and optimality in fence insertion for TSO. In: ESOP. LNCS, vol. 9032, pp. 308–332.
    Springer (2015)
 3. Alglave, J., Kroening, D., Nimal, V., Poetzl, D.: Don’t sit on the fence: a static
    analysis approach to automatic fence insertion. ACM Trans. on Progr. Lang. and
    Syst. 39(2), 6 (2017)
 4. Alglave, J., Maranget, L.: Stability in weak memory models. In: CAV. LNCS,
    vol. 6806, pp. 50–66. Springer (2011)
 5. Alglave, J., Maranget, L., Sarkar, S., Sewell, P.: Fences in weak memory models.
    In: CAV. LNCS, vol. 6174, pp. 258–272. Springer (2010)
 6. Amighi, A.: Specification and verification of synchronisation classes in Java: A
    practical approach. Ph.D. thesis, University of Twente (2018). https://doi.org/
    10.3990/1.9789036544399, chapter 5 - Verification of Synchronisers: Exclusive
    Access
 7. Amighi, A., Blom, S., Huisman, M.: Resource protection using atomics: Patterns
    and verification. In: Asian Symposium on Programming Languages and Systems.
    pp. 255–274. Springer (2014)
 8. Armborst, L., Bos, P., van den Haak, L.B., Huisman, M., Rubbens, R., Şakar, Ö.,
    Tasche, P.: The VerCors Verifier: A Progress Report. In: CAV. LNCS, vol. 14682,
    pp. 3–18. Springer (2024)
 9. Atig, M.F., Bouajjani, A., Parlato, G.: Getting rid of store-buffers in TSO analysis.
    In: CAV. LNCS, vol. 6806, pp. 99–115. Springer (2011)
20      Ö. Şakar et al.

10. Berdine, J., Calcagno, C., O’Hearn, P.: Smallfoot: Modular Automatic Asser-
    tion Checking with Separation Logic. In: de Boer, F., Bonsangue, M., Graf, S.,
    de Roever, W. (eds.) FMCO. LNCS, vol. 4111, pp. 115–137. Springer (2005)
11. Bornat, R., Calcagno, C., O’Hearn, P., Parkinson, M.: Permission accounting in
    separation logic. In: Proceedings of the 32nd ACM SIGPLAN-SIGACT Symposium
    on Principles of programming languages. pp. 259–270 (2005). https://doi.org/
    10.1145/1040305.1040327
12. Bouajjani, A., Derevenetc, E., Meyer, R.: Checking and enforcing robustness
    against TSO. In: ESOP. LNCS, vol. 7792, pp. 533–553. Springer (2013)
13. Boyland, J.: Checking Interference with Fractional Permissions. In: Cousot, R.
    (ed.) SAS. LNCS, vol. 2694, pp. 55–72. Springer (2003). https://doi.org/10.
    1007/3-540-44898-5_4
14. Burckhardt, S., Musuvathi, M.: Effective program verification for relaxed memory
    models. In: CAV. LNCS, vol. 5123, pp. 107–120. Springer (2008)
15. Chakraborty, S., Krishna, S., Pavlogiannis, A., Tuppe, O.: GPUMC: A Stateless
    Model Checker for GPU Weak Memory Concurrency. In: CAV. LNCS, vol. 15933,
    pp. 321–346. Springer (2025)
16. Doko, M., Vafeiadis, V.: A program logic for c11 memory fences. In: International
    Conference on Verification, Model Checking, and Abstract Interpretation. pp. 413–
    430. Springer (2015)
17. Doko, M., Vafeiadis, V.: Tackling real-life relaxed concurrency with FSL++. In:
    Programming Languages and Systems: 26th European Symposium on Program-
    ming, ESOP 2017, Held as Part of the European Joint Conferences on Theory and
    Practice of Software, ETAPS 2017, Uppsala, Sweden, April 22–29, 2017, Proceed-
    ings 26. pp. 448–475. Springer (2017)
18. Fang, X., Lee, J., Midkiff, S.: Automatic fence insertion for shared memory multi-
    processing. In: ICS. pp. 285–294. ACM Press (2003)
19. He, M., Qin, S., Xu, Z.: A Program Logic for Reasoning About C11 Programs With
    Release-Sequences. IEEE Access 8, 173874–173903 (2020). https://doi.org/10.
    1109/ACCESS.2020.3024681
20. He, M., Vafeiadis, V., Qin, S., Ferreira, J.F.: GPS+: Reasoning about fences and
    relaxed atomics. International Journal of Parallel Programming 46(6), 1157–1183
    (2018)
21. Jacobs, B.: Verifying tso programs. CW Reports (2014)
22. Jonsson, B.: State-space exploration for concurrent algorithms under weak memory
    orderings. ACM SIGARCH Computer Architecture News 36, 65–71 (2009)
23. Kang, J., Hur, C.K., Lahav, O., Vafeiadis, V., Dreyer, D.: A promising semantics
    for relaxed-memory concurrency. ACM SIGPLAN Notices 52(1), 175–189 (2017)
24. Kuperstein, M., Vechev, M., Yahav, E.: Partial-coherence abstractions for relaxed
    memory models. In: PLDI. pp. 187–198. ACM Press (2011)
25. Lahav, O., Vafeiadis, V., Kang, J., Hur, C.K., Dreyer, D.: Repairing sequential
    consistency in c/c++ 11. ACM SIGPLAN Notices 52(6), 618–632 (2017)
26. Lee, J., Padua, D.: Hiding relaxed memory consistency with a compiler. IEEE
    Trans. Comput. 50, 824–833 (2001)
27. Lee, S.H., Cho, M., Podkopaev, A., Chakraborty, S., Hur, C.K., Lahav, O.,
    Vafeiadis, V.: Promising 2.0: global optimizations in relaxed memory concurrency.
    In: Proceedings of the 41st ACM SIGPLAN Conference on Programming Language
    Design and Implementation. pp. 362–376. PLDI 2020, Association for Comput-
    ing Machinery, New York, NY, USA (2020). https://doi.org/10.1145/3385412.
    3386010, https://doi.org/10.1145/3385412.3386010
                           Deductive Verification of Weak Memory Programs            21

28. Linden, A., Wolper, P.: A verification-based approach to memory fence insertion in
    PSO memory systems. In: TACAS. LNCS, vol. 7795, pp. 339–353. Springer (2013)
29. Margalit, R., Lahav, O.: Verifying observational robustness against a c11-style
    memory model. Proc. ACM Program. Lang. 5(POPL) (Jan 2021). https://doi.
    org/10.1145/3434285, https://doi.org/10.1145/3434285
30. Müller, P., Schwerhoff, M., Summers, A.: Viper - a verification infrastructure for
    permission-based reasoning. In: Jobstmann, B., Leino, K.R.M. (eds.) Verification,
    Model Checking, and Abstract Interpretation. VMCAI. Springer Berlin Heidelberg
    (2016). https://doi.org/10.1007/978-3-662-49122-5_2
31. de Putter, S., Wijs, A.: Lock and Fence When Needed: State Space Exploration +
    Static Analysis = Improved Fence and Lock Insertion. In: iFM. LNCS, vol. 12546,
    pp. 297–317. Springer (2020)
32. Şakar, Ö., Chakraborty, S., Huisman, M., Wijs, A.: Artifact for the paper: De-
    ductive verification of weak memory programs with view-based protocols (2026).
    https://doi.org/10.4121/cd7ac73c-883e-4340-8425-35b4faa00146
33. Summers, A.J., Müller, P.: Automating deductive verification for weak-memory
    programs (extended version). International Journal on Software Tools for Technol-
    ogy Transfer 22(6), 709–728 (2020)
34. Sura, Z., Fang, X., Wong, C.L., Midkiff, S., Lee, J., Padua, D.: Compiler techniques
    for high performance sequentially consistent Java programs. In: PPOPP. pp. 2–13.
    ACM Press (2005)
35. Svendsen, K., Pichon-Pharabod, J., Doko, M., Lahav, O., Vafeiadis, V.: A sep-
    aration logic for a promising semantics. In: Ahmed, A. (ed.) Programming Lan-
    guages and Systems - 27th European Symposium on Programming, ESOP 2018,
    Held as Part of the European Joint Conferences on Theory and Practice of
    Software, ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings.
    Lecture Notes in Computer Science, vol. 10801, pp. 357–384. Springer (2018).
    https://doi.org/10.1007/978-3-319-89884-1_13, https://doi.org/10.1007/
    978-3-319-89884-1_13
36. Turon, A., Vafeiadis, V., Dreyer, D.: GPS: navigating weak memory with
    ghosts, protocols, and separation. SIGPLAN Not. 49(10), 691–707 (Oct
    2014). https://doi.org/10.1145/2714064.2660243, https://doi.org/10.1145/
    2714064.2660243
37. Vafeiadis, V.: Concurrent separation logic and operational seman-
    tics. Electronic Notes in Theoretical Computer Science 276, 335–351
    (2011).       https://doi.org/https://doi.org/10.1016/j.entcs.2011.09.029,
    https://www.sciencedirect.com/science/article/pii/S1571066111001204,
    twenty-seventh Conference on the Mathematical Foundations of Programming
    Semantics (MFPS XXVII)
38. Vafeiadis, V.: Program verification under weak memory consistency using separa-
    tion logic. In: Majumdar, R., Kunčak, V. (eds.) Computer Aided Verification. pp.
    30–46. Springer International Publishing, Cham (2017)
39. Vafeiadis, V., Narayan, C.: Relaxed separation logic: A program logic for c11 con-
    currency. In: Proceedings of the 2013 ACM SIGPLAN international conference
    on Object oriented programming systems languages & applications. pp. 867–884
    (2013)
22       Ö. Şakar et al.

 1   a_V x = new a_V(N);
 2   invariant inv( /*@ Global invariant
 3     Perm(x.G[*], 1\2) **
 4     Perm(x.L[*], 1\2) **
 5     (∀ int t1, t2=0..N; intra(x.L[t1][t2]) <= intra(x.G[t2]) ||
 6              intra(x.G[t2]) <= intra(x.L[t][t2])) @*/) {
 7     par (int t=0..N) // Thread contract
 8     /*@ context Perm(x.G[t], 1\2) ** Perm(x.L[t], 1\2);
 9         context x.G[t] == x.L[t][t];
10         requires x.G[t] == s0(t);
11         requires (∀ int t1; x.L[t][t1] == sx0(t);
12         ensures isF(t, x.G[t]); @*/
13     {/* body */}
14   }
15   if (!∀ int t1, t2=0..N; intra(x.L[t1][t2]) <= intra(x.G[t2]))
16     {/*exclude inconsistent views*/}


        Fig. 14: General template for using relaxed atomics on a location x.



A     General contract for parallel programs with atomics

    With protocols defined (see Fig. 9) we continue with the encoding of the
local views and an (atomic) invariant. Fig. 14 shows the general structure of a
parallel program with atomics. Note that some parts of the invariant are omitted
for readability, such as null checks and arrays lengths.
    The atomic location x (l.1) is an instance of the class a_V. The class has
four methods, namely the constructor, load, store, and rmw. The contracts
of these methods are in Section 5. The class a_V has two fields L and G. The
field L contains the (thread-)local views, which is an array of sequences (i.e.,
an immutable list) of ps where ∀t ∈ T. L[t] = Ltx . The encoding introduces a
global view G. This view is an array of ps, where ∀t ∈ T.L[t][t] = G[t], i.e.,
the global view is consistent with every thread’s view of its protocol state. G is
used as a shorthand to ease verification, with the relation between G and L being
maintained throughout the program (e.g., at l.9).
    The invariant has two main parts. Firstly, using fractional permissions, we
keep half of the permissions to each location of G and L in the invariant inv (3
and 4). Keeping half permission in the invariant allows any thread to (atomically)
read from the view of another thread. The other half of the permissions is given
to the individual threads (l.8). This allows every thread t to update its view
x.L[t] when reading or writing. Secondly, the relation between the views of all
threads is expressed, where either thread t has speculated about the writing of
thread t1 (l.6) or not (l.5), encoding condition CC2 mentioned in Section 3.
    The contract of threads is structured as follows. The global view is in the
initial state (l.10) and all protocols in the local view are also in their initial states
                              Deductive Verification of Weak Memory Programs                23

                                                       ′           w                 ′
               t, t′ ∈ T     s ∈ Readtx (L, π, τ ) ∩ Sxt           →t,x s′
                                                           Ltx (t) −         w′ = Vxt (s)
    (RMW-S)
                                            ⟨
                                             L[(t, x) 7→ Ltx [t′ 7→ s][t 7→ s′ ]],
                                       ′
                                rmw(x,w ,w)  π[x 7→ s′ ],
                  ⟨L, π, τ, σ⟩ −−−−−−−→t,x
                                             τ [x 7→ τ (x) ∪ {(π(x), s), (s, s′ )},
                                             σ[s 7→ σ(s)+1]
                                            ⟩
                                                               ′       ′
                              t, t′ ∈ T   s ∈ Readtx (L) ∩ Sxt     Vxt (s) ̸= v
           (RMW-F)
                                                   ⟨
                                                    L[(t, x) 7→ Ltx [t′ 7→ s]],
                                        rmw(x,v,_)  π[x 7→ s],
                           ⟨L, π, τ, σ⟩ −−−−−−→
                                                    τ [x 7→ τ (x) ∪ {(π(x), s)}],
                                                    σ
                                                   ⟩

Fig. 15: Operational semantics for protocol views with successful and unsuccessful rmw
operations.



(l.11). Finally, all threads ensure their global view ends up in an accepting state
(l.12), encoding condition CC1 mentioned in Section 3.
    After the parallel block, a case distinction is made (l.16). In the end, a view
is consistent iff there are no speculations anymore, i.e., the property in l.5 holds.
We only reason about consistent non-speculating views, otherwise the state is
discarded.


B    Read-Modify-Write

With the operational semantics for load and store operations in Section 3, we
can define operational semantics for rmw operations. A case distinction is made
between a successful and unsuccessful rmw operation. A successful rmw operation
reads the result of some load operation, followed by a store operation, putting
a new constraint on an execution: no other rmw operation may read the result of
the same store operation, i.e., atomicity of the rmw operation.
     In the operational semantics, this constraint is formalized by keeping track of
a multiset σ of states from which rmw operations have read values. We interpret
this multiset as a function σ : S → N, with N the domain of natural numbers.
     Fig. 15 presents the SOS rules RMW-S and RMW-F, respectively for suc-
cessful and unsuccessful rmw operations. Essentially, these are combinations of
the SOS rules for store and load. The only difference is that the verification
states have been extended with σ, and after execution of rmw (x,w’,w), σ has
been updated to σ[s 7→ σ(s)+1], i.e., s has been added to the multiset σ where
Vxt (s) = w′ . In the rule RMW-F, σ is not updated. The Write and Read rules
should now also be interpreted with σ being part of verification states, but it
plays no role there.
24        Ö. Şakar et al.



         rmw (x, 0, 1)   rmw (x, 0, 1)
                 T0       T1



 Fig. 16: An example program with rmw operations (left) and its protocols (right).



    Once the verification procedure for a program with rmw operations has fin-
ished, the final consistency check involves two more conditions.

                               ∀s ∈ S.σ(s) = 0 ∨ σ(s) = 1                        (CC3)

     ∀x ∈ A, s, s′ ∈ Sx .(s ̸= s′ ∧ σ(s) = σ(s′ ) = 1) =⇒ s ̸∈ Ŝx ∨ s′ ̸∈ Ŝx   (CC4)
    CC3 expresses that every state occurs at most once in σ. If a state would
occur more than once, this would mean that multiple rmw operations have read
the result of the store operation, violating atomicity. CC4 addresses the special
case for initial states: for every x ∈ A, no two distinct states in σ may be both
initial, otherwise, again, atomicity would be violated.

Example 1. Consider the example program and its protocols in Fig. 16. Since
both rmw operations expect to read the same value, and since they both write a
value different from that value in case of success, exactly one of the instructions
should succeed. Initially, we have L0x (0) = L1x (0) = ŝ0,0           0         1
                                                             x and Lx (1) = Lx (1) =
  1,0                                                     0          0,0 1,0 1,1
ŝx . First, for T0 , rmw(x, 0, 1) is can succeed, as Readx (L) = {ŝx , ŝx , sx }. For
this, we can either select ŝ0,0        1,0
                               x or ŝx , update π and τ accordingly, and add one
of those states to σ. Let us add ŝ0,0                          1,0
                                         x to σ, the case for ŝx is similar. Next, if
we consider the rmw instruction of T1 , we have to conclude that only the failing
rmw(x, 0, 1) is possible; for a rmw operation, we would again have to select either
ŝ0,0    1,0                                0,0
  x or ŝx . In the case that we add ŝx to σ, CC3 is violated, and in the case
                 1,0
that we add ŝx to σ, CC4 is violated. Symmetrically, T0 can execute a failing
rmw(x, 0, 1), in which case T1 can execute a successful rmw(x, 0, 1). The case
that neither rmw instructions succeeds is ruled out as it would involve invalid
speculations: if T0 ’s rmw(0, x, 0) operation fails, then after the execution, we
must have L0x (1) = s1,1  x . Similarly, for T1 , execution of rmw(x, 0, 1) leads to
L1x (0) = s0,1
           x   . However,  in that case, CC2 is violated.


B.1     Encoding into VerCors

Fig. 17 shows the contract for the rmw method. The contract of the rmw operation
is a combination of the contracts for load and store. With the contracts for the
abstract load and store methods, the implementation of the rmw method can be
verified. For brevity, parts of the rmw’s contract overlapping with the contracts
of load and store are omitted to focus on the differences. The contract mainly
consists of two parts:
                          Deductive Verification of Weak Memory Programs        25

 1   /*@ given seq<ps> oldLV;
 2     yields seq<ps> newLV;
 3     given int N, tid, depTid, prev;
 4     yields int next;
 5   1)ensures !\result ==> G[tid] == \old(G[tid]);
 6     ensures !\result ==> next != oldVal;
 7     ensures !\result ==> descriptionFail(newLV);
 8   2)ensures \result == G[tid] == ps.next(oldLV[tid]);
 9     ensures \result ==> newLV[tid] == ps.next(oldLV[tid]);
10     ensures \result ==> ps.val(newLV[tid]) == newVal;
11     ensures \result ==> next == newVal;
12     ensures \result ==> next \in Read(newLV);
13     ensures \result ==> CASSuccess(tid,newLV[depTid]);
14     ensures \result ==> descriptionSuccess(newLV);@*/
15   boolean rmw(int oldVal, int newVal) {
16     int c = get() given {...} yields {...};
17     if (c == oldVal) { return true; }
18     return false;
19   }


                     Fig. 17: The contract of the rmw method.



 1. rmw fail: When the operation fails, the global view of t does not change (l.5).
    The call to load updates the local view. The return value of load cannot be
    equivalent to oldVal (l.6). Finally, a description of newLV can be given (l.7).
    The predicate descriptionFail is a placeholder and is to be defined by the
    user to use in further proofs. It can be used to exclude certain executions,
    see Fig. 16.
 2. rmw success: The newLV is specified to have changed similarly to the store
    method’s contract. In addition to this, a token CASSuccess is given to signify
    that the operation has succeeded (l.13). This token captures the state that
    oldVal is read from. The token is used to exclude multiple operations reading
    from the same write. Again, a description of newLV can be given (l.14) with
    the predicate descriptionSuccess.


C     The encoding of the COH example
Fig. 18 shows the PVL encoding of the COH example from Fig. 2. The encoding
of the atomics and some helper methods are omitted for readability.
26               Ö. Şakar et al.


 1   given int N; context_everywhere NBound(N);
 2   void main() {
 3     GSX gx = new GSX(N); assume x() == gx;
 4
 5       invariant inv(/*@
 6         NBound(N) ** gspsx(x(), N) **
 7         // For x
 8         (Perm(x().G[*], 1\2)) **
 9
10           (∀ int t=0..N; ps.N(x().G[t]) == N) **
11           (∀ int t=0..N; padhereX(x().G[t], t, N)) **
12
13           x().L != null **
14           x().L.length == N **
15           (∀* int t=0..N; Perm(x().L[t], 1\2)) **
16           (∀ int t=0..N; |x().L[t]| == N) **
17
18           // G[t] reachable from L[t][t’] or vice versa
19           (∀ int t=0..N, int t1=0..N;
20               // L[t] older value than G[t]                    or L[t] speculates into a future of G[t]
21               ps.intra(x().L[t][t1]) <= ps.intra(x().G[t1]) || ps.intra(x().L[t][t1]) >= ps.intra(x().G[t1])
22           ) **
23
24           // G[t] and L[t][t] always consisntent
25           (∀ int t=0..N; x().L[t][t] == x().G[t]) @*/) {
26           par (int tid=0..N)
27           /*@ context_everywhere NBound(N) ** gspsx(x(), N);
28             // For x
29             context_everywhere Perm(x().L[tid], 1\2) ** |x().L[tid]| == N;
30             requires x().L[tid] == psInitXSeq(N);
31             context_everywhere handle(Px(), tid, x().L[tid]) ** handle(Cx(), tid, x().L[tid]);
32             context_everywhere Perm(x().G[tid], 1\2);
33             context_everywhere x().G[tid] == x().L[tid][tid];
34             context_everywhere (∀ int t=0..N; padhereX(x().L[tid][t], t, N));
35
36               requires x().G[tid] == ps.sx0(tid,N);
37               ensures ps.isF(tid, x().G[tid]); @*/
38           {
39               int lvx=\choose(ReadX(x().L[tid]));
40               lemmaReadXHelperInit(x().L[tid],0,N);
41               assert lvx == 0; // Ghost state, initial l(ocal)v(iew)
42               int wx=tid;
43               ps lsx=x().L[tid][wx];
44
45               if (tid == 0) {
46                 atomic(inv) {seq<ps> tmp1;
47                   x().store(1) given {oldLV=x().L[tid],N=N,tid=tid,prev=lvx,prevW=wx,prevPi=lsx}
48                                yields {lvx=next,wx=nextW,lsx=nextPi,tmp1=newLV};
49                   x().L[tid] = tmp1;}
50
51
52                   int a;
53                   atomic(inv) {seq<ps> tmp1;
54                     a = x().load() given {oldLV=x().L[tid],N=N,tid=tid,prev=lvx,prevW=wx,prevPi=lsx}
55                                    yields {lvx=next,wx=nextW,lsx=nextPi,tmp1=newLV};
56                     x().L[tid] = tmp1;}
57
58               } else {
59                 atomic(inv) {seq<ps> tmp1;
60                   x().store(2) given {oldLV=x().L[tid],N=N,tid=tid,prev=lvx,prevW=wx,prevPi=lsx}
61                                yields {lvx=next,wx=nextW,lsx=nextPi,tmp1=newLV};
62                   x().L[tid] = tmp1;}
63
64                   int b;
65                   atomic(inv) {seq<ps> tmp1;
66                     b = x().load() given {oldLV=x().L[tid],N=N,tid=tid,prev=lvx,prevW=wx,prevPi=lsx}
67                                    yields {lvx=next,wx=nextW,lsx=nextPi,tmp1=newLV};
68                     x().L[tid] = tmp1;}
69               }
70           }
71       }
72         // Exclude all inconsistent view, i.e., views with unkept promises.
73       if (!x().consistentL()) {inhale false;}
74       refute false;
75   }



                                  Fig. 18: The encoding of the COH example.
