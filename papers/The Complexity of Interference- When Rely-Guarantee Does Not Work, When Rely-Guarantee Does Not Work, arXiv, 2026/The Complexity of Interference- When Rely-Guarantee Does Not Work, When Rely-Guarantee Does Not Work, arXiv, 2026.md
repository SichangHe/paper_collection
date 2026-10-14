                                                        The Complexity of Interference:
                                                      When Rely/Guarantee Does Not Work

                                                                          Nisansala P. Yatapanage

                                                          School of Computing, The Australian National University
arXiv:2609.27392v1 [cs.LO] 23 Sep 2026




                                                Abstract. Rely/Guarantee is a well-known verification technique for reason-
                                                ing about concurrent programs. However, for some algorithms, devising suit-
                                                able rely and guarantee conditions is challenging, due to the strong interfer-
                                                ence exhibited in these algorithms. The Ben-Ari concurrent garbage collector is
                                                an algorithm where the complex interactions between the components prevent
                                                the construction of compositional rely and guarantee conditions. This paper in-
                                                vestigates an approach for verifying the Ben-Ari algorithm, which enables rea-
                                                soning to be performed in a more compositional manner in cases where com-
                                                positional reasoning would not otherwise be possible. This is accomplished by
                                                reasoning that a given property holds for all instances of a particular variable
                                                and then instantiating the variable to the local variable required. As well as
                                                providing a reasoning approach which is more compositional, the result is the
                                                identification of the core property required of a component, thus enabling a
                                                deeper understanding about the reasons why the algorithm works correctly.
                                                This helps to reveal the reasons why the rely/guarantee approach does not
                                                work directly for some problems.


                                         1   Introduction

                                         Interference is a key aspect of concurrent algorithms, yet the study of interference
                                         has received very little attention. Concurrency creates complex interactions which
                                         make verification challenging. The core challenge is in specifying the interference
                                         that concurrent processes exhibit on each other.
                                             Rely/guarantee [Jon90] is a well-known reasoning technique revolving around
                                         interference. The interference a process can accept from its environment is specified
                                         abstractly, as the rely predicate, without needing to refer to the detailed behaviour
                                         of the environment processes. The guarantee of a process is a predicate describing
                                         the behaviour that the process exhibits. To verify that two processes can operate
                                         together concurrently, it must be shown that the guarantee of one process implies
                                         the rely of the other, and vice versa. Rely/guarantee is a useful technique which
                                         works well for many concurrent algorithms. However, there is a class of algorithms
                                         for which rely/guarantee properties cannot easily be devised. Understanding the
                                         reasons why it is difficult to devise suitable rely/guarantee properties is essential, in
                                         order to develop suitable verification techniques for these algorithms.
                                             The algorithms which have been successfully verified using rely/guarantee fall
                                         into certain classes. The first group are the classic rely/guarantee examples, often
                                         used by Jones, the creator of rely/guarantee [Jon90]. These problems include findp,
2                                                     The Complexity of Interference

which uses parallel threads to speed up the search for the first index of an array
satisfying a given property p, and the parallel Sieve of Eratosthenes, which uses
parallel threads to identify the set of prime numbers below a given maximum value.
See [HJ18] for rely/guarantee developments of these problems. These problems
all fall into the same class, which contain algorithms that are inherently parallel
rather than concurrent. While there is some interference when writing the results of
the parallel searches, this is only minor interference which is easily handled using
constructs such as Compare-and-Swap.
    Rely/guarantee is often combined with other logics, in particular separation log-
ics, as with RGSep [VP07]. RGSep uses rely/guarantee for the shared parts of the
memory and separation logic for the local parts. These logics are ideal for problems
which have an aspect of separation present.
   Non-blocking concurrent algorithms are the most challenging type to verify. Rely/
guarantee has been used for verifying a non-blocking concurrent garbage collector
[JY19], Simpson’s four-slot algorithm for concurrent readers and writers [JH16],
and concurrent stack and queue algorithms in [Yat24]. For all of these approaches, it
was concluded that rely and guarantee conditions could not be devised in a straight-
forward manner. In [JH16], in order to verify Simpson’s four-slot algorithm, a new
notion, possible values was devised, to essentially describe the history of values held
by a variable throughout the program execution. In [JY19], the notion of possible
values was again used, in order to handle the unpredictable nature of the problem.
    In [Yat24], it is demonstrated that some concurrent stacks and queues pose prob-
lems for constructing rely conditions, because multiple environment processes could
interfere with each other, thus making it difficult to identify conditions which hold
over any arbitrary set of environment steps.
    In [JY19], Ben-Ari’s concurrent garbage collector is specified with rely/guarantee,
but it is concluded that there is no way of specifying suitable rely and guarantee con-
ditions without breaking compositionality. The Ben-Ari algorithm allows both the
Mutator and the Collector to run at the same time without corrupting the memory.
The difficulty with devising suitable rely and guarantee conditions is due to a specific
interaction between the components, where the interference could cause memory in
use to be incorrectly reclaimed by the Collector. While the algorithm prevents this,
the reason why it works is not obviously clear.
     This paper investigates the interference in this algorithm further. In particular,
the interference is handled using a novel proof technique, whereby the processes are
verified without requiring them to reason about each other’s local variables. Instead,
the rely of the Collector, which contains a local variable, is shown to be satisfied by
the Mutator by instead proving that the Mutator maintains a certain property over
all the variables of a set. When instantiated with the specific variable required by the
Collector, the rely is shown to hold. The property essentially acts as a bridge between
the guarantee of the Mutator and the rely of the Collector. This thereby allows both
processes to ensure that their interactions are safe, without having to specifically
reference local variables of one process in the other’s guarantee. This idea is very
briefly mentioned in [JY19] as one possible verification method, but not explored.
The Complexity of Interference                                                         3

    There are two interesting aspects which arise from this. The first is the proof tech-
nique itself, which is applicable to other problems. The technique allows strongly in-
tertwined behaviour to be separated, without requiring ghost variables. The second
interesting aspect is the abstract predicate which is used for the algorithm. The pred-
icate provides more than a simple bridge between the two components; it uncovers
the core property that is required by the Collector. This reveals a deeper insight into
why the algorithm works. Most verification approaches focus on showing that an
algorithm is correct, but does not provide any understanding of why it works. Un-
derstanding this can aid in devising further concurrent algorithms.
    Finally, the approach also provides insights into the nature of interference and
why rely/guarantee is insufficient for some algorithms.



2   Rely/Guarantee Reasoning

Rely/guarantee reasoning [Jon90] is a compositional reasoning approach based on
Hoare logic. Instead of the usual Hoare triples, there are quintuples, with an ad-
ditional rely and guarantee condition. For each process, its rely condition specifies
what it is able to handle from the environment, while the guarantee details what
the process ensures to do. The rely/guarantee laws (see [HJ18] for an introduction
using an algebraic approach) require that the guarantee of each process must satisfy
the rely of the other, ensuring that the processes can run concurrently. Figure 1 pro-
vides an overview. Note that the rely and guarantee conditions must hold transitively
over all of the environment, respectively program, steps.




                            Fig. 1. Rely/Guarantee Reasoning
4                                                     The Complexity of Interference

3   Ben-Ari Concurrent Garbage Collector


The Ben-Ari garbage collection algorithm [BA84] is a mark-and-sweep algorithm
where the Collector runs concurrently with the Mutator, thus allowing lost memory
to be reclaimed while a program is running. Fig. 2 shows the cycle of behaviour by
the two components of the system: the Mutator which uses and loses memory and
the Collector which must free the garbage.




                       Fig. 2. Overview of the Garbage Collector




     The Mutator algorithm consists of three actions: redirecting, allocating and re-
moving. A redirect changes a link to point to a different node. Nodes can be allocated
by taking a new node from the Free set, and links can be removed. The Mutator may
choose to perform any of the actions at any time. Note that the removing of a link
can be considered to be the same as a redirect, where a link is changed to point to
nil.
    The algorithm for the Collector operates in three phases: Mark, Sweep and Unmark.
Nodes may be either marked or unmarked. The Collector uses the marking to de-
termine which nodes are garbage and need to be reclaimed. It starts by iterating
through all of the addresses in memory and for each marked address, all the ad-
dresses it points to (referred to as the child nodes), are marked as well. After every
cycle, the number of marked nodes is checked. If it has increased, the cycle runs
again, searching for marked nodes with unmarked children and marking them. An
outline of the algorithm for this phase of the Collector’s operation, called Mark, is
shown in Figure 3, adapted from [JY19].
    During the Sweep phase, executed after Mark, the Collector reclaims any un-
marked nodes and stores them into the Free set. The Unmark phase is responsible
for unmarking all of the nodes, except the roots and free set, ready for the next
round of Mark.
The Complexity of Interference                                                       5


                            Mark △
                               do
                                  currentCount = get the number of marked nodes
                                  Propagate
                               while (currentCount == originalCount)

                 Propagate △
                     consid = { };
                     do while consid ⊆ Addr
                       let x ∈ (Addr − consid) in
                       if x ∈ marked then mark x’s children
                       else skip
                       fi;
                       consid = consid ∪ {x}
                     od


                       Fig. 3. Code for Mark, adapted from [JY19]



3.1   Interference in the Algorithm

The algorithm as stated above has a significant issue when run concurrently with an
active Mutator. The issue is that addresses that are currently in use could be deemed
garbage by the Collector and incorrectly freed. To understand why this is the case,
consider the following example, shown in Fig. 4. Suppose that the Collector is in
the middle of its Mark phase. It has examined address A, finding that there are no
children. The Mutator then interrupts, and changes the pointer from A to point to
C. The Mutator then removes the link from B to C. The Collector then resumes, but
it does not check A again. The Collector moves on to B, which no longer has any
children. Node D is then checked, but is not marked. The cycle completes, and the
number of marked nodes has not increased, so the cycle does not run again. The
Collector begins the Sweep phase, where it removes all unmarked nodes. This now
includes node C, which is therefore removed, even though it is in use.
    The Ben-Ari algorithm avoids this situation by requiring the Mutator to perform
some actions in order to help the Collector: whenever the Mutator redirects a pointer
in the heap, it must mark the new address. This ensures that the Collector will not
inadvertently deallocate memory that is still in use. In the previous example, after
the Mutator redirects the pointer from A to point to C, it must mark C. This ensures
that even though the Collector does not mark C, at the end of the cycle, the Collector
will still recognise that the number of marked nodes has increased, and run the
cycle again. On the next cycle, the link from A to C will ensure that C is marked. The
essential requirement is that the Mutator must mark the destination node before
performing another update, such as a deletion as in the example.
    There are many ways of specifying the interference in this scenario. There needs
to be a way of specifying the required order of the three actions of the Mutator: redi-
rect; mark; delete. The problem only arises when a redirect is followed immediately
by a delete. The difficulty with devising a rely condition for the Collector is that it
6                                                      The Complexity of Interference




Fig. 4. Example of the Collector Incorrectly Removing Addresses (Green nodes are marked)




would have to specify this order, whereas rely conditions are binary conditions hold-
ing between the start and end states of a block of environment steps. There is no
way to refer to steps in the middle. Furthermore, the Mutator’s actions might not all
fall into a single block of steps. The Mutator might perform a redirect and then be
interrupted by the Collector. It must be ensured that when the Mutator resumes, it
will mark before any further actions.
     One approach for modelling this is to use a ghost variable, as in [JY19]. A ghost
variable tbm (or to be marked) is used. This is a shared ghost variable, which the
Mutator updates whenever there is a pending mark operation. The rely condition
of the Collector needs to refer to this ghost variable, requiring the Mutator to mark
any pending nodes before any further actions. The disadvantage of this approach is
that the Collector must have detailed knowledge about the Mutator’s behaviour, i.e.
which node has just been modified and is due to be marked.
     Another approach would be to use temporal logic to specify the required order
of the steps. When considering only the Mutator’s steps on the trace, the temporal
logic condition required would state that a redirect step should be followed imme-
diately by a marking step. This would require defining the temporal logic behaviour
on projected traces consisting of only the Mutator’s steps. However, such an ap-
proach requires reasoning over the entire traces, instead of utilising the benefit of
rely/guarantee where reasoning is performed over single steps or blocks of steps.
     Instead of trying to model the interference directly, it is useful to think of the
problem in a different way. The Collector requires the Mutator to mark between
changes. However, why does it want this? When examining the specific scenario
discussed above, it is clear that marking is required to prevent the Collector from
missing nodes that are in use. What is not so clear is whether this is the only scenario
where nodes can be missed. When verifying by focussing on this specific scenario, it
The Complexity of Interference                                                        7

is impossible to be certain that it is the only situation that causes problems. Instead,
the method shown in this paper reveals a deeper insight into why marking is needed.



3.2     Required Definitions From [JY19]


Before proceeding, some preliminary definitions are required, taken directly from
[JY19], presented using VDM syntax. For further details on VDM, please refer to
[Jon90].
    The state of the concrete representation consists of a set of addresses that form
the roots, the heap and a set of free addresses. It is defined as follows:
      Σ1 :: roots : Addr-set
            hp    : Heap
            free : Addr-set
      where

      inv-Σ1 (mk-Σ1 (roots, hp, free)) △ free ∩ reach(roots, hp) = { }




where the Heap is defined as a mapping from a pair, consisting of an address and
an index, to an address:
                               m
      Heap = (Addr × Index) −→ Addr

and the function reach returns all the nodes which are reachable from a given set s,
by following child links transitively. The invariant ensures that there is no overlap
between the free addresses and the ones which are currently in use.



4     Rely of the Collector

To determine why the Collector requires marking, it is helpful to reason about its be-
haviour. The Collector attempts to ensure that all marked nodes in the set of consid-
ered nodes, consid, have marked children. Without any interference by the Mutator,
the Collector would maintain this property; it is only the Mutator’s modification of
links while the Collector is still in progress that could undermine this. The Mutator’s
marking of all target nodes after a change solves the problem.
    These observations suggest that a property can-be-marked would be useful, which
states that the child of a marked node that has already been considered is either
marked as well or can still be marked in the future by Propagate. In order to make
the property as general as possible, instead of using consid, can-be-marked takes as
a parameter an abstract set s:
8                                                             The Complexity of Interference

     can-be-marked : Addr-set × Σ2 → B
     can-be-marked(s, mk-Σ2 (roots, hp, free, marked)) △
         ∀a ∈ (marked ∩ s) ·
             ∀i ∈ dom hp(a) ·
                  hp(a, i) ∈ (Addr − marked) ∧ hp(a, i) ∈ reach(roots, hp) ⇒
                  ∃(c, j) ∈ dom hp ·
                        (c ∈ reach(roots) ∨ c ∈ reach(marked ∩ (Addr − s), hp)) ∧
                        (c ∈
                           /s∨c∈   / marked) ∧
                        a ̸= c ∧ hp(c, j) = hp(a, i)


    The can-be-marked property states that for every node that is marked and in the
set s, if one of its children are unmarked, then there must be another path to that
node via another node c. This node c should be reachable from the roots, or from a
marked node that is not in s. This ensures that c will eventually be marked on some
iteration of Propagate.1 The c ∈/s∨c∈ / marked requirement ensures that c has either
not been considered yet by the Collector or has not been marked yet, although it will
be marked in the future as it is reachable from a marked node.

     all-ok : Addr-set × Σ2 → B
     all-ok(s, mk-Σ2 (roots, hp, free, marked)) △
          ∀(a, j) ∈ dom hp ·
                a ∈ s ∧ a ∈ marked ∧ hp(a, j) ∈ reach(roots, hp) ⇒ hp(a, j) ∈ marked


     This property is stronger than can-be-marked, stating that there are no marked
nodes with unmarked children. At whatever time the Collector is interrupted, it
would have a local consid set containing the addresses that have been explored so
far. At the point that they were added to the consid set, these addresses would all
have satisfied all-ok, as all marked nodes in the set would have had marked children.
     However, there is one situation that changes this. If the Collector marks a child
of a marked node, it is possible that the child was already in consid. In that case, it
violates all-ok, as there would then be a marked node in consid without necessarily
having marked children. Recall that when a node is explored, if it is not marked,
it is just added to consid without marking its children. This is not a problem for
the Collector: as the number of marked nodes increases, the Propagate loop will run
again, finding the problem node on the next iteration.
     Therefore, instead of the consid set, there is a subset, referred to as safe, which
are the nodes that the Collector will not necessarily revisit. These are the nodes of
consid that still satisfy all-ok at the point when the Mutator interrupts.
     Since the Collector will assume that the safe addresses have finished being exam-
ined, the Mutator must ensure that there is some way that will cause the Collector
to revisit them. There are two options: either there is another path to the node that
1
    It may seem sufficient to state that c is reachable from the roots, but it is possible that the
    redirection could have broken the path from the roots to c. In such a case, c will still be
    found in the search via the broken path, if that path was already partially explored.
The Complexity of Interference                                                        9

is yet to be explored, as defined by can-be-marked, or the number of marked nodes
have increased, which will cause the Collector to run another cycle of Propagate.
    This reasoning gives the following rely condition:

     rely-Collector : Σ2 × Σ2 → B
     rely-Collector(σ, σ′ ) △
          marked ⊆ marked′ ∧
          (∀(c, i) ∈ dom hp ·
               hp′ (c, i) ̸= hp(c, i) ∧ hp′ (c, i) ∈ (Addr − free)
               ⇒ hp′ (c, i) ∈ reach(roots, hp)) ∧
          (all-ok(safe, σ) ⇒ can-be-marked(safe, σ′ ) ∨ (σ′ .marked > σ.marked))




5     Holds For All Reasoning

An interesting observation is that the Mutator intuitively satisfies the conditions re-
quired by the Collector in rely-Collector without needing to understand the notion
of safe, nor even the contents of safe; these conditions are simply satisfied by the
Mutator’s actions, in particular its marking of a target node before proceeding to
make another change. This suggests that the Mutator’s actions satisfy these condi-
tions not just on the safe set, but on any similar set that possesses certain qualities.
This abstract set forms the basis of this paper’s approach for reasoning about this
problem. The outline of the approach in general is as follows:


Theorem 1. Holds For All

                              guar-B(σ, σ′ )
                              p(s, σ)
                              ∀w · guar-B(σ, σ′ ) ∧ p(w, σ) ⇒ q(w, σ, σ′ )
                              p(s, σ) ∧ q(s, σ, σ′ ) ⇒ rely-A(σ, σ′ )
                holds-for-all
                              rely-A(σ, σ′ )

     The idea is to find a suitable property p and a relation q such that if:

    – the guarantee of one of the components, B, holds between the states σ and σ′ ,
    – a property p holds on σ,
    – for any w, if p holds on σ and the guarantee of B holds between σ and σ′ , then
      a relation q holds over the two states and w, and
    – the property p holding on σ with a specific variable s, and the relation q holding
      between σ and σ′ with s, implies the rely of the other component, A,

then it can be concluded that rely-A holds between σ and σ′ .

   Proof.
Since guar-B holds and p holds over σ and s, then from the third clause, it can be
10                                                         The Complexity of Interference

concluded that q(s, σ, σ′ ) holds. From the last clause, this implies that rely-A holds
between σ and σ′ .                                                                    ⊔
                                                                                      ⊓
    For this particular application of the rule, the variable s is a set of addresses.
This allows reasoning about the safe set of the Collector without actually referring to
the safe set. The Mutator is required to show that the third clause above holds over
any variable w. This proof does not require the Mutator to have knowledge of what
addresses are currently in the safe set. Using the above reasoning, this establishes
that the rely condition of the Collector holds, which refers to the safe set.


5.1     The Mutator Proof Obligations

Applying the Holds For All theorem, with all-ok(s, σ′ ) as p and can-be-marked(s, σ′ ) ∨
(σ′ .marked > σ.marked) as q, the proof obligation of the Mutator is to show that
for any set of addresses, if p holds on σ, then q holds between σ and σ′ .
    The Mutator consists of two atomic operations, Change and MarkTbm, which are
described below. As these operations are atomic, the Mutator’s overall guarantee is
formed by the postconditions of each of the operations.
    The post-Change condition ensures that if a redirection occurred, the new target
node is stored as tbm and that node was reachable from the roots in the original hp.
Note that it may no longer be reachable in hp′ , but as long as it was reachable in the
previous state, it satisfies the required conditions of the Collector.

      post-Change : Σ2 × Σ2 → B
      post-Change(σ, σ′ ) △
           let (x, k) = ι (x, k) · hp(x, k) ̸= hp′ (x, k) in
           ((hp′ (x, k) = nil ∧ tbm′ = nil) ∨
           (tbm′ = hp′ (x, k) ∧ hp′ (x, k) ∈ reach(roots, hp)))
           ∧ σ′ .marked = σ.marked


After Mark-Tbm finishes, the node that was stored as tbm must have been marked.

      post-MarkTbm : Σ2 × Σ2 → B
      post-MarkTbm(σ, σ′ ) △
           ((tbm = nil ∧ marked′ = marked) ∨
           marked′ = marked ∪ {tbm}) ∧ tbm′ = nil


    Starting from an all-ok state, the Mutator can execute post-Change. This results
in can-be-marked holding on the final state, given by Lemma 1.

Lemma 1. all-ok(s, σ) ∧ post-Change(σ, σ′ ) ⇒ can-be-marked(s, σ′ ) ∧ tbm-put(s, σ′ )

The above lemma also results in the condition tbm-put. The tbm-put property ensures
that tbm is the only unmarked node with a marked parent in the set. The need for this
new property is that while can-be-marked ensures that all nodes requiring marking
are accessible via another unexplored node, it does not ensure that such nodes are
The Complexity of Interference                                                          11

recorded by the tbm variable. This is needed for specifying the requirements under
which MarkTbm executes.

      tbm-put : Addr-set × Σ2 → B
      tbm-put(s, mk-Σ2 (roots, hp, free, marked)) △
          ∀(a, j) ∈ dom hp ·
               (σ.tbm ̸= hp(a, j) ∧ a ∈ s ∧ a ∈ marked ⇒
                         hp(a, j) = nil ∨ hp(a, j) ∈ marked)

    If can-be-marked holds on a set s, as well as the property tbm-put, then executing
MarkTbm will ensure that the set either satisfies all-ok or the number of marked
nodes has increased. This is given by Lemma 2. If the Mutator was responsible for
adding an unmarked node, tbm-put holds. Therefore, after the MarkTbm operation,
in which tbm is marked, ideally, there would not be any more problem nodes. How-
ever, it is possible for the Mutator to mark a destination node that is already in the
set s, similarly to how the Collector could mark a child that is already in consid. In
such a case, all-ok would not hold, but the number of marked nodes would have
increased.2

Lemma 2. can-be-marked(s, σ) ∧ tbm-put(s, σ) ∧ post-MarkTbm(σ, σ′ ) ⇒
                                        all-ok(s, σ′ ) ∨ (σ′ .marked > σ.marked)

    Lemma 1 requires all-ok before Change executes. Since the Ben-Ari algorithm
requires the Mutator to mark in between every change, there needs to be a way
of constructing a suitable set that satisfies all-ok after a MarkTbm operation. After
marking, as discussed above, there may be at most one new problem node. Thus,
the set of all nodes in s except that node satisfies all-ok.
    The alternation of Change and MarkTbm potentially results in a smaller set each
time that MarkTbm executes. Each time the set reduces, the number of marked nodes
has increased, by Lemma 2. Therefore, for any sequence of Mutator steps, either
can-be-marked can be shown to hold at the end of the sequence, or the number of
marked nodes would have increased. This satisfies the requirements of rely-Collector.

5.2     Showing that rely-Collector holds
In order to use the HoldsForAll rule, it now remains to be shown that using all-ok(s, σ′ )
as p and can-be-marked(s, σ′ ) ∨ (σ′ .marked > σ.marked) as q implies rely-Collector.
This is trivial for the last clause of rely-Collector. The other clauses do not involve any
internal variables of the Collector, so it is simple to directly prove that the Mutator
satisfies these clauses.
    As explained earlier, the set which satisfies all-ok or can-be-marked may decrease
after steps of the Collector or Mutator. The safe set represents the set for which the
 2
     Note that it is possible for a MarkTbm operation to not increase the number of marked
     nodes, if the node it attempts to mark is already marked. Nevertheless, since the node
     is already marked, such cases cannot result in a new problem node, and therefore,
     can-be-marked still holds.
12                                                    The Complexity of Interference

Collector has preserved all-ok/can-be-marked. If the Mutator reduces the set, it must
increase the number of marked nodes, as shown by the q clause. This guarantees that
another round of marking will take place and the required nodes will be identified.


6    Related Work and Conclusion

This paper has proposed an approach for verifying algorithms with two components,
known as Holds For All reasoning, for reasoning about the local variables of another
component, without the need for shared auxiliary variables. The idea is to identify a
general property that holds over an abstract, universally quantified variable, which
is then instantiated to the particular local variable required. The proofs are currently
being mechanised and will be completed for future work.
     Apart from the benefit of avoiding breaks in compositionality, the approach is
useful because it helps to identify what the required core property of the component
is. Even though the rely condition of the Collector focussed on the safe local variable,
the actual needs of the Collector were identified through the can-be-marked property.
     Havelund [Hav99] verifies the Ben-Ari algorithm using the PVS theorem prover
and also with the Murφ model checker in order to perform a comparison of the
two techniques. A requirement is formalised that no marked node can point to an
unmarked node, but, as stated in the paper, the proofs contain 55 lemmas, and
therefore, it is not easy to determine the overall properties that are required, nor the
details of how they were verified. Both of the proofs given are not compositional,
relying instead on an overall proof of the system as a whole.
     Another attempt at verifying Ben-Ari’s algorithm is [NE00], which uses Owicki-
Gries reasoning [OG76]. The proof uses two auxiliary variables. As well as this,
the key property of the Collector given in this paper, can-be-marked, is not identi-
fied in [NE00]. A few other attempts at the verification of Ben-Ari’s algorithm exist,
but some were shown to contain flaws, such as Ben-Ari’s own proof of correctness.
Havelund [Hav99] gives an interesting account of several authors who encountered
similar mistakes in reasoning about Ben-Ari’s algorithm, demonstrating how difficult
it is to prove its correctness, due to the intricate interactions between the compo-
nents. For this reason, identifying a clear requirement for the Collector to perform
correctly is essential.
     Identifying the core property enables more efficient algorithms to potentially be
designed. For example, it is clear from the can-be-marked property that the Mutator
marks excessive nodes than it needs to in order to ensure that the Collector’s marking
is kept stable. An alternative algorithm may be devised which allows the Mutator
access to the consid set, in order to determine whether or not a particular node needs
to be marked. This is similar to the algorithm verified in [ZCD+ 17], in which the two
components have access to each other’s current state. Such approaches would break
compositionality.
     The identification of the core property also provides a deeper understanding of
how Ben-Ari’s algorithm works, and in particular, why it works. The same approach
could be useful for understanding further classic algorithms, for which it is difficult
to understand why they work.
The Complexity of Interference                                                            13

References
[BA84]   Mordechai Ben-Ari. Algorithms for on-the-fly garbage collection. ACM Transactions
         on Programming Languages and Systems, 6(3):333–344, 1984.
[Hav99] Klaus Havelund. Mechanical verification of a garbage collector. In International
         Parallel Processing Symposium, pages 1258–1283. Springer, 1999.
[HJ18] I. J. Hayes and C. B. Jones. A guide to rely/guarantee thinking. In J. P. Bowen,
         Z. Liu, and Z. Zhang, editors, Engineering Trustworthy Software Systems, volume
         11174 of LNCS, pages 1–38. Springer International Publishing, Cham, 2018.
[JH16] Cliff B. Jones and Ian J. Hayes. Possible values: Exploring a concept for concurrency.
         Journal of Logical and Algebraic Methods in Programming, 85(5, Part 2):972–984,
         August 2016.
[Jon90] C. B. Jones. Systematic Software Development using VDM. Prentice Hall Interna-
         tional, second edition, 1990.
[JY19] Cliff B. Jones and Nisansala Yatapanage. Investigating the limits of rely/guarantee
         relations based on a concurrent garbage collector example. Formal Aspects of Com-
         puting, 31:353–374, 2019.
[NE00] Leonor Prensa Nieto and Javier Esparza. Verifying single and multi-mutator
         garbage collectors with Owicki-Gries in Isabelle/HOL. In MFCS 2000, volume 1893
         of LNCS, pages 619–628. Springer, 2000.
[OG76] S. S. Owicki and D. Gries. An axiomatic proof technique for parallel programs I.
         Acta Informatica, 6(4):319–340, 1976.
[VP07] Viktor Vafeiadis and Matthew Parkinson. A marriage of rely/guarantee and separa-
         tion logic. In Luís Caires and Vascot Vasconcelos, editors, CONCUR 2007 – Concur-
         rency Theory, volume 4703 of Lecture Notes in Computer Science, pages 256–271.
         Springer, 2007.
[Yat24] Nisansala P. Yatapanage. Exploring the boundaries of rely/guarantee and links to
         linearisability. In Ana Cavalcanti and James Baxter, editors, The Practice of Formal
         Methods: Essays in Honour of Cliff Jones, Part II, volume 14781 of Lecture Notes in
         Computer Science, pages 247–267. Springer, 2024.
[ZCD+ 17] Yannick Zakowski, David Cachera, Delphine Demange, Gustavo Petri, David
         Pichardie, Suresh Jagannathan, and Jan Vitek. Verifying a concurrent garbage col-
         lector using a rely-guarantee methodology. In Mauricio Ayala-Rincón and César A.
         Muñoz, editors, Interactive Theorem Proving - 8th International Conference, ITP
         2017, Brasília, Brazil, September 26-29, 2017, Proceedings, volume 10499 of Lec-
         ture Notes in Computer Science, pages 496–513. Springer-Verlag, 2017.
14                                                      The Complexity of Interference

7    Appendix

This Appendix contains the proof of Lemma 1. The other lemmas are simple to prove
and less interesting to discuss in detail.
   Proof of Lemma 1:
Assume all-ok(s, σ) and post-change(σ, σ′ ).

   From post-Change(σ, σ′ ), let (x, k) = ι (x, k) · hp(x, k) ̸= hp′ (x, k) (the change
which occurred). There are two cases from post-change(σ, σ′ ) :

   Case 1: hp′ (x, k) = nil ∧ tbm′ = nil: From the assumption of all-ok(s, σ), there
were no marked nodes in s with unmarked children. Therefore, removing a link will
not change this and so, all-ok(s, σ′ ) holds, which implies can-be-marked(s, σ′ ).

    Case 2: tbm′ = hp′ (x, k) ∧ hp′ (x, k) ∈ reach(roots, hp):
∃(c, j) ∈ dom(hp)·hp(c, j) = hp′ (x, k) (There had to be another node c pointing to the
new child of a), from hp′ (x, k) ∈ reach(roots, hp) in post-change(σ, σ′ ).

             / reach(roots, hp′ ) or c ∈ reach(roots, hp′ )
    Either c ∈
                / reach(roots, hp′ ):
    Case 2.1: c ∈
As only one link was changed, this must mean that c was only reachable via the
original hp(x, k), so the link is broken: c ∈ reach({hp(x, k)}, hp)

    Case 2.1.1: x ∈ s ∧ x ∈ marked:
Therefore, hp(x, k) ∈ marked, from all-ok(s, σ).
Let q be the address such that q ∈ (reach({hp(x, k}, σ) ∪ {hp(x, k)})) and
q ∈ marked ∧ ∃r ∈ dom(hp(q) · hp(q, r) ∈  / marked ∧ c ∈ (reach({r}, σ) ∪ {r})
(q is the first marked node with an unmarked child that is an ancestor of c).
Therefore, c satisfies the conditions of can-be-marked, to provide an alternative path
to hp′ (x, k).
From all-ok(s, σ), there is no node y ∈ (marked ∩ s) such that ∃j ∈ hp(y) · hp(y, j) ∈
                                                                                     /
marked. Since marked′ ≥ marked, ∀z ∈ (marked′ ∩ s)·∀h ∈ hp′ (z)·hp′ (z, h) ∈ marked.
Therefore, can-be-marked(s, σ) holds.

   Case 2.1.2: x ∈/s∨x∈  / marked:
From all-ok(s, σ) and the fact that the only change was hp(x, k) redirecting to hp′ (x, k),
can-be-marked holds vacuously.

   Case 2.2: c ∈ reach(roots, hp′ ):
Since roots ⊆ marked in all states, this gives that c ∈ reach(marked, hp′ ).

     Either c ∈ reach(s, hp′ ) or c ∈
                                    / reach(s, hp′ ).

     Case 2.2.1: c ∈ reach(s, hp′ ):
The Complexity of Interference                                                         15

   Case 2.2.1.1: c ∈ (s ∪ marked):
Then, from all-ok(s, σ), hp(x, k) ∈ marked.
From all-ok(s, σ) and the fact that the only change was hp(x, k) redirecting to hp′ (x, k),
can-be-marked holds vacuously.

    Case 2.2.1.2: (c ∈/ s) ∨ (c ∈
                                / marked):
Therefore, c satisfies the conditions of can-be-marked, to provide an alternative path
to hp′ (x, k).

    Showing that tbm-put holds is straight-forward using all-ok(s, σ) and post-Change(σ, σ′ ),
as post-Change sets tbm to the new destination node, and from all-ok(s, σ), there are
no other nodes in s and marked with unmarked children.
