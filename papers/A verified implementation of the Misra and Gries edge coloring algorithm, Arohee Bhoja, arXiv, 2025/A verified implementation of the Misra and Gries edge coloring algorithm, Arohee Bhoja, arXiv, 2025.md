                                         A verified implementation of the Misra and Gries
                                                      edge coloring algorithm
arXiv:2512.13999v1 [cs.DM] 16 Dec 2025




                                                                          Arohee Bhoja

                                                                                2025

                                                                              Abstract
                                                  Vizing’s theorem states that every simple undirected graph can be
                                              edge-colored using fewer than ∆ + 1 colors, where ∆ is the graph’s max-
                                              imum degree. The original proof was given through a polynomial-time
                                              algorithmic procedure that iteratively extends a partial coloring until it
                                              becomes complete. In this work, I used the Lean theorem prover to pro-
                                              duce a verified implementation of the Misra and Gries edge-coloring algo-
                                              rithm, a modified version of Vizing’s original method (available as source
                                              code [1]). The focus is on building libraries for relevant mathematical
                                              objects and rigorously maintaining required invariants.



                                         1    Introduction
                                         Let G be a simple undirected graph. We denote the maximum degree of G by
                                         ∆(G), or simply ∆.
                                             - A proper edge coloring of G maps edges in G to colors such that no two
                                               incident edges share a color. This edge coloring is complete if every edge
                                               in the graph is colored.
                                             - The edge chromatic number of G, denoted as χ′ (G), is the minimum num-
                                               ber of colors necessary to create a proper edge coloring of G.
                                         Immediately, we can conclude that ∆ ≤ χ′ (G). This is because if two edges
                                         are incident, they cannot have the same color, and the degree of a vertex is its
                                         number of incident edges.
                                         In 1965, Soviet mathematician Vadim Vizing described a polynomial-time algo-
                                         rithmic procedure that proved χ′ (G) ≤ ∆ + 1. [2] It turns out that this is the
                                         tightest bound we can achieve with a deterministic polynomial-time algorithm,
                                         since it is NP-complete to determine, for a given graph G, whether χ′ (G) = ∆
                                         or χ′ (G) = ∆ + 1. [3]
                                         During the latter half of the 20th century, there were several efforts made to
                                         simplify Vizing’s original algorithm and its proof of correctness. Bollobás pre-
                                         sented a shorter proof in 1979, which was really more of a sketch as it omitted


                                                                                  1
several nontrivial pieces of the argument. [4] In the early 1990s, simplified algo-
rithms were designed by Rao and Dijkstra [5] and by Misra and Gries [6], that
introduced nomenclature for auxiliary data structures and reduced branching
wherever possible.
However, even after these improvements, the proofs of correctness are neces-
sarily rather complex. There are several auxiliary data structures used in the
description of each algorithm, which interact with one another in subtle ways.
They must all be shown to maintain certain invariants over several subroutines
that are themselves nontrivial. In other words: the algorithm itself does not
straightforwardly motivate its proof of correctness, which makes it an interest-
ing case study for formal verification.
A number of graph theoretic algorithms have been formally verified using both
interactive and automated theorem provers. In 2024, Tobias Nipkow verified
the Gale–Shapley stable matching algorithm in Isabelle by progressing from ab-
stract specifications to concrete implementations via stepwise refinement. [7]
However, this approach does not readily extend to the Misra and Gries algo-
rithm, as its complexity and reliance on auxiliary data structures makes stepwise
concretization impractical. Additionally, in 2018, Tarjan’s algorithm for com-
puting the strongly connected components of a directed graph was verified in
the deductive program verifier Why3 and the interactive theorem provers Rocq
and Isabelle. [8] While valid, these verifications relied on abstract library data
types and therefore did not constitute rigorous proofs of computationally effi-
cient implementations.
Earlier work by Joachim Breitner in 2011 implemented the Misra and Gries
edge-coloring algorithm in the modeling formalism Event-B and verified it us-
ing the Rodin tool. [9] Rodin automatically extracts proof obligations from the
implementation to be discharged manually in Isabelle. While the resulting for-
mal proof of correctness was sound, it had several limitations: it relied on the
assumed soundness of Rodin, and the automatically generated proofs were de-
scribed as “write-once, read-never.” Through the use of an interactive theorem
prover, the present work seeks to mitigate these issues by establishing a closer
correspondence between informal and formal proofs.


2    The algorithm and its proof of correctness
We now present the algorithm as it is implemented in the formalization.
Let V (G) denote the vertex set of G, and E(G) denote its edge set.
Let u ∈ V (G), and c be a color. Fix a (partial) proper (∆ + 1)-edge coloring C.
c is an:
    - incident color on u if there exists an edge incident to u that is colored c
    - free color on u otherwise.
A fan F = ⟨f1 , ...fk ⟩ on a vertex x is a nonempty sequence of distinct neighbors


                                        2
of x that satisfies the following properties:
    - The edge {x, f1 } is uncolored.
    - Fan color property: for every i < k, the color of {x, fi+1 } is free on fi .
When x is clear from context, elements of the fan will be used as shorthand for
their corresponding fan edges (e.g. fi as shorthand for {x, fi }).
If we would like to color {x, f1 }, there is an easy process to do so based on the
properties of the fan – since every fan edge’s color is free on its predecessor, we
can rotate each color down one edge and leave the last fan edge uncolored.
For every i, let ci denote the color of edge {x, fi }. We can now describe this
procedure in pseudocode:
  function rotate C[F ]
    For every i < k, recolor {x, fi } with ci+1 .
    Uncolor {x, fk }.

Rotation lemma. This operation maintains the properness of the edge coloring.

Proof. Consider some arbitrary i < k. We want to show that ci+1 is a valid
color for {x, fi } (i.e. that it maintains the properness of the edge coloring).
By definition, ci+1 was free on fi before the fan was rotated.
Moreover, {x, fi } must be the only edge incident on x colored ci+1 after the
rotation. Assume for a contradiction that there exists a vertex v ̸= fi incident
to x such that {x, v} is colored ci+1 after the rotation.
 Case 1: v ∈ F . Then, v = fj for some j ̸= i, and so fj+1 was colored ci+1
 before the rotation. But this is not possible, since fi+1 was colored ci+1 , and
 the edge coloring is proper.
 Case 2: v ∈/ F . The rotation only affects edges contained in the fan, so {x, v}
 must have been colored ci+1 before the rotation. We also know that fi+1 was
 colored ci+1 before the rotation, and that fi+1 ̸= v since v ∈ / F . As earlier,
 this is not possible since the edge coloring is proper.


An alternating path P = ⟨p1 , ...pl ⟩ on a vertex x with colors c, d is a nonempty
sequence of distinct vertices such that p1 = x, and for every i < l, the color of
{pi , pi+1 } is either c or d.
If this path is maximal (i.e. it cannot be extended on either side), we can invert
the path without sacrificing the properness of the edge coloring. This may be
useful to change the set of free colors on x, since if c was free on x prior to the
inversion, then d will be afterwards, and vice versa.
We describe the inversion procedure in pseudocode:
 function invert C[P ]




                                         3
    For every i < l, flip the color of {pi , pi+1 }. If it was colored c, recolor it
    with d; if it was colored d, recolor it with c.

Inversion lemma. If P is maximal, this operation maintains the validity of the
edge coloring.
Proof. Consider some arbitrary i < l, and suppose WLOG that {pi , pi+1 } was
colored c. (The other case is symmetric, and follows by relabeling.) We want
to show that d is a valid color for {pi , pi+1 } post-inversion.
Since the edge coloring is proper, we know that:
   1. {pi−1 , pi } and {pi+1 , pi+2 } were both colored d prior to the inversion.
   2. No other edges incident to pi or pi+1 were colored d.
After the inversion, {pi−1 , pi } and {pi+1 , pi+2 } are both colored c, leaving d free
on pi and pi+1 as required.

Another function that will be useful in describing the main algorithm is re-
color, which sets the color of an edge within the edge coloring.
  function recolor C[{u, v} 7→ a]
    Returns the edge coloring given by C but with the edge {u, v} recolored
    with color a

We now describe a procedure extend C U , that starts with a partial (∆ + 1)-
edge coloring C, and a set U which consists of the edges in G that are uncolored
in C.
Choose an edge {x, y} in U to color. The main idea: if we can find a fan on x
whose first element is y and whose last element shares some free color u with
x, we can simply rotate the fan to color {x, y}, and then color the last fan edge
with u.
Our task is then to find such a fan. We start by constructing a maximal fan
F = ⟨f1 , ..., fk ⟩ on x whose first element is y. We are guaranteed that such a
fan exists, since the singleton fan ⟨y⟩ is valid. We then choose a free color c on
x, and a free color d on fk . c and d must exist, since every vertex in G can have
at most ∆ incident colors, and C is a (∆ + 1)-edge coloring.
If d is free on x, we can rotate F , recolor {x, fk } with d, and then recursively
color the remaining edges in U − {x, y}.
However, if d is incident on x, it must be made free. We construct an alternating
path on x with colors c and d by iteratively choosing edges colored c and d until
the path cannot be extended any further. We then invert the path. Since c was
free on x prior to the inversion, d must be free on x afterwards.
We are not guaranteed that the path inversion preserves the properties of F , but
it is possible to show that there exists a subfan of F that exhibits the necessary
properties – i.e. that there is some w ≤ k such that ⟨f1 , ..., fw ⟩ is a fan and d is
free on fw . We will refer to this fact as the subfan existence lemma, and justify
it later.


                                          4
We can then rotate the subfan, recolor {x, fw } with d, and recursively color the
remaining edges.
Here is the algorithm in pseudocode:
 1: function extend U C ··=
 2:    if U = ∅ then C
 3:    else
 4:        Choose {x, y} ∈ U .
 5:        Let F = ⟨f1 , ...fk ⟩ be a maximal fan on x with f1 = y.
 6:        Let c be a free color on x, and d be a free color on fk .
 7:        if d is an incident color on x then
 8:              Let P be a maximal alternating path on x with colors c, d.
 9:              C ··= invert C[P ]
10:        Let w ≤ k such that F ′ = ⟨f1 , ...fw ⟩ is a fan and d is free on fw .
11:        C ′ ··= rotate C[F ′ ]
12:        C ′ ··= recolor C ′ [{x, fw } 7→ d]
13:        extend (U − {x, y}) C ′

As promised, here is the proof of the subfan existence lemma:
Lemma. The inversion of the alternating path guarantees the existence of a
w ≤ k such that ⟨f1 , ..., fw ⟩ is a fan and d is free on fw (see: line 10 of extend).

Proof. In the case that d is free on x, take w = k and we’re done. Otherwise:
Observe that F must have exactly one edge colored d. It cannot have more than
one, since each fi is a neighbor of x and C is a proper edge coloring. It also
cannot have fewer than one, since otherwise we could append the neighbor of x
whose incident edge is colored d to F , contradicting the maximality of F .
Let {x, fi } be this edge.
Obs 1. i > 1 since f1 = y and {x, y} is uncolored.
Obs 2. By definition of an alternating path, x is an endpoint of P . Since P is
       maximal, it must contain all of x’s neighbors that are colored c or d. We
       can then conclude that fi ∈ P .
Obs 3. d is free on fi−1 ; this is given by the definition of a fan since {x, fi } is
       colored d.
Case 1: fi−1 ∈   / P.
The path inversion only affects edges colored c and d. F does not have an edge
colored c (since c is free on x). So, for all j ̸= i, the free colors on fj and the
color of {x, fj } are unchanged. Since F was a fan, we can conclude that the fan
color property still holds for all fj .
Take w = i − 1. By Obs. 3, we are done.
Case 2: fi−1 ∈ P . Take w = k.
As earlier, we have that fj respects the fan color property for all j ̸= i. By
Obs. 2, {x, fi } is colored c after the inversion. Since d was free on fi−1 (by


                                          5
Obs. 3), fi−1 must be an endpoint of P , and so c must be free on fi−1 after the
inversion.
Moreover, fk ∈ / P . Suppose that it were; it would then have to be an endpoint
since d was free on fk prior to the inversion. However, this is impossible, because
x and fi−1 are the endpoints of P .
We can therefore conclude that d remains free on fk , since it is unaffected by
the inversion.


We can now finally describe the main algorithm color G, which takes in a
graph and returns a complete proper edge coloring.
  function color G ··=
     Let C be an empty (∆ + 1)-edge coloring.
     extend E(G) C

It is much easier to reason mathematically about purely functional programs
than ones that contain side effects or mutable data. For this reason, color
differs from the algorithm presented by Misra and Gries.
We can now proceed to proving Vizing’s theorem, which follows from:
Theorem. color G is a complete proper edge coloring of G with at most ∆ + 1
colors.

Proof. By construction, extend only uses ∆ + 1 colors. We have already justi-
fied that each operation carried out in extend preserves the properness of its
input edge coloring. We can thus apply an inductive argument to conclude that
color G is a proper edge coloring.
Obs. At the start of each iteration of extend, {x, y} must always be uncolored.
To justify this, suppose that every edge in U is uncolored in C. The only edges
in G whose colors are affected by extend are either in P , which contains no
uncolored edges, or in F , whose only uncolored edge is {x, y}. Therefore, every
edge in U − {x, y} must be uncolored in C ′ . Applying this argument inductively
yields the desired conclusion.
We may now proceed to proving completeness, using another inductive argu-
ment. It suffices to show that C ′ contains one more colored edge than C.
Inverting the path does not affect the total number of edges colored, and nei-
ther does rotating the fan (provided that {x, y} is uncolored, which we showed
above). After line (6), {x, fk } is uncolored, and line (7) colors it d, increasing
the total number of edges colored by one as required.




                                        6
3     Formalization: the library
Many of the mathematical objects required to implement the algorithm have
abstract definitions in Mathlib, Lean’s open-source library of formalized mathe-
matics. [10, 11] However, these definitions are not optimized for computational
efficiency, so I chose to use Lean core data types such as lists and arrays in-
stead. This allowed for a polynomial-time implementation of the algorithm, but
required significant additional work — in particular, I had to define:
    - A representation of each mathematical object that preserves the polyno-
      mial time complexity of the algorithm
    - Implementations of key subroutines (recoloring an edge, rotating a fan,
      and inverting a path), and proofs that they preserve the invariants of the
      objects that they modify
    - Formalizations of various notions (such as maximality) that are presented
      without explicit definition in the informal proof
The Lean code in this section is cleaned up, with some technical details omitted
for readability.


3.1    Simple graphs
Vertices are represented as natural numbers less than n, and edges are repre-
sented as pairs of vertices.
variable (n : Nat)
abbrev Vertex := Fin n
abbrev Edge := Vertex n × Vertex n

The type Fin n represents natural numbers less than n.
A neighbor set is defined as a list of unique vertices whose length is less than
n; the inequality is strict to disallow self loops. (nodupAx alone only implies
that the length is less than or equal to n, so we impose the additional condition
sizeAx.)
structure Nbors (n : Nat) where
  val : List (Vertex n)
  sizeAx : val.length < n
  nodupAx : val.Nodup

Here, val.length is shorthand for List.length val.
The predicate Nodup indicates that a vertex is not allowed to be present multiple
times within a neighbor set – i.e. multi-edges are not allowed.
Simple graphs are represented as adjacency lists, that map vertices to their
neighborhoods. We also have the additional properties that every vertex is
represented in the graph, that edges are bi-directional, and that there are no
self loops.


                                       7
structure Graph (n : Nat) where
  val : Array (Nbors n)
  sizeAx : val.size = n
  symmAx : ∀ u v : Vertex n,
    u ∈ val[v] ↔ v ∈ val[u]
  noSelfLoopsAx : ∀ u : Vertex n, u ∈
                                    / val[u]

Notably, edges are represented as tuples even though the graph is undirected.
Ideally, the Edge type would have been unordered, but the type for unordered
pairs in Mathlib (sym2) would have caused more messiness in theorem state-
ments and required the use of many additional library lemmas over the course
of the formalization. This choice did not result in much extra work – I defined
a few lemmas about symmetry and used them to rewrite statements wherever
necessary. However, this could be a good candidate for using macros and refac-
toring.
The edge set of a graph is defined as a list of graph edges (i.e. a subset of E(G)),
with a few additional properties:
    - If (u, v) is present in the edge set, (v, u) must also be.
    - No multi-edges.


3.2     Edge colorings
3.2.1   Definitions

Color is defined as an option type: either a natural number less than c, or none.
This is to allow for partial edge colorings.
EdgeColoring c G is a structure type parametrized by the graph being colored
and the number of colors in the edge coloring. The data is represented as a
modified adjacency matrix, where indices correspond to the vertices present
in an edge pair and entries correspond to colors (either none, if the edge is
uncolored, or some c, if the edge is colored with a color c).
We also have the following properties:
    - The adjacency matrix is n by n.
    - Every edge that is colored in the edge coloring is present in the graph.
    - No two incident edges have the same color (unless that color is none).
    - The matrix is symmetric – C[u][v] = C[v][u].
2D arrays have the nice computational property of constant-time access, but
they can cause difficulty when writing statements and proofs, and when using
automation to discharge goals within those proofs.
For example, in order to access the element at a given index of an array, Lean
requires a proof that the index is in bounds. In a 2D array, this becomes
particularly messy. Here is a function that returns the color of a given edge in


                                         8
an edge coloring:
variable (C : EdgeColoring c G)

def color (e : Edge n) :=
  (C.val[e.1]’(by rw [C.sizeAx1]; exact e.1.isLt))[e.2]’
  (by rw [C.sizeAx2]; exact e.2.isLt)

I found that prioritizing computational efficiency foremost and then ease of
using automation before ease of writing statements and proofs was the best
strategy to write a relatively efficient implementation that did not require me
to manually discharge as many difficult and technical goals.
There are a number of other functions and lemmas about edge colorings in the
Lean files, which I implemented for ease of proving later theorems. They are
omitted here for brevity.

3.2.2   Implementing the recolor operation

The last important piece of the edge coloring library is the implementation of
the recolor operation from the previous section.
We begin by formalizing the notion of validity. If a color a is valid for edge e
(i.e. edgeColorValid e a), then either a is none, or it is free on both vertices in
e.
We implement a function to set a cell in a 2D matrix to a given value. We also
prove the following specifications:
    - The size of the array remains invariant.
    - Every other value in the array remains invariant.
    - The value at the given cell is indeed the given value.
    - Every row in the array aside from the ith one remains invariant.
    - Setting two distinct cells in a 2D square matrix is a commutative opera-
      tion.
    - We also include lemmas that allow us to reason about the count of a given
      value in the array before and after the operation.
Many list and array library functions have incomplete APIs; I tried to avoid
using those functions wherever possible. For this reason, the library includes a
specification of the edgeColorValid predicate that uses the function Array.count.
This lemma states that a is free on {u, v} if and only if the count of a is zero in
both C[u] and C[v].
We can now define a function to recolor an edge, which sets both cells in the
edge coloring that correspond with that edge. This operation comes with its
own set of specifications to prove. Essentially, if we recolor edge e = {u, v} with
color a in edge coloring C:
    - The size and symmetry of C are preserved.


                                        9
   - e is indeed colored with a, and the colors of the other edges remain invari-
     ant.
   - For any color b, the count of b in the neighborhoods of u and v increases
     by one if a = b, decreases by one if e was previously colored with b, and
     remains the same otherwise.
Lastly, to create an object of type EdgeColoring, we must prove that this oper-
ation maintains the properties listed in the definition of an edge coloring (size,
representing the graph, properness, and symmetry). These proofs were long
and technical since they required casework over indices and many invocations
of symmetry lemmas; they are again omitted here.


3.3     Fans
3.3.1   Definitions

We define a fan F on vertices x and y as a nonempty array of distinct vertices
with the following additional properties:
   - The first element of F is y.
   - Every element of F is in the neighborhood of x.
   - The fan color property holds as described in the previous section.
To implement the fan color property, we use the Chain’ function in Lean, which
indicates that a given predicate holds between adjacent elements of the list.
This allows us to express an index-dependent property without actually using
indices, which will save us a lot of proof obligations later.
def fan_prop (x : Vertex n) (f1 f2 : Vertex n) :=
  color C (x, f2 ) ∈ freeColorsOn C f1

def colorAx (F : Array (Vertex n)) (x : Vertex n) :=
  F.toList.Chain’ (fan_prop C x)

We also define the notion of a singleton fan on vertices x and y, and prove that
the fan properties hold under the assumption that the edge {x, y} is present in
the graph.

3.3.2   Creating a maximal fan

Given an uncolored edge {x, y}, the algorithm requires that we produce a max-
imal fan on x whose first element is y.
We start by defining a function add that, given a partial fan F and a list of
neighbors nbors that are not currently present in the fan, adds as many elements
to the fan as possible.
add uses the find? function to search nbors for a vertex z such that the color of



                                       10
{z, x} is free on the last vertex in F. If such a z exists, it is added to the back
of F and erased from nbors. Otherwise, F is returned unchanged.
If List.erase is given a value that is not present in the list, it returns the list
unchanged. So, in order to prove that add terminates, we must show that z
is always a member of nbors prior to its removal. By default, we do not have
access to the definition of z within the cases of the match statement. So, we use
the function List.attach to bundle z together with a proof that it is a member
of nbors. This looks slightly less clean than adding a hypothesis to the match
discriminant, but allows the simplifier and split to work more effectively on the
match statement.
def add (x y : Vertex n) (F : Array (Vertex n)) (nbors : List (Vertex n))
  (h : F ̸= #[]) :=
  match (List.attach nbors).find? (fun ⟨z, _⟩ 7→
    color C (x, z) ∈ freeColorsOn C (F.back (Array.size_pos_iff.mpr
    h))) with
  | some z => add x y (F.push z.val) (nbors.erase z.val)
    Array.push_ne_empty
  | none => F
  termination_by nbors.length
  decreasing_by
    rw [List.length_erase_of_mem z.prop]
    apply Nat.sub_one_lt_of_le
    apply List.length_pos_iff_exists_mem.mpr
    exact ⟨z.val, z.prop⟩
    rfl

We then state and prove lemmas which show that the fan properties are invariant
under add. Since add is not structurally recursive, we induct over the function
definition itself using the fun_induction tactic; this allows for simpler proofs
despite the complex structure of the function.
The maximality condition is formulated similarly to the function definition itself
– after calling add on a fan, every neighbor of x not already present in the fan
cannot be added to the back of the fan without violating the coloring invariant.
Functional induction allows for a straightforward proof.
Finally, we define a wrapper function maximalFan that creates an object of type
Fan. For the data, we call add on the singleton fan ⟨y⟩ and the neighbor set
nbhd x −{y}. For the properties, we invoke the lemmas we proved earlier about
add along with the properties of the singleton fan.


3.3.3   Implementing the rotate operation

To rotate a fan F = ⟨f1 , ..., fk ⟩ on edge coloring C with a given color a, we
recolor {x, fk } with a, then recursively rotate the fan ⟨f1 , ..., fk−1 ⟩ with the
previous color of {x, fk }.
Since the formal definition of a fan is dependent on an edge coloring, we are


                                        11
required to prove that ⟨f1 , ..., fk−1 ⟩ is still a fan on C[{x, fk } 7→ a] before we
can make the recursive call.
To accomplish this, we write a function mkFan, which takes in the fan ⟨f1 , ..., fk ⟩
on edge coloring C (along with the color a and a few additional hypotheses),
and returns the fan ⟨f1 , ..., fk−1 ⟩ on edge coloring C[{x, fk } 7→ a].
def mkFan (a : Color c)
  (hvalid : edgeColorValid C (x, last F) a) (hsize : F.val.size > 1):
  Fan (setEdgeColor C (x, last F) a (last_present F) hvalid) x y where
  ...

We can then use mkFan to implement the rotateFan operation as described above.
def rotateFan (C : EdgeColoring c G) (F : Fan C x y) (a : Color c)
  (hvalid : edgeColorValid C (x, last F) a)
  : EdgeColoring c G :=
  let a’ := color C (x, last F)
  let C’ := setEdgeColor C (x, last F) a (last_present F) hvalid
  if h : F.val.size > 1 then
  let F’ := mkFan F a hvalid h
  have hvalid’ : edgeColorValid C’ (x, last F’) a’ := by . . .
  rotateFan C’ F’ a’ hvalid’
  else C’
  termination_by . . .
  decreasing_by . . .



3.4     Paths
3.4.1    Defining an alternating property

Before we can state a definition for an alternating path, we must define the
notion of a property that alternates over contiguous values in a list. Chain’ is
unfortunately not useful here, since we would need access to the indices of each
element in order to describe the alternating aspect.
Instead, we recursively define a function alternates, which takes in a function
p, two values a, b, and a list vs. alternates p a b vs indicates that the function
p alternates in value between a and b when evaluated over contiguous elements
of the list. That is, if vs = ⟨v1 , v2 , v3 , ..., vn ⟩, p v1 v2 = a, p v2 v3 = b, and so
on.
def alternates {V C : Type*} (p : V → V → C) (a b : C) : List V → Prop
  | []               => True
  | _ :: []          => True
  | v1 :: (v2 :: vs) => p v1 v2 = a ∧ alternates p b a (v2 :: vs)

We also define a function next, which returns the next value that p should
evaluate to, if an element were appended to the list that respects the alternating



                                           12
property. That is, for any element w, alternates p a b (vs ++ [w]) if and only
if next a b vs = p vn w.
def next {V C : Type*} (a b : C) : List V → C
  | []      => b
  | _ :: vs => next b a vs

We prove several properties of these functions, to more easily reason about them
later. Here are a few examples, where vs = ⟨v1 , ..., vn ⟩ is an arbitrary list.
    - next a b vs is always equal to either a or b.
    - For some element w, if alternates p a b vs and p vn w, alternates p a
      b (vs ++ [w]).
    - If alternates p a b (x :: xs), then alternates p b a xs.
It is often useful to view a list in two different ways: as its inductive definition,
and as a function that maps indices to values. This is possible in Lean, but it is
not particularly natural to do both at the same time, and translating between
representations often requires a lot of work. To reduce future messiness, we
prove a few lemmas involving indices:
    - For any list L, if next a b L = a, p L[L.length − 2] L[L.length − 1] = b,
      and vice versa (which we prove using mutual induction).
    - Let 0 < i < L.length − 1. Then, p L[i − 1] L[i] = a and p L[i] L[i + 1] = b,
      or vice versa.
There are also several library lemmas about Chain’ that translate between these
perspectives. These may be useful later, so we prove that if alternates p a b L,
then List.Chain’ (fun x y 7→ p x y = a ∨ p x y = b) L.

3.4.2   Creating a maximal path

Until now, we have defined each mathematical object as a structure type with
data and invariants. This allows for better organized and more readable code,
but has the unfortunate side effect of rendering many of Lean’s automation
tactics less effective (including induction, which will be necessary for many of
the proofs in this section).
To work around this, we declare the data and invariants as variables now, prove
some necessary lemmas, and then state “nice versions” of each lemma later.
variable
  (P : List (Vertex n)) (a b : Color c) (hne : P ̸= [])
  (x : Vertex n)
  (hx : P[0]’(. . .) = x)
  (hfree : b ∈ freeColorsOn C x)
  (hnodup : P.Nodup)
  (ha : a.isSome)
  (hb : b.isSome)
  (hneq : a ̸= b)


                                         13
Here, a path is represented as a list of vertices, such that the edge between
incident elements is colored either a or b. We require that a and b be actual
colors (rather than none), and that the path contain no cycles. As in the informal
definition, x is the first element of the path. hfree is not a path invariant, but
we can assume it here and supply it later when we create a maximal path in
the algorithm.
The algorithm requires us to produce a maximal alternating path containing
a vertex x whose edges are colored with either a or b, so our next task is to
implement this.
For convenience, we define a predicate alternatesColor using alternates. We
also define a function nextVertex, which finds a possible candidate for the next
vertex to add onto an alternating path. The result must be connected to the
last vertex in the path with an edge colored either a or b. If such a vertex z
exists, nextVertex returns some z; otherwise, it returns none.
To prove maximality later, we must also show that any candidates for the next
vertex cannot already be present in the path. This statement is never justified
in the informal proof, but is complex and tedious (almost 75 lines long!) to
formalize. Here is a sketch of the proof:
Let P = ⟨p0 = x, ..., pn ⟩. Let some z be the value returned by nextVertex.
Assume for the sake of contradiction that z is present in P . Then, there must
exist some i such that z = pi .
 Case 1: i = 0, so z = p0 = x. Since P is an alternating path, {pn , x} must be
 colored either a or b. b is free on x, so we can conclude {pn , x} is colored a,
 and {pn−1 , pn } must be colored b.
 Since the edge coloring is proper, x cannot have two incident edges colored a,
 and pn = p1 . P cannot contain duplicates, so P = ⟨x, p1 ⟩ and pn−1 = x. We
 reach a contradiction, since {x, p1 } cannot be colored both a and b.
 Case 2: 0 < i < n. Immediately, we know that n > 1.
 Since P is an alternating path, {pn , pi } must be colored either a or b. Assume
 WLOG that {pn , pi } is colored a. Since pi is an interior vertex, we have that
 {pi−1 , pi } is colored a, or that {pi , pi+1 } is colored a. In the former case,
 n = i − 1, but this is impossible since i < n. So, suppose that {pi , pi+1 } is
 colored a. Then, n = i + 1, and since the last path edge is colored a, the next
 one must be colored b. We reach a contradiction, since {pn , pi } cannot be both
 colored a and b.
 Case 3: i = n, so pi = pn . {pn , pi } is a self-loop, so it must be uncolored.
 But {pn , pi } must be colored either a or b, both of which cannot be none, so
 we reach a contradiction.
Armed with this lemma, we can define a function to extend an existing path
until it is maximal. extendPath is similar in structure to add in the fan library
(i.e. not structurally recursive, so we will have to manually prove termination).
We first search for a candidate vertex z to add to the path; if one does not exist,
we return the path unchanged. Otherwise, we add z to the path, and prove that


                                        14
each path invariant is still maintained before calling extendPath recursively on
the resulting path.
def extendPath {a b : Color c} {x : Vertex n}
  (P : List (Vertex n)) (hne : P ̸= [])
  (hx : P[0]’(by exact List.length_pos_iff.mpr hne) = x)
  (hfree : b ∈ freeColorsOn C x)
  (hnodup : P.Nodup)
  (ha : a.isSome) (hb : b.isSome) (hneq : a ̸= b)
  (hcolor : alternatesColor C P a b) : List (Vertex n) :=
  match Option.attach (nextVertex C P a b hne) with
  | none => P
  | some ⟨z, h⟩ =>
    have hnodup’ : (P.concat z).Nodup := by . . .
    have hcolor’ : alternatesColor C (P.concat z) a b := by . . .
    have hx’ : (P.concat z)[0]’(by simp) = x := by . . .
    extendPath (P.concat z) (by simp) hx’ hfree hnodup’ ha hb hneq
    hcolor’
  termination_by (n + 1) - P.length
  decreasing_by . . .

Like earlier, we use functional induction to prove that the path invariants are
preserved, and that this function produces a maximal path. The proofs are
omitted here.

3.4.3   Definitions

We can now finally proceed to defining an alternating path as a structure type:
structure Path (a b : Color c) (x : Vertex n) where
  val : List (Vertex n)
  nonemptyAx : val ̸= []
  firstElemAx : val[0] = x
  nodupAx : val.Nodup
  colorAx : alternatesColor C val a b

The strategy for creating a maximal path is similar to the version for fans: we
call extend on a singleton path. We define a predicate for path maximality (that
the next color in the path is free on its last vertex), and prove that the maximal
path satisfies this condition.

3.4.4   Reasoning about adjacent elements in a list

Earlier in this section, I referenced a common challenge in proving theorems
about lists – that it is difficult to translate between viewing a list inductively,
and viewing it as a function that maps indices to values. This was especially
true when reasoning about adjacent pairs in a list, a notion that Mathlib does
not already define. We will define it here.


                                        15
First, a definition based on indices: if elements u and v are adjacent in a list xs,
there must exist an index i such that u = xs[i] and v = xs[i + 1], or vice versa.
variable
  {α : Type*}
  {xs : List α}

def adjacent (u v : α) (xs : List α) :=
  (∃ i, ∃ (h : i < xs.length - 1), xs[i] = u ∧ xs[i+1] = v) ∨
  (∃ i, ∃ (h : i < xs.length - 1), xs[i] = v ∧ xs[i+1] = u)

Second, an inductive definition: given a list xs, allAdjacentPairs xs returns
the list of each adjacent pair in xs.
def allAdjacentPairs : List α → List (α × α)
  | [] => []
  | [_] => []
  | x1 :: x2 :: xs => (x1 , x2 ) :: (x2 , x1 ) :: (allAdjacentPairs (x2 ::
    xs))

We prove a lemma that allows us to translate between these notions of adjacency.
Functional induction is useful here, since the recursive cases do not mirror the
inductive structure of the list.
theorem mem_allAdjacentPairs_iff_adjacent (u v : α) (xs : List α) :
  (u, v) ∈ allAdjacentPairs xs ↔ adjacent u v xs :=


3.4.5   Path edges

By definition, (u, v) is a path edge if u and v are adjacent in P . So, we define
path edges as adjacent pairs in P :
def pathEdges := allAdjacentPairs P.val

We prove a few more useful properties:
    - Let u, v be adjacent in P , and let v be an interior vertex. There must
      exist some vertex w adjacent to v, such that (u, v) and (u, w) are different
      colors.
    - If a vertex v is a member of a maximal path, any of its incident edges
      colored a or b must be present in the path.

3.4.6   Implementing the invert operation

Our last task is to implement the invert operation described earlier.
The simplest possible solution is to iteratively flip the color of each edge. Un-
fortunately, this will not work here, since we defined setEdgeColor to only allow
edges to be recolored with valid colors. With a clever choice of hypotheses, we


                                        16
could recursively flip the tail of the path, then recolor the head. However, since
the proof of correctness will require us to reason over multiple nested function
calls, I chose a less elegant but simpler solution – fully uncoloring the path, and
then recoloring it in the opposite order. This intermediate step makes it easier
to prove that the invariants are maintained.
We implement a function uncolor, which takes in a list of vertices and recursively
sets the edge color of each adjacent pair to none. We also prove some auxiliary
lemmas:
    - Setting the color of a non-path edge does not affect the color invariant of
      the path.
    - If a color was free on a vertex prior to uncoloring the path, it must be free
      after.
    - After uncoloring the path, a and b must both be free on every path vertex.
    - Every non-path edge is unaffected by uncoloring the path.
    - After uncoloring the path, every edge in the path is colored none.
We can now proceed to defining recolor, which takes in an edge coloring C,
colors a, b, and a list of vertices L, along with some hypotheses. If L is an
empty list or a singleton, we return the edge coloring unchanged. Otherwise, let
L = p1 :: p2 :: ps. We call recolor recursively on edge coloring C[(p1 , p2 ) 7→ b],
colors b, a (with order flipped), and list of vertices p2 :: ps.
The one subtlety here is that we cannot carry through the hypothesis that both
a and b are free on every vertex in L. This is true at the very start of the
procedure, but once the first path edge is colored, b is no longer free on p2 .
We account for this asymmetry by a more careful choice of hypotheses: we are
always guaranteed that the color we used last is free on the tail elements of L,
and that the color we will use next is free on every element in L. This is all we
need to show that each setEdgeColor operation is valid.
def recolor (C : EdgeColoring c G) (a b : Color c) (ha : a.isSome) (hb :
    b.isSome)
  (hne : a ̸= b)
  (L : List (Vertex n)) (hnodup : L.Nodup)
  (h1 : List.Chain’ (fun e1 e2 7→ present G (e1 , e2 )) L)
  (h2 : ∀ v ∈ L.tail, a ∈ freeColorsOn C v)
  (h3 : ∀ v ∈ L, b ∈ freeColorsOn C v)
  : EdgeColoring c G :=
  match hl : L with
  | [] => C
  | [_] => C
  | p1 :: p2 :: ps =>
    have hpres : present G (p1 , p2 ) := . . .
    have hvalid : edgeColorValid C (p1 , p2 ) b := . . .
    have auxa : ∀ v ∈ p2 :: ps,
      a ∈ freeColorsOn (setEdgeColor C (p1 , p2 ) b hpres hvalid) v := . . .
    have auxb : ∀ v ∈ (p2 :: ps).tail,


                                        17
      b ∈ freeColorsOn (setEdgeColor C (p1 , p2 ) b hpres hvalid) v := . . .
    recolor (setEdgeColor C (p1 , p2 ) b hpres hvalid)
      b a hb ha (. . .) (p2 :: ps) (. . .) (. . .) auxb auxa

We prove the following specifications:
    - If an edge is not present in the path, its color remains invariant.
    - The path alternates color between b and a.
The main inversion function, invert, uncolors the path and then recolors it.
def invert {P : Path C a b x} (h : isMaximalPath P) : EdgeColoring c G :=
  recolor (uncolor C a b ha hb P.val P.nodupAx P.colorAx)
    a b ha hb hne P.val P.nodupAx (. . .) (. . .)

To prove its correctness, we start by defining the predicate isInverted, which
takes in two edge colorings C and C ′ , and a path P . isInverted C C’ P indicates
that for all edges:
    - isInverted_notmem C C’ P: if e ∈
                                     / P , color C e = color C’ e.
    - isInverted_mem C C’ P: if e ∈ P :
        – If color C e = a, then color C’ e = b.
        – If color C e = b, then color C’ e = a.
Lastly, we prove more specification lemmas about invert:
    - The edge coloring returned by the invert function respects the isInverted
      predicate.
    - If an edge is not colored a or b prior to the inversion, it is not affected by
      the inversion.
    - If an edge is not colored a or b after the inversion, it was not affected by
      the inversion.
    - If a vertex is present in a maximal path and has an incident edge colored
      with a or b after the inversion, that edge must be present in the path.
    - If a was free on a path vertex prior to the inversion, b must be free after
      (and vice versa).
Many of these lemmas are variations of each other, for convenience in writing
later proofs.


4    Formalization: the algorithm
The implementation of the algorithm is similar to the pseudocode in the informal
proof: we define a subroutine extendColoring, which takes in a proper edge
coloring and recursively extends it until it is complete. The main function,
mkEdgeColoring, calls extendColoring on the empty edge coloring.
A few notes:


                                         18
   - The proofs of each have statement are omitted for brevity.
   - To prove termination, we must show that every edge in E is uncolored in
     C. This is proved by induction, similarly to its informal counterpart.
   - We will implement findSubfan and prove the subfan existence lemma in
     the next section.
Here are the implementations of both functions; they are not too different from
the pseudocode in the informal proof!
def extendColoring (E : EdgeSet G) (C : EdgeColoring (maxDegree G + 1) G)
  (h : ∀ e ∈ E.val, color C e = none) :
  EdgeColoring (maxDegree G + 1) G :=
match hE : E.val with
| [] => C
| (x, y) :: es =>
  have hterm : (remove E (x, y)).val.length < E.val.length
  have h’ : ∀ e ∈ (remove E (x, y)).val, color C e = none

  let F := maximalFan C (. . .)
  have auxF : isMaximal F

  let a := (freeColorsOn C (last F)).head (existsFreeColor C (by omega)
    (last F))
  let b := (freeColorsOn C x).head (existsFreeColor C (by omega) x)
  have ha : a.isSome
  have hb : b.isSome
  have auxa : a ∈ freeColorsOn C (last F)
  have auxb : b ∈ freeColorsOn C x

  if heq : a = b then
    have aux : edgeColorValid C (x, last F) a
    let C’ := (rotateFan C F a aux)
    have h’ : ∀ e ∈ (remove E (x, y)).val, color C’ e = none
    extendColoring (remove E (x, y)) (rotateFan C F a aux) h’

  else
    let P : Path C a b x := maximalPath C ha hb heq (by simp [b])
    have auxP : isMaximalPath P
    let C’ := invert ha hb heq auxb auxP
    have auxC’ : isInverted C C’ P
    let F’ := findSubfan ha hb auxb auxC’ auxa (by simp_all) auxF auxP
    have aux : edgeColorValid C’ (x, last F’) a
    let C’’ := (rotateFan C’ F’ a aux)
    have h’ : ∀ e ∈ (remove E (x, y)).val, color C’’ e = none
    extendColoring (remove E (x, y)) C’’ h’

termination_by
  E.val.length

def mkEdgeColoring (G : Graph n) : EdgeColoring (maxDegree G + 1) G :=


                                      19
  extendColoring (toEdgeSet G) empty (. . .)



4.1    Finding the subfan
The inversion of the alternating path guarantees the existence of a subfan of F ,
such that a is free on its last element.
The informal proof of the subfan existence lemma is subtle, so to complete the
formalization we must prove the following statements:
    - If a vertex is not a path endpoint, its free colors are unaffected by the
      path inversion.
    - If a color not equal to a or b was free on a vertex prior to the path inversion,
      it remains free after the inversion.
    - If the path is empty, the color property of a fan is preserved. (This is
      trivially true since the inversion does nothing, but requires a little bit of
      work to formalize.)
    - Suppose there exists a fan edge e with color a. Then, every edge in the
      fan not equal to e is unchanged by the path inversion.
    - The maximal path containing x is a singleton if there does not exist a fan
      edge colored a.
The statement and proof of the lemma is omitted here, since it follows the
same structure as its informal counterpart but required extensive casework and
arithmetic. Control structures (especially tactics that allowed me to work on
multiple goals at once), and specialized automation (such as omega and grind)
were particularly helpful.
Now that we have proved the existence of the subfan, we can proceed to finding
it. This task is straightforward – if there is an index i such that {x, fi } is colored
a and fi−1 ∈ / P , we return the first i − 1 elements of F . Otherwise, we return
F unchanged. In Lean:
def mkSubfan (F : Fan C x y) (P : Path C a b x) : Array (Vertex n) :=
  match Array.findFinIdx? (fun u 7→ color C (x, u) = a) F.val with
  | some i => if F.val[i.val - 1] ∈ P.val then F.val else Array.extract
    F.val 0 i
  | none => F.val

We can now write a “nice” version of this function that returns a Fan object
(i.e. that contains a proof of each fan property). The last property left to prove
is that a is always free on the last vertex in the subfan. The proofs are omitted
here for brevity.




                                          20
4.2    The proof of correctness
In the informal proof, the correctness argument had two main components:
properness and completeness. The first part is already done – mkEdgeColoring
produces an object of type EdgeColoring, which is proper by definition! All that
is left is proving completeness.
We use a familiar strategy here – first, we prove that extendColoring preserves
properness (i.e. that every edge we have removed from the edge set is colored
in the graph).
theorem extendColoring_proper (E : EdgeSet G) (C : EdgeColoring
    (maxDegree G + 1) G)
  (he1 : ∀ e ∈ E.val, color C e = none)
  (e : Edge n) (h1 : e ∈ (toEdgeSet G).val)
  (h2 : e ∈
          / E.val → (color C e).isSome) :
  (color (extendColoring E C he1) e).isSome :=

The proof is similar to its informal counterpart (but requires the rotation lemmas
we proved earlier), so we omit it here.
We can now state the last proof of correctness: that mkEdgeColoring creates a
proper edge coloring.
theorem mkEdgeColoring_proper :
  ∀ e ∈ (toEdgeSet G).val, (color (mkEdgeColoring G) e).isSome :=

The proof follows almost immediately from the previous lemma, and we are
done.


5     Conclusion
In this work, I wrote a polynomial-time verified implementation of the Misra
and Gries edge coloring algorithm in the proof assistant Lean 4. The algorithm
was initially developed to simplify the proof of a complex theorem, so having a
computer-verified proof of correctness is exciting!
Using an interactive theorem prover was essential – many of the proofs required
subtle arguments that would be difficult for fully automated tools to synthesize.
However, this choice presented its own set of challenges:
    - A common strategy in mathematical proof is to translate between different
      representations of the same object. For example, within a single proof, I
      often needed to view a list both inductively and as a function mapping
      indices to values. Such translations are more challenging in formalized
      proofs, but I addressed this by writing dedicated lemmas to carry them
      out wherever they were needed.
    - Formalizing a mathematical algorithm introduces competing objectives
      that have to be balanced during implementation: representations that


                                       21
         are easy to reason about mathematically are not always the most com-
         putationally efficient, and vice versa. I chose to prioritize computational
         efficiency, since it is an inherent property that cannot be improved without
         changing the underlying representations. To manage the messy and com-
         plex proofs that resulted, I relied on a variety of strategies, particularly
         automation wherever possible.
       - These considerations raise the question of whether it would be easier to
         use entirely separate representations for computation and for proof, and
         then show that they are equivalent. I suspect the proofs would be simpler
         – especially if I used the definitions in Mathlib – though this would require
         a significant amount of additional translation back and forth.
There are many possible directions for future work. The library could be helpful
to implement more verified graph-theoretic algorithms with nice computational
properties. In addition, there are many places where macros, custom automa-
tion, or different choices of representation could have allowed for shorter and
more elegant proofs. As more work like this is completed, I am excited to
see best practices emerge for representing and reasoning about mathematical
objects.


References
 [1]     Arohee Bhoja. A verified implementation of the Misra and Gries edge
         coloring algorithm. url: https://github.com/aroheebhoja/vizing.
 [2]     V. G. Vizing. “Critical graphs with given chromatic class”. In: Metody
         Diskret. Analiz. 5 (1965), pp. 9–17.
 [3]     Ian Holyer. “The NP-Completeness of Edge-Coloring”. In: SIAM Journal
         on Computing 10.4 (1981), pp. 718–720. doi: 10.1137/0210055. eprint:
         https://doi.org/10.1137/0210055. url: https://doi.org/10.1137/
         0210055.
 [4]     Béla Bollobás. Graph theory: an introductory course. Vol. 63. Springer
         Science & Business Media, 2012.
 [5]     Josyula R. Rao and Edsger W. Dijkstra. “Designing the proof of Vizing’s
         Theorem”. In: Programming and Mathematical Method. Ed. by Manfred
         Broy. Berlin, Heidelberg: Springer Berlin Heidelberg, 1992, pp. 17–25.
         isbn: 978-3-642-77572-7.
 [6]     J. Misra and David Gries. “A constructive proof of Vizing’s theorem”. In:
         Information Processing Letters 41.3 (1992), pp. 131–133. issn: 0020-0190.
         doi: https://doi.org/10.1016/0020-0190(92)90041-S. url: https:
         //www.sciencedirect.com/science/article/pii/002001909290041S.
 [7]     Tobias Nipkow. “Gale-Shapley Verified”. In: Journal of Automated Rea-
         soning 68.2 (June 2024), p. 12. issn: 1573-0670. doi: 10.1007/s10817-
         024-09700-x. url: https://doi.org/10.1007/s10817-024-09700-x.


                                           22
 [8]   Ran Chen et al. “Formal Proofs of Tarjan’s Algorithm in Why3, Coq,
       and Isabelle”. In: CoRR abs/1810.11979 (2018). arXiv: 1810.11979. url:
       http://arxiv.org/abs/1810.11979.
 [9]   Joachim Breitner. Proving Vizing’s Theorem with Rodin. Mar. 2011. url:
       https://www.joachim-breitner.de/.
[10]   Leonardo de Moura and Sebastian Ullrich. “The Lean 4 Theorem Prover
       and Programming Language”. In: Automated Deduction – CADE 28. Ed.
       by André Platzer and Geoff Sutcliffe. Cham: Springer International Pub-
       lishing, 2021, pp. 625–635. isbn: 978-3-030-79876-5.
[11]   The mathlib Community. “The lean mathematical library”. In: Proceed-
       ings of the 9th ACM SIGPLAN International Conference on Certified
       Programs and Proofs. CPP 2020. New Orleans, LA, USA: Association
       for Computing Machinery, 2020, pp. 367–381. isbn: 9781450370974. doi:
       10.1145/3372885.3373824. url: https://doi.org/10.1145/3372885.
       3373824.




                                      23
