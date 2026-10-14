                                         Precise Reasoning about Container-Internal Pointers
                                                        with Logical Pinning
                                                                    Yawen Guan                                                    Clément Pit-Claudel
                                                                        EPFL                                                              EPFL
                                                                Lausanne, Switzerland                                             Lausanne, Switzerland
                                                                 yawen.guan@epfl.ch                                            clement.pit-claudel@epfl.ch

                                        Abstract                                                                  1   Introduction
                                        Most separation logics hide container-internal pointers for               Separation logic [10, 24–26] is an extension of Hoare logic
                                        modularity. This makes it difficult to specify container APIs             for modular verification of pointer-manipulating programs.
                                        that temporarily expose those pointers to the outside, and                A central challenge in reasoning about such programs is
arXiv:2509.23229v2 [cs.PL] 5 Dec 2025




                                        to verify programs that use these APIs.                                   aliasing, since mutating a shared memory cell may affect the
                                           We present logical pinning, a lightweight borrowing model              value of syntactically unrelated expressions.
                                        for sequential programs that allows users to selectively track               Separation logic helps avoid this challenge by enabling
                                        container-internal pointers at the logical level. Our model               assertions over disjoint heap fragments using the separating
                                        generalizes the magic-wand operator for representing partial              conjunction operator ★, such that mutating a single memory
                                        data structures, making it easy to write and prove precise                cell in the heap affects only one ★-conjunct. The primitive
                                        specifications, including pointer-stability properties. Because           heap proposition in the logic is 𝑝 ↦→ 𝑣, asserting exclusive
                                        it only changes the way representation predicates and speci-              ownership (permission to access and mutate) of the cell at
                                        fications are written, our approach is compatible with most               location 𝑝 storing data 𝑣. A ★-conjunction like 𝑝 ↦→ 𝑣 ★ 𝑞 ↦→
                                        separation logic variants.                                                𝑢 ensures that 𝑝 and 𝑞 are not aliases: the ★ captures the
                                           We demonstrate the practicality of logical pinning by ver-             absence of sharing, enforcing non-aliasing by construction.
                                        ifying small but representative pointer-manipulating pro-                    In separation logic, mutable containers such as linked lists
                                        grams, and deriving more precise versions of common con-                  and trees are described using predicates, called representa-
                                        tainer specifications. In doing so, we show that our approach             tion predicates, which relate the container’s logical model
                                        subsumes some well-known proof patterns, simplifies some                  to a concrete heap representation. For modularity, most of
                                        complex proofs, and enables reasoning about program pat-                  them hide the container’s internal pointers and assert full
                                        terns not supported by traditional specifications. All of our             ownership of the container and its content.
                                        results are mechanized in the Rocq proof assistant, using the                For example, consider a linked list whose nodes are repre-
                                        CFML library.                                                             sented in C as:

                                        CCS Concepts: • Theory of computation → Separation                        struct lnode { elem x; struct lnode* next; };
                                        logic; Program verification.                                              Assume that the C type elem corresponds to the logical type
                                                                                                                  𝐴, and that the representation predicate 𝑅𝐴 𝑥 𝑝 asserts that
                                        Keywords: Representation predicates, Containers, Sharing
                                                                                                                  an element 𝑥 of type 𝐴 is stored at 𝑝. The typical representa-
                                                                                                                  tion predicate of such lists, List, can be defined as:
                                        ACM Reference Format:
                                        Yawen Guan and Clément Pit-Claudel. 2026. Precise Reasoning                List 𝑅𝐴 [] 𝑝 ≜ ⌊𝑝 = null⌋
                                        about Container-Internal Pointers with Logical Pinning. In Proceed-        List 𝑅𝐴 (𝑥 :: 𝑙) 𝑝 ≜ 𝑅𝐴 𝑥 𝑝 ★ ∃ 𝑞. 𝑝 + 1 ↦→ 𝑞 ★ List 𝑅𝐴 𝑙 𝑞
                                        ings of the 15th ACM SIGPLAN International Conference on Certified
                                        Programs and Proofs (CPP ’26), January 12–13, 2026, Rennes, France.       This asserts that the pointer 𝑝 is null when the list is empty,
                                        ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/3779031.        and otherwise the head 𝑥 is stored at location 𝑝 and a pointer
                                        3779096                                                                   𝑞 pointing to the tail 𝑙 is stored at 𝑝 + 1. The recursive use
                                                                                                                  of ★ enforces that all list nodes occupy disjoint heap frag-
                                                                                                                  ments. Such representations are convenient and effective
                                                                                                                  when the non-aliasing assumption holds, namely, that each
                                                                                                                  element is accessible only through a unique path rooted at
                                        This work is licensed under a Creative Commons Attribution 4.0 Interna-   the container’s entry point.
                                        tional License.
                                        CPP ’26, Rennes, France
                                                                                                                     Unfortunately, the non-aliasing assumption often breaks
                                        © 2026 Copyright held by the owner/author(s).                             down in practice: container interfaces and implementations
                                        ACM ISBN 979-8-4007-2341-4/2026/01                                        commonly expose internal pointers to elements (stored items)
                                        https://doi.org/10.1145/3779031.3779096                                   or substructures to the outside. Graphs are inherently built
CPP ’26, January 12–13, 2026, Rennes, France                                                      Yawen Guan and Clément Pit-Claudel


on sharing, whereas other containers expose internal point-         to be simplified, and enables verification of new program
ers only temporarily, either to client code or during internal      patterns. We conclude with related work in section 7.
operations such as tree rebalancing. In this work, we focus
                                                                    Contributions.
on containers with transient internal-pointer exposure, both
flat (e.g., arrays and records) and recursive (e.g., linked lists   • We introduce logical pinning, a model and proof discipline
and trees), and develop techniques for reasoning about them           for precise reasoning about exposed internal pointers in
in sequential programs written in pointer-manipulating lan-           containers.
guages such as C.                                                   • We showcase applications of the model in a series of case
   To illustrate the challenges concretely, consider the follow-      studies, covering containers ranging from single cells to
ing logger example, inspired by the APIs of the C++ logging           arrays, records, linked lists, and trees.
library spdlog [2] and rewritten in C for simplicity. A logger      • We show that logical-pinning enables maximally precise
is an object that maintains a configuration, such as log levels,      specifications for realistic APIs by specifying a realistic,
and directs messages to designated outputs. Applications              low-level API for linked lists.
often manage a dictionary of named loggers; in this example,        • We show that logical pinning is easy to implement in
registry is a pointer to such a dictionary, whose loggers             practice on top of existing separation logics by formalizing
can be updated individually or collectively.                          all of our examples using the CFML library.

1 struct logger* lgr = get(registry, k);                            2   Overview and Key Ideas
2 // spdlog::set_level                                              Many programming idioms require containers to temporarily
3 set_level_all(registry, INFO);                                    expose their internal pointers to the outside:
4 // spdlog::logger::set_level                                      • Pointer caching, to avoid repeated lookups in performance-
5 set_level(lgr, DEBUG);                                              critical code;
                                                                    • Direct manipulation, such as swapping two values stored
Line 1 retrieves a pointer to the logger associated with key          in a list after retrieving pointers to them;
k and stores it in variable lgr; line 3 sets the log level of all   • Transient cross-container sharing, such as binary-tree ro-
loggers in registry to INFO; and line 5 overrides the level           tation (fig. 1) where a subtree 𝑡𝑟𝑙 is temporarily shared
of the logger pointed to by lgr to DEBUG. This program is             between two trees.
safe because the implementation of set_level_all ensures
pointer stability: it updates loggers in place, so the pointer
lgr remains valid for use on line 5.
   Conceptually, set_level_all is a map operation that up-
dates all loggers in the dictionary. Let Dict 𝑑 𝑝 denote the
representation predicate for a dictionary 𝑑 stored at 𝑝, and
𝑔[lvl := 𝑣] denote the logger 𝑔 with its level substituted by 𝑣.
A typical specification of set_level_all is:                                  Figure 1. Left rotation of a binary tree.
∀ 𝑑 𝑝 𝑣. { Dict 𝑑 𝑝 } set_level_all(𝑝, 𝑣)
                                                                       Exposing internal pointers raises two challenges: (1) rea-
                     { 𝜆 _. Dict (map (𝜆 𝑔. 𝑔[lvl := 𝑣]) 𝑑) 𝑝 }
                                                                    soning about their validity under container operations, and
Unfortunately, this specification is insufficient to verify the     (2) supporting multiple borrows, where ownership of several
program: it does not capture pointer stability, and hence           subparts referenced by exposed pointers may be temporarily
permits implementations that relocate (move) loggers and            detached from the container for local reasoning. Existing
invalidate exposed internal pointers such as lgr.                   approaches, such as magic wands, fall short on resolving
   Existing approaches fall short on verifying this pattern         these challenges and are discussed further in section 3.
for various reasons (section 3). In this paper, we introduce a
logical-pinning model for reasoning about exposed internal          2.1 Key Idea: Capture Pointer Stability with a Precise
pointers, together with a proof discipline in which the user se-        Classification of Writes
lectively exposes such pointers in the logical representations      Pointer stability is a property of a container operation that
and precisely tracks pointer validity in API specifications.        ensures pointers to its subparts remain valid, i.e., the subparts
   Section 2 outlines the key ideas of our approach. Sec-           are neither deallocated nor relocated. This property allows
tion 3 discusses the limitations of existing state-of-the-art       clients to safely cache and reuse pointers across operations.
approaches. Section 4 presents the logical-pinning model and           The traditional read-write model, which broadly classifies
proof discipline. Sections 5 and 6 apply the model to a series      memory operations as reads and writes, is too coarse to
of containers and discuss the results, showing that it sub-         reason about pointer stability because it fails to distinguish
sumes existing ad hoc proof patterns, allows complex proofs         between fundamentally different types of writes:
Precise Reasoning about Container-Internal Pointers with Logical Pinning                           CPP ’26, January 12–13, 2026, Rennes, France


• In-place writes: Writes that perform in-place mutation,
   such as the set_level_all operation. They change the
   content without invalidating existing pointers.
• Full writes: Writes that may deallocate or relocate objects,
   such as resizing, rebalancing, or restructuring containers.
  They can invalidate previously exposed pointers.
Many container APIs (e.g., in C++ STL) explicitly document
whether an operation invalidates internal pointers [1]. Corre-
spondingly, we would like to capture in specifications which
kind of writes a function may perform. Consider a container
𝑐 consisting of four elements 𝑒 1 . . . 𝑒 4 , where only two inter-
nal pointers are exposed: 𝑝 1 to 𝑒 1 and 𝑝 3 to 𝑒 3 (left of fig. 2;
the right is discussed in section 4.3.3). For readability, we
          𝑅
write 𝑝 −
        → 𝑥 for application 𝑅 𝑥 𝑝 in figures. Conceptually,
any function 𝑓 that manipulates 𝑐 while promising to pre-
serve these exposed pointers must treat 𝑒 1 and 𝑒 3 as pinned
at their location, meaning 𝑓 may only perform reads and
in-place writes to them. In contrast, 𝑒 2 and 𝑒 4 are considered
floating; 𝑓 may perform full writes to them.
                        Logical Borrow

                  offered at                     borrowed at




                     offered at                     borrowed at



                        Logical Return


Figure 2. Two views of a container 𝑐 with elements 𝑒 1 . . . 𝑒 4
and exposed internal pointers 𝑝 1 and 𝑝 3 . Left: 𝑐 owns all
elements. Right: 𝑒 1 and 𝑒 3 are borrowed from 𝑐.
                                                                           Figure 3. An informal proof sketch of the functional correct-
                                                                           ness of the logger example. For simplicity, we assume the
2.2   Key Idea: Encode Representation Predicates as                        dictionary initially contains three key-logger pairs (𝑘 0, 𝑔0 ),
      Tagged Multi-Hole Contexts                                           (𝑘 1, 𝑔1 ) and (𝑘 2, 𝑔2 ), where 𝑘 = 𝑘 1 . Each step is annotated
In practice, programs often maintain multiple exposed point-               with the corresponding abstract heap state, denoted { state },
ers to container subparts (elements and substructures) rather              together with a brief informal explanation (shown in blue).
than just one. A simple example is the element-swapping                    [lgr] denotes an alias list with a single element lgr. Color
program which retrieves pointers to two list elements and                  markers: to change, just changed.
swaps their contents. When ownership of these subparts
is detached for local reasoning (i.e., these subparts are bor-
rowed), the container is left with multiple holes.
                                                                              This specification performs two logical steps at once: it
   Consider a key-value tree 𝑡 pointed to by 𝑝. The program
                                                                           records the subtree relation between 𝑞 1 and 𝑝, and transfers
below looks up potentially overlapping subtrees 𝑡 1 and 𝑡 2
                                                                           ownership of 𝑡 1 to 𝑞 1 . This ownership transfer is incompat-
rooted at keys 𝑘 1 and 𝑘 2 before passing them on to compare:
                                                                           ible with the second lookup, which requires 𝑝 to have full
1 struct tree* q1 = lookup(p, k1);                                         ownership of 𝑡.
2 struct tree* q2 = lookup(p, k2);                                            Our approach distinguishes these two steps: in it, the calls
3 compare(q1, q2);                                                         to lookup pin 𝑡 1 to 𝑞 1 and 𝑡 2 to 𝑞 2 without detaching them,
                                                                           and without changing the predicate used to represent 𝑡. Later,
   A typical specification for lookup(𝑝, 𝑘 1 ) requires the full           when separate ownership is needed to call compare, we add
ownership of 𝑡, and splits that ownership between 𝑡 1 (rooted              a logical borrowing step to detach 𝑡 1 and 𝑡 2 .
at 𝑞 1 ) and a partial tree rooted at 𝑝. This partial tree is often           To do so, we adopt a uniform representation for whole
represented using a custom predicate or a magic wand.                      and partial containers using tagged multi-hole contexts, in
CPP ’26, January 12–13, 2026, Rennes, France                                                         Yawen Guan and Clément Pit-Claudel


which each borrowable subpart is augmented with a fine-
                                                                          ⌊𝑃⌋ ≜ 𝜆 ℎ. ℎ = ∅ ∧ 𝑃
grained borrowing state that indicates whether the subpart
is pinned or floating, and whether the container still has its         𝑝 ↦→ 𝑣 ≜ 𝜆 ℎ. ℎ = (𝑝 → 𝑣) ∧ 𝑝 ≠ null
ownership. This allows precise specifications that support           𝐻 1 ★ 𝐻 2 ≜ 𝜆 ℎ. ℎ 1 ⊥ ℎ 2 ∧ ℎ 1 ⊎ ℎ 2 ∧ 𝐻 1 ℎ 1 ∧ 𝐻 2 ℎ 2
flexible pointer tracking and ownership transfers for indi-            ∃ 𝑥 . 𝐻 ≜ 𝜆 ℎ. ∃ 𝑥 . 𝐻 ℎ      ∀∀ 𝑥 . 𝐻 ≜ 𝜆 ℎ. ∀ 𝑥 . 𝐻 ℎ
vidual subparts without breaking the container abstraction.         𝐻 1 − 𝐻 2 ≜ ∃ 𝐻 . 𝐻 ★ ⌊(𝐻 1 ★ 𝐻 ) ⊢ 𝐻 2 ⌋




                                                                          ★
   This subtree-compare example is verified using our ap-                          where 𝐻 1 ⊢ 𝐻 2 ≜ ∀ ℎ. 𝐻 1 ℎ → 𝐻 2 ℎ
proach; the key to handling potential overlapping subtrees           𝐻1 ∧∧ 𝐻 2 ≜ 𝜆 ℎ. 𝐻 1 ℎ ∧ 𝐻 2 ℎ 𝐻 1 ∨   ∨ 𝐻 2 ≜ 𝜆 ℎ. 𝐻 1 ℎ ∨ 𝐻 2 ℎ
is the use of non-separating conjunction (section 3.1) in the
precondition of compare. See section A for details.                           Figure 4. Basic heap predicate combinators.
2.3   The Logger Example Revisited
                                                                    two disjoint parts satisfying 𝐻 1 and 𝐻 2 respectively. ∃ 𝑥 . 𝐻
Figure 3 presents an informal correctness proof of the logger       and ∀∀ 𝑥 . 𝐻 are existential and universal quantification over
example under our approach. The predicate Logger 𝑔 𝑝 as-            values in the heap (★ has higher precedence than ∃ and ∀∀).
serts that the logger 𝑔 is stored at 𝑝. We write specifications     The magic wand (separating implication), 𝐻 1 − 𝐻 2 , denotes




                                                                                                                         ★
with implicit universal quantification over free variables (e.g.,   a heap that, when extended with any heap satisfying 𝐻 1 ,
𝑔, 𝑝, 𝑣 below). The specification of set_level is:                  yields a heap satisfying 𝐻 2 . The non-separating conjunction
{ Logger 𝑔 𝑝 } set_level(𝑝, 𝑣) { 𝜆 _. Logger 𝑔[lvl := 𝑣] 𝑝 }        𝐻1 ∧∧ 𝐻 2 asserts that the heap satisfies 𝐻 1 and 𝐻 2 , while the
We tag each logger in the dictionary with one of the four           disjunction 𝐻 1 ∨∨ 𝐻 2 asserts it satisfies at least one of them.
borrowing states: Owned, Offered, Borrowed or Missing. We              We specify programs using Hoare triples of the form
refine the specification of get to mark the returned pointer        { 𝐻 } 𝑒 { 𝜆 𝑣. 𝑄 𝑣 } where 𝑒 is an expression, 𝐻 is the precon-
lgr by offering the owned logger 𝑔1 at lgr, essentially pinning     dition describing the heap before execution, 𝑣 is the return
it without detaching its ownership from the dictionary. We          value of 𝑒, and 𝑄 𝑣 is the postcondition describing the heap
update the specification of set_level_all to preserve all           after the execution of 𝑒. This triple asserts total correctness: if
pinned locations in the dictionary, ensuring the validity of        the initial heap satisfies 𝐻 , then 𝑒 will terminate and produce
exposed internal pointers.                                          an output value 𝑣 and a heap fragment satisfying 𝑄 𝑣.
                                                                       A representation predicate 𝑅𝐴 relates the logical model
3     Background                                                    of an object with a location (its entry point) and a heap
                                                                    fragment (the memory it occupies). Formally, 𝑅𝐴 has type
In this section, we first briefly introduce separation logic,       𝐴 → loc → hProp, abbreviated as repr 𝐴.
then review and discuss the limitation of the main state-of-
the-art approaches for reasoning about access to and muta-          3.2   Magic Wands
tion of container subparts.
                                                                    In separation logic, detaching ownership (borrowing) is tra-
3.1   Separation Logic                                              ditionally modeled using a magic wand − . This operator is
                                                                                                                     ★
                                                                    well-suited for a single immutable borrow, where the bor-
Separation logic is a refinement of Hoare logic that enables        rowed subpart can later be returned unchanged.
local reasoning: one can prove a Hoare triple by describing            In the logger example, a possible but unhelpful specifica-
only the relevant heap fragment and apply the triple in a           tion of get tracks the returned pointer using a magic wand:
larger context. We use a standard shallow embedding of a
linear separation logic in a higher-order logic, which models       { ⌊𝑑 [𝑘] = 𝑔⌋ ★ Dict 𝑑 𝑝 } get(𝑝, 𝑘)
                                                                                   { 𝜆 𝑟 . Logger 𝑔 𝑟 ★ (Logger 𝑔 𝑟 − Dict 𝑑 𝑝) }
                                                                                                                         ★




heaps (heap fragments) as partial functions from locations
to values, with type loc → val (abbreviated as heap).               𝑑 [𝑘] denotes the logger associated with key 𝑘 stored in dictio-
   We assume the existence of a distinguished null pointer          nary 𝑑. This specification is limited: after performing get, op-
and allow pointer arithmetic on locations, so an expression         erations that require the dictionary representation Dict 𝑑 𝑝,
like 𝑝 + 𝑛 denotes the location 𝑛 steps offset from the base        such as get and set_level_all, cannot be performed until
location 𝑝. We denote the empty heap as ∅. Two heaps ℎ 1 and        the current wand is canceled. However, wand cancelation
ℎ 2 are disjoint (written ℎ 1 ⊥ℎ 2 ) when their domains do not      logically forgets the exposed pointer and thus invalidates
overlap, and can be combined by union, denoted as ℎ 1 ⊎ ℎ 2 .       it. Moreover, if the borrowed logger is mutated, the wand
   A heap predicate 𝐻 is a function of type heap → prop             cannot be canceled at all, leaving the dictionary inaccessible.
(abbreviated as hProp), used to describe properties of heaps.
                                                                               (wand cancellation)   𝐻 1 ★ (𝐻 1 − 𝐻 2 ) ⊢ 𝐻 2
                                                                                                                 ★




Figure 4 shows the basic heap predicate combinators. ⌊𝑃⌋
asserts a pure (non-spatial) proposition 𝑃. 𝑝 ↦→ 𝑣 denotes a        Therefore, when verifying the logger example with this spec-
singleton heap mapping location 𝑝 to value 𝑣. The separating        ification, lgr is invalid after calling set_level_all, causing
conjunction 𝐻 1 ★𝐻 2 holds when the heap can be divided into        the verification to get stuck at set_level(lgr, DEBUG).
Precise Reasoning about Container-Internal Pointers with Logical Pinning                            CPP ’26, January 12–13, 2026, Rennes, France


   Magic wand as frame. The magic-wand-as-frame [8, 29]                    same pattern naturally arises in Rust, where the type system
technique extends the traditional use of magic wand to sup-                enforces memory safety through controlled aliasing.
port a single mutable borrow. Instead of fixing the borrowed                  We return in section 7 to Rust’s borrowing model, includ-
value, it universally quantifies over all possible updates, al-            ing the standard borrows, splitting borrows and deferred bor-
lowing the value to be modified and later reintegrated.                    rows. While these mechanisms provide strong safety guar-
   Under this approach, get can be specified as:                           antees, they remain insufficient to express certain patterns
                                                                           of internal pointer exposure: current Rust cannot easily ex-
{ ⌊𝑑 [𝑘] = 𝑔⌋ ★ Dict 𝑑 𝑝 } get(𝑝, 𝑘)
                                                                           press the above examples (logger updates, element swaps,
{ 𝜆 𝑟 . Logger 𝑔 𝑟 ★ (∀ 𝑔′ . Logger 𝑔′ 𝑟 − Dict 𝑑 [𝑘 := 𝑔′ ] 𝑝) }


                                             ★
                                                                           or borrowing multiple elements and subtrees in a tree). The
𝑑 [𝑘 := 𝑔′ ] denotes the dictionary 𝑑 with the logger associated           Rustonomicon calls our element-swapping example “pretty
with key 𝑘 substituted by 𝑔′ .                                             clearly hopeless” for “general container types like a tree” [28].
   This specification allows the borrowed logger 𝑔 to be up-
dated in place and returned to the dictionary afterward. How-              4 The Logical-Pinning Model for Reasoning
ever, the magic-wand-as-frame technique still does not sup-                  About Internal Pointers
port multiple borrows: a second call to get again requires
                                                                           In this section, we present logical pinning, a lightweight
canceling the wand and thereby revoking the first borrow.
                                                                           borrowing model for reasoning about sequential programs
3.3   Trees with Holes and Cut Subtrees                                    that expose and manipulate pointers to container subparts
                                                                           (i.e., elements and substructures). At its core, the model de-
Charguéraud [9] introduces a technique to take multiple mu-                fines fine-grained borrowing states along with transitions
table borrows of elements or subtrees within a tree. Consider              that describe how these states evolve in response to program
a binary tree whose nodes are represented in C as:                         operations or logical reasoning steps.
struct tnode { elem x; struct tnode *lt, *rt; };                               Building on this model, we introduce a proof discipline in
                                                                           which users (1) identify borrowable subparts and redefine the
In addition to the standard constructors for leaves and nodes,
                                                                           container’s representation predicate to track their borrowing
datatype treehc includes two additional constructors:
                                                                           states; (2) enrich API specifications to reflect the validity of
 treehc 𝐴 ≜ Leaf | Node (𝑥 : 𝐴) (𝑡𝑙 , 𝑡𝑟 : treehc 𝐴)                       exposed internal pointers; and (3) prove correctness of API
           | Hole (𝑞 : loc) (𝑡𝑙 , 𝑡𝑟 : treehc 𝐴) | Cut (𝑞 : loc)           and client programs with explicit logical borrow and return
                                                                           steps around subpart access. Our technique is formulated
Node 𝑥 𝑡𝑙 𝑡𝑟 denotes a node with element 𝑥, left and right
                                                                           entirely within the basic form of separation logic defined in
subtrees 𝑡𝑙 and 𝑡𝑟 ; Hole 𝑞 𝑡𝑙 𝑡𝑟 denotes a node whose element
                                                                           section 3.1, and does not require language-level extensions.
stored at 𝑞 is absent, while the subtrees remain owned; and
Cut denotes an absent subtree at 𝑞.
                                                                           4.1 Informal Overview
   The type treehc models trees with possibly absent elements
(holes) and subtrees (cuts), and thus provides a uniform rep-              Each borrowable subpart has two orthogonal properties: (1)
resentation for whole and partial trees. Each hole and cut is              whether this subpart is available to the container owner,
annotated with its location to enable reattachment. The tree               i.e., the container owner has ownership of this subpart and
representation is the same as for ordinary trees, except that              therefore can access its logical value 𝑣; (2) whether it is pinned
if a tree stored at 𝑝 is Hole 𝑞 𝑡𝑙 𝑡𝑟 or Cut 𝑞, then 𝑝 = 𝑞 and             at an exposed memory location 𝑞. The combination of these
the ownership of the absent element or subtree is not held.                properties yields four borrowing states for each borrowable
   This representation models ownership transfer in a single               element or substructure of a container:
step: an element or subtree is either present or replaced by               • Owned 𝒗: The subpart is available and unpinned. The
a hole or a cut. However, this granularity is too coarse for                 container owner may freely relocate it without affecting
patterns such as the subtree–compare example in section 2.2.                 its logical state.
There, specifying lookup(𝑝, 𝑘 1 ) with this representation re-             • Offered 𝒗 (𝒒 :: 𝒒𝒔): The subpart is available but pinned to
quires converting 𝑡 1 into a cut to track its pointer 𝑞 1 , thereby          a specific exposed location 𝑞. The list 𝑞𝑠 (possibly empty)
detaching its ownership from 𝑡. This detachment is undesir-                  represents additional exposed aliasing pointers.
able, since it either (1) blocks a second lookup, or (2) forces              In this state, the container owner retains ownership of this
the restoration of 𝑡 1 into 𝑡, which hides the location of 𝑡 1               subpart, but exposes its location for others to borrow it
behind the representation of 𝑡 and thus logically forgets and                in the future. To preserve the same exposed location, the
invalidates 𝑞 1 before it is used in compare.                                owner may perform only in-place updates, not relocation.
                                                                           • Borrowed (𝒒 :: 𝒒𝒔): The subpart is pinned to the exposed
3.4   Borrows in Rust                                                        location 𝑞 (with additional aliases 𝑞𝑠) and currently bor-
The pattern of exposing and manipulating internal pointers                   rowed by another party. The subpart is unavailable to the
of containers is common in low-level programming. The                        container owner until it is returned at the same location.
CPP ’26, January 12–13, 2026, Rennes, France                                                       Yawen Guan and Clément Pit-Claudel


• Missing: The subpart is unavailable and not tracked.                 We also use records (section 5.1.2) to syntactically encapsu-
The Offered and Borrowed states are particularly important          late pointer arithmetic, allowing Dict to be further rewritten
for modeling ownership transfer. One can decompose a con-           as below. Here, Cell is the points-to predicate asserting a
tainer 𝑐 that holds offered elements as follows:                    value occupies a single cell:
        c with element e offered at q is stored in memory                              ∀ 𝑣 𝑝. Cell 𝑣 𝑝 ≜ 𝑝 ↦→ 𝑣
  ≡     c with an element borrowed at q is stored in memory
                                                                    Dict : repr (list (int × logger))
           ★ e is stored at q
                                                                    Dict [] 𝑝 ≜ ⌊𝑝 = null⌋
The forward direction corresponds to a logical borrow, and          Dict ((𝑘, 𝑔) :: 𝑑) 𝑝 ≜
the backward direction to a logical return.
                                                                         Record ⟨ key : Cell 𝑘; log : ∗ Logger 𝑔; nxt : ∗ Dict 𝑑 ⟩ 𝑝
    We introduce the borrowable datatype to lift a base logi-
cal type 𝐴 to its borrow-aware form borrowable 𝐴 (writ-             When the dictionary is non-empty, 𝑝 points to a record with
ten ♭𝐴) that models the four borrowing states described             three fields: the “key” field stores 𝑘 within a single memory
above. We also define a predicate transformer liftToB that          cell described by Cell; the “log” and “nxt” fields store 𝑔 and
lifts the corresponding base representation predicate 𝑅𝐴 to         𝑑 indirectly, that is, store an intermediate pointer to the
liftToB 𝑅𝐴 (written ♭ 𝑅𝐴 ) that describes borrowable objects        corresponding objects.
of type ♭𝐴. Full definitions are provided later in section 4.3.1.
                                                                         Step 1. Identify borrowable subparts and redefine the
                             type    representation predicate       container’s representation predicate to track their bor-
         base object          𝐴                  𝑅𝐴 : repr 𝐴        rowing states. We first identify the borrowable subparts, in
      borrowable object       ♭𝐴               ♭ 𝑅 : repr ♭ 𝐴       this case the loggers, and lift their logical models (of type
                                                  𝐴
                                                                    logger) to the borrow-aware form (of type ♭ logger), where
4.2    Step-by-Step Guide                                           each logger is annotated with its borrowing state. We use
                                                                    𝑣 ′ , 𝑅 ′ and 𝑓 ′ to denote the borrow-aware forms of the log-
We illustrate the use of our model and proof discipline step
                                                                    ical value 𝑣, predicate 𝑅 and function 𝑓 , respectively. We
by step using the motivating logger example introduced in
                                                                    then define a borrow-aware representation predicate Dicte
section 1. For simplicity, assume that logger keys are integers.
                                                                    to describe a dictionary whose elements are borrowable:
Suppose that the dictionary is implemented as a linked list
of key–logger pairs, whose nodes are represented in C as:           Dicte : repr (list (int × ♭ logger))
struct dnode { int key; struct logger* log;                         Dicte [] 𝑝 ≜ ⌊𝑝 = null⌋
                        struct dnode* nxt; };                       Dicte ((𝑘, 𝑔′ ) :: 𝑑) 𝑝 ≜
A typical representation predicate for such dictionaries is:           Record ⟨ key : Cell 𝑘; log : ∗♭ Logger 𝑔′ ; nxt : ∗ Dicte 𝑑 ⟩ 𝑝
Dict : repr (list (int × logger))                                   This definition states that when the dictionary is non-empty,
Dict [] 𝑝 ≜ ⌊𝑝 = null⌋                                              the “log” field stores a borrowable logger 𝑔′ indirectly.
Dict ((𝑘, 𝑔) :: 𝑑) 𝑝 ≜ 𝑝 ↦→ 𝑘                                          Step 2. Enrich API specifications to reflect the valid-
                     ★ ∃ 𝑞 1 . 𝑝 + 1 ↦→ 𝑞 1 ★ Logger 𝑔 𝑞 1          ity of exposed internal pointers. To capture the fact that
                     ★ ∃ 𝑞 2 . 𝑝 + 2 ↦→ 𝑞 2 ★ Dict 𝑑 𝑞 2            set_level_all updates loggers in place, we refine its spec-
                                                                    ification to explicitly ensure pointer stability:
When the dictionary is non-empty, the head key 𝑘 is stored
at 𝑝, a pointer to the head logger 𝑔 is stored at 𝑝 + 1, and a              { ⌊∀ 𝑔′ ∈ 𝑑. isAvailable 𝑔′ ⌋ ★ Dicte 𝑑 𝑝 }
pointer to the rest of the dictionary 𝑑 is stored at 𝑝 + 2.                      set_level_all(𝑝, 𝑣)
   Step 0. Abstract indirection and pointer arithmetic.                     { 𝜆 _. Dicte (map (𝜆 𝑔′ . 𝑔′ ⟦lvl := 𝑣⟧) 𝑑) 𝑝 }
The “log” and “nxt” fields store intermediate pointers rather       isAvailable 𝑔′ asserts that the underlying value of 𝑔′ is acces-
than embedding the referenced objects in place. We express          sible, i.e., 𝑔′ is in the Owned or Offered state. This specifica-
such indirection using the indirection transformer “∗ ” (sec-       tion requires the availability of all loggers in the dictionary,
tion 4.4), so the definition below desugars to the one above.       allowing them to be offered at exposed locations. In the post-
Changes are marked using the “just changed” color conven-           condition, 𝑔′ ⟦lvl := 𝑣⟧ denotes a borrow-aware substitution
tion from fig. 3.                                                   that preserves exposed locations.
Dict : repr (list (int × logger))                                      We can now specify get to track the returned pointer in
Dict [] 𝑝 ≜ ⌊𝑝 = null⌋                                              the borrowing state without detaching 𝑔 ([𝑟 ] denotes 𝑟 :: []):
Dict ((𝑘, 𝑔) :: 𝑑) 𝑝 ≜                                              (weakest) { ⌊𝑑 [𝑘] = Owned 𝑔⌋ ★ Dicte 𝑑 𝑝 }
                𝑝 ↦→ 𝑘 ★ ∗ Logger 𝑔 (𝑝 + 1) ★ ∗ Dict 𝑑 (𝑝 + 2)                   get(𝑝, 𝑘) { 𝜆 𝑟 . Dicte 𝑑 [𝑘 := Offered 𝑔 [𝑟 ]] 𝑝 }
Precise Reasoning about Container-Internal Pointers with Logical Pinning                                  CPP ’26, January 12–13, 2026, Rennes, France


This first specification allows loggers other than 𝑑 [𝑘] to be
unavailable; but it prohibits repeated calls to get with the                                          Floating                   Pinned
same key, as it requires 𝑑 [𝑘] to be in the Owned state. We
can strengthen it to allow the queried logger to be either
Owned or Offered:                                                            Available                 Owned                     Offered
                                                                                                                                     3            4

(weaker) { ⌊𝑑 [𝑘] = 𝑔′ ∧ isAvailable 𝑔′ ⌋ ★ Dicte 𝑑 𝑝 }
                                                                             Unavailable                Missing                  Borrowed
                     get(𝑝, 𝑘) { 𝜆 𝑟 . Dicte 𝑑 [𝑘 := pin 𝑔′ 𝑟 ] 𝑝 }
                                                                               1
                                                                                    Pinning by Static Calculation or Program Operation
Function pin 𝑣 ′ 𝑟 pins a borrowable value 𝑣 ′ at 𝑟 . The predi-               2
                                                                                    Logical Forget
cate transformer “♭ ” ensures that if 𝑣 ′ is already pinned, the               3
                                                                                    Logical Borrow                (borrowable)             (non-borrowable)
existing and new locations coincide.                                           4
                                                                                    Logical Return                Owned
          𝑣′                       pin 𝑣 ′ 𝑟                                   5
                                                                                    Canonical Embedding

          Owned 𝑣                  Offered 𝑣 (𝑟 :: [])
          Offered 𝑣 (𝑞 :: 𝑞𝑠)      Offered 𝑣 (𝑟 :: 𝑞 :: 𝑞𝑠)                        Figure 5. Borrowing states and transitions.
          Borrowed (𝑞 :: 𝑞𝑠)       Borrowed (𝑟 :: 𝑞 :: 𝑞𝑠)
          Missing                  Borrowed (𝑟 :: [])
                                                                           4.3.1 Borrowing States. The logical datatype borrowable
We can further strengthen the specification by allowing the                models the borrowing states and lifts a base type 𝐴 to its
queried logger to be Borrowed or Missing as well:                          borrow-aware form:
(strongest) { ⌊𝑑 [𝑘] = 𝑔′ ⌋ ★ Dicte 𝑑 𝑝 }
                                                                              borrowable 𝐴 (written ♭𝐴) ≜ (option 𝐴) × (list loc)
                     get(𝑝, 𝑘) { 𝜆 𝑟 . Dicte 𝑑 [𝑘 := pin 𝑔′ 𝑟 ] 𝑝 }
                                                                                                     Floating 𝑜 𝑣                Pinned 𝑜 𝑣 (𝑞 :: 𝑞𝑠)
   Step 3. Prove correctness with explicit logical borrow                                            ≜ (𝑜 𝑣 ,     [])            ≜ (𝑜 𝑣 ,    𝑞 :: 𝑞𝑠)
and return steps around subpart access. Figure 3 illus-
                                                                             Available 𝑣 𝑞𝑠          Owned 𝑣                     Offered 𝑣 (𝑞 :: 𝑞𝑠)
trates a correctness proof of the logger example, with the
                                                                             ≜ (Some 𝑣, 𝑞𝑠)          ≜ (Some 𝑣, [])              ≜ (Some 𝑣, 𝑞 :: 𝑞𝑠)
correctness theorem stated as:
                                                                             Unavailable 𝑞𝑠          Missing                     Borrowed (𝑞 :: 𝑞𝑠)
 (∀ 𝑔′ ∈ 𝑑. isAvailable 𝑔′ ) ∧ (𝑔𝑘′ = 𝑑 [𝑘]) →                               ≜ (None, 𝑝𝑠)            ≜ (None,           [])      ≜ (None, 𝑞 :: 𝑞𝑠)
 let 𝑑 1 ≜ map (𝜆 𝑔′ . 𝑔′ ⟦lvl := INFO⟧) 𝑑 in
 { Dicte 𝑑 registry } (the logger program)                                    The Offered and Borrowed states capture the fact that
    { 𝜆 _. Dicte 𝑑 1 [𝑘 := pin 𝑔𝑘′ ⟦lvl := DEBUG⟧ lgr] registry }          the borrowable subpart remains at its previously exposed
                                                                           location 𝑞 (with additional aliases 𝑞𝑠); we call them the pinned
   Immediately before set_level, we perform logical bor-                   states. Pinned states indicate the validity of exposed internal
row to detach the target logger’s ownership from the dictio-               pointers to the element.
nary. From the dictionary’s perspective, the logger transi-                   Owned and Missing are floating states. For flat containers
tions from being offered at lgr (available for future borrow-              such as arrays, vectors and records, floating states can be
ing) to being borrowed at lgr (held by another party), with                upgraded to pinned states purely by static calculation (tran-
lgr enabling future return.                                                sition ○1 in fig. 5), i.e., by computing each subpart’s location
   After performing set_level, whose specification frames                  from the container’s base address and the subpart’s offset
out the partial dictionary, we perform a logical-return step               that is known statically.
(using the handle lgr) to restore the updated logger’s owner-                 Missing and Borrowed are unavailable states, indicating
ship to the dictionary, thereby recovering the full dictionary             that the subpart has been logically detached from the con-
representation for subsequent operations.                                  tainer and replaced by a tagged hole. In contrast, available
                                                                           states, Owned and Offered, indicate that the container owner
4.3   Borrowability                                                        has ownership of this subpart.
In flat containers such as arrays and records, borrowable
                                                                           4.3.2   Containers with Borrowable Subparts.
subparts are typically the stored items (elements), such as
record fields and array entries. They can be individually ma-                 Logical datatypes. Consider the following standard defi-
nipulated without affecting the overall structure. In recursive            nition of a logical list. We write [] for Nil, 𝑥 :: 𝑙 for Cons 𝑥 𝑙,
containers such as lists and trees, borrowable subparts in-                and [𝑥 1 ; . . . ; 𝑥𝑛 ] for Cons 𝑥 1 (. . . (Cons 𝑥𝑛 Nil)).
clude both elements and recursively defined substructures,
such as list tails and subtrees.                                                         list 𝐴 ≜ Nil | Cons (𝑥 : 𝐴) (𝑙 : list 𝐴)
CPP ’26, January 12–13, 2026, Rennes, France                                                                  Yawen Guan and Clément Pit-Claudel


By lifting the element type from 𝐴 to ♭𝐴, we obtain lists              A second variant, Lists , supports borrowing tails:
whose elements can be borrowed independently:                          Lists : (repr 𝐴) → repr (lists 𝐴)
                                             ♭
                             liste 𝐴 ≜ list 𝐴                          Lists 𝑅 [] 𝑝 ≜ ⌊𝑝 = null⌋
This definition captures the borrowing pattern in which each           Lists 𝑅 (𝑥 :: 𝑙 ′ ) 𝑝 ≜ 𝑅 𝑥 𝑝 ★ ∃ 𝑞. 𝑝 + 1 ↦→ 𝑞 ★ ♭ (Lists 𝑅) 𝑙 ′ 𝑞
element of a container can be accessed independently. For
                                                                       Similarly, Listes combines both forms, supporting borrowable
instance, in the logger example (section 4.2), the borrow-
                                                                       elements and borrowable tails:
aware dictionary has type list (int × ♭ logger).
   Supporting borrowable recursive substructures (such as                   Listes : (repr 𝐴) → repr (listes 𝐴)            Listes 𝑅 ≜ Lists ♭ 𝑅
list tails or subtrees) requires modifying the inductive defini-       4.3.3 Borrowing State Transitions. Figure 5 shows the
tion of the container (its underlying “shape”). For example,           transitions between the borrowing states.
lists describes lists in which each tail is borrowable:                    Transition ○   1 (Pinning by Static Calculation or Pro-
         lists 𝐴 ≜ Nils | Conss (𝑥 : 𝐴) (𝑙 ′ : ♭ (lists 𝐴))            gram Operation) pins a container subpart at a newly ex-
                                                                       posed location. Static calculation, as already discussed in
We write [] for Nils and 𝑥 :: 𝑙 ′ for Conss 𝑥 𝑙 ′ .                    section 4.3.1, derives the subpart’s location based on static
  Combining these two forms, we obtain listes 𝐴 for lists in           knowledge. It is applicable only in flat containers.
which both elements and tails are borrowable:                              For most pointer-based containers, subpart locations are
                            listes 𝐴 ≜ lists ♭𝐴                        often not statically known, and must instead be computed
                                                                       dynamically by executing traversal operations. For example,
   Representation predicates. The generic borrow trans-                in the logger example, the get function exposes the location
former on representation predicates, liftToB, lifts a predicate        of a logger stored in a linked list, whose address cannot be
𝑅 of type repr 𝐴 to a predicate of type repr ♭𝐴. We write ♭ 𝑅          determined statically.
for liftToB 𝑅. The transformer is defined as follows:                      A pinning transition always produces a pinned state. As-
            ♭
                𝑅 (𝑜 𝑣 , 𝑞𝑠) 𝑝 ≜ val♭ 𝑅 𝑜 𝑣 𝑝 ★ loc♭ 𝑅 𝑞𝑠 𝑝            sume that the newly exposed location is 𝑟 . Such a transition
  ♭                                     ♭                              can convert a floating state into a pinned state, for example,
val 𝑅 (Some 𝑣) 𝑝 ≜ 𝑅 𝑣 𝑝              loc 𝑅 𝑞𝑠 𝑝 ≜ ⌊∀ 𝑞 ∈ 𝑞𝑠. 𝑞 = 𝑝⌋   from Owned 𝑣 to Offered 𝑣 [𝑟 ]. If starting from an already
  ♭
val 𝑅 (None ) 𝑝 ≜ ⌊⊤⌋                                                  pinned state such as Offered 𝑣 (𝑞 :: 𝑞𝑠), it extends the alias
                                                                       list with 𝑟 , yielding Offered 𝑣 (𝑟 :: 𝑞 :: 𝑞𝑠).
The representation predicate ♭ 𝑅 for the borrowable value                  Transition ○  2 (Logical Forget) is the reverse of pinning:
(𝑜 𝑣 , 𝑞𝑠) has two components: the value part val♭ 𝑅 𝑜 𝑣 𝑝, which      it logically invalidates an exposed pointer by discarding the
describes the underlying value if available; and the location          pure constraint that tracks it.
part loc♭ 𝑅 𝑞𝑠 𝑝, which asserts that every pointer in the ex-                                      ♭
                                                                                (logical forget)       𝑅 (𝑜 𝑣 , 𝑞 :: 𝑞𝑠) 𝑝 ⊢ ♭ 𝑅 (𝑜 𝑣 , 𝑞𝑠) 𝑝
posed alias list 𝑞𝑠 is equal to the canonical location 𝑝.
   Tracking an alias list rather than a single optional exposed           Logical forget always starts with a pinned state. If all
pointer simplifies specifications: equality among all aliases          pointers in the alias list are forgotten, it yields a floating
is encapsulated in ♭ 𝑅, so functions that read or create aliases       state; otherwise the produced state is still pinned. Logical
do not need to track it explicitly. For example, consider get          return is useful for unifying a state with one without certain
on a dictionary where the queried logger 𝑔 already has an              aliases, such as postconditions that do not track pointers
exposed pointer 𝑞. One could explicitly track the new alias 𝑟 :        exposed temporarily within the function body.
                                                                          Transition ○  3 (Logical Borrow) and Transition ○   4 (Log-
{ ⌊𝑑 [𝑘] = Offered 𝑔 [𝑞]⌋ ★ Dicte 𝑑 𝑝 }
                                                                       ical Return) implement the key feature of our model: sup-
                       get(𝑝, 𝑘) { 𝜆 𝑟 . ⌊𝑟 = 𝑞⌋ ★ Dicte 𝑑 𝑝 }         porting flexible ownership transfers.
Using the alias list, the same postcondition can be expressed             Specifically, a subpart offered at an exposed location can
equivalently and more cleanly as (in the same manner as the            be logically borrowed from the container for local reasoning.
specifications in section 4.2):                                        Its ownership can be later reclaimed by the original container,
                                                                       as long as the subpart is not moved (but it may be mutated).
             { 𝜆 𝑟 . Dicte 𝑑 [𝑘 := Offered 𝑔 [𝑟 ; 𝑞]] 𝑝 }
                                                                       Formally, the logical borrow and return rules are captured
           ≡ { 𝜆 𝑟 . Dicte 𝑑 [𝑘 := pin 𝑑 [𝑘] 𝑟 ] 𝑝 }                   by the following equivalence:
   The borrow transformer “♭ ” enables modular lifting of              ♭
                                                                           𝑅 (Offered 𝑣 (𝑞 :: 𝑞𝑠)) 𝑝 ≡ ♭ 𝑅 (Borrowed (𝑞 :: 𝑞𝑠)) 𝑝 ★ 𝑅 𝑣 𝑞
representation predicates to support borrow tracking. Start-
                                                                       Figure 2 provides an intuitive illustration. A container 𝑐
ing from the standard list representation predicate List (sec-
                                                                       with elements 𝑒 1 offered at 𝑝 1 and 𝑒 3 offered at 𝑝 3 can be
tion 1), we define Liste that supports borrowing elements:
                                                                       decomposed into (1) a partial container with holes at 𝑝 1
    Liste : (repr 𝐴) → repr (liste 𝐴)             Liste 𝑅 ≜ List ♭ 𝑅   and 𝑝 3 , and (2) the two detached elements 𝑒 1 and 𝑒 3 . This
Precise Reasoning about Container-Internal Pointers with Logical Pinning                               CPP ’26, January 12–13, 2026, Rennes, France


decomposition corresponds to logical borrow, and the reverse               useful when the client may update the tail by modifying the
operation (recomposition) to logical return.                               intermediate pointer, for example, to point to a different list.
  Transition ○ 5 (Canonical Embedding) shows that non-                        We have ∗♭ 𝑅 ≠ ♭∗𝑅, ∗∗ 𝑅 ≠ ∗𝑅, but
borrowable values are equivalent to owned borrowable value:                         ♭♭
                                                                                         𝑅 (Some 𝑣 ′, 𝑞𝑠) 𝑝 = ♭ 𝑅 𝑣 ′ 𝑝 ★ ♭♭
                                                                                                                          loc 𝑅 𝑞𝑠 𝑝
                     𝑅 𝑣 𝑝 ≡ ♭ 𝑅 (Owned 𝑣) 𝑝                                             ♭♭
                                                                                              𝑅 (None, 𝑞𝑠) 𝑝 = ♭♭
                                                                                                               loc 𝑅 𝑞𝑠 𝑝
We often omit this transition in the rest of the paper.                      By composition of “♭ ” and “∗ ”, we can express a wide
                                                                           range of memory manipulation patterns in a principled and
4.4    Indirection
                                                                           reusable way. For example, ♭∗♭ 𝑅 is useful when the interme-
Many containers store their elements or substructures indi-                diate pointer and pointed-to object are both borrowable.
rectly through intermediate pointers rather than embedding
them in place. Such indirection is standard in pointer-based               5     Case Studies
containers such as linked lists and trees.
                                                                           In this section, we illustrate logical pinning across a series
   Unlike borrowability, modeling indirection does not re-
                                                                           of containers. We adopt a simple imperative 𝜆-calculus with
quire modifying the logical datatype, as functional datatypes
                                                                           dynamic allocation, along with the linear separation logic
already abstract away low-level pointer indirection.
                                                                           presented in section 3.1. The language includes let-bindings,
   We introduce the indirection transformer “∗ ” to map a
                                                                           conditional expressions, fixpoints, equality checks, pointer
representation predicate 𝑅 for values stored in place to a
                                                                           arithmetic, and mutable arrays. Its core heap-manipulating
predicate for values stored via an intermediate pointer. Al-
                                                                           primitives are as follows:
though “∗ ” is not directly related to borrowing, it composes
nicely with the borrow transformer “♭ ”.                                       alloc(𝑛)          Allocate 𝑛 contiguous uninitialized cells,
 ∗                                  ∗
                                                                                                 and return the starting location.
     : ∀ 𝐴. (repr 𝐴) → repr 𝐴           𝑅 𝑣 𝑝 ≜ ∃ 𝑞. 𝑝 ↦→ 𝑞 ★ 𝑅 𝑣 𝑞            free(𝑛, 𝑝)        Deallocate 𝑛 contiguous cells starting at 𝑝.
With “∗ ”, the non-empty case of List can be written as:                       𝑝 ←𝑣              Write value 𝑣 to memory location 𝑝.
                                                                               !𝑝                Read value at memory location 𝑝.
         List 𝑅 (𝑥 :: 𝑙) 𝑝 ≡ 𝑅 𝑥 𝑝 ★ ∗ (List 𝑅) 𝑙 (𝑝 + 1)
                                                                              Our development, including correctness proofs of con-
4.5    Compositions of Predicate Transformers                              tainer implementations with respect to our specifications
The two representation predicate transformers “♭ ” and “∗ ”                and case-study programs, is formalized on top of a variant
serve as the fundamental abstraction for modeling recursive                of the core CFML calculus in the Rocq proof assistant. The
containers with borrowable subparts. By composing them,                    formalization is available at:
we can express different patterns of memory organization.                        https://github.com/epfl-systemf/logical-pinning
Here, “◦” denotes the standard function composition opera-
tor: (𝑔 ◦ 𝑓 ) 𝑥 = 𝑔 (𝑓 𝑥).                                                 5.1   Flat Containers
  ∗ ◦ ♭ models a borrowable value stored indirectly. For
                                                                           5.1.1 Single Cells. We present two examples of cells that,
example, the non-empty case of Lists can be written as:                    while not useful in isolation as cells are the smallest memory
                                                                           units, become valuable if combined into larger structures.
        Lists (𝑥 :: 𝑙 ′ ) 𝑝 ≡ 𝑅 𝑥 𝑝 ★ ∗♭ (Lists 𝑅) 𝑙 ′ (𝑝 + 1)
                                                                             A cell with a borrowable primitive value. Such a cell
Here, ∗♭ (Lists 𝑅) 𝑙 ′ (𝑝 +1) states that an intermediate pointer          can be read from or written to when the borrowable value is
is stored at 𝑝 + 1, and this pointer points to the borrowable              available. Neither operations invalidate pointers to this cell:
tail 𝑙 ′ . This predicate is useful for reasoning about in-place
updates to the tail, but not about modifying the intermediate              { ♭ Cell (Available 𝑣 𝑞𝑠) 𝑝 } !𝑝
pointer, since it is not borrowable.                                                               { 𝜆 𝑟 . ⌊𝑟 = 𝑣⌋ ★ ♭ Cell (Available 𝑣 𝑞𝑠) 𝑝 }
   ♭ ◦ ∗ models the case where the intermediate pointer itself
                                                                           { ♭ Cell (Available 𝑣 𝑞𝑠) 𝑝 } 𝑝 ← 𝑢
can be borrowed (along with the memory it points to). Con-
sider the lists modeled by Lists′ which is defined as follows:                                                     { ♭ Cell (Available 𝑢 𝑞𝑠) 𝑝 }

       Lists′ : (repr 𝐴) → repr (lists 𝐴)                                     A cell with an indirectly-stored borrowable value. As-
                                                                           sume that the cell at location 𝑝 is described by ∗𝑅 𝑣 𝑝, that is,
       Lists′ 𝑅 [] 𝑝 ≜ ⌊𝑝 = null⌋
                                                                           it stores an intermediate pointer to 𝑣, and 𝑣 can be described
       Lists′ 𝑅 (𝑥 :: 𝑙 ′ ) 𝑝 ≜ 𝑅 𝑥 𝑝 ★ ♭∗ (Lists′ 𝑅) 𝑙 ′ (𝑝 + 1)          by predicate 𝑅. Reads and writes to this cell operate on the
                                                                           intermediate pointer without affecting 𝑣:
Here, ♭∗ (Lists′ 𝑅) 𝑙 ′ (𝑝 + 1) states that a borrowable interme-
diate pointer is stored at 𝑝 + 1, and borrowing this pointer                      { ∗ 𝑅 𝑣 𝑝 } !𝑝 { 𝜆 𝑟 . Cell 𝑝 𝑟 ★ 𝑅 𝑣 𝑟 }
transitively borrows the tail it points to. This predicate is                     { ∗ 𝑅 𝑣 𝑝 } 𝑝 ← 𝑞 { 𝜆 _. Cell 𝑝 𝑞 ★ ∃ 𝑞 𝑣 . 𝑅 𝑣 𝑞 𝑣 }
CPP ’26, January 12–13, 2026, Rennes, France                                                            Yawen Guan and Clément Pit-Claudel


Although the above specification is precise, it exposes the                We add the following notations as syntactic sugar for field
internal structure of “∗ ” and thus breaks the abstraction of            access and exposing field location:
indirection, reducing modularity. For example, it does not                 Notation     C Syntax                        Desugars to
allow reading from or writing to the same cell twice, since
the pre- and postconditions do not have the same shape.                    𝑝.𝑓          (*p).f, p→f         !(𝑝 + offset 𝑓 )
   The intermediate pointer being operated on is an internal               𝑝.𝑓 ← 𝑣      (*p).f = v, p→f = v (𝑝 + offset 𝑓 ) ← 𝑣
pointer of this single-cell container, thereby its exposure or             &𝑝.𝑓         &(p→f)              𝑝 + offset 𝑓
mutation can instead be handled by our borrowing model:
                                                                            Field access. Accessing a record field reduces to accessing
  { ∗♭ 𝑅 𝑣 ′ 𝑝 } !𝑝 { 𝜆 𝑟 . ∗♭ 𝑅 (pin 𝑣 ′ 𝑟 ) 𝑝 }                        a single cell (section 5.1.1), hence we can lift the single-cell
≡ { ∗♭ 𝑅 𝑣 ′ 𝑝 } !𝑝 { 𝜆 𝑟 . ∗♭ 𝑅 (Borrowed [𝑟 ]) 𝑝 ★ ♭ 𝑅 𝑣 ′ 𝑟 }         specifications for field operations. For example, reading a
                                                                         field that stores a borrowable value in place is specified as fol-
  { ∗♭ 𝑅 (Borrowed [𝑟 ]) 𝑝 ★ ♭ 𝑅 𝑣 ′ 𝑟 } 𝑝 ← 𝑞
                                                                         lows. Crucially, only the target field’s value must be available,
                        { 𝜆 _. ∗♭ 𝑅 (Borrowed [𝑞]) 𝑝 ★ ♭ 𝑅 𝑣 ′ 𝑟 }       and other fields may be borrowed independently.
Here, we make the inner value borrowable. Exposing the                   { ⌊𝑙 [𝑓 ] = RV ♭ Cell (Available 𝑣 𝑞𝑠)⌋ ★ Record 𝑙 𝑝 }
intermediate pointer pins the inner value, and replacing this                                          𝑝.𝑓 { 𝜆 𝑟 . ⌊𝑟 = 𝑣⌋ ★ Record 𝑙 𝑝 }
pointer with 𝑞 is treated as replacing the inner value with a
hole at 𝑞 (the target of 𝑞 is unknown).                                    Exposing field location. Because records are flat contain-
                                                                         ers, a field can always be pinned at its address statically:
5.1.2 Arrays and Records. A plain array is a contiguous
block of memory without a header as in C, and we model it                         Record 𝑙 [𝑓 := RV ♭ 𝑅 𝑣 ′ ] 𝑝
as a list of values laid out sequentially in memory:                           ≡ Record 𝑙 [𝑓 := RV ♭ 𝑅 (pin 𝑣 ′ (𝑝 + offset 𝑓 ))] 𝑝
Array : ∀ 𝐴. (repr 𝐴) → repr (list 𝐴)                                    Alternatively, the location can be obtained dynamically:
Array 𝑅 [] 𝑝 ≜ ⌊𝑝 = null⌋
                                                                         { ⌊𝑙 [𝑓 ] = RV ♭ 𝑅 𝑣 ′ ⌋ ★ Record 𝑙 𝑝 } &𝑝.𝑓
Array 𝑅 (𝑥 :: 𝑙) 𝑝 ≜ ⌊𝑝 ≠ null⌋ ★ 𝑅 𝑥 𝑝 ★ Array 𝑅 𝑙 (𝑝 + 1)
                                                                                             { 𝜆 𝑟 . Record 𝑙 [𝑓 := RV ♭ 𝑅 (pin 𝑣 ′ 𝑟 )] 𝑝 }
   We consider records as heterogeneous arrays, where each
field occupies one cell that stores a value in place or an               By the definition of Record, 𝑟 equals 𝑝 + offset 𝑓 .
intermediate pointer to the value, and the representation
                                                                         5.2   Recursive Containers
predicate of each field may differ. To uniformly describe
such fields, we introduce a helper type ReprVal to package a             Recursive containers are the natural use case of the logical-
value with its representation predicate:                                 pinning model: element locations are not statically known,
                                                                         and their pointer-rich APIs often expose internal pointers.
         ReprVal ≜ RV (𝑡 : type) (𝑅𝑡 : repr 𝑡) (𝑣 : 𝑡)                   Our model marks these pointers on demand; we demonstrate
When 𝑡 is clear from context, we write RV 𝑅 𝑣 with the type              its generality and practicality on linked lists and trees, by
left implicit.                                                           deriving precise specifications for standard APIs.
   Each field label 𝑓 is associated with a natural number index
                                                                         5.2.1 Linked Lists. We study singly linked lists, with
offset 𝑓 , indicating the field’s offset from the entry location
                                                                         nodes represented in C as lnode (sections 1 and 4.3.2). We
of the record. The representation predicate for records is
                                                                         start with the traditional representation of lists — a logical
defined as follows:
                                                                         model whose elements and tails are not borrowable:
        Record : repr (list (Field × ReprVal))
                                                                                  CList : repr (list int)      CList ≜ List Cell
        Record [] 𝑝 ≜ ⌊𝑝 = null⌋
                                                                         Consider the specification of the function size, which com-
        Record ((𝑓 , RV 𝑅 𝑣) :: 𝑙) 𝑝 ≜
                                                                         putes the list’s length |𝑙 |, in this model:
          ⌊𝑝 ≠ null⌋ ★ 𝑅 𝑣 (𝑝 + offset 𝑓 ) ★ Record 𝑙 𝑝
                                                                               { CList 𝑙 𝑝 } size(𝑝) { 𝜆 𝑟 . ⌊𝑟 = |𝑙 |⌋ ★ CList 𝑙 𝑝 }
We write ⟨ 𝑓0 : 𝑅0 𝑣 0 ; . . . ; 𝑓𝑛−1 : 𝑅𝑛−1 𝑣𝑛−1 ⟩ for a record with
𝑛 fields 𝑓0 to 𝑓𝑛−1 . For each 𝑖 ∈ {0, . . . , 𝑛 − 1}, field 𝑓𝑖 stores   Even for such a simple function, the CList-base specification
value 𝑣𝑖 with representation predicate 𝑅𝑖 .                              is imprecise. size neither exposes internal pointers, nor
   Records serve as a fundamental abstraction for defining               relocates objects, nor transfers ownership, yet (1) it demands
containers in our approach. Recall the list representation               more permissions than necessary, as size depends only on
predicate Lists (section 4.3.2), its non-empty case can be               the list shape and does not need ownership of elements; and
encoded as a record with two fields:                                     (2) it does not capture pointer stability, which makes pointer
                                                                         tracking impossible.
Lists 𝑅 (𝑥 :: 𝑙) 𝑝 ≡ Record ⟨ elem : 𝑅 𝑥; next : ∗♭ (List 𝑅) 𝑙 ⟩ 𝑝          Let us instead use logical pinning. We introduce CListe ,
where offset elem is 0, offset next is 1.                                which describes the same list but with borrowable elements.
Precise Reasoning about Container-Internal Pointers with Logical Pinning                            CPP ’26, January 12–13, 2026, Rennes, France


                                              { CListe 𝑙 𝑝 }      size(𝑝)      { 𝜆 𝑟 . ⌊𝑟 = |𝑙 |⌋ ★ CListe 𝑙 𝑝 }
                                              { CListe 𝑙 𝑝 }   is_empty(𝑝)     { 𝜆 𝑟 . ⌊𝑟 = true ↔ 𝑙 = []⌋ ★ CListe 𝑙 𝑝 }
                     { CListe ((Available 𝑣 𝑞𝑠) :: 𝑙) 𝑝 }          𝑝.elem      { 𝜆 𝑟 . ⌊𝑟 = 𝑣⌋ ★ CListe ((Available 𝑣 𝑞𝑠) :: 𝑙) 𝑝 }
                     { CListe ((Available 𝑣 𝑞𝑠) :: 𝑙) 𝑝 }       𝑝.elem ← 𝑢     { 𝜆 _. CListe ((Available 𝑢 𝑞𝑠) :: 𝑙) 𝑝 }
             { ⌊∀ 𝑣 ′ ∈ 𝑙 . isAvailable 𝑣 ′ ⌋ ★ CListe 𝑙 𝑝 }   incr_all(𝑝)     { 𝜆 𝑟 . CListe (mape (𝜆 𝑣. 𝑣 + 1) 𝑙) 𝑝 }
{ ⌊𝑛 < |𝑙 | ∧ nth 𝑛 𝑙 = Available 𝑣 𝑞𝑠⌋ ★ CListe 𝑙 𝑝 } nth_elem(𝑛, 𝑝) { 𝜆 𝑟 . ⌊𝑟 = 𝑣⌋ ★ CListe 𝑙 𝑝 }
                                { ⌊𝑛 < |𝑙 |⌋ ★ CListe 𝑙 𝑝 } nth_elem_ptr(𝑛, 𝑝) { 𝜆 𝑟 . CListe 𝑙 [𝑛 := pin (nth 𝑛 𝑙) 𝑟 ] 𝑝 }
                                     { CListe (𝑣 ′ :: 𝑙) 𝑝 }   pop_front(𝑝)    { 𝜆 𝑟 . CListe 𝑙 𝑟 ★ ♭ Cell 𝑣 ′ 𝑝 }

                     Figure 6. API specification for lists with borrowable elements and non-borrowable tails.

 { ⌊allTailAvl (Owned 𝑙)⌋ ★ CListes 𝑙 𝑝 }            size(𝑝)        { 𝜆 𝑟 . ⌊𝑟 = |𝑙 |⌋ ★ CListes 𝑙 𝑝 }
                               { CListes 𝑙 𝑝 }     is_empty(𝑝)      { 𝜆 𝑟 . ⌊𝑟 = true ↔ 𝑙 = []⌋ ★ CListes 𝑙 𝑝 }
      { CListes ((Available 𝑣 𝑞𝑠) :: 𝑙 ′ ) 𝑝 }        𝑝.elem        { 𝜆 𝑟 . ⌊𝑟 = 𝑣⌋ ★ CListes ((Available 𝑣 𝑞𝑠) :: 𝑙 ′ ) 𝑝 }
                                         ′
      { CListes ((Available 𝑣 𝑞𝑠) :: 𝑙 ) 𝑝 }       𝑝.elem ← 𝑢       { 𝜆 _. CListes ((Available 𝑢 𝑞𝑠) :: 𝑙 ′ ) 𝑝 }
 { ⌊allAvl (Owned 𝑙)⌋ ★ CListes 𝑙 𝑝 }            incr_all(𝑝)      { 𝜆 𝑟 . CListes (mapes (𝜆 𝑣. 𝑣 + 1) 𝑙) 𝑝 }
  ⌊𝑛 < |𝑙 | ∧ nthes 𝑛 𝑙 = Available 𝑣 𝑞𝑠⌋
                                                 nth_elem(𝑛, 𝑝)     { 𝜆 𝑟 . ⌊𝑟 = 𝑣⌋ ★ CListes 𝑙 𝑝 }
                              ★ CListes 𝑙 𝑝
                 { ⌊𝑛 < |𝑙 |⌋ ★ CListes 𝑙 𝑝 } nth_elem_ptr(𝑛, 𝑝) { 𝜆 𝑟 . CListes 𝑙 [𝑛 := pin (nthes 𝑛 𝑙) 𝑟 ] 𝑝 }
        { CListes (𝑣 ′ :: Available 𝑙 𝑞𝑠) 𝑝 }     pop_front(𝑝)      { 𝜆 𝑟 . CListes 𝑙 𝑟 ★ ⌊∀ 𝑞 ∈ 𝑞𝑠. 𝑞 = 𝑟 ⌋ ★ ♭ Cell 𝑣 ′ 𝑝 }
                                   ′     ′
                      { CListes (𝑣 :: 𝑙 ) 𝑝 }         𝑝.next        { 𝜆 𝑟 . CListes (𝑣 ′ :: pin 𝑙 ′ 𝑟 ) 𝑝 }
                                   ′     ′
                      { CListes (𝑣 :: 𝑙 ) 𝑝 }       𝑝.next ← 𝑞      { 𝜆 𝑟 . CListes (𝑣 ′ :: Borrowed [𝑞]) 𝑝 ★∃∃ 𝑞𝑙 ′ . ♭ CListes 𝑙 ′ 𝑞𝑙 ′ }
                 { ⌊𝑛 < |𝑙 |⌋ ★ CListes 𝑙 𝑝 } nth_tail(𝑛, 𝑝) { 𝜆 𝑟 . CListes (substTailes 𝑛 (pin (skipnes 𝑛 𝑙) 𝑟 ) 𝑙) 𝑝 }
                              { CListes 𝑙 𝑝 } push_front(𝑣, 𝑝) { 𝜆 𝑟 . CListes ((Owned 𝑣) :: Offered 𝑙 [𝑝]) 𝑟 }
                ⌊allTailAvl (Owned 𝑙 1 )⌋
                                                  append(𝑝 1, 𝑝 2 ) { 𝜆 𝑟 . ♭ CListes ((Offered 𝑙 1 [𝑝 1 ]) ++ (Offered 𝑙 2 [𝑝 2 ])) 𝑟 }
           ★ CListes 𝑙 1 𝑝 1 ★ CListes 𝑙 2 𝑝 2
 { ⌊allTailAvl (Owned 𝑙)⌋ ★ CListes 𝑙 𝑝 } push_back(𝑣, 𝑝) { 𝜆 𝑟 . ♭ CListes ((Offered 𝑙 [𝑝]) ++ [Owned 𝑣]) 𝑟 }

Figure 7. API specification for lists with borrowable elements and borrowable tails. allTailAvl 𝑙 ′ (resp. allAvl 𝑙 ′ ) asserts every
tail (resp. subpart) of 𝑙 ′ is available; 𝑙 1′ ++ 𝑙 2′ denotes the borrow-aware concatenation of two lists; [𝑥] denotes 𝑥 :: Owned [].

This lets specifications require only the necessary element                elements and tails borrowable:
ownership, and track pointers to elements:
                                                                                CListes : repr (lists ♭ int)     CListes ≜ Lists ♭ Cell
       CListe : repr (list ♭ int)       CListe ≜ List ♭ Cell               Figure 7 shows the CListes -based API, with operations that
                                                                           expose tail pointers highlighted. Such operations are diffi-
Figure 6 shows a complete CListe -based API specification. In              cult to specify precisely with CListe , and therefore do not
particular, the new specification of size permits elements to              appear in fig. 6. They include operations on the next field,
be unavailable, preserves their borrowing states, and there-               push_front (which adds a new head), append (which con-
fore preserves all exposed pointers tracked in those states.               catenates a second list), and push_back (which appends a
Other functions are is_empty, which returns true iff the list              new node at the tail).
is empty; 𝑝.elem and 𝑝.elem ← 𝑢, which read and write                         These CListes -based specifications are maximally precise:
the “elem” field; incr_all, which increments all elements in               they account for every internal pointer to elements and tails,
place; nth_elem and nth_elem_ptr, which return the value                   and require minimal ownership. For example, the specifica-
of, and a pointer to, the 𝑛-th element; and pop_front, which               tion of append preserves the two original head pointers 𝑝 1
removes the head and returns a pointer to the new head.                    and 𝑝 2 in a clean and natural form. All CListe -based specifi-
   These CListe -based specifications are more precise than                cations can be derived from the CListes -based ones.
CList-based ones: they require minimal element ownership,
and account for all possible exposed pointers to elements.                   Case study: swaps. Our specification of nth_elem_ptr
For example, the specification of nth_elem_ptr tracks the                  requires no element ownership, and tracks exposed point-
returned element pointer by simply pinning it.                             ers without altering the container representation. This lets
   Some APIs also expose pointers to tails, rather than just               us prove the correctness of an element-swapping program
elements. For those, we introduce CListes , which makes both               that invokes nth_elem_ptr twice, on the same or distinct
CPP ’26, January 12–13, 2026, Rennes, France                                                                      Yawen Guan and Clément Pit-Claudel


indices, to obtain element pointers, and then calls memswap to               state by letting one tree keep ownership of the subtree and
exchange their contents (section B). Here too, we see that log-              offer it at location 𝑞, while the other tree treats this subtree
ical pinning naturally supports traditionally hard-to-verify                 as borrowed at 𝑞. The ownership of the shared subtree can
patterns.                                                                    then be flexibly transferred between the two trees. Crucially,
                                                                             without the Offered state, as in trees with holes and cuts,
5.2.2 Binary Trees. We define trees with predicate Trees
                                                                             such ownership transfer would not be possible since the tree
to model binary trees with borrowable subtrees:
                                                                             currently owning the subtree would hide its location.
   trees 𝐴 ≜ Leafs | Nodes (𝑥 : 𝐴) (𝑡𝑙′, 𝑡𝑟′ : ♭ (trees 𝐴))                     In the proof using our model (the full proof is given in
   Trees : (repr 𝐴) → repr (trees 𝐴)                                         section C), this state is represented as:
   Trees 𝑅 Leafs 𝑝 ≜ ⌊𝑝 = null⌋                                                    
                                                                                     Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed (𝑝𝑟 :: 𝑞𝑠𝑟 ))) 𝑝
                                                                                                                                       
   Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ 𝑡𝑟′ ) 𝑝 ≜ Record                                                 ★ Trees 𝑅 (Nodes 𝑥𝑟 (pin 𝑡𝑟𝑙′ 𝑝𝑟𝑙 ) 𝑡𝑟𝑟
                                                                                                                              ′
                                                                                                                                 ) 𝑝𝑟
      ⟨ elem : 𝑅 𝑥; lt : ∗♭ (Trees 𝑅) 𝑡𝑙′ ; rt : ∗♭ (Trees 𝑅) 𝑡𝑟′ ⟩ 𝑝
                                                                               Assume left_rotate returns a pointer to the root of the
In contrast, a custom representation predicate Treehc for                    rotated tree. Our following specification preserves the origi-
trees with holes and cuts (section 3.3) would be written as:                 nal root pointer 𝑝. Here, rotL maps a tree to its rotated form.
 Treehc : (repr 𝐴) → repr (treehc 𝐴)                                                { ⌊𝑡 = Nodes 𝑥 𝑡𝑙′ (Available 𝑡𝑟 𝑞𝑠𝑟 )⌋ ★ Trees 𝑅 𝑡 𝑝 }
 Treehc 𝑅 Leaf 𝑝 ≜ ⌊𝑝 = null⌋                                                            left_rotate(𝑝)
 Treehc 𝑅 (Node 𝑥 𝑡𝑙 𝑡𝑟 ) 𝑝 ≜ Record                                                { 𝜆 𝑟 . ♭ (Trees 𝑅) (rotL (Offered 𝑡 [𝑝])) 𝑟 }
  ⟨ elem : 𝑅 𝑥;     lt : ∗ (Treehc 𝑅) 𝑡𝑙′ ; rt : ∗ (Treehc 𝑅) 𝑡𝑟′ ⟩ 𝑝
 Treehc 𝑅 (Hole 𝑞 𝑡𝑙 𝑡𝑟 ) 𝑝 ≜ Record                                         6      Discussion
  ⟨ elem : (= 𝑝) 𝑥; lt : ∗ (Treehc 𝑅) 𝑡𝑙′ ; rt : ∗ (Treehc 𝑅) 𝑡𝑟′ ⟩ 𝑝        Our logical-pinning model captures ad hoc proof patterns
 Treehc 𝑅 (Cut 𝑞) 𝑝 ≜ ⌊𝑝 = 𝑞⌋                                                that occur in existing separation-logic developments: (1) the
                                                                             notion of holes and cut in trees (section 3.3) can be expressed
Our model subsumes this technique: our type trees ♭𝐴 de-
                                                                             uniformly as Borrowed in our model; (2) when two pointers
scribes trees with both borrowable elements and subtrees,
                                                                             𝑝 and 𝑞 are aliases in separation logic, the common approach
unifying holes and cuts as just Borrowed. This lets us re-
                                                                             is to introduce a pure constraint 𝑝 = 𝑞 and shift ownership
produce the motivating example of the original paper on
                                                                             between the aliasing pointers via equality rewriting:
trees with holes and cuts [9], a find function that returns a
subtree at a given path, with an enhanced specification that                                   𝑅 𝑣 𝑝 ★ ⌊𝑝 = 𝑞⌋ ≡ 𝑅 𝑣 𝑞 ★ ⌊𝑝 = 𝑞⌋
supports repeated lookups and guarantees pointer stability:
                                                                             In our model, pinning captures such aliasing constraints:
{ ♭ (Trees 𝑅) 𝑡 ′ 𝑝 ★ ⌊path 𝑖 𝑡 ′ 𝑡 1′ ⌋ } find(𝑖, 𝑝)
                                                                             ♭
                                                                                 𝑅 (𝑜 𝑣 , 𝑞 :: 𝑞𝑠) 𝑝 ≡ ♭ 𝑅 (𝑜 𝑣 , 𝑝 :: 𝑞 :: 𝑞𝑠) 𝑝 ≡ ♭ 𝑅 (𝑜 𝑣 , 𝑝 :: 𝑞𝑠) 𝑞
                            { 𝜆 𝑟 . ♭ (Trees 𝑅) 𝑡 ′ ⟦𝑖 := pin 𝑡 1′ 𝑟 ⟧ 𝑝 }
Here, path 𝑖 𝑡 ′ 𝑡 1′ states that a valid path 𝑖 in tree 𝑡 ′ reaches            We have demonstrated that our model enables more pre-
a subtree 𝑡 1′ , and 𝑡 ′ ⟦𝑖 := 𝑡𝑥′ ⟧ denotes the borrow-aware sub-           cise specifications. We verify the correctness of the logger
stitution of 𝑡 ′ in which the subtree at 𝑖 is replaced by 𝑡𝑥′ .              example using a precise specification of set_level_all
                                                                             that guarantees the function does not relocate elements. For
   Case study: binary-tree left rotation. In this case study,                linked lists, we provide API specifications that precisely track
we show that our model simplifies some complex proofs and                    all exposed pointers to elements and tails, enabling the verifi-
enables more precise specifications.                                         cation of representative programs such as element-swapping.
   During a binary-tree left rotation (fig. 1), a subtree is tem-               Our model also simplifies proofs that are conceptually
porarily shared between two trees. In the traditional ap-                    complex under traditional approaches. For instance, our
proach, this situation requires unfolding the tree abstraction               proof of tree rotation avoids unfolding the tree represen-
two layers deep and managing the resulting split nodes and                   tation predicate, keeping the reasoning simple: at most two
subtrees, which is conceptually cumbersome. An intermedi-                    trees need to be tracked, rather than two split records (each
ate state has the following form, where Tree is a traditional                with three fields) and three subtrees.
representation predicate of binary trees:                                       Our model further enables proving program patterns not
  𝑝 ↦→ 𝑥 ★ ∗ (Tree 𝑅) 𝑡𝑙 (𝑝 + 1) ★ 𝑝 + 2 ↦→ 𝑝𝑟                             supported by traditional specifications, notably expose-then-
                                                                             mutate: exposing internal pointers, optionally performing
                                                       
 
                                  ∗                    
                                                        
    ★ 𝑝𝑟 ↦→ 𝑥𝑟 ★ 𝑝𝑟 + 1 ↦→ 𝑝𝑟𝑙 ★ (Tree 𝑅) 𝑡𝑟𝑟 (𝑝𝑟 + 2)
  ★ ⌊∀ 𝑞 ∈ 𝑞𝑠 . 𝑞 = 𝑝 ⌋ ★ ∗ (Tree 𝑅) 𝑡 𝑝
                                                       
                                                                            container operations that do not invalidate them, and later
              𝑟        𝑟               𝑟𝑙 𝑟𝑙                               using those pointers to read or modify container subparts.
  With our model, the tree abstraction does not need to                      This is exactly the pattern in the previous examples (logger,
be unfolded. The key idea is to represent this intermediate                  element-swapping, subtree-compare).
Precise Reasoning about Container-Internal Pointers with Logical Pinning                                CPP ’26, January 12–13, 2026, Rennes, France


   Internal sharing within a container. Some contain-                      token that can mutate the state and multiple fragment tokens
ers allow the same subpart to be referenced multiple times                 that provide consistent read-only views of its parts.
within the container. For instance, the same object may be                    Rust borrows permit either one mutable reference or
pushed to a queue more than once. In optimized trees such                  multiple immutable references to each object or object field,
as compressed tries (e.g., directed acyclic word graphs) or                but not both. Standard mutable borrows freeze the entire
binary decision diagrams (BDDs), distinct nodes may share                  container, so ad hoc APIs have been developed to allow si-
a common subtree, preserving logical tree semantics while                  multaneous borrows (pick2_mut, get_disjoint_mut [27]),
structurally forming a directed acyclic graph (DAG).                       but they either require unsafe code, or have runtime costs,
   Take an example of a tree with an internally shared subtree.            or have usage restrictions (e.g., most require obtaining all
We can model the situation by letting one node own the                     references simultaneously).
subtree and offer it at a location 𝑞, while any other node that               Deferred borrows [12] are a borrowing system that en-
references this subtree view it as borrowed at 𝑞, analogous to             sures the safety of a common workaround for the limitations
the case in tree rotation (section 5.2.2). The entire structure is         of borrowing: using paths (indices in an array, keys of a
then viewed as a partial normal tree with one subtree absent.              map, . . . ) instead of pointers. In combination with custom
   Such partial containers cannot be expressed using magic                 container types and custom path-returning APIs, deferred
wands. Magic wands do not model partial structures directly,               borrows enable safe path references to multiple elements in
but instead specify that the complete structure can be re-                 a container, with actual borrows delayed until access time,
constructed once the missing part is supplied. In this case, a             at which point the path is (re-)resolved into a pointer. In
“complete” tree does not exist: the shared subtree cannot be               contrast, logical pinning is a purely logical discipline.
simultaneously reclaimed by all referencing nodes while the                   In RefinedRust [15], a value can be logically marked as
heap segments owned by those nodes remain distinct.                        borrowed by replacing it with a borrow name. In contrast,
                                                                           logical pinning records the location of the borrowed value.
  Open questions. Our model does not answer the follow-
ing questions:                                                             8   Conclusion
• How can container-internal pointers be reasoned about in                 Logical pinning is a new lightweight borrowing model that
  concurrent programs?                                                     makes exposed internal pointers explicit in the logical rep-
• How can container-internal pointers be reasoned about in                 resentation of containers, enabling direct reasoning about
  general graphs with unrestricted sharing?                                pointer validity while preserving modularity. This technique
• Can our model be integrated with fractional resources [6,                unifies several ad hoc proof patterns and supports precise yet
  7] to distinguish read-only from read–write access? A pre-               modular specifications for common idioms such as pointer
  liminary formulation of the logical borrow–return rule is:               caching, expose-then-mutate, and consecutive lookups.
     ( ♭ 𝑅 (Offered 𝑣 (𝑞 :: 𝑞𝑠)) 𝑝) 𝜋                                         Our case studies show that it simplifies existing proofs
  ≡ 𝑅 (Borrowed (𝑞 :: 𝑞𝑠)) 𝑝 ★ ( ♭ 𝑅 (Owned 𝑣) 𝑞) 𝜋
     ♭                                                                     and allow new patterns to be verified, all without reformu-
  where 𝜋 ∈ (0, 1] is the permission fraction.                             lating the underlying separation logic. We implemented the
• How can container invariants be systematically tracked                   approach in CFML to demonstrate its soundness and practi-
  and enforced across borrow–return transitions?                           cality. Our mechanization is available online for reference.
• How can logical models, representation predicates and
  container-specific transition lemmas be automatically de-                Data Availability Statement
  rived for containers with borrowable subparts? We sus-                   The formalization of the logical-pinning model and associ-
  pect that existing work on contexts [3, 17, 20–22] and                   ated case studies are available at https://github.com/epfl-
  lenses [5, 13] could nicely combine with our approach.                   systemf/logical-pinning. The artifact [14] of this paper is
                                                                           available at https://doi.org/10.5281/zenodo.17815704.
7    Other Related Work
                                                                           A    The Subtree-Compare Example
Beyond the work discussed in section 3, previous work differs
from ours by focusing on automation [4, 11], on read-only                  Let 𝑓 be the logical comparison function, and allSubtreeAvl 𝑡 ′
sharing [11], or on modeling specific access patterns [4, 16].             assert that every subtree of 𝑡 ′ is available. The specification
   The iterated separating conjunction [23, 26] general-                   of compare uses the non-separating conjunction in its pre-
izes ★ to range over sets of heap locations. It is particularly            condition to handle potentially overlapping subtrees:
useful to specify unstructured containers, which it represents                 allSubtreeAvl 𝑡 1′ ∧ allSubtreeAvl 𝑡 2′ →
as a collection of elements with all internal pointers exposed.
                                                                               { ( ♭ (Trees 𝑅) 𝑡 1′ 𝑞 1 ★ 𝐻 1 ) ∧
                                                                                                                ∧ ( ♭ (Trees 𝑅) 𝑡 2′ 𝑞 2 ★ 𝐻 2 ) }
In contrast, logical pinning supports selective exposure.
   Authoritative cameras [18, 19] in Iris maintain a coher-                       compare(𝑞 1, 𝑞 2 )
ent global view of a resource by designating an authoritative                  { 𝜆 𝑟 . ⌊𝑟 = 𝑓 𝑡 1′ 𝑡 2′ ⌋ ★ ♭ (Trees 𝑅) 𝑡 2′ 𝑞 2 ★ 𝐻 2 }
CPP ’26, January 12–13, 2026, Rennes, France                                                                     Yawen Guan and Clément Pit-Claudel


  Starting from ♭ (Trees 𝑅) 𝑡 ′ 𝑝, the state after performing                            p.rtree <- prl
the two lookup operations is as follows:                                            
                                                                                    
                                                                                     Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed [𝑝𝑟𝑙 ])) 𝑝                
                                                                                                                                               
                                                                                                                                               
     (Trees 𝑅) 𝑡 ′ ⟦𝑘 1 := pin 𝑡 ′ [𝑘 1 ] 𝑞 1 ⟧⟦𝑘 2 := pin 𝑡 ′ [𝑘 2 ] 𝑞 2 ⟧ 𝑝
 ♭
                                                                                    
                                                                                                ♭
                                                                                                                                               
                                                                                                                                               
                                                                                         ★∃∃ 𝑞. (Trees 𝑅) (Borrowed (𝑝𝑟 :: 𝑞𝑠𝑟 )) 𝑞
                                                                                                                             ′       ′
                                                                                                                                              
                                                                                     ★ Trees 𝑅 (Nodes 𝑥𝑟 (pin 𝑡𝑟𝑙 𝑝𝑟𝑙 ) 𝑡𝑟𝑟 ) 𝑝𝑟 
                                                                                                                                              
In unification with compare’s precondition, 𝐻 1 is the partial                                                                                
tree with 𝑡 ′ [𝑘 1 ] borrowed (𝐻 2 is obtained analogously):                        
                                                                                     Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed [𝑝𝑟𝑙 ])) 𝑝             
                                                                                    
                                                                                                                                            
                                                                                                                                             
               ♭
                   (Trees 𝑅) 𝑡 ′ ⟦𝑘 1 := Borrowed [𝑞 1 ]⟧ 𝑝                       ≡      ★ ⌊∀ 𝑞 ∈ 𝑞𝑠𝑟 . 𝑞 = 𝑝𝑟 ⌋
                                                                                     ★ Tree 𝑅 (Node 𝑥 (pin 𝑡 ′ 𝑝 ) 𝑡 ′ ) 𝑝 
                                                                                                                                            
                                                                                                 s               s 𝑟
A logical return step after compare can restore 𝑡 ′ .                                                                       𝑟𝑙 𝑟𝑙 𝑟𝑟      𝑟 
                                                                                         pr.ltree <- p
                                                                                                                ′
B      Proof of Swapping Two Elements in a List                                     
                                                                                    
                                                                                    
                                                                                      Tree s 𝑅 (Nodes 𝑥 𝑡𝑙 (Borrowed [𝑝𝑟𝑙 ])) 𝑝                    
                                                                                                                                                   
                                                                                                                                                   
                                                                                     ★ ⌊∀ 𝑞 ∈ 𝑞𝑠𝑟 . 𝑞 = 𝑝𝑟 ⌋
                                                                                                                                                  
Assume memswap swaps the contents of the cells pointed to
                                                                                    
                                                                                                                                                  
                                                                                                                                                   
                                                                                                                                                   
                                                                                                                                          ′
by two distinct pointers, or does nothing if given the same                         
                                                                                        ★  Tree s  𝑅 (Node       𝑥
                                                                                                                 s 𝑟    (Borrowed  [𝑝]) 𝑡 𝑟𝑟 ) 𝑝 𝑟 
                                                                                                                                                   
pointer. In the following, we give the correctness proof of
                                                                                                                                                  
                                                                                     ★∃∃ 𝑞. ♭ (Trees 𝑅) (pin 𝑡 ′ 𝑝𝑟𝑙 ) 𝑞
                                                                                                                                                  
                                                                                                                                                   
                                                                                                                          𝑟𝑙
the element-swapping program; due to space constraints, we
                                                                                                                                                  
                                                                                     Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed [𝑝𝑟𝑙 ])) 𝑝                   
omit the case where 𝑛 1 = 𝑛 2 , which follows the same proof                        
                                                                                    
                                                                                     ★ ⌊∀ 𝑞 ∈ 𝑞𝑠𝑟 . 𝑞 = 𝑝𝑟 ⌋
                                                                                    
                                                                                                                                                  
                                                                                                                                                  
                                                                                                                                                  
                                                                                                                                                  
style. In the proof, we highlight logical borrow steps, logical                   ⊢
                                                                                    
                                                                                                                                                 
                                                                                                                                                  
                                                                                                                                         ′
return steps and logical forget steps using different colors.                       
                                                                                        ★ Trees 𝑅 (Nodes 𝑥𝑟 (Borrowed [𝑝]) 𝑡𝑟𝑟 ) 𝑝𝑟             
                                                                                                                                                 
                                                                                     ★ ♭ (Trees 𝑅) 𝑡 ′ 𝑝𝑟𝑙
                                                                                                                                                 
𝑛 1 ≠ 𝑛 2 ∧ 𝑛 1 < |𝑙 | ∧ 𝑛 2 < |𝑙 | →
                                                                                                                                                  
                                                                                                           𝑟𝑙                                    
                                                                                                               ′          ′
nth 𝑛 1 𝑙 = Available 𝑣 1 𝑞𝑠 1 ∧ nth 𝑛 2 𝑙 = Available 𝑣 2 𝑞𝑠 2 →                    Trees 𝑅 (Nodes 𝑥 𝑡𝑙 (pin 𝑡𝑟𝑙 𝑝𝑟𝑙 )) 𝑝
                                                                                                                                                  
                                                                                                                                                   
                                                                                    
                                                                                                                                                  
                                                                                                                                                   
      { CListe 𝑙 𝑝 }                                                             ≡       ★  ⌊∀ 𝑞   ∈ 𝑞𝑠 𝑟 . 𝑞  =  𝑝 𝑟 ⌋
      let 𝑞 1 ≜ nth_elem_ptr(𝑝, 𝑛 1 ) in                                             ★ Tree 𝑅 (Node 𝑥 (Borrowed [𝑝]) 𝑡 ′ ) 𝑝 
                                                                                                                                                  
                                                                                                s              s 𝑟                      𝑟𝑟     𝑟 
      { CListe 𝑙 [𝑛 1 := Offered 𝑣 1 (𝑞 1 :: 𝑞𝑠 1 )] 𝑝 }
                                                                                    Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ 𝑡𝑟𝑙′ ) 𝑝            
      let 𝑞 2 ≜ nth_elem_ptr(𝑝, 𝑛 2 ) in                                           
                                                                                   
                                                                                                                             
                                                                                                                              
                                                                                                                              
                                                                                 ⊢      ★ ⌊∀ 𝑞 ∈ 𝑞𝑠𝑟 . 𝑞 = 𝑝𝑟 ⌋
        CListe 𝑙 [𝑛 1 := Offered 𝑣 1 (𝑞 1 :: 𝑞𝑠 1 )]
                                                      
                                                                                    ★ Tree 𝑅 (Node 𝑥 (Borrowed [𝑝]) 𝑡 ′ ) 𝑝 
                                                                                                                             
                                                                                              s          s 𝑟                𝑟 
                 [𝑛 2 := Offered 𝑣 2 (𝑞 2 :: 𝑞𝑠 2 )] 𝑝                                                               𝑟𝑟

     CListe 𝑙 [𝑛 1 := Borrowed (𝑞 1 :: 𝑞𝑠 1 )]                                     
                                                                                      Trees 𝑅 (Nodes 𝑥𝑟                               
                                                                                                                                       
                                                                                                                               ′
                                                                                            (Offered (Nodes 𝑥 𝑡𝑙′ 𝑡𝑟𝑙′ ) [𝑝]) 𝑡𝑟𝑟
                                                                                   
                                                                                                                                      
                                                                                                                                       
  ≡
    
    
               [𝑛 2 := Borrowed (𝑞 2 :: 𝑞𝑠 2 )] 𝑝
                                                     
                                                     
                                                                                 ≡                                                ) 𝑝𝑟
                                                                                   
                                                                                      ★ ⌊∀ 𝑞 ∈ 𝑞𝑠 . 𝑞 = 𝑝 ⌋                           
                                                                                                                                       
     ★ Cell 𝑣 1 𝑞 1 ★ Cell 𝑣 2 𝑞 2                                                                  𝑟      𝑟
                                                                                                                                    
                                                     
       memswap(𝑞 1 , 𝑞 2 )                                                        ≡ { ♭ (Trees 𝑅) (rotL (Offered 𝑡 (𝑝 :: []))) 𝑝𝑟 }
     CListe 𝑙 [𝑛 1 := Borrowed (𝑞 1 :: 𝑞𝑠 1 )] 
                                                                                      ) else p
                                                                                      Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed (𝑝𝑟 :: 𝑞𝑠𝑟 ))) 𝑝
    
                                                    
                                                     
                [𝑛 2 := Borrowed (𝑞 2 :: 𝑞𝑠 2 )] 𝑝
                                                                                                                                     
    
     ★ Cell 𝑣 𝑞 ★ Cell 𝑣 𝑞                          
                   2 1         1 2
                                                     
                                                                                         ★ Trees 𝑅 Leafs 𝑝𝑟
      CListe 𝑙 [𝑛 1 := Offered 𝑣 2 (𝑞 1 :: 𝑞𝑠 1 )]                                ≡ { Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Offered Leafs (𝑝𝑟 :: 𝑞𝑠𝑟 ))) 𝑝 }
                                                    
  ≡
               [𝑛 2 := Offered 𝑣 1 (𝑞 2 :: 𝑞𝑠 2 )] 𝑝
                                                                                  ⊢ { Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Available Leafs 𝑞𝑠𝑟 )) 𝑝 }
                                                                                    (                                                   )
C       Proof of Binary-Tree Left Rotation                                            ♭
                                                                                        (Trees 𝑅) (Offered
                                                                                  ≡
                                                                                            (Nodes 𝑥 𝑡𝑙′ (Available Leafs 𝑞𝑠𝑟 )) [𝑝]) 𝑝
    { Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Available 𝑡𝑟 𝑞𝑠𝑟 )) 𝑝 }
       let pr := p.rtree in                                                       ≡ { ♭ (Trees 𝑅) (rotL (Offered 𝑡 [𝑝])) 𝑝𝑟 }
    { Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Offered 𝑡𝑟 (𝑝𝑟 :: 𝑞𝑠𝑟 ))) 𝑝 }
                                                                                Acknowledgments
      Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed (𝑝𝑟 :: 𝑞𝑠𝑟 ))) 𝑝
                                                      
  ≡                                                                             We thank Jade Philipoom for early discussions on this topic.
         ★ Trees 𝑅 𝑡𝑟 𝑝𝑟                                                        We also thank Aurèle Barrière, Arthur Charguéraud, Gre-
           if not (_is_empty pr) then (                                         gory Malecha, Alexandre Moine, François Pottier, and the
        
          Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed (𝑝𝑟 :: 𝑞𝑠𝑟 ))) 𝑝
                                                                               anonymous reviewers for their valuable feedback and sug-
                                                                                gestions.
             ★ Trees 𝑅 (Nodes 𝑥𝑟 𝑡𝑟𝑙′ 𝑡𝑟𝑟
                                       ′
                                          ) 𝑝𝑟
             let prl := pr.ltree in
          Trees 𝑅 (Nodes 𝑥 𝑡𝑙′ (Borrowed (𝑝𝑟 :: 𝑞𝑠𝑟 ))) 𝑝
                                                         

             ★ Trees 𝑅 (Nodes 𝑥𝑟 (pin 𝑡𝑟𝑙′ 𝑝𝑟𝑙 ) 𝑡𝑟𝑟
                                                  ′
                                                     ) 𝑝𝑟
Precise Reasoning about Container-Internal Pointers with Logical Pinning                                        CPP ’26, January 12–13, 2026, Rennes, France


References                                                                          [15] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and
 [1] 2025. Containers Library - Cppreference.Com. Retrieved 2025-07-                     Derek Dreyer. 2024. RefinedRust: A Type System for High-Assurance
     23 from https://en.cppreference.com/w/cpp/container.html#Iterator_                  Verification of Rust Programs. Proceedings of the ACM on Programming
     invalidation                                                                        Languages 8, PLDI (June 2024), 192:1115–192:1139. doi:10.1145/3656422
 [2] 2025. Spdlog: Fast C++ Logging Library. Retrieved 2025-07-23 from              [16] Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust Verification
     https://github.com/gabime/spdlog/tree/v1.x                                          by Functional Translation. Proceedings of the ACM on Programming
 [3] Michael Abbott, Thorsten Altenkirch, Neil Ghani, and Conor McBride.                 Languages 6, ICFP (Aug. 2022), 116:711–116:741. doi:10.1145/3547647
     2003. Derivatives of Containers. In Typed Lambda Calculi and Appli-            [17] Gérard Huet. 1997. The Zipper. Journal of Functional Programming 7,
     cations, Martin Hofmann (Ed.). Springer, Berlin, Heidelberg, 16–30.                 5 (Sept. 1997), 549–554. doi:10.1017/S0956796897002864
                                                                                    [18] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak,
     doi:10.1007/3-540-44904-3_2
                                                                                         Lars Birkedal, and Derek Dreyer. 2018. Iris from the Ground up: A
 [4] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J.
                                                                                         Modular Foundation for Higher-Order Concurrent Separation Logic.
     Summers. 2019. Leveraging Rust Types for Modular Specification and
                                                                                         Journal of Functional Programming 28 (Jan. 2018), e20. doi:10.1017/
     Verification. In Object-Oriented Programming Systems, Languages, and
                                                                                         S0956796818000151
     Applications (OOPSLA), Vol. 3. ACM, 147:1–147:30. doi:10.1145/3360573
                                                                                    [19] Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen, Aaron
 [5] Aaron Bohannon, J. Nathan Foster, Benjamin C. Pierce, Alexandre
                                                                                         Turon, Lars Birkedal, and Derek Dreyer. 2015. Iris: Monoids and Invari-
     Pilkiewicz, and Alan Schmitt. 2008. Boomerang: Resourceful Lenses
                                                                                         ants as an Orthogonal Basis for Concurrent Reasoning. In Proceedings
     for String Data. In Proceedings of the 35th Annual ACM SIGPLAN-
                                                                                         of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of
     SIGACT Symposium on Principles of Programming Languages (POPL
                                                                                         Programming Languages (POPL ’15). Association for Computing Ma-
     ’08). Association for Computing Machinery, New York, NY, USA, 407–
                                                                                         chinery, New York, NY, USA, 637–650. doi:10.1145/2676726.2676980
     419. doi:10.1145/1328438.1328487
                                                                                    [20] Daan Leijen and Anton Lorenzen. 2023. Tail Recursion Modulo Con-
 [6] Richard Bornat, Cristiano Calcagno, Peter O’Hearn, and Matthew
                                                                                         text: An Equational Approach. Proceedings of the ACM on Programming
     Parkinson. 2005. Permission Accounting in Separation Logic. In Pro-
                                                                                         Languages 7, POPL (Jan. 2023), 40:1152–40:1181. doi:10.1145/3571233
     ceedings of the 32nd ACM SIGPLAN-SIGACT Symposium on Principles
                                                                                    [21] Conor McBride. 2001. The Derivative of a Regular Type Is Its Type of
     of Programming Languages (POPL ’05). Association for Computing Ma-
                                                                                         One-Hole Contexts. (2001). http://strictlypositive.org/diff.pdf
     chinery, New York, NY, USA, 259–270. doi:10.1145/1040305.1040327
                                                                                    [22] Yasuhiko Minamide. 1998. A Functional Representation of Data
 [7] John Boyland. 2003. Checking Interference with Fractional Permis-
                                                                                         Structures with a Hole. In Proceedings of the 25th ACM SIGPLAN-
     sions. In Proceedings of the 10th International Conference on Static
                                                                                         SIGACT Symposium on Principles of Programming Languages (POPL
     Analysis (SAS’03). Springer-Verlag, Berlin, Heidelberg, 55–72. doi:10.
                                                                                         ’98). Association for Computing Machinery, New York, NY, USA, 75–84.
     5555/1760267.1760273
                                                                                         doi:10.1145/268946.268953
 [8] Qinxiang Cao, Shengyi Wang, Aquinas Hobor, and Andrew W. Appel.
                                                                                    [23] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Au-
     2019. Proof Pearl: Magic Wand as Frame. arXiv:1909.08789 doi:10.
                                                                                         tomatic Verification of Iterated Separating Conjunctions Using Sym-
     48550/arXiv.1909.08789
                                                                                         bolic Execution. In Computer Aided Verification, Swarat Chaudhuri
 [9] Arthur Charguéraud. 2016. Higher-Order Representation Predicates in
                                                                                         and Azadeh Farzan (Eds.). Springer International Publishing, Cham,
     Separation Logic. In Proceedings of the 5th ACM SIGPLAN Conference on
                                                                                         405–425. doi:10.1007/978-3-319-41528-4_22
     Certified Programs and Proofs (CPP 2016). Association for Computing
                                                                                    [24] Peter O’Hearn. 2019. Separation Logic. Commun. ACM 62, 2 (Jan.
     Machinery, New York, NY, USA, 3–14. doi:10.1145/2854065.2854068
                                                                                         2019), 86–95. doi:10.1145/3211968
[10] Arthur Charguéraud. 2023. A Modern Eye on Separation Logic for
                                                                                    [25] Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local
     Sequential Programs. Thesis. Université de Strasbourg. https://inria.
                                                                                         Reasoning about Programs That Alter Data Structures. In Proceedings
     hal.science/tel-04076725
                                                                                         of the 15th International Workshop on Computer Science Logic (CSL ’01).
[11] Andreea Costea, Amy Zhu, Nadia Polikarpova, and Ilya Sergey. 2020.
                                                                                         Springer-Verlag, Berlin, Heidelberg, 1–19. doi:10.5555/647851.737404
     Concise Read-Only Specifications for Better Synthesis of Programs
                                                                                    [26] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable
     with Pointers. In Programming Languages and Systems, Peter Müller
                                                                                         Data Structures. In Proceedings 17th Annual IEEE Symposium on Logic
     (Ed.). Springer International Publishing, Cham, 141–168. doi:10.1007/
                                                                                         in Computer Science. IEEE Computer Society, 55–74. doi:10.1109/LICS.
     978-3-030-44914-8_6
                                                                                         2002.1029817
[12] Chris Fallin. 2020. Safe, Flexible Aliasing with Deferred Borrows. In
                                                                                    [27] The Rust Project Developers. 2025. Slice::Get_disjoint_mut - The
     34th European Conference on Object-Oriented Programming (ECOOP
                                                                                         Rust Standard Library. Retrieved 2025-09-12 from https://doc.rust-
     2020) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 166),
                                                                                         lang.org/std/primitive.slice.html#method.get_disjoint_mut
     Robert Hirschfeld and Tobias Pape (Eds.). Schloss Dagstuhl – Leibniz-
                                                                                    [28] The Rust Project Developers. 2025. Splitting Borrows - The Rustonomi-
     Zentrum für Informatik, Dagstuhl, Germany, 30:1–30:26. doi:10.4230/
                                                                                         con. Retrieved 2025-09-12 from https://doc.rust-lang.org/nomicon/
     LIPIcs.ECOOP.2020.30
                                                                                         borrow-splitting.html
[13] John Nathan Foster. 2009. Bidirectional Programming Languages. Ph. D.
                                                                                    [29] Shengyi Wang, Qinxiang Cao, Anshuman Mohan, and Aquinas Hobor.
     Dissertation. University of Pennsylvania.
                                                                                         2019. Certifying Graph-Manipulating C Programs via Localizations
[14] Yawen Guan and Clément Pit-Claudel. 2025. Artifact: Precise Reasoning
                                                                                         within Data Structures. Proceedings of the ACM on Programming
     about Container-Internal Pointers with Logical Pinning. doi:10.5281/
                                                                                         Languages 3, OOPSLA (Oct. 2019), 171:1–171:30. doi:10.1145/3360597
     zenodo.17815704
                                                                                    Received 2025-09-03; accepted 2025-11-13
