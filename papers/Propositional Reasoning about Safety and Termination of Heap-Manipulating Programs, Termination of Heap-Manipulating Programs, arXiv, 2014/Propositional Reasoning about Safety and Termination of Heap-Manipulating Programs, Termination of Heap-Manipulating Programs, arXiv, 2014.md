                                             Propositional Reasoning about Safety and
                                            Termination of Heap-Manipulating Programs

                                                       Cristina David, Daniel Kroening, and Matt Lewis

                                                                         University of Oxford
arXiv:1410.5088v1 [cs.LO] 19 Oct 2014




                                              Abstract. This paper shows that it is possible to reason about the
                                              safety and termination of programs handling potentially cyclic, singly-
                                              linked lists using propositional reasoning even when the safety invariants
                                              and termination arguments depend on constraints over the lengths of
                                              lists. For this purpose, we propose the theory SLH of singly-linked lists
                                              with length, which is able to capture non-trivial interactions between
                                              shape and arithmetic. When using the theory of bit-vector arithmetic as
                                              a background, SLH is efficiently decidable via a reduction to SAT. We
                                              show the utility of SLH for software verification by using it to express
                                              safety invariants and termination arguments for programs manipulating
                                              potentially cyclic, singly-linked lists with unrestricted, unspecified shar-
                                              ing. We also provide an implementation of the decision procedure and use
                                              it to check safety and termination proofs for several heap-manipulating
                                              programs.


                                        Keywords: Heap, SAT, safety, termination.


                                        1   Introduction
                                        Proving safety of heap-manipulating programs is a notoriously difficult task. One
                                        of the main culprits is the complexity of the verification conditions generated for
                                        such programs. The constraints comprising these verification conditions can be
                                        arithmetic (e.g. the value stored at location pointed by x is equal to 3), structural
                                        (e.g. x points to an acyclic singly-linked list), or a combination of the first two
                                        when certain structural properties of a data structure are captured as numeric
                                        values (e.g. the length of the list pointed by x is 3). Solving these combined
                                        constraints requires non-trivial interaction between shape and arithmetic.
                                            For illustration, consider the program in Figure 1b, which iterates simulta-
                                        neously over the lists x and y. The program is safe, i.e., there is no null pointer
                                        dereferencing and the assertion after the loop holds. While the absence of null
                                        pointer dereferences is trivial to observe and prove, the fact that the assertion
                                        after the loop holds relies on the fact that at the beginning of the program and
                                        after each loop iteration the lengths of the lists z and t are equal. Thus, the
                                        specification language must be capable of expressing the fact that both z and t
                                        reach null in the same number of steps. Note that the interaction between shape
                                        and arithmetic constraints is intricate, and cannot be solved by a mere theory
                                        combination.
2

    The problem is even more pronounced when proving termination of heap-
manipulating programs. The reason is that, even more frequently than in the
case of safety checking, termination arguments depend on the size of the heap
data structures. For example, a loop iterating over the nodes of such a data
structure terminates after all the reachable nodes have been explored. Thus,
the termination argument is directly linked to the number of nodes in the data
structure. This situation is illustrated again by the loop in Figure 1b.
    There are few logics capable of expressing this type of interdependent shape
and arithmetic constraint. One of the reasons is that, given the complexity of
the constraints, such logics can easily become undecidable (even the simplest use
of transitive closure leads to undecidability [1]), or at best inefficient.
    The tricky part is identifying a logic expressive enough to capture the cor-
responding constraints while still being efficiently decidable. One work that in-
spired us in this endeavor is the recent approach by Itzhaky et al. on reasoning
about reachability between dynamically allocated memory locations in linked
lists using effectively-propositional (EPR) reasoning [2]. This result is appealing
as it can harness advances in SAT solvers. The only downside is that the logic
presented in [2] is better suited for safety than termination checking, and is best
for situations where safety does not depend on the interaction between shape
and arithmetic. Thus, our goal is to define a logic that can be used in such
scenarios while still being reducible to SAT.
    This paper shows that it is possible to reason about the safety and termi-
nation of programs handling potentially cyclic, singly-linked lists using proposi-
tional reasoning. For this purpose, we present the logic SLH which can express
interdependent shape and arithmetic constraints. We empirically prove its utility
for the verification of heap-manipulating programs by using it to express safety
invariants and termination arguments for intricate programs with potentially
cyclic, singly-linked lists with unrestricted, unspecified sharing.
   SLH is parametrised by the background arithmetic theory used to express the
length of lists (and implicitly every numeric variable). The decision procedure re-
duces validity of a formula in SLH to satisfiability of a formula in the background
theory. Thus, SLH is decidable if the background theory is decidable.
    As we are interested in a reduction to SAT, we instantiate SLH with the
theory of bit-vector arithmetic, resulting in SLH[TBV ]. This allows us to handle
non-linear operations on lists length (e.g. the example in Figure 1c), while still
retaining decidability. However, SLH can be combined with other background
theories, e.g., Presburger arithmetic.
    We provide an implementation of our decision procedure for SLH[TBV ] and
test its efficiency by verifying a suite of programs against safety and termination
specifications expressed in SLH. Whenever the verification fails, our decision
procedure produces a counterexample.
                                                                                    3



        Contributions:
    * We propose the theory SLH of singly-linked lists with length. SLH allows
    unrestricted sharing and cycles.
    * We define the strongest post-condition for formulae in SLH.
    * We show the utility of SLH for software verification by using it to express
    safety invariants and termination arguments for programs with potentially
    cyclic singly-linked lists.
    * We present the instantiation SLH[TBV ] of SLH with the theory of bit-vector
    arithmetic. SLH[TBV ] can express non-linear operations on the lengths of
    lists, while still retaining decidability.
    * We provide a reduction from satisfiability of SLH[TBV ] to propositional
    SAT.
    * We provide an implementation of the decision procedure for SLH[TBV ]
    and test it by checking safety and termination for several heap-manipulating
    programs (against provided safety invariants and termination arguments).



2     Motivation

Consider the examples in Figure 1. They all capture situations where the safety
(i.e. absence of null pointer dereferencing and no assertion failure) and termina-
tion of the program depend on interdependent shape and arithmetic constraints.
In this section we only give an intuitive description of these examples, and we
revisit and formally specify them in Section 7. We assume the existence of the
following two functions: (1) length(x) returns the number of nodes on the path
from x to NULL if the list pointed by x is acyclic, and MAXINT otherwise;
(2) circular(x) returns true iff the list pointed by x is circular (i.e., x is part of
a cycle).
    In Figure 1a, we iterate over the potentially cyclic singly-linked list pointed
by x a number of times equal with the result of length(x). The program is safe
(i.e. y is not NULL at loop entry) and terminating. A safety invariant for the
loop needs to capture the length of the path from y to NULL.
    The loop in Figure 1b iterates over the lists pointed by x and y, respectively,
until one of them becomes NULL. In order to check whether the assertion after
the loop holds, the safety invariant must relate the length of the list pointed by
x to the length of the list pointed by y. Similarly, a termination argument needs
to consider the length of the two lists.
    The example in Figure 1c illustrates how non-linear arithmetic can be en-
coded via singly-linked lists. Thus, the loop in divides(x, y) iterates over the list
pointed by x a number of nodes equal to the quotient of the integer division
length(x)/length(y) such that, after the loop, the list pointed by z has a length
equal with the remainder of the division.
    The function in Figure 1d returns true iff the list passed in as a parameter is
circular. The functional correctness of this function is captured by the assertion
4




                                                      List x, y, z = x, t = y;

                                                      assume(length(x)==length(y));
        List x, y = x;
        int n = length(x), i = 0;                     while (z!=NULL && t!=NULL) {
                                                        z = z→next;
        while ( i < n) {                                t = t→next;
          y = y→next;                                 }
          i = i+1;
        }                                             assert (z==NULL && t==NULL);

                           (a)                                            (b)




int divides(List x, List y) {
  List z = y;
  List w = x;

    assume(length(x)!=MAXINT &&                         int isCircular (List l ) {
          length(y)!=MAXINT &&                            List p = q = l;
          y != NULL);
                                                             do {
    while (w != NULL) {                                        if (p != NULL) p = p→next;
      if (z == NULL) z = y;                                    if (q != NULL) q = q→next;
      z = z→next;                                              if (q != NULL) q = q→next;
      w = w→next;                                            }
    }                                                        while (p!=NULL && q!=NULL
                                                                    && p!=q);
    assert (z == NULL ⇔
            length(x)%length(y)==0);                         assert (p == q ⇔ circular(l));
    return z == NULL;                                        return p == q;
}                                                       }

                           (c)                                            (d)

                            Fig. 1: Motivational examples.
                                                                                    5

after the loop checking that pointers p and q end up being equal iff the list l is
circular.


3     Theory of Singly Linked Lists with Length

In this section we introduce the theory SLH for reasoning about potentially
cyclic singly linked lists.


3.1   Informal Description of SLH

We imagine that there is a set of pointer variables x, y, . . . which point to heap
cells. The cells in the heap are arranged into singly linked lists, i.e. each cell has
a “next” pointer which points somewhere in the heap. The lists can be cyclic
and two lists can share a tail, so for example the following heap is allowed in our
logic:
                                                     •      y

                                  z    •    •   •

                                  x    •        •    null


    Our logic contains functions for examining the state of the heap, along with
the four standard operations for mutating linked lists: new , assign, lookup and
update. We capture the side-effects of these mutation operators by explicitly
naming the current heap – we introduce heap variables h, h′ etc. which denote
the heap in which each function is to be interpreted. The mutation operators
then become pure functions mapping heaps to heaps. The heap functions of the
logic are illustrated by example in Figure 3 and have the following meanings:
            alias (h, x, y): do x and y point to the same cell in heap h?
          isPath(h, x, y): is there a path from x to y in h?
     pathLength(h, x, y): the length of the shortest path from x to y in h.
             isNull (h, x): is x null in h?
           circular (h, x): is x part of a cycle, i.e. is there some non-empty path from
                             x back to x in h?
         h′ = new (h, x): obtain h′ from h by allocating a new heap cell and reas-
                             signing x so that it points to this cell. The newly allocated
                             cell is not reachable from any other cell and its successor is
                             null. This models the program statement x = new(). For
                             simplicity, we opt for this allocation policy, but we are not
                             restricted to it.
     h′ = assign(h, x, y): obtain h′ from h by assigning x so that it points to the same
                             cell as y. Models the statement x = y.
    h′ = lookup(h, x, y): obtain h′ from h by assigning x to point to y’s successor.
                             Models the statement x = y→next.
    h′ = update(h, x, y): obtain h′ from h by updating x’s successor to point to y.
                             Models x→next = y.
6




                                                    •     •       •         •     •    •
    •   •        •         •        •       •
                                                                        ⇒
                       ⇒                            x            null             •
    y   x       null       y        x   null
                                                                                  x   null

                lookup(h, x, y)                                     new (x)
                 x = y→next;                                      x = new();


    •   •         •        •        •       •       •     •       •         •     •    •

                       ⇒                                                ⇒
        •                           •                     •                       •

    x   y       null       x        y   null        x     y      null       x     y   null
                 assign(x, y)                                   update(x, y)
                    x = y;                                      x→next = y;


            z                           •       y
                                                    pathLength (x, y) = 3
                                                        isPath(z, y) = true
            •          •       •
                                                        isPath(x, z) = false
                                                          alias(x, z) = false
            •                  •
                                                              isNull(x) = false
                                                         circular (y) = true
            x              null


                                   Fig. 3: SLH by example
                                                                                          7

3.2   Syntax of SLH

The theory of singly-linked lists with length, SLH, uses a background arithmetic
theory TB for the length of lists (implicitly any numeric variable). Thus, SLH
has the following signature:

      ΣSLH = ΣB ∪ {alias(·, ·, ·), isPath(·, ·, ·), pathLength(·, ·, ·), isNull (·, ·),
                  circular (·, ·), ·=new (·, ·), ·=assign(·, ·, ·),
                  ·=lookup(·, ·, ·), ·=update(·, ·, ·)}.

where the nine new symbols correspond to the heap-specific functions described
in the previous section.

Sorts. Heap variables (e.g. h in alias(h, x, y)) have sort SH , pointer variables
have sort SAddr (e.g. x and y in alias(h, x, y)), numeric variables have sort SB
(e.g. n in n = pathLength(h, x, y)).

Literal and formula. A literal in SLH is either a heap function or a TB -literal. A
formula in SLH is a boolean combination of SLH-literals.


3.3   Semantics of SLH

We give the semantics of SLH by defining the models in which an SLH formula
holds. An interpretation Γ is a function mapping free variables to elements of
the appropriate sort. If an SLH formula φ holds in some interpretation Γ , we
say that Γ models φ and write Γ |= φ.
   Interpretations may be constructed using the following substitution rule:
                                             (
                                                 H     if x = h
                          Γ [h 7→ H](x) =
                                                 Γ (x) otherwise

    Pointer variables are considered to be a set of constant symbols and are thus
given a fixed interpretation. The only thing that matters is that their interpreta-
tion is pairwise different. We assume that the pointer variables include a special
name null. The set of pointer variables is denoted by the symbol P .
    We will consider the semantics of propositional logic to be standard and the
semantics of TB given, and thus just define the semantics of heap functions. To
do this, we will first define the class of objects that will be used to interpret heap
variables.

Definition 1 (Heap). A heap over pointer variables P is a pair H = hL, Gi.
G is a finite graph with vertices V (G) edges E(G). L : P → V (G) is a labelling
function mapping each pointer variable to a vertex of G. We define the cardinality
of a heap to be the cardinality of its underlying graph’s vertices: kHk = kV (G)k.
8

Definition 2 (Singly Linked Heaps). A heap H = hL, Gi is a singly linked
heap iff each vertex has outdegree 1, except for a single sink vertex that has
outdegree 0 and is labelled by null:

                ∀v ∈ V (G).(outdegree(v) = 1 ∧ L(null) 6= v)∨
                            (outdegree(v) = 0 ∧ L(null) = v)


    Having defined our domain of discourse, we are now in a position to define
the semantics of the various heap functions introduced in Section 3.1. We begin
with the functions examining the state of the heap and will use a standard
structural recursion to give the semantics of the functions with respect to an
                                                                             n
implicit interpretation Γ , so that JhK = Γ (h). We will use the shorthand u → v
to say that if we start at node u, then follow n edges, we arrive at v. We also
use L(H) to select the labelling function L from H:

                                  n   def
                                u → v = hu, vi ∈ E n
                                      def         n
                            u →∗ v = ∃n ≥ 0.u → v
                                      def         n
                           u →+ v = ∃n > 0.u → v


                0
    Note that u → u. The semantics of the heap functions are then:

                                                                  
                           def                  n
    JpathLength(h, x, y)KΓ = min {n | L(JhK)(x) → L(JhK)(y)} ∪ {∞}
                          def
         Jcircular (h, x)KΓ = ∃v ∈ V (JhK).L(JhK)(x) →+ v ∧ v →+ L(JhK)(x)
                          def
         Jalias (h, x, y)KΓ = JpathLength(h, x, y)K = 0
                          def
        JisPath(h, x, y)KΓ = JpathLength(h, x, y)K 6= ∞
                          def
          JisNull (h, x)KΓ = JpathLength(h, x, null)K = 0


    Note that since the graph underlying H has outdegree 1, pathLength and
circular can be computed in O(kHk) time, or equivalently they can be encoded
with O(kHk) arithmetic constraints.
    To define the semantics of the mutation operations, we will consider sep-
arately the effect of each mutation on each component of the heap – the la-
belling function L, the vertex set V and the edge set E. Where a mutation’s
effect on some heap component is not explicitly stated, the effect is id. For
example, assign does not modify the vertex set, and so assign V = id. In the
following definitions, we will say that succ(v) is the unique vertex such that
(v, succ(v)) ∈ E(H).
                                                                                    9


                                 def
                 Jnew V (h, x)KΓ = V (JhK) ∪ {q}where q is a fresh vertex
                                 def
                  Jnew E (h, x)KΓ = E(JhK) ∪ {(q, null)}
                                 def
                  Jnew L (h, x)KΓ = L(JhK)[x 7→ q]
                                 def
             Jassign L (h, x, y)KΓ = L(JhK)[x 7→ L(JhK)(y)]
                                 def
             Jlookup L (h, x, y)KΓ = L(JhK)[x 7→ succ(y)]
                                 def
             Jupdate E (h, x, y)KΓ = (E(JhK) \ {(L(JhK)(x), succ(L(JhK)(x)))}) ∪
                                {(L(JhK)(x), L(JhK)(y))}



4     Deciding Validity of SLH
We will now turn to the question of deciding the validity of an SLH formula,
that is for some formula φ we wish to determine whether φ is a tautology or if
there is some Γ such that Γ |= ¬φ. To do this, we will show that SLH enjoys a
finite model property and that the existence of a fixed-size model can be encoded
directly as an arithmetic constraint.
     Our high-level strategy for this proof will be to define progressively coarser
equivalence relations on SLH heaps that respect the transformers and observa-
tion functions. The idea is that all of the heaps in a particular equivalence class
will be equivalent in terms of the SLH formulae they satisfy. We will eventually
arrive at an equivalence relation (homeomorphism) that is sound in the above
sense and which is also guaranteed to have a small heap in each equivalence
class.
     From here on we will slightly generalise the definition of a singly linked heap
and say that the underlying graph is weighted with weight function w : E(H) →
N. When we omit the weight of an edge (as we have in all heaps up until now),
it is to be understood that the edge’s weight is 1.

4.1   Sound Equivalence Relations
We will say that an equivalence relation ≈ is sound if the following conditions
hold for each pair of pointer variables x, y and transformer τ :
        ∀H, H ′ · H ≈ H ′ ⇒pathLength(H, x, y) = pathLength(H ′ , x, y) ∧          (1)
                                                              ′
                            circular (H, x) = circular (H , x) ∧                   (2)
                            τ (H) ≈ τ (H ′ )                                       (3)
    The first two conditions say that if two heaps are in the same equivalence
class, there is no observation that can distinguish them. The third condition says
that the equivalence relation is inductive with respect to the transformers. There
is therefore no sequence of transformers and observations that can distinguish
two heaps in the same equivalence class.
    We begin defining two sound equivalence relations:
10

Definition 3 (Reachable Sub-Heap). The reachable sub-heap H|P of a heap
H is H with vertices restricted to those reachable from the pointer variables P :
                        V (H|P ) = {v | ∃p ∈ P.hL(p), vi ∈ E ∗ }
      Then the relation {hH, H ′ i | H|P = H ′ |P } is sound.
Definition 4 (Heap Isomorphism). Two heaps H = hL, Gi, H ′ = hG′ , L′ i
are isomorphic (written H ≃ H ′ ) iff there exists a graph isomorphism f : G|P →
G′ |P that respects the labelling function, i.e., ∀p ∈ P.f (L(p)) = L′ (p).
Example 1. H and H ′ are not isomporphic, even though their underlying graphs
are.
                  H:                    H′ :
                         •      •             •     •

                              x    null              x       null
Theorem 1. Heap isomorphism is a sound equivalence relation.

4.2     Heap Homeomorphism
The final notion of equivalence we will describe is the weakest. Loosely, we would
like to say that two heaps are equivalent if they are “the same shape” and if
the shortest distance between pointer variables is the same. To formalise this
relationship, we will be using an analog of topological homeomorphism.
Definition 5 (Edge Subdivision). A graph G′ is a subdivison of G iff G′ can
be obtained by repeatedly subdividing edges in G, i.e., for some edge (u, v) ∈ E(G)
introducing a fresh vertex q and replacing the edge (u, v) with edges (u, q), (q, v)
such that w′ (u, q) + w′ (q, v) = w(u, v). Subdivision for heaps is defined in terms
of their underlying graphs.
   We define a function subdivide, which subdivides an edge in a heap. As usual,
the function is defined componentwise on the heap:
subdivide V (H, u, v, k) =V ∪ {q}
subdivide E (H, u, v, k) = (E \ {(u, v)}) ∪ {(u, q), (q, v)}
subdivide W (H, u, v, k) =W (H)[(u, v) 7→ ∞, (u, q) 7→ k, (q, v) 7→ W (H)(u, v) − k]
   The dual of edge subdivision is edge smoothing – if we have two edges
   n    m
u −→ q −→ v, where q is unlabelled and has no other incoming edges, we can
                                   n+m
remove q and add the single edge u −→ v.
Example 2. H ′ is a subdivision of H.
               H:                             H′ :
                           3                             1       2
                     •            •                  •       •        •

                        x           null             x               null
                                                                                                          11

Lemma 1 (Subdividing an Edge Preserves Observations). If H ′ is ob-
tained from H by subdividing one edge, then for any x, y we have:

                    pathLength(H, x, y) = pathLength(H ′ , x, y)                                          (4)
                         circular (H, x) = circular (H ′ , x)                                             (5)

Definition 6 (Heap Homeomorphism). Two heaps H, H ′ are homeomor-
phic (written H ∼ H ′ ) iff there there is a heap isomorphism from some subdivi-
sion of H to some subdivision of H ′ .
    Intuitively, homeomorphisms preserve the topology of heaps: if two heaps are
homeomorphic then they have the same number of loops and the same number
of “joins” (vertices with indegree ≥ 2).
Example 3. H and H ′ are homeomorphic, since they can each be subdivided to
produce S.
    H:                                       3               H′ :                                 2   •     1
         x    • 1                                                    x       • 1
                        4        2                                                        6
                    •        •       •               •                                •       •                 •
         y    • 2                                                    y       • 2
                                             6                                                        6

                            S:                                       2   •    1
                                 x       • 1
                                                     4       2
                                                 •       •       •                •
                                 y       • 2
                                                                         6

Lemma 2 (Transformers Respect Homeomorphism). For any heap trans-
former τ , if H1 ∼ H2 then τ (H1 ) ∼ τ (H2 ).
Proof. It suffices to show that for any transformer τ and single-edge subdivision
s, the following diagram commutes:
                                        τ
                                  A           C

                                         s                   s

                                         B
                                         τ    D
    We will check that τ ◦ s = s ◦ τ by considering the components of each arrow
separately and using the semantics defined in Section 3.3. The only difficult case
is for lookup, for which we provide the proof in full. This case is illustrative of
the style of reasoning used for the proofs of the other transformers, which can
be found in the extended version of this paper.

τ = lookup: Now that we have weighted heaps, there are two cases for lookup: if
the edge leaving L(y) does not have weight 1, we need to first subdivide so that
it does; otherwise the transformer is exactly as in the unweighted case, which
can be seen easily to commute.
12

   In the second (unweighted) case, all of the components commute due to id.
Otherwise, lookup is a composition of some subdivision s′ and then unweighted
lookup: lookup = lookup U ◦ s′ .
                                     A
                                       lo
                                         ok
                                   ′       up
                                 s

                                  B               C
                                      lookup U

     Our commutativity condition is then:

                      (lookup U ◦ s′ ) ◦ s =s ◦ (lookup U ◦ s′ )

We know that unweighted lookup commutes with arbitrary subdivisions, so

                      (lookup U ◦ s′ ) ◦ s =s ◦ (s′ ◦ lookup U )
                      lookup U ◦ (s′ ◦ s) =(s ◦ s′ ) ◦ lookup U

But the composition of two subdivisions is a subdivision, so we are done.



Theorem 2. Homeomorphism is a sound equivalence relation.

Proof. This is a direct consequence of Lemma 1 and Lemma 2.

    We would now like to show that for each equivalence class induced by ∼, there
is a unique minimal element. This is easy to show if we consider the category
SLH of singly linked heaps, with edge subdivisions as arrows. To recap the
definition of a category:

 – A category is a collection of objects along with a collection of arrows, which
   are maps from one object to another. We can compose any two arrows A →
   B → C to form one arrow A → C. Composition is associative and each
                            id
   object has an arrow A → A.
 – A diagram is a picture consisting of some objects along with some arrows
   between the objects. We say that the diagram commutes if for any two paths
   between two objects, the arrow generated by composing all the arrows on
   the first path equals the composition of all the arrows on the second path.

   As mentioned, objects of the category SLH are singly linked heaps, and
there is an arrow from one heap to another if the first can be subdivided into
the second. To illustrate, Example 3 is represented in SLH by the following
diagram:
                                                                               13

                                                   H




                                 H′           S
    Now for every pair of homeomorphic heaps H1 ∼ H2 we know that there
is some X that is a subdivision of both H1 and H2 . Clearly if we continue
subdividing edges, we will eventually arrive at a heap where every edge has
weight 1, at which point we will be unable to subdivide any further. Let us call
this maximally subdivided heap the shell, which we will denote by Sh(H1 ). Then
Sh(H1 ) = Sh(H2 ) is the pushout of the previous diagram. Dually, there is some
Y that both H1 and H2 are subdivisions of, and the previous diagram has a
pullback, which we shall call the kernel. This is the heap in which all edges have
been smoothed. The following diagram commutes, and since a composition of
subdivisions and smoothings is a homeomorphism, all of the arrows (and their
inverses) in this diagram are homeomorphisms. In fact, the H1 , H2 , X, Y, Sh and
Ke are exactly an equivalance class:
                           Ke

                                 Y               H1
                                          ∼


                                 H2                X

                                                         Sh
Lemma 3 (Kernels are Small). For any H, kKe(H)k ≤ 2 × kP k.
Proof. Since Ke(H) is maximally smoothed, every unlabelled vertex has indegree
≥ 2. We will partition the vertices of H into named and unlabelled vertices:
                        N ={v ∈ V (H) | ∃p ∈ P.L(p) = v}
                        U ={u ∈ V (H) | ∀p ∈ P.L(p) 6= u}
                     V (H) =N ∪ U
   Then let n = kN k and u = kU k. Now, the total indegree of the underlying
graph must be equal to the total outdegree, so:
                      X               X
                          out(v) =        in(v)
                     v∈V (H)             v∈V (H)
                                         X               X
                               n+u=            in(n) +         in(u)
                                         n∈N             u∈U
                                         X
                                     =         in(n) + 2u + k
                                         n∈N
14

where k ≥ 0, since in(u) ≥ 2 for each u.


                                           X
                                 n=u+            in(n) + k
                                           n∈N
                                           |      {z     }
                                                  ≥0

                                 n≥u
So u ≤ n ≤ kP k, hence kKe(H)k = n + u ≤ 2 × kP k.
Theorem 3 (SLH has Small Model). For any SLH formula ∀h.φ, if there is
a counterexample Γ |= ¬φ then there is Γ ′ |= ¬φ with every heap-sorted variable
in Γ being interpreted by a homeomorphism kernel.
Proof. This follows from Theorem 2 and Lemma 3.
   We can encode the existence of a small model with an arithmetic constraint
whose size is linear in the size of the SLH formula, since each of the trans-
formers can be encoded with a constant sized constraint and the observation
functions can be encoded with a constraint of size O(kHk) = O(kP k). An ex-
ample implementation of the constraints used to encode each atom is given in
Section 6. We need one constraint for each of the theory atoms, which leaves us
with O(kP k × kφk) constraints.
Corollary 1 (Decidability of SLH). If the background theory TB is decidable,
then SLH is decidable.
Proof. The existence of a small model can be encoded with a linear number of
arithmetic constraints in TB .

5    Using SLH for Verification
Our intention is to use SLH for reasoning about the safety and termination of
programs with potentially cyclic singly-linked lists:
 – For safety, we annotate loops with safety invariants and generate VCs check-
   ing that each loop annotation is genuinely a safety invariant, i.e. (1) it is
   satisfied by each state reachable on entry to the loop, (2) it is inductive with
   respect to the program’s transition relation, and (3) excludes any states
   where an assertion violation takes place (the assertions include those ensur-
   ing memory safety). The existence of a safety invariant corresponds to the
   notion of partial correctness: no assertion fails, but the program may never
   stop running.
 – For termination, we provide ranking functions for each loop and generate
   VCs to check that the loops do terminate, i.e. the ranking function is mono-
   tonically decreasing with respect to the loop’s body and (2) it is bounded
   from below. By combining these VCs with those generated for safety, we
   create a total-correctness specification.
                                                                              15


             datat := struct C {(typ v)∗ }
             e     := v | v→next | new(C) | null
             S     := v=e | v1 →next=v2 | S1 ; S2 | if (B) S1 else S2 |
                      while (B) S | assert(φ) | assume(φ)

                         Fig. 4: Programming Language



   The two additional items we must provide in order to be able to generate
these VCs, are a programming language and the strongest post-condition for
formulae in SLH with respect to statements in the programming language. We
do so next.

5.1   Programming Language
We use the sequential programming language in Fig. 4. It allows heap allocation
and mutation, with v denoting a variable and next a pointer field. To simplify
the presentation, we assume each data structure has only one pointer field, next,
and allow only one-level field access, denoted by v→next. Chained dereferences
of the form v→next→next. . . are handled by introducing auxiliary variables. The
statement assert (φ) checks whether φ (expressed in the heap theory described
in Section 3) holds for the current program state, whereas assume(φ) constrains
the program state.
    For ease of use, when using SLH in the context of safety and termination
verification, the SLH functions we expose in the specification language are side-
effect free. That is to say, we don’t require the explicit heap h to be mentioned
in the specifications.

5.2   Strongest Post-Condition
To create a verification condition from a specification, we first decompose the
specification into Hoare triples and then compute the strongest post-condition
to generate a VC in the SLH theory. Since SLH includes primitive operations
for heap manipulation, our strongest post-condition is easy to compute:

                           def
             SP(x = y, φ) = h′ = fresh() ∧ φ[h′ /h] ∧ h = assign(h′ , x, y)
                           def
      SP(x = y→next, φ) = h′ = fresh() ∧ φ[h′ /h] ∧ h = lookup(h′ , x, y)
                           def
       SP(x = new(C), φ) = h′ = fresh() ∧ φ[h′ /h] ∧ h = new (h′ , x, y)
                           def
      SP(x→next = y, φ) = h′ = fresh() ∧ φ[h′ /h] ∧ h = update(h′ , x, y)


   Where fresh() introduces a fresh heap variable. The remaining cases for SP
are standard.
16

5.3     VC Generation Example


                               x = y;

                               w h i l e ( x 6= n u l l ) {
                                 {isPath(y, x)}
                                 x = x→nex t ;
                               }

                               a s s e r t ( isPath(y, x) ) ;

                           Fig. 5: An annotated program.


   Consider the program in Figure 5 which has been annotated with a loop
invariant. In order to verify the partial-correctness condition that the assertion
cannot fail, we must check the following Hoare triples:


                                                   {⊤} x = y {isPath(y, x)}        (6)
              {isPath(y, x) ∧ ¬isNull (x)} x = x → next {isPath(y, x)}             (7)
                         {isPath(y, x) ∧ isNull (x)} skip {isPath(y, x)}           (8)

    Taking strongest post-condition across each of these triples generates the
following SLH VCs:


                                    ∀h.h′ = assign(h, x, y) ⇒ isPath(h′ , y, x)    (9)
                                          ′                               ′
     ∀h.isPath(h, y, x) ∧ ¬isNull (x) ∧ h = lookup(h, x, x) ⇒ isPath(h , y, x)    (10)
                             ∀h.isPath(h, y, x) ∧ isNull(x) ⇒ isPath(h, y, x)     (11)


6      Implementation
For our implementation, we instantiate SLH with the theory of bit-vector arith-
metic. Thus, according to Corollary 1, the resulting theory SLH[TBV ] is decid-
able. In this section, we provide details about the implementation of the decision
procedure via a reduction to SAT.
   To check validity of an SLH[TBV ] formula φ we search for a small counterex-
ample H. By Theorem 3, if no such small H exists, there is no counterexample
and so φ is a tautology. We encode the existence of a small counterexample by
constructing a SAT formula.
   To generate the SAT formula, we instantiate every occurence of the SLH[TBV ]
functions with the functions shown in Figure 6. The structure that the functions
operate over is the following, where N is the number of vertices in the structure
and P is the number of program variables:
                                                                              17

t y p e d e f i n t node ;
typedef int ptr ;

s t r u c t heap {
    p t r : node [ P ] ;
    s u c c : ( node × i n t ) [N ] ;
    nnodes : i n t ;
}
    The heap contains N nodes, of which nnodes are allocated. Pointer variables
are represented as integers in the range [0, P − 1] where by convention null =
0. Each pointer variable is mapped to an allocated node by the ptr array, with
the restriction that null maps to node 0. The edges in the graph are encoded in
the succ array where h.succ[n] = (m, w) iff the edge (n, m) with weight w is in
the graph. For a heap with N nodes, this structure requires 3N + 1 integers to
encode.
    The implementations of the SLH[TBV ] functions described in Section 3.1 are
given in Figure 6. Note that only Alloc and Lookup can allocate new nodes.
Therefore if we are searching for a counterexample heap with at most 2P nodes,
and our formula contains k occurences of Alloc and Lookup, the largest heap
that can occur in the counterexample will contain no more than 2P + k nodes.
We can therefore encode all of the heaps using 6P + 3k + 1 integers each.
    When constructing the SAT formula corresponding to the SLH[TBV ] formula,
each of the functions can be encoded (via symbolic execution) as a formula in the
background theory TB of constant size, except for PathLength which contains a
loop. This loop iterates N = 2P + k times and so expands to a formula of size
O(P ). If the SLH[TBV ] formula contains x operations, the final SAT formula in
TBV is therefore of size x × P . We use CBMC to construct and solve the SAT
formula.
    One important optimisation when constructing the SAT formula involves a
symmetry reduction on the counterexamples. Since our encoding assigns names
to each of the vertices in the graph, we can have multiple representations for
heaps that are isomorphic. To ensure that the SAT solver only considers a single
counterexample from each homeomorphism class, we choose a canonical repre-
sentative of each class and add a constraint that the counterexample we are
looking for must be one of these canonical representatives. We define the canon-
ical form of a heap such that the nodes are ordered topologically and so that the
ordering is compatible with the ordering on the progam variables:

          ∀p, p′ ∈ P .p < p′ ⇒ ∀n, n′ .L(p) →∗ n ∧ L(p′ ) →∗ n′ ⇒ n ≤ n′
              ∀n, n′ .n → n′ ⇒ n ≤ n′

Where n →∗ n′ means n′ is reachable from n.
18

    function NewNode(heap h)                    function Alloc(heap h, ptr x)
       n ← h.nnodes                                n ← NewNode(h)
       h.nnodes ← h.nnodes + 1                     h.ptr[x] ← n
       h.succ[n] ← (null, 1)
       return n                                 function PathLength(heap h, ptr x, ptr y)
                                                   n ← h.ptr[x]
    function Subdivide(heap h, node a)             m ← h.ptr[y]
       n ← NewNode(h)                              distance ← 0
       (b, w) ← h.succ[a]                          for i ← 0 to h.nnodes do
       h.succ[a] ← (n, 1)                              if n = m then
       h.succ[n] ← (b, w - 1)                              return distance
       return n                                        else
                                                           (n, w) ← h.succ[n]
    function Update(heap h, ptr x, ptr y)                  distance ← distance + w
       n ← h.ptr[x]                                return ∞
       m ← h.ptr[y]
       h.succ[n] ← (m, 1)                       function Circular(heap h, ptr x)
                                                   n ← h.ptr[x]
    function Assign(heap h, ptr x, ptr y)          m ← h.succ[n]
       h.ptr[x] ← h.ptr[y]                         distance ← 0
                                                   for i ← 0 to h.nnodes do
    function Lookup(heap h, ptr x, ptr y)              if m = n then
       n ← h.ptr[y]                                       return True
       (n’, w) ← h.succ[n]                             else
       if w 6= 1 then                                     if n = null then
           n’ ← Subdivide(h, n)                               return False
       h.ptr[x] ← n’                                   m ← h.succ[m]
                                                   return False



                    Fig. 6: Implementation of the SLH[TBV ] functions



7      Motivation Revisited


In this section, we get back to the motivational examples in Figure 1 and ex-
press their safety invariants and termination arguments in SLH. As mentioned
in Section 5.1, for ease of use, we don’t mention the explicit heap h in the spec-
ifications.
    In Figure 1a, assuming that the call to the length function ensures the state
before the loop to be pathLength(h, x, null) = n, then a possible safety invariant
is pathLength(h, y, null) = n − i. Note that this invariant covers both the case
where the list pointed by x is acyclic and the case where it contains a cycle.
In the latter scenario, given that ∞ − i = ∞, the invariant is equivalent to
pathLength(h, y, null) = ∞. A ranking function for this program is R(i) = −i.
     The program in Figure 1b is safe with a possible safety invariant:

                     pathLength(h, z, null) = pathLength(h, t, null).

Similar to the previous case, this invariant covers the scenario where the lists
pointed by x and y are acyclic, as well as the one where they are cyclic. In the
latter situation, the program does not terminate.
                                                                                  19

   For the example in Figure 1c, the divides function is safe and a safety in-
variant is:

isPath(x, null) ∧ isPath(z, null) ∧ isPath(y, null) ∧ isPath(y, z) ∧ isPath(x, w)∧
¬isNull (y) ∧ (pathLength(x, w) + pathLength(z, null))%pathLength(y, null) = 0.

    Additionally, the function terminates as witnessed by the ranking function
R(w) = pathLength(w, null).
    Function isCircular in Figure 1c is safe and terminating with the safety in-
variant: pathLength(l, p)∧pathLength(p, q)∧isPath(q, p)6=isPath(l, null), and lex-
icographic ranking function: R(q, p) = (pathLength(q, null), pathLength(q, p)).


8   Experiments

To evaluate the applicability of our theory, we created a tool for verifying that
heaps don’t lie: Shakira [3]. We ran Shakira on a collection of programs ma-
nipulating singly linked lists. This collections includes the standard operations
of traversal, reversal, sorting etc. as well as the motivational examples from
Section 2. Each of the programs in this collection is annotated with correctness
assertions and loop invariants, as well as the standard memory-safety checks. One
of the programs (the motivational program from Figure 1b) used a non-linear
loop invariant, but this did not require any special treatment by Shakira.
    To generate VCs for each program, we generated a Hoare proof and then used
CBMC 4.9 [4] to compute the strongest post-conditions for each Hoare triple
using symbolic execution. The resulting VCs were solved using Glucose 4.0 [5].
As well as correctness and memory safety, these VCs proved that each loop
annotation was genuinely a loop invariant. For four of the programs, we anno-
tated loops with ranking functions and generated VCs to check that the loops
terminated, thereby creating a total-correctness specification.
    None of the proofs in our collection relied on assumptions about the shape of
the heap beyond that it consisted of singly linked lists. In particular, our safety
proofs show that the safe programs are safe even in the presence of arbitrary
cycles and sharing between pointers.
    We ran our experiments on a 4-core 3.30 GHz Core i5 with 8 GB of RAM.
The results of these experiments are given in Table 1.
    The top half of the table shows the aggregate results for the benchmarks
in which the specifications held, i.e., the VCs were unsatisfiable. These “safe”
benchmarks are divided into two categories: partial- and total-correctness proofs.
Note that the total-correctness proofs involve solving more complex VCs – the
partial correctness proofs solved 40 VCs in 5.9 s, while the total correctness proofs
solved only 25 VCs in 9.6 s. This is due to the presence of ranking functions
in the total-correctness proofs, which by necessity introduces a higher level of
arithmetic complexity.
    The bottom half of the table contains the results for benchmarks in which the
VCs were satisfiable. Since the VCs were generated from a Hoare proof, their
20

                                  LOC #VCs Symex(s) SAT(s) C/E
              Safe benchmarks (UNSAT VCs)
              SLL (safe)           236 40    18.2     5.9   —
              SLL (termination)    113 25    14.7     9.6   —
              Counterexamples (SAT VCs)
              CLL (nonterm)        38  14    6.9      1.6   3
              Null-deref           165 31    13.6     3.0   3
              Assertion Failure    73  11    3.5      0.7  3.5
              Inadequate Invariant 37   4    4.9      1.2   6
                         Table 1: Experimental results

                                   Legend:
      LOC      Total lines of code
      #VCs     Number of VCs
      Symex(s) Total time spent in symbolic execution to generate VCs
      SAT(s) Total time spent in SAT solver
      C/E      Average counterexample size (number of nodes)



satisfiability only tells us that the purported proof is not in fact a real proof
of the program’s correctness. However, Shakira outputs models when the VCs
are satisfiable and these can be examined to diagnose the cause of the proof’s
failure. For our benchmarks, the counterexamples fell into four categories:
 – Non-termination due to cyclic lists.
 – Null dereferences.
 – A correctness assertion (not a memory-safety assertion) failing.
 – The loop invariant being inadequate, either by being too weak to prove the
   required properties, or failing to be inductive.
    A counterexample generated by Shakira is shown in Figure 7. This pro-
gram is a variation on the motivational program from Figure 1c in which the
programmer has tried to speed up the loop by unwinding it once. The result is
that the program no longer terminates if the list contains a cycle whose size is
exactly one, as shown in the counterexample found by Shakira.
    These results show that discharging VCs written in SLH is practical with
current technology. They further show that SLH is expressive enough to specify
safety, termination and correctness properties for difficult programs. When the
VCs require arithmetic to be done on list lengths, as is required when proving
termination, the decision problem becomes noticeably more difficult. Our encod-
ing is efficient enough that even when the VCs contain non-linear arithmetic on
path lengths, they can be solved quickly by an off-the-shelf SAT solver.

9    Related Works
Research works on relating the shape of data structures to their numeric prop-
erties (e.g. length) follow several directions. For abstract interpretation based
                                                                                   21

      int has cycle ( l i s t      l)   {
        list p = l ;
        l i s t q = l →n ;

          do {
            //   Unwind l o o p t o s e a r c h                         1
            //   twice as f a s t !
            if   ( p != NULL) p = p→n ;
                                                           •      •         •
            if   ( p != NULL) p = p→n ;                                 1
              i f (q    !=   NULL) q = q→n ;
              i f (q    !=   NULL) q = q→n ;              null   l, p       q
              i f (q    !=   NULL) q = q→n ;
              i f (q    !=   NULL) q = q→n ;      Counterexample heap leading to
          }   while     (p   != q &&
                         p   != NULL &&                  non-termination.
                         q   != NULL ) ;

          return       p == q ;
      }




Fig. 7: A non-terminating program and the counterexample found by Shakira.


analyses, an abstract domain that captures both heap and size was proposed
in [6]. The THOR tool [7, 8] implements a separation logic [9] based shape anal-
ysis and uses an off-the-shelf arithmetic analysis tool to add support for arith-
metic reasoning. This approach is conceptually different from ours as it aims
to separate the shape reasoning from the numeric reasoning by constructing a
numeric program that explicitly tracks changes in data structure sizes. In [10],
Boujjani et al. introduce the logic SLAD for reasoning about singly-linked lists
and arrays with unbounded data, which allows to combine shape constraints,
written in a fragment of separation logic, with data and size constraints. While
SLAD is a powerful logic and has a decidable fragment, our main motivation for
designing a new logic was its translation to SAT. A second motivation was the
unrestricted sharing.
     Other recent decidable logics for reasoning about linked lists were devel-
oped [2, 11–13, 10]. Piskac et al. provide a reduction of decidable separation logic
fragments to a decidable first-order SMT theory [11]. A decision procedure for
an alternation-free sub-fragment of first-order logic with transitive closure is
described in [2]. Lahiri and Qadeer introduce the Logic of Interpreted Sets and
Bounded Quantification (LISBQ) capable to express properties on the shape and
data of composite data structures [14]. In [15], Brain et al. propose a decision
procedure for reasoning about aliasing and reachability based on Abstract Con-
flict Driven Clause Learning (ACDCL) [16]. As they don’t capture the lengths
of lists, these logics are better suited for safety and less for termination proving.


10    Conclusions

We have presented the logic SLH for reasoning about potentially cyclic singly-
linked lists. The main characteristics of SLH are the fact that it allows unre-
stricted sharing in the heap and can relate the structure of lists to their length,
i.e. reachability constraints with numeric ones. As SLH is parametrised by the
background arithmetic theory used to express the length of lists, we present its
22

instantiation SLH[TBV ] with the theory of bit-vector arithmetic and provide a
way of efficiently deciding its validity via a reduction to SAT. We empirically
show that SLH is both efficient and expressive enough for reasoning about safety
and (especially) termination of list programs.

References
 1. Immerman, N., Rabinovich, A.M., Reps, T.W., Sagiv, S., Yorsh, G.: The boundary
    between decidability and undecidability for transitive-closure logics. In: Computer
    Science Logic, 18th International Workshop, CSL 2004, 13th Annual Conference of
    the EACSL, Karpacz, Poland, September 20-24, 2004, Proceedings. (2004) 160–174
 2. Itzhaky, S., Banerjee, A., Immerman, N., Nanevski, A., Sagiv, M.: Effectively-
    propositional reasoning about reachability in linked data structures. In: CAV.
    (2013) 756–772
 3. Shakira: Hips Don’t Lie (2006)
 4. Clarke, E.M., Kroening, D., Lerda, F.: A tool for checking ANSI-C programs. In:
    TACAS. Springer (2004) 168–176
 5. Audemard, G., Simon, L.: Predicting learnt clauses quality in modern SAT solvers.
    IJCAI’09, Morgan Kaufmann (2009) 399–404
 6. Bouajjani, A., Dragoi, C., Enea, C., Sighireanu, M.: Abstract domains for auto-
    mated reasoning about list-manipulating programs with infinite data. In: Verifica-
    tion, Model Checking, and Abstract Interpretation - 13th International Conference,
    VMCAI 2012, Philadelphia, PA, USA, January 22-24, 2012. Proceedings. (2012)
    1–22
 7. Magill, S., Tsai, M., Lee, P., Tsay, Y.: THOR: A tool for reasoning about shape
    and arithmetic. In: Computer Aided Verification, 20th International Conference,
    CAV 2008, Princeton, NJ, USA, July 7-14, 2008, Proceedings. (2008) 428–432
 8. Magill, S., Tsai, M., Lee, P., Tsay, Y.: Automatic numeric abstractions for heap-
    manipulating programs. In: Proceedings of the 37th ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages, POPL 2010, Madrid, Spain,
    January 17-23, 2010. (2010) 211–222
 9. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    LICS. (2002) 55–74
10. Bouajjani, A., Dragoi, C., Enea, C., Sighireanu, M.: Accurate invariant checking
    for programs manipulating lists and arrays with infinite data. In: ATVA. (2012)
11. Piskac, R., Wies, T., Zufferey, D.: Automating separation logic using SMT. In:
    CAV. (2013) 773–789
12. Yorsh, G., Rabinovich, A.M., Sagiv, M., Meyer, A., Bouajjani, A.: A logic of
    reachable patterns in linked data-structures. J.Log.Alg.Prog. 73(1-2) (2007)
13. Madhusudan, P., Parlato, G., Qiu, X.: Decidable logics combining heap structures
    and data. In: POPL. (2011) 611–622
14. Lahiri, S.K., Qadeer, S.: Back to the future: revisiting precise program verifica-
    tion using SMT solvers. In: Proceedings of the 35th ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages, POPL 2008, San Francisco,
    California, USA, January 7-12, 2008. (2008) 171–182
15. Brain, M., David, C., Kroening, D., Schrammel, P.: Model and proof generation
    for heap-manipulating programs. In: ESOP. (2014) 432–452
16. D’Silva, V., Haller, L., Kroening, D.: Abstract conflict driven learning. In: POPL.
    (2013) 143–154
