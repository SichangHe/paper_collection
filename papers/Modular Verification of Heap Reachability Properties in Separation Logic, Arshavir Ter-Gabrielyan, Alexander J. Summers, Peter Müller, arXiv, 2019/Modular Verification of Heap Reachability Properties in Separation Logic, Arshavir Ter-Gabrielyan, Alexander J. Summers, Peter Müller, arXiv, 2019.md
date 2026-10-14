                                         Modular Verification of Heap Reachability Properties in
                                         Separation Logic
arXiv:1908.05799v1 [cs.PL] 16 Aug 2019




                                         ARSHAVIR TER-GABRIELYAN, ETH Zurich, Switzerland
                                         ALEXANDER J. SUMMERS, ETH Zurich, Switzerland
                                         PETER MÜLLER, ETH Zurich, Switzerland
                                         The correctness of many algorithms and data structures depends on reachability properties, that is, on the
                                         existence of chains of references between objects in the heap. Reasoning about reachability is diﬃcult for
                                         two main reasons. First, any heap modiﬁcation may aﬀect an unbounded number of reference chains, which
                                         complicates modular veriﬁcation, in particular, framing. Second, general graph reachability is not supported
                                         by SMT solvers, which impedes automatic veriﬁcation.
                                            In this paper, we present a modular speciﬁcation and veriﬁcation technique for reachability properties in
                                         separation logic. For each method, we specify reachability only locally within the fragment of the heap on
                                         which the method operates. A novel form of reachability framing for relatively convex subheaps allows one to
                                         extend reachability properties from the heap fragment of a callee to the larger fragment of its caller, enabling
                                         precise procedure-modular reasoning. Our technique supports practically important heap structures, namely
                                         acyclic graphs with a bounded outdegree as well as (potentially cyclic) graphs with at most one path (modulo
                                         cycles) between each pair of nodes. The integration into separation logic allows us to reason about reachability
                                         and other properties in a uniform way, to verify concurrent programs, and to automate our technique via
                                         existing separation logic veriﬁers. We demonstrate that our veriﬁcation technique is amenable to SMT-based
                                         veriﬁcation by encoding a number of benchmark examples into the Viper veriﬁcation infrastructure.



                                         1 INTRODUCTION
                                         Separation logic [Reynolds 2002] has greatly simpliﬁed the veriﬁcation of basic heap data struc-
                                         tures such as lists and trees by leveraging the disjointness of sub-heaps to reason about the eﬀects
                                         of heap modiﬁcations. However, verifying data structures that permit unbounded sharing remains
                                         challenging. Their correctness often depends on heap reachability properties, that is, the existence
                                         of paths of references between objects. For instance, the path compression of union-ﬁnd needs to
                                         preserve the reachability of the root object, the termination of heap traversals might rely on the
                                         absence of cyclic paths, and the invariant of a garbage collector may prescribe that each object is
                                         reachable from the list of allocated objects or the free-list, but not from both.
                                            Reasoning about reachability properties is diﬃcult for two main reasons. (1) Modularity: reacha-
                                         bility is inherently a non-local property. Any heap modiﬁcation may aﬀect an unbounded number
                                         of heap paths, which complicates framing, that is, proving modularly that a heap update or method
                                         call does not aﬀect a given reachability property. (2) Automation: general graph reachability is not
                                         supported by SMT solvers, which power most automatic veriﬁcation tools.
                                            Existing work addresses these challenges typically by supporting only certain kinds of reacha-
                                         bility properties or certain classes of data structures. For instance, Itzhaky et al. [2014] present a
                                         modular veriﬁcation technique for reachability properties of a broad class of linked-list programs,
                                         but do not support structures that can have more than one outgoing reference per object. Such
                                         structures may contain an arbitrary number of alternative paths between two objects, and main-
                                         taining reachability information via ﬁrst-order formulas becomes infeasible. Flows [Krishna et al.
                                         2018] is a technique providing local reasoning for updates to subgraphs which preserve properties
                                         such as reachability, e.g., changes to a subgraph which neither add nor remove paths between
                                         nodes in its boundary. However, ﬂows do not provide analogous means for local reasoning about
                                         methods which are intended to change these paths (e.g., a function which connects two subgraphs).

                                         2019-08-19 00:46. Page 1 of 1–34.
2                                 Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

   This paper presents a modular veriﬁcation technique for general heap reachability properties
that supports both acyclic data structures with a bounded number of outgoing references per object
(for instance, DAG structures such as BDDs [Akers Jr. 1978]) and (potentially cyclic) 0–1-path
graphs, that is, graphs that contain at most one path (modulo cycles) between each pair of objects
(such as a ring buﬀer). Our technique is integrated into separation logic, which allows us to reason
about reachability and other properties in a uniform way, to verify concurrent programs, and to
automate our technique via existing separation logic veriﬁers. Our technique enables modular
reasoning by specifying reachability properties locally within the memory footprint of a method
rather than in the entire heap. A novel form of reachability framing allows one to extend the
reachability properties guaranteed by a callee method to the (larger) footprint of its caller. As a
result, each method can be veriﬁed modularly, without considering the heap outside its footprint,
the implementations of other methods, or other threads.

    Contributions. Our paper makes the following technical contributions:
      • Speciﬁcation: We introduce a speciﬁcation technique for reachability properties in the con-
        text of separation logic. It enables modular veriﬁcation, even for concurrent programs (Sec. 2).
      • Veriﬁcation: We present a novel veriﬁcation technique for reachability properties. In partic-
        ular, we identify relative convexity of method footprints as a property that enables precise
        reachability framing and procedure-modular reasoning. Our technique goes beyond prior
        work [Itzhaky et al. 2014] by supporting all acyclic graphs (Sec. 3).
      • Cyclic graphs: We extend our veriﬁcation technique to cyclic 0–1-path graphs. While reach-
        ability framing carries over from the acyclic case, cyclic graphs require a more elaborate
        machinery to handle reference ﬁeld updates (Sec. 4).
      • Automation: We demonstrate that our veriﬁcation technique is amenable to SMT-based ver-
        iﬁcation by encoding a number of benchmark examples into the Viper veriﬁcation infras-
        tructure [Müller et al. 2016b] (Sec. 5).

2 SPECIFICATION TECHNIQUE
In this section, we illustrate our technique using a DAG data structure with node type Node and
ﬁelds left and right. Method merge in Fig. 1 takes as arguments references l and r to two nodes
of disjoint DAGs and attaches r as descendant of l. It returns link, a node of the ﬁrst DAG to
which r was attached. The postcondition ensures that exactly one connection was created (via an
edge from link to the root of the second DAG, r), and that heap paths exist either if they existed in
the pre-state or were connected by the new edge, (link, r). We explain the speciﬁcation of merge
in full detail in the remainder of this section.

2.1    Footprints
Separation logics associate an access permission with each memory location. Access permissions
are held by method executions and may be transferred between methods upon calls and returns;
they can be thought of as additional program state used for reasoning (ghost state). A heap location
can be accessed only while the corresponding permission is held. The set of locations that a method
may access is called its footprint. Due to (de)allocation or concurrency, the footprint of a method
may change during its execution.
   A method’s precondition speciﬁes which permissions to transfer on calling the method. The
initial footprint of a method contains exactly the locations for which its precondition requires
permission. Conversely, the method postcondition speciﬁes which permissions to return to the
caller when the method terminates.

                                                                            2019-08-19 00:46. Page 2 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                              3


method merge(l: Node, r: Node,
                   g : Graph, ldag: Graph, rdag: Graph) // ghost parameters
    returns link: Node                                         // updated node
    requires g = ldag ⊎ rdag ∧ l ∈ ldag ∧ r ∈ rdag
             ∀x, y ∈ g • ¬E(g, x, y) ∨ ¬P(g, y, x)           // acyclic invariant
             ∀n • n ∈ ldag ⇔ P(g, l, n)
             ∀n • n ∈ rdag ⇔ P(g, r, n)
    ensures link ∈ ldag
            ∀x, y ∈ g • ¬E(g, x, y) ∨ ¬P(g, y, x)            // acyclic invariant
            ∀x, y • E(g, x, y) ⇐⇒ E0 (g, x, y) ∨ x = link ∧ y = r
            ∀x, y • P(g, x, y) ⇐⇒ P0 (g, x, y) ∨ P0 (g, x, link) ∧ P0 (g, r, y)
{
      if (l.right != null) {
           var nldag := sub(g , ldag, l.right)                 // deﬁne new ghost parameter
           link := merge(l.right, r, nldag ⊎ rdag, nldag, rdag)
      } else {
           l.right := r
           link := l
      }
}


Fig. 1. An example program and specification. Method merge attaches the DAG rooted in r to a
node of the DAG rooted in l, and returns that node. We use the edge predicate E and the path
predicate P to specify reachability properties, within a set of objects g. Each specification line is a
separate conjunct. The footprint g is closed due to the equivalences in the last two preconditions.



   The footprint of any method operating on linked heap structures, e.g., lists and DAGs, contains
a statically unknown number of memory locations. To provide a convenient way to refer to a
method’s footprint, we equip each method with a distinct ghost parameter g : Graph to denote
its footprint. For simplicity, instead of specifying the footprint as a set of object-ﬁeld pairs, we let
Graph denote sets of non-null objects and keep the ﬁelds implicit when they are clear from the
context. The set stored in g is updated whenever the footprint changes, for instance, due to alloca-
tion. In order to be able to refer to the ﬁnal footprint of a method execution in its postcondition,
we make g an in-out parameter. For simplicity, we assume in the following that the footprint of a
method remains unchanged, s.t. the value of g is constant; an extension is straightforward.
   We equip each method with implicit pre- and postconditions to require and ensure permissions
to all locations in the footprint:

    requires ∀n ∈ g • acc(n.left) ∗ acc(n.right)
    ensures     ∀n ∈ g • acc(n.left) ∗ acc(n.right)

Here, acc(x.f ) denotes an access permission to the memory location for ﬁeld f of object x (like
x .f 7→_ in traditional separation logic [Reynolds 2002]), ∗ denotes separating conjunction, and
the universal quantiﬁer is an iterated separating conjunction [Müller et al. 2016a; Reynolds 2002],
which (here) denotes permissions to all ﬁeld locations of objects in the footprint g. In contrast

2019-08-19 00:46. Page 3 of 1–34.
4                                Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

to using recursive deﬁnitions to specify unbounded heap structures (e.g., separation logic pred-
icates [Parkinson and Bierman 2005; Yang 2001b]), iterated separating conjunction permits arbi-
trary sharing within the set g (many ﬁeld values may alias the same node) and does not prescribe
a traversal order within the data structure. We assume for simplicity that a method speciﬁcation
expresses all required and returned permissions via these implicit contracts with respect to g, but
it is easy to also support other permission speciﬁcations, e.g., points-to predicates and recursive
predicates.
   In our example, we use two additional ghost parameters ldag and rdag to allow our speciﬁcation
to simply denote the sets of objects constituting the ﬁrst and second DAG, respectively. The ﬁrst
precondition expresses that the method footprint is the disjoint union of these two DAGs.

2.2   Local Reachability
Reasoning in a separation logic has the key advantage that one can modularly verify properties of
a method, and reuse this veriﬁcation for all calling contexts (and concurrently-running threads).
Enforcing that properties veriﬁed for the method depend only on its footprint, guarantees that
they hold independently of the context; we refer to these as the local properties of the footprint.
However, classical reachability in the heap is not a local property of this form. Hence, combining
reachability and separation logic requires us to reﬁne the notion of reachability to one that is local,
as we explain next.
   Our technique provides two predicates to express reachability properties in speciﬁcations. We
generalize classical reachability by adding an extra footprint parameter, g to make the property
local. The edge predicate EF (g, x, y) expresses that object x is in the set g and has a ﬁeld from the
set of ﬁelds F storing a non-null object y (which need not be in g). The path predicate P denotes,
for a ﬁxed g and F , the reﬂexive, transitive closure of E, that is, PF (g, x, y) expresses that either
x = y, or there is a path of ﬁeld references from x to y s.t. all objects on the path (except possibly
y) are in g and all ﬁelds are in F ; in particular P may denote reachability via multiple ﬁelds. We
omit the parameter F when the set of ﬁelds is clear from the context; for instance, in our example,
F consists of the (only) reference-typed ﬁelds left and right . We say that a path x . . . y is g-local
if P(g, x, y) holds. Both our edge and path predicates are deﬁned over a mathematical abstraction
of the current heap graph (cf. Sec. 3.1), and are pure in the separation logic sense, allowing us to
freely repeat them in speciﬁcations.
   Our edge and path predicates enable rich reachability speciﬁcations within a method’s footprint.
The preconditions of merge express that the method footprint is acyclic and closed under the
edge relation (due to the second and the last two preconditions), and that ldag and rdag contain
exactly the objects reachable from l and r, resp. In general, method speciﬁcations are checked to
only employ edge and path predicates whose ﬁrst parameter is the method’s footprint or a subset
thereof.
   Method postconditions typically express how reachability changes within this footprint. In our
example, the ﬁrst postcondition speciﬁes that the result link is part of the ﬁrst DAG and its right-
ﬁeld was initially null. The old-expression allows postconditions to refer to pre-state values; we
write E0 (. . .) to abbreviate old(E(. . .)), and analogously for P. We can freely mix reachability
speciﬁcations with speciﬁcations in terms of the program heap (e.g., the link.right expression).
The other postconditions illustrate how we can specify the new edge and path relations in terms
of their originals, summarizing the method’s eﬀect. In particular, the last postcondition expresses
that an object x reaches an object y in the post-state iﬀ it reached y already in the pre-state, or
if x reaches link in the ﬁrst DAG and y is in the second DAG. Our method speciﬁcation leaves
link underspeciﬁed, whereas the implementation chooses the rightmost node in the ﬁrst DAG. We


                                                                          2019-08-19 00:46. Page 4 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                              5


                                    l              l.right            link    r




                                    frame                     nldag            rdag


Fig. 2. An example scenario of running merge on two DAGs rooted in l and r. Small circles corre-
spond to heap objects; solid arrows represent fields initialized in the pre-state that are unchanged;
the dashed arrow represents the new heap edge (created in the post-state by initializing a field).
The frame of the recursive call is surrounded with blue; the footprint is surrounded with red.


could easily provide a less abstract speciﬁcation by using path predicates over (only) the right-
ﬁeld.
  The recursive call in method merge needs to supply values for the three ghost parameters.
We construct these values using a predeﬁned function sub(g :Graph,h :Graph,root:Node), which
yields the subset of h reachable from the node root via g-local paths. The properties known for
the resulting set are summarized by the following heap-dependent function [Müller et al. 2016b]
declaration:1
function sub(g : Graph, h : Graph, root: Node): Graph
   requires root ∈ h ∧ h ⊆ g
   ensures result ⊆ h ∧ root ∈ result ∧ CLOSEDh (result ) ∧
               ∀n • n ∈ result ⇔ P(g, root, n)
where result refers to the result value of the function; CLOSEDh (r) denotes that an edge that exits
must not end in h:
                     CLOSEDh (r) ..⇐⇒ ∀x ∈ r, y • E(r, x, y) =⇒ y < h\r                          (1)
  Note that CLOSEDh (r) is permissive enough to allow selecting new footprints for method calls
even if the current footprint is open, i.e., if there exist edges that exits the current footprint. To
specify that a subheap is closed in the global heap, we would use a stronger condition:
                          CLOSED(g) ..⇐⇒ ∀x ∈ g, y < g • ¬E(g, x, y)                                (2)

2.3    Verification Challenges
The speciﬁcation ingredients presented above allow us to combine separation logic speciﬁcation
with reachability. However, practical veriﬁcation of these speciﬁcations requires the solution of
three challenges. Firstly, we must handle direct updates to the program heap, and model their
eﬀects on our E and P predicates. SMT solvers cannot eﬃciently automate reasoning about a di-
rect deﬁnition of P as transitive closure, but it has been shown that a ﬁrst-order approximation
technique can be eﬃciently used for this purpose [Dong and Su 1995; Lev-Ami et al. 2009]. Sec-
ondly, and most challenging, we require a technique to deduce reachability for a method caller
from what is known about its callee’s footprint: a problem we call reachability framing. This is
necessary, for example, when reasoning about the recursive call to merge in our example; we must
1 Unlike methods, functions in our language are guaranteed to be side-eﬀect free. Hence, we do not distinguish between P

and P0 in the postcondition of sub (similar for E and E0 ).


2019-08-19 00:46. Page 5 of 1–34.
6                                 Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

relate local reachability information in the caller’s footprint to that of its callee. Finally, we require
a modeling of our veriﬁcation technique in an automated tool; we aim for proof obligations ulti-
mately amenable to ﬁrst-order SMT solvers, which necessitates eﬀective quantiﬁer instantiation
strategies.

3 REACHABILITY IN ACYCLIC STRUCTURES
In this section, we explain the core ingredients of our veriﬁcation technique for combining reach-
ability information with separation logic style reasoning. Reasoning about a method starts with
assuming its precondition. The precondition provides permissions to access the objects (i.e., nodes)
in its footprint and the reachability constraints that guarantee the existence or the absence of heap
paths connecting some objects from the footprint. As the program performs modiﬁcations to some
parts of the heap, our goal is to determine a precise way of checking any (local) reachability query
(e.g., in the method’s postcondition) after these changes. Hence it is important to identify the paths
that were unchanged and those that were created or destroyed by each operation.
   Heap modiﬁcations are performed either directly by ﬁeld updates or indirectly through method
calls. In the former case, the reachability properties known to hold before the update need to be
adjusted to reﬂect the change of heap references (Sec. 3.2). For a ﬁeld update, the local reachabil-
ity properties before and after the update can be expressed within the same (enclosing method’s)
footprint. The situation is more complex for method calls (Sec. 3.3). To determine the reachability
properties after a call (the reachability framing problem), one needs to combine reachability prop-
erties before the call that are known to be outside of the call’s footprint (hence, unaﬀected by the
call) with reachability properties guaranteed by the callee method (as expressed in the callee’s post-
condition). These two sets of properties are expressed within the footprints of the client and the
callee, respectively. If these footprints are not equal, then the reachability properties guaranteed
by the callee need to be re-interpreted in the client’s footprint.
   We present our techniques for tackling these challenges in the remainder of the paper. We dis-
cuss how our reachability reasoning technique is integrated with separation logic in Sec. 3.1. The
technique for direct ﬁeld updates discussed in Sec. 3.2 requires the current method’s footprint to
be acyclic; note that we generally permit arbitrary structures, including those with heap cycles,
outside of the footprint. However, our technique for method calls, and all of the formulas that we
present in Sec. 3.3, do not require acyclicity. Instead, we require and exploit relative convexity of
method footprints, a novel restriction that is strong enough to reduce the reachability framing
problem to ﬁrst-order formulas tractable for SMT solvers, but permissive enough to embrace a
broad spectrum of challenging data structures. Sec. 4 explains how our technique can be extended
to potentially cyclic 0–1-path graphs.

3.1   Encoding of Edge and Path Predicates
Our speciﬁcation technique supports reachability via the edge predicate E and the path predi-
cate P. In order to verify such speciﬁcations, we encode them into a ﬂavor of separation logic
and use an existing veriﬁcation tool to construct proofs in that logic. We use Implicit Dynamic
Frames [Smans et al. 2012] for this purpose, a variation of separation logic [Parkinson and Summers
2011] that separates speciﬁcations of access permissions for memory locations from speciﬁcations
of the values stored in these locations. For instance, separation logic’s points-to predicate x .f 7→ v
is speciﬁed in implicit dynamic frames as a conjunction of the access permission and the ﬁeld
content: acc(x . f ) * x . f = v. This separation of permissions and value properties allows us to
conveniently express additional value properties, e.g., sortedness, in addition to reachability prop-
erties, without having to deﬁne a new graph-abstraction that exposes the values of interest.

                                                                             2019-08-19 00:46. Page 6 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                 7

     Our edge predicates could be deﬁned directly, e.g., as (x .f 1 = v ∨ x .f 2 = v) for two ﬁelds f 1 and
f 2 ; conceptually, E is a ﬁrst-order abstraction over this property, which may, in particular, be used
in the syntactic triggering patterns [Barrett et al. 2017; de Moura and Bjørner 2008; Detlefs et al.
2005; Moskal 2009] that the SMT solver requires to control quantiﬁer instantiations (and which
cannot include logical operations such as ∨ above).
     Unlike the edge predicate E, directly deﬁning the path predicate P would compromise automa-
tion. A deﬁnition would involve transitive closure, which is notoriously diﬃcult to handle for SMT
solvers. Therefore, we take a diﬀerent approach here. We leave the path predicate undeﬁned and
axiomatize its essential properties, for instance, how it is aﬀected by heap updates. We specify
these axioms over mathematical graphs and not directly over the heap-dependent edge and path
predicates. Therefore, our encoding ﬁrst abstracts the heap within a footprint to a set of edges
(ordered pairs of nodes) and then expresses reachability over those. This abstraction is deﬁned
by a predeﬁned function called snapshot . For simplicity, we deﬁne snapshot using the notation
of our source language, but it is only used internally by our encoding. In particular, the function
implicitly depends on the heap and requires permissions to all objects in its footprint g:
function snapshot F (g : Graph): Edgeset
     ensures ∀x, y • x ∈ g ∧ y , null ∧ (x .f 1 = y ∨ . . . ∨ x .fn = y) ⇐⇒ (x, y) ∈ result

Here, Edgeset is the type of sets of pairs of nodes, and F = { f 1 , . . . , fn }; we omit this parameter
when it is clear from the context. The postcondition can be thought of as an axiom over an un-
interpreted function that deﬁnes its semantics. Note that snapshot also collapses edges between
two objects for diﬀerent ﬁeld names (duplicate edges are not needed to keep track of reachability).
   This abstraction function lets us deﬁne the edge predicate in a straightforward way:
                                    EF (g, x, y) ..⇐⇒ (x, y) ∈ snapshot F (g)                          (3)
To avoid the issues with transitive closure mentioned above, we do not deﬁne the path predicate
directly, but axiomatize the properties we need for veriﬁcation. In fact, we deﬁne the path relation
in terms of a function P̂ over graphs and then axiomatize the latter, state-independent function:
                                    PF (g, x, y) ..⇐⇒ P̂ (snapshot F (g), x, y)                        (4)
For this axiomatization, we carefully control the quantiﬁer instantiation performed by SMT solvers
to avoid diverging proof search. For instance, we include the axiom below, but let the solver in-
stantiate it only to a ﬁxed depth of unrolling P̂ [Leino and Monahan 2009].
                           P̂(G, x, y) ..⇐⇒ x = y ∨ ∃z • (x, z) ∈ G ∧ P̂(G, z, y)                      (5)

3.2 Field Updates
A ﬁeld update x.f := v may aﬀect reachability properties in the heap and, thus, both edge and
path predicates. Since our encoding contains a precise deﬁnition of the edge predicate in terms
of the underlying heap (via (3) and the deﬁnition of snapshot ), the veriﬁer can determine which
edge predicates hold after a ﬁeld update.
   However, determining the eﬀect of a single ﬁeld update on the path relation is more intricate as
its the axiomatization is not suﬃcient to determine which predicates hold after a ﬁeld assignment
(e.g., because this reasoning step would require induction proofs, which SMT solvers cannot ﬁnd
automatically). We solve this problem by adapting an existing approach: for acyclic graphs (which
we focus on in this section), one can provide ﬁrst-order update formulas that express precisely how
adding or deleting a single edge aﬀects reachability [Dong and Su 1995; Lev-Ami et al. 2009]. For
example, the following update formula characterizes the eﬀect of adding an edge between nodes

2019-08-19 00:46. Page 7 of 1–34.
8                                 Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller


                                      x          u     v           y



Fig. 3. The reachability update problem in presence of alternative paths. Concrete heap edges are
represented by straight arrows, while (possibly, zero-length) heap paths are represented by wavy
arrows. The upper path x . . . y depends on the edge (u,v); removing this edge would destroy the
path, but x may still reach y after deleting (u,v), here, via the lower path. Alternative paths may
occur in our setting because we permit multiple reference fields per object.


a and b (e.g., by initializing a ﬁeld of a):
                   ∀x, y • PF (g, x, y) ⇐⇒ P0F (g, x, y) ∨ P0F (g, x, a) ∧ P0F (g, b, y)                  (6)
where P and P0 denote the path predicate in the states before and after the update.
   The update formula for removing an edge is more complex. Since we allow for an arbitrary
out-degree of nodes (via multiple reference ﬁelds), it is possible for there to exist multiple paths
between two diﬀerent nodes (Fig. 3). When adding an edge between two nodes, the new P relation
can be updated relatively simply, e.g., via (6); no paths have been lost, and only paths connected
by this new edge are created. On removal of an edge, no paths are created, but, for node pairs
previously connected by a path using this edge, it is unclear whether or not they belong to the
new P relation, due to the possibility of alternative paths. This entails a more-complex update
formula for the edge-removal case (due to Dong and Su [1995]); see App. A for details. A general
ﬁeld update entails removing and then adding an edge, as we demonstrate for our merge example
in Fig. 7.
   Our veriﬁcation technique rewrites each ﬁeld update x. f := v with a method call to an internal
update method with the same footprint g as for the current method. The postconditions of update
make the reachability update formulas available to the SMT solver. This way, we assume the update
formulas for each ﬁeld set F that is used in the current method speciﬁcation and that contains the
updated ﬁeld f (reachability for other ﬁeld sets is not aﬀected by the update).
   The else-branch in the example from Fig. 1 modiﬁes the heap through a single ﬁeld update.
The second postcondition describes the eﬀect on the edge relation; it follows directly from the
deﬁnition of the edge predicate. The third postcondition, about the path relation, is exactly the
update formula (6), with link and r for a and b, resp.

3.3   Method Calls and Relatively Convex Footprints
Update formulas allow us to precisely capture the eﬀect of adding or removing individual edges,
which is suﬃcient to reason about ﬁeld updates. However, reasoning modularly about method calls
requires us to determine the eﬀect of multiple heap updates. According to the callee’s speciﬁcation,
we can partition the footprint g of the client into the footprint h of the callee and the remainder f
(g = f ⊎ h). This remainder is the frame of the call and cannot be modiﬁed by the callee method.
The postcondition of a callee method provides a speciﬁcation of reachability information within its
footprint h. The challenge is to determine the eﬀect of the call on reachability within the (generally
larger) footprint g of its client. For the edge relation, this extrapolation is straightforward:
                       ∀x ∈ f ⊎ h, y • E(f ⊎ h, x, y) ⇐⇒ E(f, x, y) ∨ E(h, x, y)                          (7)
In separation logic, a method may modify any heap edges that originate in its footprint; hence, the
predicate E(h, x, y) implies that x is in the footprint h and E(f, x, y) implies that x is in the frame f.

                                                                             2019-08-19 00:46. Page 8 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                9


                                                          P0 (g)
                                                            (9)
                                                                    h ≺ g (11)
                                                 (15)
                                                                    P0 (h)

                                            P0 (f)=P(f)            call(h )

                                                                     P(h)
                                                  (8)
                                                                    h ≺ g (12)
                                                            (9)
                                                          P(g)


Fig. 4. The flow of reachability information in the presence of method calls. Reachability informa-
tion in the client’s footprint g = f ⊎ h is split into reachability information within h and f before the
call, the eﬀect of the call on h is accounted for, and then the information is recombined to paths in
g. The numbers in parentheses indicate ingredients of our technique explained in this section.



We refer to edges that cross the boundary of the footprint as cut points: if x ∈ h, y < h, then (x, y)
is an exit point of the footprint, and if x < h, y ∈ h, then (x, y) is an entry point into the footprint.
    Unfortunately, a simple rule such as (7) does not exist for relating paths in f⊎h to those in f and h.
A path can span ﬁelds from both heap partitions, and, in general, could cross the boundary between
the two unboundedly many times. It is known that, in full generality, a ﬁrst-order reachability
framing formula for our path predicate cannot exist (see e.g., [Itzhaky et al. 2014]). The key insight
behind our technique for handling method calls is that this intractable situation becomes tractable
if the footprint of the callee is relatively convex in the composed heap.

   Definition 1 (Relatively Convex Footprints). In a given program state and for a given set of
reference ﬁelds F , footprint h deﬁnes a relatively convex sub-footprint of footprint g (written h ≺ g)
iﬀ g = f ⊎ h for some footprint f, and no paths within g leave h and then return:

                                    ∀x, y ∈ h, u ∈ f • ¬PF (g, x, u) ∨ ¬PF (g, u, y)

   We show, in the remainder of this section, how we exploit this property to enable precise, ﬁrst-
order, and modular reasoning about reachability in presence of method calls. In particular, we are
able to make tractable the problem of framing reachability information when a method footprint h
is relatively convex in its client’s footprint g. This requirement is checked by our technique at the
call site, but is typically naturally the case. For example, any method operating on a recursively-
deﬁned data type, its sub-structures or portions thereof (such as linked list segments), a strongly
connected component of a potentially-cyclic structure, or combinations of these will have a rela-
tively convex footprint. DAG traversals also have relatively convex footprints. For instance, the
recursive call to merge in our running example of Fig. 1 and the corresponding illustration in Fig. 2
demonstrate a method call with a relatively convex footprint. Note that both acyclicity and relative
convexity are deﬁned relatively to a ﬁeld set F . Therefore, even operations on data structures with
back-pointers (such as parent-pointers in a tree) typically have relatively convex footprints as long
as the path predicates are deﬁned in terms of only forward-references or only back-pointers.

2019-08-19 00:46. Page 9 of 1–34.
10                                     Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller


                                                x i footprint (h) yi           frame (f)
                                x ii           a ii   yii x iii        b iii      yiii
                                x iv           a iv                    b iv       yiv
                                xv                                                yv


Fig. 5. No paths originating and ending inside a relatively convex footprint may go though nodes
of its frame. Therefore, the paths that originate in the frame may enter and exit the footprint at
most once. This gives five possibilities for a path to interact with a relatively convex footprint.


Method call overview. A high-level overview of our solution is illustrated in Fig. 4. We use P0 to
represent the paths before the call, and P for those afterwards. According to standard separation
logic reasoning, method calls are only allowed if the callee’s footprint h is a subset of the client’s
(g = f ⊎ h, for some frame f). Under the additional requirement that h ≺ g, the technique we
present in this section shows how to decompose reachability information before the call (i.e., ex-
pressed in terms of P0 (g, . . .)) into paths in the callee’s footprint (P0 (h, . . .)) and paths in the frame
(P0 (f, . . .)). The callee’s speciﬁcation is responsible for relating P(h, . . .) information to P0 (h, . . .)
information, i.e., specifying how reachability changes within the callee’s footprint. Conversely,
reachability purely in the frame f cannot be changed by a call, since it does not have the permis-
sions to do so. Indeed, based on consideration of the permissions not passed to the method call, we
know that the following formula holds (which we call separation-logic framing):
                                  ∀x ∈ f, y • P(f, x, y) ⇐⇒ P0 (f, x, y)                                               (8)
Our technique then provides means of reconstructing reachability in the client’s footprint (P(g, . . .))
from the information we have after the call in terms of P(h, . . .) and P(f, . . .).
Path partitioning. The ﬁrst key step of our solution is path partitioning. We exploit relative convex-
ity of the callee’s footprint to deﬁne a set of formulas for soundly and precisely relating reachability
in a caller’s footprint to reachability in the callee and its frame, and vice versa. Fig. 5 illustrates the
possibilities for a path in the client’s footprint g to interact with a relatively convex footprint h. We
proceed by analyzing Fig. 5 by cases, deriving formulas one of which must hold in each possible
case.
   Crucially, our relative convexity assumption h ≺ g guarantees that no paths x . . . y in g = f ⊎ h
enter or leave h more than once. We summarize the ﬁve cases for paths from x to y based on the
distribution of these nodes between the footprint, h, and the frame of the call, f: (i) x, y ∈ h as
is the whole path, (ii) x ∈ f, y ∈ h; the path crosses the boundary once, (iii) x ∈ h, y ∈ f again
crossing once, (iv) x, y ∈ f with a path entering and leaving h once, and (v) x, y ∈ f with a path
entirely in f. Note that these cases are exhaustive for a path between x, y ∈ g, due to our convexity
restriction.
   These ﬁve cases translate to the following formulas, allowing us to relate reachability in f ⊎ h
and reachability in the two subheaps f and h individually, which we call path partitioning formulas:
                  (i)   ∀x ∈ h, y ∈ h • P(f ⊎ h, x, y) ⇐⇒ P(h, x, y)
                 (ii)   ∀x ∈ f, y ∈ h • P(f ⊎ h, x, y) ⇐⇒ ∃a ∈ h • P(f, x, a) ∧ P(h, a, y)
                (iii)   ∀x ∈ h, y ∈ f • P(f ⊎ h, x, y) ⇐⇒ ∃b ∈ f • P(h, x, b) ∧ P(f, b, y)                             (9)
            (iv)–(v) ∀x ∈ f, y ∈ f • P(f ⊎ h, x, y) ⇐⇒ P(f, x, y) ∨
                                            ∃a ∈ h, b ∈ f • P(f, x, a) ∧ P(h, a, b) ∧ P(f, b, y)

                                                                                         2019-08-19 00:46. Page 10 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                               11

                                                                  u

                                                       y x
                                                      footprint

Fig. 6. The footprint (surrounded with red) is relatively convex before a method call, satisfying (11).
The heap edge created by the call is represented by a dashed arrow. The new edge (x, u) is an exit
point of the footprint into the frame; since its end node u reaches the footprint via some path u . . . y,
adding (x, u) violates the relative convexity property of the footprint (12).


   These formulas can be used left-to-right or right-to-left. In the former case, we obtain a canonical
means of decomposing information about paths in a composed footprint of the client into informa-
tion about paths in the callee’s footprint and paths in the frame. In the latter case, we obtain means
of reassembling reachability information in the composed footprint from that in the constituent
parts. In practice, we add separate assume statements for both directions of each formula, so that
we can clearly specify to the underlying SMT solver when to instantiate the formula in which
direction.
   It is due to our relative convexity assumption that there exist simple ﬁrst-order path partitioning
formulas (9). Without this assumption, the number of cut points of h could be arbitrary, and local-
ization of reachability information would require either considering an unbounded set of cases or
higher-order reasoning, preventing automatic veriﬁcation.
   For simplicity, formulas (9) cover only the cases x, y ∈ g: however, paths that are local to a
particular footprint may leave that footprint by a single edge (and so case (i) above, for example,
does not provide information about such paths in h). The following formulas reduce the case y < g
to the cases already covered by introducing a node u ∈ g with an edge to y:
                    ∀x ∈ h, y < h • P(h, x, y) ⇐⇒ ∃u ∈ h • P(h, x, u) ∧ E(h, u, y)
                                                                                                     (10)
                     ∀x ∈ f, y < f • P(f, x, y) ⇐⇒ ∃u ∈ f • P(f, x, u) ∧ E(f, u, y)

Checking relative convexity of footprints. In terms of reasoning about calls, we emit assume state-
ments for our path partitioning formulas both before and after a method call (to decompose paths
into those matching the callee’s footprint and frame before the call, and to reconstruct information
from these sources back to the client’s footprint, afterwards; cf. Fig. 4). In both cases, before assum-
ing our path-partitioning formulas, we ﬁrst check that the footprint is relatively convex (since this
property justiﬁes their soundness); as we show in Fig. 6, a method’s footprint could be relatively
convex before the call but non-convex in the client’s footprint afterwards. The two checks em-
ployed by our technique must be expressed in slightly diﬀerent terms. Before the call (and without
yet emitting our path-partitioning formulas) the g-local reachability information is available, and
we directly use the formula from Def. 1:
                                     ∀x, y ∈ h, u ∈ f • ¬P(g, x, u) ∨ ¬P(g, u, y)                    (11)
   However, after the call we obtain the h-local reachability from the postcondition of the callee,
while the f-local reachability is preserved. We cannot use g-local reachability in the post-state of
the call; the aim of our path-partitioning formulas is to deduce information in this form, and these
are only justiﬁed after making the convexity check. Therefore, after the method call, we use the
following alternative formulation:
                                     ∀x, y ∈ h, u ∈ f • ¬P(h, x, u) ∨ ¬P(f, u, y)                    (12)



2019-08-19 00:46. Page 11 of 1–34.
                                                                                                                                                                                                                          12
                                                                                                                method merge(l: Ref, r: Ref,
                                                                                                                     g: Set[Ref], ldag: Set[Ref], rdag: Set[Ref])
                                                                                                                    returns link: Ref




                                                                                                           rs
                                                                                                        ete
                                                                                                                    requires ...




                                                                                                      am
                                                                                                                    ensures




                                                                                                  par
                                                                                                                               ...
                                     method merge(l: Node, r: Node,                                             {




                                                                                             ct s
                                                                                                                    if (l.right != null) {




                                                                                         t ra
                                             g :Graph, ldag:Graph, rdag:Graph)




                                                                                     co n
                                         returns link: Node                                                          var nldag: Set[Ref] := sub(g, ldag, l.right)
                                         requires ...                                                                var g1: Set[Ref] := nldag union rdag
                                         ensures    ...                                                              DeduceRelationshipBetweenSubHeaps(g1, g)                           // Convert (1)⇄(2)




                                                                                                                                                                                                                          Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller
                                     {                                                                               var frame: Set[Ref] := g setminus g1
                                         if (l.right != null) {                                                      EnableFocusOnConvexSubHeap(g, g1)                                  // (10), case i of (9)
                                             var nldag := sub(g , ldag, l.right)                                     EnableFocusOnFrame(g1, g, frame)                                   // (10), (15)
                                             link := merge(l.right, r,                                               label l1                                                           // Pre-state of the call
                                                                                             call                    link := merge(l.right, r,
                                               nldag⊎rdag, nldag, rdag)
                                         } else {                                                                       nldag union rdag, nldag, rdag)
                                             l.right := r                                                            label l2                                                           // Post-state of the call
                                             link := l                                                               EnableFocusOnConvexSubHeap(g, g1)                                  // (10), case i of (9)
                                                                                                                     EnableFocus(g, frame)                                              // (1), (2)
                                                                                       ﬁel


                                         }
                                                                                           du



                                     }                                                                               ApplyConvexTCFraming(l1, l2, g1, g, frame)                         // (7), (8), cases ii–iv of (9)
                                                                                               p da




                                                                                                                    } else {
                                                                                                   te




                                                                                                                     if (r != l.right) {
2019-08-19 00:46. Page 12 of 1–34.




                                                                                                                                                              { left, right }
                                                                                                                        if (l.right != null) unlinkDAG right                    (g, l) // (6)
                                                                                                                                                { left, right }
                                                                                                                        if (r != null) linkDAG right              (g, l, r) }           // Sec. 3.2
                                                                                                                     link := l }
                                                                                                                }

                                     Fig. 7. Encoding merge in Viper. Types are translated directly. The specifications (Sec. 2.1) are omitted for brevity. The reference field update
                                     is translated via unlinkDAG , linkDAG (Sec. 3.2). The method call is augmented with local assumptions in the form of macros (lines starting with
                                     capital letters), constraining the states l1, l2. The macros with infix Convex also check relative convexity of corresponding footprints (Sec. 3.3).
                                     The complete encoding is part of the publicly available artifact [Ter-Gabrielyan et al. 2019].
Modular Verification of Heap Reachability Properties in Separation Logic                                  13

Relating reachability information before and after a method call. Based solely on our assumption
of relatively convex footprints, we now have a rich set of formulas available for precisely relating
reachability information before and after a method call. To illustrate how our formulas can be used
in practice, we consider one of the veriﬁcation conditions needed for verifying the postcondition
in Fig. 1 after the recursive call to merge. Concretely, we consider the following Hoare triple:
                                                                                        
         l.right , null ∧ P0 (g, r, n)     link := merge(l.right, r, h , ...)                P(g, l, n)

Here, g and h are the footprints of the client and the callee, resp., l and r are the roots of the
left and right DAGs, resp. (Fig. 2), and n is some node reachable from r in the pre-state; we omit
the rest of the arguments of merge for brevity. The condition l.right , null comes from the
if statement in Fig. 1 and holds before (and after) the recursive call; we enter this branch iﬀ we
have not yet found the link node and must keep recursively traversing the current structure. We
proceed with a proof sketch for the postcondition of this Hoare triple. Other checks needed to
verify the Hoare triple include relative convexity checks (11) and (12), and the precondition check
before the recursive call; these require similar reasoning steps and are omitted for brevity.
   The postcondition P(g, l, n) expresses the existence of a path l . . . n. We justify this postcon-
dition by showing the existence of a (single-edge) frame-local path l . . . l.right and an h-local
path l.right . . . n (where h is the footprint of the call). The former sub-path starts in l < h and
ends in l.right ∈ h (since h = nldag ⊎ rdag, where nldag was constructed via sub), and the
latter sub-path starts in l.right ∈ h and ends in n ∈ h (n ∈ rdag follows from the precondi-
tion P0 (g, r, n) of the Hoare triple and the last precondition of merge, while rdag ⊆ h because
h = nldag ⊎ rdag). The distribution of the starting and ending nodes of these sub-paths enables
an instantiation of (ii) from (9) with l, l.right, n for x, a, y, resp., reducing the overall proof goal
to the two predicates P(f, l, l.right) and P(h, l.right, n). First, since l.right , null, the former
predicate can be justiﬁed by (5) and the postcondition of snapshot . Second, we instantiate the last
postcondition of merge with l.right , n for x, y, resp. in order to reduce the latter predicate to
P0 (h, l.right, link) and P0 (h, r, n). Note that, since the path l.right . . . link starts in the root
of nldag, the former predicate is implied by the last postcondition of merge. We can justify the
latter predicate, P0 (h, r, n), with an instantiation of (i) from (9) with r, n for x, y, resp., since (as we
argued above) r, n ∈ h.                                                                                     

3.4 Frame-Localized Reachability
The ingredients presented thus far form the core of our solution for handling method calls, but are
not yet suﬃcient to preserve reachability information in all cases, as we explain next. In some cases,
we need to be able to localize reachability information in the frame of the call (cf. the left branch
in Fig. 4). But precise frame-local reachability information cannot be obtained the same way as
footprint-local reachability because, unlike method footprints, our technique permits the frame to
be non-convex in the client’s footprint. For example, consider a call to a method that operates on
an acyclic list segment; the footprint of this call must be convex, while the frame would generally
be non-convex in the entire list. Since the issue is subtle, we illustrate how information can be lost
with a concrete example, and then show how to plug the gap.

The problematic scenario. The program in Fig. 8 consists of two methods: the client, joinAndModify ,
and the callee, disconnectAll . This program concerns a particular shape of DAG structure, which
we call a hammock between two nodes. We say that a (closed) DAG h is a hammock between two
(distinct) nodes s and t iﬀ it consists of all nodes reachable from its node s (called the source) that

2019-08-19 00:46. Page 13 of 1–34.
14                                     Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller


method joinAndModify(g : Graph,                           method disconnectAll(g : Graph)
         f: Graph, s 1 : Node, t 1 : Node,                   ensures (∀x, y ∈ g • P(g, x, y) ⇔ x = y) ∧
         h : Graph, s 2 : Node, t 2 : Node)                    ∀x ∈ g, y < g • E(g, x, y) ⇔ E0 (g, x, y)
     requires g = f ⊎ h ∧
       HAMMOCKg (f, s1 , t1 ) ∧ HAMMOCKg (h, s2 , t2 )    The method disconnectAll destroys all non-
                                                          trivial paths inside h (exemplifying a possible de-
       ∧ s 1 .left = null ∧ t 2 .right = null             structive update to the heap structure).
     ensures P(g, s 1 , t 1 )
{
     /* state 0 */ s 1 .left := s 2 ; t 2 .right := t 1
     /* state 1 */ disconnectAll(h )
     /* state 2 */ }


Fig. 8. The method joinAndModify first attaches the hammock h to the hammock f, creating a larger
hammock, and then calls the method disconnectAll , creating a frame that is non-convex in g. Ver-
ification of the postcondition is challenging, as it requires localizing reachability in the frame, f,
of the call to disconnectAll . Fig. 10 illustrates a typical run of joinAndModify .


reach its distinct node t (called the sink):
             HAMMOCKg (h, s, t) ..⇐⇒ s ∈ h ∧ t ∈ h ∧ CLOSED(h) ∧ ACYCLICg (h) ∧ s , t ∧
                                                                                                             (13)
                                             ∀n ∈ h • P(g, s, n) ∧ P(g, n, t)

                    ACYCLICg (h) ..⇐⇒ h ⊆ g ∧ ∀x, y ∈ h • ¬E(g, x, y) ∨ ¬P(g, y, x)                          (14)
The essential property of the example in Fig. 8 is that the client method creates heap edges inside
the footprint of the callee (and not just in the frame of the call), whereas the callee destroys some
of the paths in its footprint.
   We start reasoning about joinAndModify in state 0, with the footprint being comprised of two
(disjoint) hammocks, f and h, where s 1 and s 2 are their sources and t 1 and t 2 are their sinks, resp.
The ﬁrst two operations are ﬁeld updates, resulting in state 1. They join the two hammocks into
one by creating exactly two edges: (s 1 , s 2 ) and (t 2 , t 1 ). Hence, there must exist at least two distinct
paths from s 1 to t 1 in state 1: one path through the nested hammock, h, and one inside f. Note
that this makes the subheap f non-convex in g, even though h is still relatively convex in g. The
last operation in joinAndModify is a method call with a (relatively convex) footprint, h, which
results in state 2. The callee method, disconnectAll , destroys all heap paths inside its footprint
(ﬁrst conjunct of the postcondition), while preserving all of its exit points (second conjunct of the
postcondition). We omit the callee’s implementation because the problem that we are about to
explain occurs exclusively at the call site.
   The postcondition of joinAndModify says that there still exists a g-local path s 1 . . . t 1 in state 2.
Intuitively, this claim should hold, as these two nodes were, before the call to disconnectAll ,
reachable via at least one f-local path that could not have been destroyed as a result of the method
call (because f is the frame of that call). However, our path-partitioning formulas (9) do not cap-
ture that such a frame-local path deﬁnitely existed; we learn from cases (iv)–(v) of (9) only the
disjunction describing that at least one of the two paths from s 1 to t 1 , labeled “iv” and “v” in Fig. 5,
must have existed before the call, but we do not know which. Since the call is known to destroy
the paths corresponding to one disjunct, we cannot deduce P2 (g, s 1 , t 1 ) after the call unless we can
precisely derive frame-local reachability.

                                                                                2019-08-19 00:46. Page 14 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                     15

                                             z            footprint (h)      frame (f)
                               x                                                 y
                                                 z1


                                                      σ    τ

Fig. 9. Paths starting and ending in the frame of a relatively convex footprint may either be local
to the frame or go through the footprint. Relative convexity of the footprint guarantees that there
must be at most one entry and one exit point per path. Note that x and σ , as well as τ and y may
possibly alias each other, but x , y and σ , τ are guaranteed.


Localizing reachability in the frame of a relatively convex footprint. Fig. 9 demonstrates the general
problem of localizing reachability information in the frame of a method call. Consider a method
call with a relatively convex footprint h and the frame f; the client’s footprint g is their disjoint
union g = f ⊎ h. Our path partitioning formulas (9) allow us to precisely deﬁne h-local reachability
based solely on g-local reachability. As demonstrated by our joinAndModify example of Fig. 8,
we additionally need a complementary formula that would precisely deﬁne f-local reachability
(again, based solely on g-local reachability). In other words, we are looking for a ﬁrst-order formula
over the relation P (with the ﬁrst parameter ﬁxed to g) that, for a given pair of nodes x, y ∈ f,
precisely deﬁnes the existence of an f-local path x . . . y. Fortunately, such an in-frame reachability
localization formula exists if f is a frame of a relatively convex footprint h (even if f itself is non-
convex in g):
                                                                                    
           ∀x, y ∈ f • ∀z ∈ h • ¬P(g, x, z) ∨ ¬P(g, z, y) =⇒ P(f, x, y) ⇔ P(g, x, y)
                                                           
           ∀x, y ∈ f • ∃z ∈ h • P(g, x, z) ∧ P(g, z, y) =⇒ P(f, x, y) ⇔ ∃σ , τ ∈ f •
                                                                                                            (15)
                                                            P(g, x, σ ) ∧ E(g, σ , τ ) ∧ P(g, τ , y)∧
                                                                                                      
                                                 ∃z 1 ∈ h. P(g, σ , z 1 ) ∧ ¬ ∃z 2 ∈ h. P(g, τ , z 2 )
   We explain and justify (15) using the diagram of Fig. 9. Generally, since g = f ⊎ h, we can case
split on whether there exists a path x . . . y that goes through h, allowing us to obtain the required
f-local reachability formula. The ﬁrst formula above covers the case in which such a path does
not exist; thus, the following must hold: ∀z ∈ h. ¬P(g, x, z) ∨ ¬P(g, z, y) (which trivially holds
for all x, y ∈ f in the special case when f is convex in g). The second formula above says that, if
there exists a path through h (the upper kind of path in Fig. 9), it must pass through some node
z ∈ h; hence, the following condition must hold: ∃z ∈ h. P(g, x, z) ∧ P(g, z, y). Under this condition,
we must deﬁne the existence of an f-local path that also connects x . . . y. The key idea that we
exploit to justify the second formula in (15) is to use our relative convexity assumption to justify
a three-way split of the (hypothetical) f-local path x . . . y into three segments: a path P(f, x, σ ), an
edge E(f, σ , τ ), and a path P(f, τ , y) (the lower kind of path in Fig. 9). Furthermore, we choose (σ , τ )
such that σ is the last node that reaches h (∃z 1 ∈ h. P(g, σ , z 1 )) and τ is the ﬁrst node that does not
reach h (¬∃z 2 ∈ h. P(g, τ , z 2 )). Under our assumptions about x and y, this requirement can always
be satisﬁed because the footprint of the callee, h, is reachable from (at least) the node x and is
unreachable from (at least) the node y.
   We summarize the conditions under which the predicates deﬁning the three-way split of our
hypothetical path x . . . (σ , τ ) . . . y can be rewritten with g instead of f, without losing precision:

2019-08-19 00:46. Page 15 of 1–34.
16                                    Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller


                                                                      footprint (h)
                                         s2                             t2




                                    s1                                      t1
                                           s 1 .right
                                                                          frame (f)

Fig. 10. An example scenario of running the method joinAndModify . In state 0, only the solid edges
exist. In state 1, the client has created two new edges: (s 1 , s 2 ) and (t 2 , t 1 ). In state 2, the callee has
destroyed all solid-red edges, but there still exists a path s 1 . . . t 1 via solid-blue edges. However, we
cannot deduce the existence of this path using just the path partitioning formulas alone due to the
disjunction in case (iv)–(v) of (9) that does not allow us to distinguish whether all paths between
s 1 and t 1 were passing through the footprint in state 1. Therefore, recovering this bit after the call
to disconnectAll requires precise localization of reachability information in the frame (15).


     • The footprint of the call, h, is convex in the client’s footprint, g.
     • Both nodes x and y are in the frame of the call, f.
     • We picked σ that reaches h and τ that does not reach h s.t. (σ , τ ) is on the path x . . . y.
For the ﬁrst predicate, we need to argue by contradiction: suppose that P(g, x, σ ) were the case, but
P(f, x, σ ) were not (the opposite implication is direct, since f ⊆ g). Then, the path from x to σ must
visit the callee’s footprint, h. However, by construction, σ is known to have a path to some node
in the callee’s footprint, and this violates the assumption that this footprint is relatively convex.
Hence, we get P(f, x, σ ) = P(g, x, σ ). The second predicate is easiest: a single edge between two
nodes in the frame (f) can only depend on the frame itself; therefore, we get E(f, σ , τ ) = E(g, σ , τ ).
The third predicate expresses the existence of a path τ . . . y; since we have picked τ s.t. it does
not reach the footprint, such a path exists in this case exactly when it exists in the frame, giving
P(f, τ , y) = P(g, τ , y). Thus, our construction of σ and τ , along with our relative convexity property
for method footprints, allows us to justify the formulation in (15). These formulas now provide the
missing ingredient for our technique that complements our path-partitioning formulas of (9). 
Revisiting the problematic scenario. We return to our joinAndModify method, and show that we can
now verify the last conjunct of its postcondition. Previously, we were unable to verify P2 (g, s 1 , t 1 )
after the call to disconnectAll , while intuitively, a g-local path s 1 . . . t 1 exists in state 2, because
the method call could not have destroyed the existing frame-local path s 1 . . . t 1 that existed in
state 1 (Fig. 10). Thus, if we could deduce P1 (f, s 1 , t 1 ) (before the call to disconnectAll ), we would
obtain our proof goal. This is now possible using the second equation from (15): instantiating s 1 for
x and t 1 for y, we deduce the hypothesis of the implication, since before the call to disconnectAll
we can deduce that paths from s 1 to t 1 exist passing through the footprint. To deduce P1 (f, s 1 , t 1 )
from our formula, we need to obtain the following property (recall that g = f ⊎ h):
                                                                                                                      
    ∃σ , τ ∈ f. P(g, s 1 , σ ) ∧ E(g, σ , τ ) ∧ P(g, τ , t 1 ) ∧ ∃z 1 ∈ h. P(g, σ , z 1 ) ∧ ¬ ∃z 2 ∈ h. P(g, τ , z 2 )
The existentially-quantiﬁed pair (σ , τ ) can be witnessed by (s 1 , s 1 .right). From this, and our ham-
mock properties (13), all conditions above follow directly, allowing us to deduce our interme-
diate proof goals, P1, 2 (f, s 1 , t 1 ), and use the last case of (9) to deduce the ultimate proof goal,
P2 (g, s 1 , t 1 ).                                                                                    
   Together with (15), the ingredients of our technique presented in Fig. 4 empower completely
general, precise reasoning about reachability in the presence of method calls with relatively convex

                                                                                      2019-08-19 00:46. Page 16 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                      17

footprints. Note that, in examples where stronger properties are known about a method’s footprint,
our formulas from (15) reduce to much simpler criteria. In particular, if a method operates on a
closed data structure (no paths leave the footprint), we can always apply the ﬁrst of our formulas;
the full expressiveness of our conditions is required only in the presence of potential paths crossing
the callee’s footprint (e.g., Fig. 10). Our technique is complete, provided that callee postconditions
specify suﬃcient information about reachability within their footprint. However, even in examples
where this information is incomplete, our technique is applicable and provides useful information
at the call site, for instance, by deducing which frame-local paths will be preserved across a method
call. It is the restriction to method calls with relatively convex footprints which enables us to
express appropriate formulas to preserve this information; without this restriction, we would not
be able to precisely deﬁne the existence of frame-local paths exclusively via coarser reachability
information. Finally, we note on the eﬃciency of formulas (15): in our encoding (demonstrated
in Fig. 7 and validated in Sec. 5), we supply appropriate triggers for the universal quantiﬁers and
Skolemize the existential quantiﬁers.
   This completes our treatment of acyclic graphs and method calls; the latter is the most complex
part of our technique, and applies equally to the cyclic case, which we tackle in the next section.

4     REACHABILITY IN CYCLIC STRUCTURES
In the previous section, we presented our technique for enabling modular reasoning about heap
reachability in combination with ﬁrst-order separation logic. The presented technique operates
under two key restrictions: (1) that method footprints are always relatively convex in their client’s
footprint and (2) that all footprints used contain acyclic graphs. These are two independent crite-
ria, which our technique checks where necessary. Restriction (1) alone enables our handling of
method calls. In this section, we show that we can adapt our technique to a particular setting in
which restriction (2) is dropped: that of general 0–1-path graphs. A graph is called a 0–1-path graph
(hereafter, ZOPG) if there exists at most one (non-trivial) path (modulo cycles) between all pairs of
nodes in the graph; for instance, {(a, b), (b, c), (c, a), (c, d)} is a ZOPG, but {(a, b), (b, a), (a, c), (c, a)}
is not since there are two distinct (non-trivial) paths from a to itself [Dong and Su 1995]. Al-
though this notion does not permit arbitrary cyclic graphs, the technique presented in this section
allows us to adapt our work to reason about reachability in the presence of potentially-cyclic
lists in the heap or more-complex data structures consisting of these, including, for example:
trees where the children of each node are stored in a cyclic list (e.g., using Java LinkedList), gen-
eralized tree-like structures in which some nodes consist of rings, and the ring representation
of heap-ordered trees [Fredman et al. 1986]. Therefore, the ZOPG class is an important general-
ization of (potentially-cyclic) singly-linked lists, which is the class handled in the closest prior
work [Itzhaky et al. 2014].
   Extending our technique to ZOPGs requires a new way of handling direct ﬁeld updates (Sec. 4.1);
our handling in Sec. 3 depended on acyclicity, and a way to retain that certain graphs in the pro-
gram are ZOPGs; modifying a ZOPG by adding an edge could violate the ZOPG invariant (Sec. 4.2).
Note that our requirement of relatively convex footprints (Def. 1) is again crucial, enabling an ef-
ﬁcient solution of the latter problem.

4.1    Field Updates in ZOPGs
To support direct ﬁeld updates, we adapt prior work [Dong and Su 1995] that shows how to pre-
cisely update a more-reﬁned reachability relation called DEP for ZOPGs. There are few changes in
our adaptation: our DEP relation is compatible with the reﬂexive reachability relation (P), whereas
Dong and Su work with irreﬂexive reachability, and we parameterize our DEP relation with two
extra parameters, F and g, supporting separation-logic reasoning, as we did for P in Sec. 2.2. The

2019-08-19 00:46. Page 17 of 1–34.
18                                Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

predicate DEPF (g, x, y, u, v) expresses the existence of a (non-trivial) path of ﬁeld references from
x to y such that all objects on the path (except possibly y) are in g, all ﬁelds are in F , and the path
depends on the edge (u, v). Intuitively, this means that removing (u, v) from the graph will destroy
the path x . . . y (which is the unique path from x to y in a ZOPG). We will omit the parameter F
when it is clear from the context. Note that DEP(g, x, y, u, v) ⇒ u , v since an edge (v, v) cannot
be a dependency of any path: deleting such an edge would not aﬀect reachability. Note also that
DEP(g, x, y, u, v) ⇒ x , y since a trivial path x . . . x does not depend on any edges.
   Although precisely updating the classical reachability relation P in potentially-cyclic graphs af-
ter destructive heap operations is beyond ﬁrst-order logic (and cannot be eﬃciently automated),
the information about the DEP relation can be updated precisely and eﬃciently after such destruc-
tive operations [Dong and Su 1995]. For example, if the edge (s, t) is deleted by executing the
statement s.adj := null in a method with footprint g, then the new relation, DEP, can be simply
expressed via the old relation DEP0 as follows:
           ∀x, y, u, v • DEPF (g, x, y, u, v) ⇐⇒ DEP0F (g, x, y, u, v) ∧ ¬DEP0F (g, x, y, s, t)          (16)
For ﬁxed F and g, the intuition for (16) is this: (x, y, u, v) is in the new relation iﬀ it was in the old
relation and the deleted edge (s, t) was not a dependency of the path x . . . y before the update.
   Precisely updating DEP after an operation that only creates an edge (e.g., by executing the state-
ment s.adj := t) is also possible, provided one additionally checks that the newly-created edge
does not violate the ZOPG invariant; we describe how this check is enforced in Sec. 4.2. As before,
a general ﬁeld update entails removing and then adding an edge (see App. B). Our treatment of the
DEP relation is similar to the treatment of the P relation described in Sec. 3.2: since the mathemati-
cal deﬁnitions of these relations are beyond ﬁrst-order logic, we provide the veriﬁer with a partial
axiomatization (see App. C). We rewrite each ﬁeld update with a call to an internal updateZOPG
method with the same footprint g as for the current method; the postconditions of updateZOPG
make the DEP update formulas (e.g., (16)) available to the SMT solver.
   A technical diﬀerence between our reachability relation P and the DEP relation is that the latter
carries richer information (in particular, knowledge of every edge on which each path depends).
Conversely, it seems unlikely that having to enumerate all edge facts in a graph would be suit-
able for a method speciﬁcation; the abstraction provided by P is typically desirable. Thus, we do
not provide DEP as a primitive in our speciﬁcations, and instead provide a means of converting
between information in one relation and the other, while losing as little information as possible.
Our conversion rules are based on the following main axiom:
                   ∀h, x, y • PF (h, x, y) ∧ x , y ⇐⇒ ∃u, v • DEPF (h, x, y, u, v)                       (17)
Unlike the update formulas that are emitted for concrete method footprints, our conversion axioms
(e.g., (17)) quantify over the footprint (h); as before, we carefully select the triggers for these axioms
to guide the SMT solver’s quantiﬁer instantiation procedure.
   In general, formula (17) does not capture full information in principle expressible with the DEP
relation; intuitively, this is because a single path x . . . y (described by the LHS) may depend on
multiple edges, all of which match the RHS existential quantiﬁer. To partially mitigate this fact,
we augment our axiomatization with a number of additional properties. For instance, one can
easily prove the following formula (an axiom in our technique) about ZOPGs, providing (for ﬁxed
F and g) some quadruples which do not belong to the DEP relation:
                                   ∀h, u, v, w • ¬DEPF (h, v, w, u, v)                                   (18)
Note that if v = w, ¬DEP(h, v, v, u, v) holds because a trivial path v . . . v does not depend on any
edges. Assume v , w. There can be at most one (cycle-free) path from v to w in a ZOPG. If there

                                                                            2019-08-19 00:46. Page 18 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                   19

are no paths from v to w, then we get ¬DEP(h, v, w, u, v) from (17). Otherwise, the edge (u, v) is
not part of the (cycle-free) path v . . . w and cannot be one of its dependencies.                     
   Our ZOPG axiomatization is based on a set of formulas like (18) that, together with (17), help
reasoning about the DEP relation (we provide the full axiomatization in App. C). Equipped with this
conversion between relations P and DEP, precise reachability information is preserved in all cases
that we have observed. This is interesting because the DEP relation carries more information than
the transitive relation P, so (for ﬁxed F and g) not all quadruples (x, y, u, v) in DEP can be extracted
precisely from P, even if all pairs (x, y) in P are known. Intuitively, these missing quadruples appear
not to be needed in practice because the overall proof goals are phrased in terms of just P (and not
DEP).
   We illustrate how reachability information is preserved throughout the transformations be-
tween P and DEP with a concrete example. Consider the following Hoare triple that describes
a heap update in a ZOPG with footprint g and a single reference ﬁeld next:
                                           
                x, y ∈ g ∧ x.next = y ∧                           
                                               x.next := null        ∀m ∈ g • P(g, y, m)
                ∀n, m ∈ g • P0 (g, n, m)
We can justify the postcondition assertion as follows. Consider an arbitrary node m ∈ g. If m = y,
then we trivially get P(g, y, y). Otherwise, we assume m , y, and the remaining proof obligation is
P(g, y, m); to justify this, we need to exploit information from the pre-state. Since by (17), we can
reduce the current proof obligation to DEP(g, y, m, y, y.next), we can instantiate the DEP update
formula (16), obtaining two pre-state conditions: DEP0 (g, y, m, y, y.next) and ¬DEP0 (g, y, m, x, y).
The former is justiﬁed by the precondition quantiﬁer (providing P0 (g, y, m)) and the main conver-
sion axiom (17), whereas the latter can be obtained directly from the additional conversion axiom
(18).
   This example, as well as our evaluation (Sec. 5), show that necessary reachability information
can be fully recovered after the following steps: ﬁrst, conversion from P to DEP, second, application
of update formulas for the DEP relation, and third, conversion from DEP to P. We plan to investigate
as future work the extent to which this approach is always precise for preserving reachability
information of this kind.

4.2   Preservation of the ZOPG Invariant
To justify the handling of ﬁeld updates from the previous subsection, we require knowledge that
the graph being updated is a ZOPG. Since this fact can be violated by changes to the heap, an
important question is how we can know if the ZOPG invariant holds. It can be expressed in ﬁrst-
order logic with the combination of edge and path predicates as follows:
      ZOPG(h) ..⇐⇒ ∀x 1 , x 2 , a, b ∈ h, y • (x 1 , x 2 ∨ a , b) ∧ P(h, x 1, x 2 ) ∧ P(h, x 2, x 1 ) ∧
                               E(h, x 1, a) ∧ ¬P(h, a, x 1 ) ∧
                                                                                        
                               E(h, x 2, b) ∧ ¬P(h, b, x 2) =⇒ ¬P(h, a, y) ∨ ¬P(h, b, y) ∧                (19)
                         ∀x, a, b ∈ h • a , x ∧ b , x ∧ E(h, x, a) ∧ P(h, a, x) ∧
                                                                 E(h, x, b) ∧ P(h, b, x) =⇒ a = b

    The ﬁrst conjunct of the formula expresses a situation in which two (potentially aliasing) nodes
x 1 and x 2 are on the same strongly-connected component (SCC), and two edges (starting in x 1 and
x 2 ) that are diﬀerent—at least by source or target—end in nodes a and b, resp., outside of the SCC
(a and b may alias unless x 1 = x 2 ). In such a case, it is forbidden that any node y is reachable
from both a and b (this would form two diﬀerent paths from the SCC to y). The second conjunct

2019-08-19 00:46. Page 19 of 1–34.
20                                  Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller



method testZopgObligations(g : Zopg, R : Graph, r : Node, u : Node)
     requires {u} ⊎ R ⊆ g ∧ CLOSED({u}) ∧ RINGg (R) ∧ r ∈ R ∧
               ∀x ∈ g, y • P(g, x, y) ∧ P(g, x, u) =⇒ ¬P(g, r , y) // (Pre)
{
       var h : Zopg := {u} ⊎ R // define new ghost parameter
       ringInsert(h , R , r , u )
}
method ringInsert(g : Zopg, R : Graph, r : Node, u : Node)
     requires g = {u} ⊎ R ∧ CLOSED({u}) ∧ RINGg (R) ∧ r ∈ R
                                                            
     ensures RINGg (g) ∧ ∀n < g • P(g, u, n) ⇔ P0 (g, r , n) ∧
                                                                     
              ∀x ∈ g, y • x , u ∧ y , u =⇒ P(g, x, y) ⇔ P0 (g, x, y)
{
       u.next := r.next
       r.next := u
}
                     RINGg (h) ..⇐⇒ FUNCTIONAL(h) ∧ UNSHARED(h) ∧ SCCg (h)
                      SCCg (h) ..⇐⇒ ∀x, y ∈ h • P(g, x, y)
                                                                                                      (20)
                FUNCTIONAL(h) ..⇐⇒ ∀a, b, c ∈ h • E(h, a, b) ∧ E(h, a, c) =⇒ b = c
                  UNSHARED(h) ..⇐⇒ ∀a, b, c ∈ h • E(h, a, c) ∧ E(h, b, c) =⇒ a = b

Fig. 11. An example client with a ZOPG footprint. For simplicity, the method testZopgObligations
has no postconditions. In order to verify it, one must nonetheless prove that the ZOPG invariant
is maintained after the call to ringInsert . The definition of RING is given in (20). Note the diﬀerent
meaning of footprint parameters written in subscripts vs. those written in parentheses (e.g., g and
h, resp., in the definition of SCCg (h)): the former are used as arguments for the E and P predicates,
whereas the latter are used for restricting the domain of quantification.



restricts the structure of SCCs themselves: no two diﬀerent edges may leave the node x and stay
within the same SCC.
   Intuitively, formula (19) is hard to automate because it uses a non-trivial combination of edge and
reachability predicates. Establishing ZOPG(h) would require, for example, the information about
all path splits in h, i.e., all nodes x ∈ h s.t. ∃a, b ∈ h • a , b ∧ E(h, x, a) ∧ E(h, x, b). Such
details ultimately require speciﬁcations to enumerate edges in the graph, which is impractical, and
breaks the abstraction that reachability speciﬁcations grant. Even if the full information about the
edge relation were present, establishing ZOPG(h) would require an induction proof that is beyond
the power of modern SMT solvers. Instead of checking this invariant from scratch, we design a
mechanism for checking that the ZOPG invariant is preserved across changes to the heap.

Extending the specification language for potentially-cyclic footprints. As a ﬁrst step, we introduce an
additional annotation in our speciﬁcation language, so that we can label certain method footprints
as ZOPGs. In addition to general graphs (whose structure is only constrained by other speciﬁca-
tions), such as h : Graph, we allow the footprints of some methods to be more speciﬁcally marked
as ZOPGs, using the syntax g : Zopg. For method footprints declared this way, we will explain the

                                                                         2019-08-19 00:46. Page 20 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                21

                                                footprint (h)

                                               r


                                               u                 frame (f)

Fig. 12. A typical scenario of running testZopgObligations . r is an arbitrary node of the ring, and
u is added to the ring after the call to ringInsert . The diagram demonstrates a data structure with
nodes that can have two reference fields (for simplicity, the implementation of ringInsert shows
a single field, next). The second conjunct in the client’s precondition says that no (non-trivial)
paths may originate from u (there may be paths ending in u). The footprint may have both entry
and exit points, but (as required by the last conjunct in the client’s precondition) each connected
component of the frame may have at most one entry or exit point into the footprint; otherwise, the
ZOPG invariant would be violated by the call.



additional proof obligations necessary to check that we maintain the ZOPG invariant. In particu-
lar, a method with footprint g : Zopg can be translated to a method with footprint g : Graph with
additional ZOPG proof obligations.
   We illustrate the generation of ZOPG proof obligations based on the example in Fig. 11. The
client, testZopgObligations , operates on a ZOPG g that includes two disjoint parts: a ring R and
a (closed) singleton graph consisting of just one node, u. The extra node r denotes an arbitrary
node of the ring. The only operation performed by the client is a call to ringInsert . To verify
that g remains a ZOPG by the end of testZopgObligations , we need to check that the callee does
not create alternative paths—not just in its footprint, h (which is guaranteed to remain a ZOPG,
as the methods with footprints marked by Zopg are locally checked to preserve this property), but
also in the larger subheap, g. The callee ringInsert , operates on a ZOPG that equals the union
of two disjoint parts: a closed singleton graph u and a ring R (these two parts must be mutually-
unreachable in the pre-state). The callee attaches u to the ring R, resulting in a larger ring, u ⊎ R.
The callee’s postcondition says that (in the post-state) its entire footprint is a ring (thus, all pairs of
footprint nodes are mutually reachable), and precisely deﬁnes its local reachability. Local paths that
end outside of the callee’s footprint (i.e., outgoing paths) are deﬁned by the last two conjuncts: the
former says that all exit points reachable from the ring in the pre-state are exactly the exit points
reachable from u in the post-state, whereas the latter preserves all outgoing paths of the initial
ring, i.e., all exit points of the footprint in the pre-state where {u} was closed. Fig. 12 illustrates
the client’s footprint in a state after ringInsert has executed.
Maintaining the ZOPG invariant after a field update. The knowledge that a subheap was a ZOPG
in the pre-state of an operation helps checking that that subheap is still a ZOPG in the post-state,
as we show next. We translate a general ﬁeld update u.next := v in a method with the footprint
g : Zopg to u.next := null; u.next := v, where (assuming v is not null) the ﬁrst update deletes
an edge and the second one creates a new edge. Deleting edges does not alter the graph class
of g. However, a newly added edge may create an alternative path between some nodes of the
graph. Concretely, new paths will be created between all pairs of nodes (x, y) s.t. there exist two
paths: x . . . u and v . . . y. Therefore, we get the following soundness criterion (emitted as a proof
obligation before the second update) for a ﬁeld update in a ZOPG:

                      u , v =⇒ ∀x ∈ g, y • P(g, x, u) ∧ P(g, v, y) =⇒ ¬P(g, x, y)                     (21)

2019-08-19 00:46. Page 21 of 1–34.
22                                      Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller


     x              a     y        x                 a      y     x       a          b   y      x      a            c      y
                    b                                b                                                b             d
     frame         footprint      footprint         frame         frame                         fr.   ft.          frame

             (α)                              (β)                             (γ )                          (δ )
Fig. 13. The four configurations that violate the ZOPG invariant after a method call with a rela-
tively convex ZOPG footprint (in red) and a ZOPG frame (in blue).


Note that y may be outside of the current method’s footprint because a g-local path may leave g
(iﬀ its last edge leaves that subheap). The formula (21) is much simpler than, e.g., (19) because it
is (a) an incremental condition (we used the knowledge that the subheap was a ZOPG before the
update; otherwise, we would need to consider alternative paths other than those introduced by
the new creation) and (b) the operation is a ﬁeld update (hence, only one edge has been added to
the graph). Keeping track of graph classes in the presence of method calls is more involved, but
the idea (a) is again helpful for tackling this problem.
Maintaining the ZOPG invariant after a method call. A method call may violate the ZOPG invariant
at call site even if the footprint of the call remains a ZOPG (a condition which is checked locally
for the callee). The condition that a method call does not violate the ZOPG invariant at call site is
generally as hard to check as the formula (19) itself. Fortunately, this condition can be drastically
simpliﬁed if the footprints or the callee and the client are relatively convex.
   We proceed as follows. First, we enumerate the ways in which a method call that preserves
the ZOPG invariant on its own footprint, could potentially violate that invariant for its client’s
footprint. In particular, this must be by the creation of at least one new path. A call to a method
with a convex footprint may result in one of the four bad heap conﬁgurations (violating the ZOPG
invariant) depicted in Fig. 13. Second, we conjoin the negated formulas (22), (23), (24), (25) charac-
terizing these four bad conﬁgurations, comprising an eﬃcient criterion for preserving the ZOPG
invariant. Checking this criterion can be easily automated: unlike formula (19), our criterion re-
quires no information about the edge relation whatsoever. Our technique encodes this criterion
as a proof obligation for the client. Finally, we sketch a proof of completeness for the four cases in
Fig. 13.
   The bad conﬁguration in Fig. 13 (α) corresponds to a scenario in which the method call has
created an alternative path from x to y, where the former node does not belong to the callee’s
footprint. We can describe this conﬁguration via the following formula:
                  ∃x ∈ f, a, b ∈ h, y < f • a , b ∧ P0 (f, x, a) ∧ P0 (f, x, b)
                                                                                                  (22)
                                                  ∧ P(h, a, y) ∧ ¬P0 (h, a, y) ∧ P(h, b, y)
The symbols P0 and P denote the reachability relation before and after the method call; h is the
callee’s footprint; f is the frame of the call. We evaluate the ﬁrst two reachability predicates in the
old state because frame-local reachability is not aﬀected by the call. The information about the last
three predicates comes from the postcondition of the callee2 . We assume w.l.o.g. that a . . . y has
been newly created by the call (whereas b . . . y may have existed before the call). Both paths could
not have existed before the call, as that would contradict our assumption that g was a ZOPG.
   Returning to our example of Fig. 11, we observe that the precondition of testZopgObligations
is strong enough to prevent the bad conﬁguration (α) after the call to ringInsert ; we prove this
2 It is also possible to get the information about the old reachability relation from a modiﬁed version of (22) where

¬P0 (h, a, y) is dropped and all other path predicates are evaluated in the pre-state.

                                                                                         2019-08-19 00:46. Page 22 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                      23

by contradiction. Assume that, while preserving its local ZOPG invariant, the call results in the
bad conﬁguration (α) for some x ∈ f, a, b ∈ h, y < f; thus, we learn the conjuncts (say, #1 to #6)
from the body of (22). Note that a and b must be distinct (due to #1) and cannot both be in R (due to
#4 and #6; otherwise, there would be alternative paths, violating the ZOPG invariant of the callee’s
footprint in the post-state). We draw the contradiction by instantiating the last conjunct, (Pre), of
the precondition of testZopgObligations : ∀x ∈ g, y. P(g, x, y) ∧ P(g, x, u) ⇒ ¬P(g, r , y). With our
path partitioning formulas (9), #2 and #3 imply P0 (g, x, a) and P0 (g, x, b), resp. Together, #4 and #5
express that a . . . y is a newly created path; hence either a = u or y = u (see Fig. 12). If a = u, y , u,
then b ∈ R; we draw the contradiction by instantiating (Pre) with x, b for x, y. Otherwise, a , u,
y = u = b, then a ∈ R; we draw the contradiction by instantiating (Pre) with x, a for x, y.              
   Similarly, we can describe the bad conﬁguration in Fig. 13 (β) using the following formula:
                  ∃x ∈ h, a, b ∈ f, y < h • a , b ∧ P0 (f, a, y) ∧ P0 (f, a, y)
                                                                                                       (23)
                                                   ∧ P(h, x, a) ∧ ¬P0 (h, x, a) ∧ P(h, x, b)
In this conﬁguration, the source of the alternative paths falls into the callee footprint, and their
end into the frame; this results in alternative paths x . . . a . . . y and x . . . b . . . y. In our example of
Fig. 11, the new outgoing paths that ringInsert creates originate in u; all other outgoing paths
also existed before the call (due to the last postcondition). In order to avoid the bad conﬁguration
(β), testZopgObligations requires that no paths may originate in the attached node u. Thus, any
new outgoing path must pass through R before it reaches the callee’s footprint. Since ringInsert
preserves the paths that start in R and end in the frame (due to its last postcondition), and we
assumed that the callee’s footprint is a ZOPG before and after the call, the last three conjuncts in
(23) cannot be satisﬁed. Hence, our speciﬁcation is strong enough to prevent (β).                             
   The scenario depicted in Fig. 13 (γ ) illustrates that any new path a . . . b created by the method
call, combined with suitable frame paths, may violate the ZOPG invariant:
      ∃x, b ∈ f, a ∈ h, y < h • P0 (f, x, y) ∧ P0 (f, x, a) ∧ P0 (f, b, y) ∧ P(h, a, b) ∧ ¬P0 (h, a, b).    (24)
In order to avoid the bad conﬁguration (γ ), we must ensure that an arbitrary frame node x that
reaches the footprint node a does not reach any of the frame nodes (e.g., y) that will be reachable
from a after the call. In our example of Fig. 11, the precondition of testZopgObligations is strong
enough to prevent (γ ) after the call to ringInsert . The nodes x and y in the last conjunct of this
precondition can be thought of as those in (24) and Fig. 13 (γ ); the condition rules out the possibility
that the eﬀect of the call will connect up such alternative path.                                              
   The most subtle bad conﬁguration is Fig. 13 (δ ), where both alternative paths x . . . y go via the
footprint of the method call. This heap conﬁguration can be expressed via the following formula:
   ∃x, c, d ∈ f, a, b ∈ h, y < h • a , b ∧ c , d ∧ P0 (f, x, a) ∧ P0 (f, x, b) ∧ P0 (f, c, y) ∧ P0 (f, d, y)
                                                                                                             (25)
                                                 ∧ P(h, a, c) ∧ ¬P0 (h, a, c) ∧ P(h, b, d).
This conﬁguration can be realized when a and b are mutually unreachable in both states (otherwise,
the conﬁguration is covered by (α) and (β)). This conﬁguration cannot occur in the post-state of
our example because after the method call u is attached to the ring.                            
Completeness proof sketch. To derive the four cases in Fig. 13, consider a ZOPG subheap g com-
prised of the ZOPG frame f and the (relatively convex) ZOPG footprint h of a method call. Assume
that the method call creates at least one new path s.t. the ZOPG invariant of its footprint is main-
tained while the ZOPG invariant of the (larger) client’s footprint is violated. Consider as well two
nodes x and y that are connected (in the state after the call) by multiple (at least two) g-local paths
x . . . y. We assume that x and y are both in g; if y is outside g, we ﬁrst apply (10), providing some
node u ∈ g s.t. P(g, x, u) ∧ E(g, u, y); we then continue the argument for x . . . u instead of x . . . y.

2019-08-19 00:46. Page 23 of 1–34.
24                                 Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

  Multiple paths x . . . y may not be entirely inside just one of the two subheaps f or h because that
would violate our assumption that these are ZOPG subheaps. Therefore, at least one of these paths
must cross the border between f and h. We proceed with a case analysis based on the distribution of
the nodes x and y between (disjoint) subheaps h and f:
      • The case x, y ∈ h cannot be realized because a path starting in x may leave h just once and
        may never come back to reach y (otherwise our convexity assumption would be violated).
      • If x ∈ h, y ∈ f, then again, the paths starting in x may leave h just once and may never come
        back due to h ≺ g. Since two diﬀerent paths starting in x may not merge in h (otherwise,
        alternative paths will exist within h, contradicting our assumption that it is a ZOPG), such
        paths must reach two diﬀerent frame nodes a, b ∈ f, creating alternative paths of the form
        x . . . a . . . y and x . . . b . . . y, as covered by case (β) of Fig. 13.
      • If x ∈ f, y ∈ h, then no path that starts in the frame node x can enter the footprint more than
        once due to h ≺ g. Next, since in this case these paths must end in y, they cannot leave the
        (relatively convex) footprint h at all. Finally, these paths may not merge until at least one of
        them enters h (otherwise, alternative paths will exist within f, contradicting our assumption
        that it is a ZOPG). This gives us two diﬀerent footprint nodes a, b ∈ h, creating alternative
        paths of the form x . . . a . . . y and x . . . b . . . y, as covered by case (α) of Fig. 13.
      • In the most subtle case of x, y ∈ f, each pair of alternative paths of the form x . . . y is s.t.
        either just one or each of the two alternative paths enters and exits the footprint exactly once,
        as covered by cases (γ ) and (δ ) of Fig. 13, resp.                                            
   The simplicity of our formulas (22), (23), (24), (25) is due to the fact that, in our technique, foot-
prints of method calls must be relatively convex, limiting the number of bad conﬁgurations to just
four. The bad conﬁgurations that we have identiﬁed are helpful for deriving weakest preconditions
for method calls that operate over ZOPGs, like in our testZopgObligations example. In combina-
tion with local heap updates (for which (21) is the eﬃcient ZOPG preservation criterion), we have
explained how our technique is generalized for modular reasoning about ZOPGs.

5     EVALUATION
We have evaluated our technique on a variety of challenging example programs taken from the
literature, illustrating our technique for diﬀerent classes of graphs and data structures (including
the running examples of closely-related work).

5.1    Experimental Setup
We encoded each example by-hand into the Viper veriﬁcation language [Müller et al. 2016b]: an
intermediate veriﬁcation language designed for expressing heap-based veriﬁcation problems, and
with native support for separation logic reasoning. Although manual, our encoding of each exam-
ple was performed methodically, simulating the translation that a front-end veriﬁcation tool could
perform. Each example consists of a common set of background deﬁnitions and axioms, along
with a translation of the code of the example, statement by statement, according to the technique
presented in Sec. 3 and Sec. 4. For instance, a source-level method call is encoded with additional
assume and assert statements before and after the call which enable reachability framing on rel-
atively convex method footprints, as deﬁned in Sec. 3.4.
   The background deﬁnitions common to our examples are organized in separately-included li-
brary ﬁles, and we make heavy use of Viper’s macros to improve the readability of our encoded ex-
amples. Our examples are veriﬁed with Viper’s standard Boogie-based [Leino 2008] veriﬁer, which
uses the Z3 SMT solver [de Moura and Bjørner 2008] for checking veriﬁcation conditions. We in-
dicate Viper’s run time for each example in Tab. 1. The experiments were performed on a laptop

                                                                           2019-08-19 00:46. Page 24 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                               25


          Example           Variant          Class           ≺ Time Notes
          Merge (Fig. 1)   Tree              DAG     X     X     16.1   Path-partitioning,
                           DAG               DAG     X   X X     14.5   Unbounded cut-points
                           Fail 1            DAG     X   X X     13.2   Bug in code
                           Fail 2            DAG     X   X X     33.9   Bug in spec.
          Left-Child-      Tree, add sibl.   DAG     X     X     10.5   Encodes n-ary tree as binary
          Right-Sibling Tree, add child      DAG     X     X     15.0          —”—
                           DAG, add sibl.    DAG     X   X X     10.1   Unbounded cut-points
                           DAG, add child    DAG     X   X X     17.1          —”—
          Harris List      Original          DAG         X       14.5   From [Krishna et al. 2018]
          Acyclic List     Reverse           DAG                  7.9   From [Lev-Ami et al. 2009]
                           Append            DAG                  6.9          —”—
          Ring-Insert:     Sorted            ZOPG    X   X       87.2   Functional spec.
          Impl.            Anywhere          ZOPG    X   X       10.1          —”—
          Ring-Insert:     Closed {u}        ZOPG    X   X   X   11.5   Non-convex frame,
          Client (Fig. 11) Open {u}          ZOPG    X   X   X   10.8   ZOPG obligations
                           Fail 1            ZOPG    X   X   X   12.4   Failure due to (β)
                           Fail 2            ZOPG    X   X   X   10.7   Failure due to (α), (γ )
Table 1. Experimental results. We indicate example features via X where and denote exam-
ples with greater-than-one outdegree and with sharing, resp.; ≺ means convex framing.




running macOS, with a 2.8 GHz Intel Core i7 CPU, with Z3 version 4.8.5 - 64 bit. The Viper ﬁles
used in our experiments are available as artifact of this paper [Ter-Gabrielyan et al. 2019].
   An important practical issue arising in the successful use of SMT-based veriﬁcation tools is con-
trolling the instantiation of quantiﬁers; our technique employs a large number of quantiﬁed formu-
las, and we have carefully selected appropriate triggers [Barrett et al. 2017; de Moura and Bjørner
2008; Detlefs et al. 2005; Moskal 2009] for these, guided by the intended situations in which these
formulas are relevant; for the rich reachability properties expressed by our technique, such trig-
gers are essential for performance. Since our source-level speciﬁcations can also contain quantiﬁed
formulas, we require these to be annotated with appropriate triggers (for simple cases, Viper can
also infer appropriate choices if omitted).

5.2 Experiments
Tab. 1 gives an overview of our experiments. The “Merge” example is our ﬁrst running example
of Fig. 1, in variants with both tree and DAG structures for the underlying graphs (obtaining the
DAG variant simply requires dropping the tree requirements throughout; no other changes are
necessary). “Left-Child-Right-Sibling” is a technique for encoding trees with arbitrary multiplici-
ties using only two ﬁelds (representing a list of children at each node), as employed in binomial
heaps [Cormen et al. 2009], and recently proposed as a veriﬁcation challenge [Müller 2018]. We
again show a DAG variant (directly obtained by removing tree requirements), and verify adding
sibling and child structures. As with the running example, these are non-functional graphs with
(in the DAG case) sharing and requiring our convex framing to frame reachability across sub-calls;
to our knowledge, they are beyond reach for all existing automated graph-veriﬁcation techniques.
   The “Fail” variants of Merge are buggy, with the bug being (1) negation of the branch condition in
the body of merge and (2) missing merge’s last precondition. We have observed that the failure time
does not diverge from the time of a successful veriﬁcation attempt. This is important in practice if

2019-08-19 00:46. Page 25 of 1–34.
26                               Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller


       Data structure                        Class     Itz. Gr. Nv. Author
       Arbitrary linked-list structures      ZOPG     X     –
       2-opt, 3-opt, etc.                    ZOPG         X Croes [1958]; Lin [1965]
       Hierarchical rings                    ZOPG         X Fredman et al. [1986]
       The priority inheritance protocol     ZOPG         X Sha et al. [1990]
       Trees encoded via Java’s LinkedList   ZOPG         X Sun, Oracle
       Union-Find                            ZOPG/DAG X     Tarjan [1975]
       Trees                                 ZOPG/DAG   X   –
       Binary Decision Diagrams                   DAG     X Akers Jr. [1978]; Lee [1959]
       General DAGs (DFG, VCS, etc.)              DAG     X –
Table 2. Supported data structure categories. “Itz.” denotes [Itzhaky et al. 2014]; “Gr.” denotes
GRASShopper [Piskac et al. 2014]; “Nv.” indicates whether, to our knowledge, our technique en-
ables automated verification of modularly specified reachability properties for the first time.




a program’s implementation and speciﬁcation are developed iteratively, with multiple invocations
of the veriﬁer.
   Lev-Ami et al. verify reachability for linked-list reverse and append methods [Lev-Ami et al.
2009]; the recent Flows framework [Krishna et al. 2018] uses the Harris List as running example.
In both cases, we prove the same invariants and reachability speciﬁcations, simply encoded in our
language. In the latter case, we use two reachability relations based on diﬀerent edges.
   “Ring-Insert” is a series of six 0–1-path graph examples. We wrote two variants of the Ring-Insert
method. “Sorted” is an implementation that traverses a sorted ring and inserts a newly allocated
node into the right place. We can prove both reachability (the ring remains a ring) and sortedness;
our connection to separation-logic reasoning makes layering additional functional speciﬁcations
of this kind straightforward. “Anywhere” is the version discussed in Sec. 4, where the insertion
happens at an arbitrary point in the ring. We also veriﬁed two types of clients of Ring-Insert.
“Closed {u}” is the example of Fig. 11, where the attached node does not have outgoing paths,
whereas “Open {u}” permits the attached node to be both reachable from the frame and have
outgoing paths. The latter requires a more subtle precondition to satisfy the 0–1-path preservation
criteria. In the ﬁnal two cases, we show that our technique allows us to automatically identify the
type of bad conﬁgurations that may violate the 0–1-path invariant in cases where the heap is
under-constraint before a method call Sec. 4.2.

5.3 Results
Our experiments show that reachability properties are amenable to SMT-based veriﬁcation for a
broad class of heap-manipulating programs. In particular, we have observed that our technique is
well-suited for this task despite heavy usage of quantiﬁed formulas. While developing the speciﬁ-
cations, we have experienced that our technique helps the programmer to better understand the
subtle eﬀects of heap operations on data structure invariants. Even with good tool support, writ-
ing consistent preconditions and postconditions requires particular craftsmanship, especially for
recursive methods, like merge. Additionally, SMT-based veriﬁcation with quantiﬁers requires the
programmer to annotate the speciﬁcations with triggers.

6    RELATED WORK
Most work on separation logic focuses on data structures with limited sharing, with some no-
table exceptions. Iterated separating conjunction has been used to verify the Schorr-Waite graph

                                                                        2019-08-19 00:46. Page 26 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                           27

marking algorithm [Yang 2001a], but without any tool support or automation. Recent work on
Flows [Krishna et al. 2018] allows one to prove the preservation of a rich variety of graph invari-
ants including reachability properties, but requires ﬁxpoint computations that are hard to auto-
mate. Methods can operate on a subgraph; under the condition that interfaces [Krishna et al. 2018]
of these subgraphs are preserved, a view on the caller’s graph can be reconstructed. They make no
convexity restriction, but the interface preservation conditions rule out the possibility of method
calls adding or removing paths between nodes in subgraph boundaries. By contrast, our reacha-
bility framing technique explicitly enables such side-eﬀectful methods, and the reconstruction of
appropriate changes in the caller’s footprint. For instance, in our running example of Fig. 2, new
reachability relations are ﬁrst established (by creating an edge from link to the root of rdag) and
then propagated (by the enclosing method calls) to the larger context (the entirety of the client’s
footprint).
   We adapted the precise transitive-closure update formulas from Dong and Su [1995] to program
heaps and separation logic, rather than mathematical graphs. Their work also inspired our DEP
relation; however, our version of the DEP relation is compatible with the reﬂexive reachability
relation and is used only in the internal encoding, whereas theirs is exposed to programmers.
Reachability has been integrated into separation logic before (e.g., in GRASShopper [Piskac et al.
2014]), but only in a limited way that supports lists and trees but not heap structures with sharing.
   Our work was inspired by Itzhaky et al. [2014, 2013]. Their veriﬁcation technique allows one
to prove reachability properties in various forms of list data structures. A focus of their work is
to obtain decidable proof obligations. We sacriﬁced decidability in favor of supporting arbitrary
acyclic graphs (with bounded out-degree) as well as 0–1-path graphs; our evaluation shows that
we nevertheless achieve good automation. In contrast to Itzhaky et al., we integrated our work into
separation logic, which allows us to verify concurrent programs and to reason about reachability
and other properties in a uniform way. Moreover, we do not restrict method footprints in the num-
ber of entry and exit points or the number of SCCs in them. Tab. 2 summarizes the expressiveness
of our technique and compares it with closely-related work.



7 CONCLUSIONS
We presented a speciﬁcation and veriﬁcation technique that allows one to reason about heap reach-
ability properties modularly. The technique is integrated into separation logic and, thus, beneﬁts
immediately from the plurality of techniques and tools in this area. The key challenge of this
integration is to specify reachability locally, within the footprint of a method. We solved this chal-
lenge by specifying reachability relatively to a given heap fragment and introducing a novel form
of reachability framing to extend reachability properties in the footprint of a callee method to the
larger footprint of the caller. Even though reasoning about general reachability properties is dif-
ﬁcult to automate, the proof obligations required by our technique are amenable to SMT solvers,
which we demonstrate in our experiments.
   As future work, we plan to extend our technique to graphs with unbounded outdegree. This
can be done by using a generalized version of iterated separating conjunction [Müller et al. 2016a]
that can specify permissions to sets of resources. Another direction of future work is to adapt our
technique to separation logic with fractional permissions [Boyland 2003] to distinguish read and
write access, especially in concurrent settings. We also plan to investigate the extent to which our
approach to cyclic graphs is always precise. Finally, we are planning to implement a front-end
veriﬁcation tool that will simplify the process of writing modular reachability speciﬁcations.


2019-08-19 00:46. Page 27 of 1–34.
28                                     Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

ACKNOWLEDGMENTS
We are grateful to the anonymous referees for their thoughtful comments. We also thank Uri Juhasz,
Marco Eilers, Gishor Sivanrupan, Jérôme Dohrau, Sviatlana-Maryia Zdobnikava,
Alexandra-Olimpia Bugariu, Siddharth Krishna, Felix Wolf, Vytautas Astrauskas, Federico Poli,
Martin Clochard, K. Rustan M. Leino, and Shachar Itzhaky for their help. This work was funded
in part by SNF under project 200021-156980.


REFERENCES
Sheldon B. Akers Jr. 1978. Binary Decision Diagrams. IEEE Trans. Comput. 27, 6 (1978), 509–516.
Clark Barrett, Pascal Fontaine, and Cesare Tinelli. 2017. The SMT-LIB Standard: Version 2.6. Technical Report. Department
   of Computer Science, The University of Iowa. Available at www.SMT-LIB.org.
John Tang Boyland. 2003. Checking Interference with Fractional Permissions. In SAS (Lecture Notes in Computer Science),
   Vol. 2694. Springer, 55–72.
Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Cliﬀord Stein. 2009. Introduction to Algorithms, 3rd Edition.
   MIT Press.
G. A. Croes. 1958. A Method for Solving Traveling-Salesman Problems. Operations Research 6, 6 (1958), 791–812.
Leonardo Mendonça de Moura and Nikolaj Bjørner. 2008. Z3: An Eﬃcient SMT Solver. In TACAS (Lecture Notes in Computer
   Science), C. R. Ramakrishnan and Jakob Rehof (Eds.), Vol. 4963. Springer, 337–340.
David Detlefs, Greg Nelson, and James B. Saxe. 2005. Simplify: A Theorem Prover for Program Checking. Journal of the
   ACM 52, 3 (2005), 365–473.
Guozhu Dong and Jianwen Su. 1995. Incremental and Decremental Evaluation of Transitive Closure by First-Order Queries.
   Inf. Comput. 120 (1995), 101–106.
Michael L. Fredman, Robert Sedgewick, Daniel Dominic Sleator, and Robert E. Tarjan. 1986. The pairing heap: A new form
   of self-adjusting heap. Algorithmica 1 (1986), 111–129.
Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Ori Lahav, Aleksandar Nanevski, and Mooly Sagiv. 2014. Modular
   Reasoning About Heap Paths via Eﬀectively Propositional Formulas. In POPL, Suresh Jagannathan and Peter Sewell
   (Eds.). ACM, 385–396.
Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Aleksandar Nanevski, and Mooly Sagiv. 2013. Eﬀectively-
   Propositional Reasoning about Reachability in Linked Data Structures. In CAV, Natasha Sharygina and Helmut Veith
   (Eds.). Springer Berlin Heidelberg, 756–772.
Siddharth Krishna, Dennis E. Shasha, and Thomas Wies. 2018. Go with the ﬂow: compositional abstractions for concurrent
   data structures. PACMPL 2, POPL (2018), 37:1–37:31.
C. Y. Lee. 1959. Representation of switching circuits by binary-decision programs. The Bell System Technical Journal 38, 4
   (1959), 985–999.
K Rustan M Leino. 2008. This is Boogie 2. (2008). https://www.microsoft.com/en-us/research/publication/this-is-boogie-2-2/
K. Rustan M. Leino and Rosemary Monahan. 2009. Reasoning about comprehensions with ﬁrst-order SMT solvers. In SAC,
   Sung Y. Shin and Sascha Ossowski (Eds.). ACM, 615–622.
Tal Lev-Ami, Neil Immerman, Thomas W. Reps, Mooly Sagiv, Siddharth Srivastava, and Greta Yorsh. 2009. Simulating reach-
   ability using ﬁrst-order logic with applications to veriﬁcation of linked data structures. Logical Methods in Computer
   Science 5, 2 (2009).
Shen Lin. 1965. Computer solutions of the traveling salesman problem. The Bell System Technical Journal 44, 10 (1965),
   2245–2269.
Michal Moskal. 2009. Programming with triggers. ACM International Conference Proceeding Series (2009).
Peter Müller. 2018. The Binomial Heap Veriﬁcation Challenge in Viper. In Principled Software Development, Peter Müller
   and Ina Schaefer (Eds.). Springer-Verlag, 203–219.
Peter Müller, Malte Schwerhoﬀ, and Alexander J. Summers. 2016a. Automatic Veriﬁcation of Iterated Separating Conjunc-
   tions using Symbolic Execution. In CAV (LNCS), Swarat Chaudhuri and Azadeh Farzan (Eds.), Vol. 9779. Springer-Verlag,
   405–425.
Peter Müller, Malte Schwerhoﬀ, and Alexander J. Summers. 2016b. Viper: A Veriﬁcation Infrastructure for Permission-Based
   Reasoning. In VMCAI (LNCS), Barbara Jobstmann and K. Rustan M. Leino (Eds.), Vol. 9583. Springer-Verlag, 41–62.
Matthew J. Parkinson and Gavin M. Bierman. 2005. Separation logic and abstraction. In POPL, Jens Palsberg and Martín
   Abadi (Eds.). ACM, 247–258.
Matthew J. Parkinson and Alexander J. Summers. 2011. The Relationship between Separation Logic and Implicit Dynamic
   Frames. In ESOP, Gilles Barthe (Ed.). 439–458.


                                                                                       2019-08-19 00:46. Page 28 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                            29

Ruzica Piskac, Thomas Wies, and Damien Zuﬀerey. 2014. GRASShopper - Complete Heap Veriﬁcation with Mixed Speci-
   ﬁcations. In TACAS (Lecture Notes in Computer Science), Erika Ábrahám and Klaus Havelund (Eds.), Vol. 8413. Springer,
   124–139.
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In IEEE Symposium on Logic in
   Computer Science (LICS ’02). IEEE Computer Society, 55–74.
Lui Sha, Ragunathan Rajkumar, and John P. Lehoczky. 1990. Priority inheritance protocols: an approach to real-time
   synchronization. IEEE Trans. Comput. 39, 9 (1990), 1175–1185.
Jan Smans, Bart Jacobs, and Frank Piessens. 2012. Implicit Dynamic Frames. ACM Transactions on Programming Languages
   and Systems 34, 1, Article 2 (2012), 58 pages.
Robert Endre Tarjan. 1975. Eﬃciency of a Good But Not Linear Set Union Algorithm. Journal of the ACM 22, 2 (1975),
   215–225.
Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller. 2019. Modular Veriﬁcation of Heap Reachability Prop-
   erties in Separation Logic (Artifact). https://doi.org/10.5281/zenodo.3367478
Hongseok Yang. 2001a. An example of local reasoning in BI pointer logic: the Schorr-Waite graph marking algorithm. In
   Proceedings of the SPACE Workshop.
Hongseok Yang. 2001b. Local Reasoning for Stateful Programs. Ph.D. Dissertation. Advisor(s) Uday S. Reddy.




2019-08-19 00:46. Page 29 of 1–34.
30                                Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

Appendix A PRECISE UPDATE FORMULAS FOR THE REACHABILITY QUERY IN
           ACYCLIC STRUCTURES
In this section, we present the general encoding of ﬁeld updates in acyclic graphs, as introduced
in Sec. 3. Our goal is to rewrite operations of the form from.f := to in such a way that would
introduce reachability update formulas [Dong and Su 1995] to the veriﬁer. We denote the footprint
of the method enclosing this ﬁeld update as g. We assume that this methods implementation and
speciﬁcation mentions reference ﬁelds from the set F ; in particular, f ∈ F .
   Since general ﬁeld updates may result in a deletion and then a creation of two diﬀerent heap
edges, we rewrite them, w.l.o.g., as sequence of two (conceptually simpler) operations:
define updateDAG fF (g : Graph, from: Node, to: Node) {
     // state 1
     if ( to != from.f ) {
      if ( from.f , null ) {
        assert ACYCLIC(g)
        unlinkDAG fF (g , from)
      } // state 2
      if ( to , null ) {
        linkDAGfF (g , from, to)
        assert ACYCLIC(g)
}} // state 3 }
   If to == from.f , then state 1 and state 3 are identical; therefore, neither the ﬁeld value, nor the
reachability relation should be updated. Otherwise, we proceed with two (conditional) operations
(we postpone the discussion of the explicit assertions until the end of this section). The ﬁrst op-
eration, called unlinkDAG , removes exactly one heap edge by assigning null to node.f ; note that
the pre- and post-states of this operation (state 1 and state 2, resp.) are identical if the value of
the considered ﬁeld is already null; hence, the ﬁrst if statement. The second operation, called
linkDAG , requires that its last argument, to (i.e., the destination of the created edge) is non-null;
the operation then creates exactly one heap edge by assigning to to node.f ; note that the pre- and
post-states of this operation (state 2 and state 3, resp.) are identical if the value of the considered
ﬁeld is already to; hence, the second if statement.
   The memory speciﬁcations in our unlinkDAG and linkDAG operations express access permis-
sions to all reference ﬁelds from F of all objects in the current method’s footprint (g). In logics
that diﬀerentiate read and write permissions (e.g., [Boyland 2003]), we require write permissions
only to the single reference ﬁeld that is modiﬁed by this operation; that is, concretely, node.f and
from.f in the contracts of unlinkDAG and linkDAG , resp. For all other reference ﬁelds, we require
read permissions, because we are only interested in the existing values of those ﬁelds (to be able
to deﬁne our g-local reachability relation). These memory speciﬁcations can be realized via the
iterated separating conjunction [Müller et al. 2016a] available in Viper [Müller et al. 2016b].




                                                                         2019-08-19 00:46. Page 30 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                     31

method unlinkDAG fF (g : Graph, node: Node)
  requires MEMORY_SPECSfF (g, node)
  requires node ∈ g ∧ f ∈ F ∧ node.f , null
  ensures MEMORY_SPECSF (g, node)f
  ensures node.f = null
                Ó                                           
  ensures           e∈F , e,f old(node.e) , old(node.f )        =⇒ UNLINKF (g, node, old(node.f ))

method linkDAG fF (g : Graph, from: Node, to: Node)
  requires MEMORY_SPECSfF (g, from)
  requires from ∈ g ∧ f ∈ F ∧ from.f = null ∧ to , null
  ensures MEMORY_SPECSF (g, from)f
  ensures from.f = to
                Ó                                
  ensures           e∈F , e,f old(from.e) , to       =⇒ LINKF (g, from, to)


                     LINKF (g, α, β) ..⇐⇒ G_PLUS_DELTA(old(snapF (g)), snapF (g), α, β)∧
                                           TC_G_MINUS_DELTA(old(snapF (g)), snapF (g), α, β)∧
                                           TC_G_PLUS_DELTA(old(snapF (g)), snapF (g), α, β),
                 UNLINKF (g, α, β) ..⇐⇒ G_MINUS_DELTA(snapF (g), old(snapF (g)), α, β)∧
                                           TC_G_MINUS_DELTA(snapF (g), old(snapF (g)), α, β)∧
                                           TC_G_PLUS_DELTA(snapF (g), old(snapF (g)), α, β),
      G_PLUS_DELTA(д, G, α, β) ..⇐⇒ ∀x, y • (x, y) ∈ G == (x, y) ∈ д ∨ x = α ∧ y = β,
     G_MINUS_DELTA(д, G, α, β) ..⇐⇒ ∀x, y • (x, y) ∈ д == (x, y) ∈ G ∧ (x , α ∨ y , β),
 TC_G_PLUS_DELTA(д, G, α, β) ..⇐⇒ ∀x, y • P̂ (G, x, y) == P̂(д, x, y) ∨ P̂(д, x, α) ∧ P̂(д, β, y),
                                                                                                    
TC_G_MINUS_DELTA(д, G, α, β) ..⇐⇒ ∀x, y • ¬P̂(G, x, α) ∨ ¬P̂(G, β, y) =⇒ P̂(д, x, y) == P̂(G, x, y)
                                           ∧ ∀x, y • P̂(G, x, α) ∧ P̂(G, β, y) =⇒
                                                                    P̂(д, x, y) == casei (G, x, α, β, y)∨
                                                                                   caseii (G, x, α, β, y)∨
                                                                             caseiii (G, x, α, β, y),
                                     .
               casei (G, x, α, β, y) .⇐⇒ ∃u • u , α ∧ u , β ∧ P̂(G, α, u) ∧ P̂ (G, u, β),
              caseii (G, x, α, β, y) ..⇐⇒ ∃u • P̂(G, x, u) ∧ P̂(G, u, y) ∧
                                                                                                     
                                           ¬P̂(G, u, α) ∧ ¬P̂(G, α, u) ∨ ¬P̂(G, u, β) ∧ ¬P̂(G, β, u) ,
             caseiii (G, x, α, β, y) ..⇐⇒ ∃u, v • (u , α ∨ v , β) ∧ Ê(G, u, v) ∧
                                           P̂(G, x, u) ∧ P̂(G, u, α) ∧ P̂(G, β, v) ∧ P̂(G, v, y).
   Our reachability update formulas, called LINKF and UNLINKF , are three-fold. First, we update the
edge relation, E, using the macros called G_MINUS_DELTA and G_PLUS_DELTA. Second, we directly
update the transitive path relation, P, using the macros TC_G_MINUS_DELTA and TC_G_PLUS_DELTA
for UNLINKF and LINKF , resp. These correspond to the decremental and incremental transitive
closure update formulas by Dong and Su [1995], with two exceptions: (1) our macros use ternary

2019-08-19 00:46. Page 31 of 1–34.
32                                  Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

reachability and edge predicates and (2) our reachability relation is reﬂexive, whereas Dong and Su
[1995] consider an irreﬂexive transitive closure relation. The direct update formulas provide a
canonical form of the reachability relation in the new state (e.g., P ⇔ (. . .)) based on the reach-
ability relation in the old state (e.g., (. . .) ⇔ Q[P0 ], where Q[R] is a ﬁrst-order formula over R).
Finally, we exploit the fact that both unlinkDAG and linkDAG relate two neighboring states: a state
in which the heap graph has exactly one fewer edges and a state in which the heap graph has
exactly one extra edge. Therefore, for each of the operations, we can also use the indirect update of
the reachability relation: TC_G_PLUS_DELTA and TC_G_MINUS_DELTA for UNLINKF and LINKF , resp.
   Remarkably, the formulation in TC_G_MINUS_DELTA is more complex than in TC_G_PLUS_DELTA.
This is due to the problem of recovering reachability after destructive updates (cf. Fig. 3). The
formal justiﬁcations for both formulations are given in [Dong and Su 1995].
   Since the reachability update formulas described above are deﬁned for DAGs, the assertions
in updateDAG ensure soundness of our technique for ﬁeld updates. The ﬁrst assertion checks that
the heap graph represented by g is acyclic before the ﬁrst operation, unlinkDAG . The second asser-
tion checks that the acyclic invariant is preserved after the second operation, linkDAG .

Appendix B PRECISE UPDATE FORMULAS FOR THE REACHABILITY QUERY IN
           0–1-PATH STRUCTURES
In this section, we present the general encoding of ﬁeld updates for ZOPGs, as introduced in Sec. 4.
We assume that the reader understand the previous case of DAGs discussed in App. A; similarly, our
goal now is to rewrite operations of the form from.f := to in such a way that would introduce
precise update formulas to the veriﬁer, except this time we are interested in the auxiliary DEP
relation for ZOPGs (and not P). As before, we denote the footprint of the method enclosing this ﬁeld
update as g. We assume that this methods implementation and speciﬁcation mentions reference
ﬁelds from the set F ; in particular, f ∈ F .
define updateZOPG fF (g : Zopg, from: Node, to: Node) {
     // state 1
     if ( to != from.f ) {
      if ( from.f != null ) {
        assert NO_ALT_PATHS_VIA_EDGE(snapF (g), from, to)
         unlinkZOPG fF (g , from)
      } // state 2
      if ( to != null ) {
         linkZOPG fF (g , from, to)
         assert NO_ALT_PATHS_VIA_EDGE(snapF (g), from, to)
}} // state 3 }
  The assertions in the code above are the main diﬀerence from the DAG case so far. The macro
used in these assertions directly corresponds to the (21).

       NO_ALT_PATHS_VIA_EDGE(д, α, β) ..⇐⇒ ∀x, y • P̂(д, x, α) ∧ P̂(д, β, y) =⇒ ¬P̂(д, α, β)




                                                                         2019-08-19 00:46. Page 32 of 1–34.
Modular Verification of Heap Reachability Properties in Separation Logic                                   33

method unlinkZOPG fF (g : Graph, node: Node)
  requires MEMORY_SPECSfF (g, node)
  requires node ∈ g ∧ f ∈ F ∧ node.f , null
  ensures MEMORY_SPECSF (g, node)f
  ensures node.f = null
                Ó                                          
  ensures           e∈F , e,f old(node.e) , old(node.f )       =⇒ ZOPG_UNLINKF (g, node, old(node.f ))


method linkZOPG fF (g : Graph, from: Node, to: Node)
  requires MEMORY_SPECSfF (g, from)
  requires from ∈ g ∧ f ∈ F ∧ from.f = null ∧ to , null
  ensures MEMORY_SPECSF (g, from)f
  ensures from.f = to
                Ó                                
  ensures           e∈F , e,f old(from.e) , to       =⇒ ZOPG_LINKF (g, from, to)


              ZOPG_LINKF (g, α, β) ..⇐⇒ G_PLUS_DELTA(old(snapF (g)), snapF (g), α, β)∧
                                            DEP_G_MINUS_DELTA(old(snapF (g)), snapF (g), α, β)∧
                                            DEP_G_PLUS_DELTA(old(snapF (g)), snapF (g), α, β),
           ZOPG_UNLINKF (g, α, β) ..⇐⇒ G_MINUS_DELTA(snapF (g), old(snapF (g)), α, β)∧
                                            DEP_G_MINUS_DELTA(snapF (g), old(snapF (g)), α, β)∧
                                            DEP_G_PLUS_DELTA(snapF (g), old(snapF (g)), α, β),
DEP_G_MINUS_DELTA(д, G, α, β) ..⇐⇒ ∀x, y, u, v • DEP           b(G, x, y, u, v) ∧
                                                 b(д, x, y) == DEP
                                                                 b(G, x, y, α, β),
                                                               ¬DEP
                               .
                               .
  DEP_G_PLUS_DELTA(д, G, α, β) ⇐⇒ α , β ∧ ∀x, y, u, v • u , v ∧ x , y =⇒
                                  
                                    b(G, x, y, u, v) == DEP
                                    DEP                   b(д, x, y, u, v) ∨
                                                                     (x = u = α ∧ y = v = β) ∨
                                                                                                             
                                                                  ∃w, z • Ψ(д, α, β, x, y, u, v, w, z) ∨
                                                                                                               
                                                                  ∃u ′, v ′ • Ψ(д, α, β, x, y, u ′, v ′, u, v) ∨
                                                                                                                
                                            u = α ∧ v = β ∧ ∃u ′, v ′, w, z • Ψ(д, α, β, x, y, u ′, v ′, w, z) ,
                                                                                  
         Ψ(д, α, β, x, y, U , V , w, z) ..⇐⇒ ∀u ′′, v ′′ • ¬DEP
                                                            b(д, x, y, u ′′, v ′′) ∧
                                                                                               
                                             b(д, x, α, u, v) ∧ x , α ∨ x = u = α ∧ v = β
                                             DEP
                                                                                               
                                             b(д, β, y, w, z) ∧ y , β ∨ α = w ∧ β = z = y .
                                             DEP

   The structure of ZOPG_UNLINKF and ZOPG_LINKF is conceptually the same as in their DAG coun-
terparts, UNLINKF and LINKF . The essential diﬀerence here are the update formulas which, for the
DEP relation, are more complex in the case of DEP_G_PLUS_DELTA than DEP_G_MINUS_DELTA. Our
DEP update formulas are adapted from [Dong and Su 1995] with few modiﬁcations, as explained
in Sec. 4.

2019-08-19 00:46. Page 33 of 1–34.
34                                       Arshavir Ter-Gabrielyan, Alexander J. Summers, and Peter Müller

Appendix C CONVERSION RULES FOR THE DEP RELATION
The auxiliary DEP relation enables precise reasoning about reachability in 0–1-path graphs. How-
ever, the formal deﬁnition of DEP 3 is beyond ﬁrst-order logic:
          ∀x, y, u, v • DEP(x, y, u, v) ..⇐⇒ E(u, v) ∧ u , v ∧
                                                           P(x, u) ∧ P(v, y) ∧                       (MetaDeﬁnitionDEP)
                                                           ¬TC[E \ {(u, v)}](x, y)
Here TC[R] is the reﬂexive, transitive closure of the binary relation R and E is the edge relation.
The last conjunct says that removing the edge (u, v) results in the destruction of the path x ..y.
  Our 0–1-path graph axiomatization includes a number of formulas—that can be derived from
(MetaDeﬁnitionDEP)—enabling conversions between reachability information in terms of P vs.
DEP. The core of this axiomatization consists of the following formulas:
              ∀x, y, u, v • P(x, y) ∧ x , y ⇐⇒ ∃u, v • DEP(x, y, u, v)                                               (PToDep)
              ∀x, y, u, v • DEP(x, y, u, v) =⇒ x , y ∧ u , v ∧ P(x, y) ∧ E(u, v)                                     (DepToP)
                     ∀x, y • DEP(x, y, x, y) ⇐⇒ E(x, y) ∧ x , y                                                 (SimplePath)
  Given the knowledge that the graph is a 0–1-path graph, we derive the remaining part of our
axiomatization:
           ∀x, y, n • ¬DEP(y, n, x, y)                                                                   (UnrollFromHead)
           ∀x, y, n • ¬DEP(n, x, x, y)                                                                     (UnrollFromTail)
           ∀x, y, v • x , y ∧ x , v∧
                          ¬P(v, x) ∧ E(x, v) ∧ P(v, y) =⇒ DEP(x, y, x, v)                       (HeadTriangleImposable)
           ∀x, y, u • x , y ∧ u , y∧
                          ¬P(y, u) ∧ P(x, u) ∧ E(u, y) =⇒ DEP(x, y, u, y)                         (TailTriangleImposable)
       ∀ν, n, µ, σ • ν , n ∧ n , σ ∧ ν , µ ∧ µ , σ ∧
                          E(ν, σ ) ∧ E(µ, σ ) =⇒ ¬DEP(ν, n, µ, σ )                                                 (Slingshot)
       ∀x, y, u, v • ¬P(x, u) ∨ ¬P(v, y) =⇒ ¬DEP(x, y, u, v)                                    (CoalignedEdgeAndPath)
   Some of the formulas above can be written more precisely by using additional quantiﬁcation, but
it seems that these more-precise formulas can only be applied in an inductive proof. For example,
we can strengthen the formula (HeadTriangleImposable) as follows:

         ∀x, y, v • x , y ∧ x , v ∧
                        (¬P(v, x) ∨ ∀β • P(x, β) ⇒ ¬DEP(v, y, x, β))
                         ∧ E(x, v) ∧ P(v, y)                                                  =⇒ DEP(x, y, x, v).
However, the above formula is diﬃcult to eﬃciently automate, because in its premise it would
require DEP information about a potentially unbounded number of quadruples, either of the form
(v, y, x, β) or (x, y, x, v).
  In practice, the imprecision of our 0–1-path graph axiomatization does not cause loss of reach-
ability information, as explained in Sec. 4.


3 Note that here we omit the ﬁrst parameter (i.e., the sub-heap) in all relation symbols as it is implicitly universally quantiﬁed

and the same in all formulas.

                                                                                             2019-08-19 00:46. Page 34 of 1–34.
