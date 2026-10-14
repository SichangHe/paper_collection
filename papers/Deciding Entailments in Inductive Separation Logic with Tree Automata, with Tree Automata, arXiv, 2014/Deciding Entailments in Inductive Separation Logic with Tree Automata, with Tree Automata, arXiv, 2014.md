                                           Deciding Entailments in Inductive Separation Logic
                                                          with Tree Automata
                                                            Radu Iosif, Adam Rogalewicz, and Tomáš Vojnar
                                                           CNRS/Verimag, France and FIT BUT, Czech Republic
                                                         radu.iosif@imag.fr, {rogalew,vojnar}@fit.vutbr.cz
arXiv:1402.2127v2 [cs.LO] 11 Feb 2014




                                               Abstract. Separation Logic (SL) with inductive definitions is a natural formal-
                                               ism for specifying complex recursive data structures, used in compositional veri-
                                               fication of programs manipulating such structures. The key ingredient of any au-
                                               tomated verification procedure based on SL is the decidability of the entailment
                                               problem. In this work, we reduce the entailment problem for a non-trivial subset
                                               of SL describing trees (and beyond) to the language inclusion of tree automata
                                               (TA). Our reduction provides tight complexity bounds for the problem and shows
                                               that entailment in our fragment is EXPTIME-complete. For practical purposes,
                                               we leverage from recent advances in automata theory, such as inclusion checking
                                               for non-deterministic TA avoiding explicit determinization. We implemented our
                                               method and present promising preliminary experimental results.

                                        1 Introduction
                                        Separation Logic (SL) [17] is a logical framework for describing recursive mutable
                                        data structures. The attractiveness of SL as a specification formalism comes from the
                                        possibility of writing higher-order inductive definitions that are natural for describ-
                                        ing the most common recursive data structures, such as singly- or doubly-linked lists
                                        (SLLs/DLLs), trees, hash maps (lists of lists), and more complex variations thereof,
                                        such as nested and overlaid structures (e.g. lists with head and tail pointers, skip-lists,
                                        trees with linked leaves, etc.). In addition to being an appealing specification tool, SL
                                        is particularly suited for compositional reasoning about programs. Indeed, the principle
                                        of local reasoning allows one to verify different elements (functions, threads) of a pro-
                                        gram, operating on disjoint parts of the memory, and to combine the results a-posteriori,
                                        into succinct verification conditions.
                                            However, the expressive power of SL comes at the price of undecidability [6]. To
                                        avoid this problem, most SL dialects used by various tools (e.g. S PACE I NVADER [3],
                                        P REDATOR [10], or I NFER [7]) use hard-coded predicates, describing SLLs and DLLs,
                                        for which entailments are, in general, tractable [9]. For graph structures of bounded tree
                                        width, a general decidability result was presented in [13]. Entailment in this fragment
                                        is EXPTIME-hard as proved in [1].
                                            In this paper, we present a novel decision procedure for a restriction of the decidable
                                        fragment of [13] that describes recursive structures in which all edges are local with
                                        respect to a spanning tree. Examples of such structures include SLLs, DLLs, trees and
                                        trees with parent pointers, etc. For structures outside of this class (e.g. skip-lists or trees
                                        with linked leaves), our procedure is sound (the answer is positive if the entailment
                                        holds), but not complete (the answer might be negative and the entailment could still
                                        hold). In terms of program verification, such a lack of completeness in the entailment
                                        prover can cause non-termination of the fixpoint, but will not provide unsound results.
                                            The method described in the paper belongs to the class of automata-theoretic deci-
                                        sion techniques: we translate an entailment problem ϕ |= ψ into a language inclusion
problem L (Aϕ ) ⊆ L (Aψ ) for tree automata (TA) Aϕ and Aψ that (roughly speaking)
encode the sets of models of ϕ and ψ, respectively. Yet, a naı̈ve translation of the in-
ductive definitions of SL into TA encounters a polymorphic representation problem:
the same structure can be defined in several different ways, and TA simply mirroring
the definition will not report the entailment. For example, DLLs with selectors next
and prev for the next and previous nodes, respectively, can be described by a for-
ward unfolding of the inductive definition DLL(head, prev,tail, next) ≡ ∃x. head 7→
(x, prev) ∗ DLL(x, head,tail, next) as well as by a backward unfolding of the definition
DLLrev (head, prev,tail, next) ≡ ∃x. tail 7→ (next, x) ∗ DLLrev (head, prev, x,tail). Also,
one can define a DLL starting with a node in the middle and unfolding backward to the
left of this node and forward to the right: DLLmid (head, prev,tail, next) ≡ ∃x, y, z . x 7→
(y, z) ∗ DLL(y, x,tail, next) ∗ DLLrev (head, prev, z, x). The entailments DLL(a, b, c, d) |=
DLLrev (a, b, c, d) and DLLmid (a, b, c, d) |= DLL(a, b, c, d) hold, but a naı̈ve structural
translation to TA might not detect this fact. To bridge this gap, we define a closure
operation on TA, called canonical rotation, which automatically adds all possible rep-
resentations of a given inductive definition, encoded as a tree automaton.
     Our reduction from SL to TA provides tight complexity bounds showing that entail-
ment in our fragment is EXPTIME-complete. Moreover, from a practical point view, we
implemented our method using the VATA [14] tree automata library, which leverages
from recent advances in non-deterministic language inclusion for TA [5], and obtained
quite encouraging experimental results.
Related work. Given the large body of literature on decidable logics for describing mu-
table data structures, we need to restrict this section to the related work that focuses on
SL [17]. The first (proof-theoretic) decidability result for SL on a restricted fragment
defining only SLLs was reported in [4], which describe a co-NP algorithm. The full
basic SL without recursive definitions, but with the magic wand operator was found to
be undecidable when interpreted in any memory model [6]. A PTIME entailment pro-
cedure for SL with list predicates is given in [9]. Their method was extended to reason
about nested and overlaid lists in [11]. More recently, entailments in an important SL
fragment with hardcoded SLL/DLL predicates were reduced to Satisfiability Modulo
Theories (SMT) problems, leveraging from recent advances in SMT technology [16].
     Closer to our work on SL with user-provided inductive definitions is the fragment
used in the tool S LEEK, which implements a semi-algorithmic entailment check, based
on unfoldings and unifications [15]. Our previous work [13] gives a general decidabil-
ity result for SL with inductive definitions interpreted over graph-like structures, under
several necessary restrictions. The work [1] provides a rather complete picture of com-
plexity for the entailment in various SL fragments with inductive definitions, including
EXPTIME-hardness of the decidable fragment of [13], but provides no upper bound.
The EXPTIME-completness result in this paper provides an upper bound for the frag-
ment of local definitions, and strengthens the EXPTIME-hard lower bound as well.

2 Definitions
The set of natural numbers is denoted by N. For a finite set S, we denote by ||S|| its car-
dinality. If x = hx1 , . . . , xn i and y = hy1 , . . . , ym i are tuples, x · y = hx1 , . . . , xn , y1 , . . . , ym i
denotes their concatenation, and (x)i = xi denotes the i-th element of x. If x is an ele-
ment, we denote by x¬x the result of projecting out all occurrences of x from x, and if S
                                                          2
is a set, we denote by x¬S the result of projecting out all occurrences of some element
s ∈ S from x. The intersection x ∩ S denotes the tuple in which only elements of S are
maintained. The union (intersection) x ∪y (x ∩y) denotes the set of elements from either
(both) x and y. For two tuples of variables x = hx1 , . . . , xk i and y = hy1 , . . . , yk i, of equal
                            V
length,
     Vk
          we write x = y for ki=1 xi = yi . Moreover, for a single variable z, we write x = z
for i=1 xi = z.
     For a partial function f : A ⇀ B, and ⊥ ∈    / B, we denote f (x) = ⊥ the fact that
 f is undefined at some point x ∈ A. The domain of f is denoted dom( f ) = {x ∈ A |
 f (x) 6= ⊥}, and the image of f is denoted as img( f ) = {y ∈ B | ∃x ∈ A . f (x) = y}. By
 f : A ⇀ f in B, we denote any partial function whose domain is finite. Given two partial
functions f , g defined on disjoint domains, we denote by f ⊕ g their union.

2.1 Stores, Heaps, and States
We consider Var = {x, y, z, . . .} to be a countably infinite set of variables and nil ∈
Var be a designated variable. We assume a total lexicographical ordering on the set of
variables Var, and for any set S ⊆ Var, we denote by minlex(S) the unique minimal
element with respect to this ordering. Let Loc be a countably infinite set of locations,
null ∈ Loc be a designated location, and Sel = {1, . . . , S }, for some given S > 0, be a
finite set of natural numbers, called selectors in the following.
Definition 1. A state is a pair hs, hi where s : Var ⇀ Loc is a partial function mapping
pointer variables into locations such that s(nil) = null, and h : Loc ⇀ f in Sel ⇀ f in Loc
is a finite partial function such that (i) null 6∈ dom(h) and (ii) for all ℓ ∈ dom(h) there
exists k ∈ Sel such that (h(ℓ))(k) 6= ⊥.
      Given a state S = hs, hi, s is called the store and h the heap. For any k ∈ Sel, we write
  k                                                   k
ℓ−→S ℓ′ for (h(ℓ))(σ) = ℓ′ . We call a triple ℓ −
                                                →S ℓ′ an edge ofSS. Sometimes we omit the
subscript when it is obvious from the context. Let Img(h) = ℓ∈Loc img(h(ℓ)) be the set
of locations which are destinations of some edge in h. A location ℓ ∈ Loc is said to be
allocated in hs, hi if ℓ ∈ dom(h) (i.e. it is the source of an edge), and dangling in hs, hi
if ℓ ∈ [img(s) ∪ Img(h)] \ dom(h), i.e. it is referenced by a store variable, or reachable
from an allocated location in the heap, but it is not allocated in the heap itself. The
set loc(S) = img(s) ∪ dom(h) ∪ Img(h) is the set of all locations either allocated or
referenced in the state S.
     For any two states S1 = hs1 , h1 i and S2 = hs2 , h2 i, such that (i) s1 and s2 agree on
the evaluation of common variables (∀x ∈ dom(s1 ) ∩ dom(s2 ) . s1 (x) = s2 (x)), and
(ii) h1 and h2 have disjoint domains (dom(h1 ) ∩ dom(h2 ) = 0),   / we denote by S1 ⊎ S2 =
hs1 ∪ s2 , h1 ⊕ h2 i the disjoint union of S1 and S2 . The disjoint union is undefined if one
of the above conditions does not hold.
     For a state S = hs, hi and a location ℓ ∈ dom(h), the neighbourhood of ℓ in S is a
state denoted as Shℓi = hsℓ , hℓ i, where:
                          k
  – hℓ = {hℓ, λk . if ℓ −
                        →S ℓ′ then ℓ′ else ⊥i}
  – sℓ (x) = if s(x) ∈ dom(hℓ ) ∪ img(hℓ ) then s(x) else ⊥
Intuitively, the neighbourhood of an allocated location ℓ is the state in which only ℓ is
                                                                  k
allocated and all other locations ℓ′ for which there is an edge ℓ −
                                                                  →S ℓ′ are dangling.

                                                  3
2.2 Trees
Let Σ be a countable alphabet, and N∗ be the set of sequences of natural numbers. Let
ε ∈ N∗ denote the empty sequence, and p.q denote the concatenation of two sequences
p, q ∈ N∗ . We say that p is a prefix of q if q = p.q′ , for some q′ ∈ N∗ .
     The total order on N extends to a total lexicographical order on N∗ , and for any set
S ⊆ N∗ , we denote by minlex(S)1 the lexicographically minimal element of S.
     A tree t over Σ is a finite partial function t : N∗ ⇀ f in Σ such that dom(t) is a finite
prefix-closed subset of N∗ and, for each p ∈ dom(t) and i ∈ N, we have t(p.i) 6= ⊥ only
if t(p. j) 6= ⊥, for all 0 ≤ j < i. The sequences p ∈ dom(t) are called positions in the
following. Given two positions p, q ∈ dom(t), we say that q is the i-th successor (child)
of p if q = p.i, for i ∈ N.
     We denote by D (t) = {−1, 0, . . ., N} the direction alphabet of t, where N = max{i ∈
N | ∃p ∈ N∗ . p.i ∈ dom(t)}, and we let D+ (t) = D (t) \ {−1}. By convention, we have
(p.i).(−1) = p, for all p ∈ N∗ and i ∈ D+ (t). Given a tree t and a position p ∈ dom(t),
we define the arity of the position p as #t (p) = max{d ∈ D+ (t) | p.d ∈ dom(t)} + 1,
and the subtree of t rooted at p as t| p (q) = t(p.q), for all q ∈ N∗ .
     A path in t, from p1 to pk , is a sequence p1 , p2 , . . . , pk ∈ dom(t) of pairwise distinct
positions, such that, for all 1 ≤ i < k, there exist di ∈ D (t) such that pi+1 = pi .di . Notice
that a path in the tree can also link sibling nodes, not just ancestors to their descendants
or vice versa. However, a path may not visit the same tree position twice.
     Given a position p ∈ dom(t), we denote by t| p the subtree of t starting at position p,
i.e. t|p (q) = t(p.q), for all q ∈ N∗ .
Definition 2. Given two trees t1 ,t2 : N∗ ⇀ f in Σ, we say that t2 is a rotation of t1 denoted
by t1 ∼r t2 if and only if r : dom(t1 ) → dom(t2 ) is a bijective function such that: ∀p ∈
dom(t1 )∀d ∈ D+ (t1 ) : p.d ∈ dom(t1 ) ⇒ ∃e ∈ D (t2 ) . r(p.d) = r(p).e. We write t1 ∼ t2
if there exists a function r : dom(t1 ) → dom(t2 ) such that t1 ∼r t2 .
    An example of a rotation r of a tree t1                                    r
                                                                 t1                        t2
to a tree t2 such that r(ε) = 2, r(0) = ε,                   ε                         ε
r(1) = 20, r(00) = 0, and r(01) = 1 is                                             0
                                                         0                 1                    1   2
shown in Fig. 1. Note that, e.g., for p =
ε ∈ dom(t1 ) and d = 0 ∈ D+ (t1 ) where             00
                                                                      01
                                                                                                        20
p.d = ε.0 ∈ dom(t1 ), we get e = −1 ∈
D (t2 ) and r(ε.0) = 2.(−1) = ε.                         Fig. 1. An example of a rotation.

Proposition 1. The relation ∼ is an equivalence relation.
Proof. The relation ∼ is clearly reflexive as one can choose r as the identity function.
To prove that ∼ is transitive, let t1 ,t2 ,t3 : N∗ ⇀ f in Σ be trees such that t1 ∼r1 t2 and
t2 ∼r2 t3 , and let r1 : dom(t1 ) → dom(t2 ) and r2 : dom(t2 ) → dom(t3 ) be the bijective
functions from Def. 2, respectively. Then, for all p ∈ dom(t1 ) and d ∈ D+ (t1 ) such that
p.d ∈ dom(t1 ), there exists e1 ∈ D (t2 ) such that r1 (p.d) = r1 (p).e1 . We distinguish two
cases:
 1. If e1 ∈ D+ (t2 ), then there exists e2 ∈ D (t3 ) such that (r2 ◦ r1 )(p.d) = r2 (r1 (p).e1 ) =
    (r2 ◦ r1 )(p).e2 .
 1 The distinction with the lexicographical order on Var is clear from the type of elements in S.


                                                4
 2. Otherwise, if e1 = −1, then r1 (p) = r1 (p.d).e′1 , for some e′1 ∈ D+ (t2 ). Then there
    exists e2 ∈ D (t3 ) such that (r2 ◦ r1 )(p) = r2 (r1 (p.d).e′1 ) = (r2 ◦ r1 )(p.d).e2 , and
    consequently, (r2 ◦ r1 )(p.d) = (r2 ◦ r1 )(p).(−1).
    To show that ∼ is symmetric, let t1 ∼r t2 be two trees, and let p ∈ dom(t2 ) and
d ∈ D+ (t2 ) such that p.d ∈ dom(t2 ). We prove that there exists e ∈ D (t1 ) such that
r−1 (p.d) = r−1 (p).e, where r is the bijective function from Def. 2. By contradiction,
suppose that there is no such direction, and since r−1 (p), r−1 (p.d) ∈ dom(t1 ), there
exists a path r−1 (p) = p1 , . . . , pi , . . . , pk = r−1 (p.d) of length k > 2 in t1 such that:
 – p j+1 = p j .(−1), for all 1 ≤ j < i,
 – p j+1 = p j .d j , for all i ≤ j < k and di , . . . , dk−1 ∈ D+ (t1 )
where p1 , . . . , pk are distinct positions in dom(t1 ). Then r(p1 ), . . . , r(pk ) are distinct
positions in dom(t2 ) such that:
 – r(p j ) = r(p j+1 ).e j , for all 1 ≤ j < i and some e j ∈ D (t2 ),
 – r(p j+1 ) = r(p j ).e j , for all i ≤ j < k and some e j ∈ D (t2 ).
So there exists a path p = r(p1 ), . . . , r(pk ) = p.d of length k > 2 in t2 , which contradicts
with the fact that t2 is a tree.                                                               ⊓
                                                                                               ⊔

    A rotation function r between two trees t ∼r u is said to revert two positions p, q ∈
dom(t), if q is a prefix of p and r(p) is a prefix of r(q). We show next that the only
reversions in dom(t) due to r appear on the (unique) path from the root ε to r−1 (ε).

Lemma 1. Let t, u : N∗ ⇀ f in Σ be two trees, r : dom(t) → dom(u) be a bijective function
such that t ∼r u, and p ∈ dom(t) be a position such that r(p) = ε is the root of u. Then,
for all q ∈ dom(t) and all 0 ≤ d < #t (q), r(q.d) = r(q).(−1) iff q.d is a prefix of p.

Proof. “⇒” Let q ∈ dom(t) be an arbitrary position such that r(q.d) = r(q).(−1), for
some 0 ≤ d < #t (q). Suppose, by contradiction, that q.d is not a prefix of p. There are
two cases:
 1. p is a strict prefix of q.d, i.e. there exists a sequence p = p0 , . . . , pk = q, for some
    k > 0, such that, for all 0 ≤ i < k, there exists 0 ≤ ji < #t (pi ) such that pi+1 = pi . ji .
    Then, there exists ℓ ∈ D (u) such that r(q) = r(pk−1 . jk−1 ) = r(pk−1 ).ℓ. If ℓ ≥ 0,
    we have r(pk−1 ) = r(q).(−1) = r(q.d) = r(pk−1 . jk−1 .d). Since both jk−1 , d ≥ 0,
    pk−1 and pk−1 . jk−1 .d are distinct nodes from dom(t), and we reach a contradiction
    with the fact that r is bijective. Hence, ℓ = −1 is the only possibility. Applying the
    same argument inductively on p0 , . . . , pk , we find that r(p) is either equal or is a
    descendant of r(q), which contradicts with the fact that r(p) = ε is the root of u.
 2. p is not a prefix of q.d, and there exists a common prefix p0 of both p and q.d.
    Let p0 be the maximal such prefix. Since p0 is a prefix of q.d, there exists a se-
    quence p0 , . . . , pk = q, for some k > 0, such that, for all 0 ≤ i < k there exists
    0 ≤ ji < #t (pi ) such that pi+1 = pi . ji . By the argument of the previous case, we
    have that r(q) = r(pk ), r(pk−1 ), . . . , r(p0 ) is a strictly descending path in u, i.e.
    r(pi ) is a child of r(pi+1 ), for all 0 ≤ i < k. Since p0 is a prefix of p, there ex-
    ists another non-trivial sequence p0 = p′0 , . . . , p′m = p, for some m > 0, such that,

                                                  5
    for all 0 ≤ i < m there exists 0 ≤ ji′ < #t (p′i ) and p′i+1 = p′i . ji′ . Moreover, since
                                                                                               /
    p0 is the maximal prefix of p and q.d, we have {p1 , . . . , pk } ∩ {p′1 , . . . , p′m } = 0.
    Then r(p′1 ) = r(p0 . j0′ ) = r(p0 ).ℓ, for some ℓ ∈ D (u). If ℓ = −1, then necessar-
    ily r(p′1 ) = r(pk−1 ), which contradicts with the fact that r is a bijection, since
    p′1 6= pk−1 . Then the only possibility is ℓ ≥ 0. By applying the same argument
    inductively on p′0 , . . . , p′m = p, we obtain that r(p) is a strict descendant of r(p0 ),
    which contradicts with r(p) = ε being the root of u.
Since both cases above lead to contradictions, the only possibility is that q.d is a prefix
of p.
“⇐” If q.d is a prefix of p, there exists a non-trivial sequence q = q0 , q.d = q1 , . . . , qk =
p, for some k > 0, such that, for all 0 ≤ i < k, there exists 0 ≤ ji < #t (qi ) such that qi+1 =
qi . ji . Then, ε = r(p) = r(qk ) = r(qk−1 . jk−1 ) = r(qk−1 ).(−1). Reasoning inductively, we
obtain that, for all 0 < i ≤ k, r(qi ) = r(qi−1 ).(−1), hence r(q.d) = r(q1 ) = r(q0 ).(−1) =
r(q).(−1).                                                                                      ⊓
                                                                                                ⊔

    A rotation function r between two trees t ∼r u is said to revert two positions p, q ∈
dom(t), if q is a prefix of p and r(p) is a prefix of r(q). One can see that the only
reversions in dom(t) due to r appear on the (unique) path from the root ε to r−1 (ε).

Definition 3. Given a state S = hs, hi, a spanning tree of S is a bijective tree t : N∗ →
                                                                                       k
dom(h) such that ∀p ∈ dom(t)∀d ∈ D+ (t) . p.d ∈ dom(t) ⇒ ∃k ∈ Sel . t(p) −
                                                                         →S t(p.d).
             k
An edge ℓ −→S ℓ′ is said to be local with respect to a spanning tree t iff there exist
p ∈ dom(t) and d ∈ D (t) ∪ {ε} such that t(p) = ℓ and t(p.d) = ℓ′ . Moreover, t is a local
spanning tree of S if t is a spanning tree of S, and S has only local edges wrt. t.
                                                                            p
    An example of a doubly-linked list and two of its            hd          prev

spanning trees is shown in Fig. 2. Note that both the
                                                                 next       prev
next and prev edges are local in both cases (they get
mapped either to the 0 or −1 direction) and so both of           next       prev
the spanning trees are local.
    Notice that a spanning tree covers exactly the set of        next       prev

allocated locations in a state. Moreover, if a state S has a
spanning tree t, then every location ℓ ∈ loc(S), not nec-        next       prev

essarily allocated, is reachable from t(ε) by a chain of                    next
                                                                 tl
edges. In other words, the state does not contain garbage               n


nodes.                                                                  Fig. 2. Spanning trees.

Lemma 2. Let S = hs, hi be a state and t its spanning tree. If all edges of S are local
with respect to t, then for each spanning tree t ′ of S we have t ∼t ′−1 ◦t t ′ , and, moreover,
all edges of S are local with respect to t ′ as well.

Proof. Let p ∈ dom(t) be an arbitrary position and d ∈ D+ (t) be an arbitrary non-
negative direction such that p.d ∈ dom(t). If t is a spanning tree, then t is bijective,
                                                    s
                                                   → t(p.d) is an edge in S. Since t ′ is a
and there exists a selector s ∈ Sel such that t(p) −
spanning tree, it is also bijective, hence there exist p′ , p′′ ∈ dom(t ′ ) such that t ′ (p′ ) =
t(p) and t ′ (p′′ ) = t(p.d).

                                               6
    By contradiction, suppose that p′′ 6= p′ .e for all e ∈ D (t ′ ). Since p′ , p′′ ∈ dom(t ′ ),
there exists a path p′ = p1 , . . . , pk such that k > 2, and, for all 1 ≤ i < k, we have
pi+1 = pi .ei , for some e1 , . . . , ek−1 ∈ D (t ′ ). Because t ′ is a spanning tree of S, there
exist selectors s1 , . . . , sk−1 ∈ Sel such that one of the following holds, for all 1 ≤ i < k:
              s
  – t ′ (pi ) −
              →i
                  t ′ (pi+1 ) or
                 s
  – t ′ (pi+1 ) −→ i
                       t ′ (pi ).
Since all the above edges of S are local wrt. t, there exists a path p = (t −1 ◦ t ′ )(p1 ), . . . ,
(t −1 ◦ t ′ )(pk ) = p.d of pairwise distinct positions in t, for k > 2, which contradicts with
the fact that t is a tree. In conclusion, for all p ∈ dom(t) and d ∈ D+ (t), such that
p.d ∈ dom(t) there exists e ∈ D (t ′ ) such that (t ′−1 ◦ t)(p.d) = (t ′−1 ◦ t)(p).e, and since
t ′−1 ◦ t is a bijective mapping, we have t ∼t ′−1 ◦t t ′ .
                                                                                            s
     Finally, we are left with proving that all edges are local with respect to t ′ . Let ℓ −
                                                                                            → ℓ′
be an arbitrary edge of S, for some s ∈ Sel. The edge is local with respect to t, thus there
exists p ∈ dom(t) and d ∈ D (t) ∪ {ε} such that t(p) = ℓ and t(p.d) = ℓ′ . We distinguish
three cases:
 1. If d = ε, then p = p.d, and trivially ℓ = t ′ ((t ′−1 ◦ t)(p)) = t ′ ((t ′−1 ◦ t)(p.d)) =
    t ′ ((t ′−1 ◦ t)(p).d) = ℓ′ .
 2. Otherwise, if d ∈ D+ (t), taking into account that t ∼t ′−1 ◦t t ′ , by the first part of this
    lemma, we have (t ′−1 ◦ t)(p.d) = (t ′−1 ◦ t)(p).e, for some e ∈ D (t ′ ). But t ′ ((t ′−1 ◦
                                                                          s
    t)(p)) = t(p) = ℓ and t ′ ((t ′−1 ◦ t)(p.d)) = t(p.d) = ℓ′ , so ℓ −  → ℓ′ is local wrt. t ′ .
 3. Otherwise, if d = −1, there exists q ∈ dom(t) and d ′ ∈ D+ (t) such that p = q.d ′ .
    Since t ∼t ′−1 ◦t t ′ , by the first part of this lemma, we have (t ′−1 ◦ t)(q.d ′ ) = (t ′−1 ◦
    t)(q).e, for some e ∈ D (t ′ ). But t ′ (t ′−1 ◦ t)(q.d ′ ) = t(p) = ℓ and t ′ ((t ′−1 ◦ t)(q)) =
                                   s
    t(q) = t(p.d) = ℓ′ , so ℓ −   → ℓ′ is local with respect to t ′ .
                                                                                                    ⊓
                                                                                                    ⊔

    As a consequence, if all edges of a state are local with respect to some spanning
tree, they are also local with respect to any other spanning tree, hence we will simply
say that they are local. A state is said to be local if it has only local edges.

2.3 Separation Logic
The syntax of basic formulae of Separation Logic (SL) is given below:
                     α ∈ Var \ {nil}; x ∈ Var;
                     Π ::= α = x | Π1 ∧ Π2
                     Σ ::= emp | α 7→ (x1 , . . . , xn ) | Σ1 ∗ Σ2 , for some n > 0
                     ϕ ::= Σ ∧ Π | ∃x . ϕ1
                              V
A formula of the form ni=1 αi = xi defined by the Π nonterminal in the syntax above is
said to be pure. A formula of the form ⋆ki=1 αi 7→ (xi,1 , . . . , xi,n ) defined by the Σ nonter-
minal in the syntax above is said to be spatial. The atomic proposition emp denotes the
empty spatial conjunction. A variable x is said to be free in ϕ if it does not occur under
the scope of any existential quantifier. We denote by FV (ϕ) the set of free variables,
and by AP(ϕ) the set of atomic propositions of ϕ.

                                                   7
    In the following, we shall use two equality relations. The syntactic equality, denoted
α ≡ β, means that α and β are the same syntactic object (formula, variable, tuples of
variables, etc.). On the other hand, by writing x =Π y, for two variables x, y ∈ Var and a
pure formula Π, we mean that the equality of the values of x and y is implied by Π.
    A substitution is an injective partial function σ : Var ⇀ f in Var. Given a basic for-
mula ϕ and a substitution σ, we denote by ϕ[σ] the result of simultaneously replacing
each variable (not necessarily free) x that occurs in ϕ, by σ(x). For instance, if σ(x) = y,
σ(y) = z and σ(z) = t, then (∃x, y . x 7→ (y, z) ∧ z = x)[σ] ≡ ∃y, z . y 7→ (z,t) ∧ t = y.
    The semantics of a basic formula ϕ is given by the relation S |= ϕ, where S = hs, hi
is a state such that FV (ϕ) ⊆ dom(s), and ϕ is a basic SL formula. The definition of |=
is by induction on the structure of ϕ:
          S |= emp                     ⇐⇒ dom(h) = 0/
          S |= α 7→ (x1 , . . . , xn ) ⇐⇒ s = {(α, ℓ0 ), (x1 , ℓ1 ), . . . , (xn , ℓn )} and
                                          h = {hℓ0 , λi . if 1 ≤ i ≤ n then ℓi else ⊥i}
                                           for some ℓ0 , ℓ1 , . . . , ℓn ∈ Loc
          S |= ϕ1 ∗ ϕ2                 ⇐⇒ S1 |= ϕ1 and S2 |= ϕ2 where S1 ⊎ S2 = S
          S |= ∃x . ϕ                  ⇐⇒ hs[x ← ℓ], hi |= ϕ for some ℓ ∈ Loc
    The semantics of = and ∧ is classical in first order logic. Note that we adopt here the
strict semantics, in which a points-to relation α 7→ (x1 , . . . , xn ) holds in a state consisting
                                                                                 k
of a single cell pointed to by α, with exactly n outgoing edges s(α) −           →S s(xk ), 1 ≤ k ≤ n,
towards either the single allocated location (if s(xk ) = s(α)), or dangling locations (if
s(xk ) 6= s(α)). The empty heap is specified by emp.
    A variable x ∈ FV (Σ) is said to be allocated in a basic spatial formula Σ if it occurs
on the right hand side of a points-to atomic proposition x 7→ (y0 , . . . , yk−1 ) of Σ. If Σ is
satisfiable, then clearly each free variable x ∈ FV (Σ) is allocated at most once. For a
basic quantifier-free SL formula ϕ ≡ Σ ∧ Π and two variables x, y ∈ FV (ϕ), we say that
y is ϕ-reachable from x in iff there exists a sequence x =Π α0 , . . . , αm =Π y, for some
m ≥ 0, such that, for each 0 ≤ i < m, αi 7→ (βi,1 , . . . , βi,pi ) is a points-to proposition in
Σ, and βi,s =Π αi+1 , for some 1 ≤ s ≤ pi . A variable x ∈ FV (Σ) is said to be a root of Σ
if every variable y ∈ FV (Σ) is reachable from x.
Remark. Notice that there is no explicit disequality between variables in the basic frag-
ment of SL. This is in part justified by the fact that disequality can be partially defined
using the following implication: α 7→ (x1 , . . . , xn ) ∗ β 7→ (y1 , . . . , ym ) ⇒ α 6= β. This im-
plication enforces disequality only between allocated variables. However, in practice,
most SL specifications do not impose disequality constraints on dangling variables.

2.4 Inductive Definitions
A system of inductive definitions2 (inductive system) P is a set of rules of the form:
                    P1 (x1,1 , . . . , x1,n1 ) ≡ |mj=1
                                                     1
                                                        R1, j (x1,1 , . . . , x1,n1 )
                                                ...                                    (1)
                                                    mk
                     Pk (xk,1 , . . . , xk,nk ) ≡ | j=1 Rk, j (xk,1 , . . . , xk,nk )
where {P1, . . . , Pk } is a set of predicates, xi,1 , . . . , xi,ni are called formal parameters, and
the formulae Ri, j are called the rules of Pi . Concretely, each rule is of the form:
                        Ri, j (x) ≡ ∃z . Σ ∗ Pi1 (y1 ) ∗ . . . ∗ Pim (ym ) ∧ Π
 2 The name inductive suggests that every structure described by the system is finite.

                                                  8
              / and all of the following hold:
where x ∩ z = 0,
                  de f
 1. head(Ri, j ) ≡ Σ is a non-empty spatial formula (i.e. Σ 6≡ emp), and FV (Σ) ⊆ x ∪ z,
               de f
 2. tail(Ri, j ) ≡ hPi1 (y1 ), . . . , Pim (ym )i is an ordered sequence of predicate occurrences,
    where y1 ∪ . . . ∪ ym ⊆ x ∪ z,
 3. Π is a pure formula, and FV (Π) ⊆ z ∪ x. In the following, we restrict the pure part
    of each rule such that, for all formal parameters β ∈ x, we allow only equalities of
    the form α =Π β, where α is allocated in Σ. This restriction is of technical nature
    (see Section 4.1). It is possible to lift it, but only at the expense of an exponential
    blowup in the size of the resulting tree automaton.
 4. For all 1 ≤ r, s ≤ m, if xi,k ∈ yr , xi,l ∈ ys , and xi,k =Π xi,l , for some 1 ≤ k, l ≤ ni , then
    r = s. In other words, a formal parameter of a rule cannot be passed to two or more
    subsequent occurrences of predicates in that rule. This technical restriction can be
    lifted at the cost of introducing expensive tests for double allocation as was done
    in the translation of the inductive definitions to Monadic Second-Order Logic on
    graphs, reported in [13].

The size of a rule R is denoted by |R| and is defined inductively as follows:
                |α = x| = 1        |emp| = 1       |α 7→ (x1 , . . . , xn )| = n + 1
            |ϕ • ψ| = |ϕ| + |ψ| |∃x . ϕ| = |ϕ| + 1     |P(x1 , . . . , xn )| = n

where α ∈ Var \ {nil}, x, x1 , . . . , xn ∈ Var, and • ∈ {∗, ∧}. The size of an inductive
system P = {Pi ≡ |mj=1
                    i
                       Ri, j }ni=1 is defined as |P | = ∑ni=1 ∑mj=1
                                                                 i
                                                                    |Ri, j |.

Example 1. To illustrate the use inductive definitions (with the above restrictions), we
first show how to define a predicate DLL(hd, p,tl, n) describing doubly-linked lists of
length at least one. As depicted on the left of Fig. 2, the formal parameter hd points to
the first allocated node of such a list, p to the node pointed by the prev selector of hd, tl
to the last node of the list (possibly equal to hd), and n to the node pointed by the next
selector from tl. This predicate can be defined as follows:
     DLL(hd, p,tl, n) ≡ hd 7→ (n, p) ∧ hd = tl | ∃x. hd 7→ (x, p) ∗ DLL(x, hd,tl, n)

                                                        root
                                                                        n
                                                                l       r
                                                            n                               n
                             ll
                                            l       r                           l       r
                                                n                   n               n               n   lr
                                  l     r               l       r       l   r               l   r
                                      Fig. 3. A tree with linked leaves.




Example 2. Another example is the predicate TLL(root, ll, lr) describing binary trees
with linked leaves, whose root is pointed by the root formal parameter, the left-most
leaf is pointed to by ll, and the right-most leaf points to lr (cf. Fig. 3):
        TLL(root, ll, lr) ≡ root 7→ (nil, nil, lr) ∧ root = ll
                            | ∃x, y, z. root 7→ (x, y, nil) ∗ TLL(x, ll, z) ∗ TLL(y, z, lr)
                                               9
Remark. The first restriction above (head(Ri, j ) 6≡ emp) currently does not allow defin-
ing data structures of zero size (such as empty lists, trees, etc.) and, more importantly,
certain types of structure concatenation. For instance, considering the DLL predicate
from the above example, the following predicate cannot be defined in our framework3:

               JOIN DLL(hd, p,tl, n) ≡ ∃x, y . DLL(hd, p, x, y) ∗ DLL(x, y,tl, n)

An extension to handle such definitions is possible, by introducing a special “concate-
nation” operation at the level of tree automata, which is considered for further investi-
gation.                                                                                ⊓
                                                                                       ⊔


Definition 4. Given a system P = {Pi ≡ |mj=1                    i
                                                                  Ri, j }ni=1 of inductive definitions, a rule
Ri, j (xi,1 , . . . , xi,k ) ≡ ∃z . Σ ∗ Pi1 (y1 ) ∗ . . . ∗ Pim (ym ) ∧ Π is connected if and only if there
exists a formal parameter xi,ℓ , 1 ≤ ℓ ≤ k such that:

  – xi,ℓ is a root of Σ, and
  – for each j = 1, . . . , m, there exists 0 ≤ s < |y j | such that (y j )s is Σ ∧ Π-reachable
    from xi,ℓ , and xi j ,s is a root of the head of each rule of Pi j .

An inductive system is said to be connected if all its rules are connected. In the rest
of this section, we consider only connected systems. This condition is necessary, since
later on it is proved that entailment between predicates of disconnected systems is un-
decidable, in general (Thm. 2 in Sec. 5). Notice that the DLL and TLL systems from
Examples 1 and 2 are both connected.


2.5 Tree Automata
A (finite, non-deterministic, bottom-up) tree automaton (abbreviated as TA in the fol-
lowing) is a quadruple A = hQ, Σ, ∆, Fi, where Σ is a finite alphabet, Q is a finite set of
states, F ⊆ Q is a set of final states, Σ is an alphabet, and ∆ is a set of transition rules
of the form σ(q1 , . . . , qn ) → q, for σ ∈ Σ, and q, q1 , . . . , qn ∈ Q. Given a tree automaton
A = hQ, Σ, ∆, Fi, for each rule ρ = (σ(q1 , . . . , qn ) −
                                                         → q), we define its size as |ρ| = n + 1.
The size of the tree automaton is |A| = ∑ρ∈∆ |ρ|. A run of A over a tree t : N∗ ⇀ f in Σ
is a function π : dom(t) → Q such that, for each node p ∈ dom(t), where q = π(p), if
                                                                                              π
qi = π(p.i) for 1 ≤ i ≤ n, then ∆ has a rule (t(p))(q1 , . . . , qn ) → q. We write t =⇒ q
to denote that π is a run of A over t such that π(ε) = q. We use t =⇒ q to denote that
   π
t =⇒ q for some run π. The language of a A is defined as L (A) = {t | ∃q ∈ F, t =⇒ q}.

3 Tiles and Semantics of Inductive Definitions
A tile is a tuple T = hϕ, x−1 , x0 , . . . , xd−1 i, for some d ≥ 0, where ϕ is a basic SL formula
and each xi is a tuple of pairwise distinct variables, called a port, such that xi ∩ x j = 0,   /
for all −1 ≤ i < j < d, and x−1 ∪ x0 ∪ . . . ∪ xd−1 ⊆ FV (ϕ). The set of all tiles is denoted
 3 However, defining concatenation of trees with linked leaves is possible when the root is allo-

   cated: JOIN TLL(root, ll, lr) ≡ ∃x, y, z . root 7→ (x, y, nil) ∗ TLL(x, ll, z) ∗ TLL(y, z, lr).


                                                     10
by T . The variables from x−1 are said to be incoming, the ones from x0 , . . . , xd−1 ,
are said to be outgoing, and the ones from par(T ) = FV (ϕ) \ (x−1 ∪ x0 ∪ . . . ∪ xd−1 )
are called parameters. The arity of a tile T = hϕ, x−1 , x0 , . . . , xd−1 i is the number of
outgoing ports, denoted by #(T ) = d. In the following, we denote form(T ) ≡ ϕ and
porti (T ) ≡ xi , for all i = −1, 0, . . . , d − 1.
    Given two tiles T1 = hϕ1 , x1−1 , x10 , . . . , x1d−1 i and T2 = hϕ2 , x2−1 , x20 , . . . , x2e−1 i such
that FV (ϕ1 ) ∩ FV (ϕ2 ) = 0,  / for some 0 ≤ i ≤ d − 1 such that |x1i | = |x2−1 |, we define
their i-composition:

                 T1 ⊛i T2 = hψ, x1−1 , x10 , . . . x1i−1 , x20 , . . . , x2e−1 , x1i+1 , . . . , x1d−1 i
                 where ψ ≡ ∃x1i ∃x2−1 . ϕ1 ∗ ϕ2 ∧ x1i = x2−1 .

For a tree position q ∈ N∗ and a tile T = hϕ, x−1 , x0 , . . . , xd−1 i, we denote by T q the tile
obtained by renaming every free variable x ∈ x−1 ∪ x0 ∪ . . . ∪ xd−1 by xq . Note that the
parameters x ∈ par(T ) are not changed by this renaming.
Definition 5. A tiled tree is a tree t : N∗ ⇀ f in T such that, for all positions p ∈ dom(t),
the following holds:
  – #t (p) = #(t(p)), i.e. the arity of p equals the arity of its label in t, and
  – for all 0 ≤ i < #t (p), the d-composition t(p) p ⊛i t(p.i) p.i is defined.
A tiled tree t corresponds to a tile defined inductively, for any p ∈ dom(t), as:
        Φ(t, p) = t(p) p ⊛0 Φ(t, p.0) ⊛1 Φ(t, p.1) . . . ⊛#(p)−1 Φ(t, p.(#t (p) − 1)).
The tile Φ(t, ε) is said to be the characteristic tile of t and it is denoted in the following
as Φ(t). It can be easily shown, by induction on the structure of the tiled tree t, that
Φ(t) = hψ, x−1 i, for an SL formula ψ and an incoming port x−1 . In other words, Φ(t)
has no outgoing ports. In this case, we write S |= Φ(t) for S |= ψ.
      Given an inductive system P = {Pi ≡ |mj=1         i
                                                          Ri, j }ni=1 of the form (1), for each rule
Ri, j (x) ≡ ∃u . Σ ∗ Pi0 (y0 ) ∗ . . . ∗ Pin−1 (yd−1 ) ∧ Π, where x ∩ u = 0,     / we define a tile
Ti, j = hϕ, x, z0 , . . . , zd−1 i, where zi are disjoint from y j , for all 0 ≤ i, j < d, and ϕ =
                   V
∃u . Σ ∧ Π ∧ d−1      i=0 zi = yi .
                                                 n
Definition 6. Let P = Pi ≡ |mj=1
                                       i
                                           Ri, j i=1 be an inductive system (1). An unfolding tree
of P is a tiled tree t : N∗ ⇀ f in T such that:
  – t(ε) = Ti, j , for some 1 ≤ j ≤ mi , and
  – for every position p ∈ dom(t), if t(p) = Ti, j and tail(Ri, j ) = hPi0 , . . . , Pid−1 i, where
       d = #(Ti, j ), then for all 0 ≤ j < d, we have t(p. j) = Ti j ,k , for some 1 ≤ k ≤ mi j .
If t(ε) = Ti, j , for some 1 ≤ j ≤ mi , we say that t is i-rooted.
We denote by Ti (P ) the set of i-rooted unfolding trees of P . The semantics of a predi-
cate Pi (x) ∈ P is defined as follows: S |= Pi (x) ⇐⇒ S |= Φ(t), for some t ∈ Ti (P ). Given
an inductive system P and two predicates Pi (x1 , . . . , xn ) and Pj (y1 , . . . , yn ) of P , with the
same number of formal parameters n, and a tuple of variables x, where |x| = n, the en-
tailment problem is defined as follows: Pi (x) |=P Pj (x) : ∀S . S |= Pi (x) ⇒ S |= Pj (x).
A rooted inductive system hP , Pi i is an inductive system P with a designated predicate
Pi ∈ P . Two rooted systems hP , Pi i and hQ , Q j i are said to be equivalent if and only if
Pi |=P ∪Q Q j and Q j |=P ∪Q Pi .
                                                          11
Definition 7. A rooted inductive system h{P1 , . . . , Pn }, Pi i is said to be local if and only
if for each unfolding tree t ∈ Ti (P ) and each state S |= Φ(t), S is local.

The locality problem asks, given an inductive system P = {P1 , . . . , Pn }, and an index
i = 1, . . . , n, whether the rooted system hP , Pi i is local. Our method for deciding entail-
ment problems of the form Pi |=P Pj is shown to be sound and complete provided that
both hP , Pi i and hP , Pj i are local. Otherwise, if one system is not local, our method is
sound, i.e. the algorithm returns “yes” only if the entailment holds. We describe fur-
ther a canonization procedure (Sec. 4.1) which performs a sufficient locality test on the
system, prior to the encoding of the inductive system as a tree automaton.

3.1 Canonical Tiles
This section defines a class of canonically tiled trees (or, to be short, canonical trees)
intended to reduce the number of ways in which a given local state can be encoded.
Moreover, it is shown that despite a local state can still be described by several different
canonical trees, such trees must be in a rotation relation called a canonical rotation. This
fact is the basis of the completeness argument of our method. By defining a closure
of tree automata (accepting canonical trees of states described by a given inductive
predicate) under canonical rotations, we ensure that any entailment between two local
inductive predicates can be reduced to a language inclusion problem. The case of non-
local states is subsequently dealt with in a sound (yet, in general, not complete) way in
the next subsection (Sec. 3.2).
    A tile T = hϕ, x−1 , x0 , . . . , xd−1 i is said to be a singleton if ϕ is of one of the forms:
 1. ∃z . z 7→ (y0 , . . . , ym−1 ) ∧ Π or
 2. z 7→ (y0 , . . . , ym−1 ) ∧ Π and z ∈ par(T )
and the following holds:
  – For all −1 ≤ i < d, xi ∩ ({z, nil} ∪ par(T )) = 0,        / i.e. neither the incoming nor the
     outgoing tuples of variables contain z, nil, or parameters.
  – For each 0 ≤ j < m, exactly one of the following holds: either (i) y j ≡ z, (ii) y j ≡ nil,
     (iii) y j ∈ par(T ), or (iv) there exists a unique tuple of variables xi , −1 ≤ i < d, such
     that y j occurs in xi .
  – For each outgoing tuple of variables xi , 0 ≤ i < d, there exists a variable y j 6∈
     {z, nil} ∪ par(T ), for some 0 ≤ j < m, such that y j occurs in xi .

We denote the spatial formula of a singleton tile as (∃z) z 7→ (y0 , . . . , ym−1 ) in order to
account for the optional quantification of the allocated variable z. A singleton tile T =
h(∃z) z 7→ (y0 , . . . , ym−1 ) ∧ Π, x−1 , x0 , . . . , xd−1 i is said to be canonical if, moreover, for
                                                           fw
all −1 ≤ i < d, xi can be factorized as xi ≡ xi · xbw             i such that:

 1. xbw
      −1 = hyh0 , . . . , yhk i, for some ordered sequence 0 ≤ h0 < . . . < hk < m, i.e. the
    incoming tuple is ordered by the selectors referencing its elements.
                               fw
 2. For all 0 ≤ i < d, xi ≡ hy j0 , . . . , y jki i, for some ordered sequence 0 ≤ j0 < . . . <
     jk < m, i.e. each outgoing tuple is ordered by the selectors referencing its elements.
                                    fw                  fw
 3. For all 0 ≤ i, j < d, if (xi )0 ≡ y p and (x j )0 ≡ yq , for some 0 ≤ p < q < m, then
    i < j, i.e. outgoing tuples are ordered by the selector referencing the first element.
                                                                              V
 4. (x−1fw
              0 ∪ . . . ∪ xd−1 ) ∩ {y0 , . . . , ym−1 } = 0
           ∪ xbw              bw                           / and Π ≡ x−1
                                                                      fw
                                                                         = z ∧ d−1   bw
                                                                                i=0 xi = z.
                                                  12
                        p             p
             hd          prev          prev                                           r
                                        ϕ: hd (y0,p)
                                next         /\ hd = x1
                                    y0 x 1
             next       prev
                                    x0 y 1
                                         prev
                                        ϕ: ∃z. z (y0,y1)
                                next            /\ z = x0
                                    y x         /\ z = x1
             next        prev        0       1
                                    x0 y 1
                                                                            ϕ: ∃z. z (y0,y1)
                                        prev
                                                                               /\ z = x0 /\ z = x1
                                       ϕ: ∃z. z (y0,y1)
                                                                             next
                                next          /\ z = x0                                    prev

                                    y0 x 1     /\ z = x1                    y0 x 1                y1 x 0
             next        prev
                                    x0 y 1                                  x0 y 1                x1 y 0
                                        prev                                                                 next

                                       ϕ: ∃z. z (y0,y1)      ϕ: ∃z. z (y0,y1) prev                           ϕ: ∃z. z (y0,y1)
                                next          /\ z = x0         /\ z = x0 next               prev
                                                                                                                    /\ z = x0
                                               /\ z = x1        /\ z = x1                                            /\ z = x1
             next       prev        y x
                                     0       1                               y0 x 1               y1 0       x
                                   x0 y 1                                    x0 y 1               x1 y 0
                                       prev                                                                  next

                                      ϕ: tl (n,y1)               ϕ: tl (n,y1)       prev
                                                                                                             ϕ: hd (y0,p)
             tl         next     next      /\ z = x0                /\ z = x0   next              prev
                                                                                                                  /\ hd = x1
                    n                    n                                      n                        p



Fig. 4. An example of a DLL with two of its canonical trees (related by a canonical rotation r).


     Given a canonical tile T = h(∃z) z 7→ (y0 , . . . , ym−1 ) ∧ Π, x−1 , x0 , . . . , xd−1 i, the
                                             fw                                       fw
decomposition of each tuple xi into xi and xbw        i is unique. This is because xi contains
all referenced variables y j that occur in an output port xi (since xi ∩{y0 , . . . , ym−1 } = 0)
                                                                        bw                       /
in the same order in which they are referenced in z 7→ (y0 , . . . , ym−1 ). The same holds for
                                              fw
the input port x−1 , with the roles of x−1 and xbw     −1 swapped. As each outgoing port must
contain at least one such variable, by the definition of singleton tiles, we also have that
  fw
xi 6= 0,/ for all 0 ≤ i < d. We denote further by portif w (T ) and portbw       i (T ) the tuples
  fw
xi and xbw i , resp., for all i = −1, . . . , d − 1. The set of canonical tiles is denoted as T c .


Definition 8. A tiled tree t : N∗ ⇀ f in T c is said to be canonical if and only if, for any
                                                          fw                fw
p ∈ dom(t) and each 0 ≤ i < #t (p), we have |porti (t(p))| = |port−1 (t(p.i))| and
     bw                bw
|porti (t(p))| = |port−1 (t(p.i))|.


Example 3 (cont. of Ex. 1). To illustrate the notion of canonical trees, Fig. 4 shows two
canonical trees for a given DLL. The tiles are depicted as big rectangles containing
the appropriate basic formula as well the input and output ports. In all ports, the first
variable is in the forward and the second in the backward part.


     We will now work towards the notion of canonical rotations. For that, we first give
one technical definition. Given a canonical tree t : N∗ ⇀ f in T c , and a state S = hs, hi, let
u : dom(t) → dom(h) be an arbitrary tree labeled with allocated locations from S. For
each position p ∈ dom(t) its explicit neighbourhood with respect to t and u is the state
Sht,u,pi = hs p , h p i defined as follows:


 – h p = h, and

                                                            13
            
                                      fw
            
            
             u(p)        if x ∈ port−1 (t(p)) ∪ portbw                      bw
                                                      0 (t(p)) ∪ . . . ∪ port#t (p)−1 (t(p))
                                     fw
 – s p (x) = u(p.i)       if x ∈ porti (t(p)), for some 0 ≤ i < #t (p)
            
            
             u(p.(−1)) if p 6= ε and x ∈ portbw−1 (t(p))
              s(x)        otherwise
            
   where Shu(p)i = hs, hi is the neighbourhood of the location u(p) in S.

   An important property of canonical trees is that each state that is a model of the
characteristic tile Φ(t) of a canonical tree t (i.e. S |= Φ(t)) can be uniquely described
by a local spanning tree u : dom(t) → Loc, which has the same structure as t, i.e.
dom(u) = dom(t). An immediate consequence is that any two models of Φ(t) differ
only by a renaming of the allocated locations, i.e. they are identical up to isomorphism.

Lemma 3. Let t : N∗ ⇀ f in T c be a canonical tree, and let S = hs, hi be a state. Then
S |= Φ(t) iff there exists a local spanning tree u : dom(t) → dom(h) such that, for all
p ∈ dom(t):

          fw                                k
 1. |porti (t(p))| = ||{k ∈ Sel | u(p) −
                                       →S u(p.i)}||, for all 0 ≤ i < #t (p).
                                            k
 2. |portbw                               →S u(p.(−1))}|| if p 6= ε.
           −1 (t(p))| = ||{k ∈ Sel | u(p) −
 3. Sht,u,pi |= form(t(p)).

Proof. “⇒” By induction on the structure of t. For the base case #t (ε) = 0, i.e. dom(t) =
{ε}, we have t(ε) = hform(t(ε), port−1 (t(ε))i and therefore S |= Φ(t) if and only if
S |= form(t(ε)). Since t(ε) is a canonical tile, only one location is allocated in dom(h),
i.e. dom(h) = {ℓ}, for some ℓ ∈ Loc. We define u = {(ε, ℓ)}. It is immediate to check
that u is a local spanning tree of S, and that Sht,u,εi = S |= form(t(ε)) – points (1) and
(2) are vacuously true.
     For the induction step #t (ε) = d > 0, we have:

                      Φ(t, ε) = t(ε)ε ⊛0 Φ(t, 0) . . . ⊛d−1 Φ(t, d − 1)

Since S |= Φ(t, ε), there exist states Si = hsi , hi i, for each −1 ≤ i < d, such that S−1 |=
t(ε)ε and Si |= Φ(t, i), for all 0 ≤ i < d, and moreover, S = S−1 ⊎ S0 ⊎ . . . ⊎ Sd−1 .
By the induction hypothesis, for each 0 ≤ i < d there exists a local spanning tree
ui : dom(t|i ) → dom(hi ), meeting conditions (1), (2) and (3). Since S−1 |= t(ε)ε , it must
be that dom(h−1 ) = {ℓ} for some location ℓ ∈ Loc. We define u as follows:

                                u(ε) = ℓ
                               u(i.q) = ui (q) for all q ∈ dom(ui )

To prove that u is a spanning tree of S, let p ∈ dom(u) be a position, and 0 ≤ i < #u (p)
be a direction. We distinguish two cases:
                                                                          k
                          fw
                                  / hence there exists an edge ℓ −
 – if p = ε, then porti (t(p)) 6= 0,                             →S−1 ui (ε). Then
          k
   u(p) −→S u(p.i) as well.
 – if p = j.q, and q ∈ dom(u j ), for some 0 ≤ j < d, by the induction hypothesis, there
                                                k                              k
                                             →S j u j (q.i) = u(p.i), i.e. u(p) −
    exists k ∈ Sel, such that u(p) = u j (q) −                                  →S u(p.i).
                                             14
                                                      k
To prove that u is a local spanning tree of S, let κ −
                                                     →S κ′ be an edge, for some κ, κ′ ∈
dom(h). Since dom(h) is a disjoint union of dom(h−1 ) = {ℓ}, dom(h0), . . . , dom(hd−1 ),
we distinguish several cases:

 – if κ ∈ dom(h−1) and κ′ ∈ dom(hi ), for some 0 ≤ i < d, then u(p) = κ = ℓ and
   u(i) = ui (ε) = κ′ is the only possibility – due to the strict semantics of SL, it is not
   possible to define an edge between ℓ and an location κ′ = ui (q), unless q = ε.
 – if κ, κ′ ∈ dom(hi ), for some 0 ≤ i < d, then, by the induction hypothesis, there exists
   q ∈ dom(ui ) and 0 ≤ j < #ui (q) such that κ = ui (q) = u(i.q) and κ′ = ui (q. j) =
   u(i.q. j).
 – if κ ∈ dom(hi ) and κ′ ∈ dom(h j ), for some 0 ≤ i, j < d, then we reach a contra-
   diction with the strict semantics of SL – since there is no equality between output
   ports in t(ε), it is not possible to define an edge between a location from dom(hi )
   and dom(h j ),

The proofs of points (1), (2) and (3) are by the strict semantics of SL.
“⇐” By induction on the structure of t. In the base case #t (ε) = 0, i.e. dom(t) = {ε},
then t(ε) = hform(t(ε), port−1 (t(ε))i. We have S = Sht,u,εi |= form(t(ε)), by point (3),
hence S |= Φ(t).
    For the induction step #t (ε) = d > 0, let ui = u|i , for all 0 ≤ i < d. Since u is a
                                                    / for all 0 ≤ i < j < d. For all −1 ≤
bijective function, we have img(ui ) ∩ img(u j ) = 0,
i < d, we define Si = hsi , hi i, where:
                           
                            h(ℓ) if ℓ ∈ img(ui )
                hi (ℓ) =                            for all ℓ ∈ Loc, if i ≥ 0
                           ⊥ otherwise
                            h(ℓ) if u(ε) = ℓ
               h−1 (ℓ) =                                      for all ℓ ∈ Loc
                           ⊥ otherwise
                            s(x) if s(x) ∈ Img(hi )
                 si (x) =                                     for all x ∈ Var
                            ⊥ otherwise

It is not hard to show that S = S−1 ⊎ S0 ⊎ . . . Sd−1 . Since u is a local spanning tree of
S, ui is a local spanning tree for Si , for all 0 ≤ i < d, and conditions (1), (2) and (3)
hold for Si and ui , respectively. By the induction hypothesis, we have Si |= Φ(t|i , ε). By
points (1), (2) and (3) moreover, we have that S−1 |= form(t(ε)). Hence S |= Φ(t). ⊓       ⊔

The following definition is a refinement of Def. 2. The change in the structure of the
tree is mirrored by a change in the structure of the canonical tiles labeling the tree.


Definition 9. Given two canonical trees t, u : N∗ ⇀ f in T c , we say that u is a canonical
rotation of t, denoted t ∼cr u, if and only if r : dom(t) → dom(u) is a bijective func-
tion, and for all p ∈ dom(t), there exists a substitution σ p : Var ⇀ f in Var such that
form(t(p))[σ p ] ≡ form(u(r(p))), and for all 0 ≤ i < #t (p), there exists j ∈ D (u) such
that r(p.i) = r(p). j, and:

                                            15
            fw                                    fw
       porti (t(p))[σ p ] ≡ if j ≥ 0 then port j (u(r(p))) else portbw
                                                                    −1 (u(r(p)))
           bw                                 bw                    fw
       porti (t(p))[σ p ] ≡ if j ≥ 0 then port j (u(r(p))) else port−1 (u(r(p)))


Example 4 (cont. of Ex. 3). The notion of canonical rotation is illustrated by the canon-
ical rotation r relating the two canonical trees of a DLL shown in Fig. 4. In its case,
the variable substitutions are simply the identity in each node. Note, in particular, that
when the tile 0 of the left tree (i.e., the second one from the top) gets rotated to the tile
1 of the right tree (i.e., the right successor of the root), the input and output ports get
swapped and so do their forward and backward parts.


    The following lemma is the key for proving completeness of our entailment check-
ing for local inductive systems: if a (local) state is a model of the characteristic tiles of
two different canonical tree, then these trees must be related by canonical rotation.


Lemma 4. Let t : N∗ ⇀ f in T c be a canonical tree and S = hs, hi be a state such that
S |= Φ(t). Then, for any canonical tree u : N∗ ⇀ f in T c , we have S |= Φ(u) iff t ∼c u.


Proof. If S |= Φ(t), there exists a local spanning tree ts : dom(t) → dom(h) of S, that
meets the three conditions of Lemma 3.
“⇒” If S |= Φ(u) there exists a local spanning tree us : dom(u) → dom(h) of S, that
meets the three conditions of Lemma 3. Since ts and us are spanning trees of S, by
Lemma 2, we have ts ∼u−1    s ◦ts
                                  us . Let r = u−1
                                                s ◦ ts from now on. Clearly, for any p ∈
dom(t), we have ts (p) = us (r(p)). Since dom(t) = dom(ts ) and dom(u) = dom(us ), we
have t ∼r u as well.
    We further need to prove the three points of Def. 9 in order to show that t ∼cr u.
Let p ∈ dom(t) be an arbitrary location. For the first two points, let 0 ≤ i < #t (p) be a
direction. We have ts (p.i) = us (r(p.i)) = us (r(p). j), for some j ∈ D (u). We distinguish
two cases:


 – if j ≥ 0, we compute:

                         fw                              k
                   |porti (t(p))| = ||{k ∈ Sel | ts (p) −
                                                        →S ts (p.i)}||
                                                                 k
                                   = ||{k ∈ Sel | us (r(p)) −
                                                            →S us (r(p). j)}||
                                   = |port fj w (u(r(p)))|

                   |portbw               bw
                        i (t(p))| = |port−1 (t(p.i))| (by Def. 8)
                                                             k
                                   = ||{k ∈ Sel | ts (p.i) −
                                                           →S ts (p)}||
                                                                     k
                                   = ||{k ∈ Sel | us (r(p). j) −
                                                               →S us (r(p))}||
                                   = |portbw
                                           j (u(r(p)))|


                                             16
 – if j = −1, we compute:
                   fw                                    k
             |porti (t(p))| = ||{k ∈ Sel | us (r(p)) −
                                                     →S us (r(p).(−1))}||
                            = |portbw
                                    −1 (u(r(p)))|

                                                                k
             |portbw
                  i (t(p))| = ||{k ∈ Sel | us (r(p).(−1)) −
                                                          →S us (r(p))}||
                                                                k
                                                              →S us (r(p).(−1). j′ )}||
                                = ||{k ∈ Sel | us (r(p).(−1)) −
                                   for some j ≥ 0 such that r(p) = r(p).(−1). j′
                                               ′
                                        fw
                                = |port j′ (u(r(p).(−1)))|
                                       fw
                                = |port−1 (u(r(p)))| (by Def. 8)

Since all variables are pairwise distinct in porti (t(p)) and port j (u(r(p))), respectively,
one can define a substitution σ p meeting the conditions of the first two points of Def. 9.
    For the third point of Def. 9, by Lemma 3, we have that Sht,ts ,pi |= form(t(p)) and
Shu,us ,r(p)i |= form(u(r(p))), where Sht,ts ,pi = hst , ht i is the explicit neighbourhood of p
w.r.t t and ts , and Shu,us ,pi = hsu , hu i is the explicit neighbourhood of r(p) w.r.t u and us .
Since t(p) and u(r(p)) are canonical tiles, we have:

                           form(t(p)) ≡ (∃z) z 7→ (y0 , . . . , ym−1 ) ∧ Πt
                        form(u(r(p))) ≡ (∃w) w 7→ (v0 , . . . , vn−1 ) ∧ Πu

where
                           fw               V# (p)−1
             Πt ≡ port−1 (t(p)) = z ∧ i=0
                                        t
                                               portbwi (t(p)) = z
                      fw                  V#u (r(p))−1
             Πu ≡ port−1 (u(r(p))) = w ∧ i=0           portbw
                                                           i (u(r(p))) = w
We extend the substitution σ p to σ p [z ← w] in the following. It is not hard to check that
st ◦ σ p = su and ht = hu . Hence Shu,us ,pi |= form(t(p))[σ p ]. Since both form(t(p))[σ p ]
and form(u(r(p))) have the same model, by the definition of the (strict) semantics of
SL, it follows that the numbers of edges are the same, i.e. m = n, and either both z and w
are quantified, or they are free. Thus, we obtain that form(t(p))[σ p ] ≡ form(u(r(p))).
”⇐” It t ∼c u, there exists a bijective function r : dom(t) → dom(u), meeting the con-
ditions of Def. 9. Let us = ts ◦ r−1 be a tree. Since ts and r are bijective, then also us is
bijective, and dom(us ) = dom(u). To prove that S |= Φ(u), it is enough to show that us
is a local spanning tree of S, meeting the three conditions of Lemma 3.
     To show that us is a local spanning tree of S, let p ∈ dom(us ) and i ∈ D+ (us ) such
that p.i ∈ dom(us ). Since ts ∼r us , by Prop. 1, we have us ∼r−1 ts , hence there exists
 j ∈ D (ts ) such that r−1 (p.i) = r−1 (p). j. Since ts is a spanning tree of S, there exists a
selector k ∈ Sel such that:
                                      k
               us (p) = ts (r−1 (p)) →
                                     − S ts (r−1 (p). j) = ts (r−1 (p.i)) = us (p.i)
                                                                                k
Hence us is a spanning tree of S. In order to prove its locality, let ℓ −  → ℓ′ be an edge
of S, for some ℓ, ℓ ∈ loc(S) and k ∈ Sel. Since ts is a local spanning tree of S, there
exist p ∈ dom(ts ) and i ∈ D+ (ts ) such that ℓ = ts (p) = us (r(p)) and ℓ′ = ts (p.i) =
us (r(p.i)). Since ts ∼r us , there exists j ∈ D (us ) such that r(p.i) = r(p). j. Hence we
                     k
                   → ℓ′ = us (r(p). j), i.e. the edge is local w.r.t. us as well.
have us (r(p)) = ℓ −

                                                17
    To prove point (1) of Lemma 3, let p ∈ dom(u) be an arbitrary position, and 0 ≤ i <
#u (p) be a direction. Since us ∼r−1 ts , we have r−1 (p.i) = r−1 (p). j, for some j ∈ D (t).
We compute:
                            k                                            k
                          →S us (p.i)}|| = ||{k ∈ Sel | ts (r−1 (p)) −
      ||{k ∈ Sel | us (p) −                                          →S ts (r−1 (p.i)}||
                                                                         k
                                             = ||{k ∈ Sel | ts (r−1 (p)) −
                                                                         →S ts (r−1 (p). j)}||
We distinguish two cases:
 – if j ≥ 0, we have, by Lemma 3 applied to t and ts :
                                         k                                fw
               ||{k ∈ Sel | ts (r−1 (p)) −
                                         →S ts (r−1 (p). j)}|| = |port j (t(r−1 (p)))|
                                                                       fw
                                                               = |porti (u(p))|

   The last equality is because r(r−1 (p). j) = r(r−1 (p)).i.
 – if j = −1, there exists d ∈ D+ (t) such that r−1 (p) = (r−1 (p).(−1)).d. But then we
   have:
                   r((r−1 (p).(−1)).d) = r(r−1 (p)) = p = (p.i).(−1)
                                         = r(r−1 (p).(−1)).(−1)
    We compute, further:
                                k
     ||{k ∈ Sel | ts (r−1 (p)) −
                               →S ts (r−1 (p). j)}|| = |portbw     −1
                                                            −1 (t(r (p)))|
                                                            bw     −1
                                                     = |portd (t(r (p).(−1)))| (by Def. 8)
                                                             fw
                                                     = |port−1 (u(p.i))| (by Def. 9)
                                                             fw
                                                     = |porti (u(p))| (by Def. 8)
For point (2) of Lemma 3, one applies a symmetrical argument. To prove point (3) of
Lemma 3, let Sht,ts ,r−1 (p)i = hst , ht i be the explicit neighbourhood of r−1 (p) w.r.t t and
ts . It is not hard to check that Shu,us ,pi = hst ◦ σ p , ht i, hence:

               Shu,us ,pi = hst ◦ σ p , ht i |= form(t(r−1 (p)))[σ p ] ≡ form(u(p))

The last equivalence is by Def. 9.                                                               ⊓
                                                                                                 ⊔

3.2 Quasi-Canonical Tiles
This section introduces a generalization of canonical trees, denoted as quasi-canonical
trees, that are used to define states with non-local edges. A singleton tile T = hϕ ∧
Π, x−1 , x0 , . . . , xd−1 i, for some d ≥ 0, is said to be quasi-canonical if and only if xi ≡
  fw           eq
       i · xi , for each −1 ≤ i < d, Π is pure formula, and all of the following holds:
xi · xbw
          fw           fw              fw
 1. hϕ, x−1 · xbw             bw                bw
                 −1 , x0 · x0 , . . . , xd−1 · xd−1 i is a canonical tile.
                           eq              eq                   eq         eq
 2. For each 0 ≤ i < |x−1 |, either (x−1 )i ∈ FV (ϕ) or (x−1 )i =Π (xk ) j for some unique
                                            fw
    indices 0 ≤ k < d and 0 ≤ j < |xk |.
                                                     eq            eq
 3. For each 0 ≤ k < d and each 0 ≤ j < |xk |, either (xk ) j ∈ FV (ϕ) or exactly one
                                        eq         eq                                      eq
    of the following holds: (i) (xk ) j =Π (x−1 )i for some unique index 0 ≤ i < |x−1 |.
           eq           eq                                                         eq
    (ii) (xk ) j =Π (xr )s for some unique indices 0 ≤ r < d and 0 ≤ s < |xr |.
                                        eq    S       eq
 4. For any two variables x, y ∈ x−1 ∪ d−1      i=0 xi , x =Π y only in one of the cases above.

                                                  18
                                                      ϕ: root      (y0,y1,nil) /\ x1 = x2
                                                                 root   n
                                                             l                   r


                                        y0 x1                                                 y1 x2
          ϕ: ∃z. z (y0,y1,nil)          x0 x1                                                 x0 x1       ϕ: ∃z. z        (y0,y1,nil)
             /\ z = x0                                                                                                   /\ z = x0
             /\ x2 = x3       n                                                                           n              /\ x1 = x2
                                                                                                              r
             /\ x1 = x4 l      r                                                                l
                                                                                                                         /\ x3 = x4
                      y0 x2       y1 x3 x4                                                   y0 x2 x3             y1 x4
                      x0 y0       x0 x1 y0                                                   x0 x1 y0             x0 x1
 ϕ: ll (nil,nil,y0)                          n                                                        n                      ϕ: ∃z. z (nil,nil,lr)
                             n                                                                                           n
    /\ ll = x0  ll                          ϕ: ∃z. z (nil,nil,y0)        ϕ: ∃z. z (nil,nil,y0)                                 lr   /\ z = x0
                       l r            l r      /\ z = x0                    /\ z = x0          l r                 l r             /\ z = x1
                                               /\ z = x1                    /\ z = x1


 Fig. 5. An example of a quasi-canonically tiled tree for the tree with linked leaves from Fig. 3.

    Notice that in a quasi-canonical tile T = h(∃z) z 7→ (y0 , . . . , ym−1 )∧Π, x−1 , x0 , . . . , xd−1 i,
the free variables from the set {y0 , . . . , ym−1 } \ {z, nil} are allowed to occur in some tu-
      eq
ple xi , for −1 ≤ i < d, as well. These variables can be used to describe non-local
                                                                 eq      eq
edges of states because equality constraints between x−1 and xi , for 0 ≤ i < d, may
span several tiles in a tree. In this case, the factorization of each port xi , −1 ≤ i < d,
       fw                 eq
into xi , xbw
            i , and xi is not uniquely determined by the distribution of the referenced
variables y0 , . . . , ym−1 . In practice (Sec.4.1) we use a conservative heuristic to define
                                                           eq         eq
this factorization. We denote in the following porti (T ) ≡ xi , for all −1 ≤ i < d. The
set of quasi-canonical tiles is denoted by T qc . The next definition of quasi-canonical
trees extends Def. 8 to the case of quasi-canonical tiles.
Definition 10. A tiled tree t : N∗ ⇀ f in T qc is quasi-canonical if and only if, for any
p ∈ dom(t) and each 0 ≤ i < #t (p), such that t(p) = hϕ, x−1 , x0 , . . . , xd−1 i, t(p.i) =
                                      fw       eq           fw          eq              fw
hψ, y−1 , y0 , . . . , ye−1 i, xi ≡ xi · xbw                      bw
                                          i · xi and y−1 ≡ y−1 · y−1 · y−1 , we have |xi | =
  fw                               eq      eq
|y−1 |, |xbw            bw
          i | = |y−1 |, and |xi | = |y−1 |.

Example 5 (cont. of Ex. 2). For an illustration of the notion of canonical trees, see
Fig. 5, which shows a canonical tree for the TLL from Fig. 3. The figure uses the same
notation as Fig. 4. In all the ports, the first variable is in the forward part, the backward
part is empty, and the rest is the equality part.
    For a quasi-canonical tree t : N∗ ⇀ f in T qc , we define its canonical projection as
t : dom(t) → T c , such that, for all p ∈ dom(t), we have:
 c

                                 fw                                                    fw
  t c (p) = hψ, port−1 (t(p)) · portbw                                           bw
                                    −1 (t(p)), . . . , port#t (p)−1 (t(p)) · port#t (p)−1 (t(p))i
                                  eq                     eq
            where ψ ⇐⇒ ∃port−1 (t(p)) . . . ∃port#t (p)−1 (t(p)) . form(t(p))

Intuitively, the canonical projection of a tree removes all equality variables from every
tile in the tree. Since these variables are involved only in equality constraints, the above
                    eq
quantifiers ∃porti (t(p)) can be eliminated. We can now define the notion of quasi-
canonical rotation for quasi-canonical trees as an extension of Def. 9.
Definition 11. Given two quasi-canonical trees t, u : N∗ ⇀ f in T qc , we say that u is
                                            qc
a quasi-canonical rotation of t, denoted t ∼r u, if and only if r : dom(t) → dom(u) is

                                                                        19
a bijective function such that t c ∼cr uc and, for all p ∈ dom(t), there exists a substitution
σ p : Var ⇀ f in Var such that, for all 0 ≤ i < #t (p) and all −1 ≤ j < #t (p), where r(p.i) =
                       eq                    eq
r(p). j, we have porti (t(p))[σ] ≡ port j (u(r(p))).

    The increase in expressivity (i.e. the possibility of defining non-local edges) comes
at the cost of a loss of completeness. The following lemma generalizes the necessity
direction (⇐) of Lemma 4 for quasi-canonical tiles. Notice that the sufficiency (⇒)
direction does not hold in general.

Lemma 5. Let t, u : N∗ ⇀ f in T qc be quasi-canonical trees such that t ∼qc u. For all
states S, if S |= Φ(t), then S |= Φ(u).

Proof. Let S be a state such that S |= Φ(t), and r : dom(t) → dom(u) be a bijective
                             qc
function such that t ∼r u. Then S |= Φ(t c ), and since we have t c ∼cr uc by Def. 11, then
also S |= Φ(u ), by Lemma 4. Also, for every p ∈ dom(t), let σ p : Var ⇀ f in Var be the
                    c

substitution from Def. 9.
     Assume that S 6|= Φ(u). Then there exists a non-trivial path p0 , . . . , pk ∈ dom(u),
for some k > 0, and some variables x0 ∈ FV (form(u(p0 ))), . . . , xk ∈ FV (form(u(pk ))),
such that x0 and xk are allocated in form(u(p0 )) and form(u(pk )), respectively, and for
all 0 ≤ i < k, we have xi =Πu xi+1 , where Πu is the pure part of form(Φ(u)). But then
                                                                         p0 (x0 ) and σ pk (xk ) are
r−1 (p0 ), . . . , r−1 (pk ) ∈ dom(t) is a path in t, and the variables σ−1             −1

allocated in t(r−1 (p0 )) and t(r−1 (pk )), respectively. Moreover, we have σ−1        pi (xi ) =Πt
σ pi+1 (xi+1 ), where Πt is the pure part of form(Φ(t)). Hence S 6|= Φ(t), contradiction.
  −1

                                                                                                  ⊓
                                                                                                  ⊔



4 From Inductive Definitions to Tree Automata
This section describes the reduction of an entailment problem, for given inductive sys-
tems, to a language inclusion problem between two tree automata. This reduction is the
basis of our method for entailments checking. The complexity of the reduction algo-
rithm is polynomial in the size of the input system.

4.1 Canonization

Given a rooted inductive system hP , Pi i, the canonization procedure described in this
section will produce an equivalent rooted inductive system hQ , Q j i, such that each un-
folding tree t ∈ T j (Q ) is canonical. For the latter inductive system, we define a TA rec-
ognizing its set of unfolding trees. For the rest of this section, let P = {Pi ≡ |mj=1
                                                                                     i
                                                                                       Ri, j }ni=1
be an inductive system of the form (1), where each rule is of the form Ri, j (x) ≡ ∃z . Σ ∗
Pi1 (y1 )∗ . . . ∗ Pim (ym )∧Π, y1 ∪. . . ∪ym ∪FV (Π) ⊆ x ∪z. We recall that Σ is a non-empty
spatial formula, and the pure formula Π can only specify equalities between (i) two ex-
istentially quantified variables from z, (ii) an existentially quantified variable from z
and a formal parameter from x, or (iii) between an allocated parameter from x and
some other formal parameter in x. Notice that equality between two different allocated
variables leads to unsatisfiable rules, therefore it will cause a pre-processing error.
                                                20
Elimination of equalities. The first pre-processing step consists in eliminating equal-
ities involving existentially quantified variables from the pure part Π of a rule. We use
the equivalence relation =Π induced by Π on the variables in the rule. For each variable
x ∈ x ∪ z, its equivalence class [x]Π either (i) contains at most one formal parameter, or
(ii) contains one or more formal parameters, out of which exactly one is allocated. We
consider this parameter to be the representative of the equivalence class, and replace
each occurrence of a variable in a rule by its representative. The result is an equivalent
system of the same size as the original.
     Let alloc(Σ) denote the set of allocated variables in Σ. For each equivalence class
[x]Π , where x ∈ x ∪ z, we define its representative to be either one of the following:
  – the unique formal parameter x ∈ [x]Π , if [x]Π ∩ x 6= 0/ and [x]Π ∩ x ∩ alloc(Σ) = 0,
                                                                                       /
                                                                                       /
  – the unique allocated parameter x ∈ [x]Π ∩ x ∩ alloc(Σ), if [x]Π ∩ x ∩ alloc(Σ) 6= 0,
  – the lexicographically minimal element minlex([x]Π ) of [x]Π , if [x]Π ∩ x = 0./
For a tuple of variables y = hy1 , . . . , yℓ i, let [y]Π denote the tuple of representatives of
the equivalence classes [y1 ]Π , . . . , [yℓ ]Π , respectively. Then we define the rule:

                       i, j (x) ≡ Σ ∗ Pi1 ([y1 ]Π ) ∗ . . . ∗ Pim ([ym ]Π ) ∧ Π
                      R=           =                                            =


where Σ= is obtained from Σ by replacing each free variable x ∈ FV (Σ) by the rep-
                                    V
resentative of [x]Π , and Π= ≡ {x = y | x, y ∈ x, x ∈ [y]Π ∩ alloc(Σ)} keeps only the
equalities between formal parameters, one of which is allocated. It is not hard to check
that any rooted system hP [R=                                                        =
                              i, j /Ri, j ], Pk i, obtained by replacing Ri, j with Ri, j , is equiva-
lent to the original rooted system hP , Pk i, for all k = 1, . . . , n. Moreover, the two systems
have the same size.
Reduction to one points-to proposition per rule. The second step of the canonization
procedure builds an inductive system in which the head of each rule consists of exactly
one points-to atomic proposition of the form x 7→ (y0 , . . . , yℓ ). This step succeeds under
the assumption that P is a connected system, and no rule has an empty head (other-
wise the system breaks the restrictions that we have introduced, and the computation is
aborted). The result is an equivalent connected system Q , whose size is increased by at
most a linear factor, i.e. |Q | = O (|P |). Algorithm 1 describes the splitting of rules into
sets of rules with exactly one points-to proposition.
     For each rule Ri, j , with head(Ri, j ) ≡ Σ, the procedure D EPTH F IRST T RAVERSE(Σ, x)
(line 8) performs a depth-first traversal of the spatial formula Σ ≡ ⋆si=1 xi 7→ (yi,1 , . . . ,
yi,mi ) starting with a randomly chosen free variable x ∈ FV (Σ), and builds an injective
depth-first spanning tree t : N∗ ⇀ f in AP(Σ) of the formula4. Each position p ∈ dom(t) is
labeled by one points-to atomic proposition
                                         S
                                                     from Σ, and each atomic proposition from Σ
is found in the tree, i.e. AP(Σ) = p∈dom(t) t(p). Formally, for all positions p ∈ dom(t),
such that t(p) ≡ xi 7→ (yi,1 , . . . , yi,mi ), we have:
  – For all 0 ≤ d < #t (p), alloc(t(p.d)) = {yi, j }, for some 1 ≤ j ≤ mi , i.e. the children
    of each position correspond to points-to formulae that allocate variables pointed to
    by the proposition of that position.
 4 It must be possible to build the spanning tree from any free variable x ∈ FV (Σ) unless the

  system is disconnected (in which case an error is announced and the computation aborted).


                                                 21
Algorithm 1 Reduction to one points-to proposition per rule
  input An inductive system P = {Pi ≡ |mj=1
                                         i
                                            Ri, j }ni=1
  output An inductive system Q with one points-to proposition per rule
 1: function SPLIT S YSTEM(P )
 2:    Q ← 0/
 3:     for all i = 1, . . . , n do                                              ⊲ iterate over all predicates
 4:         Pi ← empty predicate
 5:         for all j = 1, . . . , mi do                                         ⊲ iterate over all rules of Pi
 6:              assume Ri, j (x) ≡ ∃z . Σ ∗ Pi1 (y1 ) ∗ . . . ∗ Pik (yk )
 7:              choose root ∈ x ∩ FV (Σ)
 8:              t ← D EPTH F IRST T RAVERSE(Σ, root)
 9:              if dom(t) = 0/ then
10:                  error(“empty rule Ri, j ”)
                      S
11:              if   p∈dom(t) t(p) 6= AP(Σ) then
12:                   error(“disconnected rule Ri, j ”)
13:              for all s = 1, . . . , k do
14:                                                                                                /
                     Xs ← {p ∈ dom(t) | t(p) ≡ y 7→ (z1 , . . . , zℓ ), ys ∩ {z1 , . . . , zℓ } 6= 0}
15:                  if Xs = 0/ then
16:                      error(“disconnected rule Ri, j ”)
17:              for all p ∈ dom(t) do                                         ⊲ create fresh predicates
                       p       p                                       p.d
18:                  Pi, j = {Ri, j ≡ [p = ε ? ∃z] t(p) ∗ ⋆0≤d<#t(p) Pi, j (x, z) ∗ ⋆ s=1,...,k Pis (ys )}
                                                                                            minlex(Xs )=p
19:              Pi ← Pi | Rεi, j                                              ⊲ create root-level predicates
20:              Q ← Q ∪ {Pi,pj | p ∈ dom(t) \ {ε}}
21:         Q ← Q ∪ {Pi }
22:     return C LEANUP(Q )



  – For all 0 ≤ d < e < #t (p), if alloc(t(p.d)) = {yi, j } and alloc(t(p.e)) = {yi,k }, then
    j < k, i.e. the children of each node are ordered with respect to the selectors via
    which they are pointed to.
                                                                                    p       p
The spanning tree t is used to create a set of fresh predicates Pi, j ≡ Ri, j , one for each
position p ∈ dom(t) \ {ε}, and top rules Pi ≡ |mj=1     i
                                                          Rεi, j , which are the only rules in which
existential quantification is allowed. For each predicate occurrence Pi1 (y1 ), . . . , Pik (yk ),
the sets X1 , . . . , Xk ⊆ dom(t) correspond to the positions p where the actual parame-
ters are referred to by t(p) ≡ y 7→ (z1 , . . . , zℓ ). We chose the lexicographically minimal
position from each set X1 , . . . , Xk (line 18) to place the occurrences of Pi1 , . . . , Pik , re-
spectively.
    Finally, the new inductive system Q is cleaned (line 22) by removing (i) all unused
variables from the rules and from the calls to the predicates in which they are declared,
and (ii) moving existential quantifiers inside the rules where they are used. For instance,
in the example below, the existential quantifier ∃z has been moved from R1 (left) to R2
(right), because z is used in the points-to formula of R2 :
                                                                                             
         R1 (x) ≡ ∃y, z . x 7→ y ∗ R2(y, z) C LEANUP               R1 (x) ≡ ∃y . x 7→ y ∗ R2(y)
                                                −−−−−→
       R2 (y, z) ≡ y 7→ z                                          R2 (y) ≡ ∃z . y 7→ z

                                                       22
The elimination of useless variables is done in reversed topological order, always pro-
cessing a predicate Pi before Pj only if Pi occurs in a rule of Pj , whereas the elimination
of existential quantifiers is performed in topological order, i.e. we process Pi before Pj
only if Pj occurs in a rule of Pi .
    It can be easily checked that D EPTH F IRST T RAVERSE(Σ, root) takes time O (|Σ|),
and C LEANUP(Q ) takes time O (|Q|). Moreover, since the inductive system Q is ob-
tained (line 21) in time O (|P |), it must be the case that |Q | = O (|P |). Thus, the entire
Algorithm 1 takes time O (|P |). It is not hard to check that the result of Algorithm 1 is an
inductive system which is equivalent to the input, i.e. hP , Pi i and hSPLIT S YSTEM(P ), Pi i
are equivalent, for all i = 1, . . . , n.
Parameter elimination. The final pre-processing step, before conversion of a rooted
inductive system hP , Pi i to a tree automaton, is the specialisation of P with respect
to the predicate Pi (xi,1 , . . . , xi,ni ), and a tuple of actual parameters α = hα1 , . . . , αni i, not
occurring in the system. We say that a formal parameter xi,k of a rule Ri, j (xi,1 , . . . , xi,ni ) ≡
∃z . Σ ∗ Pi1 (y1 ) ∗ . . . ∗ Pim (ym ) ∧ Π is directly propagated to some (unique) parameter
of a predicate occurrence Pi j , for some 1 ≤ j ≤ m, if and only if xi,k 6∈ FV (Σ) and
xi,k ≡ (yi j )ℓ , for some 0 ≤ ℓ < |yi j |, i.e. xi,k is neither allocated nor pointed to by the head
of the rule, before being passed on to Pi j . We denote direct propagation of parameters
by the relation xi,k ❀ xi j ,ℓ , where xi j ,ℓ is the formal parameter of Pi j which is mapped to
the occurrence of (yi j )ℓ . We say that xi,k is propagated to xr,s if Xi,k ❀∗ xr,s , where ❀∗
denotes the reflexive and transitive closure of the ❀ relation. Algorithm 2 describes
the elimination of all variables that are propagated from the formal parameter tuple
of a given predicate. Notice that all eliminated variables are collected in a global set
Parameters, which will be used later, by Algorithm 4 to produce a tree automaton.
     The tracking/elimination of a given formal parameter is implemented by a recursive
function TRACK E LIMINATE(Pr , xr , del), where Pr is the current predicate, xr,s is the
currently tracked formal parameter of Pr (i.e. Tracked ❀∗ xr,s is an invariant for every
call to TRACK E LIMINATE), and del = true if and only if xr,s is to be removed from the
definition of Pr . If the currently tracked parameter xr,s is either allocated in a rule of Pr or
it is not propagated further, then every occurrence of xr,s is replaced with Tracked (line
8). Otherwise, if the parameter is propagated to Pj as x j,ℓ (line 10) and it is referenced
by the current rule (line 13), then it will not be removed any longer from the system
(line 15). In this case, we keep tracking it only to place the global variable Tracked in
the right place (line 8). Otherwise, if the parameter is not referenced, it will be removed
completely from the rule (line 18). Finally, the old predicates in Q ∩ P , which have
become unreachable from the Pi , due to the insertion of the new ones (Qr ), are removed
from the system by a call to the T RIM procedure. The running time of the algorithm is
linear in the size of P (i.e. each rule is visited at most once) and the size of the output
system is reduced with respect to the input, i.e. |Q | ≤ |P |.

Example 6 (cont. of Ex. 1). As an example of parameter elimination, let us take the
predicate DLL introduced in Sect. 2.4, called as DLL(a, b, c, d). After the parameter
elimination and renaming the newly created predicates, we have a call Q1 (without
parameters) of the following inductive system:
                  Q1 () ≡ a 7→ (d, b) ∧ a = c | ∃x. a 7→ (x, b) ∗ Q2 (x, a)
             Q2 (hd, p) ≡ hd 7→ (d, p) ∧ hd = c | ∃x. hd 7→ (x, p) ∗ Q2(x, hd)

                                                   23
4.2 Conversion to tree automata
The following algorithm takes as input a rooted inductive system hP , Pi i such that Pi has
no formal parameters, the head of each rule in P is of the form ∃z . α 7→ (y0 , . . . , ym−1 )∧
Π, and for each x ∈ FV (Π), we have (i) α ∈ [x]Π and (ii) [x]Π ∩ {y0 , . . . , ym−1 } = 0./ It is
easy to see that these conditions are ensured by the first two steps of pre-processing (i.e.
the elimination of equalities and the reduction to one points-to proposition per rule). The
first step of the conversion computes several sets of parameters that are called signatures
and defined as follows:
              fw
         sig j = {x j,k | x j,k is allocated in every rule of Pj } ∩
                    {x j,k | there is an edge to (y)k in every occurrence Pj (y) of P }
         sigbwj   = {x j,k | there is an edge to x j,k in every rule of Pj } ∩
                    {x j,k | (y)k is allocated for every occurrence Pj (y) of P }
               eq                                   fw
          sig j = {x j,1 , . . . , x j,n j } \ (sig j ∪ sigbw
                                                           j )
where hx j,1 , . . . , x j,n j i is the tuple of formal parameters of the predicate Pj , in P , for all
j = 1, . . . , n. The signatures of the system are computed via Algorithm 3 .
    The result of the algorithm can be used to implement a sufficient test of locality: a
given system is local if sigi = 0,
                                      eq
                                            / for each i. This simple test turned out to be powerful
enough for all the examples that we considered in our experiments in Section 6.
Example 7 (cont. of Ex. 6). The signatures for the system in Example 6 are:
       fw             eq
              1 = sig1 = 0
  – sig1 = sigbw          /
  – sig2 = {0}, sig2 = {1}, sig2 = 0/
       fw          bw          eq


The fact that, for each i, we have sigi = 0/ informs us that the system is local.
                                           eq

      Next, we define a normal form for the quasi-canonical tiles, used as alphabet sym-
bols in the rules of the tree automaton. Given a quasi-canonical tile T = hϕ, x−1 , x0 , . . . ,
xk−1 i, for some k ≥ 0, where ϕ ≡ (∃z) z 7→ (y0 , . . . , ym−1 ) ∧ Π, for some m > 0, let
ξ0 , . . . , ξm be unique variable namesi. Let σ be the substitution defined as σ(z) = ξ0 , and
σ(yi ) = ξi+1 , for all 0 ≤ i < m. For all variables x−1 ∪ x0 ∪ . . . ∪ xk−1 = {α1 , . . . , αn }, we
chose unique names ξm+1 , . . . , ξm+n , according to the order in which they appear in the
ports x−1 , x0 , . . . , xk−1 , respectively, and we extend the substitution further by defining
σ(αi ) = ξm+i , for all i = 1, . . . , n. We define the normal tile T = hϕ[σ], x−1 [σ], x0 [σ], . . . ,
xk−1 [σ]i. For a quasi-canonical tree t : N∗ ⇀ f in T qc , we define the normal tree t as
t(p) = t(p), for all p ∈ dom(t).
      The SL 2 TA function (Algorithm 4) builds a tree automaton A, for a rooted system
hP , Pi i. For each rule in the system, the algorithm creates a quasi-canonical tile, where
                                                         fw        eq
the input and output ports xi are factorized as xi · xbw      i · xi , according to the precom-
                                                                bw
puted signatures. The backward part of the input port x−1 and the forward parts of the
                    fw
output ports xi , for i ≥ 0, are sorted according to the order of incoming selector edges
from the single points-to formula α 7→ (β), by the SELECTOR S ORT function (lines 18
and 28). The output ports xi , i ≥ 0, are sorted within the tile, according to the order of
                                         fw
the selector edges pointing to (xi )0 , for each i = 0, 1, . . . (function SORT T ILE, line 31).
Finally, each predicate name Pj is associated a state q j (line 33), and for each inductive
rule, the algorithm creates a transition rule in the tree automaton (line 34). The final
state corresponds to the root of the system (line 35). The following lemma summarizes
the tree automata construction.
                                                  24
                                                                                                     n
Lemma 6. Given a rooted inductive system hP , Pi (x)i where P = Pi ≡ |mj=1
                                                                                            i
                                                                                               Ri, j i=1
and x = hxi,1 , . . . , xi,ni i, and a vector α = hα1 , . . . , αni i of variables not used in P . Then,
for every state S, we have S |= Pi (α) if and only if there exists t ∈ L (A) such that
S |= Φ(t) where A = SL 2 TA(P , i, α). Moreover, |A| = O (|P |).

Example 8 (cont. of Ex. 7). The automaton corresponding to the DLL system called by
DLL(a, b, c, d) is A = hΣ, {q1 , q2 }, ∆, {q1 }i where:
                                        /
               ha 7→ (b, d) ∧ a = c, 0i()    → q1 ha 7→ (x, b), 0,  / (x, a)i(q2 ) → q1 
                                                                                        

           ∆ = h∃hd ′ .hd ′ 7→ (d, p) ∧ hd = c ∧ hd ′ = hd, (hd, p)i()              → q2
                h∃hd ′ .hd ′ 7→ (x, p) ∧ hd ′ = hd, (hd, p), (x, hd)i(q2 )
              
                                                                                    → q2
                                                                                         




4.3 Rotation of Tree Automata
This section describes the algorithm that produces the closure of a quasi-canonical
tree automaton (i.e. a tree automaton recognizing quasi-canonical trees only) under
rotation. The result of the algorithm is a tree automaton Ar that recognizes all trees
u : N∗ ⇀ f in T qc such that t ∼qc u, for some tree t recognized by A = hQ, Σ, ∆, Fi. Al-
gorithm 5 describes the rotation closure. The result of Algorithm 5 (function SL 2 TA)
is a language-theoretic union of A and automata Aρ , one for each rule ρ of A. The idea
                                                                  f
behind the construction of Aρ = hQρ , Σ, ∆ρ , {qρ }i can be understood by considering
a tree t ∈ L (A), a run π : dom(t) → Q, and a position p ∈ dom(t), which is labeled
with the right hand side of the rule ρ = T (q1 , . . . , qk ) −          → q of A. Then L (Aρ ) will con-
                                                qc
tain the rotated tree u, i.e. t ∼r u, where the significant position p is mapped into the
root of u by the rotation function r, i.e. r(p) = ε. To this end, we introduce a new rule
                                                         f
Tnew (q0 , . . . , q j , qrev , q j+1 , . . . , qn ) −
                                                     → qρ , where the tile Tnew mirrors the change in the
                                                     rev
structure of T at position p, and q ∈ Qρ is a fresh state corresponding to q. The con-
struction of Aρ continues recursively, by considering every rule of A that has q on the
left hand side: U(q′1 , . . . , q, . . . , q′ℓ ) →    − s. This rule is changed by swapping the roles of
q and q′ and producing a rule Unew (q′1 , . . . , srev , . . . q′ℓ ) −    → qrev , where Unew mirrors the
                                                                         rev
change in the structure of U. Intuitively, the states {q |q ∈ Q} mark the unique path
from the root of u to r(ε) ∈ dom(u). The recursion stops when either (i) s is a final state
of A, (ii) the tile U does not specify a forward edge in the direction marked by q, or (iii)
all states of A have been visited.
     The following lemma proves the correctness of Algorithm 5.
Lemma 7. Let A = hQ, T qc , ∆, Fi be a tree automaton. Then L (Ar ) = {u | u : N∗ ⇀ f in
T qc , ∃t ∈ L (A) . u ∼qc t}. Moreover, the size of Ar is of the order of O (|A|2 ).
                                                                                           S
Proof. “⊆” Let u ∈ L (Ar ) be a normal quasi-canonical tree. Then u ∈ L (A)∪ ρ∈∆ L (Aρ )
(lines 1 and 14 in Alg. 5). If u ∈ L (A), then we choose t = u and trivially t ∼qc u.
                                                         f
Otherwise u ∈ L (Aρ ), where Aρ = hQρ , T qc , ∆ρ , {qρ }i, for some ρ ∈ ∆ (line 13). Let
π : dom(u) → Qρ be the run of Aρ on u. Also let p0 ∈ dom(u) be the maximal (i.e. of
maximal length) position such that u(p0 ) = qrev , for some qrev ∈ Qrev (line 7). Let u| p .i
                                                                                                  0
be the subtrees of u rooted at the children of p0 , for all i = 0, . . . , #u (p0 ) − 1. Since p0 is
the maximal position of π to be labeled by some state in Qrev , it is easy to see that π| p .i
                                                                                                      0



                                                  25
are labeled by states in Q, hence π| p .i are runs of A over t| p .i , for all i = 0, . . . , #u (p0 )− 1
                                         0                                0
(the only rules of Aρ involving only states from Q are the rules of A, cf. line 8).
       We build a quasi-canonical tree t : N∗ ⇀ f in T qc and a run θ : dom(t) → Q of A on t
top-down as follows. Let p0 , p1 , . . . , pn = ε be the path composed of the prefixes of p0 ,
i.e. pi = pi−1 .(−1), for all i = 1, . . . , |p0 | = n. We build t, θ, and a path p0 = ε, p1 =
 j0 , . . . , pn ∈ dom(t), by induction on this path.
                                               fw               eq
       For the base case, let u(p0 ) = hϕ, x−1 · xbw  −1 · x−1 , x0 , . . . , x#u (p)−1 i be the tile which
labels u at position p0 . Let t(ε) = hϕ, 0,   / x0 , . . . , x j0 −1 , xbw     fw    eq
                                                                        −1 · x−1 · x−1 , x j0 , . . . , x#u (p)−1 i,
                                                                                f w eq
where j0 + 1 is the canonical position of the output port xbw             −1 · x−1 x−1 , in t(ε), according
to the order of selector edges in ϕ. Then Aρ has a rule:
                          u(p0 )(π(p0 .0), . . . , π(p0 .(#u (p) − 1))) −
                                                                        → π(p)
such that {π(p0 .0), . . . , π(p0 .(#u (p) − 1)} ∩ Qrev = 0.  / Since p0 is the maximal position
labeled with a state from Qrev , this rule was generated at line 9 in Alg. 5. It follows that
A has a rule
                          t(ε)(π(p0 .0), . . . , π(p0 .(#u (p0 ) − 1))) −
                                                                        →q
for some final state q ∈ F (line 7). Then let θ(ε) = q. We further define:
                                                                π| p .i
      (                                                       (
        u| p .i     if i = 0, . . . , j0 − 1                                if i = 0, . . . , j0 − 1
t|i =       0                                           θ|i =       0
        u| p .(i+1) if i = j0 + 1, . . . , #u (p0 ) − 1         π| p .(i+1) if i = j0 + 1, . . . , #u (p0 ) − 1
            0                                                                 0

For the induction step, for each 0 < i ≤ n, we have pi−1 = pi .ki , for some 0 ≤ ki <
#u (pi−1 ). We have u(pi ) = hϕ, x−1 , x0 , . . . , x#u (pi )−1 i, and define:
                                fw    eq                                fw        eq
       t(pi ) = hϕ, xbw                                       bw
                     ki · xki · xki , x0 , . . . , x ji −1 , x−1 · x−1 · x−1 , x ji , . . . , x#u (pi )−1 i
                                                                         fw       eq
where ji + 1 is the canonical position of the port xbw
                                                    −1 · x−1 · x−1 given by the the selector
edges in ϕ. Moreover, Aρ has a rule:
                          u(pi )(π(pi .0), . . . , π(pi .(#u (pi ) − 1))) →
                                                                          − π(pi )
                                                                                                   f
where π(pi .ki ) = π(pi−1 ) ∈ Qrev , π(pi ) ∈ Qrev if 0 ≤ i < n, and π(pn ) = qρ . Moreover,
this rule was introduced at line 18, if i < n, or at line 11, if i = n. Let i < n (the case
i = n uses a similar argument). If π(pi−1 ) = srev and π(pi ) = qrev , then A must have a
rule:
          t(pi )(π(pi .0), . . . , π(pi .( ji − 1)), q, π(pi. ji ), . . . , π(pi .(#u (pi ) − 1))) −
                                                                                                   →s
Let pi+1 = pi . ji and θ(pi+1 ) = q. We further define:
                                                                        π| p .ℓ
          (                                                           (
            u| p .ℓ     if ℓ = 0, . . . , ji − 1                                    if ℓ = 0, . . . , ji − 1
t| p .ℓ =       i                                           θ| p .ℓ =       i
    i       u| p .(ℓ+1) if ℓ = ji + 1, . . . , #u (pi ) − 1     i       π| p .(ℓ+1) if i = ji + 1, . . ., #u (pi ) − 1
                i                                                                      i

We define the following rotation function r : dom(t) → dom(u). For each i = 0, . . . , n,
we have r(pi ) = pi , and:
                              
                                r(pi .ℓ)       if ℓ = 0, . . . , ji − 1
                   r(pi .ℓ) =
                                r(pi .(ℓ + 1)) if ℓ = ji , . . . , #u (pi ) − 1

                                                        26
                                              qc
It is easy to check that indeed t ∼r u, and that θ is a run of A over t.
                                                                          qc
”⊇” Let u : N∗ ⇀ f in T qc be a quasi-canonical tree such that t ∼r u, for some t ∈ L (A)
and a bijective function r : dom(t) → dom(u). Let π : dom(t) → Q be a run of A over
t. We build an accepting run θ of Ar over the normal tree u. Let p0 ∈ dom(t) such
that r(p0 ) = ε is the root of u. If p0 = ε, it is easy to show that dom(u) = dom(t) and
r(p) = p, for all p ∈ dom(t), because both t and u are quasi-canonical trees, and the
order of children is given by the order of selector edges in the tiles labeling the trees.
Moreover, the normal form of these tiles is identical, i.e. u(p) = t(p), for all p ∈ dom(t),
hence u ∈ L (A) ⊆ L (A)r (cf. line 1).
     Otherise, if p0 6= ε, we consider the sequence of prefixes of p0 , defined as pi =
pi−1 .(−1), for all i = 1, . . . , n = |p0 |. Applying Lemma 1 to p0 , . . . , pn successively, we
obtain a path ε = r(p0 ), r(p1 ), . . . , r(pn ) ∈ dom(u), such that r(pi+1 ) = r(pi ).di , for all
i = 0, . . . , n − 1, and some positive directions d0 , . . . , dn−1 ∈ D+ (u).
     We build the run θ by induction on this path. For the base case, let t(p0 ) = q0 . Then
A has a rule ρ = (t(p0 )(q1 , . . . , q#t (p0 ) ) −
                                                  → q0 ) ∈ ∆. By the construction of Ar , cf. line
11, Aρ has a rule

                                                                                         f
                       (u(ε))(q1 , . . . , qd0 , qrev
                                                  0 , qd0 +1 , . . . , q#t (p0 ) ) −
                                                                                   → qρ .

                       f
We define θ(ε) = qρ and:

                                       π| p .i
                                   (
                                                   if i = 0, . . . , d0 − 1
                           θ|i =           0
                                       π| p .(i+1) if i = d0 + 1, . . . , #t (p0 ) − 1
                                          0


For the induction step, we denote qi = π(pi ), for all 0 < i ≤ n. Then A has a rule

     (t(pi ))(π(i.0), . . . , π(i.(ki − 1)), qi , π(i.(ki + 1)), . . . , π(i.(#t (pi ) − 1))) −
                                                                                              → qi+1 ,

for each 0 < i ≤ n. By the construction of Ar , cf. line 18, Aρ has a rule:

 (u(r(pi )))(π(i.0), . . . , π(i.(di − 1)), qrev
                                             i+1 , π(i.(di + 1)), . . . , π(i.(#t (pi ) − 1))) −
                                                                                               → qrev
                                                                                                  i .

We define θ(r(pi )) = qrev
                       i and:

                                         π|r(p ).ℓ
                                     (
                                                       if ℓ = 0, . . . , di − 1
                       θ|r(p ).ℓ =            i
                            i            π|r(p ).(ℓ+1) if i = di + 1, . . ., #t (pi ) − 1
                                               i


                                                                                                f
It is not difficult to prove that θ is a run of Aρ , and, moreover, since θ(ε) = qρ , it is an
accepting run, hence u ∈ L (Aρ ) ⊆ Ar (cf. line 14).
      Concerning the size of Ar , notice that |Ar | ≤ |A| + ∑ρ∈∆ |Aρ | where Aρ = hQρ , Σ, ∆ρ ,
    f
{qρ }i. We have that ||∆ρ || ≤ ||∆||, and for each rule τ ∈ ∆ρ \ ∆ created at lines 9, 11,
or 18, there exists a rule ν ∈ ∆ such that |τ| ≤ |ν| + 1. Moreover, ||∆ρ \ ∆|| ≤ ||Q|| since
we introduce a new rule for each state in the set visited ⊆ Q. Hence |Aρ | = |A| +
                                                             2          2
∑τ∈∆ρ \∆ |τ| ≤ |A| + |A| + ||Q|| ≤ 3|A|. Hence |Ar | ≤ 3|A| = O (|A| ).                      ⊓
                                                                                             ⊔

                                                        27
   The main result of this paper is given by the following theorem. The entailment
problem for inductive systems is reduced, in polynomial time, to a language inclusion
problem for tree automata. The inclusion test is sound (if the answer is yes, the entail-
ment holds), and moreover, complete assuming that both systems are local.
                                                n
Theorem 1. Let P = Pi ≡ |mj=1
                                      i
                                          Ri, j i=1 be a system of inductive definitions. Then, for
any two predicates Pi (xi,1 , . . . , xi,ni ) and Pj (x j,1 , . . . , x j,n j ) of P such that ni = n j and for
any variables α = {α1 , . . . , αni } not used in P , the following holds:
  – [Soundness] Pi (α) |=P Pj (α) if L (A1 ) ⊆ L (Ar2 ),
  – [Completness] Pi (α) |=P Pj (α) only if L (A1 ) ⊆ L (Ar2 ) provided that the rooted
    systems hP , Pi i and hP , Pj i are both local
where A1 = SL 2 TA(P , i, α) and A2 = SL 2 TA(P , j, α).
Proof (Soundness). Let S be a state such that S |= Pi (α). By Lemma 6, there exists
a tree t ∈ L (A1 ) such that S |= Φ(t). Since t ∈ L (A1 ) ⊆ L (Ar2 ), by Lemma 7, there exists
a quasi-canonical tree u ∈ L (A2 ) such that t ∼qc u. By Lemma 5, we have S |= Φ(u),
and by Lemma 6 again, we obtain S |= Pj (α). Hence Pi (α) |=P Pj (α).
     [Completness] If hP , Pi i and hP , Pj i are local rooted systems, it follows that A1 and
A2 recognize only normal canonical trees. Let t ∈ L (A1 ) be a normal canonical tree. It is
not difficult to see that starting from t, one can build a state S and its spanning tree such
that the right-hand side of Lemma 3 holds. Then, by Lemma 3, one gets that S |= Φ(t).
By Lemma 6, we have S |= Pi (α), and since Pi (α) |=P Pj (α), we have S |= Pj (α).
By Lemma 6 again, we obtain a canonical tree u ∈ L (A2 ) such that S |= Φ(u). Since
S |= Φ(t) and S |= Φ(u), by Lemma 4, we have t ∼c u, and since t is normal, we obtain
t ∈ L (Ar2 ), by Lemma 7. Hence L (A1 ) ⊆ L (Ar2 ).                                          ⊓
                                                                                             ⊔
Example 9 (cont. of Ex. 8). The automaton Ar corresponding to the rotation closure of
                                        2 , q f in }, ∆, {q1 , q f in }i where:
the automaton A is Ar = hΣ, {q1 , q2 , qrev
                                        /
                ha 7→ (b, d) ∧ a = c, 0i()    → q1 ha 7→ (x, b), 0,  / (x, a)i(q2 ) → q1 
                                                                                          
              
                                                                                          
                h∃hd ′ .hd ′ 7→ (d, p) ∧ hd = c ∧ hd ′ = hd, (hd, p)i()             → q2 
              
                                                                                          
              
                                                                                          
                                                                                           
               h∃hd ′ .hd ′ 7→ (x, p) ∧ hd ′ = hd, (hd, p), (x, hd)i(q )
              
                                                                                    → q2 
                                                                                           
              
                                                                       2                  
                                                                                           
           ∆ = h∃hd .hd 7→ (d, p) ∧ hd = c ∧ hd = hd, 0,
                     ′     ′                          ′        / (p, hd)i(q2 ) → q f in
                                                                            rev

                ha 7→ (x, b), (a, x)i()                                             → qrev
              
                                                                                          
                                                                                           
                                                                                       2 
              
                                                                                          
                     ′     ′                ′                           rev            rev
                                                                                          
               h∃hd .hd 7→ (x, p) ∧ hd = hd, (hd, x), (p, hd)i(q2 )                → q2 
              
                                                                                          
                                                                                          
                h∃hd .hd 7→ (x, p) ∧ hd = hd, 0,    / (x, hd), (p, hd)i(q2 , q2 ) → q f in
                                                                                           
                    ′     ′                ′                                 rev          


5 Complexity
In this section, we prove tight complexity bounds for the entailment problem in the
fragment of SL with inductive definitions under consideration (i.e. with the restrictions
defined in Sec. 2.4). The first result shows the need for connected rules in the system
as allowing unconnected rules leads to the undecidability of the entailment problem.
As a remark, the general undecidability of entailments for SL with inductive definitions
has already been proved in [1]. In addition to their result, our proof stresses the fact that
undecidability occurs due the lack of connectivity within some rules.
Theorem 2. The entailment problem Pi |=P Pj , for some 1 ≤ i, j ≤ n, is undecidable
for inductive systems P = {Pi ≡ |mj=1
                                   i
                                      Ri, j }ni=1 that can have unconnected rules.
                                                     28
Proof. A context-free grammar is a tuple G = hX , Σ, δi where X is a finite nonempty
set of nonterminals, Σ is a finite nonempty alphabet such that X ∩ Σ = 0,         / and δ ⊆
X × (Σ ∪ X )∗ is a finite set of productions. Given two strings u, v ∈ (Σ ∪ X )∗ , we define
a step u =⇒G v if there exists a production (X, w) ∈ δ and some words y, z ∈ (Σ ∪ X )∗
such that u = yXz and v = ywz. We denote by =⇒∗G the reflexive and transitive closure
of the =⇒G relation. The language of a grammar G generated by a nonterminal X ∈ X
is defined as LX (G) = {w ∈ Σ∗ | X =⇒∗G w}. It is known that the inclusion problem
LX (G) ⊆ LY (G), for some nonterminals X,Y ∈ X , is undecidable as originally proved in
[2]. We reduce from this problem to entailment within unconnected inductive systems.
    Let Σ = {σ1 , . . . , σN } be the alphabet of G. We define the set of selectors

                                  Sel = {1, . . . , ⌈log2 N⌉ + 1}

and, for each alphabet symbol σK , we define a basic SL formula ϕK (x, y) ≡ x 7→ (β, y)
where, for all 0 ≤ i < ⌈log2 N⌉:
                 
                    x if 1 occurs on position i in the binary encoding of K
            βi =
                    nil if 0 occurs on position i in the binary encoding of K

A word w = σi1 · . . . · σin ∈ Σ∗ is encoded by the formula

                   ϕw (x, y) ≡ ∃x1 . . . ∃xn−1 . ϕi1 (x, x1 ) ∗ . . . ϕin (xn−1 , y).

We define a predicate name PX (x, y) for each nonterminal X ∈ X , and for each pro-
duction π ≡ (X, w1 · Xi1 · . . . · wn · Xin · wn+1 ) ∈ δ where w1 , . . . , wn ∈ Σ∗ are words and
Xi1 , . . . , Xin ∈ X are non-terminals, we have the rule:

      Rπ (x, y) ≡ ∃x1 . . . ∃x2n . ϕw1 (x, x1 ) ∗ PXi1 (x1 , x2 ) ∗ . . .∗
                                   ϕwn (x2n−2 , x2n−1 ) ∗ PXin (x2n−1 , x2n ) ∗ ϕwn+1 (x2n , y).

Finally, each predicate is defined as PX ≡ |(X,w)∈δ R(X,w) , and the inductive system is
PG = {PX | X ∈ X }. It is immediate to check that PX (x, y) |=PG PY (x, y) if and only if
LX (G) ⊆ LY (G).                                                                                   ⊓
                                                                                                   ⊔
    The second result of this section provides tight complexity bounds for the entailment
problem for connected systems with the restrictions defined in Sec. 2.4. We must point
out that EXPTIME-hardness of entailments in the fragment of [13] was already proved
in [1]. The result below is stronger as the fragment under consideration is a restriction of
the fragment from [13]. In particular, we do not allow branching parameter copying and
do not consider checking entailments between formulae with empty spatial heads like,
e.g., ∃z . DLL(x, z) ∗ DLL(z, y) |= DLL(x, y). On the other hand, these restrictions allow us
to set an EXPTIME upper bound on the entailment problem for connected systems.
Theorem 3. The entailment problem Pi |=P Pj , for some 1 ≤ i, j ≤ n, is EXPTIME-
complete for connected inductive systems P = {Pi ≡ |mj=1
                                                      i
                                                         Ri, j }ni=1 .
Proof. We reduce from and to the inclusion problem for non-deterministic (bottom-up)
tree automata. It is known that the language inclusion problem for non-deterministic
tree automata is EXPTIME-complete (see, e.g. Corollary 1.7.9 in [8]).

                                                  29
    For the hardness part, let A1 = hQ1 , Σ, ∆1 , F1 i and A2 = hQ2 , Σ, ∆2 , F2 i be two tree
automata over the same alphabet Σ = {σ1 , . . . , σN }. We assume w.l.o.g. that Q1 ∩ Q2 =
/ We define the set of selectors
0.

                        Sel = {1, . . . , ⌈log2 N⌉ + max{#(σ) | σ ∈ Σ}}.

For each alphabet symbol σK , 1 ≤ K ≤ N and each rule ρ ≡ (σK (q1 , . . . , qn ) −             → q) ∈
                                          ρ
∆1 ∪ ∆2 , we define a basic SL formula ϕK (x, y1 , . . . , yn ) ≡ x 7→ (β, y1 , . . . , yn ) where, for
all 0 ≤ i < ⌈log2 N⌉:
                  
                    x if 1 occurs on position i in the binary encoding of K
             βi =
                    nil if 0 occurs on position i in the binary encoding of K

    For each state q ∈ Qi of Ai , we consider a predicate name Pq (x) and an extra predi-
cate name Pi (x), for both i = 1, 2. For each transition rule ρ ≡ (σK (q1 , . . . , qn ) −
                                                                                         → q), of
either A1 or A2 , we define the following connected inductive rule:
                                             ρ
               Rρ (x) ≡ ∃y1 . . . ∃yn . ϕK (x, y1 , . . . , yn ) ∗ Pq1 (y1 ) ∗ . . . ∗ Pqn (yn )

Then we define the predicates:

                                             → q) ∈ ∆1 ∪ ∆2 }
             Pq = {Rq | (σ(q1 , . . . , qn ) −
                                             → q) ∈ ∆i and q ∈ Fi } for both i = 1, 2
             Pi = {Rq | (σ(q1 , . . . , qn ) −

                                                → q) ∈ ∆1 ∪ ∆2 } ∪ {P1, P2 }. It is easy to
Finally, we have P = {Pq | (σ(q1 , . . . , qn ) −
check that P1 (x) |=P P2 (x) if and only if L (A1 ) ⊆ L (A2 ). Hence the entailment problem
is EXPTIME-hard.
     For the EXPTIME-completness part, Theorem 1 shows that any entailment problem
Pi |=P Pj , for a connected system P , can be reduced, in polynomial time, to a language
inclusion problem between tree automata L (APi ) ⊆ L (ArPj ). Hence the entailment prob-
lem is in EXPTIME.                                                                        ⊓
                                                                                          ⊔


6 Experiments
We implemented a prototype tool [12] that takes as input two rooted inductive sys-
tems hPlhs , Plhs i and hPrhs , Prhs i with eliminated parameters (i.e. the result of Alg. 2).
Table 1 lists the entailment queries on which we tried out our tool. The upper part of
the table contains local inductive systems whereas the bottom part contains non-local
systems. Apart from the DLL and TLL predicates from Sect. 2.4, the considered entail-
ment queries contain the following predicates : DLLrev that encodes a DLL from the
end, TREE pp encoding trees with parent pointers, TREErev   pp that encodes trees with par-
ent pointers starting from an arbitrary leaf, TLL pp encoding TLLs with parent pointers,
and TLLrev
         pp which encodes TLLs with parent pointers starting from their left most leaf.
These predicates are defined in Fig. 6. Columns |Alhs |, |Arhs |, and |Arrhs | of Table 1 pro-
vide information about the number of states and transitions of the respective automata.
The tool answered all queries correctly (despite the incompleteness for non-local sys-
tems), and the running times were all under 1 sec. on a standard PC (Intel Core2 CPU,
3GHz, 4GB RAM).

                                                     30
Table 1. Experimental results. The upper table contains local systems, while the lower table non-
local ones. Sizes of initial TA (col. 3,4) and rotated TA (col. 5) are in numbers of states/transitions
                            Entailment LHS |= RHS                             Answer |Alhs | |Arhs | |Arrhs |
                   DLL(a,nil,c,nil) |= DLLrev (a,nil,c,nil)                    True   2/4 2/4 5/8
                   DLLrev (a,nil,c,nil) |= DLL(a,nil,c,nil)                    True   2/4 2/4 5/8
                   DLLmid (a,nil,c,nil) |= DLL(a,nil,c,nil)                    True   4/8 2/4 5/8
                   DLL(a,nil,c,nil) |= DLLmid (a,nil,c,nil)                    True   2/4 4/8 12/18
 ∃x,n,b. x 7→ (n,b) ∗ DLL rev (a,nil,b,x) ∗ DLL(n,x,c,nil) |= DLL(a,nil,c,nil) True   3/5 2/4 5/8
 DLL(a,nil,c,nil) |= ∃x,n,b. x 7→ (n,b) ∗ DLLrev (a,nil,b,x) ∗ DLL(n,x,c,nil) False   2/4 3/5 9/13
     ∃y,a. x 7→ (y,nil) ∗ y 7→ (a,x) ∗ DLL(a,y,c,nil) |= DLL(x,nil,c,nil)      True   3/4 2/4 5/8
     DLL(x,nil,c,nil) |= ∃y,a. x 7→ (nil,y) ∗ y 7→ (a,x) ∗ DLL(a,y,c,nil)      False  2/4 3/4 8/10
                       TREE pp (a,nil) |= TREErev
                                                pp (a,nil)                     True   2/4 3/8 6/11
                       TREErevpp (a,nil) |= TREE pp (a,nil)                    True   3/8 2/4 5/10
                  TLL pp (a,nil,c,nil) |= TLLrev
                                               pp (a,nil,c,nil)                True   4/8 5/10 16/26
                  TLLrev
                       pp (a,nil,c,nil) |= TLL pp (a,nil,c,nil)                True 5/10 4/8 13/22
    ∃l,r,z. a 7→ (l,r,nil,nil) ∗ TLL(l,c,z) ∗ TLL(r,z,nil) |= TLL(a,c,nil)     True   4/7 4/8 13/22
    TLL(a,c,nil) |= ∃l,r,z. a 7→ (l,r,nil,nil) ∗ TLL(l,c,z) ∗ TLL(r,z,nil)     False  4/8 4/7 13/21


    DLLrev (hd, p,tl, n) ≡ hd 7→ (n, p) ∧ hd = tl | ∃x. tl 7→ (n, x) ∗ DLLrev (hd, p, x,tl)
    DLLmid (hd, p,tl, n) ≡ hd 7→ (n, p) ∧ hd = tl | hd 7→ (tl, p) ∗ tl 7→ (n, hd)
                             | ∃x, y, z. x 7→ (y, z) ∗ DLL(y, x,tl, n) ∗ DLL rev (hd, p, z, x)
           TREE pp (x, b) ≡ x 7→ (nil, nil, b) | ∃l, r. x 7→ (l, r, b) ∗ TREE pp (l, x) ∗ TREE pp (r, x)
           TREErev                                                                         aux
                   pp (t, b) ≡ t 7→ (nil, nil, b) | ∃x, up.x 7→ (nil, nil, up) ∗ TREE pp (t, b, up, x)
            aux
     TREE pp (t, b, x, d) ≡ ∃r.x 7→ (d, r, b) ∗ TREE pp (r, x) ∧ x = t
                             | ∃l.x 7→ (l, d, b) ∗ TREE pp (l, x) ∧ x = t
                             | ∃r, up.x 7→ (d, r, up) ∗ TREE auxpp (t, b, up, x) ∗ TREE pp (r, x)
                             | ∃l, up.x 7→ (l, d, up) ∗ TREEaux  pp (t, b, up, x) ∗ TREE pp (l, x)
      TLL pp (r, p, ll, lr) ≡ r 7→ (nil, nil, p, lr) ∧ r = ll
                             | ∃x, y, z. r 7→ (x, y, p, nil) ∗ TLL pp (x, r, ll, z) ∗ TLL pp (y, r, z, lr)
     TLLrevpp (t, p, ll, lr) ≡ ll 7→ (nil, nil, p, lr) ∧ ll = t
                             | ∃up, z.ll 7→ (nil, nil, up, z) ∗ TLLauxpp (t, p, up, ll, z, lr)
  TLLaux
     pp  (t, p, x, d, z, lr) ≡ ∃r.x 7→ (d, r, p, nil) ∗ TLL pp (r, x, z, lr) ∧ x = t
                             | ∃r, up, q.x 7→ (d, r, up, nil) ∗ TLL aux
                                                                      pp (t, p, up, x, q, lr) ∗ TLL pp (r, x, z, q)

                    Fig. 6. Inductive definitions of predicates used in experiments.


    For each experiment, we first replaced each left/right-hand side of an entailment
query containing a points-to predicate by a new top-level predicate and then performed
the parameter elimination. We have not yet implemented this step, but we tightly fol-
lowed Alg. 2. Subsequently, we have applied our tool. Column Answer of Table 1 shows
the results given by the tool. The answers provided by the tool are all correct despite
the incompleteness of the approach for non-local systems. The experiments show that
our approach is indeed capable of handling quite complex predicates, including the
possibility of encoding the same data structures starting from different entry points.
Moreover, the approach is also rather efficient: columns |Alhs |, |Arhs |, and |Arrhs | provide
information about the number of states and transitions of the respective automata. Note
that no reduction technique was applied to reduce the size of Arrhs .

7 Conclusion
We have presented a novel automata-theoretic decision procedure for the entailment
problem of a non-trivial subset of SL with inductive predicates. Our reduction to TA can
                                                        31
deal with the problem that the same recursive structure may be represented differently
when viewed from different entry points. To deal with this problem, our procedure
uses a special closure operation which closes a given TA representation with respect to
all rotations of its spanning trees. Our procedure is sound and complete for recursive
structures in which all edges are local with respect to a spanning tree. For this case,
using our reduction, we show that the entailment problem is EXPTIME-complete. For
structures outside of this class, our procedures is incomplete but still sound. We have
implemented our approach in a prototype tool which we tested through a number of
non-trivial experiments. In the experiments, the incompleteness of our approach has
never showed up. Moreover, the experiments also showed that our approach is quite
efficient. In the future, we plan to improve the implementation, extend the experiments,
as well as to integrate our decision procedure into some verification tool dealing with
programs with dynamic linked structures.


References
 1. Antonopoulos, T., Gorogiannis, N., Haase, C., Kanovich, M., Ouaknine, J.: Foundations for
    decision problems in separation logic with general inductive predicates. In: To appear in
    Proc. of FOSSACS’14 (2014)
 2. Bar-Hillel, Y., Perles, M., Shamir, E.: On formal properties of simple phrase structure gram-
    mars. Zeitschrift fr Phonetik, Sprachwissenschaft und Kommunikationsforschung 14(2),
    143–172 (1961)
 3. Berdine, J., Calcagno, C., Cook, B., Distefano, D., O’Hearn, P., Wies, T., Yang, H.: Shape
    analysis for composite data structures. In: Proc. CAV’07. LNCS, vol. 4590. Springer (2007)
 4. Berdine, J., Calcagno, C., O’Hearn, P.W.: A decidable fragment of separation logic. In: Proc.
    of FSTTCS’04. LNCS, vol. 3328. Springer (2004)
 5. Bouajjani, A., Habermehl, P., Holik, L., Touili, T., Vojnar, T.: Antichain-based universality
    and inclusion testing over nondeterministic finite tree automata. In: Proc. of CIAA. LNCS,
    vol. 5148. Springer (2008)
 6. Brotherston, J., Kanovich, M.: Undecidability of propositional separation logic and its neigh-
    bours. In: Proceedings of the 2010 25th Annual IEEE Symposium on Logic in Computer
    Science. pp. 130–139. LICS ’10 (2010)
 7. Calcagno, C., Distefano, D.: Infer: An automatic program verifier for memory safety of c
    programs. In: Proc. of NASA Formal Methods’11. LNCS, vol. 6617. Springer (2011)
 8. Comon, H., Dauchet, M., Gilleron, R., Jacquemard, F., Lugiez, D., Tison, S., Tommasi, M.:
    Tree Automata Techniques and Applications (2005),
    URL: http://www.grappa.univ-lille3.fr/tata
 9. Cook, B., Haase, C., Ouaknine, J., Parkinson, M.J., Worrell, J.: Tractable reasoning in a
    fragment of separation logic. In: Proc. of CONCUR’11. LNCS, vol. 6901. Springer (2011)
10. Dudka, K., Peringer, P., Vojnar, T.: Predator: A practical tool for checking manipulation
    of dynamic data structures using separation logic. In: Proc. of CAV’11. LNCS, vol. 6806.
    Springer (2011)
11. Enea, C., Saveluc, V., Sighireanu, M.: Compositional invariant checking for overlaid and
    nested linked lists. In: Proc. of ESOP’13. pp. 129–148 (2013)
12. Iosif, R., Rogalewicz, A., Vojnar, T.: Slide: Separation logic with inductive definitions,
    URL: http://www.fit.vutbr.cz/research/groups/verifit/tools/slide/
13. Iosif, R., Rogalewicz, A., Simacek, J.: The tree width of separation logic with recursive
    definitions. In: Proc. of CADE-24. LNCS, vol. 7898. Springer (2013)


                                               32
14. Lengal, O., Simacek, J., Vojnar, T.: Vata: a tree automata library,
    URL: http://www.fit.vutbr.cz/research/groups/verifit/tools/libvata/
15. Nguyen, H.H., Chin, W.N.: Enhancing program verification with lemmas. In: Proc of
    CAV’08. LNCS, vol. 5123. Springer (2008)
16. Piskac, R., Wies, T., Zufferey, D.: Automating separation logic using smt. In: Proc. of
    CAV’13. LNCS, vol. 8044 (2013)
17. Reynolds, J.: Separation Logic: A Logic for Shared Mutable Data Structures. In: Proc. of
    LICS’02. IEEE CS Press (2002)




                                            33
Algorithm 2 Elimination of propagated formal parameters
  input A rooted system hP , Pi i, where P = {Pi (xi,1 , . . . , xi,ni ) ≡ |mj=1
                                                                              i
                                                                                 Ri, j }ni=1 , and Pi (x)
  output A rooted system hQ , Qi i, where Qi has empty formal parameter tuple
  global Q ← P , Visited ← 0,   / Parameters ← 0,  / Tracked
 1: function ELIMINATE PARAMETERS(Pi, α)                                ⊲ α is the tuple of actual parameters
 2:    for all k = 1, . . . , ni do                                     ⊲ iterate through all parameters of Pi
 3:        Tracked ← αk
 4:        TRACK E LIMINATE(Pi , xi,k , true)
 5:        Parameters ← Parameters ∪ {Tracked}
 6:    return T RIM(Q , Pi )
 1: function TRACK E LIMINATE (Pr, xr,s , del)                      ⊲ parameter xr,s of Pr , boolean del
 2:    xnew ← if del then x¬xr,s else x                      ⊲ initialize a new formal parameter tuple
 3:    Qr (xnew ) ← empty predicate
 4:    Q ← Q ∪ {Qr }                                                      ⊲ create a new predicate name
 5:    for all q = 1, . . . , mr do                                     ⊲ iterate through the rules of Pr
 6:        assume Rr,q (x) ≡ ∃z . α 7→ (y) ∗ Pi1 (u1 ) ∗ . . . ∗ Pim (um )
                                   S
 7:        if xr,s ≡ α or xr,s 6∈ mj=1 u j then            ⊲ xr,s is allocated in Rr,q or not propagated
 8:             Rnew (xnew ) ← Rr,q [Tracked/xr,s ]       ⊲ replace xr,s in Rr,q by the global Tracked
 9:        else             ⊲ check if the current tracked parameter xr,s is passed to P j on position ℓ
10:             if ∃ j, ℓ . 1 ≤ j ≤ m ∧ 0 ≤ ℓ < |y j | ∧ xr,s ≡ (u j )ℓ then
11:                  if the choice of j and ℓ is not unique then
12:                       error (“branching propagation for parameter xr,s ”)
13:                    if xr,s ∈ y then      ⊲ the tracked parameter is referenced before being passed
14:                         Rnew (xnew ) ← if del then ∃xr,s . Rr,q else Rr,q
15:                         del ← false
16:                    else                 ⊲ the tracked parameter is passed without being referenced
17:                         if del then
18:                             Rnew (xnew ) ← ∃z . α 7→ (y) ∗ Pi1 (u1 ) ∗ . . . ∗ Qi j (u¬xr,s ) ∗ . . . ∗ Pim (um )
19:                         else
20:                             Rnew (xnew ) ← Rr,q
21:                    if x j,ℓ 6∈ Visited then                ⊲ continue tracking parameter x j,ℓ of P j
22:                         Visited ← Visited ∪ {x j,ℓ }
23:                         TRACK E LIMINATE (Pj, x j,ℓ , del)
24:           Qr ≡ Qr | Rnew




                                                        34
Algorithm 3 Signature computation
  input A rooted system hP , Pi i, where P = {Pi ≡ |mj=1
                                                      i
                                                         Ri, j }ni=1
               fw               eq          fw              eq
  global sig1 , sigbw                                bw
                       1 , sig1 , . . . , sign , sign , sign
 1: function FW E DGE (index, predno , P )
 2:    for all i = 1, . . . , n do                                          ⊲ iterate through all predicates
 3:        for all j = 1, . . . , mi do                                           ⊲ iterate through all rules
 4:             assume Ri, j (x) ≡ ∃z . α 7→ y ∗ Pi0 (x0 ) ∗ . . . ∗ Pik (xk ) ∧ Π
 5:             res ← true
 6:             for all ℓ = 0, . . . , k do                  ⊲ iterate through all predicate occurrences
 7:                 if iℓ = predno then
 8:                       if (xℓ )index 6∈ y then ⊲ parameter not referenced in occurrence of Ppredno
 9:                             res ← false
10:    return res
 1: function BW E DGE (index, predno , P )
 2:    for all i = 1, . . . , n do                                          ⊲ iterate through all predicates
 3:        for all j = 1, . . . , mi do                                           ⊲ iterate through all rules
 4:             assume Ri, j (x) ≡ ∃z . α 7→ y ∗ Pi0 (x0 ) ∗ . . . ∗ Pik (xk ) ∧ Π
 5:             res ← true
 6:             for all ℓ = 0, . . . , k do                  ⊲ iterate through all predicate occurrences
 7:                 if iℓ = predno then
 8:                       if (xℓ )index 6=Π α then ⊲ parameter not allocated in occurrence of Ppredno
 9:                             res ← false
10:    return res
 1: function ALLOCATED(index,predno ,P )
 2:    res ← true
 3:    for all j = 1, . . . , mpredno do                             ⊲ iterate through all rules of Ppredno
 4:        assume Rpredno , j (x) ≡ ∃z . α 7→ y ∗ Pi0 (x0 ) ∗ . . . ∗ Pik (xk ) ∧ Π
 5:        if (x)index 6=Π α then                    ⊲ formal parameter index not allocated in Ppredno
 6:             res ← false
 7:    return res
 1: function REFERENCED(index,predno ,P )
 2:    res ← true
 3:    for all j = 1, . . . , mpredno do                             ⊲ iterate through all rules of Ppredno
 4:        assume Rpredno , j (x) ≡ ∃z . α 7→ y ∗ Pi0 (x0 ) ∗ . . . ∗ Pik (xk ) ∧ Π
 5:        if (x)index 6∈ y then                   ⊲ formal parameter index not referenced in Ppredno
 6:             res ← false
 7:    return res
 1: function COMPUTE S IGNATURES(P )
 2:    for all i = 1, . . . , n do                                   ⊲ iterate through all predicates of P
 3:        assume Pi (x)                                                       ⊲ Pi has formal parameters x
 4:        for all p = 0, . . . , |x| − 1 do               ⊲ iterate through all formal parameters of Pi
                     fw
 5:             sigi ← 0,      / sigbw
                                     i ← 0,  / sigeq
                                                  i ←0   /
 6:             if FW E DGE(i, p, P ) and ALLOCATED(i, p, P ) then
                           fw           fw
 7:                 sigi ← sigi ∪ {p}
 8:             else
 9:                 if BW E DGE(i, p, P ) and REFERENCED(i, p, P ) then
10:                       sigbw            bw
                                i ← sigi ∪ {p}
11:                  else
                                eq         eq
12:                       sigi ← sigi ∪ {p}

                                                    35
Algorithm 4 Converting rooted inductive systems to tree automata
  input A rooted system hP , Pindex i, P = {Pi ≡ |mj=1
                                                    i
                                                       Ri, j }ni=1 , and actual parameters u of a call
  of Pindex
  output A tree automaton A = hΣ, Q, ∆, Fi
 1: function SL 2 TA(P , index, u)
 2:    P ← SPLIT S YSTEM(P )
 3:    P ← ELIMINATE PARAMETERS(Pindex , u)
 4:    COMPUTE S IGNATURES(P )
 5:    ∆ ← 0, / Σ ← 0/
 6:    for all i = 1, . . . , n do                                    ⊲ iterate through all predicates of P
 7:         for all j = 1, . . . , mi do                                     ⊲ iterate through all rules of Pi
 8:             assume Ri, j (x) ≡ ∃z . α 7→ β ∗ Pi0 (z0 ) ∗ . . . ∗ Pik (zk ) ∧ Π
 9:             φ ← if α ∈ Parameters then α 7→ (β) ∧ Π else ∃α′ . α′ 7→ (β) ∧ Π ∧ α = α′
                  fw                        eq
10:             x−1 ← hi, xbw    −1 ← hi, x−1 ← hi                                    ⊲ initialize input ports
11:             for all ℓ = 0, . . . , |x| − 1 do     ⊲ iterate through the formal parameters of Ri, j
                                   fw
12:                  if ℓ ∈ sigi then
                              fw      fw
13:                       x−1 ← x−1 · h(x)ℓ i
14:                   if ℓ ∈ sigbw
                                i then
15:                        xbw
                            −1 ← xbw
                                   −1 · h(x)ℓ i
                                 eq
16:                   if ℓ ∈ sigi then
                            eq    eq
17:                        x−1 ← x−1 · h(x)ℓ i
18:                              −1 , β)
                 SELECTOR S ORT(xbw
19:              for all ℓ = 0, . . . , k do               ⊲ iterate through predicate occurrences in Ri, j
                       fw                         eq
20:                  xℓ ← hi, xbw   ℓ    ←   hi, xℓ  ←  hi                        ⊲ initialize output ports
21:                  for all r = 0, . . . , |zℓ | − 1 do ⊲ iterate through variables of occurrence Piℓ (zℓ )
                                        fw
22:                       if r ∈ sigiℓ then
                                fw         fw
23:                           xℓ ← xℓ · h(zℓ )r
24:                       if r ∈ sigbw
                                    iℓ then
25:                            xbw
                                ℓ  ←  xbw
                                       ℓ · h(zℓ )r i
                                      eq
26:                       if r ∈ sigiℓ then
                                eq     eq
27:                            xℓ ← xℓ · h(zℓ )r i
                                      fw
28:                   SELECTOR S ORT(xℓ , β)
29:             T ← hφ, x−1 , x0 , . . . , xk i                                          ⊲ create a new tile
30:             lhs ← hqi0 , . . . , qik i        ⊲ create the left hand side of the transition rule for Ri, j
31:             (Tnew , lhsnew ) ← SORT T ILE(T, lhs)
32:             Σ ← Σ ∪ {Tnew }                                     ⊲ insert normalized tile in the alphabet
33:             Q ← Q ∪ {qi , qi0 , . . . , qik }
34:             ∆ ← ∆ ∪ {Tnew (lhsnew ) → qi }                    ⊲ build transition using normalized tile
35:      F = {qindex }
36:      return A = hQ, Σ, ∆, Fi




                                                       36
Algorithm 5 Rotation Closure of Quasi-canonical TA
  input A quasi-canonical tree automaton A = hQ, Σ, ∆, Fi
  output A tree automaton Ar , where L (Ar ) = {u : N∗ ⇀ f in T qc | ∃t ∈ L (A) . u ∼qc t}
 1: Ar = hQr , Σ, ∆r , Fr i ← A                                                 ⊲ make a copy of A into Ar
 2: for all ρ ∈ ∆ do                                                        ⊲ iterate through the rules of A
 3:     assume ρ ≡ T (q0 , . . . , qk ) → q and T ≡ hϕ, x−1 , x0 , . . . , xk i     ⊲ the chosen rule ρ will
    recognize the root of the rotated tree
 4:     if x−1 6= 0/ or q 6∈ F then
                               fw            eq
 5:         assume x−1 ≡ x−1 · xbw     −1 · x−1                                    ⊲ factorize the input port
 6:         if xbw
                −1  =
                    6  0/ then
 7:             Qrev ← {qrev | q ∈ Q}                  ⊲ states qrev label the unique reversed path in Ar
                                                  f
 8:             (Qρ , ∆ρ ) ← (Q ∪ Q ∪ {qρ }, ∆)
                                        rev                     ⊲ assuming Q ∩ Qrev = 0,    / qρf 6∈ Q ∪ Qrev
 9:              p ← POSITION O F(xbw     −1 , ϕ) ⊲ find new output port for x−1 based on selectors of ϕ
                                                           f w eq                                               fw
10:                            / x0 , . . . , x p , xbw
                    Tnew ← hϕ, 0,                    −1 · x−1 · x−1 , x p+1 , . . . , xk i   ⊲ swap xbw
                                                                                                      −1 with x−1
                                                                                     f
11:                 ∆ρ ← ∆ρ ∪ {Tnew (q0 , . . . , q p , q , q p+1 , . . . , qk ) −
                                                         rev                     → qρ }
12:                 (∆ρ , ) ← ROTATE RULE(q, ∆, ∆ρ , 0,       / F)              ⊲ continue building ∆ρ recursively
                                         f
13:                 Aρ ← hQρ , Σ, ∆ρ , {qρ }i            ⊲ Aρ recognizes trees whose roots are labeled by ρ
14:                  r      r
                    A ← A ∪ Aδ                                                            ⊲ incorporate Aδ into Ar
15: return Ar
 1: function ROTATE RULE (q, ∆, ∆new, visited, F)
 2:    visited ← visited ∪ {q}
 3:    for all (U(s0 , . . . , sℓ ) → s) ∈ ∆ do                                           ⊲ iterate through the rules of A
 4:        for all 0 ≤ j ≤ ℓ such that s j = q do                              ⊲ for all occurrences of q on the rhs
 5:             assume U = hϕ, x−1 , x0 , . . . , x j , . . . , xℓ i
                                      fw          eq
 6:             assume x j ≡ x j · xbw      j ·xj                                           ⊲ factorize the x j output port
 7:             if x−1 = 0/ and s ∈ F then                 ⊲ remove x j from output and place it as input port
                                           f w eq
 8:                 U ′ ← hϕ, xbw    j · x j · x j , x0 , . . . , x j−1 , x j+1 , . . . , xℓ i
 9:                 ∆new ← ∆new ∪ {U ′ (s0 , . . . , s j−1 , s j+1 , . . . , sℓ ) −    → qrev }
10:             else                                                                                   ⊲ swap x−1 with x j
                                  fw           eq
11:                 x−1 ≡ x−1 · xbw         ·
                                        −1 −1 x
12:                      −1 6= 0
                    if xbw         / then
13:                      ports ← hx0 , . . . , x j−1 , x j+1 , . . . , xℓ i
14:                      states ← (s0 , . . . , s j−1 , s j+1 , . . . , sℓ )
                                                                      f w eq
15:                       p ← INSERT O UT P ORT(xbw           −1 · x−1 · x−1 , ports, ϕ)
16:                                                    rev
                          INSERT L HS S TATE(s , states, p)
                                                    f w eq
17:                      Unew ← hϕ, xbw       j · x j · x j , portsi                                   ⊲ create rotated tile
18:                      ∆new ← ∆new ∪ {Unew (states) → qrev }                                        ⊲ create rotated rule
19:                      if s 6∈ visited then
20:                             (∆new , visited) ← ROTATE RULE(s, ∆, ∆new , visited, F)
21:     return (∆new , visited)




                                                             37
