                                         (Nearest) Neighbors You Can Rely On: Formally Verified 𝑘-d Tree
                                                         Construction and Search in Coq
                                                                                                                     Nadeem Abdul Hamid
                                                                                                                        nadeem@acm.org
                                                                                                                          Berry College
                                                                                                                     Mount Berry, Georgia, USA

                                         ABSTRACT                                                                                        arise in numerous areas, including machine learning and classi-
                                         The 𝑘-d tree [3, 8] is a classic binary space-partitioning tree used                            fication [6], recommendation systems [13], computer vision [19],
arXiv:2311.10965v1 [cs.LO] 18 Nov 2023




                                         to organize points in 𝑘-dimensional space. While used in computa-                               and image retrieval [9]. Wu et al. [20] include 𝐾-nearest neighbor
                                         tional geometry and graphics, the data structure has a long history                             classification among the 10 most influential algorithms in the data
                                         of application in nearest neighbor search. The objective of the near-                           mining research community.
                                         est neighbor search problem is to efficiently find the closest point(s)                            To improve on the brute-force approach of searching through
                                         to a given query point, and is the basis, in turn, of common machine                            the entire data set for every query point, effective solutions to
                                         learning techniques. We present in this paper a case study in the                               the KNN search problem rely on preprocessing the set of points to
                                         certified implementation, using the Coq proof assistant, of 𝑘-d tree                            enable more efficient computation of solutions for multiple arbitrary
                                         construction from a set of data and the accompanying 𝐾-nearest                                  query points. A classic algorithm presented in [3, 8] introduced the
                                         neighbors search algorithm. Our experience demonstrates an in-                                  𝑘-d tree, a space-partitioning binary tree structure that enables a
                                         tuitive method for specifying properties of these algorithms using                              branch-and-bound search technique, resulting in sub-linear search
                                         the notion of list permutations.                                                                complexity.
                                                                                                                                         Contributions. In this paper we present a formal verification of
                                         CCS CONCEPTS                                                                                    𝑘-d tree construction and search algorithms using the Coq proof
                                         • Software and its engineering → Formal software verifica-                                      assistant [1]. The significant contributions of this work are formally
                                         tion; Software verification; • Information systems → Cluster-                                   verified implementations in Coq of:
                                         ing and classification.                                                                             • A partitioning variant of the classic quickselect algorithm,
                                                                                                                                               used for finding medians in the data during tree construction;
                                         KEYWORDS                                                                                            • An algorithm for building a traditional 𝑘-d tree structure
                                         nearest neighbors search, quickselect, k-d tree, formally verified                                    and searching for the nearest neighbor to a query point; and
                                         algorithms, coq                                                                                     • A generalized algorithm for searching 𝐾-nearest neighbors
                                                                                                                                               of a query point, using a 𝑘-d tree and bounded priority queue.
                                         ACM Reference Format:
                                         Nadeem Abdul Hamid. 2024. (Nearest) Neighbors You Can Rely On: Formally                         Context and Motivations. As society becomes ever more depen-
                                         Verified 𝑘-d Tree Construction and Search in Coq. In Proceedings of . ACM,                      dent on applications that rely on core algorithms such as nearest
                                         New York, NY, USA, 10 pages. https://doi.org/xx.xxx/xxx_x
                                                                                                                                         neighbor search, it is worthwhile to move in the direction of apply-
                                                                                                                                         ing formal verification methods to such algorithms. Safety-critical
                                         1     INTRODUCTION                                                                              applications such as autonomous driving, medical imaging, and cy-
                                         The problem of finding the closest object(s) to a set of data points in                         bersecurity systems depend not only on low-level safety properties,
                                         a metric space has a long history in computing and a wide variety                               but on high-level characteristics of correctness and accuracy. In par-
                                         of applications. Formally, the nearest neighbor (NN) search problem                             ticular, machine learning-based systems are currently implemented
                                         is defined as: for some data set of points in 𝑘 dimensions, 𝑆 ⊂ R𝑘 ,                            primarily as black boxes with only empirical tests of performance
                                         given any query point 𝑞 ∈ R𝑘 , find a point 𝑝 ∈ 𝑆 that minimizes a                              and accuracy.
                                         distance metric, 𝛿𝑞 (𝑝). Knuth [14] calls this the post office problem,                             The results described here are obtained in pursuit of the applica-
                                         referring to the context of assigning a residence to the nearest post                           tion of formal methods to specify and verify properties of machine
                                         office. The problem is easily generalizable to seeking out the 𝐾                                learning systems and algorithms, in particular, classification and
                                         closest points to 𝑞 from the data set. Applications of (K)NN search                             regression based on KNN search. This paper focuses on core classi-
                                                                                                                                         cal algorithms and their formal verification. Our larger motivation
                                         Permission to make digital or hard copies of all or part of this work for personal or           is the development of a top-to-bottom verified implementation of
                                         classroom use is granted without fee provided that copies are not made or distributed           a realistic machine learning system. This necessitates working at
                                         for profit or commercial advantage and that copies bear this notice and the full citation
                                         on the first page. Copyrights for components of this work owned by others than the
                                                                                                                                         different levels of abstraction, reusing and extending existing veri-
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or          fied components, and identifying needs and opportunities for new
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission   proof automation tools and techniques. Section 6 situates the result
                                         and/or a fee. Request permissions from permissions@acm.org.
                                         , ,                                                                                             of this paper in the context of future work.
                                         © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN xyz. . . $15.00                                                                        Outline. In the sections that follow, we provide an overview of 𝑘-d
                                         https://doi.org/xx.xxx/xxx_x                                                                    trees, the nearest neighbor search algorithm, and the Coq proof
           , ,                                                                                                                                                              Nadeem Abdul Hamid


J                                                                                                                 A concrete example is provided in Figure 1. The bottom portion
                                                           A
                                                         (51, 75)                                            of the figure illustrates how the structure of the 𝑘-d tree on top
    G                                                                                                        splits the plane into subplanes, alternating horizontal and vertical
                                                                                                             divisions. The highlighted coordinate in each node identifies the
                                          B                                  C                               dimension and value around which the nodes in the subtrees are
                                        (25, 40)                          (70, 70)
        C                                                                                                    partitioned. For instance, all the nodes to the right of B have an
                                                                                                             x-coordinate less than 51 (A’s x-value) and y-coordinate greater
                                 D                  E               F                 G                      than equal to 40 (B’s y-value).
                               (10, 30)          (35, 90)         (55, 1)           (60, 80)
                                                                                                                  Constructing a balanced 𝑘-d tree is achieved by selecting the
                                                                                                             data point with the median value for the dimension associated with
                         H                                  I                   J                            the current level of the tree. In the example of Figure 1, starting with
                       (1, 10)                           (50, 50)           (55, 95)                         set of points {A, . . . , J}, the point A would be selected, for having
F                                                                                                            median x-coordinate value, as the initial root. The rest of the points
                                                                                                             would be partitioned into two subsets - one with x-coordinates less
                                                                                                             than 51, and everything else in the other. Each of these two subsets
                                                              J                                              would       be recursively processed to build the left and right subtrees
                                                                                                             of the root. In        Aeach case, the point with the median y-coordinate
                                             E                                                                                    (51, 75)
                                                                                                             will be selected as the root of the subtree. Section 3.2 describes
                                                                    G
                                                       A                                                     details of the formalization.
                                                                                                                  Searching
                                                                                                                   B               the 𝑘-d treeCfor the nearest neighbor of a query point
                                                                                                                (25, 40)
                                                                                                             𝑞 proceeds         by maintaining     (70, 70) the currently known closest point (ini-
                                                                                  C
                                                                                                             tially none). The root of the tree is considered and replaces the
                                                  I
                                                                                                             current closest point if it is closer to 𝑞. If the root and all points in
                                                                                                       D                    E                F                 G
                                                                                                     (10, 30)the (sub)tree(35, 90)are farther
                                                                                                                                           (55, 1)   away(60,than
                                                                                                                                                                80) the closest known point (see dis-

                                        B                                                                    cussion on bounding boxes in Section 3.3), then the entire (sub)tree
                                                                                                             is discarded (i.e. pruned) and the closest known point is maintained
                                                                                               H                                     I
                                                                                                             as the result. Otherwise,                   J
                                                                                                                                                       proceed     to recursively search the left and
                                  D                                                          (1, 10)                              (50, 50)           (55, 95)
                            H                                                                                right    subtrees       of  the     root.    In  order to prioritize searching the most
                                                               F
                                                                                                             promising subtree, if the value of the current dimension coordinate
                                                                                                             of the root is less than the query’s, we search the left subtree first,
           Figure 1: A 𝑘-d tree and induced partitions in the R2 plane.
                                                                                                             then the right; otherwise, the right subtree and then the left.
                                                                                                                  Generalizing the search to 𝐾-nearest neighbors1 involves main-
          assistant. Following that we present our implementations in Coq                                    taining a 𝐾-bounded max priority queue instead of a single closest
          (Section 3) and then explain their formal verification in Section 4.                               known point. At each subtree in the search process, if the root is
          Related work is reviewed in Section 5 followed by a discussion of fu-                              eligible for consideration (i.e. is at least as close to 𝑞 as the top,
          ture directions and conclusion. An appendix listing Coq statements                                 or maximum element, of the queue) it is added to the queue. The
          of lemmas and theorems is also included.                                                           bounded nature of the queue ensures that if its size exceeds 𝐾, then
                                                                                                             the point with largest distance from the query will be discarded.
          2 BACKGROUND                                                                                       While       our Coq developments also include verification of the (sin-
                                                                                                             gle) nearest neighbor search algorithm, for the purposes of this
          2.1 Nearest Neighbor Search Using 𝑘-d trees                                                        paper we focus on the general variant. Section 3.4 presents the
          A 𝑘-d tree is a binary tree whose nodes are 𝑘-dimensional data                                     implementation of 𝐾-nearest neighbors search in Coq.
          points. Each level in the tree is associated with one of the 𝑘 dimen-
          sions, usually cycling through them in order, 0 . . . (𝑘 − 1). Internal                            2.2 The Coq Proof Assistant
          (non-leaf) nodes partition the set of nodes in their subtrees based
                                                                                                             Coq [1] is an interactive proof assistant based on a higher-order
          on the dimension axis associated with the level they appear at.
                                                                                                             predicate logic extended with inductive data types. By virtue of
          In geometric terms, each non-leaf node of a 𝑘-d tree splits the
                                                                                                             the Curry-Howard isomorphism relating proofs and programs, the
          𝑘-dimensional space along a hyperplane perpendicular to the asso-
                                                                                                             Coq system provides a development environment in which pro-
          ciated dimension’s axis.
                                                                                                             gramming and proving are closely intertwined. It enables the user
             For the sake of intuition and ease of explanation, assume our
                                                                           2                                 to define data types and functions in a functional programming
          data points are two-dimensional vectors in R . Thus, the root node
                                                                                                             paradigm while writing rich logical specifications and constructing
          will partition nodes based on their “x” coordinates: all nodes with
                                                                                                             proofs in the same framework. For brevity, we only highlight here
          an x-coordinate less than that of the root will be in the left subtree;
                                                                                                             some salient features of Coq.
          the remainder will be in the right. At the next level, the root’s
          immediate children will partition the remaining nodes based on
          their “y” coordinates. Internal nodes at the third level will resume                               1 Throughout the paper, lowercase 𝑘 denotes the number of dimensions of the data
          partitioning based on the x coordinate values.                                                     points and uppercase 𝐾 is the number of nearest neighbors that are sought.
(Nearest) Neighbors You Can Rely On: Formally Verified 𝑘 -d Tree Construction and Search in Coq                                                                       , ,


                                                                                    1   Fixpoint qsp {X:Set} (steps:nat) (k:nat) (l:list X) (le:X -> X -> bool)
   Inductive definitions allow the introduction of basic data types                 2     : option (list X * X * list X) :=
such as natural numbers2 and polymorphic lists3 . Functions that                    3     match steps with
                                                                                    4     | 0 => None (* case should never happen *)
incorporate pattern matching and recursion on inductive objects are                 5     | S steps' =>
defined using Fixpoint and match constructs, as in the following                    6       match l with
                                                                                    7       | nil => None
definition of dropn:                                                                8       | pivot::lst => let '(sm, eq, lg) := partition_sm_eq_lg pivot lst le in
                                                                                    9           if k <? length sm then
(* produces the list after dropping the first n elements *)                        10             match qsp steps' k sm le with
Fixpoint dropn {A:Type} (n:nat) (lst:list A) : list A :=                           11             | None => None
                                                                                   12             | Some (a, x, b) => Some (a, x, b ++ ((pivot::eq) ++ lg))
  match n with                                                                     13             end
    | 0 => lst                  (* n = 0 case    *)                                14           else if (length sm + length eq ) <? k then
                                                                                   15             match qsp steps' (k - S (length sm + length eq)) lg le with
    | S n' => match lst with    (* n = 1+n' case *)                                16             | None => None
                 | [] => []                                                        17             | Some (a, x, b) => Some (a ++ (sm ++ (pivot::eq)), x, b)
                                                                                                  end
                 | h :: t => dropn n' t                                            18
                                                                                   19           else Some (sm ++ (firstn (k - length sm) eq),
               end                                                                 20                       pivot, (dropn (k - length sm) eq) ++ lg)
  end.                                                                             21       end end.
                                                                                   22
                                                                                   23   Definition quick_select {X} k l le := @qsp X (length l) k l le.
   Recursive definitions must satisfy strict syntactic constraints                 24
to ensure termination and totality. Generally speaking, Coq only                   25   Definition median_partition {X:Set} (l:list X) (le:X -> X -> bool)
                                                                                   26     := quick_select (div2 (length l)) l le.
accepts structurally recursive functions. A common device to define
functions with complex recursions is to introduce an extra nat
parameter (called the “fuel”) as the primary recursive argument.                        Figure 2: An expected linear time 𝑘 th -smallest element se-
A wrapper definition can then be provided for the function that                         lection algorithm.
provides enough fuel– essentially an upper bound on the depth of
recursion– for it to produce a result in every case. Examples of this
                                                                                        3.1       Quickselect
are in the quick_select and build_kdtree functions presented
later.                                                                                  We use a functional variant of Hoare’s classic Find algorithm [12]
   Besides defining data types, inductive definitions are used in Coq                   that selects the 𝑘th smallest element in a list, in expected linear
to define logical concepts and propositions. For example, the Coq                       time. Figure 2 presents our Coq implementation, which returns
standard library defines4 (Permutation lst1 lst2) as a relation                         not only the 𝑘th smallest element (where 𝑘 = 0 is the smallest of
between two lists stating that the elements of one can be reordered                     all), but also produces partitions of the remainder of the list. For
to get the other. The specification defines a permutation as being                      example, (quick_select 3 [15; 90; 32; 7; 86] Nat.leb)
a composition of adjacent transpositions. A proof that lst1 is a                        produces Some ([32; 7; 15], 86, [90]).
reordering of lst2 involves constructing a well-typed object of type                        The steps parameter of qsp is a fuel argument (see Section 2.2).
(Permutation lst1 lst2).                                                                The quick_select function passes the length of list l as the initial
   In general, theorems and lemmas in Coq are defined as objects                        fuel value, along with an arbitrary “less than equal” comparison
with a type that represents a logical proposition. While proofs may                     predicate le for the elements in the list. Lemma 4.8 later establishes
be constructed directly by writing a complete well-formed expres-                       that steps will never reach 0 in qsp. Since Coq functions must be
sion with the correct type, more often they are built interactively                     total, we define the workhorse function, qsp, to return an option
and incrementally using a script of proof tactics. In the remainder of                  type: either None, or Some (a, x, b) triple containing the 𝑘th
the paper, we write theorem statements in a stylized form and omit                      smallest element x, along with a list a of the 𝑘 items preceding x in
proof scripts (which only provide insight anyway when executed                          l were it to be sorted, and the remaining elements b after it. Finally,
interactively). The Appendix provides the precise Coq syntax for                        we define a median_partition function to partition a given list
the theorem statements presented in the body of this paper. The                         around its pivot.
complete code development, using Coq version 8.16.1, is available                           For simplicity, our implementation always chooses the head of
at https://github.com/nadeemabdulhamid/knn-search-coq.                                  the list l as the pivot, then filters the tail, lst, into three partitions
                                                                                        (line 8) – elements strictly less than, equal to, and strictly greater
                                                                                        than pivot. The lengths of these three sublists are examined to
3    COQ IMPLEMENTATION: ALGORITHMS
                                                                                        determine in which one the 𝑘 th smallest element falls. If it is in
     AND DATA STRUCTURES                                                                the equal partition (line 19), then the pivot is the 𝑘 th smallest
Efficient search of a 𝑘-d tree tree for nearest neighbor queries                        element (and we divide the partition of equal elements around it
relies partly on having constructed a well-balanced tree. This in                       to obtain the 𝑘 elements preceding it when combined with the
turn, depends on being able to select median values for the root of                     smaller). Otherwise, the function recursively descends (lines 10, 15)
each subtree. In the following sections, we present our formalized                      into the appropriate partition, adjusting the value of k relative to
quickselect algorithm, data structures for representing bounding                        the partition lengths (line 15).
boxes, and then the 𝑘-d tree construction and search algorithms.
                                                                                        3.2 𝑘-d tree Construction
2 https://coq.inria.fr/library/Coq.Init.Datatypes.html#nat                              We define a simple structure representing 𝑘-d trees, which are either
3 https://coq.inria.fr/library/Coq.Init.Datatypes.html#list                             empty or a node with a data point and two subtrees. The natural
4 https://coq.inria.fr/library/Coq.Sorting.Permutation.html                             number in the node is the index of the dimension along which data
     , ,                                                                                                                                                           Nadeem Abdul Hamid


 1   Fixpoint build_kdtree_ (fuel:nat) (k:nat) (data:list datapt) (depth_mod:nat)           1   Parameter priqueue: forall A:Type, (A -> t) -> Type.
 2     : kdtree :=                                                                          2
 3     match fuel with                                                                      3   Parameter empty: forall A key, priqueue A key.
 4     | 0 => mt_tree (* case should never happen *)                                        4   Parameter insert: forall A key, A -> priqueue A key -> priqueue A key.
 5     | S fuel' =>                                                                         5   Parameter delete_max: forall A key, priqueue A key -> option (A * priqueue A key).
 6         match data with                                                                  6   Parameter peek_max: forall A key, priqueue A key -> option A.
 7         | [] => mt_tree                                                                  7   Parameter size: forall A key, priqueue A key -> nat.
 8         | _ => match median_partition data (ith_leb depth_mod) with                      8
 9                 | None => mt_tree                                                        9   Definition insert_bounded (K:nat) A key (e:A) (pq:priqueue A key)
10                 | Some (sm, pvt, lg) =>                                                 10     : priqueue A key :=
11                     node depth_mod pvt                                                  11     let updpq := (insert A key e pq)
12                         (build_kdtree_ fuel' k sm (next_depth k depth_mod))             12     in if K <? (size A key updpq)
13                         (build_kdtree_ fuel' k lg (next_depth k depth_mod))             13        then match delete_max _ key updpq with
14     end end end.                                                                        14             | None => updpq               (* should never happen *)
15                                                                                         15             | Some (_ , updpq') => updpq' (* the removed element is discarded *)
16   Definition build_kdtree (k:nat) (data:list datapt) : kdtree                           16             end
17     := build_kdtree_ (length data) k data 0.                                            17        else updpq.


                          Figure 3: Building a 𝑘-d tree.                                        Figure 4: The priority queue ADT and bounded insert opera-
                                                                                                tion.

     in the subtrees is split by the node. The length of every datapt
                                                                                                Inductive bbox : Set
     should match the number of dimensions, 𝑘.                                                    := mk_bbox : (list (option nat)) -> (list (option nat)) -> bbox.
     Definition datapt := list nat.                                                                To compute bounding boxes for child nodes, we use a function
                                                                                                that splits one bounding box into two, based on a dimension index
     Inductive kdtree :=
                                                                                                and a value. For example,
     | mt_tree : kdtree
     | node : nat -> datapt -> kdtree -> kdtree -> kdtree.                                                   bb_split([(10, −∞ , 4), (∞, 30 , 20)], 1, 11 )
        The build_kdtree_ function in Figure 3 proceeds by partition-                                        = ( [(10, −∞ , 4), (∞, 11 , 20)],
     ing the data list around the median coordinate value of the cur-                                             [(10, 11 , 4), (∞, 30 , 20)] )
     rent depth in the tree. It then builds a node with the pivot point                            Given any arbitrary point 𝑞 in 𝑘-dimensional space and a bound-
     and recursively builds left and right subtrees with the smaller                            ing box 𝐵, an important operation will be to find the point 𝑝 ∈ 𝐵
     and larger partitions around the pivot. At a level 𝑑 deep in the                           that minimizes the distance to 𝑞. (Note, if 𝑞 ∈ 𝐵, then 𝑝 = 𝑞.) While
     tree, (next_depth k depth_mod) = ((𝑑 + 1) mod 𝑘); thus, the                                not immediately intuitively obvious, the following computes the
     depth_mod argument cycles through the dimensions along which                               closest enclosed point:
     data is split as the recursion descends. (ith_leb i) produces a
     function that compares two data points on their 𝑖 th dimension. For                                   cep(𝑞, [𝑠, 𝑡]) = 𝑝        where 𝑝𝑖 = median(𝑞𝑖 , 𝑠𝑖 , 𝑡𝑖 ) 5
     example, (build_kdtree 2 [[1;10]; [50;50]; ...; [70;70]])                                     For the purpose of our formalization, we adopt the Manhattan
                                                                                                                          Í
     produces the tree of Figure 1,                                                             distance metric, 𝛿𝑞 (𝑝) = 𝑖 |𝑞𝑖 − 𝑝𝑖 |, throughout our development;
           node 0 [51; 75]                                                                      though any well-behaved metric would work. Our distance metric
             (node 1 [25; 40]                                                                   𝛿𝑞 (𝑝) is thus defined as a Coq function,
               (node 0 [10; 30] (node 1 [1; 10] ...))                                                           sum_dist : datapt -> datapt -> nat.
               (node 0 [50; 50] (node 1 [35; 90] ...)))
             (node 1 [60; 80]
               (node 0 [70; 70] (node 1 [55; 1] ...))
                                                                                                3.4      Nearest Neighbor Search
               (node 0 [55; 95] ...))                                                           The generalized KNN search algorithm uses a priority queue to col-
                                                                                                lect candidates for the 𝐾-nearest neighbors. We adapt the priority
     3.3     Bounding Boxes and Distance Metric                                                 queue ADT described in Verified Functional Algorithms (VFA) [2]
                                                                                                for our purposes. The VFA implementation uses the Coq module
     Every node in the 𝑘-d tree can be associated with a bounding box
                                                                                                system to separate an abstract signature of the queue and its opera-
     that describes the minimum and maximum extent of the tree rooted
                                                                                                tions (and their properties) from the implementation. Both unsorted
     at that node. Bounding boxes can be described as a pair of data
                                                                                                list and traditional binary heap implementations are developed in
     points, [(𝑠 0, . . . , 𝑠𝑘 −1 ), (𝑡 0, . . . , 𝑡𝑘 −1 )], where 𝑠𝑖 , 𝑡𝑖 ∈ N ∪ {±∞}. A
                                                                                                VFA. We generalize the priority queue to contain any type of data
     point 𝑝 = (𝑝 0, . . . , 𝑝𝑘 −1 ) is contained in such a bounding box if
                                                                                                elements and equip it with a key function mapping data elements to
     𝑠𝑖 <= 𝑝𝑖 <= 𝑡𝑖 . In the example of Figure 1, the bounding box of
                                                                                                a comparable type (like nat). Additionally, we added peek and size
     the root, A, would be [(−∞, −∞), (+∞, +∞)], while the bounds
                                                                                                operations to the ADT. Like delete_max, peek produces None if ap-
     associated with I would be [(35, 40), (51, +∞)]. In other words,
                                                                                                plied to an empty queue. Since this is a functional implementation,
     any data point occurring in a subtree rooted at I would have x-
                                                                                                delete_max produces an updated queue along with the removed
     coordinate between 35 and 51, and y-coordinate greater than 40
                                                                                                element. Figure 4 also presents a bounded insert operation that is
     (and unbounded on top). The correspondence to the divided plane
                                                                                                used to maintain a queue with maximum size 𝐾.
     in bottom of the figure should hopefully be clear.
                                                                                                    Finally, Figure 5 presents the complete KNN search algorithm.
        In the Coq development, we define a bounding box as a structure
                                                                                                Recall, 𝐾 is the number of nearest neighbors desired, while 𝑘 is
     containing two lists of optional values, where (Some n) represents
     a concrete number 𝑛, and None represents ±∞.                                               5 median(𝑥, 𝑦, 𝑧 ) is the median of the three values 𝑥 , 𝑦 , and 𝑧 .
     (Nearest) Neighbors You Can Rely On: Formally Verified 𝑘 -d Tree Construction and Search in Coq                                                                              , ,


     Fixpoint knn (K:nat) (k:nat) (tree:kdtree) (bb:bbox) (query:datapt)
 1
 2                (pq:priqueue datapt (sum_dist query))                                      given a query point, we expect the result of knn_search from
 3     : priqueue datapt (sum_dist query) :=                                                 Figure 5 to satisfy the following:
 4     match tree with
 5       | mt_tree => pq                                                                         (1) The result should be a list of 𝐾 elements, but no more than
 6       | node ax pt lft rgt =>
 7           let body (pq':priqueue datapt (sum_dist query)) :=                                      |data|.
 8               let dx := nth ax pt 0 in                                                        (2) The result should be a subset of the original data. We ex-
 9               let bbs := bb_split bb ax dx in
10               if (ith_leb ax pt query)                                                            press this by positing that there exists a leftover list which,
11               then (knn K k rgt (snd bbs) query                                                   together with result, is some permutation of data (effec-
12                       (knn K k lft (fst bbs) query pq'))
13               else (knn K k lft (fst bbs) query                                                   tively describing a reordered partitioning).
                         (knn K k rgt (snd bbs) query pq'))
14
15           in
                                                                                                 (3) Every element in the result should be, according to the met-
16           match (peek_max _ _ pq) with                                                            ric of distance from the query point, less than or equal to every
             | None => body (insert_bounded K _ _ pt pq)
17
18           | Some top => if (K <=? (size _ _ pq))                                                  other element from the data that is not in the result (i.e.
19                   && ((sum_dist query top)                                                        that is in leftover). In other words, they are the elements
20                           <? (sum_dist query (closest_edge_point query bb)))
21                       then pq                                                                     with the smallest distances from the query.
22                       else body (insert_bounded K _ _ pt pq)
23           end                                                                             Establishing these properties depends on preconditions captured
24     end.                                                                                  in the full Coq statement of what is ultimately the final theorem of
25
26   Definition knn_search (K:nat) (k:nat) (tree:kdtree) (query:datapt)                      our development:
27     : list datapt :=
28     pq_to_list                                                                                Theorem 4.1 (knn_search_build_kdtree_correct).
29       (knn K k tree                                                                       forall (K:nat) (k : nat) (data : list datapt),
30            (mk_bbox (repeat None k) (repeat None k)) query
31            (empty datapt (sum_dist query))).                                                0 < K ->      (* at least one nearest neighbor sought *)
                                                                                               0 < length data ->                 (* data is non-empty *)
           Figure 5: The 𝐾-nearest neighbors search algorithm.                                 0 < k ->                (* dimension space is non-empty *)
                                                                                               (forall v' : datapt,    (* all data points well-formed, *)
                                                                                                     In v' data -> length v' = k) ->   (* k dimensions *)
                                                                                               forall tree query result,
     the number of dimensions. The main function, knn_search (line                                 tree = (build_kdtree k data) ->
     26), initializes an empty priority queue (using the distance from                             result = knn_search K k tree query ->
     the query to compute key values) and an unconstrained bounding                                exists leftover,
                                                                                                     length result = min K (length data)            (*1*)
     box, and handles converting the final returned priority queue into
                                                                                                     /\ Permutation data (result ++ leftover)       (*2*)
     a list. In the knn function, as long as the tree is not empty, we                               /\ all_in_leb (sum_dist query) result leftover.(*3*)
     first attempt to peek at the top of the queue (line 16). If the priority
     queue is full (line 18) and the closest point to the query that lies                        In our experience, it is easier to separate out and prove the first
     in the current bounding box is farther away than the element at                         property independently of the other two. The following general-
     the top of the queue, then the entire tree is ignored and the queue                     ized proposition is established by induction on 𝑡, proceeding by
     produced unchanged (line 21). Otherwise, the root node is inserted                      case analysis on the possible execution paths of knn (Figure 5).
     into the queue (lines 17, 22) and the body is executed. In the body                     Its proof relies on correctness of the bounded insertion operation
     expression, dx is the coordinate value of the tree root for the axis                    (insert_bounded) with respect to maintaining a maximum queue
     (dimension index) around which the tree is partitioned at this level.                   size of 𝐾. Contents_kdtree is an inductively-defined relation that
     The current bounding box is split into its two components, bbs, and                     associates a 𝑘-d tree with a list of all the data points it contains in
     then two recursive calls are made according to the most promising                       its nodes.6
     order, as described in Section 2.1.
                                                                                                 Lemma 4.2 (knn_search_build_size_gen). For any data point
                                                                                             list 𝐷 and tree 𝑡, where Contents_kdtree(𝑡) = 𝐷; and priority queue
     4     FORMAL VERIFICATION                                                               𝑝𝑞, where |𝑝𝑞| ≤ 𝐾,
     We now highlight aspects of our formal specification and verifica-                                     |knn(𝐾, 𝑘, 𝑡, 𝐵, 𝑞, 𝑝𝑞)| = min(𝐾, |𝐷 | + |𝑝𝑞|).
     tion of the algorithms and data structures defined in the preceding
     section. While presented here in top-down order, the appendix                              In many cases, propositions like Lemma 4.2 come in pairs, with
     contains Coq statements of supporting lemmas and intermediate                           another top-level lemma (named knn_search_build_size in this
     definitions in the order they appear in the actual proof scripts. No-                   case) that is specialized to initial conditions; for example, that 𝑡 =
     tations used here include |𝑙 | for length or size, (𝑙1 ++ 𝑙2) for list                  build_kdtree(𝑘, 𝐷) and 𝐵 = [(−∞, −∞), (+∞, +∞)]. Applying this
     concatenation, and (𝑙1 ⊲⊳ 𝑙2) for (Permutation l1 l2). The bi-                          to the proof of Theorem 4.1 depends on the relationship between
     nary relation on lists, all_in_leb, denoted by 𝑙 1 ≤≤ 𝑙 2 , holds if                    Contents_kdtree and build_kdtree (see Lemma 4.7).
     ∀𝑒 1 ∈ 𝑙 1, 𝑒 2 ∈ 𝑙 2, 𝑒 1 ≤? 𝑒 2 . The ≤? relation is a total order (see               6 As noted in Section 3.4, we adapt the VFA priority queue module for our use. That
     Theorem 4.9).                                                                           library frames correctness of the ADT using a model-based specification: the abstract
                                                                                             priqueue type is associated with a representation invariant (priq) as well as an abstrac-
                                                                                             tion relation (Abs) that establishes a correspondence between the priqueue type and
     4.1     KNN Search                                                                      the concrete list type. This enables reasoning about programs that use a priqueue
                                                                                             through simpler reasoning about behaviors of lists, regardless of how the priqueue is
     To specify correctness of the overall KNN search algorithm, suppose                     implemented. The proposition statements in this section elide hypotheses involving
     we have a list of data points from which we build a 𝑘-d tree. Then,                     these invariants, but they appear in the full Coq statements in the appendix.
  proved by induction on the structure
                   algorithm,          of thebytree.
                              and is proved      induction on the structure of the tree.

 generalized lemma
n_full_relate_gen).
                 Lemma  unravels
                      For       data the
                                      pointdetails
                           any(knn_full_relate_gen).
                          10                           oft bounded
                                            list D, tree   the For
                                                                data
                                                                   any flow   through
                                                                        data point         thet bounded
                                                                                   list D, tree
                 by      priority
                       (where      queue
m, and is proved by induction on the structure
ntents_kdtree(t) =  D),
                    B                      pq,   and
                                Contents_kdtree(t)    result Rof=priority
                                                         = D),            queue pq, and result R =
                                                                  the tree.
pq),             knn(K, k, t, B, q, pq),

pq10    (knn_full_relate_gen).
   sm , pqlg , Dsm, ,, Dlg , L, (pqsm + + pq9pq
                                             lg )sm
                                                       For
                                                  ./ ,pq
                                                      pq      any data point list
                                                         lg ,^Dsm , Dlg , L, (pqsm + + pq D,    tree t bounded
                                                                                            lg ) ./ pq ^                                                  Nadeem Abdul Hamid
where Contents_kdtree(t)        (Dsm ++ D=       D),
                                            lg ) ./  D priority
                                                           ^           queue (Dsmpq,++ Dandlg ) ./result
                                                                                                   D ^ R =
k, t, B, q, pq),                (pqsm ++ Dsm ) ./ R ^                        (pqsm ++ Dsm ) ./ R ^
                                                                                                       in the kdtree data type, bounding boxes are crucial for reasoning
                   pq           (pqlg ++ Dlg ) ./ L ^            D           (pqlg ++ Dlg ) ./ L ^
                                                                                                       about the properties of the search algorithm. We define a compu-
            9pqsm , pqpqlgsm ,RDsm L pq^lg
                                       , Dlg , L, (pqsm ++ pqlgDsm) ./       R pq
                                                                                 L D^ ^lg
                                                                                                       tational function, kdtree_bounded, to check if a tree is properly
                                (|R| < K) ) L = [].                          (|R| < K) ) L = [].
                                                     (Dsm ++ Dlg ) ./ D ^                              constrained by a given bounding box. This does not simply check
                                                                                                       that every point in the tree occurs in the root’s bounding box, but
                                                     (pqknn
                                                          sm +  + Dsm ) ./ R ^
                                                                                                       rather the more nuanced property that subtrees are constrained by
                        R                            (pqlg +L+ Dlg ) ./ L ^                            the boxes appropriately split (Section 3.3) according to the dimen-
                                                     R  L ^                                          sion and value associated with the root.
                                                     (|R| < K) ) L = [].                                  We can then establish that the build_kdtree algorithm (Fig-
                            Figure 6: Partitions induced by the knn function.                          ure 3) constructs a tree that is properly constrained by an initially
                                                                                                       unbounded box. The proof of this lemma relies on properties of
                                                                                                       quick_select (Theorem 4.9):
                       For the latter two properties of Theorem 4.1, we develop another
                                                                                                          Lemma 4.5 (build_kdtree_bounded). Given a list of data points,
                  pair of lemmas expressing that knn_search effectively partitions
                                                                                                       𝐷, each of dimension 𝑘,
                  the input data into two lists, 𝑅 (result) and 𝐿 (leftover), where 𝑅 ≤≤ 𝐿.
                  The top-level one is stated:                                                           kdtree_bounded(build_kdtree(𝑘, 𝐷), [(−∞, −∞), (+∞, +∞)]).

                    Lemma 4.3 (knn_full_relate). Given a list of data points 𝐷,                      One other crucial proposition related to bounding boxes is that
                  query point 𝑞, and tree 𝑡 = build_kdtree(𝑘, 𝐷),                                 the cep function (Section 3.3) does in fact compute the closest
                                                                                                  enclosed point. This is necessary for the proof of Lemma 4.4:
                     ∃𝑅, 𝐿, knn_search(𝐾, 𝑘, 𝑡, 𝑞) = 𝑅 ∧ 𝐷 ⊲⊳ (𝑅 ++ 𝐿) ∧ 𝑅 ≤≤ 𝐿.
                                                                                                    Lemma 4.6 (cep_min_dist). Given a point 𝑞 and bounding box 𝐵,
                     The associated generalized lemma unravels the details of the                 ∀𝑝 ∈ 𝐵, 𝛿𝑞 (cep(𝑞, 𝐵)) ≤ 𝛿𝑞 (𝑝).
                  data flow through the algorithm, and is proved by induction on the
                  structure of the tree:                                                             Besides conforming to bounding box constraints, the build_kdtree
                                                                                                  algorithm should result in a tree whose contents are exactly some
                     Lemma 4.4 (knn_full_relate_gen). For any data point list 𝐷,                  permutation of the items in the original list. Establishing this also re-
                  tree 𝑡 bounded by 𝐵 (where Contents_kdtree(𝑡) = 𝐷), priority queue              quires validating the viability of the fuel argument for build_kdtree_
                  𝑝𝑞, and result 𝑅 = knn(𝐾, 𝑘, 𝑡, 𝐵, 𝑞, 𝑝𝑞),                                      in Figure 3 (because if the fuel ran out early, the function would
                                                                                                  not process all the items in the list):
                          ∃𝑝𝑞𝑠𝑚 , 𝑝𝑞𝑙𝑔 , 𝐷𝑠𝑚 , 𝐷𝑙𝑔 , 𝐿,   (𝑝𝑞𝑠𝑚 ++ 𝑝𝑞𝑙𝑔 ) ⊲⊳ 𝑝𝑞 ∧
                                                                                                     Lemma 4.7 (build_kdtree_contents_perm_gen). For a list
                                                          (𝐷𝑠𝑚 ++ 𝐷𝑙𝑔 ) ⊲⊳ 𝐷 ∧
                                                                                                  of data points, 𝐷, if 𝑘 > 0, 𝑑𝑚𝑜𝑑 < 𝑘, and 𝑓 ≥ |𝐷 |, then ∃𝑙,
                                                          (𝑝𝑞𝑠𝑚 ++ 𝐷𝑠𝑚 ) ⊲⊳ 𝑅 ∧                   Contents_kdtree(build_kdtree_(𝑓 , 𝑘, 𝐷, 𝑑𝑚𝑜𝑑)) = 𝑙 ∧ 𝑙 ⊲⊳ 𝐷.
                                                          (𝑝𝑞𝑙𝑔 ++ 𝐷𝑙𝑔 ) ⊲⊳ 𝐿 ∧
                                                          𝑅 ≤≤ 𝐿 ∧                                Here 𝑑𝑚𝑜𝑑 represents the value (𝑑 mod 𝑘) where 𝑑 is the current
                                                          ((|𝑅| < 𝐾) ⇒ 𝐿 = []).                   depth level of the tree being constructed through the recursive calls
                                                                                                  of build_kdtree_ (see depth_mod in Section 3.2). In addition to
                  A graphical intuition for Lemma 4.4 is given in Figure 6. The effect            having a sufficient bound on the fuel 𝑓 , correct behavior depends on
                  induced by knn on its input priority queue (viewed abstractly as a              the number of dimensions 𝑘 being non-zero and the value of 𝑑𝑚𝑜𝑑
                  list) and list of data points (contained in the 𝑘-d tree) is to partition       being a valid dimension index. The proof is fairly straightforward
                  each of those lists into two chunks, where all elements of the first            through unfolding the different execution paths in build_kdtree_.
                  chunk (𝑝𝑞𝑠𝑚 and 𝐷𝑠𝑚 ) are less than or equal to those in the second             The (quick_select_permutation) lemma of Theorem 4.9 in the next
                  (𝑝𝑞𝑙𝑔 and 𝐷𝑙𝑔 , respectively). Then, knn selects out the two chunks             section is necessary for establishing the permutation property.
                  of lesser elements to form the result it produces, leaving behind
                  a (discarded) result that contains the two larger chunks of each                4.3     Quickselect
                  list. While it appears intuitively correct, the proof of this lemma
                                                                                                  To account for the fuel argument used by qsp (Figure 2), we prove
                  was extremely long and tedious to develop. One reason was the
                                                                                                  that as long as steps is at least the length of the input list, and k is
                  lack of automation for reasoning about Permutations (discussed
                                                                                                  less than its length, quick_select will always produce some result
                  later). The other was that large portions of the proof tactics were
                                                                                                  (as opposed to None).
                  duplicated to cover the different execution paths in the function
                  (the conditional expressions leading to the evaluation of the body                 Lemma 4.8 (qsp_works). If 𝑘 < |𝑙 | and |𝑙 | ≤ steps, then
                  in Figure 5). When reasoning through the nested recursive calls,                                   ∃𝑝, qsp(steps, 𝑘, 𝑙, ≤? ) = Some 𝑝.
                  each intermediate result gets partitioned into additional pieces as it
                  feeds through the next application of knn, resulting in invocations               With this established, we can specify and prove properties of
                  of the inductive hypotheses with slightly different contexts.                   quick_select as stated by the following theorem. The labels in
                                                                                                  parentheses correspond to names of lemmas in the Coq proof script,
                  4.2    Bounding Boxes and 𝑘-d trees                                             each property stated and proved independently.
                  Lemmas 4.3 and 4.4 also rely on properties about bounding boxes                   Theorem 4.9 (qick_select_exists_correct). For any well-
                  and their relationship to 𝑘-d trees. While not explicitly represented           behaved “less than or equal” operation, ≤? , if 𝑘 < |𝑙 |, then
(Nearest) Neighbors You Can Rely On: Formally Verified 𝑘 -d Tree Construction and Search in Coq                                                                , ,


    (1) ∃𝑙 1, 𝑣, 𝑙 2,                                                                        our primary focus was on the KNN search algorithm. In contrast,
        quick_select(𝑘, 𝑙, ≤? ) = Some (𝑙 1, 𝑣, 𝑙 2 ) (quick_select_always_some)             our implementation of quickselect produces a balanced partition
    (2) 𝑙 ⊲⊳ (𝑙 1 ++ [𝑣] ++ 𝑙 2 ) (quick_select_permutation)                                 of the input list in addition to its median value. In Rau’s develop-
    (3) |𝑙 1 | = 𝑘 (qsp_position)                                                            ment [17], a different form of 𝑘-d trees was implemented, where all
    (4) ∀𝑥 ∈ 𝑙 1, 𝑥 ≤? 𝑣 (qsp_all_smaller)                                                   data points occur at the leaves of the tree and internal nodes only
    (5) ∀𝑥 ∈ 𝑙 2, 𝑣 ≤? 𝑥 (qsp_all_larger)                                                    store the dimension (axis) being split on and a median value for
                                                                                             comparison. Thus, their search implementation proceeds through
    For quick_select, (1) we always get a partition of the original
                                                                                             the tree and only inserts into the queue when it reaches the leaves.
list into three pieces: two lists and an element. The combination
                                                                                             Our data structure, storing data points at all nodes in the tree, ap-
of these pieces should be a reordering of the input list (2). If 𝑣 is
                                                                                             pears closer to traditional implementations. The formulation of the
meant to be the 𝑘 th smallest element (where 𝑘 = 0 for the minimum
                                                                                             KNN search algorithm verified in this paper also appears more true
of entire list), then 𝑙 1 should contain exactly 𝑘 elements (3). We
                                                                                             to standard formulations, such as in the specification of bounding
also expect that everything in 𝑙 1 is less than or equal to 𝑣 (4); and
                                                                                             boxes (“geometric boundaries” of [8]) and use of a priority queue
symmetrically, that everything in 𝑙 2 is greater than or equal to 𝑣 (5).
                                                                                             ADT.
The properties of ≤? needed to establish (4) and (5) above are that
                                                                                                In terms of specification of the overall algorithms, while appear-
it be transitive and total:
                                                                                             ing logically equivalent to ours (a good thing!), [7, 17] appeal to
Definition le_props {X:Set} (le:X -> X -> bool) : Prop :=                                    notions of sorting and sortedness, whereas we avoid any depen-
    (forall a b c, le a b = true -> le b c = true
                                                                                             dence on notions of sorting and formulate our propositions using
                                 -> le a c = true) /\
                                                                                             more elementary properties of Permutation and all_in_leb. We
    (forall a b, le a b = true \/ le b a = true).
                                                                                             feel the use of permutations for the specification is simpler and
   Theorem 4.9 above is one possible formulation of correctness for                          more understandable, and in some cases also provides better clar-
quick_select. Alternatively, an early iteration used the following                           ity and understanding about the properties and data flow of the
(in which the function only produced the median value):                                      algorithm (à la Figure 6). Finally, there are differences in the un-
            If quick_select(𝑘, 𝑙, ≤? ) = Some 𝑣, then                                        derlying logic of the systems themselves, discussion of which is
          (1) |(filter (_ <? 𝑣) 𝑙)| ≤ 𝑘,7                                                    beyond the scope of this paper. For example, function definitions
          (2) |(filter (_ =? 𝑣) 𝑙)| ≤ |𝑙 |, and                                              such as knn_search in Coq, being actually computational, must
          (3) |(filter (𝑣 <? _) 𝑙)| < |𝑙 | − 𝑘.                                              satisfy syntactic termination conditions. Thus, a well-typed func-
    In our assessment, while logically equivalent and more concise,                          tion is guaranteed to terminate by virtue of its definition being type
this formulation is much less intuitive. It is also not convenient at                        checked. In Isabelle/HOL, termination is established after the fact
all to work with when reasoning about a larger algorithm that uses                           (though automatically in many cases) through additional external
quick_select. Appealing to the concept of Permutation enables                                proof obligations generated by the framework [15].
concise and intuitive specification of the algorithm’s behavior.

5     RELATED WORK                                                                           6   DISCUSSION AND CONCLUSION
Verification of classic, or “textbook,” algorithms and data structures                       As commonly the case with formalization exercises, our experience
has a long history in mechanical verification and theorem proving.                           with the KNN search algorithm forced a complete understanding
The subtle and nuanced invariants involved mean that the process                             of all its operational nuances. In particular, since portions of the
often needs to be guided interactively (as opposed to using fully                            development were attended by a team of undergraduate students,
automated methods). Nipkow et al.[16] reviews the state of the art                           correctness of the pruning behavior and understanding of its rigor-
at the beginning of the current decade. As surveyed in that work,                            ous justification, instead of simply an intuitive sense, became very
there are a variety of systems and frameworks used for algorithm                             necessary. Low-level details that are often omitted, assumed, or
verification. In our use of Coq, the present work resembles algo-                            ignored in standard presentations had to be explicitly worked out
rithms and data structures verified by Appel [2], although 𝑘-d trees                         and stated in order for the proof development to go through. In fact,
are slightly more complex than the material covered there. In terms                          presentations of the 𝑘-d tree-based KNN search algorithm generally
of the complexity of the data structure and algorithm, our work                              omit rigorous explanation of correctness, assuming that it is self-
is similar to the verification of the Gale-Shapley stable matching                           evident. Thus, in developing the specifications and proofs described
algorithm in [11].                                                                           above, we followed our own initiative, rather than following a prior
   To our knowledge, there is no prior work in Coq formally veri-                            published “paper” proof.
fying 𝑘-d trees or any type of nearest neighbor search algorithm.                               While achievable with reasonable effort, the formal develop-
After completing our verification project, we did became aware of                            ments were still non-trivial. In our project, we used only the stan-
an earlier, independent formalization and verification based on the                          dard Coq library and little proof automation, leading to some long
Isabelle/HOL proof assistant, not described or published other than                          proof scripts, particularly for Lemma 4.4. Patterns emerged in the
the script in the Archive of Formal Proofs [7, 17]. The latter verifies                      proofs, where many progressed by induction on the 𝑘-d tree struc-
a more sophisticated pivot selection algorithm, median-of-medians,                           ture and then case analysis of the three conditional expressions of
whereas our formalization simply picks an arbitrary pivot, since                             the algorithm (lines 9, 17, 18 in Figure 5). Since there were sym-
                                                                                             metric, but different orders, of the recursive calls in the body, this
7 This says, the number of elements in 𝑙 strictly less than 𝑣 is less than or equal to 𝑘 .   led to duplicate runs of tactics in the script with slightly different
, ,                                                                                                                                                      Nadeem Abdul Hamid


initial contexts. This leaves an opportunity to explore better ways                      REFERENCES
to structure or refactor the proofs to abstract the commonalities                         [1] 2022. The Coq Proof Assistant, v8.16. https://coq.inria.fr/
based on the execution paths of the algorithm.                                            [2] Andrew W. Appel. 2023. Verified Functional Algorithms. Electronic textbook.
                                                                                              https://softwarefoundations.cis.upenn.edu/vfa-current
   An alternate avenue for future exploration would be better proof                       [3] Jon Louis Bentley. 1975. Multidimensional Binary Search Trees Used for Asso-
automation [5] and the use of more sophisticated techniques or                                ciative Searching. Commun. ACM 18, 9 (sep 1975), 509–517. https://doi.org/10.
                                                                                              1145/361002.361007
extensions [10]. In particular, while we believe the concept of list                      [4] Thomas Braibant and Damien Pous. 2011. Tactics for Reasoning Modulo AC in
permutations is a good way to express specifications, the most                                Coq. In Certified Programs and Proofs, Jean-Pierre Jouannaud and Zhong Shao
verbose and tedious portions of the proof involved deriving facts                             (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 167–182.
                                                                                          [5] Adam Chlipala. 2013. Certified Programming with Dependent Types: A Pragmatic
about permutation relationships. Reasoning about permutations                                 Introduction to the Coq Proof Assistant. The MIT Press.
between lists seems like a good candidate for proof automation.                           [6] Pádraig Cunningham and Sarah Jane Delany. 2021. K-Nearest Neighbour Clas-
Many exercises in [2] also lead to tedious proofs involving permu-                            sifiers - A Tutorial. ACM Comput. Surv. 54, 6, Article 128 (jul 2021), 25 pages.
                                                                                              https://doi.org/10.1145/3459665
tations, but to our knowledge there is no existing tactic library to                      [7] Manuel Eberl. 2017. The Median-of-Medians Selection Algorithm. Archive of
assist with such.8 Developing a decision procedure for this purpose                           Formal Proofs (December 2017). https://isa-afp.org/entries/Median_Of_Medians_
                                                                                              Selection.html, Formal proof development.
would contribute a useful tool to the Coq ecosystem and we hope                           [8] Jerome H. Friedman, Jon Louis Bentley, and Raphael Ari Finkel. 1977. An Al-
to pursue this in the short term.                                                             gorithm for Finding Best Matches in Logarithmic Expected Time. ACM Trans.
   Coq provides a Program [18] tactic that would allow defining                               Math. Softw. 3, 3 (sep 1977), 209–226. https://doi.org/10.1145/355744.355745
                                                                                          [9] Giorgio Giacinto. 2007. A Nearest-Neighbor Approach to Relevance Feedback
functions like qsp and build_kdtree_ without a fuel argument. It                              in Content Based Image Retrieval. In Proceedings of the 6th ACM International
does, however, introduce its own additional layers of complexity in                           Conference on Image and Video Retrieval (Amsterdam, The Netherlands) (CIVR
the verification process. In future work, the trade-offs of using that                        ’07). Association for Computing Machinery, New York, NY, USA, 456–463. https:
                                                                                              //doi.org/10.1145/1282280.1282347
alternate definition could be explored.                                                  [10] Georges Gonthier, Assia Mahboubi, and Enrico Tassi. 2016. A Small Scale Reflec-
   There are several different directions we envision future work                             tion Extension for the Coq system. Research Report RR-6455. Inria Saclay Ile de
                                                                                              France. https://inria.hal.science/inria-00258384
could pursue in the long term. One would be to develop a verifica-                       [11] Nadeem Abdul Hamid and Caleb Castleberry. 2010. Formally Certified Stable
tion of an imperative implementation of the algorithms and data                               Marriages. In Proceedings of the 48th Annual Southeast Regional Conference (Ox-
structures described in this paper. While that involves additional                            ford, Mississippi) (ACM SE ’10). Association for Computing Machinery, New York,
                                                                                              NY, USA, Article 34, 6 pages. https://doi.org/10.1145/1900008.1900056
levels of complexity (and would necessitate reasoning about a sepa-                      [12] C. A. R. Hoare. 1961. Algorithm 65: Find. Commun. ACM 4, 7 (jul 1961), 321–322.
rate language, e.g. C or Java), in developing our work for this paper                         https://doi.org/10.1145/366622.366647
we attempted to stay as close to traditional presentations of the                        [13] Kimikazu Kato and Tikara Hosino. 2010. Solving K-Nearest Neighbor Problem
                                                                                              on Multiple Graphics Processors. In Proceedings of the 2010 10th IEEE/ACM Inter-
algorithms as possible. We believe this will make it easier to port                           national Conference on Cluster, Cloud and Grid Computing (CCGRID ’10). IEEE
the specifications and proofs to an imperative context. There are                             Computer Society, USA, 769–773. https://doi.org/10.1109/CCGRID.2010.47
                                                                                         [14] Donald Knuth. 1973. The Art Of Computer Programming, vol. 3: Sorting And
also a number of alternate, modern space-partitioning tree variants                           Searching. Addison-Wesley. 391–392 pages.
used for both exact and, particularly, approximate KNN search. Ap-                       [15] Alexander Krauss, Christian Sternagel, René Thiemann, Carsten Fuhs, and Jürgen
plying our methods to any of these is a way to make the results                               Giesl. 2011. Termination of Isabelle Functions via Termination of Rewriting. In In-
                                                                                              teractive Theorem Proving, Marko van Eekelen, Herman Geuvers, Julien Schmaltz,
more potentially applicable for practical, industry use.                                      and Freek Wiedijk (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 152–
   Finally, we hope to extend our current results to explore specifi-                         167.
cation and verification of machine learning algorithms built upon                        [16] Tobias Nipkow, Manuel Eberl, and Maximilian P. L. Haslbeck. 2020. Verified
                                                                                              Textbook Algorithms. A Biased Survey. In ATVA 2020, Automated Technology for
nearest neighbor search. As alluded to in the introduction, there                             Verification and Analysis (LNCS, Vol. 12302), Dang Van Hung and Oleg Sokolsky
are a wide variety of areas where such techniques are used that are                           (Eds.). Springer, 25–53. Invited paper.
                                                                                         [17] Martin Rau. 2019. Multidimensional Binary Search Trees. Archive of Formal Proofs
becoming increasingly safety-critical. We envision formal methods                             (May 2019). https://isa-afp.org/entries/KD_Tree.html, Formal proof development.
and theorem proving techniques as a useful tool for developing and                       [18] Matthieu Sozeau. 2007. Subset Coercions in Coq. In Types for Proofs and Programs,
verifying high-level operational properties of such systems, built                            Thorsten Altenkirch and Conor McBride (Eds.). Springer Berlin Heidelberg, Berlin,
                                                                                              Heidelberg, 237–252.
upon core data structures and algorithms such as those verified in                       [19] Pavan Turaga and Rama Chellappa. 2010. Nearest-Neighbor Search Algorithms
this paper.                                                                                   on Non-Euclidean Manifolds for Computer Vision Applications. In Proceedings of
                                                                                              the Seventh Indian Conference on Computer Vision, Graphics and Image Processing
                                                                                              (Chennai, India) (ICVGIP ’10). Association for Computing Machinery, New York,
ACKNOWLEDGMENTS                                                                               NY, USA, 282–289. https://doi.org/10.1145/1924559.1924597
                                                                                         [20] Xindong Wu, Vipin Kumar, J. Ross Quinlan, Joydeep Ghosh, Qiang Yang, Hiroshi
The author would like to thank his students, Matthew Bowker, Jes-                             Motoda, Geoffrey J. McLachlan, Angus Ng, Bing Liu, Philip S. Yu, Zhi-Hua Zhou,
sica Herring, and Bernny Velasquez for participating in discussions                           Michael Steinbach, David J. Hand, and Dan Steinberg. 2007. Top 10 Algorithms
on this project and preliminary efforts on verification of the single                         in Data Mining. Knowl. Inf. Syst. 14, 1 (dec 2007), 1–37. https://doi.org/10.1007/
                                                                                              s10115-007-0114-2
nearest neighbor algorithm. Another team of students, Riley Croker,
Britt Smith, and Jeffrey Stephens, worked much earlier on an initial
formalization of quick_select in Coq, which served as a base for the
version presented in this work.
   The author would also like to thank the anonymous reviewers
for their valuable comments and constructive suggestions on earlier
versions of the manuscript.

8 The closest we found is [4], a general-purpose Coq plugin for rewriting modulo asso-
ciativity and commutativity with some limited application to lists and permutations.
(Nearest) Neighbors You Can Rely On: Formally Verified 𝑘 -d Tree Construction and Search in Coq                                                    , ,


A     COQ STATEMENTS OF LEMMAS AND                                                      Lemma In_kdtree_bounded_bb_contains :
      THEOREMS                                                                              forall tree bb v, kdtree_bounded tree bb = true ->
                                                                                            In_kdtree v tree -> bb_contains bb v = true.
(** Quickselect **)
                                                                                        Lemma build_kdtree_bounded : forall (k:nat) (data:list datapt),
Theorem qsp_works :
                                                                                            0 < k ->
  forall (X:Set) steps (k:nat) (l:list X) (le:X -> X -> bool),
                                                                                            (forall v', In v' data -> length v' = k) ->
  k < length l ->
                                                                                            kdtree_bounded (build_kdtree k data)
  length l <= steps ->
                                                                                                       (mk_bbox (repeat None k) (repeat None k)) = true.
  exists p, qsp steps k l le = Some p.
                                                                                        Lemma cep_min_dist :
Theorem quick_select_always_some :
                                                                                            forall vs mins maxs ws,
  forall (X:Set) (k:nat) (l:list X) (le:X -> X -> bool),
                                                                                            cep vs mins maxs = ws ->
  k < length l ->
                                                                                            forall pt, bb_contains (mk_bbox mins maxs) pt = true ->
  exists l1 v l2, quick_select k l le = Some (l1,v,l2).
                                                                                            sum_dist vs ws <= sum_dist vs pt.
Theorem quick_select_permutation :
                                                                                        Lemma build_kdtree_contents_perm_gen
  forall (X:Set) (k:nat) (l:list X) (le:X -> X -> bool) l1 l2 v,
                                                                                            : forall fuel k data depth_mod,
  quick_select k l le = Some (l1, v, l2) ->
                                                                                              0 < k ->    (* need for next_depth_lt *)
  Permutation l (l1 ++ v :: l2).
                                                                                              depth_mod < k ->
                                                                                              length data <= fuel) ->
Theorem qsp_position : forall (X:Set) steps (k:nat) (l:list X)
                                                                                              exists lst,
    (le:X -> X -> bool) l1 l2 v,
                                                                                                Contents_kdtree
  qsp steps k l le = Some (l1, v, l2) ->
                                                                                                    (build_kdtree_ fuel k data depth_mod) lst /\
  length l1 = k.
                                                                                                Permutation data lst.
Theorem qsp_all_smaller : forall (X:Set) steps (k:nat) (l:list X)
                                                                  Lemma build_kdtree_contents_perm
    (le:X -> X -> bool) l1 l2 v (Hle:le_props le),
                                                                      : forall k data (Hk : 0 < k),
  qsp steps k l le = Some (l1, v, l2) ->
                                                                        exists lst, Contents_kdtree (build_kdtree k data) lst /\
  forall x, In x l1 -> le x v = true.
                                                                                    Permutation data lst.
Theorem qsp_all_larger : forall (X:Set) steps (k:nat) (l:list X)
                                                                                        (** KNN Search **)
    (le:X -> X -> bool) l1 l2 v (Hle:le_props le),
  qsp steps k l le = Some (l1, v, l2) ->
                                                                                        Lemma knn_search_build_size_gen :
  forall x, In x l2 -> le v x = true.
                                                                                            forall tree bb K k data query pq lst,
                                                                                            priq _ _ pq ->
Theorem quick_select_exists_correct :
                                                                                            Abs _ _ pq lst ->
  forall (X:Set) (k:nat) (l:list X) (le:X -> X -> bool),
                                                                                            Contents_kdtree tree data ->
  le_props le ->
                                                                                            size _ _ pq <= K ->
  k < length l ->
                                                                                            size datapt (sum_dist query) (knn K k tree bb query pq)
  exists l1 v l2,
                                                                                                = (min K ((length data) + (size _ _ pq))).
    quick_select k l le = Some (l1,v,l2) /\
    Permutation l (l1 ++ v :: l2) /\
                                                                                        Lemma knn_search_build_size :
    length l1 = k /\
                                                                                            forall K k data query,
    (forall x, In x l1 -> le x v = true) /\
                                                                                            0 < k ->
    (forall x, In x l2 -> le v x = true).
                                                                                            size datapt (sum_dist query)
                                                                                                (knn K k (build_kdtree k data)
(** Bounding Boxes and k-d Trees **)
                                                                                                         (mk_bbox (repeat None k) (repeat None k))
                                                                                                         query (empty _ _))
Definition bb_split (bb:bbox) (d:nat) (v:nat) : bbox * bbox :=
                                                                                                = min K (length data).
  let `(mk_bbox bb_min bb_max) := bb in
  ( mk_bbox bb_min (list_set bb_max d (Some v)),
                                                                  Lemma perm_split_rearrange_all_in_leb :
    mk_bbox (list_set bb_min d (Some v)) bb_max ).
                                                                      forall A key lst (a:list A) b c d
    (* list_set updates the d'th coordinate of a data point *)
                                                                          (Hab : Permutation (a ++ b) lst)
                                                                          (Hde : Permutation (c ++ d) lst)
Fixpoint kdtree_bounded (tree:kdtree) (bb:bbox) : bool :=
                                                                          (Hleb : @all_in_leb A key c d),
    match tree with
                                                                          exists a1 a2 b1 b2, Permutation (a1 ++ a2) a /\
    | mt_tree => true
                                                                                              Permutation (b1 ++ b2) b /\
    | node ax pt lft rgt =>
                                                                                              Permutation (a1 ++ b1) c /\
       bb_contains bb pt
                                                                                              Permutation (a2 ++ b2) d /\
       && kdtree_bounded lft (fst (bb_split bb ax (nth ax pt 0)))
                                                                                              all_in_leb key a1 a2 /\
       && kdtree_bounded rgt (snd (bb_split bb ax (nth ax pt 0)))
                                                                                              all_in_leb key b1 b2.
    end.
, ,                                                                     Nadeem Abdul Hamid




Lemma knn_full_relate_gen :
    forall (K k : nat) (tree : kdtree) (bb : bbox)
           (query : list nat)
           (pq : MaxPQ.priqueue datapt (sum_dist query))
           (lst data result : list datapt),
    0 < K ->
    kdtree_bounded tree bb = true ->
    Contents_kdtree tree data ->
    MaxPQ.priq datapt (sum_dist query) pq ->
    MaxPQ.Abs datapt (sum_dist query) pq lst ->
    MaxPQ.priq datapt (sum_dist query) (knn K k tree bb query pq) ->
    MaxPQ.Abs datapt (sum_dist query)
                                 (knn K k tree bb query pq) result ->
    exists lstSm lstLg dataSm dataLg leftover : list datapt,
         Permutation (lstSm ++ lstLg) lst /\
         Permutation (dataSm ++ dataLg) data /\
         Permutation (lstSm ++ dataSm) result /\
         Permutation (lstLg ++ dataLg) leftover /\
         (MaxPQ.size datapt (sum_dist query)
                            (knn K k tree bb query pq) < K ->
          leftover = []) /\
         all_in_leb (sum_dist query) result leftover

Lemma knn_full_relate :
    forall K k data query,
    0 < K ->
    0 < length data ->
    0 < k ->
    (forall v' : datapt, In v' data -> length v' = k) ->
    forall pq,
    pq = (knn K k (build_kdtree k data)
                  (mk_bbox (repeat None k) (repeat None k))
                  query (empty datapt (sum_dist query))) ->
    exists result leftover : list datapt,
        Permutation data (result ++ leftover) /\
        Abs datapt (sum_dist query) pq result /\
        all_in_leb (sum_dist query) result leftover.

Theorem knn_search_build_kdtree_correct :
    forall (K:nat) (k : nat) (data : list datapt),
    0 < K ->
    0 < length data ->
    0 < k ->
    (forall v' : datapt, In v' data -> length v' = k) ->
    forall tree query result,
    tree = (build_kdtree k data) ->
    knn_search K k tree query = result ->
    exists leftover,
        length result = min K (length data)
        /\ Permutation data (result ++ leftover)
        /\ all_in_leb (sum_dist query) result leftover.
