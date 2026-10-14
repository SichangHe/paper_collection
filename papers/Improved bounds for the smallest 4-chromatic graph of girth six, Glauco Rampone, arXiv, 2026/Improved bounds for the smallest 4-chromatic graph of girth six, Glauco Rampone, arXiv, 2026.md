                                                                   Improved bounds for the smallest
                                                                     4-chromatic graph of girth six
                                                                                     Glauco Rampone
                                                                                     grampone@ethz.ch
arXiv:2608.23652v1 [math.CO] 24 Aug 2026




                                                                                        August 2026


                                                                                          Abstract
                                                    For integers k, g ≥ 3 let ng (k) denote the minimum order of a graph with chromatic
                                                number k and girth at least g. Exoo and Goedgebeur (DMTCS 2019) proved 26 ≤ n6 (4) ≤
                                                66, the upper bound being given by an explicit 66-vertex graph that has remained the smallest
                                                known 4-chromatic graph of girth 6. We improve both bounds to

                                                                                     29 ≤ n6 (4) ≤ 64.

                                                The upper bound is witnessed by an explicit 4-chromatic graph of girth 6 on 64 vertices with
                                                152 edges; it is vertex- and edge-critical, and its automorphism group is cyclic of order 8 and
                                                acts semiregularly. The lower bound is an exhaustive isomorph-free computation in the SAT
                                                modulo symmetries framework with co-certificate learning, driven by the edge-density bound
                                                of Liu and Postle for 4-critical graphs of girth five; it re-derives the bound n6 (4) ≥ 26 of
                                                Exoo and Goedgebeur by a disjoint method and is validated in both directions on the known
                                                values n4 (4) = 11 and n5 (4) = 21. We complement the bounds with structural obstructions:
                                                no smaller witness can be obtained from either known witness by local modifications; no
                                                4-chromatic Cayley graph of girth 6 exists on 54–63 vertices (for orders 59 and 61 no vertex-
                                                transitive witness exists at all); and no witness on at most 63 vertices admits a semiregular
                                                automorphism group with two or three vertex orbits, for any finite group. Every known
                                                witness of an ng (4) record with g ≥ 6 is a lift of a small base graph along a semiregular group
                                                action; the results above close the most symmetric part of that regime below 64 vertices. All
                                                claimed properties of the new graph are verified by independent programs and, in addition,
                                                formally certified in the Lean 4 proof assistant: the non-3-colourability is established inside
                                                Lean by a formally verified checker that re-validates a 219,532-node refutation certificate
                                                produced by an external search, with a machine-checked soundness theorem.

                                           Keywords: chromatic number, girth, critical graphs, Cayley graphs, voltage graphs, SAT mod-
                                           ulo symmetries, formal verification, Lean.
                                           MSC 2020: 05C15, 05C38, 05C25, 05C85, 68V20.


                                           1    Introduction
                                           A classical theorem of Erdős [1] states that there exist graphs of arbitrarily large girth and
                                           chromatic number; the proof is probabilistic, and explicit small witnesses are hard to find. Fol-
                                           lowing [3], for integers k, g ≥ 3 let ng (k) denote the minimum number of vertices of a graph with
                                           chromatic number k and girth at least g.


                                                                                               1
    For k = 4 the first two values are classical: n4 (4) = 11, attained by the Grötzsch graph [15],
and n5 (4) = 21, attained by exactly 18 graphs including the Brinkmann graph [2] (the value and
the count are due to Royle; see [3]). For girth 6, Exoo and Goedgebeur [3] proved

                                       26 ≤ n6 (4) ≤ 66,

where the lower bound rests on an exhaustive computation and the upper bound on an explicit
5-regular graph of order 66 with a semiregular automorphism with 6 orbits of length 11. To the
best of our knowledge no improvement of either bound has been published since. (The regular
variant of the problem, the minimum order of an r-regular graph of girth g and chromatic number
χ, has recently been studied in [4], where upper bounds on it are derived from explicit graphs
of girth g and chromatic number χ, so that smaller such graphs translate into smaller bounds
there.)
    We improve both bounds.

Theorem 1. There exists a graph on 64 vertices with girth exactly 6 and chromatic number 4.
Consequently n6 (4) ≤ 64.

Theorem 2. Every graph of girth at least 6 on at most 28 vertices is 3-colourable. Consequently
n6 (4) ≥ 29.

    Beyond the two theorems, the paper contributes structural obstructions and machine-checkable
evidence. Section 6 proves that no smaller witness can be obtained from G64 (or from the 66-
vertex graph of [3]) by local modifications, that no witness on 54–63 vertices can be a Cayley
graph (for orders 59 and 61, no vertex-transitive witness exists at all), and that no witness on
at most 63 vertices admits a semiregular automorphism group with two or three vertex orbits,
for any finite group. Since every known witness of an ng (4) record with g ≥ 6 is a lift of a small
base graph along a semiregular group action, these results close the most symmetric part of the
regime in which all such witnesses live. (The restriction to g ≥ 6 is necessary: the Grötzsch
graph, with automorphism group of order 10 on 11 vertices, admits no nontrivial semiregular
action.)
    Theorem 2 closes the orders 26, 27 and 28, which were beyond the reach of [3]. It is obtained
with the SAT modulo symmetries framework of Kirchweger and Szeider [10] together with co-
certificate learning [11], both used as distributed; our contribution is the encoding, in particular
a reduction to 4-critical graphs that lets the edge-density bound of Liu and Postle [9] enter as a
propositional constraint, together with the campaign and its audit trail. The change in cost is
worth recording: [3] spent about 2.5 CPU-years to reach 25 vertices, whereas the entire ladder
14 ≤ n ≤ 28 took about 113 hours on one core of a consumer machine.
    Finally, every claim about G64 is checked by several mutually independent programs and,
beyond that, certified in the Lean 4 proof assistant (Section 4). Verified certificate checkers are
well established; what we emphasize is the end result, unusual for records of this kind: a reader
can re-derive Theorem 1 mechanically in minutes, from a self-contained file whose only trusted
components are the Lean kernel and its compiled evaluator.
    The paper is organized as follows. Section 2 defines G64 and states its properties; Section 3
documents the search that found it; Section 4 describes the verification and the Lean certification;
Section 5 proves Theorem 2; Section 6 proves the obstructions. All code, data, logs and the Lean
formalization are available at https://github.com/glaucorampone/G64 and as ancillary files;
the graph itself is deposited in the House of Graphs [5].


                                                2
2      The graph
Let G64 be the graph with vertex set Z64 = {0, . . . , 63} whose edge set is the union of the orbits,
under the map v 7→ v + 8 (mod 64), of the 20 edges

                                                    {i, i + t mod 64}

for the pairs (i, t) listed in Table 1. Explicitly, the orbit of the pair (i, t) consists of the edges
{ {v, v + t mod 64} : v ≡ i (mod 8) }; orbits with t = 32 contain 4 distinct edges and all others
contain 8, for a total of 152 edges. The graph is drawn in Figure 1.

       (0, 15)   (0, 24)    (0, 49)      (0, 60)     (1, 5)         (1, 22)    (1, 38)      (1, 42)       (2, 10)   (2, 32)
       (2, 45)   (2, 52)    (3, 17)      (3, 32)     (3, 42)        (4, 8)     (5, 1)       (5, 41)       (5, 42)   (5, 57)

                  Table 1: Edge-orbit representatives (i, t) of G64 under v 7→ v + 8.


Proposition 3. The graph G64 is 4-connected (indeed κ = λ = δ = 4), has 64 vertices, 152
edges, 48 vertices of degree 5 and 16 of degree 4, and satisfies:

    (i) G64 contains no cycle of length 3, 4 or 5, and contains the 6-cycle (0, 40, 36, 44, 34, 15);
        hence its girth is exactly 6;

 (ii) G64 admits the proper 4-colouring listed in Table 2, and admits no proper 3-colouring; hence
      χ(G64 ) = 4;

(iii) G64 is vertex-critical and edge-critical: for every vertex v the graph G64 − v is 3-colourable,
      and for every edge e the graph G64 − e is 3-colourable;

 (iv) the independence number of G64 is 24;

    (v) Aut(G64 ) is cyclic of order 8, generated by the semiregular automorphism v 7→ v+8 mod 64;
        consequently G64 has 8 vertex orbits and 20 edge orbits.

    Theorem 1 follows from (i) and (ii). Item (iii) shows that G64 carries no smaller witness as
a subgraph, and item (iv) shows that non-3-colourability is not forced by a counting argument
(3·24 ≥ 64), which is one reason why short certificates of χ ≥ 4 are not immediate for this graph.
Item (v) records that the symmetry exploited by the search of Section 3 is the entire symmetry
of the graph, a point we return to in Section 6.

                           c = (0, 0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 0, 3, 0, 3, 3, 2, 1, 0, 0, 2, 1, 0, 2,
                                3, 2, 1, 2, 1, 1, 0, 3, 0, 1, 2, 2, 2, 1, 0, 2, 3, 1, 3, 2, 0, 3, 2, 3,
                                2, 3, 1, 3, 1, 1, 2, 2, 3, 0, 3, 0, 3, 1, 2, 3)

Table 2: A proper 4-colouring c of G64 (colour of vertex v at position v, v = 0, . . . , 63), as verified
in the Lean formalization.




                                                                3
                                                               63   0    1
                                                          62                  2
                                                     61                            3
                                                60                                      4
                                           59                                                5
                                      58                                                          6

                                 57                                                                    7

                            56                                                                              8

                       55                                                                                        9

                  54                                                                                                  10

             53                                                                                                            11


        52                                                                                                                      12


       51                                                                                                                        13


   50                                                                                                                                14


  49                                                                                                                                  15


  48                                                                                                                                  16


  47                                                                                                                                  17


   46                                                                                                                                18


       45                                                                                                                        19


        44                                                                                                                      20


             43                                                                                                            21

                  42                                                                                                  22

                       41                                                                                        23

                            40                                                                              24

                                 39                                                                    25

                                      38                                                          26
                                           37                                                27
                                                36                                      28
                                                     35                            29
                                                          34                  30
                                                               33   32   31



Figure 1: The graph G64 , drawn with vertex v at position v on a circle (vertex 0 at the top,
clockwise), so that each edge orbit of Table 1 appears as a chord pattern repeated under the
rotation v 7→ v + 8. Vertex shapes and shades encode the four colour classes of Table 2 (class
0: white circle, 1: light-grey square, 2: grey triangle, 3: black diamond); the bold cycle is the
6-cycle (0, 40, 36, 44, 34, 15) of Proposition 3(i). The figure is generated from record64.json by
gen_fig_g64.py.




                                                                    4
3    How the graph was found
The graph was found by a randomized search over graphs with a semiregular cyclic automor-
phism, in the spirit of the searches of [3], but sweeping a broader family of factorizations. For a
factorization n = rs, the search samples maximal sets of edge-orbits under v 7→ v + r (mod rs)
subject to girth ≥ 6 and to a cap on the degree of each vertex class, maintained incrementally:
by symmetry, adding an orbit creates a short cycle if and only if it creates one through the rep-
resentative edge, which is checked by a single bounded breadth-first search. Candidates that are
dense enough to be 4-chromatic (by the bound of Kostochka and Yancey [6], a 4-critical graph
has at least (5n − 2)/3 edges; the deposited code now uses the sharper girth-5 bound (5n + 2)/3
of Liu and Postle [9], which the candidate that produced G64 , with 152 edges, passes as well)
are filtered by randomized DSATUR and tabu 3-colouring heuristics, and survivors are decided
exactly by a backtracking solver and the SAT solver CaDiCaL [14]. The search family is the
one of [3]; what we add is a wider sweep of factorizations and the incremental girth test. We
document the search here so that the discovery is reproducible.
    The campaign that produced G64 consisted of sixteen buckets r × s with 54 ≤ rs ≤ 65. The
eighteen runs that terminated normally sampled 5 828 084 candidates in about 6.2 CPU-hours
and left 366 instances that resisted the heuristics, none of them a witness; G64 arose in the
factorization 64 = 8 × 8 and is the only witness the campaign ever produced. The search is
seeded, so the discovery reproduces from a cold start in under five minutes; the log of that run
and the tally above are deposited with the code.
    It is perhaps worth noting that the 66-vertex witness of [3] has s = 11 prime, while our
sweep covered composite values of s as well, and the new witness arose at the fully composite
factorization 64 = 8×8. Whether this regime is genuinely richer or the observation is an accident
of a single sample, we cannot say.


4    Verification
None of the claims of Section 2 need be taken on trust: each is decided by more than one program,
and Theorem 1 is in addition reduced to the kernel of a proof assistant.
    All properties in Proposition 3 were verified by independent computations: girth by di-
rect enumeration of paths and common neighbourhoods; non-3-colourability both by an exact
forward-checking backtracking solver and by CaDiCaL (unsatisfiability of the standard colouring
encoding); criticality by 64 + 152 further exact colourability checks; the independence number
by branch and bound.
    In addition, Theorem 1 is formally certified in the Lean 4 proof assistant [19], in a self-
contained file using only the Lean core library. The formalization states and proves, for the
concrete adjacency structure of G64 : (a) there is no cycle of length 3, 4 or 5 (and the explicit
6-cycle exists); (b) the colouring of Table 2 is proper; (c) no proper 3-colouring exists. For (c),
a direct verified exhaustive search in the style of a static-order backtracking is not feasible (we
measured static search trees exceeding 2 · 108 nodes over hundreds of vertex orderings), so the
formalization instead uses a refutation certificate: the branching tree of an external forward-
checking solver (219,532 internal nodes: 209,002 MRV branching nodes plus 10,530 domain-
wipeout nodes; serialized to 1.76 million tokens) is re-traversed inside Lean by a certificate
checker, and a machine-checked soundness theorem (proved by structural induction, using no
evaluation axioms) states that acceptance of any certificate implies that no proper 3-colouring


                                                5
exists. The certificate itself is untrusted data: a corrupted certificate would simply be rejected
by the checker. Beyond the kernel, the only trusted component is Lean’s compiled evaluation
mechanism (native_decide), used to run the checker and the finite girth and colouring checks;
each of these evaluations is corroborated by the independent computations above.
    The Lean sources, the certificate, the adjacency data (including a graph6 string) and the
search code are available as ancillary files. The graph is also deposited in the House of Graphs
[5] as graph 57236 (https://houseofgraphs.org/graphs/57236), where its invariants (girth,
chromatic number, connectivity and automorphism group size among them) were recomputed
by an independent implementation.


5    An improved lower bound: n6 (4) ≥ 29
The lower bound n6 (4) ≥ 26 of [3] was obtained by generating, with a girth-pruned extension of
geng, all graphs with minimum degree 3, maximum degree at most 6 and girth at least 6 on 19–25
vertices (≈ 2.5 CPU-years) and 3-colouring them all, combined with a separate argument showing
that a 4-vertex-critical graph of girth at least 6 with maximum degree at least 7 must have at
least 26 vertices. We extend the exhaustion to 28 vertices with a different and substantially
faster method.
    Reduction to 4-critical graphs. Suppose some graph of girth ≥ 6 on at most 28 vertices is
not 3-colourable. Take a subgraph H that is edge-minimal subject to having chromatic number
≥ 4, and delete its isolated vertices. The result is 4-critical: its chromatic number is exactly
4 (deleting an edge lowers the chromatic number by at most one), deleting any edge leaves a
3-colourable graph by edge-minimality, and deleting any vertex v does too, since v is incident to
some edge e and H − v is a subgraph of H − e. It still has girth ≥ 6 and some order n′ ≤ 28.
Every 4-critical graph has minimum degree ≥ 3, and, being of girth ≥ 5, has at least (5n′ + 2)/3
edges by the bound of Liu and Postle [9]. Moreover n′ ≥ 14: in a graph of minimum degree
3 and girth 6, the balls of radius 2 around the two endpoints of any edge are disjoint trees, so
n′ ≥ 2(1 + 2 + 4) = 14 (the (3, 6)-cage is the Heawood graph). It therefore suffices to show that
for each 14 ≤ n ≤ 28 there is no graph on n vertices with girth ≥ 6, chromatic number ≥ 4,
minimum degree ≥ 3 and at least ⌈(5n + 2)/3⌉ edges. Note that, unlike in [3], no upper bound
on the maximum degree is imposed.
    Method. For each n we ran an exhaustive isomorph-free search in the SAT modulo sym-
metries (SMS) framework of Kirchweger and Szeider [10]: a CDCL SAT solver (CaDiCaL [14])
equipped with a propagator that prunes partial adjacency matrices which cannot extend to lexi-
cographically minimal representatives of their isomorphism classes. Girth, minimum degree and
edge-count constraints are encoded propositionally; the co-NP condition “no proper 3-colouring
exists” is handled by co-certificate learning [11]: each time the solver proposes a graph, a second
solver searches for a proper 3-colouring, and any colouring found is added as a clause excluding
every graph coloured by it. The minimality check was run with a recursion cutoff, which can
only weaken the symmetry breaking; this is sound for nonexistence results (at worst, more than
one representative per isomorphism class is explored). Concretely, when the cutoff is reached
the checker increments a counter and returns without emitting a symmetry-breaking clause, so
the graph is left in the search space: the explored space is a superset of a set of canonical rep-
resentatives, and exhausting a superset without a model implies that no model exists. Over
the whole ladder the cutoff was reached exactly once, at n = 28, in 1 of the 44,418,587 calls to
the minimality checker at that order; the solver’s own statistics record this and are reproduced


                                                6
in the deposited output. It would affect an exact-count claim, which we do not make, but not
Theorem 2.
    What is ours. The framework, the minimality propagator and the co-certificate learning
mechanism are due to [10, 11] and were used as distributed. Our contribution to Theorem 2 is
the encoding above (in particular the reduction to 4-critical graphs, which lets the Liu–Postle
density bound enter as a propositional edge-count constraint and dispenses with any cap on the
maximum degree), together with the campaign and the audit trail described below.
    Result. For every 14 ≤ n ≤ 28 the search terminates with an empty enumeration. This
establishes Theorem 2. The exploratory ladder 14 ≤ n ≤ 26 ran on a single consumer laptop
(WSL, one core per instance) in under three hours in total; the figures quoted here are instead
those of the audited rerun, in which every order was executed on one core of an Apple M4 under
one pinned toolchain, so that the per-order costs are mutually comparable. The two new orders
dominate the cost: n = 27 took 37,533 seconds of solver time and n = 28 took 361,682 seconds,
just over four days. The per-order cost is collected in Table 3.

                     n                  24     25      26        27        28
                     solver time (s)   286   1,598   6,485   37,533   361,682

Table 3: Solver time per order on one core of an Apple M4, from the audited rerun; each order
costs between four and ten times the previous one, the ratio rising to 9.6 at the last step. For
scale, the enumeration of [3] required about 2.5 CPU-years to cover the orders 19–25. The two
computations are not strictly comparable ([3] enumerate all graphs of girth ≥ 6 with minimum
degree 3 and maximum degree at most 6, whereas the search here is confined to the denser
4-critical candidates and imposes no degree cap), but the difference in scale is what allows the
exhaustion to be pushed three orders further on consumer hardware.

    Validation. The identical pipeline was checked in both directions against known values. In
the nonexistence direction, the runs for 14 ≤ n ≤ 25 re-derive the bound n6 (4) ≥ 26 of [3]
by a disjoint method. In the existence direction: with girth constraint 4 (triangle-free) the
pipeline enumerates on 11 vertices exactly one 4-chromatic graph (the Grötzsch graph, whose
uniqueness is Chvátal’s theorem [15]) and none on 10, a setting already used as a benchmark
for co-certificate learning in [11], whose Table 1 covers triangle-free non-3-colourable graphs
on 10–14 vertices; with girth constraint 5 it finds on 21 vertices a 4-chromatic graph of girth 5
within 39 seconds (consistent with n5 (4) = 21), whose girth and non-3-colourability we re-verified
independently by breadth-first search and exhaustive backtracking. The encodings themselves
are validated by an ancillary harness that regenerates each deposited CNF from the recorded
encoder command (checking it byte-identical to the deposited SHA-256 hash), fixes complete
edge-variable assignments of candidate graphs, and checks that satisfiability always coincides
with a direct combinatorial evaluation of the encoded predicate; models of free solves are likewise
decoded and re-checked. Finally, the whole ladder 14 ≤ n ≤ 26 was rerun in audited form on
a second machine and operating system, and the two new orders n = 27 and n = 28 were run
there in audited form as well, with the solver’s own exit code recorded verbatim at every level
and its full output deposited alongside hashes of the pinned toolchain.

Remark 4. Unlike Theorem 1, whose proof is formally certified in Lean, Theorem 2 rests on the
correctness of the SMS toolchain and of our encoding. The framework can emit machine-checkable
certificates (DRAT proofs for the SAT reasoning and a witnessing permutation for each learned

                                                7
symmetry-breaking clause [10]), and an end-to-end pipeline that checks SMS runs inside Lean,
with LRAT proofs imported by reflection, has very recently been announced [12, 13]. Producing
and formally checking a complete certificate for the n = 26, n = 27 and n = 28 runs along those
lines is left as future work. The validation above, and the agreement with [3] on 14–25 vertices,
are our present evidence of correctness.


6    Obstructions below 64
Whether n6 (4) < 64 remains open (the exhaustive bound of Section 5 stops at 28 vertices),
but we can prove that a smaller witness, if it exists, cannot be obtained from G64 by local
modifications, cannot be a Cayley graph, and cannot admit any semiregular group action with
two or three vertex orbits (Proposition 7). All computational claims in this section were verified
exhaustively; the scripts, including a re-verification of Proposition 5 that runs in seconds, are
among the ancillary files.
Proposition 5 (Rigidity of G64 ). (i) G64 has diameter 4. In particular no two vertices are
    at distance ≥ 5, so no edge can be added to G64 without creating a cycle of length at most
    5; the same holds for G64 − v for every vertex v.

 (ii) For every pair of vertices {u, v} (there are 256 orbits of pairs under the automorphism
      v 7→ v + 8), the graph G64 − {u, v} admits at most 3 girth-preserving edge additions, and
      every maximal sequence of girth-preserving additions results in a 3-colourable graph.

 (iii) For every pair of nonadjacent vertices u, v there exists a u–v path of length 3, 4 or 5.
       Consequently every identification of two nonadjacent vertices of G64 creates a cycle of
       length at most 5; identifying two adjacent vertices, that is, contracting an edge uv, yields
       a 3-colourable graph instead, since every proper 3-colouring of G64 − uv, which exists by
       Proposition 3(iii), satisfies c(u) = c(v) (otherwise it would properly 3-colour G64 ) and
       hence descends to the quotient.
     Hence no 4-chromatic graph of girth 6 on fewer than 64 vertices can be obtained from G64 by
deleting up to two vertices and adding girth-preserving edges, or by identifying two vertices.
    We note, concerning (iii), that identifying two nonadjacent vertices u, v of a non-3-colourable
graph always preserves non-3-colourability (a proper 3-colouring of the quotient is a proper 3-
colouring of the original graph with c(u) = c(v)), and that paths of length 2 collapse harmlessly
to single edges in the quotient; so a nonadjacent pair whose only short connections have length
2 would immediately yield a 63-vertex witness. Item (iii) rules this out. The same rigidity
phenomena hold for the 66-vertex graph of [3], which we re-verified: it has diameter 4 and no
distance-≥ 5 pair survives any single vertex deletion.
    The second obstruction concerns symmetry. Cayley graphs are a natural candidate family
here (the smallest Cayley witness found in [3] has order 96), and the witness G64 admits a
semiregular automorphism and, by Proposition 3(v), nothing beyond it; but no witness on 54–63
vertices can be a Cayley graph:
Proposition 6. (i) Every Cayley graph of an abelian group with degree at least 3 has girth at
                                                       / {s, s−1 }, then (e, s, s+t, t) is a 4-cycle.
    most 4: if s, t are connection-set elements with t ∈

 (ii) No Cayley graph of a (generalized) dihedral group Dih(A) has both girth ≥ 6 and chromatic
      number ≥ 4: a connection set containing a “rotation” a ∈ A and a “reflection” ρ yields the

                                                 8
      4-cycle (e, ρ, ρa, a−1 ); a rotation-only set falls under (i); and a reflection-only set gives a
      bipartite graph.

 (iii) For every remaining group, that is, every group of orders 54–63 that is neither abelian
       nor generalized dihedral (including A5 , the dicyclic groups, the Frobenius groups Z11 ⋊ Z5 ,
       Z19 ⋊ Z3 and Z32 ⋊ Z7 , the semidirect products Z7 ⋊ Z8 and Z7 ⋊ Z9 (whose actions are
       not faithful, so they are not Frobenius), the remaining semidirect products of orders 54, 56
       and 60, and direct products of smaller dihedral, dicyclic and alternating groups with cyclic
       groups), an exhaustive enumeration of all connection sets of degrees 4 to 7 finds no Cayley
       graph with girth ≥ 6 and χ ≥ 4. This range suffices: degrees ≤ 3 are excluded by Brooks’
       theorem [16], since K4 has girth 3 and odd cycles are 3-colourable, while the Moore-type
       bound for girth 6 (the balls of radius 2 around the endpoints of an edge are disjoint, so
       n ≥ 2(d2 − d + 1)) already makes degree 7 impossible below 86 vertices, so the enumerated
       range includes a margin. For groups of odd order the connection sets have even size, so
       only degrees 4 and 6 occur there.
     Consequently no 4-chromatic Cayley graph of girth ≥ 6 exists on 54–63 vertices. For n = 59
and n = 61, since every vertex-transitive graph of prime order is a circulant [7], no vertex-
transitive witness exists at all.

    Item (i) is folklore, and items (i) and (ii) fit a known pattern: the closer a group is to being
abelian, the smaller the girth of its Cayley graphs; see [8] for quantitative versions for nilpotent
and solvable groups in the context of cage constructions.
    The enumeration behind (iii) is feasible because Cayley graphs are vertex-transitive: the
girth equals the length of a shortest cycle through the identity, which can be tested locally
and monotonically along a backtracking search over connection sets. The quantification over
all groups is itself machine-verified: an ancillary script (group_census.py) constructs explicit
multiplication tables for every isomorphism class of orders 54–63: it derives the candidate lists
from Sylow-theoretic normal-subgroup arguments, checks the group axioms in full, checks the
classes pairwise non-isomorphic, and checks their number against the classical classification [18]
(55 classes in total); it then maps each class to the lemma or to the enumeration log that covers
it. The search spaces collapse dramatically under the girth constraint (for instance, of the 16,926
girth-≥ 6 connection sets of degree 5 on the dihedral group of order 62, every single one is
reflection-only and hence bipartite), and the non-bipartite girth-6 Cayley graphs that exist in
this range are few (all of degree 4, e.g. 315 graphs on Z7 ⋊ Z9 , except for 40 of degree 5 on
F20 × Z3 ), and all are easily 3-colourable. This may be read as an explanation of why the
witnesses at both 64 and 66 vertices possess semiregular, but not transitive, symmetry.
    The third obstruction extends the second to exactly that semiregular symmetry. For a finite
group H and an integer r ≥ 2, consider the graphs on n = r|H| vertices admitting a semiregular
action of H with r vertex orbits (“fibers”), equivalently lifts of an r-vertex base multigraph with
voltages in H [17]. For H = Zs these are the cyclic lifts of Section 3, and G64 itself is the case
H = Z8 , r = 8. Every such graph is a union of edge classes (orbits of vertex pairs under the
action), so an entire symmetry type is encoded by one Boolean variable per class, and “does this
type contain a witness?” becomes a satisfiability question: cycles of length 3 and 4 are excluded
by clauses through fiber representatives, longer short cycles lazily from proposed models, and
non-3-colourability is enforced by co-certificate learning [11] exactly as in Section 5. The search
is exhaustive over the type: it terminates either by producing a witness or by proving that none
exists.


                                                  9
Proposition 7. For every n ≤ 63, every finite group H and every r ∈ {2, 3} with r|H| = n, no
graph on n vertices with girth ≥ 6 and chromatic number ≥ 4 admits a semiregular action of H
with r vertex orbits. Moreover, the same holds for the types (H, r) with r ≥ 4 listed in Table 4.

Proof (computational). For n ≤ 28 the statement follows from Theorem 2, so let 30 ≤ n ≤ 63 (a
semiregular action with 2 or 3 orbits forces 2 | n or 3 | n, so n = 29 is vacuous). This gives 106
pairs (H, r): the 66 isomorphism classes of orders 15–31 at r = 2 and the 40 classes of orders
10–21 at r = 3. The exhaustive search described above, run with the additional constraint of
minimum degree 3, terminates with an empty enumeration on every one of them. The minimum-
degree constraint is discharged by induction on r: vertex degrees are constant along fibers, and a
fiber of degree ≤ 2 is disjoint from every 4-critical subgraph, so a hypothetical witness violating
the constraint reduces, by deleting that fiber, to a witness with the same action and one fiber
fewer. From (H, 3) this lands in (H, 2), covered by the same argument at order 2|H| ≤ 42
(or by Theorem 2 when 2|H| ≤ 28); from (H, 2) it lands in the Cayley case (H, 1) of order
|H| ≤ 31: orders up to 28 are excluded by Theorem 2, orders 29 and 31 by Proposition 6(i),
and order 30 by Proposition 6(i)–(ii) for Z30 and D15 together with an exhaustive enumeration
(as in Proposition 6(iii), degrees 4–5) for Z3 ×D5 and Z5 ×D3 . The same descent discharges the
constraint for the types of Table 4, whose fiber-deleted cases all land in the r ∈ {2, 3} statement
or below 29 vertices. The quantification over all isomorphism classes of each order is verified by
the same census script as in Proposition 6, which also maps every class to its exhaustion log.


             n   r   exhausted types with r ≥ 4
            40   4   (Z10 , 4), (D5 , 4) (both groups of order 10)
            36   4   (Z9 , 4), (Z23 , 4) (both groups of order 9)
            32   4   (Z8 , 4), (Z2 ×Z4 , 4), (Z32 , 4), (D4 , 4), (Q8 , 4) (all five groups of order 8)
            30   5   (Z6 , 5), (D3 , 5) (both groups of order 6)

Table 4: The exhausted semiregular types with more than three orbits (Proposition 7); the types
with r ∈ {2, 3} are all of them, for every order, and are not listed. Dm is the dihedral group of
order 2m and Q8 the quaternion group. The per-type model counts are recorded in the deposited
logs.

    Since a semiregular action of H restricts to a semiregular action of any subgroup K ≤ H,
with [H : K] times as many orbits, Proposition 7 has a corollary complementing Proposition 6
below order 54: no witness on at most 63 vertices is a Cayley graph of a group possessing a
subgroup of index 2 or 3.
    Three positive controls validate the machinery. On the type (Z11 , 6) at n = 66 the same search
terminates in seven minutes by finding a witness, isomorphic to the 66-vertex graph of [3]; at
girth 5 on (Z7 , 3) it immediately finds a 21-vertex non-3-colourable graph of girth 5 (matching
n5 (4) = 21); and G64 is verified to be a union of 20 classes of the (Z8 , 8) type. Runs at r|H| ≤ 28
terminate empty, consistently with Theorem 2. The proposition covers, in particular, the hottest
regions of our randomized searches: the types (Z21 , 3) at n = 63 and (D15 , 2) at n = 60, whose
random sampling had produced thousands of near-4-chromatic candidates, are provably empty.
    Every known witness of an ng (4) record with g ≥ 6 (G64 , and the graphs on 66 and 171
vertices of [3], the latter described there as LCF graphs) is a lift with a semiregular cyclic group
action, with 8, 6 and 9 orbits respectively. Proposition 7 closes the more symmetric end of this
regime below 64 vertices completely (up to 3 orbits, every group and every order) and parts of

                                                       10
the rest (Table 4); what remains open at n = 63 are the types (Z9 , 7) and (Z3 ×Z3 , 7), which
remained undecided after 7.4 and 2.6 million candidate models respectively, and (Z7 , 9) and
(Z3 , 21), which we did not attempt; the analogous finding run on the (Z8 , 8) type at n = 64,
which must terminate with a witness, was likewise not run to completion.


7    Concluding remarks
The bounds on n6 (4) now stand at

                                       29 ≤ n6 (4) ≤ 64.

The lower-bound computation of Section 5 might be pushed, by the observed growth rate, one
or two orders further (the n = 28 level already took just over four days on a single core, and the
cost ratio rose to 9.6 at that step, so n = 29 is a matter of weeks on modest hardware), but not
to the range 54–63 where a smaller witness, if any, is most plausibly to be found. Our searches
below 64 vertices found no smaller witness. They comprised over twenty-five million randomized
candidates for 54 ≤ n ≤ 63, drawn from semiregular cyclic factorizations and from lifts of small
base graphs with voltage assignments in non-abelian groups, together with asymmetric local
searches at n = 60, 62, 63 warm-started from mutilated copies of both known witnesses, and
the exhaustive analyses of Section 6. Among these candidates, roughly 104 resisted randomized
heuristic 3-colouring and were decided by exact solvers: every one of them is 3-colourable. The
random searches are far from exhaustive, and we do not consider the evidence sufficient to
conjecture whether n6 (4) = 64; what Section 6 does establish is that a smaller witness, if one
exists, has essentially none of the symmetry that produced every witness known so far.
    We close with three natural directions. First, deciding the remaining semiregular types at
n = 63 (notably (Z9 , 7) and (Z23 , 7)) would make the symmetry obstruction complete at that
order. Second, Theorem 2 could be brought to the same standard of evidence as Theorem 1 by
producing and formally checking certificates for the SMS runs (Remark 4). Third, the graph
G64 , being 4-critical with a transparent algebraic description, may be of independent interest as
a test case for colouring algorithms and for formal verification of computational combinatorics.

Acknowledgements
The search pipeline, the verification scripts and the Lean formalization were developed with
the assistance of an AI system (Claude, Anthropic); all final artifacts are deterministic and
independently checkable. We thank the authors of [3] for their clear account of the state of the
art, and Andrea Nicastro for suggesting the use of Lean for the formal verification.


References
 [1] P. Erdős, Graph theory and probability, Canadian Journal of Mathematics 11 (1959),
     34–38.

 [2] G. Brinkmann and M. Meringer, The smallest 4-regular 4-chromatic graphs with girth 5,
     Graph Theory Notes of New York 32 (1997), 40–41.

 [3] G. Exoo and J. Goedgebeur, Bounds for the smallest k-chromatic graphs of given girth,
     Discrete Mathematics & Theoretical Computer Science 21(3) (2019), #9. arXiv:1805.06713.

                                               11
 [4] G. Araujo-Pardo, J. C. Díaz-Calderón, J. Fresán-Figueroa, D. González-Moreno, L. Lesniak
     and M. Olsen, On (r, g, χ)-graphs and cages of regularity r, girth g and chromatic number
     χ, The Art of Discrete and Applied Mathematics 8 (2025), #P3.07.

 [5] K. Coolsaet, S. D’hondt and J. Goedgebeur, House of Graphs 2.0: a database of interesting
     graphs and more, Discrete Applied Mathematics 325 (2023), 97–107. Available at https:
     //houseofgraphs.org.

 [6] A. Kostochka and M. Yancey, Ore’s conjecture on color-critical graphs is almost true,
     Journal of Combinatorial Theory, Series B 109 (2014), 73–101.

 [7] J. Turner, Point-symmetric graphs with a prime number of points, Journal of Combinatorial
     Theory 3 (1967), 136–145.

 [8] M. Conder, G. Exoo and R. Jajcay, On the limitations of the use of solvable groups in Cayley
     graph cage constructions, European Journal of Combinatorics 31 (2010), 1819–1828.

 [9] C.-H. Liu and L. Postle, On the minimum edge-density of 4-critical graphs of girth five,
     Journal of Graph Theory 86 (2017), 387–405.

[10] M. Kirchweger and S. Szeider, SAT modulo symmetries for graph generation and enumer-
     ation, ACM Transactions on Computational Logic 25(3) (2024), #18; conference version:
     SAT modulo symmetries for graph generation, CP 2021, LIPIcs 210, 34:1–34:16.

[11] M. Kirchweger, T. Peitl and S. Szeider, Co-certificate learning with SAT modulo symmetries,
     in Proceedings of IJCAI 2023, 1944–1953. arXiv:2306.10427.

[12] M. Kirchweger, P. Manrique and S. Szeider, Formally verified graph generation with
     SAT modulo symmetries and Lean, in Automated Reasoning (IJCAR 2026), LNCS 16688,
     Springer, 2026, 117–135.

[13] S. Szeider, LRAT-Catcher: importing SAT solver certificates into Lean 4 by reflection,
     arXiv:2607.00815 (2026).

[14] A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks and F. Pollitt, CaDiCaL 2.0, in
     Computer Aided Verification (CAV 2024), LNCS 14681, Springer, 2024, 133–152.

[15] V. Chvátal, The minimality of the Mycielski graph, in Graphs and Combinatorics
     (Proc. Capital Conf., George Washington Univ., 1973), Lecture Notes in Mathematics 406,
     Springer, 1974, 243–246.

[16] R. L. Brooks, On colouring the nodes of a network, Proceedings of the Cambridge Philo-
     sophical Society 37 (1941), 194–197.

[17] J. L. Gross, Voltage graphs, Discrete Mathematics 9 (1974), 239–246.

[18] H. U. Besche, B. Eick and E. A. O’Brien, A millennium project: constructing small groups,
     International Journal of Algebra and Computation 12 (2002), 623–644.

[19] L. de Moura and S. Ullrich, The Lean 4 theorem prover and programming language, in
     Automated Deduction – CADE 28, LNCS 12699, Springer, 2021, 625–635.



                                               12
