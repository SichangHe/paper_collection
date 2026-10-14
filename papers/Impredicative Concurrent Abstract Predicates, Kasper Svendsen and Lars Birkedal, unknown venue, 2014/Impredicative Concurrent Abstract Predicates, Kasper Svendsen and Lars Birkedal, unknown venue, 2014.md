    Impredicative Concurrent Abstract Predicates

                         Kasper Svendsen and Lars Birkedal

                                  Aarhus University
                           {ksvendsen,birkedal}@cs.au.dk


       Abstract. We present impredicative concurrent abstract predicates –
       iCAP – a program logic for modular reasoning about concurrent, higher-
       order, reentrant, imperative code. Building on earlier work, iCAP uses
       protocols to reason about shared mutable state. A key novel feature of
       iCAP is the ability to deﬁne impredicative protocols; protocols that are
       parameterized on arbitrary predicates, including predicates that them-
       selves refer to protocols. We demonstrate the utility of impredicative
       protocols through a series of examples, including the speciﬁcation and
       veriﬁcation, in the logic, of a spin-lock, a reentrant event loop, and
       a concurrent bag implemented using cooperation, against modular
       speciﬁcations.


1     Introduction
It is well-known that modular speciﬁcation and veriﬁcation of concurrent higher-
order imperative programs is very challenging. Recently good progress has been
made on reasoning about subsets of these language features. For instance, con-
current abstract predicates [8] has proved useful for reasoning about shared
mutable data structures in a concurrent setting and state transition systems [10]
have proved useful for reasoning about higher-order functions and shared muta-
ble data structures and, very recently, also concurrency [23].
Internal and External Sharing. The logics referred to above extend rely-
guarantee versions of separation logic [24,11] with protocols governing access to
shared mutable state. These logics are suﬃciently expressive to verify implemen-
tations of abstract data structures that use sharing internally against abstract
speciﬁcations that hide this internal sharing. However, in practice programmers
often also use shared mutable data structures to facilitate external sharing –
the sharing of a mutable data structure through another shared mutable data
structure. A lock is the canonical example of a data structure used to facilitate
external sharing. In higher-order separation logic we can easily express specifi-
cations that support reasoning about external sharing, by parameterizing our
speciﬁcations with assertions that describe the external resources shared through
the data structure. However, without imposing severe predicativity restrictions
(as in our earlier [21]), verifying implementations against such higher-order spec-
iﬁcations in the logic is currently impossible!
   To illustrate, consider a simple lock. We can specify a lock in higher-order sep-
aration logic by parameterizing our lock speciﬁcation with a resource invariant

Z. Shao (Ed.): ESOP 2014, LNCS 8410, pp. 149–168, 2014.

c Springer-Verlag Berlin Heidelberg 2014
150       K. Svendsen and L. Birkedal

R that describes the resources protected by the lock (the externally shared re-
sources):

                                {R} new Lock() {isLock(R, ret)}
                      {isLock(R, x)} x.Acquire() {locked(R, x) ∗ R}
                  {locked(R, x) ∗ R} x.Release() {isLock(R, x)}
                       isLock(R, x) ⇔ isLock(R, x) ∗ isLock(R, x)
Here isLock and locked are abstract predicates; isLock(R, x) expresses that x is a
lock protecting the resource invariant R and locked(R, x) expresses that the lock
x is indeed locked. Acquiring the lock grants ownership of R, while releasing the
lock requires the client to relinquish ownership of R. Since the resource invariant
R is universally quantiﬁed, this is a very strong speciﬁcation; in particular, the
client is free to instantiate R with any assertion, including assertions about other
shared resources or even the lock itself. In Section 2.2 we will see that resource
invariants that refer to the lock itself are useful for reasoning about reentrancy.
   There has been some previous work on logics for languages with built-in locks
[12,14]. In [14] the built-in locks were shown to satisfy a similar higher-order
speciﬁcation, as part of the logic’s soundness proof. However, to reason about
libraries in general (not just built-in locks), we, of course, need to able to verify
that implementations satisfy such speciﬁcations in the logic.
   Our ﬁrst contribution is a new program logic, impredicative Concurrent Ab-
stract Predicates or iCAP, that is suﬃciently expressive to support modular
reasoning about both internal and external sharing. It is the ﬁrst logic that can
verify implementations of synchronization primitives, such as locks, against such
higher-order speciﬁcations in the logic.
Layered and Recursive Abstractions. One of the main objectives of iCAP
is to support modular reasoning about libraries consisting of concurrent, higher-
order, reentrant, imperative code. In iCAP we have focused on two types of
modularity that are both important in programming practice. The ﬁrst type is
simply the ability to build layers of abstractions; for instance, we want to be
able to reason about a hashtable library implemented using a linked list library
through an abstract linked list speciﬁcation and hide this internal use of the
linked list abstraction in the abstract hashtable speciﬁcation. The second type
of modularity is more challenging, namely the ability to build recursive abstrac-
tions; for instance, we want to be able to verify reentrant libraries against an
abstract speciﬁcation that allows clients to register callbacks that can themselves
use the abstract library speciﬁcation to reason about calls into the library.
   To illustrate the problem of modular reasoning about reentrant libraries, con-
sider an event loop library satisfying the interface given below.1




1
    The ﬁrst line declares a delegate type (a type-safe function pointer type) by the name
    handler for delegates that do not take any arguments and do not return anything.
                                  Impredicative Concurrent Abstract Predicates   151

public delegate void handler();

interface IEventLoop {
  void loop();
  void signal();
  void when(handler f);
}

This library allows clients to emit an event using the signal method, to register
an event handler using the when method and start the event loop using the loop
method. Crucially, this library explicitly allows event handlers to emit events
and thereby schedule themselves for execution once again! We have simpliﬁed
this example to focus on the main diﬃculty introduced by reentrancy – namely
that clients can tie Landin’s knot through the library – however, this pattern
is ubiquitous in the real world. For instance, event-driven code is ubiquitous
in GUI applications and high-performance network applications as a way of
implementing asynchronous I/O [1,18].
   To support modular reasoning about such examples and in particular the event
loop, we need a logic that is suﬃciently expressive to (1) deﬁne an abstract event
loop speciﬁcation that allows clients to register callbacks that emit events and
reason about these callbacks using the same abstract specification and (2) allow
implementors to verify an implementation of the event loop against the abstract
event loop speciﬁcation.
   In Section 2.2 we explain how to verify an implementation against such an
abstract speciﬁcation, by deﬁning the memory footprint of the event loop im-
plementation recursively. In iCAP we achieve this using guarded recursion. One
of the implementations we consider uses the lock module and thus, as we shall
see, the recursively deﬁned predicate involves the abstract isLock predicate. To
the best of our knowledge, iCAP is the ﬁrst program logic that supports such
modular reasoning about layered and recursive abstractions, and a key techni-
cal contribution of our work is the model used to show the soundness of this
expressive logic, in particular, the ability to deﬁne predicates recursively across
abstraction boundaries.
Fine-Grained Concurrency. Fine-grained concurrent ADTs allow multiple
threads to interleave memory operations on the underlying data representation,
with the goal of reducing critical sections as much as possible, often down to basic
compare-and-swap operations. Sophisticated ﬁne-grained concurrent ADTs also
employ cooperation [23] among threads and in particular the technique of helping,
where one thread may help another complete its operation [13].
   Conceptually, separation logic achieves modular reasoning about shared mu-
table state through the notion of resources that describe information about some
part of the state and assert certain rights to modify this part of the state. To sup-
port modular reasoning about ADTs we need abstract speciﬁcations that allow
clients to deﬁne high-level ADT resources with a notion of rights expressed in
terms of the operations provided by the ADT rather than rights to modify the
underlying data representation. Previous CAP-based techniques for reasoning
152    K. Svendsen and L. Birkedal

about ﬁne-grained concurrent data structures have either not scaled to handle
implementations that employed helping [21], or have veriﬁed implementations
with helping against non-modular speciﬁcations [8] that imposed a ﬁxed notion
of rights – choosen by the module implementor – on clients.
   In iCAP, using impredicative protocols, we can verify ﬁne-grained concurrent
ADTs implemented with helping against modular speciﬁcations that allow clients
to deﬁne high-level ADT resources. In Section 2.3 we present an example to show
how this is done.
   Details and proofs can be found in the accompanying appendix and technical
report available at:
             https://bitbucket.org/logsem/public/wiki/icap

1.1    Summary of Contributions
In summary, our contributions include the design of a new sound program logic,
iCAP, for modular reasoning about concurrent, higher-order, reentrant, imper-
ative programs. In particular, iCAP supports modular reasoning about internal
and external sharing, layered and recursive abstractions, and ﬁne-grained coop-
erative implementations of concurrent data structures.
   iCAP’s expressiveness derives from the fact that it is a higher-order logic sup-
porting guarded recursion and impredicative protocols. The presence of these
features means that soundness of iCAP is non-trivial. Thus a key technical con-
tribution of our work is our soundness proof of iCAP, which uses a novel model
construction that we explain in Section 3.


2     Examples
2.1    Internal and External Sharing – A Lock
Following concurrent separation logic and its descendants [16,12,14], assertions in
iCAP describe resources that may potentially be shared between several threads
according to some protocol. A key feature of iCAP is that it supports full higher-
order quantiﬁcation over assertions in speciﬁcations. This means that we can
give the following general abstract speciﬁcation for a lock, which we explained
informally in the introduction.
         ∃isLock, locked : Prop × Val → Prop. ∀R : Prop. stable(R) ⇒
                 {R}new Lock(−) {ret. isLock(R, ret)}
              ∧ {isLock(R, x)} x.Acquire(−) {locked(R, x) ∗ R}
              ∧ {locked(R, x) ∗ R} x.Release(−) {ret. emp}
              ∧ valid(∀x : Val. isLock(R, x) ⇔ isLock(R, x) ∗ isLock(R, x))
              ∧ ∀x : Val. stable(isLock(R, x)) ∧ stable(locked(R, x))
In this formal speciﬁcation Prop is the type of iCAP assertions, which includes
assertions about shared resources. The speciﬁcation thus explicitly requires the
                              Impredicative Concurrent Abstract Predicates      153

resource invariant R to be stable (invariant under any changes to the state
the environment is permitted to make). The existentially quantiﬁed predicates
isLock and locked are used to support modular reasoning about internal shar-
ing, whereas the universally quantiﬁed predicate R is used to support modular
reasoning about external sharing.
   This speciﬁcation asserts the existence of a lock representation predicate that
is parametric in the resource invariant R. This allows us to use the lock repre-
sentation predicate itself when deﬁning resource invariants and thus to deﬁne
recursive resource invariants. Had we simply asserted that for each resource in-
variant R, there exists a non-parametric lock representation predicate isLockR ,
this would not be possible! As we will see in Section 2.2, the above third-order
lock speciﬁcation and the ability to deﬁne recursive resource invariants is critical
for reasoning about the reentrancy of a multi-threaded event loop.
   To verify an implementation against this speciﬁcation we have to provide con-
crete instantiations for the parametric isLock and locked predicates and prove
that the implementation satisﬁes the speciﬁcation with these concrete instantia-
tions. Since this speciﬁcation explicitly allows clients to deﬁne recursive resource
invariants, most of the diﬃculty in verifying an implementation boils down to
deﬁning the parametric isLock and locked predicates. In iCAP this is trivial using
impredicative protocols.
A Spin-Lock. The implementation we have in mind is a simple spin-lock; it
maintains a single boolean ﬁeld, locked, which is true if and only if the lock is
currently held. When the lock is unlocked, the lock owns the resource invariant
R. Once the lock has been locked, only the exclusive owner of the locked resource
is allowed to unlock the lock! We can express this protocol formally using iCAP.
   iCAP extends separation logic with shared regions. Resources in shared re-
gions are — as the name implies — shared between all clients. Upon allocation
of a new shared region, we can pick a protocol of our choice, describing what
resources the shared region must own. A protocol consists of a labelled transition
system, labelled with action identifiers, and an assertion for each abstract state
in the transition system that describes the resources the shared region must own
in the given state. The transitions then specify how the abstract states of the
region are allowed to evolve and the labels how diﬀerent clients are allowed to
evolve the states. In particular, for a client to change the state from s1 to s2 ,
the client must own permissions to labels along a path from s1 to s2 .
   In the case of the spin-lock, for each instance of the spin-lock, we introduce
a new shared region that governs that spin-lock and the resources protected by
that lock. The labelled transition system that governs a spin-lock is very simple:
it contains two abstract states — locked (L) and unlocked (U) — and the two
obvious transitions:


                                       Acq
                              U                    L
                                       Rel
154     K. Svendsen and L. Birkedal

The next step is to deﬁne an assertion for each abstract state describing the
resources owned by the spin-lock region (conceptually, the lock) in the given
state. This is mostly straightforward. When the lock is locked, the lock owns the
locked ﬁeld, which contains true. However, when the lock is unlocked, the lock
owns both the locked ﬁeld, which contains false, and the resource invariant R:
 I(n, R, x)(L) = x.locked → true       I(n, R, x)(U) = x.locked → false ∗ R ∗ [Rel]n1
              def                                    def



 To capture that only the owner of the locked resource is allowed to unlock
the lock, we also let the lock take full ownership of the Rel transition for the
given region, when the lock is unlocked. Formally this is expressed using an
action assertion, [α]nπ . Here π is a fraction between 0 and 1, and [α]nπ asserts
π-ownership of the α action on region n. When the client locks the lock, the
client can thus take ownership of both the resource invariant R and the exclusive
(1) permission to transition the shared region back into the unlocked state. Note
that this spin-lock protocol is parameterized over an arbitrary resource invariant
R provided by the client and is thus an impredicative protocol.
   With these ingredients we are now ready to instantiate isLock. The isLock
predicate asserts that there exists a shared region governed by the above spin-
lock protocol, that is either in the unlocked or locked state; and furthermore, it
asserts non-exclusive permission to the Acq action. Formally, this is expressed
as follows (where Tlock refers to the labelled transition system above):
  isLock(R, x) = ∃n : RId. [Acq]n ∗ rintr(I(n, R, x), n) ∗ region({L, U}, Tlock , n)
               def



  The region assertion, region(X, T, n), asserts that there exists a region with
region identiﬁer n, whose labelled transition system is T and that the current
abstract state of region n is a member of the set X. The labelled transition system
T is represented as a function from action identiﬁers to relations on abstract
states; see the appendix for details. To specify the spin-lock protocol we also need
to specify what resources the spin-lock must own in the diﬀerent abstract states.
This is expressed using the region interpretation assertion, rintr(I, n), which takes
as argument a predicate I, indexed by the abstract states of the given region.
We use [α]n as shorthand for ∃π. [α]nπ to express non-exclusive ownership of an
action α.
   This illustrates the use of iCAP’s impredicative protocols for deﬁning the con-
crete instantion of isLock for a spin-lock. Now that isLock has been deﬁned, the
actual veriﬁcation of the spin-lock implementation with this concrete instantia-
tion follows the structure of the original CAP proof of a spin-lock [8]. One crucial
diﬀerence is that iCAP features enough proof rules to carry out the proof in the
logic, including stability proofs. In the appendix, we show in detail how to verify
the spin-lock implementation with this concrete instantiation using the formal
iCAP proof system.
   Compared to earlier work on concurrent abstract predicates [8,9,21], in iCAP
we simplify the description of protocols, by describing them using state transi-
tion systems. This presentation is inspired by earlier work by Dreyer et. al. on
protocols for reasoning about local state in higher-order programs [10]. We be-
lieve this description of protocols is a useful conceptual simpliﬁcation compared
                                Impredicative Concurrent Abstract Predicates     155

to the original CAP presentation [8], in particular since protocols can now eas-
ily be drawn. However, we stress that this presentation also simpliﬁes stability
proofs in the program logic, since they only have to refer to abstract states in
the transition system. The iCAP stability obligations for the veriﬁcation of the
spin-lock are thus signiﬁcantly easier to prove that the corresponding stability
obligations from the original spin-lock CAP proof.

2.2     Layered and Recursive Abstractions – An Event Loop
The previous example illustrated how iCAP’s impredicative protocols allow mod-
ular reasoning about internal and external sharing. In this section we illustrate
how higher-order logic and guarded recursion allow modular reasoning about
layered and recursive abstractions.
A Single-Threaded Event Loop. Recall the reentrant event loop library from
the introduction. We can express an abstract event loop speciﬁcation for single-
threaded event loops that explicitly allows clients to reason about event handlers
using the same event loop speciﬁcation as follows:
         ∃eloop : Val → Prop.
                 {emp}new EventLoop(−) {ret. eloop(ret)}
               ∧ {eloop(x)} x.loop(−) {eloop(x)}
               ∧ {eloop(x)} x.signal(−) {eloop(x)}
               ∧ {eloop(x) ∗ f → {eloop(x)}{eloop(x)}} x.when(f) {eloop(x)}
This speciﬁcation asserts the existence of an abstract event loop resource, eloop,
which is created by creating a new event loop instance and preserved by all event
loop methods. The when method for registering event handlers requires that the
given event handler satisﬁes the nested Hoare triple
                              f → {eloop(x)}{eloop(x)},
thereby explicitly allowing event handlers to use the abstract eloop resource to
emit events. In a sense this is a very weak speciﬁcation, in that it only allows
us to reason about memory safety of our clients. However, in the presence of
reentrancy, verifying an implementation against this simpliﬁed speciﬁcation is
highly non-trivial and beyond almost all current program logics.2
   To deﬁne a concrete eloop resource, imagine a concrete implementation that
maintains a set of pending events and a set of registered handlers, as sketched
below.
class EventLoop : IEventLoop {
  private Set<event> signals;
  private Set<handler> handlers;
  ...
}
2
    The exception being our own HOCAP [21], which, however, had other severe restric-
    tions compared to iCAP.
156     K. Svendsen and L. Birkedal

To allow the event loop to call registered event handlers, the eloop resource must
assert that the registered event handlers satisfy some speciﬁcation. To allow event
handlers to emit events, this speciﬁcation must itself refer to the eloop resource.
In iCAP we can express this recursion by guarding the recursive occurence of
the eloop resource and deﬁning eloop by guarded recursion (note the use of the
“later” () connective, which serves as a guard):

      eloop = fix( λeloop : Val → Prop. λx : Val. ∃y, z : Val. ∃A, B : Pﬁn (Val).
                     x.signals → y ∗ x.handlers → z ∗ set(y, A) ∗ set(z, B) ∗
                       ∀b ∈ B.  b → {eloop(x)}{eloop(x)})

This event loop resource asserts exclusive ownership of the signals ﬁeld, the
handlers ﬁeld, the set of pending events, the set of registered handlers, and that
all registered handlers satisfy the speciﬁcation f → {eloop(x)}{eloop(x)}, one
step later.
   In our operational semantics each atomic statement takes one step to execute
and executing a method or delegate call executes one atomic statement before the
body of the method or delegate is executed. Hence, to verify a call to a method
or delegate, it suﬃces to know the speciﬁcation of the method or delegate body,
one step later. We can thus verify calls from the event loop to the registered
event handlers using the guarded eloop resource deﬁned above.
   Note that eloop is not deﬁnable by induction, as the recursive argument is not
applied to a structurally smaller argument, nor by Tarski’s ﬁxed-point theorem,
as nested Hoare triples are contravariant in the pre-condition and covariant in
the postcondition.
   As with the lock example, the interesting part of the veriﬁcation of a reen-
trant event loop is the deﬁnition of the event loop resource. Once the event
loop resource has been deﬁned, the veriﬁcation is routine. The real challenge is
deﬁning a logic and accompanying model that supports such recursive resource
deﬁnitions!
A Multi-threaded Event Loop. The single-threaded event loop example il-
lustrated the use of guarded recursion for reasoning about recursive abstractions.
To make the example even more challenging and truly illustrate the power of im-
predicative protocols, let us now consider a multi-threaded reentrant event loop
library. The abstract event loop speciﬁcation remains the same, expect with the
added axiom that the abstract event loop resource is freely duplicable (thus
allowing any number of clients to use the event loop concurrently):

                   valid(∀x : Val. eloop(x) ⇔ eloop(x) ∗ eloop(x))

As for the implementation, imagine a lock-based implementation that extends
the previous implementation with a lock that protects the set of pending events
and the set of registered event handlers. Conceptually, we thus have a library
that allows clients to tie Landin’s knot through a reference protected by a lock.
To verify the single-threaded implementation, we needed to refer to eloop to
specify the registered handlers when deﬁning eloop. Likewise, now eloop must
                              Impredicative Concurrent Abstract Predicates       157

assert the existence of a lock that protects the registered event handlers that are
again speciﬁed in terms of eloop (note the use of isLock):

eloop = fix( λeloop : Val → Prop. λx : Val. ∃l : Val. x.lock → l ∗
               isLock(l, ∃y, z : Val. ∃A, B : Pﬁn (Val).
                            x.signals → y ∗ x.handlers → z ∗ set(y, A) ∗ set(z, B) ∗
                               ∀b ∈ B.  b → {eloop(x)}{eloop(x)}))

This deﬁnition is extremely interesting! First of all, it illustrates the true power
of the third-order lock speciﬁcation to deﬁne recursive resource invariants that
refer back to the lock itself. This is only possible because the abstract lock spec-
iﬁcation asserts the existence of a parameterized lock representation predicate;
thus allowing us to define the resource invariant in terms of the lock itself (the
resource invariant we use for the lock is the argument given to isLock, which
refers to eloop, which again refers to isLock).
   This example also illustrates the ability of iCAP to combine layered and recur-
sive abstractions; in this example we are reasoning about the recursive event loop
abstraction in terms of the lock abstraction deﬁned in Section 2.1. In particular,
the eloop representation predicate is deﬁned in terms of an abstract isLock rep-
resentation predicate. To ensure that eloop is well-deﬁned we thus have to prove
guardedness across an abstraction boundary (i.e., that the recursive occurence
of eloop inside the abstract isLock assertion is guarded). This is automatically
enforced in iCAP (!), and thus iCAP supports modular reasoning about guard-
edness. Semantically, this is enforced in the interpretation of the iCAP function
space, which intuitively does not consist of all set-theoretic functions, but only
those functions that are suitably non-expansive. Note that these intracies in the
model are abstracted away by the iCAP logic and the proof in iCAP of the well-
deﬁnedness of the eloop predicate above is completely trivial and just follows
from the fact that the recursive occurrence of eloop is under a  guard.
   These two event loop examples illustrate how we can reason about recursive
abstractions in iCAP and also exemplify the power of impredicative protocols.
For presentation purposes we considered the core part of a simple example —
we emphasize that this style of reasoning also scales to full functional veriﬁ-
cation of complicated examples such as the joins library [19], which combines
layered and recursive abstractions with internal and external sharing in a higher-
order, concurrent, reentrant, imperative library. We have previously veriﬁed a
lock-based joins implementation in HOCAP against an abstract joins speciﬁca-
tion with an explicit predicative stratiﬁcation [20]. In iCAP, using impredicative
protocols, we can verify the joins implementation against a much simpler and
more expressive joins speciﬁcation. Furthermore, in HOCAP we could not verify
a ﬁne-grained implementation of the joins library; in iCAP this is now possible
using the techniques explained in the following.
158     K. Svendsen and L. Birkedal

2.3    Fine-Grained Concurrency – A Concurrent Bag
In this section we illustrate how iCAP supports modular reasoning about ad-
vanced concurrent ADTs by verifying a ﬁne-grained implementation of a con-
current bag, implemented using helping, against a modular ADT speciﬁcation.
   We start by recalling our speciﬁcation pattern from HOCAP [21] for express-
ing modular ADT speciﬁcations that allow clients to deﬁne a high-level ADT
resources with a notion of rights that matches the client’s intended use. Next,
we sketch how to verify a ﬁne-grained implementation with helping of a concur-
rent bag against an abstract bag speciﬁcation expressed using this speciﬁcation
pattern. See the associated technical report for the full proof.
A Modular ADT Specification. Recall that in a sequential setting, one typ-
ically speciﬁes data structure operations by relating an abstraction of the initial
and terminal state of the operation through an abstract representation predi-
cate. For instance, we might specify a Push method for an unordered bag as
follows:
                    {bag(x, A)} x.Push(y) {bag(x, A ∪ {y})}
This says that if, initially, the bag contains the elements in the multiset A, then,
upon termination, the bag contains the elements in A and y. Crucially, this
speciﬁcation relates the abstract initial and terminal eﬀects of the entire Push
method.
   In a concurrent setting we can reason modularly about implementations that
satisfy that for each intermediate state in its execution, there exists some abstract
state describing the concrete state and the method contains zero or more atomic
instructions that modify the abstract state. Following our earlier work [21], the
idea now is to allow clients to reason about the abstract initial and terminal state
for each of these atomic instructions, rather than the abstract initial and termi-
nal state of the entire method. By allowing clients to reason about the atomic
instructions that modify the abstract state, clients can deﬁne their own high-
level ADT resources with a notion of rights expressed in terms of the abstract
state.
   Technically, we achieve this using a phantom field, shared between the concur-
rent ADT and any clients, that stores the current abstract state of an instance.
Phantom ﬁelds play a similar role as ghost/auxiliary variables [17], in that they
                                                             π
are ﬁelds used only for speciﬁcation purposes. We use xf → v to assert fractional
ownership of phantom ﬁeld f on object x with fraction π. By splitting owner-
ship of the phantom ﬁeld we ensure that the concurrent ADT and any clients
agree on the current abstract state. To allow clients to reason about the atomic
instructions that modify the abstract state (and thus the phantom ﬁeld), we fur-
ther parameterize the speciﬁcation of each method with a view shift. View shifts
describe updates to the instrumented state that do not aﬀect the concrete state.
View shifts can thus be used to update phantom ﬁelds, allocate new regions and
change the abstract state of a region, potentially transferring ownership of some
resource in the process. We use P Q to express that P can be view shifted to
Q. See the appendix for proof rules relating to phantom ﬁelds and view shifts.
                                  Impredicative Concurrent Abstract Predicates   159

A Modular Bag Specification. We present part of the bag speciﬁcation in
Figure 1; we now explain it. We only include an operation to create the bag and
a push operation, the speciﬁcation for a pop method is similar and omitted.


            ∃bag : RId × Val → Prop.
                                                                      1/2
            {emp} new Bag(−) {ret. ∃n : RId. bag(n, ret) ∗ retcont → ∅}
            ∀P, Q : Val × Val → Prop. ∀n : RId.
            (∀X : Pm (Val). ∀x, y : Val.
                   1/2                            1/2
              xcont → X ∗ P(x, y) RId\{n} xcont → (X ∪ {y}) ∗ Q(x, y)) ⇒
              {bag(n, x) ∗ P(x, y)} x.Push(y) {bag(n, x) ∗ Q(x, y)}

                     Fig. 1. Part of a modular bag speciﬁcation


   In the case of the Push method, assuming it only contains a single atomic
instruction that “commits” the push, we can express this formally by relating
the eﬀects of the Push method with an arbitrary “push” view shift provided
by the client, see Lines 3–6 in Figure 1. The view shift expresses what should
happen at the client side when the abstract state of the push operation takes
                            1/2
place. The assertion xcont → X asserts half-ownership of the phantom ﬁeld cont,
which contains the current abstract state of the bag. By letting the data structure
own half and clients share the other half (clients get the other half by calling the
new method), clients can impose a protocol on the abstract state that matches
their intended notion of rights through their half of the phantom ﬁeld. Since
updating the phantom ﬁeld requires both halves, this forces clients to prove that
the abstract eﬀects of any call to the Push method satisﬁes any protocols clients
may have imposed.
   We call the view shift in the premise of the above rule a “push” view shift
because it requires the client to update the initial abstract state from X to
X ∪ {y}, for any abstract state X. Conceptually, this view shift is thus an atomic
“push” method at the instrumented level and the push speciﬁcation expresses
that the Push method simulates any such “push” view shift provided by the
client. The universally quantiﬁed predicates P and Q allow the client to relate its
local state with the abstract initial and terminal state of the atomic instruction
that “commits” the push. We refer to P and Q as synchronization pre- and
postconditions.
   In [21] we had to impose severe restrictions on P and Q due to the lack of
impredicative protocols, but with iCAP, there are no restrictions on P and Q,
resulting in much simpler and more expressive reﬁnable speciﬁcations.
   Finally we comment on the superscript on the view shifts and the region
identiﬁer n argument to the bag predicate, bag(n, x). In iCAP, when reasoning
about an atomic instruction, we can “open” a shared region and move the shared
resources into our local state for the duration of the atomic instruction, provided
160      K. Svendsen and L. Birkedal

we obey the protocol imposed by the region. Clearly, it is only sound to “open”
each region once for each atomic instruction (opening a region twice results in
two local copies of the shared region’s resources).3 Since the “push” view shifts
provided by the client are used during the atomic instruction that “commits” the
push, we have to ensure that the client does not “open” the module’s region with
its view shifts. We thus parameterize the bag predicate with a region identiﬁer
n to reveal that the bag module may use region n. As discussed in the appendix,
this allows us to express, qua the superscript on the view shift, that the view
shift provided by the client should not open the region n.
   Now we have explained how to give a modular, reﬁnable, speciﬁcation to
a concurrent data structure. We now sketch how iCAP can be used to verify
that a sophisticated ﬁne-grained concurrent implementation using cooperation
actually meets the modular bag speciﬁcation. iCAP is the ﬁrst program logic
that supports veriﬁcation of such sophisticated implementations against such
modular speciﬁcations (in particular, in our earlier work [21] we could not deal
with implementations using cooperation).
   To reduce contention on the main data structure used to implement the bag,
a thread seeking to push an element (the “pusher”) may oﬀer the push operation
to other threads, using a side-channel. If a thread seeking to pop (the “popper”)
then comes along, it may notice and accept the push-oﬀer, without touching the
main data structure at all. By accepting the push-oﬀer the popper also completes
the operation of the pusher, and in that sense it has helped the pusher. The
heart of the veriﬁcation is the protocol used for handling oﬀers. In our case, that
protocol can be described using the following labelled transition system, denoted
Toﬀer :


                     Ack                 Accept                 Revoke
        ack’ed                accepted                pending               revoked




Intuitively, pending means that an oﬀer has been made and it is waiting for
somebody to accept it, accepted means that the oﬀer has been accepted, ack’ed
means that we have acknowledged that somebody has accepted the oﬀer, and
revoked is used for the case where we revoke the oﬀer (since no one accepted it
and now we will re-attempt to push).
   The interpretation of the states of Toﬀer are as follows:


            Ioﬀer (n, P, Q, b, x, y)(pending) = x.state → 0 ∗ P(b, y) ∗
                                             def



                 spec(∀X : Pm (Val). ∀x, y : Val.
                        1/2                              1/2
                   xcont → X ∗ P(x, y)   RId\{n}
                                                    xcont → (X ∪ {y}) ∗ Q(x, y))


3
    See the appendix for a concrete counterexample.
                              Impredicative Concurrent Abstract Predicates    161

             Ioﬀer (n, P, Q, b, x, y)(accepted) = x.state → 1 ∗ Q(b, y)
                                              def



               Ioﬀer (n, P, Q, b, x, y)(revoked) = x.state → 2
                                              def



                Ioﬀer (n, P, Q, b, x, y)(ack’ed) = x.state → 1
                                              def




Here b refers to the bag, x refers to the oﬀer, y is the value on oﬀer, and P and
Q are the pusher’s synchronization pre- and postconditions.
   The interpretations of the states contain information about the value of pro-
gram variable state, which is used by the implementation to keep track of which
state the oﬀer is in. The point to notice, however, is that the pending state con-
tains both the pusher’s synchronization precondition, P(b, y), and the pusher’s
“push” view shift, and the accepted state contains the pusher’s synchronization
postcondition, Q(b, y). To accept an oﬀer (transition the abstract state from
pending to accepted) the popper thus has to perform the pusher’s “push” view
shift. Conceptually, the oﬀer protocol “transfers” the pusher’s view shift to the
popper.
   Note how the combination of view shifts and impredicative protocols together
allows us to prove that the ﬁne-grained implementation with helping meets the
modular bag speciﬁcation.
   See the accompanying technical report for the full proof.


3    Model
In this section we present a model of iCAP. Soundness of iCAP is non-trivial.
Indeed, in our earlier work on HOCAP [21], we discovered that a recent proposal
for a higher-order variant of concurrent abstract predicates [9] was unsound.
This led us to consider only predicative protocols in [21], which simpliﬁed the
construction of a sound model, but also resulted in much weaker and more
complicated speciﬁcations and proofs. Here instead, we follow ideas from models
of impredicative type systems with higher-order store, e.g. [2,4], and deﬁne our
model of iCAP using a guarded-recursively defined space of protocols. We deﬁne
our model in the type theory and logic of the topos of trees [4]. This has the
advantage that most of the model construction is done as if we were working with
ordinary sets, except for those places where we need to guard some recursive
deﬁnitions for well-deﬁnedness. More importantly, it makes it straightforward
to deﬁne a higher-order logic, since the recursively deﬁned space of protocols
is now simply a type in the type theory of the topos of trees, which already
includes function and powerset types! The resulting program logic includes the
later operator from the ambient type theory. As we have already seen, we use this
later operator to deﬁne guarded-recursive assertions and protocols. It can also
be used to deﬁne guarded-recursive speciﬁcations. We emphasize that readers
need not be familiar with [4] in order to understand the present paper.
Topos of Trees. The internal language of the topos of trees is an intuitionistic
higher-order logic over a simply-typed term language extended with subset types
and guarded-recursive types. This internal language features a new type former
162      K. Svendsen and L. Birkedal

, pronounced later, for deﬁning guarded-recursive types, and a new logical
connective , also pronounced later, for deﬁning guarded-recursive predicates.
(For readers who are familiar with the use of theorem provers, such as Coq,
for formalizing models of logics or programming languages, it may be helpful
to think of the type theory of the topos of trees as playing the rôle of the Coq
type theory.) The point of using the guarded type theory and logic is that it
makes it easy to deﬁne the space of protocols, which needs to be recursively
deﬁned. Crucially, this results in a type in the guarded type theory, and thus,
since that type theory includes higher function types, we can then easily deﬁne
the interpretation of the function spaces in iCAP.4 The guarded type theory
also includes types of the form ΔX, for any ordinary set X. Such types ΔX are
referred to as constant sets. We deﬁne the non-recursive part of the model in the
category of sets and use these as constant sets to construct the recursive part of
the model in the topos of trees.
   The presentation of the iCAP model is inspired by the Views framework [7]
and models of impredicative type systems, e.g., [5], with higher-order store.
   The Views framework provides a general way of relating a concrete semantics
with an instrumented semantics and constructing a separation logic over the
instrumented semantics. In our case the concrete semantics is a subset of C#
with an interleaving semantics. The instrumented semantics extends the concrete
C# states with phantom ﬁelds, shared regions, and protocols and enforces that
clients respect the protocols governing shared resources.
   The model of iCAP is deﬁned in Figure 2, and is deﬁned over countably
inﬁnite and disjoint set of action identiﬁers, AId, state identiﬁers, SId, object
identiﬁers, OId, closure identiﬁers CId, region identiﬁers RId, class names CN,
ﬁeld names FN, and method names MN.
   Instrumented states (m ∈ M) are tuples consisting of three components: a
local state, a shared state and an action model. We use m.l, m.s and m.a to
refer to the ﬁrst, second and third component of m. The local state (l ∈ LS)
consists of a partial C# heap, a partial phantom heap and a capability map. The
partial C# heap and phantom heaps specify the current value and permissions to
heap cells and phantom ﬁelds, respectively. The capability map speciﬁes action
permissions on shared regions. In particular, it records the fractional permission
the client owns on each region and action identiﬁer. The shared state (s ∈ SS)
speciﬁes the current abstract state of each allocated region and the labelled
transition system governing the given region. We use s(r).s and s(r).p to refer
to the state and labelled transition system of region r of a shared state s. The
set of abstract states, AS, consists of pairs of local and shared state. Finally,
the action model (ς ∈ AMod) speciﬁes the interpretation of the abstract states
of each allocated region. Since the interpretation of each abstract state is given
by a general assertion, which is itself a subset of instrumented states, a naive

4
    If we had worked in the category of sets and used step-indexing directly, we would
    have had to deﬁne an appropriate notion of function space between the resulting
    indexed space of protocols and itself, and that would essentially amount to unrolling
    the deﬁnition from the topos of trees model.
                                                Impredicative Concurrent Abstract Predicates                   163


Semantic domains in the category of Sets
            def
      Cap = {f : (RId × AId) → [0, 1] | ∃R ⊆ﬁn RId. ∀r ∈ RId \ R. ∀α ∈ AId. f (r, α) = 0}
            def
     Heap = (OId × FN ﬁn Val) × (OId ﬁn CN) × (CId ﬁn OId × MN)
            def
    PHeap = {(pc, ph) ∈ (OId × FN → [0, 1]) × (OId × FN ﬁn Val) |
                     ∀o ∈ OId. ∀f ∈ FN. pc(o, f ) = 0 ⇒ (o, f ) ∈ dom(ph)}
                    def                                                       def
          l ∈ LS = PHeap × Heap × Cap                                    LTS = AId → P(SId × SId)
                    def                                                       def
          s ∈ SS = RId ﬁn (SId × LTS)                                     AS = LS × SS

Semantic domains in the topos of trees


          RIntr ∼                                   ↑                                              def
                = ((ΔSId × (ΔRId ﬁn RIntr)) →mon P (ΔAS))                                s ∈ Spec = Ω
                                                                                           p ∈ Prop = P ↑ (M)
             def                                           def                                       def
  ς ∈ AMod = ΔRId ﬁn RIntr                       m ∈ M = ΔLS × ΔSS × AMod

where the ordering on M is RRId and the ordering on ΔAS is

                          m1 ≤ m2     iﬀ        m1 .l ≤ m2 .l ∧ m1 .s ≤ m2 .s ∧ m1 .a ≤ m2 .a

Interference relation

                                          def
                             acts(l, r) = {α | π3 (l)(r, α) < 1}
                                          def
                          upds(l, r, p) = {(s1 , s2 ) | ∃α ∈ acts(l, r). (s1 , s2 ) ∈ p(α)}
                            def
                      RA = {((l1 , s1 ), (l2 , s2 )) | l1 ≤ l2 ∧ ∀r ∈ dom(s1 ).
                                      ((r ∈ A ∧ (s1 (r).s, s2 (r).s) ∈ upds(l1 , r, s1 (r).p))
                                           ∨ s1 (r).s = s2 (r).s) ∧ s1 (r).p = s2 (r).p}

where (−) denotes the transitive, reﬂexive closure.

Orderings                  l1 ≤ l2   iﬀ     ∃l3 . l2 = l1 •LS l3
                          s1 ≤ s2    iﬀ     ∀r ∈ dom(s1 ). r ∈ dom(s2 ) ∧ s1 (r) = s2 (r)
                           ς1 ≤ ς2   iﬀ     ∀r ∈ dom(ς1 ). r ∈ dom(ς2 ) ∧ ς1 (r) = ς2 (r)

Composition

              def                                         def
      x •= y = x              if x = y            f •+ g = λx. f (x) + g(x)          if ∀x. f (x) + g(x) ≤ 1
                           def
                   f •∪ g = f ∪ g                                        if dom(f ) ∩ dom(g) = ∅
                           def
                   f •? g = f ∪ g                         if ∀x ∈ dom(f ) ∩ dom(g). f (x) = g(x)
                    def                                                             def
            •Heap = •∪ × •= × •=                                            •PHeap = •+ × •?
                    def                                                             def
              •LS = •PHeap × •Heap × •+                                       •M = •LS × •= × •=

                                      def
Erasure                     (s, ς)r = {l ∈ LS | (l, s) ∈ app(ς(r))(s(r).s, ς)}

                          (l, s, ς)A = {h ∈ Heap | ∃l , sr : dom(s) ∩ A → LS.
                                      def


                                                    h = l .h ∧ l = l • Πr∈dom(s)∩A sr(r) ∧
                                                    ∀r ∈ dom(s) ∩ A. sr(r) ∈ (s, ς)r }



                                                Fig. 2. Model of iCAP
164      K. Svendsen and L. Birkedal

deﬁnition of AMod in set theory is not well-deﬁned. Instead, we let RIntr (the
type of interpretations of abstract states for a single region) denote a solution
to the following guarded-recursive equation
             RIntr ∼
                   = ((ΔSId × (ΔRId ﬁn RIntr)) →mon P ↑ (ΔAS))
Here ΔSId is the constant set of state identiers, ΔRId is the constant set of region
identiﬁers, ΔAS is the constant set of abstract states, and P ↑ (ΔAS) consistst
of the upwards-closed subsets of ΔAS with respect to the ordering shown in
Figure 2. Note the use of the  operator, which acts as a guard, and ensures
that RIntr is well-deﬁned (unique up to isomorphism). Using RIntr we can then
deﬁne the type of action models as the type of ﬁnite functions from region
                                             def
identiﬁers to region interpretations: AMod = ΔRId ﬁn RIntr. From the above
isomorphism we can deﬁne the following abstraction and application functions
to fold and unfold elements of RIntr:
                   lam : (ΔSId × AMod →mon P ↑ (ΔAS)) → RIntr
                   app : RIntr → (ΔSId × AMod →mon P ↑ (ΔAS))
Crucially, because of the guard, if we unfold a folded element x, we get back the
element x, one step later: app ◦ lam = , where  refers to the pointwise lifting
of  to function spaces.
   Assertions in iCAP are modeled as upwards-closed subsets of instrumented
states (see the deﬁnition of Prop in Figure 2), where the upwards-closure ex-
presses that assertions should be closed under allocation of new regions and
extensions of the local state. Assertions in the speciﬁcation logic are simply
modeled as assertions in the topos of trees. The function types of iCAP are sim-
ply modeled using the function space in the guarded type theory! (We emphasize
again that this is one of the advantages of using the topos of trees as the ambient
theory in which to deﬁne the model of iCAP; if we had worked in ordinary sets,
then iCAP types could not simply be interpreted as sets,5 they would have to
be indexed families of sets, and then the iCAP function space would also have
to be appropriate families of functions satisfying certain naturality conditions.
Interference Relation and Stability. The interference relation, RA , speciﬁes
how the environment is allowed to modify the abstract state of shared regions.
The interference relation is indexed by a set of region identiﬁers, A, of regions
that are allowed to change. RRId thus allows the environment to change the
abstract state using any path in the labelled transition system governing the
region, along actions not exclusively owned by the client. RA is deﬁned in Figure
2 in terms of two functions, acts and upds. The acts function speciﬁes the actions
not exclusively owned by the client and the upds function speciﬁes the set of
transitions labelled with actions not exclusively owned by the client.
   Unlike previous models of CAP, this interference relation is expressed entirely
in terms of abstract states and is completely independent of the interpretation
5
    Why? Because then we could not guarantee the existence of guarded recursive predi-
    cates involving higher-order functions (such as the eloop predicate from Section 2.2).
                               Impredicative Concurrent Abstract Predicates       165

of these abstract states. This is why stability in iCAP is also expressed at the
abstract level and why it is much simpler than previous versions of CAP. An
assertion is A-stable if it is closed under RA :
                        stableA(p) = (RA × idAMod )(p) ⊆ p
                                    def




where R(p) = {m ∈ M | ∃m ∈ p. (m, m ) ∈ R}. Intuitively, an assertion is
A-stable if it is closed under interference from the environment on regions in A.
An assertion is thus stable if it is RId-stable.
Erasure. The relation between the instrumented semantics and the concrete se-
mantics is expressed through an erasure function, −A , that maps instrumented
states to sets of concrete states. Like the interference relation, the erasure is in-
dexed by a set of region identiﬁers, A, of regions to erase. The erasure works
by picking a concrete state lr for each allocated region r ∈ A that satisﬁes the
interpretation of the current abstract state of the given region, and composing
all these states with the current local state. The erasure is deﬁned in terms of
a single-region erasure, −r , that deﬁnes the set of concrete states satisfying
the interpretation of the current abstract state of region r. Note that this is ex-
pressed in terms of the application function, app, introduced earlier for unfolding
a region interpretation.
   View shifts describe changes at the instrumented level that preserves the
state at the concrete level. An A-view shift p A q describes a view shift that is
only allowed to modify regions in A. We can express this formally (and build-in
framing) by requiring the view shift to preserve all A-stable frames r:

                     q = ∀r ∈ Prop. stableA(r) ⇒ p ∗ rA ⊆ q ∗ rA
                 A    def
             p
The operational semantics of the underlying programming language is deﬁned in
                                                      a
terms of a labelled thread pool evaluation relation, → , and an action semantics,
                                                        a
[[−]]. The labelled thread pool evaluation relation, →, deﬁnes the local eﬀects
(i.e., stack eﬀects) of executing a single thread for one step of execution, while
the action semantics deﬁnes the global eﬀects (i.e., heap eﬀects) of executing an
atomic action. Atomic satisfaction expresses what it means for an atomic action
a to satisfy a given Hoare speciﬁcation:

             a satA {p} {q} = ∀r ∈ Prop. ∀m ∈ M. ∀h, h ∈ Heap.
                              def



                  m ∈ p ∗ r ∧ h ∈ mA ∧ h ∈ [[a]](h) ∧ stableA (r)
                      ⇒ ∃m ∈ M.  (m ∈ q ∗ r ∧ h ∈ m A )
This is the case, if, executing a from any initial concrete state h in the erasure
of p there exists an abstract state in q that erases to the terminal concrete state
h ∈ [[a]](h), and preserves r, for all stable frames r. Intuitively, the  operator
expresses that executing an atomic action corresponds to one step of execution
in the operational semantics.
   Safety, safe(s, p, q), extends satisfaction from atomic actions to statements s.
Intuitively, it expresses that every step of s at the concrete level has a correspond-
ing step at the abstract level. Formally, safe is deﬁned using guarded recursion to
166      K. Svendsen and L. Birkedal

establish the connection between steps in the underlying operational semantics
and steps in the topos of trees. See the accompanying technical report for the
formal deﬁnition.
Interpretation. Most of the interpretation of iCAP is fairly straightforward
and reduces directly to the topos of trees. For instance, conjunction in iCAP is
interpreted using conjunction in the topos of trees: p∧q = {m ∈ M | m ∈ p∧m ∈
                                                         def


q}. The most interesting case is the interpretation of the region interpretation
assertion, rintr(−):

          rintr(I, r) = {(l, s, ς) ∈ M | r ∈ dom(ς) ∧ ∀x ∈ Δ(SId).
                      def



                        ∀ς  ≥ ς. app(ς(r))(x, ς  ) = (λ(l, s). I(x)(l, s, ς  ))}

Readers familiar with models of ML references may understand this region in-
terpretation assertion by analogy to the ref type constructor of ML, which can
be modelled by a similar equation [2,4].6 The reference type in ML describes a
simple invariant for a single location, which expresses that the values stored at
that location are always of the given type. With iCAP we can describe invariants
given by a protocol and covering a region of memory (varying according to the
protocol).


4      Logic
In the accompanying appendix we introduce a formal proof system for iCAP
and in the accompanying technical report we present the entire proof system.
We stress that the logic contains suﬃcient proof rules for proving all the examples
sketched in this paper, including all stability proofs and all proofs about atomic
instructions!
   In the accompanying technical report we prove that iCAP is sound with re-
spect to the model described in the previous section. As a corollary of this
soundness theorem it follows that if Γ | −  (Δ).{P}s{Q}, then

            ∀ϑ ∈ [[Γ ]]. safe(s, [[Γ ; Δ  P : Prop]](ϑ), [[Γ ; Δ  Q : Prop]](ϑ)).


5      Discussion
We have presented iCAP, the ﬁrst program logic for modular reasoning about
higher-order concurrent imperative programs that supports full impredicative
quantiﬁcation over general predicates, including predicates describing protocols
over shared regions of memory. We have presented examples illustrating how
iCAP supports modular reasoning about internal and external sharing, layered
6
    Think of ς as the world in models of references; then the equation says that, for all
    future worlds, the interpretation of the region recorded in the world agrees with the
    interpretation given by I.
                                Impredicative Concurrent Abstract Predicates        167

and recursive abstractions, and ﬁne-grained concurrent ADTs implemented using
helping, entirely in the logic.
   We have discussed related work on program logics along the way. As an alter-
native to program logics, there has also been several recent advances on using
relational models for reasoning about concurrent programs. In particular, Liang
et. al. [15] presented a simulation relation based on rely-guarantee to verify pro-
gram transformations for a ﬁrst-order concurrent imperative language; Birkedal
et. al. [5] presented a logical relations model for verifying eﬀect-based program
transformations for a higher-order concurrent imperative language, and Turon et.
al. [23,22] extended [5] with an extension of the protocols of Dreyer et. al. [10]
to allow for relational reﬁnement proofs of sophisticated ﬁne-grained concurrent
algorithms, including cooperation. To reason about cooperation, the model and
logic of Turon et. al. [23,22] uses speciﬁcation code (i.e., an expression of the
programming language) as a transferrable resource. This is similar to how view
shifts are transferred here to reason about cooperation; the diﬀerence is that
here we do not use code (since we are not proving reﬁnement), but allow for
transfer of more abstract speciﬁcations given by view shifts. The model in [23]
is deﬁned using step-indexing and involves an indexed deﬁnition of what essen-
tially amounts to a recursively deﬁned space of protocols, similar in spirit to
the one we are using in this paper. However, the model in [23] does not support
impredicative protocols, technically since island predicates (corresponing to re-
gion predicates) in loc. cit. have a restriction on how they can be parameterized.
It is probably possible to lift this restriction, but one would still need a richer
notion of model in order to model impredicative higher-order logic, essentially
since constant sets would no longer suﬃce. As explained earlier, we use the type
theory of the topos of trees as our metatheory for that purpose.
   In this paper we have focused on the foundational issue of establishing sound-
ness of a new very expressive logic for reasoning about higher-order concurrent
imperative programs. Future work includes implementing a tool for interactive
veriﬁcation of programs using iCAP. We plan to do so in Coq, following the
approaches of the Bedrock [6] and Charge! [3] tools, which have been successful
in using Coq tactics to automate large parts of formal reasoning.

Acknowledgements. This research was supported in part by the ModuRes
Sapere Aude Advanced Grant from The Danish Council for Independent Re-
search for the Natural Sciences (FNU).


References
 1. Node.js, http://www.nodejs.org
 2. Appel, A.W., Melliès, P.-A., Richards, C.D., Vouillon, J.: A Very Modal Model of
    a Modern, Major, General Type System. In: Proceedings of POPL (2007)
 3. Bengtson, J., Jensen, J.B., Birkedal, L.: Charge! In: Beringer, L., Felty, A. (eds.)
    ITP 2012. LNCS, vol. 7406, pp. 315–331. Springer, Heidelberg (2012)
168     K. Svendsen and L. Birkedal

 4. Birkedal, L., Møgelberg, R., Schwinghammer, J., Støvring, K.: First Steps in Syn-
    thetic Guarded Domain Theory: Step-Indexing in the Topos of Trees. In: Proceed-
    ings of LICS (2011)
 5. Birkedal, L., Sieczkowski, F., Thamsborg, J.: A Concurrent Logical Relation. In:
    Proceedings of CSL (2012)
 6. Chlipala, A.: Mostly-Automated Veriﬁcation of Low-Level Programs in Computa-
    tional Separation Logic. In: Proceedings of PLDI (2011)
 7. Dinsdale-Young, T., Birkedal, L., Gardner, P., Parkinson, M., Yang, H.: Views:
    Compositional Reasoning for Concurrent Programs. In: Proceedings of POPL
    (2013)
 8. Dinsdale-Young, T., Dodds, M., Gardner, P., Parkinson, M.J., Vafeiadis, V.: Con-
    current Abstract Predicates. In: D’Hondt, T. (ed.) ECOOP 2010. LNCS, vol. 6183,
    pp. 504–528. Springer, Heidelberg (2010)
 9. Dodds, M., Jagannathan, S., Parkinson, M.J.: Modular reasoning for deterministic
    parallelism. In: Proceedings of POPL, pp. 259–270 (2011)
10. Dreyer, D., Neis, G., Birkedal, L.: The Impact of Higher-Order State and Control
    Eﬀects on Local Relational Reasoning. In: Proceedings of ICFP (2010)
11. Feng, X., Ferreira, R., Shao, Z.: On the Relationship between Concurrent Separa-
    tion Logic and Assume-Guarantee Reasoning. In: De Nicola, R. (ed.) ESOP 2007.
    LNCS, vol. 4421, pp. 173–188. Springer, Heidelberg (2007)
12. Gotsman, A., Berdine, J., Cook, B., Rinetzky, N., Sagiv, M.: Local Reasoning for
    Storable Locks and Threads. In: Shao, Z. (ed.) APLAS 2007. LNCS, vol. 4807,
    pp. 19–37. Springer, Heidelberg (2007)
13. Herlihy, M., Shavit, N.: The Art of Multiprocessor Programming. Morgan Kauf-
    mann (2008)
14. Hobor, A., Appel, A.W., Nardelli, F.Z.: Oracle semantics for concurrent separa-
    tion logic. In: Drossopoulou, S. (ed.) ESOP 2008. LNCS, vol. 4960, pp. 353–367.
    Springer, Heidelberg (2008)
15. Liang, H., Feng, X., Fu, M.: A rely-guarantee-based simulation for verifying con-
    current program transformations. In: POPL (2012)
16. O’Hearn, P.W.: Resources, Concurrency and Local Reasoning. Theor. Comput.
    Sci. 375(1-3), 271–307 (2007)
17. Owicki, S.S.: Axiomatic Proof Techniques for Parallel Programs. PhD thesis, Cor-
    nell (1975)
18. Provos, N., Mathewson, N.: libevent – an event notiﬁcation library,
    http://www.monkey.org/~ provos/libevent
19. Russo, C.V.: The Joins Concurrency Library. In: Hanus, M. (ed.) PADL 2007.
    LNCS, vol. 4354, pp. 260–274. Springer, Heidelberg (2007)
20. Svendsen, K., Birkedal, L., Parkinson, M.: Joins: a Case Study in Modular Spec-
    iﬁcation of a Concurrent Reentrant Higher-order Library. In: Castagna, G. (ed.)
    ECOOP 2013. LNCS, vol. 7920, pp. 327–351. Springer, Heidelberg (2013)
21. Svendsen, K., Birkedal, L., Parkinson, M.: Modular Reasoning about Separation
    of Concurrent Data Structures. In: Felleisen, M., Gardner, P. (eds.) ESOP 2013.
    LNCS, vol. 7792, pp. 169–188. Springer, Heidelberg (2013)
22. Turon, A., Dreyer, D., Birkedal, L.: Unifying Reﬁnement and Hoare-Style Reason-
    ing in a Logic for Higher-Order Concurrency. In: Proceedings of ICFP (2013)
23. Turon, A., Thamsborg, J., Ahmed, A., Birkedal, L., Dreyer, D.: Logical Relations
    for Fine-Grained Concurrency. In: Proceedings of POPL (2013)
24. Vafeiadis, V., Parkinson, M.: A Marriage of Rely/Guarantee and Separation
    Logic. In: Caires, L., Vasconcelos, V.T. (eds.) CONCUR 2007. LNCS, vol. 4703,
    pp. 256–271. Springer, Heidelberg (2007)
