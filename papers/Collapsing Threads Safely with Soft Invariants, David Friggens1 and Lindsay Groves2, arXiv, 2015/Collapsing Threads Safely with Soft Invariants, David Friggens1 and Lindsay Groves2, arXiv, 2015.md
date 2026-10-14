                                             Collapsing Threads Safely with Soft Invariants

                                                                David Friggens1 and Lindsay Groves2
                                                                           1
                                                                              david@frigge.nz
                                                                  2
                                                                      Victoria University of Wellington
arXiv:1512.09186v1 [cs.LO] 31 Dec 2015




                                                                         lindsay@ecs.vuw.ac.nz



                                                Abstract. Canonical abstraction is a static analysis technique that rep-
                                                resents states as 3-valued logical structures, and produces finite abstract
                                                systems. Despite providing a finite bound, these abstractions may still
                                                suffer from the state explosion problem. Notably, for concurrent pro-
                                                grams with arbitrary interleaving, if threads in a state are abstracted
                                                based on their location, then the number of locations will be a combina-
                                                torial factor in the size of the statespace.
                                                We present an approach using canonical abstraction that avoids this
                                                state explosion by “collapsing” all of the threads in a state into a sin-
                                                gle abstract representative. Properties of threads that would be lost by
                                                the abstraction, but are needed for verification, are retained by defining
                                                conditional “soft invariant” instrumentation predicates. This technique is
                                                used to adapt previous models for verifying linearizability of nonblocking
                                                concurrent data structure algorithms, resulting in exponentially smaller
                                                statespaces.


                                         1     Introduction
                                         Canonical abstraction [13] is a powerful technique for reasoning about heap-
                                         manipulating programs. It is effective for analyzing concurrent systems with
                                         interleaving threads, allowing on-the-fly model checking of safety properties.
                                         However, the standard abstraction is still affected by the statespace explosion
                                         problem. In this paper, we introduce a way of using canonical abstraction for
                                         concurrent systems that is combinatorially more efficient.

                                         1.1   Motivation
                                         Canonical abstraction represents states as 3-valued logical structures. A (poten-
                                         tially infinite) concrete statespace is abstracted to a finite abstract statespace by
                                         mapping the (potentially infinite) heap objects in each state to a finite number
                                         of abstract heap objects. The abstract heap objects are equivalence classes with
                                         respect to a predetermined (finite) set of unary predicates. Each abstract heap
                                         object represents all of the heap objects in the concrete state with the same
                                         truth valuation of the abstraction predicates.
                                             Canonical abstraction was initially developed for sequential systems, but Ya-
                                         hav and Sagiv [15] showed how it can be used for concurrent systems with inter-
                                         leaving threads. The logical structures are extended to include an object for each
thread, and predicates for the possible program locations (labels) of the threads.
The set of abstraction predicates includes the location predicates and possibly
properties of thread fields, such as whether a particular field is null. As a result,
the number of equivalence classes of abstract thread objects is determined by
the number of locations and possibly some user defined properties.
    This approach has some benefits. For example, if an important property of
a system is that the Y field of a thread is always null at location X , then this is
implicitly recorded in the abstract statespace. In every reachable abstract state
there will only be a thread object with the “at location X ” predicate true and
with the “Y is null” predicate true, never with “Y is null” false.
    There is an important downside to this approach, however. For each abstract
heap configuration, there is an abstract state with a different combination of
interleaving thread states. For example, if there are three interleaving locations
X , Y and Z , then every abstract heap configuration has seven corresponding
abstract states: three when all threads are at the same location (X , Y or Z ),
three when all threads are at one of two locations ({X , Y }, {X , Z } or {Y , Z }),
and one when there are threads at all three locations.
    As the number of possible interleaving thread states increases, the number
of these combinations increases, and the less efficient the abstract statespace
becomes. Can we avoid the statespace explosion, but still make the abstraction
precise enough to verify interesting properties?


1.2    Soft Invariants

The “obvious” fix is to map all thread objects to a single abstract thread object
in each abstract state. This avoids the problem of combinatorial thread objects,
but loses too much precision — for example, the abstract thread object can
record whether Y is null for all threads, whatever location they are in, but not
for only threads at location X .
    We propose new derived unary predicates to explicitly preserve certain prop-
erties of threads at particular locations. These predicates are defined using con-
ditional formulas of the form, e.g. “if the location is X then the field Y is null”.
The predicate will be true for all threads at locations other than X , and if Y is
always null at location X , then the predicate will be true for all those threads
also. Thus the predicate will be true for the single abstract thread object in each
abstract state.
    If Y is sometimes non-null at location X , then the predicate will be false for
those thread objects, and will be “unknown” for the resulting abstract thread
object.3 We call these predicates “soft invariants”, as they allow us to explicitly
preserve invariants of the system (such as “at location X , field Y is always
null”) but without having to prove that the property is invariant. If they are not
actually invariant then the predicate does not affect the analysis.
3
    In the 3-valued semantics, “unknown” indicates that the abstract predicate rep-
    resents instances in corresponding concrete states when it is true, and when it is
    false.
    The paper is structured as follows. In Section 2, we give some background
details about canonical abstraction. In Section 3, we illustrate the use and effects
of soft invariants with a simple example, advancing a pointer along a circular
linked list. In Section 4, we show the results of using soft invariants to verify
two nonblocking data structures, improving on our previous work. In Section 5,
we discuss choosing soft invariants, and demonstrate that they can be safely
over-defined. Finally, in Section 6 we discuss related work.


2    Preliminaries

States as logical structures Sagiv et al. [13] represent states as 3-valued
logical structures, where predicates describe relationships between objects, and
multiple concrete objects can be represented by a single abstract “summary
object”. Since a summary object can represent two or more concrete objects, an
abstract state with summary objects can represent an infinite number of concrete
states.
    First, a finite set of predicates P = {eq, p1 , . . . , pn } is fixed for the analysis,
and we define Pk to be the set of k -ary predicates in P (the equality predicate
eq has arity 2). Then, an (abstract ) configuration S = hU , ιi has a universe U
that is a (finite or infinite) set of objects and an interpretation ι over the logical
values true (1), false (0) and unknown ( 12 ). For each k -ary predicate p,

    ι(p) : U k → {1, 0, 21 }

Additionally, for each u1 , u2 ∈ U where u1 6= u2 , ι(eq)(u1 , u2 ) = 0. An object u,
for which ι(eq)(u, u) = 21 is called a summary object. A concrete configuration is
one where all interpretations are 1 or 0.
    Intuitively, one configuration represents a less abstract one if it contains the
same information, except for some conservative information loss. In other words,
it has the same universe of objects, though some may have been merged together
into summary objects, and it has the same predicate interpretations, though
some may have become unknown. This is formalised by the notion of embedding,
which relates configurations that are related by conservative information loss.
    We say that a configuration S1 = hU1 , ι1 i embeds into a configuration S2 =
hU2 , ι2 i if there exists a surjective function f : U1 → U2 such that for every
k -ary predicate p, and u1 , . . . , uk ∈ U1 ,

    ι1 (p)(u1 , . . . , uk ) ⊑ ι2 (p)(f (u1 ), . . . , f (uk ))

where, for l1 , l2 ∈ {1, 0, 12 }, l1 ⊑ l2 iff l1 = l2 or l2 = 21 .
    We further define a tight embedding to be one that minimises information
loss, i.e. a predicate interpretation only becomes unknown if two objects are
being merged together, one which has a true interpretation and the other a false
interpretation. Formally, there exists a surjective function f : U1 → U2 such that
for every k -ary predicate p, and u1 , . . . , uk ∈ U2 ,

    ι2 (p)(u
           1 , . . . , uk′ ) = −1
           1 if ∀ u1 ∈ f (u1 ), . . . , uk′ ∈ f −1 (uk ) • ι1 (p)(u1′ , . . . , uk′ ) = 1
             0 if ∀ u1′ ∈ f −1 (u1 ), . . . , uk′ ∈ f −1 (uk ) • ι1 (p)(u1′ , . . . , uk′ ) = 0
          1
             2 otherwise


Canonical abstraction Canonical abstraction is a method for constructing
tight embeddings. Given a subset of the unary predicates A ⊆ P1 , called the
abstraction predicates, we map objects in the original configuration to the same
abstract object if they have the same interpretations over the abstraction predi-
cates. The interpretation in the abstract configuration is constructed as per the
definition of tight embeddings above. We say that a configuration is canonically
abstract, with respect to A, if it is the canonical abstraction of itself.
    Canonical abstraction has a number of important properties:

 – Every configuration has a single canonical abstraction, as each object has a
   single canonical mapping in the embedding function.
 – Since there are a finite number of abstraction predicates, it follows that there
   is a finite bound on the number of objects in the universe of a canonically
   abstract configuration, and thus a finite bound on the number of potential
   states in an abstract system.

   The soundness of the canonical abstraction approach rests upon the Em-
bedding Theorem [13, Theorem 4.9]. Informally, this says that if a structure S
embeds into a structure S ′ , then any information extracted from S ′ via a formula
ϕ is a conservative approximation of the information extracted from S via ϕ.
Alternatively, if we prove a property ϕ true or false in S ′ , then we know it has
the same value in S .


Graphical representation It is often helpful for comprehension to represent
logical structures using graphs. We use graph nodes to represent objects in the
universe, with a double line indicating a summary object. Labels on nodes rep-
resent unary predicates — for each object, they are present if true, present with
annotation (e.g. “x = 21 ”) if unknown, or absent if false. Labelled arrows repre-
sent binary predicates — for each pair of objects, a solid line if true, a dotted
line if unknown, or absent if false. Additionally, we use different node shapes to
represent object type predicates, instead of labels — hexagons for threads and
rectangles for linked list nodes.


Refining abstractions Canonical abstraction using the fixed predicates P is
often too coarse, resulting in too much information being lost (i.e. evaluating
to unknown) for a property to be verified. A key method for refining abstrac-
tions is to introduce additional predicates that record properties derived from
the other predicates. These instrumentation predicates add no new information
                               1: operation Inc( )
                               2:    repeat
                               3:       a := x
                               4:       b := a.next
                               5:    until CAS(x, a, b)
                               6:    return
                               7: end operation

            Fig. 1: Operation to advance a pointer x along a linked list




to a concrete state, since they evaluate to the same truth values as their defining
formulas. However, in an abstract state they may add information: an instru-
mentation predicate may evaluate to a definite value (true or false) whilst its
defining formula may evaluate to unknown. Additionally, unary instrumentation
predicates are usually included in the set of abstraction predicates A, which can
prevent some objects from being merged together into summary objects. In this
paper, we make a point of removing certain instrumentation predicates from A
so that thread objects are merged together.



Tool Support Canonical abstraction has been implemented in TVLA4 (for
Three Valued Logic Analyzer), produced at Tel Aviv University [9, 3]. All of the
results in this paper use the “partial join” option [11].



3     Example


Figure 1 shows a simple operation to advance a global pointer x along a linked
list. The thread takes a snapshot (a) of x, then of that node’s next field (b).
If the snapshot is unchanged, the atomic Compare-and-Swap (CAS) command5
advances x. Otherwise, if another thread has altered x, then the loop is restarted
to try again.
    To illustrate the use of soft invariants, we will consider a system composed
of an arbitrary number of threads that repeatedly perform the Inc operation.
The system is initialised with a circular linked list with a single shared variable
x pointing at one of the list nodes. We will check the safety property that x is
never null.

4
    http://www.cs.tau.ac.il/~ tvla/
5
    CAS(x, a, b) is an atomic command that sets x to b and returns true only if x = a;
    otherwise it just returns false.
3.1     Predicates

To begin the model, we define unary core predicates for the object types, global
variable, and thread locations:6

      is thread, is node, x, at[idle], at[line3], at[line4], at[line5], at[line6]

and binary core predicates for the object’s fields:

      next, a, b

To preserve the fact that the nodes’ next fields are always non-null, and to
record whether the thread fields are null or not, we define the following unary
instrumentation predicates:

      has[next](v ) ⇔ ∃ u • next(v , u)
      has[a](v ) ⇔ ∃ u • a(v , u)
      has[b](v ) ⇔ ∃ u • b(v , u)

To record whether a thread’s b field is the next-successor of its a field, we define
the following unary shape predicate [7]:

      succ[a, b, next](v ) ⇔ ∃ u1 , u2 • a(v , u1 ) ∧ b(v , u2 ) ∧ next(u1 , u2 )


3.2     Initial State

In the initial state, all threads are at the idle location, and all their fields are
null. The node objects are indistinguishable except for the one pointed to by x.
Figure 2 shows a diagram of the state.


                                                    next

                                         x
               at[idle]              has[next]                has[next]             next

                                                    next

                          Fig. 2: Initial state of the example system




3.3     Combinatorial States

By default, the set of abstraction predicates is the set of unary predicates. In
this simple example system, the circular list is identical in every abstract state
— when x advances along the list, the old node is abstracted with the rest and
          at[idle] at[line3] at[line4] at[line5] at[line6] has[a] has[b] succ[a, b, next]
             1         0         0         0         0       0      0           0
             0         1         0         0         0       0      0           0
             0         0         1         0         0       1      0           0
             0         0         0         1         0       1      1           1
             0         0         0         0         1       1      1           1
             0         1         0         0         0       1      1           1
             0         0         1         0         0       1      1           0
             0         0         1         0         0       1      1           1
               Table 1: Predicate values for abstract thread objects



the abstract representation remains unchanged. Thus the differences between
the abstract states are solely due to the thread objects.
    There are five thread locations, but eight possible distinct abstract thread
objects, as shown in Table 1. At the idle location, the fields a and b are null,
so the instrumentation predicates has[a], has[b] and succ[a, b, next] are false (0).
They remain null/false at line 3, but at line 4, a is assigned a value so has[a]
is true (because x is also non-null). Then at line 5, b is assigned to a’s (non-
null) successor, so has[b] and succ[a, b, next] are true. At line 6 after a successful
CAS step, the fields are unchanged, so the instrumentation predicates remain
unchanged. The fields are similarly unchanged after an unsuccessful CAS step,
when the thread returns to line 3; since the instrumentation predicates differ,
threads at line 3 repeating the loop are distinguished from those that have just
started the operation. Similarly at line 4, the instrumentation predicates dis-
tinguish initial from repeating threads; in the latter case, the a field has been
reassigned, so the succ[a, b, next] instrumentation predicate may be false or may
(by coincidence) still be true.
    Knowing that there are eight distinct types of interleaving threads, we can
predict that there will be 255 abstract states — the number of different possible
combinations. Indeed, that is the number reported by TVLA (see Table 2).


3.4    Soft Invariants

If we remove the location predicates and instrumentation predicates on thread
fields from the set of abstraction predicates, then all threads get mapped to a
single abstract thread object. The abstraction is too coarse though, and TVLA
gives a spurious error for our property — the fact that b is non-null at line 5 is
not preserved, so a successful CAS step can result in x being set to null.
    The properties we need to preserve are:

 1. At line 4, has[a] is true.
 2. At line 5, has[a], has[b] and succ[a, b, next] are true.
6
    The square brackets have no meaning other than being a visual indicator.
To do this, we define the following instrumentation predicates:

    if[line4, has[a]](v ) ⇔ is thread(v ) ∧ (at[line4](v ) → has[a](v ))
    if[line5, succ[a, b, next]](v ) ⇔ is thread(v ) ∧ (at[line5](v ) → succ[a, b, next](v ))

We could also have defined similar instrumentation predicates if[line5, has[a]] and
if[line5, has[b]], but has[a] and has[b] are both logical consequences of succ[a, b, next],
so they are not necessary.
     With these two soft invariant instrumentation predicates, TVLA constructs
an abstract system that verifies our property, and has just one abstract state —
shown in Figure 3 — two orders of magnitude less than without soft invariants.
Table 2 shows the results reported by TVLA with and without soft invariants,
for unbounded (∞) threads.




                          at[idle]: 21
                 at[line3]: 12 , at[line4]: 21
                                                     a
                 at[line5]: 12 , at[line6]: 21                  x
                    has[a]: 21 , has[b]: 12                 has[next]
                     succ[a, b, next]: 12
                     if[line4, has[a]]: 21           b
               if[line4, succ[a, b, next]]: 12
                                                     a
                                                             next       next


                                                 b
                                                            has[next]          next




                                Fig. 3: Single abstract state




                              Heap        Ave Max
                              Limit Time RAM RAM   CA Stored
                      SIs Th. (MB) (s) (MB) (MB) States States
                      N ∞       800 6.1 131 279    255 4,335
                      Y ∞       800 0.3     1   1     1      7
                          Table 2: Example verification results
3.5     Safety

In this example, we chose two soft invariants, which were both necessary and
sufficient to verify the property of interest. We could have defined further soft
invariant predicates though, without affecting the safety of the analysis. There
are three possible cases: properties that:

 1. are invariant and needed, but are logical consequences of others specified;
 2. are invariant but not needed; or
 3. are not invariant.

   For the first case, we previously mentioned the possibility of defining the
predicates if[line5, has[a]] and if[line5, has[b]]. For the second case, we can look at
Table 1 and see the possibility of defining, e.g.

      if[idle, has[a]](v ) ⇔ is thread(v ) ∧ (at[idle](v ) → ¬ has[a](v ))
      if[line6, succ[a, b, next]](v ) ⇔ is thread(v ) ∧ (at[line6](v ) → succ[a, b, next](v ))

However, these properties, whilst invariant, do not impact on the verification of
the property, so can be left out to avoid the overhead they would incur. For the
third case, we could for example “mistakenly” define

      if[line3, has[a]](v ) ⇔ is thread(v ) ∧ (at[line3](v ) → ¬ has[a](v ))

This property is not invariant because of the loop, but defining it does not assert
the property in the system. When a thread performs an unsuccessful CAS step at
line 5, the resulting thread object would have if[line3, has[a]] false. Thus the single
abstract thread object would have this soft invariant unknown. There is some
overhead incurred maintaining the non-invariant predicate, but the analysis is
otherwise unaffected.
    See Section 5 for more discussion on this topic.


4     Application

In previous work [7] we have used canonical abstraction to (attempt to) verify
linearizability [8] for three nonblocking concurrent data structure algorithms. We
had mixed success, due to the size of the abstract statespaces exceeding memory
resources. Here we demonstrate greatly improved results using soft invariants.


4.1     Stack

The first algorithm is a stack, introduced by Treiber [14]. Versions of the algo-
rithm have been formally verified by many authors [4, 2, 7]; our analysis adds to
this and demonstrates the applicability of canonical abstraction.
Base Model The model is described in detail elsewhere [6, 7] but contains
30 core predicates, including 16 location predicates, and 19 instrumentation
predicates. Because TVLA does not implement partial order reduction, we con-
structed two models — one with manually specified restrictions on thread inter-
leaving at certain locations, and one with full interleaving. We were able to verify
linearizability for the restricted interleaving model with unbounded threads, list
nodes and data values. For the model with full interleaving, we were only able
to verify linearizability with three threads — with four or more threads the
statespace was too large.

Soft Invariants To identify the necessary and sufficient soft invariants, we used
the same approach we took to identify instrumentation predicates in the initial
model — a combination of inference and trial-and-error. We constructed tables
equivalent to Table 1 for the example, and for the restricted model we were able
to check this against the abstract statespace reported by TVLA.
    We defined 12 soft invariants for the restricted interleaving model and 22 for
the full interleaving model — the lists and full discussion are omitted for space
reasons, but are available elsewhere [6, Chapter 8].
    There are two notable points to be made, relating to more complex properties.
First, there were cases where the value of a predicate at a location depended on
the value of another predicate, so we defined conditional soft invariants with
structures like:
    if[X, Q](v ) ⇔ is thread(v ) ∧ (at[X](v ) → (P(v ) → Q(v )))
    if[X, R](v ) ⇔ is thread(v ) ∧ (at[X](v ) → (¬ P(v ) → R(v )))
Second, there was a more complicated property that was most easily addressed
by defining a new instrumentation predicate, and then defining a soft invariant
for the value of that new predicate. Adding another instrumentation predicate
to the model was extra work, but was an extension of the work involved in
identifying the instrumentation predicates in the inital model.

Results We analysed the models using TVLA 3.0α on a machine with an Intel
Core 2 3.0 GHz processor and 4 GB of RAM, running Java 1.6.0 on a 32-bit
GNU/Linux operating system. Tables 3 and 4 show the results of verifying lin-
earizability for both models, with and without soft invariants. The first three
columns note whether soft invariants were used, the bound on the number of
threads and how much RAM was allocated to TVLA; the remainder are num-
bers reported by TVLA’s output.
    Collapsing threads using soft invariants is very effective, with a 99.2% reduc-
tion in the abstract statespace, and a 99.4% reduction in states stored, for the
restricted interleaving model.
    The collapsed threads approach is even more effective for the full interleaving
model, with the collapsed unbounded statespace 99.8% reduced compared to the
non-collapsed 3-thread statespace. This indicates that the reduction compared
to the non-collapsed unbounded statespace should be far greater.
                          Heap        Ave Max
                          Limit Time RAM RAM   CA Stored
                  SIs Th. (MB) (s) (MB) (MB) States States
                  N 3       800 102 173 336    440 6,493
                  N ∞ 2,048 1,934 849 1,603 1,910 74,056
                  Y ∞       800   25 115 280     16   447
         Table 3: Stack verification results with restricted interleaving



    Compared to the results in Table 3, the collapsed unbounded model stores
more than twice the number of states, a great improvement over the non-
collapsed 3-thread model, which stores nearly 23 times as many states. The
amount of memory used by TVLA only increases slightly, but the analysis takes
nearly six times as long. However, the analysis is still 13 times faster than the
model with restricted interleaving and without collapsed threads.


                          Heap        Ave Max
                          Limit Time RAM RAM     CA Stored
                  SIs Th. (MB) (s) (MB) (MB) States States
                  N 3 2,048 2,931 1,089 1,946 21,107 148,191
                  Y ∞       800 141 149 295       32     932
            Table 4: Stack verification results with full interleaving




4.2   Queues

The remaining algorithms are two nonblocking concurrent queue algorithms,
the original introduced by Michael and Scott [12] (“MS queue”), and a modified
version by Doherty et al. [5] (“DGLM queue”); the latter authors provided the
first formal verification of linearizability.


Base Models These algorithms have a similar singly-linked-list structure, so
construction of the canonical abstraction models was relatively straightforward
— most of the core and instrumentation predicates were able to be copied from
the stack model. The models were larger, with 44 core predicates, including 26
thread locations, and 22 instrumentation predicates.
    As with the stack, we constructed two models for each queue — one with
manually restricted interleaving and one with full interleaving.
    Previously [7], we were able to verify linearizability for the restricted in-
terleaving models with two threads, but not three. For the models with full
interleaving, even when bounded to two threads the statespace was too large for
the memory available.
Soft Invariants We followed a similar process as for the stack, and defined
25–57 soft invariants. The lists and full discussion are omitted for space reasons,
but are available elsewhere [6, Chapter 8]. Table 5 shows the number of distinct
interleaving thread configurations and the number of defined soft invariants for
each component of the two algorithms — idle state (in between operations),
enqueue operation (shared by both), the MS and DGLM dequeue operations,
and then the two algorithms in total.


                                    Restricted Full
                                    locs   SIs locs SIs
                              idle     1     1 1 1
                            enqueue    5    11 10 18
                           dequeueM    5    23 12 38
                           dequeueD    5    13 12 24
                              MS      11    35 23 57
                            DGLM      11    25 23 43
   Table 5: Interleaving location and soft invariant counts for queue models



    As with the stack, we defined conditional soft invariants. We also had to
define a new instrumentation predicate for the MS queue, but for a different
property than the stack.

Results For both the restricted and full interleaving models, we were able
to verify linearizability for unbounded threads, list nodes and data values, with
relatively small resources — a considerable improvement over the models without
soft invariants. Tables 6 and 7 show the results.

                            Heap        Ave Max
                            Limit Time RAM RAM   CA Stored
                Deq SIs Th. (MB) (s) (MB) (MB) States States
                MS N 2        800 393 260 476 3,770 24,271
                MS Y ∞        800   81 151 309     12   523
               DGLM N 2       800   83 189 354 1,506 10,746
               DGLM Y ∞       800 216 181 310      14   591
         Table 6: Queue verification results with restricted interleaving



     An interesting observation is that for the statespaces of the non-collapsed
models, the MS queue is much larger — 2.5 times larger with a bound of two
threads. For the statespaces of the collapsed models though, the DGLM queue is
larger, by 17%. The DGLM queue allows the Head and Tail pointers to “cross”
[5], unlike the MS queue, which results in more canonically abstract list config-
urations, and accounts for the collapsed model differences. In the non-collapsed
                             Heap        Ave Max
                             Limit Time RAM RAM   CA Stored
                 Deq SIs Th. (MB) (s) (MB) (MB) States States
                 MS Y ∞        800 3,109 304 727    96 4,148
                DGLM Y ∞       800 2,887 290 731  112 4,604
            Table 7: Queue verification results with full interleaving



models, the MS queue has more canonical thread objects — which is related to
the larger number of soft invariants needed — and this becomes a larger factor
than the differing number of list structures.


5     Choosing Soft Invariants

Collapsing thread objects with soft invariants provides an exponential reduction
in the size of the statespace, as evidenced by the results presented so far. Ex-
tending models with soft invariants requires extra manual effort though, so some
discussion on the subject is warranted.
    Ultimately, soft invariants do not add anything technically new to canonical
abstraction — they are “just” instrumentation predicates — so their discovery
and definition is an extension of the effort necessary for these anyway. In the
basic case, a spurious error is reported, which indicates that the abstraction is too
coarse. Examining the output, the user can infer what property is needed to be
preserved, and then define an instrumentation predicate to refine the abstraction.
    For the models we have looked at, defining soft invariants was relatively little
extra effort, as they mostly built on the effort of determining the thread instru-
mentation predicates. Consider the example system from Section 3 — the two
soft invariants require an understanding of the values and mutual relationship of
the a and b fields at lines 4 and 5. But those facts had already been determined in
order to define the instrumentation predicates has[a], has[b] and succ[a, b, next].
Constructing a model with collapsed threads initially — as opposed to extending
an existing model — may make determining soft invariants less straightforward.
In these cases we expect that over defining the soft invariants may be effective.


5.1   Over Defining Soft Invariants

The amount of effort needed to identify soft invariants could be mitigated, es-
pecially for unfamiliar systems, by exploiting the “soft” nature of soft invariants
and over defining them. As mentioned in Section 3.5, if a property is not actually
invariant, there is no consequence for the abstract statespace, it just adds some
overhead to the analysis. Thus we can define a range of soft invariants, many of
which may not be necessary or even correct.
    To confirm and quantify this idea, we modified the stack model with full
interleaving from Section 4.1 with soft invariants for every thread predicate. For
every thread predicate p, and every location loc, we defined two soft invariants:

    if[loc, p](v ) ⇔ is thread(v ) ∧ (at[loc](v ) → p(v ))
    nif[loc, p](v ) ⇔ is thread(v ) ∧ (at[loc](v ) → ¬ p(v ))

We kept the six conditional soft invariants, distinguishing them with a ‘c’ prefix.
   Table 8 shows the results of the analysis, with the first line repeated from
Table 4. The canonically abstract statespace is unchanged with 32 states, though
fewer intermediate states are stored. Memory use increases and the time roughly
doubles.


                          Heap        Ave Max
                     Over Limit Time RAM RAM    CA Stored
                     def. (MB) (s) (MB) (MB) States States
                      N     800 141 149 295      32   932
                      Y     800 278 202 338      32   726
          Table 8: Stack verification results with extra soft invariants



    These results show that the tradeoff between analysis efficiency and deter-
mining a minimal set of soft invariants is likely to be a practical one. Here, at
least half of the properties defined are not invariant, with some being false in
the initial state, and the increases in time and memory are acceptable.


6   Related Work
The closest work to ours is by Manevich et al. [10] and Berdine et al. [2], who
also attempt to address the state explosion problem caused by canonical thread
objects. Their approaches are orthogonal to ours, as they attempt to improve
the storage of states by decomposing each state in to thread components and
storing each unique component only once. They verify the same algorithms that
we do, but it is difficult to directly compare results, as they extend previous
work [1] that uses an additional technique (delta heap abstraction) to abstract
lists for verifying linearizability, and which does not abstract threads; we ex-
tend previous work [7] that verifies linearizability for unbounded threads using
canonical abstraction alone. Nonetheless, their approach reduces, but does not
remove, the effect of canonical thread permutations, so our approach may scale
better for larger systems.


7   Conclusions
We have presented a novel approach to canonical abstraction, which exponen-
tially reduces the statespace size by collapsing all thread objects in a state into
a single summary object. This has allowed us to verify linearizability for three
concurrent data structure algorithms with unbounded threads, list lengths and
data values, where previously the statespaces were impractically large.
    The coarse abstraction on threads is refined by defining “soft invariant” in-
strumentation predicates, which preserve properties of threads at specific loca-
tions. The identification of sufficient soft invariants is currently a manual process.
However, the soft invariants are safe to define — correctness is not affected if the
properties are not actually invariant — so they can be over-defined to reduce
the manual effort. Identifying the minimal set, or even a likely superset, may
well be a problem amenable to automation.
    This approach should be applicable to any multi-process canonical abstrac-
tion model. In fact, there is nothing inherently process/thread-specific about
these instrumentation predicates, so the same idea could be applied to other
types of models to reduce the abstract statespace.


References
 1. Amit, D., Rinetzky, N., Reps, T., Sagiv, M., Yahav, E.: Comparison under abstrac-
    tion for verifying linearizability. In: Damm, W., Hermanns, H. (eds.) Proceedings of
    the 19th International Conference on Computer Aided Verification (CAV). Lecture
    Notes in Computer Science, vol. 4590, pp. 477–490. Springer (2007)
 2. Berdine, J., Lev-Ami, T., Manevich, R., Ramalingam, G., Sagiv, M.: Thread quan-
    tification for concurrent shape analysis. In: Gupta, A., Malik, S. (eds.) Proceedings
    of the 20th International Conference on Computer Aided Verification (CAV). Lec-
    ture Notes in Computer Science, vol. 5123, pp. 399–413. Springer (2008)
 3. Bogudlov, I., Lev-Ami, T., Reps, T., Sagiv, M.: Revamping TVLA: Making para-
    metric shape analysis competitive. In: Damm, W., Hermanns, H. (eds.) Proceed-
    ings of the 19th International Conference on Computer Aided Verification (CAV).
    Lecture Notes in Computer Science, vol. 4590, pp. 221–225. Springer (2007)
 4. Colvin, R., Doherty, S., Groves, L.: Verifying concurrent data structures by simula-
    tion. In: Derrick, J., Boiten, E.A. (eds.) Proceedings of the Refinement Workshop.
    Electronic Notes in Theoretical Computer Science, vol. 137.2, pp. 93–110. Elsevier
    (2005)
 5. Doherty, S., Groves, L., Luchangco, V., Moir, M.: Formal verification of a practical
    lock-free queue algorithm. In: de Frutos-Escrig, D., Núñez, M. (eds.) Proceedings
    of the 24th International Conference on Formal Techniques for Networked and
    Distributed Systems (FORTE). Lecture Notes in Computer Science, vol. 3235, pp.
    97–114. Springer (2004)
 6. Friggens, D.: On the Use of Model Checking for the Bounded and Unbounded
    Verification of Nonblocking Concurrent Data Structures. Ph.D. thesis, Victoria
    University of Wellington (2013)
 7. Friggens, D., Groves, L.: Shape predicates allow unbounded verification of lineariz-
    ability using canonical abstraction. In: Thomas, B.H., Parry, D. (eds.) Proceedings
    of the 37th Australasian Computer Science Conference (ACSC). Conferences in
    Research and Practice in Information Technology, vol. 147, pp. 49–56. Australian
    Computer Society (2014)
 8. Herlihy, M.P., Wing, J.M.: Linearizability: A correctness condition for concurrent
    objects. ACM Transactions on Programming Languages and Systems 12(3), 463–
    492 (Jul 1990)
 9. Lev-Ami, T., Sagiv, M.: TVLA: A system for implementing static analyses. In:
    Palsberg, J. (ed.) Proceedings of the 7th International Symposium on Static Anal-
    ysis (SAS). Lecture Notes in Computer Science, vol. 1824, pp. 280–301. Springer
    (2000)
10. Manevich, R., Lev-Ami, T., Sagiv, M., Ramalingam, G., Berdine, J.: Heap decom-
    position for concurrent shape analysis. In: Alpuente, M., Vidal, G. (eds.) Proceed-
    ings of the 15th International Symposium on Static Analysis (SAS). Lecture Notes
    in Computer Science, vol. 5079, pp. 363–377. Springer (2008)
11. Manevich, R., Sagiv, M., Ramalingam, G., Field, J.: Partially disjunctive heap
    abstraction. In: Giacobazzi, R. (ed.) Proceedings of the 11th International Sympo-
    sium on Static Analysis (SAS). Lecture Notes in Computer Science, vol. 3148, pp.
    265–279. Springer (2004)
12. Michael, M.M., Scott, M.L.: Non-blocking algorithms and preemption-safe lock-
    ing on multiprogrammed shared memory multiprocessors. Journal of Parallel and
    Distributed Computing 51(1), 1–26 (1998)
13. Sagiv, M., Reps, T., Wilhelm, R.: Parametric shape analysis via 3-valued logic.
    ACM Transactions on Programming Languages and Systems 24(3), 217–298 (2002)
14. Treiber, R.K.: Systems programming: Coping with parallelism. Tech. Rep. RJ 5118,
    IBM Almaden Research Centre (Apr 1986)
15. Yahav, E., Sagiv, M.: Verifying safety properties of concurrent heap-manipulating
    programs. ACM Transactions on Programming Languages and Systems 32(5)
    (2010), article 18
