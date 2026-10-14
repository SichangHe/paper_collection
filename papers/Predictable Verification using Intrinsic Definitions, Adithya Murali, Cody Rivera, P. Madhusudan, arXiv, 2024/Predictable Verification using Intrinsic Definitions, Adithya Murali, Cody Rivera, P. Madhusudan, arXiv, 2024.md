                                         Predictable Verification using Intrinsic Definitions
                                         ADITHYA MURALI, University of Illinois at Urbana-Champaign, USA
                                         CODY RIVERA, University of Illinois at Urbana-Champaign, USA
                                         P. MADHUSUDAN, University of Illinois at Urbana-Champaign, USA
arXiv:2404.04515v2 [cs.PL] 30 Apr 2024




                                         We propose a novel mechanism of defining data structures using intrinsic definitions that avoids recursion and
                                         instead utilizes monadic maps satisfying local conditions. We show that intrinsic definitions are a powerful
                                         mechanism that can capture a variety of data structures naturally. We show that they also enable a predictable
                                         verification methodology that allows engineers to write ghost code to update monadic maps and perform
                                         verification using reduction to decidable logics. We evaluate our methodology using Boogie and prove a suite
                                         of data structure manipulating programs correct.
                                         CCS Concepts: • Software and its engineering → Formal software verification; • Theory of computation
                                         → Logic and verification; Automated reasoning.
                                         Additional Key Words and Phrases: Predictable Verification, Intrinsic Definitions, Verification of Linked Data
                                         Structures, Decidability, Ghost-Code Annotations
                                         ACM Reference Format:
                                         Adithya Murali, Cody Rivera, and P. Madhusudan. 2024. Predictable Verification using Intrinsic Definitions.
                                         Proc. ACM Program. Lang. 8, PLDI, Article 220 (June 2024), 42 pages. https://doi.org/10.1145/3656450

                                         1   INTRODUCTION
                                         In computer science in general, and program verification in particular, classes of finite structures
                                         (such as data structures) are commonly defined using recursive definitions (aka inductive definitions).
                                         Proving that a set of structures is in such a class or proving that structures in the class have a
                                         property is naturally performed using induction, typically mirroring the recursive structure in its
                                         definition. For example, trees in pointer-based heaps can be defined using the following recursive
                                         definition in first-order logic (FOL) with least fixpoint semantics for definitions:
                                                    tree(𝑥) ::=lfp 𝑥 = nil ∨ 𝑥 ≠ nil ∧ tree(𝑙 (𝑥)) ∧ tree(𝑟 (𝑥))
                                                                                                                                                          
                                                                     ∧ 𝑥 ∉ htree(𝑙 (𝑥)) ∧ 𝑥 ∉ htree(𝑟 (𝑥)) ∧ htree(𝑙 (𝑥)) ∩ htree(𝑟 (𝑥)) = ∅                     (1)
                                                  htree(𝑥) ::=lfp 𝑖𝑡𝑒 (𝑥 = nil, ∅, htree (𝑙 (𝑥)) ∪ htree (𝑟 (𝑥)) ∪ {𝑥 })
                                            In the above, htree maps each location 𝑥 in the heap to the set of all locations reachable from 𝑥
                                         using 𝑙 and 𝑟 pointers, and the definition of tree uses this to ensure that the left and right trees are
                                         disjoint from each other and the root. Definitions in separation logic are similar (with heaplets being
                                         implicitly defined, and disjointness expressed using the separating conjunction ’★’ [51, 52, 59]).
                                            When performing imperative program verification, we annotate programs with loop invariants
                                         and contracts for methods, and reduce verification to validation of Hoare triples of the form {𝛼 }𝑠{𝛽},
                                         where 𝑠 is a straight-line program (potentially with calls to other methods encoded using their
                                         Authors’ addresses: Adithya Murali, University of Illinois at Urbana-Champaign, Urbana, USA, adithya5@illinois.edu; Cody
                                         Rivera, University of Illinois at Urbana-Champaign, Urbana, USA, codyjr3@illinois.edu; P. Madhusudan, University of
                                         Illinois at Urbana-Champaign, Urbana, USA, madhu@illinois.edu.

                                         Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
                                         the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses,
                                         contact the owner/author(s).
                                         © 2024 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2024/6-ART220
                                         https://doi.org/10.1145/3656450


                                                                             Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:2                                                                 Adithya Murali, Cody Rivera, and P. Madhusudan


contracts). The validity of each Hoare triple is translated to a pure logical validity question, called
the verification condition (VC). When 𝛼 and 𝛽 refer to data structure properties, the resulting VCs
are typically proved using induction on the structure of the recursive definitions. Automation of
program verification reduces to automating validity of the logic the VCs are expressed in.
   Logics that are powerful enough to express rich properties of data structures are invariably
incomplete, not just undecidable, i.e., they do not admit any automated procedure that is complete
(guaranteed to eventually prove any valid theorem, but need not terminate on invalid theorems).
For instance, validity is incomplete for both first-order logic with least fixpoints and separation
logic. Consequently, though verification frameworks like Dafny [35] support rich specification
languages, validation of verification conditions can fail even for valid Hoare triples. Automated
verification engines hence support several heuristics resulting in sound but incomplete verification.
   When proofs succeed in such systems, the verification engineer is happy that automation has
taken the proof through. However, when proofs fail, as they often do, the verification engineer
is stuck and perplexed. First, they would crosscheck to see whether their annotations are strong
enough and that the Hoare triples are indeed valid. If they believe they are, they do not have clear
guidelines to help the tool overcome its incompleteness. Engineers are instead required to know
the underlying proof mechanisms/heuristics the verification system uses in order to figure out why
the system is unable to succeed, and figure out how to help the system. For instance, for data
structures with recursive definitions, the proof system may just unfold definitions a few times,
and the engineer must be able to see why this heuristic will not be able to prove the theorem
and formulate new inductively provable lemmas or quantification triggers that can help. Such
unpredictable verification systems that require engineers to know their internal heuristics and
proof mechanisms frustrate verification experience.
Predictable Verification. In this paper, we seek an entirely new paradigm of predictable verification.
We want a technique where:
(a) the verification engineer is asked to provide upfront a set of annotations that help prove
      programs correct, where these annotations are entirely independent of the verification mech-
      anisms/tools, and
(b) the program verification problem, given these annotations, is guaranteed to be decidable (and
      preferably decidable using efficient engines such as SMT solvers).
  The upfront agreement on the information that the verification engineer is required to provide
makes their task crystal clear. The fact that the verification is decidable given these annotations
ensures that the verification engine, given enough resources of time and space (of course) will
eventually return proving the program correct or showing that the program or annotations are
incorrect. There is no second-guessing by the engineer as the verification will never fail on valid
theorems, and hence they need not worry about knowing how the verification engine works, or give
further help. Note that the verification without annotations can (and typically will be) undecidable.
Intrinsic Definitions of Data Structures. In this paper, we propose an entirely new way of
defining data structures, called intrinsic definitions, that facilitates a predictable verification paradigm
for proving their maintenance. Rather than defining data structures using recursion, like in equation
(1) above (which naturally calls for inductive proofs and invariably entails incompleteness), we
define data structures by augmenting each location with additional information using ghost maps
and demanding that certain local conditions hold between each location and its neighbors.
   Intrinsic definitions formally require a set of monadic maps (maps of arity one) that associate
values to each location in a structure (we can think of these as ghost fields associated with each
location/object). We demand that the monadic maps on local neighborhoods of every location

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                220:3


satisfy certain logical conditions. The existence of maps that satisfy the local logical conditions
ensures that the structure is a valid data structure.
  For example, we can capture trees in pointer-based heaps in the following way. Let us introduce
maps tree : 𝐿𝑜𝑐 → 𝐵𝑜𝑜𝑙, rank : 𝐿𝑜𝑐 → Q+ (non-negative rationals), and 𝑝 : 𝐿𝑜𝑐 → 𝐿𝑜𝑐 (for
“parent”), and demand the following local property:
    ∀𝑥 :: 𝐿𝑜𝑐.(tree(𝑥) ⇒( (𝑙 (𝑥) ≠ nil ⇒ (tree(𝑙 (𝑥)) ∧ 𝑝 (𝑙 (𝑥)) = 𝑥 ∧ rank(𝑙 (𝑥)) < rank(𝑥)))
                               ∧ (𝑟 (𝑥) ≠ nil ⇒ (tree(𝑟 (𝑥)) ∧ 𝑝 (𝑟 (𝑥)) = 𝑥 ∧ rank(𝑟 (𝑥)) < rank(𝑥)))
                               ∧ ((𝑙 (𝑥) ≠ nil ∧ 𝑟 (𝑥) ≠ nil) ⇒ 𝑙 (𝑥) ≠ 𝑟 (𝑥))
                               ∧ (𝑝 (𝑥) ≠ nil ⇒ (𝑟 (𝑝 (𝑥)) = 𝑥 ∨ 𝑙 (𝑝 (𝑥)) = 𝑥))) )
   The above demands that ranks become smaller as one descends the tree, that a node is the parent
of its children, and that a node is either the left or right child of its parent.
   Given a finite heap, it is easy to see that if there exist maps tree, rank and 𝑝 that satisfy the above
property, and if tree(𝑙) is true for a location 𝑙, then 𝑙 must point to a tree (strictly decreasing ranks
ensure that there are no cycles and existence of a unique parent ensures that there are no “merges”).
Furthermore, in any heap, if 𝑇 is the subset of locations that are roots of trees, then there are maps
that satisfy the above property and have precisely 𝑡𝑟𝑒𝑒 (𝑙) to be true for locations in 𝑇 .
   Note that the above intrinsic definition does not use recursion or least fixpoint semantics. It simply
requires maps such that each location satisfies the local neighborhood condition.
Fix-What-You-Break Program Verification Methodology.
   Intrinsic definitions are particularly attractive for proving maintenance of structures when
structures undergo mutation. When a program mutates a heap 𝐻 to a heap 𝐻 ′ , we start with
monadic maps that satisfy local conditions in the pre-state. As the heap 𝐻 is modified, we ask the
verification engineer to also repair the monadic maps, using ghost map updates, so that the local
conditions on all locations are met in the heap in the post-state 𝐻 ′ .
   For instance, consider a program that walks down a tree from its root to a node 𝑥 and introduces a
newly allocated node 𝑛 between 𝑥 and 𝑥’s right child 𝑟 . Then we would assume in the precondition
that the monadic maps tree, rank, and 𝑝 exist satisfying the local condition (2) above. After the
mutation, we would simply update these maps so that tree(𝑛) is true, 𝑝 (𝑟 ) = 𝑛, 𝑝 (𝑛) = 𝑥, and
𝑟𝑎𝑛𝑘 (𝑛) is, say, (rank(x) + rank(𝑟 ))/2.
   The annotations required of the user, therefore, are ghost map updates to locations such that
the local conditions are valid for each location. We will guarantee that checking whether the local
conditions holds for each location, after the repairs, is expressible in decidable logics.
   We propose a modular verification approach for verifying data structure maintenance that asks
the programmer to fix what they break. Given a program that we want to verify, we instead verify
an augmented program that keeps track of a ghost set of broken locations Br. Broken locations are
those that (potentially) do not satisfy the local condition. When the program destructively modifies
the fields of an object/location, it and some of its neighbors (accessible using pointers from the
object) may not satisfy the local condition anymore, and hence will get added to the broken set. The
verification engineer must repair the monadic maps on these broken locations and ensure (through
an assertion) that the local condition holds on them before removing them from the broken set 𝐵𝑟 .
However, even while repairing monadic maps on a location, the local condition on its neighboring
locations may fail and get added to the broken set.
   We develop a fix-what-you-break (FWYB) program verification paradigm, giving formal rules of
how to augment programs with broken sets, how users can modify monadic maps, and fixed recipes
of how broken sets are maintained in any program. In order to verify that a method 𝑚 maintains a
data structure, we need to prove that if 𝑚 starts with the broken set being empty, it returns with the

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:4                                                                  Adithya Murali, Cody Rivera, and P. Madhusudan


empty broken set. We prove this methodology sound, i.e., if the program augmented with broken
sets and ghost updates is correct, then the original program maintains the data structure properties
mentioned in its contracts.
Decidable Verification of Annotated Programs. The general idea of using local conditions to
capture global properties has been explored in the literature to reduce the complexity of proofs (e.g.,
iterated separation in separation logic [60]; see Section 6). Intrinsic definitions of data structures and
the fix-what-you-break program verification methodology are more specifically designed to ensure
the key property of decidable verification of annotated programs by avoiding both recursion/least-
fixpoint definitions and avoiding even quantified reasoning.
   The verification conditions for Hoare triples involving basic blocks of our annotated programs
have the following structure. First, the precondition can be captured using uninterpreted monadic
functions that are implicitly assumed to satisfy the local condition on each location that is not
in the broken set 𝐵𝑟 (avoiding universal quantification). The monadic map updates (repairs) that
the verification engineer makes can be captured using map updates. The postcondition of the
ghost-code augmented program can, in addition to properties of variables, assert properties of
the broken set 𝐵𝑟 using logics over sets. Finally, we show that capturing the modified heap after
function calls can be captured using parameterized map update theories, that are decidable [18].
Consequently, the entire verification condition is captured in quantifier-free logics involving maps,
parametric map updates, and sets over combined theories. These verification conditions are hence
decidable and efficiently handled by modern SMT solvers1 .
Intrinsic Definitions for Representative Data Structures and Verification in Boogie. Intrinsic
definitions of data structures is a novel paradigm and capturing data structures requires thinking
anew in order to formulate monadic maps and local conditions that characterize them.
   We give intrinsic definitions for several classic data structures such as linked lists, sorted lists,
circular lists, trees, binary search trees, AVL trees, and red-black trees. These require novel defini-
tions of monadic maps and local conditions. We also show how standard methods on these data
structures (insertions, deletions, concatenations, rotations, balancing, etc.) can be verified using the
fix-what-you-break strategy and standard loop invariant/contract annotations. We also consider
overlaid data structures consisting of multiple data structures overlapping and sharing locations.
In particular, we model the core of an overlaid data structure that is used in an I/O scheduler in
Linux that has a linked list (modeling a FIFO queue) overlaid on a binary search tree (for efficient
search over a key field). Intrinsic definitions beautifully capture such structures by compositionally
combining the instrinsic definitions for each structure and a local condition linking them together.
We show methods to modify this structure are provable using fix-what-you-break verification.
   We model the above data structures and the annotated methods in the low-level programming
language Boogie. Boogie is an intermediate programming language with verification support that
several high-level programming languages compile to for verification (e.g., C [15, 16], Dafny [35],
Civl [28], Move [19]). These annotated programs do not use quantifiers or recursive definitions,
and Boogie is able to verify them automatically using decidable verification in negligible time,
without further user-help.
Contributions. The paper makes the following contributions:
    • A new paradigm of predictable verification that asks upfront for programmatic annotations
      and ensures annotated program verification is decidable, without reliance on users to give
      heuristics and tactics.
1 Assuming of course that the underlying quantifier-free theories are decidable; for example, integer multiplication in the

program or in local conditions would make verification undecidable, of course.


Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                220:5


      • A novel notion of intrinsic definitions of data structures based on ghost monadic maps and
        local conditions.
      • A predictable verification methodology for programs that manipulate data structures with
        intrinsic definitions following a fix-what-you-break (FWYB) methodology.
      • Intrinsic definitions for several classic data structures, and fix-what-you-break annotations
        for programs that manipulate such structures, with realization of these programs and their
        verification using Boogie.

2     INTRINSIC DEFINITIONS OF DATA STRUCTURES: THE FRAMEWORK
In this section we present the first main contribution of our paper, the framework of intrinsically
defined data structures. We first define the notion of a data structure in a pointer-based heap.

2.1    Data Structures
In this paper, we think of data structures defined using a class 𝐶 of objects. The class 𝐶 can coexist
with other classes, heaps, and data structures, potentially modeled and reasoned with using other
mechanisms. For technical exposition and simplicity, we restrict the technical definitions to a single
class of data structures over a class 𝐶.
   A class 𝐶 has a signature (S, F ) consisting of a finite set of sorts S = {𝜎0, 𝜎1 . . . , 𝜎𝑛 } and a finite
set of fields F = {𝑓1, 𝑓2 . . . , 𝑓𝑚 }. We assume without loss of generality that the sort 𝜎0 represents
the sort of objects of the class 𝐶, and we denote this sort by 𝐶 itself. We use 𝐶 to model objects in
the heap. The other “background” sorts, e.g., integers, are used to model the values of the objects’
fields. Each field 𝑓𝑖 : 𝐶 → 𝜎 is a unary function symbol and is used to model pointer and data
fields of heap locations/objects. We model nil as a non-object value and denote the sort 𝐶 ⊎ {nil}
consisting of objects as well as the nil value by 𝐶?.
   A 𝐶-heap 𝐻 is a finite first-order model of the signature of 𝐶. More formally, it is a pair (𝑂, 𝐼 )
where 𝑂 is a finite set of objects interpreting the foreground sort 𝐶 and 𝐼 is an interpretation of
every field in F for every object in 𝑂.
   Example 2.1 (𝐶-Heap). Let 𝐶 be the class consisting of a pointer              next             next
                                                                             𝑜1             𝑜2           nil
   field next : 𝐶 → 𝐶? and a data field key : 𝐶 → Int. The figure on
   the right represents a 𝐶-heap consisting of objects 𝑂 = {𝑜 1, 𝑜 2 }         key             key
   and the illustrated interpretation 𝐼 for next and key.             □      1               2
We now define a data structure. We fix a class 𝐶.
  Definition 2.2 (Data Structure). A data structure 𝐷 of arity 𝑘 is a set of triples of the form (𝑂, 𝐼, 𝑜)
such that (𝑂, 𝐼 ) is a 𝐶-heap and 𝑜 is a 𝑘-tuple of objects from 𝑂.                                      □
   Informally, a data structure is a particular subset of 𝐶-heaps along with a distinguished tuple of
locations 𝑜 in the heap that serve as the “entry points” into the data structure, such as the root of a
tree or the ends of a linked list segment.
   Example 2.3 (Sorted Linked List). Let 𝐶 be the class defined in Example 2.1. The data structure
of sorted linked lists is the set of all (𝑂, 𝐼, 𝑜 1 ) such that 𝑂 contains objects 𝑜 1, 𝑜 2 . . . 𝑜𝑛 with the
interpretation next (𝑜𝑖 ) = 𝑜𝑖+1 and key(𝑜𝑖 ) ≤ key(𝑜𝑖+1 ) for every 1 ≤ 𝑖 < 𝑛, and next (𝑜𝑛 ) = nil. For
example, let (𝑂, 𝐼 ) be the 𝐶-heap described in Example 2.1. The triple (𝑂, 𝐼, 𝑜 1 ) is an example of a
sorted linked list. Here 𝑜 1 represents the head of the sorted linked list.                                 □

2.2    Intrinsic Definitions of Data Structures
In this work, we propose a characterization of data structures using intrinsic definitions. Intrinsic
definitions consist of a set of monadic maps that associate (ghost) values to each object and a set of

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:6                                                                 Adithya Murali, Cody Rivera, and P. Madhusudan


local conditions that constrain the monadic maps on each location and its neighbors. A 𝐶-heap is
considered to be a valid data structure if there exists a set of monadic maps for the heap that satisfy
the local conditions.
   Annotations using intrinsic definitions enable local and decidable reasoning for correctness of
programs manipulating data structures using the Fix-What-You-Break (FWYB) methodology, which
is described later in Section 3. We develop the core idea of intrinsic definitions below.
Ghost Monadic Maps. We denote by 𝐶 G = (S, F ∪ G) an extension of 𝐶 with a finite set of
monadic (i.e., unary) function symbols G. We can think of these as ghost fields of objects.
   The key idea behind intrinsic definitions is to extend a 𝐶-heap with a set of ghost monadic
maps and formulate local conditions using the maps that characterize the heaps belonging to
the data structure. The existence of such ghost maps satisfying the local conditions is then the
intrinsic definition. Definitions are parameterized by a multi-sorted first-order logic L in which
local conditions are stated. The logic has the sorts S and contains the function symbols in F ∪ G,
as well as interpreted functions over background sorts (such as + and < on integers, and ⊆ on sets).
   Definition 2.4 (Intrinsic Definition). Let 𝐶 = (S, F ) be a class. An intrinsic definition IDS(𝑦) over
the class 𝐶 is a tuple (G, L, LC, 𝜑 (𝑦)) where:
   (1) G is a finite set of monadic map names and function signatures disjoint from F ,
   (2) L is a first-order logic over the sorts S containing the interpreted functions of the background
       sorts as well as the function symbols in F ∪ G,
   (3) A local condition formula LC of the form ∀𝑥 : 𝐿𝑜𝑐. 𝜌 (𝑥) such that 𝜌 is a quantifier-free
       L-formula, and
   (4) A correlation formula 𝜑 (𝑦) that is a quantifier-free L-formula over free variables 𝑦 ∈ 𝐿𝑜𝑐. □
   We denote an intrinsic definition by (G, LC, 𝜑 (𝑦)) when the logic L is clear from context. In
this work L is typically a decidable combination of quantifier-free theories [48, 49, 64], containing
theories of integers, sets, arrays [18], etc., supported effectively in practice by SMT solvers [7, 17].
   Definition 2.5 (Data Structures defined by Intrinsic Definitions). Let 𝐶 = (S, F ) be a class and
IDS(𝑦) = (G, LC, 𝜑 (𝑦)) be an intrinsic definition over 𝐶 consisting of monadic maps G, local
condition LC and correlation formula 𝜑. The data structure defined by IDS is precisely the set of all
(𝑂, 𝐼, 𝑜) where there exists an interpretation 𝐽 that extends 𝐼 with interpretations for the symbols
in G such that 𝑂, 𝐽 |= 𝐿𝐶 and 𝑂, 𝐽 [𝑦 ↦→ 𝑜] |= 𝜑 (𝑦), where [𝑦 ↦→ 𝑜] denotes that the free variables
𝑦 are interpreted as 𝑜.
   Informally, given a data structure DS consisting of triples (𝑂, 𝐼, 𝑜), an intrinsic definition demands
that there exist monadic maps G such that the 𝐶-heaps (𝑂, 𝐼 ) in the data structure can be extended
with values for maps in G satisfying the local conditions LC, and the entrypoints 𝑜 are characterized
in the extension by the quantifier-free formula 𝜑.
   Example 2.6 (Sorted Linked List). Recall the data structure of sorted linked lists defined in Exam-
ple 2.3. We capture sorted linked lists by an intrinsic definition SortedLL(𝑦) using monadic maps
sortedll : 𝐶 → Bool and rank : 𝐶 → Q+ such that:
             
  LC ≡ ∀𝑥 . (sortedll(𝑥) ∧ next (𝑥) ≠ nil) ⇒                                                         
                           (sortedll(next (𝑥)) ∧ rank(next (𝑥)) < rank(𝑥) ∧ key(𝑥) ≤ key(next (𝑥)))
𝜑 (𝑦) ≡ sortedll(𝑦)
   In the above definition the rank field decreases wherever sortedll holds as we take the next
pointer, and hence assures that there are no cycles. Observe that without the constraint on rank,
the triple ({𝑜 1, 𝑜 2 }, 𝐼, 𝑜 1 ) where 𝐼 = {next (𝑜 1 ) = 𝑜 2, next (𝑜 2 ) = 𝑜 1, key(𝑜 1 ) = key(𝑜 2 ) = 0} denoting
a two-element circular list would satisfy the definition, which is undesirable.

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                220:7



     𝑃 B 𝑥 := nil | 𝑥 := 𝑦 | 𝑣 := 𝑏𝑒 | 𝑦 := 𝑥 .𝑓 | 𝑣 := 𝑥 .𝑑
         | 𝑥 .𝑓 := 𝑦 | 𝑥 .𝑑 := 𝑣 | 𝑥 := new 𝐶 () | 𝑟 := Function(𝑡)
         | skip | assume cond | return | 𝑃 ; 𝑃 | if cond then 𝑃 else 𝑃 | while cond do 𝑃
  cond B 𝑥 = 𝑦 | 𝑥 ≠ 𝑦 | be (Condition Expressions)
Fig. 1. Grammar of while programs with recursion. 𝑥, 𝑦 are variables denoting objects of class 𝐶? (i.e., 𝐶
objects or nil), 𝑣, 𝑤 are a background sort(s) variables, 𝑟, 𝑡 denote variables of any sort, 𝑓 is a pointer field, 𝑑 is
a data field, and 𝑏𝑒 is a expression of the background sort(s).


  Note that the above allows for a heap to contain both sorted lists as well as unsorted lists. We
are guaranteed by the local condition that the set of all objects where sortedll is true will be the
heads of sorted lists.
  We can also replace the domain of ranks in the above definition using any strict partial order,
say integers or reals (with the usual < order on them), and the definition will continue to define
sorted lists. Well-foundedness of the order is not important as heaps are finite in our work (see
definition of 𝐶-heaps in Section 2.1)                                                              □

3 FIX WHAT YOU BREAK (FWYB) VERIFICATION METHODOLOGY
In this section we present the second main contribution of this paper: the Fix-What-You-Break
(FWYB) methodology. We begin by describing a while programming language and defining the
verification problem we study. We fix a class 𝐶 = (S, F ) throughout this section.

3.1    Programs, Contracts, and Correctness
Programs. Figure 1 shows the programming language used in this work. Note that we can use
variables and expressions over non-object sorts. Functions can return multiple outputs. We assume
that method signatures contain designated output variables and therefore the return statement
does not mention values.
   Our language is safe (i.e., allocated locations cannot point to un-allocated locations) and garbage-
collected. Formally we consider configurations 𝜃 consisting of a store (map from variables to values)
and a heap along with an error state ⊥ to model error on a null dereference. We denote that a
formula 𝛼 is satisfied on a configuration 𝜃 by writing 𝜃 |= 𝛼.
Intrinsic Hoare Triples. The verification problem we study in this paper is maintenance of data
structure properties. Fix an intrinsic definition (G, LC, 𝜑 (𝑦)) where G = {𝑔1, 𝑔2 . . . , 𝑔𝑘 }. Let 𝑧 be the
input/output variables for a program that we want to verify. We consider pre and post conditions
of the form
                                    ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑘 . (LC ∧ 𝜑 (𝑤) ∧ 𝜓 (𝑧))
where each 𝑔𝑖 is a ghost monadic map (unary function over locations), 𝜓 is a quantifier-free formula
over 𝑧 that can use the ghost monadic maps 𝑔𝑖 , and 𝑤 is a tuple of variables from 𝑧 whose arity
is equal to 𝑦. Note that the above has a second-order existential quantification (∃∃) over function
symbols 𝑔1, . . . , 𝑔𝑘 , and LC has first-order universal quantification over a single location variable.
Read in plain English, “ 𝑤 points to a data structure IDS such that the (quantifier-free) property
𝜓 (𝑧) holds”.
We study the validity of the following Hoare Triples:
                                      ⟨ 𝛼 (𝑥) ⟩ P(𝑥, ret : 𝑟 ) ⟨ 𝛽 (𝑥, 𝑟 ) ⟩
where 𝛼 and 𝛽 are pre and post conditions of the above form, P is a program, and 𝑥, 𝑟 are input and
output variables for P respectively.

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:8                                                                   Adithya Murali, Cody Rivera, and P. Madhusudan


   Example 3.1 (Running Example: Insertion into a Sorted List). Let SortedLL(𝑦) = (G, LC, sorted (𝑦))
as in Example 2.6 where G = {sortedll, rank}. The following Hoare triple says that insertion into a
sorted list returns a sorted list:
 ⟨ ∃ sortedll, rank. LC ∧ sortedll(𝑥) ⟩ sorted−insert (𝑥, 𝑘, ret : 𝑥) ⟨ ∃ sortedll, rank. LC ∧ sortedll(𝑥) ⟩
where 𝑥, 𝑟 are variables of type 𝐶, 𝑘 is of type Int and sorted−insert is the usual recursive method.

Validity of Intrinsic Hoare Triples. We now define the validity of Hoare Triples.
  Definition 3.2 (Validity of Intrinsic Hoare Triples). An intrinsic triple ⟨ 𝛼 ⟩ 𝑃 ⟨ 𝛽 ⟩ is valid if for
every configuration 𝜃 such that 𝜃 |= 𝛼, transitioning according to 𝑃 starting from 𝜃 does not
encounter the error state ⊥, and furthermore, if 𝜃 transitions to 𝜃 ′ under 𝑃, then 𝜃 ′ |= 𝛽.

3.2     Ghost Code
In this work we consider the augmentation of procedures with ghost or non-executed code. Ghost
code involves the manipulation of a set of distinct ghost variables and ghost fields, distinguished from
regular or ‘user’ variables and fields. In program verification, ghost code provides a programmatic
way of constructing values/functions that witness a particular property.
   We defer a formal definition of ghost code to the Appendix of our supplementary material2 and
only provide intuition here. Intuitively, ghost variables/fields cannot influence the computation
of non-ghost variables/fields. Therefore, ghost variables and maps can be assigned values from
user variables and maps, but the reverse is not allowed. Similarly, when conditional statements
or loops use ghost variables in the condition, the body of the statement must also consist entirely
of ghost code. Simply, ghost code cannot control the flow of the user program. These conditions
can be checked statically. Finally, we also require that ghost loops and functions always terminate
since nonterminating ghost code can change the meaning of the original program. Our definition
is agnostic to the technique used to establish termination, however, we use ranking functions to
establish termination in our implementation in Dafny.
   We formalize the above into a grammar that extends the original programming language in
Figure 1 into a ghost code-augmented language in Figure 6 in Appendix A.2 of our supplementary
material. The language of ghost programs is similar to 𝑃 in Figure 1, except that we do not have
allocation or assume statements, and loops/functions must always terminate. See prior literature
for a more detailed formal treatment of ghost code [23, 27, 38, 58].
Projection that Eliminates Ghost Code. We can define the notion of ‘projecting out’ ghost code,
which takes a program that contains ghost code and yields a pure user program with all ghost
code simply eliminated. Intuitively, the fact that ghost code does not affect the execution of the
underlying user program makes the projection operation sensible.
   Fix a main method 𝑀 with body 𝑃. Let 𝑁𝑖 , 1 ≤ 𝑖 ≤ 𝑘 be a set of auxiliary methods with bodies
𝑄𝑖 that 𝑃 can call. Note that the bodies 𝑃 and 𝑄𝑖 contain ghost code. Let us denote a program
containing these methods by [(𝑀 : 𝑃); (𝑁 1 : 𝑄 1 ) . . . (𝑁𝑘 : 𝑄𝑘 )]. We then define projection as
follows:
   Definition 3.3 (Projection of Ghost-Augmented Code to User Code). The projection of the ghost-
augmented program [(𝑀 : 𝑃); (𝑁 1 : 𝑄 1 ) . . . (𝑁𝑘 : 𝑄𝑘 )] is the user program [( 𝑀ˆ : 𝑃);
                                                                                         ˆ ( 𝑁ˆ1 :
𝑄ˆ1 ) . . . ( 𝑁ˆ𝑘 : 𝑄ˆ𝑘 )] such that:
   (1) The input (resp. output) signature of 𝑀ˆ is that of 𝑀 with the ghost input (resp. output)
          parameters removed.
2 Our supplementary material is available in either our technical report [47] or the permanent DOI record at https://doi.org/

10.1145/3656450.


Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                220:9


   (2) 𝑃ˆ is derived from 𝑃 by: (a) eliminating all ghost code, and (b) replacing each non-ghost
       function call statement of the form 𝑟 := 𝑁 𝑗 (𝑡) with the statement 𝑠 := 𝑁ˆ 𝑗 (𝑢), where 𝑢 is the
       non-contiguous subsequence of 𝑡 with the elements corresponding to ghost input parameters
       removed and 𝑠 is obtained from 𝑟 similarly. Each 𝑄ˆ𝑖 is derived from the corresponding 𝑄𝑖 by
       a similar transformation.

   We provide an expanded version of this definition in our supplementary material in Appendix A.2.

An Overview of FWYB
We develop the Fix-What-You-Break (FWYB) methodology in three stages, in the following subsec-
tions. We give here an overview of the methodology and the stages.
   Recall that intrinsic triples are of the form ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑘 . (LC ∧𝜑 ∧𝛼) ⟩ 𝑃 ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑘 . (LC ∧
𝜑 ∧ 𝛽) ⟩. In Stage 1 (Section 3.3) we remove the second-order quantification. We do this by requiring
the verification engineer to explicitly construct the 𝑔𝑖 maps in the post state from the maps in the
pre state using ghost code. We then obtain triples of the form ⟨ LC ∧ 𝜑 ∧ 𝛼 ⟩ 𝑃 G ⟨ LC ∧ 𝜑 ∧ 𝛽 ⟩ where
𝑃 G is an augmentation of 𝑃 with ghost code that updates the G maps.
   Note that the LC in the contract universally quantifies over objects. In Stages 2 (Section 3.4)
and 3 (Section 3.5) we remove the quantification by explicitly tracking the objects where the local
conditions do not hold and treating them as implicitly true on all other objects. We call this set
Br the broken set. Intuitively, the broken set grows when the program mutates pointers or makes
other changes to the heap, and shrinks when the verification engineer repairs the G maps using
ghost code to satisfy the LC on the broken objects. The specifications assume an empty broken
set at the beginning of the program and the engineer must ensure that it is empty again at the
end of the program. However, they do not have to track the objects manually. We develop in Stage
3 (Section 3.5) a discipline for writing only well-behaved manipulations of the broken set. This
reduces the problem to triples of the form ⟨ 𝜑 ∧ 𝛼 ⟩ 𝑃 G,Br ⟨ 𝜑 ∧ 𝛽 ⟩, where 𝑃 G,Br contains ghost code
for updating both G and Br. Note that these specifications are quantifier-free, and checking them
can be effectively automated using SMT solvers [7, 17].

3.3    Stage 1: Removing Existential Quantification over Monadic Maps using Ghost Code
Consider an intrinsic Hoare Triple ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑘 . (LC ∧ 𝜑 ∧ 𝛼) ⟩ 𝑃 ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑘 . (LC ∧ 𝜑 ∧ 𝛽) ⟩.
Read simply, the precondition says that there exist maps {𝑔𝑖 } satisfying some properties, and the
postcondition says that we must show the existence of maps {𝑔𝑖 } satisfying the post state properties.
  We remove existential quantification from the problem by re-formulating it as follows: we assume
that we are given the maps {𝑔𝑖 } as part of the pre state such that they satisfy LC ∧ 𝜑 ∧ 𝛼, and we
require the verification engineer to compute the {𝑔𝑖 } maps in the post state satisfying LC ∧ 𝜑 ∧ 𝛽.
The engineer computes the post state maps by taking the given pre state maps and ‘repairing’ them
on an object whenever the program breaks local conditions on that object. The repairs are done
using ghost code, which is a common technique in verification literature [23, 27, 38, 58].

   Formally, fix an intrinsically defined data structure (G, LC, 𝜑). We extend the class signature
𝐶 = (S, F ) (and consequently the programming language) to 𝐶 G = (S, F ∪ G) and treat the
symbols in G as ghost fields of objects of class 𝐶 in the program semantics. Performing the
transformation described above reduces the verification problem to proving triples of the form
⟨ LC ∧ 𝜑 ∧ 𝛼 ⟩ 𝑃 G ⟨ LC ∧ 𝜑 ∧ 𝛽 ⟩, where there is no existential quantification over G and 𝑃 G is an
augmentation of 𝑃 with ghost code that updates the G maps. The following proposition captures
the correctness of this reduction:


                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:10                                                                  Adithya Murali, Cody Rivera, and P. Madhusudan


   Proposition 3.4. Let 𝜓 pre and 𝜓 post be quantifier-free formulae over F ∪G. If ⟨ LC∧𝜓 pre ⟩ 𝑃 G ⟨ LC∧
𝜓 post ⟩ is valid then ⟨ ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 pre ⟩ 𝑃 ⟨ ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 post ⟩ is valid 3 , where 𝑃 is
the projection of 𝑃 G obtained by eliminating ghost code.
   Proof Gist. The full proof is in our supplementary material. The first Hoare triple shows that
if we are given any maps 𝑔𝑖 (implicitly encoded as values of ghost fields) that satisfy 𝐿𝐶 in the
pre-state, then the program with ghost code computes a modified version of these maps such that
the 𝐿𝐶 is holds in the post-state. Surely then, if there was a set of maps 𝑔𝑖 that satisfied 𝐿𝐶 in the
pre-state, there will exists a set of maps 𝑔𝑖′ that satisfy 𝐿𝐶 in the post-state.                    □
We note a point of subtlety about the reduction in this stage here: the simplified triple eliminates
existential quantification over G by claiming something stronger than the original specification,
namely that for any maps {𝑔𝑖 } such that 𝜓 pre is satisfied in the pre state, there is a computation that
yields corresponding maps in the post state such that 𝜓 post holds. The onus of coming up with such
a computation is placed on the verification engineer.

3.4      Stage 2: Relaxing Universal Quantification using Broken Sets
We turn to verifying programs whose pre and post conditions are of the form LC ∧ 𝛾, where
LC ≡ ∀𝑧. 𝜌 (𝑧) is the local condition. Consider a program 𝑃 that maintains the data structure. The
local conditions are satisfied everywhere in both the pre and post state of 𝑃. However, they need
not hold everywhere in the intermediate states. In particular, 𝑃 may call a method 𝑁 which may
neither receive nor return a proper data structure. To reason about 𝑃 modularly we must be able
to express contracts for methods like 𝑁 . To do this we must be able to talk about program states
where only some objects may satisfy the local conditions.
Broken Sets. We introduce in programs a ghost set variable Br that represents the set of (potentially)
broken objects. Intuitively, at any point in the program the local conditions must always be satisfied
on every object that is not in the broken set. Formally, for a program 𝑃 we extend the signature of
𝑃 with Br as an additional input and an additional output. We also write pre and post conditions of
the form (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛾 to denote that local conditions are satisfied everywhere outside the
broken set, where 𝛾 can now use Br. In particular, given the Hoare triple
                            ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝛼 ⟩ 𝑃 G (𝑥, ret : 𝑦) ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝛽 ⟩
from Stage 1, we instead prove the following Hoare triple (whose validity implies the validity of
the triple above):
       ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛼 ∧ Br = ∅ ⟩ 𝑃 G,Br (𝑥, Br, ret : 𝑦, Br) ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛽 ∧ Br = ∅ ⟩
where Br is a ghost input variable of the type of set of objects and 𝑃 G,Br is an augmentation of 𝑃
with ghost code that computes the G maps as well as the Br set satisfying the postcondition.
   𝑃 may also call other methods 𝑁 with bodies 𝑄. We similarly extend the input and output
signatures of the called methods and use the broken set to write appropriate contracts for the
methods, introducing triples of the form ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛼 𝑁 ⟩ 𝑄 Br (𝑠, Br, ret : 𝑟, Br) ⟨ (∀𝑧 ∉
Br. 𝜌 (𝑧)) ∧ 𝛽 𝑁 ⟩. Again, 𝑄 G,Br is an augmentation of 𝑄 with ghost code that updates G and Br.
   For the main method that preserves the data structure property, the broken set is empty at the
beginning and end of the program. However, called methods or loop invariants can talk about
states with nonempty broken sets. We require the verification engineer to write ghost code that
maintains the broken set accurately. The soundness of this reduction is captured by the following
Proposition:
3 Here the notion of validity for both triples is given by Definition 3.2, where configurations are interpreted appropriately

with or without the ghost fields.


Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                               220:11


   Proposition 3.5. Let 𝛼 and 𝛽 be quantifier-free formulae over F ∪ G (they cannot mention Br).
If ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛼 ∧ Br = ∅ ⟩ 𝑃 G,Br (𝑥, Br, ret : 𝑦, Br) ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛽 ∧ Br = ∅ ⟩ is valid
then ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝛼 ⟩ 𝑃 G (𝑥, ret : 𝑦) ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝛽 ⟩ is valid, where 𝑃 G is the projection of 𝑃 G,Br
obtained by eliminating the statements that manipulate Br.
  The proof of this proposition is similar to the proof of Proposition 3.4, except that projections
only eliminate Br. We provide a detailed argument in our supplementary material in Appendix B.

3.5    Stage 3: Eliminating the Universal Quantifier for Well-Behaved Programs
We consider triples of the form
                   ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛼 ⟩ 𝑃 G,Br (𝑥, Br, ret : 𝑦, Br) ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛽 ⟩
where 𝑃 G,Br is a program augmented with ghost updates to the G-fields as well as the Br set, and
𝛼, 𝛽 are quantifier-free formulae that can also mention the fields in G and the Br set. In this stage
we would like to eliminate the quantified conjunct entirely and instead ask the engineer to prove
the validity of the triple
                                          {𝛼 } 𝑃 G,Br (𝑥, Br, ret : 𝑦, Br) {𝛽}
   However, the above two triples are not, in general, equivalent (as broken sets can be manipulated
wildly). In this section we define a syntactic class of well-behaved programs that force the verification
engineer to maintain broken sets correctly, and for such programs the above triple are indeed
equivalent. For example, for a field mutation, well-behaved programs require the engineer to
determine the set of impacted objects where local conditions may be broken by the mutation. The
well-behavedness paradigm then mandates that the engineer add the set of impacted objects to
the broken set immediately following the mutation statement. Similarly, well-behaved programs
do not allow the engineer to remove an object from the broken set unless they show that the
local conditions hold on that object. The imposition of this discipline ensures that programmers
carefully preserve the meaning of the broken set (i.e., objects outside the broken set must satisfy
local conditions). This allows for the quantified conjunct in the triple obtained from Stage 2 to be
dropped since it always holds for a well-behaved program. Let us look at such a program:
  Example 3.6 (Well-Behaved Sorted List Insertion). We use the running example (Example 3.1) of
insertion into a sorted list. We consider a snippet where the key 𝑘 to be inserted lies between the
keys of 𝑥 and next (𝑥) (which we assume is not nil). We ignore the conditionals that determine
next (𝑥) ≠ nil and key(𝑥) ≤ 𝑘 ≤ key(next (𝑥)) for brevity.
  We first relax the universal quantification as described in Stage 2 (Section 3.4) and rewrite the pre
and post conditions to (∀ 𝑧 ∉ Br. LC (𝑧)) ∧ sortedll(𝑥) ∧ Br = ∅. Making the first conjunct implicit,
we write the following program that manipulates the broken set in a well-behaved manner. We
show the value of the broken set through the program in comments on the right:
          pre: sortedll (𝑥 ) ∧ Br = ∅                           z.sortedll := True;
          post: sortedll (𝑥 ) ∧ Br = ∅                          Br := Br ∪ {z}; // {z}
           assert x ∉ Br;                                       x.next := z;
           assume LC(x);                                        Br := Br ∪ {x}; // {x,z}
           y := x.next;         // {}                           z.rank := (x.rank + y.rank)/2;
           z := new C();                                        Br := Br ∪ {z}; // {x,z}
           Br := Br ∪ {z}; // {z}                               // x and z satisfy LC
           z.key := k;                                          assert LC(z);
           Br := Br ∪ {z}; // {z}                               Br := Br \ {z}; // {x}
           z.next := y;                                         assert LC(x);
           Br := Br ∪ {z}; // {z}                               Br := Br \ {x}; // {}


                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:12                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


   We depict the statements enforced by the well-behavedness paradigm in pink and the ghost
updates written by the verification engineer in blue. Observe that the paradigm adds the impacted
objects to the broken set after each mutation and allocation. Determining the impact set of a
mutation is nontrivial; we show how to construct them in Section 4.1. Note also that to remove 𝑥
from the broken set we must show LC (𝑥) holds (assert followed by removal from Br). Finally, we
see at the beginning of the snippet that if we show 𝑥 ∉ Br then we can infer that LC (𝑥) holds. This
follows from the meaning of the broken set.
Putting it All Together. The above program corresponds to the program 𝑃 G,Br obtained from the
Stage 3 reduction, consisting of ghost updates to the G maps and Br. Since it is well-behaved and
satisfies the contract ⟨ sortedll(𝑥) ∧ Br = ∅ ⟩ 𝑃 G,Br ⟨ sortedll(𝑥) ∧ Br = ∅ ⟩ we can conclude that it
satisfies the contract ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ sortedll(𝑥) ∧ Br = ∅ ⟩ 𝑃 G,Br ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ sortedll(𝑥) ∧
Br = ∅ ⟩. Using Propositions 3.4 and 3.5 we can project out all augmented code and conclude that
the triple given in Example 3.1 with the user’s original program and intrinsic specifications is
valid! In this way, using FWYB we can verify programs with respect to intrinsic specifications
by verifying augmented programs with respect to quantifier-free specifications. The latter can be
discharged efficiently in practice using SMT solvers [7, 17] (see Section 3.7).                            □

We dedicate the rest of this section to developing the general theory of well-behaved programs.

Rules for Constructing Well-Behaved Programs
We define the class of well-behaved programs using a set of rules. We first introduce some notation.
   We distinguish the triples over the augmented programs and quantifier-free annotations by
{𝜓 pre } 𝑃 {𝜓 post }, with {} brackets rather than ⟨ ⟩. ⊢ {𝜓 pre } 𝑃 {𝜓 post } denotes that a triple is provable.
Our theory is agnostic to the underlying mechanism for proving triples correct (we use the off-
the-shelf verification tool Boogie in our evaluation). However, we assume that the mechanism is
sound with respect to the operational semantics. We denote that a snippet 𝑃 is well-behaved by
⊢WB 𝑃. We also denote that local conditions hold on an object 𝑥 by LC (𝑥).
   Figure 2 shows the rules for writing well-behaved programs. We only explain the interesting
cases here.
   Mutation. Since mutations can break local conditions, we must grow the broken set. Let 𝐴 be a
finite set of object-type terms over 𝑥 such that for any 𝑧 ∉ 𝐴, if LC (𝑧) held before the mutation,
then it continues to hold after the mutation. We refer to such a set 𝐴 as an impact set for the
mutation, and we update Br after a mutation with its impact set. The impact set may not always be
expressible as a finite set of terms, but this is indeed the case for all the intrinsically defined data
structures we use in this paper. We show how to construct impact sets in Section 4.1.
   Allocation. Allocation does not modify the heap on any existing object. Therefore, we simply
update the broken set by adding the newly created object 𝑥 (this was also the case in Example 3.6).
   Assert LC and Remove. This rule allows us to shrink the broken set once the verification
engineer fixes the local conditions on a broken location. The snippet assert LC(x); Br := Br\{x}
in Example 3.6 uses this rule. Informally, the verification engineer is required to show that LC (𝑥)
holds before removing 𝑥 from Br.
   Infer LC Outside Br. Recall that for well-behaved programs we know implicitly that ∀𝑥 ∉
Br. 𝜌 (𝑥) holds. This rule allows us to instantiate this implicit fact on objects that we can show lie
outside the broken set. The snippet assert x∉Br; assume LC(x) in Example 3.6 uses this rule.
We show that the above rules are sound for the elimination of the universal quantifier in Stage 3:
  Proposition 3.7. Let [(𝑀 : 𝑃); (𝑁 1 : 𝑄 1 ) . . . , (𝑁𝑘 : 𝑄𝑘 )] be a program (which can use G and
Br) such that ⊢WB 𝑃 and ⊢WB 𝑄𝑖 , 1 ≤ 𝑖 ≤ 𝑘. Let 𝛼 and 𝛽 be quantifier-free formulae over F ∪ G

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                        220:13


                                                                Mutation
          Skip/Assignment/Lookup/Return
                                                                ⊢ { 𝑧 ∉ 𝐴 ∧ 𝐿𝐶 (𝑧 ) ∧ 𝑥 ≠ nil } 𝑥 .𝑓 := 𝑣 { 𝐿𝐶 (𝑧 ) }
          ⊢WB 𝑠 where 𝑠 is of the form                                    ⊢WB 𝑥 .𝑓 := 𝑣 ; Br := Br ∪ 𝐴
          skip, x:=y, x:=y.f, or return                           where 𝐴 is a finite set of location terms over 𝑥

                    Allocation                                             Function Call

                    ⊢WB 𝑥 := new 𝐶 ( ) ; Br := Br ∪ {𝑥 }                   ⊢WB 𝑦, Br := Function(𝑥, Br )

                                                                                                         Composition
  Infer LC Outside Br                                      Assert LC and Remove
                                                                                                         ⊢WB 𝑃          ⊢WB 𝑄
  ⊢WB if (𝑥 ≠ nil ∧ 𝑥 ∉ Br ) then assume 𝐿𝐶 (𝑥 )           ⊢WB if 𝐿𝐶 (𝑥 ) then Br := Br \ {𝑥 }                  ⊢WB 𝑃 ; 𝑄

                   If-Then-Else                                        While

                           ⊢WB 𝑃        ⊢WB 𝑄                                        ⊢WB 𝑃
                        ⊢WB if cond 𝑃 else 𝑄                                ⊢WB while cond do 𝑃
                    where cond does not mention Br                      where cond does not mention Br


Fig. 2. Rules for constructing well-behaved programs. Local condition formula instantiated at 𝑥 is denoted by
LC (𝑥). The statement (if cond then 𝑆) is sugar for (if cond then 𝑆 else skip).


which can use Br. If {𝛼 } 𝑃 (𝑥, Br, ret : 𝑦, Br) {𝛽} is valid, then ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛼 ⟩ 𝑃 (𝑥, Br, ret :
𝑦, Br) ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛽 ⟩ is valid.
  We prove the above proposition by structural induction on the rules in Figure 2. We provide the
proof in Appendix B of our supplementary material.
   In the above presentation we use only one broken set for simplicity of exposition. Our general
framework allows for finer-grained broken sets that can track breaks over a partition on the local
conditions. For example, in Section 4.4 we verify deletion in an overlaid data structure consisting
of a linked list and a binary search tree using two broken sets: one each for the local conditions of
the two component data structures.

3.6    Soundness of FWYB
In this section we state the soundness of the FWYB methodology.
   Theorem 3.8 (FWYB Soundness). Let (G, LC, 𝜑) be an intrinsic definition with G = {𝑔1, 𝑔2 . . . , 𝑔𝑙 }.
Let [(𝑀 : 𝑃); (𝑁 1 : 𝑄 1 ) . . . , (𝑁𝑘 : 𝑄𝑘 )] be an augmented program constructed using the FWYB
methodology such that ⊢WB 𝑃 and ⊢WB 𝑄𝑖 , 1 ≤ 𝑖 ≤ 𝑘, i.e., the programs 𝑃 and 𝑄𝑖 are well-behaved
(according to the rules in Figure 2). Let 𝜑, 𝜓 pre , and 𝜓 post be quantifier-free formulae that do not mention
Br (but can mention the maps in G). Finally, let [( 𝑀ˆ : 𝑃);     ˆ ( 𝑁ˆ1 : 𝑄ˆ1 ) . . . , ( 𝑁ˆ𝑘 : 𝑄ˆ𝑘 )] be the projected
user-level program according to Definition 3.3. Then, if the triple:
                                   {𝜑 ∧ 𝜓 pre ∧ Br = ∅} 𝑃 {𝜑 ∧ 𝜓 post ∧ Br = ∅}
is valid, then the triple
                  ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑙 . (LC ∧ 𝜑 ∧ 𝜓 pre ) ⟩ 𝑃ˆ ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑙 . (LC ∧ 𝜑 ∧ 𝜓 post ) ⟩
is valid (according to Definition 3.2).

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:14                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


   Informally, the soundness theorem says that given a user-written program, if we (a) augment it
with updates to ghost fields and the broken set only using the discipline for well-behaved programs,
and (b) show that if the broken set is empty at the beginning of the program it will be empty at the
end, then the original user-written program satisfies the intrinsic specifications on preservation of
the data structure.
   The proof of the theorem trivially follows from the soundness of the three stages. Let us write
𝑃 as 𝑃 G,Br to emphasize that the program contains ghost code that manipulates both the G maps
and Br. We begin with the fact that {𝜑 ∧ 𝜓 pre ∧ Br = ∅} 𝑃 G,Br {𝜑 ∧ 𝜓 post ∧ Br = ∅} is valid.
Since 𝑃 and its auxiliary functions are well-behaved we have from Proposition 3.7 that ⟨ (∀𝑧 ∉
Br. 𝜌 (𝑧)) ∧ 𝜑 ∧ 𝜓 pre ⟩ 𝑃 G,Br ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝜑 ∧ 𝜓 post ⟩ is valid.
   Next, we use Proposition 3.5 to conclude that ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝜑 ∧𝜓 pre ⟩ 𝑃 G ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝜑 ∧𝜓 post ⟩
is valid, where 𝑃 G is the projection of 𝑃 G,Br obtained by eliminating the statements that manipulate
Br. Finally, we use Proposition 3.4, along with the fact that ∀𝑧. 𝜌 (𝑧) is LC and 𝑃ˆG is the same as 𝑃ˆ
to conclude that ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑙 . (LC ∧ 𝜑 ∧𝜓 pre ) ⟩ 𝑃ˆ ⟨ ∃ 𝑔1, 𝑔2 . . . , 𝑔𝑙 . (LC ∧ 𝜑 ∧𝜓 post ) ⟩ is valid4 . □

3.7      Generating Quantifier-Free Verification Conditions
We state at several points in this paper that verifying augmented programs with quantifier-free
specifications reduces to validity over combinations of quantifier-free theories. However, this is
not obvious. Unlike scalar programs, quantifier-free contracts do not guarantee quantifier-free
verification conditions (VCs) for heap programs. In particular, commands such as allocation and
function calls pose challenges. However, we show that in our case it is indeed possible to obtain
quantifier-free VCs. We do this by transforming a given heap program into a scalar program that
explicitly models changes to the heap. We model allocation using a ghost set Alloc corresponding
to the allocated objects and update it when a new object is allocated. We reason about arbitrary
changes to the heap across a function call by requiring a ‘modifies’ annotation from the user and
adding assumptions that the fields of objects outside the modified set of a function call remain the
same across the call. We express these assumptions using parameterized map updates which are
supported by the generalized array theory [18]. We detail this reduction in our supplementary
material in Appendix A.3.

4     ILLUSTRATIVE DATA STRUCTURES AND VERIFICATION
Intrinsic definitions and the fix-what-you-break verification methodology are new concepts that
require thinking afresh about data structures and annotating methods that operate over them. In
this section, we present several classical data structures and methods over them, and illustrate how
the verification engineer can write intrinsic definitions (which maps to choose, and what the local
conditions ensure) and how they can fix broken sets to prove programs correct.

4.1      Insertion into a Sorted List
In this section we present the verification of insertion into a sorted list implemented in the FWYB
methodology in its entirety. Our running example in Section 3 illustrates the key technical ideas
involved in verifying the program. In this section we present an end-to-end picture that mirrors
the verification experience in practice.

4 The presentation of FWYB augments the original program 𝑃 with manipulations to G and Br in separate stages. This is

done for clarity of exposition. This may not be possible in general since we may write ghost code with expressions that
use both the G maps and Br. However, we can combine the proofs of Propositions 3.4 and 3.5 to show the soundness of
projecting out all ghost code in a single stage, and Theorem 3.8 continues to hold in the general case.


Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                   220:15


                                              𝑦 =
              prev                  prev      old (next (𝑥)) Table 1. Table of impact sets corresponding to field
                                                                mutations for sorted lists (See 2 in Section 4.1). old (𝑡 )
    𝑤                      𝑥                      𝑦             refers to the value of the term 𝑡 before the mutation.
              next                                              Terms only belong to the sets if not equal to nil.
                                 next
                                                  𝑧                 Mutated Field 𝑓        Impacted Objects 𝐴 𝑓
                                                                        𝑥 .next              {𝑥, old (next (𝑥))}
   Fig. 3. Reasoning about the set of objects broken by                  𝑥 .key                {𝑥, prev(𝑥)}
   x.next := z. The dashed arrow represents the old next                𝑥 .prev              {𝑥, old (prev(𝑥))}
   pointer before the mutation. The grey nodes denote                  𝑥 .hslist               {𝑥, prev(𝑥)}
   objects where local conditions can be broken by the                 𝑥 .length               {𝑥, prev(𝑥)}
   mutation. We see that only 𝑥 and 𝑦 may violate next                  𝑥 .keys                {𝑥, prev(𝑥)}
   and prev being inverses.



Data Structure Definition. We first revise the definition of a sorted list (Example 2.6) with
a different set of monadic maps. We have the following monadic maps G— prev : 𝐶 → 𝐶?,
length : 𝐶 → N, keys : 𝐶 → Set (Int), hslist : 𝐶 → Set (C) that model the previous pointer (inverse
of next), length of the sorted list, the set of keys stored in it, and its heaplet (set of locations that
form the sorted list) respectively. We use the length, keys, and heaplet maps to state full functional
specifications of methods. The local conditions are:
 ∀𝑥 . next (𝑥) ≠ nil ⇒ ( key(𝑥) ≤ key(next (𝑥)) ∧ prev(next (𝑥)) = 𝑥
                            ∧ length(𝑥) = 1 + length(next (𝑥)) ∧ keys(𝑥) = {key(𝑥)} ∪ keys(next (𝑥))
                            ∧ hslist (𝑥) = {𝑥 } ⊎ hslist (next (𝑥)) )                  (⊎: disjoint union)
   ∧ prev(𝑥) ≠ nil ⇒ next (prev(𝑥)) = 𝑥
   ∧ next (𝑥) = nil ⇒ ( length(𝑥) = 1 ∧ keys(𝑥) = {key(𝑥)} ∧ hslist (𝑥) = {𝑥 } )
                                                                                                     (2)
  The above definition is slightly different from the one given in Example 2.6. The length map
replaces the rank map, requiring additionally that lengths of adjacent nodes differ by 1.
  The prev map is a gadget we find useful in many intrinsic definitions. The constraints on
prev ensure that the 𝐶-heaps satisfying the definition only contain non-merging lists. To see
why this is the case, consider for the sake of contradiction distinct objects 𝑜 1, 𝑜 2, 𝑜 3 such that
next (𝑜 1 ) = next (𝑜 2 ) = 𝑜 3 . Then, we can see from the local conditions that we must simultaneously
have prev(𝑜 3 ) = 𝑜 1 and prev(𝑜 3 ) = 𝑜 2 , which is impossible. Finally, the hslist and keys maps
represent the heaplet and the set of keys stored in the sorted list (respectively).
  The heads of all sorted lists in the 𝐶-heap is then defined by the following correlation formula:
                                                𝜑 (𝑦) ≡ prev(𝑦) = nil.
Constructing Provably Correct Impact Sets for Mutations. We now instantiate the rules
developed in Section 3.5 for sorted lists. Recall that well-behaved programs must update the broken
set with the impact set of a mutation. Table 1 captures the impact set for each field mutation. Note
that the terms denoting the impacted objects belong to 𝐴 𝑓 only if they do not evaluate to nil.
   Let us consider the correctness of Table 1, focusing on the mutation of next as an example. Figure 3
illustrates the heap after the mutation x.next := z. We make the following key observation: the
local constraints LC (𝑣) for an object 𝑣 refer only to the properties of objects 𝑣, next (𝑣), and prev(𝑣)
(see 2), i.e., objects that are at most “one step” away on the heap. Therefore, the only objects that
can be broken by the mutation x.next := z are those that are one step away from 𝑥 either via an

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:16                                                                   Adithya Murali, Cody Rivera, and P. Madhusudan


incoming or an outgoing edge via pointers next and prev. This is a general property of intrinsic
definitions: mutations cannot immediately affect objects that are far away on the heap. 5
   In our case, we claim that the impact set contains at most 𝑥 and old (next (𝑥)). Here’s a proof
(see Fig 3): Consider 𝑧 such that 𝑧 ≠ old (next (𝑥)) (as there is no real mutation otherwise). If 𝑧 was
not broken before the mutation, then it cannot be the case that prev(𝑧) = 𝑥. Looking at the local
conditions, it is clear that such a 𝑧 will remain unbroken after the mutation. Now consider a 𝑤 not
broken before the mutation such that next (𝑤) = 𝑥. Then it follows from the local conditions that
there can only be one such (unbroken) 𝑤, and further 𝑤 ≠ 𝑥. 𝑤’s fields are not mutated, and by
examining LC, it is easy to see that 𝑤 will not get broken (as LC (𝑣) does not refer to next (next (𝑣))).
The argument is the same for 𝑤 such that prev(𝑥) = 𝑤. Finally, consider a 𝑦 not broken before the
mutation such that prev(𝑦) = 𝑥. We can then see from the local conditions that 𝑦 = old (next (𝑥)),
which is already in the impact set.
   The above argument is subtle, but we can automatically check whether impact sets declared by a
verification engineer are correct. The Mutation rule in Figure 2 characterizes the impact set 𝐴𝑛𝑒𝑥𝑡
for mutation of the field 𝑛𝑒𝑥𝑡 as follows:
                     ⊢ {𝑢 ≠ 𝑥 ∧ 𝑢 ≠ next (𝑥) ∧ LC (𝑢) ∧ 𝑥 ≠ nil} 𝑥 .next := 𝑧 {LC (𝑢)}
The above says that any location 𝑢 that is not in the impact set which satisfied the local conditions
before the mutation must continue to satisfy them after the mutation. We present the formulation
for the general case in our supplementary material in Appendix C. Finally, note that the validity of
the above triple is decidable. In our realization of the FWYB methodology we prove our impact sets
correct by encoding the triple in Boogie (see Section 5.3).
Macros that Ensure Well-Behaved Programs. In Section 3.5 we characterized well-behaved
programs as a set of syntactic rules (Figure 2). We can realize these restrictions using macros:
   (1) Mut(x,f,v,Br) for each 𝑓 ∈ F ∪ G, which represents the sequence of statements x.f :=
       v; Br := Br U Af (x). Here Af (x) is the impact set corresponding to the mutation on 𝑓
       on 𝑥 as given by the table above. This macro is used instead of x.f := v and automatically
       ensures that the impact set is added to the broken set.
   (2) NewObj(x,Br), which represents the statements x := new C(); Br := Br U { x }.
       This macro is used instead of x := new C() and ensures that any newly allocated object is
       automatically added to the broken set.
   (3) AssertLCAndRemove(x,Br), which represents the statements assert LC(x); Br := Br \
       { x }. This macro is allowed anytime the engineer wants to assert that 𝑥 satisfies the local
       condition, and then remove it from the broken set.6
   (4) InferLCOutsideBr(x, Br), which represents the statements assert (x ≠ nil ∧ x ∉ Br);
       assume LC(x). This allows the engineer at any time to assert that 𝑥 is not in the broken set
       and assume it satisfies the local condition.
  The above macros correspond to the rules Mutation, Allocation, Assert LC and Remove,
and Infer LC Outside Br respectively. Restricting to the syntactic fragment that contains the
above macros and disallows mutation and allocation otherwise enforces the programming discipline
that ensures well-behaved programs.

5 Note that a mutation can necessitate changes to monadic maps for an unbounded number of nodes eventually; however,

these are not necessary immediately. As we fix monadic maps on a broken object, its neighbors could get broken and
need to be fixed, leading to their neighbors breaking, etc. This can lead to a ripple effect that would eventually require an
unbounded number of locations to be fixed.
6We extend our basic programming language defined in Figure 1 with an assert statement and give it the usual semantics

(program reaches an error state if the assertion is not satisfied, but is equivalent to skip otherwise).


Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                           220:17


We present the full well-behaved code written using the above macros and discuss it in our
supplementary material in Appendix D.1.

4.2    Reversing a Sorted List
We return to lists for another case study: reversing a sorted list. The purpose of this example is to
demonstrate how the fix-what-you-break philosophy works with iteration/loops. We augment the
definition of sorted linked lists from Case Study 4.1 to make sortedness optional and determined by
predicates that capture sortedness in non-descending order, with sorted : 𝐶 → 𝐵𝑜𝑜𝑙, and sortedness
with non-ascending order, with rev_sorted : 𝐶 → 𝐵𝑜𝑜𝑙. The relevant additions to the local condition
and the impact sets for these monadic maps can be seen below:

  (next (𝑥 ) ≠ nil ⇒
   sorted (𝑥 ) ⇒ (key (𝑥 ) ≤ key (next (𝑥 ) ) ∧ sorted (𝑥 ) = sorted (next (𝑥 ) ) )   Mutated Field 𝑓   Impacted Objects 𝐴 𝑓
                                                                                          sorted           {𝑥, prev (𝑥 ) }
   ∧ rev_sorted (𝑥 ) ⇒ (key (𝑥 ) ≥ key (next (𝑥 ) )                                    rev _sorted         {𝑥, prev (𝑥 ) }
                         ∧ rev_sorted (𝑥 ) = rev_sorted (next (𝑥 ) ) ) )


   We present the full local condition and code in our supplementary material in Appendix D.3.
However, the gist of the method is that we are popping 𝐶 nodes off of the front of a temporary list
𝑐𝑢𝑟 , and pushing them to the front of a new reversed list 𝑟𝑒𝑡 repeatedly using a loop. A technique
we use to verify loops using FWYB is to maintain that the broken set contains no nodes or only a
finite number of nodes for which we specify how they are broken. In the case of this method, 𝐵𝑟
remains empty, as the loop maintains 𝑐𝑢𝑟 and 𝑟𝑒𝑡 as two valid lists, not modifying any other nodes.
When popping 𝑥 from 𝑐𝑢𝑟 and adding it to 𝑟𝑒𝑡, in addition to repairing the new 𝑐𝑢𝑟 by setting its
parent pointer to nil, we also need to update fields such as length and keys on 𝑥, so it satisfies the
relevant local conditions as the new head of the 𝑟𝑒𝑡 list.

4.3 Circular Lists
Our next example is circular lists. This example illustrates a neat trick in FWYB that where we
assert that we can reach a special node known as a scaffolding node, and that in addition to asserting
properties on the node that is given to the method, one can also assert properties on this scaffolding
node. In order to make verification of properties on this scaffolding node easier, the scaffolding
node remains unchanged in the data structure, and is never deleted. We start with a data structure
containing a pointer 𝑛𝑒𝑥𝑡 : 𝐶 → 𝐶 and a monadic map 𝑝𝑟𝑒𝑣 : 𝐶 → 𝐶. We build on this data
structure to define circular lists by adding a monadic map 𝑙𝑎𝑠𝑡 : 𝐶 → 𝐶 where 𝑙𝑎𝑠𝑡 (𝑢) for any
location 𝑢 points to the last item in the list, which is the scaffolding node in this case. The scaffolding
node 𝑥 must in turn point to another node whose 𝑙𝑎𝑠𝑡 map points to 𝑥 itself: this ensures cyclicity.
We also define monadic maps 𝑙𝑒𝑛𝑔𝑡ℎ : 𝐶 → 𝑁 𝑎𝑡 and 𝑟𝑒𝑣_𝑙𝑒𝑛𝑔𝑡ℎ : 𝐶 → 𝑁 𝑎𝑡 to denote the distance
to the 𝑙𝑎𝑠𝑡 node by following 𝑝𝑟𝑒𝑣 or 𝑛𝑒𝑥𝑡 pointers. The partial local conditions for 𝑥 are as below:
                       (𝑥 = 𝑙𝑎𝑠𝑡 (𝑥) ⇒ 𝑙𝑎𝑠𝑡 (next (𝑥)) = 𝑥 ∧ 𝑙𝑒𝑛𝑔𝑡ℎ(𝑥) = 0 ∧ 𝑟𝑒𝑣_𝑙𝑒𝑛𝑔𝑡ℎ(𝑥) = 0)
                   ∧ (𝑥 ≠ 𝑙𝑎𝑠𝑡 (𝑥) ⇒ 𝑙𝑎𝑠𝑡 (next (𝑥)) = 𝑙𝑎𝑠𝑡 (𝑥) ∧ 𝑙𝑒𝑛𝑔𝑡ℎ(𝑥) = 𝑙𝑒𝑛𝑔𝑡ℎ(next (𝑥)) + 1
                                      ∧ 𝑟𝑒𝑣_𝑙𝑒𝑛𝑔𝑡ℎ(𝑥) = 𝑟𝑒𝑣_𝑙𝑒𝑛𝑔𝑡ℎ(prev(𝑥)) + 1)

   Here is the gist of inserting a node at the back of a circular list. We are given a node 𝑥 such
that next (𝑥) = 𝑙𝑎𝑠𝑡 (𝑥) (at the end of a cycle). We insert a newly allocated node after 𝑥, making
local repairs there. Then, in a ghost loop similar to the one in Case Study 4.2, we make appropriate
updates to the length and keys maps, which are not fully described here, following the 𝑝𝑟𝑒𝑣 map
until we reach 𝑙𝑎𝑠𝑡 (𝑥). Like in the previous case study, we present the full local condition and code
in our supplementary material in Appendix D.4.

                                        Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:18                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


4.4      Overlaid Data Structure of List and BST
One of the settings where intrinsic definitions shine is in defining and manipulating an overlaid
data structure that overlays a linked list and a binary search tree. The list and tree share the same
locations, and the next pointer threads them into a linked list while the left, right pointers on them
defines a BST. Such structures are often used in systems code (such as the Linux kernel) to save
space [34]. For example, I/O schedulers use an overlaid structure as above, where the list/queue
stores requests in FIFO order while the bst enables faster searching according requests with respect
to a key. While there has been work in verification of memory safety of such structures [34], we
aim here to check preservation of such data structures.
   Intrinsic definition over such an overlaid data structure is pleasantly compositional. We simply
take intrinsic definitions for lists and trees, and take the union of the monadic maps and the
conjunction of their local conditions. The only thing that is left is then to ensure that they contain
the same set of locations. We introduce a monadic map bst_root that maps every node to its root
in the bst, and introduce a monadic map list_head that maps every node to the head of the list it
belong to (using appropriate local conditions). We then demand that all locations in a list have the
same bst_root and all locations in a tree have the same list_head, using local conditions. We also
define monadic maps that define the bst-heaplet for tree nodes and list-heaplet for list nodes (the
locations that belong to the tree under the node or the list from that node, respectively) using local
conditions. We define a correlation predicate Valid that relates the head ℎ of the list and root 𝑟 of
the tree by demanding that the bst-root of ℎ is 𝑟 and the list-head of 𝑟 is ℎ, and furthermore, the
list-heaplet of ℎ and tree-heaplet of 𝑟 are equal. This predicate can be seen here:
             Valid ≡ bst_root(ℎ) = 𝑟 ∧ list_root(𝑟 ) = ℎ ∧ list_heaplet(ℎ) = bst_heaplet(𝑟 )
   We prove certain methods manipulating this overlaid structure correct (such as deleting the first
element of the list and removing it both from the list as well as the BST). These ghost annotations
are mostly compositional— with exceptions for fields whose mutation impacts the local condition
of multiple components, we fix monadic maps for the BST component in the same way we fix them
for stand-alone BSTs and fix monadic maps for the list component in the same way we fix them for
stand-alone lists. In fact, we maintain two broken sets, one for BST and one for list, as updating a
pointer for BST often does not break the local property for lists, and vice versa.

Limitations. In modeling the data structures above, we crucially used the fact that for any location,
there is at most one location (or a bounded number of locations) that has a field pointing to this
location. We used this fact to define an inverse pointer (prev or parent/p), which allows us to capture
the impact set when a location’s fields are mutated. Consequently, we do not know how to model
structures where locations can have unbounded indegree. We could model these inverse pointers
using a sequence/array of pointers, but verification may get more challenging. Data structures with
unbounded outdegree can however be modeled using just a linked-list of pointers and hence seen
as a structure with bounded outdegree.

5     IMPLEMENTATION AND EVALUATION
5.1      Implementation Strategy of IDS and FWYB in Boogie
We implement the technique of intrinsically defined data structures and FWYB verification in
the program verifier Boogie [6]. Boogie is a low-level imperative programming language which
supports systematic generation of verification conditions that are checked using SMT solvers.
  We choose Boogie as it is a low-level verification condition generator. We expect that scalar
programs with quantifier-free specifications, annotations, and invariants, and given our careful

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                               220:19


modeling of the heap and its modification across function calls (Section 3.7), reduces to quantifier-
free verification conditions that fall into decidable logics. We further cross-check that our encodings
indeed generate decidable queries by checking the generated SMT files. Furthermore, a plethora
of higher-level languages compile to Boogie (e.g., VCC and Havoc for C [15, 16], Dafny [35]
with compilation to .NET, Civl for concurrent programs [28], Move for smart contracts [19], etc.).
Implementing a technique in Boogie hence shows a pathway for implementing IDS and FWYB for
higher-level languages as well.
Modeling Fix-What-You-Break Verification in Boogie. We model heaps in Boogie by having
a sort Loc of locations and modeling pointers as maps from Loc to sorts. We implement monadic
maps also as maps from locations to field values. We implement our benchmarks using the macros
for well-behaved programming defined in Section 4.1. We implement allocation with an Alloc set
and heap change across function calls using parameterized map updates as described in Section 3.7
and our supplementary material in Appendix A.3.
   We ensure that the VCs generated by Boogie fall into decidable fragments, and there are
several components that ensure this. First, note that all specifications (contracts and invariants) are
quantifier-free. Second, pure functions (used to implement local conditions) are typically encoded
using quantification, but we ensure Boogie inlines them to avoid quantification. Third, heap updates
that are the effect of procedures and set operations for set-valued monadic maps are modeled using
parameterized map updates [18], which Boogie supports natively. Finally, we cross-check that the
generated SMT query is quantifier-free and decidable by checking the absence of statements that
introduce quantified reasoning, including exists, forall, and lambda.

5.2    Benchmarks
We evaluate our technique on a variety of data structures and methods that manipulate them. Our
benchmark suite consists of data structure manipulation methods for a variety of different list and
tree data structures, including sorted lists, circular lists, binary search trees, and balanced binary
search trees such as Red-Black trees and AVL trees. Methods include core functionality such as
search, insertion and deletion. The suite includes an overlaid data structure that overlays a binary
search tree and a linked list, implementing methods needed by a simplified version of the Linux
deadline IO scheduler [34]. The contracts for these functions are complete functional specifications
that not only ask for maintenance of the data structure, but correctness properties involving the
returned values, the keys stored in the container, and the heaplet of the data structure.

5.3    Evaluation
We first evaluate the following two research questions:
RQ1: Can the data structures be expressed using IDS, and can the FWYB methodology for
methods on these structures be expressed in Boogie?
RQ2: Is Boogie with decidable verification condition generation dispatched to SMT solvers
effective in verifying these methods?
   As we have articulated earlier, intrinsic definitions and monadic map updates require a new way
of thinking about programs and repairs. We implement the specifications using monadic maps and
local conditions, and the benchmarks using the well-behavedness macros and ghost updates. We
were able to express all data structures and FWYB annotations for the methods on these structures
for our benchmarks in Boogie (RQ1). Importantly, we were able to write quantifier-free modular
contracts for the auxiliary methods and loop invariants using the monadic maps and strengthening
the contracts using quantifier-free assertions on broken sets (which may not be empty for auxiliary
methods). We do not prove termination for these methods except for ghost loops and ghost recursive

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:20                                                                  Adithya Murali, Cody Rivera, and P. Madhusudan


Table 2. Implementation and verification of Boogie programs on the benchmarks. The columns give data
structure, size of local conditions for capturing the datatructure as number of conjuncts, method, lines of
executable code in the method, lines of specification (pre/post), lines of ghost code annotations (invari-
ants/monadic map updates), and verification time in seconds.

                            𝐿𝐶                          LOC+Spec      Verif.                        LOC+Spec      Verif.
         Data Structure                     Method                                       Method
                           Size                             +Ann    Time(s)                             +Ann    Time(s)
                                            Append        4+11+10       2.0          Insert-Back      6+13+12       2.0
                                           Copy-All         7+8+9       2.0         Insert-Front       3+13+7       2.0
   Singly-Linked List        8
                                          Delete-All      10+9+16       2.0                Insert     9+13+23       2.0
                                               Find         4+4+2       1.9              Reverse       6+8+18       2.1
                                          Delete-All      10+9+16       2.1               Merge       11+9+20       2.1
             Sorted List    14                 Find         4+4+2       1.9              Reverse      5+14+22       2.1
                                              Insert      9+16+27       2.1
          Sorted List
 (w. 𝑚𝑖𝑛, 𝑚𝑎𝑥 maps)         20         Concatenate       6+10+13         2.2            Find-Last     5+10+9         2.0
                                        Insert-Front      4+12+41       2.3         Delete-Front     3+12+39         2.4
           Circular List    27
                                         Insert-Back      5+14+45       2.4         Delete-Back      3+13+55         2.4
                                                Find        4+3+5       2.0               Delete    10+13+30         2.8
  Binary Search Tree        35
                                               Insert     9+12+37       2.7        Remove-Root      17+15+47         3.8
                                                Find        4+3+5       2.0               Delete    10+13+30         3.1
                  Treap     37
                                               Insert    19+12+74      10.2        Remove-Root      24+15+74         5.4
                                               Insert    12+12+36       5.1            Find-Min        5+5+8         2.1
              AVL Tree      45
                                              Delete     43+13+62       5.3             Balance     40+17+95         5.0
                                               Insert   76+12+203      74.1         Del-L-Fixup     33+20+93         8.9
         Red-Black Tree     48                Delete     56+13+76       5.8         Del-R-Fixup     33+20+93         7.4
                                           Find-Min         5+5+8       2.1
     BST+Scaffolding        59         Delete-Inside      1+24+51       4.8        Remove-Root      44+31+61       10.2
    Scheduler Queue                   Move-Request         4+10+8       2.9    BST-Delete-Inside     1+29+55        4.9
                            72
  (overlaid SLL+BST)              List-Remove-First       5+13+10       2.7    BST-Remove-Root      44+36+65       15.0

procedures (termination for latter is required for soundness). We provide the benchmarks with
annotations in a public repository [46].
   Our annotation measures and verification results are detailed in the table in Table 2, for 42
methods across 10 data structure definitions. These measurements were taken from a machine with
an Intel™ Core i5-4460 processor at 3.20 GHz. We found the verification performance excellent
overall (RQ2): all the methods verify in under 2 minutes, and all but four verify in under 10 seconds.
We used the option that sets the maximum number of VC splits to 8 in Boogie. The times reported
for each method are the sum of times taken for the following steps: verifying that the impact sets
are correct (<3s for all data structures), generating verification conditions with Boogie, injecting
parametric update implementations, and solving the SMT queries.
   Notice that the lines of ghost code written is nontrivial, but these are typically simple, involving
programmatically repairing monadic maps and manipulating broken sets. In fact, a large fraction
(∼ 60%) of ghost updates in our benchmarks were definitional updates that simply update a field
according to its definition in the local condition. An example is updating 𝑥 .length to 𝑥 .next.length+1
for lists. We believe that the annotation burden can be significantly lowered in future work by
automating such updates. More importantly, note that none of the programs required further
annotations like instantiations, triggers, inductive lemmas, etc. in order to prove them correct.
RQ3: What is the performance impact of generating decidable verification conditions?
   In order to study this, we implemented the entire benchmark suite described in Table 2 in Dafny,
a higher-level programming language that uses Boogie to perform its verification. We implemented
the data structures and the FWYB methodology identically in Dafny to the Boogie version.

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                               220:21


   Even though our annotations are all quantifier-
free, Dafny generates Boogie code where several
aspects of the language, in particular allocation and
heap change across function calls, are modeled us-
ing quantifiers, resulting in quantified queries to
SMT solvers. The scatter plot on the right shows the
performance of Boogie and Dafny on the bench-
marks. The plot clearly strongly suggests that even
though Dafny is able to prove the FWYB-annotated
programs correct, using decidable verification condi-
tions results in much better performance. We hence
believe that implementing program verifiers (such
as Dafny) that exploit the fact that FWYB annotations can be compiled to annotations in Boogie
that result in decidable VCs is a promising future direction to achieve faster high-level IDS+FWYB
frameworks.

6   RELATED WORK
There have been mainly two paradigms to automated verification of programs annotated with
rich contracts written in logic. The first is to restrict the specification logic so that verification
conditions fall into a decidable logic. The second allows validity of verification conditions to fall into
an undecidable or even an incomplete logic (where validity is not even recursively enumerable), but
support effective strategies nevertheless, using heuristics, lemma synthesis, and further annotations
from the programmer [2–5, 9, 10, 12–14, 20, 26, 44, 50, 51, 54, 56, 59, 63]. In this paper, we have
proposed a new paradigm of predictable verification that calls for programmers to write a reasonable
amount of extra annotations under which validity of verification conditions becomes decidable.
To the best of our knowledge, we do not know of any other work of this style (where validity of
verification conditions is undecidable but an upfront set of annotations renders it decidable).
Decidable Verification. There is a rich body of research on decidable logics for heap verification:
first-order logics with reachability [36], the logic Lisbq in the Havoc tool [32], several decidable
fragments of separation logic known [8, 55] as well as fragments that admit a decidable entailment
problem [22]. Decidable logics based on interpreting bounded treewidth data structures on trees
have also been studied, for separation logics as well as other logics [25, 39, 40]. In general, these
logics are heavily restricted— the magic wand in separation logic quickly leads to undecidability [11],
the general entailment problem for separation logic with inductive predicates is undecidable [1],
and validity of first-order logic with recursive definitions is undecidable and not even recursively
enumerable and does not admit complete proof procedures.
Validity Checking of Undecidable and Incomplete Logics. Heap verification using undecidable
and incomplete logics has been extensively in the literature. The work on natural proofs [37, 54]
for imperative programs and work on Liquid Types [61] for functional programs propose such
approaches that utilize SMT solvers, but require extra user help in the form of inductive lemmas to
verify programs. Users need to understand the underlying heuristic SMT encoding mechanisms and
their shortcomings, as well as theoretical shortcomings (the difference between fixed point and least
fixed point semantics of recursive definitions) in order to provide these lemmas (see [37, 44, 45]).
In contrast, the user help we seek in this work is upfront ghost code that updates monadic maps to
satisfy local conditions independently of the heuristics the solvers use. Furthermore, for programs
with such annotations, we assure decidable validation of the associated verification conditions.

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:22                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


Monadic Maps. Monadic maps have been exploited in earlier work in other forms for simplifying
verification of properties of global structures. In shape analysis [62], monadic predicates are often
used to express inductively defined properties of single locations on the heap. In separation logic,
the iterated separating conjunction operator, introduced already by Reynolds in 2002 [60], expresses
local properties of each location, and is akin to monadic maps. Iterated separation conjunction has
been used in verification, for both arrays as well as for data structures, in various forms [21, 43]. The
work on verification using flows [29–31, 41, 42, 53] introduces predicates based on flows, and utilizes
such predicates in iterated separation formulas to express global properties of data structures and
to verify algorithms such as the concurrent Harris list. In these works, local properties of locations
and proof systems based on them are explored, but we do not know of any work exploiting monadic
maps for decidable reasoning, which is crucial for predictable verification. The work by Gyori
et al [24] exploits a class of monadic maps called linear measures that satisfy certain algebraic
properties in order to incrementally maintain and check properties of linked lists at runtime.
Ghost Code. The methodology of writing ghost code is a common paradigm in deductive program
verification [23, 27, 38, 58] and supported by verification tools such as Boogie and Dafny [6, 35].
Ghost code involves code that manipulates auxiliary variables to perform a parallel computation
with the original code without affecting it. Our use of ghost code establishes the required monadic
maps that satisfy local conditions by allowing the programmer to construct the maps and verify
the local conditions using a disciplined programming methodology. Furthermore, we assure that
the original code with the ghost code results in decidable verification problems, which is a salient
feature not found typically in other contexts where ghost code is used.

7   CONCLUSIONS
We introduced intrinsic definitions that eschew recursion/induction and instead define data struc-
tures using monadic maps and local conditions. Proving that a program maintains a valid data
structure hence requires only maintaining monadic maps and verifying the local conditions on
locations that get broken. Furthermore, verifying that engineer-provided ghost code annotations
are indeed correct falls into decidable theories, leading to a predictable verification framework.
Future Work. First, it would be useful to develop verification engines for higher-level languages
(like Java [26], Rust [33], and Dafny [35]) that that have native support for intrinsic definitions
and produce verification conditions in decidable theories that SMT solvers can handle (see RQ3 in
Section 5.3). Second, it would be interesting to see how intrinsic definitions with fix-what-you-break
proof methodology can coexist and exchange information with traditional recursive definitions
with induction-based proof methodology. Third, as mentioned in Section 5.3, many updates of
monadic maps are straightforward using definitions, and tools that automate this can reduce
annotation burden significantly. Fourth, we are particularly intrigued with the ease with which
intrinsic data structures capture more complex data structures such as overlaid data structures.
Exploring intrinsic definitions for verifying concurrent and distributed programs that maintain data
structures is particularly interesting. Fifth, intrinsic definitions opens up an entirely new approach
to defining properties of structures that simplify reasoning. We believe that exploiting intrinsic
definitions in other verification contexts, like mathematical structures used in specifications (e.g.,
message queues in distributed programs), parameterized concurrent programs (configurations
modeled as unbounded sequences of states), and programs that manipulate big data concurrently
(like Apache Spark) are exciting future directions. Finally, it would be interesting to adapt IDS for
functional programs. Since functional data structures are not mutable, ghost fields will always meet
local conditions. However, we may need to (re-)establish rather than repair local conditions, which
may require ghost code, e.g., establishing that the ghost map sorted on a functional list 𝑥 is true.

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                 220:23


ARTIFACT AVAILABILITY STATEMENT
We have prepared a publicly available artifact [46] containing our benchmark suite and a Docker
image for reproducing our evaluation in Section 5.3.

ACKNOWLEDGEMENTS
We thank the anonymous reviewers for their valuable feedback. In particular, we thank one reviewer
for pointing out that Boogie supports parameterized map updates natively; using this feature
simplifies the present version of our paper and artifact. This work is supported in part by a research
grant from Amazon.

REFERENCES
 [1] Timos Antonopoulos, Nikos Gorogiannis, Christoph Haase, Max Kanovich, and Joël Ouaknine. 2014. Foundations
     for Decision Problems in Separation Logic with General Inductive Predicates. In Foundations of Software Science and
     Computation Structures, Anca Muscholl (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 411–425.
 [2] Anindya Banerjee, Mike Barnett, and David A. Naumann. 2008. Boogie Meets Regions: A Verification Experience
     Report. In Verified Software: Theories, Tools, Experiments, Natarajan Shankar and Jim Woodcock (Eds.). Springer Berlin
     Heidelberg, Berlin, Heidelberg, 177–191.
 [3] Anindya Banerjee and David A. Naumann. 2013. Local Reasoning for Global Invariants, Part II: Dynamic Boundaries.
     J. ACM 60, 3, Article 19 (jun 2013), 73 pages. https://doi.org/10.1145/2485981
 [4] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. 2008. Regional Logic for Local Reasoning about Global In-
     variants. In ECOOP 2008 – Object-Oriented Programming, Jan Vitek (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     387–411.
 [5] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. 2013. Local Reasoning for Global Invariants, Part I: Region
     Logic. J. ACM 60, 3, Article 18 (June 2013), 56 pages. http://doi.acm.org/10.1145/2485982
 [6] Mike Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and K. Rustan M. Leino. 2006. Boogie: A Modular
     Reusable Verifier for Object-Oriented Programs. In Formal Methods for Components and Objects, Frank S. de Boer,
     Marcello M. Bonsangue, Susanne Graf, and Willem-Paul de Roever (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     364–387.
 [7] Clark Barrett, Christopher L. Conway, Morgan Deters, Liana Hadarean, Dejan Jovanović, Tim King, Andrew Reynolds,
     and Cesare Tinelli. 2011. CVC4. In Computer Aided Verification, Ganesh Gopalakrishnan and Shaz Qadeer (Eds.).
     Springer Berlin Heidelberg, Berlin, Heidelberg, 171–177.
 [8] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. A Decidable Fragment of Separation Logic. In FSTTCS
     2004: Foundations of Software Technology and Theoretical Computer Science, Kamal Lodaya and Meena Mahajan (Eds.).
     Springer Berlin Heidelberg, Berlin, Heidelberg, 97–109.
 [9] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Symbolic Execution with Separation Logic. In Program-
     ming Languages and Systems, Kwangkeun Yi (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 52–68.
[10] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2006. Smallfoot: Modular Automatic Assertion Checking
     with Separation Logic. In Proceedings of the 4th International Conference on Formal Methods for Components and Objects
     (Amsterdam, The Netherlands) (FMCO’05). Springer-Verlag, Berlin, Heidelberg, 115–137. https://doi.org/10.1007/
     11804192_6
[11] Rémi Brochenin, Stéphane Demri, and Etienne Lozes. 2008. On the Almighty Wand. In Computer Science Logic, Michael
     Kaminski and Simone Martini (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 323–338.
[12] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2011. Compositional Shape Analysis by
     Means of Bi-Abduction. J. ACM 58, 6, Article 26 (dec 2011), 66 pages. https://doi.org/10.1145/2049697.2049700
[13] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. 2007. Automated Verification of Shape, Size
     and Bag Properties. In Proceedings of the 12th IEEE International Conference on Engineering Complex Computer Systems
     (ICECCS ’07). IEEE Computer Society, USA, 307–320. https://doi.org/10.1109/ICECCS.2007.17
[14] Duc-Hiep Chu, Joxan Jaffar, and Minh-Thai Trinh. 2015. Automatic Induction Proofs of Data-Structures in Imperative
     Programs. In Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation
     (Portland, OR, USA) (PLDI ’15). Association for Computing Machinery, New York, NY, USA, 457–466. https://doi.org/
     10.1145/2737924.2737984
[15] Ernie Cohen, Markus Dahlweid, Mark Hillebrand, Dirk Leinenbach, Michał Moskal, Thomas Santen, Wolfram Schulte,
     and Stephan Tobies. 2009. VCC: A Practical System for Verifying Concurrent C. In Theorem Proving in Higher Order
     Logics, Stefan Berghofer, Tobias Nipkow, Christian Urban, and Makarius Wenzel (Eds.). Springer Berlin Heidelberg,
     Berlin, Heidelberg, 23–42.


                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:24                                                                   Adithya Murali, Cody Rivera, and P. Madhusudan


[16] Jeremy Condit, Brian Hackett, Shuvendu K. Lahiri, and Shaz Qadeer. 2009. Unifying Type Checking and Property
     Checking for Low-Level Code. SIGPLAN Not. 44, 1 (jan 2009), 302–314. https://doi.org/10.1145/1594834.1480921
[17] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Proceedings of the 14th International
     Conference on Tools and Algorithms for the Construction and Analysis of Systems (Budapest, Hungary) (TACAS’08).
     Springer-Verlag, Berlin, Heidelberg, 337–340.
[18] Leonardo de Moura and Nikolaj Bjørner. 2009. Generalized, efficient array decision procedures. In 2009 Formal Methods
     in Computer-Aided Design. IEEE, 45–52. https://doi.org/10.1109/FMCAD.2009.5351142
[19] David Dill, Wolfgang Grieskamp, Junkil Park, Shaz Qadeer, Meng Xu, and Emma Zhong. 2022. Fast and Reliable Formal
     Verification of Smart Contracts with the Move Prover. In Tools and Algorithms for the Construction and Analysis of
     Systems, Dana Fisman and Grigore Rosu (Eds.). Springer International Publishing, Cham, 183–200.
[20] Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2006. A Local Shape Analysis Based on Separation Logic. In
     Tools and Algorithms for the Construction and Analysis of Systems, Holger Hermanns and Jens Palsberg (Eds.). Springer
     Berlin Heidelberg, Berlin, Heidelberg, 287–302.
[21] Dino Distefano and Matthew Parkinson. 2008. jStar: Towards Practical Verification for Java. Sigplan Notices - SIGPLAN
     43, 213–226. https://doi.org/10.1145/1449764.1449782
[22] Mnacho Echenim, Radu Iosif, and Nicolas Peltier. 2021. Unifying Decidable Entailments in Separation Logic with
     Inductive Definitions. In Automated Deduction – CADE 28, André Platzer and Geoff Sutcliffe (Eds.). Springer International
     Publishing, Cham, 183–199.
[23] Jean-Christophe Filliâtre, Léon Gondelman, and Andrei Paskevich. 2016. The spirit of ghost code. Formal Methods in
     System Design 48 (2016), 152–174.
[24] Alex Gyori, Pranav Garg, Edgar Pek, and P. Madhusudan. 2017. Efficient Incrementalized Runtime Checking of Linear
     Measures on Lists. In 2017 IEEE International Conference on Software Testing, Verification and Validation, ICST 2017,
     Tokyo, Japan, March 13-17, 2017. IEEE Computer Society, 310–320. https://doi.org/10.1109/ICST.2017.35
[25] Radu Iosif, Adam Rogalewicz, and Jiri Simacek. 2013. The Tree Width of Separation Logic with Recursive Definitions.
     In Automated Deduction – CADE-24, Maria Paola Bonacina (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 21–38.
[26] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     Powerful, Sound, Predictable, Fast Verifier for C and Java. In Proceedings of the Third International Conference on NASA
     Formal Methods (Pasadena, CA) (NFM’11). Springer-Verlag, Berlin, Heidelberg, 41–55.
[27] C. B. Jones. 2010. The Role of Auxiliary Variables in the Formal Development of Concurrent Programs. In Reflections on
     the Work of C.A.R. Hoare, A.W. Roscoe, Cliff B. Jones, and Kenneth R. Wood (Eds.). Springer London, London, 167–187.
     https://doi.org/10.1007/978-1-84882-912-1_8
[28] Bernhard Kragl and Shaz Qadeer. 2021. The Civl Verifier. In 2021 Formal Methods in Computer Aided Design (FMCAD).
     143–152. https://doi.org/10.34727/2021/isbn.978-3-85448-046-4_23
[29] Siddharth Krishna, Nisarg Patel, Dennis Shasha, and Thomas Wies. 2020. Verifying Concurrent Search Structure
     Templates. In Proceedings of the 41st ACM SIGPLAN Conference on Programming Language Design and Implementation
     (London, UK) (PLDI 2020). Association for Computing Machinery, New York, NY, USA, 181–196. https://doi.org/10.
     1145/3385412.3386029
[30] Siddharth Krishna, Dennis E. Shasha, and Thomas Wies. 2018. Go with the flow: compositional abstractions for
     concurrent data structures. Proc. ACM Program. Lang. 2, POPL (2018), 37:1–37:31. https://doi.org/10.1145/3158125
[31] Siddharth Krishna, Alexander J. Summers, and Thomas Wies. 2020. Local Reasoning for Global Graph Properties.
     In Programming Languages and Systems - 29th European Symposium on Programming, ESOP 2020, Held as Part of the
     European Joint Conferences on Theory and Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings
     (Lecture Notes in Computer Science, Vol. 12075), Peter Müller (Ed.). Springer, 308–335. https://doi.org/10.1007/978-3-
     030-44914-8_12
[32] Shuvendu Lahiri and Shaz Qadeer. 2008. Back to the Future: Revisiting Precise Program Verification Using SMT Solvers.
     SIGPLAN Not. 43, 1 (jan 2008), 171–182. https://doi.org/10.1145/1328897.1328461
[33] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
     and Chris Hawblitzel. 2023. Verus: Verifying Rust Programs Using Linear Ghost Types. Proc. ACM Program. Lang. 7,
     OOPSLA1, Article 85 (apr 2023), 30 pages. https://doi.org/10.1145/3586037
[34] Oukseh Lee, Hongseok Yang, and Rasmus Petersen. 2011. Program Analysis for Overlaid Data Structures. In Computer
     Aided Verification, Ganesh Gopalakrishnan and Shaz Qadeer (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     592–608.
[35] K Rustan M Leino. 2010. Dafny: An automatic program verifier for functional correctness. In International conference
     on logic for programming artificial intelligence and reasoning. Springer, 348–370.
[36] Tal Lev-Ami, Neil Immerman, Thomas Reps, Mooly Sagiv, Siddharth Srivastava, and Greta Yorsh. 2009. Simulating
     reachability using first-order logic with applications to verification of linked data structures. Logical Methods in
     Computer Science 5 (04 2009). https://doi.org/10.2168/LMCS-5(2:12)2009


Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                   220:25


[37] Christof Löding, P. Madhusudan, and Lucas Peña. 2018. Foundations for natural proofs and quantifier instantiation.
     PACMPL 2, POPL (2018), 10:1–10:30. https://doi.org/10.1145/3158098
[38] P Lucas. 1968. Two constructive realizations of the block concept and their equivalence, IBM Lab. Technical Report.
     Vienna TR 25.085.
[39] P. Madhusudan, Gennaro Parlato, and Xiaokang Qiu. 2011. Decidable Logics Combining Heap Structures and Data.
     SIGPLAN Not. 46, 1 (jan 2011), 611–622. https://doi.org/10.1145/1925844.1926455
[40] P. Madhusudan and Xiaokang Qiu. 2011. Efficient Decision Procedures for Heaps Using STRAND. In Static Analysis,
     Eran Yahav (Ed.). Springer Berlin Heidelberg, Berlin, Heidelberg, 43–59.
[41] Roland Meyer, Thomas Wies, and Sebastian Wolff. 2022. A Concurrent Program Logic with a Future and History. Proc.
     ACM Program. Lang. 6, OOPSLA2, Article 174 (oct 2022), 30 pages. https://doi.org/10.1145/3563337
[42] Roland Meyer, Thomas Wies, and Sebastian Wolff. 2023. Make Flows Small Again: Revisiting the Flow Framework. In
     Tools and Algorithms for the Construction and Analysis of Systems: 29th International Conference, TACAS 2023, Held as
     Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2023, Paris, France, April 22–27, 2023,
     Proceedings, Part I (Paris, France). Springer-Verlag, Berlin, Heidelberg, 628–646. https://doi.org/10.1007/978-3-031-
     30823-9_32
[43] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. 2016. Automatic Verification of Iterated Separating
     Conjunctions Using Symbolic Execution. In Computer Aided Verification, Swarat Chaudhuri and Azadeh Farzan (Eds.).
     Springer International Publishing, Cham, 405–425.
[44] Adithya Murali, Lucas Peña, Eion Blanchard, Christof Löding, and P. Madhusudan. 2022. Model-Guided Synthesis
     of Inductive Lemmas for FOL with Least Fixpoints. Proc. ACM Program. Lang. 6, OOPSLA2, Article 191 (oct 2022),
     30 pages. https://doi.org/10.1145/3563354
[45] Adithya Murali, Lucas Peña, Ranjit Jhala, and P. Madhusudan. 2023. Complete First-Order Reasoning for Properties of
     Functional Programs. Proc. ACM Program. Lang. 7, OOPSLA2, Article 259 (oct 2023), 30 pages. https://doi.org/10.1145/
     3622835
[46] Adithya Murali, Cody Rivera, and P. Madhusudan. 2024. Artifact for “Predictable Verification using Intrinsic Definitions”
     (v1.0). https://doi.org/10.5281/zenodo.10963124
[47] Adithya Murali, Cody Rivera, and P. Madhusudan. 2024. Predictable Verification using Intrinsic Defintitions (Technical
     Report), arXiv 2404.04515. https://arxiv.org/abs/2404.04515
[48] Charles Gregory Nelson. 1980. Techniques for Program Verification. Ph. D. Dissertation. Stanford University, Stanford,
     CA, USA. AAI8011683.
[49] Greg Nelson and Derek C. Oppen. 1979. Simplification by Cooperating Decision Procedures. ACM Trans. Program.
     Lang. Syst. 1, 2 (oct 1979), 245–257. https://doi.org/10.1145/357073.357079
[50] Huu Hai Nguyen and Wei-Ngan Chin. 2008. Enhancing Program Verification with Lemmas. In Proceedings of the
     20th International Conference on Computer Aided Verification (Princeton, NJ, USA) (CAV ’08). Springer-Verlag, Berlin,
     Heidelberg, 355–369. https://doi.org/10.1007/978-3-540-70545-1_34
[51] Peter W. O’Hearn. 2012. A Primer on Separation Logic (and Automatic Program Verification and Analysis). In Software
     Safety and Security - Tools for Analysis and Verification, Tobias Nipkow, Orna Grumberg, and Benedikt Hauptmann
     (Eds.). NATO Science for Peace and Security Series - D: Information and Communication Security, Vol. 33. IOS Press,
     286–318. https://doi.org/10.3233/978-1-61499-028-4-286
[52] Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning About Programs That Alter Data
     Structures. In Proceedings of the 15th International Workshop on Computer Science Logic (CSL ’01). Springer-Verlag,
     London, UK, UK, 1–19. http://dl.acm.org/citation.cfm?id=647851.737404
[53] Nisarg Patel, Siddharth Krishna, Dennis Shasha, and Thomas Wies. 2021. Verifying Concurrent Multicopy Search
     Structures. Proc. ACM Program. Lang. 5, OOPSLA, Article 113 (oct 2021), 32 pages. https://doi.org/10.1145/3485490
[54] Edgar Pek, Xiaokang Qiu, and P. Madhusudan. 2014. Natural Proofs for Data Structure Manipulation in C Using
     Separation Logic. SIGPLAN Not. 49, 6 (jun 2014), 440–451. https://doi.org/10.1145/2666356.2594325
[55] Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2013. Automating Separation Logic Using SMT. In Proceedings of
     the 25th International Conference on Computer Aided Verification (Saint Petersburg, Russia) (CAV’13). Springer-Verlag,
     Berlin, Heidelberg, 773–789. https://doi.org/10.1007/978-3-642-39799-8_54
[56] Ruzica Piskac, Thomas Wies, and Damien Zufferey. 2014. Automating Separation Logic with Trees and Data. In
     Proceedings of the 16th International Conference on Computer Aided Verification (CAV’14). Springer-Verlag, Berlin,
     Heidelberg, 711–728.
[57] Shaz Qadeer. 2023. Boogie Pull Request #669: Monomorphization of polymorphic maps and binders. https://github.
     com/boogie-org/boogie/pull/669
[58] John C. Reynolds. 1981. The craft of programming. Prentice Hall.
[59] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings of the 17th
     Annual IEEE Symposium on Logic in Computer Science (LICS ’02). IEEE Computer Society, USA, 55–74.


                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:26                                                                 Adithya Murali, Cody Rivera, and P. Madhusudan


[60] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In Proceedings of the 17th
     Annual IEEE Symposium on Logic in Computer Science (LICS ’02). IEEE Computer Society, USA, 55–74.
[61] Patrick M. Rondon, Ming Kawaguci, and Ranjit Jhala. 2008. Liquid types. SIGPLAN Not. 43, 6 (jun 2008), 159–169.
     https://doi.org/10.1145/1379022.1375602
[62] Mooly Sagiv, Thomas Reps, and Reinhard Wilhelm. 2002. Parametric Shape Analysis via 3-Valued Logic. ACM Trans.
     Program. Lang. Syst. 24, 3 (may 2002), 217–298. https://doi.org/10.1145/514188.514190
[63] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2016. Automated Mutual Explicit Induction
     Proof in Separation Logic. In FM 2016: Formal Methods, John Fitzgerald, Constance Heitmeyer, Stefania Gnesi, and Anna
     Philippou (Eds.). Springer International Publishing, Cham, 659–676. https://doi.org/10.1007/978-3-319-48989-6_40
[64] Cesare Tinelli and Calogero G. Zarba. 2004. Combining Decision Procedures for Sorted Theories. In Logics in Artificial
     Intelligence, Jóse Júlio Alferes and João Leite (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 641–653.




Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                     220:27


A     DETAILS FOR SECTION 3
A.1     Operational Semantics

           ∗
       ⊥→
        − ⊥
           skip
(𝑠, 𝑂, 𝐼 ) −−−→ (𝑠, 𝑂, 𝐼 )
           𝑥 := nil
(𝑠, 𝑂, 𝐼 ) −−−−−→ (𝑠 [𝑥 ↦→ nil], 𝑂, 𝐼 )
           𝑥 := 𝑦
(𝑠, 𝑂, 𝐼 ) −−−−→ (𝑠 [𝑥 ↦→ 𝑠 (𝑦)], 𝑂, 𝐼 )
           𝑣 := 𝑏𝑒
(𝑠, 𝑂, 𝐼 ) −−−−→ (𝑠 [𝑣 ↦→ 𝑒], 𝑂, 𝐼 )               where 𝑏𝑒 interprets to 𝑒 according to 𝑠 and 𝐼
           𝑦 := 𝑥 .𝑓
(𝑠, 𝑂, 𝐼 ) −−−−−→ (𝑠 [𝑦 ↦→ 𝐼 (𝑓 , 𝑠 (𝑥))], 𝑂, 𝐼 ) if (𝑓 , 𝑠 (𝑥)) ∈ dom(𝐼 )                            (similarly for 𝑣 := 𝑥 .𝑑)
           𝑦 := 𝑥 .𝑓
(𝑠, 𝑂, 𝐼 ) −−−−−→ ⊥ if (𝑓 , 𝑠 (𝑥)) ∉ dom(𝐼 )                                                          (similarly for 𝑣 := 𝑥 .𝑑)
           𝑥 .𝑓 := 𝑦
(𝑠, 𝑂, 𝐼 ) −−−−−→ (𝑠, 𝑂, 𝐼 [(𝑓 , 𝑠 (𝑥)) ↦→ 𝑠 (𝑦)]) if (𝑓 , 𝑠 (𝑥)) ∈ dom(𝐼 )                          (similarly for 𝑥 .𝑑 := 𝑣)
           𝑥 .𝑓 := 𝑦
(𝑠, 𝑂, 𝐼 ) −−−−−→ ⊥ if (𝑓 , 𝑠 (𝑥)) ∉ dom(𝐼 )                                                          (similarly for 𝑥 .𝑑 := 𝑣)
           𝑥 := new 𝐶 ( )
(𝑠, 𝑂, 𝐼 ) −−−−−−−−−→ (𝑠 [𝑥 ↦→ 𝑜], 𝑂 ∪ {𝑜 }, 𝐼 [(𝑓 , 𝑜) ↦→ default 𝑓 ])
                               for some 𝑜 ∈ N such that 𝑜 ∉ 𝑂
           𝑟 := Function(𝑡 )                                                               𝑄 (𝑚, ret: 𝑛)
(𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−→ (𝑠 [𝑟 ↦→ 𝑠 ′ (𝑛)], 𝑂 ′, 𝐼 ′ ) if (∅[𝑚 ↦→ 𝑠 (𝑡)], 𝑂, 𝐼 ) −−−−−−−−−→ (𝑠 ′, 𝑂 ′, 𝐼 ′ )
                                where 𝑄 (𝑚, ret : 𝑛) is the code of the method Function,
                                with 𝑚 and 𝑛 being the formal input and output parameters for 𝑄
           assume cond
(𝑠, 𝑂, 𝐼 ) −−−−−−−−−→ (𝑠, 𝑂, 𝐼 ) if cond interprets to True according to 𝑠 and 𝐼
           𝑃1 ; 𝑃2                                  𝑃1
(𝑠, 𝑂, 𝐼 ) −−−−→ (𝑠 ′′, 𝑂 ′′, 𝐼 ′′ ) if (𝑠, 𝑂, 𝐼 ) −→ (𝑠 ′, 𝑂 ′, 𝐼 ′ )
                                                           𝑃2
                                      and (𝑠 ′, 𝑂 ′, 𝐼 ′ ) −→ (𝑠 ′′, 𝑂 ′′, 𝐼 ′′ ) for some (𝑠 ′, 𝑂 ′, 𝐼 ′ )
           if cond then 𝑃1 else 𝑃 2                              assume cond ; 𝑃1
(𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−−−−−→ (𝑠 ′, 𝑂 ′, 𝐼 ′ ) if (𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−−→ (𝑠 ′, 𝑂 ′, 𝐼 ′ )
           if cond then 𝑃1 else 𝑃 2                              assume ¬cond ; 𝑃2
(𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−−−−−→ (𝑠 ′, 𝑂 ′, 𝐼 ′ ) if (𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−−−→ (𝑠 ′, 𝑂 ′, 𝐼 ′ )
           while cond do 𝑃                                 assume cond ; 𝑃 ; while cond do 𝑃
(𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−→ (𝑠 ′, 𝑂 ′, 𝐼 ′ ) if (𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−−−−−−−−−−−−−→ (𝑠 ′, 𝑂 ′, 𝐼 ′ )
           while cond do 𝑃                               assume ¬cond
(𝑠, 𝑂, 𝐼 ) −−−−−−−−−−−→ (𝑠, 𝑂, 𝐼 ) if (𝑠, 𝑂, 𝐼 ) −−−−−−−−−−→ (𝑠, 𝑂, 𝐼 )



                                               Fig. 5. Operational Semantics

   We give the formal operational semantics for programs in our language (Figure 1) in Figure 5
below.
   Configurations are of the form (𝑠, 𝑂, 𝐼 ) where 𝑂 ⊂finite N represents the set of allocated objects,
𝑠 represents the store and interprets program variables, and 𝐼 represents the heap and interprets
mutable fields in F —including ghost fields G when they are used— on 𝑂 (interpretations are total).

                                       Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:28                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


Although formally 𝑠 and 𝐼 are a family of functions indexed by the sorts of the variables (resp.
signatures of the maps), we abuse notation and use 𝑠 (𝑥) to denote the interpretation of a variable
𝑥, and similarly 𝐼 (𝑓 , 𝑜) to denote the value of the field 𝑓 on the object 𝑜 in the configuration. We
add a sink state ⊥ to model error.
   Our language is safe, (i.e., allocated locations cannot point to un-allocated locations) and garbage-
collected. The operational semantics is the usual one for such programs. Figure 5 presents a
simplified operational semantics without considering return statements. The full semantics adds a
marker to signify completion of a procedure. Procedures can only end after return statements (we
syntactically disallow statements after a return) or at the end of a program.
   The rules for assignments, skip, sequencing, conditionals, and loops are trivial. De-referencing a
variable that does not point to an object (i.e., is nil) leads to the error state ⊥. Allocation ensures
memory safety by assigning the value of a field 𝑓 on a newly allocated object to a constant default 𝑓 .
For pointer fields this value is nil. Finally, we define the operational semantics for function calls
using summaries.

A.2      Ghost Code


     𝑃 B 𝑥 := Expr [Var𝑈 , F ] | 𝑦 := 𝑥 .𝑓 | 𝑥 .𝑓 := 𝑦 | 𝑧 := new 𝐶 ()
         | 𝑟 := Func(𝑡)         𝑟, 𝑡 are variables in Var𝑈 ∪ Var 𝐺
          (Functions can have ghost input/output parameters)
         | 𝐺𝑃
          (GP are “pure” ghost programs)
         | skip | assume cond | return
         | 𝑃 ; 𝑃 | if cond then 𝑃 else 𝑃 | while cond do 𝑃
  cond B BoolExpr [Var𝑈 , F ]
  𝐺𝑃 B 𝑎 := Expr [Var𝑈 ∪ Var 𝐺 , F ∪ G] | 𝑏 := 𝑥 .𝑔 | 𝑏 := 𝑥 .𝑓
         (Ghost variables can read from both user and ghost variables/maps)
        | 𝑥 .𝑔 := 𝑏 | 𝑥 .𝑔 := 𝑦
         (Ghost maps can only be assigned values from ghost variables)
        | 𝑠 := GhostFunc(𝑣)       𝑠, 𝑣 are variables in Var 𝐺 , GhostFunc is always terminating
        | skip | 𝐺𝑃 ; 𝐺𝑃 | if Gcond then 𝐺𝑃 else 𝐺𝑃
        | while Gcond do 𝐺𝑃 loop is always terminating
Gcond B BoolExpr [Var𝑈 ∪ Var 𝐺 , F ∪ G]

Fig. 6. Grammar of programs with ghost code. 𝑥, 𝑦, 𝑧 are user variables Var𝑈 , 𝑎, 𝑏 are ghost variables Var 𝐺 ,
𝑓 ∈ F is a user field, and 𝑔 ∈ G is a ghost map. Notation Expr [Vars, Maps] denotes expressions over
the vocabulary given by variables Vars and maps Maps, similarly BoolExpr [Vars, Maps] denotes boolean
expressions. Termination for ghost loops and functions can be established in any way.


   In this section we formally define our programming language augmented with ghost code, as
well as the projection of ghost-augmented code to ‘user’ code.
   Fix a set of user variables Var𝑈 and ghost variables Var 𝐺 . We already introduced user fields F
and ghost fields/maps G in Section 2.2. We define a programming language over this vocabulary in
Figure 6 below. The main aspects to note are: (a) ghost variables can read from user variables/maps,
but the reverse is not allowed, (b) ghost conditionals and loops must only contain bodies that are
purely ghost, and (c) ghost loops and functions must always terminate. These choices ensure that

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                               220:29


ghost variables do not affect the execution of the user program. We can formalize this claim using
the idea of ‘projecting out’ ghost code and obtaining a pure user program
Projection that Eliminates Ghost Code. Fix a main method 𝑀 with body 𝑄 0 . Let 𝑁𝑖 , 1 ≤ 𝑖 ≤ 𝑘 be a
set of auxiliary methods with bodies 𝑄𝑖 that 𝑄 0 can call. Note that the bodies 𝑄 0 and 𝑄𝑖 contain ghost
code. Let us denote a program containing these methods by [(𝑀 : 𝑄 0 ); (𝑁 1 : 𝑄 1 ) . . . (𝑁𝑘 : 𝑄𝑘 )]. We
then define projection as follows:

   Definition A.1 (Projection of Ghost-Augmented Code to User Code). The projection of the ghost-
augmented program [(𝑀 : 𝑄 0 ); (𝑁 1 : 𝑄 1 ) . . . (𝑁𝑘 : 𝑄𝑘 )] is the user program [( 𝑀ˆ : 𝑄ˆ0 ); ( 𝑁ˆ1 :
𝑄ˆ1 ) . . . ( 𝑁ˆ𝑘 : 𝑄ˆ𝑘 )] such that:
   (1) The input (resp. output) signature of 𝑀ˆ is that of 𝑀 with the ghost input (resp. output)
          parameters removed. Formally, given a sequence of parameters 𝑥 with some elements in
          the sequence marked as ghost, we can define the projection as the sequence formed by the
          non-continguous subsequence of parameters in 𝑥 consisting of non-ghost parameters.
   (2) 𝑄ˆ0 is derived from 𝑄 0 by: (a) eliminating all ghost code, i.e., replacing yields of the nonterminal
          GP in Figure 6 with skip, and (b) replacing each non-ghost function call statement of the
          form 𝑟 := 𝑁 𝑗 (𝑡) with the statement 𝑠 := 𝑁ˆ 𝑗 (𝑢), where 𝑢, 𝑠 are obtained from 𝑡, 𝑟 by projecting
          out the elements corresponding to the ghost parameters in the signature of 𝑁 𝑗 . Each 𝑄ˆ𝑖 is
          derived from the corresponding 𝑄𝑖 by a similar transformation.
          We define this formally as a recursive transformation on the structure of the grammar of 𝑃
          (ghost-augmented programs) in Figure 6:

                                 Projection(𝐺𝑃) = skip
                                                      ˆ
                      Projection(𝑟 B Func(𝑡)) = 𝑠 B Func(𝑢)
                                                        𝑢, 𝑠 are obtained from 𝑡, 𝑟 by projecting out
                                                        elements corresponding to ghost parameters
                                Projection(stmt) = stmt for all other statements
                              Projection(𝑃 1 ; 𝑃2 ) = Projection(𝑃1 ) ; Projection(𝑃2 )
         Projection(if cond then 𝑃1 else 𝑃2 ) = if cond then Projection(𝑃1 ) else Projection(𝑃 2 )
                Projection(while cond do 𝑃) = while cond do Projection(𝑃)

A.3    Generating Quantifier-Free Verification Conditions
The FWYB methodology described in previous sections shows that we can soundly reduce the
problem of verifying programs with intrinsic specifications to the problem of verifying programs
(with ghost code) with quantifier-free contracts. We then argue that we can reason with the latter
using combinations of various quantifier-free theories including sets and maps with pointwise
updates. In this section we detail some subtleties involved in the argument.
   It is well-known that we can reason with scalar programs with quantifier-free contracts by
generating quantifier-free verification conditions (which in turn can be handled by SMT solvers).
However, this is not immediately clear for programs that dynamically manipulate heaps. In particu-
lar, commands such as allocation and function calls pose challenges in formulating quantifier-free
verification conditions.
   At a high level, our solution transforms the given heap program into a scalar program that
explicitly encodes changes to the heap. Specifically, we show an encoding for the field mutation,
allocation, and function call statements.

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:30                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


Modeling Field Mutation. As described earlier, we model the monadic maps and fields as updatable
maps [18]. Formally, we introduce a map 𝑀 𝑓 (also called an array in SMT solvers like Z3 [17]) for
every field/monadic map 𝑓 . We then encode the commands for field lookup and mutation as map
operations. For example, the mutation 𝑥 .𝑓 B 𝑦 is encoded as 𝑀 𝑓 [𝑥] := 𝑦.
Modeling Allocation. We model programs in a safe garbage-collected programming language.
We introduce a ghost global variable Alloc to model the allocated set of objects in the program. We
then add several assumptions (i.e., assume statements) throughout the program. Specifically, we
assume for every program parameter of type Object, the parameter itself as well as the values of
the monadic maps of type Object/Set-of-Objects on the parameter are all contained in Alloc. For
example, in the case of our running example (Example 3.6), we add the assumptions 𝑥 ∈ Alloc and
next (𝑥) ≠ nil ⇒ next (𝑥) ∈ Alloc. If we had a monadic map hslist corresponding to the heaplet of
the sorted list, we would also add the assumption hslist (𝑥) ⊆ Alloc. Similarly, whenever an object
is dereferenced on a field of type Object/Set-of-Objects in the program, we add an assumption that
the resulting value is contained in Alloc. Note that these are quantifier-free assumptions. They can
be added soundly since they are valid under the semantics of the underlying language.
   We then model allocation by introducing a new object to Alloc and ensure that the default
values of the various fields on the newly allocated object belong to Alloc. These constraints can be
expressed using a quantifier-free formula over maps.
Modeling Heap Change Across Function Calls. The main challenge in modeling function calls
is to ensure the ability to do frame reasoning. To do this, we extend the programming language
with a modified set annotation for methods. We require the modified set to be a term of type
Set-of-Objects that is constructed using object variables in the current scope and monadic maps
over them. In the case of our running example (Example 3.1), we would add a monadic map hslist
of type Set-of-Objects corresponding to the heaplet of the sorted list and annotate the program
with hslist (𝑥) as the modified set. Figure 7 shows the full version of sorted list insertion with the
modified set annotation.
   Given a modified set Mod, we model changes to the heap across a function call by introducing
new maps corresponding to the various fields (including monadic maps) after the call. We then add
assumptions that the values of the new maps are equal to the values of the maps before the call
on all locations that do not belong to the modified set Mod. Although this constrains the maps on
unboundedly many objects, it can be written without quantifiers by using pointwise operators on
maps [18]. Formally, for a field 𝑓 modeled as a map 𝑀 𝑓 , we introduce a new map 𝑀 𝑓′ and update
𝑀 𝑓 as:
                                    𝑀 𝑓 [𝑥] := ite(𝑥 ∈ Mod, 𝑀 𝑓′ [𝑥], 𝑀 𝑓 [𝑥])
The above update can be expressed using pointwise operators as 𝑀 𝑓 B ite(Mod, 𝑀 𝑓′ , 𝑀 𝑓 ), where
the ite operator is applied pointwise over the maps Mod, 𝑀 𝑓 , and 𝑀 𝑓′ . The value of the field 𝑓
on an object 𝑥 after the call will then be equal to 𝑥 .𝑓 before the call if 𝑥 was not modified, and a
havoc-ed value given by 𝑀 𝑓′ otherwise. Pointwise operators are supported by the generalized array
theory [18] whose quantifier-free fragment is decidable.
  Program verifiers like Boogie [57] offer VC generation frameworks that are amenable to the
modeling described in this section. Indeed, our implementation of the IDS/FWYB methodology
described in Section 5.1 uses Boogie.

B    PROOFS OF SOUNDNESS FOR STAGES 1, 2, AND 3 OF FWYB
In this section we detail the proofs of soundness for the various stages of the FWYB methodology.
We first introduce some notation and show some preliminary lemmas.

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                               220:31


Projection for Configurations. The stages of FWYB deal with two kinds of triples, one whose
validity is stated with respect to configurations that interpret ghost variables and maps, and one over
configurations that only interpret user variables and fields. Given a configuration 𝐶 that interprets
ghost variables/maps, we denote by 𝐶ˆ the projection of that configuration to user variables that
simply eliminates all ghost interpretations. Conversely, given a configuration 𝑐 we say that 𝐶
extends 𝑐 with an interpretation for ghost variables/maps if 𝐶ˆ = 𝑐. We define 𝑏𝑜𝑡   ˆ = ⊥.
Lemmas About Projection that Eliminates Ghost Code. We show the following lemmas about
projection that eliminates ghost code (Definition A.1). We assume that there is only one procedure
𝑀 in the program for simplicity of presentation. Recall that 𝑀 can contain ghost code and 𝑀ˆ
is the projection of 𝑀 that eliminates the ghost code (with appropriately modified input/output
parameters).
  Lemma B.1. Let 𝐶 1 be a configuration that interprets ghost variables/maps. If 𝑀 is a “pure ghost”
program, (i.e., a yield of GP in the grammar in Figure 6), then 𝑀 always terminates starting from 𝐶 1 .
  The above lemma says that pure ghost programs always terminate. It follows directly from the
definition of ghost code which requires pure ghost loops and functions to be terminating.    □
  Lemma B.2. Let 𝑐 be a configuration that does not interpret ghost variables/maps. If 𝑀ˆ (projected
code that does not contain ghost code) terminates starting from 𝑐, then 𝑀 (which contains additional
ghost code) must terminate starting from any configuration 𝐶 that extends 𝑐.
  The above lemma says that the termination of the original user program is preserved by any
augmentation with ghost code. In a certain sense, it ‘lifts’ Lemma B.1 to programs that contain
both user and ghost code.
   Proof. The lemma follows from structural induction on the definition of projection, i.e., on the
structure of the grammar for the nonterminal 𝑃 in Figure 6. The argument for basic statements
is trivial. For pure ghost programs the result follows from Lemma B.1. The argument for all
compositions (sequential, conditional, loop) and function calls follows from the induction hypothesis.
                                                                                                   □

  Lemma B.3. Let 𝐶 1 be a configuration that interprets ghost variables/maps. If 𝑀 is a “pure ghost”
program and 𝑀 starting from 𝐶 1 reaches some 𝐶 2 and 𝐶 2 ≠ ⊥, then 𝐶ˆ1 = 𝐶ˆ2 .
  The above lemma says that ghost code does not affect the values of user (non-ghost) variables
and maps. It follows trivially by structural induction on the GP grammar, using the definition of
operational semantics (Figure 5). The key observation is that GP syntactically disallows non-ghost
variables/maps to read from ghost variables/maps.                                               □
  We can similarly ‘lift’ the above lemma to programs that contain both user code and ghost code.
   Lemma B.4. Let 𝑐 be a configuration that does not interpret ghost variables/maps. If 𝑀ˆ starting
from 𝑐 1 reaches some 𝑐 2 , then 𝑀 starting from any configuration 𝐶 1 that extends 𝑐 1 must either reach
⊥ or some 𝐶 2 that extends 𝑐 2 .
  The above lemma says that augmentation with ghost code does not affect how the original
program executes.
  Proof. As with Lemma B.2, we proceed by structural induction on the grammar for 𝑃 in Figure 6.
The argument for basic non-ghost statements follows trivially from the definition of operational
semantics. They key observation is that non-ghost statements do not affect the values of ghost
variables/maps (ensured by the syntactic restrictions). For pure ghost programs the result follows

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:32                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


from Lemma B.3. The argument for all compositions (sequential, conditional, loop) and function
calls follows from the induction hypothesis.                                                 □

PROOF OF PROPOSITION 3.4
We can state the proposition simply as follows: if ⟨ LC ∧ 𝜓 pre ⟩ 𝑀 ⟨ LC ∧ 𝜓 post ⟩ is valid, then
⟨ ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 pre ⟩ 𝑀ˆ ⟨ ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 post ⟩ is valid.
    Fix configurations (without ghost state) 𝑐 1, 𝑐 2 such that 𝑐 1 satisfies ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 pre and
𝑀ˆ starting from 𝑐 1 reaches 𝑐 2 . To show that the given Hoare triple for 𝑀ˆ is valid, we must establish
that 𝑐 2 is not ⊥, and further that 𝑐 2 satisfies ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 post .
    Since 𝑐 1 |= ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 pre , by the semantics of second order logic there exists a configu-
ration (taken as a model) extending 𝑐 1 , say 𝐶 1 , such that 𝐶 1 |= LC ∧ 𝜓 pre . First, using Lemma B.2 we
have that 𝑀 starting from 𝐶 1 must terminate. Further, since the triple ⟨ LC ∧ 𝜓 pre ⟩ 𝑀 ⟨ LC ∧ 𝜓 post ⟩
is valid, it must be the case that 𝑀 starting from 𝐶 1 reaches some 𝐶 2 such that 𝐶 2 ≠ ⊥ and
𝐶 2 |= LC ∧ 𝜓 post .
    We now use Lemma B.4 to conclude that 𝐶ˆ2 = 𝑐 2 . Since 𝐶 2 ≠ ⊥, we have that 𝑐 2 ≠ ⊥. Further,
since 𝐶 2 |= LC ∧ 𝜓 post , we have from the semantics of the logic that 𝐶 2 |= ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 post .
    Observe that the formula ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 post is stated over the common vocabulary of 𝐶 2
and 𝑐 2 , where the interpretations of the two configurations agree. Therefore, we can conclude that
𝑐 2 |= ∃𝑔1, 𝑔2 . . . , 𝑔𝑘 . LC ∧ 𝜓 post . This concludes the proof.                                             □

Proof of Proposition 3.5
The proof of Proposition 3.5 is similar to the above proof for Proposition 3.4, except that we must
now consider a definition of ghost code (akin to the development in Section A.2) that only considers
the variable Br as ghost.
   Repeating the arguments in the proof of Proposition 3.4 appropriately, we obtain that if
       ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛼 ∧ Br = ∅ ⟩ 𝑃 G,Br (𝑥, Br, ret : 𝑦, Br) ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛽 ∧ Br = ∅ ⟩
is valid, then                                                                                      
   ⟨ ∃Br. (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛼 ∧ Br = ∅ ⟩ 𝑃 G (𝑥, ret : 𝑦) ⟨ ∃Br. (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛽 ∧ Br = ∅ ⟩
is valid. This triple can be simplified to ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝛼 ⟩ 𝑃 G (𝑥, ret : 𝑦) ⟨ (∀𝑧. 𝜌 (𝑧)) ∧ 𝛽 ⟩, which
concludes the proof.

PROOF OF PROPOSITION 3.7
Given a well-behaved program 𝑃 such that {𝛼 } 𝑃 {𝛽} is valid, we must show that ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧
𝛼 ⟩ 𝑃 ⟨ (∀𝑧 ∉ Br. 𝜌 (𝑧)) ∧ 𝛽 ⟩ is valid.
   The proof proceeds by an induction on the nesting depth of method calls in a trace of the
program 𝑃. We elide this level of induction here because it is routine. Importantly, given a particular
execution of the program 𝑃, we must show that the claim holds, assuming it holds for all method calls
occurring in the execution. We show this by structural induction on the proof of well-behavedness
of 𝑃.
   There are several base cases.
   Skip/Assignment/Lookup/Return There is nothing to show for skip, assignment, lookup,
or return statements. These do not change the heap at all and the rule does not update Br either,
therefore if ⟨ 𝛼 ⟩ stmt ⟨ 𝛽 ⟩ is valid then certainly ⟨ (∀𝑧 ∉ Br. 𝜌) ∧ 𝛼 ⟩ stmt ⟨ (∀𝑧 ∉ Br. 𝜌) ∧ 𝛽 ⟩ is
valid.
   Mutation The claim is true for the mutation rule since by the premise of the rule we update
the broken set with the impact set consisting of all potential objects where local conditions may
not hold.

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                               220:33


   Function Call Here we simply appeal to the induction hypothesis.
   Allocation We refer to our operational semantics, which ensures that no object points to
a freshly allocated object. Therefore, the allocation of an object could have only broken the local
conditions on itself at most.
   Infer LC Outside Br There is nothing to prove for this rule as it does not alter the Br set at
all.
   Assert LC and Remove The claim holds for this rule by construction. If LC holds everywhere
outside Br , and we know that LC (𝑥) holds, then we can conclude that LC holds everywhere outside
Br \ {𝑥 }.
   It only remains to show that the claim holds for larger well-behaved programs obtained by
composing smaller well-behaved programs using sequencing, branching, or looping constructs. The
proof here is trivial as the argument for sequencing is trivial (we can think of a loop as unboundedly
many sequenced compositions of the smaller well-behaved program): we can always compose two
well-behaved programs to obtain a well-behaved program.                                             □

C    DETAILS FOR WELL-BEHAVED PROGRAMMING
General Construction for Automatically Checking Correctness of Impact Sets
Fix a class with maps F ∪ G = {𝑓1, 𝑓2, . . . 𝑓𝑛 } (includes both original and ghost fields) and an intrinsic
definition (G, LC, 𝜑) over which we prove correctness of programs. Without loss of generality, let
𝑓1, . . . 𝑓𝑘 for some 𝑘 ≤ 𝑛 alone correspond to pointer fields (where the range is an object); the others
we assume are data fields that range over background sorts. In the sequel we assume for simplicity
that LC (𝑥) only relates the fields of 𝑥 with those of 𝑓𝑖 (𝑥) for 1 ≤ 𝑖 ≤ 𝑘, i.e., the local conditions
only constrain the fields of 𝑥 with those of its neighboring objects that are “one pointer hop” away
from 𝑥.
   Consider a mutation 𝑥 .𝑓 B 𝑦 for some 𝑓 in 𝑓1 through 𝑓𝑛 and an arbitrary 𝑦. It is clear that the
only set of objects whose local condition can be impacted by this mutation are those that are one
pointer hop away via an incoming or outgoing edge in the heap (seen as a directed graph with
labeled edges corresponding to pointers), apart from 𝑥 itself. In general there can be unboundedly
many such objects, but in our work we only handle impact sets that can be expressed as a finite set
of terms over 𝑥 (see Section 3.5 under ‘Rules for Constructing Well-Behaved Programs’). Note here
that the impact set can be larger than the set of impacted objects as we only require that objects
not belonging to the impact set retain that LC holds on them under mutation. However, we attempt
here to construct of impact sets that are as small as possible.
   Following the above discussion, let us assume that the impact set consists of terms from the
following set:
                 ImpactableObjects = {𝑥, 𝑓1 (𝑥), . . . 𝑓𝑘 (𝑥)} ∪ {old (𝑓 (𝑥)) | 𝑓 is a pointer field}
   The reader may be inclined to suggest here that when 𝑓 is a pointer field, 𝑦 (the new value of
𝑓 (𝑥)) may also belong to the minimal impact set. However, this is not possible in general since
𝑦 is arbitrary, and in particular 𝑦 can be an object in the heap that is “far away” from 𝑥, i.e., not
one pointer hop away (either incoming or outgoing). The same argument applies to terms over 𝑦.
Therefore, if the (minimal) impact set is at all expressible as a set of terms over the vocabulary of
the mutation statement it must be a subset of the terms in the set ImpactableObjects defined above.
   Let this subset of terms be 𝐴. We then generate the following triple to check that 𝐴 is in fact an
impact set:
                               Ó
                          ⊢ {( 𝑡 ∈𝐴 𝑢 ≠ 𝑡) ∧ LC (𝑢) ∧ 𝑥 ≠ nil} 𝑥 .𝑓 := 𝑦 {LC (𝑢)}
   The triple says that any location 𝑢 that is not 𝐴 which satisfied LC before the mutation must
continue to satisfy it after the mutation. As discussed in the main text, this validity of this triple

                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:34                                                                           Adithya Murali, Cody Rivera, and P. Madhusudan

 pre: Br = ∅
 post: LC (𝑟 ) ∧ prev (𝑟 ) = nil
      ∧ Br = ite (old (prev (𝑥 ) ) = nil, ∅, {old (prev (𝑥 ) ) } )
      ∧ length(𝑟 ) = old (length(𝑥 ) ) + 1                                 Mut(z, prev, x, Br);
      ∧ keys (𝑟 ) = old (keys (𝑥 ) ) ∪ {𝑘 }                                AssertLCAndRemove(z, Br);
      ∧ old (hslist (𝑥 ) ) ⊂ hslist (𝑟 )                                   Mut(x, prev, nil, Br);
 modifies: hslist (𝑥 )                                                     Mut(x, hslist, {x} ∪ {z}, Br);
 sorted_list_insert(x: C, k: Int, Br: Set(C))                              Mut(x, length, 2, Br);
 returns r: C, Br: Set(C)                                                  Mut(x, keys, {x.key} ∪ {k}, Br);
 {                                                                         AssertLCAndRemove(x, Br);
   InferLCOutsideBr(x, Br);                                                r := x;
   if (x.key ≥ k) then { // k inserted before x                          }
     NewObj(z, Br);                  // {z}                              else { // recursive case
     Mut(z, key, k, Br);          // {z} since z.prev = nil                 y := x.next;
     Mut(z, next, x, Br); // {z} since z.next = nil                         InferLCOutsideBr(y, Br);
     Mut(z, hslist, {z} ∪ x.hslist, Br); // {z}                             tmp, Br := sorted_list_insert(y, k, Br); // {x}
     Mut(z, length, 1 + x.length, Br);              // {z}                  InferLCOutsideBr(y, Br);
     Mut(z, keys, {k} ∪ x.keys, Br);                // {z}                  if (y.prev = x) then {
     Mut(x, prev, z, Br);             // {z, x, old(prev(x))}                 Mut(y, prev, nil, Br);     // {y, x}
     AssertLCAndRemove(z, Br); // {x, old(prev(x))}                         }
     AssertLCAndRemove(x, Br); // {old(prev(x))}                            Mut(x, next, tmp, Br);       // {y, x}
     r := z;                                                                AssertLCAndRemove(y, Br); // {x}
   }                                                                        Mut(tmp, prev, x, Br);       // {tmp, x}
   else {                                                                   AssertLCAndRemove(tmp, Br); // {x}
   if (x.next = nil) then { // one-element list                             Mut(x, hslist, {x} ∪ tmp.hslist, Br); // {x, prev(x)}
     NewObj(z, Br);                                                         Mut(x, length, 1 + tmp.length, Br);    // {x, prev(x)}
     Mut(z, key, k, Br);                                                    Mut(x, keys, {x.key} ∪ tmp.keys, Br); // {x, prev(x)}
     Mut(z, next, nil, Br);                                                 Mut(x, prev, nil, Br);        // {x, old(prev(x))}
     Mut(z, hslist, {z}, Br);                                               AssertLCAndRemove(x, Br); // {old(prev(x))}
     Mut(z, length, 1, Br);                                                 r := x;
     Mut(z, keys, {k}, Br);                                              }}
     Mut(x, next, z, Br);                                            }

Fig. 7. Code for insertion into a sorted list written in the syntactic fragment for well-behaved pro-
grams(Section 4.1). Black lines denote code written by the user, and blue lines denote lines written by
the verification engineer. The comments on the right show the state of the broken set Br after the statement
on the corresponding line.


can be check effectively by decision procedures over quantifier-free combinations of theories that
are supported by SMT solvers [7, 17].
  Finally, we can compute a provably correct and minimal impact set automatically, if one exists, by
considering subsets of ImpactableObjects in turn and checking the corresponding triple as described
above. However, in our experiments we compute impact sets manually and check their correctness
automatically.

D     DETAILS FOR CASE STUDIES IN SECTION 4
In this appendix we provide further details for the various case studies discussed in the main text
and detail some other case studies not featured in the main text.

D.1      Discussion on Sorted List Insertion (Section 4.1)
We provide the specifications and the code augmented with ghost annotations in Figure 7.
   Specifications. The precondition states that the broken set is empty at the beginning of the
program. The postcondition states that the returned object 𝑟 satisfies the local conditions and
satisfies the correlation formula for a sorted list (i.e., prev(𝑟 ) = nil). However, the broken set is only
empty if the input object 𝑥 was the head of a sorted list, and it is {prev(𝑥)} otherwise. The other
conjuncts express functional specifications for insertion in terms of the length, heaplet, and set
of keys. We also add a ‘modifies’ clause which enables program verifiers for heap manipulating
programs to utilize frame reasoning across function calls.

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                           220:35


   Summary. The proof works at a high-level as follows: we recurse down the list, reaching the
appropriate object 𝑥 before which the new key must be inserted. This is the first branch in Figure 7,
and we show the broken set at each point in the comments to the right. We create the new object 𝑧
with the appropriate key and point 𝑧.next to 𝑥. We then fix the local conditions on 𝑥 and 𝑧. However,
these fixes break the LC on old (prev(𝑥)). We maintain this property up the recursion, at each point
fixing LC on 𝑥 and breaking it on old (prev(𝑥)) in the process. This is shown in the last branch in
the code. We eventually reach the head of the sorted list, whose prev in the pre state is nil, and at
that point the fixes do not break anything else, i.e., the broken set is empty (as desired).
   The verification engineer adds ghost code to perform these fixes as shown in blue in Figure 7.
We can also see that there are essentially as many lines of ghost code as there are lines of user code;
we compare these values across our benchmark suite (see Table 2) and find that this is typical for
many methods. However, the verification conditions for the (augmented) program are decidable
because they can be stated using quantifier-free formulas over decidable combinations of theories
including maps, map updates, and sets.

D.2    BST Right-Rotation
We now turn to another data structure and method that illustrates intrinsic definitions for trees,
namely verifying a right rotate on a binary search tree. Such an operation is a common tree
operation, and rotations are used widely in maintaining balanced search trees, such as AVL and
Red-Black Trees, on which several of our benchmarks operate.
  We augment the definition of binary trees discussed in Section 1 to include the 𝑚𝑖𝑛 : 𝐵𝑆𝑇 → 𝑅𝑒𝑎𝑙
and 𝑚𝑎𝑥 : 𝐵𝑆𝑇 → 𝑅𝑒𝑎𝑙 maps, which capture the minimum and maximum keys stored in the tree
rooted at a node, to help enforce binary search tree properties locally. The local condition and the
impact sets are as below:

      LC ≡ ∀𝑥 . 𝑚𝑖𝑛 (𝑥 ) ≤ 𝑘𝑒𝑦 (𝑥 ) ≤ 𝑚𝑎𝑥 (𝑥 )
      ∧ (𝑝 (𝑥 ) ≠ nil ⇒ 𝑙 (𝑝 (𝑥 ) ) = 𝑥 ∨ 𝑟 (𝑝 (𝑥 ) ) = 𝑥 )                          Mutated Field 𝑓   Impacted Objects 𝐴 𝑓
       ∧ (𝑙 (𝑥 ) = 𝑛𝑖𝑙 ⇒ 𝑚𝑖𝑛 (𝑥 ) = 𝑘𝑒𝑦 (𝑥 ) )                                              𝑙            {𝑥, old (𝑙 (𝑥 ) ) }
                                                                                            𝑟            {𝑥, old (𝑟 (𝑥 ) ) }
       ∧ (𝑙 (𝑥 ) ≠ nil ⇒ 𝑝 (𝑙 (𝑥 ) ) = 𝑥 ∧ 𝑟𝑎𝑛𝑘 (𝑙 (𝑥 ) ) < 𝑟𝑎𝑛𝑘 (𝑥 )                       𝑝            {𝑥, old (𝑝 (𝑥 ) ) }
                        ∧ 𝑚𝑎𝑥 (𝑙 (𝑥 ) ) < 𝑘𝑒𝑦 (𝑥 ) ∧ 𝑚𝑖𝑛 (𝑥 ) = 𝑚𝑖𝑛 (𝑙 (𝑥 ) ) )            key                 {𝑥 }
                                                                                          min              {𝑥, 𝑝 (𝑥 ) }
      ∧ (𝑟 (𝑥 ) = 𝑛𝑖𝑙 ⇒ 𝑚𝑎𝑥 (𝑥 ) = 𝑘𝑒𝑦 (𝑥 ) )                                             max              {𝑥, 𝑝 (𝑥 ) }
       ∧ (𝑟 (𝑥 ) ≠ nil ⇒ 𝑝 (𝑟 (𝑥 ) ) = 𝑥 ∧ 𝑟𝑎𝑛𝑘 (𝑟 (𝑥 ) ) < 𝑟𝑎𝑛𝑘 (𝑥 )                     rank             {𝑥, 𝑝 (𝑥 ) }
                        ∧ 𝑚𝑖𝑛 (𝑟 (𝑥 ) ) > 𝑘𝑒𝑦 (𝑥 ) ∧ 𝑚𝑎𝑥 (𝑥 ) = 𝑚𝑎𝑥 (𝑟 (𝑥 ) ) )



   We first describe the gist of how the data structure is repaired and provide the fully annotated
program below. Recall that in a BST right rotation, that there are two nodes 𝑥 and 𝑦 such that 𝑦
is 𝑥’s left child. After the rotation is performed, 𝑦 becomes the new root of the subtree, while 𝑥
becomes 𝑦’s right child. Several routine updates of the monadic map 𝑝 (parent) will have to be made.
The most interesting update is that of the 𝑟𝑎𝑛𝑘 : 𝐵𝑆𝑇 → 𝑅𝑒𝑎𝑙 map. Since 𝑦 is now the root of the
affected subtree, its rank must be greater than all its children. One way of doing this is to increase
𝑦’s rank to something greater than 𝑥’s rank. This works if 𝑦 has no parent, but not in general. To
solve this issue, we use the density of the Reals to set the rank of 𝑦 to (𝑟𝑎𝑛𝑘 (𝑥) + 𝑟𝑎𝑛𝑘 (𝑝 (𝑦)))/2.
Note that there are a fixed number of ghost map updates, as the various monadic maps for distant
ancestors and descendents of 𝑥, 𝑦 do not change (the min/max of subtrees of such nodes do not
change).
   We present the fully annotated program below, with comments displaying the state of the broken
set 𝐵𝑟 at the corresponding point in the program.

                                          Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:36                                                                  Adithya Murali, Cody Rivera, and P. Madhusudan


 pre: Br = ∅ ∧ 𝑙 (𝑥 ) ≠ nil ∧ 𝑝 (𝑥 ) = 𝑥𝑝
 post: Br = ∅ ∧ 𝑝 (𝑟𝑒𝑡 ) = 𝑥𝑝
       ∧ 𝑙 (𝑟𝑒𝑡 ) = old (𝑙 (𝑙 (𝑥 ) ) ) ∧ 𝑟𝑒𝑡 = old (𝑙 (𝑥 ) ) ∧ 𝑟 (𝑟𝑒𝑡 ) = 𝑥
       ∧ 𝑙 (𝑟 (𝑟𝑒𝑡 ) ) = old (𝑟 (𝑙 (𝑥 ) ) ) ∧ 𝑟 (𝑟 (𝑟𝑒𝑡 ) ) = old (𝑟 (𝑥 ) )
 bst_right_rotate(x: BST, xp: BST?, Br: Set(BST))
 returns ret: BST, Br: Set(BST)
 {
   LCOutsideBr(x, Br);
   if (xp ≠ nil) then {
        LCOutsideBr(xp, Br);
   }
   if (x.l ≠ nil) then {
        LCOutsideBr(x.l, Br);
   }
   if (x.l ≠ nil ∧ x.l.r ≠ nil) then {
        LCOutsideBr(x.l.r, Br);
   }
   var y := x.l;                            // {}
   Mut(x, l, y.r, Br);                      // {x, y}
   if (xp ≠ nil) then {
        if (x = xp.l) then {
              Mut(xp, l, y, Br); // {xp, x, y}
        }
        else {
              Mut(xp, r, y, Br); // {xp, x, y}
        }
   }
   Mut(y, r, x, Br);                        // {xp, x, y, x.l} (Note: x.l == old(y.r))
   // (1): Repairing x.l
   if (x.l ≠ nil) then {
        Mut(x.l, p, x, Br);                 // {xp, x, y, x.l}
   }
   // (2): Repairing x
   Mut(x, p, y, Br);                        // {xp, x, y, x.l}
   Mut(x, min, if x = nil then x.k else x.l.min, Br);                       // {xp, x, y, x.l}
   // (3): Repairing y
   Mut(y, p, xp, Br);                       // {xp, x, y, x.l}
   Mut(y, max, x.max, Br);                  // {xp, x, y, x.l}
   Mut(y, rank, if xp = nil then x.rank+1 else (xp.rank+x.rank)/2, Br);                        // {xp, x, y, x.l}
   AssertLCAndRemove(x.l, Br); // {xp, x, y}
   AssertLCAndRemove(x, Br);                // {xp, y}
   AssertLCAndRemove(y, Br);                // {xp}
   AssertLCAndRemove(xp, Br);               // {}
   ret := y // return y
 }

D.3      Discussion on Sorted List Reversal (Section 4.2)
What follows are the complete local conditions and impact sets for Sorted List Reverse:
   The following program reverses a sorted list as defined by the local condition above. We annotate
this program with comments on the current composition of the broken set according to the rules
of Table 3.
 pre: Br = ∅ ∧ 𝜑 (𝑥 ) ∧ sorted (𝑥 )
 post: Br ′ = ∅ ∧ 𝜑 (𝑟𝑒𝑡 ) ∧ rev_sorted (𝑟𝑒𝑡 ) ∧ keys (𝑟𝑒𝑡 ) = old (keys (𝑥 ) ) ∧ hslist (𝑟𝑒𝑡 ) = old (hslist (𝑥 ) )
 sorted_list_reverse(x: C, Br: Set(C))
 returns ret: C, Br: Set(C)
 {

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                220:37


          LC ≡ ∀𝑥 . prev(𝑥) ≠ nil ⇒ next (prev(𝑥)) = 𝑥
                    ∧ next (𝑥) ≠ nil ⇒ prev(next (𝑥)) = 𝑥
                                               ∧ length(𝑥) = length(next (𝑥)) + 1
                                               ∧ keys(𝑥) = keys(next (𝑥)) ∪ {key(𝑥)}
                                               ∧ hslist (𝑥) = hslist (next (𝑥)) ⊎ {𝑥 }
                                               ∧ sorted (𝑥) ⇒ key(𝑥) ≤ key(next (𝑥))
                                                                   ∧ sorted (𝑥) = sorted (next (𝑥))
                                               ∧ rev_sorted (𝑥) ⇒ key(𝑥) ≥ key(next (𝑥))
                                                                   ∧ rev_sorted (𝑥) = rev_sorted (next (𝑥))
                   ∧ (next (𝑥) = nil ⇒ length(𝑥) = 1 ∧ keys(𝑥) = {𝑥 } ∧ hslist (𝑥) = {𝑥 })

                             Fig. 9. Full local condition for lists for Sorted List Reverse


                                      Mutated Field 𝑓          Impacted Objects 𝐴 𝑓
                                           next                  {𝑥, old (next (𝑥))}
                                            key                    {𝑥, prev(𝑥)}
                                           prev                  {𝑥, old (prev(𝑥))}
                                          length                   {𝑥, prev(𝑥)}
                                           keys                    {𝑥, prev(𝑥)}
                                           hslist                  {𝑥, prev(𝑥)}
                                          sorted                   {𝑥, prev(𝑥)}
                                        rev_sorted                 {𝑥, prev(𝑥)}
                              Table 3. Full impact sets for lists for Sorted List Reverse




   LCOutsideBr(x, Br);
   var cur := x;
   ret := null;
   while (cur ≠ nil)
      invariant 𝑐𝑢𝑟 ≠ nil ⇒ 𝐿𝐶 (𝑐𝑢𝑟 ) ∧ sorted (𝑐𝑢𝑟 ) ∧ 𝜑 (𝑐𝑢𝑟 )
      invariant 𝑟𝑒𝑡 ≠ nil ⇒ 𝐿𝐶 (𝑟𝑒𝑡 ) ∧ rev_sorted (𝑟𝑒𝑡 ) ∧ 𝜑 (𝑟𝑒𝑡 )
      invariant 𝑐𝑢𝑟 ≠ nil ∧ 𝑟𝑒𝑡 ≠ nil ⇒ key (𝑟𝑒𝑡 ) ≤ 𝑘𝑒𝑦 (𝑐𝑢𝑟 )
      invariant old (keys (𝑥 ) ) = ite (𝑐𝑢𝑟 = nil, ∅, keys (𝑐𝑢𝑟 ) ) ∪ ite (𝑟𝑒𝑡 = nil, ∅, keys (𝑟𝑒𝑡 ) )
      invariant old (hslist (𝑥 ) ) = ite (𝑐𝑢𝑟 = nil, ∅, hslist (𝑐𝑢𝑟 ) ) ∪ ite (𝑟𝑒𝑡 = nil, ∅, hslist (𝑟𝑒𝑡 ) )
      invariant 𝐵𝑟 = ∅
      decreases ite (𝑐𝑢𝑟 ≠ nil, 0, length(𝑐𝑢𝑟 ) )
   {
      var tmp := cur.next;                           // {}
      if (tmp ≠ nil) then {
        LCOutsideBr(tmp, Br);                        // {}
        Mut(tmp, p, nil, Br);                        // {cur, tmp}
      }
      Mut(cur, next, ret, Br);                       // {cur, tmp}
      if (ret ≠ nil) then {
        Mut(ret, p, cur, Br);                        // {cur, tmp, ret}
      }
      Mut(cur, keys,


                                      Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:38                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


           {cur.k} ∪ (if cur.next=nil then 𝜑 else cur.next.keys), Br);   // {cur, tmp, ret}
         Mut(cur, hslist,
           {cur} ∪ (if cur.next=nil then 𝜑 else cur.next.hslist), Br);   // {cur, tmp, ret}
         if (cur.next ≠ nil ∧ (cur.key > cur.next.key ∨ ¬cur.next.sorted)) {
           Mut(cur, sorted, false, Br);     // {cur, tmp, ret}
         }
         Mut(cur, rev_sorted, true, Br);    // {cur, tmp, ret}
         AssertLCAndRemove(cur, Br);        // {tmp, ret}
         AssertLCAndRemove(ret, Br);        // {tmp}
         AssertLCAndRemove(tmp, Br);        // {}
         ret := cur;
         cur := tmp;
     }
     // The current value of ret is returned
 }

D.4      Discussion on Circular List Insert Back (Section 4.3)
We first provide the local conditions and impact sets for circular lists.


     LC ≡ ∀𝑥 . next (𝑥) ≠ nil ∧ prev(𝑥) ≠ nil
            ∧ next (prev(𝑥)) = 𝑥 ∧ prev(next (𝑥)) = 𝑥
            ∧ last (𝑥) = 𝑥 ⇒ length(𝑥) = 0 ∧ rev_length(𝑥) = 0
                                 ∧ last (𝑥) = last (next (𝑥))
                                 ∧ next (𝑥) = 𝑥 ⇒ keys(𝑥) = ∅ ∧ hslist (𝑥) = {𝑥 }
                                 ∧ next (𝑥) ≠ 𝑥 ⇒ keys(𝑥) = keys(next (𝑥))                                 (C1)
                                                        ∧ hslist (𝑥) = {𝑥 } ∪ hslist (next (𝑥))            (C2)
            ∧ last (𝑥) ≠ 𝑥 ⇒ length(𝑥) = length(next (𝑥)) + 1
                                 ∧ rev_length(𝑥) = rev_length(prev(𝑥)) + 1
                                 ∧ next (𝑥) = last (𝑥) ⇒ keys(𝑥) = {key(𝑥)} ∧ hslist (𝑥) = {𝑥 }
                                 ∧ next (𝑥) ≠ last (𝑥) ⇒ keys(𝑥) = {key(𝑥)} ∪ keys(next (𝑥))               (C3)
                                                              ∧ hslist (𝑥) = {𝑥 } ∪ hslist (next (𝑥))      (C4)
                                                              ∧ 𝑥 ∉ hslist (next (𝑥))
                                 ∧ last (𝑥) = last (next (𝑥))
                                 ∧ last (last (𝑥)) = last (𝑥)
                                 ∧ 𝑥 ∈ hslist (last (𝑥))
                                 ∧ prev(𝑥) ∈ hslist (last (𝑥))
                                 ∧ next (𝑥) ∈ hslist (last (𝑥))

                        Fig. 10. Full local condition for lists for Circular List Insert Back


  The local condition LC for circular lists can be seen in Figure 10. For use in loop invariants, we
have defined two variants of the local condition. One of these variants is 𝐿𝐶𝑀𝑖𝑛𝑢𝑠𝑁 𝑜𝑑𝑒 (𝑥, 𝑛), which
can be seen as a predicate on nodes 𝑥 and 𝑛, and is formed from LC by replacing the clauses (C1),
(C3), and (C4) in Figure 10 with the three clauses (C1’), (C3’), and (C4’) in Figure 11. Additionally,

Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                               220:39


we have another variant: 𝐿𝐶𝐿𝑎𝑠𝑡 (𝑥, 𝑛), which is formed from 𝐿𝐶 by replacing the clause (C2) in
Figure 10 with hslist (𝑥) = {𝑥, 𝑛} ∪ hslist (next (𝑥)).

              (keys(𝑥) = keys(next (𝑥)) \ {key(𝑛)} ∨ keys(𝑥) = keys(next (𝑥)))                       (C1’)
              (keys(𝑥) = (key(𝑥) ∪ keys(next (𝑥))) \ {key(𝑛)}                                        (C3’)
                ∨ keys(𝑥) = (key(𝑥) ∪ keys(next (𝑥))))
              (hslist (𝑥) = (𝑥 ∪ hslist (next (𝑥))) \ {𝑛})                                           (C4’)

                               Fig. 11. Alterations to Figure 10 to form 𝐿𝐶𝑀𝑖𝑛𝑢𝑠𝑁 𝑜𝑑𝑒

   Note that in this example as well as other benchmarks where we introduce scaffolding nodes, in
order to prove a bound on the impact set, we require that a precondition 𝜙 holds before we mutate
particular fields of nodes. The fields, preconditions, and impact sets for every node can be seen
in Table 4. Note that our benchmark contains another manipulation macro, AddToLastHsList(x,
n, Br), which, if x is a scaffolding node (or last (𝑥) = 𝑥), adds the node n to the set hslist (𝑥). The
precondition for invoking this macro is that last (𝑥) = 𝑥, and the only object impacted by the macro
is {𝑥 }.

       Mutated Field 𝑓                     Mutation Precond. 𝜙                           Impacted Objects 𝐴 𝑓
            next                                      ⊤                                    {𝑥, old (next (𝑥))}
             key                                      ⊤                                      {𝑥, prev(𝑥)}
            prev                                      ⊤                                    {𝑥, old (prev(𝑥))}
             last             last (𝑥) ≠ 𝑥 ∨ (last (𝑥) = 𝑥 ∧ hslist (𝑥) = {𝑥 })              {𝑥, prev(𝑥)}
           length                                     ⊤                                      {𝑥, prev(𝑥)}
         rev_length                                   ⊤                                      {𝑥, next (𝑥)}
            keys                                      ⊤                                      {𝑥, prev(𝑥)}
            hslist            last (𝑥) ≠ 𝑥 ∨ (last (𝑥) = 𝑥 ∧ hslist (𝑥) = {𝑥 })              {𝑥, prev(𝑥)}
                          Table 4. Full impact sets for lists for Circular List Insert Back




                                     Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:40                                                                           Adithya Murali, Cody Rivera, and P. Madhusudan


   We give the specification and program for Circular List Insert Back below.
 pre: Br = ∅ ∧ next (𝑥 ) = last (𝑥 )
 post: Br = ∅ ∧ next (𝑟𝑒𝑡 ) = last (𝑟𝑒𝑡 ) ∧ last (𝑟𝑒𝑡 ) = old (last (𝑥 ) )
       ∧ keys (last (𝑟𝑒𝑡 ) ) = old (keys (last (𝑥 ) ) ) ∪ {𝑘 } ∧ 𝑓 𝑟𝑒𝑠ℎ (hslist (last (𝑟𝑒𝑡 ) ) \ old (hslist (last (𝑥 ) ) ) )
 circular_list_insert_back(x: C, k: Int Br: Set(C))
 returns ret: C, Br: Set(C)
 {
   LCOutsideBr(x, Br);
   LCOutsideBr(x.next, Br);
   LCOutsideBr(x.prev, Br);

   var last: C = x.next;
   var node: C;
   NewObj(node, Br);
   Mut(node, key, k, Br);
   Mut(node, next, x.next, Br);
   Mut(x, next, node, Br);

   AddToLastHsList(last, node, Br);
   Mut(last, prev, node, Br);
   Mut(node, prev, x, Br);
   Mut(node, length, 1, Br);
   Mut(node, rev_length, 1 + node.prev.rev_length, Br);
   Mut(node, keys, {k}, Br);
   Mut(node, hslist, {node}, Br);
   Mut(node, last, node.prev.last, Br);
   AssertLCAndRemove(node, Br);

   ghost var cur: C = x;
   label PreLoop:
   while (cur ≠ last)
      invariant 𝑐𝑢𝑟 ≠ 𝑙𝑎𝑠𝑡 ⇒
              𝐵𝑟 = {𝑐𝑢𝑟, 𝑙𝑎𝑠𝑡 }
              ∧ 𝐿𝐶𝑀𝑖𝑛𝑢𝑠𝑁 𝑜𝑑𝑒 (𝑐𝑢𝑟, 𝑛𝑜𝑑𝑒 )
              ∧ last (𝑐𝑢𝑟 ) = 𝑙𝑎𝑠𝑡
              ∧ 𝐿𝐶𝐿𝑎𝑠𝑡 (𝑙𝑎𝑠𝑡, 𝑛𝑜𝑑𝑒 )
      invariant 𝑐𝑢𝑟 = 𝑙𝑎𝑠𝑡 ⇒ 𝐿𝐶𝑀𝑖𝑛𝑢𝑠𝑁 𝑜𝑑𝑒 (𝑐𝑢𝑟, 𝑛𝑜𝑑𝑒 )
      invariant 𝑛𝑜𝑑𝑒 ∈ hslist (next (𝑐𝑢𝑟 ) )
      invariant 𝑘 ∈ keys (next (𝑐𝑢𝑟 ) )
      invariant Unchanged@PreLoop(𝑛𝑜𝑑𝑒 )
      invariant Unchanged@PreLoop(𝑙𝑎𝑠𝑡 )
      invariant 𝐵𝑟 ⊆ {𝑐𝑢𝑟, 𝑙𝑎𝑠𝑡 }
      decreases rev_length(𝑐𝑢𝑟 )
   {
      if (cur.prev ≠ last) {
        LCOutsideBr(cur.prev, Br);
      }
      Mut(cur, length, cur.next.length + 1, Br);
      Mut(cur, hslist, cur.next.hslist + {node});
      Mut(cur, keys, cur.next.keys + {node.k});
      AssertLCAndRemove(cur, Br);
      cur := cur.prev;
   }

   LCOutsideBr(node, Br);
   Mut(cur, keys, cur.next.keys, Br);
   AssertLCAndRemove(cur, Br);


Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
Predictable Verification using Intrinsic Definitions                                                                         220:41


     AssertLCAndRemove(node, Br);

     ret := node;
 }




D.5     Merging Sorted Lists
We demonstrate the ability of intrinsic definitions to handle multiple data structures at once,
using the example of in-place merging of two sorted lists. The method merges the two lists by
reusing the two lists’ elements, which is a natural pattern for imperative code. Once again, we
extend the definition of sorted lists from Case Study 4.1. We add the predicates 𝑙𝑖𝑠𝑡1 : 𝐶 → 𝐵𝑜𝑜𝑙,
𝑙𝑖𝑠𝑡2 : 𝐶 → 𝐵𝑜𝑜𝑙, and 𝑙𝑖𝑠𝑡3 : 𝐶 → 𝐵𝑜𝑜𝑙, to indicate disjoint classes of lists. The relevant local
condition and impact sets are:




            (𝑙𝑖𝑠𝑡 1(𝑥 ) ∨ 𝑙𝑖𝑠𝑡 2(𝑥 ) ∨ 𝑙𝑖𝑠𝑡 3(𝑥 ) )
         ∧ ¬(𝑙𝑖𝑠𝑡 1(𝑥 ) ∧ 𝑙𝑖𝑠𝑡 2(𝑥 ) ) ∧ ¬(𝑙𝑖𝑠𝑡 2(𝑥 ) ∧ 𝑙𝑖𝑠𝑡 3(𝑥 ) )
                                                                                    Mutated Field 𝑓   Impacted Objects 𝐴 𝑓
         ∧ ¬(𝑙𝑖𝑠𝑡 1(𝑥 ) ∧ 𝑙𝑖𝑠𝑡 3(𝑥 ) )                                                  𝑙𝑖𝑠𝑡 1           {𝑥, prev (𝑥 ) }
         ∧ (𝑙𝑖𝑠𝑡 1(𝑥 ) ⇒ (next (𝑥 ) ≠ nil ⇒ 𝑙𝑖𝑠𝑡 1(next (𝑥 ) ) ) )                      𝑙𝑖𝑠𝑡 2           {𝑥, prev (𝑥 ) }
                                                                                        𝑙𝑖𝑠𝑡 3           {𝑥, prev (𝑥 ) }
         ∧ (𝑙𝑖𝑠𝑡 2(𝑥 ) ⇒ (next (𝑥 ) ≠ nil ⇒ 𝑙𝑖𝑠𝑡 2(next (𝑥 ) ) ) )
         ∧ (𝑙𝑖𝑠𝑡 3(𝑥 ) ⇒ (next (𝑥 ) ≠ nil ⇒ 𝑙𝑖𝑠𝑡 3(next (𝑥 ) ) ) )




   Disjointness of the three lists is ensured by insisting that every object has at most one of the
three list predicates hold.
   We give a gist of the proof of the merge method. The recursive program compares the keys at the
heads of the first and second sorted lists, and adds the appropriate node to the front of the third list.
It turns out that we can easily update the ghost maps for this node (making it belong to the third
list, and updating its parent pointer and key set) as well as updating the parent pointer of the head
of the list where the node is removed from. When one of the lists is empty, we append the third list
to the non-empty list using a single pointer mutation and then, using a ghost loop, we update the
nodes in the appended list to make 𝑙𝑖𝑠𝑡3 true (this needs a loop invariant involving the broken set).



We provide below the full local conditions and impact sets.


                                           Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
220:42                                                                Adithya Murali, Cody Rivera, and P. Madhusudan


         LC ≡ ∀𝑥 .(𝑙𝑖𝑠𝑡1(𝑥) ∨ 𝑙𝑖𝑠𝑡2(𝑥) ∨ 𝑙𝑖𝑠𝑡3(𝑥))
                   ∧ ¬(𝑙𝑖𝑠𝑡1(𝑥) ∧ 𝑙𝑖𝑠𝑡2(𝑥)) ∧ ¬(𝑙𝑖𝑠𝑡2(𝑥) ∧ 𝑙𝑖𝑠𝑡3(𝑥))
                   ∧ ¬(𝑙𝑖𝑠𝑡1(𝑥) ∧ 𝑙𝑖𝑠𝑡3(𝑥))
                   ∧ (prev(𝑥) ≠ nil ⇒ next (prev(𝑥)) = 𝑥)
                   ∧ (next (𝑥) ≠ nil ⇒ prev(next (𝑥)) = 𝑥
                                        ∧ length(𝑥) = length(next (𝑥)) + 1
                                        ∧ keys(𝑥) = keys(next (𝑥)) ∪ {key(𝑥)}                                    (3)
                                        ∧ hslist (𝑥) = hslist (next (𝑥)) ⊎ {𝑥 }         (disjoint union)
                                        ∧ key(𝑥) ≤ key(next (𝑥)))
                   ∧ (next (𝑥) = nil ⇒ length(𝑥) = 1 ∧ keys(𝑥) = {key(𝑥)} ∧ hslist (𝑥) = {𝑥 })
                   ∧ (𝑙𝑖𝑠𝑡1(𝑥) ⇒ (next (𝑥) ≠ nil ⇒ 𝑙𝑖𝑠𝑡1(next (𝑥))))
                   ∧ (𝑙𝑖𝑠𝑡2(𝑥) ⇒ (next (𝑥) ≠ nil ⇒ 𝑙𝑖𝑠𝑡2(next (𝑥))))
                   ∧ (𝑙𝑖𝑠𝑡3(𝑥) ⇒ (next (𝑥) ≠ nil ⇒ 𝑙𝑖𝑠𝑡3(next (𝑥))))

                           Fig. 13. Full local condition for lists for Sorted List Reverse


    Note that we also have a variation of the local condition 𝐿𝐶 𝑁𝐶 , used in ghost loop invari-
ants, which is similar to Equation 3, except the final three conjuncts (those enforcing closure on
𝑙𝑖𝑠𝑡1, 𝑙𝑖𝑠𝑡2, 𝑙𝑖𝑠𝑡3) are removed. This is done when converting an entire list from one class to another
(i.e., converting from 𝑙𝑖𝑠𝑡1 to 𝑙𝑖𝑠𝑡3). The following are the full impact sets for all fields of this data
structure.

                                    Mutated Field 𝑓       Impacted Objects 𝐴 𝑓
                                         next               {𝑥, old (next (𝑥))}
                                          key                 {𝑥, prev(𝑥)}
                                         prev               {𝑥, old (prev(𝑥))}
                                        length                {𝑥, prev(𝑥)}
                                         keys                 {𝑥, prev(𝑥)}
                                         hslist               {𝑥, prev(𝑥)}
                                         𝑙𝑖𝑠𝑡1                {𝑥, prev(𝑥)}
                                         𝑙𝑖𝑠𝑡2                {𝑥, prev(𝑥)}
                                         𝑙𝑖𝑠𝑡3                {𝑥, prev(𝑥)}

                                 Fig. 14. Full impact sets for disjoint sorted lists


Received 2023-11-16; accepted 2024-03-31




Proc. ACM Program. Lang., Vol. 8, No. PLDI, Article 220. Publication date: June 2024.
