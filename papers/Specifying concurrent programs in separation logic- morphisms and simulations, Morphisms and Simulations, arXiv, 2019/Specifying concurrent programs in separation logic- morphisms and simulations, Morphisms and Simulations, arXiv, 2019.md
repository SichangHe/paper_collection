                                         Specifying Concurrent Programs in Separation Logic:
                                         Morphisms and Simulations

                                         ALEKSANDAR NANEVSKI, IMDEA Software Institute, Spain
arXiv:1904.07136v3 [cs.PL] 15 Oct 2019




                                         ANINDYA BANERJEE, IMDEA Software Institute, Spain
                                         GERMÁN ANDRÉS DELBIANCO, IRIF–Université de Paris, France
                                         IGNACIO FÁBREGAS, IMDEA Software Institute, Spain
                                         In addition to pre- and postconditions, program specifications in recent separation logics for concurrency have
                                         employed an algebraic structure of resources—a form of state transition systems—to describe the state-based
                                         program invariants that must be preserved, and to record the permissible atomic changes to program state. In
                                         this paper we introduce a novel notion of resource morphism, i.e. structure-preserving function on resources,
                                         and show how to effectively integrate it into separation logic, using an associated notion of morphism-specific
                                         simulation. We apply morphisms and simulations to programs verified under one resource, to compositionally
                                         adapt them to operate under another resource, thus facilitating proof reuse.
                                         Additional Key Words and Phrases: Program Logics for Concurrency, Hoare/Separation Logics, Coq

                                         This extended technical report is a companion to:
                                         Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas. 2019. Specifying
                                         Concurrent Programs in Separation Logic: Morphisms and Simulations. Proc. ACM Program. Lang. 3, OOPSLA,
                                         Article 161 (October 2019), 30 pages. https://doi.org/10.1145/3360587

                                         1   INTRODUCTION
                                         The main problem when formally reasoning about concurrent data structures is achieving compo-
                                         sitionality of proofs: how to ensure that methods of a data structure, once verified, can be used
                                         in a larger context without re-verification. There exist many solutions to the problem, roughly
                                         divided into two kinds: linearizability [Herlihy and Wing 1990], or more generally contextual refine-
                                         ment [Filipović et al. 2010a; Liang and Feng 2018; Liang et al. 2014], and Concurrent Separation Logic
                                         (CSL) [Brookes 2007; O’Hearn 2007], and its many recent extensions to fine-grained (i.e., lock-free)
                                         concurrency [da Rocha Pinto et al. 2014; Dinsdale-Young et al. 2010; Jung et al. 2015; Nanevski et al.
                                         2014; Svendsen and Birkedal 2014; Svendsen et al. 2013]. More recently, some approaches [Frumin
                                         et al. 2018; Turon et al. 2013] employed variants of separation logic to establish linearizability and
                                         contextual refinement themselves, suggesting separation logic as a general-purpose method for
                                         reasoning about concurrent programs.
                                            On the other hand, composition is also the cornerstone of type theory, where types serve as the
                                         interface that abstracts the internal properties of programs and proofs. Because both are focused on
                                         composition, type theory and separation logic are closely related. For example, from the inception
                                         of (sequential) separation logic, it has been understood [O’Hearn et al. 2001; Reynolds 2002] that its
                                         reasoning power arises from the key property of fault avoidance, which implies the features usually
                                         associated with separation logic, such as framing and small-footprint semantics. Fault avoidance
                                         states that a program verified against some pre- and postcondition, doesn’t crash (say, by reading
                                         from a deallocated pointer), if started in a state satisfying the precondition. This has inspired a
                                         stateful type theory [Nanevski 2016; Nanevski et al. 2006], where the type ascription
                                                                                             e : {P }{Q }
                                         Authors’ addresses: Aleksandar Nanevski, IMDEA Software Institute, Spain, aleks.nanevski@imdea.org; Anindya Banerjee,
                                         IMDEA Software Institute, Spain, anindya.banerjee@imdea.org; Germán Andrés Delbianco, IRIF–Université de Paris, France,
                                         gad@irif.fr; Ignacio Fábregas, IMDEA Software Institute, Spain, ignacio.fabregas@imdea.org.
2                             Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


                                                            lock_tr




                                       unlock_tr              Spin            id_tr

Fig. 1. Resource for spin locks. By convention, the idle transition id_tr will be elided in the future diagrams.

signifies that the program e has a precondition P and a postcondition Q (both predicates over
program states), in the sense of partial correctness. The Hoare type {P }{Q } is a form of dependently-
typed state monad, indexed by P and Q, which encapsulates the effects of state and divergence,
similarly to monads in Haskell. In the typed setting, fault avoidance is forced onto the formalism
by the requirement that “well-typed programs cannot go wrong” [Milner 1978]. Thus, Hoare types
give rise to not just a Hoare logic, but separation logic specifically. In other words, separation logic
is a type theory of state. Hoare types also enable a formulation and low-overhead implementa-
tion [Nanevski et al. 2008; Svendsen et al. 2011] of separation logic as an extension of, or a shallow
embedding into, a standard type theory (e.g. Coq).
   Using the above connection as a guiding principle, this paper derives a type-based formulation
of separation logic for fine-grained concurrency. Immediately motivated by the form of typeful spec-
ification for fine-grained programs, our contributions are two novel and foundational abstractions
for compositional verification—the morphisms and the simulations from the paper’s title—and a
way to incorporate them into Hoare-style reasoning by means of a single inference rule. The upshot
is conceptually simple foundations for separation logic for fine-grained concurrency.

1.1    Resources
As proposed by Dinsdale-Young et al. [2010], and utilized in different ways in many recent for-
malisms [da Rocha Pinto et al. 2014; Jung et al. 2015; Nanevski et al. 2014; Svendsen and Birkedal
2014; Svendsen et al. 2013], the key technical requirement that fine-grained concurrency imposes
on a Hoare-style logic is enriching the Hoare specifications with state transition systems (STS) of a
specific form—termed resources [Hoare 1972; O’Hearn 2007; Owicki and Gries 1976] in this paper.
For example, in our type-based setting, we extend the Hoare type with a resource V , as in
                                                   e : {P }{Q } @ V
to signify that e has a precondition P and a postcondition Q, but also that the atomic state changes
that e may carry out are circumscribed by the transitions of V . We also say that e is typed by V ,
that e inhabits V , or that e is in V .
   Two programs can be composed in parallel (or sequentially), only if they are typed by the same
resource. Thus, the resource in the type annotation bounds the interference that concurrent threads
can perform on each other’s execution, which is essential for reasoning about the composition.1
   To quickly illustrate resources in our particular setting, consider a spin lock r (a shared Boolean
pointer) and a program that locks r by setting it to true, and loops if r is already set2 :
                                      = do x ← CAS(r , false, true) while ¬x
                                 lock b
1 The idea of bounding the interference is the foundation behind the classic rely-guarantee method [Jones 1983] as well. In

fact, resources may be seen as structuring and compactly representing—in the form of transitions—the rely and guarantee
relations of the rely-guarantee method.
2 The Compare-and-Set variant of CAS(r, a, b) [Herlihy and Shavit 2008] atomically sets the pointer r to b if r contains a,

otherwise leaves r unchanged. It moreover returns a Boolean value denoting the success or failure of the operation.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                                3


   Figure 1 shows (an abstracted form of) the resource Spin, suitable to type lock.3 Every execution
of lock describes a path through Spin consisting of several idle transitions id_tr, corresponding to
unsuccessful CAS’s, followed by a locking transition lock_tr corresponding to a successful CAS.
Similarly, the Spin resource also types the unlock program
                                                         = r := false
                                                  unlock b
which may be seen as taking the unlock_tr transition if r stores true, or staying idle if r stores false
to begin with. Because lock and unlock are typed by the same resource, they can be composed,
sequentially or in parallel. The typing guarantees that the concurrent environment of lock and
unlock is bound to only ever execute the transitions of Spin, and can’t cause “surprises”, such as
deallocating the pointer r while lock or unlock are executing.

1.2    Morphisms
This brings us to the first technical contribution of the paper. As soon as resources are introduced
into types, it becomes necessary to coerce a program from one type (i.e., resource) to another.
   As one example of coercion, consider two procedures, inhabiting different resources, each
specifying its own concurrent data structure (say, a stack and a queue). If we want to use the stack
and the queue together in a program, we must coerce the procedures into a common resource that
includes the functionality of both structures, and describes how the two interact.
   As another example, consider refining the behavior of already implemented resources. Suppose
we want to use the bare-bones spin locks described by Spin to develop more sophisticated locking
protocols: CSL-style mutually exclusive locks [O’Hearn 2007], or non-mutually-exclusive locks
such as readers-writers locks [Bornat et al. 2005; Courtois et al. 1971] where a reader acquires a lock
to allow access to multiple readers, but not writers. Both developments can be seen as extending
Spin with additional ghost state to represent the invariants of the refined locking protocol, and
then coercing the lock and unlock procedures to modify this additional ghost state at the precise
moment when lock transitions by lock_tr, and unlock transitions by unlock_tr. The developments
thus compositionally reuse the definitions and proofs of lock and unlock, each in its own way. We
carry out the first development in Section 4, and the second in the Coq code [Nanevski et al. 2019].
   To achieve coercion we introduce morphisms between resources. A resource morphism f : V → W
is a structure-preserving mapping from resource V to resource W , which acts on a program e typed
by V , to derive a program typed by W , essentially by re-interpreting the V -transitions that e takes,
as W -transitions.
   Morphisms arise naturally, because a structure in mathematics typically is associated with an
appropriate notion of a structure-preserving function. Examples abound: vector spaces and linear
maps, groups and their homomorphisms, complete partial orders and continuous functions, functors
and natural transformations, etc. Morphisms endow the structure with dynamics and allow studying
it under change. This will be the case for us as well.
   More specifically, and akin to how automata homomorphisms [Ginzburg 1968] are defined
componentwise, a resource morphism f : V → W consists of two partial functions f Σ and f ∆ ,
acting respectively on states (Σ) and transitions (∆). f Σ takes a state in W and produces a state, if
defined, in V (note the contravariance); and f ∆ takes a state in W and transition in V and produces
a transition, if defined, in W . Combined, f Σ and f ∆ act on a program e inhabiting V to produce a
program inhabiting W , using the following process.

3 We’ll define the state space and the transitions of Spin in Section 2, and eventually tie them to the implementations of

lock and unlock. At this point, it suffices to know that a program in Spin may transition by lock_tr only if r is free (thereby
locking it), and by unlock_tr only if r is locked (thereby freeing it).
4                          Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


                                                     fΣ
                                            sv′            I sw′
                                           tv                    tw =f ∆ sw tv

                                            sv             I sw
                                                     fΣ
Fig. 2. Reinterpreting the transitions of a resource V into those of W , by a morphism f : V → W and an
f -simulation I . In this diagram, and in the sequel, I s denotes “state s such that the predicate I holds”.

   Referring to Figure 2, the morphed program inhabits W , so we describe it starting with a W -state
sw in the lower-right corner of the diagram (the predicate I that is applied to sw in the diagram
will be explained promptly). To compute the next state of the morphed program, we first take
sv = f Σ sw which is a state in V (utilizing contravariance of f Σ ). If e takes a transition tv to step
from sv to sv′ in V , the corresponding transition of the morphed program is tw = f ∆ sw tv . If tw
steps from sw to sw′ , the process is repeated for sw′ and the next transition of e.
   The morphing process determines a program in W that we denote morph f e. Here, morph is a
program constructor, and a form of function application of f to e. In the sequel, we introduce the
infrastructure to program (and prove!) with morphisms and morphed programs.

1.3   Simulations and Inference
To reason about morph f e, we introduce our second contribution: morphism-specific simulations.
An f -simulation (or simply, a simulation, when f is clear from the context) is a predicate I over
W -states that acts like a loop invariant for the iterative process of morphing by f . Specifically, an
f -simulation satisfies, among other conditions presented in Section 3, the key technical property
that the diagram in Figure 2 commutes. Given sw , sv , tv and sv′ that partially describe the diagram,
if I sw , then there exists a state sw′ that completes the diagram: tw = f ∆ sw tv exists, tw sw sw′ , I sw′ ,
and f Σ sw′ = sv′ . Because I sw′ holds, simulation I is preserved by f .
    Simulations provide a way to reason about morph f e compositionally, i.e., out of e’s type,
achieving our ultimate goal of program and proof re-usability. The specifics are prescribed by the
following single inference rule, which is our third contribution:
                                                e : {P }{Q }@V
                                                                                        Morph
                      morph f e : {λsw . f ˆP sw ∧ I sw }{λsw . f ˆQ sw ∧ I sw }@W

                               where f ˆR sw b
                                             = ∃ sv . sv = f Σ s w ∧ R sv
   The Morph rule translates the requirements for a morphism f : V → W , and a simulation I ,
expressed diagrammatically in Figure 2, from properties of states and transitions of the resources V
and W , into the specification of a program morph f e in W . The latter spec is structured, both in
its pre- and the postconditions, as a conjunction of (i) the transformation of e’s spec from V to W ,
and (ii) a statement that the simulation I , being in fact an invariant of the resources’ transitions,
holds at the boundaries of the morphed execution of e. For the first part, we use the predicate f ˆ_,
to lift the pre- and postconditions of e from states in V to states of W , which are related via f Σ .
This motivates the contravariance of f Σ : we have verified e in the context of the resource V , but we
intend to morph e and execute it in a new resource context, where states are inhabitants of W .
   More concretely, the precondition of morph f e in Morph assumes I sw and the existence of
sv = f Σ sw such that P sv . By fault avoidance (i.e., type safety), a program (here e in the premise)
that is ascribed a Hoare type isn’t stuck. Hence, there exists a transition tv by which e steps from
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                                 5


sv into sv′ . Because I is an f -simulation, the commuting diagram implies the existence of sw′ such
that sv′ = f Σ sw′ and I sw′ . The morphing process is then iterated for sw′ and the subsequent states.
This iteration relies on f preserving I , much like a loop relies on the loop body preserving the loop
invariant. Once e terminates in a final state sv′′, the postcondition in Morph must hold. First, Q sv′′
must hold as Q is e’s postcondition. Second, I being an f -simulation yields the commuting diagram
which implies the existence of sw′′ such that sv′′ = f Σ sw′′ (hence f ˆQ sw′′ ) and I sw′′ .
   The paper can thus be seen as introducing simulations into separation logic in a simple4 , but
also constructive manner. Customarily, an STS W simulates another STS V if whenever V takes a
transition, there exists a transition for W to take [Lynch and Vaandrager 1995]. For us, a morphism
f computes the witness of this existential (via f ∆ ), in the style of constructive logic and type theory.
Moreover, a simulation is usually defined as a relation between the states of V and W . For us, an
f -simulation is a predicate on W -states alone, as f Σ deterministically computes the unique V -state
that corresponds to a W -state in the simulation. Finally, simulations are also customarily required
to relate a distinguished set of initial states of the source and target STSs. Our resources and
f -simulations, on the contrary, don’t need to consider specific initial states of V and W , because
the initial states of any program are described by its precondition, and the Morph rule checks that
the simulation holds on the pre-state of every invocation of morph.
   The paper can also be seen as introducing a form of refinement mappings [Abadi and Lamport
1991] into separation logic, since refinement mappings, like morphisms, are functions between
STSs. The two, however, have very different technical details, largely imposed by our connection to
separation logic. This includes the introduction of the morphism action on programs and the Morph
rule, but also the treatment of state ownership, ownership transfer, and framing (cf. Section 3),
none of which have been considered with refinement mappings.
   Moreover, resource morphisms go beyond mere program specification and proof, as they also
support generic constructions over resources, such as “tensoring” two resources, adjoining an
invariant to a resource, or forgetting a ghost field from a resource (the last one with a mild
generalization to indexed morphism families). Morphisms relate a construction to its components,
much as arrows in category theory relate objects of universal constructions, and are thus essential
for the constructions to compose. This is why we see resource morphisms as a step towards a
general type-theoretic calculus of concurrent constructions.
   We formalize the development in Coq, using Coq’s predicates over states as assertions5 , building
on the code base of Fine-grained Concurrent Separation Logic (FCSL) [Nanevski et al. 2014]. The
sources are available online as an Artifact [Nanevski et al. 2019].6

   Readmap. The rest of the paper is organized as follows. Section 2 introduces resources and
associated notions of ghost state and transitions, via the spin lock example. Section 3 develops the
theory formally, including our specific notion of framing. Section 4 illustrates how to morph spin
locks into exclusive locks. Section 5 introduces indexed morphism families and applies them to
“forgetting” the ghost state of a resource. This models what is often referred to as quiescence [Aspnes
et al. 1994; Derrick et al. 2011; Jagadeesan and Riely 2014; Nanevski et al. 2014; Sergey et al. 2016],
most commonly used when installing one concurrent structure into the private state of another.
Section 6 discusses related work and Section 7 concludes.

4 Our formalization exports nine rules for Hoare-style reasoning, each addressing an orthogonal linguistic feature.
5 As apparent from the Morph rule, we explicitly bind the state s
                                                                       w , in contrast to the classic presentation of separation
logics where this state is implicit. This is merely a syntactic distinction.
6 In addition to the examples from the paper, the sources include further benchmarks such as Treiber stack [Treiber 1986],

flat combiner [Hendler et al. 2010], a concurrent allocator, a concurrent graph spanning tree algorithm [Sergey et al. 2015a],
ticketed [Mellor-Crummey and Scott 1991] and readers-writers [Courtois et al. 1971] locks.
6                               Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


                                             lock_tr                     incr_tr n
                                                               ▷◁

                        unlock_tr               Spin                      Counter


    State space Σ (Spin): s ∈ Σ (Spin) iff                           State space Σ (Counter): s ∈ Σ (Counter) iff
       s contains fields τs s, τo s ∈ Hist, and                         s contains fields κ s s, κo s ∈ N
       τs s ⊥ τo s ∧ alternate (τ̂ s) ∧ r , null                        with no additional constraints
    Erasure: ⌜s ⌝ b   = r Z⇒ ω (τ̂ s)                                Erasure: ⌜s ⌝ b   = empty heap
    Transitions ∆(Spin):                                             Transitions ∆ (Counter):
    lock_tr s s ′ b
                  = ¬ω (τ̂ s) ∧ τs s ′ = τs s • fresh (τ̂ s) Z⇒ L    incr_tr n s s ′ b
                                                                                     = κs s ′ = κs s + n
    unlock_tr s s ′ b
                    = ω (τ̂ s) ∧ τs s ′ = τs s • fresh (τ̂ s) Z⇒ U

           Abbreviations: (in the abbreviations below, h is a bound
                                                               (    variable ranging over histories)
                                                                    h (last_stamp h), if last_stamp h , 0
                     dom h b= {t | h (t ) defined} last_op h b
                                                             =
                                                                    U,                otherwise
             last_stamp h b = max ({0} ∪ dom h)
                                                         ωh b= (last_op h = L)
                    fresh h b
                            = 1 + last_stamp h
               alternate h b= (h = 1 Z⇒ L • 2 Z⇒ U • 3 Z⇒ L • · · · • last_stamp h Z⇒ last_op h)

                                Fig. 3. Spin and Counter resources (with id_tr elided).




2     BACKGROUND AND OVERVIEW
We illustrate our specification idiom, resources, and resource morphisms, by fleshing out the
example of spin locks.

2.1     Histories
To specify the locking and unlocking methods over spin lock, we build on the idea of linearizabil-
ity [Herlihy and Wing 1990], and record the operations on r in the linear sequence in which they
occurred. We do so in Hoare triples, but in a thread-local way, i.e. from the point of view of the
specified thread, which we refer to as “us” [Ley-Wild and Nanevski 2013].
   Specifically, a program state s contains a ghost component that we project as τs s, and which
keeps “our” history of lock operations. Dually, the projection τo s keeps the collective history of
all “other” (i.e. environment) threads. Each thread has these two components in scope, but they
may have different values in different threads. We refer to τs and τo as self and other histories,
respectively [Nanevski et al. 2014; Sergey et al. 2015b].
   A history is a timestamped log of the locking and unlocking operations. Mathematically, it’s a
finite map from timestamps (strictly positive nats) to the set {L, U}. For example, the self history τs s
defined as 2 Z⇒ U • 7 Z⇒ L • 9 Z⇒ L, signifies that “we” have unlocked at time 2, and locked at times
7 and 9. The timestamp gaps indicate the activity of the interfering threads, e.g., another thread
must have locked at time 1, otherwise we couldn’t have unlocked at time 2. Similarly, another
thread must have unlocked at time 8. The entries such as 2 Z⇒ U are singleton maps, and • is disjoint
union, undefined if operand histories share a timestamp. We abbreviate by τ̂ s the history τs s • τo s,
which is the combined history of all threads, and use Hist for the collection of all histories.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                          7


2.2    Resources
We next define the resource Spin from Section 1, that types spin lock methods. It is pictorially
shown in Figure 3 on the left.
   The state space of Spin, denoted Σ (Spin), makes explicit the assumptions about the components:
that the histories are disjoint (denoted τs s ⊥ τo s), that the entries in τ̂ s alternate between L and U,
and that r isn’t the null pointer.
   The erasure ⌜s⌝ shows how the state s maps to a heap once the ghost histories are removed. The
expression r Z⇒ ω (τ̂ s) denotes a heap with only the pointer r , storing the Boolean value ω (τ̂ s).
The latter computes the lock status out of the combined history τ̂ s; it equals true if the last log in
the combined history is a lock entry L, and false otherwise.
   The set of transitions of Spin, denoted ∆ (Spin), contains lock_tr, unlock_tr, and the (elided) idle
transition. The transition lock_tr adds a fresh L entry to τs s if ¬ω (τ̂ s), i.e., if the lock is free in the
pre-state. Similarly, unlock_tr adds a fresh U entry if ω (τ̂ s), i.e., the lock is taken. The lock can by
taken by “us” or by “others”, as ω is computed from the combined history τ̂ s. If the locking protocol
insists that the thread that unlocks is the same thread that last locked, then the precondition of
unlock_tr should be changed to ω (τs s). We don’t want to impose such behavior at this stage, but
show how to achieve it a posteriori, together with additional functionality, in Section 4.

2.3    Method Specifications
We now give the following pidgin code for lock and unlock, intended to further the intuition about
transitions. The actual implementation of the methods will be shown in Section 3, once we have
formally introduced our system.
              = do ⟨x ← CAS(r , false, true); if x then τs s := τs s • fresh (τ̂ s) Z⇒ L ⟩; while ¬x
         lock b
             = ⟨ x ← !r ; r := false; if x then τs s := τs s • fresh (τ̂ s) Z⇒ U ⟩
      unlock b
The brackets ⟨−⟩ denote atomic execution (i.e., uninterrupted by other threads) of real and ghost
code, the latter given in gray. Note how the bracketed code in lock implicitly describes a choice,
depending on the contents of r , between executing lock_tr or the idle transition in the resource.
The former, when considered on erased states, corresponds to CAS successfully setting r , the latter
to CAS failing. Similarly, unlock chooses between unlock_tr and the idle transition. Thus, we shall
abstractly view the atomic executions as a choice between transitions of the corresponding resource,
rather than as bracketing of ghost with real code.
   We can now explain the history-based specs for lock and unlock.
         lock : [h, k]. {λs. τs s = h ∧ k ≤ last_stamp (τ̂ s)}
                        {λs. ∃t . τs s = h • t Z⇒ L ∧ k < t }@Spin
       unlock : [h, k]. {λs. τs s = h ∧ k ≤ last_stamp (τ̂ s)}
                        {λs. ∃t . τs s = h • t Z⇒ U ∧ k < t ∨ τs s = h ∧ τ̂ s t = U ∧ k ≤ t }@Spin
   The precondition of lock starts with self history τs s equal to h 7 , which is increased in the
postcondition to log a locking event at time t. The conjunct k < t in the postcondition claims that
t is fresh, because it’s larger than any k generated prior to the call (as k ≤ last_stamp (τ̂ s) is a
conjunct in the precondition, and k is universally quantified outside of the pre- and postcondition).
The natural numbers ordering on timestamps gives the linear sequence in which the events logged
in τ̂ s occurred. Notice that the spec is stable, i.e., invariant under interference. Intuitively, other
threads can’t modify the τs s field, as it’s private to “us”. They can log new events into τo s, which
7 As customary in Hoare logic, h and k are logical variables, used to relate the pre and post-state. They are universally

quantified, scoping over pre and post-condition, and the syntax [· · · ] makes the binding explicit.
8                              Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


features in the comparison k ≤ last_stamp (τ̂ s), but this only increases the right-hand side of the
comparison and doesn’t invalidate it.
   Similarly, unlock starts with history h, which is either increased to log a fresh unlocking event
at time t, or remains unchanged if the unlocking fails because unlock encounters r already freed at
time t (conjunct τ̂ s t = U). The conjunct k ≤ t captures that another thread may have freed r after
the invocation of unlock (k < t), or that we invoked unlock with r already freed (k = t).
   Observe that the spec for unlock doesn’t require that the unlocking thread is the one that last
locked, or even that the lock is taken when unlocking is attempted. This is so because we intend
the specs to capture only the basic mechanics of spin locks, and leave it to the clients to supply
application-specific policies, via morphing, as we illustrate on exclusive locks in Section 4 (and on
readers-writers locks in [Nanevski et al. 2019]).

2.4    Morphisms
Consider next how to express a client of lock that, simultaneously with a successful lock, adds
n to the ghost component κs s of resource Counter (right half of Figure 3). Intuitively, we desire
something like ⟨lock; κs s := κs s + n ⟩ but this isn’t quite right. Indeed, bracketing would prevent
other programs from running during the iterations of lock’s loop, thus changing the granularity
of the program. We want to model that addition occurs only upon the successful CAS of the last
iteration in lock. To do so, we use morphisms as follows.
   First, we “tensor” the resources Spin and Counter, as graphically indicated8 in Figure 3; that is,
we create a new resource SC whose state is a pair of Spin and Counter states, and transitions are
lock_tr ▷◁ incr_tr n and unlock_tr ▷◁ id_tr. Operator ▷◁ (pronounced “couple”) indicates that the
operand transitions are executed simultaneously on their respective state halves. It’s defined as
follows, where s\1 and s\2 project state s to its Spin and Counter components, respectively:
                                 (t 1 ▷◁ t 2 ) s s ′ b
                                                     = t 1 (s\1) (s ′\1) ∧ t 2 (s\2) (s ′\2)
Second, for each n ∈ N, we define the morphism fn : Spin → SC as follows:
                                     (fn )Σ s                = s\1
                                                             b
                                     (fn )∆ s lock_tr   = lock_tr ▷◁ incr_tr n
                                                        b
                                     (fn )∆ s unlock_tr b
                                                        = unlock_tr ▷◁ id_tr
This definition captures: (1) starting from an SC state s, we can obtain a Spin state by taking the
first projection; (2) a Spin program can be lifted to SC by changing the transition lock_tr by (fn )∆
on the fly, to increment κs s simultaneously with the lock acquisition; and (3) unlock_tr is coupled
with the idle transition in Counter, thus κs s is unchanged by unlocking.
   Now, our desired program is
                                           morph fn lock
which is typed by SC, and executes lock_tr ▷◁ incr_tr n whenever lock executes lock_tr, thus
incrementing κs s precisely, and only, upon a successful CAS.

2.5    Inference
The Morph rule provides a way to reason about morphed programs. To illustrate the proofs, we
consider the following simple program
                                                  morph f 1 lock;
                                                  morph f 42 unlock;
                                                  morph f 2 lock
8 We elide the definition of tensoring, as it isn’t required to follow the presentation. It can be found in Appendix A.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                       9


                       1. {κs s = n}
                       2. {κs s = n ∧ τs s = h}
                       3. morph f 1 lock; // I 1 s b= κs s = n + ♯L (τs s) − ♯L h
                       4. {κ s s = n + ♯L (τs s) − ♯L h ∧ τs s = h • t Z⇒ L}
                       5. {κ s s = n + 1 ∧ τs s = h ′ }
                       6. morph f 42 unlock; // I 42 s b = κs s = n + 1
                       7. {κ s s = n + 1 ∧ (τs s = h ′ ∨ τs s = h ′ • t ′ Z⇒ U)}
                       8. {κ s s = n + 1 ∧ τs s = h ′′ }
                       9. morph f 2 lock // I 2 s b= κs s = n + 1 + 2(♯L (τs s) − ♯L h ′′)
                      10. {κ s s = n + 1 + 2(♯L (τs s) − ♯L h ′′ ) ∧ τs s = h ′′ • t ′′ Z⇒ L}
                      11. {κ s s = n + 3}

Fig. 4. Using the Morph rule to show that κs s increments by 3. ♯L (−) is the number of L-entries in a history.


                                     (f 1 )Σ
                             s ′\1             I1 s ′             κs s ′ = n + ♯L (τs s ′) − ♯L h
                                                       lock_tr
                                                                    τs s ′ = τs s • fresh (τ̂ s) Z⇒ L
                                                         ▷◁
                        lock_tr                                             κs s ′ = κs s + 1
                                                      incr_tr 1

                             s\1               I1 s               κs s = n + ♯L (τs s) − ♯L h
                                     (f 1 )Σ

Fig. 5. Diagram showing that I 1 s b
                                   = κs s = n + ♯L (τs s) − ♯L h is an f 1 -simulation (case of lock_tr transition).
The diagram specializes Figure 2 to f 1 , I 1 and lock_tr.


which, in addition to locking and unlocking, increments κs s by 1 in the first line, and by 2 in the third
line.9 The second line morphs unlock vacuously, as unlocking leaves κs s unchanged. Nevertheless,
some morphing of unlock is necessary, to bring the commands under the same resource type.
     The proof outline in Figure 4 shows that κs s increments by 3, and we discuss its main points
next. In the outline, ♯L is a function on history that computes the number of L entries in the history.
The outline starts with the precondition κs s = n, where n snapshots “our” current count. Line 2
uses h to snapshot “our” history. Line 3 applies morph to lock, and correspondingly, the Morph
rule in the proof. At this point, we choose the simulation I 1 as indicated in line 3, to state that
the counter κs increments n by the number of fresh L-entries in the history. Intuitively, I 1 is an
f 1 -simulation because it is preserved under incrementing κs s by 1 while simultaneously adding an
L-entry to τs s (Figure 5). It’s easy to see that I 1 holds in line 2, thus by Morph, it holds in line 4 as
well. But, in line 4, by postcondition of lock, the history τs s has one more locking entry. Thus, κs s
is increased by 1 (line 5). The remainder of the outline proceeds similarly.
     We close the discussion with the observation that the property of being a simulation (i.e., making
diagrams in Figures 2 and 5 commute) relies only on the resource in the program’s type, and the
morphism in question, not on the program’s code, as required for compositional reasoning. In this
respect, the simulations are different from loop invariants, which are properties of programs. The
Morph rule ties the simulations to the morphed program by conjoining them with the program’s
pre- and the postcondition. Specifically above, I 1 enables computing the end-value of κs from the
end-value of τs , and τs is given by the spec of lock.
9 Strictly speaking, we should write κ (s\2) (resp. τ (s\1)) to extract the self component of the Counter (resp. Spin)
                                      s                s
”sub-resource” of SC. However, the components have different names, so there’s no confusion which projection of s they
come from. We thus abbreviate κ s (s\2) with κ s s, τs (s\1) with τs s, and similarly for κo and τo .
10                                 Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas



      s1 :                       ao = a 2 • a 3   s2 :                       ao = a 3 • a 1   s = s1 ∗ s2 :                   ao = a 3
                            a3                                          a3                                               a3
                a1     aj                                    a1    aj                                          a1   aj

     as = a 1          a2                         as = a 2         a2                         as = a 1 • a 2        a2

                 (1) left thread θ 1                         (2) right thread θ 2               (3) parent thread θ = θ 1 ∥ θ 2
Fig. 6. Values of self component as (light shade) and other component ao (dark shade) in the states of parallel
threads and their parent. The inner white circle represents the joint component, and is equal for all threads.


3     DEFINITIONS OF THE FORMAL STRUCTURES
To develop the notions of morphisms and simulations, we first require a number of auxiliary
definitions, such as states, transitions, and resources on which morphisms act. This section defines
all the concepts formally, culminating with the inference rules of our system.

3.1          States
3.1.1 Subjective Components. Different resources may contain different state components, e.g., τ
of Spin and κ of Counter. In general, a state is parametrized by two types: M classifies the self and
other components, and T classifies the joint (aka., shared) state. Thus, s = (as , a j , ao ) is a state if
as , ao ∈ M, and a j ∈T . If we want to be explicit about the types, we say that s is an (M,T )-state.
We use as s, a j s and ao s as generic projections out of s, but rename them in specific cases, for
readability. For example, in the case of Spin: M is Hist, T is unit type, and τs /τo renames as /ao . In
the case of Counter: M is N, T is unit type, and κs /κo renames as /ao .
   Because as and ao represent thread-specific views of the state, we refer to them as subjective
components, and to s as subjective state [Ley-Wild and Nanevski 2013].
3.1.2 Algebra of Subjectivity. The specs must often combine the subjective components, cf. how
histories were unioned by • to express timestamp freshness in the spec of lock. To make the
combination uniform, M is endowed with the structure of a partial commutative monoid (PCM).
A PCM is triple (M, •, 1) where • (join) is a partial, commutative, associative, binary operation on
M, with 1 as the unit. As a generic notation, we write x ⊥ y to denote that x • y is defined.
   Example PCMs are Hist with disjoint union and the empty history ∅, and N with + and 0. Another
common PCM is the set of heaps (denoted Heap). Heaps map pointers to values, and are thus similar
to histories, which map timestamps to operations. We can therefore reuse the history notation, and
write, e.g.:
                                         x Z⇒ 3 • y Z⇒ false
to describe the heap containing pointers x and y, storing 3 and false, respectively.10 Heap is a PCM
with disjoint union and the empty heap ∅, similar to Hist. Cartesian product of PCMs is a PCM,
so PCMs can be combined, cf. the PCM of SC is constructed out of those of Spin and Counter in
Section 2.
3.1.3 Subjectivity and Parallel Composition. The subjective components are local, in the sense that
they have different values in different threads. However, despite the locality, the components of
different threads aren’t independent, but are inter-related as shown in Figure 6.
   Imagine three threads θ 1 , θ 2 and θ 3 running concurrently. Their respective states must have the
forms s 1 = (a 1 , a j , a 2 • a 3 ), s 2 = (a 2 , a j , a 3 • a 1 ) and s 3 = (a 3 , a j , a 1 • a 2 ). Indeed, any two of the
10 We silently already used this notation to define the erasure function for Spin in Figure 3.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                       11


threads combined are the environment for the third thread. Thus, the PCM join of the self ’s of any
two threads must equal the other of the third thread. Figures 6(1) and 6(2) illustrate this property
for threads θ 1 and θ 2 , with θ 3 being their implicit environment.
   If θ is the parent thread of θ 1 and θ 2 , then its state is s = (a 1 •a 2 , a j , a 3 ), since θ is the combination
of θ 1 and θ 2 , and has θ 3 as the environment. We abbreviate as s = s 1 ∗ s 2 the relationship between
the parent state s, and the children states s 1 and s 2 , and illustrate it in Figure 6(3).
3.1.4 Globality. A property or a function is global if it remains invariant under moving PCM values
between subjective components. In light of Figure 6, such properties and functions obtain equal
valuations across all concurrent threads, thus justifying the name. We introduce several operations
for surgery on subjective states, and then use them to define globality and conditional globality,
where the invariance holds only under a (global) condition.
   Definition 3.1. Let p ∈ M and s = (as , a j , ao ) be an (M,T )-state. The self-framing of s with the
frame p is the state s  p = (as • p, a j , ao ). Dually, the other-framing of s with p is the state
s  p = (as , a j , p • ao ).
   Definition 3.2. A predicate P is global, if P (s  p) ↔ P (s  p) for every p and state s such that
as s ⊥ p ⊥ ao s. A (partial) function f on states is global, if f (s  p) = f (s  p) under the same
conditions.
   Examples of global predicates from Section 2 are P s = τs s ⊥ τo s, and Q s = alternate (τ̂ s) used
in Figure 3 to characterize Spin histories. P and Q are both defined in terms of τ̂ s = τs s • τo s;
Q directly so, and P because τs s ⊥ τo s iff τs s • τo s is itself defined. In other words, both P and
Q express a property of the collective history of all threads operating over Spin, taken together.
Clearly, the value of this history is invariant across all the threads, and therefore, so are P and Q.
Specifically, they are invariant under shuffling timestamps between τs and τo , as this doesn’t alter
the total. In fact, τ̂ itself is a global function, so we proceed to refer to τ̂ as the global history.
   Definition 3.3. Let X be a global predicate. A predicate P is global under X , if P (s p) ↔ P (s p)
for every p and state s such that as s ⊥ p ⊥ ao s and X (s  p). Similarly for functions.
3.1.5 Subjectivity and Framing. Subjective state makes framing work somewhat differently than
in the customary, non-subjective, separation logics. The latter may be viewed as having the self
component, but lacking other. To illustrate the difference, we give lock (Section 2) the following
spec, which is small [O’Hearn et al. 2001] wrt. the history τs s,
                              lock : [k]. {λs. τs s = ∅ ∧ k ≤ last_stamp (τo s)}
                                          {λs. ∃t . τs s = t Z⇒ L ∧ k < t }@Spin
and then we frame the history h onto τs s to obtain the equivalent large spec we actually presented:
                           lock : [h, k]. {λs. τs s = h ∧ k ≤ last_stamp (τ̂ s)}
                                          {λs. ∃t . τs s = h • t Z⇒ L ∧ k < t }@Spin
As expected in separation logic, framing increased the starting τs s from ∅ to h, which is the key
distinction between small and large specs. But this isn’t all it did; it also deducted h from τo s. Indeed,
had τo s been unchanged (as might also be expected in separation logic), then both specs would
contain the same conjunct k ≤ last_stamp (τo s). But the large spec contains k ≤ last_stamp (τ̂ s) =
last_stamp (h • τo s), where h is joined to τo s to compensate for the deduction.
   To explain the deduction, notice that in any separation logic, framing is a special case of parallel
composition. To add a frame h to the state of a program e, it suffices to compose e in parallel with
the idle thread having h as its self. The composition executes like e, but with self enlarged by h,
12                         Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


and h remains unchanged. In the subjective setting, parallel composition joins the self ’s of two
threads, but also decreases the other of the parent, as illustrated in Figure 6. It is this decrease that is
evidenced in the large spec.
   Therefore, framing enlarges self by h, and simultaneously removes h from other, which must
already contain h. Framing shuffles existing state between components, but doesn’t introduce new
state, in contrast to the usual separation logic formulations. This preserves the values of global
functions, and facilitates their use in specs (e.g., the global history τ̂ in lock).

3.2   Resources
Resources consist of state spaces and transitions. The state spaces describe the properties that hold
for all threads of the resource, so we use global predicates and functions to represent them.
   Definition 3.4. A state space is a pair Σ = (P, ⌜−⌝), where P is a global predicate and ⌜−⌝ is a
partial function into heaps, global under P, called erasure, such that for every state s, P s implies
as (s) ⊥ ao (s) and ⌜s⌝ is defined. We write s ∈ Σ to mean P s.
   Transitions describe the allowed atomic modifications on state. We require the following proper-
ties of them, to facilitate separation-style reasoning.
  Definition 3.5. A transition t over state space Σ is a binary relation on Σ states, such that:
  (1) (partial function) if t s s 1′ and t s s 2′ then s 1′ = s 2′ .
  (2) (other-fixity) if t s s ′, then ao s = ao s ′
  (3) (transition locality) if t (s  p) x, then there exists s ′ such that x = s ′  p and t (s  p) (s ′  p)
A state s is safe for t, if there exists s ′ such that t s s ′.
   Property (2) captures that a transition can’t change the other-component, as it’s private to other
threads. However, a transition can read this component, cf. how lock_tr in Figure 3 uses τo s as part
of τ̂ s to compute a fresh timestamp.
   Transition locality (3) essentially says that transitions can be framed. To see how, let θ 1 be a
thread in the state s  p, whose sibling θ 2 has self -component p. Their parent θ is thus in the state
s  p, by Figure 6. If θ 1 performs a transition t (s  p) x, then by (3), the move can be seen as a
transition of θ in the state s  p. In other words, the transition of a child can be seen as a transition
of the parent, but with self enlarged by p, and other suitably reduced by p. This is precisely the
view of framing described in Section 3.1.5. Hence, transition locality is the base case of, and gives
rise to, framing on programs, as a program’s execution is a sequence of transitions.
  Definition 3.6. A Σ-transition t is footprint preserving if t s s ′ implies that ⌜s⌝ and ⌜s ′ ⌝ contain
the same pointers.
   Transitions that preserve footprints are important because they can be coupled with other such
transitions without imposing side conditions on the combination. For example, consider the incr_tr
transition of Counter in Figure 3, which is footprint preserving, as it doesn’t allocate or deallocate
any pointers. Were it also to allocate, we will have a problem when combining Spin and Counter, as
we must impose that incr_tr won’t allocate the pointer r , already taken by Spin. For simplicity, we
here present the theory with only footprint-preserving transitions, but have added non-preserving
(aka. external) transitions as well [Nanevski et al. 2019]. External transitions encode transfer of
data in and out of a resource [de Alfaro and Henzinger 2001], of which allocation and deallocation
are an instance. When a resource requires allocation or deallocation, it can be tensored with an
allocator resource to exchange pointers through ownership transfer [Filipović et al. 2010b; Nanevski
et al. 2014] via external transitions. We elide further discussion, but refer to the Coq files for the
implementation of an allocator resource and example programs that use it.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                           13


   Definition 3.7. A resource is a tuple V = (M,T , Σ, ∆), where Σ is a space of (M,T )-states, and ∆
a set of footprint preserving Σ transitions. We refer to V ’s components as projections, e.g. Σ (V ) for
the state space, ∆ (V ) for the transitions, M (V ) for the PCM, etc. A state s is V -state iff s ∈ Σ (V ).
  We close the discussion on resources by defining actions—atomic operations on (combined real
and ghost) state, which are the basic building blocks of programs.
  Definition 3.8. An action of type A in a resource V is a partial function a : Σ (V ) ⇀ ∆ (V ) × A,
mapping input state to output transition and value, which is local, in the sense that it is invariant
under framing. Formally, if a (s  p) = (t, v) then a (s  p) = (t, v); that is, if a is performed by a
child thread, it behaves the same when viewed by the parent.
  The effect of a is the partial function [a] : Σ (V ) ⇀ Σ (V ) × A mapping input state to output state
and value, defined as [a] s = (s ′, v) iff ∃t . a s = (t, v) ∧ t s s ′. Note that [a] is a (partial) function
because a and t are.
  For example, we model the bracketed code used in the lock loop in Section 2, as the following
action of type bool:                    (
                                          (lock_tr, true) if ¬ω (τ̂ s)
                       trylock_act s b
                                     =                                                       (1)
                                          (id_tr, false)  otherwise
The action is local, as it depends only on τ̂ s, which is invariant under framing.
  We say that a erases to an atomic read-modify-write (RMW) command c [Herlihy and Shavit
2008], if [a] behaves like c when the states are erased to heaps. In other words, if [a] s = (s ′, v),
then c ⌜s⌝ = (⌜s ′ ⌝, v). One may check that trylock_act erases to CAS(r , false, true), as expected.11
Similarly,                                    (
                                                (unlock_tr, ()) if ω (τ̂ s)
                             unlock_act s b
                                          =                                                         (2)
                                                (id_tr, ())      otherwise
is an action of unit type, which erases to r := false.

3.3    Morphisms
   Definition 3.9. A resource morphism f : V → W consists of two partial functions f Σ : Σ (W ) ⇀
Σ (V ) (note the contravariance), and f ∆ : Σ (W ) ⇀ ∆ (V ) ⇀ ∆ (W ), such that:
   (1) (locality of f Σ ) there exists a function ϕ : M (W ) → M (V ) such that if f Σ (sw  p) = sv , then
       there exists sv′ such that sv = sv′  ϕ (p), and f Σ (sw  p) = sv′  ϕ (p).
   (2) (locality of f ∆ ) if f ∆ (sw  p)(tv ) = tw , then f ∆ (sw  p)(tv ) = tw .
   (3) (other-fixity) if ao (sw ) = ao (sw′ ) and f Σ (sw ), f Σ (sw′ ) exist, then ao (f Σ (sw )) = ao (f Σ (sw′ )).
   A morphism f transforms a V -program e into a W -program, as follows. When morph f e is in a
W -state sw , it has to determine a W -transition to take. It does so by obtaining a V -state sv = f Σ (sw ).
Next, out of sv , e can determine the transition tv to take. The morphed W -program then takes the
W -transition f ∆ (sw )(tv ).
   The properties (1) and (2) of Definition 3.9 provide basic technical conditions for this process
to be invariant under framing. Property (1) is a form of “simulation of framing”, i.e., a frame p in
W can be matched with a frame ϕ (p) in V . Thus, framing a morphed program can be viewed as
framing the original program. Property (2) says that framing doesn’t change the transition that f ∆
11 All the actions we use in this paper and in the Coq code erase to some RMW command. However, we proved this only by

hand, as our formalism and the Coq implementation don’t currently issue proof obligations to check this. In general, we
currently treat code and ghost code equally, and, as customary in type theory, equally to proofs. Differentiating between
these formally is an orthogonal issue that we plan to address in the future by making a type distinction between them, such
as in the work on proof irrelevance in type theory [Barras and Bernardo 2008; Gilbert et al. 2019; Pfenning 2001].
14                           Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


produces; thus it doesn’t influence the behavior of morphed programs. The property (3) restricts
the choice of sv′ in (1) so that ao (sv′ ) is uniquely determined by ao (sw ), much as how ϕ (p) in (1) is
uniquely determined by p. This is a technical condition which we required to prove the soundness
of the frame rule.
    Example. Properties (1)-(3) are all satisfied by the morphisms fn : Spin → SC from Section 2.
Indeed, M (SC) = M (Spin) × M (Counter) = Hist × N. Thus, a frame in SC is a pair of a history
and a nat; it is transformed into a frame in Spin just by taking the history component. We thus
instantiate ϕ in (1) with the first projection function, and it is easy to see that it satisfies the rest
of (1). Property (2) holds because (fn )∆ doesn’t depend on the state argument, hence framing this
state doesn’t change the output. Finally, in (3), the values ao (sw ) and ao (sw′ ) are also pairs of a
history and a nat. If the pairs are equal, then their history components are equal too, deriving (3).
    Finally, resources and their morphisms support a basic categorical structure, under the following
notions of morphism identity and composition. We have proved in the Coq files that morphism
composition is associative, with the identity morphism as the unit, where two morphisms are equal
if their Σ and ∆ components are equal as partial functions.
  Definition 3.10. The identity morphism id : V → V is defined by idΣ s = s and id∆ s t = t. The
composition of morphisms f : U → V and д : V → W is the morphism д ◦ f : U → W defined by:
                                   (д ◦ f )Σ sw    = f Σ (дΣ sw )
                                                   b
                                   (д ◦ f )∆ sw tu b
                                                   = д∆ sw (f ∆ (дΣ sw ) tu )

3.4     Simulations
Because f Σ and f ∆ are partial, a program lifted by a morphism isn’t immediately guaranteed to
be safe (i.e., doesn’t get stuck). For example, the state sv = f Σ sw , whose computation is the first
step of morphing, needn’t exist. Even if sv does exist, and the original program takes the transition
tv in sv , then tw = f ∆ sw tv needn’t exist. Even if tw does exist, there is no guarantee that sw is
safe for tw . An f -simulation is a condition that guarantees the existence of these entities, and their
mutual agreement (e.g., that sw is safe for tw ), so that a morphed program that typechecks against
the Morph rule doesn’t get stuck.
  Definition 3.11. Given a morphism f : V → W , an f -simulation is a predicate I on W -states
such that:
     (1) if I sw , and sv = f Σ (sw ) exists, and tv sv sv′ , then there exist tw = f ∆ sw tv and sw′ such that
         I sw′ and sv′ = f Σ (sw′ ), and tw sw sw′ .
     (2) if I sw , and sv = f Σ (sw ) exists, and sw −→∗ sw′ , then I sw′ , and sv′ = f Σ (sw′ ) exists, and
                                                         W
        sv −→∗ sv′ . Here, the relation s −→ s ′ denotes that s other-steps by W to s ′, i.e., that there
             V                                 W
         exists a transition t ∈ ∆ (W ) such that t s ⊤ s ′⊤ . The transposition s ⊤ = (ao s, a j s, as s) swaps
         the subjective components of s, to obtain the view of other threads. The relation −→∗ is the
                                                                                                      W
         reflexive-transitive closure of −→, allowing for an arbitrary number of steps.
                                           W

  Property (1) says that W simulates V on states satisfying I . Property (2) states the simulation in
the opposite direction, i.e., of W by V , but allowing many other-steps to match many other-steps.
Notice that other-stepping transitions over transposed states; that is, it changes the other, but, by
Definition 3.5(2), preserves the self of the states. Intuitively, (2) ensures that interference in W may
be viewed as interference in V , so that stable Hoare triples in V can be transformed into stable
Hoare triples in W , which is required for the soundness of the Morph rule. Property (1) has already
been shown in Figure 2; we repeat it in Figure 7, together with a diagram for property (2).
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                          15

                                           fΣ                              fΣ
                                     sv′          I sw′            sv′            I sw′




                                                                   ∗




                                                                                   ∗
                                    tv               f ∆ s w tv        V               W

                                     sv           I sw             sv             I sw
                                           fΣ                              fΣ

 Fig. 7. Commutative diagrams for the properties (1) and (2) of Definition 3.11 for I to be an f -simulation.



3.5    Inference Rules
We present the system using the Calculus of Inductive Constructions (CiC) as an environment logic,
hence as a shallow embedding in Coq. We inherit from CiC the useful concepts of higher-order
functions and substitution principles, and only present the notions specific to Hoare logic12 .
   We differentiate between two different notions of program types: ST V A and [Γ]. {P } A {Q }@V .
The first type circumscribes programs that respect the transitions of the resource V , and return
a value of type A if they terminate. The second, Hoare type, is a subset of ST V A, selecting only
those programs that satisfy the precondition P and postcondition Q, under the context Γ of logical
variables. To accommodate for the return values, the postcondition Q is now a predicate over values
of type A and states (if A = unit, we elide it from the Hoare type, as we did in Section 2).
   The key concept in the inference rules is the predicate transformer vrf e Q, which takes a program
e : ST V A, and a postcondition Q, and returns the set of V -states from which e is safe to run13 and
produces a result v and ending state s ′ such that Q v s ′. Hoare types are then defined in terms of
vrf, as follows.


                    [Γ]. {P } A {Q }@V = {e : ST V A | ∀Γ. ∀s ∈ Σ (V ). P s → vrf e Q s}                              (3)


We formulate the system using both vrf and the Hoare types. The former is useful, as it leads to
compact presentation, avoiding a number of structural rules of Hoare logic. The latter is useful
because it lets us easily combine Hoare reasoning with higher-order concepts. For example, having
inherited higher-order functions from CiC, we can immediately give the following type to the
fixed-point combinator, where T is the dependent type T = Πx :A . [Γ]. {P } B {Q }@V :


                                                 fix : (T → T ) → T                                                   Fix


Here, T serves as a loop invariant; in fix (λ f . e) we assume that T holds of f , but then have to prove
that it holds of e as well, i.e., it is preserved upon the end of the iteration.
  In reasoning about programs, we keep the transformer vrf abstract, and only rely on the following
minimal set of rules. These, together with the above definition of Hoare types and typing for fix,




12 Appendix D defines the denotational semantics, in CiC, for these notions, and states a theorem, proved in Coq, that the

inference rules are sound wrt. the denotational semantics.
13 Thus ensuring fault avoidance.
16                          Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


are the only Hoare-related rules of the system. In the rules we assume that e : ST V A, ei : ST V Ai ,
a is a V -action, f : V → W is a morphism, I is an f -simulation, s ∈ Σ (V ), and sw ∈ Σ (W ).
     vrf_post    : (∀v s. J s → Q 1 v s → Q 2 v s) → J s → vrf e Q 1 s → vrf e Q 2 s
     vrf_ret     : (Q v)• s → vrf (ret v) Q s
     vrf_bnd     : vrf e 1 (λx . vrf (e 2 x) Q) s → vrf (x ← e 1 ; (e 2 x)) Q s
     vrf_par     : ((vrf e 1 Q 1 ) ∗ (vrf e 2 Q 2 )) s → vrf (e 1 ∥ e 2 ) (λv:A1 ×A2 . (Q 1 v.1) ∗ (Q 2 v.2)) s
                   where (P ∗ Q) s b       = ∃s 1 s 2 . s = s 1 ∗ s 2 ∧ P s 1 ∧ Q s 2
    vrf_frame : ((vrf e Q 1 ) ∗ Q 2• ) s → vrf e (λv. (Q 1 v) ∗ Q 2 ) s
    vrf_act      : (λs ′ . ∃s ′′ v. [a] s ′ = (s ′′, v) ∧ (Q v)• s ′′)• s → vrf ⟨a⟩ Q s
    vrf_morph : f ˆ(vrf e Q) sw → I sw → vrf (morph f e) (λv sw′ . f ˆ(Q v) sw′ ∧ I sw′ ) sw
                   where f ˆR sw b     = ∃sv . sv = f Σ sw ∧ R sv
In English:
    • The vrf_post rule weakens the postcondition, similar to the well-known rule of Consequence
      in Hoare logic. The rule allows assuming a property J when establishing a postcondition
      Q 2 out of Q 1 . Here J is an invariant, i.e., a property preserved by the transitions of V ; an
      id-simulation. Thus, invariants can be elided from program specs, and invoked by vrf_post
      when needed.
    • The vrf_ret rule applies to an idle program returning v. When we want an idle program
      that returns no value, we simply take v to be of unit type. The rule explicitly stabilizes
      the postcondition Q to allow for the state s to be changed by interference of other threads
      in between the invocation of the idle program and its termination. Here, stabilization of a
      predicate Q is Q • (s) b    = ∀s ′ . s −→∗ s ′ → Q (s ′). The predicate Q is stable if Q = Q • , and it is
                                           V
       easy to see that Q • is stable for every Q.
    • The vrf_bnd rule is a Dijkstra-style rule for sequential composition. In order to show that
       the sequential composition x ← e 1 ; (e 2 x) has a postcondition Q, it suffices to show that e 1
       has a postcondition λx . vrf (e 2 x) Q. In other words, e 1 terminates with a value x and in a
       state satisfying vrf (e 2 x) Q, so that running e 2 x in that state yields Q.
    • The vrf_par and vrf_frame rules are predicate transformer variants of the rules for parallel
       composition and framing from separation logic. The separating conjunction P ∗ Q is defined
       as customary in separation logic, except that we use the subjective splitting of state, as
       explained in Section 3.1.3 and Figure 6. The vrf_frame rule can be seen as an instance of
       vrf_par, where e 2 is taken to be the idle programs returning no value. Thus, Q 2 is explicitly
       stabilized in vrf_frame, to match the precondition of the vrf_ret rule for idle programs.
    • The vrf_act rule says that Q holds after executing action a in state s, if s steps to s ′ by
       interfering threads, and then [a] s ′ returns the pair (s ′′, v) of output state and value. The
       latter satisfy the stabilization of Q, to allow for interference on s ′′ after the termination of a.
    • The vrf_morph rule is a straightforward casting of the Morph rule from Section 1 into a
       predicate transformer style.
  Finally, we also inherit all the CiC logical and programming constructs as well, which has
important consequences for Hoare-style reasoning. For example, in CiC one can form conditionals
over any type, including propositions and ST V A types. Thus, given a Boolean b and e 1 , e 2 : ST V A,
the following rule, derivable by case analysis on b, allows us to write programs that use conditionals,
and verify them in the usual Hoare-logic style.
           vrf_cond : (if b then vrf e 1 Q s else vrf e 2 Q s) → vrf (if b then e 1 else e 2 ) Q s
All the other customary rules of Hoare logic also become derivable. For example, if e : {P } {Q }
and ∀s ∈ Σ (V ). P ′ s → P s, then also e : {P ′ } {Q }. Similarly, if e depends on a logical variable x : A
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                                    17



            = [h, k]. {λs. τs s = h ∧ k ≤ last_stamp (τ̂ s)}{λs. ∃t . τs s = h • t Z⇒ L ∧ k < t }@Spin
      tyLck b

      1. fix (λloop : unit→tyLck. λ_ : unit.
      2.   {τs s = h ∧ k ≤ last_stamp (τ̂ s)}
      3.   {∃s ′ b. [trylock_act] s = (s ′, b) ∧
                     if b then ∃t . τs s ′ = h • t Z⇒ L ∧ k < t else τs s ′ = h ∧ k ≤ last_stamp (τ̂ s ′)}
      4.   b ← ⟨trylock_act⟩;
      5.   {if b then ∃t . τs s = h • t Z⇒ L ∧ k < t else τs s = h ∧ k ≤ last_stamp (τ̂ s)}
      6.   if b then {∃t . τs s = h • t Z⇒ L ∧ k < t } ret () {∃t . τs s = h • t Z⇒ L ∧ k < t }
      7.   else {τs s = h ∧ k ≤ last_stamp (τ̂ s)} loop () {∃ t . τs s = h • t Z⇒ L ∧ k < t }
      8.   {∃ t . τs s = h • t Z⇒ L ∧ k < t }) ()
Fig. 8. Proof outline (and implementation) for lock. Here, tyLck binds the spec given to lock in Section 2.3.

(i.e., e : [x : A]. {P x } {Q x }), then x can be specialized by v : A, to derive e : {P v} {Q v}. The latter
follows because the logical variables are universally quantified in the definition of Hoare types
(context Γ in (3)), and can thus be specialized just like any other universally quantified variable.14

3.6        Revisiting Spinlocks
To illustrate the inference rules, the proof outline in Figure 8 shows the proper implementation of
lock and the proof that lock has the type from Section 2.3 (the type is named tyLck in the figure).
The program is a loop executing CAS until it succeeds to lock. This is as in Section 2.3, except there
we informally bracketed CAS with the ghost code for manipulating histories, whereas here we
explicitly invoke the trylock_act action, which erases to CAS. The outline uses stable assertions
only: for example, the precondition in tyLck is stable, as argued in Section 2.3. Thus, we dispense
with explicit stabilization of assertions, i.e., applying (−)• .
   Given the Fix rule, in order to show that lock has the type tyLck, we must first prove that tyLck
is a loop invariant for fix, i.e., that it holds of the body of lock. Thus, the outline starts with the
precondition of tyLck in line 2, and derives the postcondition of tyLck in line 8. Line 3 derives
immediately from 2 and the definition of trylock_act in Section 3.2, equation (1), to expose that
trylock_act either succeeds to lock adding an L to the self history, of fails to lock keeping the
history unchanged.15 Notice that Line 3 has exactly the form required of a premise for the vrf_act
rule, with stabilization elided. Thus, the if−then−else conjunct in Line 3 is also a postcondition of
trylock_act, and therefore holds in line 5. Next we branch on b, which corresponds to applying the
rule vrf_cond. Line 6 considers the case b = true, and the postcondition immediately follows by the
rule vrf_ret (again, eliding stabilization). Line 7 considers the case b = false, and the postcondition
immediately follows as the recursive call to loop, by assumption, already has the desired type tyLck.
As both branches of the conditional have the same postcondition, the postcondition propagates to
line 8 to complete the proof.

4     EXCLUSIVE LOCKING VIA MORPHING AND THE NEED FOR PERMISSIONS
We next illustrate a more involved application of morphisms and simulation: how to derive a
resource and methods for exclusive locking, à la CSL [O’Hearn 2007], from the resource for spin
14 We perform the described type changes silently in the paper. In Coq, they aren’t silent, but must be marked by a constructor.

Our implementation minimizes the number of such constructors, and makes them unobtrusive, but describing how is
beyond the scope of the paper.
15 In the case of failure, we could also derive that the lock was taken at the moment trylock_act was attempted, i.e.

∃t . τs s ′ = h ∧ τ̂ s ′ t = L ∧ k ≤ t ≤ last_stamp (τ̂ s ′ ). However, the rest of the proof doesn’t require the additional detail.
18                              Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas



                                           lock_tr                       open_tr
                                                               ▷◁

                                   Spin                                             CSLX

                                                               ▷◁
                                          unlock_tr                      close_tr
     State space Σ (Spin): s ∈ Σ (Spin) iff                     State space Σ (CSLX): s ∈ Σ (CSLX) iff
      τs s, τo s ∈ Hist, and πs s, πo s ∈ N, and                   α s s, αo s ∈ O, and σs s, σo s, σ j s ∈ Heap, and
      τs s ⊥ τo s ∧ alternate (τ̂ s) ∧ r , null                    α s s ⊥ α o s ∧ σ s s ⊥ σ j s ⊥ σo s ∧
                                                                   if α̂ s = own then σ j s = ∅ else R (σ j s)
     Erasure: ⌜s ⌝ b    = r Z⇒ ω (τ̂ s)                         Erasure: ⌜s ⌝ b     = σ̂ s • σ j s
     Transitions ∆(Spin):                                       Transitions ∆ (CSLX):
     lock_tr s s ′ b
                   = ¬ω (τ̂ s) ∧                                open_tr s s ′ b = α s s = own ∧ α s s ′ = own ∧
       τs s ′ = τs s • fresh (τ̂ s) Z⇒ L ∧ πs s ′ = πs s + 1       σs s = σs s • σ j s ∧ σ j s ′ = ∅
                                                                         ′
     unlock_tr s s ′ b= ω (τ̂ s) ∧ πs s > 0 ∧                   close_tr s s ′ b= α s s = own ∧ α s s ′ = own ∧
       τs s ′ = τs s • fresh (τ̂ s) Z⇒ U ∧ πs s ′ = πs s − 1       σs s = σs s ′ • σ j s ′ ∧ R (σ j s ′ )

Fig. 9. Redefinition of Spin, and CSLX resource for heap transfer in exclusive locking (in our implementation,
Spin contains external transitions for receiving and giving away permissions to unlock, and CSLX contains
transitions for reading and writing pointers in σs ; we elide both for simplicity).

locks from Section 2. An exclusive lock protects a shared heap, satisfying a user-supplied predicate
R (aka. resource invariant). Upon successful locking, the shared heap is transferred to the private
ownership of the locking thread, where it can be modified at will, potentially violating R. Before
unlocking, the owning thread must re-establish R in its private heap, after which, the part of the
heap satisfying R is moved back to the shared status. The idea is captured by the following methods
and specs, which we name exlock and exunlock to differentiate from lock and unlock in Section 2.
                   exlock : {λs. µ s s = own ∧ χs s = ∅} {λs. µ s s = own ∧ R (χs s)}@CSL
                 exunlock : {λs. µ s s = own ∧ R (χs s)} {λs. µ s s = own ∧ χs s = ∅}@CSL
Here µ s s is a ghost of type O = {own, own}, signifying whether “we” own the lock or not, and χs s
is “our” private heap. O has PCM structure with the join defined by x • own = own • x = x, so
that own is the unit of the operation. We leave own • own undefined, to capture that the locking is
exclusive, i.e., the lock can’t be owned by a thread and its environment simultaneously. Our goal in
this section is to derive exlock and exunlock using morphing and simulations to “attach” to lock
and unlock the functionality of transferring the protected heap between shared and private state.
    The idea for doing so is pictorially shown in Figure 9, where the CSLX resource contains the state
components and transitions describing the functionality needed for heap transfers. In particular,
α s s ∈ O keeps track of whether we own the lock or not, σs and σ j are the private and shared heap
respectively, and the transitions open_tr and close_tr move the heap from shared to private and
back, respectively. We want to combine the Spin and CSLX resources as shown in the figure, by
combining their state spaces, and coupling open_tr with lock_tr, and close_tr with unlock_tr, so
that the transitions execute simultaneously. This will give us an intermediate resource CSL′, and a
morphism f : Spin → CSL′ defined similarly to the morphisms in Section 2:
                                      fΣ s               = s\1
                                                         b
                                      f ∆ s lock_tr   = lock_tr ▷◁ open_tr
                                                      b
                                      f ∆ s unlock_tr b
                                                      = unlock_tr ▷◁ close_tr
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                               19


We will then restrict CSL′ into the CSL resource that we used in the specs for exlock and exunlock,
as we shall describe. The components µ s and χs used in these specs will be functions out of the
state components of CSL.
   However, if we try to carry out the above construction using the Spin resource from Section 2, we
run into the following problem. Recall that Spin can execute unlock_tr whenever the lock is taken,
irrespective of which thread took it. On the other hand, close_tr can execute only if “we” hold the
lock. But, f ∆ s unlock_tr = unlock_tr ▷◁ close_tr, and therefore, in states where others hold the
lock, Spin may transition by unlock_tr, with CSL′ unable to follow by f ∆ . Moreover, it’s impossible
to avoid such situations by choosing a specific f -simulation I that will allow unlock_tr to execute
only if we hold the lock. Simply, there is no way to define such I because we can’t differentiate in
Spin between the notions of unlock_tr being “enabled for us”, vs. “enabled for others, but not for
us”, as unlock_tr is enabled whenever the lock is taken.
   The analysis implies that we should have defined Spin in a more general way, as shown in Figure 9.
In particular, Spin should contain the integer components πs /πo which indicate if unlock_tr is
“enabled for us” (πs s > 0), or not (πs s = 0), and dually for others. These will give us the distinction
we seek, as we shall see. In line with related work, we call π permission to unlock.16,17
   A thread may have more than one permission to unlock, which it can distribute among its
children upon forking, who can then race to unlock. The addition of the new fields leads to the
following minimal modification of the specs from Section 2, to indicate that lock enables unlock_tr,
and a successful unlock consumes one permission. Note that the specs don’t assume that having a
permission to unlock implies that it was “us” who last locked, or even that the lock is taken. We will
impose such locking-protocol specific properties on CSL, but there is no need for them in Spin.18

                     lock′ : [h, k]. {λs. τs s = h ∧ k ≤ last_stamp (τ̂ s) ∧ πs s = 0}
                                     {λs. ∃t . τs s = h • t Z⇒ L ∧ k < t ∧ πs s = 1}@Spin
                   unlock′ : [h, k]. {λs. τs s = h ∧ k ≤ last_stamp (τ̂ s) ∧ πs s = 1}
                                     {λs. ∃t . τs s = h • t Z⇒ U ∧ k < t ∧ πs s = 0 ∨
                                        τs s = h ∧ τ̂ s t = U ∧ k ≤ t ∧ πs s = 1}@Spin
Let us now consider the combination CSL′ of Spin and CSLX as defined in Figure 9. The combination
has a number of state components with overlapping roles. For example, α from CSLX keeps the
status of the lock, and is needed in CSLX in order to describe the heap-transfer functionality
independently of Spin. On the other hand, Spin keeps the locking histories in τ . Thus, once Spin
and CSLX are combined, the two components must satisfy
                                                ω (τs s) = (α s s = own)                                                   (4)
                                                ω (τo s) = (α o s = own)

 as a basic coherence property. Furthermore, we want to encode exclusive locking, so we must

16 In general, the design of resource’s permissions obviously and essentially influences how that resource composes with

others. Some systems, such as CAP [Dinsdale-Young et al. 2010] and iCAP [Svendsen and Birkedal 2014], although they
don’t consider morphisms and simulations, by default provide a permission for each transition of a resource. In our example,
that would correspond to also having a permission for lock_tr. Full generality also requires external transitions that move
permissions to and from an outside resource. In our Coq code, these are used in the readers-writers example, to support
non-exclusive locking. For simplicity, we elide such generality here, and consider only the permission to unlock, which
suffices to illustrate morphisms and simulations.
17 Similar concepts arise in other concurrency models as well. For example, a transition in a Petri net fires only if there are

sufficient tokens—akin to permissions—in its input places. The tokens are consumed upon firing.
18 Following Section 3.1.5, we make the specs small wrt. π s, for simplicity. By framing, lock′ can be invoked when π s ≥ 0,
                                                          s                                                             s
in which case it increments πs s by 1.
20                             Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


require that only the thread that holds the lock has the permission to unlock:
                                        πs s = (if α s s = own then 1 else 0)                                              (5)
                                        πo s = (if α o s = own then 1 else 0)
(thus, πs s, πo s ∈ {0, 1}, and at most one of them is 1).
   Most importantly, the events recorded in the histories of Spin should correspond to exclusive
locking, and thus:
                                              τs s ⊥ω τo s                                    (6)
where h ⊥ω k is defined as
                                 (ω h → last_stamp k < last_stamp h) ∧
                                 (ω k → last_stamp h < last_stamp k) ∧ h ⊥ k
to say that if h (resp. k) indicates that a thread holds the lock, then another thread couldn’t have
proceeded to add logs to its own history k (resp. h), and unlock itself.19
   It is now easy to see that Inv = (4) ∧ (5) ∧ (6) is an invariant of CSL′. The critical point is that
(6) is preserved by the transition t = unlock_tr ▷◁ close_tr. Indeed, if in state s ∈ Inv we transition
by t, it must be πs s > 0 by t’s definition, and thus πs s = 1, and πo s = 0, by (5). Also, we add a
fresh U entry to the ending state s ′, thus making last_stamp (τs s ′) > last_stamp (τo s ′). For (6) to
be preserved, it must then be ω (τo s ′) = ω (τo s) = false, i.e., the lock wasn’t held by another thread.
But this is guaranteed by (4), (5) and πo s = 0. In other words, by using the permissions to unlock,
we have precisely achieved the distinction that our previous definition of Spin couldn’t make.
   Because Inv is invariant, we can construct a resource CSL out of CSL′, where Inv is imposed as
an additional property of the underlying PCM and state space of CSL′. Indeed, our theory ensures
that the set Σ (CSL′) ∩ Inv can be made a global predicate, and thus be used as a state space of a new
resource CSL. By Definition 3.2, globality depends on the underlying PCM, hence the construction
involves restricting the PCM of CSL′ by Inv. The mathematical underpinnings of such restrictions
involve developing the notions of sub-PCMs, PCM morphisms and compatibility relations, which
we carry out in Appendix B. Here, it suffices to say that the construction leads to the situation
summarized by the following diagram:
                                                        f             ι
                                                Spin −→ CSL′ −→ CSL
where morphism ι is defined by ι Σ s = s and ι ∆ s t = t. Intuitively, CSL states are a subset of CSL′
states satisfying Inv, and ι Σ is the injection from Σ (CSL) to Σ (CSL′).
   This gives us the CSL resource, but we still need to transform lock′/unlock′ into exlock/exunlock,
respectively. We thus introduce the following property on CSL states:
                               Sim s b
                                     = if α s s = own then R (σs s) else σs s = ∅
which says that the self heap satisfies the resource invariant R iff the thread owns the lock. Sim,
unlike Inv, is not an invariant, because it is perfectly possible for a thread to own the lock, but for its
heap to not satisfy R, because the thread has modified the acquired heap after locking it. However,
Sim is an (ι ◦ f )-simulation, as it satisfies the commuting diagrams from Figure 7. For example,
when Spin executes lock_tr, then CSL sets α s s = own and acquires the shared heap, thus making
the self heap satisfy R. When Spin executes unlock_tr, then CSL returns the shared heap, making
the self heap empty. In other words, Sim describes the state of CSL immediately after locking, and
immediately before unlocking, which suffices for the morphing of lock′ and unlock′. We only show
19 Requirement (6) restricts only the last timestamp in h and k , not all timestamps hereditarily. This suffices for our proof.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                          21


the derivation for exunlock = morph (ι ◦ f ) unlock′, and refer to the Coq code [Nanevski et al.
2019] for the derivation of exlock, which is similar.
                        1. {α s s = own ∧ R (σs s)}
                        2. {τs s = h ∧ πs s = 1 ∧ α s s = own ∧ R (σs s)}
                        3. {τs s = h ∧ k = last_stamp (τ̂ s) ∧ πs s = 1 ∧ Sim s}
                        4. morph (ι ◦ f ) unlock      // using simulation Sim
                                                  ′

                        5. {(τs s = h • t Z⇒ U ∧ k < t ∧ πs s = 0 ∨
                             τs s = h ∧ k ≤ t ∧ τ̂ s t = U ∧ πs s = 1) ∧ Sim s}
                        6. {τs s = h • t Z⇒ U ∧ k < t ∧ πs s = 0 ∧ Sim s}
                        7. {α s s = own ∧ σs s = ∅}

The key step is in line 6, where we must derive that the second disjunct in line 5 is false; that is, no
thread could have unlocked before us in line 4. We infer this by reasoning about the histories τs s
and τo s in line 5. From πs s = 1, it must be α s s = own, and then ω (τs s) = true, by the invariant
Inv which holds throughout, as s is a CSL state. By Inv again, τs s ⊥ω τo s, so last_stamp (τo s) <
last_stamp (τs s). Thus, it must be last_stamp (τs s) = last_stamp (τ̂ s) = k, because last_stamp (τ̂ s)
is the maximum of last_stamp (τs s) and last_stamp (τo s). But this contradicts that τ̂ s contains
entry U at t ≥ k. We can now derive line 7: α s s = own follows from πs s = 0 and Inv, and σs s = 0
follows by Sim. Finally, we obtain the desired spec of exunlock from the beginning of the section,
by letting µ be α and χ be σ .

5   QUIESCENCE AND INDEXED MORPHISM FAMILIES
The previous examples were about extending Spin the functionality of another resource, Counter
or CSLX. In this section, we apply resource morphism not to extend a resource, but to restrict it,
specifically by “forgetting” its ghost state. This is a feature commonly required when installing
one resource into a private state of another. We need a slight generalization, however, to indexed
morphism families (or just families, for short), as follows.
                    X
   A family f : V → W introduces a type X of indices for f . The state component f Σ : X → Σ (W ) ⇀
Σ (V ) and the transition component f ∆ : X → Σ (V ) → ∆ (V ) ⇀ ∆ (W ) now allow input X , and satisfy
a number of properties, listed in Appendix C, that reduce to Definition 3.9 when X is the unit
type. Similarly, f -simulations must be indexed too, to be predicates over X and Σ (W ), satisfying a
number of properties which reduce to Definition 3.11 when X = unit.
   The morph constructor and its rule are generalized to receive the initial index x, and postulate
the existence of an ending index y in the postcondition, as follows:
                                               e : {P } {Q }@V
                                                                                              MorphX
            morph f x e : {λsw . (f x)ˆP sw ∧ I x sw } {λsw . ∃y. (f y)ˆQ sw ∧ I y sw }@W

                             where (f x)ˆR sw b
                                              = ∃ sv . sv = f Σ x s w ∧ R sv
   To illustrate, consider the resource Stack (Figure 10) implementing concurrent stacks, and the
following spec for the stack’s push method, similar to that of lock from Section 2.
            push(v) : [k]. {λs. σs s = ∅ ∧ τs s = ∅ ∧ k ≤ last_stamp (τo s)}
                           {λs. σs s = ∅ ∧ ∃t vs. τs s = t Z⇒ (vs, v :: vs) ∧ k < t }@Stack
Here τs , and τo are histories of stack’s operations, as in the case of Spin, and σs is the thread-
private heap. The spec says that push starts with τs s = ∅ (by framing, any history) and ends with
τs s = t Z⇒ (vs, v :: vs) to indicate that a push of v indeed occurred, and after all the timestamps
from the pre-state. The joint heap σ j stores the stack’s physical layout, and α̂ s is the abstract
22                             Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas



                           Stack:
                                              σo
                                                           dom (τ̂ s) = {1, . . . , last_stamp (τ̂ s)}
                                    τs    σj       τo
                                                           layout (α̂ s) (σ j s)
                                         σs



Fig. 10. Representation of the state components of the Stack resource. The self components (σs for the heap,
and τs for the history) are in light shade, the other components are in dark; the joint component (σ j for
the heap storing the stack’s physical layout) is white. The abbreviation α̂ s is the abstract value of the stack
(computed out of τ̂ s).


contents of the stack as a mathematical sequence (computed out of τ̂ s). Intuitively, push first
allocates a new node in σs , then moves it to σ j where it is enlinked to the top of the laid-out stack,
after which push updates τs and α̂ to reflect the addition of the node. We also elide the full definition
of Stack as it isn’t essential here; it suffices to know that predicate layout describes how α̂ is laid
out in σ j (i.e., ∀s ∈ Σ (Stack). layout (α̂ s) (σ j s)), and that the global history τ̂ s has no timestamp
gaps (i.e., ∀s ∈ Σ (Stack). dom (τ̂ s) = {1, . . . , last_stamp (τ̂ s)}).20
   Consider now the program e = push(a) ∥ push(b) of the following type (also derived in Coq):
      e : {λs. σs s = ∅ ∧ τs s = ∅}
          {λs. σs s = ∅ ∧ ∃t 1 vs 1 t 2 vs 2 . τs s = t 1 Z⇒ (vs 1 , a :: vs 1 ) • t 2 Z⇒ (vs 2 , b :: vs 2 )}@Stack
The specification reflects that e pushes a and b, to change the stack contents from vs 1 to a :: vs 1
at time t 1 , and from vs 2 to b :: vs 2 at time t 2 . The order of pushes is unspecified, so we don’t know
if t 1 < t 2 or t 2 < t 1 (as • is commutative, the order of t 1 and t 2 in the binding to τs s in the post
doesn’t imply an ordering between t 1 and t 2 ). Moreover, we don’t know that t 1 and t 2 occurred
in immediate succession (i.e., t 2 = t 1 + 1 ∨ t 1 = t 2 + 1), as threads concurrent with e could have
executed between t 1 and t 2 , changing the stack arbitrarily. Thus, we also can’t infer that the ending
state of t 1 equals the beginning state of t 2 , or vice versa.
    But what if we knew that e is invoked without interfering threads, i.e., quiescently [Aspnes et al.
1994; Derrick et al. 2011; Jagadeesan and Riely 2014; Nanevski et al. 2014; Sergey et al. 2016]? For
example, imagine a resource Priv with only heaps χs and χo , and no other components (Figure 11(1)),
and transitions that allow modifying the self heap by reading, writing, CAS-ing, or executing any
other read-modify-write command [Herlihy and Shavit 2008]. A program working over Priv can
install an empty stack in χs and then invoke e over it. Because the stack is installed privately, no
threads other than the two children of e can race on it. Could we exploit quiescence, and derive
just out of the specification of e that the stack at the end stores either the list [a, b], or [b, a]? This
fact can be stated even without histories, using solely heaps, as follows:
                 {λs. layout nil (σs s)}{λs. layout [a, b] (χs s) ∨ layout [b, a] (χs s)}@Priv                         (7)
The move from Stack to Priv thus essentially forgets the ghost state of histories, and the distinction
in Stack between shared and private heaps. These components and distinctions are visible when
in the scope of Stack, but hidden when in Priv. We would like to obtain the spec (7) by applying
the Morph rule to the Stack spec of e, with a morphism д : Stack → Priv that forgets the histories.
Unfortunately, such a morphism can’t be constructed as-is. Were it to exist, then дΣ , being con-
travariant, should map a state s Priv , containing only heaps, to a state s Stack , containing heaps and
histories; thus дΣ must “invent” the history component out of thin air.
20 We mechanized this development in Coq for the Treiber variant of stacks, with some minor Treiber-specific modifications.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                                       23



                                  Priv:                                дΣ x s Priv :
                                                       χo                                       σo
                                                                                       x    σj       ∅
                                            χs                                             σs


                                                 (1)                                        (2)

Fig. 11. The left figure shows the state components of Priv. The right figure shows how Stack from Figure 10
is related to Priv by дΣ . Striped and bricked regions show the Priv’s self heap χs = σs • σ j and other heap
χo = σo , respectively. Solid regions show the Stack’s self history τs = x and other history τo = ∅.

                                                                               Hist
  This is where families come in. We make д : Stack → Priv a family over X = Hist, thereby
passing to дΣ the history x that should be added to s Priv to produce an s Stack (Figure 11(2)).
                             дΣ x s Priv = s Stack b
                                                   = χs (s Priv ) = σs (s Stack ) • σ j (s Stack ) ∧
                                                     χo (s Priv ) = σo (s Stack ) ∧
                                                     τs (s Stack ) = x ∧ τo (s Stack ) = ∅
The first conjunct directly states that Stack is installed in χs (s Priv ) by making χs (s Priv ) be the
join of the heaps σ j (s Stack ) and σs (s Stack ).21 The second conjunct says that the heap χo (s Priv ) of
the interfering threads is propagated to σo (s Stack ). The third conjunct captures that the history
component of s Stack is set to the index x, as discussed immediately above. In the last conjunct, the
τo (s Stack ) history is declared ∅, thus formalizing quiescence. We elide the definition of д∆ ; it suffices
to know that it maps a Stack transition (relation over heap and ghost state of Stack) to its “erasure”,
i.e. a relation over heaps of Priv representing a single-pointer operation such as read, write and
CAS, but ignoring the ghost histories.
   We can now obtain the quiescent spec (7) by applying the MorphX rule to e, as shown below, with
x = ∅, and I x being the always-true predicate on Priv states (the outline expands the definition of
(д x)ˆ_, and elides the always-true I x).
             1. {layout nil (χs (s Priv ))}
             2. {∃s Stack . s Stack = дΣ ∅ s Priv ∧ σs (s Stack ) = ∅ ∧ τs (s Stack ) = ∅}
             3. morph д ∅ e
             4. {∃y s Stack . s Stack = дΣ y s Priv ∧ σs (s Stack ) = ∅ ∧
                               ∃t 1 vs 1 t 2 vs 2 . τs (s Stack ) = t 1 Z⇒ (vs 1 , a :: vs 1 ) • t 2 Z⇒ (vs 2 , b :: vs 2 )}
             5. {layout [a, b] (χs (s Priv )) ∨ layout [b, a] (χs (s Priv ))}

Line 2 derives trivially from line 1, as the state s Stack is uniquely determined; i.e., take σ j (s Stack ) to be
the heap storing the empty stack, and all the other components of s Stack to be empty. We next derive
the postcondition in line 5. From the properties of Σ (Stack), we know layout (α̂ (s Stack )) (σ j (s Stack )).
From s Stack = дΣ y s Priv and other conjuncts in line 4, we know χs (s Priv ) = σ j (s Stack ), and τs (s Stack ) = y,
and τo (s Stack ) = ∅. Thus, it is also τ̂ (s Stack ) = y = t 1 Z⇒ (vs 1 , a :: vs 1 ) • t 2 Z⇒ (vs 2 , b :: vs 2 ), and:
                                                  layout (α̂ (s Stack )) (χs (s Priv ))                                           (8)
From the properties of Σ (Stack), we also know that τ̂ (s Stack ) has no timestamp gaps; thus {t 1 , t 2 } =
dom (y) = {1, 2}, i.e., t 1 and t 2 are the only, and consecutive, events in y. But then α̂ (s Stack ) must be
either [a, b] or [b, a], which, with (8), derives the postcondition.
21 As we want to build s
                         Stack out of s Priv , we have to identify the part of χ s (s Priv ) which we want to assign to σ j (s Stack ).
This part has to be uniquely determined, else дΣ won’t be a function. We ensure uniqueness by insisting that the predicate
layout is precise – a property commonly required in separation logics.
24                       Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


6    RELATED WORK
   Coalgebra morphisms and refinement mappings. Transition systems are mathematically repre-
sentable as coalgebras [Jacobs 2016; Rutten 2000]; thus, resource morphisms are closely related
to coalgebra morphisms, with differences arising from our application to concurrent separation
logic and types. For example, for us, given f : V → W , f Σ is contravariant, but in the coalgebraic
case, f is covariant on states [Hasuo et al. 2009; Rutten 2000]. A coalgebra morphism f doesn’t
have the f ∆ component, but requires that f preserve and reflect the V -transitions (i.e., if x → y is
a V -transition, then f (x) → f (y) is a W -transition, and if f (x) → t is a W -transition, then there
exists y such that x → y is a V -transition, and f (y) = t). These properties are similar in spirit to
the two clauses of our Definition 3.11 of f -simulations.
   Similarly, refinement mappings [Abadi and Lamport 1991; Lynch and Vaandrager 1995], like
coalgebra morphisms, are covariant functions on STSs, and differ from resource morphisms in
the intended use. For example, with refinement mapping, the key question is how to extend the
source STS with ghost state. The extension may be necessary, as a refinement mapping need not
exist otherwise. In contrast, we seek to give a definitive resource type to a program, which suffices
for all reasoning. The program can be morphed, to change the type, but can’t be re-typed by an
extended resource, as that violates compositionality in our setting. Given a morphism f : V → W ,
the resource W will most commonly generalize and include V ’s functionality. Thus, f Σ can compute
sv ∈ Σ (V ) out of sw ∈ Σ (W ), without needing to extend V or W . When sw lacks information to
compute sv (cf. the quiescence example in Section 5), we don’t extend the resources, but pass the
missing information by an index in a morphism family. Morphisms also exhibit a form of (weak)
simulation of W by V on the transposed states (Definition 3.11(2)).
   We further establish the action of f on programs, and provide a Hoare logic rule to reason
about it, supporting the usual compositionality notions from separation logic, such as framing and
ownership transfer, which haven’t been considered in the context of coalgebra morphisms and
refinement mappings.
   Linearizability. In a relational flavor of separation logics [Frumin et al. 2018; Liang et al. 2012;
Turon et al. 2013], and more generally, in the work on proving linearizability [Bouajjani et al. 2017;
Gu et al. 2015, 2018; Henzinger et al. 2013; Khyzha et al. 2017; Liang and Feng 2013; Schellhorn et al.
2012], the goal is to explicitly relate two programs, typically one concurrent, the other sequential.
The sequential program then serves as a spec for the concurrent one, and can replace it in any
larger context. Our goal in this paper is somewhat different; we seek to identify the concurrent
program’s type, which for us takes the form of a Hoare triple enriched with a resource. The type
serves as the program’s interface, and, as standard in type theory, any two programs with the
same type can be interchanged in clients’ code and proofs. As clients can already reason about the
program via this type, the program shouldn’t need a spec in the form of another program.
   There are several advantages of our approach over linearizability. First, a spec in the form of a
Hoare triple with a resource is much simpler, and thus easier to establish than a spec in the form of
another program. Indeed, resources aren’t programs; they are STSs and don’t admit programming
constructs such as conditionals, loops, initial or local state, or function calls. A Hoare spec is also
immediately useful in proofs, whereas with linearizability, one also has to verify the sequential
program itself. Second, in linearizability it has traditionally been difficult to address ownership
transfer of heaps between data structures [Cerone et al. 2014; Gotsman and Yang 2012], whereas
for us (and other extensions of CSL [da Rocha Pinto et al. 2014; Dinsdale-Young et al. 2010; Jung
et al. 2018, 2015; Liang and Feng 2013]), ownership transfer is directly inherited from separation
logic. We also inherit from separation logic a way to dynamically nest parallel compositions of
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                           25


threads, whereas linearizability is typically considered on programs with a fixed, though arbitrary,
number of threads.
   That said, we note that our specs of lock and unlock in Section 2 are actually very close to
what one gets from linearizability, as they essentially establish a linear order between locking
and unlocking events in the history PCM. In fact, our approach seems sufficiently powerful to
directly specify, in the state space of a resource, the general property of linearizability as a user-level
proposition over the resource’s subjective histories, which is the direction we intend to pursue
in the future. Such a development would generalize the current paper, in that the events tracked
by histories wouldn’t be instantaneous, as was the case in Section 2, but would have non-zero
duration. The histories would have to record the events’ beginning as well as ending times.
   Morphisms and simulations will play a key role in such a setting. For example, two different
resources will have two different spaces of timestamps (i.e., two different clocks). Combining the
two into a larger resource, will require constructing a history for the combination, of which the
first step is reconciling the clocks of the two components into a common clock. Morphisms and
simulations will be a necessary abstraction to relate the common clock, timestamps, and history to
the clocks, timestamps, and histories of the components.
   In future work, we thus expect to incorporate general linearizable programs and resources;
note, however, that the PCM and history-based approach is further general still, and capable of
compositionally specifying and verifying non-linearizable programs as well [Sergey et al. 2016].
      State transition systems and abstract atomicity. Abstract atomicity refers to extending the
functionality of a concurrent program so that it operates over other STSs. One of the most powerful
approaches to abstract atomicity has been parametrization by auxiliary code. For example, in the
case of spin locks, a way to make lock operate over an extension of Spin with an unknown STS X ,
is to parametrize lock a priori with an unknown ghost function α over X , thus modifying it into:
                           = do ⟨x ← CAS(r , false, true); if x then α ⟩ while ¬x
                    lock α b
This differs from our approach, where the modification to lock is done a posteriori, and is mediated
by the resource type of the program. Parametrization originated in Jacobs and Piessens [2011],
and was extended to impredicative higher-order ghost functions and state in HOCAP [Svendsen
et al. 2013], iCAP [Svendsen and Birkedal 2014] and Iris [Jung et al. 2018, 2015]). Parametrization
affords abstract specifications that are similar to specifications that one would ascribe to a data
structure in the sequential setting. It applies to the locking examples, as illustrated above, but also
to many of the examples that we included in the Coq code. Parametrization relies on higher-order
and impredicative ghost functions to specify a number of concurrency idioms, such as e.g., fork/join
concurrency, or storing of concurrent programs into the heap. In contrast, our present model is
predicative (see Appendix D); hence we currently support the more restrictive concurrency by
parallel composition.
   Thus our approach doesn’t presently extend the range of verifiable programs. Rather, it proposes
novel type-based foundations that underpin the verification, and that employ morphisms, histories,
and simulations. Histories and simulations are foundational abstractions in concurrency. Morphisms
are similarly so in mathematics, and in our case, relate to coalgebras and refinement mappings,
as discussed. It’s therefore of inherent interest to embed these abstractions into type theory and
obtain a minimalistic proof system for separation logic, as we have done.
   By relying on these foundational abstractions, we achieve some uniformity and simplicity of
reasoning, which we expect to build on in the future. For example, one challenge to parametrization
arises when the point at which to execute the ghost function can be determined only after the
program has terminated. This is a common pattern when proving linearizability, as exhibited, say,
by the queue of Herlihy and Wing [1990], but has been difficult to address by parametrization,
26                       Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


because it isn’t clear at which point in the code to invoke the parametrizing ghost function. In our
case, histories separate the termination of operations from their order in the linearization. The
order becomes just another ghost component that can be constructed at run time, with cooperation
of other threads [Delbianco et al. 2017]. A history-based spec can say that an operation finished
executing, but that its exact place in the linearization is to be fully determined only later, by the
action of other threads. We thus expect that history-based specs will support the described pattern
of linearizability proofs.
   The TaDA logic of da Rocha Pinto et al. [2014] introduces another approach to abstract atomicity
that doesn’t rely on parametrization. TaDA defines a new judgment form, ⟨P⟩ e ⟨Q⟩, that captures
that e has a precondition P and postcondition Q, but is also abstractly atomic in the following
sense: e and its concurrent environment maintain the validity of P, until at one point e takes an
atomic step that makes Q hold. Afterwards, Q may be invalidated, either by future steps of e, or
by the environment. Once judged atomic, programs can be associated with ghost code of other
resources. In this sense, TaDA’s extension of code is a posteriori, similar to ours. In contrast to
TaDA, we specify programs using ordinary Hoare triples, but rely on the PCM of histories to
express atomicity: a program is atomic if it adds a single entry to the self history. In the Coq files,
we have also applied morphisms to algorithms with helping, such as the flat combiner [Hendler
et al. 2010], where one thread executes work on behalf of others; helping is an idiom that TaDA
currently can’t express.
   Sergey et al. [2018] have designed a logic Disel for distributed systems, in which one can combine
distributed protocols—represented as STSs—by means of hooks. A hook on a transition t prevents t
from execution, unless the condition P associated with the hook is satisfied. In this sense, hooks
implement an instance of our transition coupling, where one operand is fixed to the idle transition
with a condition P, i.e. id_tr P = λs s ′ . P s ∧ s ′ = s. Disel doesn’t currently consider hooks where
both operands are non-idle, which we used in the lock examples, or notions of morphism and
simulation. On the other hand, we haven’t considered distribution so far.
   Finally, while morphisms and simulations provide a solution to abstract atomicity, they also
go beyond it. For example, they apply to quiescence (Section 5), which, unlike abstract atomicity,
doesn’t extend functions to resource combinations, but forgets the histories of a resource. They
may also provide a foundation for answering more basic, categorical, questions about concurrent
structures, such as e.g., “when are two resources isomorphic” (answer: when there are cancelling
morphisms between them). We plan to explore such questions in the future.
   Automated separation logics for concurrency. A number of recent automated tools such as
Verifast [Jacobs et al. 2011], VerCors [Amighi et al. 2018; Blom and Huisman 2014], and Viper [Müller
et al. 2016], address the reasoning about concurrent programs in various extensions of separation
logic. In general, the tools address fragments of Java or C, and completely or partially automate the
discharge of the proof obligations. Our paper is accompanied with an implementation in Coq as a
shallow embedding. Hence, Coq plays a dual role for us: it’s a framework for mechanizing proofs,
but also a concurrent programming language. The high-level difference from the automated tools
is, or course, that proofs are developed interactively. The scaling of the proving effort is achieved
by the reuse of programs and proofs, enabled by the compositional nature of the underlying type
theory. We haven’t explored automation yet, but the minimalistic nature of our setting suggests
that the underlying abstractions will be useful for both interactive and automated reasoning.
   FCSL. The current paper adds to FCSL [Nanevski et al. 2014] the novel notions of resource
morphism, and significantly modifies the notion of resources. In FCSL, each concurrent resource is a
finite map from labels (natural numbers) to sub-components. For example, using the concepts from
Section 2, one could represent SC as a finite map l 1 Z⇒ Spin ⊎ l 2 Z⇒ Counter, where l 1 and l 2 are
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                        27


labels identifying Spin and Counter, respectively. This approach provides interesting equations on
resources; for example, one can freely rearrange the finite map components by using commutativity
and associativity of disjoint union ⊎. However, it also complicates mechanized proofs, because one
frequently, and tediously, needs to show that a label is in the domain of a map, before extracting
the labeled component. In the current work, states aren’t maps, but triples which are combined by
a form of pairing (e.g., the PCM of SC is a product of PCMs of Spin and Counter). Consequently, if
we changed the definition of SC in Section 2 into SC′ by commuting Spin and Counter throughout
the construction, then SC and SC′ wouldn’t be equal resources, but they will be isomorphic, in that
we could exhibit cancelling morphisms between the two. But this requires first having a notion of
morphism, which is one of the technical contributions of this paper. FCSL supported quiescence
by means of a dedicated and very complex inference rule, whereas Section 5 demonstrates that
quiescence is merely an application of morphism families.

7   CONCLUSIONS
This paper develops novel notions of resource morphisms and associated simulations, as key
mathematical concepts that underpin a separation logic for fine-grained concurrency. This is a
natural development, as structures in mathematics are always associated with an appropriate notion
of morphism, and simulations are the invariants that the morphisms preserve. Morphisms and
simulations act on programs, and are integrated into separation logic via a single inference rule
that propagates the simulation from the precondition to the postcondition of the morphed program.
   Morphisms compose and can support different constructions and applications. One application
is abstract atomicity, whereby a general spec, such as the one for lock in Section 2, is specialized
to a specific ownership discipline, e.g., exclusive locking in Section 4. Other applications include
the managing of scope of ghost state in quiescent environments, as illustrated in Section 5, and
restricting the state space of a resource with additional state and PCM invariants, as used in
Section 4.

ACKNOWLEDGMENTS
We thank Jesús Domínguez, Constantin Enea, František Farka, Joakim Öhman, Exequiel Rivas Gadda,
Mihaela Sighireanu, Ana Sokolova, Gordon Stewart, Anton Trunov and Nikita Zyuzin for their
comments on the various drafts of the paper. We thank the anonymous reviewers from OOPSLA’19
PC and AEC for their feedback. This research was partially supported by the Spanish MICINN
projects BOSCO (PGC2018-102210-B-I00) and TRACES (TIN2015-67522-C3-3-R), the European
Research Council projects Mathador (ERC2016-COG-724464) and FOVEDIS (ERC2015-STG-678177),
and the US National Science Foundation (NSF). Any opinions, findings, and conclusions or recom-
mendations expressed in the material are those of the authors and do not necessarily reflect the
views of the funding agencies.

REFERENCES
Martín Abadi and Leslie Lamport. 1991. The existence of refinement mappings. Theoretical Computer Science (TCS) 82, 2
   (1991), 253–284. https://doi.org/10.1016/0304-3975(91)90224-P
Afshin Amighi, Marieke Huisman, and Stefan Blom. 2018. Verification of shared-reading synchronisers. In International
   Workshop on Methods and Tools for Rigorous System Design (MeTRiD@ETAPS). 107–120. https://doi.org/10.4204/eptcs.272.9
James Aspnes, Maurice Herlihy, and Nir Shavit. 1994. Counting Networks. J. ACM 41, 5 (1994), 1020–1048. https:
   //doi.org/10.1145/185675.185815
Bruno Barras and Bruno Bernardo. 2008. The Implicit Calculus of Constructions as a Programming Language with Dependent
   Types. In International Conference on Foundations of Software Science and Computation Structures (FoSSaCS). 365–379.
   https://doi.org/10.1007/978-3-540-78499-9_26
28                             Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


Yves Bertot and Pierre Castéran. 2004. Interactive theorem proving and program development. Coq’Art: The Calculus of
    Inductive Constructions. Springer Verlag.
Stefan Blom and Marieke Huisman. 2014. The VerCors tool for verification of concurrent programs. In International
    Symposium on Formal Methods (FM) (LNCS), Vol. 8442. 127–131. https://doi.org/10.1007/978-3-319-06410-9_9
Richard Bornat, Cristiano Calcagno, Peter W. O’Hearn, and Matthew J. Parkinson. 2005. Permission accounting in separation
    logic. In ACM Symposium on Principles of Programming Languages (POPL). 259–270. https://doi.org/10.1145/1040305.
    1040327
Ahmed Bouajjani, Michael Emmi, Constantin Enea, and Suha Orhun Mutluergil. 2017. Proving linearizability using forward
    simulations. In Computer Aided Verification (CAV). 542–563. https://doi.org/10.1007/978-3-319-63390-9_28
Stephen Brookes. 2007. A semantics for concurrent separation logic. Theoretical Computer Science (TCS) 375, 1-3 (2007),
    227–270. https://doi.org/10.1016/j.tcs.2006.12.034
Andrea Cerone, Alexey Gotsman, and Hongseok Yang. 2014. Parameterised linearisability. In International Colloquium on
    Automata, Languages and Programming (ICALP). 98–109. https://doi.org/10.1007/978-3-662-43951-7_9
P. J. Courtois, F. Heymans, and D. L. Parnas. 1971. Concurrent control with "readers" and "writers". Commun. ACM 14, 10
    (1971), 667–668. https://doi.org/10.1145/362759.362813
Pedro da Rocha Pinto, Thomas Dinsdale-Young, and Philippa Gardner. 2014. TaDA: A logic for time and data abstraction. In
    European Conference on Object-Oriented Programming (ECOOP). 207–231. https://doi.org/10.1007/978-3-662-44202-9_9
Luca de Alfaro and Thomas A. Henzinger. 2001. Interface Automata. ACM Software Engineering Notes (SEN) 26, 5 (2001),
    109–120. https://doi.org/10.1145/503271.503226
Germán Andrés Delbianco, Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2017. Concurrent data structures
    linked in time. In European Conference on Object-Oriented Programming (ECOOP). 8:1–8:30. https://doi.org/10.4230/
    LIPIcs.ECOOP.2017.8
John Derrick, Gerhard Schellhorn, and Heike Wehrheim. 2011. Mechanically verified proof obligations for linearizability.
    ACM Transactions on Programming Languages and Systems (TOPLAS) 33, 1 (2011), 4:1–4:43. https://doi.org/10.1145/
    1889997.1890001
Thomas Dinsdale-Young, Mike Dodds, Philippa Gardner, Matthew J. Parkinson, and Viktor Vafeiadis. 2010. Concurrent
    abstract predicates. In European Conference on Object-Oriented Programming (ECOOP). 504–528. https://doi.org/10.1007/
    978-3-642-14107-2_24
Ivana Filipović, Peter W. O’Hearn, Noam Rinetzky, and Hongseok Yang. 2010a. Abstraction for concurrent objects. Theoretical
    Computer Science (TCS) 411, 51–52 (2010), 4379–4398. https://doi.org/10.1016/j.tcs.2010.09.021
Ivana Filipović, Peter W. O’Hearn, Noah Torp-Smith, and Hongseok Yang. 2010b. Blaming the client: on data refinement in
    the presence of pointers. Formal Aspects of Computing 22, 5 (2010), 547–583. https://doi.org/10.1007/s00165-009-0125-8
Dan Frumin, Robbert Krebbers, and Lars Birkedal. 2018. ReLoC: a mechanised relational logic for fine-grained concurrency.
    In IEEE Symposium on Logic in Computer Science (LICS). 442–451. https://doi.org/10.1145/3209108.3209174
Gaëtan Gilbert, Jesper Cockx, Matthieu Sozeau, and Nicolas Tabareau. 2019. Definitional proof-irrelevance without K.
    PACMPL 3, POPL (2019), 3:1–3:28. https://doi.org/10.1145/3290316
Abraham Ginzburg. 1968. Algebraic Theory of Automata. Academic Press. https://doi.org/10.1016/b978-1-4832-0016-
    3.50006-8
Alexey Gotsman and Hongseok Yang. 2012. Linearizability with ownership transfer. In International Conference on
    Concurrency Theory (CONCUR). 256–271. https://doi.org/10.1007/978-3-642-32940-1_19
Ronghui Gu, Jérémie Koenig, Tahina Ramananandro, Zhong Shao, Xiongnan (Newman) Wu, Shu-Chun Weng, Haozhong
    Zhang, and Yu Guo. 2015. Deep specifications and certified abstraction layers. In ACM Symposium on Principles of
    Programming Languages (POPL). 595–608. https://doi.org/10.1145/2676726.2676975
Ronghui Gu, Zhong Shao, Jieung Kim, Xiongnan (Newman) Wu, Jérémie Koenig, Vilhelm Sjöberg, Hao Chen, David
    Costanzo, and Tahina Ramananandro. 2018. Certified concurrent abstraction layers. In ACM Conference on Programming
    Languages Design and Implementation (PLDI). 646–661. https://doi.org/10.1145/3192366.3192381
Ichiro Hasuo, Chris Heunen, Bart Jacobs, and Ana Sokolova. 2009. Coalgebraic Components in a Many-Sorted Microcosm.
    In Algebra and Coalgebra in Computer Science. 64–80. https://doi.org/10.1007/978-3-642-03741-2_6
Danny Hendler, Itai Incze, Nir Shavit, and Moran Tzafrir. 2010. Flat combining and the synchronization-parallelism tradeoff. In
    ACM Symposium on Parallelism in Algorithms and Architectures (SPAA). 355–364. https://doi.org/10.1145/1810479.1810540
Thomas A. Henzinger, Ali Sezgin, and Viktor Vafeiadis. 2013. Aspect-oriented linearizability proofs. In International
    Conference on Concurrency Theory (CONCUR). 242–256. https://doi.org/10.1007/978-3-642-40184-8_18
Maurice Herlihy and Nir Shavit. 2008. The art of multiprocessor programming. M. Kaufmann. https://doi.org/10.1108/
    03684920810907904
Maurice Herlihy and Jeannette M. Wing. 1990. Linearizability: a correctness condition for concurrent objects. ACM
    Transactions on Computer Systems (TOCS) 12, 3 (1990), 463–492. https://doi.org/10.1145/78969.78972
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                            29


C. A. R. Hoare. 1972. Towards a theory of parallel programming. In Operating Systems Techniques. 61–71. https:
   //doi.org/10.1007/978-1-4612-6315-9_16
Bart Jacobs. 2016. Introduction to coalgebra: towards mathematics of states and observation. Cambridge University Press.
   https://doi.org/10.1017/cbo9781316823187
Bart Jacobs and Frank Piessens. 2011. Expressive modular fine-grained concurrency specification. In ACM Symposium on
   Principles of Programming Languages (POPL). 271–282. https://doi.org/10.1145/1925844.1926417
Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: a
   powerful, sound, predictable, fast verifier for C and Java. In Proceedings of the Third International Symposium on NASA
   Formal Methods (NFM 2011). https://doi.org/10.1007/978-3-642-20398-5_4
Radha Jagadeesan and James Riely. 2014. Between linearizability and quiescent consistency - quantitative quiescent
   consistency. In International Colloquium on Automata, Languages and Programming (ICALP). 220–231. https://doi.org/10.
   1007/978-3-662-43951-7_19
Cliff B. Jones. 1983. Tentative Steps Toward a Development Method for Interfering Programs. ACM Trans. Comput. Syst. 5, 4
   (1983). https://doi.org/10.1145/69575.69577
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the ground
   up: A modular foundation for higher-order concurrent separation logic. Journal of Functional Programming (JFP) 28
   (2018), e20. https://doi.org/10.1017/S0956796818000151
Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
   monoids and invariants as an orthogonal basis for concurrent reasoning. In ACM Symposium on Principles of Programming
   Languages (POPL). 637–650. https://doi.org/10.1145/2676726.2676980
Artem Khyzha, Mike Dodds, Alexey Gotsman, and Matthew J. Parkinson. 2017. Proving linearizability using partial orders.
   In European Symposium on Programming (ESOP). 639–667. https://doi.org/10.1007/978-3-662-54434-1_24
Ruy Ley-Wild and Aleksandar Nanevski. 2013. Subjective auxiliary state for coarse-grained concurrency. In ACM Symposium
   on Principles of Programming Languages (POPL). 561–574. https://doi.org/10.1145/2429069.2429134
Hongjin Liang and Xinyu Feng. 2013. Modular verification of linearizability with non-fixed linearization points. In ACM
   Conference on Programming Languages Design and Implementation (PLDI). 459–470. https://doi.org/10.1145/2499370.
   2462189
Hongjin Liang and Xinyu Feng. 2018. Progress of concurrent objects with partial methods. In ACM Symposium on Principles
   of Programming Languages (POPL). 20:1–20:31. https://doi.org/10.1145/3158108
Hongjin Liang, Xinyu Feng, and Ming Fu. 2012. A rely-guarantee-based simulation for verifying concurrent program
   transformations. In ACM Symposium on Principles of Programming Languages (POPL). 455–468. https://doi.org/10.1145/
   2103656.2103711
Hongjin Liang, Xinyu Feng, and Zhong Shao. 2014. Compositional verification of termination-preserving refinement of
   concurrent programs. In IEEE Symposium on Logic in Computer Science (LICS). 65:1–65:10. https://doi.org/10.1145/
   2603088.2603123
Nancy A. Lynch and Frits W. Vaandrager. 1995. Forward and Backward Simulations: I. Untimed Systems. Inf. Comput. 121, 2
   (1995), 214–233. https://doi.org/10.1006/inco.1995.1134
John M. Mellor-Crummey and Michael L. Scott. 1991. Algorithms for Scalable Synchronization on Shared-memory
   Multiprocessors. ACM Transactions on Computer Systems (TOCS) 9, 1 (1991), 21–65. https://doi.org/10.1145/103727.103729
Robin Milner. 1978. A theory of type polymorphism in programming. J. Comput. System Sci. 17 (1978), 348–375. https:
   //doi.org/10.1016/0022-0000(78)90014-4
P. Müller, M. Schwerhoff, and A. J. Summers. 2016. Viper: a verification infrastructure for permission-based reasoning. In
   Verification, Model Checking, and Abstract Interpretation (VMCAI) (LNCS), Vol. 9583. 41–62. https://doi.org/10.1007/978-
   3-662-49122-5_2
Aleksandar Nanevski. 2016. Separation Logic and Concurrency. Lecture Notes for the Oregon Programming Languages
   Summer School (OPLSS). https://www.cs.uoregon.edu/research/summerschool/summer16/curriculum.php
Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas. 2019. Specifying Concurrent
   Programs in Separation Logic: Morphisms and Simulations. (2019). https://doi.org/10.5281/zenodo.3365991 Artifact
   including Coq source code.
Aleksandar Nanevski, Ruy Ley-Wild, Ilya Sergey, and Germán Andrés Delbianco. 2014. Communicating state transition
   systems for fine-grained concurrent resources. In European Symposium on Programming (ESOP). 290–310. https:
   //doi.org/10.1007/978-3-642-54833-8_16
Aleksandar Nanevski, Greg Morrisett, and Lars Birkedal. 2006. Polymorphism and separation in Hoare Type Theory.
   In Proceedings of the 11th ACM SIGPLAN International Conference on Functional Programming (ICFP 2006). https:
   //doi.org/10.1145/1159803.1159812
Aleksandar Nanevski, Greg Morrisett, Avi Shinnar, Paul Govereau, and Lars Birkedal. 2008. Ynot: Dependent Types for
   Imperative Programs. In Proceeding of the 13th ACM SIGPLAN International Conference on Functional Programming
30                              Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


    (ICFP 2008). https://doi.org/10.1145/1411204.1411237
Peter W. O’Hearn. 2007. Resources, concurrency, and local reasoning. Theoretical Computer Science (TCS) 375, 1-3 (2007).
    https://doi.org/10.1016/j.tcs.2006.12.035
Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data Structures.
    In Conference of the European Association for Computer Science Logic (CSL). 1–19. https://doi.org/10.1007/3-540-44802-0_1
Susan S. Owicki and David Gries. 1976. Verifying properties of parallel programs: an axiomatic approach. Commun. ACM
    19, 5 (1976), 279–285. https://doi.org/10.1145/360051.360224
Frank Pfenning. 2001. Intensionality, Extensionality, and Proof Irrelevance in Modal Type Theory. In IEEE Symposium on
    Logic in Computer Science (LICS). 221–230. https://doi.org/10.1109/lics.2001.932499
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings of the 17th IEEE
    Symposium on Logic in Computer Science (LICS 2002). https://doi.org/10.1109/LICS.2002.1029817
J.J.M.M. Rutten. 2000. Universal coalgebra: a theory of systems. Theoretical Computer Science 249, 1 (2000), 3 – 80.
    https://doi.org/10.1016/s0304-3975(00)00056-6
Gerhard Schellhorn, Heike Wehrheim, and John Derrick. 2012. How to prove algorithms linearisable. In Computer Aided
    Verification (CAV). 243–259. https://doi.org/10.1007/978-3-642-31424-7_21
Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2015a. Mechanized Verification of Fine-grained Concurrent
    Programs. In ACM Conference on Programming Languages Design and Implementation (PLDI). https://doi.org/10.1145/
    2737924.2737964
Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2015b. Specifying and verifying concurrent algorithms with
    histories and subjectivity. In European Symposium on Programming (ESOP). 333–358. https://doi.org/10.1007/978-3-662-
    46669-8_14
Ilya Sergey, Aleksandar Nanevski, Anindya Banerjee, and Germán Andrés Delbianco. 2016. Hoare-style specifications as
    correctness conditions for non-linearizable concurrent objects. In ACM Conference on Object-Oriented Programming
    Systems, Languages, and Applications (OOPSLA). 92–110. https://doi.org/10.1145/3022671.2983999
Ilya Sergey, James R. Wilcox, and Zachary Tatlock. 2018. Programming and proving with distributed protocols. In ACM
    Symposium on Principles of Programming Languages (POPL). 28:1–28:30. https://doi.org/10.1145/3158116
Kasper Svendsen and Lars Birkedal. 2014. Impredicative concurrent abstract predicates. In European Symposium on
    Programming (ESOP). 149–168. https://doi.org/10.1007/978-3-642-54833-8_9
Kasper Svendsen, Lars Birkedal, and Aleksandar Nanevski. 2011. Partiality, State and Dependent Types. In International
    Conference on Typed Lambda Calculi and Applications (TLCA). 198–212. https://doi.org/10.1007/978-3-642-21691-6_17
Kasper Svendsen, Lars Birkedal, and Matthew J. Parkinson. 2013. Modular reasoning about separation of concurrent data
    structures. In European Symposium on Programming (ESOP). 169–188. https://doi.org/10.1007/978-3-642-37036-6_11
The Coq Development Team. 2019. The Coq Proof Assistant Reference Manual - Version V8.10+beta2. https://coq.github.io/
    doc/V8.10+beta2/refman/.
R. Kent Treiber. 1986. Systems programming: coping with parallelism. Technical Report RJ 5118. IBM Almaden Research
    Center.
Aaron Turon, Derek Dreyer, and Lars Birkedal. 2013. Unifying refinement and Hoare-style reasoning in a logic for higher-
    order concurrency. In ACM International Conference on Functional Programming (ICFP). 377–390. https://doi.org/10.1145/
    2544174.2500600


A    PCM PRODUCTS, TRANSITION COUPLINGS AND RESOURCE COMBINATIONS
In this section we develop the combination of two resources (the combined resource or tensor
resource) that has been used in Sections 2 and 4. For that, we need first to give some basic definitions
for the product of PCMs and the coupling of transitions.
   Lemma A.1. Let A and B be PCMs. Then, the Cartesian product A × B is a PCM under the point-wise
lifting of the join operators, (a 1 , b1 ) •A×B (a 2 , b2 ) = (a 1 •A a 2 , b1 •B b2 ), and units, 1A×B = (1A , 1B ).
  For example, the PCM for SC in Figure 3 is the product of the PCMs M (Spin) and M (Counter),
that is, M (SC) = M (Spin) × M (CSLX).
  Definition A.2. Let si = (ais , aij , aoi ) be an (Mi ,Ti )-state, i = 1, 2, and s = (as , a j , ao ) be an
(M 1 × M 2 ,T1 × T2 )-state. The pair state of s 1 and s 2 is [s 1 , s 2 ] b    = ((as1 , as2 ), (a 1j , a 2j ), (ao1 , ao2 )), and
projection states of s are s\i b      = (as \i, a j \i, ao \i), i = 1, 2. The usual beta and eta laws for products
hold, i.e.: [s 1 , s 2 ]\i = si and s = [s\1, s\2].
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                               31


    Definition A.3. Given state spaces Σ1 and Σ2 , the product state space Σ1 × Σ2 is defined by:
                                    ⌜s⌝        =
                                               b     ⌜s\1⌝ Σ1 • ⌜s\2⌝ Σ2
                            s ∈ Σ1 × Σ2        iff   s\1 ∈ Σ1 ∧ s\2 ∈ Σ2 ∧ defined ⌜s⌝.
  Definition A.4. Let ti be a Σi -transition, i = 1, 2. The coupling of t 1 and t 2 is the Σ1 ×Σ2 -transition
defined as (t 1 ▷◁ t 2 ) s s ′ b
                               = t 1 (s\1) (s ′\1) ∧ t 2 (s\2) (s ′\2) 22 .
   The coupling of transitions is used extensively in our constructions, e.g. in lock_tr ▷◁ open_tr
in Section 2. As we have already explained there, the formalization in Definition A.4 entails that
the coupling of two transitions execute their components simultaneously: lock_tr from Spin and
open_tr from Counter in the aforementioned example.
   Now we can formalize the notion of combined resource, which the next definition makes precise.
  Definition A.5. Let V , W be resources, I ⊆ ∆(V ) × ∆(W ) a relation between transitions, such that
for every (tv , tw ) ∈ I the transition tv ▷◁ tw is footprint-preserving. The combined (alt. tensor)
resource V ⊗I W has the state space Σ (V ⊗I W ) = Σ (V ) × Σ (W ) and transitions:
                                       ∆ (V ⊗I W ) = {tv ▷◁ tw | (tv , tw ) ∈ I }
    For example, resource SC is the combination of resources Spin and Counter, with I defined as:
                        I = {(lock_tr, open_tr), (unlock_tr, close_tr), (id_tr, id_tr)}
Here, id is the idle transition defined as λs s ′ . s ′ = s. We have implicitly assumed that all resources
in this paper possess an idle transition, which is why we elided this transition from all the figures.

B    SUB-PCMS, COMPATIBILITY RELATIONS, AND PCM MORPHISMS
In Section 4, we implicitly used a construction to restrict the state space of the resource CSL′ with
an invariant Inv, to obtain the desired resource CSL. In this section, we formally develop that
construction, which hinges on the concept of sub-PCMs. A sub-PCM is to a PCM, what subset is to
a set. It is customary in abstract algebra to develop the notion of a sub-object of an algebraic object
by first developing the appropriate notion of morphism on the objects; in our case, this will be PCM
morphisms. The morphisms will model the injection of a sub-PCM into the PCM (similar to how
one can inject a subset into a larger set), and a retraction from the larger PCM into the sub-PCM.
   Compatibility relation. We start with the auxiliary notion of a compatibility relation, which
enables us to delineate the elements of the larger PCM that we want to include into the sub-PCM.
Interestingly, compatibility relations are binary relations, rather than simple unary predicates
over the domain of the larger PCM. This is so, because the sub-PCM construction requires not
only selecting the elements out of the larger PCM, but also restricting its join operation, i.e.,
make it ever more partial than it already is. As the join operation is itself binary, so must be
the compatibility relation. One may thus think of the compatibility relation as being an abstract
algebraic generalization of the idea of disjointness (and indeed, disjointness of histories and heaps
are instances of compatibility relations on the PCMs of histories and heaps, respectively).
    Definition B.1. Given a PCM A, relation R on A is a compatibility relation if it is:
    (1) (unitary) 1A R 1A
    (2) (commutative) x R y iff y R x
    (3) (compatible) if x R y then x ⊥ y
22 In this paper we only consider footprint preserving transitions. In Coq code we consider more general notions of transitions

which need not be footprint preserving. For that case, we somewhat modify the definition of coupling to require an additional
conjunct that ⌜s ′ ⌝ is a defined heap, similar to the definition of product state spaces.
32                          Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


     (4) (unital) if x R y then x R 1A
     (5) (associative) if x R y and (x • y) R z then x R (y • z) and y R z
     For example, the relation ⊥ω defined in Section 4 in clause (6) on page 20, as
                       x ⊥ω y = (ω x → last_stamp y < last_stamp x) ∧
                                (ω y → last_stamp x < last_stamp y) ∧ x ⊥ y
is a compatibility relation. The critical part of the proof is that of associativity, which we briefly
sketch. Let x, y and z be three histories such that x ⊥ω y and (x • y) ⊥ω z, and let the timestamps
of their last entries be t x , ty , and tz , respectively. The interesting case is when x or y end with a
locking entry. Without loss of generality, let ω x hold, and thus last_op x = L. Then, by x ⊥ω y, the
last entry of y must be U, and ty < t x . Similarly, by (x • y) ⊥ω z, the last entry of z must be U and
tz < t x . But then, trivially, y ⊥ω z, because both y and z end with an U entry. Similarly, x ⊥ω (y • z),
because y • z also ends with an U entry, and its last timestamp is max(ty , tz ) ≤ ty , tz < t x .
   The clauses (4) and (5) in Section 4 also arise as instances of compatibility relations, in a similar
way. Thus, ultimately, the invariant Inv = (4) ∧ (5) ∧ (6) can be defined as a compatibility relation
on the PCM M (CSL′).
     PCM morphisms. Now we can define morphisms between PCMs as follows:
  Definition B.2. A PCM morphism ϕ : A → B with a compatibility relation ⊥ϕ is a partial
function from A to B such that:
  (1) ϕ 1A = 1B
  (2) if x ⊥ϕ y, then ϕ x, ϕ y exist, and ϕ x ⊥B ϕ y, and ϕ (x • y) = ϕ x • ϕ y
The morphism ϕ is total if ⊥ϕ equals ⊥A .
   In Section 4 we have silently used many PCM morphisms, as the special symbols that we used
to name the components such as π , τ , µ, σ , etc., are all PCM morphisms. For example, τ and π
in Figure 9 are projections out of the PCM M (Spin) into the PCM of histories and permissions,
respectively (and projections out of tuples are morphisms). Then, τs s and τo s are abbreviations for
τ (as s) and τ (ao s) respectively, and similarly for π .
     sub-PCMs. We can now define the notion of sub-PCMs as follows:
   Definition B.3. PCM A is a sub-PCM of a PCM B if there exists a total PCM morphism ι : A → B
(injection) and a morphism ρ : B → A (retraction), such that:
   (1) ρ (ι a) = a
   (2) if b ⊥ρ 1B then ι (ρ b) = b
   (3) if (ρ x) ⊥A (ρ y) then x ⊥ρ y
   Property (1) says that ι is injective, i.e., if we coerce a ∈ A into ι a, we can recover a back by ρ,
since no other element of A maps by ι into ι a. The dual property (2) allows the same for a subset
of B’s elements, that are related by ⊥ρ to 1B . Hence, intuitively, A is in 1-1 correspondence with
that subset of B. Property (3) extends the correspondence to compatibility relations, i.e., ⊥A , when
considered on images under ρ, implies (and hence, by properties of morphisms, equals) ⊥ρ .
   Definition B.3 says what it means for A to be a sub-PCM of B. The following lemma shows how
to construct a sub-PCM of B given a compatibility relation R on B. We used this construction in
Section 4 to obtain the PCM for the resource CSL out of the PCM M (CSL′).
   Lemma B.4. Given PCM A and compatibility relation R on A, the set A/R = {x ∈ A | x R 1A } forms
a PCM under unit 1A , and join operation defined as x •A/R y = x •A y if x R y and undefined otherwise.
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                      33


The PCM A/R is a sub-PCM of A under the injection ι and retraction ρ defined as ∀x ∈ A/R. ι (x) = x
and ∀a ∈ A. ρ (a) = a if a R 1A , and ρ (a) undefined otherwise. Moreover, R = ⊥ρ = ⊥A/R .
  Using the above notation, the PCM of the resource CSL can be defined formally as M (CSL′)/Inv.
  We now have all the ingredients to formalizing the construction for restricting a resource that
we set out to define.
   Definition B.5. Let R be an invariant compatibility relation on M (V ). The sub-resource V /R is
defined with the same type, transitions and erasure as V , but with the PCM and the state space
defined as
   (1) M (V /R) = M (V )/R
   (2) s ∈ Σ (V /R) iff s ∈ Σ (V ) ∧ (as s) R (ao s)
There is a generic resource morphism ι : V → V /R that is inclusion on states and identity on
transitions.
  For example, the resource CSL from Section 4 is the sub-resource of CSL′ taken under the
invariant Inv, and the resource morphism ι : CSL′ → CSL from Section 4 (page 20), is the generic
morphism defined above.
   Algebraic properties. We finish this section by providing some additional evidence that compat-
ibility relations and PCM morphisms compose, and have pleasant mathematical properties. For
example, the operations of morphism composition and join come with the compatibility relations
as follows.
             (f ◦ д) (x) b
                         = f (д x)    x ⊥f ◦д y b
                                                = x ⊥д y ∧ д x ⊥f д y
             (f • д) (x) b
                         = f x • д x x ⊥f •д y b= x ⊥f y ∧ x ⊥д y ∧ f (x • y) ⊥ д (x • y)
Or, given PCM morphisms f and д, we can define compatibility relation that implements the PCM
versions of the algebraic notions of kernel (preimages of unit) and equalizer (values on which two
morphisms agree), as follows.
                          x (ker f ) y b
                                       = x ⊥f y ∧ f x = f y = 1
                        x (eql f д) y b= x ⊥f y ∧ x ⊥д y ∧ f x = д x ∧ f y = д y
Importantly, the above are all compatibility relations, as we have proved in the Coq files. Similarly,
we can restrict a morphism to a compatibility relation R, to define another PCM morphism.
                          f x,         if x R 1
                       
                     =
          (f /R) (x) b                                  with x ⊥f /R y b= x ⊥f y ∧ x R y
                          undefined, otherwise
The import of the above abstract constructions is in the reduction of proof burden. For example,
a morphism equalizer is a compatibility relation by construction, so the user need not bother
proving compatibility for equalizers. The constructions also combine to concisely state invariants
and assertions. For example, the compatibility relation that gives rise to Inv, and is thus used
to construct the sub-resource CSL, may be defined as the equalizer eql (π • α) (ω ′ ◦ τ ), where
ω ′ : hist → O is the morphism defined on a history h as ω ′ h = if ω h then own else own.

C   INDEXED MORPHISM FAMILIES
In this appendix, we show how the definitions of morphism and f -simulations generalize to indexed
families. When X is the unit type, we recover the morphism-related definitions from Section 3.
                                                                         X
  Definition C.1. An indexed family of morphisms f : V → W (or just family), consists of
partial functions f Σ : X → Σ (W ) ⇀ Σ (V ) (note the contravariance), and f ∆ : X → ∆ (V ) ⇀ ∆ (W )
on transitions, such that:
34                              Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


     (1) (locality of f Σ ) there exits a function f A : M (W ) → M (V ) such that if f Σ x (sw  p) = sv ,
         then sv = sv′  f A (p), and f Σ x (sw  p) = sv′  f A (p).
     (2) (locality of f ∆ ) if f ∆ x (sw  p) t = t ′, then f ∆ x (sw  p) t = t ′.
     (3) (other-fixity) if ao (sw ) = ao (sw′ ) and f Σ x sw , f Σ x ′ sw′ exist, then ao (f Σ x sw ) = ao (f Σ x ′sw′ ).
     (4) (injectivity on indices) if f Σ x 1 sw 1 and f Σ x 2 sw 2 exist and f Σ x 1 sw 1 = f Σ x 2 sw 2 , then x 1 = x 2 .
  In most of the properties of Definition C.1, the index x is simply propagated unchanged. The
only property where x is significant is the new property (4), which requires that f Σ x sw uniquely
determines the index x. In the Stack example in Section 5, it is easy to see that the definition of f Σ
satisfies this property, because equal states have equal histories.
                                                                  X
  Definition C.2. Given a morphism family f : V → W , an f -simulation is a predicate I on X
and W -states such that:
  (1) if I x sw , and f Σ x sw = sv , and t sv sv′ , then there exist x ′, t ′ = f ∆ x sw t, and sw′ such that
      I x ′ sw′ and f Σ x ′ sw′ = sv′ , and t ′ sw sw′ .
  (2) if I x sw , and sv = f Σ x sw exists, and sw −→∗ sw′ , then I x sw′ , and sv′ = f Σ x sw′ exists, and
                                                              W
         sv −→∗ sv′ .
              V

  Compared to Definition 3.11, property (1) allows that x changes into x ′ by a transition. In the
Stack example in Section 5, if we lift e by using the index x = empty (i.e., write morph empty f e),
then this index will evolve with e taking the transitions of Stack to track how e changes the self
history by adding the entries for pushing 1 and 2. In property (2), the index x simply propagates.

D      DENOTATIONAL SEMANTICS
Our semantic model largely relies on the denotational semantic of action trees [Ley-Wild and
Nanevski 2013]. A tree implements a finite partial approximation of one execution of a program.
Thus, a program of type ST V A will be denoted by a set of such trees. The set may be infinite,
as some behaviors (i.e., infinite loops) can only be represented as an infinite set of converging
approximated executions. Because a program may contain multiple executions, our denotational
semantics can represent non-determinism in the form of internal choice, though our language
currently does not make use of that feature.
   An action tree is a generalization of the Brookes’ notion of action trace [Brookes 2007] in the
following sense. Where action trace semantics represent a program by a set of traces, we represent
a program with a set of trees. A tree differs from a trace in that a trace is a sequence of actions
and their results, whereas a tree contains an action followed by a continuation which itself is a tree
parametrized wrt. the output of the action.
   In this appendix, we first define the denotation of each of our commands as a set of trees. Then
we define the semantic behavior for trees wrt. resource states, in a form of operational semantics
for trees, thus formalizing single execution of a program. Then we relate this low-level operational
semantics of trees to high-level transitions of a resource by an always predicate (Section D.3) that
ensures that a tree is resilient to any amount of interference, and that all the operational steps by a
tree are safe. The always predicate will be instrumental in defining the vrf-predicate transformer
from Section 3, and from there, in defining the type of Hoare triples {P } A {Q }@V . Both the ST V A
type and the Hoare triple type will be complete lattices of sets of trees, giving us a suitable setting
for modeling recursion. The soundness of FCSL follows from showing that the lemmas about the
vrf predicate transformer listed in Section 3, are satisfied by the denotations of the commands.
   We choose the Calculus of Inductive Constructions (CiC) [Bertot and Castéran 2004; The Coq
Development Team 2019] as our meta logic. This has several important benefits. First, we can
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                       35


define a shallow embedding of our system into CiC that allows us to program and prove directly
with the semantic objects, thus immediately lifting to a full-blown programming language and
verification system with higher-order functions, abstract types, abstract predicates, and a module
system. We also gain a powerful dependently-typed λ-calculus, which we use to formalize all
semantic definitions and meta theory, including the definition of action trees by iterated inductive
definitions [The Coq Development Team 2019], specification-level functions, and programming-
level higher-order procedures. Finally, we were able to mechanize the entire semantics and meta
theory in the Coq proof assistant implementation of CiC.

D.1    Action trees and program denotations
   Definition D.1 (Action trees). The type tree V A of (A-returning) action trees is defined by the
following iterated inductive definition.
                           tree V A b
                                    = Unfinished
                                    | Ret (v : A)
                                    | Act (a : action V A)
                                    | Seq (T : tree V B) (K : B → tree V A)
                                    | Par (T1 : tree V B 1 ) (T2 : tree V B 2 )
                                           (K : B 1 × B 2 → tree V A)
                                                         X
                                        | Morph (f : W → V ) (x : X ) (T : tree W A)
  Most of the constructors in Definition D.1 are self-explanatory. Since trees have finite depth,
they can only approximate potentially infinite computations, thus the Unfinished tree indicates an
incomplete approximation. Ret v is a terminal computation that returns value v : A. The constructor
Act takes as a parameter an action a : action V A, as defined in Section 3. Seq T K sequentially
composes a B-returning tree T with a continuation K that takes T ’s return value and generates
the rest of the approximation. Par T1 T2 K is the parallel composition of trees T1 and T2 , and a
continuation K that takes the pair of their results when they join. CiC’s iterated inductive definition
permits the recursive occurrences of tree to be nonuniform (e.g., tree Bi in Par) and nested (e.g.,
the positive occurrence of tree A in the continuation). Since the CiC function space includes case-
analysis, the continuation may branch upon the argument. The Morph constructor embeds an
                                    X
index x : X , morphism f : W → V , and tree T : tree W A for the underlying computation. The
constructor will denote T should be executed so that each of its actions is modified by f with an
index x. We can now define the denotational model of our programs; that is the type ST V A of sets
of trees, containing Unfinished.
                             ST V A b
                                    = {e : set (tree V A) | Unfinished ∈ e}
  The denotations of the various constructors combine the trees of the individual denotations, as
shown below.
                            ret (r : A) b
                                        = {Unfinished, Ret r }
                           x ← e1 ; e2 b= {Unfinished} ∪
                                              {Seq T1 K | T1 ∈ e 1 ∧ ∀x . K x ∈ e 2 }
                               e1 ∥ e2 b= {Unfinished} ∪
                                              {Par T1 T2 Ret | T1 ∈ e 1 ∧ T2 ∈ e 2 }
                                        = {Unfinished, Act a}
                                    ⟨a⟩ b
                          morph f x e b = {Unfinished} ∪ {Morph f x T | T ∈ e}
The denotation of ret simply contains the trivial Ret tree, in addition to Unfinished, and similarly
in the case of ⟨a⟩. The trees for sequential composition of e 1 and e 2 are obtained by pairing up the
trees from e 1 with those from e 2 using the Seq constructor, and similarly for parallel composition
and morphism application.
36                              Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


                                                     unwind_act ∆ x̄ x̄ ′ a s s ′ v
                                                                 ChoiceAct
                                           ∆ ⊢ x̄, s, Act a −−−−−−−−→ x̄ ′, s ′ ; Ret v

                                                                                                        π
                                                                                       ∆ ⊢ x̄, s,T −→ x̄, s ′,T ′
                                       SeqRet                                                       SeqStep π
          ∆ ⊢ x̄, s, Seq (Ret v) K −−−−−−→ x̄, s, K v                      ∆ ⊢ x̄, s, Seq T K −−−−−−−−→ x̄ ′, s ′, Seq T ′ K

                                π                                                                           π
                  ∆ ⊢ x̄, s,T1 −→ x̄ ′, s ′,T1′                                           ∆ ⊢ x̄, s,T2 −→ x̄ ′, s ′,T2′
                              ParL π                                                                    ParR π
     ∆ ⊢ x̄, s, Par T1 T2 K −−−−−−→ x̄ ′, s ′, Par T1′ T2 K                 ∆ ⊢ x̄, s, Par T1 T2 K −−−−−−→ x̄ ′, s ′, Par T1 T2′ K


                                                                              ParRet
                                ∆ ⊢ x̄, s, Par (Ret v 1 ) (Ret v 2 ) K −−−−−→ x̄, s, K (v 1 , v 2 )


                                                                            MorphRet
                                    ∆ ⊢ x̄, s, Morph f y (Ret v) −−−−−−−−→ x̄, s, Ret v

                                                                       π
                                                ∆, f ⊢ (x̄, y), s,T −→ (x̄ ′, y ′ ), s ′,T ′
                                                              MorphStep π
                               ∆ ⊢ x̄, s, Morph f y T −−−−−−−−−−−→ x̄ ′, s ′, Morph f y ′ T ′

                                       π
Fig. 12. Judgment ∆ ⊢ x̄, s,T −→ x̄ ′, s ′,T ′ , for operational semantics on trees, which reduces a tree with
respect to the path π .



   The denotations of composed programs motivate why we denote programs by non-empty sets,
i.e., why each denotation contains at least Unfinished. If we had a program Empty whose denotation
is the empty set, then the denotation of x ← Empty; e ′, Empty ∥ e ′ and morph f x Empty will all
also be empty, thus ignoring that the composed programs exhibit more behaviors. For example,
the parallel composition Empty ∥ e ′ should be able to evaluate the right component e ′, despite the
left component having no behaviors. By including Unfinished in all the denotations, we ensure
that behaviors of the components are preserved in the composition. For example, the parallel
composition {Unfinished} ∥ e ′ is denoted by the set:

                                 {Unfinished} ∪ {Par Unfinished T Ret | T ∈ e ′ }

which contains an image of each tree from e ′, thus capturing the behaviors of e ′.

D.2     Operational semantics of action trees
                                                                                                                            π
The judgment for small-step operational semantics of action trees has the form ∆ ⊢ x̄, sw ,Tv −
                                                                                              → x̄ ′, sw′ ,Tv′
(Figure 12). We explain the components of this judgment next.
   First, the component ∆ is a morphism context. This is a sequence, potentially empty, of morphism
families
                                                X0                  X1                         Xn
                                    f 0 : V1 → W , f 1 : V2 → V1 , . . . , fn : V → Vn
We say that ∆ has resource type V → W , and index type (X 0 , · · · , X n ). An empty context · has
resource type V → V for any V .
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                               37


  Second, the components x̄ and x̄ ′ are tuples, of type (X 0 , · · · , X n ), and we refer to them as indexes.
Intuitively, the morphism context records the morphisms under which a program operates. For
example, if we wrote a program of the form

                                     morph f 0 x 0 (· · · (morph fn x n e) · · · ),

it will be that the trees that comprise e execute under the morphism context f 0 , . . . , fn , with an
index tuple (x 0 , . . . , x n ).
   Third, the components sw and sw′ are W -states, and Tv ,Tv′ : tree V A, for some type A. The
meaning of the judgment is that a tree Tv , when executed in a state sw , under the context of
morphisms ∆ produces a new state sw′ and residual tree Tv′ , encoding what is left to execute. The
resource of the trees and the states disagree (the states use resource W , the trees use V ), but the
morphism context ∆ relates them as follows. Whenever the head constructor of the tree is an action,
the action will first be morphed by applying all the morphisms in ∆ in order, to the transitions that
constitute the head action, supplying along the way the projections out of x to the morphisms. This
will produce a new index x ′ and an action on W -states, which can be applied to sw to obtain sw′ .
   Fourth, the component π is of path type, identifying the position in the tree where we want to
make a reduction.

                           = ChoiceAct | SeqRet
                      path b                                 | SeqStep (π : path) |
                             ParRet    | ParL (π : path)     | ParR (π : path)    |
                             MorphRet | MorphStep (π : path)


The key are the constructors ParL π and ParR π . In a tree which is a Par tree, these constructors
identify that we want to reduce in the left and right subtree, respectively, iteratively following the
path π . If the tree is not a Par tree, then ParL and ParR constructors will not form a good path; we
define further below when a path is good for a tree. The other path constructors identify positions
in other kinds of trees. For example, ChoiceAct identifies the head position in the tree of the form
Act(a), SeqRet identifies the head position in the tree of the form Seq (Ret v) K (i.e., it identifies a
position of a beta-reduction), SeqStep π identifies a position in the tree Seq T K, if π identifies a
position within T , etc. We do not paths for trees of the form Unfinished and Ret v, because these
do not reduce.
   In order to define the operational semantics on trees, we next require a few auxiliary notions.
First, we need the relation ComSquares ∆ x̄ x̄ ′ sv sv′ tv sw sw′ tw encoding the composition of the
commutative diagrams below (each commutative diagram is an instance of Figure 3(b), for one of
the morphisms f 0 , f 1 ,. . . , fn , in the context ∆ = f 0 ; f 1 ; · · · ; fn ).

                                     f nΣ x n′                   f 0Σ x 0′
                               sv′               sn′      s 1′               sw′
                                                                        ⌞
                             tv                  tn       t1                   tw =f 0∆ x 0 sw t 1

                               sv                sn       s1                 sw
                                     f nΣ x n                    f 0Σ x 0



  The relation captures that tv is morphed by iterating the state component of the morphisms in
∆, starting from the state sw , and passing along the elements of the tuple x̄ or type (X 0 , · · · , X n ),
until we reach the state sv . Then transition tv is executed in sv to obtain sv′ , and the transition
38                        Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


components of the morphisms are ran backwards to obtain tw , and the associated end state sw′ .
Formally:
                          ComSquares · () () sv sv′ tv sw sw
                                                           ′ t   =
                                                               w b
                             sv = sw ∧ sv′ = sw′ ∧t =t
                                                     v    w
                                                   X0
                          ComSquares (f 0 : V1 → W ), ∆) (x 0 , x̄) (x 0′ , x̄ ′ )
                                           sv sv′ tv sw sw
                                                         ′ t   =
                                                             w b
                             ∃s 1 s 1 t 1 . ComSquares ∆ x̄ x̄ ′ sv sv′ tv s 1 s 1′ t 1 ∧
                                    ′
                             f 0Σ x 0 sw = s 1 ∧ f 0Σ x 0′ sw
                                                            ′ = s′
                                                                 1
     We will often abbreviate ComSquares, and write:
                       unwind_tr ∆ x̄ x̄ ′ tv sw sw′ b =
                         ∃sv sv′ tw . ComSquares ∆ x̄ x̄ ′ sv sv′ tv sw sw′ tw
                       unwind_act ∆ x̄ x̄ ′ a sw sw′ v b  =
                         ∃sv sv′ tv tw . a sv = (tv , v) ∧
                                         ComSquares ∆ x̄ x̄ ′ sv sv′ tv sw sw′ tw
Given a context ∆, input indices x̄, input state sw and input transition tv , unwind_tr “unwinds”
the transition, in the sense that it computes the output index x̄ ′, output state sw′ , obtained by the
morphing iteratively by the morphisms in ∆. The abbreviation unwind_act does the same, but for
input action a : actionV A. In the process, unwind_act also computes the return value v.
   In the frequent cases where ∆ is the empty context (and correspondingly, x̄ and x̄ ′ are empty
                                                                                        π
tuples ()), we will abbreviate the judgment from Figure 12, and simply write s,T −     → s ′,T ′.
   The operational semantics on trees in Figure 12 may not make a step on a tree for two different
reasons. The first, benign, reason is that the the chosen path π does not actually determine an action
or a redex in the tree T . For example, we may have T = Unfinished and π = ParR. But we can
choose the right side of a parallel composition only in a tree whose head constructor is Par, which
is not the case with Unfinished. We consider such paths that do not determine an action or a redex
in a tree to be ill-formed. The second reason arises when π is actually well-formed. In that case,
the constructors of the path uniquely determine a number of rules of the operational semantics
that should be applied to step the tree. However, the premises of the rules may not be satisfies.
For example, in the ChoiceAct rule, there may not exist a v such that unwind ∆ x̄ x̄ ′ a s s ′ v. To
differentiate between these two different reasons, we first define the notion of well-formed, or good
path, for a given tree.
  Definition D.2 (Good paths). Let T : tree V A and π be a path. Then the predicate good T π
recognizes good paths for a tree T as follows:
                       good (Act a)                ChoiceAct   = true
                                                               b
                       good (Seq (Ret v) _)        SeqRet      = true
                                                               b
                       good (Seq T _)              SeqRet π    = good T π
                                                               b
                       good (Par (Ret _) (Ret _) _)ParRet      = true
                                                               b
                       good (Par T1 T2 _)          ParL π      = good T1 π
                                                               b
                       good (Par T1 T2 _)          ParR π      = good T2 π
                                                               b
                       good (Morph f x (Ret _)) MorphRet       = true
                                                               b
                       good (Morph f x T )         MorphStep π b
                                                               = good T π
                       good T                      π           = false otherwise
                                                               b

   Definition D.3 (Safe configurations). We say that a state s is safe for the tree T and path π , written
s ∈ safe t π if:
                                                              π
                                   good T π → ∃s ′ T ′ . s,T −→ s ′,T ′
Specifying Concurrent Programs in Separation Logic: Morphisms and Simulations                                         39


   Notice that in the above definition, the trees Unfinished and Ret v are safe for any path, simply
because there are no good paths for them, as such trees are terminal. On the other hand, a tree
Act a does have a good path, namely ChoiceAct, but may be unsafe, if the action a is not defined
on input state s. For example, the a may be an action for reading from some pointer x, but that
pointer may not be allocated in the state s.
   Safety of a tree will be an important property in the definition of Hoare triples, where we will
require that a precondition of a program implies that the trees comprising the program’s denotation
are safe for every path.
   The following are several important lemmas about trees and their operational semantics, which
lift most of the properties of transitions, to trees.
                                                                                                                  π
  Lemma D.4 (Coverage of stepping by transitions). Let ∆ : V → W , and ∆ ⊢ x̄, s,T −                  → x̄ ′, s ′,T ′.
Then either the step corresponds to an idle transition, that is, (x̄, s) = (x̄ , s ), or there exists a transition
                                                                              ′   ′

a ∈ ∆ (V ), such that unwind_tr ∆ x̄ x̄ ′ a s s ′ v.
                                                                                                      π
   Lemma D.5 (Other-fixity of stepping). Let ∆ : V → W and ∆ ⊢ x̄, s,T −
                                                                       → x̄ ′, s ′,T ′. Then
ao (s) = ao (s ).
              ′

                                                                                                              π
   Lemma D.6 (Stepping preserves state spaces). Let ∆ : V → W and ∆ ⊢ x̄, s,T −
                                                                              → x̄ ′, s ′,T ′. If
s ∈ Σ (W ) then s ∈ Σ (W ).
                 ′

                                                                                          π
    Lemma D.7 (Stability of stepping). Let ∆ : V → W and ∆ ⊢ x̄, s,T −
                                                                     → x̄ ′, s ′,T ′. Then s ⊤ −→∗
                                                                                                                      W
s ′⊤ .
                                                                                                          π
  Lemma D.8 (Determinism of stepping). Let ∆ : V → W and ∆ ⊢ x̄, s,T −
                                                                     → x̄ ′, s ′,T ′, and
            π
∆ ⊢ x̄, s,T −
            → x̄ , s ,T . Then x̄ = x̄ , s = s and T = T .
                ′′  ′′ ′′        ′    ′′  ′   ′′    ′   ′′

                                                                                              π
  Lemma D.9 (Locality of stepping). Let ∆ : V → W and ∆ ⊢ x̄, (s  p),T −
                                                                        → x̄ ′, s ′,T ′. Then there
                                                    π
exists s such that s = s  p, and ∆ ⊢ x̄, (s  p),T −
        ′′          ′   ′′                          → x̄ , (s  p),T .
                                                        ′    ′′     ′


    Lemma D.10 (Safety-monotonicity of stepping). If s  p ∈ safe T π then s  p ∈ safe T π .
                                                                                                  π
  Lemma D.11 (Frameability of stepping). Let s  p ∈ safe T π , and s  p,T −
                                                                            → s ′,T ′. Then there
                                         π
exists s such that s = s  p and s  p,T −
        ′′          ′   ′′               → , s  p,T .
                                              ′′     ′


   The following lemma is of crucial importance, as it relates stepping with morphisms. In particular,
it says that the steps of a tree are uniquely determined, no matter the morphism under which it
appears. Intuitively, this holds because each transition that a tree makes has a unique image under
                        X
a morphism f : V → W .

  Lemma D.12 (Stepping under morphism). Let f : V → W X and f x sw = sv . Then the following
hold:
                  π                                                                 π
    (1) if sv ,T −
                 → sv′ ,T ′, then ∃x ′ sw′ . f x ′ sw′ = sv′ and f ⊢ (x), sw ,T −  → (x ′), sw′ ,T ′.
                           π                                                            π
    (2) if f ⊢ (x), sw ,T −→ (x ′), sw′ ,T ′, then ∃x ′ sv′ . f x ′ sw′ = sv′ and sv ,T −
                                                                                        → sv′ ,T ′.

   The first property of this lemma relies on the fact that for a step over states in V , we can also
find a step over related states in W , i.e., that f encodes a simulation. The second property relies on
the fact that f ’s state component is a function in the contravariant direction. Thus, for each sw
there are unique x and sv , such that f x sw = sv .
40                      Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas


D.3   Predicate transformers
In this section we define a number of predicate transformers over trees that ultimately lead to
defining the vrf predicate transformer on programs.
   Definition D.13 (Modal Predicate Transformers). Let T : tree V A, and ζ be a sequence of paths.
Also, let X be an assertion over V -states and V -trees, and Q be an assertion over A-values and
V -states. We define the following predicate transformers:
                       alwaysζ T X s b   =
                           if ζ = π :: ζ ′ then
                              ∀s 2 . (s −→∗ s 2 ) → safe T π s 2 ∧ X s 2 T ∧
                                        V
                                                 π
                                 ∀s 3 T ′ . (s 2 ,T −→ s 3 ,T ′ ) → alwaysζ T2 X s 3
                                                                          ′


                            else ∀s 2 . (s −→∗ s 2 ) → X s 2 T
                                            V
                                    = ∀ζ . alwaysζ T X s
                       always T X s b

                       after T Q b
                                 = always T (λ s ′ T ′ . ∀v. T ′ = Ret v → Q v s ′ )

  The helper predicate alwaysζ T X s expresses the fact that starting from the state s, the tree T
remains safe and the user-chosen predicate X holds of all intermediate states and trees obtained
by evaluating T in the state s according to the sequence of paths ζ . The predicate X remains valid
under any any environment steps of the resource V .
  The predicate always T X s quantifiers over the path sequences. Thus, it expresses that T is safe
and X holds after any finite number of steps which can be taken by T in s.
  The predicate transformer after T Q encodes that T is safe for any number of steps; however,
Q v s ′ only holds if T has been completely reduced to Ret v and state s ′. In other words Q is a
postcondition for T , as it is required to hold only if, and after, T has terminated.
  Now we can define the vrf predicate transformer on programs, by quantifying over all trees in
the denotation of a program.
                                   vrf e Q s b
                                             = ∀T ∈ e. after T Q s
   This immediately gives us a way to define when a program e has a precondition P and postcon-
dition Q: when all the trees in T have a precondition P and postcondition Q according to the after
predicate, or equivalently, when
                                     ∀s ∈ Σ (V ). P s → vrf e Q s
which is the formulation we used in Section 3 to define the Hoare triples.
   We can now state the following soundness theorem, each of whose three components has been
established in the Coq files.
   Theorem D.14 (Soundness).
    • All the properties of vrf predicate transformer from Section 3 are valid.
    • The sets ST V A and {P } A {Q } are complete lattices under subset ordering with the set
      {Unfinished} as the bottom. Thus one can compute the least fixed point of every monotone
      function by Knaster-Tarski theorem.
    • All program constructors are monotone.
