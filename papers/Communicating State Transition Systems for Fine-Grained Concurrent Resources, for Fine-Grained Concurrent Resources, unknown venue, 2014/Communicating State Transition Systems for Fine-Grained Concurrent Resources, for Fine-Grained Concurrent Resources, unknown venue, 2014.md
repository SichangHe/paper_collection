              Communicating State Transition Systems
              for Fine-Grained Concurrent Resources

Aleksandar Nanevski1 , Ruy Ley-Wild2 , Ilya Sergey1, and Germán Andrés Delbianco1
                                   1
                              IMDEA Software Institute, Spain
              {aleks.nanevski,ilya.sergey,german.delbianco}@imdea.org
                                  2
                                    LogicBlox, USA
                             ruy.leywild@logicblox.com



         Abstract. We present a novel model of concurrent computations with shared
         memory and provide a simple, yet powerful, logical framework for uniform Hoare-
         style reasoning about partial correctness of coarse- and fine-grained concurrent
         programs. The key idea is to specify arbitrary resource protocols as communicat-
         ing state transition systems (STS) that describe valid states of a resource and the
         transitions the resource is allowed to make, including transfer of heap ownership.
             We demonstrate how reasoning in terms of communicating STS makes it easy
         to crystallize behavioral invariants of a resource. We also provide entanglement
         operators to build large systems from an arbitrary number of STS components,
         by interconnecting their lines of communication. Furthermore, we show how the
         classical rules from the Concurrent Separation Logic (CSL), such as scoped re-
         source allocation, can be generalized to fine-grained resource management. This
         allows us to give specifications as powerful as Rely-Guarantee, in a concise,
         scoped way, and yet regain the compositionality of CSL-style resource manage-
         ment. We proved the soundness of our logic with respect to the denotational se-
         mantics of action trees (variation on Brookes’ action traces). We formalized the
         logic as a shallow embedding in Coq and implemented a number of examples,
         including a construction of coarse-grained CSL resources as a modular composi-
         tion of various logical and semantic components.


1 Introduction

There are two main styles of program logics for shared-memory concurrency, customar-
ily divided according to the supported kind of granularity of program interference. Log-
ics for coarse-grained concurrency such as Concurrent Separation Logic (CSL) [12,14]
restrict the interference to critical sections only, but generally lead to more modular
specifications and simpler proofs of program correctness. Logics for fine-grained con-
currency, such as Rely-Guarantee (RG) [8] admit arbitrary interference, but their spec-
ifications have traditionally been more monolithic, as we shall illustrate. In this paper,
we identify the essential ingredients required for compositional specification of con-
current programs, and combine them in a novel way to reconcile the two approaches.
We present a semantic model and a logic that enables specification and reasoning about
fine-grained programs, but in the style of CSL. To describe our contribution more pre-
cisely, we first compare the relevant properties of CSL and RG.

Z. Shao (Ed.): ESOP 2014, LNCS 8410, pp. 290–310, 2014.
c Springer-Verlag Berlin Heidelberg 2014
       Communicating State Transition Systems for Fine-Grained Concurrent Resources                 291

    CSL employs shared resources and associated resource invariants [13], to abstract
the interference between threads. A resource r is a chunk of shared state, and a resource
invariant I is a predicate over states, which holds of r whenever all threads are outside
the critical section. By mutual exclusion, when a thread enters a critical section for r,
it acquires ownership and hence exclusive access to r’s state. The thread may mutate
the shared state and violate the invariant I, but it must restore I before releasing r and
leaving the critical section, as given by the following CSL rule [2].
                                  Γ  {p ∗ I} c {q ∗ I}
                                                               C RIT S EC CSL
                              Γ, r : I  {p} with r do c {q}

Γ is a context of currently existing resources. The rule for parallel composition assumes
that forked threads don’t share any state beyond that of the resources in Γ, and may
divide the private state of the parent thread disjointly among the children.
                            Γ  {p1 } c1 {q1 }     Γ  {p2 } c2 {q2 }
                                                                        PAR CSL
                                Γ  {p1 ∗ p2 } c1  c2 {q1 ∗ q2 }

A private heap of a thread may be promoted into a freshly allocated shared resource in
a scoped manner by the following rule.
                                     Γ, r : I  {p} c {q}
                                                                    R ESOURCE CSL
                            Γ  {p ∗ I} resource r in c {q ∗ I}

One may see from these rules that resources are abstractions that promote modularity.
In particular, one may verify a thread wrt. the smallest resource context required. By
context weakening, the introduction of new resources will not invalidate the existing
verification. Thread-local resources can be hidden from the environment by the R E -
SOURCE CSL rule.
   In RG, the interaction between threads is directly specified by the rule for parallel
composition.1
                    R ∨ G2 , G1  {p} c1 {q1 }      R ∨ G1 , G2  {p} c2 {q2 }
                                                                                 PAR RG
                              R, G1 ∨ G2  {p} c1  c2 {q1 ∧ q2 }

The rely transition R and guarantee transitions G1 and G2 are relations on states. A
rely specifies the thread’s expectations of state transitions made by its environment.
A guarantee specifies the state transitions made by the thread itself. The disjunctive
combinations of R and G’s in the rule captures the idea we call forking shuffle, whereby
upon forking, the thread c1 becomes part of the environment for c2 and vice-versa.
   RG is more expressive than CSL because transitions can encode arbitrary protocols
on shared state, whereas CSL is specialized to a fixed mutual exclusion protocol on
critical sections. But, CSL is more compositional in manipulating resources. Where a
CSL resource invariant specifies the behavior of an individual chunk of shared state, the
transitions in RG treat the whole state as monolithically shared. Feng’s work on Local
Rely Guarantee (LRG) [5] has made first steps in improving RG in this respect.
 1
     In the presence of heaps, the rule is more complicated [6, 18], but we elide the issue here.
292     A. Nanevski et al.

1.1 Contributions

We propose that a logic for fine-grained concurrency can be based on a notion of a fine-
grained resource. Fine-grained resources serve as buildings blocks for program specifi-
cation, and generalize CSL-style coarse-grained resource management. A fine-grained
resource is specified by a resource invariant, as in CSL, but it also adds transitions in the
form of relations between resource states. Thus, it is best viewed as a state transition
system (STS), where the resource invariant specifies the state space. We identify a num-
ber of properties that an STS has to satisfy to specify a fine-grained resource, and refer
to such STSs as concurroids. We refer to our generalization of CSL as Fine-grained
CSL (FCSL).
    There are two main ideas that we build on in FCSL, and which separate FCSL from
LRG and other recent related work [4,15,17] (see Section 6 for details): (a) subjectivity
and (b) communication. Subjectivity [10] means that each state of a concurroid STS
describes not only the shared resource, but also two abstractions of it that represent the
views of the state by the thread, and by its environment, respectively. Subjectivity will
enable us to capture the idea of forking shuffle by a rule for parallel composition akin to
PAR CSL (but with a somewhat generalized notion of separating conjunction (∗) [10]),
rather than in the monolithic style of PAR RG.
    To compositionally build large systems out of a number of smaller ones, we make
concurroids communicate. In addition to standard for STS internal transitions between
states, concurroids contain external transitions. These may be thought of as “wires”
whose one end is connected to a state in the STS, but whose other end is dangling,
representing either an “input” into or an “output” out of the STS. Concurroids can be
entangled, i.e., composed by interconnecting their dangling wires of opposite polar-
ity, where the interconnections serve to transfer heap ownership between concurroids.
Communication and entanglement endow FCSL with the compositionality of CSL. For
example, entanglement generalizes the notion of adding a resource to the context Γ in
R ESOURCE CSL. We also rely on entanglement to formulate a rule generalizing the
scoped resource allocation of R ESOURCE CSL. More precisely, our contributions are:

 – We identify STSs with subjectively-shaped states (concurroids) and a number of
   algebraic properties, as a natural model for scalable concurrency verification. We
   show how communication enables composing larger STSs out of smaller ones.
 – We present FCSL—a simple and expressive logic for fine-grained resources that
   combines expressivity of RG with the compositional resource management of CSL.
 – We illustrate FCSL by showing how to implement a coarse-grained resource of
   CSL by a fine-grained resource of FCSL in which an explicit spin lock protects the
   resource’s state. We also implemented examples such as ticketed locks, that go be-
   yond coarse-grained CSL resources, and present them in the extended version [11].
 – We implemented FCSL [11] as a shallow embedding within the type theory of the
   Calculus of Inductive Constructions (i.e., Coq [1, 16]). Thus, FCSL naturally rec-
   onciles with features such as higher-order functions, abstract predicates, modules
   and functors. We formally instantiated the whole stack of abstractions: the semantic
   model is formalized in Coq, FCSL is built on top of the semantic model, CSL is
   built on top of FCSL, and then verified programs are built on top of CSL.
       Communicating State Transition Systems for Fine-Grained Concurrent Resources             293

2 An Overview of Fine-Grained Resources

There are three different aspects along which fine-grained resources can be composed:
space (i.e., states), ownership, and time (i.e., transitions). In this section, we describe
how to represent these aspects in the assertion logic of FCSL.


Space. The heap belonging to a fine-grained resource,2 is explicitly identified by a
resource label. We use assertions in the “points-to” style of separation logic, to name
resources and identify their respective heaps. For example, the assertion
                                            j           j
                                        1 → h1 ∗ 2 → h2

describes a state in which the heaps h1 and h2 are associated with the resources labeled
1 and 2 , respectively. The connective ∗ ensures that 1 and 2 are distinct labels, and
that h1 and h2 are disjoint heaps. The superscript j indicates that the heaps are joint
(shared), i.e., can be accessed by any thread, even though they are owned by the re-
sources 1 and 2 , respectively.
   The heaps h1 and h2 are not described by means of points-to assertions, but are built
                                                              · For example, the heap of
using operators for singleton heaps x  v and disjoint union ∪.
the resource lock, which explicitly encodes a coarse-grained resource with the resource
invariant I [12] may be described by the assertion
                           j
                     lock → ((lk  b) ∪· h) ∧ if b then h = empty else I h.                    (1)

The assertion exposes the fact that the heap owned by lock contains a boolean pointer lk
encoding a lock that protects the heap h. The conditional conjunct is a pure (i.e., label-
free) assertion, which describes an aspect of the ownership transfer protocol of CSL.
When the lock is not taken (i.e. b = false), the heap h satisfies the resource invariant.
When the lock is taken, the heap is transfered to the private ownership of the locking
thread, so h equals the empty heap, but lk remains in the ownership of lock.


Ownership. Data in FCSL may be owned by a resource, as illustrated above, or by
individual threads. The thread-owned data, however, is also associated with a resource,
which it refines with thread-relative information. For example, the resource lock owns a
pointer lk which operationally implements a lock. However, just knowing that the lock
is taken or not is not enough for reasoning purposes; we need to know which thread
has taken it, if any. Thus, we associate with each thread an extra bit of lock-related
information, Own or       
                         Own, which will identify the lock-owning thread as follows.
    Following the idea of subjectivity [10], FCSL assertions are interpreted in a thread-
relative way. We use self to name the interpreting thread, and other to name the combi-
nation of all other threads running concurrently with self (i.e., the environment of self ).
                                                                           s         o
We use two different assertions to describe thread-relative views:  → v and  → v. The
first is true in the self thread, if self ’s view of the resource  is v. The second is true in
 2
     Or just resource for short. Later on, we explicitly identify CSL resources as coarse-grained.
294       A. Nanevski et al.

                                                                              j
the self thread, if other’s view of the resource  is v. In this sense, the  → v describes
the resource’s view of the data. In the case of lock, the thread that acquired the lock will
validate the assertion:
                                    s              j
                               lock → Own ∧ lock → (lk  true),

while the symmetric assertion holds in all other threads at the same moment of time:
                                    j                      o
                               lock → (lk  true) ∧ lock → Own.

In general, the values of the self and other views for any resource are elements of
some resource-specific partial commutative monoid (PCM) [10]. A PCM is a set with
a commutative and associative operation • with a unit element. • combines the self
and other views into a view of the parallel composition of self and other threads. The
• operation is commutative and associative because parallel composition of threads is
commutative and associative, and the unit element models the view of the idle thread.
Partiality models impossible thread combinations. For example, the elements of O =
{
 Own, Own} represent thread-relative views of the lock lk. O forms a PCM under the
    
operation defined as x • Own=
                                    
                                   Own • x = x, with Own • Own undefined. The unit
element is   
              
           Own, and the undefinedness of the last combination captures that two threads
can’t simultaneously own the lock. Notice that heaps form a PCM under disjoint union,
with the empty heap as unit. Thus, they too obey the discipline required of the general
self and other components.
    Anticipating lock-related examples in Section 3, we combine thread-relative views
of the lock with thread-relative views of the lock-protected heap h. We parametrize the
resource lock by a PCM U, which the user may choose depending on the application.
                                                     s                   o
Then we use assertions over pairs, such as lock → (mS , aS ) and lock → (mO , aO ), to
express that mS , mO ∈ O are views of the lock lk, and aS , aO ∈ U are views of the
heap h. The following assertion illustrates how the different FCSL primitives combine.
It generalizes (1) and defines the valid states of the resource lock.
                s                   o                  j
          lock → (mS , aS ) ∧ lock → (mO , aO ) ∧ lock → ((lk  b) ∪· h) ∧            (2)
          if b then h = empty ∧ mS • mO = Own else I (aS • aO ) h ∧ mS • mO = 
                                                                              Own

The assertion states that if the lock is taken (b = true) then the heap h is given away,
otherwise it satisfies the resource invariant I. In either case, the thread-relative views
mS , mO , aS and aO are consistent with the resource’s views of lk and h. Indeed, notice
how mS , mO and aS , aO are first •-joined (by the •-operations of O and U, respectively)
and then related to b and h; the former implicitly by the conditional, the latter explicitly,
by the resource invariant I, which is now parametrized by aS • aO .

Private heaps. In addition to a private view of a resource, a thread may own a pri-
vate heap as well. We describe such thread-private heaps by means of the same thread-
relative assertions, but with a different resource label. We consider a dedicated resource
                                                                                 s
for private heaps, with a dedicated label priv. Then we can write, say, priv → x  4
to describe a heap consisting of a pointer x private to the self thread. By definition,
      j
priv → empty, i.e., the joint heap of the priv resource is always empty.
       Communicating State Transition Systems for Fine-Grained Concurrent Resources                 295

Time. Fine-grained reasoning requires characterization of the possible changes the
threads can make to the state. We encode such a characterization as relations between
states of possibly multiple resources (i.e., using multiple labels). For example, coarse-
grained resources require that upon successful acquisition, the resource’s heap is trans-
fered into the private ownership of the acquiring thread. In our fine-grained encoding,
the transition can be represented as follows:
                    s
               priv → hS
                                         s
                                ∗ (lock → (, aS ) ∧ lock → ((lk  false) ∪· h)) 
                                            Own
                                                                j

                    s                    s                      j                                    (3)
               priv → (hS ∪· h) ∗ (lock → (Own, aS ) ∧ lock → (lk  true))

This transition preserves heap footprints, in the sense that the domain of the combined
heaps in the source of the transition equals the domain in the target of the transition. We
refer to such transitions as internal. Footprint preservation is an essential property, as it
facilitates composing and framing transitions. In particular, adding additional labels and
heaps with non-overlapping footprint to a source of an internal transition is guaranteed
to produce non-overlapping footprints in the target of the transition as well.
   We also consider external transitions that can acquire and release heaps. We use
external transitions to build internal ones. For example, the above internal transition
over priv and lock resources can be obtained as an interconnection (to be defined in
Section 4) of two external transitions, each operating on an individual label.
                                                  s     +h          s
                                             priv → hS  priv → (hS ∪· h)
           s
     lock → (, aS ) ∧ lock → ((lk  false) ∪· h)  lock → (Own, aS ) ∧ lock → lk  true
              Own
                                j                       −h          s                   j

                                                                                                      (4)
The transition over priv takes a heap h as an input and attaches it to the self heap.
The transition over lock gives the heap h as an output. When interconnected, the two
transitions exchange the ownership of h between the lock and priv, producing (3).
   A concurroid is an STS that formally represents a collection of resources. Each state
of the STS contains a number of components, identified by the labels naming the in-
dividual resources. Each concurroid contains one internal transition, and an arbitrary
number of external ones. The internal transition describes how threads specified by the
concurroid may change their state in a single step. The external transitions are the “dan-
gling wires”, which provide means for composing different concurroids by entangling
them, i.e., interconnecting (some or all of) their dually polarized external transitions, to
obtain a larger concurroid.
   For example, if P is the concurroid for private heaps (containing a single label priv),
and L{lock,lk,I} is the concurroid for a lock (with a single label lock, lock pointer lk and
protected heap described by the coarse-grained resource invariant I), we could con-
struct the entangled concurroid CSL{lock,lk,I} = P  L{lock,lk,I} that captures the heap
ownership-exchange protocol (3) of CSL for programs with one coarse-grained re-
source.3 The entanglement can be iterated, to obtain an STS for two coarse-grained
resources CSL{lock,lk,I},{lock ,lk ,I } = CSL{lock,lk,I}  L{lock ,lk ,I } , and so on. In this way, con-
curroids generalize the notion of resource context from the R ESOURCE CSL rule, with
entanglement modeling the addition of new resources to the context.
 3
     The formal definition of the  is postponed until Section 4.
296      A. Nanevski et al.

Fig. 1. Semantics of selected FCSL assertions
           w |=        iff always
                   s
           w |=  → v iff valid w, and w. s =   v
                   j
           w |=  → h iff valid w, and w. j =   h
                   o
           w |=  → v iff valid w, and w. o =   v
           w |= p ∧ q iff w |= p and w |= q
           w |= p ∗ q iff valid w, and w = w1 ∪· w2 , and w1 |= p and w2 |= q
           w |= p −−∗ q iff for every w1 , valid w ∪· w1 and w1 |= p implies w ∪· w1 |= q
           w |= p  q iff valid w, and w. s = s1 ∪· s2 , and
                            [s1 | w. j | s2 ◦ w. o] |= p and [s2 | w. j | s1 ◦ w. o] |= q
           w |= this w if w = w
             |= p ↓ h iff for every valid w, w |= p implies w = h



3 Reasoning with Concurroids
Auxiliary Definitions. A PCM-map is a finite map from labels (isomorphic to nat)
to ΣU:pcm U. It associates each label with a pair of a PCM U and a value v ∈ U. A
heap-map is a finite map from labels to heaps. If m1 , m2 are PCM-maps, then m1 ◦ m2
is defined as empty ◦ empty = empty, and (( U v1 ) ∪· m1 ) ◦ (( U v2 ) ∪· m2 ) =
( U v1 • v2 ) ∪· (m1 ◦ m2 ), and undefined otherwise. By overloading the notation, we
define state w as a triple [s | j | o], where s, o are PCM-maps, and j is a heap-map. We
abbreviate [  v s |   v j |   vo ] with   [v s | v j | vo ]. w is valid if w. s, w. j, w. o
have the same domain as PCM-maps, w. s ◦ w. o is defined, and the heaps in w. s, w. j
and w. o are disjoint (if w. s and w. o contain heaps in their codomain). State flattening
w is the disjoint union of all such heaps. w1 ∪· w2 is the pairwise disjoint union of
component maps of w1 and w2 . The semantics of the main FCSL assertions is provided
                                                        s
in Figure 1. The subjective assertions (e.g., w |=  → v) constrain the value of one state
component, assuming others to be existentially quantified over.
   FCSL specifications take the form of Hoare 4-tuple {p} c {q}@U expressing that the
thread c has a precondition p, postcondition q, in a state space and under transitions
defined by the concurroid U, which in FCSL takes the role of a resource context from
CSL. We next present the characteristic inference rules of FCSL.
Parallel Composition. The rule for parallel composition in FCSL is similar to PAR CSL,
with Γ replaced by a concurroid U, which we will define formally in Section 4.

                              {p1 } c1 {q1 }@U    {p2 } c2 {q2 }@U
                                                                     PAR
                                {p1  p2 } c1  c2 {q1  q2 }@U

The PAR rule uses subjective separating conjunction  (see [10] and Figure 1) to split
the state of c1  c2 into two. The split states contain the same labels, and equal joint
portions, but the self and other portions are recombined to match the thread-relative
views of c1 and c2 . When the parent thread forks the children c1 and c2 , the PCM values
in the parent’s self components are split between the children (similarly ∗ splits heaps in
CSL), while the children’s other component are implicitly induced to preserve overall
      Communicating State Transition Systems for Fine-Grained Concurrent Resources                       297

•-total (i.e., c1 ’s other view includes c2 ’s self view, and vice versa). For example, in the
case of one label , we have
                  s               o                   s         o                s           o
              → a • b ∧  → c =⇒ ( → a ∧  → c • b)  ( → b ∧  → c • a).
The implication encodes the idea of a forking shuffle from RG, but via states, rather than
transitions as in RG. It allows us to use the same concurroid U to specify the transitions
of both c1 and c2 in PAR, much like PAR CSL uses the same context Γ. Essentially, we
rely on the recombination of views to select the transitions of U available to each of c1
and c2 , instead of providing distinct transitions for c1 and c2 as in PAR RG.
   We commonly encounter cases where the other views are existentially abstracted,
                            o
hence the conjuncts  → − are omitted. In those cases, we have the simplified
bi-implication:
                                 s                 s        s
                               → a • b ⇐⇒  → a   → b                             (5)
The implications generalize to -separated assertions with more than one distinct label.
   We illustrate PAR and  with the example of concurrent incrementation [10, 13] in a
setting of a concurroid CSLlock,lk,I (i.e., private state and one lock). The lock lk protects
a shared integer pointer x, that is, the resource invariant is I (a : nat) (h : heap)     =
h = x  a. For the nat argument, we chose the PCM structure under addition; thus, an
                s
assertion lock → (−, aS ) expresses that the self thread has added aS to x, and dually for
      o
lock → (−, aO ). Therefore, whenever the lock is not taken, x stores the sum aS + aO .
This follows from interpreting • with + in the lock state invariant (2).
   Procedure incr(n) acquires the lock to ensure exclusive access to x, increments x by
n, and releases the lock. In FCSL, it has the following specification:
                                                                                              
         s
   priv → empty ∗ lock → (, 0) incr(n) priv → empty ∗ lock → (
                              s
                            Own
                                                                    s
                                                                     , n) @CSLlock,lk,I
                                                                    Own
                                                                                     s



The specification states that incr runs in an empty private heap (hence by framing, in
any larger heap), the lock is not owned by the calling thread initially, and will not be
owned in the end. The addition of calling thread to x increases from 0 to n (hence by
framing, from m to m + n). We now prove that incr(i)  incr( j) increments x by i + j.
                                                                            
                                                  s
                                          priv → empty ∗ lock → (, 0)
                                                                   Own
                                                                        s

                                                                                        
                                  s
                          priv → empty ∪· empty ∗ lock → (•
                                                            Own  , 0 + 0)
                                                                Own
                                                                    s

                                                                                      
                      s               s
              (priv → empty ∗ lock → (  , 0))  (priv →
                                          Own
                                                           s                s
                                                              empty ∗ lock → (, 0))
                                                                               Own
                                                                                    
                        s               s
                priv → empty ∗ lock → (  , 0) priv →
                                          Own
                                                            s                s
                                                              empty ∗ lock → ( , 0)
                                                                               Own

                             incr(i)                                     incr( j)                 
                      s
                priv → empty ∗ lock → ( , i)
                                         Own
                                              s           s               s
                                                    priv → empty ∗ lock → ( , j)
                                                                             Own
                                                                                    
                      s               s
               (priv → empty ∗ lock → (, i))  (priv → empty ∗ lock → (
                                         Own
                                                          s               s
                                                                              , j))
                                                                             Own
                                                                                
                                              s
                                      priv → empty ∗ lock → (, i + j)
                                                                s
                                                               Own

The proof uses the bi-implication (5) to move between -separated assertions and •-
joined views. The proof is compositional in the sense that the same verification of incr
is used as a black box in both parallel threads, with the subproofs merely instantiating
the parameter n with i and j respectively.
298        A. Nanevski et al.

Injection. The PAR rule requires c1 and c2 to share the same concurroid U, which
describes the totality of their resources. If the threads use different concurroids, they
first must be brought into a common entanglement, via the rule I NJECT.

                                           {p} c {q}@U                 r stable under V
                                                                                              I NJECT
                                            {p ∗ r} inject c {q ∗ r}@U  V

If c is verified wrt. concurroid U, it can be injected (i.e. coerced) into a larger concur-
roid U  V. In programs, we use the explicit coercion inject to describe the change of
“type” from U to U  V. Reading the rule bottom-up, it says we can ignore V, as V’s
transitions and c operate on disjointly-labeled state. V may change U’s state by commu-
nication, but the change is bounded by U’s external transitions. Thus, we are justified
in verifying c against U alone. In this sense, I NJECT may be seen as generalizing the
rule for resource context weakening of CSL.
   The connective ∗ splits the state according to labels of U and V; p and q describe
the part labeled by U, and r describes the part labeled by V. Since r describes both the
prestate and poststate, it has to be stable [11] under V; that is, determine a subset of V’s
states that remains fixed under transitions the other thread takes over the labels from V.
   We illustrate I NJECT and stability by verifying incr. To set the stage, we need atomic
commands for reading from and writing to a pointer x. These have the following obvi-
ous specification relative to the concurroid P for private state:
                                  s
                                                                         s
                                                                                                   
                            priv → x  v             read x       priv → x  v ∧ res = v @P
                                  s
                                                                         s
                                                                                     
                            priv → x  − write x v priv → x  v @P

The commands for acquiring and releasing lock exchange ownership of the protected
pointer x. Thus, they have specifications relative to the concurroid CSLlock,lk,I = P 
Llock,lk,I , which we have already used before.
                                                                                         
                                                  s
                                           priv → empty ∗ lock → (, 0)
                                                                    Own
                                                                            s


                                              acquire                    
                          s                 s                  o
               ∃aO .priv → x  aO ∗ (lock → (Own, 0) ∧ lock → (−, aO )) @CSLlock,lk,I
                             s                                    s                           o
                                                                                                        
                     priv → x  aS + aO ∗ (lock → (Own, 0) ∧ lock → (−, aO ))

                                                          release               
                                       s
                                 priv → empty ∗ lock → (, aS ) @CSLlock,lk,I
                                                          Own
                                                               s



acquire assumes that lock is not taken, and that the self thread so far has added 0 to x.
Thus, the overall contents of x is 0 + aO = aO , where aO is the addition of the other
threads. Note that acquire does not have to be atomic:4 as implemented, it just spins
on lk, and after acquisition, x is transferred into the private heap of self . aO must be
existentially quantified, because other’s may add to x while acquire is spinning.
 4
     The implementation of acquire and release relies on atomic actions (Section 5), specific for a
     particular concurroid, e.g. CSLlock,lk,I .
       Communicating State Transition Systems for Fine-Grained Concurrent Resources            299

   release assumes that lock is taken by self , and that prior to taking lock, self and other
have added 0 and aO to x, respectively. After acquiring x, self has mutated it, so that its
contents is aS + aO . After releasing, x is moved from the private heap to the joint portion
of lock. The postcondition does not mention x, as once in joint, x’s contents becomes
unstable. Indeed, other may acquire the lock and change x after release terminates.
However, other can’t change the self view of x, which is now set to aS .
   The following proof outline presents the implementation and verification of incr(n).
                                                
                     s                 s
               priv → empty ∗ lock → (, 0)
                                        Own
              acquire
                     ;                                                      
                          s                 s                    o
               ∃aO .priv → x  aO ∗ (lock → (Own, 0) ∧ lock → (−, aO ))
              res ← injects (read x);                  s                  o
                                                                                       
                ∃aO .priv → x  aO ∧ res = aO ∗ (lock → (Own, 0) ∧ lock → (−, aO ))
              inject (write x (res + n));                                      
                           s                     s                  o
                ∃aO .priv → x  n + aO ∗ (lock → (Own, 0) ∧ lock → (−, aO ))
              release
                                                
                     s                 s
               priv → empty ∗ lock → (, n)
                                        Own

I NJECT is used twice, to coerce read and write from the concurroid P to CSLlock,lk,I .
These commands manipulate the contents of priv, but retain the framing predicate
       s                       o
lock → (Own, 0) ∧ lock → (−, aO ). This predicate is stable wrt. Llock,lk,I . Intuitively,
because self owns lock, other can’t acquire x and add to it. Thus, no matter what other
does, aO and the framing predicate remain invariant.
   To simplify the proof, we have not emphasized the invariance of aO between calls
to acquire and release, even though it is the case (we could do it using the rule E XIST
from Figure 2). However, this invariance is what allowed us to calculate the contribution
of self to x as n (i.e., final contents of x minus aO ). Without tracking aO , we would not
know how much of the final contents of x is attributable to self , and how much to other.
Hiding. refers to the ability to construct a concurroid V from the thread-private heap,
in a scope of a thread c. The children forked by c can interfere on V’s state, respecting
V’s transitions, but V is hidden from the environment of c. To the environment, V’s state
changes look like changes of the private heap of c. In this sense, hiding generalizes the
R ESOURCE CSL rule to fine-grained resources.
         s
                            s
                                   
     priv → h ∗ p c priv → h ∗ q @(P  U)  V         (omitted side condition on U and V)
                                                                                              H IDE
              {Ψ g h ∗ (Φ (g) −−∗ p)} hideΦ,g c {∃g .Ψ g h ∗ (Φ (g ) −−∗ q)}@P  U
                                                          s
                         where Ψ g h = ∃k:heap. priv → h ∪· k ∧ Φ (g) ↓ k
Since installing V consumes a chunk of private heap, the rule requires the overall con-
curroid to support private heaps, i.e., to be an entanglement P  U, where P is the
concurroid for private heaps, and U is arbitrary (it is also possible to generalize the rule
so as to be not tied to the specific concurroid P, see [11]). The omitted side condition
on U and V is essential for the existence of entanglement and will be explained in Sec-
tion 5. When U is of no interest, we set it to the empty concurroid E (Section 4), for
which P  E = P.
300        A. Nanevski et al.

   In programs, we use the explicit coercion hideΦ,g to indicate the change of type from
(P  U)  V to P  U. The annotation Φ(g) corresponds to a set of concrete states of
a concurroid V to be created. Its parameter g is a meaningful abstraction of such a set
(e.g., (mS , aS ) for the L{lock,lk,I} concurroid) and can be thought of as an “abstract state”.
In the rule H IDE, g is the initial abstract state, i.e., upon creation, the state of V satisfies
                                                                    s
Φ (g). In the premise of the H IDE rule, the predicates priv → − describe the behavior
of c on the private heaps, while p and q describe the state of the labels belonging to U
and V. In the conclusion, Ψ g h and Ψ g h map the abstract states g and g into private
heaps h and h . This follows from the definition of Ψ , in which Φ (g) ↓ k indicates that
states satisfying Φ (g) erase to the private heap k (see Figure 1). Thus, changes that c
imposes on abstract states, appear as changes to private heaps for hideΦ,g c.
   In the conclusion, the assertion Φ (g) −−∗ p states that attaching any state satisfying
Φ (g) to the chunk of the initial state identified by the labels from U produces a state in
which p holds, “compensating” for the component k in Ψ . That is, p corresponds to an
abstract state g and c can be safely executed in such a state. The rule guarantees that if
c terminates with a postcondition q, then q corresponds to some abstract state g .
   We illustrate the rule with a proof outline for program hideΦ,g (incr(n)). We show
how to choose Φ and g so that the program implements the following functionality. It
starts with only the concurroid P, and the private heap containing pointers lk and x. It
locally installs Llock,lk,I , which makes x a shared pointer, protected by the lock lk. It runs
incr(n), after which the local concurroid is disposed, and lk and x return to the private
heap. We prove that if initially x  0, then in the end x  n. The abstract states are
pairs (mS , aS ), encodings of the self views of the concrete state of lock. Φ maps a self
view into a predicate on the full state of lock, specifying joint and other views as well.
                        s                    o
  Φ (mS , aS ) = lock → (mS , aS ) ∧ lock → (, 0) ∧
                                               Own
                   if mS =  then lock → ((lk  false) ∪· (x  aS )) else lock → (lk  true)
                           Own
                                             j                                         j



We choose the initial state g = (mS , aS ) = (    , 0): indicating that the lock is installed
                                                   
                                                 Own
with lk unlocked, and x set to 0.
   The proof outline uses the facts that Φ (      , aS ) ↓ lk  false ∪· x  aS , and thus
                                                   
                                                 Own
Ψ (  
                              s                                                   s
    Own, aS ) empty = priv → lk  false ∪· x  0. Also, Φ (mS , aS ) −−∗ lock → (mS , aS )
is equivalent to (mS , aS ) = (mS , aS ) in the label-free state.
              s
                                     
        priv → lk  false ∪· x  0 @P
              , 0) empty}@P
        (
       {Ψ  Own                                                     
        Ψ (
           Own, 0) empty ∗ (Φ (Own, 0) −−∗ lock →
                                                    s
                                                        (
                                                         Own , 0)) @P (= P  E)
                                                          
       hideΦ,(,0)  priv →
                          
                            s
                              empty ∗ lock →
                                           
                                             s
                                               ( 
                                                 Own  , 0)  @CSLlock,lk,I (= P  E  Llock,lk,I )
              Own

                       (n)
                      incr                                 
                            s
                       priv → empty ∗ lock → (, n) @CSLlock,lk,I
                                                 s
                                                Own
                                                   
                                          s
        ∃g2 .Ψ g2 empty ∗ (Φ g2 −−∗ lock → (, n)) @P
                                             Own
              , n) empty}@P
        (
       {Ψ  Own                     
              s
        priv → lk  false ∪· x  n @P
     Communicating State Transition Systems for Fine-Grained Concurrent Resources                  301

The soundness of H IDE depends on a number of semantic properties of Φ [11]. The
most important one is that states in the range of Φ have fixed other views for every label
 of V; equivalently, that environment threads for the program hideΦ,g1 c do not interfere
with c on the states of V: all interference on V is hidden within the hide-section.
                                o                                o
            if w1 |= Φ g1 ∧ ( → v1 ∗ ) and w2 |= Φ g2 ∧ ( → v2 ∗ ) then v1 = v2
                                         o
Concretely for our example, Φ g ∧ (lock → v) implies v = (, 0), thus the above
                                                           Own
property clearly holds.


4 Concurroids Abstractly

A concurroid is a 4-tuple V = (L, W, τ, E) where: (1) L is a set of labels, where a label
is a nat; (2) W is the set of states, each state w ∈ W having the structure described in
Section 3; (3) τ is the internal transition, which is a relation on W; (4) E is a set of pairs
(α, ρ), where α and ρ are external transitions of V. An external transition is a function,
mapping a heap h into a relation on W. The components must satisfy a further set of
requirements, discussed next.
State Properties. Every state w ∈ W is valid as defined in Figure 1, and its label
footprint is L, i.e. dom (w. s) = dom (w. j) = dom (w. o) = L. Additionally, W
satisfies the property:

     Fork-join closure: ∀t:PCM-map. w t ∈ W ⇐⇒ w t ∈ W,
                        where w t = [t ◦ w. s | w. j | w. o], and w t = [w. s | w. j | t ◦ w. o]

The property requires that W is closed under the realignment of self and other com-
ponents, when they exchange a PCM-map t between them. Such realignment is part
of the definition of , and thus appears in proofs whenever the rule PAR is used, i.e.
whenever threads fork or join. Fork-join closure ensures that if a parent thread forks in
a state from W, then the child threads are supplied with states which also are in W,
and dually for joining.
Transition Properties. A concurroid transition γ is a relation on W satisfying:

     Guarantee: (w, w ) ∈ γ =⇒ w. o = w . o
     Locality: ∀t:PCM-map. w. o = w . o =⇒ (w t, w              t) ∈ γ =⇒ (w t, w        t) ∈ γ

Guarantee restricts γ to only modify the self and joint components. Therefore, γ de-
scribes the behavior of a viewing thread in the subjective setting, but not of the thread’s
environment. In the terminology of Rely-Guarantee logics [5, 6, 8, 18], γ is a guarantee
relation. To describe the behavior of the thread’s environment, i.e. obtain a rely relation,
we merely transpose the self and other components of γ:

               γ = {(w1 , w2 ) | (w1 , w2 ) ∈ γ}, where w = [w. o | w. j | w. s].

In this sense, FCSL transitions always encode both guarantee and rely relations.
302        A. Nanevski et al.

   Locality ensures that if γ relates states with a certain self components, then γ also
relates states in which the self components have been simultaneously framed by a PCM-
map t, i.e., enlarged according to t. It thus generalizes the notion of locality from sepa-
ration logic [14], with a notable difference. In separation logic, the frame t materializes
out of nowhere, whereas in FCSL, t has to be appropriated from other; that is, taken out
from the ownership of the environment.
   An internal transition τ is a transition which is reflexive and preserves heap foot-
prints. An acquire transition α, and a release transition ρ are functions mapping heaps
to transitions which extend and reduce heap footprints, respectively, as formalized be-
low. An external transition is either an acquire or a release transition. If (α, ρ) ∈ E, then
α is an acquire transition, and ρ is a release transition.

         Footprint preservation: (w, w ) ∈ τ =⇒ dom w = dom w 
         Footprint extension:    ∀h:heap. (w, w ) ∈ (α h) =⇒ dom (w ∪· h) = dom w 
         Footprint reduction:    ∀h:heap. (w, w ) ∈ (ρ h) =⇒ dom (w  ∪· h) = dom w

Internal transitions are reflexive so that programs specified by such transitions may be
idle (i.e., transition from a state to itself). Footprint preservation requires internal tran-
sitions to preserve the domains of heaps obtained by state flattening. Internal transitions
may exchange the ownership of subheaps between the self and joint components, or
change the contents of individual heap pointers, or change the values of non-heap (i.e.,
auxiliary) state, which flattening erases. However, they cannot add new pointers to a
state or remove old ones, which is the task of external transitions, as formalized by
Footprint extension and reduction.
Example 1 (The concurroid for private state). P = ({priv}, WP , τP , {(αP , ρP )}), with
                                                                               
      WP              =   priv  [hS | empty | hO ] | hS and hO disjoint heaps , and
      (w, w ) ∈ τP   ⇐⇒ w. s = priv  hS , w . s = priv  hS , dom hS = dom hS , w. o = w . o
      (w, w ) ∈ αP h ⇐⇒ w. s = priv  hS , w . s = priv  hS ∪· h, w. o = w . o
      (w, w ) ∈ ρP h ⇐⇒ w. s = priv  hS ∪· h, w . s = priv  hS , w. o = w . o

The internal transition admits arbitrary footprint-preserving change to the private heap
hS , while the acquire and release transitions simply add and remove the heap h from hS .

Example 2 (The concurroid for a lock). Llock,lk,I = ({lock}, WL , τL , {(αL , ρL )}), with
WL = { w | w |= assertion (2) }, and (assuming w. o = w . o everywhere):

         (w, w ) ∈ τL   ⇐⇒ w = w
         (w, w ) ∈ αL h ⇐⇒ w. s = lock  (Own, aS ), w. j = lock  (lk  true),
                           w . s = lock  (, a ), w . j = lock  ((lk  false) ∪· h)
                                           Own
                                            , aS ), w. j = lock  ((lk  false) ∪· h),
                                                 S
         (w, w ) ∈ ρL h ⇐⇒ w. s = lock  (Own
                           w . s = lock  (Own, aS ), w . j = lock  (lk  true)

The internal transition admits no changes to the state w. The αL transition corresponds
to unlocking, and hence to the acquisition of the heap h. It flips the ownership bit from
Own to Own, the contents of the lk pointer from true to false, and adds the heap h to
           
the resource state. The ρL transition corresponds to locking, and is dual to αL . When
locking, the ρL transition keeps the auxiliary view aS unchanged. Thus, the resource
     Communicating State Transition Systems for Fine-Grained Concurrent Resources                            303

“remembers” the auxiliary view at the point of the last lock. Upon unlocking, the αL
transition changes this view into aS , where aS is some value that is coherent with the
acquired heap h, i.e., which makes the resource invariant I (aS • aO ) h hold, and thus,
the whole state belongs to WL .

Entanglement. Let U = (LU , WU , τU , EU ) and V = (LV , WV , τV , EV ), be concur-
roids. The entanglement U  V is a concurroid with the label component LUV =
LU ∪ LV . The state set component combines the individual states of U and V by union-
ing their labels, while ensuring that the labels contain only non-overlapping heaps.

             WUV = {w ∪· w | w ∈ WU , w ∈ WV , and w disjoint from w }

To define the transition components of U  V, we first need the auxiliary concept of
transition interconnection. Given transitions γU and γV over WU and WV , respectively,
the interconnection γ1 γ2 is a transition on WUV which behaves as γU (resp. γV ) on
the part of the states labeled by U (resp. V).

       γ1     γ2 = {(w1 ∪· w2 , w1 ∪· w2 ) | (wi , wi ) ∈ γi , w1 ∪· w2 , w1 ∪· w2 ∈ WUV }.
The internal transition of U  V is defined as follows, where idU is the diagonal of WU .
                                                         
  τUV = (τU      idV ) ∪ (idU   τV ) ∪                                          (αU h   ρV h) ∪ (αV h   ρU h).
                                          h, (αU , ρU ) ∈ EU , (αV , ρV ) ∈ EV


Thus, U  V steps internally whenever U steps and V stays idle, or when V steps and
U stays idle, or when there exists a heap h which U and V exchange ownership over by
synchronizing their external transitions.
Example 3. The transitions α p of P and ρL of Llock,lk,I have already been described in
display (4) of Section 2, but using assertions, rather than semantically. The display (3)
of Section 2 presents the interconnection αP h ρL h, which moves h from Llock,lk,I to
P, and is part of the definition of τPLlock,lk,I . The latter further allows moving h in the
opposite direction (αL h ρP h), independent stepping of P (τP idL ) and of Llock,lk,I
(idP τL ).
   The external transitions of U  V are those of U, framed wrt. the labels of V.

               EUV = {(λh. (αU h)           idV , λh. (ρU h)            idV ) | (αU , ρU ) ∈ EU }

We note that EUV somewhat arbitrarily chooses to frame on the transitions of U rather
than those of V. In this sense, the definition interconnects the external transitions of
U and V, but it keeps those of U “open” in the entanglement, while it “shuts down”
those of V. The notation U  V is meant to symbolize this asymmetry. The asymmetry
is important for our example of encoding CSL resources, as it enables us to iterate the
(non-associative) addition of new resources as ((P  Llock1 ,lk1 ,I1 )  Llock2 ,lk2 ,I2 )  · · · while
keeping the external transitions of P open to exchange heaps with new resources.
    Clearly, many ways exist to interconnect transitions of two concurroids and select
which transitions to keep open. In our implementation, we have identified several opera-
tors implementing common interconnection choices, and proved a number of equations
304        A. Nanevski et al.

and properties about them (e.g., all of them validate an instance of the I NJECT rule). We
also show a version of the I NJECT rule with a different operator () [11]. However, as
none of these operators is needed for the examples in this paper, we omit them.
Lemma 1. U  V is a concurroid.
We can also reorder the iterated addition of lock concurroids.
Lemma 2 (Exchange law). (U  V)  W = (U  W)  V.
   We close the section with the definition of the concurroid E which is the right unit
of the entanglement operator . E is defined as E = (∅, WE , id, ∅), where WE contains
only the empty state (i.e. the state with no labels).

5 Language and Logic
In the tradition of axiomatic program logics, the language of FCSL splits into purely
functional expressions e (v when the expression is a value), and commands c with the
effects of divergence, state and concurrency. We also include procedures F, for com-
mands with arguments.
FCSL Commands. A command c satisfies the Hoare tuple {p} c : A {q}@U if c’s effect
on states respects the internal transition of the concurroid U, c is memory-safe when ex-
ecuted from a state satisfying p, and concurrently with any environment that respects the
transitions (internal and external) of U. Furthermore, if c terminates, it returns a value
of type A in a state satisfying q. Formally, q may use a dedicated variable res of type A
to name the return result.5 FCSL uses a procedure tuple, ∀x:B. {p} f (x) : A {q}@U, to
specify a potentially recursive higher-order procedure f taking an argument x of type
B to a result of type A. The assertions p and q may depend on x. FCSL does not treat
first-order looping commands, as these are special cases of recursive procedures. In the
case of recursive procedures, p and q in the procedure tuple together correspond to a
loop invariant, and typically are provided by the programmer.
    The syntax of commands and procedures is as follows.
      c ::= x ← c1 ; c2 | c1  c2 | if e then c1 else c2 | F(e) | return v | act a | inject c | hideΦ,g c
      F ::= f | fix f. x. c

Commands and procedures include atomic actions act a, a monadic unit return v that
returns v and terminates, a monadic bind (i.e. sequential composition) x ← c1 ; c2 that
runs c1 then substitutes its result v1 for x to run c2 (we write c1 ; c2 when x  FV(c2 )),
parallel composition c1  c2 , a conditional, a procedure application F(e), a procedure
variable f , a fixed-point construct for recursion, and injection and hiding commands.
Judgments and Inference Rules. The FCSL judgments are hypothetical under a con-
text Γ that maps program variables x to their type and procedure variables f to their
specification. We allow each specification to depend on the variables declared to the left.

                             Γ ::= · | Γ, x:A | Γ, ∀x:B.{p} f (x) : A {q}@U
 5
     When A = unit, we suppress the type and the variable res, as we did in previous sections.
     Communicating State Transition Systems for Fine-Grained Concurrent Resources                                               305

Fig. 2. FCSL inference rules

                      Γ  {p} c1 : B {q}@U          Γ, x : B  {[x/res]q} c2 : A {r}@U         x  FV(r)
                                                                                                            SEQ
                                                Γ  {p} x ← c1 ; c2 : A {r}@U

            Γ  {p1 } c1 : A1 {q1 }@U       Γ  {p2 } c2 : A2 {q2 }@U                      ∀x:B. {p} f (x) : A {q}@U ∈ Γ
                                                                                PAR                                            H YP
     Γ  {p1  p2 } c1  c2 : A1 × A2 {[π1 res/res]q1  [π2 res/res]q2 }@U                 Γ  ∀x:B. {p} f (x) : A {q}@U

       Γ  {p1 } c : A {q1 }@U     Γ  (p1 , q1 )  (p2 , q2 )               Γ  {p} c : A {q}@U      r stable under U
                                                                 C ONSEQ                                                   FRAME
                     Γ  {p2 } c : A {q2 }@U                                       Γ  {p  r} c : A {q  r}@U

                        Γ  {e = true ∧ p} c1 : A {q}@U            Γ  {e = false ∧ p} c2 : A {q}@U
                                                                                                       IF
                                           Γ  {p} if e then c1 else c2 : A {q}@U

         Γ  {p1 } c : A {q1 }@U        Γ  {p2 } c : A {q2 }@U                 Γ  {p} c : A {q}@U         α  dom Γ
                                                                  C ONJ                                                  E XIST
                  Γ  {p1 ∧ p2 } c : A {q1 ∧ q2 }@U                              Γ  {∃α:B. p} c : A {∃α:B. q}@U

            Γe:A         p stable under U                        Γ, ∀x:B. {p} f (x) : A {q}@U, x:B  {p} c : A {q}@U
                                                  R ET                                                                   FIX
         Γ  {p} return e : A {p ∧ res = e}@U                           Γ  ∀x:B. {p} (fix f. x. c)(x) : A {q}@U

         Γ  ∀x:B. {p} F(x) : A {q}@U           Γe:B                      Γ  {p} c : A {q}@U      r stable under V
                                                           A PP                                                         INJECT
               Γ  {[e/x]p} F(e) : A {[e/x]q}@U                             Γ  {p ∗ r} inject c : A {q ∗ r}@U  V
                     s
                                     s
                                                
            Γ  priv → h ∗ p c priv → h ∗ q @(P  U)  V          P, U and V have disjoint sets of labels
                                                                                                          H IDE
                       Γ  {Ψ g h ∗ (Φ (g) −−∗ p)} hideΦ,g c ∃g .Ψ g h ∗ (Φ (g ) −−∗ q) @P  U
                                                                       s
                                   where Ψ g h = ∃k:heap. priv → h ∪· k ∧ Φ (g) ↓ k

        a = (U, A, σ, μ) is an action       Γ  (σ ∧ this w, λw . (w, w , res) ∈ μ)  (p, q)       p, q stable under U
                                                                                                                          ACTION
                                                   Γ  {p} act a : A {q}@U




Γ does not bind logical variables. In first-order Hoare logics, logical variables are im-
plicitly universally quantified with global scope. In FCSL, we limit their scope to the
Hoare tuples in which they appear. This is required for specifying recursive procedures,
where a logical variable may be instantiated differently in each recursive call [9]. We
also assume a formation requirement on Hoare tuples FLV(p) ⊇ FLV(q), i.e., that all
free logical variables of the postcondition also appear in the precondition.
   The inference rules of the Hoare tuple judgments for commands and procedures
are presented in Figure 2. We note that the assertions and the annotations in the rules
(e.g., Φ in the H IDE rule) may freely use the variables in Γ. To reduce clutter, we
silently assume the checks that all such specification level-entities are well-typed in
their respective contexts Γ.
   We have already discussed PAR, I NJECT and H IDE rules in their versions where
the return type A = unit. The generalization to arbitrary A is straightforward. A side
condition of H IDE ensures that the sets of labels of P, U and V don’t clash, so the
entanglement (P  U)  V is defined. The rule F RAME is a special case of PAR when
c2 is taken to be the idle thread (i.e., c2 = return()). Just like in the rule R ET, we
need to prove the framing assertion r stable, to account for the interference of the other
threads. The rule F IX requires proving a Hoare tuple for the procedure body, under a
306      A. Nanevski et al.

hypothesis that the recursive calls satisfy the same tuple. The procedure APPlication
rule uses the typing judgment for expressions Γ  e : A, which is the customary one
from a typed λ-calculus, so we omit its rules; in our formalization in Coq, this judgment
will correspond to the CiC’s typing judgment. The C ONSEQ rule uses the judgment
Γ  (p1 , q1 )  (p2 , q2 ), which generalizes the customary side conditions p2 =⇒ p1 for
strengthening the precondition and q1 =⇒ q2 for weakening the postcondition, to deal
with the local scope of logical variables [11]. The other rules are standard from Hoare
logic, except the ACTION rule for atomic actions. We devote the rest of the section to it.
Atomic Actions. Actions perform atomic steps from state to state, such as, e.g., re-
aligning the boundaries between, or changing the contents of self , joint and other state
components. The actions thus serve to synchronize the changes to operational state (i.e.,
heaps), with changes to the logical information required for verification (i.e. auxiliary,
or abstract, parts of the state: aS , aO , etc.). If the logical information is erased, that is, if
the states are flattened to heaps, then an action implements a single atomic memory op-
eration such as looking up or mutating a heap pointer, CAS-ing over a heap pointer, or
performing some other atomic Read-Modify-Write operation [7, § 5.6]. How an action
manipulates the logical state is up to the user, depending on the application: we provide
a formal definition of actions, and require that user’s choices adhere to the definition.
   An action is a 4-tuple a = (U, A, σ, μ) where: (1) the concurroid U whose internal
transition a respects, (2) the type A of the action’s return value, (3) the predicate σ on
states describing the states in which the action could be executed, and (4) the relation μ
relating the initial state, the ending state, and the ending result of the action. σ and μ are
given in a large-footprint style, giving fully the heaps and the auxiliaries they accept.
   For example, consider the action release used in Section 3 to release a lock and
transfer the pointer x from a private heap of a thread to the ownership of the lock re-
source. This action is over the entangled concurroid CSLlock,lk,I = P  Llock,lk,I as it
transfers the ownership of (x  −). Its return value type is A = unit. It can be executed
in states in which the lock is taken by the self thread, and the pointer x is in the private
heap. The contents of x is aS + aS + aO , for some aS and aS , so that once x is transfered
to the ownership of the lock resource, it satisfies the resource invariant. Thus:

 w∈σ              ⇐⇒ w = priv  [x  (aS + aS + aO ) ∪· hS | empty | hO ] ∪·
                         lock  [(Own, aS ) | lk  true | ( , aO )]
                                                           Own
 (w, w , res) ∈ μ ⇐⇒ w = priv  [x  (aS + aS + aO ) ∪· hS | empty | hO ] ∪·
                         lock  [(Own, aS ) | lk  true | ( , aO )] ∧
                                                           Own
                     w = priv  [hS | empty | hO ] ∪·
                         lock  [( , aS + a ) | lk  false ∪· x  (aS + a + aO ) | (
                                  Own                                                  , aO )]
                                                                                      Own
                                               S                             S


Once the states are flattened into heaps, the σ and μ components of release reduce
to describing the behavior of a memory mutation on the pointer lk. For example, the
relation μ = {(w, w , r) | (w, w , r) ∈ μ} relates (h, h , r) iff

                       h = (x  (aS + aS + aO )) ∪· hS ∪· (lk  true) ∪· hO
                       h = (x  (aS + aS + aO )) ∪· hS ∪· (lk  false) ∪· hO

Thus, operationally, release can be implemented as a single mutation to the lk pointer.
     Communicating State Transition Systems for Fine-Grained Concurrent Resources         307

   The inference rule ACTION takes an action a = (U, A, σ, μ) and checks that a satisfies
that σ can be strengthened into p and μ can be weakened into q. As μ is not a postcondi-
tion itself, but a relation taking input states, we first introduce a fresh logical variable w
to name the input state using a predicate this. Then the predicate expressing post states
for the action is computed out of μ and w, and it is this predicate that’s weakened into q.
p and q must be stable wrt. U, in order to account for the possibility that an interference
of the environment appears just before, or just after, the action is executed.
Soundness and Implementation. We have established the soundness of FCSL by
exhibiting a denotational model based on action trees [10, 11], which are a variation on
Brookes’ action trace semantics, so we can formulate the following theorem.

Theorem 1. FCSL is sound with respect to the denotational model of action trees.

We developed the model in the logics of Calculus of Inductive Constructions, thus, the
model is a shallow embedding in Coq, and its implementation is available on-line [11].
The implementation also defines denotational semantics for constructs and ascribes
them types corresponding to rules in Figure 2. These type ascriptions require proofs,
and together establish soundness of the logic, although rules/types in the implemen-
tation differ somewhat from those in Figure 2, facilitating encoding in Coq: (1) they
use binary postconditions, (2) pre-/postconditions are in higher-order logic over heaps
and PCMs, instead of notation from Figure 1, (3) they infer weakest-pre-/strongest-
postconditions and (4) assertions are stabilized. The correspondence between the im-
plementation and Figure 2 is straightforward, but established by hand.


6 Related Work

FCSL builds on the previous work on subjective auxiliary state and SCSL logic [10].
The SCSL logic contained the distinction between self and other views, which was es-
sential for compositional implementation of auxiliary state. However, it contained ex-
actly one coarse-grained resource, with no ability to create and dispose new resources.
In contrast, FCSL can introduce any number of fine-grained resources in a scoped way.
   The work on Concurrent Abstract Predicates (CAP) [4] introduces a notion of shared
region that serves a similar purpose as concurroids, in that regions circumscribe a chunk
of shared heap with a protocol governing its evolution. A protocol is defined by a set of
atomic actions, which are RG-style transitions on private state and a region. In addition
to heaps, regions may contain abstract capabilities that identify enabled actions. Thus
there is a subtle mutual recursion in a protocol definition between an action and the
capability to perform the action. A recurring pattern for this approach is quantification
over all possible capabilities and placing them in a shared region, to be used up if needed
in the execution of the protocol. The CAP framework could atomically change only
one region; a restriction lifted in the recent work on Views [3] and HOCAP [15] that
introduced view shifts to synchronize changes in several regions. Once allocated, CAP’s
regions have dynamically-scoped lifetime, and they can be disposed by a particular
thread if it collects all corresponding region’s capabilities. To the best of our knowledge,
HOCAP does not allow the removal or scoped hiding of a shared region.
308     A. Nanevski et al.

   In contrast with CAP and their successors, FCSL does not require capabilities to
perform actions, as these are naturally represented in the self and other views associated
with a resource (and can also be seen as auxiliary state). Such auxiliary state is simpler
than capabilities; it is not subject to ownership transfer, and there is no need to quantify
over all capabilities. In our experience, this simplicity extends to the specification of
invariants and transitions, and to the proofs of stability. In FCSL, synchronizing changes
over a number of concurroids is achieved directly at the level of transitions by means of
entanglement, and at the level of programs by allowing actions to be defined over any
concurroid, including entangled ones. Thus, no view shifts are required. The burden of
stability proofs is further reduced in FCSL by formulating private heaps as a separate
concurroid that one may, but need not, entangle with. Thus, when an action manipulates
only the internal state of a resource, the attendant stability proofs can ignore private
heaps, e.g., the take action of a ticketed lock [4, 11]. Moreover, the communication in
FCSL makes it possible for concurroids to pass heaps between each other directly, rather
than going through private state. While the current paper does not present examples that
exploit this ability, we have found it useful when verifying in FCSL a more advanced
example of readers-writers, which we will present in future work.
   CaReSL [17] uses the same notion of shared region as CAP, though it specifies the
transitions in a manner closer to FCSL, namely by means of STS’s. CaReSL does not
directly provide subjective self and other views of a resource, but it provides a notion of
tokens, whose ownership is exchanged between a thread and its environment. CaReSL
assertions explicitly allow statements only about self-owned tokens, not other-owned
ones. Thus, reasoning about the lack of logical changes to environment-owned data has
to be encoded with a level of indirection, potentially quantifying over all tokens, similar
to CAP’s quantification over capabilities. A frequent side condition in CaReSL rules is
that various assertions are token-pure, which does not have a direct correspondent in
FCSL. Similar to CAP, CaReSL currently allows actions that work over only a single
region, and will require an extension akin to view shifts to enable synchronized updates.
CaReSL does not consider removal or scoped hiding of shared regions, although it
can be emulated by introducing an empty “final” protocol state. Instead of stability
checks in FCSL, in CaReSL one may stabilize assertions by composing them with
environment stepping. In our experience, this does not change the proofs: the same
obligations reappear in proofs out of stabilized hypotheses. On the other hand, CaReSL
can reason about fine-grained data structure by means of refinement (a generalization of
linearizability). FCSL supports higher-order functions by means of shallow embedding
into CiC [1, 16], but we have not considered linearizability so far, which is future work.
   Feng’s Local Rely-Guarantee (LRG) [5] is, to the best of our knowledge, the first
work that reconciled fine-grained reasoning in the style of RG with framing and hiding
at the level of transitions (similar to our I NJECT and H IDE). We differ from LRG in
that we introduce communication and subjectivity into the mix; thus our injection and
hiding rules take self and other views into account. The latter are a compositional form
of auxiliary state, whereas LRG in practice has to use the classical, non-compositional
form of auxiliary state [10, 13].
     Communicating State Transition Systems for Fine-Grained Concurrent Resources         309

7 Conclusion and Future Work

We presented concurroids—a novel model for scalable shared-memory concurrency
verification, based on communicating STS, and FCSL—a logic for concurroids.
   In the future work, we are going to build a number of concurroids to encode common
programming patterns. For example, dynamic allocation and deallocation of memory
can be encoded via an allocator concurroid (without extensions of FCSL), and similarly
for dynamic allocation and deallocation of locks. We hope to investigate if concur-
roids can be endowed with analogues of channel relabeling and restriction operators
from process algebras, to provide finer control over interconnection and closure of ex-
ternal transitions. Finally, we plan to consider refinement which allows weakening the
ascribed concurroid U of a program, to a coarser-grained concurroid V, if U can be
shown to simulate V. One could then verify fine-grained concurrent ADTs against V,
and afterwards hide the granularity by switching to U.

Acknowledgments. We thank Anindya Banerjee, Thomas Dinsdale-Young and the
ESOP 2014 anonymous reviewers for their comments. This research was partially sup-
ported by Spanish MINECO projects TIN2012-39391-C04-01 Strongsoft, TIN2010-
20639 Paran10, AMAROUT grant PCOFUND-GA-2008-229599, and Ramon y Cajal
grant RYC-2010-0743.


References
 1. Bertot, Y., Castéran, P.: Interactive Theorem Proving and Program Development. Coq’Art:
    The Calculus of Inductive Constructions. Springer (2004)
 2. Brookes, S.: A semantics for concurrent separation logic. Th. Comp. Sci. 375(1-3) (2007)
 3. Dinsdale-Young, T., Birkedal, L., Gardner, P., Parkinson, M.J., Yang, H.: Views: composi-
    tional reasoning for concurrent programs. In: POPL 2013 (2013)
 4. Dinsdale-Young, T., Dodds, M., Gardner, P., Parkinson, M.J., Vafeiadis, V.: Concurrent
    abstract predicates. In: D’Hondt, T. (ed.) ECOOP 2010. LNCS, vol. 6183, pp. 504–528.
    Springer, Heidelberg (2010)
 5. Feng, X.: Local rely-guarantee reasoning. In: POPL 2009 (2009)
 6. Feng, X., Ferreira, R., Shao, Z.: On the relationship between concurrent separation
    logic and assume-guarantee reasoning. In: De Nicola, R. (ed.) ESOP 2007. LNCS, vol. 4421,
    pp. 173–188. Springer, Heidelberg (2007)
 7. Herlihy, M., Shavit, N.: The art of multiprocessor programming. M. Kaufmann (2008)
 8. Jones, C.B.: Tentative steps toward a development method for interfering programs. ACM
    Trans. Prog. Lang. Syst. 5(4) (1983)
 9. Kleymann, T.: Hoare logic and auxiliary variables. Formal Asp. Comput. 11(5) (1999)
10. Ley-Wild, R., Nanevski, A.: Subjective auxiliary state for coarse-grained concurrency.
    In: POPL 2013 (2013)
11. Nanevski, A., Ley-Wild, R., Sergey, I., Delbianco, G.A.: Supporting Material,
    http://software.imdea.org/˜ aleks/fcsl/
12. O’Hearn, P.W.: Resources, concurrency, and local reasoning. Th. Comp. Sci. 375(1-3) (2007)
13. Owicki, S.S., Gries, D.: Verifying properties of parallel programs: An axiomatic approach.
    Commun. ACM 19(5) (1976)
310      A. Nanevski et al.

14. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In: LICS (2002)
15. Svendsen, K., Birkedal, L., Parkinson, M.: Modular reasoning about separation of
    concurrent data structures. In: Felleisen, M., Gardner, P. (eds.) ESOP 2013. LNCS, vol. 7792,
    pp. 169–188. Springer, Heidelberg (2013)
16. The Coq Development Team. The Coq Proof Assistant Reference Manual - Version V8.4
    (2012), http://coq.inria.fr/
17. Turon, A., Dreyer, D., Birkedal, L.: Unifying refinement and Hoare-style reasoning in a logic
    for higher-order concurrency. In: ICFP 2013 (2013)
18. Vafeiadis, V., Parkinson, M.: A marriage of rely/guarantee and separation logic. In: Caires,
    L., Vasconcelos, V.T. (eds.) CONCUR 2007. LNCS, vol. 4703, pp. 256–271. Springer, Hei-
    delberg (2007)
