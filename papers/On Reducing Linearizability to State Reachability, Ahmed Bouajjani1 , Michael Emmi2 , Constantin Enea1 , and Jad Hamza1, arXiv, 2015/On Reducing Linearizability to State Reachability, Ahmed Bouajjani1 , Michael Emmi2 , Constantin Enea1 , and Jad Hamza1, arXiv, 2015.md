                                               On Reducing Linearizability to State Reachability⋆

                                                  Ahmed Bouajjani1 , Michael Emmi2 , Constantin Enea1 , and Jad Hamza1
                                                                      1
                                                                          LIAFA, Université Paris Diderot, France
arXiv:1502.06882v2 [cs.LO] 25 May 2015




                                                                           2
                                                                             IMDEA Software Institute, Spain



                                                  Abstract. Efficient implementations of atomic objects such as concurrent stacks
                                                  and queues are especially susceptible to programming errors, and necessitate
                                                  automatic verification. Unfortunately their correctness criteria — linearizability
                                                  with respect to given ADT specifications — are hard to verify. Even on classes
                                                  of implementations where the usual temporal safety properties like control-state
                                                  reachability are decidable, linearizability is undecidable.
                                                  In this work we demonstrate that verifying linearizability for certain fixed ADT
                                                  specifications is reducible to control-state reachability, despite being harder for ar-
                                                  bitrary ADTs. We effectuate this reduction for several of the most popular atomic
                                                  objects. This reduction yields the first decidability results for verification without
                                                  bounding the number of concurrent threads. Furthermore, it enables the applica-
                                                  tion of existing safety-verification tools to linearizability verification.


                                         1 Introduction

                                         Efficient implementations of atomic objects such as concurrent queues and stacks are
                                         difficult to get right. Their complexity arises from the conflicting design requirements
                                         of maximizing efficiency/concurrency with preserving the appearance of atomic behav-
                                         ior. Their correctness is captured by observational refinement, which assures that all
                                         behaviors of programs using these efficient implementations would also be possible
                                         were the atomic reference implementations used instead. Linearizability [11], being an
                                         equivalent property [7, 4], is the predominant proof technique: one shows that each con-
                                         current execution has a linearization which is a valid sequential execution according to
                                         a specification, given by an abstract data type (ADT) or reference implementation.
                                              Verifying automatically3 that all executions of a given implementation are lineariz-
                                         able with respect to a given ADT is an undecidable problem [3], even on the typical
                                         classes of implementations for which the usual temporal safety properties are decidable,
                                         e.g., on finite-shared-memory programs where each thread is a finite-state machine.
                                         What makes linearization harder than typical temporal safety properties like control-
                                         state reachability is the existential quantification of a valid linearization per execution.
                                              In this work we demonstrate that verifying linearizability for certain fixed ADTs
                                         is reducible to control-state reachability, despite being harder for arbitrary ADTs. We
                                         believe that fixing the ADT parameter of the verification problem is justified, since in
                                         practice, there are few ADTs for which specialized concurrent implementations have
                                         ⋆
                                              This work is supported in part by the VECOLIB project (ANR-14-CE28-0018).
                                          3
                                              Without programmer annotation — see Section 6 for further discussion.
been developed. We provide a methodology for carrying out this reduction, and instan-
tiate it on four ADTs: the atomic queue, stack, register, and mutex.
     Our reduction to control-state reachability holds on any class of implementations
which is closed under intersection with regular languages4 and which is data indepen-
dent — informally, that implementations can perform only read and write operations on
the data values passed as method arguments. From the ADT in question, our approach
relies on expressing its violations as a finite union of regular languages.
     In our methodology, we express the atomic object specifications using inductive
rules to facilitate the incremental construction of valid executions. For instance in our
atomic queue specification, one rule specifies that a dequeue operation returning empty
can be inserted in any execution, so long as each preceding enqueue has a correspond-
ing dequeue, also preceding the inserted empty-dequeue. This form of inductive rule
enables a locality to the reasoning of linearizability violations.
     Intuitively, first we prove that a sequential execution is invalid if and only if some
subsequence could not have been produced by one of the rules. Under certain condi-
tions this result extends to concurrent executions: an execution is not linearizable if and
only if some projection of its operations cannot be linearized to a sequence produced
by one of the rules. We thus correlate the finite set of inductive rules with a finite set
of classes of non-linearizable concurrent executions. We then demonstrate that each of
these classes of non-linearizable executions is regular, which characterizes the viola-
tions of a given ADT as a finite union of regular languages. The fact that these classes
of non-linearizable executions can be encoded as regular languages is somewhat surpris-
ing since the number of data values, and thus alphabet symbols, is, a priori, unbounded.
Our encoding thus relies on the aforementioned data independence property.
     To complete the reduction to control-state reachability, we show that linearizability
is equivalent to the emptiness of the language intersection between the implementa-
tion and finite union of regular violations. When the implementation is a finite-shared-
memory program with finite-state threads, this reduces to the coverability problem for
Petri nets, which is decidable, and EXPSPACE-complete.
     To summarize, our contributions are:
 – a generic reduction from linearizability to control-state reachability,
 – its application to the atomic queue, stack, register, and mutex ADTs,
 – the methodology enabling this reduction, which can be reused on other ADTs, and
 – the first decidability results for linearizability without bounding the number of con-
   current threads.
Besides yielding novel decidability results, our reduction paves the way for the applica-
tion of existing safety-verification tools to linearizability verification.
    Section 2 outlines basic definitions. Section 3 describes a methodology for induc-
tive definitions of data structure specifications. In Section 4 we identify conditions un-
der which linearizability can be reduced to control-state reachability, and demonstrate
that typical atomic objects satisfy these conditions. Finally, we prove decidability of
linearizability for finite-shared-memory programs with finite-state threads in Section 5.
Proofs to technical results appear in the appendix.
 4
     We consider languages of well-formed method call and return actions, e.g., for which each
     return has a matching call.


                                               2
2 Linearizability
We fix a (possibly infinite) set D of data values, and a finite set M of methods. We
consider that methods have exactly one argument, or one return value. Return values
are transformed into argument values for uniformity.5 In order to differentiate methods
taking an argument (e.g., the Enq method which inserts a value into a queue) from
the other methods, we identify a subset Min ⊆ M of input methods which do take an
argument. A method event is composed of a method m ∈ M and a data value x ∈ D,
and is denoted m(x). We define the concatenation of method-event sequences u · v in
the usual way, and ǫ denotes the empty sequence.

Definition 1. A sequential execution is a sequence of method events,

    The projection u|D of a sequential execution u to a subset D ⊆ D of data values is
obtained from u by erasing all method events with a data value not in D. The set of
projections of u is denoted proj(u). We write u r x for the projection u|D\{x}.

Example 1. The projection Enq(1)Enq(2)Deq(1)Enq(3)Deq(2)Deq(3) r 1 is equal to
Enq(2)Enq(3)Deq(2)Deq(3).

   We also fix an arbitrary infinite set O of operation (identifiers). A call action is
composed of a method m ∈ M, a data value x ∈ D, an operation o ∈ O, and is denoted
callo m(x). Similarly, a return action is denoted reto m(x). The operation o is used to
match return actions to their call actions.

Definition 2. A (concurrent) execution e is a sequence of call and return actions which
satisfy a well-formedness property: every return has a call action before it in e, using
the same tuple m, x, o, and an operation o can be used only twice in e, once in a call
action, and once in a return action.

Example 2. The sequence callo1 Enq(7) · callo2 Enq(4) · reto1 Enq(7) · reto2 Enq(4)
is an execution, while callo1 Enq(7) · callo2 Enq(4) · reto1 Enq(7) · reto1 Enq(4) and
callo1 Enq(7) · reto1 Enq(7) · reto2 Enq(4) are not.

Definition 3. An implementation I is a set of (concurrent) executions.

    Implementations represent libraries whose methods are called by external programs,
giving rise to the following closure properties [4]. In the following, c denotes a call
action, r denotes a return action, a denotes any action, and e, e′ denote executions.
 – Programs can call library methods at any point in time:
   e · e′ ∈ I implies e · c · e′ ∈ I so long as e · c · e′ is well formed.
 – Calls can be made earlier:
   e · a · c · e′ ∈ I implies e · c · a · e′ ∈ I.
 5
     Method return values are guessed nondeterministically, and validated at return points. This
     can be handled using the assume statements of typical formal specification languages, which
     only admit executions satisfying a given predicate. The argument value for methods without
     argument or return values, or with fixed argument/return values, is ignored.


                                                3
  – Returns been made later:
    e · r · a · e′ ∈ I implies e · a · r · e′ ∈ I.
Intuitively, these properties hold because call and return actions are not visible to the
other threads which are running in parallel.
    For the remainder of this work, we consider only completed executions, where each
call action has a corresponding return action. This simplification is sound when im-
plementation methods can always make progress in isolation [10]: formally, for any
execution e with pending operations, there exists an execution e′ obtained by extending
e only with the return actions of the pending operations of e. Intuitively this means that
methods can always return without any help from outside threads, avoiding deadlock.
    We simply reasoning on executions by abstracting them into histories.
Definition 4. A history is a labeled partial order (O, <, l) with O ⊆ O and l : O →
M × D.
The order < is called the happens-before relation, and we say that o1 happens before o2
when o1 < o2 . Since histories arise from executions, their happens-before relations are
interval orders [4]: for distinct o1 , o2 , o3 , o4 , if o1 < o2 and o3 < o4 then either o1 < o4 ,
or o3 < o2 . Intuitively, this comes from the fact that concurrent threads share a notion
of global time. Dh ⊆ D denotes the set of data values appearing in h.
    The history of an execution e is defined as (O, <, l) where:
  – O is the set of operations which appear in e,
  – o1 < o2 iff the return action of o1 is before the call action of o2 in e,
  – an operation o occurring in a call action callo m(x) is labeled by m(x).
Example 3. The history of the execution callo1 Enq(7)·callo2 Enq(4)·reto1 Enq(7)·
reto2 Enq(4) is ({o1 , o2 }, <, l) with l(o1 ) = Enq(7), l(o2 ) = Enq(4), and with < being
the empty order relation, since o1 and o2 overlap.
     Let h = (O, <, l) be a history and u a sequential execution of length n. We say that h
is linearizable with respect to u, denoted h ⊑ u, if there is a bijection f : O → {1, . . . , n} s.t.
  – if o1 < o2 then f (o1 ) < f (o2 ),
  – the method event at position f (o) in u is l(o).
Definition 5. A history h is linearizable with respect to a set S of sequential executions,
denoted h ⊑ S, if there exists u ∈ S such that h ⊑ u.
A set of histories H is linearizable with respect to S, denoted H ⊑ S if h ⊑ S for all
h ∈ H. We extend these definitions to executions according to their histories.
    A sequential execution u is said to be differentiated if, for all input methods m ∈
Min , and every x ∈ D, there is at most one method event m(x) in u. The subset of
differentiated sequential executions of a set S is denoted by S, . The definition extends
to (sets of) executions and histories. For instance, an execution is differentiated if for all
input methods m ∈ Min and every x ∈ D, there is at most one call action callo m(x).
Example 4. callo1 Enq(7) · callo2 Enq(7) · reto1 Enq(7) · reto2 Enq(7) is not differ-
entiated, as there are two call actions with the same input method (Enq) and the same
data value.

                                                 4
    A renaming r is a function from D to D. Given a sequential execution (resp., ex-
ecution or history) u, we denote by r(u) the sequential execution (resp., execution or
history) obtained from u by replacing every data value x by r(x).

Definition 6. The set of sequential executions (resp., executions or histories) S is data
independent if:

  – for all u ∈ S, there exists u′ ∈ S, , and a renaming r such that u = r(u′ ),
  – for all u ∈ S and for all renaming r, r(u) ∈ S.

    When checking that a data-independent implementation I is linearizable with re-
spect to a data-independent specification S, it is enough to do so for differentiated execu-
tions [1]. Thus, in the remainder of the paper, we focus on characterizing linearizability
for differentiated executions, rather than arbitrary ones.

Lemma 1 (Abdulla et al. [1]). A data-independent implementation I is linearizable
with respect to a data-independent specification S, if and only if I, is linearizable with
respect to S, .


3 Inductively-Defined Data Structures

A data structure S is given syntactically as an ordered sequence of rules R1 , . . . , Rn ,
each of the form u1 · u2 · · · uk ∈ S ∧ Guard(u1, . . . , uk ) ⇒ Expr(u1 , . . . , uk ) ∈ S, where
the variables ui are interpreted over method-event sequences, and

  – Guard(u1, . . . , uk ) is a conjunction of conditions on u1 , . . . , uk with atoms
     • ui ∈ M ∗ (M ⊆ M)
     • matched(m, ui )
  – Expr(u1 , . . . , uk ) is an expression E = a1 · a2 · · · al where
     • u1 , . . . , uk appear in that order, exactly once, in E,
     • each ai is either some u j , a method m, or a Kleene closure m∗ (m ∈ M),
     • a method m ∈ M appears at most once in E.

We allow k to be 0 for base rules, such as ǫ ∈ S.
    A condition ui ∈ M ∗ (M ⊆ M) is satisfied when the methods used in ui are all in
M. The predicate matched(m, ui ) is satisfied when, for every method event m(x) in ui ,
there exists another method event in ui with the same data value x.
    Given a sequential execution u = u1 ·. . .·uk and an expression E = Expr(u1 , . . . , uk ),
we define JEK as the set of sequential executions which can be obtained from E by
replacing the methods m by a method event m(x) and the Kleene closures m∗ by 0 or
more method events m(x). All method events must use the same data value x ∈ D.
    A rule R ≡ u1 · u2 · · · uk ∈ S ∧Guard(u1 , . . . , uk ) ⇒ Expr(u1 , . . . , uk ) ∈ S is applied
to a sequential execution w to obtain a new sequential execution w′ from the set:
                                    [
                                         JExpr(w1 , . . . , wk )K
                               w=w1 ·w2 ···wk ∧
                               Guard(w1 ,...,wk )


                                                    5
                        R
We denote this w −→ w′ . The set of sequential executions JSK = JR1 , . . . , Rn K is then
defined as the set of sequential executions w which can be derived from the empty
word:
                                    Ri1       Ri2       Ri p
                            ǫ = w0 −−→ w1 −−→ w2 . . . −−→ w p = w,
where i1 , . . . , i p is a non-decreasing sequence of integers from {1 . . . , n}. This means
that the rules must be applied in order, and each rule can be applied 0 or several times.
    Below we give inductive definitions for the atomic queue and stack data structures.
Other data structures such as atomic registers and mutexes also have inductive defini-
tions, as demonstrated in the appendix.
Example 5. The queue has a method Enq to add an element to the data structure, and a
method Deq to remove the elements in a FIFO order. The method DeqEmpty can only
return when the queue is empty (its parameter is not used). The only input method is
Enq. Formally, Queue is defined by the rules R0 , REnq , REnqDeq and RDeqEmpty .
           R0 ≡ ǫ ∈ Queue
         REnq ≡ u ∈ Queue ∧ u ∈ Enq∗ ⇒ u · Enq ∈ Queue
      REnqDeq ≡ u · v ∈ Queue ∧ u ∈ Enq∗ ∧ v ∈ {Enq, Deq}∗ ⇒ Enq · u · Deq · v ∈ Queue
     RDeqEmpty ≡ u · v ∈ Queue ∧ matched(Enq, u) ⇒ u · DeqEmpty · v ∈ Queue
One derivation for Queue is:
            REnqDeq
ǫ ∈ Queue −−−−−→ Enq(1) · Deq(1) ∈ Queue
            REnqDeq
            −−−−−→ Enq(2) · Enq(1) · Deq(2) · Deq(1) ∈ Queue
            REnqDeq
            −−−−−→ Enq(3) · Deq(3) · Enq(2) · Enq(1) · Deq(2) · Deq(1) ∈ Queue
            RDeqEmpty
            −−−−−−−→ Enq(3) · Deq(3) · DeqEmpty · Enq(2) · Enq(1) · Deq(2) · Deq(1) ∈ Queue
Similarly, Stack is composed of the rules R0 , RPushPop , RPush , RPopEmpty .
         R0 ≡ ǫ ∈ Stack
   RPushPop ≡ u · v ∈ Stack ∧ matched(Push, u) ∧ matched (Push, v) ∧ u, v ∈ {Push, Pop}∗
               ⇒ Push · u · Pop · v ∈ Stack
      RPush ≡ u · v ∈ Stack ∧ matched(Push, u) ∧ u, v ∈ {Push, Pop}∗ ⇒ u · Push · v ∈ Stack
  RPopEmpty ≡ u · v ∈ Stack ∧ matched(Push, u) ⇒ u · PopEmpty · v ∈ Stack

    We assume that the rules defining a data structure S satisfy a non-ambiguity prop-
erty stating that the last step in deriving a sequential execution in JSK is unique and it can
be effectively determined. Since we are interested in characterizing the linearizations of
a history and its projections, this property is extended to permutations of projections of
sequential executions which are admitted by S. Thus, we assume that the rules defining
a data structure are non-ambiguous, that is:
 – for all u ∈ JSK, there exists a unique rule, denoted by last(u), that can be used as
   the last step to derive u, i.e., for every sequence of rules Ri1 , . . . , Rin leading to u,
   Rin = last(u). For u < JSK, last(u) is also defined but can be arbitrary, as there is
   no derivation for u.

                                                    6
 – if last(u) = Ri , then for every permutation u′ ∈ JSK of a projection of u, last(u′ ) =
   R j with j ≤ i. If u′ is a permutation of u, then last(u′ ) = Ri .

   Given a (completed) history h, all the u such that h ⊑ u are permutations of one
another. The last condition of non-ambiguity thus enables us to extend the function
last to histories: last(h) is defined as last(u) where u is any sequential execution
such that h ⊑ u. We say that last(h) is the rule corresponding to h.

Example 6. For Queue, we define last for a sequential execution u as follows:

 – if u contains a DeqEmpty operation, last(u) = RDeqEmpty ,
 – else if u contains a Deq operation, last(u) = REnqDeq ,
 – else if u contains only Enq’s, last(u) = REnq ,
 – else (if u is empty), last(u) = R0 .

Since the conditions we use to define last are closed under permutations, we get that
for any permutation u2 of u, last(u) = last(u2 ), and last can be extended to histories.
Therefore, the rules R0 , REnqDeq , RDeqEmpty are non-ambiguous.


4 Reducing Linearizability to State Reachability

Our end goal for this section is to show that for any data-independent implementation
I, and any specification S satisfying several conditions defined in the following, there
exists a computable finite-state automaton A (over call and return actions) such that:

                                I ⊑ S ⇐⇒ I ∩ A = ∅

Then, given a model of I, the linearizability of I is reduced to checking emptiness of
the synchronized product between the model of I and A. The automaton A represents
(a subset of the) executions which are not linearizable with respect to S.
     The first step in proving our result is to show that, under some conditions, we can
partition the concurrent executions which are not linearizable with respect to S into a
finite number of classes. Intuitively, each non-linearizable execution must correspond
to a violation for one of the rules in the definition of S.
     We identify a property, which we call step-by-step linearizability, which is suffi-
cient to obtain this characterization. Intuitively, step-by-step linearizability enables us
to build a linearization for an execution e incrementally, using linearizations of projec-
tions of e.
     The second step is to show that, for each class of violations (i.e., with respect to a
specific rule Ri ), we can build a regular automaton Ai such that: a) when restricted to
well-formed executions, Ai recognizes a subset of this class; b) each non-linearizable
execution has a corresponding execution, obtained by data independence, accepted by
Ai . If such an automaton exists, we say that Ri is co-regular (formally defined later in
this section).
     We prove that, provided these two properties hold, we have the equivalence men-
tioned above, by defining A as the union of the Ai ’s built for each rule Ri .

                                            7
4.1 Reduction to a Finite Number of Classes of Violations

Our goal here is to give a characterization of the sequential executions which belong to
a data structure, as well as to give a characterization of the concurrent executions which
are linearizable with respect to the data structure. This characterization enables us to
classify the linearization violations into a finite number of classes.
    Our characterization relies heavily on the fact that the data structures we consider
are closed under projection, i.e., for all u ∈ S, D ⊆ D, we have u|D ∈ S. The reason for
this is that the guards used in the inductive rules are closed under projection.

Lemma 2. Any data structure S defined in our framework is closed under projection.

    A sequential execution u is said to match a rule R with conditions Guard if there
exist a data value x and sequential executions u1 , . . . , uk such that u can be written as
JExpr(u1 , . . . , uk )K, where x is the data value used for the method events, and such that
Guard(u1, . . . , uk ) holds. We call x the witness of the decomposition. We denote by MR
the set of sequential executions which match R, and we call it the matching set of R.

Example 7. MREnqDeq is the set of sequential executions of the form Enq(x)·u·Deq(x)·v
for some x ∈ D, and with u ∈ Enq∗ .


Lemma 3. Let S = R1 , . . . , Rn be a data structure and u a differentiated sequential
execution. Then,                                  [
                        u ∈ S ⇐⇒ proj(u) ⊆             MRi
                                                        i∈{1,...,n}

   This characterization enables us to get rid of the recursion, so that we only have to
check non-recursive properties. We want a similar lemma to characterize e ⊑ S for an
execution e. This is where we introduce the notion of step-by-step linearizability, as the
lemma will hold under this condition.

Definition 7. A data structure S = R1 , . . . , Rn is said be to step-by-step linearizable if
for any differentiated execution e, if e is linearizable w.r.t. MRi with witness x, we have:

                       e r x ⊑ JR1 , . . . , Ri K =⇒ e ⊑ JR1 , . . . , Ri K

    This notion applies to the usual data structures, as shown by the following lemma.
The generic schema we use is the following: we let u′ ∈ JR1 , . . . , Ri K be a sequential
execution such that e r x ⊑ u′ and build a graph G from u′ , whose acyclicity implies
that e ⊑ JR1 , . . . , Ri K. Then, we show that we can always choose u′ so that G is acyclic.

Lemma 4. Queue, Stack, Register, and Mutex are step-by-step linearizable.

    Intuitively, step-by-step linearizability will help us prove the right-to-left direction
of Lemma 5 by allowing us to build a linearization for e incrementally, from the lin-
earizations of projections of e.

                                                8
Lemma 5. Let S be a data structure with rules R1 , . . . , Rn . Let e be a differentiated
execution. If S is step-by-step linearizable, we have (for any j):
                                                             [
                        e ⊑ JR1 , . . . , R j K ⇐⇒ proj(e) ⊑   MRi
                                                            i≤ j

    Thanks to Lemma 5, if we’re looking for an execution e which is not linearizable
                                                             S
w.r.t. some data-structure S, we must prove that proj(e) @ i MRi , i.e., we must find a
                                                                                S
projection e′ ∈ proj(e) which is not linearizable with respect to any MRi (e′ @ i MRi ).
    This is challenging as it is difficult to check that an execution is not linearizable
w.r.t. a union of sets simultaneously. Using non-ambiguity, we simplify this check by
making it more modular, so that we only have to check one set MRi at a time.

Lemma 6. Let S be a data structure with rules R1 , . . . , Rn . Let e be a differentiated
execution. If S is step-by-step linearizable, we have:

                e ⊑ S ⇐⇒ ∀e′ ∈ proj(e). e′ ⊑ MR where R = last(e′ )

    Lemma 6 gives us the finite kind of violations that we mentioned in the beginning
of the section. More precisely, if we negate both sides of the equivalence, we have:
e @ S ⇐⇒ ∃e′ ∈ proj(e). e′ @ MR. This means that whenever an execution is
not linearizable w.r.t. S, there can be only finitely reasons, namely there must exist a
projection which is not linearizable w.r.t. the matching set of its corresponding rule.

4.2 Regularity of Each Class of Violations
Our goal is now to construct, for each R, an automaton A which recognizes (a subset
of) the executions e, which have a projection e′ such that e′ @ MR. More precisely, we
want the following property.

Definition 8. A rule R is said to be co-regular if we can build an automaton A such
that, for any data-independent implementation I, we have:

            A ∩ I , ∅ ⇐⇒ ∃e ∈ I, , e′ ∈ proj(e). last(e′ ) = R ∧ e′ @ MR

A data structure S is co-regular if all of its rules are co-regular.

    Formally, the alphabet of A is {call m(x) | m ∈ M, x ∈ D}∪{ret m(x) | m ∈ M, x ∈ D}
for a finite subset D ⊆ D. The automaton doesn’t read operation identifiers, thus, when
taking the intersection with I, we ignore them.

Lemma 7. Queue, Stack, Register, and Mutex are co-regular.

Proof. To illustrate this lemma, we sketch the proof for the rule RDeqEmpty of Queue.
The complete proof of the lemma can be found in the extended version of this paper.
    We prove in the appendix (Corollary 1) that a history has a projection such that
last(h′ ) = RDeqEmpty and h′ @ MRDeqEmpty if and only if it has a DeqEmpty operation
which is covered by other operations, as depicted in Fig. 1. The automaton ARDeqEmpty in
Fig. 2 recognizes such violations.

                                             9
                                                  M(3)                      M(3)                     M(3)

                  DeqEmpty(2)                            call DeqEmpty(2)          ret DeqEmpty(2)
                                                   q1                        q2                       q4
   Enq(1)                  Deq(1)                             call Deq(1)
                                                      ret Enq(1)                   ret Enq(1)
       Enq(1)              Deq(1)
                                                   q0        M(3)            q3       M(3)
         Enq(1)                 Deq(1)

                  Enq(1)            Deq(1)     call Enq(1)


Fig. 1. A four-pair RDeqEmpty violation.     Fig. 2. An automaton recognizing RDeqEmpty viola-
Lemma 19 demonstrates that this pat-         tions, for which the queue is non-empty, with data
tern with arbitrarily-many pairs is reg-     value 1, for the span of DeqEmpty. We assume all
ular.                                        call Enq(1) actions occur initially without loss of
                                             generality due to implementations’ closure properties.


    Let I be any data-independent implementation. We show that
ARDeqEmpty ∩ I , ∅ ⇐⇒ ∃e ∈ I, , e′ ∈ proj(e). last(e′ ) = RDeqEmpty ∧ e′ @ MRDeqEmpty
(⇒) Let e ∈ I be an execution which is accepted by ARDeqEmpty . By data independence,
let e, ∈ I and r a renaming such that e = r(e, ). Let d1 , . . . , dm be the data values which
are mapped to value 1 by r.
     Let d be the data value which is mapped to value 2 by r. Let o the DeqEmpty
operation with data value d. By construction of the automaton we can prove that o is
covered by d1 , . . . , dm , and using Corollary 1, conclude that h has a projection such that
last(h′ ) = RDeqEmpty and h′ @ MRDeqEmpty .
     (⇐) Let e, ∈ I, such that there is a projection e′ such that last(e′ ) = RDeqEmpty
and e′ @ MRDeqEmpty . Let d1 , . . . , dm be the data values given by Corollary 1, and let d
be the data value corresponding to the DeqEmpty operation.
     Without loss of generality, we can always choose the cycle so that Enq(di ) doesn’t
happen before Deq(di−2 ) (if it does, drop di−1 ).
     Let r be the renaming which maps d1 , . . . , dm to 1, d to 2, and all other values to 3.
Let e = r(e, ). The execution e can be recognized by automaton ARDeqEmpty , and belongs
to I by data independence.
    When we have a data structure which is both step-by-step linearizable and co-
regular, we can make a linear time reduction from the verification of linearizability
with respect to S to a reachability problem, as illustrated in Theorem 1.
Theorem 1. Let S be a step-by-step linearizable and co-regular data structure and
let I be a data-independent implementation. There exists a regular automaton A such
that:
                              I ⊑ S ⇐⇒ I ∩ A = ∅

5 Decidability and Complexity of Linearizability
Theorem 1 implies that the linearizability problem with respect to any step-by-step lin-
earizable and co-regular specification is decidable for any data-independent implemen-

                                                 10
tation for which checking the emptiness of the intersection with finite-state automata is
decidable. Here, we give a class C of data-independent implementations for which the
latter problem, and thus linearizability, is decidable.
     Each method of an implementation in C manipulates a finite number of local vari-
ables which store Boolean values, or data values from D. Methods communicate through
a finite number of shared variables that also store Boolean values, or data values from
D. Data values may be assigned, but never used in program predicates (e.g., in the
conditions of if and while statements) so as to ensure data independence. This class
captures typical implementations, or finite-state abstractions thereof, e.g., obtained via
predicate abstraction.
     Let I be an implementation from class C. The automata A constructed in the proof
of Lemma 7 use only data values 1, 2, and 3. Checking emptiness of I ∩ A is thus
equivalent to checking emptiness of I3 ∩ A with the three-valued implementation
I3 = {e ∈ I | e = e|{1,2,3} }. The set I3 can be represented by a Petri net since bounding
data values allows us to represent each thread with a finite-state machine. Intuitively,
each token in the Petri net represents another thread. The number of threads can be
unbounded since the number of tokens can. Places count the number of threads in each
control location, which includes a local-variable valuation. Each shared variable also
has one place per value to store its current valuation.
     Emptiness of the intersection with regular automata reduces to the EXPSPACE-
complete coverability problem for Petri nets. Limiting verification to a bounded number
of threads lowers the complexity of coverability to PSPACE [6]. The hardness part
of Theorem 2 comes from the hardness of state reachability in finite-state concurrent
programs.

Theorem 2. Verifying linearizability of an implementation in C with respect to a step-
by-step linearizable and co-regular specification is PSPACE-complete for a fixed num-
ber of threads, and EXPSPACE-complete otherwise.


6 Related Work

Several works investigate the theoretical limits of linearizability verification. Verifying
a single execution against an arbitrary ADT specification is NP-complete [8]. Verify-
ing all executions of a finite-state implementation against an arbitrary ADT specifica-
tion (given as a regular language) is EXPSPACE-complete when program threads are
bounded [2, 9], and undecidable otherwise [3].
    Existing automated methods for proving linearizability of an atomic object imple-
mentation are also based on reductions to safety verification [1, 10, 12]. Vafeiadis [12]
considers implementations where operation’s linearization points are fixed to particular
source-code locations. Essentially, this approach instruments the implementation with
ghost variables simulating the ADT specification at linearization points. This approach
is incomplete since not all implementations have fixed linearization points. Aspect-
oriented proofs [10] reduce linearizability to the verification of four simpler safety prop-
erties. However, this approach has only been applied to queues, and has not produced a
fully automated and complete proof technique. Dodds et al. [5] prove linearizability of

                                            11
stack implementations with an automated proof assistant. Their approach does not lead
to full automation however, e.g., by reduction to safety verification.


7 Conclusion
We have demonstrated a linear-time reduction from linearizability for fixed ADT spec-
ifications to control-state reachability, and the application of this reduction to atomic
queues, stacks, registers, and mutexes. Besides yielding novel decidability results, our
reduction enables the use of existing safety-verification tools for linearizability. While
this work only applies the reduction to these four objects, our methodology also applies
to other typical atomic objects including semaphores and sets. Although this method-
ology currently does not capture priority queues, which are not data independent, we
believe our approach can be extended to include them. We leave this for future work.


References
 [1] P. A. Abdulla, F. Haziza, L. Holı́k, B. Jonsson, and A. Rezine. An integrated
     specification and verification technique for highly concurrent data structures. In
     TACAS ’13. Springer, 2013.
 [2] R. Alur, K. L. McMillan, and D. Peled. Model-checking of correctness conditions
     for concurrent objects. Inf. Comput., 160(1-2), 2000.
 [3] A. Bouajjani, M. Emmi, C. Enea, and J. Hamza. Verifying concurrent programs
     against sequential specifications. In ESOP ’13. Springer, 2013.
 [4] A. Bouajjani, M. Emmi, C. Enea, and J. Hamza. Tractable refinement checking
     for concurrent objects. In POPL ’15. ACM, 2015.
 [5] M. Dodds, A. Haas, and C. M. Kirsch. A scalable, correct time-stamped stack. In
     POPL ’15. ACM, 2015.
 [6] J. Esparza. Decidability and complexity of petri net problems — an introduction.
     In Lectures on Petri Nets I: Basic Models. Springer Berlin Heidelberg, 1998.
 [7] I. Filipovic, P. W. O’Hearn, N. Rinetzky, and H. Yang. Abstraction for concurrent
     objects. Theor. Comput. Sci., 411(51-52), 2010.
 [8] P. B. Gibbons and E. Korach. Testing shared memories. SIAM J. Comput., 26(4),
     1997.
 [9] J. Hamza. On the complexity of linearizability. CoRR, abs/1410.5000, 2014. URL
     http://arxiv.org/abs/1410.5000.
[10] T. A. Henzinger, A. Sezgin, and V. Vafeiadis. Aspect-oriented linearizability
     proofs. In CONCUR ’13. Springer, 2013.
[11] M. Herlihy and J. M. Wing. Linearizability: A correctness condition for concur-
     rent objects. ACM Trans. Program. Lang. Syst., 12(3), 1990.
[12] V. Vafeiadis. Automatically proving linearizability. In CAV ’10. Springer, 2010.




                                           12
8 Appendix

8.1 Examples

For all examples, the domain D is the set of natural numbers N.


Stack Definition of the function last for a sequential execution u:

 – if u contains a PopEmpty operation, last(u) = RPopEmpty ,
 – else if u contains an unmatched Push operation, last(u) = RPush ,
 – else if u contains a Pop operation, last(u) = RPushPop ,
 – else (if u is empty), last(u) = R0 .


Register The register has a method Write used to write a data-value, and a method
Read which returns the last written value. The only input method is Write. Its rules are
R0 and RWR :

                  R0 ≡ ǫ ∈ Register
                 RWR ≡ u ∈ Register ⇒ Write · Read∗ · u ∈ Register

Definition of the function last for a sequential execution u:

 – if u is not empty, last(u) = RWR ,
 – else, last(u) = R0 .


Mutex (Lock) The mutex has a method Lock, used to take ownership of the Mutex,
and a method Unlock, to release it. The only input method is Lock. It is composed of
the rules R0 , RLock and RLU :

                      R0 ≡ ǫ ∈ Mutex
                   RLock ≡ Lock ∈ Mutex
                    RLU ≡ u ∈ Mutex ⇒ Lock · Unlock · u ∈ Mutex

    In practice, Lock and Unlock methods do not have a parameter. Here, the parameter
represents a ghost variable which helps us relate Unlock to their corresponding Lock.
Any implementation will be data independent with respect to these ghost variables.
    Definition of the function last for a sequential execution u:

 – if u contains an Unlock operation, last(u) = RLU ,
 – else if u is not empty, last(u) = RLock ,
 – else, last(u) = R0 .


                                          13
8.2 Proofs of Section 4

Lemma 1 (Abdulla et al. [1]). A data-independent implementation I is linearizable
with respect to a data-independent specification S, if and only if I, is linearizable with
respect to S, .

Proof. (⇒) Let e be a (differentiated) execution in I, . By assumption, it is linearizable
with respect to a sequential execution u in S, and the bijection between the operations
of e and the method events of u, ensures that u is differentiated and belongs to S, .
    (⇐) Let e be an execution in I. By data independence of I, we know there exists
e, ∈ I, and a renaming r such that r(e, ) = e. By assumption, e, is linearizable with
respect to a sequential execution u, ∈ S, . We define u = r(u, ), and know by data
independence of S that u ∈ S. Moreover, we can use the same bijection used for e, ⊑ u,
to prove that e ⊑ u.

Lemma 2. Any data structure S defined in our framework is closed under projection.

Proof. Let u ∈ S and let D ⊆ D. Since u ∈ S, there is a sequence of applications of rules
starting from the empty word ǫ which can derive u. We remove from this derivation
all the rules corresponding to a data-value x < D, and we project all the sequential
executions appearing in the derivation on the D. Since the predicates which appear in
the conditions are all closed under projection, the derivation remains valid, and proves
that u|D ∈ S.

Lemma 3. Let S = R1 , . . . , Rn be a data structure and u a differentiated sequential
execution. Then,                                  [
                        u ∈ S ⇐⇒ proj(u) ⊆             MRi
                                                  i∈{1,...,n}

Proof. (⇒) Using Lemma 2, we know that S is closed under projection. Thus, any
projection of a sequential execution u of S is itself in S and has to match one of the
rules R1 , . . . , Rn .
    (⇐) By induction on the size of u. We know u ∈ proj(u), so it can be decomposed
to satisfy the conditions Guard of some rule R of S. The recursive condition is then
verified by induction.

Lemma 5. Let S be a data structure with rules R1 , . . . , Rn . Let e be a differentiated
execution. If S is step-by-step linearizable, we have (for any j):
                                                             [
                        e ⊑ JR1 , . . . , R j K ⇐⇒ proj(e) ⊑   MRi
                                                                i≤ j

Proof. (⇒) We know there exists u ∈ S such that e ⊑ u. Each projection e′ of e can be
                                                                     S
linearized with respect to some projection u′ of u, which belongs to i MRi according
to Lemma 3.
    (⇐) By induction on the size of e. We know e ∈ proj(e) so it can be linearized with
respect to a sequential execution u matching some rule Rk (k < j) with some witness x.
Let e′ = e r x.

                                           14
    Since S is non-ambiguous, we know that no projection of e can be linearized to a
matching set MRi with i > k, and in particular no projection of e′ . Thus, we deduce that
           S
proj(e′ ) ⊑ i≤k MRi , and conclude by induction that e′ ⊑ JR1 , . . . , Rk K.
    We finally use the fact that S is step-by-step linearizable to deduce that e ⊑ JR1 , . . . , Rk K
and e ⊑ JR1 , . . . , R j K because k < j.

Lemma 6. Let S be a data structure with rules R1 , . . . , Rn . Let e be a differentiated
execution. If S is step-by-step linearizable, we have:

                 e ⊑ S ⇐⇒ ∀e′ ∈ proj(e). e′ ⊑ MR where R = last(e′ )

Proof. (⇒) Let e′ ∈ proj(e). By Lemma 5, we know that e′ is linearizable with respect to
MRi for some i. Since S is non-ambiguous, last(e′ ) is the only rule such that e′ ⊑ MR
can hold, which ends this part of the proof.
   (⇐) Particular case of Lemma 5.

Theorem 1. Let S be a step-by-step linearizable and co-regular data structure and
let I be a data-independent implementation. There exists a regular automaton A such
that:
                              I ⊑ S ⇐⇒ I ∩ A = ∅

Proof. Let A1 , . . . , An be the regular automata used to show that R1 , . . . , Rn are co-
regular, and let A be the (non-deterministic) union of the Ai ’s.
    (⇒) Assume there exists an execution e ∈ I ∩ A. For some i, e ∈ Ai . From the
definition of “co-regular”, we deduce that there exists e′ ∈ proj(e) such that e′ @ MRi ,
where Ri is the rule corresponding to e′ . By Lemma 6, e is not linearizable with respect
to S.
    (⇐) Assume there exists an execution e ∈ I which is not linearizable with respect
to S. By Lemma 6, it has a projection e′ ∈ proj(e) such that e′ @ MRi , where Ri is the
rule corresponding to e′ . By definition of “co-regular”, this means that I ∩ Ai , ∅, and
that I ∩ A , ∅.


8.3 Step-by-step Linearizability

Lemma 4. Queue, Stack, Register, and Mutex are step-by-step linearizable.

Proof. Even though we do not have a unique proof that the data structures are step-
by-step linearizable, we have a model of proof which is generic, which we use for each
data structure. The generic schema we use is the following: we let u′ ∈ JR1 , . . . , Ri K be a
sequential execution such that h r x ⊑ u′ and build a graph G from u′ , whose acyclicity
implies that h ⊑ JR1 , . . . , Ri K. Then we show that we can always choose u′ so that this
G is acyclic.
    For better readability we make a sublemma per data structure.

Lemma 8. Queue is step-by-step linearizable.


                                               15
Proof. Let h be a differentiated history, and u a sequential execution such that h ⊑ u.
We have three cases to consider:
    1) u matches REnq with witness x: let h′ = h r x and assume h′ ⊑ JR0 , REnq K. Since u
matches REnq , we know h only contain Enq operations. The set JR0 , REnq K is composed
of the sequential executions formed by repeating the Enq method events, which means
that h ⊑ JR0 , REnq K.
    2) u matches REnqDeq with witness x: let h′ = hrx and assume h′ ⊑ JR0 , REnq , REnqDeq K.
Let u′ ∈ JR0 , REnq , REnqDeq K such that h′ ⊑ u′ . We define a graph G whose nodes are the
operations of h and there is an edge from operation o1 to o2 if
 1. o1 happens-before o2 in h,
 2. the method event corresponding to o1 in u′ is before the one corresponding to o2 ,
 3. o1 = Enq(x) and o2 is any other operation,
 4. o1 = Deq(x) and o2 is any other Deq operation.
If G is acyclic, any total order compatible with G forms a sequence u2 such that h ⊑ u2
and such that u2 can be built from u′ by adding Enq(x) at the beginning and Deq(x) be-
fore all Deq method events. Thus, u2 ∈ JR0 , REnq , REnqDeq K and h ⊑ JR0 , REnq , REnqDeq K.
     Assume that G has a cycle, and consider a cycle C of minimal size. We show that
there is only one kind of cycle possible, and that this cycle can be avoided by choosing u′
appropriately. Such a cycle can only contain one happens-before edge (edges of type 1),
because if there were two, we could apply the interval order property to reduce the cycle.
Similarly, since the order imposed by u′ is a total order, it also satisfies the interval order
property, meaning that C can only contain one edge of type 2.
     Moreover, C can also contain only one edge of type 3, otherwise it would have to
go through Enq(x) more than once. Similarly, it can contain only one edge of type 4. It
cannot contain a type 3 edge Enq(x) → o1 at the same time as a type 4 edge Deq(x) →
o2 , because we could shortcut the cycle by a type 3 edge Enq(x) → o2 .
     Finally, it cannot be a cycle of size 2. For instance, a type 2 edge cannot form a
cycle with a type 1 edge because h′ ⊑ u′ . The only form of cycles left are the two cycles
of size 3 where:
 – Enq(x) is before o1 (type 3), o1 is before o2 in u′ (type 2), and o2 happens-before
   Enq(x): this is not possible, because h is linearizable with respect to u which
   matches REnqDeq with x as a witness. This means that u starts with the method
   event Enq(x), and that no operation can happen-before Enq(x) in h.
 – Deq(x) is before o1 (type 4), o1 is before o2 in u′ (type 2), and o2 happens-before
   Deq(x): by definition, we know that o1 is a Deq operation; moreover, since h is
   linearizable with respect to u which matches REnqDeq with x as a witness, no Deq
   operation can happen-before Deq(x) in h, and o2 is an Enq operation (or Enq). Let
   d1 , d2 ∈ D such that Deq(d1 ) = o1 and Enq(d2 ) = o2 .
   Since o1 is before o2 in u′ , we know that d1 and d2 must be different. Moreover,
   there is no happens-before edge from o1 to o2 , or otherwise, by transitivity of the
   happens-before relation, we’d have a cycle of size 2 between o1 and Deq(x).
   Assume without loss of generality that o1 is the rightmost Deq method event which
   is before o2 in u′ , and let o12 , . . . , o2s be the Enq (or Enq) method events between o1
   and o2 . There is no happens-before edge o1 ≤hb oi2 , because by applying the interval

                                             16
    order property with the other happens-before edge o2 ≤hb Deq(x), we’d either have
    o1 ≤hb Deq(x) (forming a cycle of size 2) or o2 ≤hb oi2 (not possible because h′ ⊑ u′
    and oi2 is before o2 in u′ ).
    Let u′2 be the sequence u′ where Deq(x) has been moved after o2 . Since we know
    there is no happens-before edge from Deq(x) to oi2 or to o2 , we can deduce that:
    h′ ⊑ u′2 . Moreover, if we consider the sequence of deductions which proves that
    u′ ∈ JR0 , REnq , REnqDeq K, we can alter it when we insert the pair Enq(d1 ) and o1 =
    Deq(d1 ) by inserting o1 after the oi2 ’s and after o2 , instead of before (the conditions
    of the rule REnqDeq allow it).

This concludes case 2), as we’re able to choose u′ so that G is acyclic, and prove that
h ⊑ JR0 , REnq , REnqDeq K.
    3) u matches RDeqEmpty with witness x: let o be the DeqEmpty operation correspond-
ing to the witness. Let h′ = h r x and assume h′ ⊑ Queue. Let L be the set of operations
which are before o in u, and R the ones which are after. Let DL be the data-values ap-
pearing in L and DR be the data-values appearing in R. Since u matches RDeqEmpty , we
know that L contains no unmatched Enq operations.
    Let u′ ∈ Queue such that h′ ⊑ u′ . Let u′L = u′ |DL and u′R = u′ |DR . Since Queue
is closed under projection, u′L , u′R ∈ Queue. Let u2 = u′L · o · u′R . We can show that
u2 ∈ Queue by using the derivations of u′L and u′R . Intuitively, this is because Queue is
closed under concatenation when the left-hand sequential execution has no unmatched
Enq method event, like u′L .
    Moreover, we have h ⊑ u2 , as shown in the following. We define a graph G whose
nodes are the operations of h and there is an edge from operation o1 to o2 if

 1. o1 happens-before o2 in h,
 2. the method event corresponding to o1 in u2 is before the one corresponding to o2 .

    Assume there is a cycle in G, meaning there exists o1 , o2 such that o1 happens-before
o2 in h, but the corresponding method events are in the opposite order in u2 .

 – If o1 , o2 ∈ L, or o1 , o2 ∈ R, this contradicts h′ ⊑ u′ .
 – If o1 ∈ R and o2 ∈ L, this contradicts h ⊑ u.
 – If o1 ∈ R and o2 = o, or if o1 = o and o2 ∈ L, this contradicts h ⊑ u.

This shows that h ⊑ u2 . Thus, we have h ⊑ Queue and concludes the proof that the
Queue is step-by-step linearizable.

Lemma 9. Stack is step-by-step linearizable.

Proof. Let h be a differentiated history, and u a sequential execution such that h ⊑ u.
We have three cases to consider:
    1) (very similar to case 3 of the Queue) u matches RPushPop with witness x: let a
and b be respectively the Push and Pop operations corresponding to the witness. Let
h′ = h r x and assume h′ ⊑ JRPushPop K. Let L be the set of operations which are before
b in u, and R the ones which are after. Let DL be the data-values appearing in L and DR
be the data-values appearing in R. Since u matches RPushPop , we know that L contains
no unmatched Push operations.

                                             17
     Let u′ ∈ JRPushPop K such that h′ ⊑ u′ . Let u′L = u′ |DL and u′R = u′ |DR . Since JRPushPop K
is closed under projection, u′L , u′R ∈ JRPushPop K. Let u2 = a · u′L · b · u′R . We can show that
u2 ∈ JRPushPop K by using the derivations of u′L and u′R .
     Moreover, we have h ⊑ u2 , because if the total order of u2 didn’t respect the happens-
before relation of u2 , it could only be because of four reasons, all leading to a contradic-
tion:

 – the violation is between two L operations or two R operations, contradicting h′ ⊑ u′
 – the violation is between a L and an R operation, contradicting h ⊑ u
 – the violation is between b and another operation, contradicting h ⊑ u
 – the violation is between a and another operation contradicting h ⊑ u

This shows that h ⊑ JRPushPop K and concludes case 1.
   2) u matches RPush with witness x: similar to case 1
   3) u matches RPopEmpty with witness x: identical to case 3 of the Queue

Lemma 10. Register is step-by-step linearizable.

Proof. Let h be a differentiated history, and u a sequential execution such that h ⊑ u and
such that u matches the rule RWR with witness x. Let a and b1 , . . . , b s be respectively
the Write and Read’s operations of h corresponding to the witness.
    Let h′ = h r x and assume h′ ⊑ JRWR K. Let u′ ∈ JRWR K such that h′ ⊑ u′ . Let
u2 = a · b1 · b2 · · · b s · u′ . By using rule RWR on u′ , we have u2 ∈ JRWR K. Moreover, we
prove that h ⊑ u2 by contradiction. Assume that the total order imposed by u2 doesn’t
respect the happens-before relation of h. All three cases are not possible:

 – the violation is between two u′ operations, contradicting h′ ⊑ u′ ,
 – the violation is between a and another operation, i.e., there is an operation o which
   happens-before a in h, contradicting h ⊑ u,
 – the violation is between some bi and a u′ operation, i.e., there is an operation o
   which happens’before bi in h, contradicting h ⊑ u.

    Thus, we have h ⊑ u2 and h ⊑ JRWR K, which ends the proof.

Lemma 11. Mutex is step-by-step linearizable.

Proof. Identical to the Register proof, expect there is only one Unlock operation (b),
instead of several Read operations (b1 , . . . , b s ).


8.4 Regularity

Lemma 7. Queue, Stack, Register, and Mutex are co-regular.

Proof. We have a generic schema to build the automaton, which is first to characterize
a violation by the existence of a cycle of some kind, and then build an automaton rec-
ognizing such cycles. For some of the rules, we prove that these cycles can always be
bounded, thanks to a small model property. For the others, even though the cycles can
be unbounded, we can still build an automaton

                                               18
    (Queue) The empty automaton proves that R0 and REnq are regular, as there is no
execution e′ such that last(e′ ) = R and e′ @ MR for R ∈ {R0 , REnq }. The proofs for
REnqDeq and RDeqEmpty are more complicated and can be found respectively in Lemma 16
and Lemma 19
    (Stack) The proofs can be found in Appendix 8.7.
    (Register and Mutex) Similarly to the rule REnqDeq , we can reprove Lemma 12 (with
sublemmas 13, 14 and 15) to get a small model property, and build an automaton for
the small violations.


8.5 Regularity of R Enq Deq

Lemma 12. Given a history h, if ∀d1 , d2 ∈ Dh , h|{d1 ,d2 } ⊑ REnqDeq , then h ⊑ REnqDeq .

Proof. We first identify constraints which are sufficient to prove that h ⊑ REnqDeq .
Lemma 13. Let h be a history and x a data value of Dh . If Enq(x) ≯ Deq(x), and for all
operations o, we have Enq(x) ≯ o, and for all Deq operations o, we have Deq(x) ≯ o,
then h is linearizable with respect to MREnqDeq

Proof. We define a graph G whose nodes are the element of h, and whose edges include
both the happens-before relation as well as the constraints depicted given by the Lemma.
G is acyclic by assumption and any total order compatible with G corresponds to a
linearization of h which is in MREnqDeq .

    Given d1 , d2 ∈ Dh , we denote by d1 Wh,MR d2 the fact that h|{d1 ,d2 } is linearizable
with respect to R, by using d1 as a witness for the existentially quantified x variable. We
reduce the notation to d1 W d2 when the context is not ambigious.
    First, we show that if the same data value can be used as a witness for x for all
projections of size 2, then we can linearize the whole history (using this same data
value as a witness).

Lemma 14. For d1 ∈ Dh , if ∀d , d1 , d1 W d, then h ⊑ MREnqDeq .

Proof. Since ∀d , d1 , d1 W d, the happens-before relation of h respects the constraints
given by Lemma 13, and we can conclude that h ⊑ MREnqDeq .

    Next, we show the key characterization, which enables us to reduce non-linearizability
                                                            ✚ relation.
with respect to MREnqDeq to the existence of a cycle in the ✚
                                                            W

                                                  ✚ d2 ✚
Lemma 15. If h @ MREnqDeq , then h has a cycle d1 ✚
                                                  W    ✚ ... ✚
                                                       W     ✚ dm ✚
                                                             W    ✚ d1
                                                                  W

Proof. Let d1 ∈ Dh . By Lemma 14, we know there exists d2 ∈ Dh such that d1 ✚  ✚ d2 .
                                                                               W
                                                    ✚ d3 . We continue this construc-
Likewise, we know there exists d3 ∈ Dh such that d2 ✚
                                                    W
tion until we form a cycle.

    We can now prove the small model property. Assume h @ R. By Lemma 15, it has
           ✚ d2 ✚
a cycle d1 ✚
           W    ✚ ... ✚
                W       W✚ dm ✚ ✚ d1 . If there exists a data-value x such that Deq(x)
                                W
happens-before Enq(x), then h|{x} @ REnqDeq , which contradicts our assumptions.

                                             19
     For each i, there are two possible reasons for which di ✚      W✚ d(i mod m)+1 . The first one
is that Enq(di ) is not minimal in the subhistory of size 2 (reason (a)). The second one is
that Deqdi is not minimal with respect to the Deq operations (reason (b)).
     We label each edge of our cycle by either (a) or (b), depending on which one is
true (if both are true, pick arbitrarily). Then, using the interval order property, we have
            ✚ d(i mod m)+1 for reason (a), and d j ✚
            W
that, if di ✚                                        W✚ d( j mod m)+1 for reason (a) as well, then
either di ✚W✚ d( j mod m)+1 , or d j ✚
                                     ✚ d(i mod m)+1 (for reason (a)). This enables us to reduce
                                     W
the cycle and leave only one edge for reason (a).
     We show the same property for (b). This allows us to reduce the cycle to a cycle
of size 2 (one edge for reason (a), one edge for reason (b)). If d1 and d2 are the two
data-values appearing in the cycle, we have: h|{d1 ,d2 } @ REnqDeq , which is a contradiction
as well.

Lemma 16. The rule REnqDeq is co-regular.

Proof. We prove in Lemma 12 that a differentiated history h has a projection h′ such
that last(h′ ) = REnqDeq and h′ @ MREnqDeq if and only if it has such a projection on 1
or 2 data-values. Violations of histories with two values are: i) there is a value x such
that Deq(x) happens-before Enq(x) (or Enq(x) doesn’t exist in the history) or ii) there
are two operations Deq(x) in h or, iii) there are two values x and y such that Enq(x)
happens-before Enq(y), and Deq(y) happens-before Deq(x) (Deq(x) doesn’t exist in the
history).
    The automaton AREnqDeq in Fig. 3 recognizes all such small violations (top branch
for i, middle branch for ii, bottom branch for iii).
    Let I be any data-independent implementation. We show that

  AREnqDeq ∩ I , ∅ ⇐⇒ ∃e ∈ I, , e′ ∈ proj(e). last(e′ ) = REnqDeq ∧ e′ @ MREnqDeq

    (⇒) Let e ∈ I be an execution which is accepted by AREnqDeq . By data independence,
let e, ∈ I r a renaming such that e = r(e, ), and assume without loss of generality
that r doesn’t rename the data-values 1 and 2. If e is accepted by the top or middle
branch of AREnqDeq , we can project e, on value 1 to obtain a projection e′ such that
last(e′ ) = REnqDeq and e′ @ MREnqDeq . Likewise, if e is accepted by the bottom branch,
we can project e, on {1, 2}, and obtain again a projection e′ such that last(e′ ) = REnqDeq
and e′ @ MREnqDeq .
    (⇐) Let e, ∈ I, such that there is a projection e′ such that last(e′ ) = REnqDeq and
 ′
e @ MREnqDeq . As recalled at the beginning of the proof, we know e, has to contain a
violation of type i, ii, or ii. If it is of type i or ii, we define the renaming r, which maps
x to 1, and all other data-values to 2. The execution r(e, ) can then be recognized by the
top or middle branch of AREnqDeq and belongs to I by data independence.
    Likewise, if it is of type iii, r will map x to 1, and y to 2, and all other data-values
to 3, so that r(e, ) can be recognized by the bottom branch of AREnqDeq .

8.6 Regularity of R DeqEmpt y
We first define the notion of gap, which intuitively corresponds to a point in an execution
where the Queue could be empty.

                                                20
Definition 9. Let h be a differentiated history and o an operation of h. We say that h has
a gap on operation o if there is a partition of the operations of h into L ⊎ R satisfying:
  – L has no unmatched Enq operation, and
  – no operation of R happens-before an operation of L or o, and
  – no operation of L happens-after o.
Lemma 17. A differentiated history h has a projection h′ such that last(h′ ) = RDeqEmpty
and h′ @ MRDeqEmpty if and only there exists a DeqEmpty operation o in h such that
there is no gap on o.
Proof. (⇒) Assume there exists a projection h′ such that last(h′ ) = RDeqEmpty and
h′ @ MRDeqEmpty . Let o be a DeqEmpty operation in h′ (exists by definition of last).
    Assume by contradiction that there is a gap on o. By the properties of the gap, we
can linearize h′ into a sequential execution u · o · v where u and v respectively contain
the L and R operations of the partition.
    (⇐) Assume there exists a DeqEmpty operation o in h such that there is no gap on
o. Let h′ be the projection which contains all the operations of h as well as o, except the
other DeqEmpty operations.
    Assume by contradiction that there exists a sequential execution w ∈ MRDeqEmpty
such that h′ ⊑ w. By definition of MRDeqEmpty , w can be decomposed into u · o · v such
that u has no unmatched operation. Let L be the operations of u, and R the operation of
v. Since h′ ⊑ w, the partition L ⊎ R forms a gap on operation o.
    We exploit the characterization of Lemma 17 by showing how we can recognize
the existence of gaps in the next two lemmas. First, we define the notion of left-right
constraints of an operation, and show that this constraints have a solution if and only if
there is a gap on the operation.
Definition 10. Let h be a distinguished history, and o an operation of h. The left-right
constraints of o is the graph G where:
  – the nodes are Dh , the data-values of h, to which we add a node for o,
  – there is an edge from data-value d1 to o if Enq(d1 ) happens-before o,
  – there is an edge from o to data-value d1 if o happens-before Deq(d1 ),
  – there is an edge from data-value d1 to d2 if Enq(d1 ) happens before Deq(d2 ).
Lemma 18. Let h be a differentiated history and o an operation of h. Let G be the
graph representing the left-right constraints of o. There is a gap on o if and only if G
has no cycle going through o.
Proof. (⇒) Assume that there is a gap on o, and let L ⊎ R be a partition corresponding
to the gap. Assume by contradiction there is a cycle dm → · · · → d1 → o → dm in G
(which goes through o). By definition of G, and since o → dm , and by definition of a
gap, we know that all operations with data-value dm must be in R. Since dm → dm−1 ,
the operations with data-value dm−1 must be in R as well. We iterate this reasoning until
we deduce that d1 must be in R, contradicting the fact that d1 → o.
    (⇐) Assume there is no cycle in G going through o. Let L be the set of operations
having a data-value d which has a path to o in G, and let R be the set of other operations.
By definition of the left-right constraints G, the partition L⊎R forms a gap for operation
o.


                                            21
Corollary 1. A differentiated history h has a projection h′ such that last(h′ ) = RDeqEmpty
and h′ @ MRDeqEmpty if and only if it has a DeqEmpty operation o and data-values
d1 , . . . , dm ∈ Dh such that:
  – Enq(d1 ) happens-before o in h, and
  – Enq(di ) happens before Deq(di−1 ) in h for i > 1, and
  – o happens-before Deq(dm ), or Deq(dm ) doesn’t exist in h.
We say that o is covered by d1 , . . . , dm .
Proof. By definition of the left-right constraints, and following from Lemmas 17 and
18.
Lemma 19. The rule RDeqEmpty is co-regular.
Proof. See Section 4.

8.7 Regularity of the Stack rules
Lemma 20. A differentiated history h has a projection h′ such that last(h′ ) = RPushPop
and h′ @ MRPushPop if and only if there exists a projection such that last(h′ ) = RPushPop
and either
  – there exists an unmatched Pop(d) operation in h′ , or
  – there is a Pop(d) which happens-before Push(d) in h′ , or
  – for all Push(d) operations minimal in h′ , there is no gap on Pop(d) in h′ r d.
Proof. Similar to Lemma 17.
Lemma 21. A differentiated history h has a projection h′ such that last(h′ ) = RPushPop
and h′ @ MRPushPop if and only if either:
  – there exists an unmatched Pop(d) operation, or
  – there is a Pop(d) which happens-before Push(d), or
  – there exist a data-value d ∈ Dh and data-values d1 , . . . , dm ∈ Dh such that
      • Push(d) happens-before Push(di ) for every i,
      • Pop(d) is covered by d1 , . . . , dm .
Proof. (⇐) We have three cases to consider
  – there exists an unmatched Pop(d) operation: define h′ = h|{d} ,
  – there is a Pop(d) which happens-before Push(d): define h′ = h|{d} ,
  – there exist a data-value d ∈ Dh and data-values d1 , . . . , dm ∈ Dh such that
      • Push(d) happens-before Push(di ) for every i
      • Pop(d) is covered by d1 , . . . , dm .
    Define h′ = h|{d,d1 ,...,dm } . We have last(h′ ) = RPushPop because h′ doesn’t contain
    PopEmpty operations nor unmatched Push operations. Assume by contradiction
    that h′ ⊑ MRPushPop , and let w ∈ MRPushPop such that h′ ⊑ u. Since Push(d)
    happens-before Push(di ) (for every i) the witness x of w ∈ MRPushPop has to be the
    data-value d. This means that w = Push(d) · u · Pop(d) · v for some u and v with no
    unmatched Push.
    Thus, there is a gap on operation Pop(d) in h′ rd, and that Pop(d) cannot be covered
    by d1 , . . . , dm .

                                                22
    (⇒) Let h′ be a projection of h such that last(h′ ) = RPushPop and h′ @ MRPushPop .
Assume there are no unmatched Pop(d) operation, and that for every d, Pop(d) doesn’t
happens-before Push(d). This means that h′ is made of pairs of Push(d) and Pop(d)
operations.
    Let Push(d) be a Push operation which is minimal in h′ . We know there is one,
because we assumed that last(h′ ) = RPushPop , and we know that there is a Push which
is minimal because for every d, Pop(d) doesn’t happens-before Push(d).
    By Lemma 20, we know that there is no gap on Pop(d). Similarly to Lemma 18 and
Corollary 1, we deduce that there are data-values d1 , . . . , dm ∈ Dh′ such that Pop(d) is
covered by d1 , . . . , dm . Our goal is now to prove that we can choose d and d1 , . . . , dm
such that, besides these properties, we also have that Push(d) happens-before Push(di )
for every i. Assume there exists i such that Push(d) doesn’t happen-before Push(di ). We
have two cases, either Pop(d) is covered by d1 , . . . , di−1 , di+1 , . . . , dm , in which case we
can just get rid of di ; or this is not the case, and we can choose our new d to be di and
remove di from the list of data-values. We iterate this until we have a data-value d ∈ Dh
such that
  – Push(d) happens-before Push(di ) for every i,
  – Pop(d) is covered by d1 , . . . , dm .

Lemma 22. The rule RPushPop is co-regular.

Proof. The automaton Fig. 4 recognizes the violations given by Lemma 21. The proof
is then similar to Lemma 19.

Lemma 23. The rule RPush is co-regular.

Proof. We can make a characterization of the violations similar to Lemma 21. This rule
is in a way simpler, because the Push in this rule plays the role of the Pop in RPushPop .

Lemma 24. The rule RPopEmpty is co-regular.

Proof. Identical to Lemma 19 (replace Enq by Push, Deq by Pop, and DeqEmpty by
PopEmpty).

8.8 Regular automata used to prove regularity




                                                23
       M(2)                  M(2)

               ret Deq(1)
        q7                    q8


  call Deq(1)


   M(1), M(2)           M(1), M(2)               M(1), M(2)

               ret Deq(1)            ret Deq(1)
        q4                    q5                       q6


  call Deq(1)


       M(3)                  M(3)                  M(3)                     M(3)                 M(3)

              call Enq(1)            ret Enq(1)             call Enq(2)            ret Deq(2)
        q0                    q1                       q1                    q2                   q3


  call Deq(2)


Fig. 3. A non-deterministic automaton recognizing REnqDeq violations. The top branch recognizes
executions which have a Deq with no corresponding Enq. The middle branch recognizes two
Deq’s returning the same value, which is not supposed to happen in a differentiated execution.
The bottom branch recognizes FIFO violations. By the closure properties of implementations, we
can assume the call Deq(2) are at the beginning.


     M(3)                   M(3)                 M(3)                 M(3)                 M(3)                 M(3)

             call Push(2)          ret Push(2)          ret Push(1)          call Pop(2)          ret Pop(1)
       q0                    q1                   q2                   q3                   q4                   q6


                                          call Push(1)                      call Pop(1)           ret Push(1)


                                                                                            q5          M(3)



Fig. 4. An automaton recognizing RPushPop violations. Here we have a Push(2) operation, whose
corresponding Pop(2) operation is covered by Push(1)/Pop(1) pairs. The Push(2) happens-
before all the pairs. Intuitively, the element 2 cannot be popped from the Stack there is always at
least an element 1 above it in the Stack (regardless of how linearize the execution).



                                                  24
