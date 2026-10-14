                                            Lifting the Reasoning Level in Generic Weak
                                             Memory Verification (Extended Version)⋆

                                                               Lara Bargmann and Heike Wehrheim

                                                Department of Computing Science, University of Oldenburg, Germany
arXiv:2309.01433v1 [cs.LO] 4 Sep 2023




                                               Abstract. Weak memory models specify the semantics of concurrent
                                               programs on multi-core architectures. Reasoning techniques for weak
                                               memory models are often specialized to one fixed model and verifica-
                                               tion results are hence not transferable to other memory models. A recent
                                               proposal of a generic verification technique based on axioms on program
                                               behaviour expressed via weakest preconditions aims at overcoming this
                                               specialization to dedicated models. Due to the usage of weakest precon-
                                               ditions, reasoning however takes place on a very low level requiring the
                                               application of numerous axioms for deriving program properties, even
                                               for a single statement.
                                               In this paper, we lift reasoning in this generic verification approach to
                                               a more abstract level. Based on a view-based assertion language, we
                                               provide a number of novel proof rules for directly reasoning on the level of
                                               program constructs. We prove soundness of our proof rules and exemplify
                                               them on the write-to-read causality (WRC) litmus test. A comparison
                                               to the axiom-based low-level proof reveals a significant reduction in the
                                               number of required proof steps.

                                               Keywords: Axiomatic Reasoning · Concurrency Verification · Weak
                                               Memory Models.


                                        1     Introduction

                                        The behaviour of concurrent programs running on modern multi-core processors
                                        is influenced by the (weak) memory model of the processor. A memory model
                                        fixes how concurrent threads can access shared variables, in particular which val-
                                        ues of shared variables a thread can read. The behaviour of weak memory models
                                        differs from the often assumed sequential consistency (SC) [21] in which an ex-
                                        ecution is simply an interleaving of sequential executions of threads following
                                        their program order.
                                            As weak memory models deviate from sequential consistency, verification
                                        techniques for concurrent programs like rely-guarantee [28] or Owicki-Gries rea-
                                        soning [24] become unsound on weak memory models. Consequently, past years
                                        have seen the development of numerous reasoning approaches specific to a mem-
                                        ory model (like, e.g., [4, 9, 10, 20, 25]). The drawback of all these techniques is
                                        ⋆
                                            Bargmann and Wehrheim are supported by DFG-WE2290/14-1.
that a correctness proof for a concurrent program running on one memory model
is not directly transferable to other memory models.
    To alleviate this problem, Doherty et al. [12] propose a generic reasoning
technique for weak memory models provided these have a view-based seman-
tics [13]. A view of a thread specifies which write events to shared variables a
thread can observe (and hence read from). The core of the reasoning technique
is the concept of threads being view-maximal and memory-model internal steps
to not invalidate view-maximality. On top of such novel concepts, [12] simply
builds on standard Owicki-Gries reasoning for concurrent programs [24]. So far,
memory models SC, TSO [26], PSO [1] and C11 RAR [9] have been shown to fall
into this category. Reasoning (about single program instructions) then proceeds
by applying low-level axioms based on weakest preconditions. The result is a
correctness proof of a concurrent program (a proof outline) which is sound for
every memory model satisfying the axioms.
    While providing a memory-model independent approach, the technique how-
ever suffers from the need to apply very low-level, detailed axioms combined with
standard properties of weakest preconditions. Moreover, reasoning engines (like
Isabelle, as used in [10]) might not record the axioms employed for a specific
proof. This hinders transferability to memory models fulfilling only a subset of
the axioms: we do not know anymore whether a proof is or is not valid on such
a partially fitting model.
    To improve on these shortcomings, we propose a lifting of the reasoning
technique to a higher level. Starting from a view-based language for formulat-
ing assertions on concurrent programs, we develop several novel proof rules for
program statements. We prove soundness of each of these rules via the low-level
axioms. Moreover, together with every new rule we list the required axioms.
This enables us to directly see whether a proof is transferable to a memory
model which only partially fulfills the axiom set. We exemplify our new proof
rules on the write-to-read causality litmus test (see, e.g., [5]) for which we provide
both the low-level and the novel high-level reasoning steps. This demonstrates a
significant reduction in the number of required proof steps.


2    Program Syntax

We start by introducing the syntax of concurrent programs. We define a con-
current program as a parallel composition of sequential programs. Each thread
t ∈ Tid runs a sequential program Com and with the function Π : Tid → Com
we model a concurrent program over threads Tid. We let VarG be the set of global
variables and VarL the set of local variables (or registers) with VarG ∩ VarL = ∅
and Var = VarG ∪ VarL . We assume that initially all variables have the value 0.
   For x ∈ VarG , r ∈ VarL and value v ∈ Val the following grammar defines
Com:
        E ::= v | e
     com ::= skip | fnc | r := E | r := x | r :=RS x | x := E | x :=WS E
                    {[x = 0]1 ∩ [x = 0]2 ∩ [y = 0]3 ∩ r1 = 0 ∩ r2 = 0}
     Thread 1                 Thread 2                           Thread 3
     {P1,1 : [x = 0]1         {P2,1 : [y 6≈ 1]3 ∩ r2 6= 1        {P3,1 : r1 6= 1
     ∩[x 6≈ 1]2 ∩ r1 6= 1}    ∩([x = 0]2 ∪ hx = 1i[x = 1]2 )} ∪hy = 1iS [x = 1]3 }
     1 : x := 1;              2 : r1 := x ;                      4 : r2 :=RS y;
     {P1,2 : true}            {P2,2 : [y 6≈ 1]3 ∩ r2 6= 1        {P3,2 : r1 6= 1
                              ∩(r1 6= 1 ∪ [x = 1]2 )}            ∪r2 6= 1 ∪ [x = 1]3 }
                              3 : y :=WS 1;                      5 :r3 := x ;
                              {P2,3 : true}                      {P3,3 : r1 6= 1
                                                                 ∪r2 6= 1 ∪ r3 = 1}
                               {r1 6= 1 ∪ r2 6= 1 ∪ r3 = 1}
                 Fig. 1. Write-Read-Causality litmus test as proof outline

     Com ::= com | Com; Com | if b then Com else Com | while b do Com
where e ∈ Exp and b ∈ BExp are expressions over local variables only, e arith-
metic and b boolean, and fnc is a so-called fence (or barrier) instruction. The
two annotations RS (read synchronized) and WS (write synchronized) provide
ways of synchronizing a write with a read.
Example 1. In C11 [19], the annotation Release is a WS and Acquire an RS syn-
chronization. In SC, reads and writes only occur in synchronized form (and thus
the writes and reads without annotation behave like the ones with annotation).
Such synchronizations guarantee causal consistency.
    We let Act = {rd (x , r , v ), rd RS (x , r , v ), wr (x , v ), wr WS (x , v ), fence | x ∈ VarG ,
r ∈ VarL , v ∈ Val} be the set of actions containing synchronized and unsynchro-
nized reads and writes; Actext = Act ∪ {r := v | r ∈ VarL , v ∈ Val} ∪ {τ }
(τ an internal action). For an action a ∈ Act, var(a) ∈ VarG describes the
global variable of the action. For a (synchronized or unsynchronized) read ac-
tion rd (x , r , v ), we let rdval(a) = v ∈ Val, otherwise we set rdval(a) = ⊥ 6∈ Val;
wrval(a) is similarly defined for write actions. With these functions we can
define subsets of Act: Rd = {a ∈ Act | wrval(a) = ⊥, rdval(a) 6= ⊥} and
Wr = {a ∈ Act | rdval(a) = ⊥, wrval(a) 6= ⊥}. For a value v , we assume
Rd [v ] = {a ∈ Rd | rdval(a) = v } and Wr [v ] = {a ∈ Wr | wrval(a) = v }. We
let Act|x be the set of all actions a with var(a) = x . Hence Rd|x is the set of all
reads in Act|x and Wr|x the set of all writes.

Example 2. Figure 1 shows our running example, the Write-to-Read-Causality
litmus test WRC (originally formulated by Boehm and Adve [5] and appearing
here in the form of [23]). The program is a parallel composition of three threads,
accessing global variables x and y plus using local registers r1 , r2 and r3 . In
between statements in the program, we see named assertions (in blue), making
it a proof outline. The assertion {r1 6= 1 ∪ r2 6= 1 ∪ r3 = 1} at the end (the post-
condition) states the expected outcome of the program: when both r2 and r1
take the value 1, then r3 should also be 1. Such a behaviour holds for some but
not all memory models, e.g., TSO, SC and C11 satisfy it, but, e.g., the memory
model with a promise semantics in [27] does not.
                              Σ = wlp(R, Σ)                                 (Non-aborting)
              ′                ′                        ′   ′
            R ⊆ R ∧ P ⊆ P ⇒ wlp(R, P ) ⊆ wlp(R , P )               ((Anti)-Monotonicity)
           wlp(R, wlp(R ′ , P )) = wlp(R o9 R ′ , P )                        (Composition)
                  R[wlp(R, P )] ⊆ P                               (Relation Application)
       wlp(R, P ) ∩ wlp(R, Q) = wlp(R, P ∩ Q)                               (Conjunctivity)
       wlp(R, P ) ∪ wlp(R, Q) ⊆ wlp(R, P ∪ Q)                               (Disjunctivity)


                  Fig. 2. Properties of wlp (P , Q ⊆ Σ, R, R ′ ⊆ Σ × Σ)


    The semantics of programs Com depends on the specific memory model a
program runs on. In general, such semantics are typically defined in the follow-
ing way (see, e.g., [12]): First, a semantics for the local part, i.e., the registers, is
defined. As registers are not shared among threads, every thread directly writes
to and reads from its registers. For shared variables, the local semantics sim-
ply assumes that any value can be read. In a next step, the local semantics is
combined with a specific memory model semantics that details which values can
actually be read by which threads in some given state. As we develop a generic
reasoning approach here, we cannot further detail the semantics (we have no
fixed memory model).


3     Axiomatic Reasoning

Instead of trying to provide separate correctness proofs for WRC for all memory
models, we could employ the generic approach in [12] and construct one proof
which is then valid for all memory models fulfilling the axioms employed in this
proof. To this end, the generic reasoning technique abstracts from the semantics
(and thus from a concrete memory model) and bases reasoning on axioms.


3.1   Axioms

The approach of [12] reasons about arbitrary transition systems TS =   b (Actext , Σ,
I , T ) where Actext is the set of actions, Σ a set of states, I ⊆ Σ a set of initial
states and T ∈ Tid × Act → 2Σ×Σ a set of transitions. The axiomatisation is
build upon the weakest liberal precondition transformer (wlp) [11], which is used
both as a basis for property specification and verification. For a relation R and
set of states P (representing a predicate), we let wlp : 2Σ×Σ × 2Σ → 2Σ be
                             b {σ ∈ Σ | ∀ σ ′ : (σ, σ ′ ) ∈ R ⇒ σ ′ ∈ P }
                  wlp(R, P ) =

Figure 2 details some properties of wlp where o9 denotes relational composition
and R[·] relational image. Here, R typically is the relation T (t , a), t ∈ Tid, a ∈
Actext . We say R is disabled in a state σ iff σ ∈ dis(R) holds, where dis(R) =    b
 C1 : ∀ t ∈ Tid, a ∈ Act : I ⊆ vmax(t, a)
 C2 : ∀ σ, σ ′ ∈ Σ, t, t ′ ∈ Tid, a ∈ Act :
      σ ∈ vmax(t, a) ∧ (σ, σ ′ ) ∈ T (t, a) ⇒ ∃ τ ∈ Σ : (σ ′ , τ ) ∈ β ∧ (σ, τ ) ∈ T (t ′ , a) o9 β
 C3 : ∀ t ∈ Tid, a ∈ Act : T (t, a) ⊆ β o9 interf (t, a) o9 β
 C4 : ∀ t ∈ Tid, a, b ∈ Act : vmax(t, a) ⊆ wlp(interf (t, b), vmax(t, a))


                                      Fig. 3. Core axioms


wlp(R, ∅). This will in particular be employed for read actions, to state that it
is impossible for a thread t to read a certain value of a shared variable.
    The core concept of reasoning is the idea of views of threads. In weak mem-
ory models, threads observe global variables to have certain values (namely the
values of write actions); a thread might observe several different values at a time
and different threads might have different such observations. This differs from
sequential consistency in which all threads have the same observation and can
only see one value at a time. We say that a thread is view maximal, vmax(t , a)
(on an action a operating on a variable x ∈ VarG ), if it has the “most up-to-date”
view on this variable. While non view maximal threads might be able to read
older values of x , thread t reads the most up-to-date value.

Example 3. As an example, consider the WRC program after the execution of
line 1 (x := 1). In SC, all threads observe x to be 1 (only). In TSO, in which
written values are first placed in thread-local store buffers before being flushed to
main memory, there is a state in which thread 1 observes x to be 1 while threads
2 and 3 still see x to be 0. In such a state, we, e.g., have dis(T (2, Rd|x [1]). In
C11, there is even a state in which threads 2 and 3 can see x = 1 and x = 0 at
the same time. In all these models, we have vmax(1, rd (x , ·, ·)) (thread 1 is view
maximal on x ) in that state.

    A specific memory model will give rise to some concrete definition of vmax.
For the axiomatisation it is only important to guarantee that memory model
internal steps preserve view maximality in the sense of view-preserving simula-
tions.

Definition 1. For a transition system T S = (Act, Σ, I , T ), a view-preserving
simulation, denoted β, is the weakest relation R satisfying for all threads t ∈ Tid
and all actions a ∈ Act
                  R o9 T (t , a) ⊆ T (t , a) o9 R                         (semi-commutation)
                 vmax(t , a) ⊆ wlp(R, vmax(t , a))                           (view maximality)

   A view-preserving simulation keeps view maximality of threads and semi-
commutes with the transition relation.
 SV1 : ∀ a, b ∈ Act, t, t ′ ∈ Tid s.t. var(a) 6= var(b) :
        interf (t ′ , b) o9 T (t, a) ⊆ T (t, a) o9 interf (t ′ , b)
 SV2 : ∀ a, b ∈ Act, t, t ′ ∈ Tid s.t. var(a) 6= var(b) :
        vmax(t, a) ⊆ wlp(interf (t ′ , b), vmax(t, a))
RW1 : ∀ t, t ′ ∈ Tid, x ∈ VarG , ar ∈ Rd|x , aw ∈ Wr|x s.t. rdval(ar ) 6= wrval(aw ) :
        interf (t ′ , aw ) o9 T (t, ar ) ⊆ T (t, ar ) o9 interf (t ′ , aw )
RW2 : ∀ a ∈ Act, t, t ′ ∈ Tid, ar ∈ Rd|var(a) :
        interf (t ′ , ar ) o9 T (t, a) ⊆ T (t, a) o9 interf (t ′ , ar )
RW3 : ∀ a ∈ Act, t, t ′ ∈ Tid, ar ∈ Rd|var(a) :
        vmax(t, a) ⊆ wlp(interf (t ′ , ar ), vmax(t, a))
RW4 : ∀ x ∈ VarG , t ∈ Tid : Σ ⊆ dom(T (t, Rd|x ))
RW5 : ∀ x ∈ VarG , aw ∈ Wr|x , v = wrval(aw ) : Σ ⊆ wlp(T (t, aw ), dom(T (t, Rd|x [v ])))
                                   [
RW6 : ∀ x ∈ VarG , t ∈ Tid : x↑t ⊆    [x ≡ v ]t
                                            v∈Val

RW7 : ∀ x ∈ VarG , aw , ar , a ∈ Act|x , t, t ′ ∈ Tid, s.t. wrval(aw ) = rdval(ar ) ∧ t 6= t ′ :
        vmax(t, aw ) ∩ dis(T (t ′ , ar )) ⊆ wlp(T (t, aw ), wlp(T (t ′ , ar ), vmax(t ′ , a)))


                                Fig. 4. Axioms on shared variables


Example 4. A view-preserving simulation for SC is the identity relation. For
TSO it is the flushing of contents of store buffers to main memory. For C11 in
which all write events to the same variable x are ordered in some modification
order, it is the advancement of a thread’s observation on x (a write to x of a
value) to another write which occurs later in modification order.

    The concept of views is inherent to the axiomatic reasoning and hence is
also employed for property specification. As threads might observe more than
one value for a variable, the ordinary first-order logic assertions on program
variables of Hoare-logic [15] need to be replaced by view-based assertions.

Definition 2. For a thread t , a variable x ∈ VarG and values u, v ∈ Val we
define
            [x 6≈ v ]t =
                       bTdis(T (t , Rd|x [v ]))                               (Impossible value)
            [x ≡ v ]t =b u6=v [x 6≈ u]t                                       (Definite value)
                         T
                  x↑t =b a∈Act|x vmax(t , a)                                  (Maximal view)
            [x = v ]t =b [x ≡ v ]t ∩ x↑t                                      (Maximal value)
   hy = uiS [x = v ]t =b wlp(T (t , rd RS (y, ·, u)), [x = v ]t )             (Synced conditional
                                                                               observation)
     hx = v i[x = v ]t =
                       b wlp(T (t , rd (x , ·, v )), [x = v ]t )              (Conditional
                                                                               observation)
Example 5. Consider the state of WRC after executing lines 1, 2 and 3 (in this
order). In SC, we then have [x = 1]t for all threads t (same for y). In TSO (when
store buffer contents has not been flushed yet), we, e.g., have [x = 1]1 , [y = 1]2
and [x 6≈ 1]3 (thread 3 cannot read x to be 1). In C11, we might have [y ≈ 0]3
and [y ≈ 1]3 (thread 3 can read both 0 and 1). Moreover, the following synced
conditional observation is valid in all three memory models: hy = 1iS [x = 1]3
(by a synchronized read of y to be 1, thread 3 becomes view maximal on x and
definitely observes the value 1 for x ).
    We let G be the set of (all logical combinations of) such global assertions.
In our proof outlines (like in the one of WRC) we also allow for normal Hoare-
like assertions on local registers (e.g. (r1 = 1) ∈ BExp), and define the logical
combinations of such local (L) assertions and the global assertions to be the set
A of all assertions.
    Assertions define sets of states. Of particular interest are β-stable assertions.
Definition 3. Any predicate P ∈ 2Σ is β-stable iff P ⊆ wlp(β, P ).
     All assertions in G are β-stable (see [12]). The axioms furthermore make use
of an interference relation interf ∈ Tid × Act → 2Σ×Σ which (together with
β) provides an overapproximation of the transition relation T (t , a) in order to
abstract from details of the memory model and to regain standard properties
of reasoning (like writes and reads on different variables commuting). Figure 3
gives all core axioms; Figure 4 gives axioms concerning read and write actions
on shared variables.
     We only briefly explain the axioms; an example application of the axioms for
reasoning about WRC is given below. Axiom C1 states that initially all threads
are view maximal w.r.t. all actions. Axiom C2 describe the independence of
actions w.r.t. thread identifiers (where additional β steps are required). Axiom
C3 states that interf together with β over-approximates the behaviour of an
action. Axiom C4 states that the interference relation preserves every view-
maximality property of the thread performing the interference (of the action).
     Axiom SV1 is a weakening of the commutation property present in SC. SV2
states that a view-maximality property of any thread is stable under actions
on any other variable. Axioms RW1 and RW2 capture semi-commutativity
properties for writes and reads, respectively, and are analogous to SV1. Axiom
RW3 states that view-maximality on a variable is preserved by reading the
variable. Axiom RW4 states that it is always possible to read some value of a
variable, and RW5 states that a thread t writing some value can afterwards
read it. RW6 states that whenever t is view maximal on actions over variable
x , then t has a definite value assertion over some value for x (i.e., can only read
one value for x ). Axiom RW7 considers a situation in which thread t is vmax
on a variable x but t ′ cannot read a specific value for this variable. We then
obtain view-maximality of t ′ on x after t has performed the write aw and t ′ has
read this write’s value.
     Finally, the axiom set contains one specific axiom for fences and one for
message passing. Fence instructions are employed in weak memory models to
make programs behave more like SC. The fence axiom given below states this
by saying that a fence in a thread being view maximal on some action a makes
all other threads view maximal on a as well.

FNC ∀ a ∈ Act, t , t ′ ∈ Tid: vmax(t , a) ⊆ wlp(T (t , fence), vmax(t ′ , a)).
MP For aw , ar , b ∈ Act and t, t ′ ∈ Tid such that (aw , ar ) ∈ sync, var(aw ) =
  var(ar ), wrval(aw ) = rdval(ar ), var(b) 6= var(aw ), and t 6= t ′ , we have
                     vmax(t , b) ∩ wlp(T (t ′ , ar ), vmax(t ′ , b))
                        ⊆ wlp(T (t , aw ), wlp(T (t ′ , ar ), vmax(t ′ , b))).

    The message passing axiom MP describes the passing of knowledge on vari-
able values from one thread to another upon synchronization. Synchronization is
incorporated here by requiring (aw , ar ) ∈ sync which is achieved when the write
has a WS and the read an RS annotation. More specifically, it describes a situ-
ation where a thread t is maximal on some action b (vmax(t , b)) and thread t ′
upon executing action ar would become view maximal on b as well. Then, writ-
ing the value to be read (i.e., T (t , aw )) followed by reading this value (T (t ′ , ar ))
makes thread t ′ view maximal on b.
    As a first result, we restate two lemmas stating the stability of global asser-
tions under fence and read actions.

Lemma 1 ([3]). Assume the axioms C3, SV1 and SV2 hold. For all P ∈ G
and threads t , P ⊆ wlp(T (t , fence), P ).

Lemma 2 ([12]). Assume the axioms C3, SV1, SV2, RW2 and RW3 hold.
For all P ∈ G, threads t and ar ∈ Rd, P ⊆ wlp(T (t , ar ), P ).

    Note that – contrary to [3, 12] – we name the axioms required for the proof
in the lemmata. This is of importance for dealing with memory models which
only fulfill part of the axioms (so that we can see whether a generic proof is
transferable to such a memory model).


3.2   Reasoning Example on Axiom Level

Next, we employ the axioms for showing one step in the correctness proof of
WRC. Note that the proof of WRC in the generic framework has not appeared
before. In general, such proofs involve proof steps of the form
                                  P ⊆ wlp(T (t , a), Q )
for actions a belonging to program instructions comt , where P ∈ A is the pre-
assertion before and Q ∈ A the post-assertion after the instruction. We also
write these as Hoare-triples
                                    {P } comt {Q } .
Such steps need to be performed to show local and global correctness (as of
Owicki-Gries’ approach [24]).
Definition 4. A thread t is locally correct in a proof outline if {P }comt {Q }
holds for every program command com in t with pre-assertion P and post-
assertion Q .
    A proof outline is globally correct (interference-free) if for every pair of
threads t , t ′ , {R ∩ P }comt ′ {R} holds for every assertion R in the proof outline
of t and command com with pre-assertion P in thread t ′ .

   We exemplify one such proof step for the proof outline in Fig. 1, which is
part of the local correctness of thread 3.

        {r1 6= 1 ∪ hy = 1iS [x = 1]3 } r2 :=RS
                                            3 y {r1 6= 1 ∪ r2 6= 1 ∪ [x = 1]3 }

For this we have to prove for every v ∈ Val

 r1 6= 1 ∪ hy = 1iS [x = 1]3 ⊆ wlp(T (3, rd RS (y, r2 , v )), r1 6= 1 ∪ r2 6= 1 ∪ [x = 1]3 )

Because of the disjunctivity of wlp (see Fig. 2), we can divide the proof in two
parts
 (i) r1 6= 1 ⊆ wlp(T (3, rd RS (y, r2 , v )), r1 6= 1)
(ii) hy = 1iS [x = 1]3 ⊆ wlp(T (3, rd RS (y, r2 , v )), r2 6= 1 ∪ [x = 1]3 )
For reasoning about local registers, we employ a version of the standard tech-
nique of backward substitution from the rule of assignment of Hoare-logic1, i.e.,

                        e[r := v ] ⊆ wlp(T (t , rd RS (x , r , v ))), e)

where e ∈ Exp is an expression on local variables only and [r := v ] means
replacing all occurrence of r by value v . For (i) we then have

          (r1 6= 1) = (r1 6= 1[r2 := v ]) ⊆ wlp(T (3, rd RS (y, r2 , v )), r1 6= 1)

For (ii) we look at two cases. First, let v = 1. Using the monoticity of wlp we get

           hy = 1iS [x = 1]3 = wlp(T (3, rd RS (y, r2 , 1)), [x = 1]3 )
                               ⊆ wlp(T (3, rd RS (y, r2 , v )), r2 6= 1 ∪ [x = 1]3 )

In the case v 6= 1, we need Lemma 2 and therefore the axioms C3, SV1, SV2,
RW2, and RW3 have to hold. Because of the disjunctivity of wlp we get

           hy = 1iS [x = 1]3 ⊆ Σ
                               v 6=1
                                = (r2 6= 1[r2 := v ]) ∪ [x = 1]3
                               ⊆ wlp(T (3, rd RS (y, r2 , v )), r2 6= 1 ∪ [x = 1]3 )

    Many steps of such correctness proofs are complex, time consuming and
repetitive. In the next section we summarize multiple such steps into proof rules
and thereby lift reasoning to the higher level of syntactic assertions, not employ-
ing weakest preconditions anymore.
                True                         False
                        {P } comt {true}              {false} comt {P }
                              P1 ⊇ P2   Q1 ⊆ Q2 {P1 } comt {Q1 }
                    Mono
                                        {P2 } comt {Q2 }
                              {P1 } comt {Q1 } {P2 } comt {Q2 }
                       Conj
                                  {P1 ∩ P2 } comt {Q1 ∩ Q2 }
                              {P1 } comt {Q1 } {P2 } comt {Q2 }
                       Disj
                                  {P1 ∪ P2 } comt {Q1 ∪ Q2 }

                                  Fig. 5. General rules


4     Rules
In this section we explain our novel proof rules for the axiomatic reasoning. Re-
member that for a program command comt in a thread t , we prove {P } comt {Q }
for assertions P , Q ∈ A by showing

                                  P ⊆ wlp(T (t , a), Q )

where a is the action in comt . Some interim results of those proofs can be
generalised and lifted to the higher level of syntactic assertions. We formalise
them in the form of rules which then can be used to directly prove the correctness
of a proof outline without the need of weakest preconditions.
    We start by giving general rules (Fig. 5) which hold regardless of the validity
of axioms. Those rules are all in the original Hoare-logic form [15] and are here
translated to our setting. For the rules True and False note that the assertions
{true} and {false} describe the set of states Σ and the empty set, respectively.
With that in mind both rules follow directly from our definition of Hoare-triple.
The intuitive idea of the Mono rule are that a Hoare-triple still holds if the
pre-assertion becomes stronger or the post-assertion weaker. The first follows by
definition and the second from the monotonicity of wlp (see Fig. 2). Analogously,
the rules Conj and Disj formalise the conjunctivity and disjunctivity properties
of Figure 2. Hence we get the following Theorem.
Theorem 1. The general proof rules in Figure 5 are sound.
The proof of the theorem can be found in the appendix. Note that these rules
can be used to combine different Hoare-triples from other rules.
    Next we look at rules specific to a certain program command and start with
fence actions. If we formalise the property given in Lemma 1, we get the first
rule of Figure 6: Fence1. Note that with regard to showing global correctness,
the rule implies the following lemma.
Lemma 3. In every proof outline fence actions are globally correct for β-stable
assertions, i.e., for every assertions G ∈ G and P ∈ A: {G ∩ P } fnct {G}.
1
    Such backward substitution is sound here as it only considers local registers.
                          P ∈ G C 3 SV 1 SV 2                                 FNC
   Fence1(Lemma 1)                                          Fence2
                               {P } fnct {P }                          {x↑t } fnct {x↑t ′ }

                   Fence3 C 2       C 3 SV 1 SV 2 RW 6 FNC
                                    {[x = v ]t } fnct {[x = v ]t ′ }

                                    Fig. 6. Fence rules

                                  P ∈G      C3     SV 1 SV 2 RW 2 RW 3
            Read1(Lemma 2)
                                                 {P } r :=t x {P }
    Read2                                        Read3
             {[x 6≈ v ]t } r :=t x {r 6= v }              {[x = v ]t } r :=t x {r = v }
             ConRead1
                              {hx = v i[x = v ]t } r :=t x {r 6= v ∪ [x = v ]t }
            ConRead2
                            {hx = v iS [y = u]t } r :=RS
                                                       t x {r 6= v ∪ [y = u]t }

                       P ∈ L r 6∈ reg(P )                         r 6∈ reg(P )
         ReadReg                                  LocRead
                        {P } r :=t x {P }                      {P } r :=t E {P }

        Fig. 7. Read rules (reg(P ) being the local registers occurring in P )



The FNC Axiom is formalised in Fence2 and if we additionally assume the
axioms C2 and RW6 we can not only pass view-maximality to a different thread,
but also the value that can be read. In the appendix we show the following
theorem.

Theorem 2. The fence proof rules in Figure 6 are sound.

    For read actions (Fig.7) we similarly formalise Lemma 2 in rule Read1 and
get the following lemma.

Lemma 4. In every proof outline read actions are globally correct for β-stable
assertions, i.e., for every assertions G ∈ G and P ∈ A: {G ∩ P } r :=t v {G}.

The rules Read2, Read3, ConRead1 and ConRead2 describe how we re-
place different global assertions (containing x ) by local ones (containing r ) after
reading the value of x to r . Here Read2 says that if thread t cannot read v
for x , then after reading x to r , r cannot be v . Analogous in Read3 where t
cannot read a value different from v for x and is view maximal (which means
that t can read the most up-to-date value for x ), after the read, r has to be
equal to v . If we have a conditional observation assertion hx = v i[x = v ]t and
read in the same thread from x , then either we do not read v or [x = v ]t holds
afterwards (ConRead1). We get a similar rule for the synchronized read and
the synced conditional observation (ConRead2). ReadReg tells us that a lo-
cal assertion remains unchanged after a read to a register which is not included
in the assertion. In LocRead we describe that an assertion will not change, if
we read a local expression to a register. In this case the register must not be
                                    x 6= y C 3 SV 1
                     Write1
                             {[y 6≈ u]t ′ } x :=t E {[y 6≈ u]t ′ }
                                    x 6= y C 3 SV 1
                    Write2
                             {[y ≡ u]t ′ } x :=t E {[y ≡ u]t ′ }
           x 6= y C 3 SV 2                           x 6= y C 3 SV 1 SV 2
   Write3                            Write4
          {y↑t ′ } x :=t E {y↑t ′ }               {[y = u]t ′ } x :=t E {[y = u]t ′ }
                   C3 C4                          JE K = v C 3 C 4 RW 5 RW 6
  Write5                                Write6
             {x↑t } x :=t E {x↑t }                  {[x = u]t } x :=t E {[x = v ]t }
                             JE K = v t 6= t ′ C 2 C 3 C 4
         ConWrite1 SV 1 SV 2 RW 2 RW 3 RW 5 RW 6 RW 7
                   {[x 6≈ v ]t ′ ∩ [x = u]t } x :=t E {hx = v i[x = v ]t ′ }
                            JE K = v t 6= t ′ x 6= y C 2 C 3
        ConWrite2       SV 1 SV 2 RW 2 RW 3 RW 6 MP
                  {[x 6≈ v ]t ′ ∩ [y = u]t } x :=WS
                                                 t  E {hx = v iS [y = u]t ′ }
                                             P ∈L
                     WriteReg
                                      {P } x :=t E {P }

                                     Fig. 8. Write rules



included in the assertion. Note that by reg(P ) we mean the set of registers in P .
Summarised we get

Theorem 3. The read proof rules in Figure 7 are sound.

which we also proved in the appendix.
      In Figure 8 we formalised rules for write actions. There we differentiate be-
tween global assertions about the variable written to and about other variables.
In both cases we need the C3 axiom. This allows us to apply a hand full of
axioms that describe properties of interf , e.g., SV1 and SV2. For different vari-
ables we can pass readability of a value with the axiom SV1 (see rules Write1
and Write2). If we want to pass view-maximality (Write3), we need SV2.
The rule Write4 combines Write2 and Write3. In the case where the asser-
tion contains the same variable as the write action, we can use the axiom C4 to
pass view-maximality (Write5). If we additionally assume RW5 and RW6, we
can update the value thread t can read (Write6). If we write a new value to x
(which means that before the write, t and t ′ could not read v ) in a view-maximal
thread t , then if t ′ can read v , it also has to be view-maximal. This behaviour is
decribed in rule ConWrite1. We need to assume RW7 to pass the conditional
view-maximality to a different thread. The rule ConWrite2 describes message
passing. If t ′ can read v for x and t can read u for y and is view-maximal in
t , then if we write v to x in t , [y = u]t ′ only holds if we can read v for x in
t ′ . This behaviour only differs from ConWrite1 by allowing different variables.
Because of this, we cannot apply RW7 and need MP. Hence this rule only holds
for synchronised writes. The last rule of Figure 8 (WriteReg) formalises the
    Table 1. Rules employed for showing local correctness of the WRC proof outline

        comt         Hoare-Triples             Proof Rules     Axioms
        x :=1 1 {P1,1 } x :=1 1 {P1,2 }           True
        r1 :=2 x {P2,1 } r1 :=2 x {P2,2 }   Read1, ReadReg, C3, SV1, SV2,
                                            Read3, ConRead1  RW2, RW3
        y :=WS
             2 1 {P2,2 } y :=2 1 {P2,3 }          True
        r2 :=RS
              3 y {P3,1 } r2 :=3 y {P3,2 } ReadReg, ConRead2
        r3 :=3 x {P3,2 } r3 :=3 x {P3,3 } ReadReg, Read3



fact that a write will not change the value of a register. In the appendix, we
prove

Theorem 4. The write proof rules in Figure 8 are sound.
With all these rules being sound, we can now prove correctness much easier and
shorter. Also we then know exactly which axioms we need for a certain proof
outline to be valid.


5     Correctness Proof of WRC via Proof Rules

In this section, we finally apply our rules to the correctness proof of the WRC
example in Figure 1.

Lemma 5. The proof outline in Figure 1 is valid under the axioms C2, C3,
C4, SV1, SV2, RW2, RW3, RW5, RW6, RW7 and MP.

This means that the proof outline holds for every memory model that satisfies
the axioms named.
    To prove this lemma, we have to check every Hoare-triple that we need for
local and global correctness (see Def. 4). Starting with local correctness, Table 1
gives us an overview of every Hoare-triple we need to prove. In there we see which
proofs require which rules and thus which axioms. For better readability, we have
omitted the use of the rules Mono, Conj and Disj. One of the Hoare-triples is

         {r1 6= 1 ∪ hy = 1iS [x = 1]3 } r2 :=RS
                                             3 y {r1 6= 1 ∪ r2 6= 1 ∪ [x = 1]3 }

which we already proved at the end of Section 2. With our novel proof rules
at hand we can show its validity with a fewer number of steps. As written in
Table 1 we need the rules ReadReg and ConRead2. The first one tells us

                             {r1 6= 1} r2 :=RS
                                            3 y {r1 6= 1}

and with ConRead2 we get

                  {hy = 1iS [x = 1]3 } r2 :=RS
                                            3 y {r2 6= 1 ∪ [x = 1]3 }
Table 2. Rules employed for showing global correctness of the WRC proof outline

comt             Hoare-Triples             Proof Rules          Axioms
x :=1 1   {P1,1 ∩ P2,1 } x :=1 1 {P2,1 }    Write1,         C2, C3, C4, SV1,
                                           WriteReg,        SV2, RW2, RW3,
                                           ConWrite1        RW5, RW6, RW7
         {P1,1 ∩ P2,2 } x :=1 1 {P2,2 } Write1, WriteReg        C3, SV1
         {P1,1 ∩ P2,3 } x :=1 1 {P2,3 }       True
         {P1,1 ∩ P3,1 } x :=1 1 {P3,1 }    WriteReg
         {P1,1 ∩ P3,2 } x :=1 1 {P3,2 }    WriteReg
         {P1,1 ∩ P3,3 } x :=1 1 {P3,3 }    WriteReg
r1 :=2 x {P2,1 ∩ P1,1 } r1 :=2 x {P1,1 }     Read1,          C3, SV1, SV2,
                                             Read3            RW2, RW3
         {P2,1 ∩ P1,2 } r1 :=2 x {P1,2 }      True
         {P2,1 ∩ P3,1 } r1 :=2 x {P3,1 }     Read1           C3, SV1, SV2,
                                                              RW2, RW3
          {P2,1 ∩ P3,2 } r1 :=2 x {P3,2 }    ReadReg
          {P2,1 ∩ P3,3 } r1 :=2 x {P3,3 }    ReadReg
y :=SW
     2  1 {P2,2 ∩ P1,1 } y :=2 1 {P1,1 } Write1, Write4,     C3, SV1, SV2
                                             WriteReg
          {P2,2 ∩ P1,2 } y :=2 1 {P1,2 }       True
          {P2,2 ∩ P3,1 } y :=2 1 {P3,1 }    WriteReg,      C2, C3, SV1, SV2,
                                            ConWrite2     RW2, RW3, RW6, MP
          {P2,2 ∩ P3,2 } y :=2 1 {P3,2 }     WriteReg
          {P2,2 ∩ P3,3 } y :=2 1 {P3,3 }     WriteReg
r2 :=SR
      3 y {P3,1 ∩ P1,1 } r2 :=3 y {P1,1 }     Read1,        C3, SV1, SV2,
                                             ReadReg          RW2, RW3
          {P3,1 ∩ P1,2 } r2 :=3 y {P1,2 }      True
          {P3,1 ∩ P2,1 } r2 :=3 y {P2,1 }     Read1,        C3, SV1, SV2,
                                              Read2           RW2, RW3
          {P3,1 ∩ P2,2 } r2 :=3 y {P2,2 } Read1, ReadReg,   C3, SV1, SV2,
                                              Read2           RW2, RW3
          {P3,1 ∩ P2,3 } r2 :=3 y {P2,3 }      True
r3 :=3 x {P3,1 ∩ P1,1 } r3 :=3 x {P1,1 }      Read1,        C3, SV1, SV2,
                                             ReadReg          RW2, RW3
          {P3,1 ∩ P1,2 } r3 :=3 x {P1,2 }      True
          {P3,1 ∩ P2,1 } r3 :=3 x {P2,1 }     Read1,        C3, SV1, SV2,
                                             ReadReg          RW2, RW3
          {P3,1 ∩ P2,2 } r3 :=3 x {P2,2 }     Read1,        C3, SV1, SV2,
                                             ReadReg          RW2, RW3
          {P3,1 ∩ P2,3 } r3 :=3 x {P2,3 }      True
Applying the Disj-rule we are done. Analogously we can now prove every Hoare-
triple. In this way we need significantly fewer steps to prove one triple than we
did in Section 2. Hence the entire correctness proof (which contains the proof of
31 Hoare-triple for Figure 1) is easier and shorter to prove, simply by applying
the abstract proof rules. An overview of all the rules used for global correctness
is given in Table 2. Due to the non-interference condition in Owicki-Gries style
proofs, there are still a number of proof steps to be done, however significantly
fewer than on the level of axioms. The number of proof steps could furthermore
be reduced by employing a compositional proof technique like rely-guarantee
reasoning [28]. For this, the same proof rules are sound.


6   Related Work

There are a number of approaches which propose novel program logics for weak
memory models. The view-based logic we employ here has first appeared in [13, 9]
for C11 RAR and has then been generalized to the generic reasoning approach
in [12]. The work in [4] uses (and extends) view-based assertions to persistent
memory, but does not develop a memory model independent technique. Similarly,
Lahav et al. [18] propose a new program logic for the strong-release-acquire
model of [17] and employ rely-guarantee reasoning. While the rely-guarantee
framework is independent of a concrete memory model, the program logic is
not.
    Besides that there are verification techniques which are applicable to sev-
eral memory models. Alglave and Cousot [2] present an invariance proof method
which shows that a given program is correct w.r.t. a given memory model and an
invariant specification of that program. It does so by first proving that a so-called
communication specification is sufficient for the program’s invariant. If a memory
model guarantees the communication, the program is correct under that model.
Ponce de Leon et al. [22] and Gavrilenko et al. [14] present generic bounded
model checkers which translate a given program under a given memory model
into an SMT formula. They are generic because their input contains not only
the program but also the memory model, formalised in CAT as a set of relations.
Kokologiannakis et al. [16] developed a generic model checker that transforms
a given program into an execution graph to check its correctness under a given
memory model with an axiomatic semantics. Colvin [6] proposes a special se-
quential composition operator which mimics the reordering behaviour of many
weak memory models. Coughlin et al. [7, 8] discuss rely-guarantee reasoning for
weak memory models in general and introduce a specific new verification condi-
tion called reordering-interference-freedom. This technique can be instantiated
to memory models with a reordering semantics.
    Our approach discussed here lifts the generic reasoning technique of [12] to
the syntactic level, allowing to construct proof outlines operating on the level
of program instructions and view-based assertions. Thereby, we avoid low-level
reasoning about weakest preconditions while still preserving genericity.
7   Conclusion

In this paper, we have proposed high level proof rules lifting the generic reasoning
principle of [12] to a more abstract level. Similar to standard Hoare-logic, our
proof rules allow to reason on the syntactic level of assertions, departing from the
semantic level of weakest preconditions. This significantly simplifies reasoning,
and moreover allows us to directly see which axioms have been used in a proof.
We have exemplified our proof technique by providing a generic correctness proof
for the WRC litmus test. By the results of [12] (showing that SC, TSO and
C11 RAR instantiate all axioms), this proof is valid for WRC running on a
sequentially consistent as well as the TSO and C11 memory models.


References
 1. Adve, S.V., Gharachorloo, K.: Shared memory consistency models: A tutorial.
    Computer 29(12), 66–76 (1996). https://doi.org/10.1109/2.546611
 2. Alglave, J., Cousot, P.: Ogre and pythia: an invariance proof method for weak
    consistency models. In: Castagna, G., Gordon, A.D. (eds.) POPL. pp. 3–18. ACM
    (2017). https://doi.org/10.1145/3009837.3009883
 3. Bargmann, L., Wehrheim, H.: View-Based Axiomatic Reasoning for PSO. In: TASE
    (2023), to appear
 4. Bila, E.V., Dongol, B., Lahav, O., Raad, A., Wickerson, J.: View-based
    Owicki-Gries reasoning for persistent x86-TSO. In: Sergey, I. (ed.) ESOP. Lec-
    ture Notes in Computer Science, vol. 13240, pp. 234–261. Springer (2022).
    https://doi.org/10.1007/978-3-030-99336-8 9
 5. Boehm, H., Adve, S.V.: Foundations of the C++ concurrency memory model.
    In: Gupta, R., Amarasinghe, S.P. (eds.) PLDI. pp. 68–78. ACM (2008).
    https://doi.org/10.1145/1375581.1375591
 6. Colvin, R.J.: Parallelized sequential composition and hardware weak mem-
    ory models. In: Calinescu, R., Pasareanu, C.S. (eds.) SEFM. Lecture
    Notes in Computer Science, vol. 13085, pp. 201–221. Springer (2021).
    https://doi.org/10.1007/978-3-030-92124-8 12
 7. Coughlin, N., Winter, K., Smith, G.: Rely/Guarantee Reasoning for Multicopy
    Atomic Weak Memory Models. In: Huisman, M., Pasareanu, C.S., Zhan, N. (eds.)
    FM. Lecture Notes in Computer Science, vol. 13047, pp. 292–310. Springer (2021).
    https://doi.org/10.1007/978-3-030-90870-6 16
 8. Coughlin, N., Winter, K., Smith, G.: Compositional reasoning for
    non-multicopy atomic architectures. Form. Asp. Comput. (dec 2022).
    https://doi.org/10.1145/3574137, just Accepted
 9. Dalvandi, S., Doherty, S., Dongol, B., Wehrheim, H.: Owicki-Gries Reason-
    ing for C11 RAR. In: Hirschfeld, R., Pape, T. (eds.) ECOOP. pp. 11:1–
    11:26. LIPIcs, Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2020).
    https://doi.org/10.4230/LIPIcs.ECOOP.2020.11
10. Dalvandi, S., Dongol, B., Doherty, S., Wehrheim, H.: Integrating Owicki-Gries for
    C11-style memory models into Isabelle/HOL. J. Autom. Reason. 66(1), 141–171
    (2022). https://doi.org/10.1007/s10817-021-09610-2
11. Dijkstra, E.W.: A Discipline of Programming. Prentice-Hall (1976),
    https://www.worldcat.org/oclc/01958445
12. Doherty, S., Dalvandi, S., Dongol, B., Wehrheim, H.: Unifying operational weak
    memory verification: An axiomatic approach. ACM Trans. Comput. Log. 23(4),
    27:1–27:39 (2022). https://doi.org/10.1145/3545117
13. Doherty, S., Dongol, B., Wehrheim, H., Derrick, J.: Verifying C11 programs opera-
    tionally. In: PPoPP. pp. 355–365 (2019). https://doi.org/10.1145/3293883.3295702
14. Gavrilenko, N., de León, H.P., Furbach, F., Heljanko, K., Meyer, R.: BMC for
    weak memory models: Relation analysis for compact SMT encodings. In: Dillig,
    I., Tasiran, S. (eds.) CAV. Lecture Notes in Computer Science, vol. 11561, pp.
    355–365. Springer (2019). https://doi.org/10.1007/978-3-030-25540-4 19
15. Hoare, C.A.R.: An axiomatic basis for computer programming. Commun. ACM
    12(10), 576–580 (1969). https://doi.org/10.1145/363235.363259
16. Kokologiannakis, M., Raad, A., Vafeiadis, V.: Model checking for weakly consistent
    libraries. In: McKinley, K.S., Fisher, K. (eds.) PLDI. pp. 96–110. ACM (2019).
    https://doi.org/10.1145/3314221.3314609
17. Lahav, O., Boker, U.: What’s decidable about causally consistent shared
    memory? ACM Trans. Program. Lang. Syst. 44(2), 8:1–8:55 (2022).
    https://doi.org/10.1145/3505273
18. Lahav, O., Dongol, B., Wehrheim, H.: Rely-guarantee reasoning for causally con-
    sistent shared memory. In: CAV (2023), to appear
19. Lahav, O., Giannarakis, N., Vafeiadis, V.: Taming release-acquire consis-
    tency. In: Bodı́k, R., Majumdar, R. (eds.) POPL. pp. 649–662. ACM (2016).
    https://doi.org/10.1145/2837614.2837643
20. Lahav, O., Vafeiadis, V.: Owicki-Gries Reasoning for Weak Memory Models. In:
    Halldórsson, M.M., Iwama, K., Kobayashi, N., Speckmann, B. (eds.) ICALP.
    Lecture Notes in Computer Science, vol. 9135, pp. 311–323. Springer (2015).
    https://doi.org/10.1007/978-3-662-47666-6 25
21. Lamport, L.: How to make a multiprocessor computer that correctly exe-
    cutes multiprocess programs. IEEE Trans. Computers 28(9), 690–691 (1979).
    https://doi.org/10.1109/TC.1979.1675439
22. de León, H.P., Furbach, F., Heljanko, K., Meyer, R.: BMC with memory models
    as modules. In: Bjørner, N.S., Gurfinkel, A. (eds.) FMCAD. pp. 1–9. IEEE (2018).
    https://doi.org/10.23919/FMCAD.2018.8603021
23. Maranget,        L.,   Sarkar,   S.,   Sewell,    P.:   A    Tutorial     Introduc-
    tion     to     the    ARM      and   POWER         Relaxed    Memory       Models.
    https://www.cl.cam.ac.uk/~ pes20/ppc-supplemental/test7.pdf                 (2012),
    accessed: May, 2022
24. Owicki, S.S., Gries, D.: An axiomatic proof technique for parallel programs I. Acta
    Inf. 6, 319–340 (1976). https://doi.org/10.1007/BF00268134
25. Ridge,      T.:      A    Rely-Guarantee     Proof     System      for   x86-TSO.
    In:    VSTTE.         LNCS,    vol.  6217,     pp.    55–70.    Springer    (2010),
    https://doi.org/10.1007/978-3-642-15057-9_4
26. Sarkar, S., Sewell, P., Nardelli, F.Z., Owens, S., Ridge, T., Braibant, T.,
    Myreen, M.O., Alglave, J.: The semantics of x86-CC multiprocessor machine
    code. In: Shao, Z., Pierce, B.C. (eds.) POPL. pp. 379–391. ACM (2009).
    https://doi.org/10.1145/1480881.1480929
27. Wehrheim, H., Bargmann, L., Dongol, B.: Reasoning about promises in weak mem-
    ory models with event structures. In: Chechik, M., Katoen, J., Leucker, M. (eds.)
    FM. Lecture Notes in Computer Science, vol. 14000, pp. 282–300. Springer (2023).
    https://doi.org/10.1007/978-3-031-27481-7 17
28. Xu, Q., de Roever, W.P., He, J.: The Rely-Guarantee Method for Verifying Shared
    Variable Concurrent Programs. Formal Aspects Comput. 9(2), 149–174 (1997),
    https://doi.org/10.1007/BF01211617


A     Proofs

Here you can find the soundness proofs of the theorems in Section 4. We prove
them by showing that each of the rules is sound.


A.1   Proof of Theorem 1

Proof of True. For every assertion P and every action a we have

                            P ⊆ Σ = wlp(T (t , a), Σ).

This holds because of the non-abortion of wlp.


Proof of False. For every assertion P and every action a we have

                               ∅ ⊆ wlp(T (t , a), P ).


Proof of Mono. Let {P1 }comt {Q1 }, P1 ⊇ P2 and Q1 ⊆ Q2 . This means
P2 ⊆ P1 ⊆ wlp(T (t , a), Q1 ) for the action a in comt . With the monotonicity
property of wlp we get {P2 }comt {Q2 }.


Proof of Conj. Let {P1 }comt {Q1 } and {P2 }comt {Q2 }. For the action a in
comt this means P1 ⊆ wlp(T (t , a), Q1 ) and P2 ⊆ wlp(T (t , a), Q2 ). Using the
conjunctivity of wlp we get P1 ∩ P2 ⊆ wlp(T (t , a), Q1 ∩ Q2 ).


Proof of Disj. Let {P1 }comt {Q1 } and {P2 }comt {Q2 }. For the action a in
comt this means P1 ⊆ wlp(T (t , a), Q1 ) and P2 ⊆ wlp(T (t , a), Q2 ). Using the
disjunctivity of wlp we get P1 ∪ P2 ⊆ wlp(T (t , a), Q1 ∪ Q2 ).


A.2   Proof of Theorem 2

Proof of Fence1. Follows directly from Lemma 1.


Proof of Fence2. Using the FNC axiom and the conjunctivity of wlp we get

                           x↑t ⊆ wlp(T (t , fence), x↑t ′ ).
 Proof of Fence3. Assume the axioms C2, C3, SV1, SV2, RW6 and FNC hold.
 We devide the proof of
                          [x = v ]t ⊆ wlp(T (t , fence), [x = v ]t ′ )

 into the following parts
  (i) x↑t ⊆ wlp(T (t , fence), x↑t ′ )
 (ii) [x = v ]t ⊆ wlp(T (t , fence), [x = v ]t )
(iii) [x = v ]t ∩ x↑t ′ ⊆ [x = v ]t ′
 (i) follows from the proof of Fence 2 (for which we need FNC) and (ii) from
 the proof of Fence 1 (for which we need C3, SV1 and SV2). Hence we only
 prove (iii). Because of the axiom RW6 for σ ∈ [x = v ]t ∩ x↑t ′ exists a u ∈ Val
 such that σ ∈ [x = v ]t ∩ x↑t ′ ∩ [x ≡ u]t ′ . Since C2 also holds, u = v and therefore
 σ ∈ [x = v ]t ∩ x↑t ′ ∩ [x ≡ v ]t ′ ⊆ [x = v ]t ′ .

 With (i), (ii) and the conjunctivity of wlp we get [x = v ]t ⊆ wlp(T (t , fence), [x =
 v ]t ∩ x↑t ′ ) and because of (iii) and the monotonicity we have

                          [x = v ]t ⊆ wlp(T (t , fence), [x = v ]t ′ ).

 A.3       Proof of Theorem 3
       ′
 Let v ∈ Val be the value read.

 Proof of Read1. Follows directly from Lemma 2.

 Proof of Read2.
  – Case v ′ 6= v : We get
                      wlp(T (t , rd (x , r , v ′ )), r 6= v ) ⊇ (r 6= v [r := v ′ ])
                                                             =Σ
                                                             ⊇ [x 6≈ v ]t
  – Case v ′ = v : Then because of the monotonicity of wlp
                           [x 6≈ v ]t = wlp(T (t , rd (x , r , v )), ∅)
                                      ⊆ wlp(T (t , rd (x , r , v ′ )), r 6= v ′ )

 Proof of Read3.
  – Case v ′ = v : We get
                      wlp(T (t , rd (x , r , v ′ )), r = v ) ⊇ (r = v [r := v ′ ])
                                                             =Σ
                                                             ⊇ [x = v ]t
 – Case v ′ 6= v : Then because of the monotonicity of wlp

                             [x = v ]t ⊆ [x 6≈ v ′ ]t
                                       = wlp(T (t , rd (x , r , v ′ )), ∅)
                                        ⊆ wlp(T (t , rd (x , r , v ′ )), r = v )

Proof of ConRead1.
 – Case v ′ 6= v : We get with the monotonicity of wlp

        wlp(T (t , rd (x , r , v ′ )), r 6= v ∪ [x = v ]t ) ⊇ wlp(T (t , rd (x , r , v ′ )), r 6= v )
                                                            ⊇ (r 6= v [r := v ′ ])
                                                            =Σ
                                                            ⊇ hx = v i[x = v ]t

 – Case v ′ = v : Then because of the monotonicity of wlp

                 hx = v i[x = v ]t = wlp(T (t , rd (x , r , v )), [x = v ]t )
                                   ⊆ wlp(T (t , rd (x , r , v ′ )), r 6= v ∪ [x = v ]t )

Proof of ConRead2.
 – Case v ′ 6= v : We get with the monotonicity of wlp

      wlp(T (t , rd RS (x , r , v ′ )), r 6= v ∪ [y = u]t ) ⊇ wlp(T (t , rd RS (x , r , v ′ )), r 6= v )
                                                            ⊇ (r 6= v [r := v ′ ])
                                                            =Σ
                                                            ⊇ hx = v iS [y = u]t

 – Case v ′ = v : Then because of the monotonicity of wlp

               hx = v iS [y = u]t = wlp(T (t , rd RS (x , r , v )), [y = u]t )
                                     ⊆ wlp(T (t , rd RS (x , r , v ′ )), r 6= v ∪ [y = u]t )

Proof of ReadReg. We have

                        P = P [r := v ′ ] ⊆ wlp(T (t , rd (x , r , v ′ )), P )

Proof of LocRead. Let P be an assertion with r 6∈ reg(P ). The local program
semantics is described in [3, 12]. There we can see that r := E will only change
the value of r . Since r 6∈ reg(P ) every state in P is still in P after the action.

A.4     Proof of Theorem 4
Let JE K = v .
Proof of Write1. Assume the axioms C3 and SV1 hold. Because of the prop-
erties of wlp and β, we get

           [y 6≈ u]t ′ = wlp(T (t ′ , rd (y, r , u)), ∅)
                       ⊆ wlp(T (t ′ , rd (y, r , u)) o9 interf (t , wr (x , v )), ∅)
                       ⊆ wlp(interf (t , wr (x , v )) o9 T (t ′ , rd (y, r , u)), ∅)
                       = wlp(interf (t , wr (x , v )), wlp(T (t ′ , rd (y, r , u)), ∅))
                       = wlp(interf (t , wr (x , v )), [y 6≈ u]t ′ )
                       ⊆ wlp(β o9 interf (t , wr (x , v )) o9 β, [y 6≈ u]t ′ )
                       ⊆ wlp(T (t , wr (x , v )), [y 6≈ u]t ′ )

Proof of Write2. Assume the axioms C3 and SV1 hold. Because of Write1
we have for every u ′ 6= u {[y 6≈ u ′ ]t ′ }x :=t E {[y 6≈ u ′ ]t ′ }. With Conj we get
{[y ≡ u]t ′ }x :=t E {[y ≡ u]t ′ }.

Proof of Write3. Assume the axioms C3 and SV2 hold. Because of the prop-
erties of wlp and β, we get
          y↑t ′ ⊆ wlp(interf (t , wr (x , v )), y↑t ′ ) ⊆ wlp(T (t , wr (x , v )), y↑t ′ )

Proof of Write4. Assume the axioms C3, SV1 and SV2 hold. Because of the
rules Write2 and Write3 we have

              {[y ≡ u]t ′ }x :=t E {[y ≡ u]t ′ } and {y↑t ′ }x :=t E {y↑t ′ }

Then with Conj we get {[y = u]t ′ }x :=t E {[y = u]t ′ }.

Proof of Write5. Assume the axioms C3 and C4 hold. Because of the prop-
erties of wlp and β, we get

           x↑t ⊆ wlp(interf (t , wr (x , v )), x↑t ) ⊆ wlp(T (t , wr (x , v )), x↑t )

Proof of Write6. Assume the axioms C3, C4, RW5 and RW6 hold. Then we
know, because of Write5, RW5 and RW6
 – x↑t ⊆ wlp(T (t , wr (x , v )), x↑t )
 – Σ ⊆ wlp(T
         S (t , wr (x , v )), dom(T (t , Rd|x [v ])))
 – x↑t ⊆ u ′ ∈Val [x ≡ u ′ ]t
Using the conjunctivity of wlp, we get
                                                                                   [
    [x = u]t ⊆ wlp(T (t , wr (x , v )), x↑t ∩ dom(T (t , Rd|x [v ])) ∩                      [x ≡ u ′ ]t )
                                                                                 u ′ ∈Val
              = wlp(T (t , wr (x , v )), x↑t ∩ [x ≡ v ]t )
              = wlp(T (t , wr (x , v )), [x = v ]t )
 Proof of ConWrite1. Assume the axioms C2, C3, C4, SV1, SV2, RW2, RW3,
 RW5, RW6 and RW7 hold. RW7 says that

            x↑t ∩ [x 6≈ v ]t ′ ⊆ wlp(T (t , wr (x , v )), wlp(T (t ′ , rd (x , r , v )), x↑t ′ ))

 Additionally we know, because of Write6 and Read1

              [x = u]t ⊆ wlp(T (t , wr (x , v )), [x = v ]t )
                         ⊆ wlp(T (t , wr (x , v )), wlp(T (t ′ , rd (x , r , v ))[x = v ]t ))

 With C2 and RW6 we get [x = v ]t ∩ x↑t ′ ⊆ [x = v ]t ′ and therefore because of
 wlp’s properties

  [x = u]t ∩ [x 6≈ v ]t ′ ⊆ wlp(T (t , wr (x , v )), wlp(T (t ′ , rd (x , r , v ))[x = v ]t ∩ x↑t ′ ))
                          ⊆ wlp(T (t , wr (x , v )), wlp(T (t ′ , rd (x , r , v ))[x = v ]t ′ ))
                            ⊆ wlp(T (t , wr (x , v )), hx = v i[x = v ]t )


 Proof of ConWrite2. Assume the axioms C2, C3, SV1, SV2, RW2, RW3,
 RW6 and MP hold. To show that

             [x 6≈ v ]t ′ ∩ [y = u]t ⊆ wlp(T (t , wr WS (x , v )), hx = v iS [y = u]t ′ )

 holds for x 6= y and t 6= t ′ , we first prove

  (i) y↑t ∩ [x 6≈ v ]t ′ ⊆ wlp(T (t , wr WS (x , v )), wlp(T (t ′ , rd RS (x , r , v )), y↑t ′ ))
 (ii) y↑t ⊆ wlp(T (t , wr WS (x , v )), wlp(T (t ′ , rd RS (x , r , v )), y↑t ))
(iii) [y ≡ u]t ⊆ wlp(T (t , wr WS (x , v )), wlp(T (t ′ , rd RS (x , r , v )), [y ≡ u]t ))
(iv) y↑t ∩ [y ≡ u]t ∩ y↑t ′ ⊆ [y = u]t ′
 (v) [y = u]t ′ ⊆ hx = v iS [y = u]t ′

 Then because of the conjunctivity of wlp and (i)-(iii) we get

       [x 6≈ v ]t ′ ∩ [y = u]t
        ⊆ wlp(T (t , wr WS (x , v )), wlp(T (t ′ , rd RS (x , r , v )), y↑t ∩ [y ≡ u]t ∩ y↑t ′ ))

 and, because of the monotonicity, (iv) and (v), the rule is proven. Therefore we
 now prove (i)-(v).

 (i) With the MP Axion and the conjunctivity and monotonicity of wlp we get

                       wlp(T (t , wr WS (x , v )), wlp(T (t ′ , rd RS (x , r , v )), y↑t ′ ))
                       ⊇ y↑t ∩ wlp(T (t ′ , rd RS (x , r , v )), y↑t ′ )
                       ⊇ y↑t ∩ wlp(T (t ′ , rd RS (x , r , v )), ∅)
                       ⊇ y↑t ∩ [x 6≈ v ]t ′
(ii) Using the proofs of Read 1 (for which we need C3, SV1, Sv2, RW2 and
     RW3) and Write 3 (for which we need C3 and SV2) we get

                   wlp(T (t , wr WS (x , v )), wlp(T (t ′ , rd RS (x , r , v )), y↑t ))
                   ⊇ wlp(T (t ′ , wr WS (x , v )), y↑t )
                   ⊇ y↑t

(iii) Using the proofs of Read 1 (for which we need C3, SV1, SV2, RW2 and
      RW3) and Write 2 (for which we need C3 and SV1) we get

                wlp(T (t , wr WS (x , v )), wlp(T (t ′ , rd RS (x , r , v )), [y ≡ u]t ))
                ⊇ wlp(T (t , wr WS (x , v )), [y ≡ u]t )
                ⊇ [y ≡ u]t

(iv) Because of the axiom RW6 for σ ∈ y↑t ∩ [y ≡ u]t ∩ y↑t ′ exists a u ′ ∈ Val such
     that σ ∈ y↑t ∩ [y ≡ u]t ∩ y↑t ′ ∩ [y ≡ u ′ ]t ′ . Since C2 also holds, u = u ′ and
     therefore σ ∈ y↑t ∩ [y ≡ u]t ∩ y↑t ′ ∩ [y ≡ u]t ′ ⊆ [y = u]t ′
 (v) Because of the proof of Read 1 we get

                            [y = u]t ′
                             ⊆ wlp(T (t ′ , rd RS (x , r , v )), [y = u]t ′ )
                             = hx = v iS [y = u]t ′

Proof of WriteReg. In [3, 12] the local program semantics (which is inde-
pendent of the given memory model) is described. There we can see that a write
action will not effect the local state. Hence the rule holds.
