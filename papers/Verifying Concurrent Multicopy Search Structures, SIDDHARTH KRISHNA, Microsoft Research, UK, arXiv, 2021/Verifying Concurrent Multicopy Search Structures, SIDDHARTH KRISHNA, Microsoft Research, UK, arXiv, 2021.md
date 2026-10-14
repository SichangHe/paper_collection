                                         Verifying Concurrent Multicopy Search Structures

                                         NISARG PATEL, New York University, USA
                                         SIDDHARTH KRISHNA, Microsoft Research, UK
                                         DENNIS SHASHA, New York University, USA
arXiv:2109.05631v1 [cs.PL] 12 Sep 2021




                                         THOMAS WIES, New York University, USA
                                         Multicopy search structures such as log-structured merge (LSM) trees are optimized for high insert/up-
                                         date/delete (collectively known as upsert) performance. In such data structures, an upsert on key 𝑘, which
                                         adds (𝑘, 𝑣) where 𝑣 can be a value or a tombstone, is added to the root node even if 𝑘 is already present in
                                         other nodes. Thus there may be multiple copies of 𝑘 in the search structure. A search on 𝑘 aims to return the
                                         value associated with the most recent upsert. We present a general framework for verifying linearizability
                                         of concurrent multicopy search structures that abstracts from the underlying representation of the data
                                         structure in memory, enabling proof-reuse across diverse implementations. Based on our framework, we
                                         propose template algorithms for a) LSM structures forming arbitrary directed acyclic graphs and b) differential
                                         file structures, and formally verify these templates in the concurrent separation logic Iris. We also instantiate
                                         the LSM template to obtain the first verified concurrent in-memory LSM tree implementation.

                                         CCS Concepts: • Theory of computation → Logic and verification; Separation logic; Shared memory
                                         algorithms.

                                         Additional Key Words and Phrases: template-based verification, concurrent data structures, log-structured
                                         merge trees, flow framework, separation logic

                                         1   INTRODUCTION
                                         Krishna et al. [2020a] demonstrated how to simplify the verification of concurrent search structure
                                         algorithms by abstracting implementations of diverse data structures such as B-trees, lists, and
                                         hash tables into templates that can be verified once and for all. The template algorithms considered
                                         in [Krishna et al. 2020a; Shasha and Goodman 1988] handle only search structures that perform all
                                         operations on keys in-place. That is, an operation on key 𝑘 searches for the unique node containing
                                         𝑘 in the structure and then performs any necessary modifications on that node. Since every key
                                         occurs at most once in the data structure at any given moment, we refer to these structures as
                                         single-copy (search) structures.
                                            Single-copy structures achieve high performance for reads. However, some applications, such as
                                         event logging, require high write performance, possibly at the cost of decreased read speed and
                                         increased memory overhead. This demand is met by data structures that store upserts (inserts,
                                         deletes or updates) to a key 𝑘 out-of-place at a new node instead of overwriting a previous copy of
                                         𝑘 that was already present in some other node. Performing out-of-place upserts can be done in
                                         constant time (e.g., always at the head of a list). A consequence of this design is that the same key
                                         𝑘 can now be present multiple times simultaneously in the data structure. Hence, we refer to these
                                         structures as multicopy (search) structures.
                                            Examples of multicopy structures include the differential file structure [Severance and Lohman
                                         1976], log-structured merge (LSM) tree [O’Neil et al. 1996], and the Bw-tree [Levandoski et al.
                                         2013]. These concurrent data structures are widely used in practice, including in state-of-the-art
                                         database systems such as Apache Cassandra [Apache Software Foundation 2021] and Google
                                         LevelDB [Google 2021].

                                         ,,
                                         2021.


                                                                                                1
,,                                                 Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


                     Client Level              Template Level                Representation Level




                                                                                                    Specification
                                     refines       Search                        Node-level




                                                                                                       Layer
                      Map ADT
                                                  Recency                       Specifications




                                                                        es
                           assumes                    satisfies                        satisfies




                                                                      um
                                                                  ass




                                                                                                    Implementation
                                                                                     MCS
                                                   MCS




                                                                                                         Layer
                      Client code                                               Implementation
                                                 Template
                                                                                (e.g. LSM tree)




           Fig. 1. The structure of our verification effort. MCS stands for multicopy structure.



   Like the verification method proposed by Krishna et al. [2020a], we aim to prove that the
concurrent search structure of interest is linearizable [Herlihy and Tygar 1987], i.e., each of its
operations appears to take effect atomically at a linearization point and behaves according to a
sequential specification. For multicopy structures, the sequential specification is that of a (partial)
mathematical map that maps a key to the last value that was upserted for that key. The framework
proposed in [Krishna et al. 2020a; Shasha and Goodman 1988] does not extend to multicopy
structures as it critically relies on the fact that every key is present in at most one node of the
data structure at a time. Moreover, searches in multicopy structures exhibit dynamic non-local
linearization points (i.e., the linearization point of a search is determined by and may be present
during the execution of concurrently executing upserts). This introduces a technical challenge that
is not addressed by this prior work. We discuss further related work in §9.
   Contributions. This paper presents a framework for constructing linearizability proofs of concur-
rent multicopy structures with the goal of enabling proof reuse across data structures. Figure 1
provides an overview of our work. The paper starts by describing the basic intuition behind the
correctness proof of any multicopy structure (§2). We then derive an abstract notion of multicopy
structures similar to the abstract single-copy structures in the edgeset framework [Shasha and
Goodman 1988] (§3). By introducing this intermediate abstraction level ("Template Level" in the
figure) at which we can verify concurrent multicopy structure template algorithms, we aid proof
reuse in two ways. First, the template algorithms abstract from the concrete representation of the
data structure, allowing their proofs to be reused across diverse template instantiations. Second, the
specification against which the templates are verified ("Search Recency") admits simpler lineariz-
ability proofs than the standard client-level specification of a search structure. The proof relating
the client-level and template-level specification (§4) can be reused across all templates.
   We demonstrate our framework by developing and verifying concurrent multicopy templates for
a) LSM structures and b) differential file structures. The LSM template applies to existing LSM trees
as well as to structures that form arbitrary directed acyclic graphs (DAGs) (§5, §6, and §7). The
template and its proof support implementations based on different heap representations such as
lists, arrays, and B-link trees. Verifying an instantiation of one of the two templates for a specific
implementation involves only sequential reasoning about node-level operations.
   We have mechanized both the proof relating client-level and template-level specifications as
well as the verification of our template algorithms in the Coq-based interactive proof mode of the

                                                         2
Verifying Concurrent Multicopy Search Structures                                                    ,,


concurrent separation logic Iris [Jung et al. 2018; Krebbers et al. 2018, 2017]. Similar to [Krishna
et al. 2020a], our formalization uses the flow framework [Krishna et al. 2018, 2020b] to enable local
reasoning about inductive invariants of a general multicopy structure graph. In order to obtain a
concrete multicopy structure, we have instantiated the node-level operations assumed by the LSM
template for the LSM tree and verified their implementations in the automated separation logic
verifier GRASShopper [Piskac et al. 2014] (§8). The result is the first formally-verified concurrent
in-memory LSM tree implementation.
   This is an extended version of a conference paper [Patel et al. 2021]. All additional materials are
provided in the appendix.

2     MOTIVATION AND OVERVIEW
From a client’s perspective, a multicopy structure implements a partial mathematical map 𝑀 : KS ⇀
V of keys 𝑘 ∈ KS to values 𝑣 ∈ V. We refer to 𝑀 as the logical contents of the structure. The data
structure supports insertions and deletions of key/value pairs on 𝑀 and searches for the value
𝑀 (𝑘) associated with a given key 𝑘.
   The insert and delete operations are implemented by a single generic operation referred to as an
upsert. The sequential specification of upsert is as follows. The operation takes a key-value pair
(𝑘, 𝑣) and updates 𝑀 to 𝑀 [𝑘 ↣ 𝑣], associating 𝑘 with the given value 𝑣. To delete a key 𝑘 from the
structure, one upserts the pair (𝑘, □) where □ is a dedicated tombstone value used to indicate that 𝑘
has been deleted. The sequential specification of a search for a key 𝑘 is then as expected: it returns
𝑀 (𝑘) if 𝑀 is defined for 𝑘 and □ otherwise.
   Multicopy structures are commonly used in scenarios where the nodes representing the data
structure’s logical contents 𝑀 are spread over multiple media such as memory, solid-state drives,
and hard disk drives. Each node therefore contains its own data structure that is designed for the
particular characteristics of the underlying medium, typically an unsorted array at the root to allow
upserts to perform fast appends and a classical single-copy search structure (e.g., a hash structure
or arrays with bloom filters) for non-root nodes. The non-root nodes are typically read-only, so
concurrency at the node level is not an issue. In this paper, we consider the multicopy data structure
as a graph of nodes. We study template algorithms on that graph.

2.1    A Library Analogy to Multicopy Search Structures
To train your intuition about multicopy structures, consider a library of books in which new editions
of the same book arrive over time. Thus the first edition of book 𝑘 can enter and later the second
edition, then the third and so on. A patron of this library who enters the library at time 𝑡 and is
looking for book 𝑘 should find an edition that is either current at time 𝑡 or one that arrives in the
library after 𝑡. We call this normative property search recency.
   Now suppose the library is organized as a sequence of rooms. All new books are put in the first
room (near the entrance). When a new edition 𝑣 of a book arrives in the first room, any previous
editions of that book in that room are thrown out. When the first room becomes full, the books
in that room are moved to the second room. If a previous edition of some book is already in the
second room, that previous edition is thrown out. When the second room becomes full, its books
are moved to the third room using the same throwing out rule, and so on. This procedure maintains
the time-ordering invariant that the editions of the same book are ordered from most recent (at or
nearer to the first room) to least recent (farther away from the first room) in the sequence of rooms.
   A patron’s search for 𝑘 starting at time 𝑡 begins in the first room. If the search finds any edition
of 𝑘 in that room, the patron takes a photocopy of that edition. If not, the search proceeds to the
second room and so on.

                                                   3
,,                                              Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies




       (a)     𝑟   (𝑘 2 , 𝑑)            (b)     𝑟                         (c)    𝑟    (𝑘 2 , 𝑑)


       memory
       disk
                   (𝑘 1 , □)                         (𝑘 1 , □)
              𝑛1                               𝑛1                               𝑛1
                   (𝑘 2 , 𝑏)                         (𝑘 2 , 𝑑)




                                                                                      (𝑘 1 , □)
                   (𝑘 2 , 𝑎)                         (𝑘 2 , 𝑎)
              𝑛2                               𝑛2                               𝑛2    (𝑘 2 , 𝑏)
                   (𝑘 3 , 𝑐)                         (𝑘 3 , 𝑐)
                                                                                      (𝑘 3 , 𝑐)




                   (𝑘 1 , 𝑐)                         (𝑘 1 , 𝑐)                        (𝑘 1 , 𝑐)
              𝑛3                               𝑛3                               𝑛3
                   (𝑘 3 , 𝑏)                         (𝑘 3 , 𝑏)                        (𝑘 3 , 𝑏)




Fig. 2. (a) High-level structure of an LSM tree. (b) LSM tree obtained from (a) after flushing node 𝑟 to disk.
(c) LSM tree obtained (a) after compacting nodes 𝑛 1 and 𝑛 2 .


   Now suppose that the latest edition at time 𝑡 is edition 𝑣 and there is a previous edition 𝑣 ′.
Because of the time-ordering invariant and the fact that the search begins at the first room, the
search will encounter 𝑣 before it encounters 𝑣 ′. The search may also encounter an even newer
edition of 𝑘, but will never encounter an older one before returning. That establishes the search
recency property.
   Any concurrent execution of inserts and searches is equivalent to a serial execution in which (i)
each insert is placed in its relative order of entering the root node with respect to other inserts
and (iia) a search 𝑠 is placed after the insert whose edition 𝑠 copies if that insert occurred after 𝑠
began or (iib) a search 𝑠 is placed at the point when 𝑠 began, if the edition that 𝑠 copies was inserted
before 𝑠 began (or if 𝑠 returns no edition at all).
   Because the searches satisfy the search recency property, the concurrent execution is lineariz-
able [Herlihy and Wing 1990], which is our ultimate correctness goal.
   Note that the analogy as written has treated only inserts and searches. However, updates and
deletions can be implemented as inserts: an update to book 𝑘 can be implemented as the insertion
of a new edition; a delete of book 𝑘 can be implemented as the insertion of an edition whose value
is a “tombstone” which is an indication that book 𝑘 has been deleted.

2.2   Log-Structured Merge Trees
A prominent example of a multicopy structure is the LSM tree, which closely corresponds to the
library analogy described above. The data structure consists of a root node 𝑟 stored in memory
(the first room in the library), and a linked list of nodes 𝑛 1, 𝑛 2, . . . , 𝑛𝑙 stored on disk (the remaining
rooms). Figure 2 (a) shows an example.
   The LSM tree operations essentially behave as outlined in the library analogy. The upsert
operation takes place at the root node 𝑟 . A search for a key 𝑘 traverses the list starting from the
root node and retrieves the value associated with the first copy of 𝑘 that is encountered. If the
retrieved value is □ or if no entry for 𝑘 has been found after traversing the entire list, then the
search determines that 𝑘 is not present in the data structure. Otherwise, it returns the retrieved

                                                       4
Verifying Concurrent Multicopy Search Structures                                                       ,,


value. For instance, a search for key 𝑘 1 on the LSM tree depicted in Figure 2 (a) would determine
that this key is not present since the retrieved value is □ from node 𝑛 1 . Similarly, 𝑘 4 is not present
since there is no entry for this key. On the other hand, a search for 𝑘 2 would return 𝑑 and a search
for 𝑘 3 would return 𝑐.
   To prevent the root node from growing too large, the LSM tree performs flushing. As the name
suggests, the flushing operation flushes the data from the root node to the disk by moving its
contents to the first disk node. Figure 2 (b) shows the LSM tree obtained from Figure 2 (a) after
flushing the contents of 𝑟 to the disk node 𝑛 1 .
   Similar to flushing, a compaction operation moves data from full nodes on disk to their successor.
In case there is no successor, then a new node is created at the end of the structure. During the
merge, if a key is present in both nodes, then the most recent (closer-to-the-root) copy is kept,
while older copies are discarded. Figure 2 (c) shows the LSM tree obtained from Figure 2 (a) after
compacting nodes 𝑛 1 and 𝑛 2 . Here, the copy of 𝑘 2 in 𝑛 2 has been discarded. In practice, the length
of the data structure is bounded by letting the size of newly created nodes grow exponentially.
   The net effect of all these operations is that the data structure satisfies the time-ordering invariant
and searches achieve search recency.
   The LSM tree can be tuned by implementing workload- and hardware-specific data structures
at the node level. In addition, research has been directed towards optimizing the layout of nodes
and developing different strategies for the maintenance operations used to reorganize these data
structures. This has resulted in a variety of implementations today (e.g. [Dayan and Idreos 2018; Luo
and Carey 2020; Raju et al. 2017; Thonangi and Yang 2017; Wu et al. 2015]). Despite the differences
between these implementations, they generally follow the same high-level algorithms for the core
search structure operations.
   We construct template algorithms for concurrent multicopy structures from the high-level
descriptions of their operations and then prove the correctness of these operations. Notably our
LSM DAG template generalizes the LSM tree so that the outer data structure can be a DAG rather
than just a list. A number of existing LSM structures are based on trees (e.g. [Sears and Ramakrishnan
2012; Wu et al. 2015]). Practical implementations of tree-based concurrent search structures often
have additional pointer structures layered on top of the tree that make them DAGs. For instance,
many implementations use the link technique to increase performance. Here, when a maintenance
operation relocates a key 𝑘 from one node to another, it adds a pointer linking the two nodes, which
ensures that 𝑘 remains reachable via the old search path. A concurrent thread searching for 𝑘 that
arrives at the old node can then follow the link, avoiding a restart of the search from the root. Our
verified templates can be instantiated to lock-based implementations of this technique.

3     MULTICOPY SEARCH STRUCTURE FRAMEWORK
We build our formal framework of multicopy structures on the concurrent separation logic Iris [Jung
et al. 2018]. A detailed introduction to Iris is beyond the scope of this paper. We therefore introduce
only the relevant features of the logic as we use them.

3.1    Multicopy Search Structures
We abstract away from the data organization within the nodes, and treat the data structure as
consisting of nodes in a mathematical directed acyclic graph.
   Since copies of a single key 𝑘 can be present in different nodes simultaneously, we need a
mechanism to differentiate between these copies. To that end, we augment each entry (𝑘, 𝑣) stored
in a node with the unique timestamp 𝑡 identifying the point in time when (𝑘, 𝑣) was upserted:
(𝑘, (𝑣, 𝑡)). The timestamp plays the role of the book edition in the library analogy from the last
section. For example in Figure 3, (𝑘 3, 𝑐) was upserted after (𝑘 2, 𝑎), which was upserted after (𝑘 3, 𝑏).

                                                    5
,,                                                  Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


                         𝑘1     ⊥         𝑘1    (□, 6)          𝑘1      ⊥         𝑘1    (𝑐, 2)
                         𝑘2   (𝑑, 7)      𝑘2    (𝑏, 5)          𝑘2    (𝑎, 3)      𝑘2      ⊥
                         𝑘3     ⊥         𝑘3      ⊥             𝑘3    (𝑐, 4)      𝑘3    (𝑏, 1)
                              𝑟                𝑛1                    𝑛2                𝑛3


             Fig. 3. Abstract multicopy data structure graph for the LSM tree in Figure 2 (a).


To generate these timestamps, we use a single global clock, which we initialize to 1. Note that the
timestamp associated with an upserted value is auxiliary, or ghost, data that we use in our proofs to
track the temporal ordering of the copies present in the structure at any point. Implementations do
not need to explicitly store this timestamp information.
   Formally, let KS be the set of all keys and V a set of values with a dedicated tombstone value
□ ∈ V. A multicopy (search) structure is a directed acyclic graph 𝐺 = (𝑁 , 𝐸) with nodes 𝑁 and
edges 𝐸 ⊆ 𝑁 × 𝑁 . We assume that there is a dedicated root node 𝑟 ∈ 𝑁 which uniquely identifies
the structure. Each node 𝑛 of the graph is labeled by its contents 𝐶𝑛 : KS ⇀ V × N, which is a
partial map from keys to pairs of values and timestamps. For a node 𝑛 and its contents 𝐶𝑛 , we
say (𝑘, (𝑣, 𝑡)) is in the contents of 𝑛 if 𝐶𝑛 (𝑘) = (𝑣, 𝑡). We denote the absence of an entry for a
key 𝑘 in 𝑛 by 𝐶𝑛 (𝑘) = ⊥ and let dom(𝐶𝑛 ) B {𝑘 | 𝐶𝑛 (𝑘) ≠ ⊥}. We further write val(𝐶𝑛 ) : KS ⇀ V
for the partial function that strips off the timestamp information from the contents of a node,
val(𝐶𝑛 ) B 𝜆𝑘. (∃𝑣. 𝐶𝑛 (𝑘) = (𝑣, _) ? 𝑣 : ⊥).
   For each edge (𝑛, 𝑛 ′) ∈ 𝐸 in the graph, the edgeset es(𝑛, 𝑛 ′) is the set of keys 𝑘 for which an
operation arriving at a node 𝑛 would traverse (𝑛, 𝑛 ′) if 𝑘 ∉ dom(𝐶𝑛 ). We require that the edgesets
of all outgoing edges of a node 𝑛 are pairwise disjoint. Figure 3 shows a potential abstract multicopy
structure graph consistent with the LSM tree depicted in Figure 2 (a). Here, all edges have edgeset
KS.

3.2   Client-Level Specification
Our goal is to prove the linearizability of concurrent multicopy structure templates with respect to
their desired sequential client-level specification. As discussed earlier, the sequential specification
is that of a map ADT, i.e., the logical contents of the data structure is a mathematical map from keys
to values, 𝑀 : KS → V. The map 𝑀 associates every key 𝑘 with the most recently upserted value 𝑣
for 𝑘, respectively, □ if 𝑘 has not yet been upserted:
                      (
                       𝑣 if ∃𝑛 𝑡 . 𝐶𝑛 (𝑘) = (𝑣, 𝑡) ∧ 𝑡 = max {𝑡 ′ | ∃𝑛 ′ 𝑣 ′ . 𝐶𝑛′ (𝑘) = (𝑣 ′, 𝑡 ′)}
             𝑀 (𝑘) B
                        □ otherwise
We call 𝑀 (𝑘) the logical value of key 𝑘.
   Linearizability of a data structure is defined in terms of the concurrent execution histories of the
data structure’s operations [Herlihy and Tygar 1987; Herlihy and Wing 1990]. Hoare logics like Iris
emphasize proof decomposition, which means, in particular, that they strive to reason only about a
single data structure operation at a time. It is therefore difficult to specify linearizability directly in
such logics. Instead, we specify the intended behavior of each data structure operation in terms of
an atomic triple [da Rocha Pinto et al. 2014; Frumin et al. 2018; Jacobs and Piessens 2011; Jung et al.
2020, 2015]. Atomic triples can be thought of as the concurrent counterparts of sequential Hoare
triples. They formalize the intuition that a linearizable operation appears to take effect atomically
at a single point in time, the operation’s linearization point.
   More precisely, an atomic triple 𝑥®. 𝑃 𝑒 𝑣 . 𝑄 is made up of a precondition 𝑃, which may
refer to the variables 𝑥,® a postcondition 𝑄, which relates the variables 𝑥® and the return value 𝑣,
and a program 𝑒. The triple states that 𝑒 may assume that for each of its atomic steps up to its

                                                         6
Verifying Concurrent Multicopy Search Structures                                                           ,,


linearization point, the shared state satisfies 𝑃 for possibly different values of 𝑥® in each step. At
the linearization point, 𝑒 then changes the shared state to one that satisfies 𝑄 in one atomic step.
Afterwards, 𝑒 no longer access resources in 𝑃 or 𝑄. Intuitively, concurrently executing threads may
interfere with 𝑒 by modifying the shared state but they are required to maintain 𝑃 as an invariant.
   Now suppose that MCS(𝑟, 𝑀) is a representation predicate that provides the client view of a
multicopy structure with root 𝑟 , abstracting its shared state by the logical contents 𝑀. We then
require that the search and upsert methods respect the following client-level atomic specifications:
                    D                E                D                     E
                      𝑀. MCS(𝑟, 𝑀) upsert 𝑟 𝑘 𝑣 MCS(𝑟, 𝑀 [𝑘 ↣ 𝑣])                                   (1)
                    D                E              D                           E
                      𝑀. MCS(𝑟, 𝑀) search 𝑟 𝑘 𝑣. MCS(𝑟, 𝑀) ∗ 𝑀 (𝑘) = 𝑣                              (2)

The specification of upsert updates the logical value of 𝑘 to 𝑣. Thus upsert performs the “insert” of
the library analogy. The search specification states that search returns the logical value 𝑀 (𝑘) = 𝑣
of its query key 𝑘.

3.3   Template-Level Specification: Search Recency
The verification of multicopy structures requires reasoning about the dynamic non-local lineariza-
tion points of search, which are determined by the concurrently executing upserts. We want to
avoid having to do this reasoning each time we verify a new template for a multicopy structure
implementation. Our strategy is to provide an alternative template-level specification that uses a
more detailed abstraction of the computation history rather than just the logical contents. This
alternative specification will then have fixed local linearization points, simplifying the verification.
   We say that search satisfies search recency if each concurrent invocation search 𝑟 𝑘 either
returns the logical value associated with 𝑘 at the point when the search started, or any other copy
of 𝑘 that was upserted between the search’s start time and the search’s end time.
   We will show that if searches satisfy search recency and upserts take effect in a single atomic
step that changes the logical contents 𝑀 according to (1), then the multicopy structure is linearizable.
   We start by defining the upsert history 𝐻 ⊆ KS × (V × N) of a multicopy data structure as the set
of all copies (𝑘, (𝑣, 𝑡)) that have been upserted thus far. In particular, we require that any multicopy
structure will maintain the following predicates concerning 𝐻 and the global clock 𝑡:
                   HInit(𝐻 ) B ∀𝑘. (𝑘, (□, 0)) ∈ 𝐻

               HUnique(𝐻 ) B ∀𝑘 𝑡 ′ 𝑣 1 𝑣 2 . (𝑘, (𝑣 1, 𝑡 ′)) ∈ 𝐻 ∧ (𝑘, (𝑣 2, 𝑡 ′)) ∈ 𝐻 ⇒ 𝑣 1 = 𝑣 2

               HClock(𝑡, 𝐻 ) B ∀(𝑘, (_, 𝑡 ′)) ∈ 𝐻 . 𝑡 ′ < 𝑡
The predicate HUnique(𝐻 ) ensures that we can lift the total order 𝑡 1 ⩽ 𝑡 2 on timestamps to a total
order (𝑣 1, 𝑡 1 ) ⩽ (𝑣 2, 𝑡 2 ) on the pairs of values and timestamps occurring in 𝐻 . The lifted order simply
ignores the value component. Together with HInit(𝐻 ), this ensures that the following function is
well-defined:
                                       𝐻¯ B 𝜆𝑘. max {(𝑣, 𝑡) | (𝑘, (𝑣, 𝑡)) ∈ 𝐻 } .
The latest copy of a key will always be contained in some node 𝑛 ofÐthe data structure. If the data
structure implementation maintains the additional invariant, 𝐻 ⊇ 𝑛 ∈𝑁 𝐶𝑛 , then this guarantees
that 𝐻¯ is consistent with the logical contents 𝑀, i.e., for all keys 𝑘, 𝐻¯ (𝑘) = (𝑀 (𝑘), _). Finally, the
predicate HClock(𝑡, 𝐻 ) guarantees that HUnique(𝐻 ) is preserved when a new entry (𝑘, (𝑣, 𝑡)) is
added to 𝐻 for the current value of the global clock 𝑡.
   Assume that, similar to MCS(𝑟, 𝑀), we are given a template-level representation predicate
MCS(𝑟, 𝑡, 𝐻 ) that abstracts the state of a multicopy structure by its upsert history 𝐻 and the current

                                                        7
,,                                                       Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


value 𝑡 of the global clock. The desired template-level specification of upsert in terms of the new
abstraction is simply:
                      𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) upsert 𝑟 𝑘 𝑣 MCS(𝑟, 𝑡 + 1, 𝐻 ∪ (𝑘, (𝑣, 𝑡)))                               (3)

It states that upsert advances the value of the global clock from 𝑡 to 𝑡 + 1 and adds a new copy
(𝑘, (𝑣, 𝑡)) to the upsert history 𝐻 .
   The postcondition of search needs to express two properties. First, we must necessarily have
(𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 , where 𝑣 is the value returned by search, 𝑡 ′ is 𝑣’s associated timestamp, and 𝐻 is
the value of the upsert history at the linearization point. Moreover, let 𝐻 0 be the value of the upsert
history at the start of the search and define (𝑣 0, 𝑡 0 ) B 𝐻¯0 (𝑘). Then either 𝑣 is the logical value of 𝑘
at that point (i.e. 𝑣 = 𝑣 0 ) or 𝑡 ′ is the timestamp of an upsert for 𝑘 that happened after the search
started, i.e., 𝑡 0 < 𝑡 ′. This is equivalent to demanding that for all 𝑡 0′ and 𝑣 ′ such that (𝑘, (𝑣 ′, 𝑡 0′ )) ∈ 𝐻 0 ,
the returned timestamp 𝑡 ′ satisfies 𝑡 0′ ⩽ 𝑡 ′. We define the auxiliary abstract predicate SR(𝑘, 𝑣, 𝑡) to
mean that (𝑘, (𝑣, 𝑡)) ∈ 𝐻 for the value 𝐻 of the upsert history at the time point when the predicate
is evaluated.1 Using this predicate, the template-level specification of search is then expressed as
follows:
         ∀𝑣 0′ 𝑡 0′ . SR(𝑘, 𝑣 0′ , 𝑡 0′ ) −∗
               𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) search 𝑟 𝑘 𝑣 . ∃𝑡 ′ . MCS(𝑟, 𝑡, 𝐻 ) ∗ 𝑡 0′ ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻             (4)

 Here, we use the magic wand connective −∗ to express that the auxiliary local precondition
SR(𝑘, 𝑣 0′ , 𝑡 0′ ) must be satisfied at the time point when search is invoked.
   In the next section, we deal with the complexity of non-local dynamic linearization points of
searches once and for all by proving that any multicopy structure that satisfies the template-level
specification also satisfies the desired client-level specification. To prove the correctness of a given
concurrent multicopy structure, it then suffices to show that upsert satisfies its corresponding
template-level specification (3) and search satisfies (4). When proving the validity of the template-
level atomic triple of search for a particular implementation (or template), one can now always
commit the atomic triple (i.e., declare a linearization point) at the point when the return value 𝑣 of
the search is determined, i.e., when (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 is established. This linearization point is now
independent of concurrently executing upserts.

4    RELATING THE CLIENT-LEVEL AND TEMPLATE-LEVEL SPECIFICATIONS
We next prove that any concurrent execution of upsert and search operations that satisfy the
template-level specifications (3) and (4) can be linearized to an equivalent sequential execution
that satisfies the client-level specifications. Intuitively, this can be done by letting the upserts in
the equivalent sequential execution occur in the same order as their atomic commit points in the
concurrent execution, and by letting each search 𝑟 𝑘 occur at the earliest time after the timestamp
𝑡 ′ associated with the returned value 𝑣 of 𝑘. That is, if 𝑣 = 𝑣 0 (recall that (𝑣 0, 𝑡 0 ) = 𝐻¯ (𝑘) where 𝐻 is
the upsert history at the start of the search on 𝑘), then the search occurs right after it was invoked
in the concurrent execution. Otherwise we must have 𝑡 ′ > 𝑡 0 and the search occurs after the upsert
at time 𝑡 ′. The fact that such an upsert must exist follows from the template-level specifications.
    The intuitive proof argument above relies on explicit reasoning about execution histories. Instead,
we aim for a thread-modular proof that reasons about individual searches and upserts in isolation,
so that we can mechanize the proof in a Hoare logic like Iris. The proof we present below takes
inspiration from that of the RDCSS data structure by Jung et al. [2020].

1 In §4.2 we will express SR(𝑘, 𝑣, 𝑡 ) using appropriate Iris ghost state that keeps track of the upsert history.



                                                               8
Verifying Concurrent Multicopy Search Structures                                                      ,,



 1 let search 𝑟   𝑘 =                                    one-shot-prophecy-creation
                                                          True NewProph 𝑝. ∃𝑣 𝑝 . Proph(𝑝, 𝑣 𝑝 )
                                                                         
 2    let tid = NewProph in
 3    let 𝑝 = NewProph in
                                                         one-shot-prophecy-resolution
 4    let 𝑣 = search 𝑟 𝑘 in                              
                                                          Proph(𝑝, 𝑣 𝑝 ) Resolve 𝑝 to 𝑣 𝑣 𝑝 = 𝑣
                                                                                      
 5    Resolve 𝑝 to 𝑣; 𝑣

Fig. 4. Wrapper augmenting search with prophecy-related ghost code, whose specification is on the right.



4.1    Challenges and Proof Outline
Iris prophecies [Jung et al. 2020], based on the idea first introduced by Abadi and Lamport [1988],
allow a thread to predict what will happen in the future. In particular, one can use prophecies to
predict future events in order to reason about non-fixed linearization points [Vafeiadis 2008; Zhang
et al. 2012]. In our case, a thread executing search can use a prophecy to predict, at the beginning
of the search, the value 𝑣 that it will eventually return. In a thread-modular correctness proof, one
can then decide on how to linearize the operation based on the predicted value.
   The linearization point of a search operation occurs when an instruction of a concurrent upsert
is executed. One can view this as a form of helping [Liang and Feng 2013]: when an upsert operation
commits and adds (𝑘, (𝑣, 𝑡 ′)) to the upsert history 𝐻 , it also commits all the (unboundedly many)
concurrently executing search operations for 𝑘 that will return 𝑣. We encode this helping protocol
in the predicate MCS(𝑟, 𝑀) that captures the shared (ghost) state of the data structure, by taking
advantage of Iris’s support for higher-order ghost state.
   At a high level, the proof then works as follows. We augment search with auxiliary ghost code
that creates and resolves the relevant prophecies. We do this by defining the wrapper function
search given in Figure 4. The right side shows the specifications of the two functions related to
manipulating (one-shot) prophecies in Iris. The function NewProph returns a fresh prophecy 𝑝 that
predicts the value 𝑣 𝑝 . This fact is captured by the resource Proph(𝑝, 𝑣 𝑝 ) in the postcondition of the
Hoare triple specifying NewProph. The resource Proph(𝑝, 𝑣 𝑝 ) can be owned by a thread as well as
transferred between threads via shared resources such as the representation predicate MCS(𝑟, 𝑡, 𝐻 )
(as is usual in concurrent separation logics). The resource is also exclusive, meaning it cannot be
duplicated.
   The function search uses NewProph to create two prophecies, which it binds to tid and 𝑝. The
prophecy 𝑝 predicts the value 𝑣 that will eventually be returned by search. The value tid predicted
by the second prophecy will be used later as a unique identifier of the thread performing the search
when we encode the helping protocol, taking advantage of the fact that each prophecy returned by
NewProph is fresh. Freshness of prophecies also ensures that each prophecy can be resolved only
once, which is done using Resolve 𝑝 to 𝑣. This operation consumes the resource Proph(𝑝, 𝑣 𝑝 ) and
yields the proposition 𝑣 𝑝 = 𝑣. It is used on line 5 of search to express that the value predicted by 𝑝
is indeed the value 𝑣 returned by search.
   If 𝑣 is equal to the current logical value 𝑣 0 of 𝑘 at the start of search, then the proof commits
the client-level atomic triple right away. If instead 𝑣 0 ≠ 𝑣, then the proof registers the thread’s
client-level atomic triple in the shared predicate MCS(𝑟, 𝑀). The registered atomic triple serves
as an obligation to commit the atomic triple. This obligation will be discharged by the upsert
operation adding (𝑘, (𝑣, 𝑡 ′)) to 𝐻 . The proof of search then uses the template-level specification of
search to conclude that it can collect the committed triple from the shared predicate after search
has returned.

                                                   9
,,                                                Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


  Relating the high-level and low-level specification of upsert is straightforward. However, the
proof of upsert also needs to do its part of the helping protocol by scanning over all the searches
that are currently registered in the shared predicate MCS(𝑟, 𝑀) and committing those that return
the copy of 𝑘 added by the upsert.
  In the remainder of this section we explain this helping proof in more detail.

4.2    Keeping Track of the Upsert History
Our thread-modular proof exploits the observation that the upsert history 𝐻 only increases over
time. Thus, assertions such as (𝑘, (𝑣, 𝑡)) ∈ 𝐻 , as used in our specification of search recency, are
stable under interference. This style of reasoning follows the classic idea of establishing lower
bounds on monotonically evolving state (see e.g. [Fahndrich and Leino 2003; Jensen and Birkedal
2012; Jones 1983]). We formalize this in Iris using user-defined ghost state.
   Iris expresses ownership of ghost state by the proposition 𝑎 𝛾 which asserts ownership of a piece
𝑎 of the ghost location 𝛾. It is the ghost analogue of the points-to predicate 𝑥 ↦→ 𝑣 in separation
logic, except that 𝑎 𝛾 asserts only that 𝛾 contains a value one of whose parts is 𝑎. This means
ghost state can be split and combined according to the rules of the camera, the algebraic structure
from which the values (like 𝑎) are drawn. Cameras generalize partial commutative monoids, which
are commonly used to give semantics to separation logics. A camera comes equipped with a set
𝑀 and a binary composition operation (·) : 𝑀 × 𝑀 → 𝑀 that form a commutative monoid. The
composition operation gives meaning to the separating conjunction of predicates that express
                                                                                        𝛾           𝛾
fragmental ownership of ghost state at a ghost location 𝛾 via the rule: 𝑎 𝛾 ∗ 𝑏 ⊣⊢ 𝑎 · 𝑏 . A
simple example of a camera is Set(𝑋 ), where 𝑋 is some set. Here, 𝑀 = 2𝑋 and (·) is set union.
Another example is the heap camera of standard separation logic, which consists of mappings from
heap locations to values that can be composed by disjoint set union.
   Iris also provides generic “functors” for constructing new cameras from existing ones. One
example that we will be using in our proofs is the authoritative camera Auth(𝑀), which can
be constructed from any other camera 𝑀. It is used to model situations where threads share an
authoritative element 𝑎 of 𝑀 via a representation predicate and individual threads own fragments
𝑏 of 𝑎. We denote an authoritative element by •𝑎 and a fragment by ◦𝑏. The composition •𝑎 · ◦𝑏
expresses ownership of the authoritative element 𝑎 and, in addition, ∃𝑐. 𝑎 = 𝑏 · 𝑐.
   For instance, we use the authoritative set camera Auth(Set(KS × (V × N))) to keep track of
                                                                        𝛾𝑠
the upsert history 𝐻 at a ghost location 𝛾𝑠 . The proposition •𝐻 states that 𝐻 is the current
authoritative version of the upsert history. This ghost resource is kept in the representation predicate
MCS(𝑟, 𝑡, 𝐻 ), which is shared among all threads operating on the data structure. The camera can
                                                                                                      𝛾𝑠
also express lower bounds 𝐻 ′ ⊆ 𝐻 on the authoritative set 𝐻 using propositions of the form ◦𝐻 ′ .
                              𝛾𝑠         𝛾𝑠
That is, the proposition •𝐻 ∗ ◦𝐻 ′ asserts ownership of the current upsert history 𝐻 and, in
addition, 𝐻 ′ ⊆ 𝐻 . We can then define the predicate SR(𝑘, 𝑣, 𝑡), which expresses that 𝐻¯ (𝑘) = (𝑣, 𝑡)
                                                                    𝛾𝑠
was true at some point in the past, as SR(𝑘, 𝑣, 𝑡) B ◦ {(𝑘, (𝑣, 𝑡))} .
  Iris allows frame-preserving updates of ghost state, denoted by the view shift connective ⇛. For
instance, the following rules capture some frame-preserving updates of authoritative sets:
      auth-set-upd
            𝐻 ⊆ 𝐻′                                                  auth-set-frag
                         𝛾
                             auth-set-snap                                𝛾           𝛾                    𝛾
                                                                              ∗ ◦𝐻′       ⇚⇛ ◦ (𝐻 ∪ 𝐻 ′)
            𝛾                      𝛾          𝛾             𝛾
       •𝐻       ⇛ •𝐻 ′        •𝐻       ⇛ •𝐻       ∗ ◦𝐻               ◦𝐻

The rule auth-set-upd is the only way to update the authoritative element, because, intuitively,
it must maintain the validity of all lower bounds. The authoritative set camera thus implicitly

                                                       10
Verifying Concurrent Multicopy Search Structures                                                                            ,,



                MCS(𝑟, 𝑀) B ∃ 𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) ∗ ∀𝑘. (𝑀 (𝑘), _) = 𝐻¯ (𝑘)
                                          𝛾𝑠
              MCS(𝑟, 𝑡, 𝐻 ) B • 𝐻              ∗ HInit(𝐻 ) ∗ HUnique(𝐻 ) ∗ HClock(𝑡, 𝐻 )

                                    ∗ Invtpl (𝑡, 𝐻 ) ∗ Prothelp (𝐻 )

                Prothelp (𝐻 ) B ∃ 𝑅. • 𝑅
                                                𝛾𝑟
                                                     ∗
                                                         ∗
                                                         tid ∈𝑅
                                                                  ∃ 𝑘 𝑣 𝑝 𝑡 0 Φ Tok. Proph(tid, _) ∗ State(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok)

State(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) B Pending(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ) ∨ Done(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok)

  Pending(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ) B AU(Φ) ∗ (∀𝑡 . (𝑘, (𝑣 𝑝 , 𝑡)) ∈ 𝐻 ⇒ 𝑡 < 𝑡 0 )

Done(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) B (Φ(𝑣 𝑝 ) ∨ Tok) ∗ (∃𝑡 . (𝑘, (𝑣 𝑝 , 𝑡)) ∈ 𝐻 ∧ 𝑡 ⩾ 𝑡 0 )


         Fig. 5. Definition of client-level representation predicate and invariants of helping protocol.


enforces the invariant that the upsert history can only increase. We use this rule to update the
authoritative version of the upsert history at the linearization point of upsert.
   The rule auth-set-snap allows us to take a “snapshot” of the current authoritative set. We use this
rule together with the rule auth-set-frag at the call to search in search to establish the thread-
                                                                                           𝛾𝑠
local precondition SR(𝑘, 𝑣 0′ , 𝑡 0′ ) of the specification (4) from the shared resource •𝐻 . To this end,
                                                                                                       𝛾𝑠
we choose (𝑣 ′ , 𝑡 ′ ) B 𝐻¯ (𝑘), which gives us 𝐻 = 𝐻 ∪ (𝑘, (𝑣 ′ , 𝑡 ′ )) and thus ◦ (𝑘, (𝑣 ′ , 𝑡 ′ ))
                                                                                       
                0 0                                                             0 0                       .   0 0

4.3    The Helping Protocol
Before we discuss the details of our encoding of the helping protocol in terms of Iris ghost state,
let us recall the basic structure of a proof of an atomic triple 𝑥 . 𝑃 𝑒 𝑣. 𝑄 . The proof proceeds
by proving a standard Hoare triple of the form ∀Φ. AU𝑥 .𝑃,𝑄 (Φ) 𝑒 𝑣 . Φ(𝑣) . Here, AU𝑥 .𝑃,𝑄 (Φ) is
                                                                      

the atomic update token, which gives us the right to use the resources in the precondition 𝑃 when
executing atomic instructions up to the linearization point. The token also records our obligation to
preserve 𝑃 up to the linearization point, where 𝑃 must be transformed to 𝑄 in one atomic step. This
step consumes the update token. The universally quantified proposition Φ can be thought of as the
precondition for the continuation of the client of the atomic triple. At the linearization point, when
the atomic update token is consumed, the corresponding proof rule produces Φ(𝑣) as a receipt that
the obligation has been fulfilled. This receipt is necessary to complete the proof of the Hoare triple.
Figure 5 shows a simplified definition of MCS(𝑟, 𝑀) and the invariant that encodes the helping
protocol.2 The definitions are implicitly parameterized by a proposition Invtpl (𝑟, 𝑡, 𝐻 ), which ab-
stracts from the resources needed for proving that a specific multicopy structure template satisfies
the template-level specifications. In particular, this invariant will store the resources needed to
represent the node-level
                 Ð          contents 𝐶𝑛 for each node 𝑛 ∈ 𝑁 . It also ties the 𝐶𝑛 to 𝐻 , capturing the
invariant 𝐻 ⊇ 𝑛 ∈𝑁 𝐶𝑛 .
   The predicate MCS(𝑟, 𝑀) contains the predicate MCS(𝑟, 𝑡, 𝐻 ), used in the template-level atomic
triples, and defines 𝑀 in terms of 𝐻¯ . The predicate MCS(𝑟, 𝑡, 𝐻 ) owns all (ghost) resources as-
                                                                                                    𝛾𝑠
sociated with the data structure. In particular, this predicate stores the ghost resource •𝐻 ,
2 For presentation purposes, the proof outline presented here abstracts from some technical details of the actual proof done

in Iris. For a more detailed presentation of our Iris development, we refer the interested reader to Appendix A.


                                                                   11
,,                                                            Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies

     D                    E
 1       𝑀. MCS(𝑟, 𝑀)
 2 let search 𝑟       𝑘 =
         
 3         AU(Φ)
 4       let tid = NewProph in
 5       let 𝑝 = NewProph in
           AU(Φ) ∗ Proph(tid, _) ∗ Proph(𝑝, 𝑣 𝑝 )
         
 6
           AU(Φ) ∗ Proph(tid, _) ∗ Proph(𝑝, 𝑣 𝑝 ) ∗ MCS(𝑟, 𝑡, 𝐻 0 )
         
 7
         n                                               𝛾𝑠                                          o
 8         AU(Φ) ∗ Proph(tid, _) ∗ Proph(𝑝, 𝑣 𝑝 ) ∗ ◦ 𝐻 0 ∗ (𝑣 0, 𝑡 0 ) = 𝐻¯0 (𝑘) ∗ SR(𝑘, 𝑣 0, 𝑡 0 )
 9       (* Case analysis on 𝑣 𝑝 = 𝑣 0 , 𝑣 𝑝 ≠ 𝑣 0 : only showing 𝑣 𝑝 ≠ 𝑣 0 *)
           AU(Φ) ∗ Proph(tid, _) ∗ Proph(𝑝, 𝑣 𝑝 ) ∗ (𝑣 0, 𝑡 0 ) = 𝐻¯0 (𝑘) ∗ SR(𝑘, 𝑣 0, 𝑡 0 ) ∗ 𝑣 𝑝 ≠𝑣 0 ∗ . . .
         
10
              . . . ∗ AU(Φ) ∗ Proph(tid, _) ∗ (∀𝑡 . (𝑘, (𝑣 𝑝 , 𝑡)) ∈ 𝐻 0 ⇒ 𝑡 < 𝑡 0 )
            
11
              . . . ∗ Proph(tid, _) ∗ Pending(𝐻 0, 𝑘, 𝑣𝑝, 𝑡 0, Φ) ∗ Tok
            
12
            n             𝛾𝑟
                                                                             o
13            . . . ∗ • 𝑅 ∗ tid ∉ 𝑅 ∗ State(𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) ∗ Tok
                                        𝛾𝑟                      𝛾𝑟
14       (* Ghost update: • 𝑅           ⇛ • 𝑅 ∪ {tid}         *)
         n                               𝛾𝑟                                             o
15         Proph(𝑝, 𝑣 𝑝 ) ∗ Tok ∗ ◦ {𝑡𝑖𝑑} ∗ SR(𝑘, 𝑣 0, 𝑡 0 ) ∗ 𝑣 𝑝 ≠𝑣 0 ∗ MCS(𝑟, 𝑡, 𝐻 )
16       let 𝑣 = search 𝑟 𝑘 in
         n                               𝛾𝑟                                                           o
17         Proph(𝑝, 𝑣 𝑝 ) ∗ Tok ∗ ◦ {𝑡𝑖𝑑} ∗ 𝑣 𝑝 ≠𝑣 0 ∗ MCS(𝑟, 𝑡, 𝐻 ) ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻
18       Resolve 𝑝 to 𝑣;
         n                  𝛾𝑟                                                        o
19         Tok ∗ ◦ {tid} ∗ 𝑣 ≠𝑣 0 ∗ MCS(𝑟, 𝑡, 𝐻 ) ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻
         n                       𝛾𝑟                                                                      o
20         · · · ∗ Tok ∗ ◦ {tid} ∗ 𝑣 ≠𝑣 0 ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ State(𝐻, 𝑘, 𝑣, 𝑡 0, Φ, Tok)
         n                       𝛾𝑟                                                             o
21         · · · ∗ Tok ∗ ◦ {tid} ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ Done(𝐻, 𝑘, 𝑣, 𝑡 0, Φ, Tok)
         n                       𝛾𝑟                                               o
22         · · · ∗ Tok ∗ ◦ {tid} ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ (Φ(𝑣) ∨ Tok)
         n                        𝛾𝑟                                                o
23         · · · ∗ Φ(𝑣) ∗ ◦ {tid} ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ (Φ(𝑣) ∨ Tok)
         n                        𝛾𝑟                               o
24         · · · ∗ Φ(𝑣) ∗ ◦ {tid} ∗ Done(𝐻, 𝑘, 𝑣, 𝑡 0, Φ, Tok)
           Φ(𝑣) ∗ MCS(𝑟, 𝑡, 𝐻 )
         
25
         n                           o
26         MCS(𝑟, 𝑀) ∗ 𝑀 (𝑘) = 𝑣
27       𝑣
         D                                E
28           𝑣 . MCS(𝑟, 𝑀) ∗ 𝑀 (𝑘) = 𝑣

                         Fig. 6. Outline for the proof of the client-level specification for search.


holding the authoritative version of the current upsert history, the abstract template-level invariant
Invtpl (𝑟, 𝑡, 𝐻 ), and the helping protocol predicate Prothelp (𝐻 ), described below. MCS(𝑟, 𝑡, 𝐻 ) also
states the three invariants HInit(𝐻 ), HUnique(𝑡, 𝐻 ), and HClock(𝐻 ) discussed earlier, which are
needed to prove the atomic triple of search.
                                                                          𝛾𝑟
   The helping protocol predicate Prothelp contains a registry • 𝑅 of search thread IDs that
require helping from upsert threads. For each thread ID tid in the registry, the shared state contains
Proph(tid, _) along with the state of tid, which is either Pending or Done. Pending captures an
uncommitted search, and Done describes the operation after it has been committed. Note that we
omit the annotation of the pre and postcondition from AU(Φ) as it always refers to the specification
of search in this proof.

                                                                     12
Verifying Concurrent Multicopy Search Structures                                                             ,,


    The proof outline for search is shown in Figure 12. After creating the two prophecies tid and
𝑝, the proof case-splits on whether the thread requires helping or not (line 9). We only consider
the helping case (i.e., (𝑣 0, 𝑡 0 ) = 𝐻¯0 (𝑘) ∧ 𝑣 0 ≠ 𝑣 𝑝 ), where 𝐻 0 is the initial upsert history and 𝑣 𝑝 the
prophesied return value). Here, the thread registers itself with the helping protocol by replacing 𝑅
with 𝑅 ∪{tid} using rule auth-set-upd (line 14). To do this, it first establishes Pending(𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ)
by transferring its obligation to linearize to the shared state, captured by the update token AU(Φ).
The condition ∀𝑡 .(𝑘, (𝑣 𝑝 , 𝑡)) ∈ 𝐻 0 ⇒ 𝑡 < 𝑡 0 follows from 𝑣 0 ≠ 𝑣 𝑝 , the definition of 𝐻¯0 , and the
invariant HUnique(𝐻 0 ). The thread also a creates a fresh non-duplicable token Tok that it will later
trade in for the receipt Φ(𝑣 𝑝 ).
    Let us briefly switch to the role played by the upsert that updates the logical value of 𝑘 to 𝑣 𝑝 at
some time 𝑡 ⩾ 𝑡 0 . When this upsert reaches its      linearization point, our proof uses rule auth-set-upd
to update the upsert history from 𝐻 to 𝐻 ∪ (𝑘, (𝑣 𝑝 , 𝑡)) , as required by the postcondition of (3),
 also increments the global clock from 𝑡 to 𝑡 + 1. We must then show that MCS(𝑟,
and                                                                                                𝑡 + 1, 𝐻 ∪
   (𝑘, (𝑣 𝑝 , 𝑡)) ) holds after these ghost updates, which requires us to prove Prothelp (𝐻 ∪ (𝑘, (𝑣 𝑝 , 𝑡)) )
assuming Prothelp (𝐻 ) was true before the update. In particular, any search thread that was in a
Pending state State(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) and thus waiting to be helped by this upsert needs to be
committed. It can do this because the postcondition of these triples are satisfied after 𝐻 has been
updated. The proof then transfers      the receipts Φ(𝑣 𝑝 ) back to the shared representation predicate,
yielding new states Done(𝐻 ∪ (𝑘, (𝑣 𝑝 , 𝑡)) , 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) for each of these threads.
    Coming back to the proof of the search that needed helping, after the call to search on line 16,
we know from the postcondition of (4) that we must have (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 for some 𝑡 ′ such that
𝑡 ′ ⩾ 𝑡 0 where 𝐻 is the new upsert history at this point. Moreover, after resolving the prophecy on
line 18 we know 𝑣 𝑝 = 𝑣 and therefore (𝑘, (𝑣 𝑝 , 𝑡 ′)) ∈ 𝐻 . From the invariant, we can then conclude
that the thread must be in a Done state. Since the thread owns the unique token Tok, it trades it in
to obtain Φ(𝑣), which lets it complete the proof of its atomic triple specification (4).

5   THE LSM DAG TEMPLATE
This section presents a general template for multicopy structures that generalizes the LSM (log-
structured merge) tree discussed in §2.2. We prove linearizability of the template by verifying
that all operations satisfy the template-level atomic triples (§3.3). The template and the proof
parameterize over the implementation of the single-copy data structures used at the node-level.
Instantiating the template for a specific implementation involves only sequential reasoning about
the implementation-specific node-level operations.
    We split the template into two parts. The first part is a template for search and upsert that works
on general multicopy structures, i.e., arbitrary DAGs with locally disjoint edgesets. The second
part (discussed in §7) is a template for a maintenance operation that generalizes the compaction
mechanism found in existing list-based LSM tree implementations to tree-like multicopy structures.
    Figure 7 shows the code of the template for the core multicopy operations. The operations
search and upsert closely follow the high-level description of these operations on the LSM tree
(§2.2). The operations are defined in terms of implementation-specific helper functions findNext,
addContents, and inContents.
    The search operation calls the recursive function traverse on the root node. traverse 𝑟 𝑛 𝑘
first locks the node 𝑛 and uses the helper function inContents 𝑟 𝑛 𝑘 to check if a copy of key 𝑘
is contained in 𝑛. If a copy of 𝑘 is found, then its associated value 𝑣 is returned after unlocking
𝑛. Otherwise, traverse uses the helper function findNext to determine the unique successor 𝑛 ′
of the given node 𝑛 and query key 𝑘 (i.e., the node 𝑛 ′ satisfying 𝑘 ∈ es(𝑛, 𝑛 ′)). If such a successor
𝑛 ′ exists, traverse recurses on 𝑛 ′. Otherwise, traverse concludes that there is no copy of 𝑘 in

                                                      13
,,                                                     Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


      1 let rec traverse 𝑟    𝑛 𝑘 =                           13 let rec upsert 𝑟   𝑘 𝑣 =
      2    lockNode 𝑛;                                        14   lockNode 𝑟 ;
      3    match inContents 𝑟 𝑛 𝑘 with                        15   let res = addContents 𝑟 𝑘 𝑣 in
      4    | Some 𝑣 -> unlockNode 𝑛; 𝑣                        16   if res then
      5    | None ->                                          17     unlockNode 𝑟
      6      match findNext 𝑟 𝑛 𝑘 with                        18   else begin
      7      | Some 𝑛 ′ ->                                    19     unlockNode 𝑟 ;
      8        unlockNode 𝑛;                                  20     upsert 𝑟 𝑘 𝑣
      9        traverse 𝑟 𝑛 ′ 𝑘                               21   end
     10      | None -> unlockNode 𝑛; □
     11
     12 let search 𝑟   𝑘 = traverse 𝑟 𝑟 𝑘

Fig. 7. The general template for multicopy operations search and upsert. The template can be instantiated by
providing implementations of helper functions inContents, findNext, and addContents. inContents 𝑟 𝑛 𝑘
returns Some 𝑣 if (𝑣, 𝑡 ′ ) = 𝐶𝑛 (𝑘) for some 𝑡 ′ , and None otherwise. findNext 𝑟 𝑛 𝑘 returns Some 𝑛 ′ if 𝑛 ′ is the
unique node such that 𝑘 ∈ es(𝑛, 𝑛 ′ ), and None otherwise. addContents 𝑟 𝑘 𝑣 updates the contents of 𝑟 by
setting the value associated with key 𝑘 to 𝑣. The return value of addContents is a Boolean which indicates
whether the insertion was successful (e.g., if 𝑟 is full, insertion may fail leaving 𝑟 ’s contents unchanged).


the data structure and returns □. Note that this algorithm uses fine-grained concurrency, as the
thread executing the search holds at most one lock at any point (and no locks at the points when
traverse is called recursively).
   The upsert 𝑟 𝑘 𝑣 operation locks the root node and adds a new copy of the key 𝑘 with value
𝑣 to the contents of the root node using addContents. addContents 𝑟 𝑘 𝑣 adds the pair (𝑘, 𝑣) to
the root node when it succeeds. upsert terminates by unlocking the root node. The addContents
function may however fail if the root node is full. In this case upsert calls itself recursively3 .

6         VERIFYING THE TEMPLATE
We next discuss the correctness proof of the template operations. We will focus on the high-level
proof ideas and key invariants and defer the detailed proof outline and encoding of the invariants
in Iris to Appendix A.

6.1 High-Level Proof Outline
   Proof of search. We start with the proof of search. Recall that search recency is the affirmation
that if 𝑡 0 is the logical timestamp of 𝑘 at the point when search 𝑟 𝑘 is invoked, then the operation
returns 𝑣 such that (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 and 𝑡 ′ ⩾ 𝑡 0 . Since the value 𝑣 of 𝑘 retrieved by search comes
from some node in the structure, we must examine the relationship between the upsert history 𝐻
of the data structure and the physical contents 𝐶𝑛 of the nodes 𝑛 visited as the search progresses.
We do this by identifying the main invariants needed for proving search recency for arbitrary
multicopy structures.
   We refer to the spatial ordering of the copies (𝑘, (𝑣, 𝑡)) stored in a multicopy structure as the
ordering in which those copies are reached when traversing the data structure graph starting from
the root node. Our first observation is that the spatial ordering is consistent with the temporal
ordering in which the copies have been upserted. We referred to this property as the time-ordering
invariant in our library analogy in §2.1: the farther from the root a search is, the older the copies it
3 For simplicity of presentation, we assume that a separate maintenance thread flushes the root if it is full to ensure that

upserts eventually make progress.


                                                            14
Verifying Concurrent Multicopy Search Structures                                                          ,,


finds are. Therefore, if a search 𝑟 𝑘 traverses the data structure without interference from other
threads and returns the first copy of 𝑘 that it finds, then it is guaranteed to return the logical value
of 𝑘 at the start of the search.
   We formalize this observation in terms of the contents-in-reach of a node. The contents-in-reach
of a node 𝑛 is the partial function 𝐶 ir (𝑛) : KS ⇀ V × N defined recursively over the graph of the
multicopy structure as follows:
                                         𝐶 (𝑘)             if 𝑘 ∈ dom(𝐶𝑛 )
                                          𝑛
                                         
                                         
                                         
                           𝐶 ir (𝑛) (𝑘) B 𝐶 ir (𝑛 ′) (𝑘)    else if ∃𝑛 ′ . 𝑘 ∈ es(𝑛, 𝑛 ′)                (5)
                                         
                                         ⊥
                                         
                                                            otherwise
                                         
 Note that 𝐶 ir (𝑛) is well-defined because the graph is acyclic and the edgesets labeling the outgoing
edges of every node 𝑛 are disjoint. We further define ts(𝐶 ir (𝑛) (𝑘)) = 𝑡 if 𝐶 ir (𝑛) (𝑘) = (_, 𝑡) and
ts(𝐶 ir (𝑛) (𝑘)) = 0 if 𝑘 ∉ dom(𝐶 ir (𝑛)).
    For example, in the multicopy structure depicted in Figure 3, we have 𝐶 ir (𝑟 ) = {𝑘 1 ↣ (□, 6), 𝑘 2 ↣
(𝑑, 7), 𝑘 3 ↣ (𝑐, 4)} and 𝐶 ir (𝑛 3 ) = 𝐶𝑛3 .
    The observation that interference-free searches will find the current logical timestamp of their
query key is then captured by the following invariant:
Invariant 1 The logical contents of the multicopy structure is the contents-in-reach of its root
node: 𝐻¯ = 𝐶 ir (𝑟 ).
    In order to account for concurrent threads interfering with the search, we prove the condition
𝑡 0 ≤ 𝑡 ′ for the timestamp 𝑡 ′ associated with the value returned by the search. Intuitively, this is
true because the contents-in-reach of a node 𝑛 can be affected only by upserts or maintenance
operations, both of which only increase the timestamps associated with every key of any given
node: upserts insert new copies into the root node and maintenance operations move recent copies
down in the structure, possibly replacing older copies. This observation is formally captured by the
following invariant:
Invariant 2 The contents-in-reach of every node only increases. That is, for every node 𝑛 and key
𝑘, if ts(𝐶 ir (𝑛) (𝑘)) = 𝑡 at some point in time and ts(𝐶 ir (𝑛) (𝑘)) = 𝑡 ′ at any later point in time, then
𝑡 ≤ 𝑡 ′.
    Finally, in order to prove the condition (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 of search recency, we need one additional
property:
Invariant 3 All copies present in the multicopy structure have been upserted at some point in the
past. That is, for all nodes 𝑛, 𝐶𝑛 ⊆ 𝐻 .
    Now let us consider an execution of search on a operation key 𝑘. In addition to the above three
general invariants, we need an inductive invariant for the traversal performed by the search: we
require as a precondition for traverse 𝑟 𝑛 𝑘 that ts(𝐶 ir (𝑛) (𝑘)) ⩾ 𝑡 0 where 𝑡 0 is the timestamp of
the logical value 𝑣 0 of 𝑘 at the point when search was invoked. To see that this property holds
initially for the call to traverse 𝑟 𝑟 𝑘 in search, let 𝐻¯0 be the logical contents at the time point
when search was invoked. The precondition SR(𝑘, 𝑣 0, 𝑡 0 ) implies ts(𝐻¯0 (𝑘)) ⩾ 𝑡 0 , which, combined
with Invariant 1 implies that we must have had ts(𝐶 ir (𝑟 ) (𝑘)) ⩾ 𝑡 0 at this point. Since ts(𝐶 ir (𝑟 ) (𝑘))
only increases over time because of Invariant 2, we can conclude that ts(𝐶 ir (𝑟 ) (𝑘)) ⩾ 𝑡 0 when
traverse is called. We next show that the traversal invariant is maintained by traverse and is
sufficient to prove search recency.
    Consider a call to traverse 𝑟 𝑛 𝑘 such that ts(𝐶 ir (𝑛) (𝑘)) ⩾ 𝑡 0 holds initially. We must show
that the call returns 𝑣 such that (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 and 𝑡 ′ ⩾ 𝑡 0 for some 𝑡 ′. We know that the call to
inContents on line 3 returns either Some 𝑣 such that (𝑣, 𝑡 ′) = 𝐶𝑛 (𝑘) or None if 𝐶𝑛 (𝑘) = ⊥. Let us

                                                       15
,,                                               Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


first consider the case where inContents returns Some 𝑣. In this case, traverse returns 𝑣 on line 4.
By definition of 𝐶 ir (𝑛) we have 𝐶 ir (𝑛) (𝑘) = 𝐶𝑛 (𝑘). Hence, we have ts(𝐶 ir (𝑛) (𝑘)) = 𝑡 ′ and the
precondition ts(𝐶 ir (𝑛) (𝑘)) ⩾ 𝑡 0 , together with Invariant 2, implies 𝑡 ′ ⩾ 𝑡 0 . Moreover, Invariant 3
guarantees (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 .
   Now consider the case where inContents returns None. Here, 𝑘 ∉ dom 𝐶𝑛 (𝑘), indicating that
no copy has been found for 𝑘 in 𝑛. In this case, traverse calls findNext to obtain the successor
node of 𝑛 and 𝑘. In the case where the successor 𝑛 ′ exists (line 7), we know that 𝑘 ∈ es(𝑛, 𝑛 ′)
must hold. Hence, by definition of contents-in-reach we must have 𝐶 ir (𝑛) (𝑘) = 𝐶 ir (𝑛 ′) (𝑘). From
ts𝐶 ir (𝑛) (𝑘) ⩾ 𝑡 0 and Invariant 2, we can then conclude ts(𝐶 ir (𝑛 ′) (𝑘)) ⩾ 𝑡 0 , i.e. that the precondition
for the recursive call to traverse on line 9 is satisfied and search recency follows by induction.
   On the other hand, if 𝑛 does not have any next node, then traverse returns □ (line 10), indicating
that 𝑘 has not yet been upserted at all so far (i.e., has never appeared in the structure). In this
case, by definition of contents-in-reach we must have 𝐶 ir (𝑛) (𝑘) = ⊥. Invariant 2 then guarantees
ts(𝐶 ir 𝑛𝑘) = 0 = 𝑡 0 . The invariant HInit(𝐻 ) on the upsert history then gives us (𝑘, (□, 0)) ∈ 𝐻 .
Hence, search recency holds in this case for 𝑡 ′ = 0.

   Proof of upsert. In order to prove the logically atomic specification (11) of upsert, we must
identify an atomic step where the clock 𝑡 is incremented and the upsert history 𝐻 is updated.
Intuitively, this atomic step is when the lock on the root node is released (line 17 in Figure 7) after
addContents succeeds. Note that in this case addContents changes the contents of the root node
from 𝐶𝑟 to 𝐶𝑟′ = 𝐶𝑟 [𝑘 ↣ (𝑣, 𝑡)]. Hence, in the proof we need to update the ghost state for the
upsert history from 𝐻 to 𝐻 ′ = 𝐻 ∪ {(𝑘, (𝑣, 𝑡))}, reflecting that a new copy of 𝑘 has been upserted.
It then remains to show that the three key high-level invariants of multicopy structures identified
above are preserved by these updates.
   First, observe that Invariant 3, which states ∀𝑛. 𝐶𝑛 ⊆ 𝐻 , is trivially maintained: only 𝐶𝑟 is affected
by the upsert and the new copy (𝑘, (𝑣, 𝑡)) is included in 𝐻 ′. Similarly, we can easily show that
Invariant 2 is maintained: 𝐶 ir (𝑛) remains the same for all nodes 𝑛 ≠ 𝑟 and for the root node it
increases, provided Invariant 1 is also maintained.
   Thus, the interesting case is Invariant 1. Proving that this invariant is maintained amounts to
showing that 𝐻¯ ′ (𝑘) = (𝑣, 𝑡). This step critically relies on the following additional observation:
Invariant 4 All timestamps in 𝐻 are smaller than the current time of the global clock 𝑡.
This invariant implies that 𝐻¯ ′ (𝑘) = max(𝐻¯ (𝑘), (𝑣, 𝑡)) = (𝑣, 𝑡), which proves the desired property.
We note that Invariant 4 is maintained because the global clock is incremented when 𝐻 is updated
to 𝐻 ′, and, as we describe below, while 𝑟 is locked.
   In the remainder of this section, we discuss the key technical issue when formalizing the above
proof in a separation logic like Iris.

6.2   Iris Invariant
The Iris proof must capture the key invariants identified in the proof outline given above in terms
of appropriate ghost state constructions. We start by addressing the key technical issue that arises
when formalizing the above proof in a separation logic like Iris: contents-in-reach is a recursive
function defined over an arbitrary DAG of unbounded size. This makes it difficult to obtain a simple
local proof that involves reasoning only about the bounded number of modified nodes in the graph.
The recursive and global nature of contents-in-reach mean that modifying even a single edge in
the graph can potentially change the contents-in-reach of an unbounded number of nodes (for
example, deleting an edge (𝑛 1, 𝑛 2 ) can change 𝐶 ir (𝑛) for all 𝑛 that can reach 𝑛 1 ). A straightforward
attempt to prove that a template algorithm preserves Invariant 2 would thus need to reason about

                                                      16
Verifying Concurrent Multicopy Search Structures                                                   ,,


the entire graph after every modification (for example, by performing an explicit induction over
the full graph). We solve this challenge using the flow framework [Krishna et al. 2020b].
   Encoding Contents-in-Reach using Flows. The flow framework enables separation-logic-style
reasoning about recursive functions on graphs. Certain restrictions apply. The function must be
of the form fl : 𝑁 → 𝑀 where 𝑁 is the set of nodes of the graph and (𝑀, +, 0) is a commutative
cancellative monoid, called the flow domain. Further, fl must satisfy the flow equation:
                                                    ∑︁
                           ∀𝑛 ∈ 𝑁 . fl(𝑛) = in(𝑛) +      e(𝑛 ′, 𝑛) (fl(𝑛 ′))             (FlowEqn)
                                                        𝑛′ ∈𝑁

Intuitively, this equation states that fl can be computed by assigning every node an initial value
according to the inflow function in : 𝑁 → 𝑀 and then propagating these values along the edges
of the graph using the edge function e : 𝑁 × 𝑁 → 𝑀 → 𝑀 to reach a fixpoint. At each node 𝑛,
the values propagated from predecessor nodes 𝑛 ′ are aggregated using the monoid operation +. A
function fl that satisfies the flow equation is called a flow and a graph equipped with a flow is a
flow graph. The flow framework then enables us to reason compositionally about invariants of flow
graphs expressed as node-local conditions that depend on a node’s flow.
   If we can define the contents-in-reach in terms of a flow, then we can use the notion of a flow
interface to prove locally that an update to the graph does not change the flow of any nodes
outside the modified region. The flow interface of a region consists of its outflow and inflow,
maps that intuitively capture the contribution of this region to the flow of the rest of the world
and the contribution of the outside world to this region’s flow, respectively. If the interface of a
modified region is preserved, then the framework guarantees that the flow of the rest of the graph
is unchanged. Thus, our proofs need to prove only that Invariant 2 is preserved for a bounded set
of affected nodes.
   Technically, this kind of reasoning is enabled by the separation algebra structure of flow graphs
(in particular the definition of flow graph composition), which extends the composition of partial
graphs in standard separation logic so that the frame rule also preserves flow values of nodes in
the frame. Instead of performing an explicit induction over the entire graph structure to prove that
contents-in-reach values continue to satisfy desired invariants, the necessary induction is hidden
away inside the definition of flow graph composition (for more details see [Krishna et al. 2020b]).
Note that since search does not modify the multicopy structure, it trivially maintains the flow
interface of the nodes it operates on, and hence any flow-based invariants.
   Equation (5) defines contents-in-reach in a bottom-up fashion, starting from the leaves of the
multicopy structure graph. That is, the computation proceeds backwards with respect to the
direction of the graph’s edges. This makes a direct encoding of contents-in-reach in terms of a flow
difficult because the flow equation describes computations that proceed in the forward direction.
   We side-step this problem by tracking auxiliary ghost information in the data structure invariant
for each node 𝑛 in the form of a function 𝑄𝑛 : KS ⇀ V × N. If these ghost values satisfy
                                       (
                                         𝐶 ir (𝑛 ′) (𝑘) if ∃𝑛 ′ . 𝑘 ∈ es(𝑛, 𝑛 ′)
                             𝑄𝑛 = 𝜆𝑘.                                                             (6)
                                         ⊥              otherwise
and we additionally define
                              𝐵𝑛 B 𝜆𝑘. (𝑘 ∈ dom(𝐶𝑛 (𝑘)) ? 𝐶𝑛 (𝑘) : 𝑄𝑛 (𝑘))
then 𝐶 ir (𝑛) = 𝐵𝑛 . The idea is that each node stores 𝑄𝑛 so that node-local invariants can use it to
talk about 𝐶 ir (𝑛). We then use a flow to propagate the purported values 𝑄𝑛 forward in the graph to
ensure that they indeed satisfy (6). Note that while an upsert or maintenance operations on 𝑛 may

                                                   17
,,                                              Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


change 𝐵𝑛 , it preserves 𝑄𝑛 . That is, operations do not affect the contents-in-reach of downstream
nodes, allowing local reasoning about the modification of the contents of 𝑛.
  In what follows, let us fix a multicopy structure over nodes 𝑁 and some valuations of the partial
functions 𝑄𝑛 . The flow domain 𝑀 for our encoding of contents-in-reach consists of multisets of
key/value-timestamp pairs 𝑀 B KS × (V × N) → N with multiset union as the monoid operation.
The edge function induced by the multicopy structure is defined as follows:
                    e(𝑛, 𝑛 ′) (_) B 𝜒 ({(𝑘, 𝑄𝑛 (𝑘)) | 𝑘 ∈ es(𝑛, 𝑛 ′) ∧ 𝑘 ∈ dom(𝑄𝑛 )})                      (7)
Here, 𝜒 takes a set to its corresponding multiset. Additionally, we let the function in map every
node to the empty multiset. With the definitions of e and in in place, there exists a unique flow fl
that satisfies (FlowEqn). Now, if every node 𝑛 in the resulting flow graph satisfies the following
two predicates
                            𝜙 1 (𝑛) B ∀𝑘. 𝑄𝑛 (𝑘) = ⊥ ∨ (∃𝑛 ′ . 𝑘 ∈ es(𝑛, 𝑛 ′))                             (8)
                            𝜙 2 (𝑛) B ∀𝑘 𝑝. fl(𝑛) (𝑘, 𝑝) > 0 ⇒ 𝐵𝑛 (𝑘) = 𝑝                                  (9)
then 𝐵𝑛 = 𝐶 ir (𝑛). Note that the predicates 𝜙 1 and 𝜙 2 depend only on 𝑛’s own flow and its local
ghost state (i.e., 𝑄𝑛 , 𝐶𝑛 and the outgoing edgesets es(𝑛, _)).
  Encoding the Invariants in Iris. We can now define the template-specific invariant Invtpl (𝑟, 𝑡, 𝐻 ) for
the LSM DAG template, which is assumed by the representation predicate MCS(Invtpl , Prot) (𝑟, 𝑡, 𝐻 )
defined in Figure 5. We denote this invariant by InvLSM and it is defined as follows:

          InvLSM (𝑟, 𝑡, 𝐻 ) B ∃𝑁 . G(𝑟, 𝑡, 𝐻, 𝑁 ) ∗
                                                      ∗
                                                      𝑛 ∈𝑁
                                                             ∃𝑏𝑛 𝐶𝑛 𝑄𝑛 . L(𝑏𝑛 , 𝑛, NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ))
                                                                     ∗ NS (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐻 )
The existentially quantified variable 𝑁 denotes the set of nodes of the multicopy structure. The
invariant itself consists of two parts. The predicate G(𝑟, 𝑡, 𝐻, 𝑁 ) states certain invariants about
its parameters and contains global ghost resources storing the values 𝑡 and 𝑁 . The second part is
an iterated separating conjunction stating ownership of the node-local resources associated with
every node 𝑛 ∈ 𝑁 .
   The resources associated with each node 𝑛 are split between two predicates. The predicate
NS (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐻 ) holds those resources associated with 𝑛 that can be accessed by any thread
operating on the data structure regardless of whether 𝑛 is locked or not. In particular, it contains
the two predicates 𝜙 1 (𝑛) and 𝜙 2 (𝑛) needed for our encoding of contents-in-reach. The second
predicate NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) contains all resources that are accessible only to a thread that currently
holds the lock on 𝑛. Ownership of node-local ghost state such as 𝑄𝑛 is shared between the two
predicates. This ensures that a thread may update the values of these resources only when it holds
𝑛’s lock. Moreover, every thread can assume that the constraints imposed on these values by NS
are true, even at times when the thread does not hold the lock.
   NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) includes node(𝑟, 𝑛, es(𝑛, ·), val(𝐶𝑛 )), which is a predicate that encapsulates all
resources specific to the implementation of the node-specific data structure abstracted by node
𝑛. In particular, this predicate owns the resources associated with the physical representation of
the data structure and ties them to the abstract ghost state representing the high-level multicopy
structure: the node’s physical contents val(𝐶𝑛 ) (i.e., 𝐶𝑛 without timestamps) and the edgesets of its
outgoing edges es(𝑛, ·). Our template proof is parametric in the definition of node and depends
only on the following two assumptions that each implementation used to instantiate the template
must satisfy. First, we require that node is not duplicable:
                             node(𝑟, 𝑛, es, 𝑉𝑛 ) ∗ node(𝑟 ′, 𝑛, es ′, 𝑉𝑛′) ⊢ False

                                                      18
Verifying Concurrent Multicopy Search Structures                                                           ,,


 1  𝑏 𝑅. L(𝑏, 𝑛, 𝑅) lockNode 𝑛 L(true, 𝑛, 𝑅) ∗ 𝑅
 2  𝑅. L(true, 𝑛, 𝑅) ∗ 𝑅 unlockNode 𝑛 L(false, 𝑛, 𝑅)
 3 node(𝑟, 𝑛, es, 𝑉𝑛 ) inContents 𝑛 𝑘 𝑥 . node(𝑟, 𝑛, es, 𝑉𝑛 ) ∗ 𝑥 = (𝑘 ∈ dom(𝑉𝑛 ) ? Some(𝑉𝑛 (𝑘)) : None)
                                      
                                                                      ′         ′           ′
 4 node(𝑟, 𝑛, es, 𝑉𝑛 ) findNext 𝑛 𝑘 𝑥 . node(𝑟, 𝑛, es, 𝑉𝑛 ) ∗ 𝑥 = ∃𝑛 . 𝑘 ∈ es(𝑛 ) ? Some(𝑛 ) : None
                                                                                                  
                                                               ′    ′
 5 node(𝑟, 𝑟, es, 𝑉𝑟 ) addContents 𝑟 𝑘 𝑣 𝑏. node(𝑟, 𝑟, es, 𝑉𝑟 ) ∗ 𝑉𝑟 = (𝑏 ? 𝑉𝑟 [𝑘 ↣ 𝑣] : 𝑉𝑟 )
                                        


                    Fig. 8. Specifications of helper functions used by search and upsert.



Moreover, node must guarantee disjoint edgesets:

                         node(𝑟, 𝑛, es, 𝑉𝑛 ) ⊢ ∀𝑛 1 𝑛 2 . 𝑛 1 = 𝑛 2 ∨ es(𝑛 1 ) ∩ es(𝑛 2 ) = ∅

  The predicate L(𝑏, 𝑛, 𝑅𝑛 ) captures the abstract state of 𝑛’s lock and is used to specify the protocol
providing exclusive access to the resource 𝑅𝑛 protected by the lock via the helper functions lockNode
and unlockNode. The Boolean 𝑏 indicates whether the lock is (un)locked. The specifications of
the helper functions used by search and upsert, given in terms of the predicates L(𝑏, 𝑛, 𝑅𝑛 ) and
node(𝑟, 𝑛, es, 𝑉𝑛 ) are shown in Figure 8. We discuss further details in Appendix A.

7     MULTICOPY MAINTENANCE OPERATIONS
We next show that we can extend our multicopy structure template in §5 with a generic maintenance
operation without substantially increasing the proof complexity. The basic idea of our proofs here
is that for every timestamped copy of key 𝑘, denoted as the pair (𝑘, (𝑣, 𝑡)), every maintenance
operation either does not change the distance of (𝑘, (𝑣, 𝑡)) to the root or increases it while preserving
an edgeset-guided path to (𝑘, (𝑣, 𝑡)). Using these two facts, we can prove that all the structure
invariants are also preserved.

7.1    Maintenance template
For the maintenance template, we consider a generalization of the compaction operation found in
LSM tree implementations such as LevelDB [Google 2021] and Apache Cassandra [Apache Software
Foundation 2021; Jonathan Ellis 2011]. While those implementations work on lists for the high-level
multicopy structure, our maintenance template supports arbitrary tree-like multicopy structures.
The code is shown in Figure 9. The template uses the helper function atCapacity 𝑟 𝑛 to test
whether the size of 𝑛 (i.e., the number of non-⊥ entries in 𝑛’s contents) exceeds an implementation-
specific threshold. If not, then the operation simply terminates. In case 𝑛 is at capacity, the function
chooseNext is used to determine the node to which the contents of 𝑛 can be merged. If the contents
of 𝑛 can be merged to successor 𝑚 of 𝑛, then chooseNext returns Some 𝑚. In case no such successor
exists, then it returns None. If chooseNext returns Some 𝑚, then the contents of 𝑛 are merged to 𝑚.
By merge, we mean that some copies of keys are transferred from 𝑛 to 𝑚, possibly replacing older
copies in 𝑚. The merge is performed by the helper function mergeContents. It must ensure that
all keys 𝑘 merged from 𝐶𝑛 to 𝐶𝑚 satisfy 𝑘 ∈ es(𝑛, 𝑚).
   On the other hand, if chooseNext returns None, then a new node is allocated using the function
allocNode. The new node is then added to the data structure using the helper function insertNode.
Here, the new edgeset es(𝑛, 𝑚) must be disjoint from all edgesets for the other successors 𝑚 ′ of 𝑛.
Afterwards, the contents of 𝑛 are merged to 𝑚 as before. Note that the maintenance template never
removes nodes from the structure. In practice, the depth of the structure is bounded by letting the
capacity of nodes grow exponentially with the depth. The right hand side of Figure 9 shows the
intermediate states of a potential execution of the compact operation.

                                                         19
,,                                               Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


 1 let rec compact 𝑟   𝑛 =
                                                     𝑘1       7              𝑘1        3                    𝑘1       2
 2    lockNode 𝑛;                                    𝑘2       5    KS        𝑘2        ⊥      {𝑘 1, 𝑘 2 }   𝑘2       1
 3    if atCapacity 𝑟 𝑛 then begin                   𝑘3       6              𝑘3        ⊥                    𝑘3       ⊥
                                                                                                                     ⊥
 4      match chooseNext 𝑟 𝑛 with                    𝑘4       8              𝑘4        4                    𝑘4

 5      | Some 𝑚 ->                                       𝑛

 6        lockNode 𝑚;
 7        mergeContents 𝑟 𝑛 𝑚;                       𝑘1       ⊥               𝑘1       7                    𝑘1       2
                                                              ⊥    KS                         {𝑘 1, 𝑘 2 }
          unlockNode 𝑛;
                                                     𝑘2                       𝑘2       5                    𝑘2       1
 8
                                                     𝑘3       ⊥               𝑘3       6                    𝑘3       ⊥
 9        unlockNode 𝑚;                              𝑘4       ⊥               𝑘4       8                    𝑘4       ⊥
10        compact 𝑟 𝑚                                     𝑛                       𝑚
11      | None ->
12        let 𝑚 = allocNode () in                    𝑘1       ⊥              𝑘1        7                    𝑘1       2
13        insertNode 𝑟 𝑛 𝑚;                          𝑘2       ⊥    KS        𝑘2        5      {𝑘 1, 𝑘 2 }   𝑘2       1
14        mergeContents 𝑟 𝑛 𝑚;                       𝑘3       ⊥              𝑘3        ⊥                    𝑘3       ⊥
                                                              ⊥                        ⊥                             ⊥
          unlockNode 𝑛;
                                                     𝑘4                      𝑘4                             𝑘4
15
          unlockNode 𝑚;
                                                                                   𝑛
16                                                                                         {𝑘 3, 𝑘 4 }
                                                                                                                     ⊥
          compact 𝑟 𝑚
                                                                                                            𝑘1
17
                                                                                                            𝑘2       ⊥
18    end                                                                                                   𝑘3       6
19    else                                                                                                  𝑘4       8
20      unlock 𝑛                                                                                                 𝑚


Fig. 9. Maintenance template for tree-like multicopy structures. The template can be instantiated by providing
implementations of helper functions atCapacity, chooseNext, mergeContents, allocNode, and insertNode.
atCapacity 𝑟 𝑛 returns a Boolean value indicating whether node 𝑛 has reached its capacity. The helper func-
tion chooseNext 𝑟 𝑛 returns Some 𝑚 if there exists a successor 𝑚 of 𝑛 in the data structure into which 𝑛 should
be compacted, and None in case 𝑛 cannot be compacted into any of its successors. mergeContents 𝑟 𝑛 𝑚 (par-
tially) merges the contents of 𝑛 into 𝑚. Finally, allocNode is used to allocate a new node and insertNode 𝑟 𝑛 𝑚
inserts node 𝑚 into the data structure as a successor of 𝑛. The right hand side shows a possible execution of
compact. Edges are labeled with their edgesets. The nodes 𝑛 and 𝑚 in each iteration are marked in blue. For
simplicity, we here assume that the values are identical to their associated timestamps and only show the
timestamps.


7.2    High-level proof of compact
The verification framework presented in §3 can be easily extended to accommodate any maintenance
operation on multicopy structures that does not change the data structure’s abstract state. That is,
we need to prove that compact satisfies the following atomic triple:
                             𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) compact 𝑟        MCS(𝑟, 𝑡, 𝐻 )
This specification says that compact logically takes effect in a single atomic step, and at this step
the abstract state of the data structure does not change. We prove that compact satisfies this
specification relative to the specifications of the implementation-specific helper functions shown in
Figure 10. The postcondition of mergeContents is given with respect to an (existentially quantified)
set of keys 𝐾 that are merged from 𝑉𝑛 to 𝑉𝑚 , resulting in new content sets 𝑉𝑛′ and 𝑉𝑚′ . The new
contents are determined by the functions mergeLeft and mergeRight which are defined as follows:
               mergeLeft (𝐾, 𝑉𝑛 , Es, 𝑉𝑚 ) B 𝜆𝑘. (𝑘 ∈ 𝐾 ∩ dom(𝑉𝑛 ) ∩ Es ? ⊥ : 𝑉𝑛 (𝑘))
             mergeRight (𝐾, 𝑉𝑛 , Es, 𝑉𝑚 ) B 𝜆𝑘. (𝑘 ∈ 𝐾 ∩ dom(𝑉𝑛 ) ∩ Es ? 𝑉𝑛 (𝑘) : 𝑉𝑚 (𝑘))



                                                      20
Verifying Concurrent Multicopy Search Structures                                                                                                                                                            ,,


                                                     atCapacity 𝑟 𝑛 𝑏. node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 )
                                                                   
 1        node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 )
 2
      
 3  node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 )
 4 chooseNext 𝑟      𝑛
 5 𝑣 . node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 ) ∗ (𝑣 = Some(𝑚) ∗ es𝑛 (𝑚) ≠ ∅ ∨ 𝑣 = None ∗ needsNewNode(𝑟, 𝑛, es𝑛 , 𝑉𝑛 ))
  

 6
                       allocNode 𝑟                     𝑚. node(𝑟, 𝑚, (𝜆𝑛 ′ . ∅), ∅)
                                                     
 7        True
 8
     node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 ) ∗ needsNewNode(𝑟, 𝑛, es𝑛 , 𝑉𝑛 ) ∗ node(𝑟, 𝑚, (𝜆𝑛 ′ . ∅), ∅)
      
 9
10 insertNode 𝑟 𝑛 𝑚
                 ′                      ′              ′                ′             ′
11 node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 ) ∗ node(𝑟, 𝑚, (𝜆𝑛 . ∅), ∅) ∗ es𝑛 = es𝑛 [𝑚 ↣ es𝑛 (𝑚)] ∗ es𝑛 (𝑚) ≠ ∅
12
      
13        node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 ) ∗ node(𝑟, 𝑚, es𝑚 , 𝑉𝑚 ) ∗ es𝑛 (𝑚) ≠ ∅
14 mergeContents 𝑟 𝑛 𝑚
                     ′                      ′       ′                                 ′
15 node(𝑟, 𝑛, es𝑛 , 𝑉𝑛 ) ∗ node(𝑟, 𝑚, es𝑚 , 𝑉𝑚 ) ∗ 𝑉𝑛 = mergeLeft (𝐾, 𝑉𝑛 , Es, 𝑉𝑚 ) ∗ 𝑉𝑚 = mergeRight (𝐾, 𝑉𝑛 , Es, 𝑉𝑚 )


                                                     Fig. 10. Specifications of helper functions used by compact.


     𝑘1       5        {𝑘 1 }           𝑘1       3        𝑘1       5        {𝑘 1 }       𝑘1       3         𝑘1       ⊥        {𝑘 1 }       𝑘1       5     𝑘1       ⊥        {𝑘 1 }           𝑘1       ⊥
     𝑘2       6                         𝑘2       4        𝑘2       ⊥                     𝑘2       4         𝑘2       ⊥                     𝑘2       4     𝑘2       ⊥                         𝑘2       ⊥
          𝑛                                  𝑝                 𝑛                              𝑝                  𝑛                              𝑝              𝑛                                  𝑝
              {𝑘 2 }                    {𝑘 1, 𝑘 2 }                {𝑘 2 }                {𝑘 1, 𝑘 2 }                 {𝑘 2 }                {𝑘 1, 𝑘 2 }             {𝑘 2 }                     {𝑘 1, 𝑘 2 }


                          𝑘1        2                                         𝑘1     2                                          𝑘1     2                                       𝑘1        5
                          𝑘2        1                                         𝑘2     6                                          𝑘2     6                                       𝑘2        4
(1)                             𝑚                       (2)                      𝑚                      (3)                        𝑚                     (4)                         𝑚


Fig. 11. Possible execution of the compact operation on a DAG. Edges are labeled with their edgesets. The
nodes undergoing compaction in each iteration are marked in blue.


  Technically, the linearization point of the operation occurs when all locks are released, just before
the function terminates. However, the interesting part of the proof is to show that the changes to
the physical contents of nodes 𝑛 and 𝑚 performed by each call to mergeContents at line 7 preserve
the abstract state of the structure as well as the invariants. In particular, the changes to 𝐶𝑛 and
𝐶𝑚 also affect the contents-in-reach of 𝑚. We need to argue that this is a local effect that does not
propagate further in the data structure, as we did in our proof of upsert.
   Auxiliary invariants. When proving the correctness of compact, we face two technical challenges.
The first challenge arises when establishing that compact changes the contents of the nodes involved
in such a way that the high-level invariants are maintained. In particular, we must reestablish
Invariant 2, which states that the contents-in-reach of each node can only increase over time.
Compaction replaces downstream copies of keys with upstream copies. Thus, in order to maintain
Invariant 2, we need the additional auxiliary invariant that the timestamps of keys in the contents
of nodes can only decrease as we move away from the root:
Invariant 5 The (timestamp) contents of a node is not smaller than the contents-in-reach of
its successor. That is, for all keys 𝑘 and nodes 𝑛 and 𝑚, if 𝑘 ∈ es(𝑛, 𝑚) and 𝐶𝑛 (𝑘) ≠ ⊥ then
ts(𝐶 ir (𝑚) (𝑘)) ⩽ ts(𝐶𝑛 (𝑘)).

                                                                                                       21
,,                                            Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


  We can capture Invariant 5 in our data structure invariant MCS(𝑟, 𝑡, 𝐻 ) by adding the following
predicate as an additional conjunct to the predicate NS (𝑟, 𝑛, 𝐶𝑛 , 𝐵𝑛 ):
                                 𝜙 3 (𝑛) B ∀𝑘. ts(𝑄𝑛 (𝑘)) ⩽ ts(𝐵𝑛 (𝑘))                                  (10)
   The second challenge is that the maintenance template generates only tree-like structures. This
implies that at any time there is at most one path from the root to each node in the structure.
We will see that this invariant is critical for maintaining Invariant 5. However, the data structure
invariant presented thus far allows for arbitrary DAGs.
   To motivate this issue further, consider the multicopy structure in step (1) of Figure 11. The
logical contents of this structure (i.e. the contents-in-reach of 𝑛) is {𝑘 1 ↣ (5, 5), 𝑘 2 ↣ (6, 6)}.
   The structure in step (2) shows the result obtained after executing compact 𝑟 𝑛 to completion
where 𝑛 has been considered to be at capacity and the successor 𝑚 has been chosen for the merge,
resulting in (𝑘 2, (6, 6)) being moved from 𝑛 to 𝑚. Note that at this point the logical contents of the
data structure is still {𝑘 1 ↣ (5, 5), 𝑘 2 ↣ (6, 6)} as in the original structure. However, the structure
now violates Invariant 5 for nodes 𝑝 and 𝑚 since ts(𝐵𝑚 (𝑘 2 )) > ts(𝐶𝑝 (𝑘 2 )).
   Suppose that now a new compaction starts at 𝑛 that still considers 𝑛 at capacity and chooses 𝑝
for the merge. The merge then moves the copy (𝑘 1, (5, 5)) from 𝑛 to 𝑝. The graph in step (3) depicts
the resulting structure. The compaction then continues with 𝑝, which is also determined to be
at capacity. Node 𝑚 is chosen for the merge, resulting in (𝑘 1, (5, 5)) and (𝑘 2, (4, 4)) being moved
from 𝑝 to 𝑚. At this point, the second compaction terminates. The final graph in step (4) shows the
structure obtained at this point. Observe that the logical contents is now {𝑘 1 ↣ (5, 5), 𝑘 2 ↣ (4, 4)}.
Thus, this execution violates the specification of compact, which states that the logical contents
must be preserved. In fact, a timestamp in the contents-in-reach of 𝑛 has decreased, which violates
Invariant 2.
   We observe that although compact will create only tree-like structures, we can prove its correct-
ness using a weaker invariant that does not rule out non-tree DAGs, but instead focuses on how
compact interferes with concurrent search operations. This weaker invariant relies on the fact
that for every key 𝑘 in the contents of a node 𝑛, there exists a unique search path from the root 𝑟
to 𝑛 for 𝑘. That is, if we project the graph to only those nodes reachable from the root via edges
(𝑛, 𝑚) that satisfy 𝑘 ∈ es(𝑛, 𝑚), then this projected graph is a list. Using this weaker invariant we
can capture implementations based on B-link trees or skip lists which are DAGs but have unique
search paths.
   To this end, we recall from [Shasha and Goodman 1988] the notion of the inset of a node 𝑛,
ins(𝑛), which is the set of keys 𝑘 such that there exists a (possibly empty) path from the root 𝑟 to 𝑛,
and 𝑘 is in the edgeset of all edges along that path. That is, since a search for a key 𝑘 traverses only
those edges (𝑛, 𝑚) in the graph that have 𝑘 in their edgeset, the search traverses (and accesses the
contents of) only those nodes 𝑛 such that 𝑘 ∈ ins(𝑛). Now observe that compact, in turn, moves
new copies of a key 𝑘 downward in the graph only along edges that have 𝑘 in their edgeset. The
following invariant is a consequence of these observations and the definition of contents-in-reach:
Invariant 6 A key is in the contents-in-reach of a node only if it is also in the node’s inset. That
is, dom(𝐶 ir (𝑛)) ⊆ ins(𝑛).
This invariant rules out the problematic structure in step (1) of Figure 11 because we have 𝑘 2 ∈
dom(𝐶 ir (𝑝)) but 𝑘 2 ∉ ins(𝑝) = {𝑘 1 }.
   Invariant 6 alone is not enough to ensure that Invariant 5 is preserved. For example, consider the
structure obtained from (1) of Figure 11 by changing the edgeset of the edge (𝑛, 𝑝) to {𝑘 1, 𝑘 2 }. This
modified structure satisfies Invariant 6 but allows the same problematic execution ending in the
violation of Invariant 5 that we outlined earlier. However, observe that in the modified structure

                                                   22
Verifying Concurrent Multicopy Search Structures                                                          ,,


Table 1. Summary of templates and instantiations verified in Iris/Coq and GRASShopper. For each algorithm
or library, we show the number of lines of code, lines of proof annotation (including specification), total
number of lines, and the proof-checking/verification time in seconds.

 Templates (Iris/Coq)                                     Implementations (GRASShopper)
 Module               Code       Proof Total Time         Module             Code Proof Total Time
 Flow Library            0        3757 3757     41        Array Library       191   440   631    11
 Lock Implementation    10         352   362    11        LSM Implementation  207   246   453    51
 Client-level Spec       7         931   938    40
 DF Template            19         914   933    90
 LSM DAG Template       39        3666 3705    353
 Total                  75        9620 9695    535        Total                  398     686    1084    62



𝑘 2 ∈ es(𝑛, 𝑝) ∩ es(𝑛, 𝑚), which violates the property that all edgesets leaving a node are disjoint.
We have already captured this property in our data structure invariant (as an assumption on the
implementation-specific predicate node(𝑟, 𝑛, es, 𝐶𝑛 )). However, in our formal proof we need to
rule out the possibility that a search for 𝑘 can reach a node 𝑚 via two incoming edgesets es(𝑛, 𝑚)
and es(𝑝, 𝑚). Proving that disjoint outgoing edgesets imply unique search paths involves global
inductive reasoning about the paths in the multicopy structure. To do this using only local reasoning,
we will instead rely on an inductive consequence of locally disjoint outgoing edgesets, which we
capture explicitly as an additional auxiliary invariant (and which we will enforce using flows):
Invariant 7 The distinct immediate predecessors of any node 𝑛 have disjoint insets. More precisely,
for all distinct nodes 𝑛, 𝑝, 𝑚, and keys 𝑘, if 𝑘 ∈ es(𝑛, 𝑚) ∩ es(𝑝, 𝑚) then 𝑘 ∉ ins(𝑛) ∩ ins(𝑝).
Note that changing the edgeset of (𝑛, 𝑝) in Figure 11 to {𝑘 1, 𝑘 2 } would violate Invariant 7 because
the resulting structure would satisfy 𝑘 2 ∈ es(𝑛, 𝑚) ∩ es(𝑝, 𝑚) and 𝑘 2 ∈ ins(𝑛) ∩ ins(𝑝).
   In order to capture invariants 6 and 7 in MCS(𝑟, 𝑡, 𝐻 ), we introduce an additional flow that we
use to encode the inset of each node. The encoding of insets in terms of a flow follows [Krishna
et al. 2020a]. That is, the underlying flow domain is multisets of keys 𝑀 = KS → N and the actual
calculation of the insets is captured by (FlowEqn) if we define:

                 e(𝑛, 𝑛 ′) B 𝜆𝑚. 𝑚 ∩ es(𝑛, 𝑛 ′)                   in(𝑛) B 𝜒 (𝑛 = 𝑟 ? KS : ∅)

If fl ins is a flow that satisfies (FlowEqn) for these definitions of e and in, then for any node 𝑛 that
is reachable from 𝑟 , fl ins (𝑛) (𝑘) > 0 iff 𝑘 ∈ ins(𝑛). Invariants 6 and 7 are then captured by the
following two predicates, which we add to NS :

          𝜙 4 (𝑛) B ∀𝑘. 𝑘 ∈ dom(𝐵𝑛 ) ⇒ fl ins (𝑛) (𝑘) > 0             𝜙 5 (𝑛) B ∀𝑘. fl ins (𝑛)(𝑘) ⩽ 1

Note that 𝜙 5 captures Invariant 7 as a property of each individual node 𝑛 by taking advantage of
the fact that the multiset fl ins (𝑛) explicitly represents all of the contributions made to the inset of 𝑛
by 𝑛’s predecessor nodes.
   We briefly explain why we can still prove the correctness of search and upsert with the updated
data structure invariant. First note that search does not modify the contents, edgesets, or any other
ghost resources of any node. So the additional conjuncts in the invariant are trivially maintained.
   Now let us consider the operation upsert 𝑟 𝑘 𝑣. Since upsert does not change the edgesets of
any nodes, the resources and constraints related to the inset flow are trivially maintained, with the
exception of 𝜙 4 (𝑟 ): after the upsert we have 𝑘 ∈ dom(𝐵𝑟 ) which may not have been true before.
However, from in(𝑟 ) (𝑘) = 1, the flow equation, and the fact that the flow domain is positive, it
follows that we must have fl ins (𝑟 ) (𝑘) > 0 (i.e., 𝑘 ∈ ins(𝑟 ) = KS). Hence, 𝜙 4 (𝑟 ) is preserved as well.

                                                     23
,,                                                 Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


8    PROOF MECHANIZATION
We illustrate the proof methodology presented in this paper by verifying that the multicopy
template algorithm (§5, §6, and §7) satisfies search recency. We then instantiate the template
to an LSM-like implementation to demonstrate an application of the template. Our proof effort
(summarized in Table 1) also contains a mechanically-checked proof that search recency refines the
Map ADT specification (§4). We further verify a two-node multicopy structure template that can
be instantiated to differential file (DF) structure implementations [Severance and Lohman 1976].
We include this template in our artifact to demonstrate the reuse of the helping proof and because
it has a simpler invariant. Though, we provide no implementation for the two-node template. The
artifact is available as a VM image on Zenodo4 and as source code on GitHub5 . Verification time
was measured on a laptop with an Intel Core i7-8750H CPU and 16GB RAM.
   The client-level and template-level proofs were performed in Iris and mechanically verified by
the Coq tool, and comprise the left half of Table 1. The flow library formalizes the meta theory of
flow interface cameras used in the template proofs. It extends the development of [Krishna et al.
2020a] with a general theory of multiset-based flow domains (about 900 lines).
   Our LSM implementation is verified in the SMT-based separation logic tool GRASShopper, and
is described in the right half of the table. The implementation uses an unsorted array to store
key-timestamp pairs for the (in-memory) root node (with upserts adding to one end of the array),
and a read-only sorted array (also known as a sorted string table [Google 2021]) for the other
(on-disk) nodes. This array models the contents of a file. The implementation uses a library of
utility functions and lemmas for arrays that represent partial maps from keys to values.
   We verify both the helper functions for the core search structure operations (Figure 7) as well
as those needed by the maintenance template (Figure 9). Each operation demuxes between the
code for in-memory and on-disk nodes based on the reference to the operation node. For instance,
in the case of mergeContents 𝑟 𝑛 𝑚, if 𝑟 = 𝑛 then the operation flushes the in-memory node 𝑛 to
the on-disk node 𝑚. Otherwise, both 𝑛 and 𝑚 must be on-disk nodes, which are then compacted.
Alternatively, one could use separate implementations of each helper function for the two types
of nodes. The polymorphism could then be resolved statically by unfolding the recursion in the
template algorithms once, letting helper function calls in the unfolded iteration go to the in-memory
versions and all remaining ones to the on-disk versions.
   There are two gaps in the verification that would need to be bridged to obtain a complete
end-to-end proof. First, there is currently no way to formally compose the proofs done in Iris/Coq
and GRASShopper. However, the two proofs are linked by the node-level specifications of helper
functions such as findNext at the representation level. As with prior work [Krishna et al. 2020a], we
split our verification across two tools in order to take advantage of SMT-based automated techniques
for the sequential implementation proofs which are tedious but not technically challenging. Second,
GRASShopper does not support reasoning about file access directly. We effectively model each
file as a RAM disk whose contents is mapped into memory. This is consistent with the abstract
interface for performing file accesses in the LSM tree implementation of LevelDB [Google 2021].
   One specific technical challenge that we had to overcome in the Iris formalization is related to the
decoupling of the generic client-template proof from the template-implementation proofs. At the
linearization point of upsert, the proof needs to reestablish the invariant of the helping protocol.
That is, each template-implementation proof needs to update the relevant ghost resources used
for encoding this invariant. We have eliminated the dependency of the template-implementation
proof on the concrete representation of the helping protocol invariant by parameterizing this part
4 https://zenodo.org/record/5496104
5 https://github.com/nyu-acsys/template-proofs/multicopy



                                                           24
Verifying Concurrent Multicopy Search Structures                                                      ,,


of the proof over all possible helping protocols that can be maintained by an upsert. We discuss
this issue in more detail in Appendix A.3.
   A more desirable solution would be to restrict all reasoning related to the helping protocol
to the client-template proof so that the template-implementation proofs do not depend on the
helping protocol at all. Essentially, the idea would be to do the relevant ghost state updates in the
client-template level proof of upsert when the template-level atomic triple of upsert is committed.
Unfortunately, this idea cannot be realized with Iris’ current definition of atomic triples. Proving that
the helping protocol invariant is maintained involves the elimination of a so-called later modality.
That is, one needs to show that a physical computation step is executed at the linearization point
(e.g. a memory read or write). However, Iris’ atomic triples 𝑥®. 𝑃 𝑒 𝑣 . 𝑄 are in some sense too
abstract, as they do not capture whether 𝑐 performs a physical computation step. More fine-grained
notions of atomic triples are a promising direction for future work.

9   RELATED WORK
Most closely related to our work is the edgeset framework for verifying single-copy structure
templates [Krishna et al. 2020a; Shasha and Goodman 1988]. The edgeset framework hinges on
the notion of the keyset of a node, which is the set of keys that are allowed in the node. That is, a
node’s contents must be a subset of its keyset. Moreover, the keysets of all nodes must be disjoint.
The contribution of Krishna et al. [2020a] is to capture these invariants by a resource algebra in Iris
and to show how keysets can be related to the search structure graph using flows to enable local
reasoning about template algorithms for single-copy structures. Note that this work [Krishna et al.
2020a; Shasha and Goodman 1988] is limited to single-copy structures since the keyset invariants
enforce that every key appears in at most one node. In multicopy structures, the same key may
appear in multiple nodes with different associated values.
   Relative to [Krishna et al. 2020a; Shasha and Goodman 1988], the main technical novelties are: (i)
we identify a node-local quantity (contents-in-reach) for multicopy structures that plays a similar
role to the keyset in the single-copy case. Both the invariants that the contents-in-reach must
satisfy as well as how the contents-in-reach is encoded using flows is substantially different from
the keyset. (ii) We capture the order-preservation aspect of linearizability for multicopy structures
in the notion of search recency. (iii) We develop and verify new template algorithms for multicopy
structures.
   In data structures based on RCU synchronization such as the Citrus tree [Arbel and Attiya 2014],
the same key may temporarily appear in multiple nodes. However, such structures are not necessar-
ily multicopy structures. Notably, in a Citrus tree, all copies of a key have the same associated value
even in the presence of concurrent updates. Moreover, searches have fixed linearization points.
This structure can therefore be handled, in principle, using the single-copy framework of Krishna
et al. [2020a] (by building on the formalization of the RCU semantics developed in [Gotsman et al.
2013] and the high-level proof idea for the Citrus tree of Feldman et al. [2020]).
   Several other works present generic proof arguments for verifying concurrent traversals of
search structures that involve dynamic linearization points [Drachsler-Cohen et al. 2018; Feldman
et al. 2018, 2020; O’Hearn et al. 2010]. However, these approaches focus on single-copy structures
and rely on global reasoning based on graph reachability.
   The idea of tracking auxiliary ghost state about a data structure’s history to simplify its lin-
earizability proof has been used in many prior works (e.g. [Bouajjani et al. 2017; Delbianco et al.
2017; Sergey et al. 2015b]). We build on these works and apply this idea to decouple the reasoning
about the non-local linearization points of searches from the verification of any specific multicopy
structure template.

                                                   25
,,                                           Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


   We have formalized the verification of our template algorithms in Iris [Jung et al. 2018]. Our
formalization particularly benefits from Iris’s support for user-definable resource algebras, which
can capture nontrivial ghost state such as flow interfaces. However, there are a number of other
formal proof systems that provide mechanisms for structuring complex linearizability proofs,
including other concurrent separation logics [da Rocha Pinto et al. 2014; Dinsdale-Young et al.
2013; Fu et al. 2010; Gardner et al. 2014; Raad et al. 2015; Sergey et al. 2015a] as well as systems
based on classical logic [Elmas et al. 2010; Kragl and Qadeer 2018; Kragl et al. 2020]. We also
make use of Iris’s support for logically atomic triples and prophecy variables to reason modularly
about the non-local dynamic linearization points of searches. Specifically, the proof discussed in §4
builds on the prophecy-based Iris proof of the RDCSS data structure from [Jung et al. 2020] and
adapts it to a setting where an unbounded number of threads perform “helping”. The idea of using
prophecy variables to reason about non-fixed linearization points has also been explored in prior
work building on logics other than Iris [Sezgin et al. 2010; Vafeiadis 2008; Zhang et al. 2012].
   Our proofs rely on both history and prophecy-based reasoning. However, we use the two ideas
separately in the two parts of the proof (client-template vs. template-implementation). It does not
seem possible to prove the client-template part without using prophecies. The reason is that we use
an atomic triple to express the client-level specification. The atomic triple needs to be committed
at the actual linearization point. If we were to use only history-based information in the proof,
then we would determine at the point when (𝑘, (𝑣, 𝑡 ′)) is found that the linearization point already
happened in the past. However, at that point, it is already too late to commit the atomic triple.
   A proof that uses only history-based verification and does not rely on atomic triples is likely
possible. For instance, one alternative approaches to using atomic triples is to prove that the
template-level atomic specification contextually refines the client-level atomic specification of
multicopy structures using a relational program logic. A number of prior works have developed
such refinement-based approaches [Banerjee et al. 2016; Frumin et al. 2018, 2020], including for
settings that involve unbounded helping [Liang and Feng 2013; Turon et al. 2013]. An alternative
approach to using prophecy variables for reasoning about non-fixed linearization points is to
explicitly construct a partial order of events as the program executes, effectively representing all
the possible linearizations that are consistent with the observations made so far [Khyzha et al.
2017].
   There has also been much work on obtaining fully automated proofs of linearizability by static
analysis and model checking [Abdulla et al. 2013, 2018; Amit et al. 2007; Bouajjani et al. 2013,
2015, 2017; Cerný et al. 2010; Dragoi et al. 2013; Henzinger et al. 2013; Lesani et al. 2014; Vafeiadis
2009; Zhu et al. 2015]. The proof framework presented in this paper is capable of reasoning about
implementations that are beyond the reach of current automatic techniques, via interactive (though
still machine-checked) template proofs. We hope that this framework will help to inform the design
of future automated static analyzers for concurrent programs.
   Multicopy structures such as the LSM tree are often used in file and database systems to organize
data that spans multiple storage media, e.g., RAM and hard disks. Several prior projects have
considered the formal verification of file systems. SibyllFS [Ridge et al. 2015] provides formal
specifications for POSIX-based file system implementations to enable systematic testing of existing
implementations. FSCQ [Chen et al. 2015], Yggdrasil [Bornholt et al. 2016; Sigurbjarnarson et al.
2016], and DFSCQ [Chen et al. 2017] provide formally verified file system implementations that also
guarantee crash consistency. However, these implementations do not support concurrent execution
of file system operations. Our work provides a framework for reasoning about the in-memory
concurrency aspects of multicopy structures. However, we mostly abstract from issues related to
the interaction with the different storage media. Notably, in our verified LSM tree implementation,
we do not model disk failure and hence do not address crash consistency.

                                                  26
Verifying Concurrent Multicopy Search Structures                                                                             ,,


   Distributed key/value stores have to contend with copies of keys being present in multiple nodes
at a time. Several works verify consistency of operations performed on such data structures [Chordia
et al. 2013; Kaki et al. 2018; Xiong et al. 2020], including linearizability [Wang et al. 2019]. In the
distributed context, the main technical challenge arises from data replication and the ensuing
weakly consistent semantics of concurrent operations. As we consider lock-based templates, we
can assume a sequentially consistent memory model for our verification. For lock-free multicopy
structures such as the Bw-tree [Levandoski et al. 2013], weak memory consistency may be a concern.
Lock-free multicopy structures also require the development of new template algorithms, which
then need to be shown linearizable with respect to the template-level specification. However, once
this is established, linearizability with respect to the client-level specification is obtained for free. We
also believe that the high-level invariants from §6 are applicable towards proving the template-level
specification. For instance, each lock-free node-local list of the Bw-tree behaves like a multicopy
structure and satisfies the identified invariants.

10    CONCLUSION
This paper and the accompanying verification effort have made the following contributions: We
presented a general framework for verifying concurrent multicopy structures. The framework
introduces an intermediate abstraction layer that enables reasoning about concurrent multicopy
structures in terms of template algorithms that abstract from the data structure representation.
We constructed such a template algorithm that generalizes the log-structured merge tree to DAGs
and proved its correctness. The proof is decomposed into two parts to maximize proof reuse: (1)
a general reduction of linearizability of multicopy structures that eliminates the need to reason
about non-local linearization points; and (2) a generic proof of the template algorithm that abstracts
from the data structure’s memory representation in concrete implementations. The full proof is
formalized in the concurrent separation logic Iris and mechanized in Coq. We have also verified
an instantiation of the template algorithm to LSM trees, resulting in the first formally-verified
concurrent multicopy search structure.

ACKNOWLEDGMENTS
This work is funded in parts by the National Science Foundation under grants 1925605, 1815633,
1934388, 1840761, and 1339362. Further funding came from NYU WIRELESS and from the New
York University Abu Dhabi Center for Interacting Urban Networks (CITIES). We thank Elizabeth
Dietrich and Raphael Sofaer for their help on mechanizing the proofs of the differential file template.
We also extend our gratitude to the anonymous reviewers of OOPSLA’21 whose questions helped
us clarify the presentation. We would also like to thank the reviewers of the book [Krishna et al.
2021], specifically Maurice Herlihy, Eddie Kohler, Robbert Krebbers, K. Rustan M. Leino, and Peter
Müller, for their suggestions to improve the presentation.

REFERENCES
Martín Abadi and Leslie Lamport. 1988. The Existence of Refinement Mappings. In Proceedings of the Third Annual
   Symposium on Logic in Computer Science (LICS ’88), Edinburgh, Scotland, UK, July 5-8, 1988. IEEE Computer Society,
   165–175. https://doi.org/10.1109/LICS.1988.5115
Parosh Aziz Abdulla, Frédéric Haziza, Lukás Holík, Bengt Jonsson, and Ahmed Rezine. 2013. An Integrated Specification and
   Verification Technique for Highly Concurrent Data Structures. In Tools and Algorithms for the Construction and Analysis
   of Systems - 19th International Conference, TACAS 2013, Held as Part of the European Joint Conferences on Theory and
   Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings (Lecture Notes in Computer Science, Vol. 7795),
   Nir Piterman and Scott A. Smolka (Eds.). Springer, 324–338. https://doi.org/10.1007/978-3-642-36742-7_23
Parosh Aziz Abdulla, Bengt Jonsson, and Cong Quy Trinh. 2018. Fragment Abstraction for Concurrent Shape Analysis. In
   Programming Languages and Systems - 27th European Symposium on Programming, ESOP 2018, Held as Part of the European


                                                              27
,,                                                      Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


   Joint Conferences on Theory and Practice of Software, ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings
  (Lecture Notes in Computer Science, Vol. 10801), Amal Ahmed (Ed.). Springer, 442–471. https://doi.org/10.1007/978-3-319-
   89884-1_16
Daphna Amit, Noam Rinetzky, Thomas W. Reps, Mooly Sagiv, and Eran Yahav. 2007. Comparison Under Abstraction for
   Verifying Linearizability. In Computer Aided Verification, 19th International Conference, CAV 2007, Berlin, Germany, July
   3-7, 2007, Proceedings (Lecture Notes in Computer Science, Vol. 4590), Werner Damm and Holger Hermanns (Eds.). Springer,
   477–490. https://doi.org/10.1007/978-3-540-73368-3_49
Apache Software Foundation. 2021. Apache Cassandra. https://cassandra.apache.org/. Last accessed on August 12, 2021.
Maya Arbel and Hagit Attiya. 2014. Concurrent updates with RCU: search tree as an example. In ACM Symposium on
   Principles of Distributed Computing, PODC ’14, Paris, France, July 15-18, 2014, Magnús M. Halldórsson and Shlomi Dolev
   (Eds.). ACM, 196–205. https://doi.org/10.1145/2611462.2611471
Anindya Banerjee, David A. Naumann, and Mohammad Nikouei. 2016. Relational Logic with Framing and Hypotheses. In
   36th IARCS Annual Conference on Foundations of Software Technology and Theoretical Computer Science, FSTTCS 2016,
   December 13-15, 2016, Chennai, India (LIPIcs, Vol. 65), Akash Lal, S. Akshay, Saket Saurabh, and Sandeep Sen (Eds.). Schloss
   Dagstuhl - Leibniz-Zentrum für Informatik, 11:1–11:16. https://doi.org/10.4230/LIPIcs.FSTTCS.2016.11
James Bornholt, Antoine Kaufmann, Jialin Li, Arvind Krishnamurthy, Emina Torlak, and Xi Wang. 2016. Specifying
   and Checking File System Crash-Consistency Models. In Proceedings of the Twenty-First International Conference on
   Architectural Support for Programming Languages and Operating Systems, ASPLOS 2016, Atlanta, GA, USA, April 2-6, 2016,
   Tom Conte and Yuanyuan Zhou (Eds.). ACM, 83–98. https://doi.org/10.1145/2872362.2872406
Ahmed Bouajjani, Michael Emmi, Constantin Enea, and Jad Hamza. 2013. Verifying Concurrent Programs against Sequential
   Specifications. In Programming Languages and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as
   Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013.
   Proceedings (Lecture Notes in Computer Science, Vol. 7792), Matthias Felleisen and Philippa Gardner (Eds.). Springer,
   290–309. https://doi.org/10.1007/978-3-642-37036-6_17
Ahmed Bouajjani, Michael Emmi, Constantin Enea, and Jad Hamza. 2015. On Reducing Linearizability to State Reachability.
   In Automata, Languages, and Programming - 42nd International Colloquium, ICALP 2015, Kyoto, Japan, July 6-10, 2015,
   Proceedings, Part II (Lecture Notes in Computer Science, Vol. 9135), Magnús M. Halldórsson, Kazuo Iwama, Naoki Kobayashi,
   and Bettina Speckmann (Eds.). Springer, 95–107. https://doi.org/10.1007/978-3-662-47666-6_8
Ahmed Bouajjani, Michael Emmi, Constantin Enea, and Suha Orhun Mutluergil. 2017. Proving Linearizability Using Forward
   Simulations. In Computer Aided Verification - 29th International Conference, CAV 2017, Heidelberg, Germany, July 24-28,
   2017, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 10427), Rupak Majumdar and Viktor Kuncak (Eds.).
   Springer, 542–563. https://doi.org/10.1007/978-3-319-63390-9_28
Pavol Cerný, Arjun Radhakrishna, Damien Zufferey, Swarat Chaudhuri, and Rajeev Alur. 2010. Model Checking of
   Linearizability of Concurrent List Implementations. In Computer Aided Verification, 22nd International Conference, CAV
   2010, Edinburgh, UK, July 15-19, 2010. Proceedings (Lecture Notes in Computer Science, Vol. 6174), Tayssir Touili, Byron
   Cook, and Paul B. Jackson (Eds.). Springer, 465–479. https://doi.org/10.1007/978-3-642-14295-6_41
Haogang Chen, Tej Chajed, Alex Konradi, Stephanie Wang, Atalay Mert Ileri, Adam Chlipala, M. Frans Kaashoek, and
   Nickolai Zeldovich. 2017. Verifying a high-performance crash-safe file system using a tree specification. In Proceedings
   of the 26th Symposium on Operating Systems Principles, Shanghai, China, October 28-31, 2017. ACM, 270–286. https:
   //doi.org/10.1145/3132747.3132776
Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala, M. Frans Kaashoek, and Nickolai Zeldovich. 2015. Using
   Crash Hoare logic for certifying the FSCQ file system. In Proceedings of the 25th Symposium on Operating Systems
   Principles, SOSP 2015, Monterey, CA, USA, October 4-7, 2015, Ethan L. Miller and Steven Hand (Eds.). ACM, 18–37.
   https://doi.org/10.1145/2815400.2815402
Sagar Chordia, Sriram K. Rajamani, Kaushik Rajan, Ganesan Ramalingam, and Kapil Vaswani. 2013. Asynchronous
   Resilient Linearizability. In Distributed Computing - 27th International Symposium, DISC 2013, Jerusalem, Israel, October
   14-18, 2013. Proceedings (Lecture Notes in Computer Science, Vol. 8205), Yehuda Afek (Ed.). Springer, 164–178. https:
   //doi.org/10.1007/978-3-642-41527-2_12
Pedro da Rocha Pinto, Thomas Dinsdale-Young, and Philippa Gardner. 2014. TaDA: A Logic for Time and Data Abstraction.
   In ECOOP 2014 - Object-Oriented Programming - 28th European Conference, Uppsala, Sweden, July 28 - August 1, 2014.
   Proceedings (Lecture Notes in Computer Science, Vol. 8586), Richard E. Jones (Ed.). Springer, 207–231. https://doi.org/10.
   1007/978-3-662-44202-9_9
Niv Dayan and Stratos Idreos. 2018. Dostoevsky: Better Space-Time Trade-Offs for LSM-Tree Based Key-Value Stores
   via Adaptive Removal of Superfluous Merging. In Proceedings of the 2018 International Conference on Management of
   Data, SIGMOD Conference 2018, Houston, TX, USA, June 10-15, 2018, Gautam Das, Christopher M. Jermaine, and Philip A.
   Bernstein (Eds.). ACM, 505–520. https://doi.org/10.1145/3183713.3196927



                                                              28
Verifying Concurrent Multicopy Search Structures                                                                             ,,


Germán Andrés Delbianco, Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2017. Concurrent Data Structures
   Linked in Time. In 31st European Conference on Object-Oriented Programming, ECOOP 2017, June 19-23, 2017, Barcelona,
   Spain (LIPIcs, Vol. 74), Peter Müller (Ed.). Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 8:1–8:30. https://doi.org/10.
   4230/LIPIcs.ECOOP.2017.8
Thomas Dinsdale-Young, Lars Birkedal, Philippa Gardner, Matthew J. Parkinson, and Hongseok Yang. 2013. Views:
   compositional reasoning for concurrent programs. In The 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles
   of Programming Languages, POPL ’13, Rome, Italy - January 23 - 25, 2013, Roberto Giacobazzi and Radhia Cousot (Eds.).
   ACM, 287–300. https://doi.org/10.1145/2429069.2429104
Dana Drachsler-Cohen, Martin T. Vechev, and Eran Yahav. 2018. Practical concurrent traversals in search trees. In Proceedings
   of the 23rd ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming, PPoPP 2018, Vienna, Austria,
   February 24-28, 2018, Andreas Krall and Thomas R. Gross (Eds.). ACM, 207–218. https://doi.org/10.1145/3178487.3178503
Cezara Dragoi, Ashutosh Gupta, and Thomas A. Henzinger. 2013. Automatic Linearizability Proofs of Concurrent Objects
   with Cooperating Updates. In Computer Aided Verification - 25th International Conference, CAV 2013, Saint Petersburg,
   Russia, July 13-19, 2013. Proceedings (Lecture Notes in Computer Science, Vol. 8044), Natasha Sharygina and Helmut Veith
   (Eds.). Springer, 174–190. https://doi.org/10.1007/978-3-642-39799-8_11
Tayfun Elmas, Shaz Qadeer, Ali Sezgin, Omer Subasi, and Serdar Tasiran. 2010. Simplifying Linearizability Proofs with
   Reduction and Abstraction. In Tools and Algorithms for the Construction and Analysis of Systems, 16th International
   Conference, TACAS 2010, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2010,
   Paphos, Cyprus, March 20-28, 2010. Proceedings (Lecture Notes in Computer Science, Vol. 6015), Javier Esparza and Rupak
   Majumdar (Eds.). Springer, 296–311. https://doi.org/10.1007/978-3-642-12002-2_25
Manuel Fahndrich and Rustan Leino. 2003. Heap Monotonic Typestate. In Proceedings of the first International Workshop on
   Alias Confinement and Ownership (IWACO) (proceedings of the first international workshop on alias confinement and
   ownership (iwaco) ed.). https://www.microsoft.com/en-us/research/publication/heap-monotonic-typestate/
Yotam M. Y. Feldman, Constantin Enea, Adam Morrison, Noam Rinetzky, and Sharon Shoham. 2018. Order out of Chaos:
   Proving Linearizability Using Local Views. In 32nd International Symposium on Distributed Computing, DISC 2018,
   New Orleans, LA, USA, October 15-19, 2018 (LIPIcs, Vol. 121), Ulrich Schmid and Josef Widder (Eds.). Schloss Dagstuhl -
   Leibniz-Zentrum für Informatik, 23:1–23:21. https://doi.org/10.4230/LIPIcs.DISC.2018.23
Yotam M. Y. Feldman, Artem Khyzha, Constantin Enea, Adam Morrison, Aleksandar Nanevski, Noam Rinetzky, and Sharon
   Shoham. 2020. Proving highly-concurrent traversals correct. Proc. ACM Program. Lang. 4, OOPSLA (2020), 128:1–128:29.
   https://doi.org/10.1145/3428196
Dan Frumin, Robbert Krebbers, and Lars Birkedal. 2018. ReLoC: A Mechanised Relational Logic for Fine-Grained Concurrency.
   In Proceedings of the 33rd Annual ACM/IEEE Symposium on Logic in Computer Science, LICS 2018, Oxford, UK, July 09-12,
   2018, Anuj Dawar and Erich Grädel (Eds.). ACM, 442–451. https://doi.org/10.1145/3209108.3209174
Dan Frumin, Robbert Krebbers, and Lars Birkedal. 2020. ReLoC Reloaded: A Mechanized Relational Logic for Fine-Grained
   Concurrency and Logical Atomicity. CoRR abs/2006.13635 (2020). arXiv:2006.13635 https://arxiv.org/abs/2006.13635
Ming Fu, Yong Li, Xinyu Feng, Zhong Shao, and Yu Zhang. 2010. Reasoning about Optimistic Concurrency Using a
   Program Logic for History. In CONCUR 2010 - Concurrency Theory, 21th International Conference, CONCUR 2010, Paris,
   France, August 31-September 3, 2010. Proceedings (Lecture Notes in Computer Science, Vol. 6269), Paul Gastin and François
   Laroussinie (Eds.). Springer, 388–402. https://doi.org/10.1007/978-3-642-15375-4_27
Philippa Gardner, Azalea Raad, Mark J. Wheelhouse, and Adam Wright. 2014. Abstract Local Reasoning for Concurrent
   Libraries: Mind the Gap. In Proceedings of the 30th Conference on the Mathematical Foundations of Programming Semantics,
   MFPS 2014, Ithaca, NY, USA, June 12-15, 2014 (Electronic Notes in Theoretical Computer Science, Vol. 308), Bart Jacobs,
   Alexandra Silva, and Sam Staton (Eds.). Elsevier, 147–166. https://doi.org/10.1016/j.entcs.2014.10.009
Google. 2021. LevelDB. https://github.com/google/leveldb. Last accessed on August 12, 2021.
Alexey Gotsman, Noam Rinetzky, and Hongseok Yang. 2013. Verifying Concurrent Memory Reclamation Algorithms
   with Grace. In Programming Languages and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as
   Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013.
   Proceedings (Lecture Notes in Computer Science, Vol. 7792), Matthias Felleisen and Philippa Gardner (Eds.). Springer,
   249–269. https://doi.org/10.1007/978-3-642-37036-6_15
Thomas A. Henzinger, Ali Sezgin, and Viktor Vafeiadis. 2013. Aspect-Oriented Linearizability Proofs. In CONCUR 2013 -
   Concurrency Theory - 24th International Conference, CONCUR 2013, Buenos Aires, Argentina, August 27-30, 2013. Proceedings
   (Lecture Notes in Computer Science, Vol. 8052), Pedro R. D’Argenio and Hernán C. Melgratti (Eds.). Springer, 242–256.
   https://doi.org/10.1007/978-3-642-40184-8_18
Maurice Herlihy and J. D. Tygar. 1987. How to Make Replicated Data Secure. In Advances in Cryptology - CRYPTO ’87,
   A Conference on the Theory and Applications of Cryptographic Techniques, Santa Barbara, California, USA, August 16-
   20, 1987, Proceedings (Lecture Notes in Computer Science, Vol. 293), Carl Pomerance (Ed.). Springer, 379–391. https:
   //doi.org/10.1007/3-540-48184-2_33


                                                              29
,,                                                      Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


Maurice Herlihy and Jeannette M. Wing. 1990. Linearizability: A Correctness Condition for Concurrent Objects. ACM Trans.
   Program. Lang. Syst. 12, 3 (1990), 463–492. https://doi.org/10.1145/78969.78972
Bart Jacobs and Frank Piessens. 2011. Expressive modular fine-grained concurrency specification. In Proceedings of the 38th
   ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2011, Austin, TX, USA, January 26-28,
   2011, Thomas Ball and Mooly Sagiv (Eds.). ACM, 271–282. https://doi.org/10.1145/1926385.1926417
Jonas Braband Jensen and Lars Birkedal. 2012. Fictional Separation Logic. In Programming Languages and Systems - 21st
   European Symposium on Programming, ESOP 2012, Held as Part of the European Joint Conferences on Theory and Practice of
   Software, ETAPS 2012, Tallinn, Estonia, March 24 - April 1, 2012. Proceedings (Lecture Notes in Computer Science, Vol. 7211),
   Helmut Seidl (Ed.). Springer, 377–396. https://doi.org/10.1007/978-3-642-28869-2_19
Jonathan Ellis. 2011. Leveled Compaction in Apache Cassandra. https://www.datastax.com/blog/2011/10/leveled-compaction-
   apache-cassandra. Last accessed on August 12, 2021.
Cliff B. Jones. 1983. Specification and Design of (Parallel) Programs. In Information Processing 83, Proceedings of the IFIP 9th
   World Computer Congress, Paris, France, September 19-23, 1983, R. E. A. Mason (Ed.). North-Holland/IFIP, 321–332.
Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars Birkedal, and Derek Dreyer. 2018. Iris from the
   ground up: A modular foundation for higher-order concurrent separation logic. J. Funct. Program. 28 (2018), e20.
   https://doi.org/10.1017/S0956796818000151
Ralf Jung, Rodolphe Lepigre, Gaurav Parthasarathy, Marianna Rapoport, Amin Timany, Derek Dreyer, and Bart Jacobs.
   2020. The future is ours: prophecy variables in separation logic. Proc. ACM Program. Lang. 4, POPL (2020), 45:1–45:32.
   https://doi.org/10.1145/3371113
Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
   Monoids and Invariants as an Orthogonal Basis for Concurrent Reasoning. In Proceedings of the 42nd Annual ACM
   SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2015, Mumbai, India, January 15-17, 2015,
   Sriram K. Rajamani and David Walker (Eds.). ACM, 637–650. https://doi.org/10.1145/2676726.2676980
Gowtham Kaki, Kartik Nagar, Mahsa Najafzadeh, and Suresh Jagannathan. 2018. Alone together: compositional reasoning
   and inference for weak isolation. Proc. ACM Program. Lang. 2, POPL (2018), 27:1–27:34. https://doi.org/10.1145/3158115
Artem Khyzha, Mike Dodds, Alexey Gotsman, and Matthew J. Parkinson. 2017. Proving Linearizability Using Partial Orders.
   In Programming Languages and Systems - 26th European Symposium on Programming, ESOP 2017, Held as Part of the
   European Joint Conferences on Theory and Practice of Software, ETAPS 2017, Uppsala, Sweden, April 22-29, 2017, Proceedings
   (Lecture Notes in Computer Science, Vol. 10201), Hongseok Yang (Ed.). Springer, 639–667. https://doi.org/10.1007/978-3-
   662-54434-1_24
Bernhard Kragl and Shaz Qadeer. 2018. Layered Concurrent Programs. In Computer Aided Verification - 30th International
   Conference, CAV 2018, Held as Part of the Federated Logic Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings,
   Part I (Lecture Notes in Computer Science, Vol. 10981), Hana Chockler and Georg Weissenbacher (Eds.). Springer, 79–102.
   https://doi.org/10.1007/978-3-319-96145-3_5
Bernhard Kragl, Shaz Qadeer, and Thomas A. Henzinger. 2020. Refinement for Structured Concurrent Programs. In
   Computer Aided Verification - 32nd International Conference, CAV 2020, Los Angeles, CA, USA, July 21-24, 2020, Proceedings,
   Part I (Lecture Notes in Computer Science, Vol. 12224), Shuvendu K. Lahiri and Chao Wang (Eds.). Springer, 275–298.
   https://doi.org/10.1007/978-3-030-53288-8_14
Robbert Krebbers, Jacques-Henri Jourdan, Ralf Jung, Joseph Tassarotti, Jan-Oliver Kaiser, Amin Timany, Arthur Charguéraud,
   and Derek Dreyer. 2018. MoSeL: a general, extensible modal framework for interactive proofs in separation logic. Proc.
   ACM Program. Lang. 2, ICFP (2018), 77:1–77:30. https://doi.org/10.1145/3236772
Robbert Krebbers, Amin Timany, and Lars Birkedal. 2017. Interactive proofs in higher-order concurrent separation logic.
   In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages, POPL 2017, Paris, France,
   January 18-20, 2017, Giuseppe Castagna and Andrew D. Gordon (Eds.). ACM, 205–217. https://doi.org/10.1145/3009837.
   3009855
Siddharth Krishna, Nisarg Patel, Dennis Shasha, and Thomas Wies. 2021. Automated Verification of Concurrent Search
   Structures. Morgan & Claypool Publishers. https://doi.org/10.2200/S01089ED1V01Y202104CSL013
Siddharth Krishna, Nisarg Patel, Dennis E. Shasha, and Thomas Wies. 2020a. Verifying concurrent search structure
   templates. In Proceedings of the 41st ACM SIGPLAN International Conference on Programming Language Design and
   Implementation, PLDI 2020, London, UK, June 15-20, 2020, Alastair F. Donaldson and Emina Torlak (Eds.). ACM, 181–196.
   https://doi.org/10.1145/3385412.3386029
Siddharth Krishna, Dennis E. Shasha, and Thomas Wies. 2018. Go with the flow: compositional abstractions for concurrent
   data structures. Proc. ACM Program. Lang. 2, POPL (2018), 37:1–37:31. https://doi.org/10.1145/3158125
Siddharth Krishna, Alexander J. Summers, and Thomas Wies. 2020b. Local Reasoning for Global Graph Properties. In
   Programming Languages and Systems - 29th European Symposium on Programming, ESOP 2020, Held as Part of the European
   Joint Conferences on Theory and Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings (Lecture
   Notes in Computer Science, Vol. 12075), Peter Müller (Ed.). Springer, 308–335. https://doi.org/10.1007/978-3-030-44914-8_12


                                                              30
Verifying Concurrent Multicopy Search Structures                                                                             ,,


Mohsen Lesani, Todd D. Millstein, and Jens Palsberg. 2014. Automatic Atomicity Verification for Clients of Concurrent Data
   Structures. In Computer Aided Verification - 26th International Conference, CAV 2014, Held as Part of the Vienna Summer of
   Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Proceedings (Lecture Notes in Computer Science, Vol. 8559), Armin Biere
   and Roderick Bloem (Eds.). Springer, 550–567. https://doi.org/10.1007/978-3-319-08867-9_37
Justin J. Levandoski, David B. Lomet, and Sudipta Sengupta. 2013. The Bw-Tree: A B-tree for new hardware platforms.
   In 29th IEEE International Conference on Data Engineering, ICDE 2013, Brisbane, Australia, April 8-12, 2013, Christian S.
   Jensen, Christopher M. Jermaine, and Xiaofang Zhou (Eds.). IEEE Computer Society, 302–313. https://doi.org/10.1109/
   ICDE.2013.6544834
Hongjin Liang and Xinyu Feng. 2013. Modular verification of linearizability with non-fixed linearization points. In ACM
   SIGPLAN Conference on Programming Language Design and Implementation, PLDI ’13, Seattle, WA, USA, June 16-19, 2013,
   Hans-Juergen Boehm and Cormac Flanagan (Eds.). ACM, 459–470. https://doi.org/10.1145/2491956.2462189
Chen Luo and Michael J. Carey. 2020. LSM-based storage techniques: a survey. VLDB J. 29, 1 (2020), 393–418. https:
   //doi.org/10.1007/s00778-019-00555-y
Peter W. O’Hearn, Noam Rinetzky, Martin T. Vechev, Eran Yahav, and Greta Yorsh. 2010. Verifying linearizability with
   hindsight. In Proceedings of the 29th Annual ACM Symposium on Principles of Distributed Computing, PODC 2010, Zurich,
   Switzerland, July 25-28, 2010, Andréa W. Richa and Rachid Guerraoui (Eds.). ACM, 85–94. https://doi.org/10.1145/1835698.
   1835722
Patrick E. O’Neil, Edward Cheng, Dieter Gawlick, and Elizabeth J. O’Neil. 1996. The Log-Structured Merge-Tree (LSM-Tree).
   Acta Informatica 33, 4 (1996), 351–385. https://doi.org/10.1007/s002360050048
Nisarg Patel, Siddharth Krishna, Dennis E. Shasha, and Thomas Wies. 2021. Verifying Concurrent Multicopy Search
   Structures. Proc. ACM Program. Lang. 5, OOPSLA, Article 113 (Oct. 2021), 32 pages.
Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2014. GRASShopper - Complete Heap Verification with Mixed
   Specifications. In Tools and Algorithms for the Construction and Analysis of Systems - 20th International Conference, TACAS
   2014, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2014, Grenoble, France,
   April 5-13, 2014. Proceedings (Lecture Notes in Computer Science, Vol. 8413), Erika Ábrahám and Klaus Havelund (Eds.).
   Springer, 124–139. https://doi.org/10.1007/978-3-642-54862-8_9
Azalea Raad, Jules Villard, and Philippa Gardner. 2015. CoLoSL: Concurrent Local Subjective Logic. In Programming
   Languages and Systems - 24th European Symposium on Programming, ESOP 2015, Held as Part of the European Joint
   Conferences on Theory and Practice of Software, ETAPS 2015, London, UK, April 11-18, 2015. Proceedings (Lecture Notes in
   Computer Science, Vol. 9032), Jan Vitek (Ed.). Springer, 710–735. https://doi.org/10.1007/978-3-662-46669-8_29
Pandian Raju, Rohan Kadekodi, Vijay Chidambaram, and Ittai Abraham. 2017. PebblesDB: Building Key-Value Stores using
   Fragmented Log-Structured Merge Trees. In Proceedings of the 26th Symposium on Operating Systems Principles, Shanghai,
   China, October 28-31, 2017. ACM, 497–514. https://doi.org/10.1145/3132747.3132765
Tom Ridge, David Sheets, Thomas Tuerk, Andrea Giugliano, Anil Madhavapeddy, and Peter Sewell. 2015. SibylFS: formal
   specification and oracle-based testing for POSIX and real-world file systems. In Proceedings of the 25th Symposium on
   Operating Systems Principles, SOSP 2015, Monterey, CA, USA, October 4-7, 2015, Ethan L. Miller and Steven Hand (Eds.).
   ACM, 38–53. https://doi.org/10.1145/2815400.2815411
Russell Sears and Raghu Ramakrishnan. 2012. bLSM: a general purpose log structured merge tree. In Proceedings of the
   ACM SIGMOD International Conference on Management of Data, SIGMOD 2012, Scottsdale, AZ, USA, May 20-24, 2012,
   K. Selçuk Candan, Yi Chen, Richard T. Snodgrass, Luis Gravano, and Ariel Fuxman (Eds.). ACM, 217–228. https:
   //doi.org/10.1145/2213836.2213862
Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2015a. Mechanized verification of fine-grained concurrent
   programs. In Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation,
   Portland, OR, USA, June 15-17, 2015, David Grove and Stephen M. Blackburn (Eds.). ACM, 77–87. https://doi.org/10.1145/
   2737924.2737964
Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2015b. Specifying and Verifying Concurrent Algorithms with
   Histories and Subjectivity. In Programming Languages and Systems - 24th European Symposium on Programming, ESOP 2015,
   Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2015, London, UK, April 11-18, 2015.
   Proceedings (Lecture Notes in Computer Science, Vol. 9032), Jan Vitek (Ed.). Springer, 333–358. https://doi.org/10.1007/978-
   3-662-46669-8_14
Dennis G. Severance and Guy M. Lohman. 1976. Differential Files: Their Application to the Maintenance of Large Databases.
   ACM Trans. Database Syst. 1, 3 (1976), 256–267. https://doi.org/10.1145/320473.320484
Ali Sezgin, Serdar Tasiran, and Shaz Qadeer. 2010. Tressa: Claiming the Future. In Verified Software: Theories, Tools,
   Experiments, Third International Conference, VSTTE 2010, Edinburgh, UK, August 16-19, 2010. Proceedings (Lecture Notes
   in Computer Science, Vol. 6217), Gary T. Leavens, Peter W. O’Hearn, and Sriram K. Rajamani (Eds.). Springer, 25–39.
   https://doi.org/10.1007/978-3-642-15057-9_2



                                                              31
,,                                                     Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


Dennis E. Shasha and Nathan Goodman. 1988. Concurrent Search Structure Algorithms. ACM Trans. Database Syst. 13, 1
   (1988), 53–90. https://doi.org/10.1145/42201.42204
Helgi Sigurbjarnarson, James Bornholt, Emina Torlak, and Xi Wang. 2016. Push-Button Verification of File Systems via
   Crash Refinement. In 12th USENIX Symposium on Operating Systems Design and Implementation, OSDI 2016, Savannah,
   GA, USA, November 2-4, 2016, Kimberly Keeton and Timothy Roscoe (Eds.). USENIX Association, 1–16. https://www.
   usenix.org/conference/osdi16/technical-sessions/presentation/sigurbjarnarson
Risi Thonangi and Jun Yang. 2017. On Log-Structured Merge for Solid-State Drives. In 33rd IEEE International Conference
   on Data Engineering, ICDE 2017, San Diego, CA, USA, April 19-22, 2017. IEEE Computer Society, 683–694. https:
   //doi.org/10.1109/ICDE.2017.121
Aaron Joseph Turon, Jacob Thamsborg, Amal Ahmed, Lars Birkedal, and Derek Dreyer. 2013. Logical relations for fine-
   grained concurrency. In The 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
   POPL ’13, Rome, Italy - January 23 - 25, 2013, Roberto Giacobazzi and Radhia Cousot (Eds.). ACM, 343–356. https:
   //doi.org/10.1145/2429069.2429111
Viktor Vafeiadis. 2008. Modular fine-grained concurrency verification. Ph.D. Dissertation. University of Cambridge, UK.
   http://ethos.bl.uk/OrderDetails.do?uin=uk.bl.ethos.612221
Viktor Vafeiadis. 2009. Shape-Value Abstraction for Verifying Linearizability. In Verification, Model Checking, and Abstract
   Interpretation, 10th International Conference, VMCAI 2009, Savannah, GA, USA, January 18-20, 2009. Proceedings (Lecture
   Notes in Computer Science, Vol. 5403), Neil D. Jones and Markus Müller-Olm (Eds.). Springer, 335–348. https://doi.org/10.
   1007/978-3-540-93900-9_27
Chao Wang, Constantin Enea, Suha Orhun Mutluergil, and Gustavo Petri. 2019. Replication-aware linearizability. In
   Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI 2019,
   Phoenix, AZ, USA, June 22-26, 2019, Kathryn S. McKinley and Kathleen Fisher (Eds.). ACM, 980–993. https://doi.org/10.
   1145/3314221.3314617
Xingbo Wu, Yuehai Xu, Zili Shao, and Song Jiang. 2015. LSM-trie: An LSM-tree-based Ultra-Large Key-Value Store for Small
   Data Items. In 2015 USENIX Annual Technical Conference, USENIX ATC ’15, July 8-10, Santa Clara, CA, USA, Shan Lu and Erik
   Riedel (Eds.). USENIX Association, 71–82. https://www.usenix.org/conference/atc15/technical-session/presentation/wu
Shale Xiong, Andrea Cerone, Azalea Raad, and Philippa Gardner. 2020. Data Consistency in Transactional Storage Systems:
   A Centralised Semantics. In 34th European Conference on Object-Oriented Programming, ECOOP 2020, November 15-17,
   2020, Berlin, Germany (Virtual Conference) (LIPIcs, Vol. 166), Robert Hirschfeld and Tobias Pape (Eds.). Schloss Dagstuhl -
   Leibniz-Zentrum für Informatik, 21:1–21:31. https://doi.org/10.4230/LIPIcs.ECOOP.2020.21
Zipeng Zhang, Xinyu Feng, Ming Fu, Zhong Shao, and Yong Li. 2012. A Structural Approach to Prophecy Variables. In
   Theory and Applications of Models of Computation - 9th Annual Conference, TAMC 2012, Beijing, China, May 16-21, 2012.
   Proceedings (Lecture Notes in Computer Science, Vol. 7287), Manindra Agrawal, S. Barry Cooper, and Angsheng Li (Eds.).
   Springer, 61–71. https://doi.org/10.1007/978-3-642-29952-0_12
He Zhu, Gustavo Petri, and Suresh Jagannathan. 2015. Poling: SMT Aided Linearizability Proofs. In Computer Aided
   Verification - 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceedings, Part II
   (Lecture Notes in Computer Science, Vol. 9207), Daniel Kroening and Corina S. Pasareanu (Eds.). Springer, 3–19. https:
   //doi.org/10.1007/978-3-319-21668-3_1




                                                             32
Verifying Concurrent Multicopy Search Structures                                                    ,,


A     IRIS FORMALIZATION
In this section we present a more detailed summary of the proofs we have formalized in Iris. The
full development can be found in the supplementary materials. We start with a brief discussion
of some additional Iris concepts that we use in our proofs before proceeding to the actual proof
details.

A.1     Atomic Triples
Before we discuss the details of our encoding of the helping protocol in terms of Iris ghost state, it
is instructive to understand the basic structure of a proof of an atomic triple 𝑥 . 𝑃 𝑒 𝑣 . 𝑄 .
              logatom-intro                                 logatom-atom
               ∀Φ. AU𝑥 .𝑃,𝑄 (Φ) 𝑒 𝑣. Φ(𝑣)
                                                                  
                                                            ∀𝑥 . 𝑃 𝑒 𝑣 . 𝑄    𝑒 atomic
                     𝑥. 𝑃 𝑒 𝑣. 𝑄                                   𝑥. 𝑃 𝑒 𝑣. 𝑄

        au-abort                                             au-commit
                   𝑥 . 𝑃 ∗ 𝑃 ′ 𝑒 𝑣. 𝑃 ∗ 𝑄 ′                        𝑥 . 𝑃 ∗ 𝑃 ′ 𝑒 𝑣. 𝑄 ∗ 𝑄 ′
          AU𝑥 .𝑃,𝑄 (Φ) ∗ 𝑃 ′ 𝑒 𝑣. AU𝑥 .𝑃,𝑄 (Φ) ∗ 𝑄 ′          AU𝑥 .𝑃,𝑄 (Φ) ∗ 𝑃 ′ 𝑒 𝑣 . Φ(𝑣) ∗ 𝑄 ′
                                                                               

   The proof proceeds by proving a standard Hoare triple of the form ∀Φ. AU𝑥 .𝑃,𝑄 (Φ) 𝑒 𝑣. Φ(𝑣) .
                                                                                             

Here, AU𝑥 .𝑃,𝑄 (Φ) is the atomic update token, which gives us the right to use the resources in the
precondition 𝑃 when executing atomic instructions up to the linearization point. The token also
records our obligation to preserve 𝑃 up to the linearization point, where 𝑃 must be transformed to
𝑄 in one atomic step. This step consumes the update token. The universally quantified proposition
Φ can be thought of as the precondition for the continuation of the client of the atomic triple. At
the linearization point, when the atomic update token is consumed, the corresponding proof rule
produces Φ as a receipt that the obligation has been fulfilled. This receipt is necessary to complete
the proof of the Hoare triple.
   This can only be done at 𝑒’s linearization point which must transform 𝑃 into 𝑄 and yields Φ(𝑣) as
a receipt. Up to the linearization point, the resources in 𝑃 can be accessed using the rule au-abort,
which ensures that 𝑃 is preserved.

A.2     Invariants in Iris
In the proof of an atomic triple 𝑥 . 𝑃 𝑒 𝑣 . 𝑄 , we can access the resources represented by the
precondition 𝑃 only up to the linearization point of 𝑒. At the linearization point, the resources of 𝑃
are transferred to the postcondition 𝑄, which then become inaccessible to the proof. This restriction
presents a minor technical challenge when proving the atomic triple for search. The linearization
point of search can be in a concurrent upsert. The proof of upsert updates the registry of the
helping protocol for all search threads that it linearizes. In the corresponding case of the proof of
search, we then need to access resources associated with the data structure invariant to determine
the new state of the helping protocol, after the search has already been linearized. If the atomic
preconditions of search’s specification governs all the relevant resources, then we can no longer
access these resources after the linearization point.
   This issue can be avoided by using invariants. An invariant in Iris is a formula of the form
    N
 𝑃 , where 𝑃 is an arbitrary Iris proposition. Invariants provide an orthogonal mechanism to
atomic triples in order to reason about ownership of resources describing shared state that can be
concurrently accessed by many threads. Intuitively, an invariant is a property that, once established,
will remain true forever. It is therefore a duplicable resource and can be freely shared with any
thread.

                                                       33
,,                                                  Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


   However, in order to ensure that the invariant indeed remains valid once it has been established,
Iris’ proof rules for invariants impose restrictions on how the resources contained in an invariant
                                                                                                           N
can be accessed and manipulated. At any point in time, a thread can open an invariant 𝑃 and
gain ownership of the contained resources 𝑃. These resources can then be used in the proof of
a single atomic step of the thread’s execution. After the thread has performed an atomic step
with an open invariant, the invariant must be closed, which amounts to proving that 𝑃 has been
reestablished. Otherwise, the proof cannot succeed. In this sense, invariants behave much like the
preconditions of atomic triples before the atomic triple has been committed, as captured by the
rule au-abort. However, unlike atomic preconditions, which become inaccessible after the commit
point, an invariant is always accessible as long as it is reestablished after each atomic step.
                  N
  The N in 𝑃 refers to the namespace of the invariant. Namespaces are part of the mechanism
used in Iris to keep track of invariants that are currently open and need to be closed before the next
atomic step. This is necessary to avoid issues of re-entrancy in case of nested invariants, which
would lead to logical inconsistencies. In the following, we omit these namespace annotations for
ease of notation. For a more in-depth discussion of Iris’ invariant mechanism and the relevant proof
rules, we refer the interested reader to [Jung et al. 2018].

A.3    Decoupling the Helping and Template Proofs
In our proofs, we parameterize the representation predicate MCS by two abstract predicates
Invtpl (𝑟, 𝑡, 𝐻 ) and Prot(𝐻 ). We do this to achieve a complete decoupling of the template-specific
proofs from the helping proof, which relates the client-level and template-level specifications,
and vice versa. The predicate Invtpl (𝑟, 𝑡, 𝐻 ) abstracts from the resources needed for proving that a
particular multicopy structure template satisfies the template-level specifications. In particular, this
predicate will store the authoritative version of the global clock 𝑡. The predicate Prot(𝐻 ) abstracts
from the resources used to track the state of the helping protocol.
   The fact that Prot depends on 𝐻 creates an unfortunate entanglement between the proofs
performed at the two abstraction levels: at the linearization point of upsert, the upsert history
must be updated from 𝐻 to 𝐻 ∪ {(𝑘, (𝑡, 𝑣))}. This step happens in the proof of each particular
template algorithm for upsert. Therefore, these proofs will also have to carry out the ghost update
that replaces Prot(𝐻 ) by Prot(𝐻 ∪ {(𝑘, (𝑣, 𝑡))}).
   Fortunately, the template-specific proof does not need to know how Prot is defined. It only needs
to know that for any values of 𝐻 , 𝑘, and 𝑡, Prot(𝐻 ) can be updated to Prot(𝐻 ∪ {(𝑘, (𝑣, 𝑡))}). We
capture this assumption on Prot formally using a predicate Updatable(Prot) that we define using
Iris’s linear view shift modality:

                  Updatable(Prot) B (∀ 𝐻 𝑘 𝑡 𝑣 . Prot(𝐻 ) ⇛ Prot(𝐻 ∪ {(𝑘, (𝑣, 𝑡))}))

In order to verify a particular implementation of search and upsert with respect to a particular
template-specific invariant Invtpl (𝑟, 𝑡, 𝐻 ), one then needs to prove validity of the following Iris
propositions:

      ∀ Prot 𝑟 𝑘 𝑣. Inv(Invtpl , Prot) (𝑟 ) −∗ Updatable(Prot) −∗
          𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) upsert 𝑟 𝑘 𝑣 MCS(𝑟, 𝑡 + 1, 𝐻 ∪ (𝑘, (𝑣, 𝑡)))                                      (11)

      ∀ Prot 𝑟 𝑘 𝑣 0 𝑡 0 . Inv(Invtpl , Prot) (𝑟 ) −∗ SR(𝑘, 𝑣 0, 𝑡 0 ) −∗
          𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) search 𝑟 𝑘 𝑣. ∃𝑡 ′ . MCS(𝑟, 𝑡, 𝐻 ) ∗ 𝑡 0 ≤ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻               (12)

                                                          34
Verifying Concurrent Multicopy Search Structures                                                        ,,


These propositions abstract over any helping protocol predicate Prot that is compatible with the
ghost update of 𝐻 performed by upsert. Note that an atomic triple guarded by an invariant can be
interpreted as satisfying the atomic triple under the assumption that the shared state satisfies the
invariant.
   We show below that there exists a specific helping protocol invariant Prothelp such that the
client-level atomic triples hold for any implementation of upsert that satisfies proposition (11)
and any implementations of search that satisfies proposition (12). Formally, if we abbreviate
proposition (11) by UpsertSpec(upsert, Invtpl ) and proposition (12) by SearchSpec(search, Invtpl ).
Then we show validity of the following two propositions:
 ∀ upsert Invtpl 𝑟 𝑘 𝑣. UpsertSpec(upsert, Invtpl ) −∗
  D                                  E             D                                      E
    𝑀. MCS(Invtpl , Prothelp ) (𝑟, 𝑀) upsert 𝑟 𝑘 𝑣 MCS(Invtpl , Prothelp ) (𝑟, 𝑀 [𝑘 ↣ 𝑣])             (13)

 ∀ search Invtpl 𝑟 𝑘. SearchSpec(search, Invtpl ) −∗
  D                                  E           D                                            E
    𝑀. MCS(Invtpl , Prothelp ) (𝑟, 𝑀) search 𝑟 𝑘 𝑣. MCS(Invtpl , Prothelp ) (𝑟, 𝑀) ∗ 𝑀 (𝑘) = 𝑣 (14)
These propositions abstract over the template-specific parameters upsert, search, and Invtpl , but
fix the helping protocol invariant Prot to be Prothelp . In order to obtain the overall correctness proof
of a specific template (upsert, search, Invtpl ), the proofs of these generic propositions then need to
be instantiated only with the proofs of UpsertSpec(upsert, Invtpl ) and SearchSpec(search, Invtpl ).

A.4    The Full Helping Proof
This section presents the full proof of the helping protocol described in §4.3.
   The proof outline in Figure 12 uses rule logatom-intro to obtain the atomic update token AU(Φ)
for the atomic triple in proposition (14) right at the start of search (line 4). The proof transfers
ownership of AU(Φ) from the thread-local context of the search thread to the thread-local context
of the upsert thread that will linearize the search. We do this via the shared representation predicate
MCS, or, to be more precise, an invariant that we store in MCS. In the proof of upsert, when the
search is linearized, the associated receipt Φ(𝑣) is transferred via the shared invariant back to the
search thread. We next explain the details of this part of the proof along with the definitions of
the involved predicates.
   Figure 13 shows the full definition of the representation predicate MCS and the invariant
that encodes the helping protocol. The predicate MCS(Invtpl , Prot) (𝑟, 𝑡, 𝑀) contains the predicate
MCS(𝑟, 𝑡, 𝐻 ), used in the template-level atomic triples, and then defines 𝑀 in terms of 𝐻 via
(∀𝑘. (𝑀 (𝑘), _) = 𝐻¯ (𝑘)). All remaining (ghost) resources associated with the data structure are
owned by the predicate Inv(Invtpl , Prot) (𝑟 ). In particular, this predicate stores the ghost resource
     𝛾𝑠
 •𝐻 whose type is the authoritative RA over sets KS×(V×N). This resource holds the authoritative
version of the current upsert history 𝐻 . Notably, we can then define the predicate SR(𝑘, 𝑣 0, 𝑡 0 ) as the
                                        𝛾𝑠
fractional resource ◦ {(𝑘, (𝑣 0, 𝑡 0 ))} , which expresses the auxiliary precondition (𝑘, (𝑣 0, 𝑡 0 )) ∈ 𝐻
needed for search recency. We track the current value 𝑡 of the global clock in an authoritative
maxnat camera at ghost location 𝛾𝑡 . The camera ensures that the clock value can only increase.
   Inv also stores the abstract template-level invariant Invtpl (𝑟, 𝑡, 𝐻 ), and the abstract predicate
Prot(𝐻 ) used for the bookkeeping related to the helping protocol. In addition, Inv states the three
invariants, HInit(𝐻 ), HUnique(𝐻 ), and HClock(𝑡, 𝐻 ) that are needed to prove the atomic triple of
search.
   Note that we add Inv(Invtpl , Prot) (𝑟 ) to MCS as an Iris invariant (indicated by the box surrounding
the predicate). This provides more flexibility when proving that a template operation satisfies its

                                                    35
,,                                                              Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies

     
 1       SearchSpec(search, Invtpl ) ∗ 𝑀. MCS(Invtpl , Prothelp )(𝑟, 𝑀)
 2 let search 𝑟        𝑘 =
 3        (* Start application of logatom-intro *)
          
 4          AU(Φ)
 5        let tid = NewProph in
 6        let 𝑝 = NewProph in
            AU(Φ) ∗ Proph(tid, _) ∗ Proph(𝑝, 𝑣 𝑝 )
          
 7
          n                                                                      o
 8          AU(Φ) ∗ Proph(tid, _) ∗ Proph(𝑝, 𝑣 𝑝 ) ∗ Inv(Invtpl , Prothelp )(𝑟 )
          n                                               𝛾𝑠                                          o
 9          AU(Φ) ∗ Proph(tid, _) ∗ Proph(𝑝, 𝑣 𝑝 ) ∗ ◦ 𝐻 0 ∗ (𝑣 0, 𝑡 0 ) = 𝐻¯0 (𝑘) ∗ SR(𝑘, 𝑣 0, 𝑡 0 )
10        (* Case analysis on 𝑣 𝑝 = 𝑣 0 , 𝑣 𝑝 ≠ 𝑣 0 : only showing 𝑣 𝑝 ≠ 𝑣 0 *)
          
11          Proph(𝑝, 𝑣 𝑝 ) ∗ (𝑣 0, 𝑡 0 ) = 𝐻¯0 (𝑘) ∗ SR(𝑘, 𝑣 0, 𝑡 0 ) ∗ 𝑣 𝑝 ≠𝑣 0 ∗ . . .
               . . . ∗ AU(Φ) ∗ Proph(tid, _)
             
12
             n                                                                    𝛾𝑠𝑦 (tid)        𝛾𝑠𝑦 (tid)       o
13             . . . ∗ Proph(tid, _) ∗ Pending(𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0 Φ) ∗ ½ 𝐻 0                 ∗ ½ 𝐻0           ∗ Tok
             n             𝛾𝑟                                                                                        o
14             . . . ∗ • 𝑅 ∗ tid ∉ 𝑅 ∗ State(tid, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) ∗ Reg(tid, 𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) ∗ Tok
                                           𝛾𝑟                        𝛾𝑟
15             (* Ghost update: • 𝑅             ⇛ • 𝑅 ∪ {tid}              *)
          n                                     𝛾𝑟                                                                           o
16            Proph(𝑝, 𝑣 𝑝 ) ∗ Tok ∗ ◦ {𝑡𝑖𝑑}         ∗ State(tid, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) ∗ SR(𝑘, 𝑣 0, 𝑡 0 ) ∗ MCS(𝑟, 𝑡, 𝐻 )
17        let 𝑣 = search 𝑟 𝑘 in
          n                               𝛾𝑟                                                              𝛾𝑠 o
18          Proph(𝑝, 𝑣 𝑝 ) ∗ Tok ∗ ◦ {𝑡𝑖𝑑} ∗ MCS(𝑟, 𝑡, 𝐻 ) ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ {(𝑘, 𝑡 ′ )}
19        Resolve 𝑝 to 𝑣;
          n                𝛾𝑟                      𝛾𝑠 o
20          Tok ∗ ◦ {tid} ∗ 𝑣 𝑝 =𝑣 ∗ (𝑘, 𝑣 𝑝 )
            Φ(𝑣 ) ∗ 𝑣 𝑝 =𝑣
          
21
           𝑝
22          Φ(𝑣)
23        𝑣
24        (* End application of logatom-intro *)
25          𝑣. MCS(Invtpl , Prothelp )(𝑟, 𝑀) ∗ 𝑀 (𝑘) = 𝑣

                                       Fig. 12. Outline for the proof of proposition (14).


template-level atomic triple. By storing all resources in an invariant, the resources can be accessed
in each atomic step, regardless of whether the operation has already passed its linearization point
or not.
   As Inv is an invariant, we must ensure that it is preserved in each atomic step. However, 𝐻 and 𝑡
change with each upsert, which means that these values must be existentially quantified by Inv.
Nevertheless, we need to ensure that the values 𝑡 and 𝐻 exposed in the representation predicate
MCS(𝑟, 𝑡, 𝐻 ) of the template-level atomic triples agree with the values stored in the authoritative
resources inside Inv. We do this by introducing an additional predicate MCS• (𝑟, 𝑡, 𝐻 ) that we also
add to the invariant. We can think of the predicates MCS• (𝑟, 𝑡, 𝐻 ) and MCS(𝑟, 𝑡, 𝐻 ) as providing
two complementary views at the abstract state of the data structure, one from the perspective of the
data structure’s implementation, and one from the perspective of the client of the template-level
atomic triples. Together, they provide the following important properties:
         view-upd
              MCS• (𝑟, 𝑡, 𝐻 ) ∗ MCS(𝑟, 𝑡, 𝐻 )                    view-sync
          MCS• (𝑟, 𝑡 ′, 𝐻 ′) ∗ MCS(𝑟, 𝑡 ′, 𝐻 ′)                  MCS• (𝑟, 𝑡, 𝐻 ) ∗ MCS(𝑟, 𝑡 ′, 𝐻 ′) ⊢ 𝑡 = 𝑡 ′ ∧ 𝐻 = 𝐻 ′

                                                                      36
Verifying Concurrent Multicopy Search Structures                                                                                ,,



 MCS(Invtpl , Prot) (𝑟, 𝑡, 𝑀) B ∃ 𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) ∗ (∀𝑘. (𝑀 (𝑘), _) = 𝐻¯ (𝑘)) ∗ Inv(Invtpl , Prot) (𝑟 )
                                                                                 𝛾𝑠          𝛾𝑡
         Inv(Invtpl , Prot) (𝑟 ) B ∃ 𝑡 𝐻 . MCS• (𝑟, 𝑡, 𝐻 ) ∗ • 𝐻                      ∗ •𝑡        ∗ Invtpl (𝑡, 𝐻 ) ∗ Prot(𝐻 )
                                    ∗ HInit(𝐻 ) ∗ HUnique(𝐻 ) ∗ HClock(𝑡, 𝐻 )

                 Prothelp (𝐻 ) B ∃ 𝑅. • 𝑅
                                              𝛾𝑟
                                                    ∗
                                                        ∗
                                                        tid ∈𝑅
                                                                 ∃ 𝑘 𝑣 𝑝 𝑡 0, Φ Tok. Reg(tid, 𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok)

                                                                    𝛾𝑠𝑦 (tid)
Reg(tid, 𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) B Proph(tid, _) ∗ ½ 𝐻                         ∗ State(tid, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok)
                                                   𝛾𝑠𝑦 (tid)
 State(tid, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) B ∃ 𝐻 . ½ 𝐻
                                   ∗ (Pending(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ) ∨ Done(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok))

    Pending(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ) B AU(Φ) ∗ (∀𝑡 . (𝑘, (𝑣 𝑝 , 𝑡)) ∈ 𝐻 ⇒ 𝑡 < 𝑡 0 )

  Done(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) B (Φ(𝑣 𝑝 ) ∨ Tok) ∗ (∃𝑡 . (𝑘, (𝑣 𝑝 , 𝑡)) ∈ 𝐻 ∧ 𝑡 ⩾ 𝑡 0 )
                                                         𝛾𝑠
                   SR(𝑘, 𝑣, 𝑡) B ◦ {(𝑘, (𝑣, 𝑡))}

     Fig. 13. Full definition of client-level representation predicate and invariants of helping protocol.


The rule view-upd says that both predicates are required in order to update the views of the data
structure. This occurs in the proof of upsert when both the invariant as well as the precondition of
the template-level atomic triple are accessed at the linearization point. The rule view-sync ensures
that both copies are always in sync. The predicates MCS• (𝑟, 𝑡, 𝐻 ) and MCS(𝑟, 𝑡, 𝐻 ) are defined
using a combination of authoritative and exclusive RAs. We omit the precise definitions here as
they are unimportant for our discussion.
   Let us now return to the proof outline in Figure 12. After creating the two prophecies tid and 𝑝,
the proof uses rule au-abort to obtain access to the precondition MCS(Invtpl , Prothelp ) (𝑟, 𝑀) and
opens it to extract the invariant Inv(Invtpl , Prothelp ) (𝑟 ) (line 7). As the invariant is persistent, it
can be assumed before each of the remaining steps of the proof, though we must also show that
it is preserved by each step. In preparation for the call to search, the proof proceeds on line 8
by opening the invariant Inv(Invtpl , Prothelp ) (𝑟 ) and using rule auth-set-snap to take a snapshot
       𝛾𝑠
 ◦𝐻 0 of the authoritative upsert history, whose value at this point we denote by 𝐻 0 . The proof
then lets (𝑣 0, 𝑡 0 ) B 𝐻¯0 (𝑘), which implies (𝑘, (𝑣 0, 𝑡 0 )) ∈ 𝐻 0 . This fact and rule auth-set-frag then
                          𝛾𝑠
yield ◦ {(𝑘, (𝑣 0, 𝑡 0 ))} = SR(𝑘, 𝑣 0, 𝑡 0 ) (line 9).
   The proof now case splits on whether the value 𝑣 𝑝 prophesied by 𝑝 satisfies 𝑣 0 ≠ 𝑣 𝑝 or 𝑣 0 = 𝑣 𝑝
(line 10). The case 𝑣 0 = 𝑣 𝑝 where the call to search completes without interference from any
upserts on 𝑘 is straightforward. It implies (𝑀 (𝑘), _) = 𝐻¯0 (𝑘) = (𝑣 𝑝 , _), which allows us to commit
the atomic triple right away, i.e., without requiring any help from an upsert thread. We therefore
show only the case 𝑣 0 ≠ 𝑣 𝑝 in detail, which involves the helping protocol captured by the predicate
Prothelp .
   The predicate Prothelp keeps track of the search threads that require helping from upsert
threads. The IDs of these threads are stored in an authoritative set 𝑅 at ghost location 𝛾𝑟 . In the
case 𝑣 0 ≠ 𝑣 𝑝 of the proof, we must therefore register the thread ID tid with the invariant by
replacing 𝑅 with 𝑅 ∪ {tid} using rule auth-set-upd (line 15). The predicate Prothelp (𝐻 0 ) needs to

                                                               37
,,                                                Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


be preserved by this ghost update, because it is part of the invariant Inv. This forces the proof to
transfer some of its thread-local resources, captured by the predicate Reg(tid, 𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok),
to the invariant. The lines in the proof preceding the update of 𝑅 establish that this predicate
holds. In particular, the proof transfers the predicate State(tid, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) to Prothelp (𝐻 0 ). This
predicate keeps track of the current state of thread tid in the helping protocol. Initially, the thread
is in state Pending(𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ). To establish this predicate, the proof needs to transfer AU(Φ)
to the invariant, as explained earlier. It also needs to ensure (∀𝑡 . (𝑘, (𝑣 𝑝 , 𝑡)) ∈ 𝐻 0 ⇒ 𝑡 ≤ 𝑡 0 , which
follows from 𝐻¯0 (𝑘) = (𝑣 0, 𝑡 0 ) and HUnique(𝐻 0 ). Finally, the proof creates a fresh exclusive token
Tok that it will later trade in for the receipt Φ(𝑣 𝑝 ) of the committed atomic triple.
    A minor technicality at this point in the proof is that we must also turn the predicate State into
an Iris invariant before we add it to Reg(tid, 𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok). The reason is that the search proof
needs to be able to conclude that the Φ it will receive back from the invariant later after the call to
search returns, is the same as the one it registers with the helping protocol before calling search.
By turning State into an invariant, the predicate becomes a duplicable resource. This allows the
proof to keep one copy of the predicate in its thread-local proof context. An unfortunate side effect
of this solution is that, as an invariant, the predicate State cannot expose the upsert history as a
parameter. However, the definition of State still depends on the exact value of the upsert history
that is stored in the authoritative resource in the invariant. We solve this minor technicality by
additionally storing the upsert history at an auxiliary fractional resource at the ghost location
𝛾 sy (tid) . The invariant maintains one such ghost resource for each thread tid that is registered for
helping. We split this resource half-way between the predicates Reg and State. This ensures that
the upsert history 𝐻 referenced in State is indeed equal to the authoritative one.
    Line 13 shows the proof state after Pending(𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ) has been established and the new
                   𝛾 sy (tid)
resource 𝐻 0                  has been allocated and split into the two halves. These resources are then
assembled into State(tid, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) and then Reg(tid, 𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) as shown on line 14.
Assembling the latter also requires the proof to give up ownership of Proph(tid, _). By storing these
prophecy resources in Prothelp (𝐻 0 ) for all threads in 𝑅, the proof can use the fact that prophecy
resources are exclusive to conclude tid ∉ 𝑅 before adding tid to 𝑅. This is needed to show that the
assembled Reg(tid, 𝐻 0, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) can indeed be transferred to the invariant during the ghost
update.
    After the ghost update of 𝑅, we arrive at line 16, at which point we are ready to perform the call
to search. After using the invariant and SR(𝑘, 𝑣 0, 𝑡 0 ) to obtain the atomic triple for search from
SearchSpec(search, Invtpl ), the proof opens the precondition MCS(𝑟, 𝑀) of search once again
and extracts the precondition MCS(𝑟, 𝑡, 𝐻 ) for the template-level atomic triple. Here, 𝑡 and 𝐻 refer
to the new values of the global clock and upsert history at the linearization point of search. Next,
the proof executes the call to search using the template-level atomic triple, which leaves us with
the new proof state on line 18. We can now open the invariant again to obtain a new snapshot
       𝛾𝑠
 𝐻 ′ of the upsert history and use rule view-sync to conclude that the snapshot value 𝐻 ′ is the
same as the 𝐻 in MCS(𝑟, 𝑡, 𝐻 ). Together with (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 , we can then establish the persistent
                                    𝛾𝑠
proposition {(𝑘, (𝑣, 𝑡 ′))} . After resolving the prophecy 𝑝 on line 20, we additionally establish
𝑣 𝑝 = 𝑣.
                                                                                                           𝛾𝑟
  To complete the proof, we now open Inv(Invtpl , Prothelp ) and use the resource ◦ {tid} to
                                                                                                         𝛾𝑠
conclude that tid ∈ 𝑅. That is, we have Reg(tid, 𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok) and can now use (𝑘, (𝑣 𝑝 , 𝑡))
                                                                                          

and the fractional resources at ghost location 𝛾 sy (tid) to show that the thread must be in state
Done(𝐻, 𝑘, 𝑣 𝑝 , 𝑡 0, Φ, Tok). Since the thread still owns the unique token Tok, it can be exchanged for


                                                       38
Verifying Concurrent Multicopy Search Structures                                                        ,,


Φ(𝑣 𝑝 ) in the invariant (line 21). Using Φ(𝑣 𝑝 ), the proof can then complete the initial application of
the rule logatom-intro to show the atomic triple of search.

  Proof of Proposition (11). By comparison, proving the client-level specification of upsert from its
template-level specification is relatively simple. Recall that the goal here is to prove
     D                                  E               D                                     E
       𝑀. MCS(Invtpl , Prothelp ) (𝑟, 𝑀) upsert 𝑟 𝑘 𝑣 MCS(Invtpl , Prothelp ) (𝑟, 𝑀 [𝑘 ↣ 𝑣])

assuming UpsertSpec(upsert, Invtpl ). Let us for a moment assume that we have already estab-
lished Updatable(Prothelp ). We can then use this property to obtain the template-level atomic
triple for upsert from UpsertSpec(upsert, Invtpl ). Before the call to upsert, we open the pre-
condition MCS(Invtpl , Prothelp ) (𝑟, 𝑀) to obtain MCS(𝑟, 𝑡, 𝐻 ). Moreover, we use the properties
(∀𝑘. (𝑀 (𝑘), _) = 𝐻¯ (𝑘)) and HClock(𝑡, 𝐻 ) from the invariant to conclude that 𝑡𝑘 < 𝑡 for all 𝑡𝑘 , 𝑣𝑘
such that (𝑘, (𝑣𝑘 , 𝑡𝑘 )) ∈ 𝐻 . Applying the atomic triple gives the postcondition MCS(𝑟, 𝑡 + 1, 𝐻 ∪
{(𝑘, (𝑣, 𝑡))}). It then follows that we have for all 𝑘 ′: 𝐻 ∪ {(𝑘,¯ (𝑣, 𝑡))}(𝑘 ′) = 𝐻¯ [𝑘 ↣ (𝑣, 𝑡)] (𝑘 ′) =
(𝑀 [𝑘 ↣ 𝑡] (𝑘 ′), _). This allows us to establish the desired postcondition MCS(𝑟, 𝑀 [𝑘 ↣ 𝑣]).
   Finally, we need to show that Updatable(Prothelp ) is valid at the point where the template-level
atomic triple of upsert is applied. That is, we must show that we can reestablish Prothelp (𝐻 ∪
{(𝑘, (𝑣, 𝑡))}), assuming Prothelp (𝐻 ) is true. In this proof, we make use of the fact that HClock(𝑡, 𝐻 )
holds, which we obtain from the invariant. The important point to note here is that any search
thread tid ∈ 𝑅 that was in state Pending(𝐻, 𝑘, 𝑣, 𝑡 0, Φ) where 𝑡 ⩾ 𝑡 0 and thus waiting to be helped
by the upsert thread performing the ghost update of 𝐻 , cannot remain in this state because
Pending(𝐻 ∪ {(𝑘, (𝑣, 𝑡))} , 𝑘, 𝑣, 𝑡 0, Φ) is unsatisfiable. The ghost update is, thus, forced to commit the
atomic triples of all these search threads using their update tokens via rule au-commit. It can do
this because the postcondition of these triples are satisfied after 𝐻 has been updated. The reasoning
here follows similar steps as the proof of the postcondition of upsert above. After committing the
atomic triple, the receipt Φ(𝑣) is transferred to Prothelp (𝐻 ∪ {(𝑘, (𝑣, 𝑡))}) as part of the new state
Done(𝐻 ∪ {(𝑘, (𝑣, 𝑡))} , 𝑘, 𝑣, 𝑡 0, Φ, Tok) for each of these threads.

A.5     Invariant for LSM DAG Template
We next discuss the details of the template-specific invariant InvLSM (𝑟, 𝑡, 𝐻 ) that we use for the
proof of the LSM DAG template. It is shown in Figure 14. For presentation purposes, we omit the
additional flow interface for encoding the inset flow and the related predicates needed for the proof
of the maintenance operation. The full details of the Iris development can be found on GitHub.6
   The parameters 𝑡 and 𝐻 are to be interpreted as the current clock value and the current upsert
history. The existentially quantified variable 𝐼 is the current global flow interface used for encoding
the contents-in-reach flow. As discussed in §6.2, the invariant consists of two parts: a global part
described by the predicate G and a local part that holds for every node in the data structure. The
set of nodes 𝑁 of the data structure graph is implicitly captured by the domain dom(𝐼 ) of the flow
interface 𝐼 .
   We discuss each part of Figure 14 in detail, starting with the predicate G(𝑟, 𝑡, 𝐻, 𝐼 ):
      • We use an authoritative camera of flow interfaces at ghost location 𝛾𝐼 to keep track of the
        global interface 𝐼 , which is composed of singleton interfaces 𝐼𝑛 for each node 𝑛 ∈ dom(𝐼 ).
        The 𝐼𝑛 are tied to the implementation-specific physical representation of the individual nodes
        via the predicates NL and NS as explained below.

6 https://github.com/nyu-acsys/template-proofs/multicopy



                                                           39
,,                                                Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


                          InvLSM (𝑟, 𝑡, 𝐻 ) B ∃ 𝐼 .
                               G(𝑟, 𝑡, 𝐻, 𝐼 )
                               ∗
                             ∗ 𝑛 ∈dom(𝐼 ) ∃𝑏𝑛 𝐶𝑛 𝑄𝑛 . L(𝑏𝑛 , 𝑛, NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ))
                                                    ∗ NS (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐻 )
                                                 𝛾𝐼                 𝛾𝑓
                where G(𝑟, 𝑡, 𝐻, 𝐼 ) B • 𝐼            ∗ • dom(𝐼 )        ∗ 𝐼 .in = 𝜆0 ∗ inFP(𝑟 )
                                                      𝛾𝑓
                              inFP(𝑛) B ◦ {𝑛}
                     NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) B ∃es. node(𝑟, 𝑛, es, 𝐶𝑛 )
                                     𝛾𝑒 (𝑛)       𝛾𝑐 (𝑛)        𝛾𝑞 (𝑛)        𝛾𝑠
                            ∗ ½es           ∗ ½𝐶𝑛        ∗ ½𝑄𝑛         ∗ ◦ 𝐶𝑛

                  NS (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐻 ) B ∃es, 𝐼𝑛 .
                                      𝛾𝑒 (𝑛)       𝛾𝑐 (𝑛)       𝛾𝑞 (𝑛)
                            ∗ ½es            ∗ ½𝐶𝑛        ∗ ½𝑄𝑛
                                   𝛾𝐼
                            ∗ ◦𝐼𝑛 ∗ dom(𝐼𝑛 ) = {𝑛} ∗ inFP(𝑛) ∗ closed(es)
                            ∗ 𝐼𝑛 .out = 𝜆𝑛 ′ . 𝜒 ({(𝑘, 𝑄𝑛 (𝑘)) | 𝑘 ∈ es(𝑛 ′
                                                                         ) ∧ 𝑘 ∈ dom(𝑄𝑛 )})
                            ∗ 𝑛 = 𝑟 ? 𝐵𝑛 = 𝐻 ∗ 𝐼𝑛 .in = 𝜆0 : True
                                                 ¯
                              ∗
                            ∗ 𝑘 ∈KS • ts(𝐵𝑛 (𝑘))
                                                         𝛾 cir (𝑛) (𝑘 )

                            ∗ 𝜙 1 (𝑛, 𝑄𝑛 , es) ∗ 𝜙 2 (𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐼𝑛 )

                           closed(es) B ∀𝑛 ′ . es(𝑛 ′) ≠ ∅ ⇒ inFP(𝑛 ′)
                                    𝐵𝑛 B 𝜆𝑘. (𝑘 ∈ dom(𝐶𝑛 ) ? 𝐶𝑛 (𝑘) : 𝑄𝑛 (𝑘))
                        𝜙 1 (𝑛, 𝑄𝑛 , es) B ∀𝑘. 𝑄𝑛 (𝑘) = ⊥ ∨ (∃𝑛 ′ . 𝑘 ∈ es(𝑛 ′))
                    𝜙 2 (𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐼𝑛 ) B ∀𝑘 𝑝. 𝐼𝑛 .in(𝑛) (𝑘, 𝑝) > 0 ⇒ 𝐵𝑛 (𝑘) = 𝑝

                        Fig. 14. The invariant for the multicopy structure template.

                                           𝛾𝑓
    • The ghost resource • dom(𝐼 )         keeps track of the footprint of the data structure using
      the authoritative camera of sets of nodes. We use this resource to maintain the invariant
      of traverse that the currently visited node 𝑛 remains part of the data structure while 𝑛 is
      unlocked.
    • We require that the global flow interface 𝐼 has no inflow (𝐼 .in = 𝜆0 ), as required for our
      encoding of contents-in-reach. That is, 𝜆0 maps all nodes to the empty multiset, the unit 0 of
      the flow domain.
    • The condition inFP(𝑟 ) guarantees that 𝑟 is always in the domain of the data structure.
   The resources for a node 𝑛 are split between the predicates NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) and NS (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐻 ).
The latter is always owned by the invariant whereas the former is protected by 𝑛’s lock and
transferred between the invariant and the thread’s local state upon locking the node and vice versa
upon unlocking, as usual. We next discuss NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ):
    • The first conjunct is the implementation-specific node predicate node(𝑟, 𝑛, es, val(𝐶𝑛 )). For
      each specific implementation of the template, this predicate must tie the physical representa-
      tion of the node 𝑛 to its physical contents val(𝐶𝑛 ) : KS ⇀ V and a function 𝑒𝑠 : 𝔑 → ℘(KS),
      which captures the edgesets of 𝑛’s outgoing edges.
    • The fractional resources at ghost locations 𝛾𝑒 (𝑛) , 𝛾𝑐 (𝑛) , and 𝛾𝑞 (𝑛) ensure that the predicates
      NL and NS agree on the values of es, 𝐶𝑛 , and 𝑄𝑛 even when 𝑛 is locked.

                                                           40
Verifying Concurrent Multicopy Search Structures                                                           ,,

                                      𝛾𝑠                                          𝛾𝑠
    • The ghost resource ◦ 𝐶𝑛 when combined with • 𝐻 implies 𝐶𝑛 ⊆ 𝐻 , which captures
       Invariant 3.
    • The final conjunct of NL guarantees sole ownership of the global clock by a thread holding
       the lock on the root node.
   Moving on to NS (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐻 ), this predicate contains those resources of 𝑛 that are available
to all threads at all times:
                            𝛾𝐼
    • The resource ◦𝐼𝑛 guarantees that all the singleton interfaces 𝐼𝑛 compose to the global
       interface 𝐼 , thus, satisfying the flow equation. Similarly, the predicate inFP(𝑛) guarantees
       that 𝑛 remains in the data structure at all times. The predicate closed(es) ensures that the
       outgoing edges of 𝑛 point to nodes which are again in the data structure. Together with the
       condition inFP(𝑟 ), this guarantees that all nodes reachable from 𝑟 must be in dom(𝐼 ).
    • The next conjunct of NS defines the outflow of the singleton interface 𝐼𝑛 according to
       Equation (7) of our flow encoding of contents-in-reach. Note that, even though 𝐼𝑛 is not
       shared with the predicate NL , only its inflow can change when 𝑛 is locked, because the
       outflow of the interface is determined by 𝑄𝑛 and es, both of which are protected by 𝑛’s lock.
    • The constraint 𝐵𝑛 = 𝐻¯ holds if 𝑟 = 𝑛 and implies Invariant 1. We further require here that
       the interface of the root node has no inflow (𝐼𝑛 .in = 𝜆0 ), a property that we need in order to
       prove that upsert maintains the flow-related invariants. Moreover, we use for every key 𝑘
       an authoritative maxnat resource at ghost location 𝛾 cir (𝑛) (𝑘) to capture Invariant 2.
    • The last two conjuncts of NS complete our encoding of contents-in-reach and ensure that we
       must indeed have 𝐵𝑛 = 𝐶 ir (𝑛) at all atomic steps.
   Finally, we note that Invariant 4, which is needed for the proof of upsert, is already captured by
the predicate HClock(𝑡, 𝐻 ) included in the full invariant Inv(InvLSM , Prot) (𝑟 ).

A.6     Detailed Proof of Template Operations
We now have all the ingredients to proceed with the proof of the template operations.
A.6.1 Proof of search. The proof relies on the specification of the implementation-specific helper
functions provided in Figure 8.
   Figure 15 provides the outline of the proof of search. The intermediate assertions shown
throughout the proof represent the relevant information from the proof context at the corresponding
point. By convention, all the newly introduced variables are existentially quantified. Note that the
condition SR(𝑘, 𝑣 0, 𝑡 0 ) is persistent and, hence, holds throughout the proof. Moreover, the invariant
 Inv(InvLSM , Prot) (𝑟 ) is maintained throughout the proof since search does not modify any shared
resources. We therefore do not include these resources explicitly in the intermediate assertions.
   As most of the actual work is done by the recursive function traverse, we start with its atomic
specification:
                                                    𝛾 cir (𝑛) (𝑘 )
      Inv(InvLSM , Prot) (𝑟 ) −∗ inFP(𝑛) −∗ ◦ 𝑡 1                    −∗ 𝑡 0 ≤ 𝑡 1 −∗
            𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) traverse 𝑟 𝑛 𝑘 𝑣. ∃𝑡 . MCS(𝑟, 𝑡, 𝐻 ) ∗ (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 ∗ 𝑡 0 ⩽ 𝑡 ′
                                                                     ′

Recall the traversal invariant 𝑡 0 ⩽ ts(𝐶 ir (𝑛) (𝑘)) that we used in our informal proof of search recency.
                          𝛾
The ghost resource ◦ 𝑡 1 cir (𝑛) (𝑘 ) , together with 𝑡 0 ⩽ 𝑡 1 in the precondition of the above specification
precisely capture this invariant. In addition, traverse assumes the invariant Inv(InvLSM , Prot) (𝑟 )
and requires that 𝑛 must be a node in the graph, expressed by the predicate inFP(𝑛). The operation
then guarantees to return a value 𝑣 such that search recency holds.
  Let us for now assume that traverse satisfies the above specification and focus on the proof
of search. The precondition of search 𝑟 𝑘 assumes the invariant Inv(InvLSM , Prot) (𝑟 ) and the

                                                          41
,,                                                                    Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies

     n                                             o
 1       Inv(InvLSM , Prot) (𝑟 ) ∗ SR(𝑘, 𝑣 0, 𝑡 0 ) ∗ 𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 )
 2 let search 𝑟           𝑘 =
          n                                              𝛾 ts(cir (𝑟 ) (𝑘 ) )                     o
 3          inFP(𝑟 ) ∗ 𝐻 1 (𝑘) = 𝐵𝑟 (𝑘) ∗ ◦ 𝐵𝑟 (𝑘)
                       ¯                                                      ∗ 𝑡 0 ≤ ts(𝐻¯1 (𝑘))
          n                  𝛾
                                                      o
 4          inFP(𝑟 ) ∗ ◦ 𝑡 1 cir (𝑟 ) (𝑘 ) ∗ 𝑡 0 ≤ 𝑡 1 ∗ 𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 )
 5        traverse 𝑟 𝑟 𝑘
 6       𝑣. ∃𝑡 ′ . MCS(𝑟, 𝑡, 𝐻 ) ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻
 7
     n                                                         𝛾 cir (𝑛) (𝑘 )
                                                                                           o
 8       Inv(InvLSM , Prot) (𝑟 ) ∗ inFP(𝑛) ∗ ◦ 𝑡 1                              ∗ 𝑡 0 ≤ 𝑡 1 ∗ 𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 )
 9 let rec traverse 𝑟             𝑛 𝑘 =
10       lockNode 𝑛;
         n                                𝛾 ts(cir (𝑛) (𝑘 ) )                o
11         NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ ◦ 𝐵𝑛 (𝑘)                     ∗ 𝑡 0 ≤ 𝐵𝑛 (𝑘)
12       match inContents 𝑟 𝑛 𝑘 with
13       | Some 𝑣 ->
           
             N (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ 𝑘 ∈ dom(val(𝐶𝑛 )) ∗ 𝑣 = val(𝐶𝑛 )(𝑘)
            L
14
15           NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ (𝑣, 𝑡 ′ ) = 𝐶𝑛 (𝑘)
16         (* Linearization point *)
             N (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ 𝑡 0 ≤ ts(𝐶𝑛 (𝑘)) ∗ (𝑣, 𝑡 ′ ) = 𝐶𝑛 (𝑘)
           
            L
17
18           NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ 𝑡 0 ⩽ 𝑡 ′ ∗ MCS(𝑟, 𝑡, 𝐻 )
19         unlockNode 𝑛; 𝑣
20           𝑣 . ∃𝑡 ′ . MCS(𝑟, 𝑡, 𝐻 ) ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ 𝑡 0 ⩽ 𝑡 ′
21       | None ->
           
             N (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ 𝑘 ∉ dom(val(𝐶𝑛 ))
            L
22
23           NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ 𝑘 ∉ dom(𝐶𝑛 )
24         match findNext 𝑟 𝑛 𝑘 with
25         | Some 𝑛 ′ ->
                node(𝑟, 𝑛, es, 𝐶𝑛 ) ∗ · · · ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ 𝑘 ∉ dom(𝐶𝑛 ) ∗ 𝑘 ∈ es(n ′ )
              
26
              n                                                 ′
                                                                                   o
                NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ inFP(𝑛 ′ ) ∗ ◦ 𝑡 1 cir (𝑛 ) (𝑘 ) ∗ 𝑡 0 ≤ 𝑡 1
                                                           𝛾
27

28             unlockNode 𝑛;
               n                          ′
                                                             o
                 inFP(𝑛 ′ ) ∗ ◦ 𝑡 1 cir (𝑛 ) (𝑘 ) ∗ 𝑡 0 ≤ 𝑡 1 ∗ 𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 )
                                   𝛾
29

30              traverse 𝑟 𝑛 ′ 𝑘
31                 𝑣. ∃𝑡 ′ . MCS(𝑟, 𝑡, 𝐻 ) ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ 𝑡 0 ⩽ 𝑡 ′
32          | None ->
                  node(𝑟, 𝑛, es, 𝐶𝑛 ) ∗ · · · ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ 𝑘 ∉ dom(val(𝐶𝑛 )) ∗ ∀𝑛 ′ . 𝑘 ∉ es(𝑛 ′ )
                
33
                
34                node(𝑟, 𝑛, es, 𝐶𝑛 ) ∗ · · · ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ 𝑘 ∉ dom(𝐵𝑛 (𝑘))
                
35                NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) ∗ ts(𝐵𝑛 (𝑘)) = 0
36              (* Linearization point *)
                
                  N (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ 𝑡 0 = ts(𝐵𝑛 (𝑘)) = 0 ∗ MCS(𝑟, 𝑡, 𝐻 )
                 L
37
38                NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) ∗ (𝑘, (□, 0)) ∈ 𝐻 ∗ 𝑡 0 = 0 ∗ MCS(𝑟, 𝑡, 𝐻 )
39              unlockNode 𝑛; □
40       𝑣. ∃𝑡 ′ . MCS(𝑟, 𝑡, 𝐻 ) ∗ (𝑘, (𝑣, 𝑡 ′ )) ∈ 𝐻 ∗ 𝑡 0 ⩽ 𝑡 ′

                                                           Fig. 15. Proof of search.




                                                                                42
Verifying Concurrent Multicopy Search Structures                                                                    ,,


predicate SR(𝑘, 𝑣 0, 𝑡 0 ) (line 1). We must, hence, use these to establish the precondition for the call
traverse 𝑟 𝑛 𝑘 on line 5. To this end, we open the invariant from which we can directly obtain
                                                                                          𝛾𝑠
inFP(𝑟 ). Next, we unfold the definition of SR(𝑘, 𝑣 0, 𝑡 0 ) to obtain ◦ {(𝑘, (𝑣 0, 𝑡 0 )} . Snapshotting
       𝛾𝑠
 • 𝐻 1 in the invariant for the current upsert history 𝐻 1 , we can conclude (𝑘, (𝑣 0, 𝑡 0 ) ∈ 𝐻 1
and therefore 𝑡 0 ≤ ts(𝐻¯1 (𝑘)). From NS (𝑟, 𝑟, 𝐶𝑟 , 𝑄𝑟 , 𝐻 1 ) in the invariant we can further deduce
                                   𝛾 cir (𝑟 ) (𝑘 )
𝐻¯1 (𝑘) = 𝐵𝑟 (𝑘) and ◦ ts(𝐵𝑟 (𝑘))                  (line 3). By substituting both ts(𝐻¯1 (𝑘)) and ts(𝐵𝑟 (𝑘)) with
a fresh existentially quantified variable 𝑡 1 we obtain the precondition of traverse (line 4). We now
commit the atomic triple of search on the call to traverse and immediately obtain the desired
postcondition.

   Proof of traverse. Finally, we prove the assumed specification of traverse. The proof starts at
line 8. The thread first locks node 𝑛 which yields ownership of the predicate NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ). At
                                                                                                      𝛾 cir (𝑛) (𝑘 )
this point, we also open the invariant to take a fresh snapshot of the resource • ts(𝐵𝑛 (𝑘))
to conclude 𝑡 0 ≤ ts(𝐵𝑛 (𝑘)) from the precondition of traverse (line 11). Next, the thread executes
inContents 𝑟 𝑛 𝑘. The precondition of this call, i.e. node(𝑟, 𝑛, es, val(𝐶𝑛 )), is available to us as part
of the predicate NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ). Depending on the return value 𝑣 of inContents we end up with
two subcases.
   In the case where 𝑥 = Some(𝑣), we know 𝑘 ∈ dom(val(𝐶𝑛 )) and 𝑣 = val(𝐶𝑛 ) (𝑘) which lets
us conclude (𝑣, 𝑡 ′) = 𝐶𝑛 (𝑘) for some 𝑡 ′ (line 15). The call to unlockNode on line 19 will be the
linearization point of this case. To obtain the desired postcondition of the atomic triple, we first
retrieve NS (𝑟, 𝑛, 𝐶𝑛 , 𝐵𝑛 , 𝐻 ) from the invariant and open its definition. From 𝑘 ∈ dom(𝐶𝑛 ) and the
definition of 𝐵𝑛 we first obtain 𝐵𝑛 (𝑘) = 𝐶𝑛 (𝑘). This leaves us with the proof context on line 17.
Now we access the precondition MCS(𝑟, 𝑡, 𝐻 ) of the atomic triple and sync it with the view of
                                                                       𝛾𝑠
𝐻 and 𝑡 in the invariant. Moreover, we use the resource ◦ 𝐶𝑛 to infer 𝐶𝑛 ⊆ 𝐻 , which then
implies (𝑘, (𝑣, 𝑡 ′)) ∈ 𝐻 (line 18). The call to unlockNode returns NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) to the invariant
and commits the atomic triple, which concludes this case.
   For the second case where the return value of inContents is 𝑥 = None, we have 𝑘 ∉ dom(𝐶𝑛 )
and the thread calls findNext. Here, we unfold NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) to retrieve node(𝑟, 𝑛, es, val(𝐶𝑛 )),
which is needed to satisfy the precondition of findNext. We then end up again with two subcases:
one where there is a successor node 𝑛 ′ such that 𝑘 ∈ es(𝑛 ′), and the other where no such node
exists. Let us consider the first subcase, which is captured by the proof context on line 26. Now,
before the thread unlocks 𝑛, we have to reestablish the precondition of traverse for the recursive
call on line 30. To do this, we first open the invariant and retrieve NS (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐻 ). From predicate
closed(es), we obtain the resource inFP(𝑛 ′) because es(𝑛 ′) ≠ ∅. inFP(𝑛 ′) is the first piece for the
precondition of traverse. To obtain the remaining pieces, we must retrieve NS (𝑟, 𝑛 ′, 𝐶𝑛′ , 𝑄𝑛′ , 𝐻 )
from the invariant. This is possible because we can infer 𝑛 ′ ∈ dom(𝐼 ) using inFP(𝑛 ′).
   We first observe that 𝑘 ∉ dom(𝐶𝑛 ) implies 𝐵𝑛 (𝑘) = 𝑄𝑛 (𝑘) and which together with 𝑘 ∈ es(𝑛 ′)
gives us
                                            𝐼𝑛 .out (𝑛 ′) (𝑘, 𝐵𝑛 (𝑘)) > 0.

From the fact that 𝐼𝑛 and 𝐼𝑛′ compose, we can conclude 𝐼𝑛′ .in(𝑛 ′) (𝑘, 𝐵𝑛 (𝑘)) > 0. It then follows
from the constraint 𝜙 2 (𝑛 ′, 𝐶𝑛 , 𝑄𝑛 , 𝐼𝑛′ ) that 𝐵𝑛′ (𝑘) = 𝐵𝑛 (𝑘). We can further take a fresh snapshot
                                  𝛾 cir (𝑛′ ) (𝑘 )                                                 𝛾 cir (𝑛′ ) (𝑘 )
of the resource • ts(𝐵𝑛′ (𝑘))                      to obtain our final missing piece ◦ ts(𝐵𝑛′ (𝑘))                  for
the precondition of traverse. Then substituting both 𝐵𝑛 (𝑘) and 𝐵𝑛′ (𝑘) by a fresh variable 𝑡 1
and folding predicate NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) we arrive at line 27. Unlocking 𝑛 transfers ownership of
NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) back to the invariant. The resulting proof context satisfies the precondition of the

                                                          43
,,                                            Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


recursive call to traverse, which we use to commit the atomic triple by applying the specification
of traverse inductively.
   We are left with the last subcase where 𝑛 has no successor for 𝑘 (line 33). Here, we proceed
similarly to the first case above: we conclude 𝐵𝑛 (𝑘) = 𝑄𝑛 (𝑘) from 𝑘 ∉ dom(𝐶𝑛 ) and use ∀𝑛 ′ . 𝑘 ∉
es(𝑛 ′) and 𝜙 1 (𝑛, 𝑄𝑛 , es) to conclude that 𝑄𝑛 (𝑘) = 𝐵𝑛 (𝑘) = 𝐶𝑛 (𝑘) = ⊥. This, in turn, implies
ts(𝐵𝑛 (𝑘)) = 0. After folding predicate NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) we arrive on line 35. The linearization point
in this case is at the point when 𝑛 is unlocked, so we access the precondition MCS(𝑟, 𝑡, 𝐻 ) of the
atomic triple and sync it with the view of 𝐻 and 𝑡 in the invariant. Using the property HInit(𝐻 )
from the invariant, we can conclude (𝑘, (□, 0)) ∈ 𝐻 . The call to unlockNode returns NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 )
to the invariant and commits the atomic triple. The postcondition then follows for 𝑡 ′ = 0 and 𝑣 = □,
which is the return value in this case.
   This completes the proof of search.

A.6.2 Proof of upsert. We now focus on proving the correctness of the upsert operation. Fig-
ure 16 shows the proof outline. The proof relies on the specification of the implementation-specific
helper function addContents provided in Figure 8. The specification simply says that when the
function succeeds, the copy of 𝑘 is updated to 𝑣 in 𝑉𝑟 = val(𝐶𝑟 ). In case it fails, then no changes are
made to 𝑉𝑟 .
   With everything needed for the proof of upsert in place, let us now walk through the proof
outline shown in Figure 16. We start with the invariant Inv(InvLSM , Prot) (𝑟 ) , the view shift as-
sumption on Prot, and the atomic precondition 𝑡 𝐻 . MCS(𝑟, 𝑡, 𝐻 ) . The invariant can be accessed
at each atomic step, but must also be reestablished after each step. Similarly, the atomic precondition
is accessible at each atomic step, and must either be used to generate the postcondition of the
atomic triple or the precondition must be reestablished.
   The thread first locks the root node, which transfers ownership of NL (𝑟, 𝑟, es, 𝐶𝑟 ) from the
invariant to the thread (line 10). At this point, we unfold the definition of NL (𝑟, 𝑟, es, 𝐶𝑟 ) (line 11)
as we will need the contained resources later in the proof. The thread now calls addContents to
update 𝑟 with the new value 𝑣 for 𝑘. This leaves us with two possible scenarios depending on
whether the return value res is true (line 14) or false (line 26).
   In the case where addContents fails (res = false), no changes have been performed. Here, we
simply fold NL (𝑟, 𝑟, es, 𝐶𝑟 ) again, unlock 𝑟 to transfer ownership of the node’s resources back to the
invariant, and commit the atomic triple on the recursive call to upsert.
   In the case where addContents succeeds (res = true), we obtained 𝑉𝑟′ = val(𝐶𝑟 ) [𝑘 ↣ 𝑣] from
its postcondition, where 𝑉𝑟′ is the new physical contents of the root node. The thread will next
call unlockNode to unlock the root node 𝑟 . This will be the linearization point of this branch
of the conditional expression. Hence, we will also have to update all ghost resources to their
new values at this point. To prepare committing the atomic triple, we first open the invariant
                                            𝛾𝑠          𝛾𝑡
 Inv(InvLSM , Prot) (𝑟 ) to retrieve • 𝐻 and •𝑡 . Then we define 𝐶𝑟′ = 𝐶𝑟 [𝑘 ↣ (𝑣, 𝑡)], which
together with 𝑉𝑟′ = val(𝐶𝑟 ) [𝑘 ↣ 𝑣] gives us 𝑉𝑟′ = val(𝐶𝑟′ ). We further define 𝐻 ′ = 𝐻 ∪ (𝑘, (𝑣, 𝑡)).
This leaves us in the proof state on line 16. Next, we access the precondition of the atomic triple to
obtain MCS(𝑟, 𝑡 1, 𝐻 1 ) for some fresh variables 𝑡 1 and 𝐻 1 . We then obtain MCS• (𝑟, 𝑡, 𝐻 ) from the
invariant and use rule view-sync to conclude 𝐻 1 = 𝐻 and 𝑡 1 = 𝑡 (line 17).
   The actual commit of the atomic triple involves several steps. First, we update all relevant ghost
resources where we use, in particular, the following rule for frame-preserving updates on fractional
resources:
                                            frac-upd
                                            (1, 𝑠) ⇝ (1, 𝑠 ′)

                                                   44
Verifying Concurrent Multicopy Search Structures                                                                                       ,,

     
 1   node(𝑟, 𝑟, es, 𝐶𝑟 )
 2    addContents 𝑟 𝑘 𝑡
                        ′    ′
 3 𝑣 . node(𝑟, 𝑟, es, 𝐶𝑟 ) ∗ 𝐶𝑟 = (𝑣 ? 𝐶𝑟 [𝑘 ↣ 𝑡] : 𝐶𝑟 )
   n        𝛾𝑡
                          o                 n            𝛾
                                                           o
 4 𝑞 • 𝑡        ∗ 𝑞 > 0 readClock () 𝑣. 𝑞 • 𝑡 𝑡 ∗ 𝑣 = 𝑡
   n        o                           n        𝛾𝑡
                                                    o
          𝛾
 5    • 𝑡 𝑡 incrementClock () • 𝑡 + 1
 6
     n                                                                            o
 7       Inv(InvLSM , Prot) (𝑟 ) ∗ (∀ 𝐻 𝑘 𝑡 𝑣. Prot(𝐻 ) ⇛ Prot(𝐻 ∪ {(𝑘, (𝑣, 𝑡))})) ∗ 𝑡 𝐻 . MCS(𝑡, 𝐻 )
 8 let upsert 𝑟           𝑘 𝑣 =
 9       lockNode 𝑟 ;
         
           N (𝑟, 𝑟, 𝐶𝑟 , 𝑄𝑟 )
         n L
10
                                                   𝛾𝑠       𝛾𝑐 (𝑟 ) o
11         node(𝑟, 𝑟, es, val(𝐶𝑟 )) ∗ · · · ∗ ◦ 𝐶𝑟    ∗ ½𝐶𝑟
12       let res = addContents 𝑟 𝑘 𝑣 in
13       if res then
           n                                     𝛾𝑠       𝛾𝑐 (𝑟 )                          o
14           node(𝑟, 𝑟, es, 𝑉𝑟′ ) ∗ · · · ∗ ◦ 𝐶𝑟    ∗ ½𝐶𝑟         ∗ 𝑉𝑟′ = val(𝐶𝑟 ) [𝑘 ↣ 𝑣]
15         (* Linearization point *)
           n                                     𝛾𝑠        𝛾𝑐 (𝑟 )           𝛾𝑠
                                                                                                                                 o
             node(𝑟, 𝑟, es, 𝑉𝑟′ ) ∗ · · · ∗ ◦ 𝐶𝑟                                ∗ •𝑡 𝑡 ∗ 𝐶𝑟′ = 𝐶𝑟 [𝑘 ↣ (𝑣, 𝑡)] ∗ 𝑉𝑟′ = val(𝐶𝑟′ )
                                                                                     𝛾
16                                                  ∗ ½𝐶𝑟          ∗ •𝐻
                                                      𝛾𝑠           𝛾𝑐 (𝑟 )        𝛾𝑠
             node(𝑟, 𝑟, es, val(𝐶𝑟′ )) ∗ · · · ∗ ◦ 𝐶𝑟
           (                                                                              𝛾 )
                                                         ∗ ½𝐶𝑟             ∗ •𝐻      ∗ •𝑡 𝑡
17
                    ∗ 𝐶𝑟′ = 𝐶𝑟 [𝑘 ↣ (𝑣, 𝑡)] ∗ 𝐻 ′ = 𝐻 ∪ {(𝑘, (𝑣, 𝑡))} ∗ MCS(𝑟, 𝑡, 𝐻 )
                                                𝛾𝑠            𝛾𝑠            𝛾𝑐 (𝑟 )                𝛾𝑐 (𝑟 )
18         (* Ghost updates: • 𝐻                     ⇛ • 𝐻′        , 1𝐶𝑟              ⇛ 1𝐶𝑟′                 ,
                                           𝛾𝑡                 𝛾𝑡                       𝛾 cir (𝑛) (𝑘 )            𝛾 cir (𝑛) (𝑘 )
19                                    •𝑡         ⇛ •𝑡 + 1          , • ts(𝐵𝑛 (𝑘))                       ⇛ •𝑡                      *)
                                                      𝛾𝑠        𝛾𝑐 (𝑟 )        𝛾𝑠       𝛾𝑡 
            node(𝑟, 𝑟, es, val(𝐶𝑟′ )) ∗ · · · ∗ ◦ 𝐶𝑟    ∗ ½𝐶𝑟′         ∗ • 𝐻 ′ ∗ •𝑡 + 1 
           
           
                                                                                          
                                                                                           
20
           
                                ∗ 𝐶𝑟′ = 𝐶𝑟 [𝑘 ↣ 𝑡] ∗ 𝐻 ′ = 𝐻 ∪ {(𝑘, (𝑣, 𝑡))} ∗ MCS(𝑟, 𝑡, 𝐻 ) 
                                                                                              
           
           n                                                                                                 o
                                          𝛾
             NL (𝑟, 𝑟, 𝐶𝑟′ , 𝑄𝑟 ) ∗ • 𝐻 ′ ∗ •𝑡 𝑡 ∗ 𝐶𝑟′ = 𝐶𝑟 [𝑘 ↣ 𝑡] ∗ 𝐻 ′ = 𝐻 ∪ {(𝑘, (𝑣, 𝑡))} ∗ MCS(𝑟, 𝑡, 𝐻 )
                                            𝑠     𝛾
21

22         unlockNode 𝑟
           n        𝛾𝑠
                                                                                          o
                                   𝛾𝑡
23            • 𝐻 ′ ∗ •𝑡 + 1 ∗ 𝐶𝑟′ = 𝐶𝑟 [𝑘 ↣ 𝑡] ∗ 𝐻 ′ = 𝐻 ∪ {(𝑘, (𝑣, 𝑡))} ∗ MCS(𝑟, 𝑡, 𝐻 )
24           MCS(𝑟, 𝑡 + 1, 𝐻 ∪ {(𝑘, (𝑣, 𝑡))})
25       else begin
           n                                     𝛾𝑠       𝛾𝑐 (𝑟 )                  o
26           node(𝑟, 𝑟, es, 𝑉𝑟′ ) ∗ · · · ∗ ◦ 𝐶𝑟    ∗ ½𝐶𝑟         ∗ 𝑉𝑟′ = val(𝐶𝑟 )
           
27           NL (𝑟, 𝑟, 𝐶𝑟 , 𝑄𝑟 )
28         unlockNode 𝑟 ;
29         upsert 𝑟 𝑘
30       end
31       MCS(𝑡 + 1, 𝐻 ∪ {(𝑘, 𝑡)})

                                                       Fig. 16. Proof of upsert.




         • We update the authoritative version of the upsert history at ghost location 𝛾𝑠 in the invariant
           from 𝐻 to 𝐻 ′, using rule auth-set-upd.
         • We use the pendent of the rule auth-set-upd for the authoritative maxnat camera to update
           the global clock at ghost location 𝛾𝑡 in the invariant from 𝑡 to 𝑡 + 1.

                                                                       45
,,                                              Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


   • We use rule frac-upd to update the resource holding the root’s contents at location 𝛾𝑐 (𝑟 ) from
      𝐶𝑟 to 𝐶𝑟′ by reassembling the full resource from the half owned by the invariant, respectively,
      the half owned by the local proof context. After the update, the resource is split again into
      two halves, with one half returned to the invariant.
   • We use the pendent of the rule auth-set-upd for the authoritative maxnat camera to update the
      resource holdings the roots contents-in-reach for 𝑘 at ghost location 𝛾 cir (𝑟 ) (𝑘) from ts(𝐵𝑟 (𝑘))
      to 𝑡. This is possible because 𝐵𝑟 = 𝐻¯ and HClock(𝑡, 𝐻 ) hold according to the invariant, which
      together imply ts(𝐵𝑟 (𝑘)) < 𝑡.
This leaves us with the new proof context shown on line 20. We then reassemble the predicate
node(𝑟, 𝑟, es, 𝑉𝑟′) from the proof context at line 20 to satisfy the precondition of unlockNode. We
                                                              𝛾𝑠
have all the relevant pieces available, except for ◦ 𝐶𝑟′ . We obtain this remaining piece by
                        𝛾𝑠
observing that ◦ 𝐶𝑟          implies 𝐶𝑅 ⊆ 𝐻 ′ which in turn implies 𝐶𝑟′ ⊆ 𝐻 ′ by definition of 𝐶𝑟′ and
                                                     𝛾𝑠                                              𝛾𝑠
𝐻 ′. Using rule auth-set-snap we obtain ◦ 𝐻 ′ , which we can rewrite to ◦ (𝐻 ′ ∪ 𝐶𝑟′ ) using
the previously derived equality 𝐻 ′ = 𝐻 ′ ∪ 𝐶𝑟′ . Applying rule auth-set-frag, we can then infer
         𝛾𝑠        𝛾𝑠
 ◦ 𝐻 ′ ∗ ◦ 𝐶𝑟′ and after throwing away the first conjunct, we are left with the desired missing
piece.
   The call to unlockNode then returns node(𝑟, 𝑟, es, 𝑉𝑟′) to the invariant, leaving us in the state
shown on line 23. Finally, we use rule view-upd to update the client’s and invariant’s views of the
data structures state to MCS(𝑟, 𝑡 + 1, 𝐻 ′) and MCS• (𝑟, 𝑡 + 1, 𝐻 ′), respectively. This commits the
atomic triple, yielding the desired postcondition on line 24.
   It remains to show that the updates of the ghost resources preserve the invariant. That is, we
need to prove that all constraints in the invariant involving 𝑡, 𝐻 , 𝐶𝑟 , and 𝐵𝑟′ are       maintained if we
replace them with 𝑡 + 1, 𝐻 ′, 𝐶𝑟′ , and 𝐵𝑟′ = 𝜆𝑘 ′ . 𝑘 ′ ∈ dom(𝐶𝑟′ ) ? 𝐶𝑟′ (𝑘 ′) : 𝑄𝑟 (𝑘 ′) , respectively.
   First note that we can use the view shift assumption on Prot to reestablish Prot(𝐻 ′) from Prot(𝐻 ).
Further note that by definition we have 𝐵𝑟′ = 𝐵𝑟 [𝑘 ↣ (𝑣, 𝑡)]. Hence, the update to the ghost location
cir (𝑟 ) (𝑘) preserved the invariant. We can similarly see that the updates to 𝛾𝑡 , 𝛾𝑆 , and 𝛾𝑐𝑟 preserve
the invariant.
   Next, observe that HClock(𝑡 + 1, 𝐻 ′) and HUnique(𝐻 ′) follow directly from the definition of
  ′
𝐻 , HClock(𝑡, 𝐻 ), and HUnique(𝐻 ). We obtain the later two from the invariant prior to the ghost
update of 𝑡 and 𝐻 . Likewise, HInit(𝐻 ′) holds again because 𝐻 ⊆ 𝐻 ′ and HInit(𝐻 ) holds before the
update.
   To show 𝐻¯ ′ = 𝐵𝑟′ , we need to prove that for all keys 𝑘 ′
                              𝐻¯ ′ (𝑘 ′) = 𝑘 ′ ∈ dom(𝐶𝑟′ ) ? 𝐶𝑟′ (𝑘 ′) : 𝑄𝑟 (𝑘 ′)
                                                                                  

If 𝑘 ′ ≠ 𝑘, the equality follows directly from 𝐻¯ = 𝐵𝑟 and the definitions of 𝐻 ′ and 𝐶𝑟′ . For the case
where 𝑘 ′ = 𝑘 observe that HClock(𝑡, 𝐻 ) implies 𝐻¯ ′ (𝑘) = (𝑣, 𝑡). Moreover, we have 𝐶𝑟′ (𝑘) = (𝑣, 𝑡)
by definition of 𝐶𝑟′ .
   Finally, observe that 𝜙 2 (𝑟, 𝐶𝑟′ , 𝑄𝑟 , 𝐼𝑟 ) holds trivially because 𝐼𝑟 .in = 𝜆0 . Hence, we conclude that
the updates maintain the invariant, which also concludes the proof of upsert.
   Our careful encoding of contents-in-reach ensured that the sets 𝑄𝑛 and the node-local interfaces
𝐼𝑛 are not affected by the upsert for any node 𝑛, including 𝑟 . This considerably simplified the prove
that the invariant Inv(InvLSM , Prot) (𝑟 ) is maintained at the linearization point.
A.6.3 Proof of compact. As discussed in §7, we need to extend the data structure invariant InvLSM
with ghost resources that track the inset of each node. We do this via an additional flow interface.
The new global interface, denoted 𝐽 , is stored at a new ghost location 𝛾 𝐽 in InvLSM . Similar to the
contents-in-reach flow interface 𝐼 , the associated RA is authoritative flow interfaces over the flow

                                                     46
Verifying Concurrent Multicopy Search Structures                                                      ,,


domain of multisets of keys. We add the constraint dom(𝐼 ) = dom(𝐽 ) to ensure that 𝐼 and 𝐽 agree
on which nodes belong to the graph.
   The actual calculation of the insets is captured by the following constraint on the outflow of the
singleton interfaces 𝐽𝑛 which we add to the predicate NS :
                               𝐽𝑛 .out = 𝜆𝑛 ′ 𝑘. (𝑘 ∈ es𝑛 (𝑛 ′) ? 𝐽𝑛 .in(𝑛) (𝑘) : 0)                (15)
Additionally, we add the following constraint to G, which requires that the global interface 𝐽 gives
the full keyspace as inflow to the root node 𝑟 and no inflow to any other node:
                                          𝐽 .in = 𝜆𝑛 𝑘. (𝑛 = 𝑟 ? 1 : 0)
Together, these constraints guarantee that for any node 𝑛 that is reachable from 𝑟 , 𝐽𝑛 .in(𝑘) > 0 iff
𝑘 ∈ ins(𝑛).
  Finally, we add the following predicates to NS in order to capture Invariants 5-7:
                            𝜙 3 (𝑛, 𝐶𝑛 , 𝑄𝑛 ) B ∀𝑘. ts(𝑄𝑛 (𝑘)) ≤ ts(𝐵𝑛 (𝑘))
                        𝜙 4 (𝑛, 𝐶𝑛 , 𝑄𝑛 , 𝐽𝑛 ) B ∀𝑘. 𝑘 ∈ 𝑑𝑜𝑚(𝐵𝑛 ) ⇒ 𝐽𝑛 .in(𝑛) (𝑘) > 0
                                 𝜙 5 (𝑛, 𝐽𝑛 ) B ∀𝑘. 𝐽𝑛 .in(𝑛) (𝑘) ≤ 1
   The specifications of the implementation-specific helper functions assumed by compact are
provided in Figure 10. A thread performing compact 𝑛 starts by locking node 𝑛 and checking if
node 𝑛 is at full capacity using the helper function atCapacity. By locking node 𝑛, the thread
receives the resources available in NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ), for some contents 𝐶𝑛 and successor contents-in-
reach 𝑄𝑛 . The precondition of atCapacity requires the predicate node(𝑟, 𝑛, es𝑛 , val(𝐶𝑛 )), which is
available to the thread as part of NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ). The return value of atCapacity 𝑛 is a boolean
indicating whether node 𝑛 is full or not. The precise logic of how the implementation of atCapacity
determines whether a node is full is immaterial to the correctness of the template, so the specification
of atCapacity abstracts from this logic. If 𝑛 is not full, compact releases the lock on 𝑛, transferring
ownership of NL (𝑟, 𝑛, 𝐶𝑛 , 𝑄𝑛 ) back to the invariant and then terminates. The call to unlockNode
on line 20 is the commit point of the atomic triple in the else branch of the conditional.
   Thus, let us consider the other case, i.e. when 𝑛 is full. Here, the contents of node 𝑛 must be
merged with the contents of some successor node 𝑚 of 𝑛. This node 𝑚 is determined by the helper
function chooseNext. chooseNext either returns an existing successor 𝑚 of 𝑛 (i.e., es𝑛′ (𝑚) ≠ ∅),
or 𝑛 needs a new successor node, which we capture by the implementation-specific predicate
needsNewNode(𝑟, 𝑛, es, val(𝐶𝑛 )). In the former case, we can establish that 𝑚 is part of the data
structure due to the fact that the edgeset of 𝑛 directs some keys to 𝑚. This follows from the property
closed(𝑛) in the invariant Inv(InvLSM , Prot) (𝑟 ).
   In the latter case, a new node is allocated using the helper function allocNode and inserted
into the data structure as a successor of 𝑛 using the helper function insertNode. After this call,
𝑚 becomes reachable from the root node 𝑟 from 𝑛. To ensure that the node-local invariant of 𝑛 is
maintained, 𝑚 must be “registered” in Inv(InvLSM , Prot) (𝑟 ). To this end, we must extend the domain
of the global flow interfaces tracked by InvLSM with the new node 𝑚. This can be done using a frame-
preserving update of the authoritative version of the interfaces at ghost locations 𝛾𝐼 and 𝛾 𝐽 . Showing
that the invariant is preserved afer this update is easy because the postcondition of insertNext
together with the invariant guarantee that 𝑚 has no outgoing edges and can only be reached via 𝑛.
In particular, the fact that 𝑉𝑚 = ∅ and es𝑚 = 𝜆𝑛. ∅ imply in this case that 𝜙 4 (𝑚, 𝐶𝑚 , 𝑄𝑚 , 𝐽𝑚 ) holds,
where 𝐶𝑚 = 𝐵𝑚 = ∅. Additionally, the conjunct es𝑛′ = es𝑛 [𝑚 ↣ es𝑛′ (𝑚)] ensures that the inset
of any nodes other than 𝑛 and 𝑚 do not change. Hence, the flow interfaces at 𝛾𝐼 and 𝛾 𝐽 can be
contextually extended to include node 𝑚 in their domains.

                                                        47
,,                                             Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies


   Overall, once it has been established that node 𝑚 is in the domain of the global flow interfaces 𝐼
and 𝐽 in the invariant Inv(InvLSM , Prot) (𝑟 ), 𝑚 is locked and the contents of 𝑛 is (partially) merged
into 𝑚 using the helper function mergeContents (line 7).
   Let us now examine the specification of mergeContent in detail. mergeContents 𝑛 𝑚 merges the
data from node 𝑛 into node 𝑚. By merge, we mean that copies of keys drawn from some set 𝐾 ⊆ KS
are transferred from 𝑛 to 𝑚, possibly replacing older copies in 𝑚. In general, mergeContents
modifies the contents of the two nodes according to the specification given in Figure 10. The
precondition demands ownership of the physical representation of the nodes’ contents and that 𝑚
is a successor of 𝑛. The contents are modified to 𝑉𝑛′ and 𝑉𝑚′ respectively such that
                                    𝑉𝑛′ = mergeLeft (𝐾, 𝑉𝑛 , Es, 𝑉𝑚 )
                                   𝑉𝑚′ = mergeRight (𝐾, 𝑉𝑛 , Es, 𝑉𝑚 )
We can extend the definition of the functions mergeLeft and mergeRight to work on the contents
extended with timestamps:
              mergeLeft (𝐾, 𝐶𝑛 , Es, 𝐶𝑚 ) B 𝜆𝑘. (𝑘 ∈ 𝐾 ∩ dom(𝐶𝑛 ) ∩ Es ? ⊥ : 𝐶𝑛 (𝑘))
            mergeRight (𝐾, 𝐶𝑛 , Es, 𝐶𝑚 ) B 𝜆𝑘. (𝑘 ∈ 𝐾 ∩ dom(𝐶𝑛 ) ∩ Es ? 𝐶𝑛 (𝑘) : 𝐶𝑚 (𝑘))
We then define the new (timestamp) contents of 𝑛 and 𝑚 as:
                                 𝐶𝑛′ = mergeLeft (𝐾, 𝐶𝑛 , es𝑛 (𝑚), 𝐶𝑚 )
                                  ′
                                 𝐶𝑚 = mergeRight (𝐾, 𝐶𝑛 , es𝑛 (𝑚), 𝑉𝑚 )
Note that this gives us 𝑉𝑛′ = val(𝐶𝑛′ ) and 𝑉𝑚′ = val(𝐶𝑚′ ).

   We next explain that, together, these constraints and definitions ensure that we can consistently
update all relevant ghost resources in the invariant by locally recalculating the values of the ghost
resources constrained by the contents of 𝑛 and 𝑚. In particular, the contents-in-reach of 𝑚 can only
increase and the contents-in-reach of all other nodes, including 𝑛 remain unchanged.
   We let the set 𝐾 ′ B dom(𝐶𝑛 ) \ dom(𝐶𝑛′ ) denote all keys whose copies are merged from 𝐶𝑛 into
𝐶𝑚 . That is, we have 𝐾 ′ = 𝐾 ∩ dom(𝐶𝑛 ) ∩ es𝑛 (𝑚) and for all keys 𝑘 ∉ 𝐾 ′, we have 𝐶𝑛′ (𝑘) = 𝐶𝑛 (𝑘)
and 𝐶𝑚  ′ (𝑘) = 𝐶 (𝑘). We will use this observation freely in the remainder of the proof.
                   𝑚
   Before we proceed with the rest of the proof, we fix instantiations for the existentially quantified
variables in the invariant Inv(InvLSM , Prot) (𝑟 ) when we assume it before the call to mergeContents.
For a node 𝑝 in the structure, we denote by 𝐼𝑝 and 𝐽𝑝 the fragmental singleton flow interface of
node 𝑝 at ghost locations 𝛾𝐼 and 𝛾 𝐽 , respectively. Moreover, let 𝑄 𝑝 be the set stored at ghost location
𝛾𝑞 (𝑝) (i.e., the successor contents-in-reach of 𝑝 before the call to mergeContents).
   First, since the update of 𝐶𝑚 also affects the contents-in-reach of 𝑚, we need to update the
resource storing 𝐵𝑚 appropriately. We do this by defining:
                                    ′
                                   𝐵𝑚 B 𝜆𝑘. (𝑘 ∈ 𝐾 ′ ? 𝐶𝑛 (𝑘) : 𝐵𝑚 )
and then replace for each key 𝑘, ts(𝐵𝑚 (𝑘)) at ghost location 𝛾𝐶ir (𝑚) (𝑘) by ts(𝐵𝑚    ′ (𝑘)). To do this,

the authoritative maxnat RA requires us to show that ts(𝐵𝑚 (𝑘)) ⩽ ts(𝐵𝑚 (𝑘)). If 𝑘 ∉ 𝐾 ′, then
                                                                                  ′

𝐵𝑚 (𝑘) = 𝐵𝑚 ′ (𝑘) by definition. Hence consider the case where 𝑘 ∈ 𝐾 ′ . We then have 𝑘 ∈ dom(𝐶 )
                                                                                                       𝑛
      ′
and 𝐵𝑚 (𝑘) = 𝐶𝑛 . From this and 𝑘 ∈ e𝑛 (𝑚), it follows that 𝐼𝑛 .out (𝑚) (𝑘, 𝑄𝑛 (𝑘)) > 0, which, using the
flow equation, enables us to conclude 𝐽𝑛 .in(𝑚) (𝑘, 𝑄𝑛 (𝑘)) > 0. We then infer from 𝜙 2 (𝑚, 𝐶𝑚 , 𝑄𝑚 , 𝐼𝑚 )
that 𝑄𝑛 (𝑘) = 𝐵𝑚 𝑘. Moreover, it follows from 𝜙 3 (𝑛, 𝐶𝑛 , 𝑄𝑛 ) that ts(𝑄𝑛 (𝑘)) ⩽ ts(𝐵𝑛 (𝑘)). Since
𝐵𝑛 (𝑘) = 𝐶𝑛 (𝑘) = 𝐵𝑚 ′ (𝑘), we can conclude that ts(𝐵 (𝑘)) ⩽ ts(𝐵 ′ (𝑘)) as desired.
                                                      𝑚               𝑚
   Second, we observe that since mergeContents 𝑛 𝑚 does not change the edgesets of any nodes,
the insets of all nodes also remain unchanged. In particular, for all nodes 𝑝, the singleton interfaces
𝐽𝑝 are unaffected and hence still compose to the global interface 𝑅. Additionally, this means that

                                                    48
Verifying Concurrent Multicopy Search Structures                                                          ,,

                                                                                               ′ , 𝑄 , 𝐽 ) is
𝜙 5 (𝑝, 𝐽𝑝 ) and the constraint (15) on 𝐽𝑝 .out are trivially maintained. To see that 𝜙 4 (𝑚, 𝐶𝑚    𝑚 𝑚
also preserved, we note that if 𝑘 ∉ dom(𝐵𝑚 ) and 𝑘 ∈ dom(𝐵𝑚 ) for some 𝑘, then 𝑘 ∈ 𝐾 ′ and hence
                                                                    ′

𝐶𝑛 (𝑘) = 𝐵𝑛 (𝑘) = 𝐵𝑚    ′ (𝑘). It then follows from 𝜙 (𝑛, 𝐶 , 𝑄 , 𝐽 ) that 𝐽 .in(𝑛) (𝑘) > 0. Moreover,
                                                         4     𝑛  𝑛 𝑛         𝑛
        ′
𝑘 ∈ 𝐾 implies 𝑘 ∈ es𝑛 (𝑚) and, hence, 𝐽𝑛 .out (𝑚) (𝑘) > 0. It then follows from the flow equation
that 𝐽𝑚 .in(𝑚) (𝑘) > 0.
    Finally, we need to reflect the change in the contents-in-reach of 𝑚 in the local invariant of 𝑛 by
updating the ghost resource holding 𝑄𝑛 to the new value
                                    𝑄𝑛′ = 𝜆𝑘. (𝑘 ∈ 𝐾 ′ ? 𝐶𝑛 (𝑘) : 𝑄𝑛 (𝑘))]
In turn, this requires an update of the singleton interfaces 𝐼𝑛 and 𝐼𝑚 to 𝐼𝑛′ and 𝐼𝑚′ such that:
               𝐼𝑛′ .in B 𝐼𝑛 .in
             𝐼𝑛′ .out B 𝜆𝑛 ′ (𝑘, 𝑝).𝐼𝑛 .out (𝑛 ′) (𝑘, 𝑝) + (𝑛 ′ = 𝑚 ∧ 𝑘 ∈ 𝐾 ′ ∧ 𝐶𝑛 (𝑘) = 𝑝 ? 1 : 0)
              𝐼𝑚′ .in B 𝜆𝑛 ′ (𝑘, 𝑝).𝐼𝑚 .in(𝑛 ′) (𝑘, 𝑝) + (𝑛 ′ = 𝑚 ∧ 𝑘 ∈ 𝐾 ′ ∧ 𝐶𝑛 (𝑘) = 𝑝 ? 1 : 0)
             𝐼𝑚′ .out B 𝐼𝑚 .out
First, note that the changes to the inflows and outflows match up consistently. One can therefore
easily verify that the old and new singleton interfaces compose to the same larger two-node
interface:
                                          𝐼𝑛 ⊕ 𝐼𝑚 = 𝐼𝑛′ ⊕ 𝐼𝑚′
This means that we can simultaneously replace all old interfaces by their new ones using a frame-
preserving update of ghost location 𝛾𝐼 .
   It remains to show that the relevant constraints in the invariant that depend on 𝐼𝑛 , 𝐼𝑚 , and 𝑄𝑛
are preserved. We defer this part of the proof to the Iris development.




                                                      49
