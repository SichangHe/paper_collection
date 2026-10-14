                                              Formal Verification of Minimax Algorithms

                                                            Wieger Wesselink1[0009−0001−6746−5115] ,
                                                            Kees Huizing1[0000−0002−4713−7253] , and
                                                           Huub van de Wetering1[0000−0002−0517−1322]

                                                        Eindhoven University of Technology, The Netherlands
                                                         {j.w.wesselink,h.v.d.wetering,c.huizing}@tue.nl
arXiv:2509.20138v2 [cs.AI] 22 Apr 2026




                                               Abstract. Minimax-based search algorithms with alpha-beta pruning
                                               and transposition tables are a central component of classical game-playing
                                               engines and remain widely used in practice. Despite their widespread use,
                                               these algorithms are subtle, highly optimized, and notoriously difficult
                                               to reason about, making non-obvious errors hard to detect by testing
                                               alone. Using the Dafny verification system, we formally verify a range
                                               of minimax search algorithms, including variants with alpha-beta prun-
                                               ing and transposition tables. For depth-limited search with transposition
                                               tables, we introduce a witness-based correctness criterion that captures
                                               when returned values can be justified by an explicit game-tree expansion.
                                               We apply this criterion to two practical variants of depth-limited nega-
                                               max with alpha-beta pruning and transposition tables: for one variant,
                                               we obtain a fully mechanized correctness proof, while for the other we
                                               construct a concrete counterexample demonstrating a violation of the
                                               proposed correctness notion. All verification artifacts, including Dafny
                                               proofs and executable Python implementations, are publicly available.

                                               Keywords: Formal Verification · Dafny · Minimax · Alpha-Beta Prun-
                                               ing · Depth-limited search · Transposition Tables.


                                         1   Introduction

                                         Game tree search algorithms, such as minimax and its optimization via alpha-
                                         beta pruning, compute optimal moves by recursively evaluating all possible out-
                                         comes under the assumption of perfect play. These algorithms assign values to
                                         game states based on the principle that one player seeks to maximize the evalua-
                                         tion, while the opponent seeks to minimize it. The alpha-beta pruning technique,
                                         which may significantly improve the efficiency of minimax by pruning branches
                                         that cannot affect the final decision, was analyzed in detail by Knuth and Moore
                                         in their seminal work [5]. Various theoretical frameworks have been applied to
                                         minimax and related algorithms, including lattice theory [1] and AND/OR tree
                                         representations [10]. Several variations of alpha-beta pruning exist. In [5], the
                                         fail-hard variant of alpha-beta pruning is discussed, while Fishburn introduced
                                         fail-soft variants in [3, 4]. More recently, Nipkow et al. have verified implementa-
                                         tions of several minimax variants in a functional programming setting using the
2       W. Wesselink et al.

Isabelle proof assistant [8]. Their work includes a verified transposition-table-
based algorithm, but only in the setting of depth-unlimited search. This setting
avoids many of the subtleties that arise in depth-limited search, where partially
explored subtrees and varying depths complicate the formulation and verifica-
tion of correctness criteria for transposition table usage. In this paper, we focus
on the formal verification of minimax and negamax [10] algorithms in an im-
perative setting using Dafny, a programming language and verifier designed for
writing provably correct programs [6]. Dafny is grounded in Floyd-Hoare logic
and supports automated reasoning through constructs such as preconditions,
postconditions, assertions, loop invariants, and lemmas.
    The central challenge we address is the formalization of correctness for depth-
limited search with transposition tables, where cached results obtained at differ-
ent depths and under different search windows break the simple tree-traversal
semantics typically used to justify minimax and alpha-beta pruning. In this set-
ting, correctness can no longer be explained solely in terms of a single execution
tree. To address this, we introduce a flexible, witness-based correctness criterion
that can account for partially explored subtrees and reused results from trans-
position tables. Using this framework, we verify both standard depth-limited
minimax/negamax and practical extensions with transposition tables. These al-
gorithms are widely used in game-playing engines and are known to be subtle
and error-prone; even small implementation differences can lead to unexpected
behavior. Our work demonstrates how formal verification can provide a robust
foundation for reasoning about their correctness in practice.

                                                                  0
2   Definitions
A game tree is a rooted directed acyclic graph rep-             0     -2
resenting the possible evolutions of a two-player
game. Each node corresponds to a game position,
and each edge to a legal move. Nodes are colored               -1      2       1
by the player to move: white for the maximizer
and gray for the minimizer, as illustrated in Fig-
ure 1. Formally, a node is defined as a record with       3       4
three attributes:
                 
                  eval     : evaluation value         Fig. 1: Game tree with white
Node = record color         : player to move (±1) maximizer nodes and gray
                 
                   children : ordered child list       minimizer nodes, labeled
                                                       with evaluation values.
The eval field encodes an integer value of a game
state: the maximizer (color =1) favors higher, while the minimizer (color =-1)
favors lower values. Internal nodes use heuristic evaluations, while leaves reflect
game-theoretic values. The children list defines the successors of a node u in a
fixed order, inducing edges (u, v) iff v ∈ u.children. A fixed order is not strictly
necessary, but it is commonly used and enables deterministic execution. We
assume acyclicity, as repetition rules in games like chess and draughts preclude
                                 Formal Verification of Minimax Algorithms       3

infinite loops in practice. Nodes abstract from concrete game states: equality is
structural, requiring identical eval, color, and isomorphic subtrees. This suffices
for search correctness while avoiding full state representation. Since a node u
implicitly defines the subtree rooted at u, we use the terms node and game tree
interchangeably. For a game tree u we recursively define minimax(u) as
  
  u.eval
                                         if |u.children| = 0
    min{minimax(v) | v ∈ u.children} if |u.children| > 0 and u.color = −1 (1)
  
    max{minimax(v) | v ∈ u.children} if |u.children| > 0 and u.color = 1
  

and negamax(u) as
         (
          u.color · u.eval                          if |u.children| = 0
                                                                               (2)
            max{−negamax(v) | v ∈ u.children} if |u.children| > 0.

For minimax, we allow the same player to move consecutively. For negamax, the
game must be turn-based, i.e., for each node u the following holds:

                      ∀v ∈ u.children : v.color = −u.color.                    (3)

Note that the two functions are the same up to a sign inversion.

                       negamax(u) = u.color · minimax(u).                      (4)

In depth-limited search, we work with truncated game trees. For a game tree
u with root node r, the depth-d truncation ⌊u⌋d is the subtree consisting of all
nodes whose path from r has length at most d, along with all edges connecting
them. The root r is at distance 0, and nodes at distance greater than d are
excluded.

2.1   Alpha-beta Pruning
Alpha-beta pruning is an optimization of minimax search that avoids explor-
ing parts of the game tree without affecting the final decision. The algorithm
maintains a window (α, β) of values that are relevant to the outcome. If the
exact minimax (or negamax) value lies strictly within this window, it must be
computed precisely; if it lies outside the window, any value that preserves the
appropriate bound is sufficient. This allows the search to terminate early in
branches that are irrelevant to the root decision. To formalize this behavior, we
introduce several predicates used in the verification of alpha-beta pruning:

  is-ab-result(x, e, α, β) = (e ≤ x ≤ α) ∨ (α < e = x < β) ∨ (β ≤ x ≤ e),      (5)
  is-negamax-ab-result(x, u, α, β) = is-ab-result(x, negamax(u), α, β)         (6)

where the predicate is-ab-result, adapted from Fishburn [4], specifies when a
value x is an acceptable result for a true minimax or negamax value e under the
4        W. Wesselink et al.

window (α, β). The three cases correspond to returning an upper bound (e ≤ x),
an exact value (e = x), or a lower bound (x ≤ e), respectively. To support
reasoning about partial computations, we also define

    is-partial-negamax-ab-result(x, u, i, α, β) = is-ab-result(x, pnm(u, i), α, β),   (7)

where pnm(u, i) = max{−negamax(u.children[j]) | 0 ≤ j < i} denotes the partial
negamax value obtained after evaluating the first i children of u. This notion is
used to express loop invariants and intermediate correctness conditions in the
verification.


2.2    Transposition Tables

A transposition table (TT) is a cache used to avoid repeated computations in
game-tree search by storing results of previously visited states. Formally, it rep-
resents a partial mapping from states (nodes) to search results. We define a table
entry as follows:

                   TableEntry = record
                       
                       value estimated minimax value,
                         depth search depth at evaluation time,
                         flag value classification (see below).
                       

The flag attribute identifies the relationship between the stored value and an
exact minimax or negamax value of the state:
                
                exact (EX)
                                      value is an exact value,
                  lowerbound (LB) value is a lower bound,
                
                  upperbound (UB) value is an upper bound.
                

Despite their widespread use, the formal semantics of transposition tables is typ-
ically underspecified. While the flag indicates how the stored value relates to an
exact minimax value, it does not specify with respect to which game tree this
exact value is defined. In particular, table entries may be produced by searches
performed at different depths, under different alpha-beta windows, and in dif-
ferent parts of the game tree. As a result, the meaning of a table entry cannot
be understood in isolation: its validity depends implicitly on a search context
that is not recorded in the table itself. This lack of a precise semantic foundation
complicates formal reasoning about the correctness of transposition-table-based
search.
    In this work, we intentionally restrict the contents of the transposition table
to values, depths, and flags, and do not store best moves. Best moves are com-
monly used to reorder successor nodes and thereby improve search efficiency, but
they do not affect the correctness of returned values. Since our focus is on estab-
lishing value correctness rather than on performance characteristics, we exclude
best-move information from the formal model.
                                 Formal Verification of Minimax Algorithms       5




Algorithm 1 Minimax                       Algorithm 2 Negamax
Input: A game tree u.                     Input: A game tree u.
Output: minimax(u).                       Output: negamax(u).
minimax(u):                               negamax(u):
 1: if |u.children| = 0 then               1: if |u.children| = 0 then
 2: return u.eval                          2: return u.color · u.eval
 3: else if u.color = −1 then              3: else
 4: value := ∞                             4: value := −∞
 5: for v ∈ u.children do                  5: for v ∈ u.children do
 6:     value := min(value, minimax(v))    6:     value := max(value, −negamax(v))
 7: return value                           7: return value
 8: else
 9: value := −∞
10: for v ∈ u.children do
11:     value := max(value, minimax(v))
12: return value



3   Algorithm Pseudocode

This section introduces a selection of the game tree search algorithms that we
have formally verified using Dafny. The classical Minimax algorithm (Algo-
rithm 1) recursively evaluates a game tree to determine the optimal value at the
root under perfect play. Each internal node loops over its children to compute ei-
ther the minimum or maximum value, depending on the player to move. Instead
of handling separate cases for minimizing and maximizing nodes Negamax (Al-
gorithm 2), is a reformulation of minimax that exploits symmetry between the
players, using negation to unify both into a single recursive structure. Negamax
simplifies implementation, making it the de facto standard. We further consider
two negamax algorithms that combine depth-limited search, alpha-beta pruning,
and transposition tables (TT), see Algorithm 3. The first, which we refer to as
NegamaxTTW, is a variant commonly described in community sources such as
Wikipedia (W), though its precise origin is unclear and likely influenced by work
such as [7, 2]. The second, which we refer to as NegamaxTTM, is a related al-
gorithm from Marsland (M) [7] that uses a different transposition table strategy.
Special handling of the best move has been removed from NegamaxTTM. Both
algorithms consist of three distinct phases: a table lookup, a negamax search and
a table update. In Section 4.5 the differences between them will be discussed.


4   Verification using Dafny

The modeling of data types in Dafny is straightforward, see Listing 1. While in
the pseudocode we used the value ∞, in our Dafny modeling we use a bounded
6      W. Wesselink et al.


Algorithm 3 Transposition-table-based Negamax search variants. Algo-
rithm NegamaxTTW follows Wikipedia [12], while Algorithm NegamaxTTM
follows Marsland [7]. Both algorithms take as input a node u, an alpha-beta win-
dow (α, β), a search depth d, and a transposition table T . Both algorithms are
subdivided in three phases: Table Lookup, Negamax Search, and Table Update.

    function NegamaxTTW(u, α, β, d, T ):
    α0 := α                                                     ▷ Table Lookup
    if u ∈ T then
       t := T [u]
       if t.depth ≥ d then
           if t.flag = exact then return t.value
           else if t.flag = lowerbound ∧ t.value ≥ β then return t.value
           else if t.flag = upperbound ∧ t.value ≤ α then return t.value
    if d = 0 ∨ |u.children| = 0 then return u.color · u.eval ▷ Negamax Search
    value := −∞
    for v ∈ u.children do
        value := max(value, −NegamaxTTW(v, −β, −α, d − 1, T ))
        α := max(α, value)
        if α ≥ β then break
    if value ≤ α0 then T [u] := (value, d, upperbound)           ▷ Table Update
    else if value ≥ β then T [u] := (value, d, lowerbound)
    else T [u] := (value, d, exact)
    return value


    function NegamaxTTM(u, α, β, depth, T ):
    if u ∈ T then                                                ▷ Table Lookup
       t := T [u]
       if t.depth ≥ d then
           if t.flag = exact then return t.value
           else if t.flag = lowerbound then α := max(α, t.value)
           else if t.flag = upperbound then β := min(β, t.value)
           if α ≥ β then return t.value
    if d = 0 ∨ |u.children| = 0 then return u.color · u.eval ▷ Negamax Search
    value := −∞
    for v ∈ u.children do                                                 
        value := max value, −NegamaxTTM(v, −β, − max(α, value), d − 1, T )
        if value ≥ β then break
    flag := exact                                                ▷ Table Update
    if value ≤ α then flag := upperbound
    if value ≥ β then flag := lowerbound
    if u ∈/ T ∨ T [u].depth ≤ d then T [u] := (value, d, flag)
    return value
                                         Formal Verification of Minimax Algorithms             7

    Listing 1 The datatypes used in Dafny
1     type bounded_int = x : int | - INFINITY < = x < = INFINITY
2     datatype Color = White | Black
3     datatype Node = Node_ ( eval : bounded_int , color : Color , children : seq < Node > )
4     datatype Flag = Lowerbound | Upperbound | Exact
5     datatype TableEntry = TableEntry_ ( depth : nat , value : bounded_int , flag : Flag )
6     type TranspositionTable = map < Node , TableEntry >




    integer type, where INFINITY is an unspecified positive integer constant. This
    is also common in practical implementations. The verifier automatically checks
    that variables remain within the allowed domain. Note that recursive datatypes
    in Dafny, such as Node, are free from cycles by construction. To verify correctness,
    we translated each algorithm from pseudocode into Dafny syntax. For example,
    NegamaxTTW in Algorithm 3 corresponds to Dafny Listing 2.


    4.1   Correctness of Transposition Table Search

    For depth-limited transposition-table-based algorithms NegamaxTT[W,M], the
    returned results may depend on values computed earlier in unrelated parts of
    the game tree, potentially at greater depth than required at the current node.
    Effectively, the algorithm explores an expansion of the depth-d truncated tree
    by greedily reusing deeper search results via the transposition table. Figure 2(r)
    illustrates this behavior: the primary search unfolds as a triangle-shaped subtree
    rooted at the current node. Upon a transposition table hit, the algorithm may
    reuse a value previously computed in a deeper search of a different subtree. So
    not only the nodes in the depth-d truncated tree contribute to the search re-
    sult, but also recursively the nodes in these (reused) subtrees. This motivates
    our notion of a witness, a concrete expansion of the truncated tree that merges
    all such reused subtrees into a single game tree. Such an expansion u′ can be
    obtained from u by removing all children of some nodes in u at depth at least
    d. Correctness is then characterized by the existence of a witness, an expansion
    whose minimax (or negamax) value equals the value returned by the algorithm.
    To formalize this notion, we impose four conditions on a witness:

     1. The witness u′ is a subtree of the original tree u.
     2. The witness contains the complete depth-d truncation of u: ⌊u⌋d = ⌊u′ ⌋d .
     3. For any node z ′ in u′ corresponding to z in u, either all children of z are
        included in u′ , or none.
     4. The algorithm’s returned value matches the negamax alpha-beta result on
        the witness u′ , as defined in (6).

    The equality ⌊u⌋d = ⌊u′ ⌋d in condition 2 is understood as isomorphism of the two
    truncated trees: they have identical branching structure and node evaluations
    within depth d. Condition 3 is crucial: it prevents a witness from including
    arbitrary subsets of a node’s children, which would produce subtrees that do
8         W. Wesselink et al.

not correspond to any valid minimax or negamax search. Conditions 1-3 are
formalized in the predicate is-expansion. Let C = u.children and C ′ = u′ .children:


is-expansion(u′ , u, d) = u.eval = u′ .eval ∧ u.color = u′ .color ∧                      (8)
  
  (|C| = |C ′ | ∧ ∀ i ∈ [0, |C|) : is-expansion(Ci′ , Ci , d − 1)) ,               if d > 0
    (|C ′ | = 0 ∨ (|C| = |C ′ | ∧ ∀ i ∈ [0, |C|) : is-expansion(C ′ , C , 0))) ,   if d = 0
                                                                     i   i


The first case ensures that the truncated tree ⌊u⌋d is included, while the second
enforces the “all-or-none children” requirement of Condition 3.
   Correctness of the algorithm is then defined as:

      is-negamax-tt-result(result, u, α, β, depth) =
                                                                                         (9)
        ∃u′ : is-expansion(u′ , u, depth) ∧ is-negamax-ab-result(result, u′ , α, β).

Moreover, for each entry t in the transposition table, a witness must exist justi-
fying that entry:

                 is-valid-table-entry(t, u) = ∃u′ : is-expansion(u′ , u, t.depth) ∧
                     
                                              ′
                     t.value ≥ negamax(u ), if t.flag = upperbound
                     
                        t.value = negamax(u′ ), if t.flag = exact                       (10)
                        t.value ≤ negamax(u′ ), if t.flag = lowerbound
                     
                     

We adopt a permissive model of the transposition table. At every iteration of
the algorithm, we allow the table’s contents to change arbitrarily, as long as the
entries satisfy (10). This reflects practical implementations, where transposition
tables are typically realized using hash tables: insertions may overwrite existing
entries due to collisions and replacement strategies.
    Importantly, this model does not restrict how a witness is obtained. Any
witness satisfying Conditions 1-3 can be justified compositionally by valid trans-
position table entries, independently of a specific execution trace. Intuitively,
the witness may be viewed as being assembled incrementally from shallow (e.g.,
one-ply) table lookups, but the correctness argument relies only on the existence
of such a witness, not on its constructive derivation.

4.2      Verification of NegamaxTTW
We formally verified the Wikipedia variant of transposition-table-based negamax
search, NegamaxTTW, using Dafny against the correctness criteria defined in
Equations (9) and (10). The Dafny development for this algorithm comprises
approximately 850 lines of code, and verification completes in about 4 seconds
on a standard workstation. The core algorithm is shown in Listing 2.
   The verification effort involved several nontrivial challenges. First, correct-
ness had to be expressed in terms of witnesses rather than concrete execution
                                             Formal Verification of Minimax Algorithms                  9

depth-limited search of game tree u         with transposition table                        expansion

                    truncated tree ⌊u⌋d
                                                                 transposition table hit

d                                                                      contributing nodes
                           visited/pruned nodes




Fig. 2: Schematic truncated game tree showing the visited/pruned nodes for
depth-d searching without (l) and with (m) transposition table. The expansion
(r) with all nodes directly and indirectly contributing to the table-based search.


traces, requiring the specification of structural properties of expanded game
trees. Second, suitable loop invariants were needed to relate intermediate search
results, transposition table contents, and partially constructed witnesses. Third,
the verification required reasoning about the incremental assembly of a witness
tree that satisfies the expansion constraints introduced in Section 2.
    Dafny proved effective for establishing many basic properties largely auto-
matically. In particular, the is-expansion predicate admits a rich collection of lem-
mas that were relatively straightforward to verify, including reflexivity and tran-
sitivity, preservation under subtree inclusion, inclusion of the depth-truncated
tree, and preservation of the expansion property when a subtree is replaced by
a witness justified by a transposition table lookup.
    At the same time, the verification process exposed limitations of automated
reasoning in the presence of deeply nested quantifiers, which arise naturally when
formalizing game trees, expansions, and transposition-table invariants. Without
careful structuring, the verifier would often time out or exhaust memory. To ad-
dress this, we systematically separated proof obligations and discharged them via
explicit lemma invocations rather than inline reasoning, particularly at return
points, loop exits, and invariant maintenance boundaries. For NegamaxTTW,
this strategy resulted in five dedicated lemma calls in the implementation (List-
ing 2), covering early returns after table lookups, the depth = 0 base case, loop
maintenance and termination, and updates to the transposition table. This de-
composition proved essential for scaling the verification to realistic algorithm
variants.

4.3     Verification of NegamaxTTM
Our attempts to verify Marsland’s transposition table algorithm NegamaxTTM
was ultimately unsuccessful. During the Dafny proof, we encountered a specific
configuration for which the postcondition of is-negamax-tt-result could not be es-
tablished. A closer analysis of this unprovable configuration led us to the discov-
     10         W. Wesselink et al.


     Listing 2 Dafny verification of NegamaxTTW
1    class NegamaxAlgorithm
2    {
3      var T : TranspositionTable
4
5        method Negamax ( u : Node , alpha0 : bounded_int , beta0 : bounded_int , depth : nat )
6          returns ( result : bounded_int )
7          modifies this ‘ T
8          requires alpha0 < beta0
9          requires turn_based ()
10         requires is_valid_table ( T)
11         ensures is_negamax_tt_result ( result , u , alpha0 , beta0 , depth )
12         ensures is_valid_table ( T )
13       {
14         var alpha , beta := alpha0 , beta0 ;
15         if u in T . Keys
16         {
17           var t := T [ u ];
18           if t . depth > = depth && (( t . flag = = Lowerbound && t . value > = beta ) ||
19                ( t . flag = = Exact ) || ( t . flag = = Upperbound && t . value < = alpha ) )
20           {
21             TableLookupReturnLemma (u , alpha , beta , depth , t , T ) ;
22             return t . value ;
23           }
24         }
25         if depth = = 0 || | u . children | = = 0
26         {
27           DepthZeroReturnLemma (u , depth , alpha0 , beta0 ) ;
28           return color ( u ) * u . eval ;
29         }
30         var value : bounded_int := - INFINITY ;
31         for i := 0 to | u . children |
32           invariant is_valid_table ( T )
33           invariant 0 < = i < = | u . children |
34           invariant i = = 0 = = > value = = - INFINITY && alpha = = alpha0
35           invariant alpha0 < = alpha < beta0
36           invariant value < = alpha0 = = > alpha = = alpha0
37           invariant alpha0 < value < beta0 = = > value = = alpha
38           invariant i > 0 = = > exists u ’: Node :: is_expansion (u ’ , u , depth ) &&
39                             is_partial_negamax_ab_result ( value , u ’ , i , alpha0 , beta0 )
40           invariant i = = | u . children | = = >
41                       is_negamax_tt_result ( value , u , alpha0 , beta0 , depth )
42         {
43           ghost var old_alpha := alpha ;
44           ghost var old_value := value ;
45           var v := u . children [ i ];
46           var negamax_v := Negamax (v , - beta , - alpha , depth - 1) ;
47           value := max ( value , - negamax_v ) ;
48           alpha := max ( alpha , value ) ;
49           if alpha > = beta
50           {
51             LoopBreakLemma (u , v , i , depth , alpha0 , beta0 , old_alpha , old_value ,
52                                 alpha , value , negamax_v ) ;
53             break ;
54           }
55           LoopMaintenanceLemma (u , v , i , depth , alpha0 , beta0 , old_alpha , old_value ,
                   alpha , value , negamax_v ) ;
56         }
57         TableUpdateLemma ( value , u , alpha0 , beta0 , depth , T ) ;
58         if value < = alpha0           {T := T [ u := TableEntry_ ( depth , value , Upperbound ) ];}
59         else if alpha0 < value < beta0 { T := T [ u := TableEntry_ ( depth , value , Exact ) ];}
60         else if value > = beta0 {T := T [ u := TableEntry_ ( depth , value , Lowerbound ) ];}
61         return value ;
62       }
63   }
                                                  Formal Verification of Minimax Algorithms        11


                       0




           0                       0




   2               1                   0




                               0



                                                          0                           0

               0



                                                      0       0                   0       0
           0               0




                                                      0       2   1               0       2    1
           0               2               1




       3       4                                  3       4                   3       4



(a) Root call on u:                            (b) First call on v:       (c) Second call on v:
depth 6, window (0, 5),                        depth 4, window (0, 2),    depth 2, window (0, 5),
returns 2 (exact)                              returns 3 (lower bound)    reuses (b)’s result and re-
                                                                          turns 2 (exact)

Fig. 3: Counterexample to NegamaxTTM. Node v (with double border) is
searched twice. Call (b) stores a lower bound of 3 in the transposition table.
Call (c) reuses this result in a shallower search with a wider window, leading to
an unexpected return value. Dotted nodes are not visited during search.


ery of a concrete counterexample, demonstrating that NegamaxTTM violates
our witness-based correctness criterion. The problematic case arises when the
returned value x satisfies
                              α0 < x ≤ α < β0 ,
where α0 and β0 denote the original alpha-beta bounds of the call, and α is the
updated lower bound after a transposition table lookup (e.g., α0 = 0, x = 2,
α = 3, β0 = 5).
    The configuration identified through formal verification turned out to be
invaluable in our search for a counterexample. It characterizes a situation in
which a value returned from a transposition table lookup raises the lower bound α
beyond the eventual return value x, while still remaining below the original upper
bound β0 . This pattern suggests that a previously computed lower bound may
trigger premature pruning, thereby preventing the exploration of subtrees that
would otherwise influence the minimax value.
    In NegamaxTTM, such a situation can arise only when the lower bound α
is increased by a transposition table lookup that yields a lower bound computed
at a greater or equal search depth. Guided by this observation, we constructed a
concrete instance realizing this mechanism by considering the window (α, β) =
12       W. Wesselink et al.

(0, 5), together with the transposition table
                   T = {v 7→ (value = 3, depth = 4, flag = LB)},
followed by a search of the same node v at depth 2 that returns a value x = 2.
After substantial manual analysis, this led to the hand-crafted counterexample
shown in Figure 3(c).
    Applied to this example, NegamaxTTM indeed returns the value 2, as
shown in Equation 11(c). This outcome is problematic for two independent rea-
sons. First, it violates standard minimax intuition: the parent of the node with
value 2 is a minimizing node, and under optimal play at depth 2 it should instead
select the branch with value 1. Second, and more importantly for our formal de-
velopment, there exists no witness tree satisfying the criterion (9) that justifies
the return value 2.
    Indeed, there are only two expansions of ⌊u⌋2 that satisfy the is-expansion
predicate, namely ⌊u⌋2 itself and the full tree u. The corresponding negamax
alpha-beta results for these expansions are 1 and 4, respectively; the value 2
cannot be obtained from any admissible witness. Crucially, the node with value 1
is never visited during the search. This is a direct consequence of the lower-bound
value 3 stored in the transposition table, which shrinks the alpha–beta window to
(3, 5) during the table-lookup phase. When the node with value 2 is subsequently
evaluated, the loop’s break condition is triggered, and no further children are
explored.
    At first glance, this counterexample might appear unconvincing, since it as-
sumes a specific non-empty transposition table at the start of the search. To
show that this situation can arise in a complete execution, we therefore extend
the example to a run starting from an empty table, as shown in Figure 3(a).
The algorithm is invoked at the root node u with window (0, 5), depth 6, and an
initially empty transposition table. This call generates two recursive searches of
node v (indicated by a double border), and no table entries are removed during
the search.
    The resulting calls are summarized in Equation 11. In particular, call (b)
stores a lower bound of 3 for v at depth 4 in the table. This entry is then
reused in call (c), which searches v at depth 2 with a wider window. The reuse
of this lower bound again causes premature pruning and leads to the return of
the problematic value 2. Also in this extended execution, no witness exists that
justifies the returned result.


     (a) NegamaxTTM(u, α = 0, β = 5, depth = 6, T = ∅)        = 2 (exact)     (11)
     (b) NegamaxTTM(v, α = 0, β = 2, depth = 4, T )           =3    (lowerbound)
     (c) NegamaxTTM(v, α = 0, β = 5, depth = 2, T )           =2    (upperbound)
The root cause of this failure is the reuse of a lower bound computed under a
narrower alpha-beta window (0, 2) in a subsequent search with wider window
(0, 5). This reuse leads to pruning of a node that would otherwise yield a better
minimax value.
                                       Formal Verification of Minimax Algorithms                 13



                                   ↓ (0, 5)
                                     ↑ 2
 1 TL: α := 3
 2 NS: value := −∞
 10 NS: value := 0                        v, 0
 17 NS: value := 2
 18 TU: return 2
                            ↓(−5,−3)             ↓(−5,−3)
                               ↑ 0                 ↑ −2            11 NS: value := −∞
                                                                   13 NS: value := −2
 3 TL: β := −3                                                     14 NS: break (value ≥ −3)
 4 NS: value := −∞                 b, 0          e, 0              15 TU: T [e] := (−2, 1, LB)
 7 NS: value := 0                                                  16 TU: return −2
 8 NS: break (value ≥ −3)   ↓ (3, 5)      ↓ (3, 5)
 9 TU: return 0               ↑ 0           ↑ 2


                                   c, 0          f, 2       g, 1
 5 TL: α := 3
 6 NS: return 0 (depth 0)

                                                                   12 NS: return 2 (depth 0)

                            d, 3          h, 4

Fig. 4: Execution trace of NegamaxTTM on the minimal counterexample from
Figure 3(c), with transposition table {v 7→ (value = 3, depth = 4, flag = LB)}.
Nodes contain an identifier and an evaluation value. Rectangular blocks show
statements executed at each node, labeled by algorithmic phase (TL/NS/TU)
and global execution order. Edge labels show the alpha-beta interval passed
downward (↓) and the value returned upward (↑).


   The counterexample shows that NegamaxTTM violates our witness-based
correctness notion: no witness exists that justifies the returned value. Moreover,
the returned value exhibits behavior that is difficult to reconcile with standard
minimax semantics. In particular, a minimizing node selects a child with value 2
even though another child with value 1 lies within the search horizon and is never
explored. These observations do not imply that NegamaxTTM is incorrect as
a practical search algorithm. However, it remains an open question whether a
useful correctness criterion exists.


4.4   Execution of the Minimal Counterexample

To understand why NegamaxTTM violates our correctness criterion while
NegamaxTTW satisfies it, we examine their concrete executions on the min-
imal counterexample of Figure 3(c). Both algorithms are called with identical
inputs:
               NegamaxTT[W,M](v, α = 0, β = 5, depth = 2, T ),

where T = {v 7→ (value = 3, depth = 4, flag = LB)}.
14      W. Wesselink et al.

NegamaxTTM Figure 4 shows the recursive depth-first search of Nega-
maxTTM through nodes v, b, c, e, and f . For each node, a text block lists
the relevant statements executed during its search, prefixed with their global
execution order. The statements are labeled by phase: TL (Table Lookup), NS
(Negamax Search), and TU (Table Update). Edges are labeled with two pieces
of information:

 – ↓ (α, β): the alpha-beta window passed to the child, after the standard nega-
   tion and swapping of bounds (−β, −α),
 – ↑ value: the value returned by the child.

Dashed edges and nodes (e.g., d, g, h) are not visited during this search. The
key steps that lead to the problematic return value 2 are:

 1. At the root v, the table lookup increases α from 0 to 3 (step 1). This nar-
    rowing of the window is caused by the stored lower bound for v.
 2. When searching child b, the window becomes (−5, −3) after negation. Its
    child c returns its own value 0 (step 6), since it is searched at depth 0. The
    search of b propagates this value 0 (step 9) to the root v (step 10).
 3. Child e is searched with window (−5, −3). Its leaf child f returns 2, which
    becomes −2 after negation (step 13). Since −2 ≥ −3, a beta-cutoff occurs
    (step 14), skipping the better child g with value 1. The value −2 is stored in
    the TT (step 15) and propagated back to the root v (step 16). After negation
    (step 17) the final return value becomes 2.

The stored lower bound 3 for v thus causes a premature cutoff at e. Consequently,
the algorithm never visits the subtree that would reveal the better minimax value
1 available at depth 2. The return value 2 cannot be justified by any witness
expansion of ⌊v⌋2 , confirming the violation of our correctness criterion.


NegamaxTTW Figure 5 illustrates the execution of NegamaxTTW. The
table lookup at v also finds the stored lower bound 3, but the check t.value ≥ β
(i.e., 3 ≥ 5) fails, so the lookup does not cause an early return. Consequently, the
search proceeds with the original window (0, 5), explores all relevant children,
and returns the expected negamax value 1. The stored entry 3 is effectively
ignored because it does not guarantee a cutoff in the current, wider window.


Comparison The two traces highlight the semantic difference between the
table-lookup strategies. NegamaxTTM uses stored bounds to narrow the search
window, which can lead to incorrect pruning when a bound computed under a
narrow window is reused in a wider one. NegamaxTTW only accepts a stored
value if it immediately guarantees a cutoff; otherwise it discards the entry and
performs a full search. This more conservative policy preserves the existence of a
witness tree, explaining why NegamaxTTW satisfies our correctness criterion
while NegamaxTTM does not.
                                          Formal Verification of Minimax Algorithms                  15



                                      ↓ (0, 5)
                                        ↑ 1
 1 NS: value := −∞
 9 NS: value := 0
 10 NS: α := 0                               v, 0
 20 NS: value := 1
 21 NS: α := 1                                                         11 NS: value := −∞
                                ↓ (−5,0)             ↓ (−5,0)
 22 TU: T [v] := (1, 2, EX)                                            13 NS: value := −2
                                   ↑ 0                 ↑ −1
 23 TU: return 1                                                       14 NS: α := −2
                                                                       16 NS: value := −1
 2 NS: value := −∞                    b, 0          e, 0               17 NS: α := −1
 4 NS: value := 0                                                      18 TU: T [e] := (−1, 1, EX)
 5 NS: α := 0                                                          19 TU: return −1
                               ↓ (0, 5)      ↓ (0, 5)       ↓ (0, 2)
 6 NS: break (α = 0 ≥ β = 0)     ↑ 0           ↑ 2            ↑ 1
 7 TU: T [b] := (0, 1, LB)
 8 TU: return 0
                                      c, 0          f, 2        g, 1
 3 NS: return 0 (depth 0)                                              15 NS: return 1 (depth 0)


                                                                       12 NS: return 2 (depth 0)
                               d, 3          h, 4

Fig. 5: Execution trace of NegamaxTTW on the minimal counterexample from
Figure 3(c), with transposition table {v 7→ (value = 3, depth = 4, flag = LB)}.


4.5    Differences between NegamaxTTW and NegamaxTTM

The algorithms NegamaxTTW and NegamaxTTM in Algorithm 3 both con-
sist of three conceptual phases: a table lookup, a negamax search, and a table
update. While structurally similar, the two algorithms differ in each of these
phases:

 – Table Lookup: NegamaxTTM uses upper and lower bounds from the
   transposition table to narrow the alpha-beta window, while NegamaxTTW
   terminates the search immediately when a matching entry is found.
 – Negamax Search: NegamaxTTM follows Fishburn’s fail-soft negamax
   scheme [4], which differs in how intermediate bounds are propagated during
   recursion.
 – Table Update: NegamaxTTM uses the current value of α to classify
   search results, while NegamaxTTW uses the initial value of α for that. In
   addition, NegamaxTTM preserves existing table entries when their recorded
   search depth exceeds that of the newly computed result.

We analyzed the impact of each of these differences on correctness with respect to
our witness-based criterion. The verification attempt for NegamaxTTM shows
that the deviation in the Table Lookup phase is decisive: reusing bounds to shrink
the search window can lead to results for which no admissible witness expansion
exists, and therefore violates our correctness notion.
16     W. Wesselink et al.

    The remaining differences were studied in isolation by incorporating them
into NegamaxTTW and re-verifying the resulting variants in Dafny. The ad-
ditional depth condition in the Table Update phase does not affect correctness,
since our transposition table model constrains only the validity of stored entries,
not their presence or replacement policy.
    Similarly, adopting Fishburn’s fail-soft negamax variant in the Negamax
Search phase does not compromise correctness. Proving this required adapta-
tions to the loop maintenance and loop break lemmas, but no changes to the
underlying correctness argument.
    In contrast, classifying results against the current value of α rather than the
initial one turned out to be more subtle. Under this modification, the three cases
in the table-update are no longer mutually exclusive. Correctness could only be
re-established by imposing a different ordering on these cases, ensuring that the
correct flag (lower bound, exact or upper bound) is assigned to the result.


5    Results

Our first contribution is the introduction of a witness-based correctness crite-
rion for depth-limited game tree search with transposition tables. This notion
formalizes the intuitive requirement that the returned value must correspond to
the exact evaluation of some fully explored subtree (the witness).
    As a second contribution, we applied this correctness notion to two repre-
sentative algorithms. We successfully verified the NegamaxTTW algorithm in
Dafny, providing, to our knowledge, the first formal proof of correctness for a
depth-limited transposition-table-based negamax search with alpha-beta prun-
ing. In contrast, the algorithm by Marsland [7] (with best move tracking omitted)
was shown to violate the criterion, based on a concrete counterexample. Whether
this outcome reflects a shortcoming in Marsland’s algorithm or highlights the
need for a different correctness notion remains an open question.
    Beyond these case studies, we developed and verified over 15 variations of
minimax and negamax algorithms, ranging from basic recursive definitions to
depth-limited and alpha-beta optimized versions. All verification artifacts, in-
cluding Dafny proofs and Python implementations with randomized testing, are
available on GitHub [11]. The most complex case, NegamaxTTW, verifies in
approximately 4 seconds with Dafny 4.10.0.


6    Conclusions

This work illustrates the value of formal verification in reasoning about correct-
ness properties of game tree search algorithms, particularly when optimizations
such as transposition tables are employed.
   Our primary contribution is a general and intuitive witness-based correct-
ness criterion for depth-limited search using transposition tables, applicable both
                                   Formal Verification of Minimax Algorithms         17

with and without alpha-beta pruning. We demonstrate that the proposed crite-
rion can be used to verify a variant found on Wikipedia (which we call Nega-
maxTTW), whereas it does not hold for a closely related variant by Marsland [7]
(NegamaxTTM). This contrast highlights how subtle algorithmic differences
can invalidate seemingly plausible correctness arguments, underscoring the ne-
cessity of precise semantic models when verifying optimized search techniques.
More broadly, our work illustrates Dafny’s suitability for verifying recursive,
stateful algorithms with nontrivial invariants, as commonly found in AI search
for games.
    Several directions for future work emerge from this study. A natural next
step is to extend the witness-based framework to other search algorithms that
rely intrinsically on the persistence of transposition table state, such as SSS ∗
[10, 9] and MTD(f ) [9]. Another goal is to find a relaxed correctness notion for
NegamaxTTM, whose behavior is not characterized by our current witness-
based criterion. Recent advances in quantum program verification (e.g., [13])
further suggest a pathway toward extending formal, semantics-based correctness
reasoning to quantum variants of game tree search.


References
 1. Bird, R.S., Hughes, J.: The alpha-beta algorithm: An exercise in program trans-
    formation. Inf. Process. Lett. 24(1), 53–57 (1987). https://doi.org/10.1016/0020-
    0190(87)90198-0
 2. Breuker, D.: Memory versus Search in Games. Ph.d. thesis, Maastricht University,
    Maastricht (1998). https://doi.org/10.26481/dis.19981016db
 3. Fishburn, J.P.: An optimization of alpha-beta search. SIGART Newsl. 72, 29–31
    (1980). https://doi.org/10.1145/1056447.1056450
 4. Fishburn, J.P.: Another optimization of alpha-beta search. SIGART Newsl. 84,
    37–38 (1983). https://doi.org/10.1145/1056623.1056628
 5. Knuth, D.E., Moore, R.W.: An analysis of alpha-beta pruning. Artif. Intell. 6(4),
    293–326 (1975). https://doi.org/10.1016/0004-3702(75)90019-3
 6. Leino, R.: Dafny: An automatic program verifier for functional correctness. In: 16th
    International Conference, LPAR-16, Dakar, Senegal. pp. 348–370. Springer Berlin
    Heidelberg (April 2010). https://doi.org/10.1007/978-3-642-17511-4_20
 7. Marsland, T.A.: A review of game-tree pruning. ICCA Journal 9(1), 3–19 (1986).
    https://doi.org/10.3233/ICG-1986-9102
 8. Nipkow, T. (ed.): Functional Data Structures and Algorithms: A Proof Assistant
    Approach, vol. 67. Association for Computing Machinery, New York, NY, USA, 1
    edn. (2025)
 9. Plaat, A., Schaeffer, J., Pijls, W., de Bruin, A.: Best-first fixed-depth minimax
    algorithms. Artif. Intell. 87(1-2), 255–293 (1996). https://doi.org/10.1016/0004-
    3702(95)00126-3
10. Stockman, G.C.: A minimax algorithm better than alpha-beta? Artif. Intell. 12(2),
    179–196 (1979). https://doi.org/10.1016/0004-3702(79)90016-X
11. Wesselink, W.: Minimax verification. https://github.com/wiegerw/minimax
    (2025), accessed: 2026-01-25
12. Wikipedia contributors: Negamax — Wikipedia, the free encyclopedia.
    https://en.wikipedia.org/wiki/Negamax (2025), accessed: 2025-06-09
18     W. Wesselink et al.

13. Ying, M.: Floyd-Hoare logic for quantum programs. ACM Trans. Program. Lang.
    Syst. 33(6), 19:1–19:49 (2011). https://doi.org/10.1145/2049706.2049708
