                                         Owicki-Gries Reasoning for C11 Programs with
                                          Relaxed Dependencies (Extended Version)?

                                                        Daniel Wright1 , Mark Batty1 , and Brijesh Dongol2
                                                                          1
                                                                              University of Kent
                                                                         2
                                                                              University of Surrey
arXiv:2108.01418v1 [cs.LO] 3 Aug 2021




                                                Abstract. Deductive verification techniques for C11 programs have ad-
                                                vanced significantly in recent years with the development of operational
                                                semantics and associated logics for increasingly large fragments of C11.
                                                However, these semantics and logics have been developed in a restricted
                                                setting to avoid the thin-air-read problem. In this paper, we propose an
                                                operational semantics that leverages an intra-thread partial order (called
                                                semantic dependencies) induced by a recently developed denotational
                                                event-structure-based semantics. We prove that our operational seman-
                                                tics is sound and complete with respect to the denotational semantics.
                                                We present an associated logic that generalises a recent Owicki-Gries
                                                framework for RC11 (repaired C11), and demonstrate the use of this
                                                logic over several example proofs.


                                        1     Introduction

                                        Significant advances have now been made on the semantics of (weak) memory
                                        models using a variety of axiomatic (aka declarative), operational and denota-
                                        tional techniques. Several recent works have therefore focussed on logics and
                                        associated verification frameworks for reasoning about program executions over
                                        weak memory models. These include specialised separation logics [9, 11, 15, 26]
                                        and adaptations of classical Owicki-Gries reasoning [7, 17]. At the level of lan-
                                        guages, there has been a particular focus on C11 (the 2011 C/C++ standard).
                                             Due to the complexity of C11 [4], many reasoning techniques have restricted
                                        themselves to particular fragments of the language by only allowing certain
                                        types of memory accesses and/or reordering behaviours. Several works (e.g.,
                                        [7, 10, 15, 17]) assume a memory model that guarantees that program order (aka
                                        sequenced-before order) is maintained [18]. While this restriction makes the log-
                                        ics and proofs of program correctness more manageable, it precludes reasoning
                                        about observable executions displaying certain real-world phenomena, e.g., those
                                        exhibited by the load-buffering litmus test under Power or ARMv7.
                                        ?
                                            We thank Simon Doherty for discussions on an earlier version of this work. Wright
                                            is supported by VeTSS. Batty is supported by EPSRC grants EP/V000470/1 and
                                            EP/R032971/1, and the Royal Academy of Engineering. Dongol is supported by
                                            EPSRC grants EP/V038915/1, EP/R032556/1, EP/R025134/2, VeTSS and ARC
                                            Discovery Grant DP190102142.
2

    Init: x = y = r1 = r2 = 0                       Init: x = y = r1 = r2 = 0
Thread 1            Thread 2                      Thread 1       Thread 2
1: r1 := [x]        3: r2 := [y]                  1: r1 := [x] 3: r2 := [x]
2: [y] := r1+1 4: [x] := 1                        2: [y] := r1 4: [x] := r2
{r1 ∈ {0, 1}}       {r2 ∈ {r1 + 1, 0}}            {r1 = 0}       {r2 = 0}
          {r1 6= 1 ∨ r2 6= 1}                              {r1 = r2 = 0}
Fig. 1. Load-buffering with a seman-             Fig. 2. Load-buffering with two
tic dependency                                   dependencies


Load buffering and the thin air problem. C11 suffers from the out of thin air
problem [5], where the language does not impose any ordering between a read
and the writes that depend on its value. The intention is to universally permit
aggressive compiler optimisation, but in doing so, this accidentally allows writes
to take illogical values. The ARM and Power processors allow the relaxed out-
come r1 = 1 and r2 = 2 in Fig. 1, where there is nothing to enforce the order of
the load and store in the second thread [25]. In Fig. 2, each thread reads and then
writes the value read – a data dependency from read to write. This dependency
makes optimisation impossible, so the relaxed outcome r1 = r2 = 1 is forbidden
on every combination of compiler and target processor. C++ erroneously allows
the outcome r1 = r2 = 1, producing the value 1 “out of thin air”.
    Formally handling load buffering while avoiding out of thin air behaviours
turns out to be an enormously complex task. Although several works [6, 14, 16,
19, 23] have been dedicated to providing semantics for different variations of the
load buffering example, many of these have also been shown to be inconsistent
with expected behaviours under certain litmus tests [13,23]. This work builds on
top of the recent MRD (Modular Relaxed Dependencies) semantics by Paviotti
et al [23]. MRD avoids thin air, and aims for compatibility with the existing ISO
C and C++ standards.
    A key component of MRD is the calculation of a semantic dependency rela-
tion, which describes when certain reorderings are disallowed. The program in
Fig. 1 contains only the semantic dependency between lines 1 and 2, whereas
the program in Fig. 2 contains semantic dependencies between lines 1 and 2, and
lines 3 and 4. The program in Fig. 1 may therefore execute line 4 before line 3,
while the program in Fig. 2 must execute both threads in order.
Contributions. Although precise, there is currently no direct mechanism for rea-
soning about programs under MRD because MRD is a denotational semantics
defined over an event structure [27]. This paper addresses this gap by devel-
oping an operational semantics for MRD, which we then use as a basis for a
deductive Owicki-Gries style verification framework. The key idea of our oper-
ational semantics is to take the semantic dependency relation as the only order
in which programs must be executed, thereby allowing intra-thread reordering.
This changes the fundamental meaning of sequential composition, allowing state-
ments that occur “later” in the program to be executed early.
    Our semantics is also designed to take non multi-copy atomicity into account,
whereby writes are not propagated to all threads at the same time and hence
                                                                                   3

may appear take effect out-of-order [1, 2]. Note that this phenomenon is distinct
from the reordering of operations within a thread (described above), and it is
possible to separate the two. Here, we adapt the operational model of weak
memory effects by Doherty et al [10] so that it follows semantic dependency
rather than the more restrictive thread order used in earlier works [7, 10, 15, 17].
    Finally, we develop a logic capable of reasoning about program executions
that exhibit both of the phenomena described above. Our logic makes use of
the technique by Dalvandi et al [7] of including assertions that enable reasoning
about the “views” of each thread. Since we have concurrent programs, the logic
we develop incorporates Owicki-Gries style reasoning for programs, in which as-
sertions are shown to be both locally correct and globally stable (interference
free). However, unlike earlier works [7,17], since we relax thread order, the stan-
dard approach to Hoare-style proof decomposition is not possible.

Overview. This paper is organised as follows. We recap MRD in Section 2 and
an operational semantics for RC11 in Section 3. Then in Section 4, we present a
combined semantics, where program order in RC11 is replaced by a more relaxed
order defined by MRD. A Hoare-like logic for reasoning about relaxed program
execution together with Owicki-Gries-like rules for reasoning about interference
is given in Section 5. We present an example proof in Section 6.


2   MRD and semantic dependencies
In this section, we review the MRD semantics for a simple C-like while language.
This provides a mechanism for defining (in a denotational manner) a relaxed
order in which statements within a thread are executed, which precludes devel-
opment of a program logic.

Events and actions Weak memory literature uses a variety of terminology to
refer to internal representations of changes to global memory, which complicates
attempts to unify multiple models. In the following, we use events to refer to
the objects created and manipulated by MRD, normally represented as integers.
We use actions to refer to objects of the form i:R x v, i:W x v, referring to a read
or write of value v at global location x arising from line i of the input program.

Program syntax. We assume shared variables x, y, z, . . . from a set X, registers
r1 , r2 , . . . from a set Reg, and register files ρ : Reg → Val mapping registers to
values from a set Val . Expressions e, e1 , e2 , . . . are taken from a set E, whose
syntax we do not specify, but which can be evaluated w.r.t. a register file using
eval ∈ E × (Reg → Val ) → Val . Thus, eval (e, ρ) is the value of e given the reg-
ister values in ρ. For basic commands, we have variable assignments (or stores)
[y] := e and register assignments (or loads) r := [x]. In this paper, we assume
that stores and loads are relaxed [3, 10, 18] unless they are explicitly specified to
be a releasing store (denoted [y] :=R e) or an acquiring load (denoted r :=A [x]).
Finally, we assume a simple language of programs. The only unconventional as-
pect of this language is that we require each (variable or register) assignment be
4

decorated with a unique control label. This allows a semantics which does not,
in general, respect program order to refer to an individual statement without
ambiguity. The syntax of commands (for a single thread) is defined by the fol-
lowing grammar, where B is an expression that evaluates to a boolean and i is
a control label. Note that since guards are expressions, they must not mention
any shared variables — any guard that relies on a shared memory variable must
load its values into a local register prior to evaluating the guard.
    ACom ::= i : skip | i : [x] :=[R] e | i : r :=[A] [x] | i : r := e
     Com ::= ACom | Com; Com | if B then Com else Com | while B do Com
We use [x] :=[R] e to denote that the releasing annotation R is optional (similarly
r :=[A] [x] for the acquiring annotation A). For simplicity, we focus attention
on the core atomic features of C11 necessary to probe the thin-air problem, and
omit more complex instructions such as CAS, fences, non-atomic accesses and
SC accesses [4].
    We assume a top level parallel composition operator. Thus, a program is
of the form C1 kC2 k . . . kCn where Ci ∈ Com. We further assume each atomic
command ACom in the program has a unique label across all threads.

Denotational MRD. For the purposes of this paper (i.e., the development of the
operational semantics and associated program logic), the precise details of the
MRD semantics [23] are unimportant. The most important aspect that we use
is the set of semantic dependency relations that it generates, which precisely
characterise the order in which atomic statements are executed.
    In MRD, the denotation of a program P is returned by the semantic inter-
pretation function JP K. This gives a coherent event structure of the form:

                                      (L, S, `, ≤)
where

    – L = (E, v, #, Lab) is an event structure [27] equipped with a labelling func-
      tion Lab from events (represented internally as integer identifiers) to actions.
      The set E contains all events in the structure, a1 v a2 for a1 , a2 ∈ E iff a1
      is program ordered before a2 . Events in # cannot happen simultaneously,
      e.g., two reads of a variable returning different values are in conflict.
    – S = (A, lk, rf, dp) is a set of partial executions, each of which represents a
      possible interaction of the program with the memory system. Each execu-
      tion in S is a tuple of relations representing lock/unlock order, a reads-from
      relation and dependency order between operations of that execution, and the
      set of events to be executed. An execution is complete if every read in A is
      linked to a write to the same location of the same value by an rf edge.
    – ` is a justification relation used in the construction of the program’s depen-
      dency relation.
    – ≤ is the preserved program order (c.f., [2]), a subset of the program order of
      F that is respected by the memory model.
                                                                                    5

    To develop our operational semantics, we only require some of these compo-
nents. From S, we only require the dependency order. From the labelled event
structure, we use the labelling function Lab to connect actions to events. From
the coherent event structure, we use ≤ to enforce ordering alongside dependency
order.3

Example 1. The event structure in Fig. 3 represents the denotation of the pro-
gram in Fig. 1. Note first that each store of a value into a register generates
multiple events – one for each possible value. This is because MRD cannot make
assertions about which values it may or may not observe during interpretation of
the structure, it can only be provided with global value range restrictions prior
to running. Instead, each read must indicate a write whose value it is observing
during the axiomatic checks, subject to various coherence restrictions. A read
will only appear in a complete execution if it can satisfy this requirement.
    Events 2 and 4 are in conflict (drawn as a red zigzag) as they represent
different potential values being read at line 1. Likewise, events 6, 8, and 10
represent different potential values at line 3. A single execution can observe
events 2 and 6, but not events 2 and 4. Events 2 and 3 are in program order
(represented by the black arrow). MRD generates a dependency order between
events 2 and 3 and events 4 and 5 (represented by the yellow arrow). The read
at line 1 is stored in register r1, which is in turn accessed by the write in line
2, leading to a data dependency. There is no semantic dependency between any
events arising from lines 3 and 4, because there is no way for the value read at
line 3 to influence the value written at line 4. This means that lines 1 and 2 must
be executed in order, but line 4 is free to execute before line 3. For example,
consider the traces H1 and H2 below.

                  H1 = Init 2:W y 1 4:W x 1 1:R x 1 3:R y 1
                  H2 = Init 1:R x 1 4:W x 1 2:W y 1 3:R y 1

For the program in Fig. 1, the trace H1 is disallowed since in H1 , the operations
at lines 2 and 1 are swapped in a manner inconsistent with the dependency order.
The trace H2 is allowed, since lines 3 and 4 are free to execute in any order.


3     Operational semantics with relaxed write propagation

To reason about the relaxed propagation of writes, Doherty et al [10] build
an operational semantics that is equivalent to a declarative (aka axiomatic)
semantics [18], which defines consistency of tagged action graphs. The opera-
tional semantics allows the stepwise construction of such graphs, in contrast to
a declarative approach which only considers complete executions that are either
accepted or rejected by the axioms of the memory model. We do not discuss
3
    MRD also defines a set of axioms that describes when a particular execution is
    consistent with a denotation. We do not discuss these in detail here, but they are
    used in the soundness and completeness proofs.
6




             Fig. 3. Coherent event structure for the program in Fig. 1



the declarative semantics here, focusing instead on the operational model, which
we generalise in Section 4. We also note that like other prior works [15, 17, 18],
the existing operational semantics [10] assumes program order within a thread
is maintained.
    Formally, tagged actions are triples (g, a, t), where g is a tag (uniquely iden-
tifying the action); a is a read or write action (potentially annotated as a
releasing write or acquiring read), and t is a thread (corresponding to the
thread that issued the action). We let TA be the set of all tagged actions,
Wr, WrR , Rd, RdA ⊆ TA be the set of write, releasing write, read and acquir-
ing reads, respectively. Note that Wr is the set of all writes, including those from
WrR (similarly, Rd).
    A tagged action graph is a tuple (D, sb, rf, mo) where D is a set of tagged
actions, which may correspond to read or write actions, and sb, rf and mo are
relations over D. Here, sb is the sequenced before relation, where b1 sb b2 iff
b1 and b2 are tagged actions of the same thread and b1 is executed before b2 .
rf ⊆ Wr × Rd is the reads-from relation [2] relating each write to the read that
reads from that write. Finally, mo ⊆ Wr × Wr denotes modification order (aka
coherence order), which is the order in which writes occur in the system, and
hence the order in which writes must be seen by all threads. Note that if b1 mo b2 ,
then b1 and b2 must act on the same variable. Moreover, mo|x is a total order,
where mo|x is the relation mo restricted to writes of variable x.
    We assume tagged action graphs are initialised with writes corresponding to
the initialisation of the program, and relations sb, rf and mo are initially empty.
    Following Lahav et al [18], the so-called repairing or restricted C11 model
(which is the model in [7, 10, 15]) instantiates sequence-before order to the pro-
gram order relation [2]. This disallows statements within a thread from being
executed out-of-order (although writes may be propagated to other threads in a
relaxed manner). In Section 4, we present an alternative instantiation of sb using
the semantic dependencies generated by MRD to enable out-of-order executions
within a thread can be considered.
    To characterise the operational semantics, we must define three further re-
lations: happens before, denoted hb (which captures a notion of causality); from
read, denoted fr (which relates each read to the write that overwrites the value
read), and extended coherence order, denoted eco (which fixes the order of writes
                                                                                        7

                  b = (g, a, t)      g∈/ tags(D)       a ∈ {i:R x n, i:RA x n}
            σ = (D, sb, rf, mo)      w ∈ OWσ (t)       var (w) = x      wrval (w) = n
    Read
                                      b
                   (D, sb, rf, mo)        (D ∪ {b}, sb +D b, rf ∪ {(w, b)}, mo)

                    b = (g, a, t)   g∈ / tags(D)    a ∈ {i:W x n, i:WR x n}
                      σ = (D, sb, rf, mo)     w ∈ OWσ (t)    var (w) = x
           Write
                                          b
                       (D, sb, rf, mo)        (D ∪ {b}, sb +D b, rf, mo[w, b])

                                  Fig. 4. Memory semantics


and reads). Formally we have:

hb = (sb ∪ (rf ∩ WrR × RdA ))+            fr = (rf −1 ; mo) \ Id    eco = (rf ∪ mo ∪ fr)+

where Id is the identity relation, ; denotes relational composition, and + denotes
transitive closure. Note that there is only a happens-before relation between a
write-read pair related by rf if the write is releasing and the read is acquiring.
   With these basic relations in place, we are now in a position to define the
transition relation governing the operational rules for read and write actions.
The rules themselves are given in Fig. 4. Assuming σ denotes the set of all
tagged action graphs, each transition is a relation       ⊆ Σ × TA × Σ. We write
    b
σ       σ 0 to denote (σ, b, σ 0 ) ∈ .
   To accommodate relaxed propagation of writes, the semantics allows different
threads to have different views of the system, formalised by a set of observable
writes. These are in turn defined in terms of a set of encountered writes, de-
noted EWσ (t), which are the writes that thread t is aware of (either directly or
indirectly) in state σ:

        EWσ (t) = {w ∈ Wr ∩ Dσ | ∃b ∈ Dσ . tid (b) = t ∧ (w, b) ∈ eco?σ ; hb?σ }

Here R? is the reflexive closure of relation R and tid returns the thread identifier
of the given tagged action. Thus, for each w ∈ EWσ (t), there must exist a tagged
action b of thread t such that w is either eco-, hb- or eco; hb-prior to b. From
these we determine the observable writes, which are the writes that thread t can
observe in its next read. These are defined as:

             OWσ (t) = {w ∈ Wr ∩ Dσ | ∀w0 ∈ EWσ (t). (w, w0 ) ∈
                                                              / moσ }

Observable writes are writes that are not succeeded by any encountered write in
modification order, i.e., the thread has not seen another write overwriting the
value being read.
   We now describe each of the rules in Fig. 4. Relations rf and mo are updated
according to the write actions in D that are observable to the thread t executing
the given action. A read action b may read from any write w ∈ OWσ (t). In the
post state, we obtain a new tagged action set D ∪ {b}, sequenced-before relation
8

        n = eval(e, γ(t))           a = i:W[R] x n              a = i:R[A] x n     ρ0 = γ(t)[r := n]
                                    a                                             a
         (i : [x] :=   [R]
                             e, γ) −→t (skip, γ)           (i : r :=[A]
                                                                          [x], ρ) −→t (skip, γ[t := ρ0 ])

                                                                           b = (g, a, t)
                                    a                                    a                         b
                  (P (t), γ) −→t (C, γ 0 )                       (P, γ) −→t (P 0 , γ 0 ) σ                σ0
 Prog                        a
                                                         Full
               (P, γ) −→t (P [t := C], γ 0 )                                       b
                                                                    (P, (σ, γ)) =⇒ (P 0 , (σ 0 , γ 0 ))

                  Fig. 5. Interpreted operational semantics of programs (sample)


sb +D b (defined below) and reads-from relation rf ∪ {(w, b)}. Relation mo is
unmodified. Formally, sb +D b introduces b at the end of sb for thread t:
                        sb +D b = sb ∪ ({b0 ∈ D | tid (b0 ) ∈ {tid (b), 0}} × {b})
Note that we assume that initialisation is carried out by a unique thread with
id 0, and that we require the set D as an input to cope with initialisation where
sb may be empty for the given thread.
    The write rule is similar except that it leaves rf unchanged and updates
mo to mo[w, b]. Given that R[x] is the relational image of x in R, we define
R⇓x = {x} ∪ R−1 [x] to be the set of all elements in R that relate to x (inclusive).
The insertion of a tagged write action b directly after a w in mo is given by
                                 mo[w, b] = mo ∪ (mo⇓w × {b}) ∪ ({b} × mo[w])
Thus, mo[w, b] effectively introduces b immediately after the w in mo.
    The final component of the operational semantics is a set of rules that link the
program syntax in Section 2 with the memory semantics. In prior work, this was
through a set of operational rules that generate the actions associated with each
atomic statement, combined with the rules in Fig. 4 to formalise the evolution
of states. A sample of these rules for reads and writes from memory are given
in Fig. 5. These are then lifted to the level of programs using the rules Prog
                                         b
and Full, where the transition rule =⇒ combines the thread-local semantics
    a                                                b
−→t and global-state semantics          . Note that we model parallel composition
as functions from thread identifiers to commands, thus P [t := C] represents the
program, where the command for thread t is updated to C.
                                                                               a
    The rules in [10] generate actions corresponding to program syntax (i.e., −→t )
in program order.4 In this paper, we follow a different approach — the actions
will be generated by (and executed in) the order defined by MRD. This therefore
allows both reordering of program statements and relaxed write propagation.

4         Operational Semantics over MRD
Recall that the MRD semantic interpretation function JP K outputs a coherent
event structure µ = (L, S, `, ≤). In this section, we develop an operational se-
4
    We present the rules from [10] in Appendix A.
                                                                                9

mantics for traversing µ, while generating state configurations that model re-
laxed write propagation. In essence, this generalises the operational semantics
in Section 3 so that threads are executed out-of-order, as allowed by MRD.


4.1   Program Futures

Defining our operational semantics over raw syntax would force us to evaluate
statements in program order. Therefore we convert this syntax into a set of
atomic statements. We call this the atomic set of C, written C. MRD evaluates
while loops using step-indexing, treating them as finite unwindings of if-then-
else commands. For these, we generate a fresh unique label for each iteration of
the while loop for each of the atomic commands within the loop body. Recall
that the parallel composition of commands is modelled by a function from thread
identifiers to (sequential) commands. The atomic set of a program P is therefore
λt. P (t).
    To retain the ordering recognised during program execution, we introduce
futures, which are sets of MRD events partially ordered by the semantic depen-
dency and preserved program order relations. Essentially, instead of taking our
operational steps in program order over the syntax, we can nondeterministically
execute any statement which our futures tell us we have executed all necessary
predecessors of.
    For an execution S = (A, lk, rf, dp) of an event structure µ, we can construct
an initial future f = (A, ), where  = dp ∪ ≤|A and ≤|A is the preserved
program order ≤ (see Section 2) restricted to events in A. We say that an action
a is available in a future (K, ) iff there exists some event g with label a such
that g ∈ K and g is minimal in , i.e., for all events g 0 ∈ K, g 0 6 g. If a is
available in f , then the future of a in f , denoted a . f , is the future

        a . f ⇐⇒ (K 0 , |K 0 )         where K 0 = K \ {g | λµ (g) = a}

We lift this to a set of futures F to describe the candidate futures of a in F ,
denoted a . F :

                    a . F = {a . f | f ∈ F ∧ a available in f }

Note that a is enabled in F iff a . F 6= ∅.
   Essentially, a . F consumes an event g with label a from each of the futures
in F provided a is available, discarding all futures in which a is not available.
Intuitively, if an event is minimal in a program future then it may be executed
immediately. If it is not minimal, its predecessors must be executed first.


4.2   Future-based Transition Relation

Our operational semantics is defined by the transition relation in Future-Step
given below, which generalises Full in Fig. 5. The transition relation is defined
over (Q, (σ, γ), F ), where Q is the atomic set corresponding to the program text,
10

(σ, γ) is a configuration and F is a set of futures. The rule generalises Full in the
                                                                              (g,a,t)   a
obvious way, i.e., by evolving the configuration as allowed by        and −→t
and consuming an available action a in F . Below, we use ] to denote disjoint
union and f [k := v] to denote function updates where f (k) is updated to v.

                                  Q(t) = C ] {i : s}            a . F 6= ∅
                                          a                         (g,a,t)
                              (i : s, γ) −→t (skip, γ 0 )       σ             σ0
           Future-Step                        µ
                            (Q, (σ, γ), F ) =⇒ (Q[t := C], (σ 0 , γ 0 ), a . F )

Once a minimal action is chosen in a step of the operational semantics, it is
checked for consistency and added to the set of executed events. The set of
futures is pruned to remove the chosen event, and to exclude any futures that
are incompatible with the chosen event. The operational semantics continues
until it has consumed all of the futures.
   The following theorem establishes equivalence of our operational semantics
and the MRD denotational semantics. A proof is provided in the appendix.
Theorem 1 (Soundness and Completeness). Every execution generated by
the MRD model can be generated by the operational semantics, and every final
state generated by the operational semantics corresponds to a complete execution
of the MRD semantics.

4.3   Example
Recall the program in Fig. 1 and its event structure representation in Fig. 3. Let
∆S = {(x, x) | x ∈ S} be the diagonal of set S. We first derive our set of futures
from this structure:
                  {2 ≺ 3, 6, 7}      {2 ≺ 3, 8, 9}          {2 ≺ 3, 10, 11}
                  {4 ≺ 5, 6, 7}      {4 ≺ 5, 8, 9}          {4 ≺ 5, 10, 11}

where {2 ≺ 3, 6, 7} represents the future ({2, 3, 6, 7}, 2 ≺ 3 ∪ ∆{2,3,6,7} ). The
atomic set of the program is
                                                                
                        1 7→ {1 : r1 := [x], 2 : [y] := r1 + 1},
                  P =
                        2 7→ {3 : r2 := [y], 4 : [x] := 1}

The initial configuration is (σ0 , γ0 ), where σ0 = ({(0x , 0:W x 0, 0), (0y , 0:W y 0, 0)},
∅, ∅, ∅) and γ0 = {1 7→ {r1 7→ 0}, 2 7→ {r2 7→ 0}}, assuming the initialising
thread has identifier 0.
    To find out which events we can execute, we check our futures set. We cannot
execute events 3 or 5, which both have pre-requisite events that have not yet
been executed. These events are the only available events generated by line 2,
so we cannot attempt to execute line 2. We can, however, execute any other
line. Suppose we execute line 4, which corresponds to 4 : [x] := 1 in P (2). To
                               µ
use the transition relation =⇒, we need to do the following: (1) determine the
                                                                                       11

                                                                    a
corresponding action, a and new thread-local state using −→2 ; (2) generate a
                                                                                  b
tagged action b = (g, a, 2) for a fresh tag g and a new global state using   ; and
(3) check that a is available in the current set of futures.
    For (1), we can only create one action a = 4:W x 1 and the local state is
unchanged. For (2), we generate a new global state using the Write rule in Fig. 4
(full details elided). For (3), we take our candidate futures a . F by examining
which MRD events have the label 4:W x 1 — in this case events 7, 9, and 11. All
futures can execute one of these events so the new future set contains all futures
in F , each minus the set {7, 9, 11}.


5     Hoare Logic and Owicki-Gries Reasoning

Recall that the standard Owicki-Gries methodology [22] decomposes proofs of
parallel programs into two cases:

 – local correctness conditions, which define correctness of an assertion with
   respect to an individual thread, and
 – non-interference conditions, which ensures stability of an assertion under the
   execution of statements in other threads.

The standard Owicki-Gries methodology has been shown to be applicable to
a weak memory setting with relaxed write propagation (but without relaxed
program order) [7]. Note that an alternative characterisation (also in a model
without relaxed program order) has been given in [17].5 Unfortunately, the un-
restricted C11 semantics captured by MRD relaxes program order and hence
sequential composition in order to allow behaviours such as those in Fig. 1,
which requires a fundamental shift in Hoare-style proof decomposition. We show
that the modular Owicki-Gries rules, for reasoning about concurrent threads
remain unchanged.
    Like Dalvandi et al [7], we assume assertions are predicates over state config-
urations. In the current paper, the operational semantics is dictated by the set
of futures generated by MRD, thus we require two modifications to the classical
meaning. First, like prior work [7], we assume predicates are over state configu-
rations, which include (local) register files and (shared) event graphs. This takes
into account relaxed write propagation. Second, we introduce Hoare-triples with
futures generated by MRD, which takes into account relaxed program execution.
    In the development below, we refer to the preprocessed form of a program P
given by P(P ) = (µ, P ), where µ is the coherent event structure JP K and P the
set normal form of P . We let Fµ be the initial set of futures corresponding to µ.

Definition 1 (Hoare triple). Suppose X and Y are predicates over state con-
figurations, P is a concurrent program, and P(P ) = (µ, P ). The semantics of a
5
    This characterisation uses standard assertions but assumes a non-standard interpre-
    tation of Hoare-triples and introduces a stronger interference freedom check. In fact,
    for the model in [17], the introduction of auxiliary variables is unsound.
12

Hoare triple is given by {X} Init; P {Y }, where

 {X} Init; P {Y } =
                  b (Init ⇒ X) ∧
                                                    µ ∗
                    (∀C, C0 . X(C) ∧ ((P , C, Fµ ) =⇒ (∅, C0 , ∅)) ⇒ Y (C0 ))

That is, {X} P {Y } holds iff for every pair of state configurations C, C0 , assuming
X(C) holds and we execute P with respect to the future Fµ until P terminates
in C0 , we have Y (C0 ).
     Although Definition 1 provides meaning for a Hoare triple, we still require
a method for decomposing the proof outline. To this end, we introduce the
concept of a future predicate, which is a predicate parameterised by both futures
and configuration states. To make use of future predicates, we introduce a notion
of a Hoare triple for programs in set normal form.
     For the definitions below, assume P is a program and P(P ) = (µ, P ). We say
an atomic set Q is a sub-program of an atomic set P iff for all t, Q(t) ⊆ P (t).
We say a set of futures F 0 is a sub-future of set of futures F iff for each f 0 ∈ F 0
there exists an f ∈ F such that f 0 is an up-closed subset of f . For example,
if F = {{1 ≺ 2, 3, 4}, {1 ≺ 2, 3}}, then {{2, 4}, {1 ≺ 2}} is a sub-future of F ,
but {{1, 3}} is not. We say the sub-program Q corresponds to a sub-future F
iff labels(Q) = labels({Lab µ [π1 f ] | f ∈ F }), where we assume labels returns the
set of all labels of its argument, π1 is the project of the first component of the
given argument, and R[S] is the relational image of set S over relation R.

Definition 2 (Hoare triple (single step)). Suppose I and I 0 are future pred-
icates, P is a program and P(P ) = (µ, P ). If G is a sub-future of Fµ , correspond-
ing to a sub-program Q of P , we define

         {I}G Q {I 0 }
                                              µ     0
      b ∀C, C0 , G0 . I(G)(C) ∧ ((Q, C, G) =⇒ (Q , C0 , G0 )) ⇒ I 0 (G0 )(C0 )
      =

We say I is future stable for (F, P ) iff for all sub-futures G of F with correspond-
ing sub-programs Q of P , we have {I}G Q {I}.

Lemma 1 (Invariant). Suppose X and Y are configuration-state predicates,
P is a program and P(P ) = (µ, P ). If X ⇒ I(Fµ ), I(∅) ⇒ Y and I is future
stable for (Fµ , P ), then {X}Init; P {Y } provided Init ⇒ X.

    By construction, the sets of futures corresponding S  to different threads are
disjoint, i.e., for each future f ∈ Fµ , we have that f = t f|t , where f|t denotes
the future f restricted to events of thread t. The only possible inter-thread
dependency in MRD is via the reads from relation [23], which does not contribute
to the set of futures. This observation leads to a technique for an Owicki-Gries-
like modular proof technique for decomposing the monolithic invariant I into an
invariant per thread.
    We define F|t = {f|t | f ∈ F }. Then, we obtain the following lemma for
decomposing invariants in the same way as Owicki and Gries.
                                                                                   13

Lemma 2 (Owicki-Gries). For each thread t, let It be a future predicate corre-
sponding to t. If Init ⇒ X, X ⇒ ∀t. It (Fµ |t ), and ∀t. It (∅) ⇒ Y , then {X}P {Y }
holds provided both of the following hold.
1. For all threads t, It is future stable for (Fµ |t , P ).       (local correctness)
2. For all threads t1 , t2 such that t1 6= t2 , sub-futures F1 of Fµ |t1 , and F2 of
   Fµ |t2 , if Q corresponds to F2 , then we have6 {It1 (F1 ) ∧ It2 }F2 Q {It1 (F1 )}.
                                                                 (global correctness)

Thus, we establish {X}P {Y } through a series of smaller proof obligations. We
require that (1) the initialisation of the program guarantees X, (2) whenever
X holds then for each thread t, It holds for the initial future Fµ |t , (3) if It (∅)
holds for all t, then the post-condition Y holds, (4) each It is maintained by the
execution of each thread, and (5) It at each sub-future of t is stable with respect
to steps of another thread.


6     A Verification Example
With the verification framework now in place, we present a correctness proof for
the program in Fig. 1. The program and invariant are given in Fig. 6. First, in
Section 6.1, we present assertions for reasoning about state-configurations.

6.1    View-based assertions
As we can see from Fig. 5, the states that we use are configurations, which are
pairs of the form (σ, γ), where σ is an tagged action graph representing the
shared state and γ is mapping from threads to register files representing the
local state. Like prior work [7], we use assertions that describe the views of each
thread, recalling that due to relaxed write propagation, the views of each thread
may be different. Note that the formalisation of a state in prior work is a time-
stamp based semantics [7]. Nevertheless, the principles for defining thread-view
assertions also carry over to our setting of tagged action graphs.
   In this paper, the programs we consider are relatively simple, and hence, we
only use two types of view assertions: synchronised view, denoted [x = v]t , which
holds iff both thread t observes the last write to x and this write updates the
value of x to v, and possible view, denoted [x ≈ v]t , which holds iff t may observe
a write to x with value v. Formally, we define

                               b ∃w. OWσ (t)|x = {w} ∧ wrval (w) = v
               [x = v]t (σ, γ) =
               [x ≈ v]t (σ, γ) =
                               b ∃w ∈ OWσ (t)|x . wrval (w) = v

where OWσ (t)|x denotes the writes in OWσ (t) restricted to the variable x. Recall
that, by definition, for any state σ generated by the operational semantics, the
6
    Technically speaking, each instance of It1 (F1 ) in the Hoare-triple is a function
    λx. It1 (F1 ).
14

     Init: x = y = r1 = r2 = 0
                   {[x = 0]1 ∧ [x = 0]2 ∧ [y = 0]1 ∧ [y = 0]2 ∧ r1 = r2 = 0}
     Thread 1                                Thread 2
     {[y = 0]2 ∧ r2 = 0                      {[x = 0]1 ∧ r1 = 0}G
        ∧ (∀i. i ∈
                 / {0, 1} ⇒ [x 6≈ i]1 )}F      {r1 = 0 ∨
     1: r1 := [x]                                 (r1 = 1 ∧ (∀i. i ∈  / {0, 2} ⇒ [y 6≈
     {[y = 0]2 ∧ r2 = 0 ∧ r1 ∈ {0, 1}}F1 i]2 ))}G4
     2: y := r1 + 1                              3: r2 := [y]
     {r1 6= 1 ∨ r2 6= 1}∅                      {[x = 0]1 ∧ r1 = 0}G3
                                                 4: x := 1
                                             {r1 6= 1 ∨ r2 6= 1}∅
                                  {r1 6= 1 ∨ r2 6= 1}

           Fig. 6. Proof outline for load buffering with semantic dependencies


last write to each variable in mo order is observable to every thread. Examples
of these assertions in the context of an Owicki-Gries-style proof outline is given
in Fig. 6.


6.2     Example proof

To reduce the domain of our future predicate, we collapse the event-based futures
used by the operational semantics into sets of label-based futures. An event
future FE can be converted into a label future FL by applying the labelling
function to all events in FE . This makes the futures {3} and {5} equivalent, as
both are instances of {2:W y 2}, thus I({3}) = I({5}). This isn’t always a valid
step, as some events which share labels may not be related by  in the same way.
Thus, the technique can only be used if the label-based representation describes
exactly the futures generated by MRD, which is the case for our example.
    We describe our initial set of label futures as {{1u < 2, 3v , 4} | u ∈ {0, 1}∧v ∈
{0, 1, 2}}, using the notation {iv } to refer to an action with the line number i
with a read that returns the value v. We verify that this is a valid step: all futures
generated by MRD are described by these labels, and they do not describe any
potential futures not generated by MRD. We partition this into F = {{1u <
2} | u ∈ {0, 1}} and G = {{3v , 4} | v ∈ {0, 1, 2}} representing the future sets of
threads 1 and 2, respectively. We let F1 = {{2}} be the future set after executing
line 1, G3 = {{4}} be the future set after executing line 3 (reading some value
for y), and G4 = {{3v } | v ∈ {0, 1, 2}} be the future set after executing line 4.
    Our future predicate I must output a configuration predicate for every sub-
future of the initial set. Our partitioning fully describes these sub-futures, so we
now attach our assertions to these futures.
    To simplify the visualisation, we interleave the future predicate components
with the program to provide Hoare-style pre/post-assertions, and place the as-
sertion above a line of code if that line of code is contained in the applied future.
We use indentation to denote that an assertion applies to more than one future.
In this example G contains both lines 3 and 4, hence both lines are indented
                                                                                15

w.r.t. the first assertion in thread 2. We apply Lemma 2, and in the discussion
below, we describe the local and global correctness checks.
    For local correctness in thread 1, we must establish that {I}F {1, 2}{I}∅ . By
the definition of the future F , line 1 must be executed before line 2. This means
we only need to verify that {I}F {1}{I}F1 and {I}F1 {2}{I}∅ , which is identical
to a standard Hoare logic proof and relatively uninteresting.
    In thread 2, no order is imposed between lines 3 and 4. This means to establish
local correctness we must check that:
 – {I}G 3: r2 := y {I}G3
 – {I}G 4: x := 1 {I}G4
 – {I}G3 4: x := 1 {I}∅
 – {I}G4 3: r2 := y {I}∅
    The first three are trivial: line 3 modifies neither x nor r1 and line 4 does
not modify r1. For the final step, the first disjunct of {I}G4 is the same as the
first disjunct of {I}∅ , and the second disjunct ensures that we cannot observe
r2 = 1 after executing line 3.
    For global correctness, we must check that every assertion in thread 1 con-
tinues to hold after every line of thread 2, and vice versa. These checks are
also straightforward, so omit a detailed discussion. The only noteworthy aspect
is that for line 3 (and similarly, line 4), our precondition is the conjunction
{I}G4 ∧ {I}G , as both G and G3 are subfutures corresponding to line 3.
    The proof described above has actually been encoded and checked using our
existing Isabelle/HOL development [7, 8] by manually encoding the re-ordering
in thread 2. We aim to develop full mechanisation support as future work.


7   Related work
Work based on assumptions unsound in C++. Most logics for weak memory
are based on simplifying assumptions that exclude thin air reads by ensuring
program order is respected, even when no semantic dependency exists [7, 10,
11, 15, 17]. These assumptions incorrectly exclude the relaxed outcome of load
buffering tests like Fig. 1, introducing unsoundness when applied to languages
like C++: compiling Fig. 1 for an ARM processor produces code that does
exhibit the relaxed behaviour. The logic of Lundberg et al [20] correctly discards
many of this spurious program ordering, but it does not handle concurrency. We
provide an operational semantics of C++ that solves the thin air problem, where
prior attempts use simplifying assumptions like those of prior logics [7, 21].

Thin-air-free semantics. Each of the concurrency definitions that solves the out-
of-thin-air problem is remarkably complex [6,14,16,19,23,24], and so too is MRD.
We choose to base our logic on MRD because MRD’s semantic dependency
relation hides much of the complexity of the model that calculates it. Where
previously we would rely on program ordering, now we consider the semantic
dependency provided by MRD.
16

Logics for thin-air-free models. There are four logics built above concurrency
models that solve the thin air problem: three of these are very simple and apply
to only a handful of examples [13, 14, 16], and one is a separation logic built
above the Promising Semantics [26]. Unfortunately, the Promising Semantics
allows unwanted out-of-thin-air behaviour, forbidden by MRD [23], and as a
result may not support type safety [13].


8    Conclusions and future work
The subtle behaviour of concurrent programs written in optimised languages
necessitates good support for reasoning, but existing logics make unsound as-
sumptions that rule out compiler optimisations, or use underlying concurrency
models that admit out of thin air behaviour (see Section 7). We present a logic
built above MRD. MRD has been recognised as a potential solution to the thin
air problem in C and C++ by the ISO [12] and is the best guess at a C++ model
that allows optimisation and forbids thin-air behaviours.
    We follow a typical path for constructing a logic and start with an opera-
tional semantics that we show equivalent to MRD, and then as far a possible,
follow the reasoning style of Owicki Gries. In each case, we diverge from a typical
development because we cannot adopt program order into our reasoning system
and instead must follow semantic dependency. Our logic supplants linear pro-
gram order with a partial order, and where traditional pre- and post-conditions
are indexed by the program counter, here we index them by their position in the
partial order. This approach will work with any memory model that can provide
a partially ordered structure over individual program actions.
    The challenge in using the logic presented here is in managing the multitude
of proof obligations that follow from the branching structure and lack of order
in semantic dependency. This problem represents an avenue for further work: it
may be possible to obviate the need for some of these additional proof obligations
within the logic or to provide tools to more conveniently manage them.


References
 1. Adve, S.V., Gharachorloo, K.: Shared memory consistency models: A tutorial.
    IEEE Computer 29(12), 66–76 (1996)
 2. Alglave, J., Maranget, L., Tautschnig, M.: Herding cats: Modelling, simulation,
    testing, and data mining for weak memory. ACM Trans. Program. Lang. Syst.
    36(2), 7:1–7:74 (2014)
 3. Batty, M., Dodds, M., Gotsman, A.: Library abstraction for C/C++ concurrency.
    In: Giacobazzi, R., Cousot, R. (eds.) POPL. pp. 235–248. ACM (2013)
 4. Batty, M., Owens, S., Sarkar, S., Sewell, P., Weber, T.: Mathematizing C++ con-
    currency. In: Ball, T., Sagiv, M. (eds.) POPL. pp. 55–66. ACM (2011)
 5. Batty, M., Memarian, K., Nienhuis, K., Pichon-Pharabod, J., Sewell, P.: The prob-
    lem of programming language concurrency semantics. In: Vitek, J. (ed.) ESOP.
    Lecture Notes in Computer Science, vol. 9032, pp. 283–307. Springer (2015),
    https://doi.org/10.1007/978-3-662-46669-8_12
                                                                                      17

 6. Chakraborty, S., Vafeiadis, V.: Grounding thin-air reads with event structures.
    Proc. ACM Program. Lang. 3(POPL), 70:1–70:28 (2019), https://doi.org/10.
    1145/3290383
 7. Dalvandi, S., Doherty, S., Dongol, B., Wehrheim, H.: Owicki-Gries reasoning for
    C11 RAR. In: Hirschfeld, R., Pape, T. (eds.) ECOOP. LIPIcs, vol. 166, pp. 11:1–
    11:26. Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2020), https://doi.
    org/10.4230/LIPIcs.ECOOP.2020.11
 8. Dalvandi, S., Dongol, B., Doherty, S.: Integrating Owicki-Gries for C11-style mem-
    ory models into Isabelle/HOL. CoRR abs/2004.02983 (2020), https://arxiv.
    org/abs/2004.02983
 9. Dang, H., Jourdan, J., Kaiser, J., Dreyer, D.: Rustbelt meets relaxed memory.
    Proc. ACM Program. Lang. 4(POPL), 34:1–34:29 (2020), https://doi.org/10.
    1145/3371102
10. Doherty, S., Dongol, B., Wehrheim, H., Derrick, J.: Verifying C11 programs op-
    erationally. In: Hollingsworth, J.K., Keidar, I. (eds.) PPoPP. pp. 355–365. ACM
    (2019), https://doi.org/10.1145/3293883.3295702
11. Doko, M., Vafeiadis, V.: Tackling real-life relaxed concurrency with FSL++. In:
    ESOP. pp. 448–475 (2017)
12. Giroux, O.: ISO WG21 SG1 concurrency subgroup vote (2019), https://github.
    com/cplusplus/papers/issues/554, unanimously approved: OOTA is a major
    problem for C++, modular relaxed dependencies is the best path forward we have
    seen, and we wish to continue to pursue this direction
13. Jagadeesan, R., Jeffrey, A., Riely, J.: Pomsets with preconditions: a simple model
    of relaxed memory. Proc. ACM Program. Lang. 4(OOPSLA), 194:1–194:30 (2020).
    https://doi.org/10.1145/3428262, https://doi.org/10.1145/3428262
14. Jeffrey, A., Riely, J.: On thin air reads: Towards an event structures model of
    relaxed memory. Log. Methods Comput. Sci. 15(1) (2019), https://doi.org/10.
    23638/LMCS-15(1:33)2019
15. Kaiser, J., Dang, H., Dreyer, D., Lahav, O., Vafeiadis, V.: Strong logic for weak
    memory: Reasoning about release-acquire consistency in iris. In: ECOOP. pp. 17:1–
    17:29 (2017)
16. Kang, J., Hur, C., Lahav, O., Vafeiadis, V., Dreyer, D.: A promising semantics for
    relaxed-memory concurrency. In: Castagna, G., Gordon, A.D. (eds.) POPL. pp.
    175–189. ACM (2017), http://dl.acm.org/citation.cfm?id=3009850
17. Lahav, O., Vafeiadis, V.: Owicki-Gries reasoning for weak memory models. In:
    ICALP (2). LNCS, vol. 9135, pp. 311–323. Springer (2015)
18. Lahav, O., Vafeiadis, V., Kang, J., Hur, C., Dreyer, D.: Repairing sequential consis-
    tency in C/C++11. In: Cohen, A., Vechev, M.T. (eds.) PLDI. pp. 618–632. ACM
    (2017)
19. Lee, S., Cho, M., Podkopaev, A., Chakraborty, S., Hur, C., Lahav, O., Vafeiadis, V.:
    Promising 2.0: global optimizations in relaxed memory concurrency. In: Donaldson,
    A.F., Torlak, E. (eds.) PLDI. pp. 362–376. ACM (2020), https://doi.org/10.
    1145/3385412.3386010
20. Lundberg, D., Guanciale, R., Lindner, A., Dam, M.: Hoare-style logic for unstruc-
    tured programs. In: de Boer, F., Cerone, A. (eds.) Software Engineering and Formal
    Methods (2020)
21. Nienhuis, K., Memarian, K., Sewell, P.: An operational semantics for C/C++11
    concurrency. In: OOPSLA. pp. 111–128. ACM (2016)
22. Owicki, S.S., Gries, D.: An axiomatic proof technique for parallel programs I. Acta
    Informatica 6, 319–340 (1976), https://doi.org/10.1007/BF00268134
18

23. Paviotti, M., Cooksey, S., Paradis, A., Wright, D., Owens, S., Batty, M.: Modu-
    lar relaxed dependencies in weak memory concurrency. In: Müller, P. (ed.) Pro-
    gramming Languages and Systems. pp. 599–625. Springer International Publishing,
    Cham (2020)
24. Pichon-Pharabod, J., Sewell, P.: A concurrency semantics for relaxed atomics
    that permits optimisation and avoids thin-air executions. In: Bodı́k, R., Ma-
    jumdar, R. (eds.) Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages, POPL 2016, St. Pe-
    tersburg, FL, USA, January 20 - 22, 2016. pp. 622–633. ACM (2016).
    https://doi.org/10.1145/2837614.2837616, https://doi.org/10.1145/2837614.
    2837616
25. Podkopaev, A., Lahav, O., Vafeiadis, V.: Bridging the gap between program-
    ming languages and hardware weak memory models. Proc. ACM Program. Lang.
    3(POPL), 69:1–69:31 (2019), https://doi.org/10.1145/3290382
26. Svendsen, K., Pichon-Pharabod, J., Doko, M., Lahav, O., Vafeiadis, V.: A sep-
    aration logic for a promising semantics. In: Ahmed, A. (ed.) ESOP. Lecture
    Notes in Computer Science, vol. 10801, pp. 357–384. Springer (2018), https:
    //doi.org/10.1007/978-3-319-89884-1_13
27. Winskel, G.: Event structures. In: Brauer, W., Reisig, W., Rozenberg, G. (eds.)
    Petri Nets: Central Models and Their Properties, Advances in Petri Nets 1986, Part
    II, Proceedings of an Advanced Course, Bad Honnef, Germany, 8-19 September
    1986. Lecture Notes in Computer Science, vol. 255, pp. 325–392. Springer (1986),
    https://doi.org/10.1007/3-540-17906-2_31
                                                                                                           19

       n = eval(e, γ)          a = i:W x n               n = eval(e, γ)            a = i:WR x n
                           a                                                      a
        (i : [x] := e, γ) −→t (skip, γ)                     (i : [x] :=R e, γ) −→t (skip, γ)
                a = i:R x n                                           a = i:RA x n
                    a                                              A        a
 (i : r := [x], γ) −→t (skip, γ[r := n])                 (i : r := [x], γ) −→t (skip, γ[r := n])
                                           n = eval(e, γ)
                                                a
                               (i : r := e, γ) −→t (skip, γ[r := n])
                                                                       a
                                                         (C1 , γ) −→t (C10 , γ 0 )
                                τ                                      a
                  (skip; C, γ) −→t (C, γ)           (C1 ; C2 , γ) −→t (C10 ; C2 , γ 0 )
            eval(B, γ) = true                                          eval(B, γ) = false
                                    τ                                                         τ
  (if B then C1 else C2 , γ) −→t (C1 , γ)               (if B then C1 else C2 , γ) −→t (C2 , γ)
                                                        a
                                          (P (t), γ) −→t (C, γ 0 )
                               Prog             a
                                        (P, γ) −→t (P [t := C], γ 0 )
                                                                                                           τ
Fig. 7. Uninterpreted operational semantics of commands and programs, where −→
represents an internal transition

                                                    a                                             b
              τ
         P −→t P 0                       (P, γ) −→t (P 0 , γ 0 )           b = (g, a, t)      σ       σ0
              τ
 (P, (σ, γ)) =⇒ (P 0 , (σ, γ))                                             b
                                                        (P, (σ, γ)) =⇒ (P 0 , (σ 0 , γ 0 ))

                   Fig. 8. Interpreted operational semantics of programs



A    Operational Semantics of Doherty et al.

This section presents the operational semantics from [10]. We formally model
parallel composition as a function T → Com, where T is the type of a thread
identifier. The uninterpreted semantics is given in Fig. 7 and the interpreted
semantics in Fig. 8.

Example 2. Consider the following program:

                             Init: x = y = r1 = r2 = 0
                      Thread 1            Thread 2
                      1: r1 := [x]        3: r2 := [x]
                      2: y := 1           4: x := 1
                                  {r1 6= 1 ∨ r2 6= 1}

    Consider the first tagged action graph below, which represents a possible
state after executing lines the program above for the model in [10], which is a
model where sb and program order coincide. For clarity, we have omitted the
tags and thread identifiers of each event.
20

                                   Derived hb and fr                   Derived eco
        0:W x 0, 0:W y 0                                                        1:R x 0
                                       0:W x 0, 0:W y 0
     rf sb           sb                                                    rf             fr
                                       hb             hb                         mo
             mo mo    3:R y 1                                       0:W x 0           4:W x 1
 1:R x 0
                                  1:R x 0   hb   hb   3:R y 1
  sb                                                                                           3:R y 1
             rf            sb
                                  hb             fr        hb
                                                                                               rf
 2:W y 1              4:W x 1                                                   mo
                                  2:W y 1             4:W x 1     0:W y 0            2:W y 1

The derived happens-before and from-read relations are given in the second
figure, and the derived extended coherence order in the third.
Example 3. Suppose σ is the state depicted in Example 2. We have OWσ (1) =
{0:W x 0, 4:W x 1, 2:W y 1} (omitting the tag and thread id of the events) since
thread 1 has “encountered” 2:W y 1, but not yet encountered 4:W x 1. Similarly,
OWσ (2) = {2:W y 1, 4:W x 1} since it has encountered both 2:W y 1 and 4:W x 1.


B      Equivalence between MRD and the operational
       semantics
B.1     Operational executions are event-structure executions
Lemma 3. Given some program P such that

                     (P, (∅, λx. (λy.0)), F ) −→∗ (skip, (σ, Γ )), F 0 )

we name the components of σ to be (D, sb, rf D , mo). There must exist an execu-
tion X = (E, dp, rf E , ≤) in JP Kn, (λx. 0) ∅ and a bijection over events E : E → D
such that E(E) = D and E(rf E ) = rf D where E(e) = (d, a, t) =⇒ λ(e) = a.
    Suppose the contrapositive: that for any execution X in the MRD structure,
either D 6= E(E) or rf D 6= E(rf E ).
    If there are no executions containing exactly the actions in D, then we cannot
                                            a
arrive at event set D by application of −→ - it requires a . f for at least one
future, and the initial future set is derived directly from the set of executions.
There must therefore exist at least one execution such that D = E(E). Consid-
ering only these executions, we now show that at least one must have equivalent
rf edges to rf D .
    We know that MRD exhaustively generates rf edges which do not create a
cycle in rf∪dp∪ ≤. There cannot be an edge in all rf E which is simply absent from
rf D with no new edge added, as this would imply that rf D is incomplete. This is
forbidden by the read execution rule. To arrive at a complete rf D relation which
contains an edge not present in any potential rf E where E = D, the proposed
edge must cause such a cycle. Given that futures are ordered by dp∪ ≤, the new
cyclical edge must connect a maximal event to a minimal one. Once again, the
requirement that e . f for some f prevents executing a maximal event before a
minimal one. Thus, there must be some rf E which is equal to rf D .
                                                                                            21

B.2    The operational semantics covers all event-structure
       executions.
Lemma 4. Let X = (E, dp, rf, ≤) be a complete execution of the MRD model
                                                                          R
JP Kn λx. 0, ∅ for large enough n to ensure termination. Let the relation −
                                                                          → be
                                                                   R ∗
dp ∪ rf ∪ ≤, observing that E is partially ordered by −
                                                      → . There exists a relation
R0                  R                     R∪R0
−→ disjoint from −
                 → such that −−−→ is total and acyclic over E, giving the
          R∪R0                                                                           w,e1
chain e1 −−−→ e2 ...ek , and an execution of the operational semantics σ1
σ2 ...σk such that e1 ..ek ∼ σk , where e1 ..en denotes X with the event set and
relations restricted to {e1 ...en } and (E, rfE , dp, ppo) ∼ (D, rfD , mo) iff λ(E) =
D ∧ λ(rfE ) = rfD .

                                                 R∪R0                                      R
Proof sketch The existence of an acyclic −−−→ is given by the acyclicity of −
                                                                            →
                                                                                  R∪R0
asserted by the MRD axiomatic check. We proceed by induction over −−−→ and
 w,e                                                          R0                 R∪R0
      . The base case is trivial: take any arbitrary −→ which makes −−−→ total.
                                     R                            rf
Because e1 must be minimal in −      →, it must be minimal in −→ and minimal
                            rf
in dp. Being minimal in −→ means it cannot be a read or RMW event. Being
minimal in dp means it must be in an available future. Let σ1 be ({λ(e1 )}, ∅, ∅).
It remains to show that e1 ..en−1 ∼ σn−1 =⇒ e1 ..en ∼ σn for n ≤ k. There are
3 cases for the event type en : a read event, a write event, or an RMW event.
    In the case where en is a read, to use the semantic rule for creating state
σn requires an event λ(w) ∈ OWσn−1 (tid(en )) such that var(w) = var(en ) ∧
wrval(w) = wrval(en ). This adds (λ(w), λ(en )) to rfD .
                                                                                   rf
     Given X is complete, there must be some write w0 such that w0 −→ en . It
                                   R∪R0                                    R
must also be true that w0 −−−→ en , due to the inclusion of rf in −→. Therefore,
we can use w0 as w.
   The event w will be in OWσn−1 (tid(w)) if it is maximal in mo. Suppose some
event w00 exists such that (w, w00 ) ∈ mo. By the construction of mo, it must also
                         ∗
                  R∪R0                     R ∗
be true that w −−−→ w00 . If w −
                               → w00 , then the axiomatic checks in MRD
               rf
prevent the w −→ en edge from being added. Otherwise, by lemma 5, there
                             R0
exists another choice of −→ such that w0 is added to σn before w and (w, w0 ) is
no longer maximal in mo.
    In the case where en is an initialising write, we only need D such that en ∈ D.
If en is a non-initialising write, meaning there is some event w ∈ X which is a
write to the same variable as en , we must show that w is in OW (en ). This follows
by the same reasoning as in the read case.
                             ∗
                   R∪R0                   R ∗
Lemma 5. If ei −−−→ ej ∧ ei −
                            6 → ej in the chain e1 ..en then there exists a
                                                         ∗
                             R00                 R∪R00                   R∪R00
valid choice of relation −−→ such that ej −−−−→ ei , the union −−−−→ is acyclic,
and there exists an event e0n in e1 ..en such that
                  R∪R0                                       R∪R00
1. e1 ..en under −−−→ is equal to e1 ..e0n under −−−−→
22

                                                                                    R∪R00
2. σn0 , the result of running the operational semantics under −−−−→, is equal to
   σn excepting relation edges between ei and ej
                                                  R00                       R∪R00
Proof. Begin by enforcing that ej −−→ ei . A cycle in −−−−→ would have the
                                                                      ∗
               R∪R00                                            R00
shape ei −−−−→ ej . As we can trivially prevent ei −−→ ej by construction, this
                                                                                            R ∗
relation edge must contain one or more event pairs e and e0 such that e −
                                                                        → e0 .
                                           R00                        R ∗
This event pair can be moved −−→-before ej unless ej −
                                                     → e, and it can be moved
R00                            R ∗                                                   R ∗
−−→-after ei unless e0 −→ ei . If both of these are true, then ei −
                                                                  → ej , which we
know is untrue.
   To find e0n , choose any element which is not equal to ej from the set of events
                                   R                                  R00
which are maximal in −  → and make it maximal in −−→. There must be some
                                                                      R
element in this set which is not ej , as otherwise we would have ∀e.e −
                                                                      → ej and
                                            R ∗
it would again be true that ei −
                               → ej .
    What remains is to create two arbitrary orderings R100 and R200 such that
       R∪R00
       1               2     R∪R00       1         2    R∪R00    R∪R00
e1 −−−−→ ej and ej −−−−→ en and both −−−−→ and −−−−→ are acyclic. Partition
                                                                 R
all remaining events into those which are and are not −
                                                      →-before ej , then construct
R100                           R200
−−→ over the first and −−→ over the second. These are individually trivial by the
                R
acyclicity of − →, and their union must be acyclic as their event sets are disjoint.
     It is trivial to establish that e1 ..en = e1 ..en0 by the fact that all relation
                                  R
edges in X are preserved in −     →. To show that σn is equivalent to σn0 excepting
(ei , ej ) edges, it suffices to show that if (e, e0 ) ∈ mo then (e, e0 ) ∈ mo0 , as rf
                                       R
edges are constrained by −      →. Events are only relocated around points ei and
ej , so any such edges would have the shape (e, ej ) or (ei , e) in σn and become
(ej , e) or (e, ei ) respectively. Focusing on the first case, any such reordering is
                                                                                     ∗
                             R ∗                                            R∪R00
only required if ej −
                    → e, as this forces e to be placed −−−−→ -after ej in our
                       R00
construction of −−→. This makes the initial mo edge impossible to observe. The
same reasoning holds for the (ei , e) edge.
                                                                                           23

C     Further Examples
C.1    Partial conditional
Our first example is the partial conditional example, whose proof outline is
given in Fig. 9. The program contains no dependencies in Thread 1 and non-
trivial dependencies in thread 2. In particular, in Thread 2 the dependencies are
condition on the values read for x and y.
 – If r1 = r2 = 1, then we have dependencies between lines 3 and 5, and
   between lines 4 and 6, but lines 3/4 and 5/6 are mutually independent.
 – If r1 = 1 and r2 = 0, there is a dependency between lines 3 and 7.
 – If r1 = 0 and r2 = 1, there is a dependency between lines 4 and 8.
This is reflected by the futures F for thread 1 and G for thread 2 in Fig. 9.


Init: x = y = r1 = r2 = 0
Thread 1                            Thread 2
{[x = 0]2 ∧ [y = 0]2 }F            {I}G
  {[x = 0]2 ∧ [y ∈ {0, 1}]2 }F2       {r2 = m ∧ I}G4n
  1: [x] := 1                         3: r1 := [x] ;
  {[x ∈ {0, 1}]2 ∧ [y = 0]2 }F1       {r1 = m ∧ I}G3m
  2: [y] := 1                         4: r2 := [y] ;
{[x ∈ {0, 1}]2 ∧ [y ∈ {0, 1}]2 }∅     {r1 = m ∧ r2 = n ∧ I}G3m ,4n
                                           if r1 = 1 & r2 = 1 {
                                           {r1 = 1 ∧ r2 = 1 ∧ I}G31 ,41
                                               {r1 = 1 ∧ r2 = 1 ∧ [w = 0]2 ∧ [z = 1]2 }G31 ,41 ,6
                                               5: [w] := 1 ;
                                               {r1 = 1 ∧ r2 = 1 ∧ [w = 1]2 ∧ [z = 0]2 }G31 ,41 ,5
                                               6: [z] := 1 ; }
                                           if r1 = 0 & r2 = 1 {
                                           {r1 = 0 ∧ r2 = 1 ∧ I}G30 ,41
                                               7: z := 1 }
                                           if r1 = 1 & r2 = 0
                                           {r1 = 1 ∧ r2 = 0 ∧ I}G31 ,40
                                              8: w := 1 ;
                                   {[w = r1]2 ∧ [z = r2]2 }∅
                          {[w = r1]2 ∧ [z = r2]2 }

Fig. 9. Partial conditional: F = {{1, 2}} G = {{31 ≺ 5, 41 ≺ 6}, {31 ≺ 8, 40 }, {41 ≺
7, 30 }, {30 , 40 }} and I = [w = 0]2 ∧ [z = 0]2




C.2    Random number generator (RNG)
Our next example is the random number generator (RNG) litmus test (see
Fig. 10) from [6], which in a poorly defined semantics has the potential to termi-
nate so that line 7 is executed. Our proof outline shows that this cannot be the
case in our semantics, i.e., the program satisfies the postcondition [x 6≈ 99]1,2,3 .
24

Init: x = y = r1 = r2 = r3 = 0
Thread 1                    Thread 2                           Thread 3
{[y = 0]2 ∧ r2 = 0          {[x = 0]1,2,3                      {∀i ∈/ {0, 1} ⇒ [x 6≈ i]3
∧ ∀i. i 6= 0 ⇒ [x 6≈ i]1 }F ∧ ∀i. i ∈
                                    / {0, 1} ⇒ [y 6≈ i]2 }G    ∧ [x 6≈ 99]1,2,3 }H
1: r1 := x                  3: r2 := y                         5: r3 := x
{[y = 0]3 ∧ r1 = 0}F1       {[x = 0]1,2,3 ∧ r2 ∈ {0, 1}}G3     {r3 ∈ {0, 1} ∧ [x 6≈ 99]1,2,3 }H5
2: y := r1 + 1              4: x := r2                             if r3 = 100 then
{true}∅                     {true}∅                                    {false}H5
                                                               6:      x := 99
                                                               {[x 6≈ 99]1,2,3 }∅
                                     {[x 6≈ 99]1,2,3 }

         Fig. 10. RNG, where F = {{1 ≺ 2}}, G = {{3 ≺ 4}}, H = {{5 ≺ 6}}


    The program is similar to Fig. 6, but contains semantic dependencies between
lines 1 and 2, between lines 3 and 4, and between lines 5 and 7. This means
that no reorderings are permitted within any of the threads, thus its proof is
straightforward. In fact, we have used our existing Isabelle/HOL formalisation [8]
for a model that assumes program order to discharge the proof obligations.

Theorem 2. The proof outline in Fig. 10 is valid.


C.3     LB+data-add+ctrl
The next two examples are designed to test whether a chain of semantic depen-
dencies on data, addresses and control are properly modelled by the semantics.


            Init: x = y = r1 = r2 = 0
            Thread 1                          Thread 2
            {[y = 0]1 ∧ r2 = 0                {∀i. i ∈
                                                     / {0, 1} ⇒ [y 6≈ i]2 }G
            ∧ ∀i. i 6= 0 ⇒ [x 6≈ i]1 }F       3: r2 := z
            1: r1 := x                        {r2 ∈ {0, 1}}G3
            {[y = 0]2 ∧ r1 = 0 ∧ r2 = 0}F1        if r2 = 2 then
            2: z := r1 + 1                           {false}G3
            {r1 6= 1 ∨ r2 6= 2}∅              4:     x := 1
                                              {true}∅
                                   {r1 6= 1 ∨ r2 6= 2}

     Fig. 11. Simple LB+data-add+ctrl, where F = {{1 ≺ 2}} and G = {{3 ≺ 4}}


   The proofs of both programs are straightforward since they do not contain
any intra-thread re-orderings. Again, we have shown correctness of both proof
outlines using our existing Isabelle/HOL formalisation [8].

Theorem 3. The proof outlines in Fig. 11 and Fig. 12 are valid.
                                                                           25




   Init: x = y = r1 = r2 = r3 = r4 = 0
   Thread 1                       Thread 2
   {[y = 0]1 ∧ [z = 0]2           {∀i. i ∈
                                         / {0, 1} ⇒ [z 6≈ i]2 }G
   ∧(∀i. i 6= 0 ⇒ [x 6≈ i]1 }F    6: r4 := z
   1: r1 := x                     {r4 ∈ {0, 1}}G6
   {[y = 0]1 ∧[z = 0]2 ∧r1 = 0}F1    if r4 = 2 then
   2: r2 := r1;                          {false}G6
   {[y = 0]1 ∧[z = 0]2 ∧r2 = 0}F2 7:     x := 1
   3: y := r2;                    {r4 ∈ {0, 1}}∅
   {[y = 0]1 ∧ [z = 0]2 }F3
   4: r3 := y;
   {[z = 0]2 ∧ r3 = 0}F4
   5: z := r3 + 1;
   {r3 = 0}∅

                                 {r3 6= 1 ∨ r4 6= 2}

Fig. 12. LB+data-add+ctrl, where F = {{1 ≺ 2 ≺ 3 ≺ 4 ≺ 5}} and G = {{6 ≺ 7}}
