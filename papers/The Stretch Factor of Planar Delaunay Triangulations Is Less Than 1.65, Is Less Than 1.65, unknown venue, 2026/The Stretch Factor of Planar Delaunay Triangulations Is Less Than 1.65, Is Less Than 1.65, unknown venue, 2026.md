                                                   The Stretch Factor of Planar Delaunay Triangulations
                                                                    Is Less Than 1.65
                                                                 Guanlin Mo1,†                 moguanlin@mail.ustc.edu.cn
                                                                 Kangke Cheng1,†                ke314159@mail.ustc.edu.cn
                                                                 Hu Ding1,*                           huding@ustc.edu.cn
                                                                 1
                                                                     University of Science and Technology of China, Hefei, China
arXiv:2609.07979v3 [cs.CG] 17 Sep 2026




                                                      †                                                           *
                                                          Guanlin Mo and Kangke Cheng contribute equally.             Corresponding author.

                                                                                             Abstract
                                                  Delaunay triangulations are a fundamental class of plane spanners, and determining their
                                              worst-case stretch factor has been a longstanding problem in computational geometry. We prove
                                              an upper bound of 1.65, improving the bound of 1.998 due to Xia (2011) and reducing the gap
                                              to the known lower bound of 1.5932 by a factor of more than seven. Our proof works with the
                                              chains of circumdisks introduced by Xia, along which a path between two sites is assembled
                                              disk by disk. Xia measures such a path against a quantity attached to the whole chain, and
                                              because that quantity is not additive, his induction has to be carried alongside a separate global
                                              estimate. Our main idea is to measure the path against the progress it makes along the segment
                                              joining the two sites. This quantity is additive, so the bound becomes a Bellman recursion that
                                              forgets all but one number about the disks already passed, and we show that the bound holds
                                              if and only if a potential on the current state satisfies three local inequalities. The smallest
                                              feasible potential is the value function of that recursion, so searching for a potential becomes the
                                              problem of fitting this value function from above. The geometry of the disks reduces the fit to a
                                              linear program over functions of one variable, in which a GPT-based multi-agent system that we
                                              developed found a feasible point, certified in exact arithmetic.


                                         1    Introduction
                                         A plane spanner is a planar graph on a finite point set whose shortest-path distances are at most
                                         a constant times the Euclidean distances. The oldest and most widely used one is the Delaunay
                                         triangulation, and the constant that measures how much worse is the quantity this paper is about:
                                         for a triangulation D of a finite planar set S, whose edges carry their Euclidean lengths, the stretch
                                         factor is
                                                                                                dD (p, q)
                                                                                st(D) = max               ,
                                                                                         p̸=q∈S ∥p − q∥

                                         where dD is shortest-path distance in the graph. Delaunay triangulations are known to have stretch
                                         factor bounded by an absolute constant, and the value of the smallest such constant is a question
                                         from the 1980s that is still open. It also propagates: several plane spanner constructions bound their
                                         spanning ratio through this constant [5, 14, 20], so an improvement for Delaunay triangulations
                                         improves those bounds as well.
                                             The known interval has been narrowed √    from both ends. Dobkin, Friedman and Supowit [9, 10]
                                         proved the first constant upper bound (1 + 5)π/2 ≈ 5.08, Keil and Gutwin [16, 17] improved it to

                                                                                                 1
     (a)    A three-disk chain                                      (b)   The ladder: rails and gates

                            rail
                                                                                  a1      rail     a2
                    a1             a2


 p                       gate G1        gate G2     q           p                                                   q
                                                                                       gate G1            gate G2
             O1             O2             O3

                    b1             b2
                                                                                  b1      rail     b2
                            rail
     A gate is the common chord of consecutive disks.               Each gate is an edge of the ladder.


Figure 1: A three-disk chain and its weighted ladder. (a) The query segment [p, q] crosses the two
gates Gi = [ai , bi ], shown in orange. The solid blue arcs are the rails; the dashed circle arcs show
the rest of each circle. (b) The rails and gates together form the ladder. Rails are drawn as straight
edges here, with weights equal to their original arc lengths; gate weights are chord lengths.


2π/(3 cos(π/6)) ≈ 2.42, and Xia [22] lowered it below 1.998. From below, Chew [7] gave π/2, Bose
et al. [4] raised it to 1.5846, and Xia and Zhang [23] to 1.5932. We move the upper end.

1.1        Our Main Result
Theorem 1.1 (main theorem, restated as Theorem 6.4). Let S ⊂ R2 be a finite set of distinct
points not contained in a line, and let D be any specified straight-line Delaunay triangulation of S:
every triangular face of D has an open circumdisk containing no point of S. Then
                                                            33
                                                  st(D) ≤      = 1.65.
                                                            20
    The theorem allows collinear subsets of S and cocircular groups of four or more sites. When
a cocircular polygon admits several Delaunay triangulations, the bound applies to each specified
choice D. Together with 1.5932 the known interval for the worst-case constant is thus reduced from
[1.5932, 1.998], of width 0.4048, to [1.5932, 1.65], of width 0.0568.

1.2        Chains of Circumdisks
The proof starts with a geometric reduction to disk chains. Following Xia [22], one looks at the
segment [p, q] and at the circumdisks of the faces it crosses (Figure 1). Consecutive disks overlap,
and each consecutive pair meets along a chord, a gate. On each disk, the two arcs between the
incoming and the outgoing gate are its rails. The rails and gates form a graph, the ladder, on which
one can walk from p to q. Roughly speaking, such a walk follows the boundary arcs of the disks and
cuts across each overlap. For this chain O, write PO for the shortest of these walks. Every rail can
be traded for a chain of Delaunay edges no longer than the arc, and every gate is itself an edge, so
PO bounds dD (p, q) from above.
    To prove Theorem 1.1, it therefore suffices to bound PO by 1.65 ∥p − q∥ for chains generated by
query segments.




                                                            2
1.3   The Bottleneck in the Previous Analysis
Xia [22] proves a bound for disk chains defined independently of a query segment. He compares
PO with the rubber length DO , the length of the shortest polyline meeting all the gates in order.
For a chain generated by [p, q], the segment itself is such a shortest polyline, so DO = ∥p − q∥. His
analysis seeks the chain inequality
                                            PO ≤ ρ D O .                                          (1)
    The points where the shortest polyline meets the gates are chosen jointly for the entire chain,
so DO is a global minimum rather than a sum of independent contributions from successive disks.
Xia’s induction uses an accumulated potential to control the growth of the ladder distance relative
to this quantity. To turn the inductive estimate into a stretch bound, a separate global argument
bounds that potential, when negative, by a fraction K of the ladder length PO on a suitably chosen
extremal chain. If the induction uses coefficient λ, the resulting bound is
                                          λ
                                    ρ=       ,        0 ≤ K < 1.                                  (2)
                                         1−K
   The same potential must therefore support the induction and satisfy the global estimate.
Increasing its negative contribution can help the induction while making the global estimate more
demanding, so the final bound depends on the combined effect on λ and K. Xia’s estimates use
λ = 1.8 and yield ρ = 1.998.

1.4   Our Main Ideas
Our main idea is to formulate the disk-chain bound as a Bellman problem, processing the disks
one at a time. We keep a query line that crosses the gates in order. The gate crossings divide the
segment from p to q into intervals whose lengths sum to ∥p − q∥. This gives an additive quantity
against which to compare the path length.
    We need to answer two questions: (a) what information must we keep when adding a
disk? and (b) how can we use it to certify a stretch bound?
    For question (a), stop at a gate and consider two shortest paths from p: one to its upper endpoint
and one to its lower endpoint, both using only the part of the ladder already processed. Their
lengths contain all the information from earlier path choices needed to update the next pair of
distances. We also show that the current disk and gate determine the geometry needed for this
update (Lemmas 4.5 and 4.8). This gives the local information needed by the Bellman recursion.
    For question (b), fix a proposed stretch bound U . At each step, we compare the cost added by
the distance recursion with U times the distance advanced along the query line. We introduce a
function of the current state, called a potential, so that any excess in this comparison is covered by
a decrease in the potential. Adding the step inequalities cancels the intermediate potential values.
The start and end inequalities handle the first and last potential values, giving PO ≤ U ∥p − q∥
(Theorem 4.7).
    Conversely, if the bound holds for every chain in our class, then a potential satisfying these
inequalities exists. The Bellman value function is the smallest such potential at each state (Theo-
rem B.2). It gives a precise target for constructing an explicit feasible potential.
    To construct the potential, we split each step into two geometric comparisons. First we move
along the old circle, using its arc lengths and the exact distance update. Then we keep the outgoing
gate fixed and vary the circle through its two endpoints (Figure 5). A derivative inequality controls
the change in potential during this second move.



                                                  3
    After scaling the disk to unit radius, we choose potentials controlled by one function of one
variable, called a profile, which governs their dependence on the disk center’s height relative to the
query line. The geometric comparisons give sufficient conditions that are affine in U , the profile
and its derivative (Theorem 5.7). Minimizing U under these conditions gives a linear program over
profiles.
    We construct a potential using a cubic spline weight function and rigorously verify the Bellman
inequalities at U = 1.65 over all admissible states.

1.5   Contributions and Organization
 1. A local state reduction for disk-chain recursion. We introduce a local state consisting of the
    current disk, its gate, and the difference between the two shortest distances from the source to
    the gate endpoints within the processed ladder. This state determines the admissible extensions
    and the increments in the exact distance recursion. After normalization, it has four parameters,
    regardless of the chain length.
 2. A Bellman characterization and a profile-based linear program. Comparing the ladder length
    against progress along the query line makes the reference quantity additive. For U ≥ π/2, the
    chain bound at level U is equivalent to the existence of a potential on the local state satisfying
    an initialization, a step, and a termination inequality. The three inequalities telescope to
    give the bound U directly, and the Bellman value function is the pointwise smallest feasible
    potential. The current disk and gate determine the geometric operations available at a state.
    Normalizing and differentiating along the circles through a fixed gate turn the step inequality
    into a pointwise condition on four angles that is affine in a one-variable profile and its first
    derivative, yielding a linear program for a feasible potential.
 3. A certified feasible point of that program at 33/20. An agent-assisted search over the shape and
    the coefficients of the profile produced an even C 2 cubic spline with exact rational coefficients,
    and its conditions are verified over the full closed domains in exact arithmetic. Since the
    program is linear, the search is a search for a feasible point, and what it must supply is fixed in
    advance by the two reductions.
    Section 2 places the result and separates what is inherited from what is new. Section 3 defines
chains, the ladder, the restricted class and gate states, and reduces Theorem 1.1 to the chain bound.
Section 4 proves that the three local inequalities imply the chain bound. Section 5 carries out
the reduction to the linear program. Section 6 exhibits the spline profile, proves Theorem 6.4,
and describes the certification. Section 7 describes the search that produced the coefficients. The
appendices follow the order in which the text calls on them: the transfer from a specified triangulation
to chains (Section A), the Bellman value function and its value equation, including the converse
implication (Section B), and the exact parameters together with the auxiliary proofs (Sections C
and D).


2     Related Work
Bounds on the Delaunay stretch factor. Table 1 collects the known bounds together with
the settings in which they hold. Dobkin, Friedman and Supowit [9, 10] proved the first constant
upper bound; Keil and Gutwin [16, 17] improved it to ≈ 2.42, which stood until Xia [22] introduced
the disk-chain analysis and obtained a bound below 1.998. Cui, Kanj and Xia [8] proved 2.33 for
point sets in convex position. On the other side, Chew [7] gave the lower bound π/2, Bose et al. [4]


                                                   4
         Value                    Setting                                        Source
 Lower   π/2 ≈ 1.5708             arbitrary finite point sets                    Chew [7]
 Lower   1.5846                   arbitrary finite point sets                    Bose et al. [4]
 Lower   1.5932                   arbitrary finite point sets                    Xia and Zhang [23]
              √
 Upper   (1 + 5)π/2 ≈ 5.08        arbitrary finite point sets                    Dobkin et al. [9, 10]
 Upper   2π/(3 cos(π/6)) ≈ 2.42   arbitrary finite point sets                    Keil and Gutwin [16, 17]
 Upper   2.33                     points in convex position                      Cui et al. [8]
 Upper   1.998                    specified triangulation, no general position   Xia [22]
 Upper   1.65                     specified triangulation, no general position   Theorem 6.4

Table 1: Known bounds on the worst-case Delaunay stretch factor. The two upper bounds in the
last two rows quantify over a triangulation named in advance, so a cocircular polygon may be
triangulated in any of its admissible ways.


showed that almost all Delaunay triangulations exceed π/2 and obtained 1.5846, and Xia and Zhang
[23] constructed point sets with stretch factor above 1.5932, which remains the best published lower
bound. Because the Delaunay stretch factor enters the spanning ratio of several plane spanner
constructions [5, 14, 20], an improved upper bound for it improves those ratios as well.

The disk-chain framework. Xia [22] introduced a disk-chain framework for bounding the stretch
of Delaunay triangulations. The basic construction follows the circumdisks of the triangular faces
crossed by the segment between two vertices. Arcs of these circles and their common chords form a
ladder joining the two vertices. A path in this ladder can be converted into a path in the Delaunay
triangulation of no greater length. The framework therefore reduces a graph-distance bound to a
geometric bound on paths through a chain of disks. We use this geometric reduction in our proof.
    Xia’s analysis compares ladder paths with the rubber length through induction and a global
estimate of an accumulated potential. Our analysis uses an exact shortest-path recursion on chains
carrying an oriented query line. For this chain class, we prove that the path bound is equivalent to
the existence of a potential satisfying three local inequalities; when the bound holds, the excess —
the Bellman value function of the recursion — is the smallest feasible potential (Theorem B.2). We
further use the disk geometry to construct a family of potentials whose sufficient conditions form
a linear program over functions of one variable (Theorem 5.7). Xia’s bound is not recovered as a
special case of ours: his induction and ours use different reference quantities, and the two analyses
share only the geometric reduction.

Computer-assisted inequalities. Two kinds of certificate are used, both standard. Exact
rational Bernstein expansions settle the polynomial positivity statements; for the Bernstein basis
see Farouki’s survey [11]. The remaining conditions involve transcendental functions on compact
domains and are settled by exhaustive covers in outward-directed interval arithmetic; for the general
method see Moore et al. [19] and, for the enclosure of π by a Machin-type identity, Borwein and
Borwein [3].

Search for a certificate. The profile was found by an agent-assisted search, described in
Section 7. Systems pairing a language model with an automated evaluator, from FunSearch [21]
and AlphaEvolve [1] to their successors [12], search for constructions scored by a program. Formal-
verifier systems [2] use proof checkers to establish correctness. Closest to the present setting
are the dual-agent convex relaxations of Kim and Pilanci [18], which certify bounds by interval


                                                    5
arithmetic; the Gilbert–Pollak search of Ke et al. [15], which uses boxes to certify a geometric
bound; and the potential-function benchmark of Brilliantov et al. [6], which searches parameterized
potential families against a proof-shaped constraint system. The design of the search space carries
mathematical content in these pipelines [13]. In the present case the two reductions are exactly
where the mathematics lies, and they are theorems: what they leave is a linear program, on which a
feasible point is a bound, certified in exact arithmetic.


3     Preliminaries
Throughout, S ⊂ R2 is a finite set of distinct points not contained in a line, and D is a specified
straight-line Delaunay triangulation of S: every triangular face has an open circumdisk containing
no point of S. Four or more points of S may be cocircular, in which case the resulting cocircular
polygon admits several triangulations and the quantifier fixes one of them. Each edge of D carries
its Euclidean length and dD is the induced shortest-path distance.

Notations. We write ∥·∥ for the Euclidean norm and p, q for the two points of S whose distance is
being bounded. A disk is a pair O = (o, r) of center and positive radius, and powO (z) = ∥z − o∥2 −r2
is the power of a point with respect to it, negative exactly inside.

3.1    Chains of disks and the ladder
This subsection makes Figure 1 precise. The definitions below also cover tangencies, repeated disks
and degenerate arcs.
    A chain is a finite ordered list O = (O1 , . . . , On ) of closed disks of positive radius, together with
two terminals u ∈ ∂O1 and v ∈ ∂On , subject to the conditions below. The list records occurrences:
the same disk may appear twice, with each occurrence represented separately.
    Consecutive circles meet at two points carrying incidence tags ai , bi ; the two may coincide
geometrically when the circles are tangent, and the tags stay distinct. Neither of two consecutive
disks contains the other. The chord
                                               Gi = [ai , bi ]
is the i-th gate, with length gi = ∥ai − bi ∥. On disk Oi , the closed arc lying inside Oi−1 and the
closed arc lying inside Oi+1 are its two caps. We require the caps on each internal disk to satisfy
strong cap-disjointness: their relative interiors are disjoint, and no endpoint of one lies in the relative
interior of the other. This makes the two gates occur in the correct order along the circle. The
terminals satisfy u = a0 = b0 ∈ / int O2 and v = an = bn ∈   / int On−1 , omitting a condition when the
neighbor does not exist.
    The two boundary arcs between the incoming and outgoing caps are the rails of Oi . The upper
rail connects ai−1 to ai , and the lower rail connects bi−1 to bi . Both arcs include their endpoints.
    Rail lengths are measured along these boundary arcs. When the endpoints coincide geometrically,
we distinguish a zero-length arc from a full circle of length 2πri . A zero-length rail still joins two
distinct tags.
    The ladder of O is the finite weighted graph whose vertices are the incidence tags, whose edges
correspond to the 2n rails, weighted by arc length, and the n − 1 gates ai bi for 1 ≤ i ≤ n − 1,
weighted by chord length. Write
                                                 PO (u, v)




                                                     6
for the shortest u–v distance in this graph. The graph uses exactly the rails, gates and incidence
identifications specified above. At each terminal, its upper and lower tags represent a single vertex.
All other tags remain distinct vertices even when their geometric locations coincide.
    Two facts about PO will be used. Both concern the passage between the triangulation and the
chain rather than the chain itself, so Section A proves them and the rest of the paper uses only
their statements. First, every rail can be traded for a walk in D no longer than the rail, and every
gate is an edge of D, so PO bounds dD from above along a chain produced by a query segment
(Lemma A.3). Second, for a single disk,
                                                         π
                                          PO (u, v) ≤      ∥u − v∥                                  (3)
                                                         2
whenever u ̸= v lie on its circle (Lemma A.4).

3.2    Chains crossed by a query line
An oriented query line is a line with a unit forward tangent e; write ne for e rotated counterclockwise
by π/2, and put
                                 x(z) = e · z,     y(z) = ne · (z − z0 )
for any fixed z0 on the line. The coordinate x increases in the forward direction, and y is the signed
perpendicular distance to the query line, positive on its left when looking in direction e.

Definition 3.1 (the chains we work with). A chain O equipped with an oriented query line belongs
to the class Q if u and v lie on the line with x(u) < x(v) and, in addition:
 (i) consecutive circles cross properly, |ri − ri+1 | < ∥oi − oi+1 ∥ < ri + ri+1 ;
(ii) each gate has its upper tag strictly above and its lower tag strictly below the line, y(ai ) > 0 >
     y(bi ), so the line meets Gi in a single point ci interior to that chord;
(iii) each pair is directed forward, e · (oi+1 − oi ) > 0;
(iv) the crossings are strictly ordered, x(u) < x(c1 ) < · · · < x(cn−1 ) < x(v).
For n = 1 only the two distinct terminals on one positive-radius circle and the orientation from u to
v are required.

   Conditions (i)–(iv) specify the domain Q. Lemma A.5 shows that the chains produced by a
query segment satisfy these conditions directly. The domain includes zero-length rails, with their
tags distinct.
   For n ≥ 2, condition (iv) orders the gate crossings along [u, v]. The lengths of the resulting
segments add up to

                       n−2
                         X                                    
         x(c1 ) − x(u) +    x(ci+1 ) − x(ci ) + x(v) − x(cn−1 ) = x(v) − x(u) = ∥u − v∥ ,           (4)
                           i=1

the last equality because u and v both lie on the query line. So the progress is additive along the
chain and equals ∥u − v∥.




                                                     7
3.3   Gate states
Fix a chain in Q and an index i ≤ n − 1, and consider the prefix ladder at gate i: the ladder of the
first i disks together with gates 1, . . . , i. Let

                                               d+
                                                i ,       d−
                                                           i

be the shortest distances in it from u to the upper and to the lower tag of gate i (Figure 2(a)).
Record them in the symmetric form
                                                −
                                          d+
                                           i + di                    −
                                   µi =           ,       δi = d+
                                                                i − di .                               (5)
                                             2
A path may switch between the endpoints of gate i at cost gi , giving |δi | ≤ gi . We call µi the ledger
and δi the balance.
   At gate i, the next disk to be processed is Oi+1 . We record si = (Oi+1 , Gi , δi ) as the state and
keep the ledger µi separately.

Definition 3.2 (gate state). A gate state is a triple s = (O, G, δ) consisting of a disk O = (o, r)
with r > 0, a chord G = [aG , bG ] of its circle with g = ∥aG − bG ∥ > 0 and y(aG ) > 0 > y(bG )
relative to a given oriented query line, and a real number δ ∈ [−g, g]. States are considered modulo
orientation-preserving isometries fixing the query line and modulo the corresponding renaming of
tags.

    Where the circle meets the query line, call the backward and forward points w− and w+ ; where
the gate meets it, call the crossing c (Figure 2(b)). The two arclength coordinates l+ and l− locate
the gate tags aG , bG from w− along the upper and the lower arc, with their actual, possibly major,
lengths. Along the query line, the lengths from w− to c and from c to w+ are, respectively,

                            L− = x(c) − x(w− ),           L+ = x(w+ ) − x(c),

as marked below the disk in Figure 2(b).

3.4   Reduction to the chain bound
Proposition 3.3. Let U ≥ π/2. Suppose that every chain in Q satisfies

                                          PO (u, v) ≤ U ∥u − v∥ .                                      (6)

Then dD (p, q) ≤ U ∥p − q∥ for every finite set S of distinct non-collinear points, every specified
straight-line Delaunay triangulation D of S, and every p, q ∈ S.

Proof. When p = q, both sides are zero. Assume p ̸= q.
    First suppose that the interior of [p, q] contains no point of S. If [p, q] is an edge of D, that edge
itself gives a path of length ∥p − q∥, and the desired bound follows from U ≥ 1.
    Otherwise, Lemma A.2 constructs a disk chain O along [p, q], with terminals p and q. By
Lemma A.5, this chain, oriented from p to q, satisfies the conditions defining Q, so the assumed
chain bound applies to it.
    To obtain a path bound in D, take a shortest walk in the ladder of O. Each gate is already an
edge of the specified triangulation D. By Lemma A.3, each rail can be replaced by a walk along
edges of D between the same endpoints, with total length at most the length of the rail. These


                                                      8
    (a)   Distances at a gate                                  (b)    Coordinates of a gate state
                                                                           aG
                           ai
                                d+
                                 i
                                                                       l+            G
                                 Oi+1                                                           r
                        Gi                                                             o
                                                                      w−             c                 w+
u                                                                                                           e
                                                                                            O
                                d−
                                 i                                      l−
                           bi
     Distances from u to ai and bi in the prefix.                             bG
        Paths may switch sides along a gate.
                                                                              L−           L+
                               −
                         d+
                          i + di
                    µi =                                                           s = (O, G, δ)
                            2
                               −
                    δi = d+
                          i − di
                                                                     At gate i: O = Oi+1 , G = Gi , δ = δi .

                 l+ , l− measure circular arcs; L− , L+ measure straight segments on the query line.


                                                                               −
Figure 2: The quantities defining a gate state. (a) The prefix distances d+
                                                                          i , di determine the ledger
µi and balance δi . (b) The disk and gate from (a) are shown in the notation O, G of Definition 3.2.
The colored arcs run from w− to aG and bG and have lengths l+ and l− . The lengths L− and L+
are measured from w− to c and from c to w+ along the query line.


replacements give a p–q walk in D of length at most PO (p, q). Since dD (p, q) is the shortest-path
distance in D, we obtain
                                dD (p, q) ≤ PO (p, q) ≤ U ∥p − q∥ ,
where the second inequality is the hypothesis (6).
    For general p, q, the segment may pass through other points of S. List all the points of S on it
in order as
                                      p = p0 , p1 , . . . , pm = q.
Each subsegment [pj−1 , pj ] has no point of S in its interior, so the case just proved gives

                                dD (pj−1 , pj ) ≤ U ∥pj−1 − pj ∥ ,       1 ≤ j ≤ m.

Concatenating shortest paths between these successive pairs produces a walk from p to q. Therefore
                                                       m
                                                       X
                                         dD (p, q) ≤       dD (pj−1 , pj )
                                                       j=1
                                                         Xm
                                                    ≤U         ∥pj−1 − pj ∥
                                                         j=1

                                                    = U ∥p − q∥ .

The final equality holds because the points p0 , . . . , pm occur in order along the straight segment
[p, q], so the lengths of its subsegments sum to ∥p − q∥.

    It therefore remains to prove (6) for chains in Q.


                                                          9
4     The Bellman Form of the Chain Bound
Our main idea is to read the chain bound as an accounting identity along the ladder. Walking
along a chain, one accumulates ladder length and one accumulates progress; if a function of the
current state can be made to absorb the difference at every single move, then summing the local
comparisons bounds the two totals. This section proves that a function on gate states satisfying
three local inequalities is sufficient for (6); Section B proves the converse and identifies the smallest
such function.

4.1    An exact shortest-path recursion on the ladder
We first identify the geometry used by the recursion. Lemma 4.1 determines which query points can
serve as the source and terminal. Lemma 4.2 identifies the endpoints and lengths of the two rails
used in a step.

Lemma 4.1 (power differences and cap positions). Let Oi = (oi , ri ) and Oi+1 = (oi+1 , ri+1 ) be
two properly crossing disks. Suppose the query line crosses their common chord Gi = [ai , bi ] at an
interior point ci . For every z ∈ R2 ,

                           powOi (z) − powOi+1 (z) = 2(oi+1 − oi ) · (z − ci ).                       (7)

Along the query line, this power difference has slope 2(oi+1 − oi ) · e.
    For either disk O, let w− (O) and w+ (O) denote the backward and forward intersections of its
circle with the query line. If the pair is directed forward, (oi+1 − oi ) · e > 0, then

                                w− (Oi ) ∈
                                         / Oi+1 ,        w+ (Oi ) ∈ int Oi+1 ,
                              w− (Oi+1 ) ∈ int Oi , w+ (Oi+1 ) ∈
                                                               / Oi .

Thus the outgoing cap on Oi contains its forward query point in its relative interior and excludes its
backward query point. The incoming cap on Oi+1 contains its backward query point in its relative
interior and excludes its forward query point.

Proof. For any point z ∈ R2 , expanding the squared distances gives

                          powOi (z) − powOi+1 (z)
                            = ∥z − oi ∥2 − ri2 − ∥z − oi+1 ∥2 − ri+1
                                                                 2
                                                                    

                            = 2(oi+1 − oi ) · z + ∥oi ∥2 − ∥oi+1 ∥2 − ri2 + ri+1
                                                                             2
                                                                                 .

The ∥z∥2 terms cancel, so the difference is affine in z. At both ai and bi , the two powers are zero
because these points lie on both circles. Along the chord, their difference varies linearly between its
two endpoint values, both zero. It therefore vanishes throughout Gi , including at ci . Substituting
z = ci in the expansion above gives

                           ∥oi ∥2 − ∥oi+1 ∥2 − ri2 + ri+1
                                                      2
                                                          = −2(oi+1 − oi ) · ci .

Using this expression for the constant term gives (7).
    On the query line, write z = ci + te, where t ∈ R is the signed distance from ci in the forward
direction e. Then (7) becomes

                        powOi (ci + te) − powOi+1 (ci + te) = 2t (oi+1 − oi ) · e.

                                                    10
This proves the slope assertion. For the remaining claims, assume (oi+1 − oi ) · e > 0. The power
difference then increases strictly along the query line and is zero there exactly at ci .
    Since ci is interior to a chord of Oi , it lies inside Oi , and hence

                                   x(w− (Oi )) < x(ci ) < x(w+ (Oi )).
                                                                                     
At these two points, powOi (w± (Oi )) = 0 and w± (Oi ) − ci = x(w± (Oi )) − x(ci ) e. Solving (7) for
the power with respect to the next disk gives
                                                              
                  powOi+1 (w− (Oi )) = −2 x(w− (Oi )) − x(ci ) (oi+1 − oi ) · e > 0,
                                                              
                  powOi+1 (w+ (Oi )) = −2 x(w+ (Oi )) − x(ci ) (oi+1 − oi ) · e < 0.

   The same crossing ci is also interior to a chord of Oi+1 , so

                                 x(w− (Oi+1 )) < x(ci ) < x(w+ (Oi+1 )).

At these query points powOi+1 (w± (Oi+1 )) = 0. Solving (7) for the power with respect to the
preceding disk now gives
                                                              
                 powOi (w− (Oi+1 )) = 2 x(w− (Oi+1 )) − x(ci ) (oi+1 − oi ) · e < 0,
                                                              
                 powOi (w+ (Oi+1 )) = 2 x(w+ (Oi+1 )) − x(ci ) (oi+1 − oi ) · e > 0.

Negative power means that a point is strictly inside the corresponding disk, and positive power
means that it is outside. The four signs give the stated containments. By continuity along each
circle, a strictly negative power also places a small arc around the query point inside the neighboring
disk, giving relative interior membership in the cap.

Lemma 4.2 (rail order and lengths). Let Oi−1 , Oi , Oi+1 be three disks whose two neighboring pairs
satisfy Definition 3.1(i)–(iii), with gates Gi−1 = [ai−1 , bi−1 ] and Gi = [ai , bi ]. Suppose the incoming
and outgoing caps on Oi are strongly disjoint, and write w± = w± (Oi ). Along the upper and lower
arcs of ∂Oi from w− to w+ , the endpoints occur in the orders

                             upper arc:   w− −→ ai−1 −→ ai −→ w+ ,
                             lower arc:   w− −→ bi−1 −→ bi −→ w+ ,

where the two middle endpoints may coincide. The arcs between them are exactly the upper and
lower rails.
   Writing |pq|
             b for arclength along the indicated upper or lower arc of ∂Oi , in the direction from
w− to w+ , the rail lengths are

                                      a\
                                       i−1 ai = w
                                                [− ai − w\
                                                         − ai−1 ,

                                       i−1 bi = w− bi − w− bi−1 .
                                      b\        [        \

Each rail length is thus the difference of two arclength coordinates measured from the same point
w− on the same circle. When the two rail endpoints coincide, that difference is zero.

Proof. By Lemma 4.1, the incoming cap contains w− in its relative interior and excludes w+ , while
the outgoing cap contains w+ in its relative interior and excludes w− .
    Follow the upper arc of ∂Oi from w− to w+ . By Definition 3.1(ii), this arc meets ∂Oi−1 only at
ai−1 and ∂Oi+1 only at ai . Each power is continuous along the arc and can change sign only at
its zero. The incoming cap therefore occupies the part from w− to ai−1 , while the outgoing cap

                                                    11
occupies the part from ai to w+ . On the lower arc, the respective intersections are bi−1 and bi , so
the incoming and outgoing parts run from w− to bi−1 and from bi to w+ .
    Strong cap-disjointness determines the order of these endpoints. If ai came before ai−1 on the
upper arc, the open arc between them would lie in the relative interiors of both caps. An ordering
with bi before bi−1 would give the same overlap on the lower arc. This proves the two stated orders,
allowing the middle endpoints to coincide. The rails are the arcs between the caps, so additivity of
arclength along each side gives the two displayed differences, including the zero-length case.

Definition 4.3 (step). A step from si = (Oi+1 , Gi , δi ) chooses a disk Oi+2 such that (Oi+1 , Oi+2 )
is a properly crossing forward pair at a gate Gi+1 of length gi+1 > 0 whose crossing satisfies
x(ci+1 ) > x(ci ), with the outgoing cap on Oi+1 strongly disjoint from the stored incoming cap.
Let αi+1 , βi+1 ≥ 0 be the lengths of the upper and lower rails on Oi+1 identified by Lemma 4.2,
connecting ai to ai+1 and bi to bi+1 , respectively. Let ∆xi = x(ci+1 ) − x(ci ) > 0.
    On each disk, its two rails are the only edges connecting the earlier and later parts of the ladder.
Removing them separates these parts, so they form a cut with two edges. This also applies to the
rails incident with the source or terminal.
Lemma 4.4 (two-edge cut). Consider a prefix ladder with a target at either endpoint of its last
gate, or a complete ladder with the terminal as target. Every simple path from the source to the
target uses exactly one of the two rails on each disk, traversing it from the earlier part to the later
part of the ladder. With nonnegative edge weights, some shortest such walk is a simple path.
Proof. Fix a disk in the ladder and remove its two rail edges. The remaining graph has an earlier
part containing the source and a later part containing the target. The target is in the later part
because it lies at the last gate of the prefix, or is the terminal of the complete ladder. The two
removed rails are the only edges joining these parts.
    Take any simple path from the source to the target. Each time it traverses one of these two rails,
it changes from one part to the other. It starts in the earlier part and ends in the later part, so it
must traverse the cut an odd number of times. A simple path repeats no vertex and hence uses
each edge at most once. Since the cut has only two edges, it can be traversed at most twice. The
only odd possibility is one traversal, which goes from the earlier part to the later part. Applying
this argument to each disk proves the assertion about every simple path.
    To prove the shortest-walk assertion, start with any walk from the source to the target. If it
visits a vertex twice, the portion between those visits starts and ends at the same vertex. Deleting
that portion preserves the endpoints of the walk. Its length is nonnegative, so the deletion does not
increase the total length, even when the deleted portion has length zero. Repeating this operation
produces a simple path of length at most that of the original walk.
    The ladder is a finite graph, so it has only finitely many simple paths between the source and
target. Choose one of minimum length. Every walk reduces to a simple path of at most its length,
and that simple path is at least as long as the chosen minimum. Thus the chosen path is also a
shortest walk among all walks from the source to the target.

    The recursion below uses distances to the endpoints of the last gate of the current prefix ladder,
as required by Lemma 4.4. In a completed ladder, a path to an earlier gate may visit later gates
and return; for such a target, the source and target lie on the same side of a later cut.
Lemma 4.5 (exact updates). For a prefix ending at gate i, a step as in Definition 4.3 gives the
new shortest distances
                                                −
                       d+           +
                                                                 
                        i+1 = min di + αi+1 , di + βi+1 + gi+1 ,
                                                                                            (8)
                       d−           −           +
                                                                 
                        i+1 = min di + βi+1 , di + αi+1 + gi+1 .


                                                  12
Proof. The enlarged prefix adds three edges to the old prefix: the upper rail from ai to ai+1 , of
length αi+1 ; the lower rail from bi to bi+1 , of length βi+1 ; and the new gate from ai+1 to bi+1 , of
                                    −
length gi+1 . Recall that d+
                           i and di are distances in the old prefix from the source u to ai and bi ,
respectively.
    We first compute the distance to the new upper endpoint ai+1 . By Lemma 4.4, a shortest walk
to this endpoint can be chosen to be a simple path. It uses exactly one of the two new rails, in the
forward direction. Before that crossing it stays in the old prefix; afterwards it stays on the side
consisting of the two new endpoints and their gate.
    If the path uses the upper rail, its part in the old prefix ends at ai and has length at least d+ i .
                                                                                          +
Traversing the rail adds αi+1 and reaches the target, so the total length is at least di + αi+1 .
    If the path uses the lower rail, its part in the old prefix ends at bi and has length at least d− i .
The rail adds βi+1 and reaches bi+1 . On this side of the cut, the only edge leading to the target ai+1
is the new gate. The path therefore also pays gi+1 , giving a total length of at least d−
                                                                                        i + βi+1 + gi+1 .
These two cases exhaust the possible rail crossings, so
                                                         −
                              d+            +
                                                                         
                               i+1 ≥ min di + αi+1 , di + βi+1 + gi+1 .

    Both candidate lengths can also be realized. A shortest path in the old prefix from u to ai ,
followed by the upper rail, has length d+ i + αi+1 . A shortest path in the old prefix from u to bi ,
followed by the lower rail and then the new gate, has length d−  i + βi+1 + gi+1 . Both are walks to
ai+1 in the enlarged prefix. Its shortest-path distance is at most either length, so
                                                      −
                             d+            +
                                                                       
                              i+1 ≤ min di + αi+1 , di + βi+1 + gi+1 .

The two inequalities prove the first line of (8).
    For the new lower endpoint bi+1 , choose a simple shortest path and apply Lemma 4.4 again.
If it uses the lower rail, it reaches the target directly and has length at least d− i + βi+1 . If it
uses the upper rail, it reaches ai+1 and then traverses the new gate to bi+1 , giving length at least
d+
 i + αi+1 + gi+1 . Hence

                              d−           −          +
                                                                     
                               i+1 ≥ min di + βi+1 , di + αi+1 + gi+1 .

A shortest old-prefix path to bi followed by the lower rail realizes the first length. A shortest
old-prefix path to ai followed by the upper rail and the new gate realizes the second. Thus
                             d−          −            +
                                                                     
                              i+1 ≤ min di + βi+1 , di + αi+1 + gi+1 ,

which proves the second line of (8).
   We now express this update in terms of the ledger and balance. Recall from (5)       that d+
                                                                                              i = µi +δi /2
and d−
                                                                                    
     i =   µi − δi /2. We use t+ =  max(t, 0) and  clip[a,b] (t) = max a,  min(b, t)  .  For any reals a, b
and g ≥ 0,
                       min(a, b + g) − min(b, a + g) = clip[−g,g] (a − b),
                                                                              
                       min(a, b + g) + min(b, a + g) = a + b − |a − b| − g + .
These identities follow by considering a − b < −g, |a − b| ≤ g, and a − b > g; the expressions agree
                                                           −
at the two boundaries. In (8), take a = d+ i + αi+1 , b = di + βi+1 , and g = gi+1 . Their difference
is δi + αi+1 − βi+1 , and their sum is 2µi + αi+1 + βi+1 . Thus the balance update and the ledger
increment are                                                   
                               ωi+1 = |δi + αi+1 − βi+1 | − gi+1 + ,
                                δi+1 = clip[−gi+1 ,gi+1 ] (δi + αi+1 − βi+1 ),                          (9)
                                        αi+1 + βi+1 − ωi+1
                                   ji =                         .
                                                  2

                                                     13
The sum of the updated distances is a+b−ωi+1 ; halving it gives the new ledger µi +ji . Consequently,

                      µi+1 = µi + ji ,      δi+1 = clip[−gi+1 ,gi+1 ] (δi + αi+1 − βi+1 ).            (10)

The next state is si+1 = (Oi+2 , Gi+1 , δi+1 ). The clipping gives |δi+1 | ≤ gi+1 .
   For fixed rail and gate lengths, (9) shows that the balance δi determines the new balance δi+1
and the ledger increment ji . The ledger is then updated by µi+1 = µi + ji . This explains why the
gate state records δi while µi is kept separately.

Initialization. An initialization chooses a properly crossing forward pair (O1 , O2 ) at a gate G1
and takes u = w− (O1 ). By Lemma 4.1, u lies strictly outside O2 , so it is an allowed source. With
α1 , β1 denoting the lengths of the two rails on O1 from u to the tags of G1 , the first two distances
are
                         d+
                          1 = min(α1 , β1 + g1 ),     d−
                                                       1 = min(β1 , α1 + g1 ).

Each minimum compares reaching the endpoint along its own rail with taking the other rail and
then the gate. Applying the same sum and difference identities gives
                                                                                    α1 + β1 − ω1
              ω1 = |α1 − β1 | − g1 + ,     δ1 = clip[−g1 ,g1 ] (α1 − β1 ),    µ1 =                .   (11)
                                                                                          2
The initial state is s1 = (O2 , G1 , δ1 ), with ledger µ1 .

Termination. A termination at s = (O, G, δ) takes v = w+ (O). This point lies strictly outside
every admissible predecessor by Lemma 4.1, so it is an allowed terminal. Let αend , βend be the
lengths of the two rails from the tags of G to v. If the prefix distances are µ + δ/2 and µ − δ/2, the
two candidate lengths to v are
                                          δ                      δ
                                     µ+     + αend ,        µ−     + βend .
                                          2                      2
By Lemma 4.4, the shortest completed path has the smaller of these lengths. Its length is µ + κend ,
where                                       δ           δ      
                               κend = min      + αend , − + βend .                             (12)
                                             2           2
For a chain ending after gate n − 1, this is

                                          PO (u, v) = µn−1 + κend .                                   (13)

   These formulas hold when a rail has length zero, when |δi | = gi , when δi + αi+1 − βi+1 = ±gi+1 ,
and when two shortest paths tie.

4.2    Three local inequalities
Definition 4.6 (feasible potential). Let U ∈ R. A feasible potential at level U is a finite real-valued
function W on gate states, invariant under orientation-preserving isometries fixing the query line
and homogeneous of degree one under positive scaling of all lengths and of δ, such that the following
hold on their entire domains.
                              
         µ1 − U x(c1 ) − x(u) + W (s1 ) ≤ 0          for every initialization,                       (I)
          ji − U ∆xi + W (si+1 ) − W (si ) ≤ 0                for every state and every step,         (E)
                      κend − U L+ − W (s) ≤ 0                 for every state and its termination.    (T)

                                                       14
   (a)    Local comparisons along the query line
                                                                 Pn−2                    
          +W (s1 )                W (s2 ) − W (s1 )               i=2 W (si+1 ) − W (si )                  −W (sn−1 )
     0               W (s1 )                          W (s2 )                                 W (sn−1 )                  0
                                                                             ···
            (I)                         (E)                     (E) at each remaining step                    (T )
                                                                  Pn−2
    µ1 − U x(c1 ) − x(u)            j1 − U ∆x1                          i=2 (ji − U ∆xi )
                                                                                                          κend − U L+

                                                                             ···
   x(u)              x(c1 )                           x(c2 )                                  x(cn−1 )                  x(v)
   (b)    Every potential cancels; length and progress remain
                           n−2
                                           "                n−2
                                                                        #
                           X                                X
                      µ1 +     ji + κend −U x(c1 ) − x(u) +     ∆xi + L+ ≤ 0
                                      i=1                                          i=1
                              |          {z           }    |                  {z                 }
                                      PO (u,v)                          x(v)−x(u)=∥u−v∥


                                                 =⇒            PO (u, v) ≤ U ∥u − v∥


Figure 3: The three inequalities telescope. Adding (I) at the first gate, one instance of (E) per step,
and (T) at the terminal, every value of W occurs once with each sign and cancels. What survives
is the ladder length against the total progress, and by (13) and (4) that is (6). The constant is U
itself: nothing is repaid at the end (Theorem 4.7).

    The three families range over the full domain of gate states, including every δ ∈ [−g, g]. This
uniform requirement gives the sufficient condition used below.
Theorem 4.7. Let U ≥ π/2 and let W be a feasible potential at level U . Then every chain in Q
satisfies PO (u, v) ≤ U ∥u − v∥.
   Roughly speaking, the proof adds up the three inequalities along the chain and watches the
potential cancel (Figure 3). We carry (I) forward with one instance of (E) per step, which is the
induction below, and close with (T) at the terminal.

Proof. Let n ≥ 2. We claim that for 1 ≤ i ≤ n − 1,
                                                                  
                                              µi − U x(ci ) − x(u) + W (si ) ≤ 0.                                              (14)
At i = 1 this is (I). Assume it at i. The next disk of the chain is a step in the sense of
Definition 4.3: the pair (Oi+1 , Oi+2 ) crosses properly and forward by Definition 3.1(i),(iii), the
new crossing satisfies x(ci+1 ) > x(ci ) by (iv), the two caps on Oi+1 are strongly disjoint, and
the two rails between them have the lengths given by Lemma 4.2. By (10), µi+1 = µi + ji and
δi+1 = clip[−gi+1 ,gi+1 ] (δi + αi+1 − βi+1 ). Adding the instance of (E) for this step to (14) and using
∆xi = x(ci+1 ) − x(ci ) gives (14) at i + 1.
    Now add to (14) at i = n−1 the instance of (T) for the actual terminal, whose L+ = x(v)−x(cn−1 ).
The potential cancels and (13) replaces the ledger by PO (u, v), giving
                                                                 
                                       PO (u, v) − U x(v) − x(u) ≤ 0.
By (4) the bracket is ∥u − v∥. For n = 2 the same computation uses (I) and (T) only. For n = 1
the bound (3) and U ≥ π/2 conclude. All inequalities also hold at equality, including ties among
shortest paths and among the two entries of a minimum.

                                                                   15
   (a)    One ordered family of predecessors                 (b)   The same cap and exposure
                     aG                                                   aG
                                                                                                   always
                                                             incoming cap
                                                                                                  exposed
                 o(Y )             G                                             G
                                                                                     o(X)
                                                  ν∥e
                 o(Z)                                                                                       e
                                  o(X)                                 w−                         w+
                                                                                            O

                          bG                                                bG

          On the perpendicular bisector of G,                           The same incoming cap
      predecessor centers lie strictly behind o(X).                      for every predecessor.
                     Z<Y <X                                         w+ ∈
                                                                       / O(Y )     for every Y < X


Figure 4: The predecessor of a state does not affect what the state can do. (a) The circles through
the fixed chord G have their centers on its perpendicular bisector, and (15) indexes them by the
signed position X of the center along it; a disk is an admissible predecessor exactly when its
parameter is strictly behind that of the current disk. (b) Every one of them cuts the same incoming
cap out of ∂O, namely the arc on the far side of the supporting line of G, and leaves the forward
query point w+ outside. So the rails a step produces, and the availability of a termination, are the
same for all of them (Lemma 4.8).


4.3      Forgetting the predecessor
A state records no predecessor. What has to be checked is that the operations available at a state
do not depend on which disk preceded it, and that nothing is lost by working with the state alone.
    The candidates for a predecessor all pass through the two gate tags, so it costs nothing to
describe them all at once. Write M = (aG + bG )/2 for the midpoint of the gate and ν for the unit
normal of G with ν · e > 0. A circle through aG and bG has its center on the perpendicular bisector
of G, so those circles form the one-parameter family
                                            p             
                          O(X) = M + Xν, X 2 + (g/2)2 ,            X ∈ R,                      (15)

and the current
        p       disk is the member at one parameter, which we call X; accordingly o = M + Xν
and r = X + (g/2)2 .
            2


Lemma 4.8 (the predecessor fiber). The disks admissible as a predecessor of a state are exactly
the members O(Y ) of (15) with Y < X. All of them cut the same incoming cap out of the current
circle, namely the arc on the far side of the supporting line of G. The forward query point w+ lies
strictly outside every one of them, and each of their backward query points lies strictly outside O
(Figure 4).
Proof. Every claim is a sign reading of one identity. For any real Y , subtracting the powers of the
two members of (15) at an arbitrary point z cancels the quadratic terms and leaves

                            powO(Y ) (z) − powO(X) (z) = 2(X − Y ) ν · (z − M ).                            (16)

The second factor is the signed height of z above the supporting line of G; the parameter Y enters
only through the scalar X − Y .

                                                        16
     Which members are predecessors. The right side of (16) vanishes exactly on
                                                                               that supporting line,
so two members meet only at aG and bG . Forwardness reads e · o(X) − o(Y ) = (X − Y )(e · ν) > 0,
which is Y < X. Such a pair crosses properly: the two centers are distinct and neither disk contains
the other, both circles passing through aG and bG , so the two strict inequalities of Definition 3.1(i)
are the triangle inequalities in the nondegenerate triangle o(X), o(Y ), aG .
     Why the cap is the same for all of them. By (16) a point z ∈ ∂O lies in O(Y ) precisely when
ν · (z − M ) ≤ 0, a condition in which Y does not appear. That half-plane cuts the stated arc out of
∂O, the same arc for every predecessor.
     Exposure. For every Y < X, the pair (O(Y ), O(X)) crosses properly and is directed forward, as
proved above. Applying Lemma 4.1 gives w+ (O(X)) ∈      / O(Y ) and w− (O(Y )) ∈  / O(X), which are
the two exposure statements.

    So the incoming cap, the gate tags, and hence the two rail lengths produced by any step are the
same for every admissible predecessor; and by Lemma 4.8 a termination is always available, so the
constructions in Section 4.1 give the operations an actual chain can perform at that state.
    Theorem 4.7 shows that a feasible potential at level U ≥ π/2 implies (6) for every chain in Q.
Section B proves the converse.
    Finally, invariance and homogeneity let us normalize the radius and the position of the query
line once and for all, after which only the shape of a state remains. Section 5 records that shape by
four angles and turns (E) into a pointwise condition on them.


5     Reduction to a Univariate Linear Program
Theorem 4.7 leaves one task: exhibit a feasible potential. We split each step into two comparisons:
first from the incoming to the outgoing gate on the current circle, then between the current and next
disks through the fixed outgoing gate. A derivative controls the second comparison. Together with
the exact distance update, these comparisons reduce the task to a family of pointwise inequalities on
a compact four-dimensional domain, indexed by four angles, in which the unknown enters through
the values of a single function of one variable and its first derivative.
     The reduction takes four steps. First, invariance and homogeneity compress a gate state to four
angles ranging over a compact set (Section 5.1). Second, the disks through the outgoing gate form a
one-parameter family, along which we differentiate the potential (Section 5.2). Third, requiring this
derivative to be nonpositive controls the change of disk; the comparison on the old circle uses angular
monotonicity and a Lipschitz bound in the balance, and together they imply (E) (Section 5.3).
Fourth, fixing the shape of the potential up to one even function of γ makes all the conditions affine
in that function and its derivative, which is the linear program (Section 5.4). Theorem 5.7 is the
endpoint.

5.1   Normalized states and the closed angular domain
Invariance and homogeneity reduce the geometric data of a gate state to its shape, together with
the normalized balance. We record that shape by four angles, and the domain they range over by a
closed set of angles that is easier to certify over than the states themselves.
    Normalize once and for all: put the query line on y = 0 with e = (1, 0) and set r = 1. What is
then left of a state is a shape, and three angles describe it — how high the center sits above the
query line, which way the gate faces, and how much of the circle the gate cuts off — while a fourth




                                                  17
records the balance in the same angular units. In order:
                   y(o)                                              X               g              δ
      γ = arcsin        ,   φ = the direction of ν,        cos θ =     ,   sin θ =      ,   ψ =φ+      ,
                    r                                                r               2r             2r
where ν = (cos φ, sin φ) is the gate normal with positive forward component and X is its parameter
in (15). These ranges are forced: |γ| < π/2, −π/2 < φ < π/2 and 0 < θ < π. We call ψ the
normalized balance; the stable range |δ| ≤ g reads |ψ − φ| ≤ sin θ. These four numbers carry every
state from here to the end of the paper.

Lemma 5.1 (arc coordinates and the angular domain). The actual upper and lower arc coordinates
of the gate tags, measured from w− , are

                                  l+                       l−
                                     = θ + γ − φ,             = θ − γ + φ,                                 (17)
                                   r                        r
and the two tags lie strictly above and below the query line if and only if

                                        |γ − φ| < θ < π − |γ + φ|.                                         (18)

Conversely every triple with |γ|, |φ| < π/2 satisfying (18), together with every ψ in the stable range,
is realized by a gate state. Moreover the two arcs from w− to w+ have total angular lengths π + 2γ
and π − 2γ, so the terminal rails have lengths

                            αend = r(π + 2γ) − l+ ,        βend = r(π − 2γ) − l− .                         (19)

Proof. The radial vectors of the upper and lower tags have polar lifts π + φ − θ and π + φ + θ,
while w− has lift π + γ; the upper arc runs clockwise and the lower counterclockwise from it, giving
(17) with the actual, possibly major, lengths. The upper tag is strictly above the line exactly when
0 < l+ /r < π + 2γ, and similarly below for the lower tag; these four strict inequalities are (18). For
the converse, take r = 1, o = (0, sin γ), M = o − cos θ ν, and the two tags at M ± sin θ (− sin φ, cos φ),
displaced from the gate midpoint along the gate itself; the same lifts show the tags are strictly
on their respective sides, and the gate length is 2 sin θ, which is the stable range. The final claim
follows since w± have lifts π + γ and −γ.

    For a fixed γ, (18) describes the interior of a convex quadrilateral in (φ, θ), the angular diamond,
with vertices                                    π π              π π        
                       (γ, 0),     (−γ, π),          , −γ ,         − , +γ .                        (20)
                                                   2 2                2 2
Let C denote the closed angular domain: all (γ, φ, θ, ψ) with |γ|, |φ| ≤ π/2, 0 ≤ θ ≤ π, |γ − φ| ≤
θ ≤ π − |γ + φ| and |ψ − φ| ≤ sin θ. This closed set is a sufficient test domain: verifying an
inequality on all of C implies it at every gate state, with the additional faces serving as boundary
test configurations.

5.2     Transport along a gate pencil
Fix a gate, the query line, and a balance δ with |δ| ≤ g, and let the current disk run along the family
(15) as X varies over R. We call this family the gate pencil of that gate (Figure 5). By Lemma 4.8,
the next disk in the second comparison has a larger value of X. To control this comparison, we
require the potential to be nonincreasing along the pencil. The crossing c is interior to the gate
chord and stays fixed, so its power is negative in every disk of the pencil; hence every closed finite
interval of X stays inside the strict domain, with r ≥ g/2 > 0 and cos γ > 0 throughout.

                                                      18
Lemma 5.2 (pencil derivatives). Along the pencil, at fixed gate, query line and dimensional balance,
                                                                   sin φ − sin γ cos θ
      rX = cos θ,              r θX = − sin θ,            r γX = A :=                  ,
                                                                          cos γ                    (21)
   r ψX = − cos θ (ψ − φ), (rθ)X = θ cos θ − sin θ, (L− )X = − cos φ + cos θ cos γ − sin γ A.

Proof. Differentiate r2 = X 2 + (g/2)2 for the first, and θ = atan2(g/2, X) for the second. For
γ, differentiate r sin γ = y(M ) + X sin φ and substitute the first two. For ψ, use ψ = φ + δ/(2r)
with φ and δ fixed. For the fifth, l+ + l− = 2rθ by (17). For the last, L− = x(c) − x(o) + r cos γ
has derivative − cos φ + cos θ cos γ − sin γ A, and a direct computation identifies this with (cos θ −
cos(γ − φ))/ cos γ.

    The potentials we shall use are built from a piecewise smooth function, so we record the
differentiation rule that applies to them.
Lemma 5.3 (curve lemma). Let F be locally Lipschitz on a neighborhood of the image of a C 1 curve
ξ defined on a compact interval. Suppose finitely many closed pieces cover that neighborhood, on
each piece F agrees with a C 1 function defined on an open neighborhood of that piece, and the values
agree on overlaps. Then F ◦ ξ is absolutely continuous, and at almost every parameter where its
derivative exists, that derivative equals ∇Fi (ξ) · ξ ′ for some piece i containing ξ at that parameter.
Proof. Compactness gives a finite Lipschitz cover of the image, so F ◦ ξ is Lipschitz on the parameter
interval and hence absolutely continuous. Fix a parameter of differentiability and let ι → 0 through
nonzero values; write ξ and ξι for the points of the curve at that parameter and at the shifted
one. Since there are finitely many closed pieces, a subsequence has all ξι in one closed piece, and
closedness puts ξ in it too. On that piece
                                                                            
                           F (ξι ) − F (ξ) = ∇Fi (ξ) · (ξι − ξ) + o ∥ξι − ξ∥ ,

and ∥ξι − ξ∥ = O(|ι|), so dividing by ι and passing to the limit along the subsequence gives the
stated value, which must be the existing derivative.

    Consequently a bound imposed on every incident gradient controls the actual derivative almost
everywhere. This covers a curve lying along a switching locus for an interval, or crossing it infinitely
often.

5.3    The step residual
Before fixing the form of the potential, note what it has to do. By (T) a state must already pay
for terminating there, and by (19) that price is at most rπ against a progress of L+ ≤ 2r cos γ; the
corresponding requirement on the potential is what the first bracket below records, so r π/2−U cos γ
is the price of a state at which the free part of the potential is zero. The remaining two terms are
bookkeeping: −rθ records how much of the circle the gate has already cut off, and U L− how far
the crossing has advanced. What is left free is a single dimensionless function H, which measures
the slack of the fit.
    Let H be a function of (γ, φ, θ, ψ), to be chosen, and set
                                      hπ                i
                               W =r       − U cos γ − H − rθ + U L− .                            (22)
                                        2
This is finite, invariant, and homogeneous of degree one, because γ, φ, θ, ψ are dimensionless while
r, l± , L− and δ scale by the common factor.

                                                  19
   (a)        First comparison: the old circle                          (b)    Second comparison: the gate pencil
                      αi+1                                                              ai+1
         ai                           ai+1
                                                    αi+1 + βi+1
                             r               θ∗ − θ =                                                   Gi+1
                      O                                  2r
                       o                              α    − βi+1                o(X0 )                 o(X1 )
   Gi                        Gi+1                      i+1                                       M
                                           φ∗ − φ = −                                                            ν
                       ∆xi                                 2r
                                             e                                                          ci+1
                 ci     ci+1                                                                                         e
                                             ∆xi = x(ci+1 ) − x(ci )
                                           gi+1
          bi
                      βi+1          bi+1                                               bi+1
                                                                                              X0 < X1
    Traverse both rails; allow a switch across the gate.

                                           ji − U ∆xi + W∗ − W (si ) + W (si+1 ) − W∗ ≤ 0
                                           |          {z          } |        {z     }
                                                  rails and gate              pencil

                             Each bracket is nonpositive; the derivative WX = E controls the second.


Figure 5: A step is two comparisons, not one. (a) On the old circle the two complete rails αi+1 , βi+1
are traversed and one update across the outgoing gate accounts for switching sides, as in (9); the
disk is unchanged, and the increments of the gate angles are (27). Write W∗ for the potential
at the outgoing gate on that same disk. (b) The outgoing gate Gi+1 and the balance are then
held fixed while the disk moves forward along the pencil (15), its center advancing from o(X0 ) to
o(X1 ) along the perpendicular bisector of Gi+1 and its radius varying according to (15). Each of
ji − U ∆xi + W∗ − W (si ) and W (si+1 ) − W∗ is nonpositive, and their sum is (E) (Proposition 5.5).


Definition 5.4 (step residual). With K(θ) = cos θ (π/2 − θ) + sin θ, the step residual of H at a
state and at one incident gradient of H is

                       E = K(θ) − U cos φ − cos θ H + cos θ (ψ − φ)Hψ − A Hγ + sin θ Hθ ,                                (23)

where subscripts denote partial derivatives at fixed remaining variables and A is as in (21). Its
cleared form, obtained by multiplying by cos γ and substituting A from (21),
                                                                                      
  Ee = cos γ K(θ) − U cos φ − cos θ H + cos θ (ψ − φ)Hψ + sin θ Hθ − sin φ − sin γ cos θ Hγ , (24)

carries no denominator.
    The two forms are used for different purposes. The coefficient A of (21) divides by cos γ, which
is positive at every gate state but vanishes at the two faces γ = ±π/2 of the closed domain C;
there both the numerator and the denominator of A vanish, and the quotient has no continuous
extension, since along γ = π/2 − t, θ = π/2, φ = vt one gets A → v for every v ∈ (−1, 1). So E is
the derivative residual, defined wherever cos γ > 0, and E
                                                         e is the quantity a closed-domain condition
can require: it is defined on all of C, and at a point with cos γ > 0 the two conditions E ≤ 0 and
Ee ≤ 0 are equivalent. Statements about C below are therefore stated for E. e

Proposition 5.5 (the step inequality is a pointwise condition). Suppose H is continuous, locally
Lipschitz in ψ on the whole real fiber, and covered by finitely many closed pieces on each of which it
agrees with a C 1 function, with matching values on overlaps. Suppose further that

                             |H(γ, φ, θ, ψ) − H(γ, φ, θ, ψ)|
                                                         e ≤ |ψ − ψ|
                                                                  e                    for all real ψ, ψ,
                                                                                                       e                 (25)

                                                                   20
that
                                       Hθ ≥ |Hφ |          at fixed γ, ψ,                               (26)
at every incident gradient, on the closed angular diamond of every γ and for every real ψ, and that
Ee ≤ 0 at every point of C and at every incident gradient. Then (E) holds for every gate state and
every step.

    The proof compares the two ends of a step in two moves (Figure 5): first along the old circle,
from the incoming to the outgoing gate, then along the pencil of the outgoing gate. The larger fiber
in (25) and (26) is needed because the first move initially carries the raw balance, before accounting
for a possible switch across the outgoing gate, so the pair it compares can leave the stable range.

Proof. Fix a step si → si+1 , O = Oi+1 .
    Along the old circle. By Lemma 4.2, the outgoing gate has arc coordinates l+ + αi+1 and
l− + βi+1 on O. Its crossing advances by ∆xi . Write φ∗ , θ∗ for the angles of the outgoing gate on O;
by (17) the two increments mean

                                     αi+1 + βi+1                        αi+1 − βi+1
                          θ∗ − θ =               ,         φ∗ − φ = −               .                   (27)
                                         2r                                 2r
Before allowing a switch across the outgoing gate, the carried balance is δi + αi+1 − βi+1 , and
(δi + αi+1 − βi+1 )/(2r) + φ∗ = δi /(2r) + φ = ψ: the raw normalized balance is unchanged. Allowing
such a switch gives δi+1 = clip[−gi+1 ,gi+1 ] (δi + αi+1 − βi+1 ) with |δi + αi+1 − βi+1 − δi+1 | = ωi+1 , so
the new normalized balance ψ ∗ differs from ψ by ωi+1 /(2r). By (25),
                                                                         ωi+1
                             −r H(γ, φ∗ , θ∗ , ψ ∗ ) − H(γ, φ∗ , θ∗ , ψ) ≤
                               
                                                                               .                        (28)
                                                                           2
Writing W∗ for (22) evaluated on the old circle at the outgoing gate, γ and r are unchanged, rθ
increases by (αi+1 + βi+1 )/2 by (27), and U L− increases by U ∆xi . Hence, using ji = (αi+1 + βi+1 −
ωi+1 )/2,
                                            ωi+1
                                                  −r H(γ, φ∗ , θ∗ , ψ ∗ ) − H(γ, φ∗ , θ∗ , ψ)
                                                                                            
              ji − U ∆xi + W∗ − W (si ) = −
                                          | {z2 } |                   {z                     }
                                                (a)                         (b)

                                             −r H(γ, φ∗ , θ∗ , ψ) − H(γ, φ, θ, ψ) .
                                                                                
                                             |                 {z                }
                                                                  (c)

The two terms (a) + (b) are ≤ 0 by (28). Term (c) compares H at two angular pairs of the same γ,
and it is ≤ 0 because H does not decrease along the straight segment joining them.
    Both pairs lie in the closed diamond of that γ, by Lemma 5.1 applied on O to the two chords
Gi and Gi+1 , whose arc coordinates are l± and l+ + αi+1 , l− + βi+1 : the tags of Gi straddle the
query line because si is a gate state, and those of Gi+1 because si+1 is one. That diamond is convex,
so the segment stays in it, and along the segment θ̇ ≥ |φ̇| by (27) and αi+1 , βi+1 ≥ 0. Applying
Lemma 5.3 to H along that segment, at the fixed γ and the fixed raw balance ψ, at almost every
parameter its derivative is Hθ θ̇ + Hφ φ̇ at some incident gradient, and
                                                                           
                       Hθ θ̇ + Hφ φ̇ ≥ Hθ θ̇ − |Hφ | |φ̇| ≥ |Hφ | θ̇ − |φ̇| ≥ 0

by (26) and θ̇ ≥ |φ̇| ≥ 0. So H does not decrease and (c) ≤ 0. The segment compares function
values along the old circle, while the ladder update remains the single move in (9).


                                                      21
    Along the pencil. It remains to compare the old circle with the new one through the common
outgoing gate, at the fixed balance δi+1 . By Lemma 4.8 the two center parameters satisfy X0 < X1 ,
so it suffices to show that W is nonincreasing in X along the pencil. Substituting (21) into (22)
and applying Lemma 5.3 to H along the pencil curve, which is C 1 with compact image inside the
strict domain, gives at almost every X, for some incident gradient,

             WX = K(θ) − U cos φ − cos θ H + cos θ (ψ − φ)Hψ − A Hγ + sin θ Hθ = E,
                                                                                
where the terms in U cancel to −U cos φ since U − cos θ cos γ + sin γ A + (L− )X = −U cos φ. Every
                                                                           e ≤ 0 gives E ≤ 0 at every
point of the pencil is a gate state, so cos γ > 0 there and the hypothesis E
incident gradient; hence WX ≤ 0 almost everywhere. W is absolutely continuous along the pencil by
Lemma 5.3, so W (X1 ) ≤ W (X0 ). The comparison holds for every positive radius ratio ri+2 /ri+1 .
    Combining the two moves gives (E).

   The term sin θ Hθ in (23) comes from −rH in (22) through the chain term −rHθ θX and
rθX = − sin θ, so it enters with a plus sign; the derivative of −rθ is −θ cos θ + sin θ, which K(θ)
absorbs.

5.4   Amplitude profiles and the sufficient conditions
We now fix the shape of H, leaving one function of one variable free. Two quantities of γ alone are
needed first: a threshold at which the balance saturates, and a smoothed |γ| that stays away from
zero at γ = 0. Fix a smoothing parameter ε ∈ (0, 1] and put, for |γ| ≤ π/2,
                                  π                  p
                              k = − cos γ,       h = γ 2 + ε2 cos2 γ,
                                  2
the parameter ε being what keeps h positive at γ = 0. Everything below holds for every such ε; a
specific value is chosen only in Theorem 6.4.
    Our idea is to let one free function do three jobs. The balance term has to absorb the clipping
that occurs when the balance saturates, so it is odd in ψ and constant beyond ±k. The angular
term has to stay monotone when a pair of complete rails is traversed, which is the inequality (26);
making it affine in (φ, θ) at fixed γ is what puts that inequality in closed form. Both terms are
scaled by one even function w of γ, and that function is the only thing left to choose.
Definition 5.6 (amplitude profile). An amplitude profile is an even C 2 function w on [−π/2, π/2],
understood with C 2 extensions through the two endpoints. Together with the smoothing parameter
ε it determines the two terms
                   ψ               h          π     i                  h           π i
 H0 = σ clip[−1,1]       with σ = γ 1 − w cos γ    −h ,         J = w cos γ γφ + h θ −       , (29)
                    k                            2                                      2
and H = H0 + J in (22). So the profile enters the first through the amplitude σ, which discounts γ
by the weight cos γ (π/2 − h), and the second as the amplitude of an affine function of (φ, θ).
     We call H0 the balance term and J the angular term, and they behave as the three jobs above
require. The balance term has three closed branches, ψ ≤ −k, −k ≤ ψ ≤ k and ψ ≥ k, on which it
equals −σ, mψ and σ, where
                                                     σ
                                                m=                                              (30)
                                                     k
is its slope on the central branch; both incident gradients are required at each of the two switches
ψ = ±k(γ), including when one branch meets the stable range in a single point. The angular term
is affine in (φ, θ) at fixed γ, which is what makes (26) checkable in closed form.

                                                 22
   The following elementary bounds hold for 0 < ε ≤ 1 and will be used throughout:
                                        π                       π
                    h ≥ ε,    |γ| ≤ h ≤ ,      k ≥ |γ|,    k ≥ − 1 > 0.                              (31)
                                        2                       2
Indeed h2 − ε2 = γ 2 − ε2 sin2 γ ≥ 0; the function γ 2 + cos2 γ has derivative 2γ − sin 2γ ≥ 0 on [0, π/2]
and endpoint value (π/2)2 , giving h ≤ π/2; and k − γ has derivative sin γ − 1 ≤ 0 with endpoint
value zero, giving k ≥ |γ| after reflection. So k and h are positive and smooth on a neighborhood of
the closed interval.
Theorem 5.7 (sufficient conditions, affine in the profile). Let U ≥ π/2, let ε ∈ (0, 1], and let w be
an amplitude profile. Suppose that for every γ ∈ [0, π/2],
                                               π     
               w ≥ 0,                  w cos γ    − h ≤ 1,                  m′ ≥ 0,               (S)
                                                2
with m the central slope (30), and that, with the two vertex values of (34) below,
                   π             γσ                       π      π     
                     − U cos γ −     + w cos γ max γ 2 − h , γ        − h ≤ 0,                        (S′ )
                   2              k                        2        2
                                           e of H = H0 + J is nonpositive at every point of C and
and suppose that the cleared step residual E
every incident gradient. Then (22) is a feasible potential at level U , and consequently
                                          dD (p, q) ≤ U ∥p − q∥                                      (32)
for every finite set of distinct non-collinear planar points, every specified straight-line Delaunay
triangulation D of it, and every pair of its points.
Proof. Finiteness, invariance and homogeneity were noted after (22).
    The fiber bound and the angular term. For γ ≥ 0, the second condition in (S) and h ≤ π/2
bound the bracket of σ in (29) between 0 and 1, so 0 ≤ σ ≤ γ ≤ k. Since w is even, σ is odd, so
|σ| ≤ k on the whole interval, which is exactly (25) for H0 because clip has Lipschitz constant one
in ψ/k and |σ/k| ≤ 1; as J is constant in ψ, (25) holds for H. Also, by w ≥ 0 and h ≥ |γ|,
                          Hθ = Jθ = w cos γ h ≥ |w cos γ γ| = |Jφ | = |Hφ |,                         (33)
on the closed diamond of every γ. Since H0 does not depend on φ, θ, these two partial derivatives
are the same at every incident gradient and for every real ψ, so (33) is (26) on the domain
Proposition    5.5 requires. For an actual pair of complete rails the increment of J is in fact J ∗ − J =
w cos γ                            
  2r      (h − γ)αi+1 + (h + γ)βi+1 ≥ 0, by (27).
    Regularity. The three expressions −σ, σψ/k, σ are C 2 on their closed branches since k, h > 0,
and agree at ψ = ±k. At ψ = k the central and outer gradients in (γ, ψ) differ by (−mk ′ , m), which
annihilates the switch tangent (1, k ′ ); at ψ = −k the analogous difference annihilates (1, −k ′ ). So
the hypotheses of Lemma 5.3 hold, and both incident gradients are genuine separate obligations.
    Steps. Proposition 5.5 applies, using (25), (33) and the assumed sign of E,      e and gives every
instance of (E).
    Initialization. At fixed γ ≥ 0, J is affine on the closed diamond, so by (20) its bracket takes at
the four vertices the values                 π            π      
                                     ± γ2 − h ,         ±γ      −h ,                                  (34)
                                              2              2
two numbers and their negatives. An affine function on a convex polytope attains every value
between its vertex extremes, so the larger of the two absolute values controls the bracket everywhere:
                                           π       π     
                   |J| ≤ w cos γ max γ 2 − h , γ       −h        on the closed diamond,               (35)
                                            2        2

                                                   23
and that maximum is exactly the one appearing in (S′ ). Since |γ| ≤ k we have H0 (γ, γ) = γσ/k, so
(S′ ) is exactly
                                          π
                       H0 (γ, γ) + J ≥      − U cos γ       on the closed diamond.                     (36)
                                          2
Now take an actual initialization and evaluate the geometric quantities on O1 , with ψ = φ + δ1 /(2r).
Its two source rails are the arc coordinates l+ , l− of the first gate, so (11) reads µ1 = (l+ + l− − ω1 )/2
with ω1 = (|l+ − l− | − g1 )+ , and by (17) the raw normalized balance is γ, while the clipped one
differs from γ by ω1 /(2r). Using l+ + l− = 2rθ and (25),
                         hπ                              i ω         hπ                            i
                                                               1
    µ1 − U L− + W = r        − U cos γ − H0 (γ, ψ) − J −          ≤r     − U cos γ − H0 (γ, γ) − J ≤ 0
                           2                                  2        2
by (36). Applying the pencil comparison of Proposition 5.5 from O1 to its actual successor at that
same gate decreases the W term further, which gives (I).
     Termination. By (19) and (17), the symmetric terminal cost is κend = rπ − rθ − r|ψ + γ|, and
L+ = 2r cos γ − L− . Hence
                                               hπ                                   i
                       κend − U L+ − W = r         − U cos γ + H0 + J − |ψ + γ| .
                                                2
Since H0 is odd in ψ, (25) gives H0 (γ, ψ) ≤ H0 (γ, −γ) + |ψ + γ| = −H0 (γ, γ) + |ψ + γ|; adding (35)
and applying (36) shows the bracket is ≤ 0. This is (T), including the case where the two entries of
the minimum tie.
     So W is a feasible potential at level U . Theorem 4.7 gives (6) and Proposition 3.3 gives (32).
    The point of Theorem 5.7 is the shape of its hypotheses. Write χ = clip[−1,1] (ψ/k) for the
saturating factor of the balance term, and collect everything that (29) multiplies by the profile into
                                       h            π     π      i
                             Z = cos γ γφ + h θ −       −γ      −h χ ,
                                                     2       2
                                                        ′
so that H = γχ+w Z and hence Hγ = (γχ)γ +w Zγ +w Z. Substituting into (23) and differentiating
at fixed remaining variables therefore gives, wherever cos γ > 0,
                                   E = R0 + R1 w + R2 w′ − U cos φ,                                    (37)
where R0 , R1 , R2 are explicit functions of (γ, φ, θ, ψ) alone, namely
                       R0 = K(θ) − cos θ γχ + cos θ (ψ − φ)(γχ)ψ − A (γχ)γ ,
                       R1 = − cos θ Z + cos θ (ψ − φ)Zψ − A Zγ + sin θ cos γ h,                        (38)
                       R2 = −A Z.
The third condition of (S) has the same shape. Write Σ = cos γ γ(π/2 − h) for the quantity that
(29) subtracts from γ, so that σ = γ − w Σ; differentiating m = σ/k and using k ′ = sin γ gives
                                   k − γ sin γ  Σ sin γ Σ′          Σ
                              m′ =       2
                                              +       2
                                                         −       w − w′ ,
                                       k            k       k         k
again affine in (w, w′ ); the remaining conditions (S) and (S′ ) are affine by inspection. Multiplying
(37) by cos γ puts the closed-domain condition E   e ≤ 0 in the same form: each coefficient of (38)
carries A only through the product cos γ A = sin φ − sin γ cos θ, so the three cleared coefficients are
defined on all of C.
    So all the hypotheses of Theorem 5.7 are, at each fixed ε and each point of C, closed affine
half-space conditions on the three numbers U, w(γ), w′ (γ) . Minimizing U subject to them is a
linear program whose unknown is a function of one variable and whose constraints are indexed by
the compact set C — a semi-infinite linear program. Section 6 exhibits a spline feasible point of
that program at 33/20.

                                                    24
6     A Certified Spline Profile
Theorem 5.7 turns a bound into a question about one univariate function. This section exhibits a
cubic spline profile feasible at 33/20, proves the main theorem, and certifies the required conditions
over their whole closed domains.

6.1     Endpoint reduction and the two reflections
Before exhibiting the profile, we cut down what has to be checked. Three reductions are available:
eliminate the balance, because the residual is affine in it on each branch; halve the range of γ,
because a reflection preserves everything; and pair up the branch obligations, because a second
reflection interchanges them.
    Fix a closed angular triple and intersect the stable interval [φ − sin θ, φ + sin θ] separately with
each of the three closed branches of H0 , keeping every nonempty intersection, including one that is
a single point. On the central branch H0 = mψ, so by (24) the cleared residual is affine in ψ with
slope −(sin φ − sin γ cos θ)m′ ; on the two outer branches H0 = ±σ it is constant in ψ. An affine
function on a compact interval attains its maximum at an endpoint, so:
Lemma 6.1 (endpoint reduction). Assume m′ ≥ 0. Then E           e ≤ 0 throughout C, at every incident
gradient, if and only if it holds at the following finitely many places for each closed angular triple:
    • the two outer branches, whenever the corresponding intersection is nonempty;
    • the central branch at ψ = φ − sin θ or ψ = −k when sin φ − sin γ cos θ ≥ 0, and at ψ = φ + sin θ
      or ψ = k when sin φ − sin γ cos θ ≤ 0, whichever of the two is the relevant endpoint of the
      central intersection.
When sin φ − sin γ cos θ = 0, either endpoint may be used, so both closed sign domains may be
retained. At ψ = ±k both incident gradients are tested. At γ = ±π/2, (24) gives E
                                                                                e = 0.

   At a switch, the central and outer gradients remain separate verification obligations.
   Two reflections cut the work down further. Both are sign bookkeeping: w is even, hence k and
h are even and σ is odd, and everything else in (23) follows.
Lemma 6.2 (two reflections). Both of the following maps preserve C and E,
                                                                       e and preserve E
wherever cos γ > 0.
    • At fixed θ, the map (γ, φ, ψ) 7→ (−γ, −φ, −ψ). It preserves H and reverses the signs of Hγ , Hψ
      and sin φ − sin γ cos θ.
    • At fixed γ, the map (φ, θ, ψ) 7→ (−φ, π −θ, −ψ). It reverses the signs of H, Hγ , sin φ−sin γ cos θ
      and cos θ, and preserves Hψ , Hθ , K(θ), sin θ and cos φ. It also interchanges the two outer
      branches, interchanges the two switches ψ = ±k, and exchanges the two central endpoints of
      Lemma 6.1 together with their sign domains sin φ − sin γ cos θ ≥ 0 and sin φ − sin γ cos θ ≤ 0.
    The first reflection reduces the work to γ ≥ 0. The second pairs up the six endpoint obligations
of Lemma 6.1, so three of them have to be verified and the other three follow.

6.2     A spline profile and the main theorem
We now construct a spline profile feasible at U = 33/20.
    To satisfy Theorem 5.7, the admissible pairs w(γ), w′ (γ) must be the values and derivatives
                                                              

of one even C 2 function. The affine conditions constrain each pair pointwise, and the spline basis
enforces the required consistency across γ, including the matching conditions at the knots.

                                                    25
    Let Bi = Bi,3 , 0 ≤ i ≤ 6, be the seven cubic clamped B-splines with the exact knot vector
                                                                                        
                              (T0 , . . . , T10 ) = 0, 0, 0, 0, 14 , 12 , 34 , 1, 1, 1, 1 .    (39)

For 0 ≤ τ < 1 and 0 ≤ i ≤ 9, set Bi,0 (τ ) = 1 if Ti ≤ τ < Ti+1 , and Bi,0 (τ ) = 0 otherwise. For
p = 1, 2, 3 and 0 ≤ i ≤ 9 − p, use the Cox recurrence
                                      τ − Ti                  Ti+p+1 − τ
                       Bi,p (τ ) =             Bi,p−1 (τ ) +               Bi+1,p−1 (τ ),                  (40)
                                     Ti+p − Ti               Ti+p+1 − Ti+1

with a term omitted when its denominator vanishes, and with each cubic piece extended to its
closed interval by its own polynomial; in particular τ = 1 is evaluated by the last polynomial.

Lemma 6.3 (coherence). Each Bi is nonnegative, 6i=0 Bi ≡ 1 on [0, 1], and at each of the three
                                                         P
interior knots the values and the first two derivatives of the two adjacent polynomial pieces agree.
The vector of first derivatives at τ = 0 is (−12, 12, 0, 0, 0, 0, 0). Consequently, for any real λ0 , . . . , λ6
with λ0 = λ1 , the function
                                                               6  |γ| 
                                              39   28 2 X
                                     w(γ) =      +    γ + λ i Bi                                           (41)
                                              200 125             π/2
                                                              i=0

is an even C 2 function on [−π/2, π/2] with C 2 extensions through the endpoints.

Proof. Every factor of a nonzero term in (40) is nonnegative on the support of its lower-degree
factor, so nonnegativity follows by induction on p. Summing the cubic coefficients on each of the four
knot intervals gives exactly (1, 0, 0, 0), which is the partition of unity; this is a finite computation
with rational coefficients. The value and two-derivative matchings at the interior knots are likewise
finite rational identities, and they hold for each basis function separately, hence for every real linear
combination. For evenness: the quadratic base has zero derivative at γ = 0, and the correction
has derivative 12(λ1 − λ0 )/(π/2) there, so λ0 = λ1 makes the one-sided first derivatives vanish; the
second derivatives from the two sides agree by the chain rule and the values agree, so the extension
across γ = 0 is C 2 . The outermost polynomial piece extends through γ = ±π/2, giving the required
regularity in a neighborhood.

Theorem 6.4 (main theorem). Let ε = 1/20, U = 33/20, and let w be the profile (41) with
                                                                                   
                       20921     20921     173      2299      1547    28913 60041
               λ = − 500000  , − 500000 , 200000 , 1000000 , 500000 , 100000 , 40000 .                     (42)

Then w satisfies all hypotheses of Theorem 5.7. Consequently, for every finite set S ⊂ R2 of distinct
points not contained in a line, every specified straight-line Delaunay triangulation D of S, and every
p, q ∈ S,
                                            33
                                dD (p, q) ≤    ∥p − q∥ = 1.65 ∥p − q∥ ,                           (43)
                                            20
where the edges of D carry their Euclidean lengths. Arbitrary choices of the diagonals of a cocircular
polygon are included.

Proof. The coefficients satisfy λ0 = λ1 , so Lemma 6.3 makes w an even C 2 amplitude profile.
Nonnegativity of the basis and the partition of unity give the uniform bound
                                      39              76579
                         w(γ) ≥           + min λi =        = 0.153158 > 0,                                (44)
                                      200    i       500000

                                                        26
    (a)       The amplitude profile                                       (b)    The correction at small angles
                                                                                 Spline minus its quadratic base, on 0 ≤ τ ≤ 1/2.

          2                                                                  0




                                                          i λi Bi (τ )
        1.5                                                                                               τ ≈ 0.368
 w(γ)




                                                                         −0.02
          1




                                                          P
        0.5
                  w(0) = 0.153158                                        −0.04
          0
              0        1/4       1/2        3/4       1                          0       1/8        1/4       3/8        1/2

                             τ = γ/(π/2)                                                       τ = γ/(π/2)

Figure 6: The spline profile (41) of Theorem 6.4. (a) The profile on the whole range; dotted lines
mark the three interior knots, the pale region marks the horizontal range used in (b), and the value at
τ = 1 is 2.248723 . . .. (b) The B-spline correction added to the quadratic base 39/200 + (28/125)γ 2 ,
which is where the extra shape freedom acts: it is negative at small angles, crosses zero at τ ≈ 0.368,
and grows to 1.501025 at τ = 1.

which is the first condition in (S). The remaining two conditions in (S), the condition (S′ ), and the
sign of the cleared step residual on C at every incident gradient are verified by rigorous arithmetic
certification on their full closed domains, including switches and boundary cases (Section 6.3). The
reductions of Lemmas 6.1 and 6.2 leave three representative branch obligations and γ ≥ 0, and
all three are covered exhaustively. Since π/2 < 11/7 < 33/20, Theorem 5.7 applies at U = 33/20
and gives (43) with the stated quantifiers. Proposition 3.3 supplies the transfer to D; the walks it
produces use only the mandatory boundary edges of maximal cocircular cells and the shared gate
edges.
    For p ≠ q the bound is strict. At an actual initialization, the gate lies in the interior of the
angular diamond of its first circle, and Jθ = w cos γ h > 0 by (44). Thus J is a nonconstant affine
function there, and |J| is strictly below the vertex bound in (35). Combining this with (S′ ) gives
                                           π
                                             − U cos γ − H0 (γ, γ) − J < 0,
                                           2
using the first reflection of Lemma 6.2 when γ < 0. The initialization calculation in Theorem 5.7
therefore makes (I) strict. The pencil comparison and the addition of (E) and (T) preserve this
strictness; the one-disk case follows from π/2 < U . The transfer in Proposition 3.3, followed by the
maximum over the finitely many distinct pairs of sites, gives st(D) < 33/20.

    Theorem 6.4 is an existence statement about the displayed profile. Figure 6 shows its shape:
it starts low at γ = 0, stays nearly flat across the first two knot intervals, and rises steeply near
γ = π/2, so the spline family can adapt the amplitude separately at the two ends of the angular
domain.

6.3       Certifying the closed conditions
The conditions to be certified are one-variable inequalities on [0, π/2] together with the sign of E
                                                                                                   e on
a compact three-dimensional set for each of three representative branches. Both are established

                                                          27
by exhaustive covers in exact arithmetic; we describe the mathematical content and omit the
implementation. The key idea is that every operation returns an interval containing the true value,
so an inequality established for the interval is established for the value.

Two obstacles before covering can start. Neither is about arithmetic; both concern the form
in which the residual is written, since an enclosure is only as good as the expression it is computed
from.
    First, clearing the denominator as in (24) keeps the residual defined at γ = ±π/2, but leaves
an expression in which the coefficient of Hγ is a difference of two nearly equal terms near that
face. Write sinc z = sin z/z for z ̸= 0, with sinc 0 = 1. Reparameterizing the closed diamond
by two normalized arc coordinates in place of (φ, θ) turns A into a quotient of sinc values whose
denominator stays above 2/π by concavity of sin; this gives a form that is smooth on the whole
closed cube, and multiplying it by cos γ returns E. e Section D.3 carries this out.
    Second, several other quantities in the residual are differences of nearly equal terms near the
faces, so a naive enclosure of each is wide exactly where the certificate needs it narrow. Each of them
has an exact cancellation-free identity — for instance h − γ = ε2 cos2 γ/(h + γ), whose denominator
is bounded away from zero by (31) — and on the outer branches the residual is a linear combination
of the two nonnegative arc coordinates, so a box touching the gate face is closed as soon as both
coefficients are nonpositive. Section D.3 gives the coefficients and the identities used.

Exact arithmetic and exhaustive covers. Two kinds of certificate are used. The polynomial
inequalities — nonnegativity of the profile on each closed knot interval — are settled by exact rational
Bernstein expansions. A power polynomial is translated to [0, 1] and its coefficients converted to the
Bernstein basis of the same degree, each Bernstein coefficient being a weighted partial sum of the
power coefficients with ratio-of-binomials weights. Since that basis is nonnegative and sums to one,
nonnegative Bernstein coefficients certify the polynomial on the whole interval.
    Everything else is settled by exhaustive covers in outward-directed interval arithmetic over exact
rational endpoints. Every elementary operation returns an interval containing the true value, and so
does every transcendental function the residual uses: π through a Machin identity, sine and cosine
through Taylor polynomials with Lagrange remainders, and sinc through its monotonicity in |z|.
Section D.2 lists the enclosures.
    The domain is covered by closed boxes in the coordinates (48), one of them the angle γ and
the other two the normalized arc coordinates. A box is closed in one of three ways: a required
accessibility or sign predicate is refuted with a strictly negative outward upper bound, so the box
contains no required point; or the residual has a nonpositive outward upper bound; or one of two
mean-value rules below applies. Otherwise the box is bisected at its exact rational midpoint into two
closed children whose union is exactly the parent. An exhausted queue therefore proves the property
on the entire initial domain, since the union of the closed leaves is the initial box. Excluding a box
requires a strict sign.
    Two mean-value rules close the boxes at the faces where the residual vanishes identically, since
there an enclosure of the residual itself is too wide to have a sign.
    The first rule handles a box touching such a face. It integrates a certified sign of a partial
derivative out from an exact zero: the residual vanishes on the gate face and, at γ = π/2, is
identically zero along one of the two arc coordinates, so certified signs of the corresponding partial
derivatives on an enlarged box bound the residual on the box.
    The second rule handles a box meeting or crossing a knot, and is the standard centered enclosure.
Take a closed box with exact rational midpoint, enclose the residual at that midpoint, and enclose


                                                  28
each of its partial derivatives on the whole box; integrating along the straight segment from the
midpoint, which stays inside the closed convex box, bounds the residual by its midpoint enclosure
widened by the sum over the coordinates of the half-width times the largest absolute value in that
partial’s enclosure. The rule applies across a knot because the residual on a fixed branch depends
on w and w′ , and its first derivative in γ on the true continuous w′′ , all of which match across knots
by Lemma 6.3.
   The exact spline coefficients and the polynomial on each knot interval are listed in Section C.1.


7    The Agent-Assisted Search
The coefficients (42) were produced by a search carried out with a GPT-based multi-agent system.
This section records what was searched and what the search had to supply, since the two are
separated by Theorem 5.7.

What the theorem leaves to be searched. By Theorem B.2, proving a bound at level U is
fitting the excess from above.  By Theorem 5.7, a sufficient fit is described by conditions that are
affine in U, w(γ), w′ (γ) at each point of the compact set C. A candidate for the search is therefore
                         

a shape for w together with rational values of its parameters, and a candidate is admissible exactly
when finitely many one-variable inequalities and one family of pointwise inequalities on C hold. The
geometric reductions yield a linear program that serves as the search problem.
     The geometric content is established in Sections 4 and 5: the chain bound is expressed through
local conditions on gate states, and the step inequality is reduced to a pointwise condition on four
angles. The search operates on the resulting algebraic constraints.

What the system did. Three things, in each round.
    First, it proposed a shape: the saturating form of the balance term with its two switches
at ψ = ±k(γ), the affine angular term J of (29), the smoothing value ε = 1/20, and later the
replacement of a quadratic amplitude by a cubic spline on the knot vector (39). Theorem 5.7
holds for every ε ∈ (0, 1] and every amplitude profile, so each proposed shape is evaluated against
conditions fixed in advance of the search.
    Second, having fixed a shape, it solved the resulting linear program numerically. Sampling the
constraints of C on a grid, together with sequences of points approaching the faces, yields a finite
linear program in U and the profile parameters, which a floating-point solver minimizes; the solution
is then rationalized. For the spline shape this produced a sampled optimum near 1.633, and (42) is
a rational point with margin above it, giving room for certifying the value 33/20.
    Third, it ran the exhaustive certification of Section 6.3 on the rationalized candidate. The
exhaustive cover in exact arithmetic establishes that the rationalized candidate satisfies the full
hypotheses of Theorem 5.7.

Certification of the search output. The search supplies the explicit rational coefficients in
(42). Their admissibility follows from the exact certification of Section 6.3, which establishes the
hypotheses needed for Theorem 6.4. Floating-point optimization guides the choice of candidates,
and the proof uses their exact coefficients and the verified inequalities. A sampled optimum is not
a bound: the reduction is what makes the difference between the two a finite, checkable list of
conditions.




                                                  29
8     Conclusion and Further Improvements
We have proved an upper bound of 1.65 on the stretch factor of every planar Delaunay triangulation.
The proof uses a Bellman formulation of the disk-chain problem and a potential constructed from a
univariate spline profile. The sufficient conditions are affine in the profile and its derivative, which
allows us to search for a potential by linear programming and certify it over the full continuous
domain.
    By extending the potential we have further improved the upper bound to 1.5949, which narrows
the interval for the worst-case stretch factor to [1.5932, 1.5949]. The explicit potential and its
certification will be presented in a later version of this paper.


Acknowledgments
The framework of this work was developed by the authors. The search for the specific form of the
potential — the shape of its free part, and the profile together with its coefficients — was carried
out by a GPT-based multi-agent system that we developed.


A     From a Specified Delaunay Triangulation to Chains
This appendix proves the five statements used in Section 3.4: the grouping of faces into maximal
cocircular cells, the decomposition of a query segment, the replacement of a ladder path by a walk in
D, the one-disk bound, and the fact that the chains so produced lie in the class Q of Definition 3.1.
Throughout, S and D are as in Section 3. The framework is Xia’s [22]; the proofs are included so
that the present paper is self-contained.
    Lemma A.1 does all the geometric work. Once the faces are grouped into maximal cocircular
cells, whose boundary edges belong to D for every admissible choice of the diagonals, the other four
statements are readings of that grouping along the query segment: which cells the segment meets
and where it may be cut (Lemma A.2), how a rail is traded for a boundary walk (Lemma A.3),
what a single disk costs (Lemma A.4), and why the conditions of Q hold (Lemma A.5).

A.1    Maximal cocircular cells
Lemma A.1. The triangular faces of D are uniquely grouped into maximal cocircular cells with the
following properties: each cell is a convex polygon inscribed in a circle whose open disk contains
no point of S; the faces of D contained in a cell triangulate it completely; and every edge of the
boundary of a cell is an edge of D.

                              b = (x1 , x2 , x21 + x22 ). A circle ∥x − c∥2 = R2 corresponds to the plane
Proof. Lift x = (x1 , x2 ) to x
z = 2c · x + R − ∥c∥ , and the vertical difference between yb and that plane is ∥y − c∥2 − R2 . So a
              2       2

disk is empty of points of S exactly when the corresponding plane supports Sb from below. Each
face of D has an empty circumdisk, hence lies in a unique maximal lower face of the convex hull
of S,
   b and the projection of that maximal lower face is a convex polygon inscribed in a circle with
empty open disk. This assigns each face of D to one cell, and the assignment is unique because
maximal lower faces are.
    To see that the faces assigned to a cell cover it, take a point in its relative interior lying on no
edge of D. It lies in the interior of a unique face, and on a planar neighborhood the affine lift of
that face agrees with the supporting affine function of the maximal lower face; two affine functions
agreeing on an open set are equal, so the three lifted vertices of the face lie on that lower face, and


                                                   30
the face belongs to the cell. Such points are dense in the cell, and a finite union of closed triangles
is closed, so those faces cover the cell.
    Finally let x, y be adjacent vertices of the cell on its circle. The open chord (x, y) lies in the
open empty disk, so it contains no point of S. The boundary of the cell is covered by edges of D
and no point of S subdivides xy, so xy ∈ E(D). Consequently the boundary edges of a cell belong
to D for every admissible triangulation of the cocircular polygon.

A.2    Decomposing a query segment
Lemma A.2. List the points of S on the segment [p, q] in order, starting at p0 = p and ending at
q. Each subsegment Jj = [pj−1 , pj ] of positive length is either an edge of D, or it crosses in order a
chain Oj of disks in the sense of Section 3.1, whose gates are shared boundary edges of consecutive
maximal cocircular cells and whose terminals are pj−1 , pj .

Proof. By Lemma A.1 the maximal cocircular cells form a face-to-face convex subdivision of the
triangulated region. The relative interior of Jj contains no point of S. If it overlaps an edge of the
subdivision or a diagonal of a cell in positive length, then convexity together with the absence of
interior points of S forces Jj to be exactly that edge, which is the first case.
     Otherwise list the cells F1 , . . . , Fm crossed by Jj in query order. Consecutive cells share a
boundary edge of positive length: a transition at a single vertex would make that vertex a point of
S in the relative interior of Jj . By Lemma A.1 these shared edges are edges of D, and we take them
as the gates. Let Oi be the empty circumdisk of Fi . If fi is the lower supporting affine function of
Fi , then for x ∈ ∂Oi ,
                                       powOi−1 (x) = fi (x) − fi−1 (x),
so the cap of Oi coming from Oi−1 is exactly the circular gap of Fi across its entrance edge, and
similarly for the exit edge. Since a convex inscribed polygon has distinct entrance and exit edges,
those two gaps have disjoint relative interiors and neither contains an endpoint of the other in its
relative interior, which is strong cap-disjointness. The two endpoints of Jj are vertices of the first
and last cell, and emptiness of the respective disks gives the terminal exposure. Hence these disks,
gates and terminals form a chain, and Jj meets the gates in order.

A.3    Expanding a ladder path in the triangulation
Lemma A.3. For a chain produced by Lemma A.2,

                                      dD (pj−1 , pj ) ≤ POj (pj−1 , pj ).

Proof. Each gate is a shared boundary edge of two maximal cocircular cells, hence an edge of D by
Lemma A.1. Consider a rail, a marked arc on the circle of radius r of one cell. List the vertices
of the cell along the arc in its direction as x0 , x1 , . . . , xt . Consecutive chords xℓ−1 xℓ are boundary
edges of the cell, hence edges of D, and for the central angle increment ηℓ of the arc from xℓ−1 to xℓ ,
                                                              ηℓ
                                     ∥xℓ−1 − xℓ ∥ = 2r sin       ≤ r ηℓ .
                                                              2
Summing over ℓ shows that the boundary walk is no longer than the rail. This holds for a minor
arc, a major arc, an arc of length zero and a full 2π arc alike, since only the sum of the central angle
increments is used. Replacing every rail of a shortest ladder path by the corresponding boundary
walk and keeping all its gates produces a walk in D of length at most POj . The resulting walk uses
boundary edges of cells and their shared edges.

                                                      31
A.4    The one-disk bound
Lemma A.4. Let u =    ̸ v lie on a circle of radius r and let the smaller of the two central angles they
subtend be ϑ ∈ (0, π]. Then the shorter arc has length rϑ, the chord has length 2r sin(ϑ/2), and

                                                  π         ϑ
                                           rϑ ≤     · 2r sin .
                                                  2         2
Proof. The claim is ϑ/2 ≤ (π/2) sin(ϑ/2) with ϑ/2 ∈ (0, π/2], that is sin t ≥ (2/π)t for t ∈ (0, π/2].
The function sin is concave on [0, π/2] and agrees with the linear function (2/π)t at both endpoints,
so it lies above it on the interval. Equality holds only at t = π/2, i.e. for antipodal terminals.

   For a one-disk chain, the ladder consists of the two complementary arcs, so PO (u, v) is the
shorter of them and (3) follows.

A.5    Coverage of the restricted class
Lemma A.5. Every chain produced by Lemma A.2, equipped with the line of [p, q] oriented from
pj−1 to pj , belongs to the class Q of Definition 3.1.

Proof. Each maximal cocircular cell contains a nondegenerate triangle, so its circumdisk has positive
radius. Adjacent cells have distinct circumcircles and share a boundary edge with two distinct
endpoints lying on both circles, so consecutive circles meet at two distinct points: they cross properly,
and neither disk contains the other. This is Definition 3.1(i).
    The relative interior of the query subsegment contains no point of S, so it meets each shared
gate in the relative interior of that chord; a contact at a gate endpoint would be an interior point of
S. The query line cannot coincide with the supporting line of a gate, since a positive-length overlap
belongs to the actual-edge case of Lemma A.2. Hence the crossings are transverse, the two gate
endpoints lie strictly on opposite sides of the line, and this is (ii). Each traversed cell has a query
interval of positive length, so consecutive crossings are distinct and strictly ordered, and the source
and terminal lie strictly before and after all interior crossings; this is (iv). For m = 1 only the two
distinct terminals on one positive-radius circle are needed.
    We prove the forward condition (iii) using power differences. For adjacent cells Fi , Fi+1 put
F = powOi − powOi+1 . At each vertex z of Fi we have powOi (z) = 0 and, by emptiness of the next
disk, powOi+1 (z) ≥ 0, so F (z) ≤ 0. Since F is affine it is nonpositive on the convex hull Fi ; the two
circles are distinct so F is a nonzero affine function, and a nonzero affine function that is nonpositive
on a set with nonempty planar interior is strictly negative at every interior point. Exchanging the
two cells gives F > 0 in the interior of Fi+1 . Along the query line, F vanishes at the shared gate
crossing, is negative just before and positive just after it, so its slope there is positive; by Lemma 4.1
that slope is 2 e · (oi+1 − oi ), whence e · (oi+1 − oi ) > 0.
    Finally, the caps supplied by Lemma A.2 are strongly disjoint. With (i)–(iii) established,
Lemma 4.2 gives the upper-to-upper and lower-to-lower matching and the rail lengths, including
zero-length rails when the entrance and exit edges of a cell share a vertex. All conditions of
Definition 3.1 hold.

    The construction in Lemmas A.1 and A.2 handles degeneracies by grouping cocircular faces into
cells, splitting the query segment at interior points of S, and assigning a positive-length overlap to
the actual-edge case. The resulting disk chains satisfy the conditions of Q directly.




                                                   32
B     The Excess and Its Value Equation
Definition B.1 (excess). A continuation η from a gate state si is a finite sequence of steps, possibly
empty, followed by a termination. Its payoff is the cost of the remaining ladder minus U times the
remaining progress:
                                  P                     P                   
                    FU (η; si ) =   steps k jk + κend − U     steps k ∆xk + L+ ,

where the balances are propagated by (9) along the way and κend is evaluated at the final state.
The excess is
                 WU∗ (si ) = sup FU (η; si ) : η is a finite continuation from si .
                                

    The empty continuation, which terminates at once, shows the supremum is over a nonempty set,
so WU∗ (si ) ≥ κend − U L+ > −∞. We prove finiteness of the supremum below assuming (6) holds
for every chain in Q.
    Two elementary properties are needed first. Fix the disks and gates of a continuation and
compare two initial balances. Each component of the exact distance update in Lemma 4.5 is the
minimum of two endpoint distances plus fixed edge lengths. Such an update satisfies
                                                                                  
                    min(x + a, y + b) − min(e
                                            x + a, ye + b) ≤ max |x − x
                                                                      e|, |y − ye| .

Thus the maximum difference between the two pairs of endpoint distances cannot increase, and
the terminal minimum in (12) has the same property. Take the initial ledger to be zero in both
computations, so the initial pairs are

                                     (δi /2, −δi /2),        (δei /2, −δei /2).

Their
P      maximum difference is |δi − δei |/2, and the final computed values are the respective sums
  k jk + κend . Since the progress is the same in both computations, subtracting U times that
progress gives
                                FU (η; si ) − FU (η; sei ) ≤ 12 δi − δei                      (45)
for si = (Oi+1 , Gi , δi ) and sei = (Oi+1 , Gi , δei ) with the same geometry. And a continuation ηb from
si+1 preceded by one step from si gives a continuation η from si , whose payoff is

                                  FU (η; si ) = ji − U ∆xi + FU (b
                                                                 η ; si+1 ).                            (46)

Theorem B.2. Let U ≥ π/2. Then (6) holds for every chain in Q if and only if a feasible potential
at level U exists. When these equivalent conditions hold, the excess WU∗ is finite at every gate state
and every balance in [−gi , gi ], it is a feasible potential at level U , it satisfies the value equation
                                 n                                                         o
                WU∗ (si ) = max κend − U L+ ,                   ji − U ∆xi + WU∗ (si+1 ) ,
                                                               
                                                       sup                                               (47)
                                                    steps from si

and it is the pointwise smallest feasible potential at level U : every feasible W satisfies WU∗ ≤ W .
Proof. The implication from a feasible potential to the chain bound is Theorem 4.7.
   Assume (6) holds for every chain in Q, and fix a state si . We first bound the excess from above.
The idea is to put one predecessor and one source in front of si , which turns every continuation
from si into an actual chain, so that the chain bound applies to it.
   For ϵ > 0, let Oϵ = O(X − ϵ) be the member of the pencil (15) just behind the current disk,
which Lemma 4.8 makes an admissible predecessor. The crossing ci is interior to the gate chord,

                                                        33
hence interior to Oϵ , so the query line meets ∂Oϵ at two points with ci strictly between them; take
the backward one as the source uϵ . By (16) its power with respect to Oi+1 is a positive multiple of
ϵ, so uϵ is exposed to Oi+1 . It lies strictly before ci , while all crossings of any continuation from
si lie strictly after ci . Hence for every ϵ > 0 and every finite continuation, the initialization at Oϵ
followed by that continuation is a chain in Q.
     Let Lϵ = x(ci ) − x(uϵ ) > 0 be the progress of that initialization and let µϵ , δϵ be its data (11),
with sϵ = (Oi+1 , Gi , δϵ ). By (13) and the chain bound, the sum of µϵ and the continuation cost is at
most U times the total progress. The total progress is Lϵ plus that of the continuation; that is

                                             FU (η; sϵ ) ≤ U Lϵ − µϵ .

By (45), for every δi ∈ [−gi , gi ],

                                       FU (η; si ) ≤ U Lϵ − µϵ + 12 |δi − δϵ |.

For one fixed ϵ the right-hand side is a finite number independent of the number, sizes and geometry
of the disks in the continuation. It therefore bounds the supremum, and WU∗ (si ) is finite.
    Finiteness in hand, (47) follows by partitioning the continuations according to whether they
terminate immediately or take a first step, using (46); the supremum over an empty step class is −∞.
Feasibility is now immediate: (T) is the empty continuation; (E) follows by taking the supremum of
(46) over continuations from si+1 ; and for (I), applying the chain bound
                                                                              to an actual
                                                                                            initialization
followed by an arbitrary continuation from s1 gives FU(η; s1 ) ≤ U x(c    1 ) − x(u) − µ1 , and taking
the supremum over continuations gives exactly µ1 − U x(c1 ) − x(u) + WU∗ (s1 ) ≤ 0. Invariance is
clear because an isometry fixing the query line maps continuations bijectively to continuations with
the same weights and progress; positive scaling multiplies all rail and gate lengths, progress and
balance by the same factor, hence multiplies each payoff by it, and a positive scalar passes through
a supremum. Thus WU∗ is a feasible potential at level U .
    Finally let W be any feasible potential at level U . Fix a state and a finite continuation, propagate
the balance by (9), add the instances of (E) along the continuation followed by its instance of (T).
The intermediate values of W cancel and what remains is exactly FU (η; si ) − W (si ) ≤ 0. Taking
the supremum over continuations gives WU∗ ≤ W .

    Theorem B.2 gives the search for a feasible potential a specific target. The bound at level U
is equivalent to the existence of a feasible potential. Since every feasible potential dominates the
excess pointwise, exhibiting a bound means fitting the excess from above by a function one can
write down, and the fit has exactly the slack that (I), (E) and (T) tolerate.
    Taking suprema in (45) also gives |WU∗ (si ) − WU∗ (e
                                                        si )| ≤ 12 |δi − δei | for two balances at the same
geometry, so the excess inherits the modulus that (45) supplies for each individual continuation.


C     Exact Parameters
C.1     The spline profile
The seven coefficients of (42), with decimal values:
                20921                      20921                     173
         λ0 = − 500000 = −0.041842, λ1 = − 500000 = −0.041842, λ2 = 200000 = 0.000865,
               2299                               1547                                 28913
         λ3 = 1000000 = 0.002299,           λ4 = 500000 = 0.003094,               λ5 = 100000 = 0.28913,
              60041
         λ6 = 40000 = 1.501025.


                                                         34
The base is 39/200 = 0.195 and 28/125 = 0.224, and ε = 1/20. The condition λ0 = λ1 of Lemma 6.3
holds.                                    P
   Writing τ = |γ|/(π/2), the correction i λi Bi (τ ) is the following polynomial on each closed
knot interval, in ascending powers of τ :

                           interval               1         τ         τ2        τ3
                           [0, 14 ]          20921
                                          − 500000           0     128121
                                                                   125000   − 25433
                                                                              12500
                           [ 14 , 12 ]      167929
                                         − 2000000       50547
                                                        100000    − 62307
                                                                    62500
                                                                               1653
                                                                               2500
                           [ 12 , 34 ]     1146357
                                         − 2000000     1720377
                                                        500000   − 171687
                                                                   25000
                                                                              71483
                                                                              15625
                           [ 34 , 1]     − 25575651
                                            1000000
                                                      25862661
                                                       250000     − 70107
                                                                     500
                                                                            1995001
                                                                             31250


The quadratic base contributes (28/125)(π/2)2 τ 2 on top of these, so the true factor (π/2)2 is
retained. The value at τ = 0 is 39/200 + λ0 = 76579/500000 = 0.153158, which is the bound (44);
the value at τ = 1 is 2.248723 . . ..


D     Auxiliary Proofs
D.1    The pencil identities
We verify the last identity of Lemma 5.2 in the form used in (21). With the query line on y = 0,
L− = x(c) − x(w− ) and x(w− ) = x(o) − r cos γ, so

                                         L− = x(c) − x(o) + r cos γ.

The gate and the crossing are fixed, and x(o) = x(M ) + X cos φ, so ∂X x(o) = cos φ. Differentiating
and using rX = cos θ and rγX = A gives

                                   (L− )X = − cos φ + cos θ cos γ − sin γ A.

Substituting A = (sin φ − sin γ cos θ)/ cos γ and clearing denominators,

                  − cos φ cos γ + cos θ cos2 γ − sin γ sin φ + sin2 γ cos θ   cos θ − cos(γ − φ)
       (L− )X =                                                             =                    ,
                                           cos γ                                     cos γ
which is the form used in the proof of Proposition 5.5. The cancellation of the terms carrying U in
that proof is then
                                     h                         cos θ − cos(γ − φ) i
 U − cos θ cos γ + sin γ A + (L− )X = U − cos θ cos γ + sin γA +                      = −U cos φ,
                                                                        cos γ

by expanding cos(γ − φ) = cos γ cos φ + sin γ sin φ and substituting A once more.

D.2    The interval enclosures
These are the enclosures used by the covers of Section 6.3. Every elementary operation returns an
interval containing the true value: sums and negations are exact, a product takes the four endpoint
products and rounds outward, a reciprocal reverses endpoints and fails if the divisor contains zero,
and a square root uses integer square roots rounded outward.
    The constant π is enclosed by alternating rational bounds in the Machin identity π = 16 arctan 51 −
          1
4 arctan 239 , obtained by integrating the finite geometric expansion of 1/(1 + t2 ). Sine and cosine

                                                       35
are enclosed by Taylor polynomials with Lagrange remainders, together with every exact extremum
contained in the argument interval.
    For sinc, the numerator z cos z−sin z of its derivative starts at zero and has derivative −z sin z ≤ 0,
so
R1 sinc  is even and nonincreasing in |z| on [0, π]; its derivatives are bounded through sinc z =
 0 cos(sz) ds, whose m-th derivative is at most 1/(m + 1) in absolute value.


D.3     Cover coordinates and cancellation-free forms
This subsection supplies the two rewritings announced in Section 6.3. Write t = π/2 − γ.
   Removing the denominator. Parameterize the closed diamond of (18), degenerate faces included,
by the two normalized arc coordinates of (17) rescaled to the unit interval: with a, b ∈ [0, 1],
                                               π                              t h 1i
                 θ = (π − t)a + t b,      φ=     − t − (π − t)a + t b,          ∈ 0, ,                (48)
                                               2                              π     2
so that l+ /r = 2(π − t)a and l− /r = 2tb. Then θ + φ − π/2 = t(2b − 1) and cos γ = sin t. Expanding
sin φ = cos θ − t(2b − 1) , using cos t(2b − 1) − cos t = 2 sin(tb) sin t(1 − b) and dividing by sin t
gives                                                                                      
                   (2b − 1) sin θ sinc t(2b − 1) + 2b(1 − b) t cos θ sinc(tb) sinc t(1 − b)
              A=                                                                              .    (49)
                                                    sinc t
Concavity of sin on [0, π/2] gives sinc t ≥ 2/π > 0, so (49) is smooth on the whole closed cube,
and equals (2b − 1) sin θ at t = 0. Multiplying the residual written this way by cos γ recovers the
required inequality everywhere, that face included. Certifying the extension nonpositive is sufficient,
and may be stronger than necessary on branch faces that are inaccessible.
    Cancellation-free forms. The differences of nearly equal terms are evaluated through

               ε2 cos2 γ     π                                                                   t
                                                                               1 − sin γ = 2 sin2 ,
                                                                         
      h−γ =              ,     − h = t − (h − γ),    k − γ = t 1 − sinc t ,
                h+γ          2                                                                   2

all with strictly positive denominators by (31). Put ξ = (π − t)a and ζ = t(1 − b). These nonnegative
angular quantities satisfy ξ + ζ = π/2 − φ and ξ − ζ = θ − t. The identity cos(ξ − ζ) − cos(ξ + ζ) =
2 sin ξ sin ζ gives
                                                2 sin ξ (1 − b) sinc ζ
                                   sin θ − A =                         .
                                                         sinc t
On the positive outer branch H0 = σ, substituting (29) into (23) and using these identities yields

                                            E = ξCξ + ζCζ ,

where
                                    2(1 − b) sinc ξ sinc ζ
                Cξ = (1 + w cos γ h)                       − (1 + w cos γ(h − γ)) cos θ
                                            sinc t
                                         ′
                      − A w cos γ(h − γ) − U sinc(ξ + ζ),
                                                                    ′
                Cζ = (1 + w cos γ(h + γ)) cos θ + A w cos γ(h + γ) − U sinc(ξ + ζ).
Here A is evaluated by (49), so the coefficients remain defined on the closed cube. Since ξ, ζ, cos γ ≥ 0,
a box on which both coefficients are nonpositive satisfies E  e ≤ 0, including a box touching the gate
face ξ = ζ = 0. The negative outer branch follows by the second reflection of Lemma 6.2.
    Write Ec , E+ , E− for the residual expressions with H0 = mψ, σ, −σ, respectively. Their differ-
ences are
                         Ec − E± = m cos θ(±k − φ) ± Ak ′ − Am′ (ψ ∓ k).
                                                              


                                                    36
At the switches ψ = ±k the last term vanishes; in the central interior it is retained. Multiplication
by cos γ gives the corresponding cleared residual identities. For the profile of Theorem 6.4, the
branch inequalities, both incident gradients at each switch, and the boundary cases are verified by
rigorous arithmetic certification.

D.4    The gate faces of the angular domain
The following identities are the ones used by the face rules of Section 6.3, and they explain how to
certify boxes touching those faces.
    On φ = π/2 the closed angular domain forces θ = π/2 − γ, and the stable interval becomes
[k, π/2 + cos γ]. There H0 = σ and J = w cos γ γ(π/2 − h), which is exactly the term subtracted
from γ in σ, so by (29)
                                            H0 + J = γ.
On φ = −π/2 one gets θ = π/2 + γ, stable interval [−π/2 − cos γ, −k], and H0 + J = −γ.
Differentiating the first identity along the curve ψ = π/2 + s cos γ, θ = π/2 − γ, −1 ≤ s ≤ 1, gives

                                        Hγ + Hψ ψ ′ − Hθ = 1

for both incident gradients at s = −1, since their difference annihilates the switch tangent as
in the proof of Theorem 5.7. For |γ| < π/2, substituting      cos θ = sin γ, sin θ = cos γ, A = cos γ,
K = γ sin γ + cos γ and U cos φ = 0 into (23) leaves Hψ cos γ ψ ′ + sin γ(ψ − π/2) = 0; the analogous
                                                        

computation on the opposite face leaves the negative of the corresponding expression. So the residual
vanishes identically on both gate faces, for every accessible incident gradient.
    At γ = ±π/2 the domain forces θ = π/2 ∓ φ, and both cos γ and sin φ − sin γ cos θ vanish, so
E = 0 there for every incident gradient. For |γ| < π/2, at θ = 0 the domain forces φ = γ and
 e
ψ = γ, and A = 0, so E itself equals the initialization residual of (36) and E e equals cos γ times it;
at θ = π the domain forces φ = −γ and ψ = −γ, with the termination residual in the same two
roles. The scalar conditions (S) and (S′ ) therefore dispose of those two faces entirely. These are
identities on the faces; a box of positive volume touching one of them is closed by the mean-value
rules of Section 6.3.


References
 [1] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, et al. AlphaEvolve: A coding agent for
     scientific and algorithmic discovery. arXiv:2506.13131, 2025.

 [2] Thomas Hubert, Rishi Mehta, Laurent Sartran, et al. Olympiad-level formal mathematical
     reasoning with reinforcement learning. Nature, 651:607–613, 2025. https://doi.org/10.103
     8/s41586-025-09833-y.

 [3] Jonathan M. Borwein and Peter B. Borwein. Pi and the AGM: A Study in Analytic Number
     Theory and Computational Complexity. Wiley, New York, 1987.

 [4] Prosenjit Bose, Luc Devroye, Maarten Löffler, Jack Snoeyink, and Vishal Verma. Almost
     all Delaunay triangulations have stretch factor greater than π/2. Computational Geometry,
     44(2):121–127, 2011.

 [5] Prosenjit Bose, Joachim Gudmundsson, and Michiel Smid. Constructing plane spanners of
     bounded degree and low weight. Algorithmica, 42(3–4):249–264, 2005.


                                                  37
 [6] Kirill Brilliantov, Etienne Bamas, and Emmanuel Abbé. k-server-bench: Automating potential
     discovery for the k-server conjecture. arXiv:2604.07240, 2026.

 [7] L. Paul Chew. There are planar graphs almost as good as the complete graph. Journal of
     Computer and System Sciences, 39(2):205–219, 1989.

 [8] Shiliang Cui, Iyad A. Kanj, and Ge Xia. On the stretch factor of Delaunay triangulations of
     points in convex position. Computational Geometry, 44(2):104–109, 2011.

 [9] David P. Dobkin, Steven J. Friedman, and Kenneth J. Supowit. Delaunay graphs are almost
     as good as complete graphs. In Proceedings of the 28th Annual Symposium on Foundations of
     Computer Science (FOCS), pages 20–26, 1987.

[10] David P. Dobkin, Steven J. Friedman, and Kenneth J. Supowit. Delaunay graphs are almost
     as good as complete graphs. Discrete & Computational Geometry, 5(4):399–407, 1990.

[11] Rida T. Farouki. The Bernstein polynomial basis: A centennial retrospective. Computer Aided
     Geometric Design, 29(6):379–419, 2012. https://doi.org/10.1016/j.cagd.2012.03.001.

[12] Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner. Mathematical
     exploration and discovery at scale. arXiv:2511.02864, 2025.

[13] Yonatan Gideoni, Sebastian Risi, and Yarin Gal. Simple baselines are competitive with code
     evolution. arXiv:2602.16805, 2026.

[14] Iyad A. Kanj, Ljubomir Perković, and Ge Xia. On spanners and lightweight spanners of
     geometric graphs. SIAM Journal on Computing, 39(6):2132–2161, 2010.

[15] Yisi Ke, Tianyu Huang, Yankai Shu, Di He, Jingchu Gai, and Liwei Wang. Towards solving
     the Gilbert–Pollak conjecture via large language models. arXiv:2601.22365, 2026.

[16] J. Mark Keil and Carl A. Gutwin. The Delaunay triangulation closely approximates the complete
     Euclidean graph. In Algorithms and Data Structures (WADS 1989), Lecture Notes in Computer
     Science 382, pages 47–56. Springer, 1989. https://doi.org/10.1007/3-540-51542-9_6.

[17] J. Mark Keil and Carl A. Gutwin. Classes of graphs which approximate the complete Euclidean
     graph. Discrete & Computational Geometry, 7:13–28, 1992. https://doi.org/10.1007/BF02
     187821.

[18] Sungyoon Kim and Mert Pilanci. AI-assisted discovery of convex relaxations via dual agents.
     arXiv:2606.31182, 2026.

[19] Ramon E. Moore, R. Baker Kearfott, and Michael J. Cloud. Introduction to Interval Analysis.
     SIAM, Philadelphia, 2009.

[20] Giri Narasimhan and Michiel Smid. Geometric Spanner Networks. Cambridge University Press,
     2007.

[21] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, et al. Math-
     ematical discoveries from program search with large language models. Nature, 625:468–475,
     2024. https://doi.org/10.1038/s41586-023-06924-6.




                                               38
[22] Ge Xia. The stretch factor of the Delaunay triangulation is less than 1.998. SIAM Journal
     on Computing, 42(4):1620–1659, 2013. https://doi.org/10.1137/110832458. A preliminary
     version appeared in Proceedings of the 27th Annual Symposium on Computational Geometry
     (SoCG 2011).

[23] Ge Xia and Liang Zhang. Toward the tight bound of the stretch factor of Delaunay triangulations.
     In Proceedings of the 23rd Canadian Conference on Computational Geometry (CCCG 2011),
     pages 175–180, 2011.




                                                 39
