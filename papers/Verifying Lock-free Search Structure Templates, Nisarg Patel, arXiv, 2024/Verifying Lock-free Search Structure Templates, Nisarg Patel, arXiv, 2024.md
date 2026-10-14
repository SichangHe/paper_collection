                                         Verifying Lock-free Search Structure Templates
                                         Nisarg Patel
                                         New York University

                                         Dennis Shasha
                                         New York University

                                         Thomas Wies
                                         New York University

                                               Abstract
                                         We present and verify template algorithms for lock-free concurrent search structures that cover a
                                         broad range of existing implementations based on lists and skiplists. Our linearizability proofs are
                                         fully mechanized in the concurrent separation logic Iris. The proofs are modular and cover the
                                         broader design space of the underlying algorithms by parameterizing the verification over aspects
arXiv:2405.13271v1 [cs.PL] 22 May 2024




                                         such as the low-level representation of nodes and the style of data structure maintenance. As a
                                         further technical contribution, we present a mechanization of a recently proposed method for reas-
                                         oning about future-dependent linearization points using hindsight arguments. The mechanization
                                         builds on Iris’ support for prophecy reasoning and user-defined ghost resources. We demonstrate
                                         that the method can help to reduce the proof effort compared to direct prophecy-based proofs.

                                         2012 ACM Subject Classification Theory of computation → Logic and verification; Theory of
                                         computation → Separation logic; Theory of computation → Shared memory algorithms

                                         Keywords and phrases skiplists, lock-free, separation logic, linearizability, future-dependent linear-
                                         ization points, hindsight reasoning


                                          1     Introduction

                                         A search structure is a key-based store that implements a mutable map of keys to values
                                         (or a mutable set of keys). It provides five basic operations: (i) create an empty structure,
                                         (ii) insert a key-value pair, (iii) search for a key and return its value, (iv) delete the entry
                                         associated with a key, and (v) update the value associated with a particular key. Because
                                         of their general usefulness, search structures are ubiquitous in data-intensive workloads.
                                              Earlier works [19, 20, 35] developed a framework to verify a wide range of lock-based
                                         implementations of concurrent search structures. Specifically, they proved that these imple-
                                         mentations are linearizable [12].
                                              A core ingredient of the framework is the idea of template algorithms [37]. A template
                                         algorithm dictates how threads interact but abstracts away from the concrete layout of
                                         nodes in memory. Once the template algorithm is verified, its proof can be instantiated on
                                         a variety of search structures.
                                              The template algorithms of [19, 20, 35] use locks as a synchronization technique. Locks
                                         ensure non-interference on portions of memory to guarantee that certain needed constraints
                                         hold in spite of concurrency.
                                              The disadvantage of locks is that if a thread holding a lock on some portion of memory p
                                         stops, then no other thread can get a conflicting lock on p. For that reason, some practical
                                         implementations such as Java’s ConcurrentSkipListMap [34] use lock-free algorithms.
                                              This paper shows how to capture multiple variants of concurrent lock-free skiplists and
                                         linked lists in the form of template algorithms. Thus, proving the correctness of such a
                                         template algorithm results in a proof that is applicable to many variants at once. Our
                                         template algorithms are parametric in the skiplist height and allow variations along the
2   Verifying Lock-free Search Structure Templates



                 L3
                 L2
                 L1
                 L0
                      -∞      4       13       22      30      34       40      45       ∞
                      hd      n1      n2       n3      n4      n5       n6      n7       tl

       Figure 1 Skiplist with four levels. A node that is marked (logically deleted) at a level is shaded
    gray at that level. The red line indicates the path taken by a traversal searching for key 42.


    following three dimensions: (i) maintenance style (eager vs lazy) (ii) node implementations
    and (iii) the order of maintenance operations on the higher levels of the skiplists.
        By instantiating our template algorithm with appropriate maintenance operations and
    node implementations we obtain verified versions of existing (skip)list algorithms from the
    literature such as the Herlihy-Shavit skiplist algorithm [11, § 14], the Michael set [32], and
    the Harris list algorithm [10]. We also obtain new concurrent skiplist algorithms that have
    not been considered before. These new algorithms are correct by construction thanks to our
    modular verification framework.
        We mechanize our development in the concurrent separation logic Iris [15, 17]. One
    technical contribution of our work is a formalization of hindsight reasoning [7, 8, 23, 27, 28,
    33] in Iris. Hindsight reasoning has shown its usefulness in dealing with future-dependent and
    external linearization points, a challenge that commonly arises in lock-free data structures.
        Specifically, we build on the hindsight theory developed in [28], providing a mechanism
    in Iris where one can establish that a linearization point has passed by inferring knowledge
    about past states using a form of temporal interpolation.
        To our knowledge, our development is the first formalization of hindsight theory in a
    foundational program logic. The usefulness of the developed theory extends beyond our
    lock-free template algorithms. In fact, we demonstrate that it can help to reduce the proof
    effort compared to alternative proof techniques in Iris. To this end, we reverify the multicopy
    template algorithms of [35] using our formalization of hindsight as opposed to our previous
    tailor-made proof argument for dealing with future-dependent linearization points. The new
    approach reduces the proof effort by 53%.
        To summarize, our contributions are (i) template algorithms for a wide variety of lock-
    free search structure algorithms, (ii) mechanized proofs of linearizability based on hindsight
    reasoning in Iris. The result is, to our knowledge, the first formal verification of fully-
    functional lock-free algorithms for skiplists of unbounded height.


     2     The Skiplist Template Algorithm
    A skiplist is a search structure over a totally ordered set of keys K. We focus our discussion
    on skiplists that implement mutable sets rather than maps. The extension of the presented
    algorithms to mutable maps is straightforward. The data structure is composed of sorted
    lists at multiple levels, with the base list determining the actual contents of the structure,
    while higher level lists are used to speed up the search. An example is shown in Figure 1.
    A skiplist node contains a key and has a height, determining how many higher level lists
    this node is a part of. Each node has a next pointer for each of its levels. Two sentinel
    nodes signify the head (hd with key −∞) and the tail (tl with key ∞) of the skiplist. Lock-
    free linked lists often use the technique of logical deletion by marking a node before it is
    physically unlinked from the list. This involves storing a mark bit together with the next
N. Patel, D. Shasha, and T. Wies                                                                   3


pointer, so as to allow reading and updating them together in a single (logically) atomic
step. Lock-free skiplist implementations also use this technique. Since a skiplist node can
be part of multiple lists, it has one mark bit per level.
    The traversal for a key not only goes left to right as usual, but also top to bottom. The
red line in Figure 1 depicts a traversal searching for key 42. The traversal begins at the
highest level of the head node. At each non-base level, the traversal continues till it reaches
a node with a key greater than or equal to the search key. Thereafter, the traversal drops
down a level, and continues at the lower levels until it terminates on the bottom level at the
first node whose key is greater than or equal to the search key.
    The traversals in a concurrent skiplist perform maintenance in the form of physically
unlinking encountered marked nodes. In Figure 1, node n5 has been unlinked at level 2,
thus the traversal does not visit it at that level. Operations that mark and change the next
pointers at the higher levels do not affect the actual contents of the structure. We therefore
consider them to be part of the maintenance.
    Many variants of lock-free skiplist algorithms have been proposed in the literature and
implemented in practice. These variants differ in (i) their node implementations, (ii) the
styles of maintenance operations and/or (iii) the orders in which they perform maintenance
operations with regard to other operations.
    For example, node implementations in low-level languages often use bit-stealing [11] (or
an equivalent of Java’s AtomicMarkableReference) so that both the next pointer and mark
bit can be atomically read or updated. Other implementations use more complex solutions.
For instance, the skiplists in [9] use nodes with back links to reduce traversal restarts due to
marked nodes. Java’s ConcurrentSkipListMap [34] implements each node as a list of simpler
nodes, one per level. The higher level nodes have both right pointers and down pointers,
while the base nodes only have right pointers. Java’s implementation also uses marker nodes
for marking, instead of bit-stealing.
    In terms of style of maintenance, the traversal in the Michael Set [32] and Herlihy-Shavit
lock-free skiplist [11, § 14] unlinks one marked node at a time. By contrast, the traversal in
the Harris List [10] unlinks the entire sequence of marked nodes in one shot with a single
CAS operation. The variants also differ in the order of marking of a node at higher levels.
In the Herlihy-Shavit skiplist, the marking of a node goes from top level to the bottom level.
This differs from skiplists in [34] and [9], whose marking goes from bottom to top.
    Despite the differences in the skiplist algorithms described above (and others to be in-
vented in the future), the bulk of their correctness reasoning remains the same. A goal of
this paper is to show how to exploit that fact.

Template algorithm. Our template algorithm for skiplists abstracts away from node-
level implementation details and the way in which traversals perform maintenance. As we
shall see, the particular details regarding how the data is stored internal to the node does
not affect the correctness of the core operations - search, insert and delete. Nor is the
correctness affected by whether the traversal unlinks one marked node at a time or an entire
sequence of marked nodes. We also show that the order in which maintenance operations
are performed on the higher levels of the list does not matter for correctness. In summary,
the template algorithm we present abstracts from: (i) node-level details; (ii) the style of
unlinking marked nodes and (iii) the order of maintenance operations on higher levels.
     The template algorithm is assumed to be operating on a set of nodes N that contains
the two sentinel nodes head hd and tail tl. Let the maximum allowed height of a skiplist
node be L (> 1). Each node n is associated with (i) its key key(n) ∈ K = N ∪ {−∞, ∞},
(ii) its height height(n) ∈ [1, L) , (iii) the next pointers next(n, i) ∈ N for each i from 0 to
4   Verifying Lock-free Search Structure Templates


     1 let search k =                                 18 let insert k =
     2   let ps = allocArr L hd in                    19   let ps = allocArr L hd in
     3   let cs = allocArr L tl in                    20   let cs = allocArr L tl in
     4   let _, _, res = traverse ps cs k in          21   let p, c, res = traverse ps cs k in
     5   res                                          22   if res then
     6                                                23     false
     7 let delete k =                                 24   else
     8   let ps = allocArr L hd in                    25     let h = randomNum L in
     9   let cs = allocArr L tl in                    26     let e = createNode k h cs in
    10   let p, c, res = traverse ps cs k in          27     match changeNext 0 p c e with
    11   if not res then                              28     | Success ->
    12     false                                      29       maintainanceOp_ins k ps cs e; true
    13   else                                         30     | Failure -> insert k
    14     maintainanceOp_del c;
    15     match markNode 0 c with
    16     | Success -> traverse ps cs k; true
    17     | Failure -> false

        Figure 2 The template algorithm for lock-free skiplists. The template can be instantiated
    by providing implementations of traverse and the helper functions markNode, createNode and
    changeNext. The markNode i c attempts to mark node c at level i atomically, and fails if c has
    been marked already. createNode k h cs creates a new node e of height h containing k, and whose
    next pointers are set to nodes in array cs. Finally, changeNext i p c cn is a CAS operation attempting
    to change the next pointer of p from c to cn. changeNext i p c cn succeeds only if mark(p, i) = false
    and next(p, i) = c. Other functions used here include randomNum to generate a random number and
    maintenance operations associated with insert and delete. maintainanceOp_del marks node c at
    the higher levels, while maintainanceOp_ins inserts a new node e at the higher levels.


    height(n) − 1, and (iv) its mark bits per level mark(n, i) ∈ {true, false} for each i from 0
    to height(n) − 1. When discussing next(n, i) or mark(n, i), we implicitly assume that i lies
    between 0 and height(n) − 1. We sometimes say a node n is unmarked to mean that it is
    unmarked at the base level, i.e., mark(n, 0) = false. The structural invariant maintains the
    following facts: key(hd) = −∞, key(tl) = ∞, height(hd) = height(tl) = L, next(tl, i) = tl for
    all i, next(hd, L − 1) = tl, mark(hd, i) = mark(tl, i) = false for all i.
        The core operations of the skiplist template are expressed using helper functions such as
    findNext and markNode that abstract from the details of the node implementation. We describe
    the behavior of these helper functions as and when we encounter them. The template is
    instantiated by implementing these functions. The helper functions are assumed to be
    logically atomic, i.e., appear to take effect in a single step during its execution.
        Figure 2 shows the core operations of the skiplist template algorithm. (We omit the code
    for the data structure initialization as it is straightforward.) All three operations begin by
    allocating two arrays ps and cs via allocArr, each of size L and values initialized to hd and tl
    respectively. These arrays are then populated by the traverse operation as it computes the
    predecessor-successor pair for operation key k at each level. Intuitively, these pairs indicate
    where k would be inserted at each level. The template algorithm here abstracts away from
    the concrete traverse implementation. We later consider two implementations of traverse
    that differ in the way that maintenance is performed, as discussed earlier.
        As far as the core operations are concerned, they rely on traverse to satisfy the following
    specification. First, it returns a triple (p, c, res) where p and c are nodes and res a Boolean
    such that p = ps[0], c = cs[0] and res is true iff k is contained in c. Second, the node c must
    have been unmarked at some point during the traversal; and third, for each 0 ⩽ i < L, the
    traversal observes that key(ps[i]) < k ⩽ key(cs[i]).
        Let us now describe the core operations, starting with the search operation. The search
    operation simply invokes the traverse function, whose result establishes whether k was in
N. Patel, D. Shasha, and T. Wies                                                                    5


the structure. The delete operation starts similarly by invoking traverse and checking
if the key is present in the structure. If it is, then delete invokes the maintenance oper-
ation maintainanceOp_del, which attempts to mark c at the higher levels (i.e. all levels
except 0). We provide the implementation of maintainanceOp_del in a moment. Once
maintainanceOp_del terminates, delete finally attempts to mark c via markNode at the
base level. If marking succeeds, it terminates by invoking traverse (which performs the
task of physically unlinking marked nodes at all levels) and returning true. Otherwise, a
concurrent thread must have already marked c, in which case delete returns false.
    The insert operation also begins with traverse. If the traversal returns true, then the
key must already have been present. Hence, insert returns false in this case. Otherwise, a
new node e is created using createNode. The node’s height is determined randomly using
randomNum, which generates a random number h such that 0 < h < L. After creating a new
node, the algorithm attempts to insert it into the list by calling changeNext at the base level
(line 27). If the attempt succeeds, insert proceeds by invoking the maintenance operation
maintainanceOp_ins, which also inserts the new node into the list at all higher levels. The
insert then returns with true. If the changeNext operation fails, then the entire operation
is restarted.
    We now describe the maintenance operations for insert and delete, shown in Figure 3.
The maintenance operations here differ from those in traditional skiplist implementations
in regards to the order in which maintenance is performed at higher levels. In traditional
implementations, the marking of a node goes from top to bottom, while insertion of a new
node goes from bottom to top. The skiplist template presented here makes sure that the
base level gets marked at the end and the insertion first happens at the base level, but it
imposes no order on how it proceeds at higher levels. That is, when marking a node, a
delete thread could for instance first mark odd levels, then even levels and finally the base
level 0. The maintenance operations in the skiplist template captures all such permutations.
As our proof shows later, the order of maintenance at higher levels has no bearing on the
correctness of the algorithm.

1 let maintainanceOp_del_rec i h pm c =        12 let maintainanceOp_ins_rec i h pm ps cs e =
2   if i < h-1 then                            13   if i < h-1 then
3     let idx = pm[i] in                       14     let idx = pm[i] in
4     markNode idx c;                          15     let p = ps[idx] in
5     maintainanceOp_del_rec (i+1) h pm c      16     let c = cs[idx] in
6   else ()                                    17     match changeNext idx p c e with
7                                              18     | Success ->
8  let maintainanceOp_del c =                  19       maintainanceOp_ins_rec (i+1) h pm ps cs e
9    let h = getHeight c in                    20     | Failure ->
10   let pm = permute h in                     21       traverse ps cs k;
11   maintainanceOp_del 0 h pm c               22       maintainanceOp_ins_rec i h pm ps cs e
                                               23   else ()
                                               24
                                               25 let maintainanceOp_ins k ps cs e =
                                               26   let h = getHeight e in
                                               27   let pm = permute h in
                                               28   maintainanceOp_ins 0 h pm ps cs e

    Figure 3 The maintenance operations for the skiplist. The getHeight c helper function returns
height(c). The permute function generates a permutation of [1 . . . (h − 1)] as an array.

   The maintainanceOp_del marks node c from levels 1 to height(c). It begins by reading
the height of c as h, and generating a permutation of [1 . . . (h − 1)] stored in array pm via
the permute function. The maintainanceOp_del_rec then recursively marks c in the order
prescribed by pm. Note that the maintenance continues regardless of whether markNode
6   Verifying Lock-free Search Structure Templates


    1  let eager_i i k p c =                                   14 let eager_rec i ps cs k =
    2    match findNext i c with                               15   let p = ps[i+1] in
     3   | cn, true ->                                         16   let c, _ = findNext i p in
     4     match changeNext i p c cn with                      17   let p′ , c ′ , res = eager_i i k p c in
     5     | Success -> eager_i i k p cn                       18   ps[i] <- p′ ;
     6     | Failure -> traverse ps cs k                       19   cs[i] <- c ′ ;
     7   | cn, false ->                                        20   if i = 0 then
     8     let kc = getKey c in
                                                               21     (p′ , c ′ , res)
     9     if kc < k then
                                                               22   else
    10       eager_i i k c cn
                                                               23   eager_rec (i-1) ps cs k
    11     else
                                                               24
    12       let res = (kc = k ? true : false) in
                                                               25   let traverse ps cs k =
    13       (p, c, res)
                                                               26     eager_rec (L - 2) ps cs k

        Figure 4 The eager traversal for the skiplist template. findNext i k c returns a pair
    (next(c, i), mark(c, i)). The getKey c helper function returns key(c).



    succeeds or fails, because c will be marked at the end regardless.
        The maintainanceOp_ins begins in the same way by reading the height, generating the
    permutation and invoking maintainanceOp_ins_rec. The maintainanceOp_ins_rec first
    collects the predecessor-successor pair at the current level from arrays ps and cs, respectively.
    Then it tries to insert the new node e using changeNext on predecessor node p. If changeNext
    succeeds, then the recursive operation continues. Otherwise, it recomputes the predecessor-
    successor pairs using traverse. After the recomputation, the insertion is retried at the same
    level.
        We can now finally turn to the implementations of traverse. We consider two imple-
    mentations that differ in their treatment of marked nodes. The eager traversal attempts
    to unlink every marked node it encounters, while the lazy traversal simply walks over the
    marked nodes till it reaches an unmarked node. The traversal then attempts to unlink the
    entire marked segment at once. The two implementations are similar in other aspects, so
    we discuss only the eager traversal in detail here. The details about the lazy traversal can
    be found in Appendix A.2.
        The eager traversal is shown in Figure 4. The traverse function is implemented using
    mutually-recursive functions eager_rec and eager_i1 . The function eager_rec populates
    the arrays ps and cs with the predecessor-successor pair at level i computed by eager_i.
    The eager_i performs a traversal at level i by first reading the mark bit and next pointer
    of c using findNext. If c is found to be marked, then eager_i attempts to physically unlink
    the node using changeNext. In the case that changeNext fails (because either p is marked
    or it does not point to c anymore), eager_i simply restarts the traverse function. In the
    case of Success of changeNext, the traversal continues. If c is unmarked, then traverse_i
    proceeds by comparing k to key(c). For key(c) < k, the traversal continues with c and cn.
    Otherwise, eager_i ends at c, returning (p, c, true) if key(c) = k and (p, c, false) otherwise.
    As mentioned before, eager_i attempts to unlink immediately whenever a marked node is
    encountered.



    1
        For ease of exposition, the implementation of the eager traversal shown in Figure 4 differs slightly
        from the version we have verified in Iris. The Iris version uses option return types instead of mutually-
        recursive functions in order to obtain a more modular proof of the eager traversal. We use the mutually
        recursive implementation here for clarity of exposition.
N. Patel, D. Shasha, and T. Wies                                                                        7


 3       Proof Intuition
Our goal is to show that the skiplist template is linearizable. That is, we must prove that
each of the core operations take effect in a single atomic step during its execution, the
linearization point, and satisfies the sequential specification shown in Figure 5. For the
skiplist template, we define the abstract state C(N ) to be the union of the logical contents
C(n) of all nodes in N , where C(n) := (mark(n, 0) ? ∅ : {key(n)}). In other words, the
abstract state of the structure is a collection of keys contained in unmarked nodes at the
base level. There are existing techniques from the literature that help us analyze the skiplist

                                
                                  ′
                                C = C ∧ (res ⇐⇒ k ∈ C)            op = search
                                
                                
     Ψop (k, C, C ′ , res) :=      ′
                                  C = C ∪ {k} ∧ (res ⇐⇒ k ̸∈ C)    op = insert
                                
                                C ′ = C \ {k} ∧ (res ⇐⇒ k ∈ C)
                                
                                                                   op = delete


    Figure 5 Sequential specification of a search structure. k refers to the operation key, C and C ′
to the abstract state before and after operation op, respectively, and res is the return value of op.


template. The two main techniques that we rely on are the Edgeset Framework [37] and
Hindsight Reasoning [7, 8, 23, 27, 28, 33]. We begin by giving a brief overview of the two
techniques, proceeded by the analysis of the skiplist template using these techniques.


3.1      The Edgeset Framework
The Edgeset Framework provides a common terminology to capture how search operations
navigate in a variety of search structures. We view each search structure as a mathemat-
ical graph whose edges are associated with an edgeset, a label that is a set of keys. We
denote the edgeset from n to n′ by es(n, n′ ), and k ∈ es(n, n′ ) signifies that a search for
key k will proceed from node n to n′ . In the context of the skiplist template, we define
the edgeset leaving n to be all values greater than the key in n if n is unmarked. If node
n is marked, then the edgeset leaving n is the entire keyspace. Formally: es(n, n′ ) :=
(n′ = next(n, 0) ∧ mark(n, 0) = false ? (key(n), ∞) : K). Note that, our definition of edge-
sets in the skiplist template depends only on the base list, and not on higher level mark bits
and next pointers.
    A notion defined in terms of edgesets is the inset of a node, denoted by inset(n), signifying
a set of keys for which a search will arrive at n. In order to understand the concept of inset
intuitively, consider Figure 6. The inset of node n4 is (2, ∞), because, for all keys greater
than 2, the search will enter n4 . We say node n1 is the logical predecessor of n4 if it is
the first unmarked predecessor of n4 . The inset of the root is K and the inset of n is the
intersection of K with the edgesets of all nodes between the root and n. For sorted linked
lists in general, a more local notion gives the same result: the inset of an unmarked node n
is (key(n′ ), ∞), where n′ is the logical predecessor of n.
    In contrast to inset, we define the outset as the union of all its outgoing edgesets:
outset(n) := n′ ∈N es(n, n′ ).
               S

    We can now define the keyset of a node n as keyset(n) := inset(n) \ outset(n), i.e. in-
tuitively, the set of keys for which a search enters n but never leaves. The importance of
keysets is that if k is in keyset(n), then k is either in the contents of n or is nowhere in the
structure. In Figure 6, the keyset of n4 is (2, 9] and in general, the keyset of an unmarked
8   Verifying Lock-free Search Structure Templates




                           n
                           hld54321
                           t15
                           0
                           2
                           4
                           7∞
                            9




        Figure 6 Possible state of the base list in the skiplist template. Nodes are labeled with the value
    of their key field. Edges indicate next pointers. Marked (logically deleted) nodes are shaded gray.
    keyset(hd) = {0}, keyset(n1 ) = (0, 2], keyset(n4 ) = (2, 9] and keyset(tl) = (9, ∞). The keyset of a
    marked node is always ∅.


    node n is (keyset(n′ ), key(n)] where n′ is its logical predecessor. The keyset of a marked
    node is ∅ because its outset is the set of all keys K.
        The technical definition of inset relies on the global data structure graph, defined as a
    solution to the following fixpoint equation
                                                       [
                         ∀n ∈ N. inset(n) = in(n) ∪        es(n′ , n) ∩ inset(n′ )
                                                         n′ ∈N

    where in(n) := (n = hd ? K : ∅). Thus, the inset is a global quantity and hence difficult to
    reason about. Fortunately, this is where the Flow Framework [21, 22, 29] comes in handy.
    It allows us to reason about quantities that can be expressed as a solution to a fixpoint
    equation (like inset) in a local manner by attaching flow values to the node. The framework
    then provides tools to track changes to the flow values that are induced by changes to the
    underlying graph. Our approach to encoding keysets in Iris using the Flow Framework is
    borrowed from [19]. We defer further details on this matter to the later sections.
        As mentioned above, keyset(n) intuitively is the set of all keys that n is responsible for.
    Consider Figure 6 again, a thread executing search(6) without any interference will reach
    node n4 and terminate, concluding that 6 is not present in the structure. In this sense, we
    say n4 is responsible for key 6 and therefore 6 is part of n4 ’s keyset. The keysets of all nodes
    partition the set of all keys and provide the crucial Keyset Property:

       ∀ n ∈ N, k ∈ K. k ∈ keyset(n) ⇒ (k ∈ C(N ) ⇔ k ∈ C(n))                                  (KeysetPr)

        This property enables one to lift a proof of the specification at the node level to a
    proof of the sequential specification Ψop . A particular situation where (KeysetPr) proves
    indispensable is when search fails to find the search key. Note that search observes only
    the nodes it visited, and hence has only a partial view of the structure. When search fails
    to find the key, the proof has to reconcile this partial view of the structure with the global
    view. In essence, if a concurrent invocation of search on key k fails to find the key, can we
    conclude that there was a point in time during its execution when k was in fact not present
    in the structure? Here, the property (KeysetPr) helps us reconcile facts gathered by search
    with the global state of the structure. Specifically, if search can determine a node n such
    that k ∈ keyset(n) and k ∈ / C(n), then we can immediately infer that k was not present in
    the structure at that point in time.

    3.2    Hindsight Reasoning
    Lock-free structures often exhibit future-dependent linearization points. That is, the linear-
    ization point of an operation cannot be determined at any fixed moment, but only at the end
N. Patel, D. Shasha, and T. Wies                                                                         9




         ⇝
         delete(7)
       n
       (p
       4
       9
       7cd)
         b)
         c)
         a)
          1
          2
          3
          4
        ⇝

         insert(7)




   Figure 7 Possible states of search(7) on the base level in presence of interference from concurrent
delete(7) and insert(7).


of the execution, once any interference of other concurrent operations has been accounted for.
To understand the interference issue, consider the search operation. Since, search returns
the result of traverse, let us look at the eager traversal implementation. To simplify the
explanation further, let us assume that the maximum height allowed for every non-sentinel
node is one. Then, we can ignore the eager_rec function and focus on eager_i called at the
base level.
    Let there be a thread T executing search(7). Concurrently, there is a thread Td execut-
ing delete(7) and a thread Ti executing insert(7). Figure 7 shows interesting scenarios
that thread T might potentially observe. Box (a) captures the state of the structure at the
beginning of the eager_i call processing n2 . Let Scenario 1 be the situation when thread
T faces no interference from Td and Ti . Here, thread T finds the key 7 in n2 and eager_i
returns true. The point when eager_i finds n2 to be unmarked becomes the linearization
point for this scenario.
    Now consider Scenario 2 to be the situation where thread Td marks n2 before eager_i
processes it, as shown in Box (b). Thread T will attempt to unlink n2 , and assuming no
further interference, the unlink will result in the structure in Box (c). Thread T will process
n3 next, finding n3 to be unmarked with key greater than 7, and will terminate with result
false. So when is the linearization point in this scenario? It cannot be when T finds n3
unmarked when processing it. Because there could be further interference from thread Ti
which inserts key 7 in a new node as shown in Box (d). The new node could be added right
before T reads the mark bit of n3 . Thus, when eager_i finds n3 unmarked and returns false,
key 7 could actually be present in the structure at that point in time.
    The linearization point is actually the point in time shown in Box (c), i.e., right after n2
is unlinked. However, thread T cannot confirm this when n2 is unlinked because eager_i
may not terminate at n3 with false as the result. The reason is that by the time T processes
n3 , it could get marked in a manner similar to n2 in Box (b), resulting in the unlinking
of n3 and potentially a restart. That Box (c) is the linearization point is confirmed when
T has found n3 to be unmarked later. The structure maintains the invariant that once a
node is marked, it remains marked. Using this invariant, an analysis of thread T ’s history
10   Verifying Lock-free Search Structure Templates


     concludes that n3 must have been unmarked at the point when n2 was unlinked. Once
     eager_i terminates at n3 with false, an analysis can establish in hindsight that Box (c)
     indeed was the linearization point.
         Hindsight reasoning as formalized in [27, 28] is designed to deal with situations like the
     search in Figure 7. It enables temporal reasoning about computations using a past predicate
     ⟐q, which expresses that proposition q held true at some prior state in the computation
     (up to the current state). For instance, ⟐(next(n1 , 0) = n2 ) holds in Box (c) even though
     next(n1 , 0) = n3 at that point. The reason is that next(n1 , 0) = n2 was true at an earlier
     point in time, namely in Box (b). Note that the past operator ⟐ abstracts away the exact
     time point when the predicate held true. Note also that a past predicate is not affected by
     concurrent interferences, as it merely records some fact about a past state.
         There are two ways to establish a past predicate that are relevant for our proofs. The
     first is to establish the predicate in the current state directly. That is, ⟐q holds if q holds
     in the current state. As an example, we obtain (next(n1 , 0) = n2 ) when findNext on n1
     returned n2 in Box (a). Thus, for all subsequent states including Box (b) and (c), we get
     ⟐(next(n1 , 0) = n2 ). The second way to establish a past predicate is through the use of
     temporal interpolation [28]. That is, one proves a lemma of the form: if there existed a past
     state that satisfied property q and the current state satisfies r, then there must have existed
     an intermediate state that satisfied o. Such lemmas can then be applied, e.g., to prove that
     if thread T finds n3 to be unmarked in Scenario 2, then it must have been unmarked when
     n2 was unlinked in Box (c).
         Equipped with the Edgeset Framework and hindsight reasoning, we are now ready to
     analyze the core operations of the skiplist template.


     3.3    Proof Outline for Core Operations
     We refer to a linearization point as modifying if the operation changes the abstract state of
     the data structure (like in the case of a succeeding delete and insert) and otherwise refer to
     it as unmodifying (like search and in the case of a failing delete or insert). The modifying
     linearization points of the skiplist template are easier to reason about because they are not
     future-dependent. For delete, the linearization point occurs when markNode succeeds, and
     similarly, for insert the linearization point occurs when the call to changeNext on line 27
     succeeds. The proof strategy for unmodifying linearization points is to combine (KeysetPr)
     with the ⟐ operator from hindsight reasoning. Let us expand on this proof strategy in detail
     and show why the skiplist template is linearizable.
         We begin by describing the specification for traverse that is assumed for analyzing the
     core operations of the template. Then, we analyze each of the operations in detail. Finally,
     we show how the eager implementations of traverse satisfies the specification that was
     assumed in the beginning. Along the way, we introduce (as and when necessary) invariants
     maintained by the skiplist template that are crucial for proving linearizability.
         Specification of traverse. The function traverse ps cs k updates arrays ps and cs
     with predecessor-successor pairs for each level and returns a triple (p, c, res) that satisfies the
     following past predicate regarding node c: ⟐(k ∈ keyset(c) ∧ (res ⇐⇒ k ∈ C(c))). Recall
     that our definition of edgesets in Section 3.1 implies the following invariant:

        Invariant 1 For all nodes n, if mark(n, 0) is set to true then keyset(n) = ∅.

     Using Invariant 1, we can establish that c is unmarked at the base level at the time point
     when k ∈ keyset(c) holds. Note that traverse may physically unlink marked nodes. How-
N. Patel, D. Shasha, and T. Wies                                                                   11


ever, this step does not change the abstract state of the structure. Hence, the specification
for traverse involves no change of the abstract state.
    We now consider each of the core operations in detail.
    Proof of search. Function search returns res out of the triple (p, c, res) returned
by traverse. The specification of traverse says res ⇐⇒ k ∈ C(c) at some point, say
t, during its execution. The specification additionally guarantees k ∈ keyset(c) at time t.
These two facts, combined with the (KeysetPr) at time point t, allow us to immediately
infer that res is true iff k was in the structure at that point. Hence, we can establish that
(res ⇐⇒ k ∈ C(c)) was true at some point during the execution of search.
    Proof of delete. We analyze delete by case analysis on the value res returned by
traverse. If res is false, then again we can establish that k was not in the structure at
some point during traverse’s execution by the same reasoning used in the proof of search.
So let us consider the case that res is true. By the specification of traverse, we can
establish a time point when c was unmarked and contained k. The delete operation then
calls maintainanceOp_del which marks c at all the higher levels. Finally, the markNode
on Line 15 attempts to mark c at the base level. If markNode succeeds, then this step
becomes the linearization point of delete and k can be considered to be deleted from
the structure. But if markNode fails, then we gain the knowledge that mark(c, 0) = true.
Hindsight reasoning allows us to infer that c was marked at the base level by a concurrent
thread between the end of traverse and the invocation of markNode. The point right after
c was marked by a concurrent thread becomes the linearization point of delete in this case,
as we can determine that k was not present in the structure at that point.
    This hindsight reasoning relies on two facts: first, the key of a node never changes and
second, once a mark bit is set to true by a successful markNode operation (at line 15 in
delete or line 4 in maintainanceOp_del), no other operation will set it back to false. In
fact, these two facts are invariant for the skiplist template:

   Invariant 2 For all nodes n and level i, once mark(n, i) is set to true, it remains true.
   Invariant 3 For all nodes n, key(n) remains constant.

    Proof of insert. Similar to delete, we begin by case analysis on res returned by
traverse. If res is true, then we can establish that k was already present in the structure
at some point. Otherwise, res is false and insert creates a new node e with key k. Using
changeNext, an attempt is made to insert node e between nodes p and c. If the attempt
succeeds, then k is now part of the structure and this becomes the linearization point. The
following maintainanceOp_ins operation does not change the abstract state of the structure,
and thus, has no effect in terms of linearizability. If the changeNext fails, then insert simply
restarts.
    As is evident with the proof outline for the core operations, the specification assumed
for traverse plays a critical role in case the operation exhibits an unmodifying linearization
point. Let us now turn to traverse and show how its specification can be proved. We
analyze the eager traversal in detail in the following section. The proof argument for the
lazy version is similar.


3.4    Proof Outline for Eager Traversal
As stated earlier, traverse returns (p, c, res) such that ⟐(k ∈ keyset(c) ∧ (res ⇐⇒ k ∈ C(c))).
Since the returned triple is the result of a call to eager_i at the base level, let us begin by
analyzing the behavior of this call.
12   Verifying Lock-free Search Structure Templates


         In the sequential setting, the traversal in a search structure maintains the invariant that
     the search key is always in the inset of the current node. This invariant holds by the design
     of the Edgeset Framework. Unfortunately, this invariant no longer holds for the skiplist
     template in the concurrent setting as evidenced by Box (c) in Figure 7. However, we argue
     first that eager_i does maintain the invariant that the search key was in the inset of the
     current node c between the start of the traversal and the point at which the eager_i accesses
     c. We call this the inset in hindsight invariant.
         We prove this invariant inductively. We make use of the following locally maintained
     invariants: (i) At all times, there is one list, denoted the reachable list, from the head node
     that includes all unmarked and some marked nodes. (This list is characterized by the set of
     nodes with non-empty inset, see Figure 6 for intuition). (ii) The keys in the reachable list
     are sorted. A consequence of these two invariants is that if a node n is in the reachable list
     (whether n is marked or not) and has a key less than k, then k is in the inset of n.
         To prove that inset in hindsight is an invariant, we have to show that (a) it is an invariant
     when eager_i takes a step (Line 2) when traversing the base level, and (b) that we can
     establish inset in hindsight when eager_rec initiates eager_i (Line 17) at the base level.
         To show (a), observe that if a node n becomes unlinked from the reachable list, then it
     will never again be part of the reachable list. Hence, if n is not in the reachable list when
     eager_i begins executing at the base list, then eager_i will never visit n. The contrapositive
     of this statement allows us to say that if eager_i reaches some node c, then it must have
     been part of the reachable list at some point during the execution of eager_i. Additionally,
     eager_i proceeds to the node following c only when key(c) < k. With the help of invariants
     (i) and (ii) above, we can thus establish that k was in the inset of n at some point.
         To show (b), we must do a case analysis on whether node p (Line 16) is marked. If
     it is unmarked, then it is straightforward to establish that k is in the inset of c currently.
     However, if p is marked, then we require temporal interpolation based on the following
     invariant:
          Invariant 4 For all nodes n and level i, once mark(n, i) is set to true, next(n, i) does
          not change.
     This invariant tells us that if p was known to be unmarked in the past, and it is marked
     currently, then p must have been pointing to c right before it got marked. At that point in
     time, we can establish that k must have been in the inset of c.
         This completes the inductive proof that inset in hindsight is indeed an invariant main-
     tained by the traversal. The inset in hindsight invariant is sufficient to prove the traverse
     specification by the following simple argument. If the traverse encounters k in an unmarked
     node n, then traverse will return true as it should. If, by contrast, traverse encounters
     an unmarked node n such that key(n) > k, then by the inset in hindsight invariant, k must
     have been in the inset of n at some point t in the past and k cannot be in the outset of n
     (because key(n) > k and n is unmarked), so therefore k must have been in the keyset of n
     at time t.

      4      Hindsight Reasoning in Iris
     Linearizability in Iris is defined via (logically) atomic triples [5, 17]. Intuitively, an atomic
     triple x. P e v. Q says that at some point during the execution of e, the resources
     described by the precondition P will be updated to satisfy the postcondition Q for return
     value v in one atomic step. The variable x can be thought of as the abstract state of the
     data structure before the update at the linearization point.
N. Patel, D. Shasha, and T. Wies                                                                     13


    Linearizability of a search structure operation op can be expressed by an atomic triple
of the form

   Inv(r) −∗ C. CSS(r, C) op r k res. ∃ C ′ . CSS(r, C ′ ) ∗ Ψop (k, C, C ′ , res) . (ClientSpec)

Here, r is the pointer to the head of the data structure. The predicate CSS(r, C) is the
representation predicate that relates the head pointer with the contents C of the structure.
The predicate Inv(r) is the shared data structure invariant. It can be thought of as a thread-
local precondition of the atomic triple, which we express using separating implication. The
invariant ties CSS(r, C) to the data structure’s physical representation and may contain other
resources necessary for proving the atomic triple. The predicate Ψop (k, C, C ′ , res) captures
the sequential specification of the structure. The specification essentially says there is a
single atomic step in op where the abstract state changes from C to C ′ according to the
sequential specification Ψop (k, C, C ′ , res) (Figure 5). This step is op’s linearization point.
We call (ClientSpec) the client-level atomic specification for the data structure under proof.
Proving atomic triples. The proof of establishing an atomic triple involves a linearizab-
ility obligation that must be discharged directly at the linearization point. However, it can
be challenging to determine the linearization point precisely and to discharge the lineariz-
ability obligation exactly at that point. When the program execution reaches a potential
linearization point that depends on future interferences by other threads, then the proof will
fail if it is unable to determine whether the linearizability obligation should be discharged
now or later. In Iris, this challenge is overcome using prophecy variables [16], which enable
the proof to reason about the remainder of the computation that has not yet been executed.
     Another challenge is that the linearization point of an operation may be an atomic step
of another operation that is executed by a different thread (like in Scenario 2 discussed in
Section 3.2). Data structures that demonstrate such behavior are said to deploy helping.
This behavior complicates thread modular reasoning. The conventional solution to this
challenge in Iris is to use a helping protocol [14, 16, 35]. The helping protocol is specified
as part of the shared data structure invariant and consists of a registry that tracks which
threads are expected to be linearized by other threads as well as conditional logic that
governs the correct transfer and discharge of the associated linearizability obligations.
     Both the use of prophecy variables and the helping protocol need to be tailored to
the specific data structure at hand, which adds considerable overhead to the proof. To
reduce this overhead, we present an alternative proof method that enables linearizability
proofs based on hindsight arguments in Iris. Rather than identifying the linearization point
precisely, the proof can establish linearizability in hindsight using temporal interpolation in
the style of the intuitive proof argument for the skiplist template presented in Section 3.2.
Hindsight specification. Our proof method offers an intermediate specification, a Hoare
triple specification, which in essence expresses that linearizability has been established in
hindsight. In our Iris formalization, we show that any data structure whose operations satisfy
the hindsight specification also satisfy the client-level atomic specification. This proof relates
the two specifications via prophecy variables and a helping protocol. However, the helping
protocol is data structure agnostic, making our proof method applicable to a broad class of
structures exhibiting future-dependent unmodifying linearization points.
    From the perspective of a proof author using our method to prove linearizability of some
structure, one has to only establish the hindsight specification to obtain the proof of the
client-level atomic specification. To this end, our method provides further guidance to the
proof author.
14   Verifying Lock-free Search Structure Templates


         In order to use hindsight reasoning, one has to have the history of computation at hand.
     Here, we offer a shared state invariant with a mechanism to store the history. The shared
     state invariant has three main components: a mechanism to store the history, the helping
     protocol, and finally, an abstract predicate that can be instantiated with invariants specific
     to the structure at hand. The first two components are data structure agnostic. The proof
     author only needs to specify the data structure-specific invariant and what information about
     the data structure state should be tracked by the history.
         In the rest of this section, we discuss our method in detail. We begin with the hindsight
     specification, followed by a discussion of the shared state invariant and how to use it.


     4.1      Linearizability in Hindsight
     We motivate the hindsight specification using the challenges we face when proving the client-
     level atomic specification for the delete operation of the skiplist template. Let us recall the
     intuitive proof argument for delete from Section 3.3. As per the observation regarding the
     modifying and unmodifying linearization points, a delete thread with modifying lineariza-
     tion point can fulfill the obligation at the point when the structure is modified. However, a
     delete thread with an unmodifying linearization point requires helping.

     Prophecy reasoning. An important detail of our proof method is how it determines
     whether a thread requires helping. In the following, we refer to the operation that a thread
     performs at its linearization point as its decisive operation. In delete, the traversal observes
     node c to be unmarked at some point during execution. In the case where c is marked by the
     time that the thread calls its decisive operation markNode (in Line 15), the thread requires
     helping from the thread that marks c.
          In order to determine in advance whether a thread requires helping, our proof method
     attaches a prophecy to each thread. A prophecy in Iris can predict a sequence of values
     and is treated as a resource that can be owned by a thread. Ownership of a prophecy p
     is captured by the predicate Proph(p, pvs), where pvs is the list of predicted values. The
     predicate signifies the right to resolve p when the thread makes a physical step that produces
     some result value v. The resolution of p establishes equality between v and the head of the
     list pvs (i.e., the next value predicted by p). The resolution step yields the updated predicate
     Proph(p, pvs ′ ) where pvs ′ is the tail of pvs. This mechanism enables the proof to do a case
     analysis on the predicted values pvs before these values have been observed in the program
     execution2 .
          The prophecy attached to a thread predicts the results of the thread’s decisive operation.
     In case of delete, the decisive operation is the call to markNode in the base list, while for
     insert, it is the call to changeNext in the base list. Note that a thread may restart if its
     decisive operation fails (like in the case of insert). Therefore, the prophecy needs to predict
     a sequence of result values, one for each attempted call to the thread’s decisive operation.
          For the purpose of this discussion, we assume that the prophecy predicts a sequence
     of Success or Failure values. If the sequence contains a Success value, then the decisive
     operation will succeed and the thread will modify the structure. Otherwise, the thread’s
     linearization point is unmodifying. Let predicate Upd(pvs) hold when pvs contains at least
     one Success value.
          The proof author only needs to identify the decisive operations that potentially change


     2
         For further details on prophecies in Iris, we refer to [16].
N. Patel, D. Shasha, and T. Wies                                                                         15


the abstract state of the structure (like markNode as discussed above) by resolving the proph-
ecy around these decisive calls.
Hindsight specification. Before we can present the hindsight specification, we need to
                                                                 atomic triple  x. P e v. Q
provide necessary details regarding the atomic triples in Iris. An
is defined in terms of standard Hoare triples of the form ∀ Φ. AUx.P,Q (Φ) e v. Φ(v) . The
predicate AUx.P,Q (Φ) is the atomic update token and represents the linearizability obligation
of the atomic triple. At the beginning of each atomic step that the thread takes up to its
linearization point, the token offers the resources in P and the token itself transforms into a
choice. That is, at the end of the atomic step, the prover has to chose to either commit the
linearization or abort. When committing, the prover has to show that the thread’s atomic
step transforms the resources in P to those in Q, receiving Φ(v) from the update token in
return, which serves as the receipt of linearization of the atomic triple. In case of an abort,
the prover needs to show that the thread’s atomic step reestablishes P .
    We also need to introduce two more auxiliary predicates:

   Thread(tid, t0 ): this predicate is used to register the thread with identifier tid in the
   shared invariant. The argument t0 denotes the time when thread tid began its execution.
   PastLin(op, k, res, t0 ): this predicate holds if there was a past state in the history between
   time t0 and the point when this predicate is evaluated for which the sequential specifica-
   tion Ψop held with result res. It essentially captures whether the sequential specification
   was true for any point after time t0 .

   We now have all the ingredients to present the hindsight specification:

     ∀ tid t0 pvs. Inv(r) −∗ Thread(tid, t0 ) −∗
     
       Proph(p, pvs) ∗ (Upd(pvs) −∗ AUop (Φ)) op r k
                ′             ′                     ′ 
     res. ∃pvs . Proph(p, pvs ) ∗ pvs = (_ @ pvs )
                                                                                    (HindSpec)
                             ∗ (Upd(pvs) −∗ Φ(res))
                                                       
              ∗ (¬Upd(pvs) −∗ PastLin(op, k, res, t0 ))
                                                       

We explain it piece by piece. The local precondition Thread(tid, t0 ) ties the thread to its
identifier tid and provides knowledge that tid begins executing at time t0 . The Hoare
triple can be best understood by observing how prophecy resources are allowed to change
(highlighted in brown) and what are the obligations when Upd(pvs) holds (in teal) versus
when it does not hold (in magenta). Let us look at each of these in detail. First, the prophecy
resource Proph(p, pvs) in the precondition changes to Proph(p, pvs ′ ) in the postcondition
where pvs ′ is a suffix of pvs. It basically says that operation op is allowed to resolve the
prophecy p as many times as it needs and then return the remaining resource at the end.
    Now let us consider the case when Upd(pvs) holds. The precondition here provides the
atomic update token AUop (Φ) to op, expecting the receipt of linearization Φ(res) in return.
Thus, the responsibility of linearization is delegated to op when Upd(pvs) holds. We can gain
better insight by relating this situation to the delete operation from the skiplist template as
before. This case corresponds to when markNode (from line 15) succeeds as Upd(pvs) holds
here. The point when markNode succeeds becomes the linearization point and so the thread
does not require help from other threads to linearize. The hindsight specification simply
asks for the receipt from linearization Φ(res) at the end.
    Finally, let us consider the case when Upd(pvs) does not hold. The precondition provides
no additional resources here, while the postcondition requires the predicate PastLin(op, k, res, t0 ).
In simple terms, this means that if Upd(pvs) is not true, i.e., the prophecy says the thread is
16   Verifying Lock-free Search Structure Templates


     not going to modify the structure, then the hindsight specification allows exhibiting a past
     state from history when the sequential specification was true. Relating again to delete,
     if the markNode fails, then the thread can look at the history of the structure and exhibit
     precisely the point when the decisive node got marked.

         The proof argument for establishing the hindsight specification is significantly simpler
     than if one were to attempt a direct proof of the client-level atomic specification. In par-
     ticular, the proof author does not need to reason about helping and atomic update tokens
     in last case discussed above. Instead, they only need to reason about the structure-specific
     history invariant.



     Soundness of the hindsight specification. Our proof that relates the hindsight spe-
     cification for op to the atomic triple specification involves a helping protocol. The details of
     the helping protocol and the soundness proof for the hindsight specification are similar to
     those of the proofs presented in [16, 35]. We therefore provide only a brief summary here.
     Additional details regarding the proof and the helping protocol can be found in Appendix B.

         Before op begins executing, the proof creates the prophecy resource Proph(p, pvs) as-
     sumed in the precondition of the hindsight specification. If the prophecy determines that
     the thread requires helping, then its client-level atomic triple is registered to a predicate
     which encodes the helping protocol as part of the shared state invariant Inv(r). The re-
     gistered atomic triple serves as an obligation for the helping thread to commit the atomic
     triple. This obligation will be discharged by the appropriate concurrent operation determ-
     ined by the op’s sequential specification Ψop . The proof then uses the hindsight specification
     to conclude that it can collect the committed triple from the shared predicate. The commit-
     ted triple serves as a receipt that the obligation to linearize has been fulfilled.

        To govern the transfer of linearizability obligations and fulfillment receipts between
     threads via the shared invariant, the helping protocol tracks a registry of thread IDs with
     unmodifying linearization points that require helping from other concurrent threads. Each
     thread registered for helping is in either pending state or done state, depending on whether
     the thread has already been linearized. A thread registered for helping must be able to de-
     termine its current protocol state in order to be able to extract its committed atomic triple
     from the registry. For this purpose, the helping protocol includes a linearization condition
     that holds iff a registered thread tid has linearized (and is, hence, in done state).

         From the point of view of a thread which does the helping, the linearization condition
     forces its proof to scan over the pool of uncommitted triples registered in the helping protocol
     and identify those that need to be linearized at its linearization point, changing their protocol
     state from pending to done. This step involves a proof obligation for the helping thread to
     show that the sequential specification of tid’s operation is indeed satisfied at the linearization
     point.

        One crucial innovation in our helping protocol is that we have formulated a linearization
     condition that is parametric in the sequential specification of the data structure operations,
     making the soundness proof for the hindsight specification applicable to many structures
     at once. In particular, we deal with the aspect of scanning and updating the registry in
     the proof of the helping thread, the proof author simply invokes a lemma provided by our
     method at the identified linearization points. Therefore, the helping protocol mechanism
     remains fully opaque to the proof author.
N. Patel, D. Shasha, and T. Wies                                                                    17


4.2    Invariant for Hindsight Reasoning
Hindsight arguments involve reasoning about past program states. Our encoding therefore
tracks information about past states using computation histories. We define computation
histories as finite partial maps from timestamps, N, to snapshots, S. A snapshot describes an
abstract view of a program state. It is a parameter of our method. For instance, a snapshot
may capture the physical memory representation of the data structure under proof, while
abstracting from the remainder of the program state. Another parameter is a function | · |
that computes the abstract state of the data structure from a given snapshot.


           Inv(r) := ∃ H T C. CSS(r, C) ∗ |H(T )| = C
                       ∗ Hist(H, T ) ∗ Invhelp (H, T ) ∗ Invtpl (r, H, T )
   Invtpl (r, H, T ) := resources(r, H(T ))
                       ∗ (∀t, 0 ⩽ t ⩽ T ⇒ per_snapshot(H(t)))
                       ∗ (∀t, 0 ⩽ t < T ⇒ transition_inv(H(t), H(t + 1)))


   Figure 8 Definition of the shared state invariant encoding the hindsight reasoning. Variable H
represents the history, T the current timestamp in use and C the abstract state of the structure.

    Figure 8 shows a simplified definition of the invariant that encodes the hindsight reas-
oning. For sake of brevity, we provide only a high-level overview of the predicates used
in the invariant. The predicate Hist(H, T ) contains the mechanism to track the history
of snapshots. That is, H denotes the history that has been observed so far and T is the
current time stamp. Using appropriate ghost resources, it ensures that the timestamps are
non-decreasing and past states recorded in H are preserved by future updates to the history.
This allows us to define a past predicate ⟐s,t0 (q) with the intuitive meaning that the history
contains state s recorded after (or at) time t0 for which proposition q holds true. The exact
definition of the past predicate uses the ghost resources used to preserve the past states.
The predicate Hist(H, T ) also guarantees that dom(H) = {0 . . . T }, ensuring that there are
no gaps in the history.
    The conjunct |H(T )| = C and the predicate CSS(r, C) together tie the abstract state C
of the data structure to the latest snapshot in the history. The predicate CSS(r, C) is the
dual of the representation predicate CSS(r, C) used in the client-level atomic specification.
Both represent one half of an ownership over the abstract state of the structure, keeping the
abstract state defined by Inv(r) synchronized with the representation predicate CSS(r, C).
    The helping protocol predicate Invhelp (M, T ) contains a registry of thread IDs with un-
modifying linearization points that require helping from other concurrent threads. For each
thread ID tid in the registry, the protocol stores information such as the start time of the
thread, whether it has been linearized or not, etc.
    The predicate Invtpl (r, H, T ) captures invariants particular to the data structure under
proof. It is further composed of three abstract predicates that are meant to be instantiated
with the structure specific invariants. The three predicates serve the following purpose. The
first predicate resources(r, H(T )) ties the current snapshot to the physical representation of
the structure. The predicate Hist(H, T ) contains a conjunct (∀t, t < T ⇒ H(t) ̸= H(t + 1)).
Together with the predicate resources, this conjunct forces a thread to update the history
whenever the structure is modified.
    The predicate per_snapshot(H(T )) captures the structural invariants that hold for any
18   Verifying Lock-free Search Structure Templates


     given snapshot. For instance, when proving the skiplist template, this predicate holds facts
     about the nodes hd and tl having maximum height, etc. The predicate transition_inv(s, s′ )
     captures a transition invariant on snapshots observed in the history. That is, it constrains
     how certain quantities evolve over time. Again as an example from the skiplist template
     proof, the fact that a node marked in s remains marked in s′ is included here. Crucially, the
     facts in transition_inv(s, s′ ) allow temporal interpolation required to establish facts about
     past states in the history (like in Section 3.2).
         To summarize, the proof author defines the snapshot of the structure, the function | · |,
     and instantiates the three abstract predicates in Invtpl appropriately. The resulting shared
     state invariant then tracks the history and handles the helping protocol without requiring
     further fine-tuning to the data structure at hand.


      5      Verifying the Skiplist Template
     We relate the intuitive proof argument from Section 3 to the development on hindsight
     reasoning in Iris in Section 4 to obtain a complete proof of the skiplist template. To achieve
     this, we must perform three tasks required by the proof method in Section 4. The first
     task is to determine the decisive operations that potentially alter the structure, and resolve
     the prophecy around those operations. As discussed previously, the decisive operations are
     markNode for delete and changeNext for insert. The search operation does not modify the
     abstract state and hence, it has no decisive operation.
         The second task is to define a snapshot in the context of the skiplist template and
     instantiate Invtpl appropriately. This includes the predicate resources that ties the concrete
     state of the structure to the latest snapshot, as well as invariants that allow temporal
     interpolation. The third and the final task is to prove the hindsight specification for the
     core operations.
         In this section we focus on the second task of defining the snapshot and providing invari-
     ants necessary to formalize the intuitive proof argument. Once, we have set up the right
     invariants, the formalized proof follows the intuitive proof very closely. We explain this with
     delete as an example.


     5.1     Snapshot and the Skiplist Template Invariant
     Recall that the notion of keysets are central to the intuitive proof argument for the core oper-
     ations of the skiplist template. Hence, a snapshot of the structure must contain information
     about the keysets. For encoding keysets in Iris, we borrow heavily from [19], especially the
     keyset camera and the representation of keysets via the Flow Framework. We defer further
     details on this matter to Appendix C.
         We define the snapshot of the skiplist template as a tuple containing the following com-
     ponents:

          the set of nodes N comprising the structure (also referred to as the footprint below)
          the abstract state of the structure (a set of keys)
          the mark bits (a map from N to N → Bool, i.e., a Boolean per level)
          the next pointers (a map from N to N → N )
          the keys (a map from N to K)
          the height of nodes (a map from N to N)
          the representation of flow values
N. Patel, D. Shasha, and T. Wies                                                                     19



         Invtpl (r, H, T ) := resources(r, H(T ))
                             ∗ (∀t, 0 ⩽ t ⩽ T ⇒ per_snapshot(H(t)))
                             ∗ (∀t, 0 ⩽ t < T ⇒ transition_inv(H(t), H(t + 1)))
           resources(s) :=
                              ∗
                             n∈FP(s)
                                       Node(n, mark(s, n), next(s, n), key(s, n), height(s, n))

                             ∗ resources_keyset(s)
   transition_inv(s, s ) := (FP(s) ⊆ FP(s′ ))
                      ′

                             ∗ (∀n, key(s′ , n) = key(s, n) ∧ height(s′ , n) = height(s, n))
                             ∗ (∀n i, mark(s, n, i) = true ⇒ mark(s′ , n, i) = true)
                             ∗ (∀n i, mark(s, n, i) = true ⇒ next(s′ , n, i) = next(s, n, i))


   Figure 9 Instantiating Invtpl with invariants of the skiplist template.



    We reparameterize the mark(n, i) function introduced earlier to take the snapshot as an
argument. Thus, we use mark(s, n, i) to mean the mark bit of node n at level i in snapshot
s. We redefine next(·), key(·), keyset(·) and other such functions similarly by adding the
snapshot s as an additional parameter. We also use FP(s) to represent the footprint of the
snapshot s.
    We now present the skiplist template invariant in Figure 9. The resources predicate ties
the snapshot to the concrete state through an intermediary node-level predicate Node(n, k, h, mk, nx).
This predicate actually ties the physical representation of a node in the heap to the abstract
quantities (key(·), height(·), mark(·) and next(·), respectively) that the skiplist template relies
on. The Node predicate also owns all the resources needed to execute the helper functions.
The skiplist template proof is parametric in the definition of Node. Thus, we achieve proof
reuse across skiplist variants that follow the same high-level skiplist algorithm, but imple-
ment the node differently. We provide more details on this matter later. We discuss some
concrete node implementations in Section 6.
    The predicate resources_keyset(s) capture the ownership resources required for keyset
reasoning. Using the ghost resources in Iris and the keyset camera from [19], it ensures that
the keysets and the logical contents of nodes in s satisfy (KeysetPr).
    The predicate per_snapshot captures structural invariants that hold for all snapshots
recorded in the history. This includes invariants of three kinds: first, invariants to ensure
that each component of the snapshot is of the correct type and the maps (from nodes to
mark bits, next pointers, etc.) are defined for all nodes in the footprint; second, the node-
level invariants relating the node’s inset, outset, mark bit, etc (like Invariant 1); and third,
invariants about the hd and tl nodes, such as key(s, hd) = −∞, height(tl) = L, etc.
    The predicate transition_inv(s, s′ ) captures invariants about how certain quantities evolve
over time, such as that mark bits once set to true remain true. The invariants 2, 3, and
7 presented in Section 3 are part of this predicate. These invariants form the crux of the
hindsight reasoning, as they enable temporal interpolation.
    Before we go into the formal proof argument for delete, we must discuss how to reason
about the node-level helper functions. Figure 10 shows the specification for the helper
functions assumed by the skiplist template. The specifications are logically atomic, i.e.,
they behave like a single atomic step in the template. The preconditions for all of the
20   Verifying Lock-free Search Structure Templates


     1    k h mk nx. Node(n, k, h, mk, nx) getKey n k. Node(n, k, h, mk, nx)
     2    k h mk nx. Node(n, k, h, mk, nx) getHeight n h. Node(n, k, h, mk, nx)
     3    k h mk nx. Node(n, k, h, mk, nx) ∗ (i < h) findNext i n n′ . Node(n, k, h, mk, nx) ∗ (nx(i) = n′ )
     4

     5
         k h mk nx. Node(n, k,′ h, mk, nx) ∗ (i < h) markNode i n
           x. Node(n, k, h, mk , nx) ∗ (mk(i) = true ⇒ x = Failure ∗ mk ′ = mk)
                                                                                
     6
                          ∗(mk(i) = false ⇒ x = Success ∗ mk ′ = mk[i ↣ true])
     7

                                                      changeNext i n n′ e
     8
         k h mk nx. Node(n, k, h, ′mk, nx) ∗ (i < h)
           x. Node(n, k, h, mk, nx ) ∗ ((mk(i) = true ∨ nx(i) ̸= n′ ) ⇒ x = Failure ∗ nx ′ = nx)
                                                                                                 
     9
                             ∗((mk(i) = false ∧ nx(i) = n′ ) ⇒ x = Success ∗ nx ′ = nx[i ↣ e])


          Figure 10 Specifications of the helper functions used by the skiplist template.


     functions rely solely on the predicate Node. The functions getKey, getHeight and findNext
     read various components of the node. Note that findNext reads both the mark bit and the
     next pointer together.
         The specification for functions markNode and changeNext is slightly more complex because
     they potentially change the structure. Let us explain them briefly. For markNode on node
     n at level i, the return value (Success or Failure) is determined by whether n is already
     marked at i. If it is, then the function returns Failure without modifying the node. If it
     is unmarked, then markNode successfully marks it, and updates the node accordingly. The
     specification for changeNext can be interpreted similarly. Here, the return value hinges upon
     the mark bit being false and the next pointer of n pointing to n′ at i.


     5.2      Proof of delete
     We now have all the ingredients to show that delete satisfies (HindSpec). We provide only
     a high-level summary of the proof here. Please see Appendix C.3 for more details.
        The precondition provides access to the invariant Inv(r) and knowledge that the thread
     ID is tid with start time t0 . Additionally, the thread has the right to resolve prophecy p
     around the decisive operations, and if the thread observes a successful decisive operation,
     then the atomic update AU(Φ) is available to help with the linearization. The delete
     operation begins with traverse. Using the ⟐ operator defined in Section 4.2, we express
     the postcondition of traverse as

          ⟐s,t0 (k ∈ keyset(s, c) ∧ (res ⇐⇒ k ∈ C(s, c))).

     Intuitively, this assertion captures that there is a past state s in the history (after time point
     t0 ) in which k is in the keyset of c and res is true iff k is in the logical contents of c.
          The argument here, like the intuitive proof argument in Section 3 proceeds by case
     analysis on res (returned by traverse). Let us first consider the case that res is false.
     The delete operation also terminates with false. Since the thread terminates without
     any calls to the decisive operations, this case corresponds to the ¬Upd(pvs) case in the
     postcondition of (HindSpec). The postcondition requires delete to establish the predicate
     PastLin(del, k, false, t0 ). In this context, establishing this predicate amounts to identifying a
     witness past state in which k was not part of the abstract state. Clearly, this is witnessed by
     state s from the specification of traverse. Applying (KeysetPr) in state s, we can establish
     the predicate PastLin(del, k, false, t0 ).
N. Patel, D. Shasha, and T. Wies                                                                    21


     Now, let us consider the case that res is true. The maintainanceOp_del marks node c at
the higher level, but the interesting part of the proof is when the decisive operation markNode
is called at the base level (Line 15). Again there are two cases to consider, depending on
whether markNode succeeds. If markNode succeeds, then we can establish Upd(pvs) as we see
a Success value being resolved. In this case, the precondition of (HindSpec) provides the
atomic update AU(Φ). Since, the thread has modified the abstract state, this becomes the
linearization point. The thread can linearize with AU(Φ) to obtain the receipt Φ and satisfy
its postcondition. The proof also has to update the history with the new snapshot of the
structure, as c goes from being unmarked to marked.
     The final (and most interesting) case is when markNode fails. Here again, we must
establish PastLin(del, k, false, t0 ) to complete the proof of (HindSpec). Two facts are useful:
(i) in the past state s referred to in the traverse spec, we can establish that mark(s, c) =
false; and (ii) since the markNode has failed, in the current state say s0 , mark(s0 , c) = true.
Hence, by using the second conjunct of transition_inv in Figure 9 and temporal interpolation
on the two facts above, we can infer the existence of two consecutive states s1 and s2 ,
such that mark(s1 , c) = false and mark(s2 , c) = true. Clearly, a concurrent delete thread
marked c in state s2 . Hence, this state becomes the witness to establish the predicate
PastLin(del, k, false, t0 ). This completes the proof that delete satisfies (HindSpec).


 6     Proof Mechanization and Evaluation
We now shed light on the mechanization of the hindsight methodology, as well as its applic-
ation to the skiplist template. We additionally reverify the multicopy template from [35]
using our new hindsight specification to modularize the proof effort. Although the mul-
ticopy algorithms are lock-based, hindsight reasoning is helpful in their verification. The
case study demonstrates a substantial reduction in proof size due to the encoding of hind-
sight reasoning in Iris, illustrating the generality of our contribution. Our development is
available as a VM and docker image on Zenodo [3].
    All of the proofs we discuss below are mechanized in Iris/Coq. The templates, traversals
and the node implementations are written in Iris’s default programming language HeapLang.
In order to correctly capture the dependence between different layers of the proofs (such as
hindsight specification and the templates, the templates and the traverse/node implement-
ations), we heavily make use of Coq’s module system.
    The organization of our proofs is shown in Figure 11. Going from left to right, the
first column relates to the formalization of hindsight reasoning in Iris. The box “Hind-
sight” captures the assumptions regarding the hindsight specification from Section 4. These
assumptions not only include the hindsight specification itself but also the relevant defin-
itions of snapshots, histories, etc. The module “Client-level Spec” relates the client-level
specification expressed in terms of atomic triples to the hindsight specification used for the
template-level proofs. The corresponding proof involves the reasoning about prophecies and
the helping protocol, which is done once and for all and applicable to all data structures
that fulfill the assumptions made in the “Hindsight” module.
    The middle column consists of modules for the two verified templates (skiplist and mul-
ticopy) and the associated proofs verifying the template operations against the hindsight
specification. We discuss them in turn.
Skiplist template case study. The skiplist template, as described in Figure 2, abstracts
from the concrete implementations of nodes and the traverse operation. Hence, we package
their specifications into separate modules. To ensure that the specified data structure invari-
22   Verifying Lock-free Search Structure Templates


                             −→
                          Traverse
                          Node
                          Client-level
                          Hindsight
                          Eager
                          Lazy
                          Multicopy
                          Skiplist
                                Travresal
                                Impl.
                                         99K
                                 Travresal
                                   Template
                                     Template
                                       Spec
                                       21
                           satisfies   assumes




        Figure 11 The structure of our proofs. Each box represents a collection of modules relevant to
     the label. The dashed arrows represent module dependence, i.e., assumption of specifications. The
     normal arrows represent implementation of the target module (fulfillment of the assumptions).


     ant for the skiplist template is not vacuous, we also verified an init routine that initializes
     the data structure and establishes the invariant.
         The final column shows modules for the two node implementations of the skiplist tem-
     plate, as well as the eager and lazy traversal discussed in Section 2. The helper functions
     markNode and changeNext are implemented using an atomic CAS operation in both of the
     node implementations. The crux of the node implementation for the skiplist template is to
     determine a memory representation of the mark bit and the next pointer (at some level)
     such that both values can be read or written together with one atomic CAS operation. The
     first node implementation does this by using a sum type. The second node implementation
     is conceptually similar but uses more low-level data types instead of a sum type.
         The traversal and node implementations above correspond to several existing lock-free
     (skip)list algorithms from the literature. The Herlihy-Shavit skiplist algorithm [11, § 14] is
     obtained by instantiating our template with the eager traversal, the node implementation
     2, and maintenance operations that link higher-level nodes in increasing order of level and
     unlink nodes in the opposite order. The Michael set [32] is obtained as a degenerate case of
     the Herlihy-Shavit template instantiation where the skiplist is restricted to L = 2 (For L = 2,
     Level 1 consists of only a fixed single edge between the sentinel nodes. So, conceptually, Level
     1 can be ignored in this case.)
         We obtain a novel variant of a skiplist by replacing the eager traversal in the Herlihy-
     Shavit instantiation with the lazy traversal. The lazy traversal is inspired by the Harris list
     algorithm [10], which is obtained as a degenerate case of this new lazy skiplist algorithm by
     restricting it to L = 2.
         We present a summary of the proof effort for the skiplist template in Table 1. The
     proof-checking time was measured on the Docker image running on an Apple M1 Pro chip
     with 16GB RAM. The flow library contains the Iris formalization of the Flow Framework
     developed in [19, 35]. As a minor contribution, we extend this library with general lemmas
     for reasoning about graph updates that have an affect on an unbounded number of nodes.
     These lemmas are useful for the proofs of insert, delete and lazy traverse. The unbounded
     updates, as well as the maintenance operations, are the reason for the relatively high number
     of proof lines for the insert and delete operations.
     Multicopy template case study. The multicopy template from [35] generalizes search
     structures such as the lock-based Log-Structured Merge (LSM) tree used widely in modern
     database systems. It satisfies the Map ADT specification, with search and upsert (for inser-
     t/update) as its core operations. To deal with the complexity of future-dependent external
N. Patel, D. Shasha, and T. Wies                                                                          23


                        Skiplist Template (Iris/Coq)
                        Module               Code    Proof     Total    Time
                        Flow Library            0      5330      5330      33
                        Hindsight               0       950       950      11
                        Client-level Spec       9       329       338      18
                        Skiplist               12      1693      1705      26
                        Skiplist Init(∗)        6       319       325      15
                        Skiplist Search(∗)      7        62        69       6
                        Skiplist Insert(∗)     37      3457      3494     111
                        Skiplist Delete(∗)     28      2401      2429      72
                        Node Impl. 1          118       908      1026      35
                        Node Impl. 2          106       836       942      35
                        Eager Traversal        38      1165      1203      96
                        Lazy Traversal         47      2063      2110     145
                        Total                 408    19513     19921     603
                         Herlihy-Shavit         243 11212       11455       390
    Table 1 Summary of the proof effort. For each module, we show the number of lines of program
code, lines of proof, total number of lines, and the proof-checking time in seconds. The code for the
initialization and the core operations of the skiplist (entries with (∗)) is technically defined in the
“Skiplist” module, however here we present them separately for each operation to provide a better
picture. The count for Herlihy-Shavit is the summation of rows “Hindsight”, “Client-level Spec”,
all “Skiplist” modules, “Node Impl. 2” and “Eager Traversal”.



linearization points, the original proof relies on an intermediate template-level specification
based on the concept of search recency.
    Table 2 presents a detailed comparison of the multicopy template proofs from [35] versus
the new proof based on the hindsight framework. The original proof consists of a total
of 2779 lines. By contrast, the definitions (“Defs”) and “Client-level Spec” proofs can be
factored out of the total cost of the hindsight-based proof, because it is part of the hindsight
library itself. Hence, the new proof based on hindsight reasoning consists of only 1310 lines,
which is a reduction of 53%. To summarize, the improvement stems from the fact that the
original proof relies on an intermediate specification and a helping protocol that is tailored
to multicopy structures, while our new proof uses a helping protocol that is shared among
all proofs that build on the new hindsight proof method.
    While the majority of the reduction in the proof size stems from the elimination of
structure-specific specifications and helping protocol proofs, we also saw a minor reduction
in the size of the remainder of the proof. One outlier is the proof of upsert. Here, the
increase is attributed to the fact that the proof has to construct a fresh snapshot when the
operation succeeds. However, this construction is conceptually simple and could be factored
out into more abstract lemmas that are provided directly by the hindsight library.


 7     Related Work

The formal verification of linearizability has received much attention in recent years. We
refer to [6] for a survey of relevant techniques and focus our discussion to the most closely
related works.
    Our work builds on the idea of template algorithms for lock-based concurrent search
24   Verifying Lock-free Search Structure Templates


                                  Multicopy Template (Iris/Coq)
                                  Module                Original Hindsight
                                  Defs                       866         (950)
                                  Client-level Spec          434         (338)
                                  LSM                        741           540
                                  Search                     411           399
                                  Upsert                     327           371
                                  Total                    2779          1310
         Table 2 Comparison of multicopy template proofs. The column “Original” shows the number
     of lines from the proofs in [35], while “Hindsight” shows them for our new proof effort. Module
     “Defs” represents definitions required for proving the client-level specification (helping invariant,
     history predicate, etc). Module “Client-level Spec” contains the proof relating the intermediate
     specification (Search Recency Specification from [35] and Hindsight Specification in our paper) to
     the client specification. Module “LSM” contains definitions required to instantiate the frameworks
     for LSM trees. Modules “Search” and “Upsert” refer to the proofs for the search and upsert
     operations, respectively. Entries in ‘()’ for the ‘Hindsight’ column are not included in the total due
     to being part of the hindsight library.



     structures of [19, 20, 35], which we extend to the setting of lock-free implementations. A
     common challenge when verifying linearizability of lock-free data structures is the prevalence
     of future-dependent and external linearization points. Hindsight theory [7, 8, 23, 27, 28, 33]
     has emerged as a suitable technique to address this challenge in the context of concurrent
     search structures. To our knowledge, we are the first to formalize hindsight reasoning within
     a foundational program logic. Tools like Poling [38], plankton [27, 28], and nekton [26]
     automate hindsight reasoning at the expense of an increased trusted code base. However,
     these tools currently cannot handle complex data structures with unbounded outdegree like
     skiplists. Also, they do not aim to characterize the design space of related concurrent data
     structures like our template algorithms do.
         Other techniques for dealing with future-dependent linearization points include argu-
     ments based on forward simulation (e.g., by tracking all possible linearizations of ongoing
     operations [13], tracking a partial order [18], or using commit points [4]) and backward sim-
     ulation (e.g., using prophecy variables [1, 16, 24]). Our encoding of hindsight reasoning in
     Iris combines forward reasoning (by tracking the history of the data structure state) and
     backward reasoning (by using prophecies). However, the details of this encoding are for the
     most part hidden from the proof engineer by providing a higher-level reasoning interface
     based on past predicates and temporal interpolation as proposed in [28]. Our comparison
     with a prior proof of multicopy structure templates [35] suggests that this abstraction helps
     to reduce the proof complexity.
         Several works propose techniques for automatically verifying concurrent skiplists. Ab-
     dulla et al. [2] propose a technique for verifying linearizability of lock-free list-based data
     structures using forest automata. The evaluation considers bounded skiplists with up to 3
     levels. However, the implementation does not scale to larger bounds and the unbounded case
     is outside the scope of the technique. We note that the height of the skiplist is tied to the
     expected runtime of the skiplist operations. To guarantee the expected worst-case runtime
     bounds, the skiplist’s height must be of order O(log(n)) where n is the expected maximal
     number of entries in the list. For this reason, real-world skiplist implementations are also
     parametric in the height. Heights up to 63 levels are feasible in deployed skiplists [25], so
     the restriction to height 3 in [2] is unrealistic. By contrast, our proofs cover skiplists of
N. Patel, D. Shasha, and T. Wies                                                                  25


arbitrary height.
    Sánchez and Sánchez [36] present an SMT-based approach towards an automated veri-
fication of concurrent lock-based skiplists. The approach is based on a decidable theory of
unbounded skiplists. However, it does not consider lock-free implementations and focuses
on establishing shape invariants preserved by the structure instead of proving linearizability.
    Unlike these automated tools, our approach does not rely on data-structure specific
decidable theories for reasoning about inductive properties of heap graphs. Instead, we build
on the Flow Framework [21, 22, 29], which enables local reasoning about such properties over
general graphs in separation logic. As a minor contribution, we extend the mechanization
of the Flow Framework from [20] with lemmas to reason about graph updates that affect
properties of an unbounded number of nodes.
    There are some skiplist algorithms that are not immediately covered by our template
algorithm. For example, skiplists based on the algorithm presented in [9] such as Java’s
ConcurrentSkipListMap [34] use backlinks to avoid restarts when a traversal fails. However,
we believe that our template algorithm can be extended to subsume such algorithms by
abstracting from the restart policy, similarly to how the present template abstracts from the
maintenance policy.
    In this paper, we assume a programming language with a garbage collected semantics.
The rationale for this assumption is that issues arising from manual memory reclamation can
be addressed by orthogonal means. For instance, [30, 31] propose a technique that decouples
the proof of data structure correctness from that of the underlying memory reclamation
algorithm, allowing the correctness proof of the data structure to be carried out under the
assumption of garbage collection. Recent work also showed how to carry out such modular
proofs in program logics like Iris [14].

 8     Conclusions and Future Work
This paper shows how to verify some of the most challenging concurrent data structure
algorithms in existence. The accompanying proofs are fully mechanized in the foundational
program logic Iris. The proofs are modular and cover the broader design space of the
underlying algorithms by parameterizing the verification over aspects such as the low-level
representation of nodes and the style of data structure maintenance.
    Besides being the first work to verify unbounded lock-free skiplists, the work has de-
veloped technologies for Iris, particularly hindsight reasoning, that can be useful in many
applications.
    Our proofs guarantee safety but not liveness. This limitation is shared by the algorithms
they verify: in any highly concurrent (minimal or no locking) setting, a thread t may never
complete because of other threads that overtake it. Fortunately, this never happens in
practice where threads all advance more or less at the same pace. Verifying liveness under
such fairness assumptions remains an interesting direction for future work.
    Another area of future work is to verify algorithms that mix locking parts with lock-free
parts both for single copy and multicopy search structures. We believe that the present
framework will be a good basis for that effort.

Acknowledgments
This work is funded in parts by NYU Wireless and by the United States National Science
Foundation under grants CCF-2304758, 1840761, 2304758, and 25-74100-F1202. Further
funding came from an Amazon Research Award Fall 2021. Any opinions, findings, and
26   REFERENCES


     conclusions or recommendations expressed in this material are those of the authors and do
     not reflect the views of Amazon. We thank Sebastian Wolff for many insightful discussions
     and his suggestions to improve the presentation of the paper.


     References
      1 Martín Abadi and Leslie Lamport. The existence of refinement mappings. Theor. Com-
        put. Sci., 82(2):253–284, 1991.
      2 Parosh Aziz Abdulla, Lukás Holík, Bengt Jonsson, Ondrej Lengál, Cong Quy Trinh,
        and Tomás Vojnar. Verification of heap manipulating programs with ordered data by
        extended forest automata. In ATVA, volume 8172 of Lecture Notes in Computer Science,
        pages 224–239. Springer, 2013.
      3 Anonymous. Artifact for "Verifying Lock-free Search Structure Templates", April 2024.
        URL: https://zenodo.org, doi:00000.
      4 Ahmed Bouajjani, Michael Emmi, Constantin Enea, and Suha Orhun Mutluergil. Prov-
        ing linearizability using forward simulations. In CAV (2), volume 10427 of Lecture Notes
        in Computer Science, pages 542–563. Springer, 2017.
      5 Pedro da Rocha Pinto, Thomas Dinsdale-Young, and Philippa Gardner. Tada: A logic
        for time and data abstraction. In ECOOP, volume 8586 of Lecture Notes in Computer
        Science, pages 207–231. Springer, 2014.
      6 Brijesh Dongol and John Derrick. Verifying linearisability: A comparative survey. ACM
        Comput. Surv., 48(2):19:1–19:43, 2015.
      7 Yotam M. Y. Feldman, Constantin Enea, Adam Morrison, Noam Rinetzky, and Sharon
        Shoham. Order out of chaos: Proving linearizability using local views. In DISC, volume
        121 of LIPIcs, pages 23:1–23:21. Schloss Dagstuhl - Leibniz-Zentrum für Informatik,
        2018.
      8 Yotam M. Y. Feldman, Artem Khyzha, Constantin Enea, Adam Morrison, Aleksandar
        Nanevski, Noam Rinetzky, and Sharon Shoham. Proving highly-concurrent traversals
        correct. Proc. ACM Program. Lang., 4(OOPSLA):128:1–128:29, 2020.
      9 Mikhail Fomitchev and Eric Ruppert. Lock-free linked lists and skip lists. In PODC,
        pages 50–59. ACM, 2004.
     10 Timothy L. Harris. A pragmatic implementation of non-blocking linked-lists. In DISC,
        volume 2180 of Lecture Notes in Computer Science, pages 300–314. Springer, 2001.
     11 Maurice Herlihy and Nir Shavit. The art of multiprocessor programming. Morgan
        Kaufmann, 2008.
     12 Maurice Herlihy and Jeannette M. Wing. Linearizability: A correctness condition for
        concurrent objects. ACM Trans. Program. Lang. Syst., 12(3):463–492, 1990.
     13 Prasad Jayanti, Siddhartha Jayanti, Ugur Yavuz, and Lizzie Hernandez. A universal,
        sound, and complete forward reasoning technique for machine-verified proofs of lineariz-
        ability. PACMPL, 8(POPL), jan 2024. doi:10.1145/3632924.
     14 Jaehwang Jung, Janggun Lee, Jaemin Choi, Jaewoo Kim, Sunho Park, and Jeehoon
        Kang. Modular verification of safe memory reclamation in concurrent separation logic.
        Proc. ACM Program. Lang., 7(OOPSLA2):828–856, 2023.
     15 Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and
        Derek Dreyer. Iris from the ground up: A modular foundation for higher-order concurrent
        separation logic. J. Funct. Program., 28:e20, 2018. doi:10.1017/S0956796818000151.
REFERENCES                                                                                  27


16 Ralf Jung, Rodolphe Lepigre, Gaurav Parthasarathy, Marianna Rapoport, Amin Timany,
   Derek Dreyer, and Bart Jacobs. The future is ours: prophecy variables in separation
   logic. Proc. ACM Program. Lang., 4(POPL):45:1–45:32, 2020.
17 Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birke-
   dal, and Derek Dreyer. Iris: Monoids and invariants as an orthogonal basis for concurrent
   reasoning. In POPL, pages 637–650. ACM, 2015.
18 Artem Khyzha, Mike Dodds, Alexey Gotsman, and Matthew J. Parkinson. Proving
   linearizability using partial orders. In ESOP, volume 10201 of Lecture Notes in Computer
   Science, pages 639–667. Springer, 2017.
19 Siddharth Krishna, Nisarg Patel, Dennis E. Shasha, and Thomas Wies. Verifying con-
   current search structure templates. In PLDI, pages 181–196. ACM, 2020.
20 Siddharth Krishna, Nisarg Patel, Dennis E. Shasha, and Thomas Wies. Automated
   Verification of Concurrent Search Structures. Synthesis Lectures on Computer Science.
   Morgan & Claypool Publishers, 2021.
21 Siddharth Krishna, Dennis E. Shasha, and Thomas Wies. Go with the flow: com-
   positional abstractions for concurrent data structures. Proc. ACM Program. Lang.,
   2(POPL):37:1–37:31, 2018.
22 Siddharth Krishna, Alexander J. Summers, and Thomas Wies. Local reasoning for global
   graph properties. In ESOP, volume 12075 of Lecture Notes in Computer Science, pages
   308–335. Springer, 2020.
23 Kfir Lev-Ari, Gregory V. Chockler, and Idit Keidar. A constructive approach for proving
   data structures’ linearizability. In DISC, volume 9363 of Lecture Notes in Computer
   Science, pages 356–370. Springer, 2015.
24 Hongjin Liang and Xinyu Feng. Modular verification of linearizability with non-fixed
   linearization points. In PLDI, pages 459–470. ACM, 2013.
25 Meta.              Facebook       Open     Source    Library:         ConcurrentSkipList.
   https://github.com/facebook/folly/blob/main/folly/ConcurrentSkipList.h. Last
   accessed: Apr 2024.
26 Roland Meyer, Anton Opaterny, Thomas Wies, and Sebastian Wolff. nekton: A lineariz-
   ability proof checker. In CAV (1), volume 13964 of Lecture Notes in Computer Science,
   pages 170–183. Springer, 2023.
27 Roland Meyer, Thomas Wies, and Sebastian Wolff. A concurrent program logic with a
   future and history. Proc. ACM Program. Lang., 6(OOPSLA2):1378–1407, 2022.
28 Roland Meyer, Thomas Wies, and Sebastian Wolff. Embedding hindsight reasoning in
   separation logic. Proc. ACM Program. Lang., 7(PLDI):1848–1871, 2023.
29 Roland Meyer, Thomas Wies, and Sebastian Wolff. Make flows small again: Revisiting
   the flow framework. In TACAS (1), volume 13993 of Lecture Notes in Computer Science,
   pages 628–646. Springer, 2023.
30 Roland Meyer and Sebastian Wolff. Decoupling lock-free data structures from memory
   reclamation for static analysis. Proc. ACM Program. Lang., 3(POPL):58:1–58:31, 2019.
31 Roland Meyer and Sebastian Wolff. Pointer life cycle types for lock-free data structures
   with memory reclamation. Proc. ACM Program. Lang., 4(POPL):68:1–68:36, 2020.
32 Maged M. Michael. High performance dynamic lock-free hash tables and list-based sets.
   In SPAA, pages 73–82. ACM, 2002.
33 Peter W. O’Hearn, Noam Rinetzky, Martin T. Vechev, Eran Yahav, and Greta Yorsh.
   Verifying linearizability with hindsight. In PODC, pages 85–94. ACM, 2010.
34 Oracle. Java concurrent skiplist set. https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/ut
   Last accessed: Jan 2024.
28   REFERENCES


     35 Nisarg Patel, Siddharth Krishna, Dennis E. Shasha, and Thomas Wies. Verifying concur-
        rent multicopy search structures. Proc. ACM Program. Lang., 5(OOPSLA):1–32, 2021.
     36 Alejandro Sánchez and César Sánchez. Formal verification of skiplists with arbitrary
        many levels. In ATVA, volume 8837 of Lecture Notes in Computer Science, pages 314–
        329. Springer, 2014.
     37 Dennis E. Shasha and Nathan Goodman. Concurrent search structure algorithms. ACM
        Trans. Database Syst., 13(1):53–90, 1988.
     38 He Zhu, Gustavo Petri, and Suresh Jagannathan. Poling: SMT aided linearizability
        proofs. In CAV (2), volume 9207 of Lecture Notes in Computer Science, pages 3–19.
        Springer, 2015.
REFERENCES                                                                                        29


 A           Proof of Traversals

We provide additional details on the proof of the eager traversal, as well as the implement-
ation and proof of the lazy traversal.


A.1          Proof of Eager Traversal
We describe the proof of eager_i in more detail. Let us formally define the traversal invariant
EagerInv for eager_i as follows:

     EagerInv(k, p, c) := ⟐(mark(p, 0) = false ∧ key(p) < k) ∗ ⟐(k ∈ inset(c))

The predicate EagerInv captures the fact that eager_i witnessed node p to be unmarked
and its key less than k at some point during its traversal. Additionally, it witnessed that k
was in the inset of c at some prior state of the structure. We put the two facts about p and
c in separate ⟐ predicates because the two facts may hold for different past states.
     
 1  EagerInv(k, p, c)
 2 let eager_i 0 k p c =
 3   match findNext 0 c with
 4   | cn, true ->
 5     match changeNext 0 p c cn with
 6     | 
         Success ->
 7        EagerInv(k, p, c) ∗ mark(p, 0) = false ∗ next(p, 0) = cn ∗ key(p) < k
             
 8            mark(p, 0) = false ∗ key(p) < k ∗ k ∈ inset(p) ∗ k ∈ outset(p) ∗ k ∈ inset(cn)
             
 9            EagerInv(k, p, cn)
10          eager_i 0 k p cn
11        | Failure -> traverse ps cs k
12        cn, false ->
         |
13          EagerInv(k, p, c) ∗ mark(c, 0) = false ∗ next(c, 0) = cn
                                                                    
          EagerInv(k, p, c) ∗ mark(c, 0) = false ∗ next(c, 0) = cn 
14                       ∗(key(c) < k =⇒ k ∈ EagerInv(k, c, cn))
                               ∗(k ⩽ key(c) =⇒ ⟐(k ∈ keyset(c)))
                                                                    
15        let kc = getKey c in
16        ifkc < k then
17            EagerInv(k, c, cn)
18          eager_i 0 k c cn
19        else
            
20            ⟐(k ∈ keyset(c))
21          let res = (kc = k ? true : false) in
22
             c, res)
            (p,
23            ⟐(k ∈ keyset(c) ∧ res ⇐⇒ k ∈ C(c))

     Figure 12 Outline for the proof of the eager_i for the base level.


    For the moment, assume that predicate EagerInv(k, p, c) holds at the beginning of the
function call eager_i 0 k p c. The proof outline in Figure 12 shows that this is sufficient to
prove the traverse specification. We explain the critical steps of the proof in the following.
    The first critical step occurs when c is found to be marked, and the subsequent changeNext
call on p succeeds (Line 6). Immediately after this step, we can establish that mark(p, 0) =
false and next(p, 0) = cn due to the success of changeNext. The Invariant 3 allows us to infer
key(p) < k from EagerInv(k, p, c). In addition, we use the following structural invariant:
30   REFERENCES


        Invariant 5 For all nodes n, if mark(n, 0) is set to false then [key(n), ∞) ⊆ inset(n). As a
        consequence of the definition of edgesets and outset(n) (from Section 3.1), we additionally
        obtain outset(n) = (key(n), ∞).
     Invariant 5 helps us establish that k ∈ inset(p), k ∈ outset(p) and since next(p, 0) = cn,
     also k ∈ inset(cn). Using the rule that q implies ⟐q for an arbitrary proposition q, we can
     establish EagerInv(k, p, cn) before the recursive call on Line 10.
         The second critical step is when findNext determines c to be unmarked (Line 12). The
     proof goes by case analysis, depending on whether key(c) < k holds. First consider that this
     condition is true. Similar to the first critical step, we are able to establish EagerInv(k, c, cn)
     here as we have all the relevant facts at this moment. The predicate EagerInv(k, c, cn) is
     used for the recursive call on Line 18. Now consider the case that k ⩽ key(c). Here, we
     use ⟐(k ∈ inset(c)) provided by EagerInv(k, p, c). Let t be the time point when k ∈ inset(c)
     held true. Since c is unmarked currently, c must also have been unmarked at time t due to
     Invariant 2. And by Invariant 5, we can establish that k ∈     / outset(c) at time t. Thus, we
     conclude that also k ∈ keyset(c) held at time t. Similarly we conclude that C(c) = {key(c)}
     as c is unmarked. Putting this all together, we obtain:
        k ∈ C(c) ⇐⇒ k = key(c) ⇐⇒ res.
     This concludes the proof that predicate EagerInv is indeed an invariant for eager_i and is
     sufficient to prove the traverse specification.
         In the previous proof, we assumed EagerInv holds when eager_i begins executing at the
     base level. The final piece remaining from the complete proof of the traverse specification
     is to show that eager_i collects enough information at higher levels to establish EagerInv
     before traversing the base level. We explain this below.
         It is easy to see that for all higher levels i, eager_i can establish ⟐(mark(p, i) = false ∧
     key(p) < k) when it returns (p, _, _). (In fact, EagerInv contains the exact same facts about
     p and the same argument as in the proof outline for the base level is applicable.) Thus,
     when a predecessor p is chose from the higher level to initiate eager_i at the base level, we
     know that ⟐(mark(p, i) = false ∧ key(p) < k) holds. The current node c is chosen by calling
     findNext 0 p at Line 16 in Figure 4. If findNext determines p to be unmarked, then we
     can establish k ∈ inset(c) using the fact ⟐(key(p) < k) and Invariant 5. However, if p is
     found to be marked, then it is a bit tricky to establish that ⟐(k ∈ inset(c)). We require the
     following additional structural invariant.
        Invariant 6 For all nodes n, if there exists an i such that mark(n, i) is set to false, then
        mark(n, 0) is set to false.
     Invariant 6 captures the fact that the base level gets marked at the end. This fact is useful
     for us because we can combine it with ⟐(mark(p, i) = false) to obtain ⟐(mark(p, 0) = false).
     Since findNext has found p to be marked at the base level, we can determine that it got
     marked at some time point between the point in time when ⟐(mark(p, 0) = false) held and
     the present. Let t be the time point right before p got marked. The following invariant gives
     us useful information about which node next(p, 0) can be pointing to at time t:
        Invariant 7 For all nodes n and level i, once mark(n, i) is set to true, next(n, i) does
        not change.
     Invariant 7 preceisely says that next(p, 0) = c at time t. Thus, we have found a moment
     in time when mark(p) = false, key(p) < k and next(p, 0) = c. These three facts allow us
     to immediately conclude that k ∈ inset(c) at time t. This finally completes the proof of
     traverse.
REFERENCES                                                                                                31


A.2     Lazy Traverse
The code for the lazy traversal is shown in Figure 13. While the lazy_rec implementation
is almost identical to eager_rec, the two differ in the per-level traversal in lazy_i and
eager_i. The lazy_i function here keeps track of three nodes while traversing: node p is
the last unmarked node it witnessed, node pn is the node that p was pointing to when p
was traversed, and c is the node that is currently being traversed. The function lazy_i
begins by reading the next pointer and mark bit of c. If c is found to be marked, then
lazy_i simply continues with the successor of c. If c is unmarked, then the operation key k
is compared with key(c). In case key(c) < k, then again lazy_i continues with c as the last
seen unmarked node. Otherwise, k ⩽ key(c). In this case, it attempts to unlink the marked
segment between nodes p and c. The conditional on Line 10 checks if there is a segment
to remove. If that is indeed the case, then lazy_i calls changeNext to unlink the segment
between p and c. If changeNext succeeds, then there is a further check to make sure c is
still unmarked. If so, then lazy_i returns with p and c. In all other cases where changeNext
fails or c is found to be marked, lazy_i restarts the traverse function.

1  let lazy_i i k p pn c =                                19 let lazy_rec i ps cs k =
2    match findNext i c with                              20   let p = ps[i+1] in
 3   | cn, true -> lazy_i i k p pn cn                     21   let c, _ = findNext i p in
 4   | cn, false ->                                       22   let p′ , c ′ , res = lazy_i i k p c c in
 5     let kc = getKey c in                               23   ps[i] <- p′ ;
 6     if kc < k then                                     24   cs[i] <- c ′ ;
 7       lazy_i i k c cn cn                               25   if i = 0 then
 8     else
                                                          26     (p′ , c ′ , res)
 9       let res = (kc = k ? true : false) in
                                                          27   else
10       if pn = c then
                                                          28     lazy_rec (i-1) ps cs k
11         (p, c, res)
                                                          29
12       else
                                                          30   let traverse ps cs k =
13         match changeNext i p pn c with
                                                          31     lazy_rec (L - 2) ps cs k
14         | Success ->
15           let _, b = findNext i c in
16           if b then traverse ps cs k
17           else (p, c, res)
18         | Failure -> traverse ps cs k

    Figure 13 The lazy traversal for the skiplist template corresponding to the Harris List style
traversal.




A.3     Proof of Lazy Traversal
The proof idea for the lazy traversal is similar to that of the eager traversal. We provide
a brief overview of the traversal invariant for lazy_i, and why it is sufficient to establish
the required specification for traverse. The following discussion focuses on the lazy_i
executing on the base level, for sake of simplicity.
   The traversal invariant for lazy_i is defined as below:

      LazyInv(k, p, pn, c) := EagerInv(k, p, pn) ∗ (pn ̸= c ⇒ ∃ ls. MarkedSeg(pn, ls, c))
    MarkedSeg(pn, ls, c) := (ls = [] ⇒ ⟐(next(pn, i) = c))
                             ∗ (ls = [n0 ,...,nl ] ⇒ ⟐(next(pn, 0) = n0 )
                                                     ∗ (∀ 0 ⩽ j < l. ⟐ next(nj , 0) = nj+1 ))
                                                     ∗ ⟐(next(nl , 0) = c)
32   REFERENCES


     The invariant LazyInv relies on EagerInv and a new predicate MarkedSeg that stores the
     segment of marked nodes. Additionally, the predicate establishes that the nodes pn and c
     are the start and end points of the marked segment.
         To see that LazyInv is indeed an invariant, consider Lines 3 and 7 where lazy_i is
     recursively called. At Line 3, the marked segment can be extended by including the marked
     node c, while p and pn remain unchanged. On the other hand, at Line 7, the second conjunct
     of LazyInv becomes trivially true, and eagerinv(k, c, cn) can be established in the same way
     as for eager_i.
         Let us now show why LazyInv is sufficient to prove the traverse specification. Consider
     the points where lazy_i terminates (lines 11 and 17). When terminating at Line 11, we
     know that pn = c. Hence, LazyInv provides the predicate EagerInv(k, p, c). Using the same
     argument as eager_i, we can establish the required postcondition. Now consider Line 17.
     In this case, the thread has successfully unlinked the marked segment, hence it can establish
     that mark(p, 0) = false and next(p, 0) = c right after the call to changeNext. Note that the
     later check whether c is unmarked must succeed in order for lazy_i to terminate. Hence,
     at the point of the successful changeNext, c must also be unmarked, giving us all the facts
     necessary to establish the required postcondition. This completes the proof of lazy_i.

      B     Soundness of Hindsight Specification
     This section focuses on the soundness of the Hindsight specification, i.e., the proof that
     any structure that satisfies (HindSpec) must also satisfy (ClientSpec). We begin with some
     background on Iris that will be necessary for the proof, followed by additional details on the
     predicate Hist and the helping invariant Invhelp . Finally, we provide a proof outline relating
     (HindSpec) to the (ClientSpec).

     B.1    Iris Primer
     Iris is a state-based concurrent separation logic. Assertions in the logic express ownership
     of resources. These resources include both physical resources that are manipulated by the
     program as well as ghost resources that capture auxiliary information for the purpose of
     the proof and that are manipulated using the proof rules of the logic. An example of an
     assertion describing a physical resource is the points-to predicate, ℓ 7→ v, which expresses
     ownership of heap location ℓ and constrains its stored value to be v. Two assertions P and
     Q (e.g. describing disjoint heap regions) can be composed using aseparating conjunction,
     P ∗ Q. The logic
                    supports
                               standard local reasoning
                                                          principles
                                                                     such as the frame rule: if the
     Hoare triple P e Q is valid, then so is P ∗ R e Q ∗ R for all frames R.
                                                                               γ
         To describe ghost resources, Iris provides assertions of the form a which state owner-
     ship of a chunk a of the ghost resource stored at ghost location γ. The chunk a must be
     drawn from a camera that is specified as part of the proof. Cameras generalize the partial
     commutative monoids that are commonly used to define the semantics of separating con-
     junction. The precise definition of these structures is immaterial for this paper. What is
     important is that a camera is a set S equipped with an operation a·b that is compatible with
                                                      γ     γ           γ
     separating conjunction in the following way: a ∗ b ⊣⊢ a · b . A simple example is the
     MaxNat camera defined by S = {Max(n) | n ∈ N} and Max(n) · Max(m) = Max(max(n, m)).
         A proof can introduce ghost resources as needed by allocating a fresh ghost location γ. A
     proof can also update chunks of ghost resources at existing ghost locations using view shifts,
         γ       γ
      a ⇛ b . A view shift is only allowed if replacing a by b is frame-preserving. Intuitively,
     this means that for any c such that the full ghost resource stored at γ may be a · c before the
REFERENCES                                                                                        33


update, b must also compose with c. For example, in the MaxNat camera, all updates are
frame-preserving because composition (maximum) is totally defined. However, in general,
this is not the case.
    To reduce the burden on the proof author, Iris provides a library of predefined paramet-
erized cameras. One such camera that we will use below is the agreement camera Ag(X)
which is defined for any set X. The elements take the form agree(x) for x ∈ X and com-
position is only defined in the case of identity: agree(x) · agree(x) = agree(x). Another
predefined camera we will use is that of finite partial maps from some set X to some camera
R, Map(X, R), with composition defined by lifting the composition on R pointwise to maps.
    To enable reasoning about shared resources, Iris provides the notion of an invariant. Any
Iris assertion P can be turned into an invariant, denoted P . Once an invariant has been
created, it becomes a duplicable resource, which means that it can be commonly owned by
all threads. An individual thread may access (and manipulate) the resources described by
the underlying assertion P when performing a computation step, provided P is reestablished
after each step.
    A reoccurring pattern in Iris proofs is to have an invariant that holds authoritative
ownership of the current state of a resource, and each thread may additionally own partial
knowledge about this resource that the thread gathered during its execution. To encode
this pattern, Iris provides the authoritative camera Auth(R) defined over any camera R. The
authoritative camera has elements of the form • a to denote authoritative ownership of
a ∈ R and ◦ a to denote fragmental ownership. The composition • a · ◦ b expresses the fact
that b is a fragment of a, i.e., ∃ c, a = b · c. For example, the camera Auth(MaxNat) is very
useful to establish lower bounds of a monotonically non-decreasing quantity. The definitions
                                                              γ             γ
of Auth(MaxNat) yields the valid entailment: • Max(n) ∗ ◦ Max(n′ ) ⊢ n′ ≤ n. The
permitted frame-preserving updates are shown below:

                                                   n ≤ n′
                        auth-max-upd               γ                 γ
                                         •Max(n)       ⇛ •Max(n′ )

                                            γ                γ               γ
                 auth-max-snap •Max(n)          ⇛ •Max(n)        ∗ ◦Max(n)

The rule auth-max-upd requires that the update only increases the authoritative value to
guarantee that the new authoritative value n′ still composes with all fragmental values.

B.2    Tracking the Computation History
Hindsight arguments involve reasoning about past program states. Our encoding therefore
tracks information about past states using computation histories. We define computation
histories as finite partial maps from timestamps, N, to snapshots, S. A snapshot describes an
abstract view of a program state at a particular time. It is a parameter of our encoding. For
instance, a snapshot may capture the physical memory representation of the data structure
under proof, while abstracting from the remainder of the program state. Another parameter
of our encoding is a function | · | that computes the abstract state of the data structure from
a given snapshot.
    The predicate Hist(H, T ) consists of two ghost resources: one resource to store the au-
thoritative computation history H, and one resource to store the last timestamp T used in
H. Whenever the program changes the program state in a way that is observable at the level
of snapshots, the invariant forces H to be updated with a new snapshot at time T + 1, and T
to be increased by 1. To track T , we use the camera Auth(MaxNat), which implicitly encodes
34   REFERENCES


     the fact that timestamps are non-decreasing, effectively serializing the snapshot changes in
     the history.
         We want threads to be able to own fragmental knowledge of the authoritative history H.
     These history fragments are then used to define past predicates that express the existence of
     a past state with a certain snapshot. To this end, we use the camera Auth(Map(N, Ag(S)))
     for the resource that tracks the history. The use of the agreement camera ensures that
     the history can only be updated by appending to it (i.e., all snapshots of past states are
     preserved).
         The predicate Hist(H, T ) is then defined as
                                        γt                  γm
          Hist(H, T ) := • Max(T )           ∗ • agree(H)
                            ∗ dom(H) = {0 . . . T } ∗ ∀t < T. H(t) ̸= H(t + 1) .

     Here, we abuse notation and write agree(H) for the function that takes the history H to an
     element of Auth(Map(N, Ag(S))) in the expected way. The second last conjunct ensures that
     the authoritative history contains no gaps. The purpose of the last conjunct is to ensure
     that a thread appends to the history whenever any change to the program state is made
     that affects the snapshot (see discussion in Section 4.2).


     B.3       Augmenting op with Prophecies
     In light of the discussion in Section 4.1, we must augment op with auxiliary ghost code that
     creates and resolves the relevant prophecies. We do this by defining the wrapper function
     op given in Figure 14. Let us first briefly discuss how prophecy variables can be used in
     Iris. The right side of Figure 14 shows the specifications of the two functions related to
     manipulating prophecies. The function NewProph returns a fresh prophecy p that predicts a
     sequence of values pvs, captured by the resource Proph(p, pvs). This resource can be owned
     and shared among threads via a shared invariant. The resource is also non-duplicable.
         The values contained in the sequence pvs are determined by how p is resolved using
     the Resolve command. The rule prophecy-resolution ties the observed value (v) to the
     next prophesied value (the head of pvs). It also updates Proph(p, pvs) to the tail of pvs for
     the remaining prophesied values that are yet to be observed. In our context, we want the
     prophecy to predict whether the decisive operations (i.e. markNode and changeNext) will
     succeed as well as their return value. Hence, we augment delete and insert by wrapping
     their decisive operations inside a Resolve command. The return value is captured by the
     resolution on Line 5. For our purposes, we assume that pvs is a sequence of Success or
     Failure values (i.e., the result of each attempted call to the decisive operation) followed by
     a special value END(res) indicating that no further future calls are expected, and that res
     will be the final return value3 . Given the prophesied sequence of values pvs, a thread will
     exhibit an unmodifying linearization point iff pvs does not contain any Success values.
         Let us now turn to op, which starts by generating a unique thread identifier using
     NewThreadID on Line 2. We also implement NewThreadID using the NewProph construct.
     There are two benefits to this: (i) Iris makes sure that prophecy identifiers are unique out
     of the box, and (ii) now we can use Iris’s erasure theorem for prophecies to argue that the
     augmented code op has the same behavior as op. After, op creates a prophecy p as described


     3
         We have to also consider the case where pvs is not of this form, but that is a trivial case to handle and
         thus we do not consider it in this discussion.
REFERENCES                                                                                                     35



1 let op r k =                                               prophecy-creation
    let tid = NewThreadID in
                                                                             
2
                                                                 True NewProph p. ∃ pvs. Proph(p, pvs)
3   let p = NewProph in
4   let v = op p r k in
                                                             prophecy-resolution
5   Resolve p to END(v); v                                   
                                                             Proph(p,   pvs) Resolve p to v
                                                              ∃ pvs ′ . Proph(p, pvs ′ ) ∗ pvs = v :: pvs ′

    Figure 14 Wrapper augmenting op with prophecy-related ghost code, whose specification is
given on the right.



                             Inv(r) := ∃ H T C. CSS(r, C) ∗ |H(T )| = C
                                          ∗ Hist(H, T ) ∗ Invhelp (H, T ) ∗ Invtpl (H, T )
                                                        γr
                      Invhelp (H, T ) := ∃ R. • R
                                          ∗
                                              ∗
                                              tid∈R
                                                      ∃ op k vp t0 Φ Tok. Reg(tid, op, k, vp , t0 , Φ, Tok)

     Reg(tid, op, k, vp , t0 , Φ, Tok) := Thread(tid, t0 ) ∗ State(op, k, vp , t0 , Φ, Tok)

        State(op, k, vp , t0 , Φ, Tok) := Pending(op, k, vp , t0 , Φ) ∨ Done(op, k, vp , t0 , Φ, Tok)

          Pending(op, k, vp , t0 , Φ) := AUop (Φ) ∗ ¬PastLin(op, k, vp , t0 )

        Done(op, k, vp , t0 , Φ, Tok) := (Φ(vp ) ∨ Tok) ∗ PastLin(op, k, vp , t0 )


     Figure 15 Definition of the invariant encoding the helping protocol.


above, it invokes the underlying operation op, and finally, terminates after resolving p to
the result of op.
   We can now finally present the client-level specification with op:

           Inv(r) −∗ C. CSS(r, C) op p r k res C ′ . CSS(r, C ′ ) ∗ Ψop (k, C, C ′ , res) .

The next section provides details on our choice of Inv(r) and the proof of op.

B.4       Proof of op
Figure 15 shows a simplified definition of the invariant that encodes the helping protocol4 .
The definitions are implicitly parameterized by a proposition Invtpl (r, H, T ), which abstracts
from the resources needed for proving that a specific structure satisfies the hindsight spe-
cification.
                                                                               γr
    The helping protocol predicate Invhelp (H, T ) contains a registry • R        of thread IDs
with unmodifying linearization points that require helping from other concurrent threads.
For each thread ID tid in the registry, the shared state contains Thread(tid, _) along with
the state of tid, which is either Pending or Done. Pending captures an uncommitted atomic
triple, and Done describes the operation after it has been committed. Note that we use the


4
    For presentation purposes, the proof outline presented here abstracts from some technical details of the
    actual proof in Iris.
36   REFERENCES


     notation AUop (Φ) to refer to the atomic update token of op and write just AU(ϕ) when op
     is clear.
         The proof outline for op is shown in Figure 16. The proof begins by creating a thread
     identifier tid and prophecy p. As alluded to earlier, NewThreadID is also just NewProph in
     disguise, hence we obtain two prophecy resources, one each for tid and p. Before we can
     invoke op, we must record the start time of this thread and perform a case split on Upd(pvs)
     to determine if this thread requires helping. For this, we open the invariant at Line 7. To
     record the start time, we give up the resource Proph(tid, _) to gain a duplicable resource
     Thread(tid, T0 ) in exchange ( T0 is the current timestamp). The exact details of this exchange
     are not relevant, so we continue with the case split on Upd(pvs). First consider the case that
     Upd(pvs) holds. Then, thread tid does not require helping and the hindsight specification
     can ensures that op linearizes correctly. This is quite straightforward, so we focus on the
     other case, i.e. Upd(pvs) does not hold.
         In order to register the thread for helping, we must establish PastLin(op, k, vp , T0 ) or
     its negation. Here, vp is the return value obtained by scanning for the end marker in pvs.
     We proceed by first checking if the thread can be linearized at the current timestamp T0 .
     If so, then we can safely linearize the thread right away. So let us focus on the more in-
     teresting case where we cannot linearize right away (Line 14). Here, the thread registers
     itself with the helping protocol by updating R to R ∪ {tid} using an update rule for the
     authoritative set camera (in Line 18). As part of registering for helping, it first establishes
     Pending(op, k, vp , T0 , Φ) by transferring its obligation to linearize to the shared state, cap-
     tured by the update token AU(Φ). The condition PastLin(op, k, vp , T0 ) follows from the
     fact that Ψop (k, |H0 (T0 )|, |H0 (T0 )|, vp ) does not hold. The thread also creates a fresh non-
     duplicable token Tok that it will later trade in for the receipt Φ(vp ).
         We are now at the point of invocation for op. Before continuing further, let us briefly
     switch to the role played by the concurrent thread that must linearize thread tid. The helping
     thread must update the structure, and as per the invariant, update the history M as well
     as the helping protocol Invhelp (H, T ). In particular, while updating the helping protocol, it
     scans over all threads registered for helping so far, moving them from state Pending to state
     Done as per the prophesied return value vp .
         Let us now return to the proof thread tid at Line 23. As precondition of (HindSpec), we
     give away Proph(p, pvs) and obtain the postcondition (Line 24). Simplifying the postcon-
     dition of (HindSpec) for our case ¬Upd(pvs), we obtain the predicate PastLin(op, k, vp , T0 ).
     Next, we make a final resolution of the prophecy on Line 26. Since, pvs ′ is the suffix of pvs,
     END(vp ) must also be the final item in pvs ′ . After resolution, we obtain END(vp ) = END(v)
     and by injectivity of the end marker, vp = v.
         We now have the predicate PastLin(op, k, v, T0 ) which we use to obtain the receipt of
     linearization from the shared invariant. Because PastLin(op, k, v, T0 ) holds now, we know
     thread tid cannot be in the Pending state. Hence, we know that thread tid must be in the
     Done state. Since the thread owns the unique token Tok, it trades it in to obtain Φ(v), which
     lets it complete the proof of its client-level specification.


      C     Additional detail on verification of the Skiplist Template

     C.1    Keysets Reasoning
     Recall that keysets exhibit two properties that are crucial for localizing the functional cor-
     rectness specification of search structures from the global data structure graph to individual
     nodes in the graph: (1) keysets partition the set of all keys, and (2) a node’s contents is
REFERENCES                                                                                                                      37




 1   Inv(r) ∗ C. CSS(r, C)
 2
      op r k =
   let
 3     AU(Φ)
 4   let tid = NewThreadID
     
 5     AU(Φ) ∗ Proph(tid, _)
 6
     n p = NewProph in
     let                                                               o
 7        AU(Φ) ∗ Proph(tid, _) ∗ Proph(p, pvs) ∗ Inv(r)
 8    (*
       Open invariant *)
 9     AU(Φ) ∗ Thread(tid, T0 ) ∗ Proph(p, pvs) ∗ CSS(r, C0 ) ∗ Invhelp (H0 , T0 ) ∗ . . .
10    (* Case analysis on Upd(pvs) : only showing ¬Upd(pvs) *)
                                                                                      γr
11     AU(Φ) ∗ Thread(tid, T0 ) ∗ Proph(p, pvs) ∗ CSS(r, C0 ) ∗ • R      ∗ tid ∈
                                                                               / R ∗ ...
12    (* Let vp such that pvs contains END(vp ) *)
13    (* Case analysis on Ψop (k, |H0 (T0 )|, |H0 (T0 )|, vp ) : only showing ¬Ψop (|H0 (T0 )|, |H0 (T0 )|, vp ) *)
                                                                            γr
14        Thread(tid, T0 ) ∗ Proph(p, pvs) ∗ CSS(r, C0 ) ∗ • R        ∗ tid ∈
                                                                            /R
          
15          · · · ∗ AU(Φ) ∗ Thread(tid, T0 ) ∗ ¬PastLin(op, k, vp , T0 )
          
16          · · · ∗ AU(Φ) ∗ Thread(tid, T0 ) ∗ Pending(op, k, vp , T0 , Φ) ∗ Tok
          
17          · · · ∗ State(op, k, vp , T0 , Φ, Tok) ∗ Tok
                                       γr                       γr
18    (* Ghost update: • R                  ⇛ • R ∪ {tid}             *)
                                                                γr                                           γr
      n                                                                                                                 o
19        Thread(tid, T0 ) ∗ Proph(p, pvs) ∗ ◦ {tid}                 ∗ Tok ∗ CSS(r, C0 ) ∗ • R ∪ {tid}            ∗ ...
                                                                γr
      n                                                                                                                o
20        Thread(tid, T0 ) ∗ Proph(p, pvs) ∗ ◦ {tid}                 ∗ Tok ∗ CSS(r, C0 ) ∗ Invhelp (H0 , T0 ) ∗ . . .
21    (* Close invariant *)
                                                                γr
      n                                                                      o
22        Thread(tid, T0 ) ∗ Proph(p, pvs) ∗ ◦ {tid}                 ∗ Tok
23
      ( v = op p r k in
      let
                                            γr                                                        )
          Thread(tid, T0 ) ∗ ◦ {tid}             ∗ Tok ∗ Proph(p, pvs ′ ) ∗ (pvs = prf ++ pvs ′ )
24
                         ∗(Upd(pvs) −∗ Φ(v)) ∗ (¬Upd(pvs) −∗ PastLin(op, k, vp , T0 ))
                                            γr
      n                                                                                                 o
25        Thread(tid, T0 ) ∗ ◦ {tid}             ∗ Tok ∗ Proph(p, pvs ′ ) ∗ PastLin(op, k, vp , T0 )
26    Resolve p to END(v);
                                            γr
      n                                                                                                            o
27        Thread(tid, T0 ) ∗ ◦ {tid}             ∗ Tok ∗ Proph(p, []) ∗ (vp = v) ∗ PastLin(op, k, vp , T0 )
28    (*
      n Open invariant *)                   γr
                                                                                                                            o
29        Thread(tid, T0 ) ∗ ◦ {tid}             ∗ Tok ∗ PastLin(op, k, v, T0 ) ∗ CSS(r, C1 ) ∗ Invhelp (H1 , T1 ) ∗ . . .
                                  γr
      n                                                                                             o
30        · · · ∗ Tok ∗ ◦ {tid}        ∗ PastLin(op, k, v, T0 ) ∗ State(op, k, v, T0 , Φ, Tok)
      
31      · · · ∗ Tok ∗ PastLin(op, k, v, T0 ) ∗ Done(op, k, v, T0 , Φ, Tok)
      
32      · · · ∗ Tok ∗ PastLin(op, k, v, T0 ) ∗ (Φ(v) ∨ Tok)
      
33      · · · ∗ Φ(v) ∗ PastLin(op, k, v, T0 ) ∗ (Φ(v) ∨ Tok)
      
34      · · · ∗ Φ(v) ∗ PastLin(op, k, v, T0 ) ∗ Done(op, k, v, T0 , Φ, Tok)
      
35      Φ(v) ∗ CSS(r, C1 ) ∗ Invhelp (H1 , T1 ) ∗ . . .
36    (*
       Close invariant *)
37      Φ(v)
38    v
39      res C ′ . CSS(r, C ′ ) ∗ Ψop (C, C ′ , res)

     Figure 16 Outline for the proof of the client-level specification for op.
38   REFERENCES


     always a subset of its keyset. To capture these properties naturally in Iris, [19] introduces a
     keyset camera. An element of the keyset camera is a pair of sets of keys (K, C) with C ⊆ K.
     We associate such pairs to regions in the data structure graph such that C is the union of
     the node contents in the region and K is the union of the nodes keysets. The composition of
     such pairs is defined as (pair-wise) disjoint union. The validity and the composition operator
     of the keyset camera then implicitly capture the desired properties (1) and (2) above.
         Using this camera we tie the keyset reasoning to the invariant for the skiplist template
     by instantiating the predicate resources_keyset (from Section 5) as follows:

        resources_keyset(s) := •(K, C(s))
                                            γ
                                                ∗
                                                     ∗
                                                    n∈FP(s)
                                                              ◦(keyset(s, n), C(s, n))
                                                                                         γ
                                                                                             .

                                γ
     The assertion •(K, C(s)) signifies ownership of the logical contents C(s) of the structure
     in the state captured by snapshot s. Recall that K is the set of all keys. The set FP(s) tracks
     the footprint of s, i.e., the set of all nodes in the data structure graph captured by s. Each
     individual node n ∈ FP(s) owns its keyset keyset(s, n) and node-local logical contents C(s, n).
     The keyset camera enforces that the keyset(s, n) are pairwise disjoint, C(s, n) ⊆ keyset(s, n)
                                     S                                   S
     for each n, and that C(s) = n∈FP(s) C(s, n), respectively, K = n∈FP(s) keyset(s, n).
         A node’s keyset and contents are then tied to the actual physical representation of the
     data structure via an abstract predicate that is instantiated for each node implementation.
     Recall that a node’s keyset is defined in terms of its inset, an inductive quantity defined
     over the edgeset graph of the structure. As in [19], we use the Flow Framework [21, 22] to
     obtain a node-local characterization of the inset quantity and to reason about insets in Iris.
     We omit these details here as they are not relevant for understanding the high-level proof
     idea.

     C.2    Helper Function Specifications
     Our encoding of the hindsight specification (HindSpec) requires us to resolve a prophecy
     around each program step that may modify the structure. In the context of the skiplist tem-
     plate, the structure is modified using calls to the helper functions markNode and changeNext
     on the base-level list. Unfortunately, prophecies in Iris can only be resolved around physical
     computation steps in the Iris programming language HeapLang and not at a more abstract
     level around logical atomic triples. Hence, the atomic triples for markNode and changeNext
     themselves must capture the relevant aspects of the reasoning related to prophecy resolution.
         Figure 17 shows these atomic triple specifications. We focus on the markNode specific-
     ation in particular. The assertions in blue are those already described in Figure 10. The
     additional assertions in brown are concerned with the prophecy reasoning. The precondition
     Proph(p, pvs) gives the right to resolve the prophecy p. The additional postcondition says
     that marknode resolves the prophecy an arbitrary number of times, but if it succeeds, then
     a Success value was seen in the list of prophesied values pvs, yielding Upd(pvs). Otherwise,
     it says that no Success value was seen so far, yielding Upd(prf ). The template proof for
     delete then uses this information to infer whether Upd(pvs) holds and prove the appropriate
     postcondition from the hindsight specification. The specification of changeNext is similar.

     C.3    Proof outline of delete
     In this section, we discuss the proof of code in more detail. The proof outline is shown in
     Figure 18. We want to show that delete satisfies (HindSpec). The precondition provides
REFERENCES                                                                                           39


1          k h mk nx. Node(n, k, h, mk, nx) ∗ (0 < h)∗Proph(p, pvs)
2                             markNode 0 n p
    *       x. Node(n, k, h, mk ′ , nx)∗Proph(p, pvs ′ ) ∗ (pvs = prf ++ pvs ′ ) +
3       ∗(mk(0) = false ⇒ x = Success ∗ mk ′ = mk[0 ↣ true]∗Upd(pvs))
                  ∗(mk(0) = true ⇒ x = Failure ∗ mk ′ = mk∗¬Upd(prf ))
4

5          k h mk nx. Node(n, k, h, mk, nx) ∗ (0 < h)∗Proph(p, pvs)
6                            changeNext 0 n n′ e p
    *                      x. Node(n, k, h, mk, nx ′ )∗Proph(p, pvs ′ ) ∗ (pvs = prf ++ pvs ′ ) +
7       ∗((mk(0) = false ∧ nx(0) = n′ ) ⇒ x = Success ∗ mk ′ = mk[0 ↣ true]∗Upd(pvs))
                  ∗((mk(0) = true ∨ nx(0) ̸= n′ ) ⇒ x = Failure ∗ mk ′ = mk∗¬Upd(prf ))


    Figure 17 Specifications of the helper functions with the prophecies.


access to the invariant Inv(r) and knowledge that the thread ID is tid with start time t0 .
Additionally, the precondition provides the conjunct (Upd(pvs) −∗ AU(Φ)), signifying that
the thread can perform its linearization in case of a successful decisive operation. The
precondition also provides the right to resolve prophecies. It is easy to see how prophecies
are mainpulated by the helper functions from the specifications in Figure 17, hence we ignore
them in the proof outline.
    The algorithm of delete begins with a call to traverse. The specification for traverse
provides the postcondition

    ⟐s,t0 (k ∈ keyset(s, c) ∧ (res ⇐⇒ k ∈ C(s, c))).

Note that we use the past operator ⟐s,t0 from Section 4.2 in the postcondition of traverse.
Intuitively, this assertion captures that there is a past state s in the history (after time point
t0 ) in which k is in the keyset of c and res is true iff k is in the logical contents of c. Note
that this implies mark(s, c, 0) = false due to Invariant 1.
     The delete algorithm proceeds by case analysis on the result of traverse. Let us first
consider the case that res is false (Line 8). The delete operation terminates with result false.
The specification (HindSpec) requires establishing the predicate PastLin(del, k, false, t0 ) in
this case. To this end, we must provide a witness past state in which k was not part of the
abstract state. We obtain this witness from the postcondition of traverse which provides
a past state s such that k ∈ keyset(s, c) and k ∈ / C(s, c). Applying (KeysetPr) in state s, we
can establish the predicate PastLin(del, k, false, t0 ) (Line 12).
     Let us now consider the case when res is true. The delete algorithm here calls the
helper function maintainanceOp_del, which marks node c at the higher levels. Thus, after
maintainanceOp_del terminates, we obtain the information that all higher levels of c are
marked (Line 16). Next, the helper function markNode is called at the base level to logically
delete c from the structure. In order to apply the specification of markNode, we open the
invariant Inv(r) to access the Node predicate for c (Line 18). Let the current snapshot at this
point (obtained by opening the invariant) be s0 . The call to markNode call either succeeds
or fails depending on whether mark(s0 , c, 0) = false holds. We consider both of the cases in
turn.
     First, suppose that markNode succeeds (Line 21). This implies that mark(s0 , c, 0) = false
and a new snapshot s1 must be constructed to record the marking of c. The proof then
appends s1 to the history stored in Inv(r) in order to reestablish Inv(r). Additionally, success
of markNode implies that Upd(pvs) holds. Hence, the thread must use the resource AU(Φ) to
40   REFERENCES

          n                                                           o
      1       Inv(r) ∗ Thread(tid, t0 ) ∗ (Upd(pvs) −∗ AU(Φ))
      2 let delete k =
      3   let ps = allocArr L hd in
      4   let cs = allocArr L tl in
      5
           p, c, res = traverse ps cs k in
          let
      6    ⟐s,t0 (k ∈ keyset(s, c) ∧ (res ⇐⇒ k ∈ C(s, c)))
      7   ifnot res then
      8       ⟐s,t0 (k ∈ keyset(s, c) ∧ (k ∈
                                           / C(s, c)))
                
      9           ⟐ (k ∈
                       / |s|)
                 s,t0
     10           ⟐s,t0 (Ψdel (k, |s|, |s|, false))
     11         false
                
     12           ¬Upd(pvs) ∗ PastLin(del, k, false, t0 )
     13       else
                
     14           ⟐s,t0 (k ∈ keyset(s, c) ∧ (k ∈ C(s, c)))
     15         maintainanceOp_del         c;
                  ⟐s,t0 (mark(s, c, 0) = false) ∗ ⟐s′ ,t0 (∀i, 0 < i < height(s′ , c) ⇒ mark(s′ , c, i) = true)
                
     16
                
     17           ⟐s,t0 (mark(s, c, 0) = false) ∗ Hist(H0 , T0 ) ∗ resources(s0 ) ∗ · · ·
                
     18          ⟐s,t0 (mark(s, c, 0) = false) ∗ Hist(H0 , T0 ) ∗ Node(c, s0 ) ∗ · · ·
     19         match markNode 0 c with
     20         | 
                  Success ->
     21            (mark(s0 , c, 0) = false) ∗ (mark(s1 , c, 0) = true) ∗ Upd(pvs) ∗ · · ·
                    
     22              Upd(pvs) ∗ AU(Φ) ∗ Ψdel (k, |s0 |, |s1 |, true) ∗ · · ·
                    
     23            Upd(pvs) ∗ Φ ∗ Hist(H0 [T0 + 1 ↣ s1 ], T0 + 1) ∗ resources(s1 ) ∗ · · ·
     24           traverse ps cs k; true
                  
     25            Upd(pvs) ∗ Φ
     26         | 
                  Failure ->
     27            ⟐s,t0 (mark(s, c, 0) = false) ∗ (mark(s0 , c, 0) = true) ∗ · · ·
                    
     28              (∃ s s t, (t0 ≤ t) ∗ Past(s1 , t) ∗ Past(s2 , t + 1) ∗ (mark(s1 , c, 0) = false) ∗ (mark(s2 , c, 0) = true)) · · ·
                     1 2
     29              (t ≤ t) ∗ Past(s1 , t) ∗ Past(s2 , t + 1) ∗ (key(s2 , c) ∈
                                                                              / |s2 |) · · ·
                     0
     30               ⟐s2 ,t0 (Ψdel (k, |s2 |, |s2 |, false)) · · ·
     31             false
                    
     32               ¬Upd(pvs) ∗ PastLin(del, k, false, t0 )

          Figure 18 Outline for the proof of the delete.


     linearize itself. The receipt of linearization Φ is exactly what is required in the postcondition
     of (HindSpec) in this case (Line 25).
         Finally, consider the case that markNode fails (Line 27). The delete algorithm terminates
     with result false in this case. Hence, we must again establish PastLin(del, k, false, t0 ) to
     complete the proof. That is, we must identify a witness past state such that k was not part of
     the abstract state of the structure. To compute this witness, note that mark(s, c, 0) = f alse
     for state s observed by traverse, while mark(s0 , c, 0) = true for the current state s0 . By
     transition_inv in Figure 9 and temporal interpolation, there must exist consecutive states
     s1 and s2 when c was marked at the base level (Line 28). Here, the predicate Past(s, t)
     represents the knowledge that the history recorded snapshot s at time t. The snapshot s2 is
     the required witness to establish the postcondition of (HindSpec) (Line 32). This completes
     the proof of delete.
