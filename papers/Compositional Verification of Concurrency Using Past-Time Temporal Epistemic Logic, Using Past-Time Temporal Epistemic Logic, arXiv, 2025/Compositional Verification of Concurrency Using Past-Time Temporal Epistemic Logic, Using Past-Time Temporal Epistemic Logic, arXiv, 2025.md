                                             Compositional Verification of Concurrency
                                             Using Past-Time Temporal Epistemic Logic

                                                                   Hamed Nemati and Mads Dam

                                                       KTH Royal Institute of Technology, Stockholm, Sweden
                                                                    {hnnemati, mfd}@kth.se
arXiv:2502.18885v3 [cs.LO] 23 Jun 2026




                                               Abstract. Shared-memory concurrency is notoriously difficult to rea-
                                               son about because each thread executes under interference from other
                                               threads. At the same time, many correctness arguments for classical al-
                                               gorithms are fundamentally epistemic: a thread enters a critical region
                                               only when, from its local view, it can rule out that another thread is
                                               concurrently in that region. We make such arguments explicit by intro-
                                               ducing a past-time temporal epistemic logic interpreted over interleav-
                                               ing executions with perfect recall over local histories. Past-time opera-
                                               tors support “since”-style reasoning, while epistemic modalities capture
                                               what a given thread can conclude from its own observation history. We
                                               give a semantics and a sound proof system, instantiate the logic to a sim-
                                               ple shared-memory language with instrumented read/write observations,
                                               and illustrate the approach on Peterson’s mutual exclusion algorithm:
                                               an epistemic condition established at the loop-exit step, combined with
                                               ownership-based stability obligations, yields global mutual exclusion. We
                                               additionally show how the logic embeds rely–guarantee reasoning as an
                                               epistemic stability-lifting principle, yielding a parallel-composition meta-
                                               theorem that matches the classical compatibility obligations.


                                         Keywords: Concurrency · Epistemic logic · Temporal logic · Rely–guarantee ·
                                         Program verification


                                         1   Introduction
                                         Correctness of shared-memory concurrent programs is notoriously sub-
                                         tle [26,18,25]. Even for safety properties, a proof must account for interference:
                                         while one thread executes, other threads can modify the shared store and
                                         invalidate reasoning that would be sound in a sequential setting. The enduring
                                         difficulty is to obtain arguments that are simultaneously local, so that they scale
                                         to realistic code, and robust, so that they imply global correctness properties
                                         such as mutual exclusion [27], linearizability [13], or freedom from data races.
                                             A recurring pattern in textbook correctness arguments is epistemic: threads
                                         make decisions based on what they can or cannot infer from their own actions and
                                         observations. In Peterson’s mutual exclusion algorithm [27], for example, each
                                         thread enters the critical section only after it has ruled out that the other thread
                                         will also enter. In lock-free code, a failed compare-and-swap provides evidence
2         Hamed Nemati and Mads Dam

that some other thread wrote a value [12]. Yet, mainstream assertion languages
for concurrent program logics are extensional [26,18,25,19]: they speak about
the current global state, but do not directly capture what a particular thread
knows given its partial view. As a result, proofs often encode epistemic reasoning
indirectly, e.g., via delicate global invariants or auxiliary (ghost) state.
    In this paper we advocate a lightweight assertion language based on past-time
temporal epistemic logic [6,10,11,22]. The epistemic modality KA φ states that φ
holds in all runs consistent with thread A’s observations; we use a perfect-recall
semantics where observations are represented as a prefix of A’s local history.
Past-time temporal operators (previously and since) allow us to talk about or-
dering and persistence of facts [28,22]. Crucially, we derive a local-time operator
PrevA φ that refers to the most recent moment before the current one at which
A executed a step. This enables thread-centric specifications and proofs that
abstract away arbitrarily many steps by other threads.
    We instantiate the logic1 to an interleaving semantics for shared-memory
programs where each step is executed by a single thread and performs at most
one shared-memory access (compound guards are desugared into read micro-
steps). Atomic propositions in the instantiation describe control-flow locations
and derived access markers. On top of this, we present a sound, sequent-style
proof system combining classical reasoning, a standard S5 basis for knowledge [6],
and fixed-point style rules for past-time temporal connectives [22]. We illustrate
the approach on Peterson’s algorithm by proving an epistemic fact about the
loop-exit step (expressed using our derived pre-state operator): whenever thread
i enters the critical section, it knows that the loop guard was false in the pre-
state of its last step. Combined with stability/ownership obligations, this yields
global mutual exclusion; as a corollary, a thread in the critical section knows
that the other is not.
    Beyond this argument, we show how the logic can serve as an assertion lan-
guage for compositional reasoning. In particular, we develop an epistemic variant
of rely–guarantee reasoning [18,30,5] in which rely/guarantee conditions are ex-
pressed as past-time temporal constraints on environment and component steps,
and thread-local knowledge assertions are connected to global invariants via sta-
bility obligations. To summarize, we make the following contributions:
    – We formalize an interleaving semantics for shared-memory programs that
      makes local histories explicit and supports perfect-recall epistemic reasoning.
    – We define a past-time temporal epistemic logic with a derived local-time
      operator PrevA and give a sound proof system.
    – We instantiate the logic to a simple shared-memory language with derived
      read/write access markers and demonstrate the expressiveness via an epis-
      temic proof sketch of Peterson’s mutual exclusion.
    – We show how the logic can be embedded into a rely–guarantee style proof
      method, and we use the running Peterson example to illustrate the resulting
      compositional reasoning obligations.
1
    Partial mechanization and verification of the base logic in Isabelle/HOL is available
    at https://github.com/FMSecure/pttel-theory
                            Past-Time Epistemic Reasoning for Concurrency           3

2    Motivation and Running Example
Epistemic view of interference. A thread reasons from a partial view: it can
only observe its local state and the values it reads from shared memory. In
our semantics, the modality KA ϕ means that ϕ holds at all points that are
indistinguishable to thread A given its entire observation history.

Last-step facts and stability. Many local proofs have the following shape. Thread
A executes a step, establishes a fact ϕ (typically by reading shared state), and
then the environment executes some number of steps. To use ϕ later, A needs an
argument that the environment cannot have falsified it. We express “the most
recent A-step” via an abbreviation PrevA ϕ (defined in §4) and use it to write

                            estA (ϕ) ≜ PrevA (KA ϕ).

The key rely–guarantee style reasoning principle we develop is: “if A established
ϕ at its last step and ϕ is stable under environmental interference since then,
then ϕ holds now.”

Running example: We use Peterson’s mutual exclusion algorithm for two threads,
0 and 1, as our running example. It uses shared variables flag[0], flag[1]
∈ {0, 1} and victim∈ {0, 1}:
            Listing 1.1. Peterson’s algorithm for thread i (with j = 1-i).
flag[i] = 1;
victim = i;
while (flag[j] == 1 && victim == i) { /* spin */ }
/* critical section */
flag[i] = 0;

   Our primary safety goal is mutual exclusion: Always ¬(InCS0 ∧InCS1 ), where
InCSi abbreviates “thread i is at its critical-section label”. We also use the ex-
ample to illustrate epistemic properties, e.g., how a thread can justify that a
guard it evaluated remains meaningful under permitted interference.


3    Program Model and Observations
We work with a simple interleaving model of shared-variable concurrency. The
intent is not to propose a new operational semantics, but to make precise the
semantic objects over which temporal and epistemic formulas are interpreted.

States and runs. Fix a finite set of thread identifiers Tid = {1, . . . , n}. A global
state s consists of:
 1. a shared store σ : Var → Val mapping shared variables to values, and
 2. for each thread A ∈ Tid , a local component λA containing a control location
    (program counter) and the values of its local variables.
4       Hamed Nemati and Mads Dam

We write s.σ for the shared store and s.λA for thread A’s local component.
                                                                            A
   The operational semantics induces a labelled transition relation s −     → s′ ,
meaning that s′ is obtained from s by executing one atomic step of thread A.
We assume interleaving (exactly one label per step) and consider infinite runs
π = s0 s1 s2 · · · where for each i ≥ 0 there exists a unique thread act(i) ∈ Tid
        act(i)
with si −−−→ si+1 . (Strictly, act depends on the run; we leave the run implicit
when it is clear from context.) We further assume the standard locality (thread-
                                                     A
                                                     → s′ , then s′ .λB = s.λB for
frame) property of shared-variable concurrency: if s −
every thread B ̸= A. That is, a step of one thread leaves the local components
of all other threads untouched (it may of course change the shared store and the
acting thread’s own local component). This property is what makes a thread’s
observation insensitive to interleaved steps of others, and we rely on it below
when relating histories across environment steps.

Scheduling predicate. We interpret A act at position (π, i) as the fact that thread
A performs the step from si to si+1 , i.e., act(i) = A.

Observations and perfect recall. A key modelling choice for epistemic logic is
what each thread can observe. We use the standard choice for shared-memory
programs: thread A observes its local component. Formally, the observation func-
tion is obsA (s) ≜ s.λA .
    Although obsA (s) exposes only A’s local component, this is not a restriction.
In a standard small-step semantics, a read from shared memory updates a local
register; hence the result of the read becomes part of λA , and therefore part of
A’s observation history. For example, in Peterson’s algorithm (Listing 1.1), eval-
uating the loop guard reads flag[j] and victim, and those values are reflected
in the control decision and (in an instrumented semantics) can be recorded in
locals. The logic therefore does not assume that a thread “magically” observes
the whole shared store; it reasons from the same information a sequential proof
would use: local state plus the values returned by reads.

Instrumentation of reads as observable locals. To make “what was read” explicit
in the state, so that it can be mentioned in atomic predicates or used in epis-
temic postconditions, we assume a lightweight instrumentation of the small-step
semantics. Concretely, for each thread A and each shared variable x that A may
read, we assume a distinguished local variable lrA  x (“A’s last-read register for
x”) that is updated on every A-step that reads x: if the pre-state shared store
satisfies σ(x) = v, then the read step sets lrAx := v in the post-state (in addi-
tion to any program-local register updates). Because lrA x is part of λA , the value
returned by a read is (i) remembered under perfect recall, and (ii) directly ad-
dressable by state predicates such as lrA
                                        x = v. This instrumentation does not add
“ghost information” beyond what the operational semantics already provides to
the executing thread; it only reifies read results as explicit local state.

Desugaring to single-access micro-steps. When a high-level command (e.g., a
compound guard) reads multiple shared variables, we assume it is compiled or
                                Past-Time Epistemic Reasoning for Concurrency                 5

desugared into a sequence of micro-steps, each performing at most one shared-
memory access and updating the corresponding last-read register lrA
                                                                  x . The Pe-
terson case study in §7 uses this standard desugaring.

Asynchrony and “no global clock”. Because observations are histories of local
states (and we do not assume a global clock is observable), a thread cannot
in general distinguish whether extra environment steps occurred while its local
state stayed the same. This stuttering-insensitivity is essential for modelling what
a thread can safely know between its own steps, and it matches the standard
asynchronous perfect-recall semantics used in the interpreted-systems literature.
    To model perfect recall, we compare points in the system by comparing entire
observation histories. Given a run π and time i, let k1 < · · · < km be the (possibly
empty) sequence of indices strictly below i at which A acts, i.e., act(kr ) = A for
r = 1, . . . , m and km < i. Define the history

       HistA (π, i) ≜ ⟨obsA (s0 ), obsA (sk1 +1 ), . . . , obsA (skm +1 ), obsA (si )⟩,

recording A’s initial observation, the observation in the post-state of each past
A-step, and the current observation. Two points (π, i) and (π ′ , i′ ) are indistin-
guishable to A, written (π, i) ∼A (π ′ , i′ ), iff HistA (π, i) = HistA (π ′ , i′ ). This is the
standard epistemic accessibility relation for asynchronous systems with perfect
recall; being defined by equality of histories, it is an equivalence relation. By
locality, if act(i) ̸= A then obsA (si+1 ) = obsA (si ) and the index i contributes
no new A-step, so HistA (π, i) = HistA (π, i + 1): a thread’s information set is
unchanged across steps it does not perform.

Atomic propositions. In addition to the scheduling predicate A act, we interpret
atomic propositions as predicates over global states. Concretely, we allow atoms
that test the values of shared variables (e.g., x = v) and atoms that test the
control location of a thread (e.g., at(A, ℓ), read “thread A is at location ℓ”). This
keeps the logic close to program states while remaining agnostic to a particular
instruction set.


4     Past-Time Temporal Epistemic Logic

This section defines the temporal–epistemic language used throughout the paper
and gives its semantics over the program model of §3.


4.1    Syntax

We assume a set AP of atomic state predicates p interpreted over global states
(e.g., equalities on shared variables and control-location tests such as at(A, ℓ)).
Formulas are generated as follows and we use ∨, →, and ↔ as abbreviations:

        ϕ, ψ ::= p | A act | ¬ϕ | ϕ ∧ ψ | Prev ϕ | ϕ Since ψ | KA ϕ.
6       Hamed Nemati and Mads Dam

4.2   State and transition formulas

For interference reasoning it is convenient to separate state properties from step
properties. A state formula is an extensional predicate: it is built from atomic
predicates p using Boolean connectives only (no Prev, Since, or K). Its truth
depends only on the current global state si (shared store and local components).
In contrast, the scheduling atom A act is a predicate of the transition label
act(i) (which thread executes the next step) and is therefore not a pure state
predicate under our model. Formulas with KA are also intensional : their truth
depends on the entire ∼A -information set induced by A’s observation history. A
transition formula (or step predicate) mentions the immediately preceding state
using Prev. For instance, (x ̸= Prev x) is intended to hold exactly when the
last transition changed the value of x. Strictly, Prev is an operator on formulas,
so an equation between a term and its previous value is syntactic sugar: for terms
t1 , t2 we read
                                           W                             
          t1 = Prev t2 ≜ Prev ⊤ →              v   t1 = v ∧ Prev (t2 = v) ,

i.e. “if a predecessor exists, the current value of t1 equals the value of t2 in that
state.” The guard Prev ⊤ makes the equation vacuously true at the initial time;
this is the intended reading, and it is what makes Always-guarded frame and
ownership conditions (§6, §7) satisfiable, since otherwise they would be falsified
at time 0. We write
                            chg(x) ≜ ¬ (x = Prev x),

so that chg(x) is false at time 0 and, at any time i > 0, holds exactly when the
transition from si−1 to si changed the value of x; we build further step predicates
on top of it below.

Convention. The atom A act is the outgoing label of the current state: (π, i) |=
A act iff the step from si to si+1 is performed by A. Readers familiar with an
incoming-label convention (in which a state is labelled by the step that pro-
duced it) should note that, in our setup, the incoming label at si is expressed as
Prev(A act). This choice is made once and used consistently.


4.3   Derived operators

We use standard derived past-time operators:

        Always ϕ ≜ ¬(⊤ Since ¬ϕ)             Sometime ϕ ≜ ⊤ Since ϕ.

Intuitively, Always ϕ means that ϕ has held at every state in the run prefix
up to the present, while Sometime ϕ means that ϕ held at some earlier state
(possibly the present).
                           Past-Time Epistemic Reasoning for Concurrency        7

4.4   Last-step operator
Rely–guarantee arguments often use facts established at a thread’s most recent
step. To express this, we distinguish the thread scheduled for the next transition
from the thread that executed the previous transition. Define the abbreviation

                            afterA ≜ Prev (A act),

so that afterA holds at time i iff i > 0 and the transition from si−1 to si was
performed by thread A. We then define the “last A-step” operator used in §2:

                    PrevA ϕ ≜ ¬afterA Since (afterA ∧ ϕ).                     (1)

Thus PrevA ϕ holds at (π, i) iff ϕ held at the most recent time j ≤ i such that
afterA held at j (i.e., the most recent state reached by an A-step), and afterA
did not hold at any k with j < k ≤ i. If thread A has not yet executed any step,
then afterA has never held, and PrevA ϕ is false.
    We also use the derived abbreviation preA ϕ ≜ PrevA (Prev ϕ), which refers
to the pre-state of A’s last step. In particular, if afterA holds now, then preA ϕ
is equivalent to Prev ϕ.

4.5   Write events and “last occurrence” reasoning
Using afterA and chg(x) we define a coarse write event:

                         WriteA (x) ≜ afterA ∧ chg(x).

Because we treat each program step as atomic, WriteA (x) holds at time i exactly
when the transition from si−1 to si was an A-step that changed x.
   Finally, we occasionally need “last occurrence” reasoning for events other
than “last A-step”. Generalizing (1), for any marker W we define

                       LastW (ϕ) ≜ ¬W Since (W ∧ ϕ).

For example, LastWriteA (x) (x = v) states that at the state reached by the most
recent A-write to x, the value of x was v.

Happens-before. We use a “happens-before” abbreviation to express that one
event was the most recent occurrence of its kind and was preceded by an occur-
rence of another:
                                                             
               ϕ ≺ ψ ≜ ¬ψ Since ψ ∧ Prev Sometime ϕ .

Thus ϕ ≺ ψ holds at (π, i) iff there is a most recent time j ≤ i at which ψ held,
and ϕ held at some strictly earlier time k < j. This is the pattern we actually
need: ψ is the event that just happened (no re-occurrence since), and ϕ already
happened before it. We use it in §7 for statements of the form “some victim=i
write occurred before the most recent victim=j write.”
8          Hamed Nemati and Mads Dam

4.6      Semantics

A model consists of the set of runs induced by the operational semantics (§3) to-
gether with the indistinguishability relations ∼A . We define satisfaction (π, i) |=
ϕ inductively:

    – (π, i) |= p iff p holds of the global state si .
    – (π, i) |= A act iff act(i) = A.
    – (π, i) |= ¬ϕ iff not (π, i) |= ϕ.
    – (π, i) |= ϕ ∧ ψ iff (π, i) |= ϕ and (π, i) |= ψ.
    – (π, i) |= Prev ϕ iff i > 0 and (π, i − 1) |= ϕ.
    – (π, i) |= ϕ Since ψ iff there exists j with 0 ≤ j ≤ i such that (π, j) |= ψ and
      for all k with j < k ≤ i, (π, k) |= ϕ.
    – (π, i) |= KA ϕ iff for all (π ′ , i′ ) with (π, i) ∼A (π ′ , i′ ), we have (π ′ , i′ ) |= ϕ.

    As ∼A is defined by equality of histories, it is an equivalence relation; con-
sequently KA satisfies the S5 principles: normality (the K axiom), truth (T,
factivity), and positive and negative introspection (4 and 5). Recall from §3
that, by locality, A’s history (hence its information set and its knowledge) is
unchanged across steps it does not perform.


5      A Sound Proof System

We present a deductive system for the fragment of the logic used in the sequel.
The system is intended to support paper-and-pencil proofs (and, ultimately,
automation); it is not meant as a complete axiomatization of all validities of
temporal–epistemic logic. Soundness is with respect to the semantics of §4.


5.1      Propositional core

A sequent has the form Γ ⊢ ϕ, where Γ isVa finite set of formulas (assumptions)
and ϕ is a formula (conclusion). We write Γ for the conjunction of all formulas
in Γ .
    We assume a standard sound sequent-style proof system for propositional
logic (conjunction, disjunction, and negation), including:

            Γ ⊢ϕ       Γ ⊢ϕ→ψ                     Γ, ϕ ⊢ ψ      Γ, ¬ϕ ⊢ ψ
                              (mp)                                        (lemE)
                     Γ ⊢ψ                                    Γ ⊢ψ

and the usual introduction/elimination rules for ∧ and ∨.


5.2      Past-time operators

The following rules capture the defining fixpoint properties of Prev and Since.
                            Past-Time Epistemic Reasoning for Concurrency         9

Previous.
                                Γ ⊢ϕ
                                               (prev)
                      Prev Γ ⊢ Prev ⊤ → Prev ϕ
where Prev Γ ≜ {Prev ψ | ψ ∈ Γ }. The guard Prev ⊤ ensures that we are
not at the initial time; without it, the derived form ⊢ Prev ϕ would be unsound
even when ⊢ ϕ (at time 0 there is no predecessor and every formula of the form
Prev ϕ is false). In practice one uses this rule in the form: if the current time
is not initial (i.e., Prev ⊤ is assumed) and all assumptions in Γ held at the
predecessor, then ϕ held there too.

Since.
       Γ ⊢ψ                        Γ ⊢ϕ      Γ ⊢ Prev(ϕ Since ψ)
                 (sinceI1 )                                      (sinceI2 )
   Γ ⊢ ϕ Since ψ                            Γ ⊢ ϕ Since ψ

      Γ ⊢ ϕ Since ψ       Γ, ψ ⊢ χ   Γ, Prev(ϕ Since ψ), ϕ ⊢ χ
                                                               (sinceE)
                                 Γ ⊢χ
Rule sinceI1 corresponds to choosing the witness time j = i. Rule sinceI2
corresponds to extending an existing witness by one step while maintaining
ϕ. Rule sinceE is the elimination rule corresponding to a single unfolding of
ϕSinceψ ≡ ψ ∨ (ϕ ∧ Prev(ϕSinceψ)): it splits on whether the witness is at
the current time (left case, hypothesis ψ) or strictly earlier (right case, hypothe-
ses ϕ and Prev(ϕSinceψ)). It is not an induction principle: its right premise
supplies Prev(ϕSinceψ), not the inductive hypothesis Prev χ, so it cannot by
itself propagate χ across unboundedly many steps.

Since-induction. For invariance reasoning we use the genuine least-fixpoint in-
duction rule for Since:
                Γ ⊢ψ→χ      Γ ⊢ (ϕ ∧ Prev χ) → χ
                                                 (sinceInd)
                     Γ ⊢ (ϕ Since ψ) → χ

Side condition: every formula in Γ is past-hereditary, i.e. holds at a point only
if it holds at all earlier points of the same run; Always-formulas (and Γ = ∅)
satisfy this. The decisive difference from sinceE is that the second premise
carries Prev χ as an inductive hypothesis, which is exactly what is needed to
transport χ along the “in between” interval of a Since witness. We will see
in §6 that the invariance Lemma 4 is an instance of sinceInd (with ϕ = ⊤,
ψ = Init ∧ I, and χ = Always I).
     We define Sometime and Always as abbreviations (§ 4); their usual derived
rules follow.


5.3      Epistemic operator

The epistemic modality follows the standard S5 principles for each thread A. We
present them as sequent rules.
10      Hamed Nemati and Mads Dam

Normality.
                                   Γ ⊢ϕ
                                            (K)
                                KA Γ ⊢ KA ϕ
where KA Γ ≜ {KA ψ | ψ ∈ Γ }.

Truth and introspection.
          Γ ⊢ KA ϕ             Γ ⊢ KA ϕ               Γ ⊢ ¬KA ϕ
                   (T)                    (4)                     (5)
           Γ ⊢ϕ               Γ ⊢ KA KA ϕ            Γ ⊢ KA ¬KA ϕ

5.4   Soundness
Theorem 1 (Soundness). If Γ ⊢ ϕ isVderivable, then Γ |= ϕ, i.e., for every
model and every point (π, i), if (π, i) |= Γ then (π, i) |= ϕ.
Proof (Proof sketch). Soundness of the propositional rules is standard; for the
remaining
V           rules we argue directly from the semantics. For prev, suppose (π, i) |=
   Prev Γ and (π, i) |= Prev ⊤. The latter gives i >V0, and (π, i) |= Prev ψ
yields (π, i − 1) |= ψ for each ψ ∈ Γ , so (π, i − 1) |= Γ . By soundness of the
premise Γ ⊢ ϕ we get (π, i − 1) |= ϕ, hence (π, i) |= Prev ϕ. Rules for Since
are sound by unfolding the semantic definition: sinceI1 takes the witness time
j = i; sinceI2 keeps the same witness time and extends the “in between” interval
by one step while preserving ϕ; sinceE is the elimination from one unfolding
(case split on whether the witness is at the current time or strictly
                                                                 V earlier). For
sinceInd, assume the premises and a point (π, i) with (π, i) |= Γ and (π, i) |=
ϕSinceψ; let j ≤ i be a witness, so (π, j) |= ψ and (π, k) |= ϕ for j < k ≤ i.
V show (π, m) |= χ for j ≤ m ≤ i by induction on m: the side condition makes
We
   Γ hold at every m ≤ i, so at m = j the first premise gives χ, and for m+1
the inductive hypothesis gives (π, m) |= χ, hence (π, m+1) |= Prev χ, and with
(π, m+1) |= ϕ the second premise gives χ; taking m = i yields (π, i) |= χ. Rules
K, T, 4, and 5 are sound because each ∼A is an equivalence relation, and KA
is interpreted as universal quantification over ∼A -accessible points.

6     Rely–Guarantee Style Reasoning via Stability
This section shows how a rely–guarantee style reasoning pattern emerges nat-
urally in past-time epistemic logic. The key ingredients are: (i) a way to talk
about the state reached by a thread’s last step (PrevA ·, §4), and (ii) a logical
characterization of stability under environment steps.

6.1   Step predicates and stability
Because the logic has only past-time operators, we express constraints on the
most recent transition using Prev and the tag afterA ≜ Prev(A act). For ex-
ample, the assertion “if the last step was by thread B, then shared variable x
did not change” is expressed as
                                                      
                      Always afterB → (x = Prev x) .
                             Past-Time Epistemic Reasoning for Concurrency     11

Definition 1 (Stability under the environment). Let A ∈ Tid and let ϕ
be a state formula (in the extensional fragment of §4). We say that ϕ is stable
under the environment of A if
                                                               
              StableA (ϕ) ≜ Always ¬afterA → (Prev ϕ → ϕ) .

      Intuitively, StableA (ϕ) means that any step not performed by A preserves ϕ.


6.2     Algebra of stable assertions

Stability is the logical form of the familiar rely–guarantee side condition “P is
stable under the rely”. A useful feature of Definition 1 is that stability can be
manipulated propositionally, which makes stability checks modular.

Lemma 1 (Closure properties). For any thread A and state formulas ϕ, ψ:

1. If StableA (ϕ) and StableA (ψ), then StableA (ϕ ∧ ψ).
2. If StableA (ϕ) and StableA (ψ), then StableA (ϕ ∨ ψ).

Proof (Proof sketch). Unfold Definition 1. For (1), use that Prev(ϕ∧ψ) is equiv-
alent to (Prev ϕ)∧(Prev ψ): on an environment step, Prev(ϕ∧ψ) implies both
Prev ϕ and Prev ψ, so the two stability assumptions yield ϕ and ψ now. For
(2), use that Prev(ϕ ∨ ψ) implies (Prev ϕ) ∨ (Prev ψ) and split cases.

   Note that stability is not closed under logical consequence in general; a short
counterexample is given in Appendix A.5.

Frame conditions yield stability. A very common rely condition is a frame prop-
erty saying that the environment does not change some variable x:
                                                              
               FrameA (x) ≜ Always ¬afterA → (x = Prev x) .

From FrameA (x) we can derive StableA (x = v) for any value v, and by Lemma 1
we can build stable assertions about tuples of frame-protected variables. In §7
we exploit exactly this pattern for the ownership assumptions on flag[i].


6.3     From last-step facts to current facts

The last-step operator PrevA ϕ is designed so that, if it holds at time i, then
there exists a unique time j ≤ i that is the most recent state reached by an
A-step, and ϕ held at j. Between j and i, all steps are by the environment (i.e.,
¬afterA holds on each intermediate state).

Lemma 2 (Stability lifting). For any thread A and any state formula ϕ,

                           StableA (ϕ) ∧ PrevA ϕ |= ϕ.
12      Hamed Nemati and Mads Dam

Proof (Proof sketch). Let (π, i) satisfy StableA (ϕ)∧PrevA ϕ, and let j ≤ i be the
witness time for PrevA ϕ in the semantics of Since (cf. (1)). By the definition
of PrevA ϕ we have (π, j) |= ϕ, and (π, k) |= ¬afterA for all k with j < k ≤ i. If
j = i the conclusion is immediate; otherwise we show (π, k) |= ϕ by induction on
k = j, . . . , i. The base case k = j is given. For the step, assume (π, k) |= ϕ with
j ≤ k < i; then k + 1 > 0, so (π, k + 1) |= Prev ϕ, while (π, k + 1) |= ¬afterA by
the hypothesis on PrevA ϕ. Stability then yields (π, k + 1) |= ϕ. Taking k = i
gives the claim.


6.4   What knowledge buys us: persistence without re-reading

A purely temporal statement PrevA ϕ says that ϕ held at A’s last step, but
it does not say that A is entitled to use ϕ as a justified local assumption. The
epistemic modality makes that justification explicit: if PrevA (KA ϕ) holds, then
A previously had enough observational evidence to rule out all alternatives where
ϕ fails.
    A key consequence of our asynchronous perfect-recall semantics is that a
thread’s information set does not change between its own steps. Therefore, if A
knew something at its last step, then it still knows it now (even if it has not
executed any further instructions).

Lemma 3 (Knowledge persistence between A-steps). For any thread A
and any formula ϕ,
                             PrevA (KA ϕ) |= KA ϕ.

Proof (Proof sketch). Let (π, i) |= PrevA (KA ϕ), and let j ≤ i be the witness
time, so that afterA ∧ KA ϕ holds at j and ¬afterA holds at every k with j < k ≤ i.
By the definition of PrevA ·, no A-step occurs strictly between j and i; hence,
by locality (§3), obsA is constant on that interval and no new A-step is recorded.
Consequently HistA (π, i) = HistA (π, j), i.e. (π, i) ∼A (π, j), so the ∼A -class is
the same at i and at j. Since KA ϕ holds at j, it holds at i.

   Lemma 3 explains why stability conditions are unavoidable: a thread can
carry forward knowledge, but to carry forward the truth of a state formula ϕ it
must also argue that the environment cannot falsify ϕ between its own steps.


Objective stability vs. epistemic quantification. StableA (ϕ) is evaluated on the
actual run (every environment step preserves ϕ), whereas KA ϕ quantifies over
all points compatible with A’s history. Under the closed-program convention
adopted below, the set of those alternatives is restricted to runs satisfying the
interface specification, which already includes the rely itself; as a result, Corol-
lary 1 draws the useful factivity conclusion (ϕ now) without having to wrap the
rely inside KA .
                           Past-Time Epistemic Reasoning for Concurrency       13

6.5   Epistemic rely–guarantee
In practice, a thread often establishes facts via local reasoning about what it
knows at its last step. Combining Lemma 2 with factivity of knowledge (the S5
axiom KA ϕ → ϕ) yields the following derived rule.

Corollary 1 (Epistemic stability lifting). For any thread A and any state
formula ϕ,
                   StableA (ϕ) ∧ PrevA (KA ϕ) |= ϕ.

Proof (Proof sketch). Although KA ϕ is not itself a state formula, factivity gives
KA ϕ → ϕ pointwise, so from PrevA (KA ϕ) we deduce PrevA ϕ (apply factivity
at the witness time j of the Since semantics in (1)). Lemma 2, applied to the
state formula ϕ, then yields ϕ at the current time.

   This corollary can be read as a rely–guarantee principle: “ if thread A es-
tablished ϕ at its last step (by knowing it then), and ϕ is stable under the
environment since that step, then ϕ holds now. ”

6.6   Encoding rely and guarantee conditions
A classic rely–guarantee proof assigns to each thread A a guarantee describing
what A may do in one step and a rely describing what the environment may do.
In our setting, a guarantee for A is naturally expressed as a formula of the shape

                        GA ≜ Always afterA → Gstep
                                                        
                                                     A    ,

where Gstep
         A is a predicate over the current state and the previous state (express-
ible using Prev). Similarly, a rely for A may be expressed as
                                                     step 
                       RA ≜ Always ¬afterA → RA             .

Compatibility of rely/guarantee assumptions becomes logical entailment obli-
gations between these formulas (e.g., GB |= RA for B ̸= A in the two-thread
case); the resulting parallel-composition step is summarized in §6.8. We use this
encoding in §7 to phrase the standard “ownership” assumptions of Peterson’s
algorithm (only thread i writes flag[i], and each thread writes victim only to
its own identifier).

Convention: rely/guarantee as model constraints. Rely/guarantee (and owner-
ship) clauses can be used in two natural ways in an epistemic setting, and in
the sequel we commit to one of them. (i) Closed-program reading (adopted here).
We fix an interface specification Φ, typically a conjunction of Always-guarded
step constraints such as guarantees and ownership clauses, and restrict atten-
tion to runs that satisfy Φ. Under this reading, KA quantifies only over alterna-
tives that also satisfy Φ, so relies may be used inside knowledge without extra
K-wrapping; any formula that holds at all points of the restricted model is au-
tomatically known by every thread. (ii) Open-system reading (not used in our
14      Hamed Nemati and Mads Dam

development). Here the clause is an assumption about the actual run, added to
the antecedent of an entailment but not restricting the epistemic alternatives.
Knowledge claims that depend on a rely then require an explicit hypothesis
KA RA . The two readings are logically consistent and interchangeable for proofs
that never appeal to knowledge about the rely itself; we adopt (i) throughout.

6.7   From rely–guarantee obligations to global invariants
A standard use of rely–guarantee is to prove that some global safety property I
is an invariant. In our past-time setting, the inductive step “I is preserved by
each transition” is captured by the step predicate
                                                               
                Pres(I) ≜ Always Prev ⊤ → (Prev I → I) ,

which says: whenever the current state has a predecessor, if I held there then I
holds now.
Lemma 4 (Invariant from step preservation). Let Init ≜ ¬Prev ⊤; this
atom holds only at time 0, so it marks the initial state syntactically. If I holds
initially and Pres(I) holds globally, then I has always held:

                 Sometime(Init ∧ I) ∧ Pres(I) |= Always I.

Proof (Proof sketch). Fix (π, i) satisfying both premises; we show (π, k) |= I
for every k ≤ i by induction on k. For k = 0: Init has unique witness 0, so
Sometime(Init ∧ I) forces (π, 0) |= I. For the step, assume (π, k) |= I with
k < i; then (π, k + 1) |= Prev I and, since k + 1 > 0, also (π, k + 1) |= Prev ⊤,
so the instance of Pres(I) at k + 1 yields (π, k + 1) |= I. Taking k = i gives
(π, i) |= I; as i was arbitrary, Always I holds.
    This is exactly the content of the Since-induction rule sinceInd (§5), in-
stantiated with ϕ = ⊤, ψ = Init ∧ I, χ = Always I, and Γ = {Pres(I)}
(an Always-formula, so the side condition holds). Its premises are discharged
within the calculus: the base Γ ⊢ (Init ∧ I) → Always I holds because Init
forces the current time to be 0, where Always I reduces to I; and the step
Γ ⊢ (⊤ ∧ Prev Always I) → Always I follows since Prev Always I gives I at
all earlier points while Pres(I) extends it to the present. The rule’s conclusion is
Sometime(Init ∧ I) → Always I, i.e. the lemma. (Note that the weaker unfold-
ing rule sinceE does not suffice here: its recursive premise would supply only
Prev Sometime(Init ∧ I), from which Pres(I)—which needs Prev I—cannot
fire.)

Compositional preservation checks. To establish Pres(I) compositionally, we can
split by which thread performed the last step. Define
                                                            
                 PresA (I) ≜ Always afterA → (Prev I → I) .

By Vthe interleaving semantics, at every time i > 0 exactly one afterA holds,
so A∈Tid PresA (I) entails Pres(I). This is the direct analogue of the classic
                            Past-Time Epistemic Reasoning for Concurrency        15

rely–guarantee proof obligation: “ show that each thread preserves I on its own
steps, under assumptions about how the environment may have affected the
shared state. ”

A proof recipe. In the examples, we repeatedly use the following pattern.

 1. Choose a global invariant I expressing the safety goal.
 2. For each thread A, prove a local step obligation PresA (I) using sequential
    reasoning about A’s code, assuming the rely constraints RA .
 3. Discharge the rely assumptions by proving compatibility: the guarantees of
    the other threads imply RA .
 4. Conclude Always I by Lemma 4.

The stability-lifting lemma (Lemma 2) is the workhorse for step (2) whenever
the local proof needs to carry facts across unboundedly many environment steps,
as in spin-wait loops.


6.8   Parallel composition as a derived rule

Classic presentations of rely–guarantee include an explicit parallel composition
rule. In our setting, interleaving composition is built into the semantics, so the
analogous step is a derived meta-theorem stated directly over the trace predicates
RA and GA .
                   V
    Write G−A ≜ B∈Tid\{A} GB for the environment guarantee seen by thread
A. For any invariant candidate I, the following derived rule packages the usual
rely–guarantee side conditions:

        ∀A ∈ Tid . (G−A |= RA )      ∀A ∈ Tid . (GA ∧ RA ) |= PresA (I)
                           V           
                                A∈Tid A |= Pres(I)
                                     G

The second premise is the model-relative local proof obligation: PresA (I) is evalu-
ated only at points where afterA holds, so it combines sequential reasoning about
A-steps (summarized by GA ) with the rely assumptions. In the two-thread case,
this specializes to the familiar compatibility obligations G0 |= R1 and G1 |= R0 ,
together with the local preservation checks (Gi ∧ Ri ) |= Presi (I). Combined with
Lemma 4, this yields the classic rely–guarantee structure: each thread is proved
correct under a rely, and the parallel system is correct once each rely is justified
by the other threads’ guarantees.


7     Case Study: Peterson’s Algorithm

We sketch how the temporal–epistemic and stability principles developed above
can be used to structure a compositional proof of Peterson’s mutual exclusion
algorithm.
16      Hamed Nemati and Mads Dam

7.1   Abstract control locations

We assume each thread i ∈ {0, 1} has control locations ℓflag , ℓvictim , ℓwaitF , ℓwaitV ,
ℓcs , ℓexit . The two waiting locations encode the standard desugaring of the com-
pound guard into read micro-steps (one shared-memory access per step): from
ℓwaitF a step reads flag[j] (where j = 1−i) and enters ℓcs if it reads 0; otherwise
it moves to ℓwaitV , reads victim, and enters ℓcs iff victim ̸= i (else loops back).
We use the state predicate at(i, ℓ) to test the current location of thread i, and
we define
                                   InCSi ≜ at(i, ℓcs ).


7.2   Event predicates for key instructions

To connect the logical proof to program steps, it is convenient to name a few
derived event predicates. Because control locations are part of the state, we can
recognize that a specific instruction has just executed by looking at the previous
location of the active thread. For thread i ∈ {0, 1}, define:

          SetFlagi ≜ afteri ∧ Prev at(i, ℓflag ),
        SetVictimi ≜ afteri ∧ Prev at(i, ℓvictim ),
         EnterCSi ≜ afteri ∧ at(i, ℓcs ) ∧ Prev at(i, ℓwaitF ) ∨ at(i, ℓwaitV ) ,
                                                                               

        ClearFlagi ≜ afteri ∧ Prev at(i, ℓexit ).

These are all transition formulas in the sense of §4: each refers to the immediately
preceding state via Prev. Intuitively, SetFlagi marks the post-state of executing
flag[i]=1, SetVictimi marks the post-state of executing victim=i, and EnterCSi
marks the post-state of taking the loop-exit transition into the critical section.
We use these predicates both as markers for last-occurrence reasoning (§4) and
as convenient names for thread guarantees. The operational semantics ensures
that each step updates a single thread’s location according to the control-flow
graph.


7.3   Ownership-style guarantees and derived stability

We encode the standard ownership assumptions of Peterson’s algorithm as step
properties.

(Gflag ) Only thread i writes flag[i]. For i ∈ {0, 1}, define
                                                             
         OwnFlagi ≜ Always ¬afteri → (flag[i] = Prev flag[i]) .

This implies that facts about flag[i] are stable under the environment of thread
i. In particular, we obtain Stablei (flag[i] = 1) and Stablei (flag[i] = 0) as
instances of Definition 1.
                            Past-Time Epistemic Reasoning for Concurrency         17

(Gvictim ) Threads write victim only to their own id. We express this at the level
of control locations:
                                                                         
       OwnVictimi ≜ Always afteri ∧ Prev at(i, ℓvictim ) → (victim = i) .

This says: if the most recent step was by i and that step executed the victim=i
command, then the resulting state satisfies victim = i.

7.4   Rely/guarantee summary
It is useful to make the rely/guarantee interfaces of Peterson explicit. For each
thread i (with j = 1 − i), we can view the following as a rely/guarantee pair
over shared variables.

Guarantee of thread i. Thread i never writes flag[j], and only writes victim
when executing victim=i:

           Gflag
                                                               
             i   ≜ Always afteri → (flag[j] = Prev flag[j]) ,
                                                                      
   Gvictim
     i     ≜ Always (afteri ∧ ¬SetVictimi ) → (victim = Prev victim) .

(The deterministic postcondition Always(SetVictimi → victim = i) comple-
ments the second formula.)

Rely of thread i. Dually, thread i relies on the environment (here, thread j) not
writing flag[i]:

            Rflag
                                                                    
             i    ≜ Always ¬afteri → (flag[i] = Prev flag[i]) ,

which coincides with the ownership-style assumption OwnFlagi in the two-thread
setting. For victim, i relies only on the weak fact that the environment changes
it only at SetVictimj , captured by the frame condition introduced above.

Compatibility. The classic rely/guarantee compatibility check “Gj |= Ri ” be-
                                                                         flag
comes a simple entailment between step predicates. For instance, Gj           entails
Rflag
  i   : if j never writes flag[i] on its own steps and i and j are the only threads,
then flag[i] is preserved on all non-i steps. This is exactly the kind of modular
interference argument that our stability operator StableA (·) is designed to en-
capsulate; a more detailed development would additionally record explicit frame
conditions for the remaining shared variables.

7.5   Local guarantees and what a thread can know
Two kinds of facts are used in the standard Peterson argument: (i) local facts
about what a thread just executed and what branch it took, and (ii) shared-state
facts that must be shown stable under interference. The temporal–epistemic view
makes this split explicit.
18     Hamed Nemati and Mads Dam

Deterministic postconditions of atomic steps. From the sequential semantics of
a single step we obtain the following guarantees:

                      Always(SetFlagi → flag[i] = 1),
                      Always(ClearFlagi → flag[i] = 0),
                      Always(SetVictimi → victim = i).

These are not epistemic statements; they are plain step facts about the oper-
ational semantics. In addition, we use the simple frame condition that victim
changes only at these assignments:
                                                                     
      Always ¬(SetVictim0 ∨ SetVictim1 ) → (victim = Prev victim) .

Why knowing a shared fact requires a rely. Even if thread i just executed
flag[i]=1, it does not automatically follow that i knows flag[i] = 1 at the re-
sulting state under our asynchronous perfect-recall semantics. Intuitively, if the
environment were allowed to change flag[i] without affecting i’s local state,
then i cannot rule out that additional environment steps have already occurred
since its assignment. Thus Ki (flag[i] = 1) becomes valid only once we com-
bine the local postcondition with an interference restriction such as OwnFlagi .
Under the closed-program convention of §6, OwnFlagi is part of the model, so
it already holds at every point quantified over by Ki ; the knowledge statement
then follows from the sequential postcondition of SetFlagi together with the fact
that no environment step can falsify flag[i]=1 in any admitted alternative run.

Knowing a past observation. In contrast, facts about what the thread observed at
its own step are robust: the past does not change. Under the desugaring above,
EnterCSi holds exactly at the post-state of the read micro-step that exits the
spin loop. Such a step can enter ℓcs only if it observed either flag[j] = 0 or
victim ̸= i in its pre-state, so the compound guard was false there. Because the
read result updates i’s local component (and thus its observation history), the
same sequential justification yields an epistemic guarantee about that pre-state
(using prei · from §4):
                                                                   
            Always EnterCSi → Ki prei ¬(flag[j]=1 ∧ victim=i) .

This is the form of knowledge we actually need: it records what i learned when it
evaluated the guard, rather than asserting knowledge of the current shared-state
values.


7.6   Key epistemic/stability reasoning steps

We highlight the two proof obligations where the temporal–epistemic view is
most useful.
                            Past-Time Epistemic Reasoning for Concurrency          19

Carrying forward a local fact. When thread i executes flag[i]=1, the post-
state satisfies flag[i] = 1 by the deterministic postcondition of the step.
Moreover, under the ownership constraint OwnFlagi the environment cannot
change flag[i] without i acting; since OwnFlagi is part of the model, this fact
is also something i can justify at that step and keep using between its own
steps (Lemma 3), yielding Ki (flag[i] = 1) at the post-state of SetFlagi . Using
Corollary 1 we can transport this fact to later times:
             OwnFlagi ∧ Previ Ki (flag[i] = 1) |= flag[i] = 1.
This is the simplest instance of the rely–guarantee pattern: the guarantee of the
environment (it does not write flag[i]) provides the stability needed to keep a
fact established at the last i-step valid while the environment executes.

The “last entrant” argument. We now make the textbook proof more explicit
in the temporal–epistemic language. Fix an arbitrary run π and suppose, for
contradiction, that at some time t both threads are in the critical section: (π, t) |=
InCS0 ∧ InCS1 . Let i ∈ {0, 1} be the thread that entered the critical section
last, and let j = 1 − i. Let e ≤ t be the entry point of i, characterized by
(π, e) |= EnterCSi and (π, e − 1) |= InCSj .

Step 1: j being in the critical section forces flag[j] = 1. By the control flow of
thread j, it executes flag[j]=1 before reaching ℓcs and executes flag[j]=0 only
after leaving the critical section. Under OwnFlagj , only thread j writes flag[j],
so flag[j] = 1 is stable between j’s own flag steps; together these facts yield
the global safety invariant
                         Always(InCSj → flag[j] = 1).
Applying this invariant at time e − 1, where (π, e − 1) |= InCSj , gives (π, e − 1) |=
flag[j] = 1, and hence at the entry step
                           (π, e) |= Prev(flag[j] = 1).                           (2)

Step 2: entering the critical section records what i learned from the loop guard.
By the epistemic guarantee for EnterCSi above, at time e thread i knows that in
the pre-state of its entry step the loop guard was false:
                   (π, e) |= Ki prei ¬(flag[j]=1 ∧ victim=i).
By factivity of knowledge (the T axiom, §5) the Ki modality may be discharged,
giving prei ¬(flag[j]=1 ∧ victim=i). Since EnterCSi implies afteri , by the iden-
tity noted in §4.4 the operator prei · coincides here with the ordinary previous-
state operator, giving
                                                              
                  (π, e) |= Prev ¬(flag[j]=1 ∧ victim=i) .                    (3)
Combining (2) and (3) yields
                            (π, e) |= Prev(victim ̸= i),
20     Hamed Nemati and Mads Dam

and since there are only two threads this simplifies to

                          (π, e) |= Prev(victim = j).                          (4)

Step 3: (4) forces j’s victim write to occur after i’s. Thread i executes victim=i
immediately before entering the loop, i.e., SetVictimi occurs strictly before
EnterCSi . By the deterministic postcondition of victim=i, the post-state of
SetVictimi satisfies victim = i, whereas (4) says that in the pre-state of the
entry step victim = j. Hence victim must be written to j at some point strictly
between SetVictimi and i’s entry. By the frame condition above, the only steps
that change victim are SetVictim0 and SetVictim1 ; and by the deterministic
postconditions SetVictim0 → victim = 0 and SetVictim1 → victim = 1, the
only one that can produce the value j is SetVictimj (the write SetVictimi
yields victim = i ̸= j). Therefore some occurrence of SetVictimj lies strictly
between SetVictimi and EnterCSi , which we summarize using the happens-before
abbreviation as
                             SetVictimi ≺ SetVictimj .

Step 4: the ordering contradicts that j was already in the critical section. Let
t∗ ≤ e be the time of the most recent victim=j write witnessed by Step 3, so
that SetVictimi occurs strictly before t∗ ; moreover t∗ < e, since SetVictimj is
a j-step while EnterCSi is an i-step. By the control flow of thread i, execut-
ing victim=i is preceded by flag[i]=1 and followed by the spin loop, with
flag[i]=0 executed only after leaving the critical section. Hence at t∗ thread
i has executed SetFlagi and not yet any ClearFlagi , and its most recent step at
or before t∗ lies in this window. Every i-step in that window is either SetFlagi
(deterministic postcondition flag[i] = 1) or a later prelude/spin step that
does not write flag[i]; combined with OwnFlagi (no environment step writes
flag[i]), a short induction shows every such post-state satisfies flag[i] = 1.
Thus Previ (flag[i] = 1) holds at t∗ , and with Stablei (flag[i] = 1) (derived
from OwnFlagi ) and Lemma 2 we obtain flag[i] = 1 at t∗ . Immediately after
SetVictimj we also have victim = j by its deterministic postcondition, so thread
j’s loop guard flag[i] = 1∧victim = j evaluates to true at t∗ . Neither flag[i]
nor victim changes between t∗ and e: by OwnFlagi only i writes flag[i], and
i remains in its spin loop through e; and since t∗ is the most recent victim=j
write no later than e, no later SetVictimj occurs before e, while no SetVictimi can
occur in (t∗ , e] (the spin loop contains no assignment to victim). Consequently
j’s guard remains true throughout (t∗ , e], so j cannot exit the spin loop in that
interval; in particular InCSj fails at time e − 1, contradicting our assumption
that j was already in the critical section then.

Summary. The formal structure mirrors the informal proof, but the logic forces
a clean separation: knowledge is used only to justify the pre-state guard fact
(3), whereas stability (rely/guarantee) transports flag-facts across unbounded
environment interference. Moreover, once mutual exclusion is established as a
global invariant, the advertised epistemic safety property follows as a corollary:
                            Past-Time Epistemic Reasoning for Concurrency          21

since InCSi is determined by i’s local control state, from Always¬(InCS0 ∧InCS1 )
we obtain Always(InCSi → Ki ¬InCSj ).


Discussion. The proof above is the familiar argument for Peterson’s algorithm,
but the temporal–epistemic presentation isolates two reusable reasoning pat-
terns: (i) carry forward a fact established at the last step using stability, and (ii)
separate what a thread can deduce at its own loop-exit point (an epistemic fact)
from what remains invariant under environmental steps (a stability fact). This
separation is precisely what rely–guarantee proofs enforce by design.
    A fully formal proof would add explicit predicates for “thread i just executed
line ℓ” and would discharge the local control-flow facts using an ordinary Hoare-
style reasoning for the sequential fragment of each thread. Our goal here is to
show that the interference reasoning can be expressed and organized cleanly in
the temporal–epistemic logic.


8    Related Work

Compositional concurrency reasoning. Owicki–Gries introduced non-interference
reasoning for proving assertions about parallel programs by checking that each
thread preserves the assertions of the others [26]. Jones’ rely–guarantee method
made environmental assumptions explicit and remains a foundational technique
for modular interference reasoning [18]. These ideas have been refined and mecha-
nized in modern frameworks, including concurrent separation logic [2,25,19] and
rely–guarantee/separation-logic hybrids [30,7,5,4,29,3]. Our contribution is or-
thogonal to these program logics: we use past-time epistemic assertions to make
thread-local inference explicit, and we package interference control as stability
obligations (§6), mirroring the classical “stable under rely” check.


Epistemic logic and verification. We adopt the interpreted-systems semantics
of knowledge with asynchronous perfect recall [6,11]. Epistemic perspectives on
concurrent computations and proof systems for parallel processes were explored
early on [15,17,16,20]. Temporal–epistemic logics have a substantial automated-
verification literature, with tool support in MCK and MCMAS [8,24]; see also
the surveys [23]. Knowledge-based specifications are also common in information-
flow security, including concurrent settings [1].


Knowledge-based correctness characterizations. Knowledge has been used to
characterize consistency conditions such as sequential consistency [21] and lin-
earizability [13]; see, e.g., [9,14]. Those works use knowledge to specify prop-
erties of executions as observed by clients or groups of observers, whereas we
use (single-thread) knowledge as a proof principle inside compositional safety
arguments.
22      Hamed Nemati and Mads Dam

9    Conclusion

We developed a past-time temporal epistemic logic for reasoning about shared-
variable concurrent programs under an interleaving semantics with perfect recall.
The central technical point is that epistemic statements about what a thread
knew at its last step can be lifted to current-state facts whenever those facts are
stable under environmental interference. This yields a clean rely–guarantee style
reasoning principle formulated directly in the logic and illustrated on Peterson’s
algorithm.

Current scope and limitations. Our semantic instantiation uses sequentially-
consistent interleaving with single-access micro-steps. This is a deliberate base-
line: it isolates the interaction between observation-based knowledge and inter-
ference control, but it does not yet address read–modify–write atomics (such as
compare-and-swap), fences, or weak-memory reorderings. Likewise, we interpret
formulas over infinite runs; terminating threads can be accommodated by stan-
dard stuttering conventions (e.g., self-loops at a final control location), but we
have not developed dedicated proof rules for termination or liveness.

Future work. Several directions suggest themselves. On the mechanization side,
extending the existing Isabelle/HOL development to cover the rely–guarantee
meta-theorem of §6.8 would provide a stronger foundation for case studies. On
the automation side, integrating the normal-form transformation of Appendix A
with SMT- or BDD-based backends is a natural next step. On the modelling
side, extending the setting to richer forms of concurrency, notably weak memory
models and fine-grained atomicity, seems a particularly promising direction, since
the epistemic perspective is designed precisely around what a thread can soundly
infer from partial observations.


Acknowledgments. We thank Robert Künnemann and Yufei Liu for their con-
tributions to the mechanization of the basic logic. This work has been supported
by the Wallenberg AI, Autonomous Systems and Software Program (WASP)
funded by the Knut and Alice Wallenberg Foundation.


References

 1. Balliu, M., Dam, M., Le Guernic, G.: Epistemic temporal logic for information flow
    security. In: PLAS 2011. ACM (2011)
 2. Brookes, S.D.: A semantics for concurrent separation logic. Theoretical Computer
    Science 375(1–3), 227–270 (2007)
 3. Dinsdale-Young, T., Birkedal, L., Gardner, P., Parkinson, M.J., Yang, H.: Views:
    Compositional reasoning for concurrent programs. In: Proceedings of the 40th An-
    nual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
    guages (POPL). pp. 287–300. ACM (2013)
                              Past-Time Epistemic Reasoning for Concurrency            23

 4. Dinsdale-Young, T., Dodds, M., Gardner, P., Parkinson, M.J., Vafeiadis, V.: Con-
    current abstract predicates. In: European Conference on Object-Oriented Program-
    ming (ECOOP). pp. 504–528. Lecture Notes in Computer Science, Springer (2010)
 5. Dodds, M., Feng, X., Parkinson, M.J., Vafeiadis, V.: Deny-guarantee reasoning.
    In: Programming Languages and Systems (ESOP). Lecture Notes in Computer
    Science, vol. 5502, pp. 363–377. Springer (2009)
 6. Fagin, R., Halpern, J.Y., Moses, Y., Vardi, M.Y.: Reasoning about Knowledge.
    MIT Press (1995)
 7. Feng, X.: Local rely-guarantee reasoning. Tech. Rep. TTIC-TR-2008-1, Toyota
    Technological Institute at Chicago (Oct 2008)
 8. Gammie, P., van der Meyden, R.: MCK: Model checking the logic of knowledge. In:
    CAV 2004. Lecture Notes in Computer Science, vol. 3114, pp. 479–483. Springer
    (2004)
 9. Gleissenthall, K.v., Rybalchenko, A.: An epistemic perspective on consistency of
    concurrent computations. In: CONCUR 2013. Lecture Notes in Computer Science,
    vol. 8052, pp. 212–226. Springer (2013)
10. Halpern, J.Y., Moses, Y.: A guide to the modal logics of knowledge and belief:
    Preliminary draft. In: Joshi, A.K. (ed.) Proceedings of the 9th International Joint
    Conference on Artificial Intelligence. Los Angeles, CA, USA, August 1985. pp. 480–
    490. Morgan Kaufmann (1985), http://ijcai.org/Proceedings/85-1/Papers/
    094.pdf
11. Halpern, J.Y., Moses, Y.: Knowledge and common knowledge in a distributed
    environment. Journal of the ACM 37(3), 549–587 (1990)
12. Herlihy, M., Shavit, N.: The Art of Multiprocessor Programming. Morgan Kauf-
    mann (2008)
13. Herlihy, M., Wing, J.M.: Linearizability: A correctness condition for concurrent
    objects. ACM Transactions on Programming Languages and Systems 12(4), 463–
    492 (1990)
14. Hirai, Y.: An intuitionistic epistemic logic for sequential consistency on shared
    memory. In: LPAR-16 2010. Lecture Notes in Computer Science, vol. 6355, pp.
    272–289. Springer (2010)
15. van der Hoek, W., van Hulst, M., Meyer, J.J.C.: Towards an epistemic approach to
    reasoning about concurrent programs. In: REX Workshop 1992: Semantics: Foun-
    dations and Applications. pp. 261–287 (1992)
16. van Hulst, M., Meyer, J.J.C.: A knowledge-based compositional proof system for
    parallel processes. Tech. Rep. UU-CS-1996-19, Utrecht University (1996)
17. van Hulst, M., Meyer, J.J.C.: An epistemic proof system for parallel processes. In:
    Proceedings of TARK 1994. pp. 243–254. Morgan Kaufmann (1994)
18. Jones, C.B.: Tentative steps toward a development method for interfering pro-
    grams. ACM Transactions on Programming Languages and Systems 5(4), 596–619
    (1983)
19. Jung, R., Swasey, D., Sieczkowski, F., Svendsen, K., Turon, A., Birkedal, L., Dreyer,
    D.: Iris: Monoids and invariants as an orthogonal basis for concurrent reasoning. In:
    Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Princi-
    ples of Programming Languages (POPL). pp. 637–650. ACM (2015)
20. Knight, S.: The Epistemic View of Concurrency Theory. Ph.D. thesis, École Poly-
    technique (2013)
21. Lamport, L.: How to make a multiprocessor computer that correctly executes mul-
    tiprocess programs. IEEE Transactions on Computers 28(9), 690–691 (1979)
22. Lichtenstein, O., Pnueli, A., Zuck, L.: The glory of the past. In: Logics of Programs.
    Lecture Notes in Computer Science, vol. 193, pp. 196–218. Springer (1985)
24      Hamed Nemati and Mads Dam

23. Lomuscio, A., Penczek, W.: Symbolic model checking for temporal-epistemic logic.
    In: Logic Programs, Norms and Action, Lecture Notes in Computer Science,
    vol. 7360, pp. 172–195. Springer (2012)
24. Lomuscio, A., Qu, H., Raimondi, F.: MCMAS: A model checker for the verifica-
    tion of multi-agent systems. In: CAV 2009. Lecture Notes in Computer Science,
    vol. 5643, pp. 682–688. Springer (2009)
25. O’Hearn, P.W.: Resources, concurrency and local reasoning. Theoretical Computer
    Science 375(1–3), 271–307 (2007)
26. Owicki, S.S., Gries, D.: An axiomatic proof technique for parallel programs I. Acta
    Informatica 6(4), 319–340 (1976)
27. Peterson, G.L.: Myths about the mutual exclusion problem. Information Processing
    Letters 12(3), 115–116 (1981)
28. Pnueli, A.: The temporal logic of programs. In: Proceedings of the 18th Annual
    Symposium on Foundations of Computer Science (FOCS). pp. 46–57. IEEE Com-
    puter Society (1977)
29. da Rocha Pinto, P., Dinsdale-Young, T., Gardner, P.: Tada: A logic for time
    and data abstraction. In: European Conference on Object-Oriented Programming
    (ECOOP). pp. 207–231. Lecture Notes in Computer Science, Springer (2014)
30. Vafeiadis, V., Parkinson, M.: A marriage of rely-guarantee and separation logic.
    In: CONCUR 2007. Lecture Notes in Computer Science, vol. 4703, pp. 256–271.
    Springer (2007)


A     Appendix: A Normal Form for Past-Time Formulas
      and a Remark on Stability
This appendix collects two auxiliary observations referred to in the main text.
First (§A.1–A.4), we sketch a normal-form transformation for the pure past-time
fragment (without knowledge); the goal is to support future automation efforts,
and it is not required for the soundness results in the main text. Second (§A.5),
we record a counterexample showing that stability is not monotone with respect
to logical consequence, as referenced in §6.

A.1    Eliminating derived operators
Because Alwaysϕ and Sometimeϕ are defined from Since, they can be elimi-
nated directly:

         Always ϕ ≡ ¬(⊤ Since ¬ϕ),             Sometime ϕ ≡ ⊤ Since ϕ.

A.2    Fixpoint unfolding for Since
The operator Since satisfies the standard unfolding equivalence

                   ϕ Since ψ ≡ ψ ∨ (ϕ ∧ Prev(ϕ Since ψ)).

This equivalence is sound under our semantics because at time 0 the Prev
subformula is false, so the base case reduces to ϕ Since ψ ≡ ψ at the initial
state, as expected.
                           Past-Time Epistemic Reasoning for Concurrency       25

A.3   Negation normal form

For the past-time fragment, a standard negation-normal-form (NNF) transfor-
mation pushes negations to atomic predicates by using

                 ¬Prevϕ ≡ (Prev⊤ ∧ Prev¬ϕ) ∨ ¬Prev⊤,

and by rewriting ¬(ϕ Since ψ) via the unfolding above and De Morgan’s laws. In
practice, one often avoids expanding ¬(ϕ Since ψ) eagerly, introducing instead
auxiliary predicates and using induction/recursion (e.g., in a model checker).


A.4   Comment on epistemic operators
A full normal form for the temporal–epistemic logic would need to account for
the semantics of KA (universal quantification over ∼A -classes), which is orthog-
onal to the temporal unfolding. One possible direction is to restrict to syntactic
fragments where epistemic operators occur only at “local time” points (e.g.,
immediately after a thread step) and to combine the temporal unfolding with
standard S5 reasoning. We leave this to future work.


A.5   Counterexample: stability is not closed under consequence
The closure properties in Lemma 1 hold for Boolean connectives, but stability is
not monotone w.r.t. logical consequence. Fix a thread A and a shared variable
x ranging over integers, and let ϕ ≜ (x = 0) and ψ ≜ (x = 0 ∨ x = 1), so that
|= (ϕ → ψ). Consider a run in which thread A never acts and the environment
performs a step that changes x from 1 to 2. At that environment step, Prev ψ
holds but ψ does not, so StableA (ψ) fails. On the other hand, StableA (ϕ) holds
vacuously on the same run if the antecedent Prev ϕ is never true on environment
steps (e.g., x is never 0 at those points). Hence StableA (ϕ) and |= (ϕ → ψ) do
not imply StableA (ψ).
