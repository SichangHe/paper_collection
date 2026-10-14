                                                     VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA
                                                                       REFINEMENT
arXiv:2108.06944v1 [cs.LO] 16 Aug 2021




                                                                               SADEGH DALVANDI AND BRIJESH DONGOL

                                               University of Surrey, Guildford, Surrey, United Kingdom
                                               e-mail address: m.dalvandi@surrey.ac.uk

                                               University of Surrey, Guildford, Surrey, United Kingdom
                                               e-mail address: b.dongol@surrey.ac.uk


                                                     Abstract. Deductive verification of concurrent programs under weak memory has thus
                                                     far been limited to simple programs over a monolithic state space. For scalability, we also
                                                     require modular techniques with verifiable library abstractions. This paper addresses this
                                                     challenge in the context of RC11 RAR, a subset of the C11 memory model that admits
                                                     relaxed and release-acquire accesses, but disallows, so-called, load-buffering cycles. We
                                                     develop a simple framework for specifying abstract objects that precisely characterises the
                                                     observability guarantees of abstract method calls. We show how this framework can be
                                                     integrated with an operational semantics that enables verification of client programs that
                                                     execute abstract method calls from a library they use. Finally, we show how implemen-
                                                     tations of such abstractions in RC11 RAR can be verified by developing a (contextual)
                                                     refinement framework for abstract objects. Our framework, including the operational se-
                                                     mantics, verification technique for client-library programs, and simulation between abstract
                                                     libraries and their implementations, has been mechanised in Isabelle/HOL.




                                                                                        1. Introduction
                                         The formal verification of concurrent programs in a weak memory setting is challenging since
                                         various writes to the memory locations may be reordered arbitrarily and therefore seen by
                                         other threads in an order different from the program order. In order to reason about such
                                         programs, the observations that a thread can make of the writes within the system should be
                                         taken into consideration. In recent work, reasoning about per-thread observations has led to
                                         operational characterisations of the memory model, where high-level predicates for reasoning
                                         about per-thread observations have been developed, and deductive verification techniques
                                         applied to standard litmus tests and non-trivial synchronisation algorithms [DDDW20a].
                                              Current operational verification techniques for weak memory are however, focussed on
                                         (closed) programs, and hence do not provide straightforward mechanisms for (de)composing
                                         clients and libraries. This problem requires special consideration under weak memory since
                                             Key words and phrases: Weak Memory, C11, Verification, Concurrent Libraries, Refinement.
                                             Supported by EPSRC Grant EP/R032556/1.



                                         Preprint submitted to                                                                       © S. Dalvandi and B. Dongol
                                         Logical Methods in Computer Science                                                         CC Creative Commons
2                                  S. DALVANDI AND B. DONGOL




the execution of a library method may induce synchronisation. That is, a thread’s observa-
tions of a system (including of client variables) can change when executing library methods.
     This paper addresses several questions surrounding client-library composition in a weak
memory context. Like prior works [DDDW20a, DDWD19, KDD+ 17], we focus on RC11-
RAR, a fragment of C11 memory model, which is one of the most interesting and challenging
fragments for verification.1
     (1) How can a client use a weak memory library, i.e., what abstract guarantees can a
library provide a client program? Prior works [DJRA18, BDG13] describe techniques for
specifying the behaviour of abstract objects, which are in turn related to their implemen-
tations using causal relaxations of linearizability. However, these works do not provide a
mechanism for reasoning about the behaviour of client programs that use abstract libraries.
In this paper, we address this gap by presenting a modular operational semantics that
combines weak memory states of clients and libraries. This is our first contribution.
     (2) What does it mean to implement an abstract library? To ensure that behaviours
of client programs using an abstract library are preserved, we require contextual refinement
between a library implementation and its abstract specification. This guarantees that no
new client behaviours are introduced when a client uses a (concrete) library implementa-
tion in place of its (abstract) library specification. Under sequential consistency (SC), it
is well known that linearizable libraries guarantee (contextual) refinement [DG16, GY11,
FORY10]. However, under weak memory, a generic notion of linearizability is difficult to
pin down [DJRA18, DDWD18]. We therefore present a direct technique for establishing
contextual refinement under weak memory. A key innovation is the development of context-
sensitive simulation rules that ensure that each client thread that uses the implementation
observes a subset of the values seen by the abstraction. This is our second contribution.
     (3) Can the same abstract library specify multiple implementations? A key benefit of
refinement is the ability to use the same abstract specification for multiple implementations,
e.g., to fine-tune clients for different concurrent workload scenarios. To demonstrate the
applicability of our framework, we provide a proof-of-concept example for an abstract lock
and show that the same lock specification can be implemented by a sequence lock and ticket
lock. The theory itself is generic and can be applied to concurrent objects in general; we
prove correctness of the Treiber Stack for RC11-RAR. The original Treiber stack assumes
SC memory. We prove correctness under relaxed and release-acquire accesses, thereby
showing where additional synchronisation is required under weak memory. This is our third
contribution.
     (4) How can we support operational verification? Can the verification techniques be
mechanised? Assuming the existence of an operational semantics for the underlying memory
model, we aim for deductive verification of both client-library composition and contextual
refinement. We show that this can be supported by prototyping the full verification stack
in the Isabelle/HOL theorem prover.2 All of the programs, theorems and proof rules in this
paper are fully verified. Our Isabelle development is around 25 KLOC (thousand lines of
code), where around 2.5 KLOC is taken from [DDDW20b]. This is our fourth contribution.
     Closely related to our work is that of Raad et al. [RDR+ 19], who have tackled the
problem of client-library programs in a declarative framework. Their framework provides
support for axiomatic specifications of weak memory concurrent libraries and verification of
   1The memory model can be extended, but since this paper focusses on verification and refinement we
keep the memory fragment small to simplify the presentation.
   2Our Isabelle theories may be accessed via [DD21]. Note that the theories require Isabelle 2020.
              VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                      3




library implementations against these specifications. Although this work addresses a similar
set of questions to ours, there are several key differences in our approach. We move from a
declarative to an operational semantics, which provides a significant step-change as it allows
integration with well-understood reasoning techniques of Owicki-Gries (cf. Section 5.2) and
refinement (cf. Section 6), as well as the possibility of rely-guarantee in future work. Raad
et al [RDR+ 19] also describe a notion of refinement, but their definition is not based on
trace refinement. Moreover, our operational semantics enables a new approach to library
specifications than Raad et al. [RDR+ 19]. In particular, we follow an approach in which
library operations interact with weak memory in a manner that is similar to the interaction
between standard reads and writes within C11 (see Section 7.1). This paves the way for
implementations that take further advantage of weak memory, since our specifications allow
new operations to be introduced in the “middle” of an existing abstract history. This is akin
to checking multiple complete executions in a declarative approach for each legal position
of the operation.
     The strength of Raad et al.’s declarative approach [RDR+ 19] is that it considers more
than one memory model and handles so-called “towers of abstraction”, where a library
implementation can in turn use other library specifications. The former is more complex
in an operational setting since the operational rules are fine-tuned to a particular memory
model, but the latter can be handled via straightforward extensions to the semantics (see
Aside 1).3 On the other hand, our approach is in a stronger position w.r.t mechanised
verification. While our development (including all examples and case studeis) is fully mech-
anised, [RDR+ 19] has only achieved a partial mechanisation over a small parts of their
contribution.
Contributions. Overally, the contributions of our work can be seen as follows. First,
it presents an approach for specifying abstract libraries and the associated view-based
assertions that allows verification of client programs that use the abstract library in an
Owicki-Gries setting. Second, it introduces a generalised operational semantics for C11
weak memory that allows implementation of C11-style libraries and also provides an asser-
tion language that allows for verification of libraries at the implementation level. Third,
it provides a refinement framework that allows one to prove that an implementation cor-
rectly refines the abstract specification. The first two, can be used independently and offers
enough support (in varying levels of abstraction) to verifying client-library programs. The
third contribution, allows for establishing a formal link between the high level abstract
specification of a library and its implemenation.
     The general workflow of our approach is as follows:
• Defining the abstract operational specification of a library.
• Verifying client programs that uses the library operations using Hoare logic and Owicki-
   Gries.
• Implementing the library using the generalised operational semantics of C11.
• Proving that the implementation is a contextual refinement of the abstract specification
   and therefore it can safely replace the abstract specification in the client programs.
Overview. In Section 2 we motivate the main ideas and illustrate the basic principle of
message-passing synchronisation, but for programs comprising a program executing with
an abstract library. Section 3 presents a modular programming language and operational
  3We have not done this here to simplify the presentation.
4                                 S. DALVANDI AND B. DONGOL




          Init: d := 0; s.init();                             Init: d := 0; s.init();
      Thread 1 Thread 2                                 Thread 1 Thread 2
      d := 5;      do r1 := s.pop()                     d := 5;       do r1 := s.popA ()
      s.push(1); until r1 = 1;                                 R
                                                        s.push (1); until r1 = 1;
                   r2 ← d;                                            r2 ← d;
          {r2 = 0 ∨ r2 = 5}                                      {r2 = 5}

Figure 1: Unsynchronised message pass-          Figure 2: Publication     via   a   synchronising
          ing                                             stack

semantics for reads/write accesses within this language. A method for encoding the op-
erational semantics of abstract objects is given in Section 4. In Section 5, we describe
verification of client programs that use abstract libraries, and in Section 6 we present our
refinement theory. We use an abstract lock and two different implementations of this lock
as running examples. Finally, in Section 7, we discuss the specification of generic concur-
rent objects that exploit view-based relaxations, making use of the framework developed in
Section 4. Here, we also describe the verification of the Treiber Stack adapted for C11.

                         2. Message passing via library objects
We first illustrate the basic principles of client-object synchronisation in weak memory.
 Client-object message passing. Under SC all threads have a single common view of the
 shared state. When a new write is executed, the “views” of all threads are updated so that
 they are guaranteed to only see this new latest write. In contrast, each thread in a C11
 program has its own view of each variable. Views may not be updated when a write occurs,
 allowing threads to read stale writes. To enforce view updates, additional synchronisation
(e.g., release-acquire) must be introduced [BOS+ 11, KDD+ 17, LVK+ 17].
      Now consider a generalisation of this idea to (client) programs that use library objects.
The essence of the problem is illustrated by the message-passing programs in Figures 1 and 2.
 Under SC, when the program in Fig. 1 terminates, the value of r2 is guaranteed to be 5.
 However, this is not necessarily true in a weak memory setting. Even if pop operation in
 thread 2 returns 1, it may be possible for thread 2 to observe a stale value 0 for d. Therefore
 the program only guarantees the weaker postcondition r2 = 0 ∨ r2 = 5.
      To address this problem, the library operations in Fig. 2 are annotated with release-
 acquire annotations. In particular, the client assumes the availability of a “releasing push”
(pushR (1)), which is to be used for message passing. Thread 2 pops from s using an
“acquiring pop” (popA ()). If this pop returns 1, the stack operations induce a happens-
 before synchronisation in the client, which in turn means that it is now impossible for
 thread 2 to read the stale initial write for d.
Verification strategy. Our aim is to enable deductive verification of such programs by
 leveraging recently developed operational semantics, assertion language and Owicki-Gries
 style proof strategy for RC11 RAR [DDDW20a]. We show that these existing concepts
 generalise naturally to client-object, and in a manner that enables modular proofs.
      The assertion language of [DDDW20a] enables reasoning about a thread’s views, e.g.,
 in Fig. 3, after initialisation, thread t ∈ {1, 2} has definite value 0 for d (denoted [d = 0]t ).
 In this paper, we extend such assertions to capture thread views over library objects. E.g.,
              VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                        5




                                Init: d := 0; s.init();
                   {[d = 0]1 ∧ [d = 0]2 ∧ [s.pop(empty)]1 ∧ [s.pop(empty)]2 }
              Thread 1                         Thread 2
              {¬hs.pop(1)i2 ∧ [d = 0]1 }       {hs.pop(1)i[d = 5]2 }
              1 : d := 5;                      3 : do r1 := s.popA () until r1 = 1;
              {¬hs.pop(1)i2 ∧ [d = 5]1 }       {[d = 5]2 }
              2 : s.pushR (1);                 4 : r2 ← d;
              {true}                           {r2 = 5}
                                       {r2 = 5}

                       Figure 3: A proof outline for message passing

after initialisation, the only value a pop by thread t can return is empty, and this is captured
by the assertion [s.pop(empty)]t . The precondition of d := 5 states that thread 2 cannot
pop value 1 from s (as captured by the assertion ¬hs.pop(1)i2 ). The precondition of the
until loop in thread 2 contains a conditional observation assertion (i.e., hs.pop(1)i[d = 5]2 ),
which states that if thread 2 pops value 1 from s then it will subsequently be in a state
where it will definitely read 5 for d.
     A key benefit of the logic in [DDDW20a] is that it enables the use of standard Owicki-
Gries reasoning and straightforward mechanisation [DDD20]. As we shall see (Section 5.3),
we maintain these benefits in the context of client-object programs.
Contextual refinement. Contextual refinement relates a client using an abstract object
with a client that uses a concurrent implementation of the object. More precisely, we say
that a concrete object CO is a contextual refinement of an abstract object AO iff for any
client C, every behaviour of C when it uses CO is a possible behaviour of C when it uses
AO. Thus, there is no observable difference to any client when it uses CO in place of AO.
     In a weak memory setting, to enable a client to use an object, one must specify how
synchronisation between object method calls affects the client state. To implement such a
specification, we must describe how the abstract synchronisation guarantees are represented
in the implementation. Prior works have appealed to extensions of notions such as lineariz-
ability to ensure contextual guarantees [DJRA18, EE19, RDR+ 19]. In this paper, we aim
for a more direct approach and consider contextual refinement directly.

                        3. Generalised operational semantics
We now present a simple program syntax that allows one to write open programs that can
be filled by an abstract method or concrete implementation of a method.

3.1. Program Syntax. We start by defining a syntax of concurrent programs, starting
with the structure of sequential programs (single threads). A thread may use global shared
variables (from GVar ) and local registers (from LVar). We let Var = GVar ∪ LVar and
assume GVar ∩ LVar = ∅. For client-library programs, we partition GVar into GVar C
(the global client variables) and GVar L (the global library variables) and similarly LVar
into LVar C and LVar L . In an implementation, global variables can be accessed in three
different synchronisation modes: acquire (A, for reads), release (R, for writes) and relaxed
(no annotation). The annotation RA is employed for update operations, which read and
6                                S. DALVANDI AND B. DONGOL




write to a shared variable in a single atomic step. We let Obj and Meth be the set of all
objects and method calls, respectively.
     We assume that ⊖ is a unary operator (e.g., ¬), ⊕ is a binary operator (e.g., ∧, +, =)
and n is a value (of type Val ). Expressions must only involve local variables. The syntax of
sequential programs, Com, is given by the following grammar with r ∈ LVar , x ∈ GVar , o ∈
Obj , m ∈ Meth, u, v ∈ Val:

     Exp L ::= Val | LVar | ⊖Exp L | Exp L ⊕ ExpL
    CExp L ::= • | Exp L
         • ::= Val | o.m([u]) | Com, where Com contains no holes
    ACom ::= • | ⊥ | r ← CAS[R][A] (x, u, v) |
             r ← FAI[R][A] (x) | r := CExp L | x :=[R] Exp L | r ←[A] x
     Com ::= ACom | Com; Com | if B then Com else Com | while B do Com
where we assume B to be an expression of type CExp L that evaluates to a boolean. We
allow programs with holes, denoted •, which may be filled by an abstract or concrete method
call. During a program’s execution, the hole may also be filled by the null value ⊥ ∈ / Val,
or the return value of the method call. The notation [X] denotes that the annotation X
is optional, where X ∈ {A, R}, enabling one to distinguish relaxed, acquiring and releasing
accesses. Within a method call, the argument u is optional. Later, we will also use do-until
loops, which is straightforward to define in terms of the syntax above.

3.2. Program Semantics. For simplicity, we assume concurrency at the top level only. We
let Tid be the set of all thread identifiers and use a function Prog : Tid → Com to model a
program comprising multiple threads. In examples, we typically write concurrent programs
as C1 || . . . ||Cn , where Ci ∈ Com. We further assume   some initialisation of variables. The
structure of our programs thus is Init; C1 || . . . ||Cn .
     The operational semantics for this language is defined in three parts. The program
semantics fixes the steps that the concurrent program can take. This gives rise to transitions
           a        ′    ′                             ′                           ′
(P, lst ) −
          →    t (P , lst ) of a thread t where P and P are programs, lst and lst is the state
of local variables and a is an action (possibly the silent action ǫ, see below). The program
semantics is combined with a memory semantics reflecting the C11 state, and in particular
the writes from which a read action can read. Finally, there is the object semantics, which
defines the abstract semantics of the object at hand.
     We assume that the set of actions is given by Act. We let ǫ ∈  / Act be a silent action and
let Actǫ = Act ∪ {ǫ}. For an expression E over local variables, we write JEKls for the value
of E in local state ls; we write ls[r := v] to state that ls remains unchanged except for the
value of local variable r which becomes v. We use C[D] to denote the program C with the
hole filled by D. If D = ⊥, we proceed with the execution of C, otherwise we execute D.
Note that if D terminates with a value (due to a method call that returns a value), then the
hole contains a value and execution may proceed by either using the rule for r := v or the
rule for v; C2 , both of which are present in Fig. 4. The last two rules, Cli and Lib, lift the
transitions of threads to a transition of a client and library program, respectively. These
are distinguished by the subscript L, which only appears in transitions corresponding to
the library.
                 VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                                                              7




     r ∈ LVar v = JEKls                       x ∈ GVar           a = wr[R] (x, JEKls )            a = rd[A] (x, v)           v ∈ Val
              ǫ                                            [R]                                       [A]
 (r := E, ls) −
              → (⊥, ls[r := v])                    (x :=                a
                                                                 E, ls) −
                                                                        → (⊥, ls)             (r ←                a
                                                                                                           x, ls) −
                                                                                                                  → (⊥, ls[r := v])
               a
     (C1 , ls) −
               → (C1′ , ls′ )                  v ∈ Val ∪ {⊥}                         JBKls                           ¬JBKls
                                ′                       ǫ                              ǫ                               ǫ
                → (C1′ ; C2 , ls )
 (C1 ; C2 , ls) −a                         (v; C2 , ls) −
                                                        → (C2 , ls)          (IF , ls) −
                                                                                       →  (C1 , ls)          (IF , ls) −
                                                                                                                       → (C2 , ls)

                       JBKls                                           ¬JBKls
                        ǫ                                                  ǫ                                       ǫ
   (WHILE , ls) −
                → (C; WHILE , ls)                             (WHILE , ls) −
                                                                           → (⊥, ls)                    (C[⊥], ls) −
                                                                                                                   → (C, ls)
                       a
               (D, ls) −
                       → (D′ , ls′ )                               a = rd(x, v ′ )   v ′ 6= u u, v, v ′ ∈ Val
                    a       ′     ′
         (C[D], ls) −
                    → L (C[D ], ls )                       (r ← CAS[R][A] (x, u, v), ls) −
                                                                                         a
                                                                                         → (⊥, ls[r := false])

               a = updX (x, u, v) u, v ∈ Val                                    a = updX (x, u, u + 1) u ∈ Val
     (r ← CASX (x, u, v), ls) −
                              a
                              → (⊥, ls[r := true])                            (r ← FAIX (x), ls) −
                                                                                                 a
                                                                                                 → (⊥, ls[r := u])
                                                                                                    ′
                            a
                (P (t), ls) −
                            → (C, ls ′ )        a ∈ Actǫ                                  a
                                                                            (P (t), lst ) −
                                                                                          → L (C, ls ) a ∈ Actǫ
         Cli                   a                  ′
                                                                     Lib                a                    ′
                     (P, lst ) −
                               → t (P [t := C], ls )                          (P, lst ) −
                                                                                        → L,t (P [t := C], ls )

Figure 4: Program semantics, where IF = if B then C1 else C2 and WHILE =
          while B do C

    The rules in Fig. 4 allow for all possible values for any read. We constrain these values
with respect to a memory semantics (formalised by a t ), which is described for reads, writes
and updates in Section 3.3 and for abstract objects in Section 4. The combined semantics
brings together a client state γ and library state β as follows.
                                            ′     ′                                     ǫ       ′     ′
                                      ǫ
                            (P, lst ) −
                                      → t (P , lst )
                                                                              (P, lst ) −
                                                                                        → L,t (P , lst )

                     (P, lst , γ, β) =⇒ (P ′ , lst ′ , γ, β)             (P, lst , γ, β) =⇒ (P ′ , lst ′ , γ, β)
                                                                                                ′
                a
      (P, lst ) −
                →     ′     ′
                  t (P , lst )           γ, β a t γ ′ , β ′
                                                                                  a
                                                                        (P, lst ) −
                                                                                  →       ′
                                                                                    L,t (P , lst )           β, γ a t β ′ , γ ′
           (P, lst , γ, β) =⇒ (P ′ , lst ′ , γ ′ , β ′ )                     (P, lst , γ, β) =⇒ (P ′ , lst ′ , γ ′ , β ′ )
These rules ensure, for example, that a read only returns a value allowed by the underlying
memory model. In Section 4, we introduce additional rules so that the memory model also
contains actions corresponding to method calls on an abstract object.
    Note that the memory semantics (see Section 3.3 and Section 4) defined by γ, β a t γ ′ , β ′
assumes that γ is the state of the component being executed and β is the state of the context.
For a client step, we have that γ is the executing component state and β is the context state,
whereas for a library step, these parameters are swapped.

3.3. Memory Semantics. Next, we detail the modularised memory semantics, which
builds on an earlier monolithic semantics [DDDW20a], which is a timestamp-based revision
of an earlier operational semantics [DDWD19]. Our present extension is a semantics that
copes with client-library interactions in weak memory. Namely, it describes how synchro-
nisation (in our example release-acquire synchronisation) in one component affects thread
views in another component. The semantics accommodates both client synchronisation
affecting a library, and vice versa.
Component State. We assume Act denotes the set of actions. Following [DDDW20a],
each global write is represented by a pair (a, q) ∈ Act × Q, where a is a write action, and
8                                     S. DALVANDI AND B. DONGOL




q is a rational number that we use as a timestamp corresponding to modification order (cf.
[KDD+ 17, DSM18, PSN16]). The set of modifying operations within a component that
have occurred so far is recorded in ops ⊆ Act × Q. Unlike prior works, to accommodate
(abstract) method calls of a data structure, we record abstract operations in general, as
opposed to writes only.
       Each state must record the operations that are observable to each thread. To achieve
this, we use two families of functions from global variables to writes (cf. [PSN16, KHL+ 17]).
• A thread view function tviewt ∈ GVar → ops that returns the viewfront of thread t.
   The thread t can read from any write to variable x whose timestamp is not earlier than
   tviewt (x). Accordingly, we define, for each state γ, thread t and global variable x, the
   set of observable writes, where tst(w) = q denotes w’s timestamp:
                    γ.Obs(t, x) = {(a, q) ∈ γ.ops | var (a) = x ∧ tst(γ.tviewt (x)) ≤ q}
• A modification view function mvieww ∈ GVar → Act × Q that records the viewfront of
   write w, i.e., the viewfront of the thread that executed w immediately after w’s execution.
   We use mvieww to compute a new value for tviewt if a thread t synchronizes with w, i.e.,
   if w ∈ WR and another thread executes an e ∈ RA that reads from w.
The client cannot directly access writes in the library, therefore the thread view function
must map to writes within the same component. On the other hand, synchronisation
in a component can affect thread views in another (as discussed in Section 2), thus the
modification view function may map to operations across the system.
       Finally, our semantics maintains a set cvd ⊆ ops. In C11 RAR, each update action
occurs in modification order immediately after the write that it reads from [DDWD19]. This
property ensures the atomicity of updates. We disallow any newer modifying operation
(write or update) from intervening between any update and the write or update that it
reads from. As we explain below, covered writes are those that are immediately prior to
an update in modification order, and new write actions never interact with a covered write
(i.e. do not write immediately after them in the modification order).
Initialisation. Suppose GVar C = {x1 , ..., xn }, GVar L = {y1 , ..., yn′ }, LVar = {r1 , ..., rm },
ki , ki′ , li ∈ Val, and Init = x1 := k1 ; . . . , xn := kn ; [r1 := l1 ; ] . . . [rm := lm ; ], where we use
the notation [ri := li ; ] to mean that the assignment ri := li may optionally appear in Init.
Thus each shared variable is initialised exactly once and each local variable is initialised at
most once. The initial values of the state components are then as follows, where we assume
0 is the initial timestamp, t is a thread, xi ∈ GVar C and yi ∈ GVar L
                        [                                           [
          γInit .ops =       {(wr(xi , ki ), 0)}     βInit .ops =           {(wr(yi , ki′ ), 0)}
                    1≤i≤n                                         1≤i≤n′
      γInit .tviewt (xi ) = (wr(xi , ki ), 0)       βInit .tviewt (yi ) = (wr(yi , ki′ ), 0)
      γInit .cvd = βInit .cvd = ∅                   γInit .mviewxi = βInit .mviewyi =
                                                                     γInit .tviewt ∪βInit .tviewt
     The local state component of each thread must also be compatible with Init, i.e., for
each t if ri ∈ dom(lst(t)) we have that (lst (t))(ri ) = li provided ri := li appears in Init.
We let lst Init be the local state compatible with Init and let ΓInit = (lst Init , γInit , βInit ).
Transition semantics. The transition relation of our semantics for global reads and writes
is given in Fig. 5 and builds on an earlier semantics that does not distinguish the state of
the context [DDDW20a]. Each transition γ, β a t γ ′ , β ′ is labelled by an action a and thread
                VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                                 9




                                  rdA (x, n)}
                    a ∈ {rd(x, n),(               (w, q) ∈ γ.Obs(t, x)    wrval (w) = n
                                    γ.tviewt ⊗ γ.mview(w,q) if (w, a) ∈ WR × RA
                        tview′ =
                                    γ.tviewt [x := (w, q)]     otherwise
                                  (
                                    β.tviewt ⊗ γ.mview(w,q) if (w, a) ∈ WR × RA
                       ctview′ =
                                    β.tviewt                    otherwise
            Read
                                      a
                             γ, β         t   γ[tviewt := tview′ ], β[tviewt := ctview′ ]

                 a ∈ {wr(x, n), wrR (x, n)}  (w, q) ∈ γ.Obs(t, x) \ γ.cvd     fresh γ (q, q ′ )
            ′                ′             ′                    ′
         ops = γ.ops ∪ {(a, q )}    tview = γ.tviewt [x := (a, q )]    mview = tview′ ∪ β.tviewt
                                                                            ′
Write
                             a
                      γ, β       t   γ[tviewt := tview′ , mview(a,q′ ) := mview′ , ops := ops′ ], β

          a = updRA (x, m, n)     (w, q) ∈ γ.Obs(t, x) \ γ.cvd    wrval (w) = m          fresh γ (q, q ′ )
              ′                 ′           ′
           ops = γ.ops ∪ {(a, q()}      cvd = γ.cvd ∪ {(w, q)}         mview = tview ∪ ctview′
                                                                              ′         ′

                                                       ′
                                  γ.tviewt [x := (a, q )] ⊗ γ.mview(w,q) if w ∈ WR
                      tview′ =
                                  γ.tviewt [x := (a, q ′ )]                  otherwise
                                       (
                                          β.tviewt ⊗ γ.mview(w,q) if w ∈ WR
                            ctview′ =
                                          β.tviewt                    otherwise
Update-RA
                           tviewt := tview′ , mview(a,q′ ) := mview′ ,
                                                                      
              γ, β a t γ                                                 , β[tviewt := ctview′ ]
                           ops := ops′ , cvd := cvd′

                  a = updR (x, m, n)      (w, q) ∈ γ.Obs(t, x) \ γ.cvd     wrval (w) = m
                  fresh γ (q, q ′ ) ops′ = γ.ops ∪ {(a, q ′ )}    cvd′ = γ.cvd ∪ {(w, q)}
                     tview′ = γ.tviewt [x := (a, q ′ )]    mview′ = tview′ ∪ β.tviewt
 Update-Rel
            γ, β a t γ tviewt := tview′ , mview(a,q′ ) := mview′ , ops := ops′ , cvd := cvd′ , β
                                                                                           


   Figure 5: Transition relation for reads, writes and updates of the memory semantics

t and updates the target state γ (the state of component being executed) and the context
β.
Read transition by thread t. Assume that a is either a relaxed or acquiring read to
variable x, w is a write to x that t can observe (i.e., (w, q) ∈ γ.Obs(t, x)), and the value read
by a is the value written by w. Each read causes the viewfront of t to be updated. For an
unsynchronised read, tviewt is simply updated to include the new write. A synchronised
read causes the executing thread’s view of the executing component and context to be
updated. In particular, for each variable x, the new view of x will be the later (in timestamp
order) of either tviewt (x) or mvieww (x). To express this, we use an operation that combines
two views V1 and V2 , by constructing a new view from V1 by taking the later view of each
variable:
        V1 ⊗ V2 = λx ∈ dom(V1 ). if tst(V2 (x)) ≤ tst(V1 (x)) then V1 (x) else V2 (x)
Write transition by thread t. A write transition must identify the write (w, q) after
which a occurs. This w must be observable and must not be covered — the second condition
preserves the atomicity of read-modify-write (RMW) updates. We must choose a fresh
timestamp q ′ ∈ Q for a, which for a C11 state γ is formalised by fresh γ (q, q ′ ) = q <
q ′ ∧ ∀w′ ∈ γ.ops. q < tst(w′ ) ⇒ q ′ < tst(w′ ). That is, q ′ is a new timestamp for variable
x and that (a, q ′ ) occurs immediately after (w, q). The new write is added to the set ops.
10                                S. DALVANDI AND B. DONGOL




      We update γ.tviewt to include the new write, which ensures that t can no longer observe
any writes prior to (a, q ′ ). Moreover, we set the viewfront of (a, q ′ ) to be the new viewfront
of t in γ together with the thread viewfront of the environment state β. If some other thread
synchronises with this new write in some later transition, that thread’s view will become
at least as recent as t’s view at this transition. Since mview keeps track of the executing
thread’s view of both the component being executed and its context, any synchronisation
through this new write will update views across components.
Update (aka RMW) transition by thread t. These transitions are best understood
as a combination of the read and write transitions. As with a write transition, we must
choose a valid fresh timestamp q ′ , and the state component ops is updated in the same way.
State component mview includes information from the new view of the executing thread
t. As discussed earlier, in Update transitions it is necessary to record that the write that
the update interacts with is now covered, which is achieved by adding that write to cvd.
Finally, we must compute a new thread view, which is similar to a Read transition, except
that the thread’s new view always includes the new write introduced by the update.
Aside 1 (Generalisation to multiple components). The semantics can be extended to handle
multiple environment components, e.g., if a single client is interacting with multiple libraries.
Here, the context β in Fig. 5 would be generalised to a set of states S. Release-acquire
synchronisation in the component γ, would lead to an updates in the thread views for each
of the context states in S. This would lead to generalisation of the assertions in Section 5
and the refinement rules in Section 6.


                              4. Abstract object semantics
The rules in Fig. 5 provide a semantics for read, write and update operations for component
programs within an executing context and can be used to model clients and libraries under
RC11 RAR. These rules do not cover the behaviour of abstract objects, which we now
consider.
     There have been many different proposals for specifying and verifying concurrent objects
memory [KRV19, BDG13, EE19, KEEJ20, RDR+ 19, DDWD18, DJRA18], since there are
several different objectives that must be addressed. These objectives are delicately balanced
in linearizability [HW90], the most well-used consistency condition for concurrent objects.
Namely, linearizability ensures:
(1) The abstract specification is explainable with respect to a sequential specification.
(2) Correctness is compositional, i.e., any concrete execution of a system comprising two
     linearizable objects is itself linearizable.
(3) Correctness ensures contextual (aka observational) refinement, i.e., the use of a lineariz-
     able implementation within a client program in place of its abstract specification does
     not induce any new behaviours in the client program.
     There is however an inherent cost to linearizability stemming from the fact that the
effect of each method call must take place before the method call returns. In the context of
weak memory, this restriction induces additional synchronisation that may not necessarily
be required for correctness [SSO+ 10]. Therefore, over the years, several types of relaxations
to the above requirements have been proposed [KRV19, BDG13, EE19, KEEJ20, RDR+ 19,
DDWD18, DJRA18].
               VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                       11




     General data structures present many different design choices at the abstract level [RDR+ 19],
but discussing these now detracts from our main contribution, i.e., the integration and verifi-
cation of clients and libraries in a weak memory model. Therefore, we restrict our attention
to an abstract lock object, which is sufficient to highlight the main ideas. Locks have a clear
ordering semantics (each new lock acquire and lock release operation must have a larger
timestamp than all other existing operations) and synchronisation requirements (there must
be a release-acquire synchronisation from the lock release to the lock acquire).
     To enable proofs of contextual refinement (see Section 6), we must ensure corresponding
method calls return the same value at the abstract and concrete levels. To this end, we
introduce a special variable rval to each local state that stores the value that each method
call returns.
Example 1 (Abstract lock). Consider the specification of a lock with methods Acquire
and Release. Each method call of the lock is indexed by a subscript to uniquely identify the
method call. For the lock, the subscript is a counter indicating how many lock operations
have been executed and is used in the example proof in Section 5.
      a = l.acquire n ls′ = ls[rval := true]           a = l.release n ls′ = ls[rval := ⊥]
Acq                                              Rel
         (l.Acquire(), ls) −
                           →a
                               (true, ls′ )               (l.Release(), ls) −
                                                                            →a
                                                                                (⊥, ls′ )
Locks, by default are synchronising, i.e., in the memory semantics, a (successful) acquire
requires the operation to synchronise with the most recent lock release (in a manner con-
sistent with release-acquire semantics), so that any writes that are happens-before ordered
before the release are visible to the thread that acquires the lock. The initial state of an
abstract lock l, γInit , is given by:
       γInit .ops = {(l.init0 , 0)}    αInit .tviewt (l) = (l.init0 , 0)   αInit .cvd = ∅
We also obtain the rules below, where α is the state of the lock and γ is the state of the
client.
       To record the thread that currently owns the lock, we derive a new action, b, from the
action a of the program semantics. Action (w, q) represents the method that is observed
by the acquire method, which must be an operation in α.ops such that q has the maximum
timestamp for l (i.e., q = maxTS (α.ops|l )). The new timestamp q ′ must be larger than q.
We create a new component state α′ from α by (1) inserting (b, q ′ ) into α.ops; (2) updating
tviewt to tview′ , where tview′ synchronises with the previous thread view in α to include
information from the modification view of (w, q), and updates t’s view of l to include the new
operation (b, q ′ ); (3) updating the contextual thread view for t to ctview′ , where ctview′
synchronises with the previous thread view in the context state γ to include information from
the modification view of (w, q); and (4) updating the modification view for the new operation
(b, q ′ ) to mview′ , where mview′ contains the view of t. Finally, the context state γ ′ updates
the thread view of t to ctview′ since synchronisation with a release may cause the view to
be updated.
       A lock release, simply introduces a new operation with a maximal timestamp, provided
that the thread executing the release currently holds the lock.


                               5. Client-library verification
Having formalised the semantics of clients and libraries in a weak memory setting, we
now work towards verification of (client) programs that use such libraries. We develop
12                                    S. DALVANDI AND B. DONGOL



              a = l.acquire n   b = l.acquire n (t)   (w, q) ∈ α.ops        w ∈ {l.init0, l.release n−1 }
                                         q = maxTS (α.ops|l )      q < q′
              ops′ = α.ops ∪ {(b, q ′ )}   mview′ = tview′ ∪ ctview′          cvd′ = σ.cvd ∪ {(w, q)}
                    ′                      ′                             ′
              tview = α.tviewt [l := (b, q )] ⊗ α.mview(w,q) ctview = γ.tviewt ⊗ α.mview(w,q)
 Acquire
                                 ops := ops′ , tviewt := tview′ ,
                                                                     
                     α, γ a t α                                         , γ[tviewt := ctview′ ]
                                 mview(b,q′ ) := mview′ , cvd := cvd′

             a = l.release n w = l.acquire n−1 (t) (w, q) ∈ α.ops q = maxTS (α.ops|l ) q < q ′
                          ops′ = α.ops ∪ {(a, q ′ )} tview′ = α.tviewt [x := (a, q ′ )]
                                         mview = tview′ ∪ γ.tviewt
                                                  ′
     Release
                     α, γ a t α ops := ops′ , tviewt := tview′ , mview(a,q′ ) := mview′ , γ
                                                                                       


                  Figure 6: Operational semantics for lock acquire and release

an assertion language for specifying client-library states in Section 5.1, a Hoare logic for
reasoning about client-library programs in Section 5.2 and an example verification of a client
program using a lock library in Section 5.3.

5.1. Assertion language. In our proof, we use observability assertions, which describe
conditions for a thread to observe a specific value for a given variable. Unlike earlier works,
our operational semantics covers clients and their libraries, and hence operates over pairs
of states.
Possible observation, denoted hx = uit , means that thread t may observe value u for
x [DDDW20a]. We extend this concept to cope with abstract method calls as follows. In
particular, for an object o and method m, we use ho.mit to denote that thread t can observe
o.m.
                      hx = nit (σ) ≡ ∃w ∈ σ.Obs(t, x). wrval (w) = n
                        ho.mit (σ) ≡ ∃q. (o.m, q) ∈ σ.ops ∧ q ≥ σ.tviewt (o)
To distinguish possible observation in clients and libraries, we introduce the following nota-
tion, where γ and β are the client and library states, respectively, and p is either a valuation
(i.e., x = n) or an abstract method call (i.e., o.m):
                   hpiC
                      t (γ, β) ≡ hpit (γ)                      hpiL
                                                                  t (γ, β) ≡ hpit (β)

Definite observation, denoted [x = u]t , means that thread t can only see the last write
to x, and that this write has written value u. Recall that each write is a pair containing a
write event and a timestamp. Let W be a set of writes with a unique timestamp for each
x, i.e., (W|x )−1 is a function. We define the last write to x in a set of writes W as:
                                last(W, x) ≡ (W|x )−1 (maxTS (W|x ))
We define the definite observation of a view function, view with respect to a set of writes
as follows:
            dview (view, W, x) = n ≡ view(x) = last(W, x) ∧ wrval (last (W, x)) = n
The first conjunct ensures that the viewfront of view for x is the last write to x in W , and
the second conjunct ensures that the value written by the last write to x in W is n. For a
              VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                        13




variable x, thread t and value n, we define:
                    [x = n]t (σ) ≡ dview (σ.tviewt , σ.ops ∩ W, x) = n
The extension of definite observation assertions to abstract method calls is straightforward
to define. Namely we have:
      [o.m]t (σ) ≡ σ.tviewt (o) = maxTS (σ.ops|o ) ∧ (o.m, maxTS (σ.ops|o )) ∈ σ.ops
As with possible observations, we lift definite observation predicates to state spaces featuring
clients and libraries:
                [p]C
                   t (γ, β) ≡ [p]t (γ)                  [p]L
                                                           t (γ, β) ≡ [p]t (β)

Conditional observation, denoted hx = ui[y = v]t , means that if thread t synchronises
with a write to variable x with value u, it must subsequently observe value v for y. For
variables x and y, thread t and values u and v, we define:
        hx = ui[y = v]t (σ)
    ≡   ∀w ∈ σ.Obs(t, x). wrval (w) = u ⇒ act(w) ∈ WR ∧ dview (σ.mvieww , σ.ops, y) = v
This is a key assertion used in message passing proofs [DDDW20a, KDD+ 17] since it guar-
antees an observation property on a variable, y, via a synchronising read of another variable,
x.
     As with possible and definite assertions, conditional assertions can be generalised to
objects and extended to pairs of states describing a client and its library. However, un-
like possible and definition observations assertions, conditional observation enables one to
describe view synchronisation across different states. For example, consider the following,
which enables conditional observation of an abstract method to establish a definite observa-
tion assertion for the thread view of the client. We assume a set Sync ⊆ Act that identifies
a set of synchronising abstract actions.
   ho.miL [y = v]C
                 t (γ, β) ≡    ∀q. (o.m, q) ∈ β.ops ∧ q ≥ β.tviewt (o) ⇒
                                        o.m ∈ Sync ∧ dview (β.mview(o.m,q) , γ.ops, y) = v
It is possible to define other variations, e.g., conditional observation synchronisation from
clients to libraries, but we leave out the details of these since they are straightforward to
construct.
Covered operations, denoted Co.m , holds iff all but the last operation m of the object o is
covered. Recall from the Acquire rule that a new acquire operation causes the immediately
prior (release) operation l.releasen−1 to be covered so that no later acquire can be inserted
between l.releasen−1 and the new acquire. To reason about this phenomenon over states,
we use:
          Co.m (σ) ≡ ∀(w, q) ∈ σ.ops|o \ σ.cvd. w = o.m ∧ q = maxTS (σ.ops|o )
where σ.ops|o is the set of operations over object o.
Hidden value, denoted Ho.m , states that the operation o.m exists, but all of these are
hidden from interaction. In proofs, such assertions limit the values that can be returned.
     Ho.m (σ) ≡ (∃q. (o.m, q) ∈ σ.ops) ∧ (∀q. (o.m, q) ∈ σ.ops ⇒ (o.m, q) ∈ σ.cvd)
Both covered and hidden-value assertions can be lifted to pairs of states and can be used to
reason about standard writes, as opposed to method calls (details omitted). For instance,
we can define CC                        L
               x (γ, β) ≡ Cx (γ) and Cx (γ, β) ≡ Cx (β).
14                                     S. DALVANDI AND B. DONGOL




5.2. Hoare Logic and Owicki-Gries for C11 and Abstract Objects. Since we have
an operational semantics, the assertions in Section 5.1 can be integrated into standard
Hoare-style proof calculus in a straightforward manner [DDDW20a, DDD20]. The only
differences are the state model (which is a weak memory state, as opposed to mappings
from variables to values) and the atomic components (which may include reads of global
variables, and, in this paper, abstract method calls).
     Following [DDDW20a, DDD20], we let ΣC and ΣL to be the set of all possible global
state configurations of the client and library, respectively and let ΣC11 = (LVar → Val ) ×
ΣC ×ΣL be the set of all possible client-library C11 states. Predicates over ΣC11 are therefore
of type ΣC11 → B. This leads to the following definition of a Hoare triple, which we note is
the same as the standard definition — the only difference is that the state component is of
type ΣC11 .
Definition 1. Suppose p, q ∈ ΣC11 → B, P ∈ Prog and E = λt : Tid . ⊥. The semantics of
a Hoare triple under partial correctness is given by:
        {p}Init{q} = q(ΓInit )
     {p}Init; P {q} = ∃r. {p}Init{r} ∧ {r}P {q}
          {p}P {q} = ∀lst, γ, β, lst ′ , γ ′ , β ′ .
                           p(lst, γ, β) ∧ ((P, lst , γ, β) =⇒∗ (E, lst ′ , γ ′ , β ′ )) ⇒ q(lst ′ , γ ′ , β ′ )
     This definition (in the context of RC11 [LVK+ 17]) allows all standard Hoare logic
rules for compound statements to be reused [DDDW20a]. Due to concurrency, follow-
ing Owicki and Gries, one must prove local correctness and interference freedom (or sta-
bility) [OG76, DDDW20a, DDD20, LV15]. This is also defined in the standard manner.
Namely, a statement R ∈ ACom with precondition pre(R) (in the standard proof outline)
does not interfere with an assertion p iff {p ∧ pre(R)} R {p}. Proof outlines of concurrent
programs are interference free if no statement in one thread interferes with an assertion in
another thread.
     The only additional properties that one must define are on the interaction between
atomic commands and predicates over assertions defined in Section 5.1. A collection of
rules for reads, writes and updates have been given in prior work [DDD20, DDDW20a].
Here, we present rules for method calls of the abstract lock object defined in Example 1.
     In proofs, it is often necessary to reason about particular versions of the lock (i.e., the
lock counter). Therefore, we use l.Acquire(v) and l.Release(v) to denote the transitions
that set the lock version to v. Also note that in our example proof, it is clear from context
whether an assertion refers to the client or library state, and hence, for clarity, we drop the
superscripts C and L as used in Section 5.1.
     The lemma below has been verified in Isabelle/HOL.
Lemma 1. Each of the following holds, where the statements are decorated with the iden-
tifier of the executing thread, assuming m ∈ {Acquire, Release} and t 6= t′
                    {Hl.releaseu } l.Acquire(v)t {v > u + 1}                                             (5.1)
                    {Hl.releaseu } l.m(v)t {Hl.releaseu }                                                (5.2)
                    {[l.release u ]t } l.Acquire(v)t {[l.acquire u+1 ]t }                                (5.3)
                    {[x = u]t } l.m(v)t′ {[x = u]t }                                                     (5.4)
                    {hl.release u i[x = n]t } l.Acquire(v)t {v = u + 1 ⇒ [x = n]t }                      (5.5)
                    
                      ¬hl.release u it′ ∧ [x = v]t l.Release(u)t {hrelease u i[x = v]t′ }                (5.6)
                VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                                   15




                             Init: d1 := 0; d2 := 0; l.init();
                         {Inv ∧ [d1 = 0]1 ∧ [d2 = 0]1 ∧ [d1 = 0]2 ∧ [d2 = 0]2 }
                 Thread 1                             Thread 2
                 1 : {Inv ∧ P1 } if l.Acquire()       1 : {Inv ∧ Q1 } if l.Acquire(rl)
                 2 : {Inv ∧ P2 } d1 := 5;             2 : {Inv ∧ Q2 } r1 ← d1 ;
                 3 : {Inv ∧ P3 } d2 := 5;             3 : {Inv ∧ Q3 } r2 ← d2 ;
                 4 : {Inv ∧ P4 } l.Release()          4 : {Inv ∧ Q4 } l.Release()
                           5 : {(r1 = 0 ∧ r2 = 0) ∨ (r1 = 5 ∧ r2 = 5)}
where assuming Ppo = (pc2 = 1 ⇒ ¬hl.release 2 i2 ) ∧ Hl.init 0 , we have
 P1 =[d1 = 0]1 ∧ [d2 = 0]1 ∧               Q′1 = 
                                                 pc1 = 5 ∧ hl.release 2 i[d1 = 5]2 ∧ hl.release 2 i[d
                                                                                                     2 = 5]2
     (pc2 = 1 ⇒ [l.init0]1 ∧ [l.init0 ]2 )         pc1 ∈
                                                       / {2, 3, 4} ⇒
                                           Q1 =
     ∧(pc2 ∈ {2, 3, 4} ⇒ Cl.acquire1 )                  ([l.init0 ]2 ∧ [d1 = 0]2 ∧ [d2 = 0]2 ) ∨ Q′1
 P2 =[d1 = 0]1 ∧ [d2 = 0]1 ∧ Ppo                 ∧ (pc1 = 1 ⇒ [l.init0 ]1 ) ∧ (pc1 = 5 ⇒ Hl.init 0 )
 P3 =[d1 = 5]1 ∧ [d2 = 0]1 ∧ Ppo           Q2 = (rl = 1 ⇒ [d1 = 0]2 ∧ [d2 = 0]2 )
 P4 =[d1 = 5]1 ∧ [d2 = 5]1 ∧ Ppo                  ∧ (rl = 3 ⇒ [d1 = 5]2 ∧ [d2 = 5]2 )
                                           Q3 = (rl = 1 ⇒ r1 = 0 ∧ [d2 = 0]2 )
                                                 ∧ (rl = 3 ⇒ r1 = 5 ∧ [d2 = 5]2 )
                                           Q4 = (rl = 1 ⇒ r1 = 0 ∧ r2 = 0)
                                                 ∧ (rl = 3 ⇒ r1 = 5 ∧ r2 = 5)

                         Figure 7: Proof outline for lock-synchronisation


5.3. Example Client-Library Verification. To demonstrate use of our logic in verifica-
tion, consider the simple program in Fig. 7, which comprises a lock object l and shared
client variables d1 and d2 (both initially 0). Thread 1 writes 5 to both d1 and d2 after
acquiring the lock while thread 2 reads d1 and d2 (into local registers r1 and r2 ) also after
acquiring the lock.
     Under SC, it is a standard exercise to show that the program terminates with r1 = r2
and ri = 0 or ri = 5. We show that the lock specification in Section 4 together with the
assertion language from Section 5.1 and Owicki-Gries logic from Section 5.2 is sufficient to
prove this property. In particular, the specification guarantees adequate synchronisation so
that if the Thread 2’s lock acquire sees the lock release in Thread 1, it also sees the writes
to d1 and d2 . The proof relies on two distinct types of properties:
• Mutual exclusion: As in SC, no two threads should execute their critical sections at the
   same time.
• Write visibility: If thread 1 enters its critical section first, its writes to both d1 and d2
   must be visible to thread 2 after thread 2 acquires the lock. Note that this property is
   not necessarily guaranteed in a weak memory setting since all reads/writes to d1 and d2
   in Fig. 7 are relaxed.
     Our proof is supported by the following global invariant:
                    Inv ≡ ¬(pc1 ∈ {2, 3, 4} ∧ pc2 ∈ {2, 3, 4}) ∧ (rl ∈ {1, 3})
The first conjunct establishes mutual exclusion, while the second ensures that the lock
version written by the acquire in thread 2 is either 1 or 3, depending on which thread enters
its critical section first. The main purpose of the definite and possible observation assertions
is to establish Q′1 (which appears in Q1 ) using rule (5.6). This predicate helps establish
[d1 = 5]2 and [d2 = 5]2 in thread 2 whenever thread 2 acquires the lock after thread 1. The
16                                 S. DALVANDI AND B. DONGOL




most critical of these assertions is Q1 , which states that if thread 1 is not executing its
critical section then we either have
• [l.init0 ]2 ∧ [d1 = 0]2 ∧ [d2 = 0]2 , i.e., thread 2 can definitely see the lock initialisation and
   definitely observe both d1 and d2 to have value 0, or
• Q′1 holds, i.e., thread 1 has released the lock and has established a state whereby if thread
   2 acquires the lock, it will be able to establish the definite value assertions [d1 = 5]2 and
   [d2 = 5]2 .
Note that Q1 also includes a conjunct pc1 = 5 ⇒ Hl.init 0 , which ensures that if thread
2 enters its critical section after thread 1 has terminated, then it does so because it sees
l.release 2 (as opposed to l.init 0 ). This means that we can establish rl = 1 ⇒ [d1 = 0]2 ∧[d2 =
0]2 (i.e., thread 2 has acquired the lock first) and rl = 3 ⇒ [d1 = 5]2 ∧ [d2 = 5]2 (i.e., thread
2 has acquired the lock second) in Q2 . Using these definite value assertions, we can easily
establish that the particular values that are loaded into registers r1 and r2 . The lemma has
been verified in Isabelle/HOL.
Lemma 2. The proof outline in Fig. 7 is valid.


                                 6. Contextual Refinement
We now describe what it means to implement a specification so that any client property
that was preserved by the specification is not invalidated by the implementation. We define
and prove contextual refinement directly, i.e., without appealing to external correctness con-
ditions over libraries, cf. linearizability [HW90, DDWD18, GY11, DJRA18, FORY10]. We
present our refinement theory in Section 6.1, including a proof technique based on forward
simulation. In Sections 6.2 and 6.3, we provide two examples of contextual refinement of
the abstract lock object introduced in Section 4.

6.1. Refinement and Simulation for Weak Memory. Since we have an operational
semantics with an interleaving semantics over weak memory states, the development of our
refinement theory closely follows the standard approach under SC [dRE98]. Suppose P
is a program with initialisation Init. An execution of P is defined by a possibly infinite
sequence Π0 Π1 Π2 . . . such that
(1) each Πi is a 4-tuple (Pi , lsi , γi , βi ) comprising a program, local state, global client state
     and global library state, and
(2) (ls0 , γ0 , σ0 ) = (ls Init , γInit , σInit ), and
(3) for each i, we have Πi =⇒ Πi+1 as defined in Section 3.2.
A client trace corresponding to an execution Π0 Π1 Π2 . . . is a sequence ct ∈ Σ∗C such that
ct i = (π2 (Πi )|C , π3 (Πi )), where πn is a projection function that extracts the nth component
of a given tuple and ls|C restricts the given local state ls to the variables in LVar C . Thus
each ct i is the global client state component of Πi .
      After a projection, the concrete implementation may contain (finite or infinite) stut-
tering [dRE98], i.e., consecutive states in which the client state is unchanged. We let
rem stut(ct) be the function that removes all stuttering from the trace ct, i.e., each consec-
utively repeating state is replaced by a single instance of that state. We let TrSF (P ) denote
the set of stutter-free traces of a program P , i.e., the stutter-free traces generated from the
set of all executions of P .
              VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                          17




     Below we refer to the client that uses the abstract object as the abstract client and
the client that uses the object’s implementation as the concrete client. The notion of
contextual refinement that we develop ensures that a client is not able to distinguish the
use of a concrete implementation in place of an abstract specification. In other words, each
thread of the concrete client should only be able to observe the writes (and updates) in the
client state (i.e., γ component) that the thread could already observe in a corresponding
of the client state of the abstract client. First we define trace refinement for weak memory
states.
Definition 2 (State and Trace Refinement). We say a concrete state γC is a refinement of
an abstract state γA , denoted (lsA , γA ) ⊑ (lsC , γC ) iff lsA = lsC , γA .cvd = γC .cvd and for
all threads t and x ∈ GVar , we have γC .Obs(t, x) ⊆ γA .Obs(t, x). We say a concrete trace
ct is a refinement of an abstract trace at, denoted at ⊑ ct, iff ct i ⊑ at i for all i.
    This now leads to a natural trace-baseed definition of contextual refinement.
Definition 3 (Program Refinement). A concrete program PC is a refinement of an abstract
program PA , denoted PA ⊑ PC , iff for any (stutter-free) trace ct ∈ TrSF (PC ) there exists a
(stutter-free) trace at ∈ TrSF (PA ) such that at ⊑ ct.
     Finally, we obtain a notion of contextual refinement for abstract objects. Suppose
P is a program with holes. We let P [O] be the program in which the holes are filled
with the operations from object O. Note that O may be an abstract object, in which
case execution of each method call follows the abstract object semantics (Section 4), or a
concrete implementation, in which case execution of each method call follows the semantics
of reads, writes and updates (Section 3.2).
Definition 4 (Contextual refinement). We say a concrete object CO is a contextual re-
finement of an abstract object AO iff for any client program C, we have C[AO] ⊑ C[CO].
     To verify contextual refinement, we use a notion of simulation, which once again is a
standard technique from the literature. The difference in a weak memory setting is the fact
that the refinement rules must relate more complex configurations, i.e., tuples of the form
(P, lst , γ, α).
     The simulation relation, R, relates triples (als, γA , α), comprising an abstract local state
als, client state γA and library state α, with triples (cls, γC , β) comprising a concrete local
state cls, a client state γC and concrete library state β. The simulation condition must
ultimately ensure (als|C , γA ) ⊑ (cls|C , γC ) at each step as defined in Definition 2. However,
since client synchronisation can affect the library state, a generic forward simulation rule is
non-trivial to define since it requires one to describe how clients steps affect the simulation
relation. We therefore present a simpler use case for libraries that are used by clients that
do not perform any synchronisation outside the library itself (e.g., the client in Fig. 7). If
Π = (P, lst, γ, α), we let state(Π) = (lst, γ, α) be the state corresponding to Π.
Definition 5 (Forward simulation for synchronisation-free clients). For an abstract object
AO and a concrete object CO and a client C that only synchronises through AO (and CO),
C[AO] ⊑ C[CO] holds if there exists a relation R such that
(1) R((als, γA , α), (cls, γC , β)) ⇒
       als|C = cls|C ∧
                                                                          (client observation)
       ∀t, x. γC .Obs(t, x) ⊆ γA .Obs(t, x) ∧ als(t)(rval) = cls(t)(rval)
(2) R(state(ΩInit ), state (ΠInit ))                                           (initialisation)
18                               S. DALVANDI AND B. DONGOL



Init:   glb = 0
                                                 Init:   nt = 0,   sn = 0
Acquire():
 1: do do r ←A glb until even(r) ;               Acquire():
 2:       loc ← CASRA (glb, r, r+1)               1: m t ← FAIRA (nt)
 3: until loc                                     2: do s n ←A sn until m t = s n
Release():                                       Release():
 1: glb :=R r + 2                                 1: sn :=R s n + 1

  Figure 8: Sequence lock in RC11-RAR                Figure 9: Ticket lock in RC11-RAR
(3) For any concrete configurations Π, Π and abstract configuration Ω, if Π =⇒ Π′ via a
                                            ′

    step corresponding to CO, and R(state(Ω), state(Π)), then either
    • R(state(Ω), state (Π)), or                                             (stuttering step)
    • there exists an abstract configuration Ω such that Ω =⇒ Ω and R(state(Ω′ ), state(Π′ )).
                                              ′                  ′

                                                                        (non-stuttering step)
Theorem 1. If R is a forward simulation between AO and CO, then for any client that
only synchronises through AO (and CO) we have C[AO] ⊑ C[CO].


6.2. Sequence Lock. The first refinement example (Fig. 8) is a sequence lock, which
operates over a single shared variable (glb). The Acquire operation returns true if, and
only if, the CAS on line 2 is successful. Therefore, in order to prove the refinement, we will
need to prove that whenever the CAS operation is successful, the abstract object can also
successfully acquire the lock maintaining the simulation relation. Also, the read on line 1
and the unsuccessful CAS are stuttering steps and we need to show that when those steps
are taken the abstract state remains unchanged and the new concrete state preserves the
simulation relation. The Release operation contains only one releasing write on variable glb,
which is considered to be a refining step. It is straightforward to show that this operation
refines the abstract object release operation. The following proposition has been verified in
Isabelle/HOL.
Proposition 1. For synchronisation-free clients, there exists a forward simulation between
the abstract lock object and the sequence lock.


6.3. Ticket Lock. Our second refinement example (Fig. 9) is the ticket lock. The ticket
lock has two shared variables nt (next ticket) and sn (serving now). Invocation of Acquire
loads the next available ticket into a local register (m t) and increases the value of nt by
one using a fetch-and-increment (FAI) operation. It then enters a busy loop and reads sn
until it sees its own ticket value in sn before it can enter its critical section.
     If the read on line 2 of the Acquire operation reads from a write whose value is equal
to the value of m t, then the lock is acquired. Therefore we will need to show that if this
situation arises, the abstract lock object can also take a step and successfully acquire the
lock. We consider the FAI operation on line 1 and the read on line 2 if it reads a value
that is not equal to m t to be a stuttering step. We prove that each of the stuttering and
non-stuttering steps preserves the simulation relation. Similar to the previous example, the
Release operation consists of only one releasing write to variable sn and it is straightforward
to show that this operation refines the abstract release operation. This proof has been
mechanised in Isabelle/HOL.
             VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                     19




Proposition 2. For synchronisation-free clients, there exists a forward simulation between
the abstract lock object and the ticket lock.


                           7. Concurrent Data Structures
The modelling approach in Section 4 provides a flexible framework for specifying abstract
objects and enables specification of synchronised and unsynchronised method calls (as de-
tailed in Fig. 2). We now show that the framework also provides a mechanism for spec-
ifying concurrent objects whose linearisation order is different from real-time order (cf.
[RDR+ 19, DJRA18, KEEJ20, EE19]). Such specifications are a natural fit with the weak
memory operational semantics where new writes may be introduced in the “middle” of
modification order [DDWD19, DSM18, KHL+ 17].

7.1. Specifying C11-Style Concurrent Data Structures. As with ordinary read, write
and RMW operations, there are two separate aspects to consider.
(1) The introduction of operations into modification order. As with the operational C11
    semantics [DDDW20a, DDWD19], we allow operations to be introduced into the middle
    of modification order (under some restrictions on thread views).
(2) The release-acquire synchronisation guarantees induced by the operations. Concurrent
    data structures are to be implemented as concurrent libraries, and hence induce inter-
    thread synchronisation across both the library and the client.
     As with writes, timestamps may be used to define a linear order of the method calls of
the object in question. However, different threads may have different views of the object
being implemented, and this phenomenon must be supported by the object specification.
To exemplify our approach, a queue and a stack specification are. given below
Example 2 (Queue specification). Consider a timeline corresponding to the state of a
shared queue as depicted below:
                                  t1                t2
                             qinit() enq(1)    enq(2)    deq(v)
where the viewfront of threads t1 and t2 are depicted above the timeline and the abstract op-
erations executed below the timeline. The state can be generated by executing the operations
in the following temporal order:
(1) Thread t2 executes enq(2), and hence t2 ’s view of the queue is that of enq(2).
(2) Thread t1 executes enq(1), but since it has not yet “seen” enq(2), it may choose a
     timestamp that is smaller than the timestamp of enq(2) for enq(1).
(3) Thread t2 executes a dequeue, deq(v), for some yet to be determined value v. Since t2
     also executed enq(2), the timestamp of the deq(v) must be larger than that of enq(2).
     One option for the execution to continue in a sensible manner is to ensure that the
effect of the dequeue is communicated to all other threads so that their views of the object
are updated. Thus, if t1 were to perform a new method call, this method call would appear
after deq(v) (with v = 1). However, imposing such a communication requirement in the
abstract specification induces additional (and potentially unnecessary) synchronisation in
an implementation. For instance, a sensible continuation of the timeline in above would be
for thread t1 to introduce additional enqueue operations between enq(1) and deq (v) (with
20                                                      S. DALVANDI AND B. DONGOL




v = 1). In fact, the only continuations that are disallowed is the introduction of new
dequeue operations between enq(1) and deq(v) (with v = 1) and new enqueue operations
before enq(1).
     Our formal specification builds on this idea. We assume a predicate, matched, that
stores pairs of timestamps corresponding to enqueues and dequeues. For any (ts, ts′ ) ∈
matched, the timestamp ts corresponds to an enqueue that is removed from the queue by the
dequeue with timestamp ts′ . To ensure first-in-first-out behaviours, for any pair (ts, ts′ ) ∈
matched, it is illegal for a dequeue to be introduced between ts and ts′ . Moreover, when a
dequeue matches an operation, it must match with the first unmatched enqueue that has a
smaller timestamp than the dequeue (or empty if no such enqueue exists). Below, we present
a specification of enqueue and dequeue operations. We let supp(R) = dom(R) ∪ ran(R) for
a relation R.
                             tst(α.tviewt (q)) < ts ′   ops′ = α.ops ∪ {(a, ts ′ )}
                     (∀(ww , tt) ∈ α.ops. ww ∈ Enq ∧ tt > ts ′ ⇒ tt ∈
                                                                    / dom(α.matched))
           (∀(ww , tt) ∈ α.ops. tt > ts ′ ⇒ ww 6= q.deqempty )   tview′ = α.tviewt [q := (a, ts ′ )]
Enq-Base
                                                            a,ts ′
                                                α                    t   α[ops := ops′ , tviewt := tview′ ]
                                                                                                                                   a,ts ′
                                                                                                                                   ′
                                           a,ts ′
                                                                                                          a = q.enquR  α        t α
           a = q.enqu                 α                 t    α′                                                ′    ′
                                                                                                         mview = α .tviewt ∪ γ.tviewt
Enq-Rlx                                                                       Enq-Sync
                              a                                                                            a
                  α, γ            t    α′ , γ                                                      α, γ        t   α′ [mview(a,ts ′ ) := mview′ ], γ
                                     max(tst(α.tviewt (q)), ts) < ts ′
                 ops′ = α.ops ∪ {(a, ts ′ )}  (w, ts) ∈ α.ops     ts ∈ / dom(α.matched)
                   (∀(ww , tt) ∈ α.ops. ww ∈ Enq ∧ tt < ts ⇒ tt ∈ dom(α.matched))
                 (∀tt ′ ∈ ran(α.matched). ts′ > tt ′ )  tview′ = α.tviewt [q := (a, ts ′ )]
Deq-Base
               a,ts ′ ,w,ts
           α                  t       α[ops := ops′ , tviewt := tview′ , matched := matched ∪ {(ts, ts ′ )}]
                              [A]                                              a,ts ′ ,w,ts                                 [R]
               a = q.dequ                 u 6= empty                      α                    t    α′         w = q.enq u        (w, a) ∈
                                                                                                                                         / R×A
Deq-NE-Rlx
                                                                                       a            ′
                                                                               α, γ        t       α ,γ
                                                               ′                               a,ts ′ ,w,ts
                     a = q.dequA   u 6= empty     α         t α    w = q.enquR
                     ′    ′                               ′
                tview = α .tviewt ⊗ α.mview(w,ts)   ctview = γ.tviewt ⊗ α.mview(w,ts)
Deq-NE-Sync
                                                    a
                                      α, γ              t    α′ [tviewt := tview′ ], γ[tviewt := ctview′ ]
            a = q.deqempty      tst(α.tviewt (q)) < ts ′    ops′ = α.ops ∪ {(a, ts ′ )}
                                       ′
           (∀(ww , tt) ∈ α.ops. tt < ts ⇒ tt ∈ supp(σ.matched) ∨ ww = q.deqempty )
                                 tview′ = α.tviewt [q := (a, ts ′ )]
Deq-Emp
                                            a
                                  α, γ          t       α[ops := ops′ , tviewt := tview′ ], γ

     Rules Enq-Base and Deq-Base define the basic rules for enqueues and dequeues,
factoring out the common aspects of relaxed and synchronising operations. Enq-Base helps
determine an appropriate timestamp for a new (enqueue) operation and advances the thread
view of the executing thread to this timestamp. For a relaxed enqueue, Enq-Rlx, no other
state changes are necessary. However, for an acquiring enqueue, the modification view of
the new operation must be updated as defined by Enq-Sync.
              VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                                                   21




     Deq-Base is similar to Enq-Base, but it also makes the enqueue that the dequeue
matches with explicit. This is used in rule Deq-NE-Sync to update thread views of both the
library and the client to be consistent with the corresponding (releasing) enqueue operation.

Example 3 (Stack specification). The specification of a stack is designed to ensure last-
in-first-out order. We motivate the main ideas of the specification below. Consider the
following timeline corresponding to the state of a shared stack:
                                   t3      t2        t1
                                             sinit() push(2) push(1)
In this state, thread t1 ’s viewfront is at push(1), thread t2 ’s viewfront is at push(2) and thread
t3 ’s viewfront is at sinit(). Consider a pop operation performed by each of the threads —
these operations must be consistent with their viewfronts. For the state above, a pop executed
by t3 may return either empty, 1 or 2, a pop executed by thread t2 may return either 2 or 1,
and a pop executed by thread t1 must return 1.
      Suppose t3 performs a pop, and that the pop returns the value 2. In this case, the state
would be updated as follows:
                                            t2        t3          t1
                                     sinit() push(2)           pop(2)    push(1)
Note that t3 ’s viewfront must include push(2), so pop(2) must occur after push(2). However,
pop(2) must not occur after push(1); otherwise the popped value would be inconsistent with
the history of a sequential stack since the history push(2) push(1) pop(2) is invalid.
     Now consider an alternative execution starting from the first state shown above, where
thread t1 performs a pop. The post state following this execution is given below:
                                 t3      t2                 t1
                                     sinit() push(2) push(1)              pop(1)
Now suppose t2 performs a pop. This pop must return the value 2 since push(1) has already
been popped and t2 ’s viewfront includes push(2). Moreover, since push(1) and pop(1) are
already matched, it would be illegal for the pop by t2 to be introduced between push(1) and
pop(1). However, it is acceptable to introduce the pop before push(1) or after pop(1) since
this histories push(2) pop(2) push(1) pop(1) and push(2) push(1) pop(1) pop(2) are both valid.
     These ideas are captured by the semantics below. Rules Push-Base and Pop-Base
capture the basic ordering requirements and thread view updates. Rules Push-Rlx and
Push-Sync define relaxed and (releasing) pushes, respectively, while rules Pop-Rlx and
Pop-Sync define unsynchronised and synchronised pops, respectively.
                           tst(α.tviewt (q)) < ts ′   ops′ = α.ops ∪ {(a, ts ′ )}
            (∀(tt, tt ) ∈ α.matched. ts < tt ∨ ts > tt′ )
                    ′                  ′          ′
                                                            tview′ = α.tviewt [q := (a, ts ′ )]
Push-Base
                                         a,ts ′
                                    α             t   α[ops := ops′ , tviewt := tview′ ]
                                                                                                       ′    a,ts ′
                                         a,ts ′
                                                                            a = q.push(u)R   α      t α
            a = q.push(u)           α             t   α′                            ′      ′
                                                                              mview = tview ∪ γ.tviewt
Push-Rlx                                                    Push-Sync
                            a                                                    a
                    α, γ        t   α′ , γ                                α, γ       t   α′ [mview(a,ts ′ ) := mview′ ], γ
22                                          S. DALVANDI AND B. DONGOL




Algorithm 1 Treiber stack with relaxed and release-acquire memory accesses
 1: procedure Init                               10: function PopA
 2:    Top := null;                              11:    repeat
                    R                            12:        repeat
 3: procedure Push (v)
 4:    n := new(node);                           13:           top ←A Top ;
 5:    n.val := v ;                              14:        until top 6= null ;
 6:    repeat                                    15:        nTop ← top.nxt ;
 7:       top ←A Top ;                           16:    until CASR (& Top, top, nTop)
 8:       n.nxt := top ;                         17:    return top.val ;
 9:    until CASR (& Top, top, n)
                  a,ts ′
              α        t α
                          ′
                               (w, ts) ∈ α.ops   ts ∈
                                                    / dom(α.matched)   ts < ts ′
                    ′′                              ′′   ′    ′′
           (∀(ww, ts ) ∈ α.ops. ww ∈ P ush ∧ ts < ts < ts ⇒ ts ∈ dom(α.matched))
Pop-Base
                                  a,ts ′ ,w,ts
                           α                     t   α′ [matched := matched ∪ {(ts, ts ′ )}]
                           [R]                             a,ts ′ ,w,ts                                [A]
              a = q.popu          u 6= empty           α                      t    α′      w = q.pushu        (w, a) ∈
                                                                                                                     / R×A
Pop-NE-Rlx
                                                                    a               ′
                                                           α, γ           t       α ,γ
                                                            ′                     a,ts ′ ,w,ts
              a = q.pop(u)A     u 6= empty    α          t α     w = q.push(u)R
                 ′    ′                                ′
            tview = α .tviewt ⊗ α.mview(w,ts)   ctview = γ.tviewt ⊗ α.mview(w,ts)
Pop-NE-Sync
                            a    ′               ′                    ′
                                                  
                      α, γ    t α tviewt := tview , γ[tviewt := ctview ]
                     [A]
           a = q.popempty           tst(α.tviewt (q)) < ts ′                            ops′ = α.ops ∪ {(a, ts ′ )}
                                                                                                             [A]
           (∀(ww , tt) ∈ α.ops. tt < ts ′ ⇒ tt ∈ sup(σ.matched) ∨ ww = q.popempty )
                                tview′ = α.tviewt [q := (a, ts ′ )]
Pop-Emp
                                    a
                           α, γ         t   α[ops := ops′ , tviewt := tview′ ], γ
     We contrast this specification with the prior declarative semantics of Raad et al. [RDR+ 19],
which defines semantics for complete executions. Note that Raad et al. [RDR+ 19] also de-
scribe weak stack specifications; but their notion of weakness relaxes the total order of
operations into a partial order. In our model, the operations are still totally ordered, but
this total order may be different from the real-time order of operations, thus represents a
relaxation of abstract specifications as used in proofs of linearizability [HW90, DD15].
     With this specification, it becomes possible to make the proof outline described in Fig. 3
more precise. In particular, we can prove the following property, which we have verified
using our Isabelle/HOL mechanisation.
Proposition 3. The proof outline in Fig. 3 is valid.
     Note that the variable d in Fig. 3 is a client variable, whereas the stack operations are
part of an abstract library. The synchronisation guarantees provided by the stack library are
sufficient to guarantee message passing in the client. Next, in Section 7.2, we show that such
a specification can indeed be implemented. In particular, we show that the Treiber stack
adapted for C11, as described by Doherty et al [DDWD18] satisfies the stack specification
from Example 3, i.e., the implementations of the push and pop operations in Algorithm 1
provide sufficient synchronisation to provide client-side message passing.
               VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                               23




Algorithm 2 Translated model and proof outline
 3: procedure PushR (v)                                          10: function PopA
              / usedAddr . [a = 0]L
      {I ∧ ∀a ∈                   t }                            11:    repeat
 4:    choose a where a, a + 1 ∈      / usedAddr :               12:        repeat
        nVal t , nNxt t , usedAddr :=                                         {I ∧ COpop }
             a, a + 1, usedAddr ∪ {a, a + 1};                   13:            topt ←A T op ;
                          L               L
      {I ∧ [nVal t = 0]t ∧ [nNxt t = 0]t }                                    {I ∧ COpop ∧ DOpop }
 5:    nVal t := v ;                                            14:        until topt 6= null ;
      {I ∧ [nVal t = v]L                  L
                          t ∧ [nNxt t = 0]t }                             {I ∧ COpop ∧ DOpop }
 6:    repeat                                                   15:        nTop t ← (topt + 1) ;
          {I ∧ [nVal t = v]L  t ∧ ∃v.[nNxt  t = v] L
                                                   t }                    {I  ∧ COpop ∧ DOpop }
 7:        topt ←A Top ;                                        16:     until CASR (Top, topt , nTop t )
                            L                    L
        {I ∧ [nVal t = v]t ∧ ∃v.[nNxt t = v]t }                         {I ∧ ∃v.[topt = v]L
                                                                                          t }
 8:        nNxt t := topt ;                                     17:     rvalt ← topt ;
        {I ∧ [nVal t = v]L                      L
                            t ∧ [nNxt t = topt ]t }
                   R
 9:    until CAS (Top, topt , nVal t )
 where TopVals is the set of all values for all writes to Top in the given weak memory state, and
             I = (7.1) ∧ (7.2) ∧ (7.3) ∧ (7.4) ∧ (7.5) ∧ (7.6)
       COpop = (∃v.[T op = v]L
                             t )
               ∧(∀a ∈ TopVals. (∃v.hTop = aiL [a = v]L                  L             L
                                                     t ) ∧ (∃v.hTop = ai [(a + 1) = v]t ))

       DOpop = (∃v. [topt = v]L                          L
                              t ) ∧ (∃v. [(topt + 1) = v]t )



7.2. C11 Treiber Stack. The example we consider (see Algorithm 1) is the Treiber
Stack [Tre86] (well-studied in a SC setting, but not in a weak memory one), executing
in the RC11 [LVK+ 17] memory model. Due to weak memory effects, the events un-
der consideration, including method invocation and response events are partially ordered
[AMT14, LGV16, DV16, LVK+ 17, BDG13]. In Algorithm 1, all accesses to Top occur in
weak memory. In particular, any read of Top (lines 7, 13) reading from a write to Top
(lines 9, 16) induces happens-before order from the write to the read. Any read of Top via
a failed CAS is relaxed (see Fig. 4).
     For simplicity, like Doherty et al [DDWD18] we assume that the Pop operation blocks
by spinning instead of returning empty. Doherty et al show that the Treiber Stack in
Algorithm 1 satisfies a property known as causal linearizability, which in turn guarantees
compositionality: any history containing executions of two causally linearizable objects will
itself be causally linearizable. However, nothing is known about the client-side guarantees of
the algorithm (namely, whether what client-side synchronisation guarantees are available).
     In this section, we address this shortcoming by proving refinement between the imple-
mentation (Algorithm 1) and the stack specification described in Example 3. In particular,
we show that the PushR (v) and PopA operations respectively implement the synchronising
push and pop operations in Example 3.
Modelling the Treiber Stack. We track a set of used addresses, usedAddr . Specifically,
each address in usedAddr is an address containing the value (n.val) and next field (n.nxt)
of the node that a thread is trying to push, or has already been pushed onto the stack. The
variable Top is a (relaxed) pointer — the value of each write to Top is an address from
usedAddr or null. The val and nxt fields of each node are modelled by (relaxed) writes to
addresses in usedAddr .
24                                     S. DALVANDI AND B. DONGOL




     For the push, at line 4, two previously unused addresses are selected and inserted
into usedAddr ; these addresses is recorded in local variable nVal t and nNxt t for thread t.
We assume that the new node constructor allocates two consecutive addresses, and hence
assume nNxt t = nVal t + 1. We also assume that both variables are initialised with value 0.
In our development, Top will point to an address holding the value, say nVal , and the next
node is defined as the value of the last write to address nVal + 1. For line 5, we introduce
a relaxed write to the address corresponding to nVal t with value v. Line 7 corresponds to
an acquiring read of Top, line 8 updates the nxt field, and line 10 executes a releasing CAS
on Top. Similarly, for the pop, at line 13, we introduce an acquiring read of Top into local
variable topt . At line 15, we generate a read of the address topt +1 (which, as describe above,
dereferences the next field), and store the value of this address in local variable nTop t . At
line 16, we perform a releasing CAS on Top.
Treiber Stack invariants. We use an auxiliary variable pushedAddr to keep track of the
addresses that have been pushed on to the stack. We set pushedAddr to pushedAddr ∪
{nVal t } at line 9 and to pushedAddr \ {topt } at line 16 whenever the corresponding CAS
operations succeed. Given a library state β, the addresses that have been pushed onto the
stack (in order) are thus given by nxtRel β (defined below), recalling that we use address
a + 1 to store writes to the next field. Thus:
                lastVal β (x) = wrval (last (β.ops, x))
                  nxtRel ls,β = {(a, b) | a ∈ ls.pushedAddr ∧ b = lastVal β (a + 1)}+
Thus, nxtRel ls,β is the transitive closure of the set that maps each pushed address (as
recorded in ls) to the address of the next node. The first component of our global invariant
ensures that nxtRelβ is a total order with Top as the minimal element (inf) and null as
the maximal element (sup).
       totalOrder(nxtRelβ ) ∧ inf(nxtRelβ ) = lastVal β (T op) ∧ sup(nxtRelβ ) = null        (7.1)
The next two components of the invariant state properties about Top, and links these values
to the auxiliary state components usedAddr and pushedAddr.
         ∀w ∈ β.ops|Top . w ∈ WR ∧ (wrval (w) 6= null ⇒ wrval (w) ∈ ls.usedAddr )            (7.2)
         lastVal β (T op) 6= null ⇒ lastVal β (T op) ∈ ls.pushedAddr                         (7.3)
Invariant (7.2) states writes to Top are releasing and non-null writes are recorded in
ls.usedAddr , while (7.3) states that whenever the last value of Top is non-null, this value is
a currently pushed address.4 Finally, we have a set of simple invariants over usedAddr and
pushedAddr .
      ls.pushedAddr ⊆ ls.usedAddr                                                            (7.4)
      ∀a1 , a2 ∈ ls.pushedAddr . a1 6= a2 ⇒ lastVal β (a1 + 1) 6= lastVal β (a2 + 1)         (7.5)
      ∀a ∈ ls.pushedAddr . lastVal β (a + 1) 6= null ⇒ lastVal β (a + 1) ∈ ls.pushedAddr     (7.6)
Invariant (7.4) states that all pushed addresses are used addresses, (7.5) states that the
next pointers of different pushed addresses are different and (7.6) states that if the value of
the next pointer of a pushed address is non-null, then the node corresponding to the next
pointer is a pushed address.
     4Invariant (7.3) could be strengthened so that we have lastVal (a) ∈ ls.pushedAddr for all a ∈
                                                                   β
dom(nxtRel ls,β ), but is not needed for our verification.
              VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                         25




Simulation relation. We now describe the simulation relation used to prove refinement
between the Treiber Stack and the stack specification in Section 3. A key component
of the relation is an injective function, f , mapping nodes corresponding to pushed ad-
dresses to unmatched push operations of the abstract specification. Recall from Example 3
that pushes are matched if they have been subsequently popped. The refinement relation
RTS ((als, γA , α), (ls, γC , β)) = ∃f. (7.7) ∧ (7.8) ∧ (7.9) ∧ (7.10) ∧ (7.11) ∧ (7.12) ∧ (7.13).
    The first component ensures injectivity of f and that the corresponding operation is a
pop that returns empty.
                        injective(f ) ∧ ∃ts. f (null) = (pop(empty), ts)                    (7.7)
We assume unmatchedPush α denotes the set of unmatched push operations in the abstract
state α. The next two conditions describe the relationship between pushed addresses in the
concrete state to the unmatched pushes:
       ∀a ∈ ls.pushedAddr . f (a) ∈ unmatchedPush α ∧ valα (f (a)) = lastVal β (a)
                                                                                            (7.8)
                            ∧ tst(f (a)) > tst(f (lastVal β (a + 1)))
       ∀a ∈ ls.pushedAddr , op ∈ unmatchedPush α .
           op 6= f (a) ∧ op 6= f (lastVal β (a + 1)) ⇒                                      (7.9)
           tst(op) < tst(f (lastVal β (a + 1)) ∨ tst(op) > tst(f (a))
Condition (7.8) states that for each pushed address, f (a) is indeed an unmatched push with
the same values. Moreover, the timestamp of the push corresponding f (a) is larger than
the timestamp of the push corresponding to the next node of a. Condition (7.9) ensures
that the timestamp of op is not in between that of f (a) and the immediately next node of
f (a).
     Suppose lastPush α returns the push in α with the largest timestamp. The next condi-
tion ensures that when the stack is non-empty, the node corresponding to the last write to
Top is the push with the largest timestamp, i.e.,
  lastVal β (T op) 6= null ⇒ lastPush β ∈ unmatchedPush α ∧ f (lastVal β (T op)) = lastPush α
                                                                                         (7.10)
Finally, we have a set of conditions describing the views of threads over client variables.
Together these assertions ensures the client observation property in Definition 5.
     ∀a ∈ ls.pushedAddr , x ∈ GVar C . tst(β.mviewf (a) (x)) ≤ tst(γC .tviewt (x))         (7.11)
     ∀a ∈ ls.pushedAddr , w ∈ β.ops. var(w) = T op ∧ val(w) = a ⇒
                                                                                           (7.12)
         ∀x ∈ GVar C . tst(α.mviewf (a) (x)) ≤ tst(β.mvieww (x))
     ∀x ∈ GVar C . tst(γA .tviewt (x)) ≤ tst(γC .tviewt (x))                               (7.13)
We then obtain the following proposition.
Proposition 4. For synchronisation-free clients, RTS is a forward simulation between the
abstract stack object and the Treiber stack.
    The simulation proof is similar to linearizability proofs in the classical (sequentially
consistent) setting [DD15]. All steps except for a successful CAS at lines 9 and 16 are
stuttering steps and are not matched with any abstract step. The successful CAS operations
corresponds to the a releasing push or an acquiring pop as allowed by the specification in
Example 3.
26                                S. DALVANDI AND B. DONGOL




7.3. Mechanisation. Our deductive proof of the Treiber stack for the RC11-RAR within
Isabelle/HOL has been a significant undertaking. Many properties that one would take for
granted in a sequentially consistent setting are no longer valid under weak memory. For in-
stance, to guarantee that the writes to the fields at lines 5 and 8 are seen by the reads in lines
15 and 17, respectively, one must ensure a happens-before relationship through the releas-
ing CAS at line 9 and the acquiring read at line 13. Moreover, client-side synchronisation
guarantees defined by the specification must also shown to be satisfied. This verification has
been made possible by the proof infrastructure developed in earlier work [DDDW20a], which
considered much simpler examples. Here, we have shown that the proof principles carry
over to pointer-based programs. Additionally, the specifications that we have developed in
Section 7.1 (and Section 4) are appropriate for guaranteeing client synchronisation through
a library object, and our refinement theory can be used to show that these client-library
synchronisation requirements are also guaranteed by the Treiber stack.
     The full development and verification of the Treiber stack is around 12 KLOC in Isabelle
accross 9 different theories. The proof is heavily dependent on the general proof rules
developed for the generalised C11 operational semantics. A considerable effort was put to
identify and prove the local and global invariants of the stack’s push and pop operations.
Each of these invariants was then proved correct locally and globally (interference freedom)
in the usual Owicki-Gries manner.

7.4. Discussion. The message passing idiom has manifested in our case study in two differ-
ent ways. In Fig. 3 and the corresponding proof of Proposition 3 involves message passing
through the stack specification. In the Treiber stack implementation, threads use message-
passing to ensure that the relaxed writes to the “val” and “nxt” fields of a node within
a push are viewed by the pop via release-acquire synchronisation on the Top pointer. In
both cases, message passing is succinctly characterised by conditional observation assertion,
suggesting that it is a key operator for reasoning about such behaviours. Conditional obser-
vation assertions capture the idea behind message passing via “ownership transfer” as used
in many separation logics [TDV15, DV17, KDD+ 17, SM20, SM18], a “communication spec-
ification” [AC17] and “protocols” [TVD14], which have been used to ensure happens-before
knowledge is passed from one thread to another. These techniques are however focussed
on message passing via reads and writes within a single object and cannot handle message
passing on client threads using library synchronisation.
     An interesting observation that has been elucidated by our refinement proof is the fact
that the Treiber stack does not need to linearize its operation in the middle of the abstract
operation order as defined by their timestamps. I.e., each new push / pop operation thereby
is not required to take advantage of the relaxation provided by the specification in Exam-
ple 3. This is however not surprising — the concrete implementation synchronises all pushes
and pops through a single Top pointer that is only modified using an RMW generated by
a CAS. We conjecture this relaxation would be required by, for example, a weak memory
implementation of the elimination stack [HSY04], which augments a standard stack with a
disjoint elimination mechanism. Operations that synchronise using the elimination mecha-
nism do not interact with the main stack data structure, and hence are not guaranteed to
advance thread views. We therefore conjecture that a C11-style relaxed-memory version of
the elimination stack would be an implementation of our specification, where the stack can
be weakly synchronised, allowing it to take advantage of our relaxed specification.
             VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                     27




                                    8. Related work
The speed of development in the area has meant that it has become almost impossible to
cover all related works. Below, we provide a brief overview of different approaches. There
are now several different approaches to program verification that support different aspects of
weak memory using pen-and-paper proofs (e.g., [LV15, TVD14, AC17, DV17]), model check-
ing (e.g., [KRV19, AAAK19]), specialised tools (e.g., [TDV15, KEEJ20, SPD+ 18, SM18]),
and generalist theorem provers (e.g., [DDDW20a]). These cover a variety of (fragments
of) memory models and proceed via exhaustive checking, separation logics, or Hoare-style
calculi.
     Library abstractions in weak memory have been considered in earlier works (e.g., [BDG13]),
but these were not accompanied by an associated program logic or verification technique.
The use of abstract methods can be used to ensure weak-memory synchronisation guaran-
tees has been established in earlier work [DDWD18, DJRA18], where it has been shown to
be necessary for contextual refinement [DJRA18] and compositionality [DDWD18].
     Krishna et al. [KEEJ20] have developed an approach to verifying implementations
of weakly consistent libraries [EE19]. Their techniques are mechanised using the CIVL
verification tool and account for weak memory relaxations by transitioning over a generic
happens-before relation encoded within a transition system. On the one hand, this means
that their techniques apply to any memory model, but on the other hand, such a happens-
before relation must ultimately be supplied. Their methods currently cover refinement of
libraries, but do not cover clients that use library specifications. Nevertheless given that
CIVL is aimed at automation, it would be interesting to see whether the assertion language
from earlier works [DDDW20a] (also see Section 5) can have a role in further improving
these verification methods.
     More recent works include that on robustness of C11-style programs, which aims to
show “adequate synchronisation” so that the weak memory executions reduce to executions
under stronger memory models [ML21]. Such reductions, although automatic, are limited
to finite state systems, and a small number of threads. Furthermore, it is currently unclear
how they would handle client-library synchronisation or relaxed non sequentially consistent
specifications. Verification tools for deductive verification of C11-style programs have been
based on separation logic [SM18, SM20, KDD+ 17] and Owicki-Gries reasoning [DDD20,
DDDW20a]. Those based on separation logic offer a degree of automation but, as far as the
authors are aware, have not been applied to verification of data structures. None of these
works cover refinement.
     Orthogonal to our paper is a series of works that address more relaxed memory seman-
tics that allow causality cycles [PCP+ 20, KHL+ 17, LCP+ 20, JJR20], e.g., the load-buffering
litmus test, which our semantics (like [LVK+ 17]) disallows. Although an important problem,
we eschew proofs of correctness in this weaker memory model since the precise weak mem-
ory semantics that appropriately handles load-buffering, yet rules out thin-air reads is still
a topic of ongoing research. Moreover, we note that many concurrent object implementa-
tions naturally induce intra-thread dependencies, whereby the relaxed model and the strict
model we use coincide without requiring introduction of any additional synchronisation.
Thus, although weak memory models with causality cycles are a real phenomenon, there is
more work to be done before they relaxations they offer can be exploited. We consider the
problem of deductive verification under such memory models to be an important problem
for future work.
28                                  S. DALVANDI AND B. DONGOL




                                         9. Conclusions
In this paper, we have presented a new approach to specifying and verifying abstract ob-
jects over weak memory by extending an existing operational semantics for RC11 RAR (a
fragment of the C11 memory model). This operational semantics allows one to execute pro-
grams in thread order and accommodates weak memory behaviours via a special encoding
of the state. Moreover, unlike prior works [DDDW20a], it describes how (release-acquire)
synchronisation within a library affects a client state, and vice versa, supporting modular
program development.
     Operational semantics are widely acknowledged as being a prerequisite to developing
program logics, complementing declarative approaches (e.g., [AMT14, RDR+ 19]), since a
meaning for stepwise program execution is needed to establish meaning for pre/postcon-
ditions. We have demonstrated this by developing an Owicki-Gries logic for client-library
programs, extending prior work [LV15, DDDW20a], which did not facilitate proof modular-
isation of this nature.
     We have also developed a novel operational technique for specifying weak memory con-
current objects, and shown that the specification allows proofs of client-library synchroni-
sation across abstract library method calls. This has been accompanied by a refinement
theory, that extends standard notions of refinement under sequential consistency [dRE98].
To exploit these operational descriptions, we have developed an assertion language that
describes a thread’s observations of client-library states, which is in turn used to verify pro-
gram invariants and proofs of refinement. We have shown that our methodology supports
two types of verification: (1) proofs of correctness of client programs that use abstract li-
braries and (2) refinement proofs between abstract libraries and their implementations. We
present the verification of two lock implementations as well as the Treiber stack adapted
for C11. This amounts to one of the more sophisticated proofs performed using a deductive
verification approach.

                                           References
[AAAK19]  P. A. Abdulla, J. Arora, M. F. Atig, and S. N. Krishna. Verification of programs under the
          release-acquire semantics. In K. S. McKinley and K. Fisher, editors, PLDI, pages 1117–1132.
          ACM, 2019.
[AC17]    J. Alglave and P. Cousot. Ogre and Pythia: an invariance proof method for weak consistency
          models. In G. Castagna and A. D. Gordon, editors, POPL, pages 3–18. ACM, 2017.
[AMT14]   J. Alglave, L. Maranget, and M. Tautschnig. Herding cats: Modelling, simulation, testing, and
          data mining for weak memory. ACM Trans. Program. Lang. Syst., 36(2):7:1–7:74, 2014.
[BDG13]   M. Batty, M. Dodds, and A. Gotsman. Library abstraction for C/C++ concurrency. In R. Gi-
          acobazzi and R. Cousot, editors, POPL, pages 235–248. ACM, 2013.
[BOS+ 11] M. Batty, S. Owens, S. Sarkar, P. Sewell, and T. Weber. Mathematizing C++ concurrency. In
          T. Ball and M. Sagiv, editors, POPL, pages 55–66. ACM, 2011.
[DD15]    B. Dongol and J. Derrick. Verifying linearisability: A comparative survey. ACM Comput. Surv.,
          48(2):19:1–19:43, 2015.
[DD21]    Sadegh       Dalvandi      and     Brijesh       Dongol.     Isabelle     files    for   “Op-
          erationally      Verifying     C11-style        Weak      Memory         Libraries”,    2021.
          https://www.dropbox.com/sh/nc85kygsa0y8ckr/AADKddr5yTrpro06aaWIciE1a?dl=0.
[DDD20]   S. Dalvandi, B. Dongol, and S. Doherty. Integrating Owicki-Gries for C11-style memory models
          into Isabelle/HOL. CoRR, abs/2004.02983, 2020.
[DDDW20a] S. Dalvandi, S. Doherty, B. Dongol, and H. Wehrheim. Owicki-gries reasoning for C11 RAR. In
          R. Hirschfeld and T. Pape, editors, ECOOP, volume 166 of LIPIcs, pages 11:1–11:26. Schloss
          Dagstuhl - Leibniz-Zentrum für Informatik, 2020.
               VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                                29




[DDDW20b] Sadegh Dalvandi, Simon Doherty, Brijesh Dongol, and Heike Wehrheim. Owicki-gries reasoning
          for C11 RAR (artifact). Dagstuhl Artifacts Ser., 6(2):15:1–15:2, 2020.
[DDWD18] S. Doherty, B. Dongol, H. Wehrheim, and J. Derrick. Making linearizability compositional for
          partially ordered executions. In C. A. Furia and K. Winter, editors, iFM, volume 11023 of
          LNCS, pages 110–129. Springer, 2018.
[DDWD19] S. Doherty, B. Dongol, H. Wehrheim, and J. Derrick. Verifying C11 programs operationally. In
          Jeffrey K. Hollingsworth and Idit Keidar, editors, PPoPP, pages 355–365. ACM, 2019.
[DG16]    B. Dongol and L. Groves. Contextual trace refinement for concurrent objects: Safety and
          progress. In ICFEM, volume 10009 of LNCS, pages 261–278, 2016.
[DJRA18]  B. Dongol, R. Jagadeesan, J. Riely, and A. Armstrong. On abstraction and compositionality
          for weak-memory linearisability. In VMCAI, volume 10747 of LNCS, pages 183–204. Springer,
          2018.
[dRE98]   W. P. de Roever and K. Engelhardt. Data Refinement: Model-oriented Proof Theories and
          their Comparison, volume 46 of Cambridge Tracts in Theoretical Computer Science. Cambridge
          University Press, 1998.
[DSM18]   S. Dolan, KC Sivaramakrishnan, and A. Madhavapeddy. Bounding data races in space and
          time. In PLDI, PLDI 2018, pages 242–255, New York, NY, USA, 2018. ACM.
[DV16]    M. Doko and V. Vafeiadis. A program logic for C11 memory fences. In VMCAI, volume 9583
          of LNCS, pages 413–430. Springer, 2016.
[DV17]    M. Doko and V. Vafeiadis. Tackling real-life relaxed concurrency with FSL++. In ESOP, pages
          448–475, 2017.
[EE19]    M. Emmi and C. Enea. Weak-consistency specification via visibility relaxation. Proc. ACM
          Program. Lang., 3(POPL):60:1–60:28, 2019.
[FORY10]  I. Filipovic, P. W. O’Hearn, N. Rinetzky, and H. Yang. Abstraction for concurrent objects.
          Theor. Comput. Sci., 411(51-52):4379–4398, 2010.
[GY11]    A. Gotsman and H. Yang. Liveness-preserving atomicity abstraction. In ICALP (2), volume
          6756 of LNCS, pages 453–465. Springer, 2011.
[HSY04]   D. Hendler, N. Shavit, and L. Yerushalmi. A scalable lock-free stack algorithm. In P. B. Gibbons
          and M. Adler, editors, SPAA, pages 206–215. ACM, 2004.
[HW90]    M. Herlihy and J. M. Wing. Linearizability: A correctness condition for concurrent objects.
          ACM TOPLAS, 12(3):463–492, 1990.
[JJR20]   R. Jagadeesan, A. Jeffrey, and J. Riely. Pomsets with preconditions: a simple model of relaxed
          memory. Proc. ACM Program. Lang., 4(OOPSLA):194:1–194:30, 2020.
[KDD+ 17] J.-O. Kaiser, H.-H. Dang, D. D., O. Lahav, and V. Vafeiadis. Strong logic for weak memory:
          Reasoning about release-acquire consistency in Iris. In Peter Müller, editor, ECOOP, volume 74
          of LIPIcs, pages 17:1–17:29. Schloss Dagstuhl - Leibniz-Zentrum fuer Informatik, 2017.
[KEEJ20]  S. Krishna, M. Emmi, C. Enea, and D. Jovanovic. Verifying visibility-based weak consistency.
          In P. Müller, editor, ESOP, volume 12075 of Lecture Notes in Computer Science, pages 280–307.
          Springer, 2020.
[KHL+ 17] J. Kang, C.-K. Hur, O. Lahav, V. Vafeiadis, and D. Dreyer. A promising semantics for relaxed-
          memory concurrency. In POPL, pages 175–189. ACM, 2017.
[KRV19]   M. Kokologiannakis, A. Raad, and V. Vafeiadis. Model checking for weakly consistent libraries.
          In K. S. McKinley and K. Fisher, editors, PLDI, pages 96–110. ACM, 2019.
[LCP+ 20] S.-H. Lee, M. Cho, A. Podkopaev, S. Chakraborty, C.-K. Hur, O. Lahav, and V. Vafeiadis.
          Promising 2.0: global optimizations in relaxed memory concurrency. In A. F. Donaldson and
          E. Torlak, editors, PLDI, pages 362–376. ACM, 2020.
[LGV16]   O. Lahav, N. Giannarakis, and V. Vafeiadis. Taming release-acquire consistency. In R. Bodı́k
          and R. Majumdar, editors, POPL, pages 649–662. ACM, 2016.
[LV15]    O. Lahav and V. Vafeiadis. Owicki-Gries reasoning for weak memory models. In M. M.
          Halldórsson, K. Iwama, N. Kobayashi, and B. Speckmann, editors, ICALP, volume 9135 of
          LNCS, pages 311–323. Springer, 2015.
[LVK+ 17] O. Lahav, V. Vafeiadis, J. Kang, C.-K. Hur, and D. Dreyer. Repairing sequential consistency
          in C/C++11. In PLDI, pages 618–632. ACM, 2017.
[ML21]    R. Margalit and O. Lahav. Verifying observational robustness against a c11-style memory
          model. Proc. ACM Program. Lang., 5(POPL), January 2021.
30                                  S. DALVANDI AND B. DONGOL




[OG76]      S. S. Owicki and D. Gries. An axiomatic proof technique for parallel programs I. Acta Inf.,
            6:319–340, 1976.
[PCP+ 20]   M. Paviotti, S. Cooksey, A. Paradis, D. Wright, S. Owens, and M. Batty. Modular relaxed
            dependencies in weak memory concurrency. In P. Müller, editor, ESOP, volume 12075 of Lecture
            Notes in Computer Science, pages 599–625. Springer, 2020.
[PSN16]     A. Podkopaev, I. Sergey, and A. Nanevski. Operational aspects of C/C++ concurrency. CoRR,
            abs/1606.01400, 2016.
[RDR+ 19]   A. Raad, M. Doko, L. Rozic, O. Lahav, and V. Vafeiadis. On library correctness under weak
            memory consistency: specifying and verifying concurrent libraries under declarative consistency
            models. Proc. ACM Program. Lang., 3(POPL):68:1–68:31, 2019.
[SM18]      A. J. Summers and P. Müller. Automating deductive verification for weak-memory programs.
            In D. Beyer and M. Huisman, editors, TACAS, volume 10805 of LNCS, pages 190–209. Springer,
            2018.
[SM20]      A. J. Summers and P. Müller. Automating deductive verification for weak-memory programs
            (extended version). Int. J. Softw. Tools Technol. Transf., 22(6):709–728, 2020.
[SPD+ 18]   K. Svendsen, J. Pichon-Pharabod, M. Doko, O. Lahav, and V. Vafeiadis. A separation logic
            for a promising semantics. In A. Ahmed, editor, ESOP, volume 10801 of LNCS, pages 357–384.
            Springer, 2018.
[SSO+ 10]   P. Sewell, S. Sarkar, S. Owens, F. Z. Nardelli, and M. O. Myreen. x86-tso: a rigorous and
            usable programmer’s model for x86 multiprocessors. Commun. ACM, 53(7):89–97, 2010.
[TDV15]     J. Tassarotti, D. Dreyer, and V. Vafeiadis. Verifying read-copy-update in a logic for weak
            memory. In D. Grove and S. Blackburn, editors, PLDI, pages 110–120. ACM, 2015.
[Tre86]     R. K. Treiber. Systems programming: Coping with parallelism. Technical Report RJ 5118,
            IBM Almaden Res. Ctr., 1986.
[TVD14]     A. Turon, V. Vafeiadis, and D. Dreyer. GPS: navigating weak memory with ghosts, protocols,
            and separation. In A. P. Black and T. D. Millstein, editors, OOPSLA, pages 691–707. ACM,
            2014.
                VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                             31




                 Appendix A. Proof Rules for Clients and Libraries
Here, we give a set of rules from our Isabelle/HOL development [DD21] that we use in the
verification of client-library programs.
     We use [S]Xt , where S is a statement, t is a thread and X ∈ {L, C} to denote that S is
statement of either the library (L) or client (C) action that is executed by thread t. E.g.,
[x := v]L t denotes that x := v is a write statement of the library being executed thread t.
     We specialise the notion of a covered operation from Section 5.1 and define covered
writes over shared locations as follows:
      CW [x, u](σ) ≡ ∀w. w ∈ σ.(W|x )−1 ∧ w 6∈ σ.cvd ⇒ w = σ.last (W, x) ∧ wrval (w) = u
The assertion CW [x, u] assumes a variable (or location) x and value u, and holds iff all but
the last write to x are covered, and that the value of the last write is u.
                      X ∈ {L, C}
(1)
       {[x =    u]X
                  t }[x    := v]X         X
                                t {[x = u]t }


                                 X ∈ {L, C}
(2)
       {∃ u . CW [x, u]} [CASR (x, v, v ′ )]X
                                            t {∃ v . CW [x, v]}


                                  X ∈ {L, C}
(3)
       {CW [x, v]X } [r ← CASR (x, u, u′ )]X            ′ X
                                           t {r ⇒ [x = u ]t }


                               X ∈ {L, C}
(4)
       {hx =    aiL [y    = b]X
                              t } [a ←
                                       A x]L {[y = b]X }
                                           t         t


                                  X, X ′ ∈ {L, C}
(5)                                                  ′
       {[x =t m]X } [r ← CASR (x, u, u′ )]X              X
                                          t {¬r ⇒ [x = m]t }


                                  X ∈ {L, C}             t 6= t′      x 6= y
(6)                                              R
        {¬ [x ≈    u]X
                     t′    ∧ [y =   v]X                     X
                                      t }[r ← CAS (x, l, u)]t {r ⇒ hx            = uiX [y = v]X
                                                                                              t′ }


                          X ∈ {L, C}        k 6= u          t 6= t′     x 6= y
(7)                                          R
        {hx =    uiX [y    =   v]X                      X
                                 t′ }[r ← CAS (x, l, k)]t {r ⇒ hx         = uiX [y = v]X
                                                                                       t′ }


                                         X ∈ {L, C}            x 6= y
(8)
       {[y =    v]X
                  t   ∧    CW [x, m]X }[r ← CASR (x, m, u)]X
                                                           t {r ⇒ hx             = uiX [y = v ]X
                                                                                               t }


                  X ∈ {L, C}
(9)
       {true}[v ←[A] x]X         X
                       t {[x ≈ v]t }
 32                                  S. DALVANDI AND B. DONGOL




                                   X ∈ {L, C}
(10)
       {CW [x, v]X } [r ← CASR (x, v, v ′ )]X              ′ X
                                            t {r ⇒ CW [x, v ] }


                              X ∈ {L, C}
(11)
       {CW [x, v]X }[r ← FAI(x)]X                 X
                                t {CW [x, (v + 1)] }


                               X ∈ {L, C}
(12)
       {T rue} [r ← CASR (x, v, v ′ )]X            ′ X
                                      t {r ⇒ [x ≈ v ]t }


                          X ∈ {L, C} ∧ x 6= y
(13)
       {¬ [x ≈ u]X           R        ′ X             X
                 t } [r ← CAS (y, v, v )]t′ {¬ [x ≈ u]t }


                          X ∈ {L, C}
(14)
       {¬ [x ≈    u]X
                    t } [v    ← y]X            X
                                  t′ {¬ [x ≈ u]t }


                               X ∈ {L, C}       y 6= x
(15)
       {hx =   viX [x     =   v]X               X
                                t } [v ← FAI(y)]t′ {hx   = viX [x = v]X
                                                                      t }


                               X ∈ {L, C}
(16)
       {hx =     viX [x   = v]X
                              t } [v ←
                                       A x]X {[x = v]X }
                                           t         t


                                 X ∈ {L, C}       t 6= t′
(17)
       {¬ [x ≈ u]X          X
                 t ∧ [x = v]t′ } [x :=
                                       R u]X {hx = uiX [x = u]X }
                                           t′                 t


                              X ∈ {L, C}      x 6= y
(18)
       {hx = uiX [x = u]X           X          X       X
                        t } [y := v]t′ {hx = ui [x = u]t }




        Appendix B. Hoare Logic Rules for The Abstract Stack Object
 In this section we provide a set of Hoare logic proof rules that we used in our Isabelle/HOL
 development to prove programs that use the abstract specification of the stack object. The
 rules relate observation assertions for abstract method calls.
     Here we assume that the pop operations are part of the library, thus we omit the
 superscript L on the assertions and operations related to the stack. Recall that m[Z] (v)t
 denotes that the annotation Z ∈ {R, A} is optional for the method m.
 (1)
       {[pop(u)]t } push[R] (v)t {[pop(v)]t }
               VERIFYING C11-STYLE WEAK MEMORY LIBRARIES VIA REFINEMENT                                                             33




 (2)
       {[pop(u)]t } push[R] (v)t {[pop(v)]t }


 (3)
       {[pop(u)]t }pop[A] (v)t {v = u}


                                  u 6= empty
 (4)
       {¬ hpop(u)it′ ∧ [y =t v]C } pushR (u)t {hpop(u)i[y = v]t′ }


                        u 6= empty
 (5)
       {hpop(u)i[y = v]C     A
                       t }pop (u)t {[y = v]t }


 (6)
       {[x = v]C       [R]            C
               t } push (u)t′ {[x = v]t }


 (7)
       {[x = v]C       [A]           C
               t′ } pop (u)t {[x = v]t′ }


 (8)
       {¬ hpop(u)it′ } [x := v]C
                               t {¬ hpop(u)it′ }


 (9)
       {¬ hpop(u)it′ } [v ← x]C
                              t {¬ hpop(u)it′ }


                        u 6= empty
(10)
       {¬ hpop(u)it′ } pop[A] (v)t {¬ hpop(u)it′ }


               u 6= z      u 6= empty       z 6= empty
(11)
       {hpop(u)i[y =     v]C      [A]                          = v]C
                           t } pop (z)t {hpop(u)i[y                t }


                        u 6= z       u 6= empty
(12)
       {hpop(u)i[y = v]C      [A]                   C
                       t } pop (z)t {hpop(u)i[y = v]t }


(13)
       {¬ hpop(u)it } [x := z]C                  C
                              t′ {hpop(u)i[x = v]t }




                                            This work is licensed under the Creative Commons Attribution License. To view a copy of this
                                            license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                            Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse
                                            2, 10777 Berlin, Germany
