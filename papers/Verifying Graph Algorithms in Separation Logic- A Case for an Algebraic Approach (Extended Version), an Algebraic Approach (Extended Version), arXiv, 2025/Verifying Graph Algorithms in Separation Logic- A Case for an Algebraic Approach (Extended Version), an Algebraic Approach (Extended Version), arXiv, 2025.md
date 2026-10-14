                                        Verifying Graph Algorithms in Separation Logic: A Case for
                                        an Algebraic Approach (Extended Version)
                                        MARCOS GRANDURY, IMDEA Software Institute and Universidad Politécnica de Madrid, Spain
                                        ALEKSANDAR NANEVSKI, IMDEA Software Institute, Spain
                                        ALEXANDER GRYZLOV, IMDEA Software Institute, Spain
                                        Verifying graph algorithms has long been considered challenging in separation logic, mainly due to structural
                                        sharing between graph subcomponents. We show that these challenges can be effectively addressed by
arXiv:2501.13603v2 [cs.LO] 9 Jul 2025




                                        representing graphs as a partial commutative monoid (PCM), and by leveraging structure-preserving functions
                                        (PCM morphisms), including higher-order combinators.
                                           PCM morphisms are important because they generalize separation logic’s principle of local reasoning. While
                                        traditional framing isolates relevant portions of the heap only at the top level of a specification, morphisms
                                        enable contextual localization: they distribute over monoid operations to isolate relevant subgraphs, even
                                        when nested deeply within a specification.
                                           We demonstrate the morphisms’ effectiveness with novel and concise verifications of two canonical graph
                                        benchmarks: the Schorr-Waite graph marking algorithm and the union-find data structure.

                                        1   Introduction
                                        The defining property of separation logic [Ishtiaq and O’Hearn 2001; O’Hearn et al. 2001; Reynolds
                                        2002] is that a program’s specification tightly circumscribes the heap that the program accesses.
                                        Then framing, with the associated frame rule of inference, allows extending the specification with
                                        a disjoint set of pointers, deducing that the program doesn’t modify the extension. This makes
                                        the verification local [Calcagno et al. 2007], in the sense that it can focus on the relevant heap by
                                        framing out the unnecessary pointers.
                                           Another characteristic property of separation logic is that data structure’s layout in the heap is
                                        typically defined in relation to the structure’s contents, so that clients can reason about the contents
                                        and abstract away from the heap. A common example is the predicate list 𝛼 (𝑖, 𝑗) [Reynolds 2002]
                                        which holds of a heap iff that heap contains a singly-linked list between pointers 𝑖 and 𝑗, and the
                                        list’s contents corresponds to the inductive mathematical sequence 𝛼. This way, spatial (i.e., about
                                        state; involving heaps and pointers) reasoning gives rise to non-spatial (i.e., purely mathematical,
                                        state-free, about contents) reasoning for the clients. Fig. 1 illustrates a heap satisfying list 𝛼 (𝑖, 𝑗)
                                        when 𝛼 = [𝑎, 𝑏, 𝑐, 𝑑].
                                           The interaction of the above two properties imparts an important requirement on non-spatial
                                        reasoning. Since framing involves decomposition of heaps into disjoint subheaps, locality mandates
                                        that the mathematical structure representing contents also needs to support some form of disjoint
                                        decomposition. For example, in Fig. 1, the heap divides into two contiguous but disjoint parts,
                                        between pointers 𝑖 and 𝑘, and 𝑘 and 𝑗, respectively. Correspondingly, at the non-spatial level, the
                                        sequence [𝑎, 𝑏, 𝑐, 𝑑] laid out between the pointers 𝑖 and 𝑗, decomposes into subsequences [𝑎, 𝑏] and
                                        [𝑐, 𝑑], such that list [𝑎, 𝑏] (𝑖, 𝑘) and list [𝑐, 𝑑] (𝑘, 𝑗) hold of disjoint subheaps.
                                           While mathematical sequences (along with sets, mathematical trees, and many other structures)
                                        admit useful forms of decomposition, graphs generally don’t. Indeed, traversing a list or a tree
                                        reduces to traversing disjoint sublists or disjoint subtrees from different children of a common root;
                                        thus lists and trees naturally divide into disjoint subcomponents. But in a graph, the subgraphs
                                        reachable from the different children of a common node need not be disjoint, preventing an easy

                                        Authors’ Contact Information: Marcos Grandury, IMDEA Software Institute and Universidad Politécnica de Madrid, Madrid,
                                        Spain, marcos.grandury@imdea.org; Aleksandar Nanevski, IMDEA Software Institute, Madrid, Spain, aleks.nanevski@
                                        imdea.org; Alexander Gryzlov, IMDEA Software Institute, Madrid, Spain, aliaksandr.hryzlou@imdea.org.
2                                                        Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


                                   list [a, b] (i, k)          list [c, d] (k, j)

                                   i                      k                         j
                                        a           b          c          d

                                               list [a, b, c, d] (i, j)

Fig. 1. Spatial predicate list 𝛼 (𝑖, 𝑗) describes the layout of a linked list, whose contents is sequence 𝛼, between
pointers 𝑖 and 𝑗. Dividing the heap is matched by dividing 𝛼.


division. Even if a graph is divided into subgraphs with disjoint nodes, one must still somehow
keep track of the edges crossing the divide, in order to eventually reattach the pieces. Keeping track
of the crossing edges is simple in the case of lists, as there’s at most one such edge (e.g., 𝑘 in Fig. 1),
but graphs generally don’t exhibit such regularity.
   The lack of natural decomposition is why graphs have traditionally posed a challenge for
separation logic. For example, the Schorr-Waite graph marking algorithm [Schorr and Waite 1967]
is a well-known graph benchmark,1 that has been verified in separation logic early on by Yang
[2001a,b], and in many other logics and tools such as Isabelle [Mehta and Nipkow 2003] and
Dafny [Leino 2010]. While these proofs share conceptually similar mathematical notions (e.g.,
reachability in a graph by paths of unmarked nodes), they are formally encoded differently, with
Yang’s proof exhibiting by far the largest formalization overhead.2
   Notably, Yang’s proof avoids using graphs in non-spatial reasoning by refraining from explicit
mathematical graph parameters in spatial predicates. Instead, these predicates are parametrized by
decomposable abstractions—such as node sequences encoding traversal paths, marked/unmarked
node sets, the graph’s spanning tree, etc.—that indirectly approximate the graph’s structure. How-
ever, these proxies are interdependent: maintaining their mutual consistency and synchronization
with the heap-allocated graph forces the proof to perpetually alternate between spatial and non-
spatial reasoning, an entanglement that accounts for most of the proof’s complexity. Furthermore,
the absence of an explicit mathematical graph parameter precludes invoking formal graph-theoretic
lemmas, which in turn limits proof reuse and scalability.
   To reconcile spatial and non-spatial reasoning, we first require a mathematical representation of
graphs that inherently supports decomposition. This motivates our generalization to partial graphs,
which are directed graphs that admit dangling edges, i.e., edges whose source node belongs to the
graph, but whose sink node doesn’t. Partial graphs decompose into subgraphs with disjoint nodes,
where an edge crossing the divide becomes dangling in the subgraph containing the edge’s source.
We formalize this decomposition by casting partial graphs as partial commutative monoid (PCM). A
PCM is a structure (𝑈 , •, 𝑒) where •, pronounced “join”, is a partial commutative and associative
binary operation over 𝑈 , with unit 𝑒, which captures how graphs combine. If 𝛾 = 𝛾 1 • 𝛾 2 , we say
that 𝛾 decomposes or splits into 𝛾 1 and 𝛾 2 , or that 𝛾 1 and 𝛾 2 join into 𝛾.
   PCMs are central to separation logic, e.g., for defining heaps [Calcagno et al. 2007], permis-
sions [Bornat et al. 2005], histories [Sergey et al. 2015b], and meta theory [Dinsdale-Young et al.
2013]. Modern separation logics further support abstract states described by arbitrary PCMs [Jung
1 The Schorr-Waite algorithm, described in Section 4, marks the nodes reachable from a given root node in a directed graph.

Unlike recursive depth-first implementation, it uses an iterative approach that simulates the call stack through graph
mutations, temporarily modifying the graph’s pointer structure during traversal and restoring it upon completion.
2 Yang’s proof is described in some 40 pages of dense mathematical text. The proof in Isabelle is mechanized in about 400

lines, and the proof in Dafny is automated, aside from some 70 lines of annotations. Of course, Yang’s proof is the only one
to use framing, which allowed restricting the focus to connected graphs without sacrificing generality.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                       3


et al. 2015; Krishna et al. 2020; Nanevski et al. 2019]. However PCMs alone are insufficient for
graph verification: while they enable spatial reasoning over diverse notions of state, effective graph
verification requires a mechanism to localize non-spatial graph proofs.
   We address this gap with the three novel contributions of this paper: (1) leveraging PCM mor-
phisms in graph reasoning, (2) utilizing higher-order morphisms (i.e., combinators), leading to (3)
new proofs of Schorr-Waite and of another graph benchmark—the union-find data structure [Char-
guéraud and Pottier 2019; Krishnaswami 2011; Wang et al. 2019]. The latter is sketched in Section 7
to illustrate the generality of the approach, but is detailed in the appendix.
   Leveraging morphisms in graph reasoning. Given PCMs 𝐴 and 𝐵, the function 𝑓 : 𝐴 → 𝐵 is
a PCM morphism if the following equations hold.3
                                                       𝑓 𝑒𝐴 = 𝑒 𝐵                                                       (1)
                                              𝑓 (𝛾 1 •𝐴 𝛾 2 ) = 𝑓 𝛾 1 •𝐵 𝑓 𝛾 2                                          (2)
Focusing on equation (2), it says that 𝑓 distributes over the join operation of the domain PCM and
determines the following two ways in which morphisms apply to verification.
   First, morphisms mediate between PCMs, as the join operation of 𝐴 is mapped to the join opera-
tion of 𝐵. We will use morphisms between various PCMs in this paper, but an important example is
to morph the PCM of graphs to the PCM of propositions of separation logic (equivalently, to the
PCM of sets of heaps). Connecting graphs to sets of heaps allows a suitable heap modification to be
abstracted as a modification of the graph, thereby elevating low-level separation logic reasoning
about pointers into higher-level reasoning about graphs. For example, if a node in a graph is repre-
sented as a heap storing the node’s adjacency list, mutating the pointers in this heap corresponds
at the graph level to modifying the node’s edges.
   Second, continuing with morphisms over graphs specifically, the value of 𝑓 over a graph de-
composed into components (𝛾 1 and 𝛾 2 in equation (2)) can be computed by applying 𝑓 to 𝛾 1 and 𝛾 2
independently and joining the results. During verification, the left-to-right direction of (2) local-
izes reasoning to the modified subgraph (say, 𝛾 1 ), while the right-to-left direction automatically
propagates and reattaches 𝛾 2 . This allows morphisms to serve an analogous localizing role to
framing in separation logic, but with two distinctions. The obvious one is that framing decomposes
heaps, whereas morphisms decompose mathematical graphs (spatial vs. non-spatial reasoning).
More importantly, framing operates only at the top level of specifications, whereas morphisms
localize deeply inside a context: equation (2) can rewrite within arbitrary context 𝐼 (−) to transform
𝐼 (𝑓 (𝛾 1 • 𝛾 2 )) into 𝐼 (𝑓 𝛾 1 • 𝑓 𝛾 2 ) and allow 𝑓 𝛾 1 and 𝑓 𝛾 2 to be manipulated independently inside 𝐼 (−).
The latter is the essential feature that differentiates non-spatial from spatial reasoning (where
top-level framing suffices), and we shall use it to enable and streamline graph proofs.
   As an illustration of morphisms, consider filtering a graph to obtain a subgraph containing only
the nodes with a specific property. Filtering differs from taking a subgraph in standard graph theory,
in that the filtered subgraph retains—as dangling—the edges into the part avoided by the filter.
This enables reattaching the two parts later on, after either has been processed. Clearly, to filter a
composite graph it suffices to filter the components and join the results, making filtering a PCM
morphism on partial graphs.
   While not all useful graph abstractions are morphisms, those that aren’t can still usefully interact
with morphisms. The canonical example of such global notions is reachability between nodes in
a graph [Krishna et al. 2020]. In verification, reachability often needs to be restricted to paths
traversing only specific (e.g., unmarked) nodes. While one could implement this restriction by
3We only consider morphisms that distribute unconditionally. Partial morphisms, which distribute only if a certain condition

on 𝛾 1 and 𝛾 2 is satisfied, are useful and have been developed to an extent by Farka et al. [2021].
4                                                Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


parametrizing reachability with admissible node sets (e.g., as done by Leino [2010]), a simpler
solution in the presence of morphisms is to evaluate the global reachability predicate on dynamically
filtered subgraphs—effectively composing reachability with filtering. This compositional approach
scales naturally, enabling us to express complex specifications (like Schorr-Waite’s) by combining
elementary graph operations from a minimal core vocabulary.
  Higher-order combinators. In the presence of morphisms, the specifications can utilize still
higher levels of abstraction. Our second contribution notes that useful graph transformations
are encodable as instances of a higher-order combinator (like map over sequences in functional
programming), itself a PCM morphism on partial graphs. Morphisms thus relate different levels of
the abstraction stack that has heaps at the bottom, and localize the reasoning across all levels.
   New proofs of Schorr-Waite and union-find. The main challenge in these proofs is estab-
lishing the invariance of complex global properties, which we address precisely using contextual
localization, morphisms and combinators. Based on these abstractions, we also develop a generic
theory of partial graphs, which reduces example-specific reasoning and yields conceptually simple
and concise proofs. The entire development (graph theory, Schorr-Waite, union-find) is mechanized
in Hoare Type Theory [HTT 2010; Nanevski et al. 2006, 2008, 2010], a Coq library for separation
logic reasoning via types, with the component sizes summarized below [Grandury et al. 2025a].
                                                                lines of specification
                                lines of proof
                                                     (definitions, annotations, notation, code)
      Graph-theory library          2070                                 1738
         Schorr-Waite               110                                   111
          Union-find                 49                                   46
   Finally, we note that working with morphisms imparts a distinct algebraic character to specifica-
tions and proofs in this paper. While our reasoning spans both spatial and non-spatial domains, the
bulk of the effort is on the non-spatial side, where decomposition is governed by the PCM operation
• rather than the separation logic’s characteristic spatial connective ∗. This shift manifests in
specifications: assertions use ∗ sparingly as decomposition occurs primarily via • at the abstract
graph level. It’s this prioritization of the PCM structure and morphisms over traditional spatial
decomposition that justifies the term ”algebraic” in the paper’s title.
   We adopt the classical separation logic formulation from O’Hearn et al. [2001], Yang’s disserta-
tion [2001b] and Reynolds [2002], whose inference rules (e.g., frame rule, consequence, etc.) are
standard and thus elided here. However, to enable the interleaving of heap-level assertions with
graph-theoretic transformations, we depart somewhat from that work by allowing the assertions
to embed unrestricted mathematical formulas, including direct applications of morphisms.
   This is an extended version of an ICFP 2025 paper [Grandury et al. 2025b], which it extends with
appendices.

2   Background
To pinpoint the patterns of separation logic that inform our approach to graphs, we consider the
following program for computing the length of a singly-linked list headed at the pointer 𝑖.
                 = 𝑛 := 0; 𝑗 := 𝑖; while 𝑗 ≠ null do 𝑗 := 𝑗 .next; 𝑛 := 𝑛 + 1 end while
               𝐿 b
To specify 𝐿, one must first describe how a singly-linked list is laid out in the heap. For that,
the proposition list 𝛼 (𝑖, 𝑗) from Section 1 is defined below to hold of a heap that stores a linked
list segment between pointers 𝑖 and 𝑗, whose contents is the mathematical sequence 𝛼. Follow-
ing Reynolds [2002], we overload • to denote attaching an element to a head or a tail of a sequence,
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                   5



        1.   {∃𝛼 𝛽. list 𝛼 (𝑖, 𝑗) ∗ list 𝛽 ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • 𝛽 ∧ 𝑗 ≠ null}
        2.   {∃𝛼 𝑏 𝛽 ′ . list 𝛼 (𝑖, 𝑗) ∗ list (𝑏 • 𝛽 ′ ) ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • (𝑏 • 𝛽 ′ )}
        3.   {∃𝛼 𝑏 𝛽 ′ 𝑘. list 𝛼 (𝑖, 𝑗) ∗ 𝑗 Z⇒ 𝑏, 𝑘 ∗ list 𝛽 ′ (𝑘, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • (𝑏 • 𝛽 ′ )}
        4.   𝑗 := 𝑗 .next;
        5.   {∃𝛼 𝑏 𝛽 ′ 𝑗 ′ . list 𝛼 (𝑖, 𝑗 ′ ) ∗ 𝑗 ′ Z⇒ 𝑏, 𝑗 ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • (𝑏 • 𝛽 ′ )}
        6.   {∃𝛼 𝑏 𝛽 ′ . list (𝛼 • 𝑏) (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = (𝛼 • 𝑏) • 𝛽 ′ }
        7. 𝑛 := 𝑛 + 1;
        8.   {∃𝛼 𝑏 𝛽 ′ . list (𝛼 • 𝑏) (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 + 1 ∧ 𝛼 0 = (𝛼 • 𝑏) • 𝛽 ′ }
        9.   {∃𝛼 𝑏 𝛽 ′ . list (𝛼 • 𝑏) (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #(𝛼 • 𝑏) ∧ 𝛼 0 = (𝛼 • 𝑏) • 𝛽 ′ }
      10.    {∃𝛼 ′ 𝛽 ′ . list 𝛼 ′ (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ′ ∧ 𝛼 0 = 𝛼 ′ • 𝛽 ′ }
Fig. 2. Proof outline that the loop body of the length-computing program 𝐿 preserves the loop invariant 𝐼 .


and concatenating two sequences.
                                      list [] (𝑖, 𝑗) b
                                                     = emp ∧ 𝑖 = 𝑗
                               list (𝑎 • 𝛼) (𝑖, 𝑗) b
                                                   = ∃𝑘. 𝑖 Z⇒ 𝑎, 𝑘 ∗ list 𝛼 (𝑘, 𝑗)
The definition is inductive in 𝛼 and says: (1) The empty sequence [] is stored in a heap between
pointers 𝑖 and 𝑗 iff the heap is empty and 𝑖 = 𝑗; (2) The sequence 𝑎 • 𝛼 is stored in the heap between
pointers 𝑖 and 𝑗 iff 𝑖 points to a list node storing 𝑎 in the value field, and some pointer 𝑘 in the next
field, so that 𝛼 is then stored between 𝑘 and 𝑗 in a heap segment disjoint from 𝑖.
   Here emp, Z⇒ and ∗ are the spatial propositional connectives of separation logic: emp holds of a
heap iff the heap is empty; 𝑖 Z⇒ 𝑣 0, . . . , 𝑣𝑛 holds of a heap that contains only the pointers 𝑖, . . . , 𝑖 + 𝑛
storing the values 𝑣 0, . . . , 𝑣𝑛 , respectively; the separating conjunction 𝑃 ∗ 𝑄 holds of a heap that
can be divided into two disjoint subheaps of which 𝑃 and 𝑄 hold respectively. Separation logic
propositions form a PCM with ∗ as the commutative/associative operation, and emp its unit.
   The following Hoare triple then applies the sequence length function #(−) to say that, upon 𝐿’s
termination, the contents 𝛼 0 of the initial null-terminated list is unchanged, but its length #𝛼 0 is
deposited into the variable 𝑛.
                                {list 𝛼 0 (𝑖, null)} 𝐿 {list 𝛼 0 (𝑖, null) ∧ 𝑛 = #𝛼 0 }
We next outline the part of the proof for this Hoare triple that examines the loop body in 𝐿,
highlighting three key high-level aspects that we later adapt to graphs.
   Dangling pointers. The first aspect is that separation logic inherently relies on dangling pointers
to capture computations’ intermediate states. For example, the loop invariant for 𝐿 is
                         = ∃𝛼 𝛽. list 𝛼 (𝑖, 𝑗) ∗ list 𝛽 ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • 𝛽
                       𝐼 b
stating that the original sequence 𝛼 0 divides into 𝛼 (processed subsequence) and 𝛽 (remaining
subsequence), with 𝑛 tracking 𝛼’s length (progress computed so far). Importantly, pointer 𝑗 connects
𝛼’s tail to 𝛽’s head, making it dangling for 𝛼 since it references memory outside of 𝛼’s heap.
  Spatial distributivity. The second aspect is that the list predicate distributes over •, in the
sense of the following equivalence, already illustrated in Fig. 1.
                             list (𝛼 • 𝛽) (𝑖, 𝑗) ⇐⇒ ∃𝑘. list 𝛼 (𝑖, 𝑘) ∗ list 𝛽 (𝑘, 𝑗)                                (3)
6                                                Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


Equation (3) is clearly related to the distributivity of morphisms (2), even though sequences don’t
form a PCM as concatenation isn’t commutative. Nonetheless, the equation underscores that
distributivity, in one form or another, is a crucial notion in separation logic. It’s typical use in
separation logic is to transfer ownership of pointers between heaps; in the case of 𝐿, to redistribute
list so that the currently counted element, pointed to by 𝑗, is moved in assertions from 𝛽 to 𝛼.
    To illustrate, we review the proof in Fig 2 that 𝐼 is the loop invariant for 𝐿. Line 1 conjoins 𝐼 with
the loop condition 𝑗 ≠ null, to indicate that the execution is within the loop. Line 2 derives that 𝛽
is non-empty, hence of the form 𝑏 • 𝛽 ′ , as otherwise 𝑗 would have been null by the definition of
list. Line 3 shows the first use of distributivity to detach 𝑏 from the head of 𝛽. Line 4 mutates 𝑗 into
𝑗 .next, which is reflected in line 5, where a fresh variable 𝑗 ′ names the value of 𝑗 before the mutation.
This line derives by the standard inference rules for pointer mutation and framing [Reynolds 2002].
Line 6 shows the second use of distributivity to attach 𝑏 to the tail of 𝛼; it also reassociates the
concatenations in 𝛼 0 correspondingly. Line 7 increments 𝑛, which is reflected in lines 8 and 9.
Finally, line 10 re-establishes 𝐼 for the updated values of 𝑗 and 𝑛.
  Non-spatial distributivity. The third aspect is that the distribution over • is important for the
non-spatial parts of the proof as well. In particular, transitioning from line 8 to line 9 requires that
the length function distributes over •; specifically, that #(𝛼 • 𝑏) = #𝛼 + 1, or more generally, that
                                           #(𝛼 • 𝛽) = #𝛼 + #𝛽
to associate the new value of 𝑛 to the length of the new processed sequence 𝛼 ′ . The transformation
occurs in the context 𝑛 = (−) in lines 8–9, illustrating a simple case of contextual localization.
   While standard treatments of separation logic rely on non-spatial distributivity only implicitly,
graph verification requires that it be made explicit and central. This is because graph specifications
commonly compose morphisms, in turn making contextual localization essential for effective proofs.
By bringing these algebraic foundations—distributivity and morphisms—to the foreground, our
approach allows them to be systematically leveraged in verification.

3   Partial Graphs
   Dangling edges. The example in Section 2 shows how dangling pointers link disjoint list segments
to specify intermediate computation states. Similarly, specifying graph algorithms requires dangling
edges to connect disjoint parts of a graph. However, unlike lists, which have a single dangling
pointer, graphs generally have multiple dangling edges bridging the divide (Fig 3). To parallel
Section 2, where the dangling pointer 𝑗 was treated as a parameter of list, one might consider
grouping the dangling edges into a set that parametrizes the predicate graph, the graph analogue
to list. Bornat et al. [2004] explored this approach, but it resulted in an unsatisfactory definition, as
the resulting predicate relied on a program-specific traversal order in addition to the graph itself.
   We instead embed dangling edges directly into the graph representation, yielding the partial
graphs informally introduced in Section 1. Specifically, we choose a graph representation where
each node is associated with its adjacency list, but we allow for the possibility that a node in the
adjacency list need not be present in the graph itself. More formally, a partial graph (or simply graph)
of type 𝑇 is a partial finite map on nodes (isomorphic to natural numbers), that, if defined on a node
𝑥, maps 𝑥 to a pair consisting of a value of type 𝑇 (𝑥’s contents, value, or mark) and the sequence of
nodes adjacent to 𝑥 (𝑥’s immediate successors, adjacency list/sequence, children), with the proviso
that the map is undefined on the node null (i.e. 0).
                                              = node ⇀fin 𝑇 × seq node
                              partial-graph 𝑇 b
  The domain of a map is the finite subset of the type node on which the map is defined. A graph
contains an edge from 𝑥 to 𝑦 if 𝑦 appears among the children of 𝑥 in the map. An edge from 𝑥 to 𝑦 is
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)     7


                                          γ1                   b             γ2
                                                           O

                                            a X                         O   c

                                                           O
                                                               d

Fig. 3. Graph decomposition. Node 𝑎 has mark X , and nodes 𝑏, 𝑐, 𝑑 have mark O . Graph 𝛾 1 has dangling
edges from 𝑎 to 𝑏 and 𝑐; graph 𝛾 2 has a dangling edge from 𝑑 to 𝑎.


dangling if 𝑦 isn’t in the map’s domain. We write binary-graph 𝑇 for the subtype of partial-graph 𝑇
where the adjacency list of each node has exactly two elements (left/right child), with the element
set to null if the corresponding child doesn’t exist. Notation 𝑥 ↦→ (𝑣, 𝛼) denotes the singleton graph,
comprising just the node 𝑥, with mark 𝑣 and adjacency list 𝛼. The notation simplifies to 𝑥 ↦→ 𝛼
when 𝑇 is the unit type, as then the mark 𝑣 isn’t important.
   For example, the graph 𝛾 1 in Fig. 3 consists of a single node 𝑎 with contents X , and adjacency list
[𝑎, 𝑏, 𝑐], capturing that 𝑎 has edges to itself, and to nodes 𝑏 and 𝑐. The latter edges are dangling, as
𝑏 and 𝑐 are outside of 𝛾 1 . In our notation, 𝛾 1 = 𝑎 ↦→ ( X , [𝑎, 𝑏, 𝑐]).
    Spatial distributivity. The definition also directly leads to a notion of graph (de)composition.
To see this, notice that finite maps admit the operation of disjoint union which combines the maps
𝛾 1 and 𝛾 2 , but only if 𝛾 1 and 𝛾 2 have disjoint domains.
                                         
                                           𝛾1 ∪ 𝛾2      if dom 𝛾 1 ∩ dom 𝛾 2 = ∅
                              𝛾1 • 𝛾2 b=
                                            undefined otherwise
The operation is denoted • to draw the analogy with consing/concatenating in the case of sequences,
and also because • is partial, commutative and associative, meaning that graphs with • form a PCM.
The unit 𝑒 is the empty graph, i.e. the everywhere-undefined map.
   For example, the full graph in Fig. 3 is a composition 𝛾 1 • 𝛾 2 , where the subgraph 𝛾 1 has already
been described, and 𝛾 2 = 𝑏 ↦→ ( O, []) • 𝑐 ↦→ ( O, [𝑏, 𝑑]) • 𝑑 ↦→ ( O, [𝑎]). The representation captures,
among other properties, that 𝛾 2 has a node 𝑑 with a dangling edge to 𝑎. However, the composite
graph 𝛾 1 • 𝛾 2 has no edges dangling.
   Similarly to list, we can now define the predicate graph that defines how a graph is laid out in the
heap. This can be achieved in several different ways, optimizing for the structure of the graphs of
interest. We will conflate nodes with pointers and, for general partial graphs, lay out the adjacency
list of each node as a linked list in the heap.
                                       graph 𝑒 b
                                               = emp
                     graph (𝑥 ↦→ (𝑣, 𝛼) • 𝛾) b
                                             = ∃𝑖. 𝑥 Z⇒ 𝑣, 𝑖 ∗ list 𝛼 𝑖 null ∗ graph 𝛾
For binary graphs, however, a simpler representation avoids linking altogether. Because adjacency
lists have exactly two children, a node 𝑥 can be represented as a heap with three cells: the pointer
𝑥 storing the mark 𝑣, with the subsequent pointers 𝑥 + 1 and 𝑥 + 2 pointing to 𝑥’s children.
                                                  graph 𝑒 b
                                                          = emp
                            graph (𝑥 ↦→ (𝑣, [𝑙, 𝑟 ]) • 𝛾) b
                                                          = 𝑥 Z⇒ 𝑣, 𝑙, 𝑟 ∗ graph 𝛾
The following equation (4) characterizes both definitions of graph as PCM morphisms from partial
graphs to separation logic propositions. This lifts heap framing and separation logic reasoning to
8                                                          Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


graphs, much like list did for sequences with equation (3).

                                  graph (𝛾 1 • 𝛾 2 ) ⇐⇒ graph 𝛾 1 ∗ graph 𝛾 2                                      (4)

   To streamline the presentation, in the remainder of the paper we focus on binary graphs. The
simpler definition of graph will let us concentrate on non-spatial reasoning, where partial graphs
interact with PCMs beyond separation logic propositions, and where contextual localization requires
the use of morphisms. We consider the basics of this interaction next.
   Non-spatial distributivity. We first introduce some common notation and write: nodes 𝛾
instead of dom 𝛾 for the set of nodes on which 𝛾 is defined as a finite map, to emphasize that 𝛾 is a
graph; nodes0 𝛾 for the disjoint union {null} ∪· nodes 𝛾; and 𝛾 val 𝑥 and 𝛾 adj 𝑥, respectively, for the
contents and the adjacency list of the node 𝑥, so that 𝛾 𝑥 = (𝛾 val 𝑥, 𝛾 adj 𝑥).
   Given the graph 𝛾 and node 𝑥, we define 𝛾\𝑥 to be the graph that removes 𝑥 and its outgoing
edges from 𝛾, but keep the edges sinking into 𝑥 as newly dangling. We can characterize 𝛾\𝑥 as a
function as follows: 𝛾\𝑥 agrees with 𝛾 on all inputs except possibly 𝑥, on which 𝛾\𝑥 is undefined.
   We can now state the following two important equalities that expand (alt.: unfold) the graph 𝛾.

                                 𝛾 = (𝑥 ↦→ 𝛾 𝑥) • (𝛾\𝑥)                if 𝑥 ∈ nodes 𝛾                              (5)

                                 𝛾=         • 𝑥 ↦→ 𝛾 𝑥
                                        𝑥 ∈ nodes 𝛾
                                                                                                                   (6)

Equality (5) expands the graph 𝛾 around a specific node 𝑥, so that 𝑥’s contents and adjacency list
can be considered separately from the rest of the graph. This is analogous to how a pointer was
separated from list in Section 2, so that it could be transferred from one sequence to another. The
equality (6) iterates the expansion to characterize the graph in terms of the nodes.
  We also require the following functions and combinators over graphs.

                                =
                            𝛾/𝑆 b           •
                                      𝑥 ∈ 𝑆 ∩ nodes 𝛾
                                                      𝑥 ↦→ 𝛾 𝑥                            (filter)                 (7)


                             |𝛾 | b
                                  =         •
                                        𝑥 ∈ nodes 𝛾
                                                      𝑥 ↦→ 𝛾 adj 𝑥                      (erasure)                  (8)


                      map 𝑓 𝛾 b
                              =             •
                                        𝑥 ∈ nodes 𝛾
                                                      𝑥 ↦→ 𝑓 𝑥 (𝛾 𝑥)                      (map)                    (9)


                                  = 𝛾/𝛾 −1 {𝑣1,...,𝑣𝑚 }
                      𝛾/𝑣1,...,𝑣𝑛 b                                        (filter by contents)                  (10)
                                           val

Filtering takes a subset of the nodes of 𝛾 that are also in the set 𝑆, without modifying the nodes’
contents or adjacency lists. Erasure replaces the contents of each node with the singleton element
of unit type, thus eliding the contents from the notation. In particular |−| : partial-graph 𝑇 →
partial-graph unit. Map modifies the contents and the adjacency list of each node according to the
mapped function. If 𝑓 : 𝑛𝑜𝑑𝑒 → 𝑇1 × 𝑠𝑒𝑞 𝑛𝑜𝑑𝑒 → 𝑇2 × 𝑠𝑒𝑞 𝑛𝑜𝑑𝑒 then map 𝑓 : partial-graph 𝑇1 →
partial-graph 𝑇2 .4 Filtering by contents selects the nodes whose contents is one of 𝑣 1, . . . , 𝑣𝑛 , by
                         −1 {𝑣 , . . . , 𝑣 }. The latter is the inverse image of 𝛾 ; thus, the set of nodes
(plain) filtering over 𝛾 val      1       𝑛                                       val
that 𝛾 val maps into {𝑣 1, . . . , 𝑣𝑛 }.

4When mapping over binary graphs, we allow 𝑓 : 𝑛𝑜𝑑𝑒 → 𝑇 × (𝑛𝑜𝑑𝑒 × 𝑛𝑜𝑑𝑒 ) → 𝑇 × (𝑛𝑜𝑑𝑒 × 𝑛𝑜𝑑𝑒 ), as adjacency lists
                                                       1                    2
have exactly two elements. When 𝑇2 = unit, we elide 𝑇2 and allow 𝑓 : 𝑛𝑜𝑑𝑒 → 𝑇1 × (𝑛𝑜𝑑𝑒 × 𝑛𝑜𝑑𝑒 ) → 𝑛𝑜𝑑𝑒 × 𝑛𝑜𝑑𝑒.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                9


                                  𝛾1                           𝛾2                            𝛾1 • 𝛾2
                                                                                         𝑎 ↦→ ( X , [𝑎, 𝑏, 𝑐])
                                                          𝑏 ↦→ ( O, [])
                                                                                      • 𝑏 ↦→ ( O, [])
     (−)                 𝑎 ↦→ ( X , [𝑎, 𝑏, 𝑐])          • 𝑐 ↦→ ( O, [𝑏, 𝑑])
                                                                                      • 𝑐 ↦→ ( O, [𝑏, 𝑑])
                                                        • 𝑑 ↦→ ( O, [𝑎])
                                                                                      • 𝑑 ↦→ ( O, [𝑎])
     nodes (−)                  {𝑎}                         {𝑏, 𝑐, 𝑑 }                    {𝑎, 𝑏, 𝑐, 𝑑 }
     (−)/{𝑏 }                     𝑒                      𝑏 ↦→ ( O, [])                   𝑏 ↦→ ( O, [])
     (−)/𝑋               𝑎 ↦→ ( X , [𝑎, 𝑏, 𝑐])                  𝑒                     𝑎 ↦→ ( X , [𝑎, 𝑏, 𝑐])
                                                                                            𝑎 ↦→ [𝑎, 𝑏, 𝑐]
                                                            𝑏 ↦→ []
                                                                                         • 𝑏 ↦→ []
     |−|                     𝑎 ↦→ [𝑎, 𝑏, 𝑐]               • 𝑐 ↦→ [𝑏, 𝑑]
                                                                                         • 𝑐 ↦→ [𝑏, 𝑑]
                                                          • 𝑑 ↦→ [𝑎]
                                                                                         • 𝑑 ↦→ [𝑎]
                                                                                          𝑎 ↦→ ( O, [𝑏, 𝑐])
                                                           𝑏 ↦→ ( X , [])
                                                                                       • 𝑏 ↦→ ( X , [])
     map 𝑓 (−)              𝑎 ↦→ ( O, [𝑏, 𝑐])            • 𝑐 ↦→ ( X , [𝑑])
                                                                                       • 𝑐 ↦→ ( X , [𝑑])
                                                         • 𝑑 ↦→ ( X , [])
                                                                                       • 𝑑 ↦→ ( X , [])
     sinks (−)                 {𝑎, 𝑏, 𝑐}                    {𝑎, 𝑏, 𝑑 }                    {𝑎, 𝑏, 𝑐, 𝑑 }
     closed (−)                 false                        false                             true
     reach (−) 𝑎                 {𝑎}                            ∅                         {𝑎, 𝑏, 𝑐, 𝑑 }

Fig. 4. Action of graph abstractions on the graph from Fig. 3. The morphisms are illustrated at the top, and
the non-morphic (aka. global) properties at the bottom. In the top part, the mapped function 𝑓 exchanges O
and X and takes the tail of the adjacency list of each node: 𝑓 𝑥 (𝑣, 𝛼) b
                                                                        = (𝑣, tail 𝛼), where O = X and X = O .


   Sinks of a graph is the set of nodes in the range of 𝛾 (i.e., nodes that possess an incoming edge).
                                                     Ø
                                         sinks 𝛾 b
                                                 =        𝛾 adj                                   (11)
                                                           nodes 𝛾

We then say that closed 𝛾 holds iff 𝛾 contains no dangling edges. A plain (i.e., standard, non-partial)
graph is a partial graph that is closed.
                                                    = sinks 𝛾 ⊆ nodes0 𝛾
                                           closed 𝛾 b                                                            (12)
  The final graph primitive in our vocabulary is reach 𝛾 𝑥, which computes the set of nodes in 𝛾
reachable from the node 𝑥. The definition is recursive, unioning 𝑥 with the nodes reachable from
every child of 𝑥 via a path that avoids 𝑥. The definition is well-founded because the (finite) set of
graph’s nodes decreases with each recursive call, and thus eventually becomes empty.
                                   (           Ð
                                      {𝑥 } ∪         reach (𝛾\𝑥) if 𝑥 ∈ nodes 𝛾
                      reach 𝛾 𝑥 b
                                =            𝛾 adj 𝑥                                             (13)
                                      ∅                          otherwise
  Fig. 4 illustrates the definitions on the graph 𝛾 1 • 𝛾 2 from Fig. 3. Erasure, map, both filters, nodes
and sinks distribute over • (and are actually morphisms), while closed and reach don’t.
   Lemma 3.1 (Morphisms). Functions nodes, (−)/𝑆 , (−)/𝑣𝑖 , |−|, map 𝑓 , and sinks are morphisms
from the PCM of graphs, to an appropriate target PCM (sets with disjoint union for nodes, graphs for
(−)/𝑆 , (−)/𝑣𝑖 , |−|, map 𝑓 , and sets with plain union for sinks).
    (1) nodes (𝛾 1 • 𝛾 2 ) = nodes 𝛾 1 ∪· nodes 𝛾 2 and nodes 𝑒 = ∅
    (2) (𝛾 1 • 𝛾 2 )/𝑆 = 𝛾 1 /𝑆 • 𝛾 2 /𝑆 and 𝑒/𝑆 = 𝑒
    (3) (𝛾 1 • 𝛾 2 )/𝑣1,...,𝑣𝑛 = 𝛾 1 /𝑣1,...,𝑣𝑛 • 𝛾 2 /𝑣1,...,𝑣𝑛 and 𝑒/𝑣1,...,𝑣𝑛 = 𝑒
10                                                          Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


      (4) |𝛾 1 • 𝛾 2 | = |𝛾 1 | • |𝛾 2 | and |𝑒 | = 𝑒
      (5) map 𝑓 (𝛾 1 • 𝛾 2 ) = map 𝑓 𝛾 1 • map 𝑓 𝛾 2 and map 𝑓 𝑒 = 𝑒
      (6) sinks (𝛾 1 • 𝛾 2 ) = sinks 𝛾 1 ∪ sinks 𝛾 2 and sinks 𝑒 = ∅

     Lemma 3.2 (Filtering).

      (1) 𝛾/𝑆1 ∪· 𝑆2 = 𝛾/𝑆1 • 𝛾/𝑆2 and 𝛾/∅ = 𝑒
      (2) 𝛾/𝑣1,...,𝑣𝑚 ,𝑤1,...,𝑤𝑛 = 𝛾/𝑣1,...,𝑣𝑚 • 𝛾/𝑤1,...,𝑤𝑚 , for disjoint {𝑣𝑖 }, {𝑤 𝑗 }
      (3) 𝛾/𝑆1 ∩𝑆2 = 𝛾/𝑆1 /𝑆2
      (4) 𝛾/𝑣1,...,𝑣𝑚 /𝑤1,...,𝑤𝑛 = 𝑒, for disjoint {𝑣𝑖 }, {𝑤 𝑗 }

     Lemma 3.3 (Mapping). map 𝑓1 𝛾 = map 𝑓2 𝛾 iff ∀𝑥 ∈ nodes 𝛾 . 𝑓1 𝑥 (𝛾 𝑥) = 𝑓2 𝑥 (𝛾 𝑥).

     Lemma 3.4 (Reachability).

      (1) reach 𝛾 𝑥 = reach |𝛾 | 𝑥
      (2) if 𝑦 ∉ reach 𝛾 𝑥, then reach 𝛾 𝑥 = reach (𝛾\𝑦) 𝑥
      (3) if 𝑦 ∈ reach 𝛾 𝑥, then reach 𝛾 𝑥 = reach (𝛾\𝑦) 𝑥 ∪ reach 𝛾 𝑦

     Lemma 3.5 (Closure).

      (1) If closed 𝛾 then closed (𝛾/reach 𝛾 𝑥 ), for every 𝑥.
      (2) If closed (𝛾 1 • 𝛾 2 ), and 𝑥 ∈ nodes (𝛾 1 • 𝛾 2 ), and nodes 𝛾 1 = reach (𝛾 1 • 𝛾 2 ) 𝑥 (i.e., 𝛾 1 is the
          subgraph reachable from 𝑥), then closed 𝛾 1 , and 𝑥 ∈ nodes 𝛾 1 , and nodes 𝛾 1 = reach 𝛾 1 𝑥.

   We elide the proofs here (they are in our Coq graph library), and just comment on the intuition
behind each. Lemmas 3.1 and 3.2 hold because combinators iterate a node-local transformation
over a set of nodes. Lemma 3.3 holds because map applies the argument function only to nodes
in the graph. Lemma 3.4 (1) holds because reachability isn’t concerned with the contents of the
nodes. Lemma 3.4 (2) holds because a node 𝑦 that isn’t reachable from 𝑥 doesn’t influence the
reachability relation, and can thus be removed from the graph. Lemma 3.4 (3) holds because, given 𝑦
that’s reachable from 𝑥, another node 𝑧 is reachable from 𝑥 iff it’s reachable from 𝑦, or is otherwise
reachable from 𝑥 by a path avoiding 𝑦. Lemma 3.5 (1) restates in the notation of partial graphs the
well-known property that in a standard non-partial graph, the nodes reachable from some node 𝑥
form a connected subgraph. Lemma 3.5 (2) is a simple consequence of Lemma 3.5 (1).
   We close by illustrating how contextual localization helps prove that a global property (here,
closed) is preserved under graph modifications—a pattern used extensively in the Schorr-Waite and
union-find verifications (Sections 4 and 7). The idea is captured in the following lemma and proof.

  Lemma 3.6. Let 𝛾 be a binary graph such that closed 𝛾, and 𝑥 ∈ nodes 𝛾 and 𝑦 ∈ nodes0 𝛾. The
graph 𝛾 ′ obtained by modifying 𝑥’s child (left or right) to 𝑦, also satisfies closed 𝛾 ′ .

   Proof. Without loss of generality, we assume that it’s the left child of 𝑥 that’s modified. In other
words, we take 𝛾 = 𝑥 ↦→ (𝑣, [𝑥𝑙 , 𝑥𝑟 ]) • 𝛾\𝑥 and 𝛾 ′ = 𝑥 ↦→ (𝑣, [𝑦, 𝑥𝑟 ]) • 𝛾\𝑥, for some 𝑣, 𝑥𝑙 and 𝑥𝑟 .
   Having assumed closed 𝛾, we need to prove closed 𝛾 ′ ; that is sinks 𝛾 ′ ⊆ nodes0 𝛾 ′ . While closed
itself is a global property, the main components of its definition, sinks and nodes, are morphisms.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)        11


The proof rewrites within the context − ⊆ − to distribute the morphisms as follows.
    sinks 𝛾 ′ =    sinks (𝑥 ↦→ (𝑣, [𝑦, 𝑥𝑟 ]) • 𝛾\𝑥) =
              =    sinks (𝑥 ↦→ (𝑣, [𝑦, 𝑥𝑟 ]) ∪ sinks 𝛾\𝑥                     Distributivity of sinks
              =    {𝑦, 𝑥𝑟 } ∪ sinks 𝛾\𝑥                                      Definition of sinks
              ⊆    {𝑦} ∪ {𝑥𝑙 , 𝑥𝑟 } ∪ sinks 𝛾\𝑥
              =    {𝑦} ∪ sinks (𝑥 ↦→ (𝑣, [𝑥𝑙 , 𝑥𝑟 ]) ∪ sinks 𝛾\𝑥             Definition of sinks
              =    {𝑦} ∪ sinks (𝑥 ↦→ (𝑣, [𝑥𝑙 , 𝑥𝑟 ]) • 𝛾\𝑥)                  Distributivity of sinks
              =    {𝑦} ∪ sinks 𝛾
              ⊆    nodes0 𝛾                                                  By assumptions 𝑦 ∈ nodes0 𝛾
                                                                             and closed 𝛾 (i.e.
                                                                             sinks 𝛾 ⊆ nodes0 𝛾)
               =   {null} ∪· nodes (𝑥 ↦→ (𝑣, [𝑥𝑙 , 𝑥𝑟 ]) • 𝛾\𝑥)
               =   {null} ∪· nodes (𝑥 ↦→ (𝑣, [𝑥𝑙 , 𝑥𝑟 ])) ∪· nodes 𝛾\𝑥       Distributivity of nodes
               =   {null} ∪· {𝑥 } ∪· nodes 𝛾\𝑥                               Definition of nodes
               =   {null} ∪· nodes (𝑥 ↦→ (𝑣, [𝑦, 𝑥𝑟 ]) ∪· nodes 𝛾\𝑥          Definition of nodes
               =   nodes0 (𝑥 ↦→ (𝑣, [𝑦, 𝑥𝑟 ]) • 𝛾\𝑥)                         Distributivity of nodes
               =   nodes0 𝛾 ′
By distributing the morphisms, the proof separates the reasoning about the node 𝑥 from that about
the subgraph 𝛾\𝑥. While it manipulates the values of sinks and nodes at 𝑥 to relate sinks 𝛾 ′ and
nodes0 𝛾 ′ to sinks 𝛾 and nodes0 𝛾, respectively, it also exploits the fact that 𝛾 and 𝛾 ′ share the same
subgraph 𝛾\𝑥. By isolating the treatment of 𝑥 from the rest of the graph, the proof enacts a style of
reasoning that’s fundamentally local, albeit distinct from the typical notion of locality of separation
logic that’s achieved by framing. This alternative, contextual, form of locality arises not from eliding
the rest of the structure, but from explicitly factoring it through morphisms.                          □

4   Schorr-Waite Algorithm
The goal of a graph-marking algorithm is to traverse a graph starting from some root node 𝑟
and mark the reachable nodes. An obvious way to implement this functionality is as a recursive
function that traverses the graph in a depth-first, left-to-right manner. However, as graph marking
is typically employed in garbage collection—when space is sparse—recursive implementation isn’t
optimal, as it uses up space on the stack to keep track of the recursive calls and execute backtracking.
The idea of Schorr-Waite’s algorithm is that the information about backtracking can be maintained
within the graph itself, while the graph is traversed iteratively in a loop.
   We consider the variant of Schorr-Waite that operates over binary graphs. We also record the
node’s status in the traversal by setting the mark to: O if the node is unmarked, i.e., the traversal
hasn’t encountered the node; L if the node has been traversed once towards the left subgraph; R if the
traversal of the left subgraph has completed, and the traversal of the right subgraph began; X if both
subgraphs have been traversed. Thus, we proceed to use graphs of type binary-graph {O, L, R, X }.
   Along with modifying the nodes’ marks, the edges of the graph are modified during traversal to
keep the backtracking information. This is illustrated in Fig. 5, where 𝛾 0 is the original unmarked
graph, and 𝛾 is an intermediate graph halfway through the execution. The figure illustrates the
traversal that started at 𝑛 1 , proceeded to 𝑛 2 , fully marked the left subgraph rooted at 𝑛 2 , reached the
node 𝑝 = 𝑛 5 and is just about to traverse the left subgraph of 𝑝 starting from the node 𝑡 = 𝑛 6 . The
variables 𝑡 (tip) and 𝑝 (predecessor) are modified as the traversal advances. The idea of Schorr-Waite
is that once the traversal has obtained the node 𝑡 from which to proceed, the corresponding edge
(or pointer) from 𝑝 to 𝑡 can temporarily be repurposed and redirected towards 𝑝’s predecessor
in the traversal (here 𝑛 2 ). As similar repurposing has been carried out for 𝑛 2 and 𝑛 1 when they
12                                                      Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


                                                                           null

            γ0 :                     O n1                   γ:                        L

                            O n2                O n9                        R               O

                   O n3              O n5                         X                   L p

                            O n6                O n8                        O t             O

                   O n4              O n7                         X                   O

Fig. 5. The unmarked graph 𝛾 0 with nodes 𝑛 1, ..., 𝑛 9 , named in depth-first, left-to-right traversal order. The
partially marked graph 𝛾 shows an intermediate state, with 𝑡 the current tip node, and 𝑝 its predecessor. The
dashed line encloses the traversal stack (top = 𝑝), which contains exactly the nodes marked L or R. A node
marked L (resp. R) has its left (resp. right) edge redirected to the predecessor through which it was reached.
This inverts the edges on the stack: the path 𝑛 1 → 𝑛 2 → 𝑛 5 in 𝛾 0 becomes 𝑛 5 → 𝑛 2 → 𝑛 1 in 𝛾.


                        p                                                                           p
                              PUSH                      SWING                     POP
                   O    t                       L   p                  R      p                 X   t

                                            t                                     t

Fig. 6. Operations PUSH, SWING, and POP on the pivot node (unshaded), coordinate the marking of the
pivot with the stack (dashed line) and with edge inversion. SWING and POP require that 𝑡 is marked or null.


were first encountered, this explicitly inverts in 𝛾 the path encompassing the sequence of nodes
𝛼 = [𝑛 1, 𝑛 2, 𝑛 5 ] in 𝛾 0 (dashed line in Fig. 5). The sequence 𝛼 serves the same role as the call stack in
a recursive implementation, as it records the nodes whose subgraphs are currently being traversed,
and the relative order in which each node has been reached. We refer to 𝛼 as the stack, with 𝛼’s last
element (also stored in 𝑝) being the stack’s top. A node on the stack can be marked L or R, but not
O or X , as the latter signifies that the node’s traversal hasn’t started, or has finished, respectively.
Conversely, a node marked L or R must be on the stack. These properties constitute some of the
main invariants of the algorithm and are formalized in Section 5.
   Fig. 6 zooms onto the tip node 𝑡 (unshaded node, pivot) to illustrate how the traversal coordinates
the marking and edge redirection around 𝑡 with the modifications of 𝑡 and 𝑝 in three separate
operations: PUSH, SWING, and POP. When 𝑡 is first encountered, it’s unmarked. PUSH promptly
marks it L, and pushes it onto the stack (dashed line in Fig. 6) by redirecting its left edge towards 𝑝.
The traversal continues by advancing 𝑡 towards the left subgraph, and 𝑝 to what 𝑡 previously was.
Once the left subgraph is fully marked, SWING restores pivot’s left pointer, but keeps the pivot
enlinked onto the stack by using the pivot’s right pointer. The tip is swung to the right subgraph,
and the mark changed to R, to indicate that the left subgraph has been traversed, and we’re moving
to the right subgraph. Once the pivot’s right subgraph is traversed as well, POP sets the mark
to X and restores the right edge. This returns the edges of the pivot to their originals from the
initial graph, but also unlinks (i.e., pops) the pivot from the stack. Nodes stored into 𝑝 and 𝑡 are
correspondingly shifted up, and the marking cycle continues from the new top of the stack.
   Algorithm in Fig. 7 takes the root node 𝑟 from which the traversal begins, and starts by setting
the tip 𝑡 to 𝑟 , and 𝑝 to null. An invariant of the algorithm is that 𝑝 is always the top of the stack.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                                                        13

    t := r; p := null;
    if t = null then tm := true else tmp := t.m; tm := (tmp ̸= O) end if ;                                                         // is t marked?
    while p ̸= null ∨ ¬tm do
       if tm then
          pm := p.m;                                                                                                               // read p’s mark
          if pm = R then
             tmp := p.r; p.r := t; p.m := X ; t := p; p := tmp                                                                     // POP
          else
             tmp1 := p.r; tmp2 := p.l; p.r := tmp2 ; p.l := t; p.m := R; t := tmp1                                                 // SWING
          end if
       else
          tmp := t.l; t.l := p; t.m := L; p := t; t := tmp                                                                         // PUSH
       end if ;
       if t = null then tm := true else tmp := t.m; tm := (tmp ̸= O) end if                                                        // is t marked?
    end while

Fig. 7. Schorr-Waite algorithm. The algorithm follows the monadic style common to many separation logics,
strictly dividing stateful commands from pure expressions. This requires pointer-dependent conditions (in
if/while) to first dereference into variables, since expressions can’t contain commands. For example, tm is
assigned before and at the loop’s end to enable its use in the loop condition.


                  p                          p                          p                          p
P
                      tmp := t.l                    t.l := p                  t.m := L                    p := t                   t := tmp
U                                                                                                                            p                         p
              O   t                      O   t                      O   t                      L   t                     L                         L
S
H                                   tmp                        tmp                        tmp                       tmp                        t



S                     tmp1 := p.r            tmp2
W                     tmp2 := p.l                p.r := tmp2                   p.l := t                  p.m := R                  t := tmp1
I             L   p                      L   p                      L   p                      L   p                     R   p                     R   p
N
          t                          t              tmp1        t              tmp1        t             tmp1        t              tmp1                   t
G


                                             tmp                        tmp                        tmp                       tmp                       p
P                     tmp := p.r                    p.r := t                p.m := X                      t := p                   p := tmp
O             R   p                      R   p                      R   p                      X   p                     X   t                     X   t
P
                        t                           t                          t                         t


                                    Fig. 8. Details of the main operations of Schorr-Waite.




Thus, 𝑝 equals null if the stack is empty, otherwise 𝑝 is marked L or R, but never O or X . Next, 𝑡’s
marking status is computed into tm. In general, if 𝑡 is unmarked and non-null, then 𝑡 is encountered
for the first time. At each iteration, the algorithm mutates the graph—illustrated in Fig. 8—using:
(1) PUSH, if 𝑡 is unmarked and non-null, thus encountered for the first time, and can be pushed
onto the stack; (2) SWING, if 𝑡 is marked or null (encountered before), and 𝑝 isn’t marked R (thus,
is marked L) signifying that 𝑝’s left subgraph has been traversed; (3) POP, if 𝑡 is marked or null
and 𝑝 is marked R signifying that 𝑝’s right subgraph has been traversed. The algorithm terminates
when 𝑝 is null (the stack is empty) and 𝑡 is marked or null (there’s nothing to push onto the stack).
14                                                    Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov



               inv′ 𝛾 0 𝛾 𝛼 𝑡 𝑝 b
                                = uniq (null • 𝛼) ∧ 𝑝 = last (null • 𝛼) ∧ 𝑡 ∈ nodes0 𝛾 ∧                      (𝑎)
                                   closed 𝛾 ∧                                                                 (𝑏)
                                   nodes 𝛾/L,R = 𝛼 ∧                                                          (𝑐)
                                   inset 𝛼 𝛾 = |𝛾 | ∧                                                         (𝑑)
                                   restore 𝛼 𝑡 𝛾 = |𝛾 0 | ∧                                                   (𝑒)
                                                 Ð
                                   nodes 𝛾/O ⊆ (reach (𝛾/O ) ◦ 𝛾𝑟 ) ∪ reach (𝛾/O ) 𝑡                         (𝑓 )
                                                  𝛼
                                = ∃𝛼 . inv′ 𝛾 0 𝛾 𝛼 𝑡 𝑝
                  inv 𝛾 0 𝛾 𝑡 𝑝 b

Fig. 9. Main invariants of Schorr-Waite, formally. The parameter 𝛾 0 is the initial graph, 𝛾 is the current
partially marked graph, 𝛼, 𝑡 and 𝑝 are the current stack, tip and predecessor, respectively.



  The verification task is to prove that the graph obtained upon termination modifies the initial
unmarked graph as follows: (1) the nodes reachable from 𝑟 , and only those, are marked X , and (2)
the edges are restored to their initial versions.

5    Schorr-Waite’s Invariants
To formalize the above specification, the first step is to state the main invariants of Schorr-Waite
that relate the initial graph 𝛾 0 to the current graph 𝛾, the stack 𝛼, and the nodes 𝑡 and 𝑝. In this
formalization, we rely solely on combining graph abstractions from the small vocabulary introduced
in Section 3. This ensures that later proofs remain compatible with graph decomposition, and
depend only on general lemmas over this core vocabulary.
   The relations to be captured are the following, all observed in the example graphs from Fig. 5.
These invariants hold throughout the execution of Schorr-Waite, except inside the three main
operations, PUSH, SWING, and POP, when the invariants are temporarily invalidated, to be restored
by the time the operation terminates.
     (𝑎) The stack 𝛼 is a sequence of distinct nodes (i.e., each node is unique), also distinct from null,
          with 𝑝 the top of stack (i.e., 𝑝 is the last element of 𝛼, or null if 𝛼 is empty). The tip 𝑡, being
          a child of 𝑝, is a node in 𝛾, or null if the child doesn’t exist.
     (𝑏) The graph 𝛾 is closed, i.e., it has no dangling edges.
     (𝑐) The stack 𝛼 contains exactly the nodes that are partially marked (labeled L or R). Intuitively,
          this holds because 𝛼 implements the call stack, and thus only contains the nodes whose
          subtrees are being currently marked.
     (𝑑) The stack 𝛼 describes a path in 𝛾 that respects the markings, in the following sense: if a node
          in 𝛼 is marked L (resp. R), then its left (resp. right) child in 𝛾 is the node’s predecessor in the
          traversal, and thus the node’s predecessor in 𝛼. For example, in the graph 𝛾 in Fig. 5, the
          node 𝑛 5 is marked L and its left child 𝑛 2 is its predecessor in 𝛼. In other words, 𝛼 stores the
          nodes in the relative order in which they are reached.
     (𝑒) Reorienting the edges of the nodes in 𝛼 produces the original graph 𝛾 0 (modulo node marks).
     (𝑓 ) The unmarked nodes (labeled O ) are “to the right” of 𝛼 and 𝑡, because the algorithm
          implements a left-to-right traversal order. More precisely, each unmarked node is reachable,
          by an unmarked path, either from 𝑡 or from a right child of some node in 𝛼. For example, in
          the graph 𝛾 in Fig. 5, the nodes 𝑛 7, 𝑛 8, 𝑛 9 (unmarked) are “to the right” of 𝛼 and 𝑡, whereas
          the nodes 𝑛 3, 𝑛 4 (marked X ) are “to the left”.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                       15


   Fig. 9 presents the formal statements of the above invariants, which we proceed to explain. The
encoding of (𝑎) and (𝑏) in Fig. 9 is direct. The statement (𝑐) says that the stack 𝛼, viewed as a set
rather than a sequence, equals the set of nodes in 𝛾 that are marked L or R. Statement (𝑓 ) denotes
by 𝛾𝑟 𝑥 the right child of 𝑥 in 𝛾,5 and directly says that an unmarked node 𝑥 (i.e., 𝑥 ∈ nodes 𝛾/O ) is
reachable from 𝑡 by an unmarked path (𝑥 ∈ reach (𝛾/O ) 𝑡), or there exists  Ð a node 𝑦 ∈ 𝛼 such that 𝑥
is reachable from the right child of 𝑦, also by an unmarked path (𝑥 ∈ 𝛼 (reach (𝛾/O ) ◦ 𝛾𝑟 )). This
leaves us with the statements (𝑑) and (𝑒), which we discuss next.
   If one ignores for a moment the property of respecting the markings, then the English description
of (𝑑) and (𝑒) says that the stack 𝛼 is the contents of a linked list embedded in the graph 𝛾, and that
reversing the linkage of this list produces the original graph 𝛾 0 . Thus, one might consider following
the approach to linked lists described in Section 2, and attempt to relate 𝛼 with the heap layouts of
𝛾 and 𝛾 0 , by somehow relating list 𝛼 with graph 𝛾 0 and list (reverse 𝛼) with graph 𝛾.6 However, in
our setting there is a more direct option, that elides the detour through heaps, and relates 𝛼 to 𝛾
and 𝛾 0 by means of the following graph transformation.
   In particular, we first define the higher-order function if-mark that branches on the marking of
an individual node, to output a transformation of the node’s edges.
                               if-mark       :     (𝑛𝑜𝑑𝑒 → 𝑛𝑜𝑑𝑒) → 𝑛𝑜𝑑𝑒 →
                                                       {O, L, R, X } × (𝑛𝑜𝑑𝑒 × 𝑛𝑜𝑑𝑒) → 𝑛𝑜𝑑𝑒 × 𝑛𝑜𝑑𝑒
                                                   
                                                    [𝑓 𝑥, 𝑟 ]    if 𝑚 = L
                                                   
                                                   
             if-mark 𝑓 𝑥 (𝑚, [𝑙, 𝑟 ])        =
                                             b       [𝑙, 𝑓 𝑥]     if 𝑚 = R
                                                   
                                                    [𝑙, 𝑟 ]
                                                                 otherwise
The transformation that if-mark computes is guided by the argument function 𝑓 , itself mapping
nodes to nodes. Thus, supplying different values for 𝑓 produces different transformations, but
within the general pattern encoded by if-mark. In more detail, if-mark applies to a node 𝑥 of 𝛾, 𝑥’s
mark 𝑚 and children [𝑙, 𝑟 ] as follows. If 𝑚 is L (resp. R), then 𝑥’s left (resp. right) child is replaced
in the output by 𝑓 𝑥, while the right (resp. left) child is passed along unchanged. Otherwise, if 𝑥 is
marked O or X , its children are returned unmodified.
   We then apply the map combinator to if-mark in two different ways, to define the following two
functions that will help us formalize the invariants (𝑑) and (𝑒) in a uniform way.
                   inset : seq 𝑛𝑜𝑑𝑒 → binary-graph {O, L, R, X } → binary-graph unit
                                                                                                                         (14)
                        = map (if-mark (prev (null • 𝛼))) 𝛾
              inset 𝛼 𝛾 b
                 restore : 𝑛𝑜𝑑𝑒 → seq 𝑛𝑜𝑑𝑒 → binary-graph {O, L, R, X } → binary-graph unit
                                                                                                                         (15)
                        = map (if-mark (next (𝛼 • 𝑡))) 𝛾
          restore 𝛼 𝑡 𝛾 b
Here prev (null • 𝛼) is a function that takes a node 𝑥 and returns the predecessor of the first
occurrence of 𝑥 in (null • 𝛼) if 𝑥 ∈ 𝛼, or null if 𝑥 ∉ 𝛼. Similarly, next (𝛼 • 𝑡) 𝑥 is the successor of the
first occurrence of 𝑥 in (𝛼 • 𝑡) if 𝑥 ∈ 𝛼, or 𝑡 if 𝑥 ∉ 𝛼. For example, if 𝛼 is the sequence [𝑛 1, 𝑛 2, 𝑛 5 ],
then prev (null • 𝛼) 𝑛 2 = 𝑛 1 , prev (null • 𝛼) 𝑛 1 = null, next (𝛼 • 𝑡) 𝑛 2 = 𝑛 5 , and next (𝛼 • 𝑡) 𝑛 5 = 𝑡.
   From the definition, it follows that graphs inset 𝛼 𝛾 and restore 𝛼 𝑡 𝛾 modify the graph 𝛾 by
manipulating the edges related to the stack 𝛼, and otherwise erasing 𝛾’s marks. Specifically, inset 𝛼 𝛾
replaces the child (left/right, based on mark) of each node in 𝛼 with its predecessor in null • 𝛼. For 𝛼
to respect the markings, as required by the invariant (𝑑), this transformation must actually preserve
the graph. Thus, invariant (𝑑) is formally stated in Fig. 9 as inset 𝛼 𝛾 = |𝛾 |. Similarly, restore 𝛼 𝑡 𝛾
5 Dually, 𝛾 𝑥 is the left child of 𝑥, so that 𝛾
            𝑙                                   adj 𝑥 is the sequence [𝛾𝑙 𝑥, 𝛾𝑟 𝑥 ].
6 In fact, relating 𝛼 to the heap layouts of 𝛾 and 𝛾 via the list predicate is precisely the approach of Yang’s proof.
                                                       0
16                                                       Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


replaces the child (left/right, based on mark) of each node in 𝛼 with its successor in 𝛼 • 𝑡, thereby
inverting the path 𝛼 in 𝛾, and redirecting the appropriate child of 𝑝 towards 𝑡. Thus, invariant (𝑒) is
formally stated in Fig. 9 as restore 𝛼 𝑡 𝛾 = |𝛾 0 |.
  Example. Consider the graphs 𝛾 and 𝛾 0 from Fig. 5, taking 𝑝 = 𝑛 5 , 𝑡 = 𝑛 6 , and 𝛼 = [𝑛 1, 𝑛 2, 𝑛 5 ].
The following calculation illustrates that restore 𝛼 𝑡 𝛾 computes the erasure of 𝛾 0 .
             restore 𝛼 𝑡 𝛾 = map (if-mark (next (𝛼 • 𝑡))) 𝛾
                           =      𝑛 1 ↦→ if-mark (next (𝛼 • 𝑡)) 𝑛 1 ( L, [null, 𝑛 9 ])
                                • 𝑛 2 ↦→ if-mark (next (𝛼 • 𝑡)) 𝑛 2 ( R, [𝑛 3, 𝑛 1 ])
                                • 𝑛 5 ↦→ if-mark (next (𝛼 • 𝑡)) 𝑛 5 ( L, [𝑛 2, 𝑛 8 ])
                                • map (if-mark (next (𝛼 • 𝑡))) (𝛾\{𝑛 1, 𝑛 2, 𝑛 5 })
                           =      𝑛 1 ↦→ [next (𝛼 • 𝑡) 𝑛 1, 𝑛 9 ]
                                • 𝑛 2 ↦→ [𝑛 3, next (𝛼 • 𝑡) 𝑛 2 ]
                                • 𝑛 5 ↦→ [next (𝛼 • 𝑡) 𝑛 5, 𝑛 8 ]
                                • |𝛾\{𝑛 1, 𝑛 2, 𝑛 5 }|
                           = 𝑛 1 ↦→ [𝑛 2, 𝑛 9 ] • 𝑛 2 ↦→ [𝑛 3, 𝑛 5 ] • 𝑛 5 ↦→ [𝑡, 𝑛 8 ] • |𝛾\{𝑛 1, 𝑛 2, 𝑛 5 }|
                           = |𝛾 0 |
When applied to 𝛾\{𝑛 1, 𝑛 2, 𝑛 5 }, the mapping returns the erasure |𝛾\{𝑛 1, 𝑛 2, 𝑛 5 }|, because if-mark
elides the contents, and doesn’t modify the children of the nodes that aren’t marked L or R. However,
the calculations modifies the edges out of 𝑛 1 , 𝑛 2 and 𝑛 5 in 𝛾 to obtain precisely the edges of 𝛾 0 .
   On the other hand, the role of inset is to ensure that 𝛼 is a marking-respecting path in 𝛾, and
thus a valid stack. For the same values of 𝛼 and 𝛾 as above, inset 𝛼 𝛾 returns |𝛾 |, because the passed
𝛼 is indeed the stack in 𝛾. However, if we passed a permutation of 𝛼, the equality to |𝛾 | won’t hold.
For example, consider passing [𝑛 2, 𝑛 5, 𝑛 1 ] for 𝛼.
             inset 𝛼 𝛾 = map (if-mark (prev (null • 𝛼))) 𝛾
                       =     𝑛 1 ↦→ if-mark (prev (null • 𝛼)) 𝑛 1 ( L, [null, 𝑛 9 ])
                           • 𝑛 2 ↦→ if-mark (prev (null • 𝛼)) 𝑛 2 ( R, [𝑛 3, 𝑛 1 ])
                           • 𝑛 5 ↦→ if-mark (prev (null • 𝛼)) 𝑛 5 ( L, [𝑛 2, 𝑛 8 ])
                           • map (if-mark (prev (null • 𝛼))) (𝛾\{𝑛 1, 𝑛 2, 𝑛 5 })
                       =     𝑛 1 ↦→ [prev (null • 𝛼) 𝑛 1, 𝑛 9 ]
                           • 𝑛 2 ↦→ [𝑛 3, prev (null • 𝛼) 𝑛 2 ]
                           • 𝑛 5 ↦→ [prev (null • 𝛼) 𝑛 5, 𝑛 8 ]
                           • |𝛾\{𝑛 1, 𝑛 2, 𝑛 5 }|
                       = 𝑛 1 ↦→ [𝑛 5, 𝑛 9 ] • 𝑛 2 ↦→ [𝑛 3, null] • 𝑛 5 ↦→ [𝑛 2, 𝑛 8 ] • |𝛾\{𝑛 1, 𝑛 2, 𝑛 5 }|
                       ≠ |𝛾 |
The calculation considers the nodes 𝑛 1 , 𝑛 2 and 𝑛 5 , as these are the nodes marked L or R. However,
because the nodes aren’t in the traversed order, the computation fails to encode |𝛾 |.              □
  The significance of using the combinator map to define inset and restore is that the general
lemmas from Section 3 apply, immediately deriving that both inset and restore are morphisms in
the argument 𝛾, and thus facilitating contextual localization in the proofs in Section 6. Similarly,
using a higher-order function if-mark lets us prove general lemmas about it once, and use them
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)    17


several times. For example, Lemma 5.1 below states a property about if-mark that immediately
applies to both inset and restore. Similarly, Lemma 5.2 is used to prove both equations (16) and (17)
of Lemma 5.3, which are in turn each used several times in the proofs of the various components of
Schorr-Waite in Section 6.
   Lemma 5.1. If nodes 𝛾/L,R = ∅ (i.e., 𝛾 has no partially marked nodes) then map (if-mark 𝑓 ) 𝛾 = |𝛾 |
for any 𝑓 . In particular, inset 𝛼 𝛾 = restore 𝛼 𝑡 𝛾 = |𝛾 | for any 𝛼 and 𝑡.
    Lemma 5.2. If 𝑓1 𝑥 = 𝑓2 𝑥 for every 𝑥 ∈ nodes 𝛾/L,R then map (if-mark 𝑓1 ) 𝛾 = map (if-mark 𝑓2 ) 𝛾.
    Lemma 5.3. Let 𝛼 be a sequence containing the nodes of 𝛾/L,R . Then the following equations hold.
                                          inset (𝛼 • 𝑝) 𝛾 = inset 𝛼 𝛾                                 (16)
                                      restore (𝛼 • 𝑝) 𝑡 𝛾 = restore 𝛼 𝑝 𝛾                             (17)
   Lemma 5.1 holds because if-mark modifies only partially marked nodes, and applies erasure to
the rest of the graph.
   In Lemma 5.2, if 𝑓1 and 𝑓2 agree on partially marked nodes, then by definition, if-mark 𝑓1 𝑥 (𝛾 𝑥) =
if-mark 𝑓2 𝑥 (𝛾 𝑥) for all 𝑥 ∈ nodes 𝛾, because if-mark modifies only partially marked nodes. The
conclusion then follows by Lemma 3.3.
   Equation (16) follows from Lemma 5.2, by taking 𝑓1 𝑥 = prev (null • 𝛼 • 𝑝) 𝑥 and 𝑓2 𝑥 =
prev (null • 𝛼) 𝑥, and observing that for every 𝑥 ∈ nodes 𝛾/L,R it must be prev (null • 𝛼 • 𝑝) 𝑥 =
prev (null • 𝛼) 𝑥, because 𝑥 ∈ 𝛼. Equation (17) follows similarly by taking 𝑓1 𝑥 = next (𝛼 • 𝑝 • 𝑡) 𝑥
and 𝑓2 𝑥 = next (𝛼 • 𝑝) 𝑥.

6     Proof of Schorr-Waite
The proof of the algorithm is divided into two steps. Following Yang [2001a], Section 6.1 first
verifies Schorr-Waite assuming that the input graph is connected from the root node 𝑟 . Section 6.2
verifies the POP fragment, and Section 6.3 extends to general graphs by framing the nodes not
reachable from 𝑟 . The subproof utilize diverse forms of contextual localization, as we discuss below.

6.1    Proof for Connected Graphs
We first establish the following specification.
                    {graph 𝛾 0 ∧ closed 𝛾 0 ∧ 𝑟 ∈ nodes 𝛾 0 ∧ nodes 𝛾 0 = reach (𝛾 0 /O ) 𝑟 }
                                               Schorr-Waite (𝑟 )                                      (18)
                                    {∃𝛾 . graph 𝛾 ∧ |𝛾 0 | = |𝛾 | ∧ 𝛾 = 𝛾/X }
The precondition in (18) says that the input graph 𝛾 0 is well-formed (graph 𝛾 0 ), closed, contains the
root node 𝑟 , and is unmarked and connected from 𝑟 (nodes 𝛾 0 = reach (𝛾 0 /O ) 𝑟 ). The postcondition
posits an ending graph 𝛾 which, aside from node marking, equals the input graph (|𝛾 0 | = |𝛾 |), and
is fully marked itself (𝛾 = 𝛾/X ).
   Fig. 10 presents the corresponding proof outline, most of which is self-explanatory by standard
Hoare logic. For clarity, we elide the details about the stateful commands in lines 5, 15, 19, 24,
and 28, summarizing their effect through assertions. The elided parts are shown elsewhere: for POP
(line 15) in Section 6.2, for SWING (line 19), PUSH (line 24), line 5 and line 28 in the appendices.
The proof of the remaining stateful command in line 11 is simple and elided altogether.
   We detail the key non-trivial aspects of the proof outline: the non-spatial reasoning steps from
the precondition at line 1 to line 2, and from line 31 to the postcondition at line 32. In both cases,
the graph is at some point decomposed into disjoint parts (e.g., by Lemma 3.2 (2)), and the proof
proceeds to analyze the relationship between those parts. These steps illustrate another example of
18                                                     Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov



      1.   {graph 𝛾 0 ∧ closed 𝛾 0 ∧ 𝑟 ∈ nodes 𝛾 0 ∧ nodes 𝛾 0 = reach (𝛾 0 /O ) 𝑟 }
      2.   {graph 𝛾 0 ∧ inv 𝛾 0 𝛾 0 𝑟 null}
      3. 𝑡 := 𝑟 ; 𝑝 := null;
      4.   {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
      5.   if 𝑡 = null then tm := true else tmp := 𝑡 .𝑚; tm := (tmp ≠ O ) end if;
      6.   {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 ∈ marked0 𝛾)}                             // loop invariant
      7.   while 𝑝 ≠ null ∨ ¬tm do
      8.     {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 ∈ marked0 𝛾) ∧ (𝑝 ≠ null ∨ ¬tm)}
      9.     if tm then
     10.        {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑝 ≠ null ∧ 𝑡 ∈ marked0 𝛾 }
     11.        pm := 𝑝.𝑚;
     12.        {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∈ marked0 𝛾 ∧ 𝛾 val 𝑝 = pm ∈ {𝐿, 𝑅}}
     13.        if pm = R then
     14.            {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∈ marked0 𝛾 ∧ 𝛾 val 𝑝 = R }
     15.            tmp := 𝑝.𝑟 ; 𝑝.𝑟 := 𝑡; 𝑝.𝑚 := X ; 𝑡 := 𝑝; 𝑝 := tmp                          // POP
     16.            {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
     17.        else
     18.            {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∈ marked0 𝛾 ∧ 𝛾 val 𝑝 = L}
     19.            tmp1 := 𝑝.𝑟 ; tmp2 := 𝑝.𝑙; 𝑝.𝑟 := tmp2 ; 𝑝.𝑙 := 𝑡; 𝑝.𝑚 := R; 𝑡 := tmp1      // SWING
     20.            {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
     21.        end if
     22.     else
     23.        {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∉ marked0 𝛾 }
     24.        tmp := 𝑡 .𝑙; 𝑡 .𝑙 := 𝑝; 𝑡 .𝑚 := L; 𝑝 := 𝑡; 𝑡 := tmp                             // PUSH
     25.        {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
     26.     end if;
     27.     {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
     28.     if 𝑡 = null then tm := true else tmp := 𝑡 .𝑚; tm := (tmp ≠ O ) end if
     29.     {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 ∈ marked0 𝛾)}
     30.   end while
     31.   {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑝 = null ∧ 𝑡 ∈ marked0 𝛾 }
     32.   {∃𝛾 . graph 𝛾 ∧ |𝛾 0 | = |𝛾 | ∧ 𝛾 = 𝛾/X }

Fig. 10. Proof outline for the connected graph specification of Schorr-Waite. The fragments verifying the
pointer primitives in lines 5, 11, 15, 19, 24, 28 are elided, and illustrated separately. Notation marked0 𝛾
abbreviates nodes0 (𝛾/L,R,X ), the set of marked nodes of 𝛾, including null.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)      19


contextual localization, here within a proof outline that can be characterized as global, since all
assertions in Fig. 10 refer to the full graph 𝛾, rather than its parts.

   Precondition (lines 1-2). Referring to Fig. 10, line 2 obtains from line 1 by unfolding the
definition of inv from Fig. 9 with 𝑡 = 𝑟 , 𝑝 = null, and instantiating the existentially quantified
stack 𝛼 with the empty sequence []. By setting 𝛼 = [], the unfolding derives proof obligations:
uniq null, null = last (null • []), 𝑟 ∈ nodes0 𝛾 0 , closed 𝛾 0 , nodes 𝛾 0 /L,R = ∅, inset [] 𝛾 0 = |𝛾 0 |,
restore [] 𝑡 𝛾 0 = |𝛾 0 |, and nodes 𝛾 0 /O ⊆ reach (𝛾 0 /O ) 𝑟 . The first four obligations are immediate,
and properties inset [] 𝛾 0 = |𝛾 0 | and restore [] 𝑡 𝛾 0 = |𝛾 0 | follow by Lemma 5.1. The property
nodes 𝛾 0 /O ⊆ reach (𝛾 0 /O ) 𝑟 is also easily shown because nodes 𝛾 0 /O ⊆ nodes 𝛾 0 and nodes 𝛾 0 =
reach (𝛾 0 /O ) 𝑟 by the assumption in line 1.
   To show the remaining nodes 𝛾 0 /L,R = ∅, note that nodes 𝛾 0 /L,R ⊆ nodes 𝛾 0 and reach (𝛾 0 /O ) 𝑟 ⊆
nodes 𝛾 0 /O because filtering and reachability select a subset of graph’s nodes. Thus, nodes 𝛾 0 /L,R ⊆
nodes 𝛾 0 = reach (𝛾 0 /O ) 𝑟 ⊆ nodes 𝛾 0 /O . By Lemma 3.2 (2), 𝛾 0 /L,R and 𝛾 0 /O select node-disjoint
subgraphs of 𝛾 0 . But nodes 𝛾 0 /L,R can be a subset of nodes 𝛾 0 /O with which it’s disjoint, only if
nodes 𝛾 0 /L,R = ∅.

   Postcondition (lines 31-32). From inv 𝛾 0 𝛾 𝑡 𝑝 in line 31, it follows 𝑝 = last (null • 𝛼) and
uniq (null • 𝛼). As 𝑝 = null, it must be 𝛼 = [], i.e., the stack is empty. Then, by (𝑒) in Fig. 9, |𝛾 0 | =
restore [] 𝑡 𝛾, which in turn equals |𝛾 | by Lemma 5.1, thus proving |𝛾 0 | = |𝛾 | in the postcondition.
By Lemma 3.2 (2), the remaining 𝛾 = 𝛾/X from the postcondition is equivalent to nodes 𝛾/O,L,R = ∅.
By Lemma 3.2 (2) again, and distributivity of nodes, the latter is further equivalent to nodes 𝛾/O ∪
nodes 𝛾/L,R = ∅. By (𝑐) in Fig. 9, nodes 𝛾/L,R = ∅, so it suffices to show nodes 𝛾/O = ∅. By (𝑓 ) of
Fig. 9, nodes 𝛾/O ⊆ reach (𝛾/O ) 𝑡, i.e., unmarked nodes of 𝛾 are reachable from 𝑡 by unmarked
paths. But 𝑡 itself is marked in line 31, so no node is reachable from 𝑡 by an unmarked path. Hence,
reach (𝛾/O ) 𝑡 = ∅, and thus nodes 𝛾/O = ∅.

6.2   Proof of POP
The pre- and postcondition for POP derive from lines 14 and 16 of Fig. 10.

                        {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∈ marked0 𝛾 ∧ 𝛾 val 𝑝 = R }
                                                     POP                                               (19)
                                      {∃𝛾 ′ . graph 𝛾 ′ ∧ inv 𝛾 0 𝛾 ′ 𝑡 𝑝}

The precondition says that the heap implements a well-formed graph 𝛾, that satisfies the invariant,
given 𝑡 and 𝑝. Additionally, 𝑡 is marked or null and 𝑝 is marked R, as POP is invoked only if these
properties are satisfied. The postcondition asserts that the heap represents a new graph 𝛾 ′ that
satisfies the invariant for the updated values of 𝑡 and 𝑝. The specification is given solely in terms of
graphs to hide the internal low-level reasoning about pointers, and expose only the more abstract
graph properties required in Fig. 10.
   The proof outline is in Fig. 11 and divides into two parts. The first part (lines 1-9) serves to show
that the stateful commands implementing POP are safe to execute, and result in a valid graph 𝛾 ′ .
The second part (lines 9-10) serves to show that 𝛾 ′ actually satisfies the Schorr-Waite invariants.
Along with the analogous steps in the proofs of SWING and PUSH, this is the most important, and
most substantial part of the whole verification. We discuss the two parts in more detail.

   POP produces valid graph (lines 1-9). Transitioning from line 1 to line 2 involves eliminating
the existential quantifier and saving the current values of 𝑡, 𝑝, and the left and right child of 𝑝
into 𝑡 0 , 𝑝 0 , 𝑝𝑙 and 𝑝𝑟 , respectively. Saving these values prepares for line 3 to omit the last three
20                                                           Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov



             1.   {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∈ marked0 𝛾 ∧ 𝛾 val 𝑝 = R }
             2.            {graph 𝛾 ∧ 𝑡 0 = 𝑡 ∧ 𝑝 0 = 𝑝
                            ∧ inv 𝛾 0 𝛾 𝑡 0 𝑝 0 ∧ 𝑡 0 ∈ marked0 𝛾 ∧ 𝛾 𝑝 0 = ( R, [𝑝𝑙 , 𝑝𝑟 ])}
             3.                  {graph (𝑝 0 ↦→ ( R, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 ) ∧ 𝑡 0 = 𝑡 ∧ 𝑝 0 = 𝑝}
             4.                  {(𝑝 0 Z⇒ R, 𝑝𝑙 , 𝑝𝑟 ∧ 𝑡 0 = 𝑡 ∧ 𝑝 0 = 𝑝) ∗ graph 𝛾\𝑝 0 }
             5.                        {𝑝 0 Z⇒ R, 𝑝𝑙 , 𝑝𝑟 ∧ 𝑡 0 = 𝑡 ∧ 𝑝 0 = 𝑝}
                                       tmp := 𝑝.𝑟 ; 𝑝.𝑟 := 𝑡; 𝑝.𝑚 := X ; 𝑡 := 𝑝; 𝑝 := tmp;           // POP
             6.                        {𝑝 0 Z⇒ X , 𝑝𝑙 , 𝑡 0 ∧ 𝑡 = 𝑝 0 ∧ 𝑝 = 𝑝𝑟 }
             7.                  {(𝑝 0 Z⇒ X , 𝑝𝑙 , 𝑡 0 ∧ 𝑡 = 𝑝 0 ∧ 𝑝 = 𝑝𝑟 ) ∗ graph 𝛾\𝑝 0 }
             8.                  {graph (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 ) ∧ 𝑡 = 𝑝 0 ∧ 𝑝 = 𝑝𝑟 }
             9.            {graph (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 ) ∧ 𝑡 = 𝑝 0 ∧ 𝑝 = 𝑝𝑟
                            ∧ inv 𝛾 0 𝛾 𝑡 0 𝑝 0 ∧ 𝑡 0 ∈ marked0 𝛾 ∧ 𝛾 𝑝 0 = ( R, [𝑝𝑙 , 𝑝𝑟 ])}
            10.   {∃𝛾 . graph 𝛾 ′ ∧ inv 𝛾 0 𝛾 ′ 𝑡 𝑝}
                       ′



Fig. 11. Proof outline for POP. The property inv 𝛾 0 𝛾 𝑡 0 𝑝 0 ∧ 𝑡 0 ∈ marked0 𝛾 ∧ 𝛾 𝑝 0 = ( R, [𝑝𝑙 , 𝑝𝑟 ]) propagates
from line 2 to line 9 because it doesn’t describe the heap or variables mutated by the program.



conjuncts of line 2, which will be re-attached in line 9. The move is valid, because the conjuncts are
unaffected by execution, as they don’t involve the heap or the variables mutated by POP.
   Proceeding with the proof outline, line 3 expands 𝛾 around 𝑝 0 (=𝑝), using equation (5), so that
distributivity of graph (4) applies in line 4 to frame away graph 𝛾\𝑝 0 . This is similar to how the
pointer 𝑗 in Section 2 was separated from the rest of the heap, in order to verify the command that
mutates it. The derivation of line 6 is elided because it’s standard, involving several applications of
framing and the inference rules for the stateful primitives. It suffices to say that the line reflects
the mutations of the pointer 𝑝 0 , and the assignment of new values to 𝑡 and 𝑝, in accord with the
illustration of POP in Fig. 6. In particular, the right edge of 𝑝 0 is redirected towards 𝑡 0 , the node is
marked X , and 𝑡 and 𝑝 are set to 𝑝 0 and 𝑝𝑟 , respectively. The remainder of the proof outline up to
line 9 restores the framed graph and the non-spatial conjuncts omitted in line 3.

   Invariant preservation (lines 9-10). This part of the proof is fully non-spatial and relies almost
entirely on the distributivity of various morphisms, along with a few general graph lemmas from
Section 3. It follows the same pattern of contextual locality as Lemma 3.6, exploiting that the graphs
in lines 9 and 10 share the subgraph 𝛾\𝑝 0 .
   As the first step, we reformulate the problem as the following implication, whose premise restates
the assertions about 𝛾 from line 9, while the conclusion specifies the ending graph 𝛾 ′ .

                                               𝛾 = 𝑝 0 ↦→ ( R, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 ∧                               (20)
                                                    ′
                                               inv 𝛾 0 𝛾 (𝛼 • 𝑝 0 ) 𝑡 0 𝑝 0 ∧                                      (21)
                                               𝑡 0 ∈ marked0 𝛾 =⇒                                                  (22)
                                           ′    ′
                                       ∃𝛾 . 𝛾 = 𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 ∧                                (23)
                                                    ′    ′
                                               inv 𝛾 0 𝛾 𝛼 𝑝 0 𝑝𝑟                                                  (24)
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                           21


    (𝑐) 𝑛𝑜𝑑𝑒𝑠 𝛾 ′ /L,R =                                                            Def. of 𝛾 ′
        = nodes (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 )/L,R                            Lem. 3.1 (1) & 3.1 (3) (distrib.)
        = nodes (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]))/L,R ∪· nodes (𝛾\𝑝 0 )/L,R               Def. of filter (10)
        = nodes (𝛾\𝑝 0 )/L,R                                                        Assump. (21.𝑐)
        =𝛼
    (𝑑) inset 𝛼 𝛾 ′ =                                                               Def. of 𝛾 ′
        = inset 𝛼 (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 )                              Lem. 3.1 (5) (distrib.)
        = inset 𝛼 (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ])) • inset 𝛼 𝛾\𝑝 0                       Def. of inset (14)
        = 𝑝 0 ↦→ [𝑝𝑙 , 𝑡 0 ] • inset 𝛼 𝛾\𝑝 0                                        Lem. 5.3
        = 𝑝 0 ↦→ [𝑝𝑙 , 𝑡 0 ] • inset (𝛼 • 𝑝 0 ) 𝛾\𝑝 0                               Assump. (21.𝑑)
        = 𝑝 0 ↦→ [𝑝𝑙 , 𝑡 0 ] • |𝛾\𝑝 0 |                                             Def. of erasure (8)
        = |𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ])| • |𝛾\𝑝 0 |                                    Lem. 3.1 (4) (distrib.)
        = |𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 |                                      Def. of 𝛾 ′
        = |𝛾 ′ |
    (𝑒) restore 𝛼 𝑝 0 𝛾 ′ =                                                         Def. of 𝛾 ′
        = restore 𝛼 𝑝 0 (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 )                        Lem. 3.1 (5) (distrib.)
        = restore 𝛼 𝑝 0 (𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ])) • restore 𝛼 𝑝 0 𝛾\𝑝 0           Def. of restore (15)
        = 𝑝 0 ↦→ [𝑝𝑙 , 𝑡 0 ] • restore 𝛼 𝑝 0 𝛾\𝑝 0                                  Lem. 5.3
        = 𝑝 0 ↦→ [𝑝𝑙 , 𝑡 0 ] • restore (𝛼 • 𝑝 0 ) 𝑡 0 𝛾\𝑝 0                         Def. of restore (15)
        = restore (𝛼 • 𝑝 0 ) 𝑡 0 (𝑝 0 ↦→ ( R, [𝑝𝑙 , 𝑝𝑟 ]))
           • restore (𝛼 • 𝑝 0 ) 𝑡 0 𝛾\𝑝 0                                           Lem. 3.1 (5) (distrib.)
        = restore (𝛼 • 𝑝 0 ) 𝑡 0 (𝑝 0 ↦→ ( R, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 )                 Assump. (21.𝑒)
        = |𝛾 0 |
    (𝑓 ) nodes 𝛾 ′ /O =                                                            Def. of filter, nodes, 𝛾 & 𝛾 ′
        = nodes 𝛾/O                                                                Assump. (21.𝑓 )
            Ð
        ⊆         (reach (𝛾/O ) ◦ 𝛾𝑟 ) ∪ reach (𝛾/O ) 𝑡 0                          𝑡 0 ∉ nodes 𝛾/O
           𝛼 ·𝑝 0
           Ð
        =        (reach (𝛾/O ) ◦ 𝛾𝑟 )                                               Comm.&Assoc. of ∪
          𝛼 ·𝑝 0
          Ð
        = (reach (𝛾/O ) ◦ 𝛾𝑟 ) ∪ reach (𝛾/O ) (𝛾𝑟 𝑝 0 )                            𝛾𝑟 𝑝 0 ∉ nodes 𝛾/O
           𝛼
                                                                                    (𝛾𝑟 = 𝛾𝑟′ on 𝛼) & (𝛾/O = 𝛾 ′ /O )
          Ð
        = (reach (𝛾/O ) ◦ 𝛾𝑟 )
           𝛼
        = (reach (𝛾 ′ /O ) ◦ 𝛾𝑟′ )                                                 𝑝 0 ∉ nodes 𝛾 ′ /O
          Ð
           𝛼
        = (reach (𝛾 ′ /O ) ◦ 𝛾𝑟′ ) ∪ reach (𝛾 ′ /O ) 𝑝 0
          Ð
            𝛼


Fig. 12. POP preserves invariants (𝑐)-(𝑓 ) for 𝛾 = 𝑝 0 ↦→ ( R, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 and 𝛾 ′ = 𝑝 0 ↦→ ( X , [𝑝𝑙 , 𝑡 0 ]) • 𝛾\𝑝 0 .


   To see that the premise follows from line 9, note that (20) expands 𝛾 around 𝑝 0 , using 𝛾 𝑝 0 =
( R, [𝑝𝑙 , 𝑝𝑟 ]) from line 9; that (21) holds because inv 𝛾 0 𝛾 𝑡 0 𝑝 0 in line 9 implies that 𝑝 0 is the top of
stack of 𝛾, which thus has the form 𝛼 • 𝑝 0 for some 𝛼; and that (22) is an explicit conjunct in line 9.
   In the conclusion of the implication, (23) reflects that the 𝑝 0 is now marked X , and that its right
edge is restored towards 𝑡 0 . On the other hand, (24) indicates that the new stack is 𝛼 (node 𝑝 0
having been popped from the prior stack 𝛼 • 𝑝 0 ), and the new tip and stack’s top are 𝑝 0 and 𝑝𝑟
respectively. These changes correspond to the illustration of POP in Fig. 8, if one takes 𝑝 0 , 𝑡 0 and 𝑝𝑟
as the initial values of 𝑝, 𝑡, and 𝑝’s right child. It’s also readily apparent that (23) and (24) imply the
postcondition of POP in line 10.
22                                                         Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov



        1.   {graph 𝛾 0 ∧ closed 𝛾 0 ∧ 𝑟 ∈ nodes 𝛾 0 ∧ 𝛾 0 = 𝛾 0 /O }
        2.   {∃𝛾 1𝛾 2 . graph (𝛾 1 • 𝛾 2 ) ∧ closed 𝛾 1 ∧ 𝑟 ∈ nodes 𝛾 1 ∧ nodes 𝛾 1 = reach (𝛾 1 /O ) 𝑟
               ∧ nodes 𝛾 1 = reach ((𝛾 1 • 𝛾 2 )/O ) 𝑟 ∧ 𝛾 2 = 𝛾 2 /O ∧ 𝛾 0 = 𝛾 1 • 𝛾 2 }
        3.      {(graph 𝛾 1 ∧ closed 𝛾 1 ∧ 𝑟 ∈ nodes 𝛾 1 ∧ nodes 𝛾 1 = reach (𝛾 1 /O ) 𝑟 )
                  ∗ (graph 𝛾 2 ∧ nodes 𝛾 1 = reach ((𝛾 1 • 𝛾 2 )/O ) 𝑟 ∧ 𝛾 2 = 𝛾 2 /O ∧ 𝛾 0 = 𝛾 1 • 𝛾 2 )}
        4.         {graph 𝛾 1 ∧ closed 𝛾 1 ∧ 𝑟 ∈ nodes 𝛾 1 ∧ nodes 𝛾 1 = reach (𝛾 1 /O ) 𝑟 }
                   Schorr-Waite (𝑟 )
                    ′
        5.          ∃𝛾 1 . graph 𝛾 1′ ∧ |𝛾 1 | = |𝛾 1′ | ∧ 𝛾 1′ = 𝛾 1′ /X
        6.      {(∃𝛾 1′ . graph 𝛾 1′ ∧ |𝛾 1 | = |𝛾 1′ | ∧ 𝛾 1′ = 𝛾 1′ /X )
                  ∗ (graph 𝛾 2 ∧ nodes 𝛾 1 = reach ((𝛾 1 • 𝛾 2 )/O ) 𝑟 ∧ 𝛾 2 = 𝛾 2 /O ∧ 𝛾 0 = 𝛾 1 • 𝛾 2 )}
        7.      {∃𝛾 1′ . graph(𝛾 1′ • 𝛾 2 ) ∧ |𝛾 0 | = |𝛾 1′ • 𝛾 2 |
                  ∧ 𝛾 1′ • 𝛾 2 = (𝛾 1′ • 𝛾 2 )/X • (𝛾 1′ • 𝛾 2 )/O ∧ nodes (𝛾 1′ • 𝛾 2 )/X = reach (𝛾 0 /O ) 𝑟 }
        8.   {∃𝛾 . graph 𝛾 ∧ |𝛾 0 | = |𝛾 | ∧ 𝛾 = 𝛾/X • 𝛾/O ∧ nodes 𝛾/X = reach (𝛾 0 /O ) 𝑟 }

                 Fig. 13. Proof outline for the general graph specification of Schorr-Waite.



   The second step of the proof proceeds to establish the invariant inv′ 𝛾 0 𝛾 ′ 𝛼 𝑝 0 𝑝𝑟 from (24) out of
inv′ 𝛾 0 𝛾 (𝛼 • 𝑝 0 ) 𝑡 0 𝑝 0 in (21), and 𝑡 0 ∈ marked0 𝛾 from (22). As inv′ is defined in Fig. 9 in terms of
conjuncts (𝑎)-(𝑓 ), each conjunct in (24) is proved starting from the corresponding conjunct in (21).
The subcase (𝑏) of this proof is explicitly Lemma 3.6, and Fig. 12 presents the subcases (𝑐)-(𝑓 ) in the
self-explanatory equational style. The proofs follow the pattern of contextual localization from
Lemma 3.6. They begin by decomposing 𝛾 and 𝛾 ′ as in (20) and (23), isolating the node 𝑝 0 from the
shared subcomponent 𝛾\𝑝 0 . Each subcase then applies the appropriate morphism to distribute over
the decomposition, ultimately reducing the goal to a property of 𝛾\𝑝 0 that is already assumed.
   The remaining subcase (𝑎) doesn’t have an equational flavor so we give it here explicitly. That
case requires showing that (20-22) imply uniq (null • 𝛼), 𝑝𝑟 = last (null • 𝛼) and 𝑝 0 ∈ nodes0 𝛾 ′ .
The only non-trivial property is 𝑝𝑟 = last (null • 𝛼), i.e., that 𝑝𝑟 is the top of the stack 𝛼. This holds
because (21) gives inset (𝛼 • 𝑝 0 ) 𝛾 = |𝛾 |, i.e., that the stack 𝛼 • 𝑝 0 is a path in 𝛾. By definition of
inset (14), prev (null • 𝛼 • 𝑝 0 ) 𝑝 0 = 𝛾𝑟 𝑝 0 = 𝑝𝑟 , and thus 𝑝𝑟 = last (null • 𝛼).

6.3   Proof for General Graphs
We can now establish the following general specification of Schorr-Waite, which doesn’t assume
that 𝛾 is connected from 𝑟 .

                           {graph 𝛾 0 ∧ closed 𝛾 0 ∧ 𝑟 ∈ nodes 𝛾 0 ∧ 𝛾 0 = 𝛾 0 /O }
                                                Schorr-Waite (𝑟 )
               {∃𝛾 . graph 𝛾 ∧ |𝛾 0 | = |𝛾 | ∧ 𝛾 = 𝛾/X • 𝛾/O ∧ nodes 𝛾/X = reach (𝛾 0 /O ) 𝑟 }

As in specification (18), the precondition says that the input graph 𝛾 0 is well-formed (graph 𝛾 0 ),
closed, contains the node 𝑟 , and is unmarked (𝛾 0 = 𝛾 0 /O ), but elides the conjunct about connect-
edness. The postcondition posits an ending graph 𝛾 which, aside from node marking, equals the
input graph (|𝛾 0 | = |𝛾 |), and splits into fully marked and unmarked parts (𝛾 = 𝛾/X • 𝛾/O ), with the
fully-marked part corresponding to the nodes initially reachable from 𝑟 (nodes 𝛾/X = reach (𝛾 0 /O ) 𝑟 ).
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                  23


     The proof is in Fig. 13, and is obtained generically, by framing (18) without reanalyzing the code.
It utilizes distributivity of graph to set up the framing, and morphisms to propagate the framed
information from smaller to larger graph. This propagation, carried out in the last step of the proof
(from line 7 to line 8), is a form of contextual localization in reverse, where instead of focusing
inward, information flows outward through the structure.
     In more detail, 𝛾 0 is first split disjointly into 𝛾 1 = 𝛾 0 /(reach 𝛾0 𝑟 ) (part connected from 𝑟 ), and its
complement 𝛾 2 , so that 𝛾 0 = 𝛾 1 • 𝛾 2 . By definition then, nodes 𝛾 1 = reach (𝛾 1 • 𝛾 2 ) 𝑟 , so that by
Lemma 3.5 (2), closed 𝛾 1 , 𝑟 ∈ nodes 𝛾 1 and nodes 𝛾 1 = reach 𝛾 1 𝑟 . Because 𝛾 1 and 𝛾 2 are subgraphs of
𝛾 0 , they are also unmarked (𝛾 1 /O = 𝛾 1 and 𝛾 2 /O = 𝛾 2 ), thus obtaining line 2 in Fig. 13. Distributivity
of graph (4) then derives line 3, which is a separating conjunction of the precondition from (18)
with the predicate that collects all the conjuncts from line 2 that refer to graph 𝛾 2 . By framing the
specification (18), we can thus derive a postcondition for Schorr-Waite in line 6 that is a separating
conjunction of the conjuncts about 𝛾 2 , with the postcondition from (18) that asserts the existence
of a graph 𝛾 1′ such that |𝛾 1 | = |𝛾 1′ | and 𝛾 1′ = 𝛾 1′ /X .
     Proceeding, line 7 joins the graphs 𝛾 1′ and 𝛾 2 together as follows. First, distributivity of graph and
erasure obtains graph (𝛾 1′ • 𝛾 2 ), and |𝛾 0 | = |𝛾 1 • 𝛾 2 | = |𝛾 1′ • 𝛾 2 |. We also get 𝛾 1′ /O = 𝛾 1′ /X /O = 𝑒 and
𝛾 2 /X = 𝛾 2 /O /X = 𝑒 by Lemma 3.2 (4). From here, 𝛾 1′ •𝛾 2 = 𝛾 1′ /X •𝛾 2 /O = (𝛾 1′ • 𝛾 2 )/X • (𝛾 1′ • 𝛾 2 )/O and
also nodes (𝛾 1′ • 𝛾 2 )/X = nodes 𝛾 1′ /X = nodes 𝛾 1′ = nodes |𝛾 1′ | = nodes |𝛾 1 | = nodes 𝛾 1 = reach (𝛾 0 /O ) 𝑟 .
Finally, line 8 abstracts over 𝛾 = 𝛾 1′ • 𝛾 2 .

7 Sketch of Union-Find Verification
The union-find data structure manages a collection of disjoint sets, supporting efficient set merging
and membership queries. Each set is represented in memory as an inverted tree, each element (a
node in the tree) points to its unique parent, and the root of the tree—which points to itself—serves
as the set’s representative. An element’s representative is obtained by following parent pointers
upward. The union operation merges two sets by making the root of one point to the root of the
other set, thereby unifying their representatives (Fig. 14).
   Because each node has a unique parent, union-find operates over unary graphs, with a graph
predicate analogous to that for binary graphs from Section 3.
                                                graph1 𝑒 b
                                                         = emp
                                  graph1 (𝑥 ↦→ 𝑦 • 𝛾) b
                                                      = 𝑥 Z⇒ 𝑦 ∗ graph1 𝛾
The main graph primitives in the specification for union-find are the following.
                                      ( Ð
                                                 summit (𝛾\𝑥) if 𝑥 ∈ nodes 𝛾
                  summit 𝛾 𝑥 b    =      𝛾 adj 𝑥
                                         {𝑥 }                 otherwise
                                        Ð
                   summits 𝛾 b    =            summit 𝛾
                                               nodes 𝛾

                              loops 𝛾     =
                                          b    {𝑥 | 𝑥 ∈ 𝛾 adj 𝑥 }
The set summit 𝛾 𝑥 contains the nodes of 𝛾 that mark an end (i.e., summit) of a path from 𝑥. More
precisely, 𝑧 ∈ summit 𝛾 𝑥 if there exists a path from 𝑥 to some node 𝑦 in 𝛾 such that 𝑧 is a child of 𝑦,
and either 𝑧 ∉ nodes 𝛾 (i.e., the edge from 𝑦 to 𝑧 is dangling) or 𝑧 is already in the path from 𝑥 to 𝑦
(thus starting a cycle). The set summits 𝛾 collects all such ending nodes. The set loops 𝛾 collects the
nodes of 𝛾 that include themselves in their adjacency list; that is, nodes forming cycles of size 1.
   Fig. 14 illustrates the relevance of the above primitives for union-find. Specifically, summit
computes the representative of a given node (e.g, summit 𝛾 𝑐 = {𝑎}), as the representatives in union-
find are precisely the path-ending nodes. Analogously, summits collects all the representatives (e.g.,
24                                                       Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov



         γ:                               d                             γ′ :                          d

                                                    UNION (a,d )
                   a                      e                                    a                      e



              b         c            f        g                            b        c            f         g



Fig. 14. Two disjoint sets encoded as inverted trees being merged by the operation of UNION. Initially, 𝑎 and
𝑑 represent the sets {𝑎, 𝑏, 𝑐} and {𝑑, 𝑒, 𝑓 , 𝑔}, respectively. After the union, 𝑑 represents all the elements.


summits 𝛾 = {𝑎, 𝑑 } and summits 𝛾 ′ = {𝑑 }). Importantly, summit and summits are somewhat more
general still, as they may return nodes that are outside of the graph (dangling edges), or nodes that
start cycles. In particular, if summits 𝛾 only contains nodes in 𝛾, then 𝛾 is closed. Furthermore, if
summits 𝛾 only contains nodes that form trivial cycles (i.e., of size 1, from loops 𝛾), then 𝛾 is acyclic
(modulo representatives), and thus an inverted tree.
   We thus use the above primitives not only to compute the representatives, but also to define
when a graph is an inverted tree. We do so via the following predicate set 𝑆 𝑥 which holds of a heap
that contains the layout of a single set 𝑆 in a union-find collection, whose representative is 𝑥.
                            = ∃𝛾 . graph1 𝛾 ∧ summits 𝛾 = loops 𝛾 = {𝑥 } ∧ nodes 𝛾 = 𝑆
                    set 𝑆 𝑥 b
Indeed, the definition requires the existence of a unary graph 𝛾 whose nodes are exactly 𝑆, such
that 𝛾 has 𝑥 as the unique summit (i.e., 𝛾 is closed), and 𝑥 forms a trivial cycle (i.e., 𝛾 is inverted
tree). For example, in the graph 𝛾 in Fig. 14 we have set {𝑎, 𝑏, 𝑐} 𝑎 and set {𝑑, 𝑒, 𝑓 , 𝑔} 𝑑.
   The following Hoare triples specify the methods of union-find, where the method’s postcondition
denotes the method’s return value by the dedicated variable result.7
                             {𝑒𝑚𝑝}            NEW             {set {result} result}
                {set 𝑆 𝑦 ∧ 𝑥 ∈ 𝑆 }          FIND (𝑥)          {set 𝑆 𝑦 ∧ result = 𝑦}
           {set 𝑆 1 𝑥 1 ∗ set 𝑆 2 𝑥 2 }   UNION (𝑥 1, 𝑥 2 )   {set (𝑆 1 ∪· 𝑆 2 ) result ∧ result ∈ {𝑥 1, 𝑥 2 }}
NEW starts from an empty heap and allocates a node that forms a singleton set and serves as its own
representative. FIND takes a node 𝑥 known to belong to some set 𝑆, and returns the representative 𝑦
of 𝑆. UNION assumes that 𝑥 1 and 𝑥 2 are representatives of disjoint sets and joins the sets, returning
one of 𝑥 1 or 𝑥 2 as the new representative (Fig. 14). Notably, our specifications refer only to the
disjoint sets each operation manipulates, following the small footprint style. While this is the norm
in separation logic generally, we’re unaware of prior union-find verifications that adopt it.
   The implementation and the proof outlines for the methods are in the appendix. Here, we
only discuss how morphisms and distributivity help with the verification of union-find. The main
challenge in this verification is establishing, in various subproofs, the inclusion summits 𝛾 ⊆ loops 𝛾,
which is one side of the defining equation summits 𝛾 = loops 𝛾 from the set predicate. This closely
resembles the definition of closed in Section 3 as sinks 𝛾 ⊆ nodes0 𝛾, where the fact that sinks and
nodes are morphisms enabled contextual localization via Lemma 3.6.
   In the case of union-find, we apply the same principle of localization by leveraging distribution
properties of loops and summits. The former is a standard PCM morphism. The latter, however,
exhibits more nuanced behavior. First, it distributes only under the specific condition that all cycles
7 This requires extending the heretofore used standard logic of O’Hearn, Reynolds and Yang with value-returning methods,

but Hoare Type Theory admits such an extension.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)   25


in the graph are trivial—a property satisfied by union-find graphs. Second, and more unusually, its
distribution doesn’t follow the standard additive form of morphisms, but subtracts nodes from the
opposing component to avoid interference.
                  summits (𝛾 1 • 𝛾 2 ) = (summits 𝛾 1 )\nodes 𝛾 2 ∪ (summits 𝛾 2 )\nodes 𝛾 1
The intuition is that a summit in a subgraph 𝛾 1 is a path-ending node. If the path ends with a
dangling edge into 𝛾 2 , the summit ceases to be path-ending in the composition, where the path
continues. The equation accounts for this by explicitly removing the overlap through set subtraction.
  While the full theory of loops and summits is more extensive, and holds for general (not just unary)
graphs, the distribution principle above suffices to draw a high-level analogy with Schorr-Waite,
and illustrate how contextual localization applies equally well to union-find.

8   Related work
   Proofs of Schorr-Waite in separation logic. The starting point of our paper has been Yang’s
proof [Yang 2001a,b], which is an early work on separation logic generally, and the first work
on graphs in separation logic specifically. The distinction with our proof is that Yang doesn’t use
mathematical graphs as an explicit argument to the graph predicate, but rather relies on non-spatial
proxy abstractions, such as the spanning tree of the graph, and various subsets of nodes. These
proxy abstractions aren’t independent, and to keep them synchronized with each other and with
the graph laid out in the heap, the proof must frequently switch between non-spatial and spatial
reasoning, at the cost of significant formal overhead. In contrast, we avoid the overhead by keeping
most of the reasoning about graphs at the non-spatial level.
   Considering his first proof too complex, Yang tackled Schorr-Waite again using relational separa-
tion logic [Yang 2007]. Relational logic establishes a contextual refinement between two programs;
in the case of Schorr-Waite, a refinement with the obvious depth-first-search (DFS) implementation
of graph marking. While the resulting proof achieved a conceptual simplification over the original
non-relational proof, this is somewhat counter-intuitive, as refinement between two programs is
generally a much stronger property—and thus more demanding to prove—than establishing a pre-
and postcondition for a program. Our result confirms this intuition. In comparison, an optimization
of Yang’s relational proof is given by Crespo and Kunz [2011], who show that Schorr-Waite is
contextually equivalent to DFS, and mechanize the proof in around 3000 lines in Coq.
   Non-separation proofs of Schorr-Waite. Being a standard verification benchmark for graph
algorithms, Schorr-Waite has been verified numerous times, using a variety of different approaches.
These ranged from automated ones [Leino 2010; Loginov et al. 2006; Roever 1977; Suzuki 1976], to
studies of the algorithm’s mathematical properties [Abrial 2003; Bornat 2000; Bubel 2007; Dershowitz
1980; Gries 1979; Griffiths 1979; Hubert and Marché 2005; Mehta and Nipkow 2003; Morris 1982;
Topor 1979], to proofs based on program transformation [Broy and Pepper 1982; Dufourd 2014;
Gerhart 1979; Giorgino et al. 2010; Preoteasa and Back 2012, 2010; Ward 1996]. The important
difference from this work is that we explicitly wanted to support and utilize framing in our proof,
as framing is the key feature of separation logic.
  Proofs of union-find. The union-find structure [Galler and Fisher 1964] is also a well-studied
graph benchmarks, with numerous correctness proofs, including in separation logic. For instance,
Conchon and Filliâtre [2007] verify a persistent version in Coq that uses two functional arrays,
while Lammich and Meis [2012] verify an implementation in Imperative/HOL. Krishnaswami [2011]
provides a non-mechanized proof, and Charguéraud and Pottier [2019] give a Coq proof with a
complexity analysis, both targeting a heap-allocated implementation, as we do. Wang et al. [2019],
additionally verifies an array-based variant in Coq. Our approach differs in two key ways: we use
26                                                Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


partial graphs rather than traditional graph theory in order to leverage PCM morphisms; we also
adopt small-footprint specifications that describe only the modified disjoint subsets, as opposed to
the whole structure.
   Graphs in separation logic, without PCMs. In the search for a graph predicate that enables
decomposition, Bornat et al. [2004] define a partial graph as a recursive tree-shaped term, encoding
the following strategy. Given some default traversal order, the first time a node is encountered, it’s
explicitly recorded in the term. Every later occurrence is recorded as a reference (i.e., pointer) to the
first one. This enables that closed graphs can be encoded in a way that facilitates decomposition,
but is dependent on the traversal order, which is problematic, as it prevents developing general
libraries of lemmas about graphs. We used the PCM of partial graphs to remove the restriction to
closed graphs, which also removes the traversal-order dependence.
   Wang [2019] and Wang et al. [2019] parametrize their graph predicate with a closed mathematical
graph, and express program invariant in terms of it. Because a closed graph doesn’t necessarily
decompose into closed subgraphs, these invariants aren’t considered under distribution. Thus, to
prove that a state modification maintains the graph invariant, one typically must resort to reasoning
about the whole graph. This global reasoning can be ameliorated by introducing additional logical
connectives and rules, such as e.g., overlapping conjunction and ramified frame rules [Hobor and
Villard 2013]. In contrast, by relying on PCMs and morphisms, we were able to stay within standard
separation logic over heaps.
   Graphs in separation logic, with PCMs. Sergey et al. [2015a] and Nanevski [2016] parametrized
their graph predicate by a heap (itself a PCM), that serves as a representation of a partial graph.
Heaps obviously decompose under disjoint union. However, since the graph predicate includes the
restriction that the implemented graph must be closed, the predicate itself doesn’t distribute. This
is worked around by introducing helper relations for when one graph is a subgraph of another,
which our formulation provides for free (e.g., 𝛾 1 is a subgraph of 𝛾 iff 𝛾 = 𝛾 1 • 𝛾 2 for some 𝛾 2 ). These
works don’t consider PCM morphisms or Schorr-Waite.
   More recently, Krishna et al. [2020] and Meyer et al. [2023] introduced a theory of flows, as a
framework to study the decomposition of graph properties. Flows evoke Yang’s first proof, in that
they serve as decomposition-supporting proxies for the specification of the graph. In contrast, we
parametrize the reasoning by the whole graph, and compute proxies by morphisms, when needed.
That said, flows are intended for automated reasoning, which we haven’t considered.
   Finally, Costa et al. [[n. d.]] define the PCM of pregraphs. A pregraph is like our partial graph,
but it may contain incoming dangling edges, not just outgoing ones that sufficed for us. The
paper proceeds to define a separation logic over pregraphs, much as separation logic over heaps
is classically defined using local actions [Calcagno et al. 2007]. In contrast, we use a standard
separation logic over heaps, where (partial) graphs are merely a secondary user-level PCM. Having
heaps and graphs coexist is necessary for representing pointer-based graph algorithms such as
Schorr-Waite, but it requires PCM morphisms to mediate between the two.
  Morphisms in separation logic. While extant separation logics extensively rely on PCMs,
PCM morphisms remains underutilized. A notable exception is the work of Farka et al. [2021],
who develop a theory of partial PCM morphisms—morphisms that distribute only under certain
conditions. These conditions give rise to separating relations, a novel algebraic structure with rich
theoretical properties. Together, morphisms and separating relations define when one PCM is a
sub-PCM of another, and how to refine Hoare logic triples accordingly.
  This refinement concept originated with Nanevski et al. [2019], who formulated it as a morphism
over resources, which are algebraic structures modeling state-transition systems for concurrency.
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)   27


Although resources involve a form of structural inclusion, they don’t form PCMs, nor does their
theory rely on join-based decomposition. Moreover, resource morphisms act on programs, to
retroactively adapt a program’s ghost code via a simulation function, whereas PCM morphisms
operate within logical assertions. As a result, resources and their morphisms address orthogonal
concerns to ours. Finally, neither of the works applies their morphisms to graphs.
   Graphs algebraically. Recent works in functional programming, theorem proving and category
theory have proposed treating graphs algebraically [Liell-Cock and Schrijvers 2024; Master 2021,
2022; Mokhov 2017, 2022], though so far without application to separation logic. Most recently, Kid-
ney and Wu [2025] share with us the representation of graphs as maps, which they further endow
with the algebraic structure of rings, comprising distinct monoids for vertices and for edges. They
also propose several different algebraic constructions along with the associated morphisms. Their
application is in implementing graph algorithms as state-free coinductive programs in Agda and
Haskell. In contrast, we use the algebra of graphs for specification and verification of programs, not
for their implementation, as our programs in general, and our variant of Schorr-Waite in particular,
are implemented in an imperative pointer-based language customary for separation logic. Our
focus on separation logic also gives rise to somewhat different monoidal structures. In particular,
as we need to relate graphs to pointers and framing, we focus on partiality and, correspondingly,
use a monoid of graphs whose join operation is very different from the constructions considered in
the above work.

9   Conclusion
This paper establishes that graphs form a PCM when extended with dangling edges, yielding partial
graphs. The PCM structure facilitates natural composition through subgraph joins, and induces
PCM morphisms as structure-preserving functions. Our central contribution demonstrates how
PCM morphisms address separation logic’s long-standing challenge of effective graph verification.
   Crucially, PCM morphisms enrich the foundational principle of locality: while traditional framing
enables spatial locality by isolating heap portions, morphisms enable non-spatial locality by isolating
relevant graph subcomponents. The key mechanism is contextual localization; that is, distributing
morphisms across subgraph joins (𝑓 (𝛾 1 • 𝛾 2 ) = 𝑓 𝛾 1 • 𝑓 𝛾 2 ). Unlike framing, which operates only at
the top level of a specification, contextual localization supports rewriting deeply inside a context.
   We further employ higher-order combinators like map to define helper notions for complex graph
invariants (e.g., in Schorr-Waite) and to support general lemmas that can be reused across multiple
instances. The integration of partial graphs, morphisms, and higher-order combinators yields novel,
mechanized proofs for both Schorr-Waite algorithm and the union-find data structure, achieving
substantial conciseness through lemma reuse and contextual localization.
   All proofs are fully mechanized in Coq using the Hoare Type Theory library. The mechanization
uses functional (non-mutable) variables in place of mutable ones used in the paper, but this is a
technical variation with no impact on the results.

Acknowledgments
We thank Anindya Banerjee and the anonymous ICFP reviewers for their numerous useful com-
ments. This work was partially supported by the Spanish MICIU grants DECO PID2022-138072OB-
I00, Maria de Maeztu CEX2024-001471-M, PRODIGY TED2021-132464B-I00, and the ERC Starting
Grant CRETE GA:101039196. Any views, opinions and findings expressed in the text are those of
the authors and don’t necessarily reflect the views of the funding agencies.
28                                                       Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


References
Jean-Raymond Abrial. 2003. Event based sequential program development: application to constructing a pointer program.
   In Formal Methods Europe (FME). 51–74. doi:10.1007/978-3-540-45236-2_5
Richard Bornat. 2000. Proving pointer programs in Hoare logic. In Mathematics of Program Construction (MPC). 102–126.
   doi:10.1007/10722010_8
Richard Bornat, Cristiano Calcagno, and Peter O’Hearn. 2004. Local reasoning, separation and aliasing. In Workshop on
   Semantics, Program Analysis and Computing Environments for Memory Management (SPACE). http://www.cs.ucl.ac.uk/
   staff/p.ohearn/papers/separation-and-aliasing.pdf
Richard Bornat, Cristiano Calcagno, Peter O’Hearn, and Matthew Parkinson. 2005. Permission accounting in separation
   logic. In Principles of Programming Languages (POPL). 259–270. doi:10.1145/1040305.1040327
Manfred Broy and Peter Pepper. 1982. Combining algebraic and algorithmic reasoning: an approach to the Schorr-Waite
   algorithm. ACM Trans. Program. Lang. Syst. 4, 3 (1982), 362–381. doi:10.1145/357172.357175
Richard Bubel. 2007. The Schorr-Waite-Algorithm. In Verification of Object-Oriented Software: The KeY Approach. 569–587.
   doi:10.1007/978-3-540-69061-0_15
Cristiano Calcagno, Peter W. O’Hearn, and Hongseok Yang. 2007. Local action and abstract separation logic. In Logic in
   Computer Science (LICS). 366–378. doi:10.1109/LICS.2007.30
Arthur Charguéraud and François Pottier. 2019. Verifying the correctness and amortized complexity of a union-find
   implementation in separation logic with time credits. J. Autom. Reasoning 62 (2019), 331–365. doi:10.1007/s10817-017-
   9431-7
Sylvain Conchon and Jean-Christophe Filliâtre. 2007. A persistent union-find data structure. In ML Workshop. 37–46.
   doi:10.1145/1292535.1292541
Diana Costa, James Brotherston, and David Pym. [n. d.]. Graph decomposition and local reasoning. Retrieved 2024 from
   http://www0.cs.ucl.ac.uk/staff/D.Pym/pregraphs.pdf
Juan Manuel Crespo and César Kunz. 2011. A machine-checked framework for relational separation logic. In Software
   Engineering and Formal Methods (SEFM). 122–137. doi:10.1007/978-3-642-24690-6_10
Nachum Dershowitz. 1980. The Schorr-Waite marking algorithm revisited. Inform. Process. Lett. 11, 3 (1980), 141–143.
   doi:10.1016/0020-0190(80)90130-1
Thomas Dinsdale-Young, Lars Birkedal, Philippa Gardner, Matthew Parkinson, and Hongseok Yang. 2013. Views: composi-
   tional reasoning for concurrent programs. In Principles of Programming Languages (POPL). 287–300. doi:10.1145/2429069.
   2429104
Jean-François Dufourd. 2014. Pointer program derivation using Coq: graphs and Schorr-Waite algorithm. In Formal Methods
   and Software Engineering (ICFEM). 139–154. doi:10.1007/978-3-319-11737-9_10
František Farka, Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas. 2021. On
   algebraic abstractions for concurrent separation logics. Proc. ACM Program. Lang. 5, POPL, Article 5 (2021). doi:10.1145/
   3434286
Bernard A. Galler and Michael J. Fisher. 1964. An improved equivalence algorithm. Commun. ACM 7, 5 (1964), 301–303.
   doi:10.1145/364099.364331
Susan L. Gerhart. 1979. A derivation-oriented proof of the Schorr-Waite marking algorithm. In Program Construction:
   International Summer School. 472–492. doi:10.1007/BFb0014678
Mathieu Giorgino, Martin Strecker, Ralph Matthes, and Marc Pantel. 2010. Verification of the Schorr-Waite algorithm - from
   trees to graphs. In Logic-Based Program Synthesis and Transformation (LOPSTR). 67–83. doi:10.1007/978-3-642-20551-4_5
Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov. 2025a. Artifact for Verifying graph algorithms in separation
   logic: a case for an algebraic approach. doi:10.5281/zenodo.15847649
Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov. 2025b. Verifying graph algorithms in separation logic: a
   case for an algebraic approach. Proc. ACM Program. Lang. 9, ICFP, Article 241 (2025). doi:10.1145/3747510
David Gries. 1979. The Schorr-Waite graph marking algorithm. In Program Construction: International Summer School.
   58–69. doi:10.1007/BFb0014658
Michael Griffiths. 1979. Development of the Schorr-Waite algorithm. In Program Construction: International Summer School.
   464–471. doi:10.1007/BFb0014677
Aquinas Hobor and Jules Villard. 2013. The ramifications of sharing in data structures. In Principles of Programming
   Languages (POPL). 523–536. doi:10.1145/2429069.2429131
HTT 2010. Hoare Type Theory. Retrieved 2025 from https://github.com/imdea-software/htt
Thierry Hubert and Claude Marché. 2005. A case study of C source code verification: the Schorr-Waite algorithm. Software
   Engineering and Formal Methods (SEFM) (2005), 190–199. doi:10.1109/SEFM.2005.1
Samin Ishtiaq and Peter W. O’Hearn. 2001. BI as an assertion language for mutable data structures. In Principles of
   Programming Languages (POPL). 14–26. doi:10.1145/360204.375719
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)                    29


Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris:
   monoids and invariants as an orthogonal basis for concurrent reasoning. In Principles of Porgramming Languages (POPL).
   637–650. doi:10.1145/2676726.2676980
Donnacha Oisín Kidney and Nicolas Wu. 2025. Formalising graph algorithms with coinduction. Proc. ACM Program. Lang.
   9, POPL, Article 56 (2025). doi:10.1145/3704892
Siddharth Krishna, Alexander J. Summers, and Thomas Wies. 2020. Local reasoning for global graph properties. In European
   Symposium on Programming (ESOP). 308–335. doi:10.1007/978-3-030-44914-8_12
Neelakantan R. Krishnaswami. 2011. Verifying higher-order imperative programs with higher-order separation logic. Ph. D.
   Dissertation. Carnegie Mellon University. http://reports-archive.adm.cs.cmu.edu/anon/2012/CMU-CS-12-127.pdf
Peter Lammich and Rene Meis. 2012. A separation logic framework for Imperative HOL. Arch. Formal Proofs (2012).
   https://www.isa-afp.org/entries/Separation_Logic_Imperative_HOL.shtml
K. Rustan M. Leino. 2010. Dafny: an automatic program verifier for functional correctness. In Logic for Programming,
   Artificial Intelligence, and Reasoning (LPAR). 348–370. doi:10.1007/978-3-642-17511-4_20
Jack Liell-Cock and Tom Schrijvers. 2024. Let a thousand flowers bloom: an algebraic representation for edge graphs. The
   Art, Science, and Engineering of Programming 8, 3 (2024). doi:10.22152/programming-journal.org/2024/8/9
Alexey Loginov, Thomas W. Reps, and Mooly Sagiv. 2006. Automated verification of the Deutsch-Schorr-Waite tree-traversal
   algorithm. In Static Analysis Symposium (SAS). 261–279. doi:10.1007/11823230_17
Jade Master. 2021. The open algebraic path problem. doi:10.48550/arXiv.2005.06682
Jade Master. 2022. How to compose shortest paths. doi:10.48550/arXiv.2205.15306
Farhad Mehta and Tobias Nipkow. 2003. Proving pointer programs in higher-order logic. In Conference on Automated
   Deduction (CADE). 121–135. doi:10.1007/978-3-540-45085-6_10
Roland Meyer, Thomas Wies, and Sebastian Wolff. 2023. Make flows small again: revisiting the flow framework. In Tools
   and Algorithms for the Construction and Analysis of Systems (TACAS). 628–646. doi:10.1007/978-3-031-30823-9_32
Andrey Mokhov. 2017. Algebraic graphs with class (functional pearl). In International Symposium on Haskell. 2–13.
   doi:10.1145/3122955.3122956
Andrey Mokhov. 2022. United monoids: finding simplicial sets and labelled algebraic graphs in trees. The Art, Science, and
   Engineering of Programming 6, 3 (2022). doi:10.22152/programming-journal.org/2022/6/12
Joseph M. Morris. 1982. A proof of the Schorr-Waite algorithm. In Theoretical Foundations of Programming Methodology:
   Lecture Notes of an International Summer School. 43–51. doi:10.1007/978-94-009-7893-5_5
Aleksandar Nanevski. 2016. Separation logic and concurrency. Lecture notes for the Oregon Programming Languages
   Summer School (OPLSS). https://www.cs.uoregon.edu/research/summerschool/summer16/curriculum.php
Aleksandar Nanevski, Anindya Banerjee, Germán Andrés Delbianco, and Ignacio Fábregas. 2019. Specifying concurrent
   programs in separation logic: morphisms and simulations. Proc. ACM Program. Lang. 3, OOPSLA, Article 161 (2019).
   doi:10.1145/3360587
Aleksandar Nanevski, Greg Morrisett, and Lars Birkedal. 2006. Polymorphism and separation in Hoare Type Theory. In
   International Conference on Functional Programming (ICFP). 62–73. doi:10.1145/1159803.1159812
Aleksandar Nanevski, Greg Morrisett, Avraham Shinnar, Paul Govereau, and Lars Birkedal. 2008. Ynot: dependent types for
   imperative programs. In International Conference on Functional Programming (ICFP). 229–240. doi:10.1145/1411203.1411237
Aleksandar Nanevski, Viktor Vafeiadis, and Josh Berdine. 2010. Structuring the verification of heap-manipulating programs.
   In Principles of Programming Languages (POPL). 261–274. doi:10.1145/1706299.1706331
Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local reasoning about programs that alter data structures.
   In Computer Science Logic (CSL). 1–19. doi:10.1007/3-540-44802-0_1
Viorel Preoteasa and Ralph-Johan Back. 2012. Invariant diagrams with data refinement. Formal Aspects Comput. 24, 1 (2012),
   67–95. doi:10.1007/S00165-011-0195-2
Viorel Preoteasa and Ralph-Johan Back. 2010. Verification of the Deutsch-Schorr-Waite graph marking algorithm using
   data refinement. Arch. Formal Proofs (2010). https://www.isa-afp.org/browser_info/current/AFP/GraphMarkingIBP/
   document.pdf
John C. Reynolds. 2002. Separation logic: a logic for shared mutable data structures. In Logic in Computer Science (LICS).
   55–74. doi:10.1109/LICS.2002.1029817
Willem-Paul Roever. 1977. On backtracking and greatest fixpoints. In International Colloquium on Automata, Languages and
   Programming (ICALP). 412–429. doi:10.1007/3-540-08342-1_32
Herbert Schorr and William M. Waite. 1967. An efficient machine-independent procedure for garbage collection in various
   list structures. Commun. ACM 10, 8 (1967), 501–506. doi:10.1145/363534.363554
Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2015a. Mechanized verification of fine-grained concurrent
   programs. In Programming Language Design and Implementation (PLDI). 77–87. doi:10.1145/2737924.2737964
Ilya Sergey, Aleksandar Nanevski, and Anindya Banerjee. 2015b. Specifying and verifying concurrent algorithms with
   histories and subjectivity. In European Symposium on Programming (ESOP). 333–358. doi:10.1007/978-3-662-46669-8_14
30                                                        Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


Norihisa Suzuki. 1976. Automatic verification of programs with complex data structures. Ph. D. Dissertation. Stanford
   University.
Rodney W. Topor. 1979. The correctness of the Schorr-Waite list marking algorithm. Acta Informatica 11 (1979), 211–221.
   doi:10.1007/BF00289067
Shengyi Wang. 2019. Mechanized verification of graph-manipulating programs. Ph. D. Dissertation. School of Computing,
   National University of Singapore. https://scholarbank.nus.edu.sg/handle/10635/166280
Shengyi Wang, Qinxiang Cao, Anshuman Mohan, and Aquinas Hobor. 2019. Certifying graph-manipulating C programs via
   localizations within data structures. Proc. ACM Program. Lang. 3, OOPSLA, Article 171 (2019). doi:10.1145/3360597
Martin Ward. 1996. Derivation of data intensive algorithms by formal transformation: the Schorr-Waite graph marking
   algorithm. IEEE Trans. Softw. Eng. 22, 9 (1996), 665–686. doi:10.1109/32.541437
Hongseok Yang. 2001a. An example of local reasoning in BI pointer logic: the Schorr-Waite graph marking algorithm.
   In Workshop on Semantics, Program Analysis and Computing Environments for Memory Management (SPACE). https:
  //citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=d93456b70d4ec3569c29409c73aabb0fddb6ed49
Hongseok Yang. 2001b. Local reasoning for stateful programs. Ph. D. Dissertation. University of Illinois at Urbana-Champaign.
   https://drive.google.com/open?id=1gFdENbez-p6tCksvz2NgdU7y_aV0zHLW
Hongseok Yang. 2007. Relational separation logic. Theor. Comput. Sci. 375 (2007), 308–334. doi:10.1016/j.tcs.2006.12.036


A    Proof outline for the length-calculating program

         {𝑙𝑖𝑠𝑡 𝛼 0 (𝑖, null)}
        𝑛 := 0;
         {𝑙𝑖𝑠𝑡 𝛼 0 (𝑖, null) ∧ 𝑛 = 0}
         𝑗 := 𝑖;
         {𝑖 = 𝑗 ∧ 𝑙𝑖𝑠𝑡 𝛼 0 (𝑖, null) ∧ 𝑛 = 0}
         {𝑙𝑖𝑠𝑡 [] (𝑖, 𝑗) ∗ 𝑙𝑖𝑠𝑡 𝛼 0 ( 𝑗, null) ∧ 𝑛 = #[] ∧ 𝛼 0 = [] • 𝛼 0 }
         {∃𝛼 𝛽. 𝑙𝑖𝑠𝑡 𝛼 (𝑖, 𝑗) ∗ 𝑙𝑖𝑠𝑡 𝛽 ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • 𝛽}
         while 𝑗 ≠ null do
            {∃𝛼 𝛽. list 𝛼 (𝑖, 𝑗) ∗ list 𝛽 ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • 𝛽 ∧ 𝑗 ≠ null}
            {∃𝛼 𝑏 𝛽 ′ . list 𝛼 (𝑖, 𝑗) ∗ list (𝑏 • 𝛽 ′ ) ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • (𝑏 • 𝛽 ′ )}
            {∃𝛼 𝑏 𝛽 ′ 𝑘. list 𝛼 (𝑖, 𝑗) ∗ 𝑗 Z⇒ 𝑏, 𝑘 ∗ list 𝛽 ′ (𝑘, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • (𝑏 • 𝛽 ′ )}
            𝑗 := 𝑗 .next;
            {∃𝛼 𝑏 𝛽 ′ 𝑗 ′ . list 𝛼 (𝑖, 𝑗 ′ ) ∗ 𝑗 ′ Z⇒ 𝑏, 𝑗 ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = 𝛼 • (𝑏 • 𝛽 ′ )}
            {∃𝛼 𝑏 𝛽 ′ . list (𝛼 • 𝑏) (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ∧ 𝛼 0 = (𝛼 • 𝑏) • 𝛽 ′ }
            𝑛 := 𝑛 + 1;
            {∃𝛼 𝑏 𝛽 ′ . list (𝛼 • 𝑏) (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 + 1 ∧ 𝛼 0 = (𝛼 • 𝑏) • 𝛽 ′ }
            {∃𝛼 𝑏 𝛽 ′ . list (𝛼 • 𝑏) (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #(𝛼 • 𝑏) ∧ 𝛼 0 = (𝛼 • 𝑏) • 𝛽 ′ }
            {∃𝛼 ′ 𝛽 ′ . list 𝛼 ′ (𝑖, 𝑗) ∗ list 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ′ ∧ 𝛼 0 = 𝛼 ′ • 𝛽 ′ }
         end while
         {∃𝛼 ′ 𝛽 ′ . 𝑙𝑖𝑠𝑡 𝛼 ′ (𝑖, 𝑗) ∗ 𝑙𝑖𝑠𝑡 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ′ ∧ 𝛼 0 = 𝛼 ′ • 𝛽 ′ ∧ 𝑗 = null}
         {∃𝛼 ′ 𝛽 ′ . 𝑙𝑖𝑠𝑡 𝛼 ′ (𝑖, 𝑗) ∗ 𝑙𝑖𝑠𝑡 𝛽 ′ ( 𝑗, null) ∧ 𝑛 = #𝛼 ′ ∧ 𝛼 0 = 𝛼 ′ • 𝛽 ′ ∧ 𝑗 = null ∧ 𝛽 ′ = []}
         {∃𝛼 ′ . 𝑙𝑖𝑠𝑡 𝛼 ′ (𝑖, null) ∗ 𝑙𝑖𝑠𝑡 [] (null, null) ∧ 𝑛 = #𝛼 ′ ∧ 𝛼 0 = 𝛼 ′ }
         {𝑙𝑖𝑠𝑡 𝛼 0 (𝑖, null) ∗ 𝑒𝑚𝑝 ∧ 𝑛 = #𝛼 0 }
         {𝑙𝑖𝑠𝑡 𝛼 0 (𝑖, null) ∧ 𝑛 = #𝛼 0 }
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)             31


B    Proof outline for computing if 𝑡 is marked (or null)
              {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
                {graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
                if 𝑡 = null then
                   {graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 = 𝑛𝑢𝑙𝑙 }
                   tm := true
                   {graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 = 𝑛𝑢𝑙𝑙 ∧ tm = true}
                   {graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 = 𝑛𝑢𝑙𝑙)}
                else
                   {graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ≠ 𝑛𝑢𝑙𝑙 }
                   {∃𝑚. 𝑡 Z⇒ 𝑚, −, − ∗ graph 𝛾\𝑡 ∧ inv 𝛾 0 𝛾 𝑡 𝑝}
                   tmp := 𝑡 .𝑚;
                   {∃𝑚. 𝑡 Z⇒ 𝑚, −, − ∗ graph 𝛾\𝑡 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tmp = 𝑚}
                   tm := (tmp ≠ O )
                   {∃𝑚. 𝑡 Z⇒ 𝑚, −, − ∗ graph 𝛾\𝑡 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tmp = 𝑚 ∧ tm = (tmp ≠ O )}
                   {∃𝑚. 𝑡 Z⇒ 𝑚, −, − ∗ graph 𝛾\𝑡 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑚 ≠ O )}
                   {graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 .𝑚 ≠ O )}
                   
                     graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 ∈ nodes 𝛾/L,R,X )
                end if
                
                  graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 = null ∨ 𝑡 ∈ nodes 𝛾/L,R,X )
                {graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 ∈ marked0 𝛾)}
              {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ tm = (𝑡 ∈ marked0 𝛾)}

C    Proof for SWING
The pre- and postcondition for SWING derive from lines 18 and 20 of Fig. 10.
                           {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∈ marked0 𝛾 ∧ 𝛾 val 𝑝 = L}
                                                      SWING                                                    (25)
                                         {∃𝛾 ′ . graph 𝛾 ′ ∧ inv 𝛾 0 𝛾 ′ 𝑡 𝑝}
The precondition says that the heap implements a well-formed graph 𝛾, that satisfies the invariant.
Additionally, 𝑡 is marked or null and 𝑝 is marked L. The postcondition asserts that the heap
represents a new graph 𝛾 ′ that satisfies the invariant for the updated values of 𝑡 and 𝑝.
         1.     {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∈ marked0 𝛾 ∧ 𝛾 val 𝑝 = L}
         2.            {graph 𝛾 ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0
                        ∧inv 𝛾 0 𝛾 𝑡 0 𝑝 0 ∧ 𝑡 0 ∈ marked0 𝛾 ∧ 𝛾 𝑝 0 = ( L, [𝑝𝑙 , 𝑝𝑟 ])}
         3.                 {graph (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 ) ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0 }
         4.                 {(𝑝 0 Z⇒ L, 𝑝𝑙 , 𝑝𝑟 ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0 ) ∗ graph 𝛾\𝑝 0 }
         5.                       {𝑝 0 Z⇒ L, 𝑝𝑙 , 𝑝𝑟 ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0 }
                                   tmp1 := 𝑝.𝑟 ; 𝑡𝑚𝑝 2 := 𝑝.𝑙; 𝑝.𝑟 := tmp2 ; 𝑝.𝑙 := 𝑡; 𝑝.𝑚 := R; 𝑡 := tmp1 ;
         6.                       {𝑝 0 Z⇒ R, 𝑡 0, 𝑝𝑙 ∧ 𝑡 = 𝑝𝑟 ∧ 𝑝 = 𝑝 0 }
32                                                        Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


        7.               {(𝑝 0 Z⇒ R, 𝑡 0, 𝑝𝑙 ∧ 𝑡 = 𝑝𝑟 ∧ 𝑝 = 𝑝 0 ) ∗ graph 𝛾\𝑝 0 }
        8.               {graph (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 ) ∧ 𝑡 = 𝑝𝑟 ∧ 𝑝 = 𝑝 0 }
        9.         {graph (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 ) ∧ 𝑡 = 𝑝𝑟 ∧ 𝑝 = 𝑝 0
                    ∧inv 𝛾 0 𝛾 𝑡 0 𝑝 0 ∧ 𝑡 0 ∈ marked0 𝛾 ∧ 𝛾 𝑝 0 = ( L, [𝑝𝑙 , 𝑝𝑟 ])}
      10.    {∃𝛾 ′ . graph 𝛾 ′ ∧ inv 𝛾 0 𝛾 ′ 𝑡 𝑝}
   Line 9 implies line 10. As for the case of POP, this step involves reformulating it as an implica-
tion, where initial and final values of the graph, stack and nodes 𝑡 and 𝑝 are made explicit.


                                            𝛾 = 𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 ∧                               (26)
                                                 ′
                                            inv 𝛾 0 𝛾 𝛼 𝑡 0 𝑝 0 ∧                                               (27)
                                            𝑡 0 ∈ marked0 𝛾 =⇒                                                  (28)
                                        ′    ′
                                     ∃𝛾 . 𝛾 = 𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 ∧                                 (29)
                                                 ′    ′
                                            inv 𝛾 0 𝛾 𝛼 𝑝𝑟 𝑝 0                                                  (30)
   SWING differs from the other two operations in that the stack remains unaltered. Furthermore,
because we know 𝑝 0 ≠ null, uniq (null • 𝛼) and 𝑝 0 = last (null • 𝛼) it follows that 𝛼 = 𝛼 ′ • 𝑝 0 for
some sequence 𝛼 ′ . The invariant (𝑎) 𝑝𝑟 ∈ nodes0 𝛾 ′ follows from (26) and (27) as we know that
𝑝𝑟 ∈ sinks 𝛾, closed 𝛾 and nodes0 𝛾 = nodes0 𝛾 ′ .
             (𝑏) sinks 𝛾 ′ =                                                        Def. of 𝛾 ′
             = sinks (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 )                             Lem. 3.1 (6) (distrib.)
             = sinks (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ])) ∪ sinks (𝛾\𝑝 0 )                     Def. of sinks (11)
             = {𝑡 0, 𝑝𝑙 } ∪ sinks (𝛾\𝑝 0 )                                          Set inclusion
             ⊆ {𝑡 0, 𝑝𝑙 , 𝑝𝑟 } ∪ sinks (𝛾\𝑝 0 )                                     Assump. (27) & (28)
             ⊆ nodes0 𝛾                                                             Def. of nodes
                          ′
             = nodes0 𝛾

             (𝑐) 𝑛𝑜𝑑𝑒𝑠 𝛾 ′ /L,R =                                                   Def. of 𝛾 ′
             = nodes (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 )/L,R                         Lem. 3.1 (1) (distrib.)
             = nodes (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]))/L,R ∪· nodes (𝛾\𝑝 0 )/L,R            Def. of filter (10)
             = nodes (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ])) ∪· nodes (𝛾\𝑝 0 )/L,R                Def. of nodes
             = {𝑝 0 } ∪· nodes (𝛾\𝑝 0 )/L,R                                         Def. of nodes
             = nodes (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ])) ∪· nodes (𝛾\𝑝 0 )/L,R                Def. of filter (10)
             = nodes (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]))/L,R ∪· nodes (𝛾\𝑝 0 )/L,R            Lem. 3.1 (1) (distrib.)
             = nodes (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 )/L,R                         Assump. (27)
             =𝛼

             (𝑑) inset 𝛼 𝛾 ′ =                                                      Def. of 𝛾 ′
             = inset 𝛼 (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 )                           Lem. 3.1 (5) (distrib.)
             = inset 𝛼 (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ])) • inset 𝛼 𝛾\𝑝 0                    Def. of inset (14)
             = 𝑝 0 ↦→ [𝑡 0, prev (null • 𝛼) 𝑝 0 ] • inset 𝛼 𝛾\𝑝 0                   Assump. (27)
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)        33


              = 𝑝 0 ↦→ [𝑡 0, 𝑝𝑙 ] • |𝛾\𝑝 0 |                                    Def. of erasure (8)
              = |𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ])| • |𝛾\𝑝 0 |                            Lem. 3.1 (4) (distrib.)
              = |𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 |                              Def. of 𝛾 ′
              = |𝛾 ′ |

             (𝑒) restore 𝛼 𝑝𝑟 𝛾 ′ =                                             Def. of 𝛾 ′
              = restore 𝛼 𝑝𝑟 (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 )                 Lem. 3.1 (5) (distrib.)
              = restore 𝛼 𝑝𝑟 (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ])) • restore 𝛼 𝑝𝑟 𝛾\𝑝 0     Def. of restore (15)
              = 𝑝 0 ↦→ [𝑡 0, next (𝛼 • 𝑝𝑟 ) 𝑝 0 ] • restore 𝛼 𝑝𝑟 𝛾\𝑝 0          Assump. (27)
              = 𝑝 0 ↦→ [𝑡 0, 𝑝𝑟 ] • restore 𝛼 𝑝𝑟 𝛾\𝑝 0                          Lem. 17
              = 𝑝 0 ↦→ [𝑡 0, 𝑝𝑟 ] • restore 𝛼 𝑡 0 𝛾\𝑝 0                         Def. of restore (15)
              = restore 𝛼 𝑡 0 (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ])) • restore 𝛼 𝑡 0 𝛾\𝑝 0   Lem. 3.1 (5) (distrib.)
              = restore 𝛼 𝑡 0 (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 )                Def. of 𝛾
              = restore 𝛼 𝑡 0 𝛾                                                 Assump. (27)
              = |𝛾 0 |

             (𝑓 ) nodes 𝛾 ′ /O =                                                Def. of 𝛾 ′
              = nodes (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]) • 𝛾\𝑝 0 )/O                      Lem. 3.1 (3) (distrib.)
              = nodes ((𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]))/O • (𝛾\𝑝 0 )/O )               Lem. 3.1 (1) (distrib.)
              = nodes (𝑝 0 ↦→ ( R, [𝑡 0, 𝑝𝑙 ]))/O ∪· nodes (𝛾\𝑝 0 )/O           Def. of filter (10)
              = nodes 𝑒 ∪· nodes (𝛾\𝑝 0 )/O                                     Def. of filter (10)
              = nodes (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]))/O ∪· nodes (𝛾\𝑝 0 )/O           Lem. 3.1 (1) (distrib.)
              = nodes ((𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]))/O • (𝛾\𝑝 0 )/O )               Lem. 3.1 (3) (distrib.)
              = nodes (𝑝 0 ↦→ ( L, [𝑝𝑙 , 𝑝𝑟 ]) • 𝛾\𝑝 0 )/O                      Def. of 𝛾
              = nodes 𝛾/O                                                       Assump. (27)
                 Ð
              ⊆          (reach 𝛾/O ◦ 𝛾𝑟 ) ∪ reach 𝛾/O 𝑡 0                      𝑡 0 ∉ nodes 𝛾/O
                𝛼 ′ ·𝑝 0
                 Ð
              =         (reach 𝛾/O ◦ 𝛾𝑟 )                                       Comm.&Assoc. of ∪
                  𝛼 ′ ·𝑝 0
                                                                                𝛾/O = 𝛾 ′ /O
                  Ð
              =        (reach 𝛾/O ◦ 𝛾𝑟 ) ∪ reach 𝛾/O 𝑝𝑟
                  𝛼′
                       (reach 𝛾 ′ /O ◦ 𝛾𝑟 ) ∪ reach 𝛾 ′ /O 𝑝𝑟                   𝛾𝑟 = 𝛾𝑟′ on 𝛼 ′
                  Ð
              =
                  𝛼′
                 (reach 𝛾 ′ /O ◦ 𝛾𝑟′ ) ∪ reach 𝛾 ′ /O 𝑝𝑟                        𝛾𝑟′ 𝑝 0 ∉ nodes 𝛾 ′ /O
                  Ð
              =
                  𝛼′
                   (reach 𝛾 ′ /O ◦ 𝛾𝑟′ ) ∪ reach 𝛾 ′ /O 𝑝𝑟
                Ð
              =
                  𝛼 ′ ·𝑝 0

D    Proof for PUSH
The pre- and postcondition for PUSH derive from lines 23 and 25 of Fig. 10.

                                   {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∉ marked0 𝛾 }
                                                        PUSH                                              (31)
                                           {∃𝛾 ′ . graph 𝛾 ′ ∧ inv 𝛾 0 𝛾 ′ 𝑡 𝑝}
34                                                              Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


The precondition says that the heap implements a well-formed graph 𝛾, that satisfies the invariant
and 𝑡 is an unmarked node different from null. The postcondition asserts that the heap represents
a new graph 𝛾 ′ that satisfies the invariant for the updated values of 𝑡 and 𝑝.

                    1.       {∃𝛾 . graph 𝛾 ∧ inv 𝛾 0 𝛾 𝑡 𝑝 ∧ 𝑡 ∉ marked0 𝛾 }
                    2.               {graph 𝛾 ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0
                                      ∧inv 𝛾 0 𝛾 𝑡 0 𝑝 0 ∧ 𝛾 𝑡 0 = ( O, [𝑡𝑙 , 𝑡𝑟 ])}
                    3.                     {graph (𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ]) • 𝛾\𝑡 0 ) ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0 }
                    4.                     {(𝑡 0 Z⇒ O, 𝑡𝑙 , 𝑡𝑟 ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0 ) ∗ graph 𝛾\𝑡 0 }
                    5.                            {𝑡 0 Z⇒ O, 𝑡𝑙 , 𝑡𝑟 ∧ 𝑡 = 𝑡 0 ∧ 𝑝 = 𝑝 0 }
                                                   tmp := 𝑡 .𝑙; 𝑡 .𝑙 := 𝑝; 𝑡 .𝑚 := L; 𝑝 := 𝑡; 𝑡 := tmp;
                    6.                            {𝑡 0 Z⇒ L, 𝑝 0, 𝑡𝑟 ∧ 𝑡 = 𝑡𝑙 ∧ 𝑝 = 𝑡 0 }
                    7.                     {(𝑡 0 Z⇒ L, 𝑝 0, 𝑡𝑟 ∧ 𝑡 = 𝑡𝑙 ∧ 𝑝 = 𝑡 0 ) ∗ graph 𝛾\𝑡 0 }
                    8.                     {graph (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 ) ∧ 𝑡 = 𝑡𝑙 ∧ 𝑝 = 𝑡 0 }
                    9.               {graph (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 ) ∧ 𝑡 = 𝑡𝑙 ∧ 𝑝 = 𝑡 0
                                      ∧inv 𝛾 0 𝛾 𝑡 0 𝑝 0 ∧ 𝛾 𝑡 0 = ( O, [𝑡𝑙 , 𝑡𝑟 ])}
                   10.       {∃𝛾 . graph 𝛾 ′ ∧ inv 𝛾 0 𝛾 ′ 𝑡 𝑝}
                                 ′


     Line 9 implies line 10. Proving this last step corresponds to proving the following implication.
                                                  𝛾 = 𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ]) • 𝛾\𝑡 0 ∧                               (32)
                                                       ′
                                                  inv 𝛾 0 𝛾 𝛼 𝑡 0 𝑝 0 =⇒                                              (33)
                                              ′    ′
                                           ∃𝛾 . 𝛾 = 𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 ∧                                 (34)
                                                       ′    ′
                                                  inv 𝛾 0 𝛾 (𝛼 • 𝑡 0 ) 𝑡𝑙 𝑡 0                                         (35)
    Proving invariant (𝑎) requires showing that (32) and (33) imply uniq (null •𝛼 •𝑡 0 ), 𝑡 0 = last (null •
𝛼 • 𝑡 0 ) and 𝑡𝑙 ∈ nodes0 𝛾 ′ . From 𝛾𝑚 𝑡 0 = O and nodes 𝛾/L,R = 𝛼 it follows uniq (null • 𝛼 • 𝑡 0 ). By 32
it follows 𝑡𝑙 ∈ sinks 𝛾. Then closed 𝛾 implies that 𝑡𝑙 ∈ nodes0 𝛾. And finally nodes0 𝛾 = nodes0 𝛾 ′ so
𝑡𝑙 ∈ nodes0 𝛾 ′ .

            (𝑏) sinks 𝛾 ′ =                                                                 Def. of 𝛾 ′
            = sinks (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 )                                      Lem. 3.1 (6) (distrib.)
            = sinks (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ])) ∪ sinks (𝛾\𝑡 0 )                              Def. of sinks (11)
            = {𝑝 0, 𝑡𝑟 } ∪ sinks (𝛾\𝑡 0 )                                                   Set inclusion
            ⊆ {𝑝 0, 𝑡𝑙 , 𝑡𝑟 } ∪ sinks (𝛾\𝑡 0 )                                              Assump. (33)
            ⊆ nodes0 𝛾                                                                      Def. of nodes
                         ′
            = nodes0 𝛾

            (𝑐) 𝑛𝑜𝑑𝑒𝑠 𝛾 ′ /L,R =                                                            Def. of 𝛾 ′
            = nodes (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 )/L,R                                  Lem. 3.1 (3) (distrib.)
            = nodes ((𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]))/L,R • (𝛾\𝑡 0 )/L,R )                         Def. of filter (10)
            = nodes (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • (𝛾\𝑡 0 )/L,R )                               Lem. 3.1 (1) (distrib.)
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)            35


            = nodes (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ])) ∪· nodes (𝛾\𝑡 0 )/L,R                  Def. of nodes
            = {𝑡 0 } ∪· nodes (𝛾\𝑡 0 )/L,R                                           Def. of filter (10)
            = {𝑡 0 } ∪· nodes (𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ]) • 𝛾\𝑡 0 )/L,R                 Def. of 𝛾
            = {𝑡 0 } ∪· nodes 𝛾/L,R                                                  Assump. (33)
            = {𝑡 0 } ∪· 𝛼                                                            Set equality
            = (𝛼 • 𝑡 0 )

           (𝑑) inset (𝛼 • 𝑡 0 ) 𝛾 ′ =                                                Def. of 𝛾 ′
            = inset (𝛼 • 𝑡 0 ) (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 )                    Lem. 3.1 (5) (distrib.)
            = inset (𝛼 • 𝑡 0 ) (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ])) • inset (𝛼 • 𝑡 0 ) 𝛾\𝑡 0    Def. of inset (14)
            = 𝑡 0 ↦→ [prev (null • 𝛼 • 𝑡 0 ) 𝑡 0, 𝑡𝑟 ] • inset (𝛼 • 𝑡 0 ) 𝛾\𝑡 0      Assump. (33)
            = 𝑡 0 ↦→ [𝑝 0, 𝑡𝑟 ] • inset (𝛼 • 𝑡 0 ) 𝛾\𝑡 0                             Lem. 16
            = 𝑡 0 ↦→ [𝑝 0, 𝑡𝑟 ] • inset 𝛼 𝛾\𝑡 0                                      Def. of erasure (8)
            = |𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ])| • |𝛾\𝑡 0 |                                   Lem. 3.1 (4) (distrib.)
            = |𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 |                                     Def. of 𝛾 ′
                 ′
            = |𝛾 |

           (𝑒) restore (𝛼 • 𝑡 0 ) 𝑡𝑙 𝛾 ′ =                                           Def. of 𝛾 ′
            = restore (𝛼 • 𝑡 0 ) 𝑡𝑙 (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 )               Lem. 3.1 (5) (distrib.)
            = restore (𝛼 • 𝑡 0 ) 𝑡𝑙 (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]))
                     • restore (𝛼 • 𝑡 0 ) 𝑡𝑙 𝛾\𝑡 0                                   Def. of restore (15)
            = 𝑡 0 ↦→ [next (𝛼 • 𝑡 0 • 𝑡𝑙 ) 𝑡 0, 𝑡𝑟 ] • restore (𝛼 • 𝑡 0 ) 𝑡𝑙 𝛾\𝑡 0   Assump. (33)
            = 𝑡 0 ↦→ [𝑡𝑙 , 𝑡𝑟 ] • restore (𝛼 • 𝑡 0 ) 𝑡𝑙 𝛾\𝑡 0                        Lem. 17
            = 𝑡 0 ↦→ [𝑡𝑙 , 𝑡𝑟 ] • restore 𝛼 𝑡 0 𝛾\𝑡 0                                Def. of restore (15)
            = restore 𝛼 𝑡 0 (𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ]))
                     • restore 𝛼 𝑡 0 𝛾\𝑡 0                                           Lem. 3.1 (5) (distrib.)
            = restore 𝛼 𝑡 0 (𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ]) • 𝛾\𝑡 0 )                       Def. of 𝛾
            = restore 𝛼 𝑡 0 𝛾                                                        Assump. (33)
            = |𝛾 0 |

           (𝑓 ) nodes 𝛾 ′ /O =                                                       Def. of 𝛾 ′
            = nodes (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]) • 𝛾\𝑡 0 )/O                             Lem. 3.1 (3) (distrib.)
            = nodes ((𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]))/O • (𝛾\𝑡 0 )/O )                      Lem. 3.1 (1) (distrib.)
            = nodes (𝑡 0 ↦→ ( L, [𝑝 0, 𝑡𝑟 ]))/O ∪· nodes (𝛾\𝑡 0 )/O                  Def. of filter (10)
            = nodes 𝑒 ∪· nodes (𝛾\𝑡 0 )/O                                            Def. of nodes
            = nodes (𝛾\𝑡 0 )/O                                                       Set difference
            = ({𝑡 0 } ∪· nodes (𝛾\𝑡 0 )/O )\𝑡 0                                      Def. of nodes
            = (nodes (𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ])) ∪· nodes (𝛾\𝑡 0 )/O )\𝑡 0             Def. of filter (10)
            = (nodes (𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ]))/O ∪· nodes (𝛾\𝑡 0 )/O )\𝑡 0           Lem. 3.1 (1) (distrib.)
36                                                                  Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


             = (nodes (𝑡 0 ↦→ ( O, [𝑡𝑙 , 𝑡𝑟 ]) • 𝛾\𝑡 0 )/O )\𝑡 0                                       Def. of 𝛾
             = (nodes 𝛾/O )\𝑡 0                                            Assump. (33)
                Ð
             ⊆ ( (reach 𝛾/O ◦ 𝛾𝑟 ) ∪ reach 𝛾/O 𝑡 0 )\𝑡 0                   Lem. 3.4 (2) & 3.4 (3)
                 𝛼
                Ð
             = ( (reach (𝛾/O )\𝑡 0 ◦ 𝛾𝑟 ) ∪ reach 𝛾/O 𝑡 0 )\𝑡 0            Def. of reach (13)
                𝛼
                Ð                                    Ð
             = ( (reach (𝛾/O )\𝑡 0 ◦ 𝛾𝑟 ) ∪ {𝑡 0 } ∪     reach (𝛾/O ))\𝑡 0 Set difference
                     𝛼                                                {𝑡𝑙 ,𝑡𝑟 }
                                                                                                       (𝛾/O )\𝑡 0 = 𝛾 ′ /O
                 Ð                                        Ð
             =       (reach (𝛾/O )\𝑡 0 ◦ 𝛾𝑟 ) ∪                    reach (𝛾/O )\𝑡 0
                 𝛼                                     {𝑡𝑙 ,𝑡𝑟 }
                     (reach 𝛾 ′ /O ) ◦ 𝛾𝑟 ) ∪                 reach 𝛾 ′ /O                             𝛾𝑟 = 𝛾𝑟′ on (𝛼 • 𝑡 0 )
                 Ð                                  Ð
             =
                 𝛼                                {𝑡𝑙 ,𝑡𝑟 }
                            (reach 𝛾 ′ /O ◦ 𝛾𝑟′ ) ∪ reach 𝛾 ′ /O 𝑡𝑙
                     Ð
             =
                 (𝛼•𝑡 0 )

E Union-Find Data Structure
E.1 Non-spatial definitions
                                                                                     Ð
                                                       = {𝑥 | 𝑥 ∈
                                              cycles 𝛾 b                                       reach 𝛾 𝑦}
                                                                                  𝑦 ∈𝛾 adj 𝑥

                                                      = cycles 𝛾 ⊆ loops 𝛾
                                         preacyclic 𝛾 b
                                                      = (sinks 𝛾)\nodes 𝛾
                                             dangls 𝛾 b
The function cycles computes the set of nodes that constitute a cycle in the graph. More precisely,
it identifies nodes that are reachable from one of their adjacent nodes. This avoids the trivial case
where every node is reachable from itself. Loops are cycles of size one—that is, nodes that explicitly
include themselves in their adjacency list. Then a preacyclic graph is one where every cycle is of
size one. Loops are given a special status as they are cycles that do not break under decomposition.
dangls 𝛾 selects the dangling nodes of a graph, those that are pointed at by a node in the graph but
are not themselves in the graph. Notice that null may be in this set.
     Lemma E.1 (Union-find abstractions).
      (1) dangls (𝛾 1 • 𝛾 2 ) = (dangls 𝛾 1 )\nodes 𝛾 2 ∪ (dangls 𝛾 2 )\nodes 𝛾 1
      (2) loops 𝛾 ⊆ cycles 𝛾 ⊆ nodes 𝛾
      (3) dangls 𝛾 ∩ nodes 𝛾 = ∅
    Lemma E.2 (Summit characterization). Let 𝛾 be a graph and 𝑥 ∈ nodes 𝛾. Then, 𝑧 ∈ summit 𝛾 𝑥
iff there exists a path from 𝑥 to 𝑦 in 𝛾 such that 𝑧 is a child of 𝑦, and either 𝑧 ∉ nodes 𝛾 (i.e., the edge
from 𝑦 to 𝑧 is dangling) or 𝑧 is already in the path from 𝑥 to 𝑦.
     Lemma E.3 (Summits).
      (1) summits 𝛾 = cycles 𝛾 ∪· dangls 𝛾
      (2) If summits 𝛾 1 = summits 𝛾 2 then summits (𝛾 1 • 𝛾 2 ) = summits 𝛾 1
      (3) If 𝑥 ∈ loops 𝛾 then summits 𝛾\𝑥 ⊆ summits 𝛾
   Lemma E.4 (Summits of inverted forest). Let 𝛾 = (𝛾 1 •𝛾 2 ) be an an inverted forest (summits 𝛾 ⊆
loops 𝛾) then
    (1) sinks 𝛾 ⊆ nodes 𝛾 (closed 𝛾)
    (2) cycles 𝛾 ⊆ loops 𝛾 (preacyclic 𝛾)
    (3) summits (𝛾 1 • 𝛾 2 ) = (summits 𝛾 1 )\nodes 𝛾 2 ∪· (summits 𝛾 2 )\nodes 𝛾 1
    (4) summit 𝛾 𝑥 = summit 𝛾 (𝛾 𝑥)
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)   37


  Lemma E.5 (Preacyclic mutation). Let 𝛾 be a unary graph such that preacyclic 𝛾, and 𝑥 ∈ nodes 𝛾
and 𝑦 ∉ nodes 𝛾. The graph 𝛾 ′ obtained by modifying 𝑥’s successor to 𝑦, also satisfies preacyclic 𝛾 ′ .

E.2    Proof outline for NEW
  1.   {emp}
  2. 𝑝 := alloc null;
  3.   {𝑝 Z⇒ null}
  4. 𝑝.𝑛𝑒𝑥𝑡 := 𝑝;
  5.   {𝑝 Z⇒ 𝑝}
  6.   return 𝑝
  7.   {𝑝 Z⇒ 𝑝 ∧ result = 𝑝}
       
  8.     graph1 (𝑝 ↦→ 𝑝) ∧ summits (𝑝 ↦→ 𝑝) = loops (𝑝 ↦→ 𝑝) = nodes (𝑝 ↦→ 𝑝) = {𝑝} ∧ result = 𝑝
       
  9.     ∃𝛾 . graph1 𝛾 ∧ summits 𝛾 = loops 𝛾 = {𝑝} ∧ nodes 𝛾 = {𝑝} ∧ result = 𝑝
10.    {set {result} result}
 The first two commands are standard separation logic, the third command in line 6 corresponds to
a value returning function supported by Hoare Type Theory. The step from line 7 to line 8 lifts the
reasoning from the heap to the abstract graph and establishes that the singleton graph is indeed an
inverted tree with result as its representative. Finally the conjunct are folded into the set predicate.

E.3    Proof outline for FIND
        1.   {set 𝑆 𝑦 ∧ 𝑥 ∈ 𝑆 }
             
        2.     ∃𝛾 . graph1 𝛾 ∧ summits 𝛾 = loops 𝛾 = {𝑦} ∧ nodes 𝛾 = 𝑆 ∧ 𝑥 ∈ 𝑆
                
        3.        graph1 𝛾 ∧ summits 𝛾 = loops 𝛾 = {𝑦} ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 = 𝑆 ∧ 𝑥 ∈ 𝑆
                
        4.        graph1 (𝑥 ↦→ 𝛾 𝑥 • 𝛾\𝑥) ∧ 𝑥 ∈ 𝑆 ∧ summits 𝛾 = loops 𝛾 = {𝑦} ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 = 𝑆
                    
        5.           𝑥 Z⇒ 𝛾 𝑥 ∗ graph1 𝛾\𝑥 ∧ 𝑥 ∈ 𝑆
        6.         𝑝 := 𝑥 .𝑛𝑒𝑥𝑡;
                   
        7.          𝑥 Z⇒ 𝛾 𝑥 ∗ graph1 𝛾\𝑥 ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥
                   
        8.           graph1 (𝑥 ↦→ 𝛾 𝑥 • 𝛾\𝑥) ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥
                   
        9.           graph1 𝛾 ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥
       10.         while 𝑝 ≠ 𝑥 do
                    
       11.            graph1 𝛾 ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥 ≠ 𝑥
       12.            𝑥 := 𝑝;
                      
       13.              graph1 𝛾 ∧ 𝑥 ∈ 𝑆 ∧ 𝑥 = 𝑝
                      
       14.              graph1 (𝑥 ↦→ 𝛾 𝑥 • 𝛾\𝑥) ∧ 𝑥 ∈ 𝑆 ∧ 𝑥 = 𝑝
                      
       15.             𝑥 Z⇒ 𝛾 𝑥 ∗ graph1 𝛾\𝑥 ∧ 𝑥 ∈ 𝑆 ∧ 𝑥 = 𝑝
       16.            𝑝 := 𝑥 .𝑛𝑒𝑥𝑡;
                      
       17.             𝑥 Z⇒ 𝛾 𝑥 ∗ graph1 𝛾\𝑥 ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥
                      
       18.              graph1 (𝑥 ↦→ 𝑛𝑥 • 𝛾\𝑥) ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥
38                                                              Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov

                        
      19.                   graph1 𝛾 ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥
      20.             end while
                      
      21.               graph1 𝛾 ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥 = 𝑥
      22.             return 𝑥
                      
      23.               graph1 𝛾 ∧ 𝑥 ∈ 𝑆 ∧ 𝑝 = 𝛾 𝑥 = 𝑥 = result
                 
      24.            graph1 𝛾 ∧ result = 𝑦 ∧ summits 𝛾 = loops 𝛾 = {𝑦} ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 = 𝑆
            
      25.       ∃𝛾 . graph1 𝛾 ∧ summits 𝛾 = loops 𝛾 = {𝑦} ∧ nodes 𝛾 = 𝑆 ∧ result = 𝑦
      26.   {set 𝑆 𝑦 ∧ result = 𝑦}
   The first five lines of the proof outline unfold the spatial predicates, first set, then graph, to
reveal the node corresponding to the argument 𝑥. The non-spatial conjuncts involving 𝛾 and 𝑦
are framed early on, as these values remain unchanged throughout the execution and will later be
reintroduced without modification. The command at line 6 assigns to 𝑝 the successor of 𝑥. In line
10, 𝑝 is compared to 𝑥. A mismatch implies that the root node, which points to itself, has not yet
been found, and thus the loop must be entered. Within the loop, the first command advances 𝑥
to its parent node. Line 13 requires showing that the new value of 𝑥 remains within 𝑆. This holds
because 𝑥 is guaranteed to be in nodes 𝛾, given that closed 𝛾 holds by lemma E.4 (1) and nodes 𝛾 = 𝑆.
Next, 𝑝 is updated to be the parent of the current 𝑥. By the end of the loop in line 19, its invariant
from line 9 is reestablished. When the loop terminates, the invariant together with the negation of
the loop guard leads to the conclusion in line 21: 𝑥 is a node in 𝑆 and points to itself in 𝛾. Line 22
sets the result of the program to be x, which by the non-spatial conjunct framed at the beginning
we know must be 𝑦, as it is established to be the only self-pointing node in 𝛾.

E.4   Proof outline for UNION
                            1.   {set 𝑆 1 𝑥 1 ∗ set 𝑆 2 𝑥 2 }
                            2.      {graph1 𝛾 1 ∗ graph1 𝛾 2
                            3.        ∧ summits 𝛾 1 = loops 𝛾 1 = {𝑥 1 } ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 1 = 𝑆 1
                            4.        ∧ summits 𝛾 2 = loops 𝛾 2 = {𝑥 2 } ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 2 = 𝑆 2 }
                                       
                            5.           graph1 (𝑥 1 ↦→ 𝑥 1 • 𝛾 1 \𝑥 1 )
                                       
                            6.          𝑥 1 Z⇒ 𝑥 1 ∗ graph1 (𝛾 1 \𝑥 1 )
                            7.         𝑥 1 .𝑛𝑒𝑥𝑡 := 𝑥 2 ;
                                       
                            8.           𝑥 1 Z⇒ 𝑥 2 ∗ graph1 (𝛾 1 \𝑥 1 )
                            9.         return 𝑥 2
                                       
                        10.             𝑥 1 Z⇒ 𝑥 2 ∗ graph1 (𝛾 1 \𝑥 1 ) ∧ result = 𝑥 2
                                       
                        11.              graph1 (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) ∧ result = 𝑥 2
                        12.         {graph1 (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) ∧ result = 𝑥 2 ∗ graph1 𝛾 2
                        13.           ∧ summits 𝛾 1 = loops 𝛾 1 = {𝑥 1 } ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 1 = 𝑆 1
                        14.           ∧ summits 𝛾 2 = loops 𝛾 2 = {𝑥 2 } ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 2 = 𝑆 2 }
                        15.         {graph1 (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) ∗ graph1 𝛾 2 ∧ result = 𝑥 2
                        16.           ∧ summits (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) = {𝑥 2 }
                        17.           ∧ loops (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) = ∅
Verifying Graph Algorithms in Separation Logic: A Case for an Algebraic Approach (Extended Version)         39


                      18.         ∧ 𝑛𝑜𝑑𝑒𝑠 (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) = 𝑆 1
                      19.         ∧ summits 𝛾 2 = loops 𝛾 2 = {𝑥 2 } ∧ 𝑛𝑜𝑑𝑒𝑠 𝛾 2 = 𝑆 2 }
                      20.       {graph1 (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 • 𝛾 2 ) ∧ result = 𝑥 2
                      21.         ∧ summits (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 • 𝛾 2 ) = {𝑥 2 }
                      22.         ∧ loops (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 • 𝛾 2 ) = {𝑥 2 }
                      23.         ∧ 𝑛𝑜𝑑𝑒𝑠 (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 • 𝛾 2 ) = 𝑆 1 • 𝑆 2 }
                      24.    {set (𝑆 1 • 𝑆 2 ) result ∧ result ∈ {𝑥 1, 𝑥 2 }}



   Similar to the FIND proof, the initial lines of the proof outline (lines 1-6) unfold the spatial
predicates isolating the node corresponding to the argument 𝑥 1 . Line 2 unfolds the set predicate,
instantiates the existentially quantified graphs as 𝛾 1 and 𝛾 2 and frames out graph1 𝛾 2 as well as the
non-spatial facts about the initial disjoint graphs. Line 5 rewrites by the equality 𝛾 1 = 𝑥 1 ↦→ 𝑥 1 •𝛾 1 \𝑥 1
which follows from 𝑥 1 ∈ loops 𝛾 1 . The command in line 7 makes 𝑥 1 point to 𝑥 2 . The second and
final command sets 𝑥 2 as the result of the program. After the final command, in line 11 reasoning
is lifted from the heap level and in line 12 the spatial conjuncts initially framed are reintroduced.
In line 15 the abstractions that constitute the specification are recomputed for the mutated graph
𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 , exploiting their distributivity. Before applying the distributivity of summits,
preacyclicity is proved for the mutated graph by application of lemma E.5.



   summits (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) =
      = (summits (𝑥 1 ↦→ 𝑥 2 ))\nodes (𝛾 1 \𝑥 1 )                Distrib. of summits
      ∪ (summits 𝛾 1 \𝑥 1 )\nodes (𝑥 1 ↦→ 𝑥 2 )
      = {𝑥 2 }\nodes (𝛾 1 \𝑥 1 ) ∪ (summits 𝛾 1 \𝑥 1 )\𝑥 1       Def. of summits and nodes
      = {𝑥 2 } ∪ (summits 𝛾 1 \𝑥 1 )\𝑥 1                         𝑥 2 ∈ nodes 𝛾 2 and
                                                                  nodes 𝛾 1 \𝑥 1 ∩ nodes 𝛾 2 = ∅
        = {𝑥 2 }                                                 Lem. E.3 (3) and Assump. in lines 12-14

   loops (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) =
       = loops (𝑥 1 ↦→ 𝑥 2 ) ∪· loops (𝛾 1 \𝑥 1 )                Distrib. of loops
       = loops (𝛾 1 \𝑥 1 )                                       Def. of loops
       =∅                                                        Assump. in lines 12-14

   nodes (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) =
      = nodes (𝑥 1 ↦→ 𝑥 2 ) ∪· nodes (𝛾 1 \𝑥 1 )                 Distrib. of nodes
      = {𝑥 } ∪· nodes (𝛾 1 \𝑥 1 )                                Def. of nodes
      = nodes (𝑥 1 ↦→ 𝑥 1 ) ∪· nodes (𝛾 1 \𝑥 1 )                 Def. of nodes
      = nodes (𝑥 1 ↦→ 𝑥 1 • 𝛾 1 \𝑥 1 )                           Distrib. of nodes
      = 𝑆1                                                       Assump. in lines 12-14



  The last step in the proof outline starting in line 20 is joining both subgraphs 𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1
and 𝛾 2 . Both loops and nodes use plain distributivity. In contrast, for summits, instead of proving
that the joined graph is preacyclic in order to apply distributivity, we exploit the fact that both
40                                                     Marcos Grandury, Aleksandar Nanevski, and Alexander Gryzlov


subgraphs have the same summits and apply lemma E.3 (2) directly.
                 loops (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 • 𝛾 2 ) =
                     = loops (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) ∪· loops 𝛾 2    Distrib. of loops
                     = {𝑥 2 }                                         Assump. in lines 12-14

                 nodes (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 • 𝛾 2 ) =
                    = nodes (𝑥 1 ↦→ 𝑥 2 • 𝛾 1 \𝑥 1 ) ∪· nodes 𝛾 2     Distrib. of nodes
                    = 𝑆 1 ∪· 𝑆 2                                      Assump. in lines 12-14
     The proof concludes in line 24 by folding the desired spatial predicate.
