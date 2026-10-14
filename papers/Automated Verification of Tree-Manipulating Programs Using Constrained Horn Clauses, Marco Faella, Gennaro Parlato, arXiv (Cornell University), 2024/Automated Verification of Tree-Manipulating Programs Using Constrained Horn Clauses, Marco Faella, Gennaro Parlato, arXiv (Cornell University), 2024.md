Automated Verification of Tree-Manipulating Programs
Using Constrained Horn Clauses
MARCO FAELLA, University of Naples Federico II, Italy
GENNARO PARLATO, University of Molise, Italy
Verifying programs that manipulate tree data structures often requires complex, ad-hoc proofs that are hard
to generalize and automate. This paper introduces an automatic technique for analyzing such programs.
Our approach combines automata and logics to tackle the challenges posed by diverse tree data structures
uniformly. At the core of our methodology is the knitted-tree encoding, which maps a program execution into
a tree data structure encapsulating input, output, and intermediate con!gurations, within a single structure.
By leveraging the compositional properties of knitted-trees, we characterize them using constrained Horn
clauses (CHCs). This encoding reduces veri!cation to solving CHC satis!ability, bene!ting from ongoing
advancements in CHC solvers. While we focus on the memory safety problem for illustration, our technique
applies broadly to various veri!cation tasks involving tree data structures.
ACM Reference Format:
Marco Faella and Gennaro Parlato. 2024. Automated Veri!cation of Tree-Manipulating Programs Using
Constrained Horn Clauses . 1, 1 (October 2024), 44 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

1    Introduction
Automated analysis of programs that manipulate dynamic memory (heaps) remains a challenging
problem in computer science, despite extensive research e"orts. A major obstacle is the unpre-
dictable nature of memory allocation and deallocation operations, which can make it hard to predict
the program’s state and the relationships between data elements over time. This unpredictabil-
ity can lead to a state-space explosion, rendering exhaustive analysis computationally infeasible.
Recursive procedures and unbounded loops introduce additional complexity, making reasoning
about termination intricate. Additionally, the use of expressive logics for specifying invariants,
preconditions, and postconditions adds another layer of complexity to the analysis task.
   This paper introduces a novel technique for automated analysis of heap-manipulating programs,
particularly those involving tree data structures. Our approach combines automata and logics to
address these challenges. Ultimately, we reduce the veri!cation to the satis!ability of constrained
Horn clauses (CHCs). This reduction allows us to capitalize on advancements in CHC solvers,
as demonstrated by the CHC-COMP competition [4, 17]. We illustrate our approach through its
application to the memory safety problem. A program is deemed memory safe if no execution
starting from a tree data structure that satis!es a given precondition (e.g., starting with a red-black
tree) leads to crashes (such as null-pointer dereferences, use after free, use of uninitialized memory,
and illegally freeing memory, as described in [32]) or results in non-termination.
   At the core of our methodology lies the knitted-tree encoding, which maps an execution 𝐿 of a
tree-manipulating program, starting from an input data tree 𝑀 , into a tree data structure called the
Authors’ Contact Information: Marco Faella, University of Naples Federico II, Italy, m.faella@unina.it; Gennaro Parlato,
University of Molise, Italy, gennaro.parlato@unimol.it.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
provided that copies are not made or distributed for pro!t or commercial advantage and that copies bear this notice and the
full citation on the !rst page. Copyrights for components of this work owned by others than the author(s) must be honored.
Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
prior speci!c permission and/or a fee. Request permissions from permissions@acm.org.
© 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM XXXX-XXXX/2024/10-ART
https://doi.org/10.1145/nnnnnnn.nnnnnnn


                                                                     , Vol. 1, No. 1, Article . Publication date: October 2024.
2                                                                        Marco Faella and Gennaro Parlato


knitted-tree of 𝐿. A knitted-tree uniquely encapsulates the input, output, and all intermediate
con!gurations of an execution within in a single structure. The underlying tree structure of the
knitted-tree, or backbone, is derived from 𝑀 by adding a !xed number of initially inactive nodes to
accommodate dynamic node allocation. Node labels consist in a sequence of records, called frames.
In turn, frames are connected in a linear tree-wide sequence, called the lace, with consecutive
frames belonging to the same node or to adjacent nodes of the tree, mimicking the knitting of a
tree-shaped object. Each frame records changes to the node, including variables pointing to it, and
the current program state, serving as a log of updates. This approach retains the original structure
of the backbone while also representing the !nal heap, which may have a di"erent graph structure.
However, the parameters de!ning a knitted-tree – namely, the number of spare nodes added to the
backbone and the number of frames in a node label – may not su#ce to encompass all possible
program executions, potentially leading to missed executions in our analysis.
   Knitted-trees enjoy compositional properties that are essential for our veri!cation approach
using CHCs. Knitted-trees allow subtree replacement: we can substitute a subtree rooted at node 𝑁
in knitted-tree 𝑀 with a subtree from another knitted-tree rooted at 𝑁 →, provided that the labels of 𝑁
and 𝑁 → satisfy an entirely local consistency property. Moreover, such consistency can be expressed
in a quanti!er-free !rst-order data theory. Using this replacement rule, we construct a CHC system
whose minimal model precisely captures the set of valid node labels for the knitted-trees of a
given program. This enables us to e#ciently check for error con!gurations reachable along an
execution. If our analysis does not !nd an error, we need an additional check to ensure the program’s
correctness. With a small change, the same CHC system can be used to verify if there are executions
that cannot be represented using the current parameter values. In that case, we increment the
parameters to capture more executions. As expected from the undecidability of the veri!cation
task, this process can potentially run inde!nitely.
   We can analyze a program under a given precondition, provided that the precondition can
be expressed as a Symbolic Data-Tree Automata (S!"#s) [23]. S!"#s work bottom-up, starting at
data tree leaves, using a tuple of state variables to represent the automaton’s state and a separate
set of variables for the alphabet. Transitions are de!ned as constraints in a joint multi-sorted
!rst-order theory over the state and alphabet variables. S!"#s can characterize many common tree
data structures, like binary-search trees (B$"), red-black trees (R%"), AVL trees, and heaps [23].
Higher-level logic formalisms, like Monadic Second-Order logic with Data (M$&’D) [23], can naturally
specify data tree properties and be translated into S!"#s. We chose S!"#s for their simplicity, which
allows us to easily impose constraints on input tree data structures by constraining the backbone
of the knitted-trees that naturally encode the input data trees. We use a construction similar to the
cross-product construction for !nite state automata. This construction can be naturally encoded by
extending the system of CHCs characterizing the set of node labels of knitted-trees.
   Our method also o"ers a unique approach to proving program termination. In knitted-trees, we
attach at least one frame to a node for every instruction executed by the program. By limiting the
number of frames per node, we can conclude that a program terminates for all inputs meeting
the precondition if no knitted-tree exceeds the allowed number of frames at any node. While
this condition might seem ad hoc, it applies to many procedures operating on well-known data
structures, making our approach valuable for proving termination in many relevant cases.
   Finally, we have implemented our approach in a prototype tool and used it to check the memory
safety of some procedures involving well-known tree data structures. This demonstrates its practical
feasibility in both producing proofs and discovering bugs. Additionally, we discuss how the proposed
approach can be extended and generalized to verify more complex properties.



, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                       3


Organization of the paper. §2 covers basic notation and de!nitions including data trees and a
generalization of S!"#s in §2.1, and CHCs in §2.2. §3 introduces a simple programming language for
heap-manipulating programs and de!nes the memory safety problem. §4 de!nes the knitted-tree
encoding, and its compositionality properties are detailed in §5. §6 describes our reduction to the
CHC satis!ability problem, with program preconditions addressed in §7. § 8 presents a sound
procedure for solving the memory safety problem. §9 demonstrates our approach’s practicality,
including our prototype implementation, optimizations, and experimental results. In §10, we discuss
how to address other program properties using the framework presented in this paper. We discuss
related work in §11 and conclude in §12, exploring potential future work and applications.

2     Preliminaries
This section outlines the basic notation and de!nitions used in the paper, including data trees and
a generalization of S!"#s in §2.1, and CHCs in §2.2.
   We denote the set of natural numbers by N. For 𝑂, 𝑃 ↑ N with 𝑂 ↓ 𝑃, we denote by [𝑂, 𝑃] the set of
integers 𝑄 such that 𝑂 ↓ 𝑄 ↓ 𝑃. Also, we denote by [ 𝑃] the set [1, 𝑃]. We use the standard syntax
and semantics for !rst-order logic (FOL) with equality [48]. Our framework includes formulas
from a many-sorted quanti!er-free !rst-order theory D, encompassing various data types found
in programs such as arithmetic, reals, and arrays. Hereafter, we refer to D as the data theory.

2.1     Data-Trees and Symbolic Data-Tree Automata
This section introduces data trees and symbolic data tree automata (S!"#s), which represent and
characterize well-known tree data structures [23].
Trees. A 𝑄-ary tree 𝑀 is a !nite, pre!x-closed subset of [𝑄] ↔ , where 𝑄 ↑ N. Each element in 𝑀 is a
node, with the empty string 𝑅 as the root. The tree has an implicit edge relation: for any 𝑆 ↑ [𝑄],
if both v and v.d are nodes in 𝑀 , then (v, v.d) is an edge, making v.d the 𝑆 th child of v, and v the
parent of v.d. Nodes without children are leaves, while those with children are internal nodes.
Data signatures. A data signature S is a collection of pairs {id𝐿 : type𝐿 }𝐿 ↑ [𝑀] , where each id𝐿 is a
!eld name and type𝐿 is its data type (e.g., integers, $oating point numbers, real numbers, Booleans
B, and !xed-length bit vectors). An evaluation 𝑇 of S maps each !eld name id to its type-speci!c
value, denoted 𝑇.id. The set of all evaluations, or the language of S, is 𝑈(S).
Data-Trees. A data-tree with data signature S, or S-tree, is a pair (𝑀 , 𝑉) where 𝑀 is a tree and 𝑉 is
a labeling function 𝑉 : 𝑀 ↗ 𝑈(S) that assigns an evaluation of S to each node 𝑊 ↑ 𝑀 . To simplify
notation, the value of a !eld id at node 𝑊 can be written as 𝑊 .id when 𝑉 is clear from the context.
Symbolic Data-Tree Automata. Symbolic data-tree automata (S!"#s) extend traditional bottom-
up !nite tree automata for data trees. They use symbolic alphabets and states, de!ned by data
signatures, with a transition function as a predicate from a many-sorted, quanti!er-free !rst-order
logic theory. Originally de!ned for binary trees [23], we extend S!"#s to 𝑄-ary trees.

    De!nition 2.1. A 𝑄-ary symbolic data-tree automaton A is a tuple (S ω, S𝑁 ,𝑋,𝑋 𝑂 ) where:
      • S ω is the alphabet data signature de!ning the tree alphabet ω = 𝑈(S ω );
      • S𝑁 is the state data signature de!ning the set of states 𝑌 = 𝑈(S𝑁 ); 𝑌 is extended to include
        nil for missing child nodes, forming 𝑌            ! = 𝑌 ↘ {nil}.
                                                                                                              ! 𝑍 ranges
      • 𝑋 (𝑍 1, 𝑍 2, . . . , 𝑍𝑃 , key, 𝑍) is the transition constraint, where 𝑍 1, 𝑍 2, . . . , 𝑍𝑃 range over 𝑌,
        over 𝑌, and key is of type S ω ;
      • 𝑋 𝑂 is a unary constraint de!ning the set of !nal states 𝑎 ≃ 𝑌,               ! i.e., the set consisting of all
        elements 𝑍 ↑ 𝑌 such that 𝑋 (𝑍) evaluates to true.
                                               𝑂


                                                                  , Vol. 1, No. 1, Article . Publication date: October 2024.
4                                                                                      Marco Faella and Gennaro Parlato


   For a "𝑄-ary S ω -tree T = (𝑀 , 𝑉),      # a run of A on T is a function 𝑏 : 𝑀 ↗ 𝑌 such that for all nodes
𝑊 ↑ 𝑀 , 𝑋 𝑍 1, 𝑍 2, . . . , 𝑍𝑃 , 𝑉(𝑊), 𝑏 (𝑊) holds, where 𝑍 𝑄 is 𝑏 (t.j) if t.j ↑ 𝑀 , otherwise nil." (𝑀 , 𝑉)
                                                                                                           # is accepted
by A if 𝑀 = ⇐ and 𝑋 𝑂 (nil) is true, or if there exists a run 𝑏 : 𝑀 ↗ 𝑌 such that 𝑋 𝑂 𝑏 (𝑅) is true. The
language of A, denoted 𝑈(A), is the set of all accepted S ω -trees.                                                    ↭

2.2    Constrained Horn Clauses
This section introduces the notation and de!nitions of constrained Horn clauses, or CHCs.
  De!nition 2.2. For a set 𝑐 of uninterpreted !xed-arity relation symbols representing the system’s
unknowns, a constrained Horn clause is a formula of the form 𝑑 ⇒ 𝑒 ⇑ 𝑓 1 ⇑ · · · ⇑ 𝑓𝑀 where:
    • 𝑒 is a constraint represented by a quanti!er-free formula of the data theory D that does not
      contain any relation symbol from 𝑐;
    • for every 𝑂 ↑ [𝑔], 𝑓𝐿 is an application 𝑕 (𝑁 1, . . . , 𝑁𝑃 ) of a relation symbol 𝑕 ↑ 𝑐 to !rst-order
      variables 𝑁 1, . . . , 𝑁𝑃 ;
    • 𝑑 is the clause head and is either false, or it is an application 𝑕 (𝑁 1, . . . , 𝑁𝑃 ) of a relation symbol
      𝑕 ↑ 𝑐 to the !rst-order variables 𝑁 1, . . . , 𝑁𝑃 .
A CHC is a fact if its body has only the 𝑒 component, and it is a query if its head is false. A !nite set
C of CHCs is called a system, corresponding to the !rst-order formula obtained by conjoining all its
CHCs, with all free variables universally quanti!ed. We assume that the semantics of constraints is
given a priori as a structure.                                                                                 ↭
   A CHC system S with relation symbols 𝑐 is satis!able if there exists an interpretation for
each relation symbol in 𝑐 that makes all clauses in S valid. The CHC satis!ability problem is the
computational task of determining whether a given system S of CHCs is satis!able.
   Every system of CHCs S has a unique minimal model w.r.t. the subset ordering,1 computable as
the !xed-point of an operator derived from the clauses of S [37, 66]. This !xed-point semantics
justi!es the correctness of the reductions in this paper.

3     Heap-manipulating Programs and the Memory Safety Problem
This section introduces a simple programming language with specialized heap manipulation
functionality and de!nes the memory safety problem for such programs.
  The heap is a fundamental data structure for dynamic memory allocation, allowing memory
blocks (or nodes) to be allocated and deallocated during program execution. These nodes typically
have a data !eld and pointer !elds linking them. Formally, a speci!c heap state, is de!ned as follows.
    De!nition 3.1. A heap is a tuple H = (S, 𝑖 , data, PF) where
     • S is a data signature de!ning the type of data that can be stored in a node.
     • 𝑖 is a !nite set of nodes, including a unique element nil representing unallocated memory.
     • data : (𝑖 ↘ {nil}) ↗ 𝑈(S) assigns a data signature evaluation of S to each node 𝑗 ↑ 𝑖 ,
       except for nil. modeling the data !eld of each node.
     • PF is a !nite sequence of distinct named pointer !elds representing the pointer !elds of each
       node: each pointer !eld is a function mapping nodes except nil to another heap node, i.e., of
       type (𝑖 \ {nil}) ↗ 𝑖 .                                                                      ↭
Syntax. Our programming language syntax is shown in Fig. 1a. A program begins with declarations
of pointer and data variables, followed by a !nite sequence of labeled instructions. Pointer variables
can point to heap nodes, or nil, and data variables store values within their data type range.
Instructions include assignments, control $ow, and heap operations. Data assignments are of the
1 See [66] for logic programs and Proposition 4.1 in [37] for constrained logic programs, equivalent to CHCs.



, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                                 5



                                                                                                    pointer root, p, p→
                           def
                Program = decl pc _stmt +                                                           int key, value
                           def
                      decl = (pointer id (,id) ↔ ) ↔ (type id (,id) ↔ ) ↔                     0 : p→ ω root ;
                           def
                  pc _stmt = pc : stmt ;                                                      1 : while (p→ ε nil) do
                           def                                                                2:         value ω p→ ↗ data ;
                     stmt = ctrl _stmt | heap_stmt
                                                                                              3:         p ω p→ ;
                           def
                 ctrl _stmt = 𝑅 ω exp | 𝑅 bool ω heap_cond | skip | exit                      4:         if (key ↓ value) then
                                 | if cond then pc _stmt + else pc _stmt + !                  5:              p→ ω p→ ↗ le” ;
                                 | while cond do pc _stmt + od                                           else
                           def
               heap_stmt = new 𝑆 | free 𝑆                                                     6:              p→ ω p→ ↗ right ;
                                 | 𝑆 ω nil | 𝑆 ω 𝑇 | 𝑆 ω q ↗ p!eld                                       !;
                                 | p ↗ p!eld ω nil | p ↗ p!eld ω 𝑇                                  od ;
                                 | p ↗ data ω exp | 𝑅 ω p ↗ data                              7 : new p→ ;
                           def                                                                8 : p→ ↗ data ω key ;
                      exp = 𝑅 | 𝑈 (exp, . . . , exp)
                                                                                              9 : if (root = nil) then
                           def
                     cond = 𝑉 (exp, . . . , exp) | (¬)? heap_cond
                                                                                             10 :        root ω p→ ;
                           def
               heap_cond = 𝑆 = 𝑇 | 𝑆 = nil                                                          else
                                 | p ↗ p!eld = 𝑇 | p ↗ p!eld = nil                           11 :        if (key ↓ value) then
                                                                                             12 :             p ↗ le” ω p→ ;
                                                                                                         else
        (a) Syntax of a basic programming language over a heap
        signature. p!eld is the name of one of the pointer fields (i.e.,                     13 :             p ↗ right ω p→ ;
        one of the functions in PF). 𝑘 and 𝑍 are variables of type                                       !;
        pointer; 𝑆 is a variable of data type; 𝑙 is a function symbol                               !;
        from the data theory and 𝑕 is a relation symbol from the                             14 : exit ;
        data theory; 𝑘𝑚 is the instruction counter; type is one of the
        sorts from the underlying data theory.
                                                                                                 (b) B$" I($)*"+&(.


                   Fig. 1. Basic programming language for heap-manipulating programs.



form 𝑆 ω exp, where 𝑆 is a data variable set to the value of the data expression exp. Data expressions
are constructed from data variables and combined using function symbols of the data theory D.
Control $ow instructions include skip, exit, conditionals (if-then-else), and loops (while). Boolean
conditions (cond) are either data conditions or heap conditions, not both simultaneously, though
this can be managed by introducing Boolean variables for each condition. Heap conditions can be
assigned to a Boolean variable with 𝑆 bool ω heap_cond, integrating them into Boolean theory. Heap
operations include creating a new node with new 𝑘 (assigning 𝑘 to the new node and initializing
its !elds to unde!ned values or nil) and deallocating a node with free 𝑘 (setting all pointers to the
node to nil). We also allow assignment and retrieval of values from node !elds.
Handling recursion: Our language lacks direct support for function calls. We can handle non-
recursive procedure calls by inlining its code at call points. We can also handle recursive functions,
such as those used for manipulating tree data structures. These functions typically operate on a
single node at a time, recursively calling themselves on the children of that node. To simulate this
type of recursion, we can add a pointer !eld to each node that points to the node from which the
current function call was made, allowing navigation back to the previous node.

                                                                            , Vol. 1, No. 1, Article . Publication date: October 2024.
6                                                                          Marco Faella and Gennaro Parlato


   A program 𝑛 is valid if it is well-formed, type-correct, has unique labels for each statement, and
ends with an exit statement. Fig. 1b shows a program that inserts the value stored in key into a
binary search tree (B$"). In 𝑛, PC 𝑊 , PV𝑊 , and DV 𝑊 are sets of program counters, pointer variables,
and data variables, respectively. The function succ : PC 𝑊 𝐿 PC 𝑊 determines the successor of a
program counter, if one exists. The exit statement has no successor, while control-$ow statements
have two successors based on a Boolean condition, denoted as succ(pc, true) and succ(pc, false).
Semantics. A program 𝑛 operates on a specialized heap called a 𝑛-heap, containing all the pointers
and all the data and pointer !elds in 𝑛. A con!guration of 𝑛 is a tuple (H, 𝑇 𝑆 , 𝑇𝑅 , pc) consisting of a
𝑛-heap, an evaluation of the pointer variables in 𝑛, an evaluation of the data variables in 𝑛, and a
label indicating the next instruction to be executed. Since we focus on programs operating on tree
data structures, a con!guration 𝑚 is an initial con!guration when satis!es the following conditions:
     • H is isomorphic to a data tree T via a bijection 𝑏 that maps each node in H to a node in T ,
       such that for all nodes 𝑜, 𝑝 in H and 𝑂 ↑ |PF |, 𝑝 = pfi (𝑜) i" 𝑏 (𝑝) = 𝑏 (𝑜).𝑂, where pfi is the
       𝑂-th pointer !eld in PF. We refer to T as the data tree of 𝑚, and may use T in place of H .
     • 𝑇 𝑆 maps the !rst pointer variable declared in 𝑛 to the H node corresponding to the root of
        T and maps the other pointer variables to nil.
     • 𝑇𝑅 assigns each variable a non-deterministic value.
     • pc is the label of the !rst statement in 𝑛.
   A transition in 𝑛 from con!guration 𝑚 to 𝑚 →, denoted 𝑚 ↗𝑊 𝑚 →, occurs when the instruction at pc is
executed, following standard instruction semantics unless noted otherwise. If pc corresponds to an
exit statement, 𝑚 is a !nal con!guration, with no further transitions. If a nil pointer is dereferenced
or used for node deallocation, the transition does not occur, making 𝑚 an error con!guration. An
execution 𝐿 of 𝑛 is a potentially in!nite sequence of con!gurations 𝑚 0𝑚 1 . . . of 𝑛, where: (i) 𝑚 0 is
initial, and (ii) 𝑚𝐿⇓1 ↗𝑊 𝑚𝐿 is valid for each con!guration index 𝑂 ↑ N. A !nite 𝐿 ending in a !nal or
error con!guration is a terminating or buggy execution. 𝐿 complies with a precondition given by an
S!"# Apre if a data tree T0 isomorphic to the 𝑛-heap in 𝑚 0 , belongs to the language of Apre .
Memory safety problem. A program 𝑛 is memory safe with respect to a precondition Apre if all
its executions complying with Apre are terminating, meaning no execution is or end in an error
con!guration. The memory safety problem asks whether 𝑛 is memory safe with respect to a given
precondition Apre . It is simple to prove that the memory safety problem is undecidable.

4     Kni!ed-trees: a data tree representation of executions
Our procedure for solving the memory safety problem is based on the knitted-tree encoding, which
we present in this section. The knitted-tree encoding represents each program execution as a
data tree, capturing input, output, and intermediate con!gurations, facilitating the veri!cation of
preconditions, (postconditions,) and other speci!cations of interest within a uni!ed structure.
   Before describing the encoding, we introduce the necessary notation and review the assumptions
and parameters involved. The encoding uses two parameters, 𝑞, 𝑔 ↑ N, which will be explained
later. Assume 𝐿 is an execution of 𝑛 starting from an initial con!guration 𝑚 0 , where T = (𝑀 , 𝑉) is a
𝑄-ary data tree of 𝑚 0 with signature S = {key : D}, and 𝑘! points to the root of T in 𝑚 0 . The encoding
maps 𝐿 to a data tree K = (𝑟, 𝑠), called the (𝑞, 𝑔)-knitted-tree of 𝐿. For technical reasons, we adopt
a non-deterministic encoding, meaning that an execution 𝐿 can lead to a set of (𝑞, 𝑔)-knitted-trees,
denoted by kt (𝐿, 𝑞, 𝑔). The rationale behind this non-deterministic approach is detailed in §4.3.
We now describe a generic knitted-tree K = (𝑟, 𝑠) from the set kt (𝐿, 𝑞, 𝑔).

4.1    The backbone
The tree 𝑟, also called the backbone of K, is the smallest tree satisfying the following conditions:

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                   7


   (1) The input tree 𝑀 is a subset of 𝑟 (𝑀 ⇔ 𝑟).
   (2) All nodes from 𝑀 are internal nodes in 𝑟.
   (3) The degree of all internal nodes in 𝑟 is 𝑄 + 𝑞.
   (4) There is at least one internal node.
Note that, in the special case where 𝑀 is empty, the backbone 𝑟 is a full tree of height 2, consisting
of a root and its 𝑄 + 𝑞 children. Fig. 2 illustrates a backbone structure.

                                                                           𝑅
                 𝑅
                                               1                           2                             3
      1                     2
                                        11     12    13            21     22      23
            12         21
                     (a)                 121   122   123    211    212   213

                                                                                                        (b)

Fig. 2. Example of backbone: Part (b) illustrates a backbone derived from the input tree displayed in Part
(a). Here, we assume 𝑄 = 2 and 𝑞 = 1.

   Intuitively, each node in 𝑟 represents a distinct heap node. Initially, all nodes in 𝑀 are active,
while the remaining nodes are inactive (dotted in Fig. 2). When an active node is freed using the
free instruction, it transitions into an inactive state, as explained later in this section.

4.2   The node log
The backbone of a knitted-tree is determined solely by the input data tree and the parameters 𝑞 and
𝑔, regardless of the execution it represents. We now annotate the backbone to track modi!cations
to the input data tree along 𝐿 by labeling the nodes. Each node is equipped with a sequence of
frames, called the log of the node. Each frame typically documents a speci!c modi!cation related
to the node, such as altering the data it contains or changing one of its pointer !elds, or assigning
that node to a pointer variable. To establish connections between nodes and create a chronological
record of updates, we organize the frames into a doubly linked list that enables us to navigate
the execution in both directions. Additionally, if two frames correspond to consecutive operations
located in di"erent nodes, we add frames to the nodes along the path that connects two nodes in the
backbone. Frames also contain information about the ongoing program state. The data signature
SK of the knitted-tree K speci!es the structure of each node’s log in K, as illustrated in Figure 3.
   A log is a sequence of 𝑔 + 1 frames, each identi!ed by its index 𝑂. Frames within the same node
are sorted temporally by index. Once a speci!c frame 𝑙 of a log 𝑡 is identi!ed and named, we omit
its index 𝑂 when referring to its !elds (e.g., 𝑙 .pc instead of 𝑡.pc𝐿 ). The last frame within each label
handles label over"ow, which occurs when more than 𝑔 frames are needed in a node, requiring the
program to use the (𝑔 + 1) th frame. The prev !eld holds a value from Dir ↖ [𝑔], not Dir ↖ [𝑔 + 1],
since a frame with index 𝑔 + 1 has no successor. The instr !eld of a frame contains the events, also
referred to as symbolic instructions, which are categorized as follows:
                  $                                                                     %
          Instr = ↙p!eld ω 𝑘∝, ↙p!eld ω nil∝, ↙𝑘 ω here∝ | p!eld ↑ PF, 𝑘 ↑ PV𝑊
                      $               % $                                %    $              %
                   ↘ *,!𝐿 | 𝑂 ↑ [𝑔] ↘ *,!𝐿,𝑆 | 𝑂 ↑ [𝑔], 𝑘 ↑ PV𝑊 ↘ (&-, )**, &&. .

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
8                                                                                    Marco Faella and Gennaro Parlato


              &
          SK = avail𝐿 : B,                           Is this frame available?
                    active𝐿 : B,                     Is this node allocated?
                    key : D,
                          𝐿
                                                     Current value of this node’s data !eld
                    pc : PC 𝑊 ,
                      𝐿
                                                     Program counter
                    {𝑆 𝐿 : D𝑅 }𝑅 ↑DV 𝐿 ,             Current value of the data variables
                    {upd𝐿𝑆 : B}𝑆 ↑PV𝐿 ,              Has 𝑘 been updated since the frame 𝑂 ⇓ 1?
                    {isnil𝐿𝑆 : B}𝑆 ↑PV𝐿 ,            Is 𝑘 nil?
                    instr : Instr,
                         𝐿
                                                     Symbolic instruction
                    active_child : B
                                   𝐿      𝑃+𝑋
                                                     Is each child allocated?
                    next𝐿 : Dir ↖ [2, 𝑔 + 1],        Link to the next frame
                                                                                                   '
                    prev : Dir ↖ [2, 𝑔]
                              𝐿
                                                     Link to the previous frame                                    ,
                                                                                                       𝐿 ↑ [𝑀+1]
    where Dir = {→, ′} ↘ [𝑄 + 𝑞] encodes the position of an adjacent frame relative to the frame node.


                                       Fig. 3. Data signature SK of the kni!ed-tree K.


The !rst group of events logs refers to changes in the node’s pointer !elds, maintaining a chronolog-
ical record of the pointer variables referencing the node. The events *,!𝐿 and *,!𝐿,𝑆 represent a
lace rewinding operation, crucial for the sequencing node updates. Other symbols include: an empty
instruction ((&-), a null-pointer dereference ()**), and an out-of-memory error (&&.) resulting
from excessive use of the statement new. Detailed explanations of these events will follow.

4.3    The labeling function
The labeling function 𝑠 of K is de!ned inductively on the length of 𝐿.
4.3.1 Base case. 𝐿 consists of an initial con!guration, say (T , 𝑇 𝑆 , 𝑇𝑅 , pc). We encode the input
tree T = (𝑀 , 𝑉) into the backbone by setting the !rst frame of each node 𝑊 ↑ 𝑟 as follows:
                                                                             (
                  1                                                     1      true if 𝑊 ↑ 𝑀
      𝑠 (𝑊).avail = false,                                  𝑠 (𝑊).active =
                                                                               false otherwise
                      (                                                      (
                        𝑉(𝑊).key    if 𝑊 ↑ 𝑀                                   true if 𝑊 .𝑃 ↑ 𝑀
        𝑠 (𝑊).key 1 =                                𝑠 (𝑊).active_child 1𝑄 =
                        unspeci!ed otherwise                                   false otherwise.
The other !elds of the !rst frame are unspeci!ed (i.e., they assume all possible values in di"erent
knitted-trees). The initial con!guration of 𝐿 is stored in the root’s second frame: 𝑠 (𝑅).avail 2 = false,
𝑠 (𝑅).prev 2 = (→, 2) (a self-loop), 𝑠 (𝑅).pc 2 is set to the !rst statement’s label in 𝑛, and 𝑠 (𝑅).isnil𝑇2 =
true for all pointer variables 𝑍 di"erent from 𝑘!. If 𝑀 is not empty, 𝑠 (𝑅).instr 2 = ↙!        𝑘 ω here∝ and
𝑠 (𝑅).isnil 𝑆2! = false; otherwise, 𝑠 (𝑅).instr 2 = (&- and 𝑠 (𝑅).isnil 𝑆2! = true. All remaining frames in all
nodes are labeled as available. The !elds active, key, and active_child of the second frame of the
root are copied from the root’s !rst frame.
4.3.2 Inductive case. We start with an overview of the encoding method, its properties, and the
required notation. Let 𝐿 = 𝐿𝑚, where 𝑚 is a con!guration and 𝐿 is a non-empty execution. Assume
that K = (𝑟, 𝑠) is a knitted-tree in kt (𝐿, 𝑞, 𝑔). We de!ne the labeling 𝑠 for 𝐿 by extending the lace

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                   9


of K based on the last instruction executed in 𝐿. To aid understanding, we list some invariants for
all knitted-trees, providing an informal explanation for brevity.
The lace. Besides individual node logs, we maintain a chronological order of all frames across all
nodes to track the execution sequence of 𝐿. All the unavailable frames in the knitted-tree with
index greater than 1 form a doubly linked list called the lace using the next and prev !elds of the
frames. The !rst frame in the lace is the root’s second frame. We identify a frame in a knitted-tree
by a pair (𝑗, 𝑂), where 𝑗 is a node and 𝑂 ↑ [𝑔 + 1] is the frame’s index. We say that frame (𝑁, 𝑃) is the
lace successor of frame (𝑗, 𝑂) and write (𝑗, 𝑂) ↗next (𝑁, 𝑃) (and (𝑗, 𝑂) is the lace predecessor of (𝑁, 𝑃),
written (𝑁, 𝑃) ↗prev (𝑗, 𝑂)) if 𝑂, 𝑃 > 1 and one of the following cases holds:
     • 𝑗 = 𝑁, 𝑃 = 𝑂 + 1, 𝑠 (𝑗).next𝐿 = (→, 𝑃), and 𝑠 (𝑁).prev 𝑄 = (→, 𝑂);
     • 𝑁 is the 𝑢 th child of 𝑗, 𝑠 (𝑗).next𝐿 = (𝑢, 𝑃), and 𝑠 (𝑁).prev 𝑄 = (′, 𝑂);
     • 𝑗 is the 𝑢 th child of 𝑁, 𝑠 (𝑗).next𝐿 = (′, 𝑃), and 𝑠 (𝑁).prev 𝑄 = (𝑢, 𝑂).
Available frames’ unspeci!ed !elds contribute to kt (𝐿, 𝑞, 𝑔)’s non-determinism.
Properties of the frame !elds. In our inductive de!nition, we extend the knitted-tree for 𝐿 from one
de!ned for 𝐿 by appending frames to the nodes’ logs based on 𝐿’s last transition. This helps us
assign meanings to !elds like upd 𝑆 , isnil 𝑆 , 𝑆, key, pc, and active_child for the unavailable frames.
The upd 𝑆 $ag tracks changes to the pointer 𝑘 outside the current node: it is set to true in frame
(𝑗, 𝑂) (for 𝑂 > 1) if 𝑘 was assigned a non-nil value in the part of the lace between frames (𝑗, 𝑂 ⇓ 1)
and (𝑗, 𝑂), excluding these frames. Thus, if frames (𝑗, 𝑂 ⇓ 1) and (𝑗, 𝑂) are adjacent in the lace (i.e.,
(𝑗, 𝑂 ⇓ 1) ↗next (𝑗, 𝑂), aka a local step), all upd 𝑆 $ags in (𝑗, 𝑂) are false. The isnil 𝑆 $ag is true in a
frame if 𝑘 equals nil at that point in the execution. The active_child $ags help track the allocation of
the child nodes of the backbone. Other !elds maintain their original meanings in the con!guration.
Pushing a frame. Appending a frame to a log involves: (1) !nding the smallest index 𝑂 where avail𝐿
is true, and (2) adding the new frame at position 𝑂. Therefore, a log operates akin to a stack, with
the bottom frame at index 1 and the top frame being the highest-index frame where avail is false.
Default values for a frame. Any frame pushed onto a log assumes default values unless speci!ed
otherwise. When pushing a frame 𝑙 on a node 𝑗, default values come from the preceding frame in
the lace, 𝑙 prev , and the frame below 𝑙 in 𝑗’s log, 𝑙 below . Note that 𝑙 prev and 𝑙 below can be the same.
The default values for the !elds of 𝑙 are as follows: for all 𝑘 ↑ PV𝑊 and 𝑆 ↑ DV 𝑊 ,
     • avail = false, instr = (&-, and upd 𝑆 = false;
     • active and key are copied from 𝑙 below ;
     • isnil 𝑆 , 𝑆, and pc are copied from 𝑙 prev ;
     • active_child 𝑄 is copied from 𝑙 prev .active if 𝑙 prev belongs to the 𝑃 th child of 𝑗; otherwise, it is
        copied from 𝑙 below .active_child 𝑄 ;
     • prev points to 𝑙 prev ;
     • next is unspeci!ed and can take any value in di"erent knitted-trees for the same execution.
Moreover, 𝑙 prev .next is updated to point to 𝑙 . This resolves the non-determinism left in the next
!eld of the previous frame, in such a way that it points to the newly added frame.
   Despite the non-determinism in the next !eld, identifying the last frame 𝑙 in a lace can be done
by checking 𝑙 and its lace successor 𝑙 →. Speci!cally, 𝑙 is the last frame of the lace if 𝑙 → is available
or 𝑙 → precedes 𝑙 in the lace, which happens when !eld of 𝑙 → .prev does not point to 𝑙 .
    Henceforth, we assume that 𝑙 is the last frame of the lace in K located as top frame of node 𝑊.
    Instructions are classi!ed as either local or walking. Local instructions only use information from
𝑙 , and push a single new frame 𝑙 onto 𝑊. The !elds of 𝑙 are set to default values, except for those
speci!ed below. The following cases correspond to the instruction pointed to by 𝑙 .pc:

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
10                                                                                       Marco Faella and Gennaro Parlato


Encoding of 𝑘 ω nil: 𝑙 .pc = succ(𝑙 .pc) and 𝑙 .isnil 𝑆 = true.
Encoding of 𝑆 ω exp: 𝑙 .pc = succ(𝑙 .pc) and 𝑙 .𝑆 is set to the value of exp, with variables in DV 𝑊
evaluated using their values from 𝑙 .
Encoding of skip: 𝑙 .pc = succ(𝑙 .pc).
   Non-local or walking instructions may access di"erent nodes in addition to 𝑊. The main reasons
to move to another node are to dereference a pointer or identify the node a pointer !eld refers to.
To get this information, we rewind the lace by moving backward to !nd the most recent assignment
to the relevant pointer variable. For example, to identify the node a pointer variable 𝑘 points to, we
rewind the lace until we !nd a frame with the symbolic instruction ↙𝑘 ! here∝.
Lace rewinding path. To de!ne the process of rewinding the lace of K, we introduce an auxiliary
function called !nd_ptr (𝑘, id). This function takes two parameters: a pointer variable 𝑘 ↑ PV𝑊 , and
a frame identi!er id = (𝑗, 𝑂). It returns a sequence of frame ids by tracing the lace backward from
id, using optimizations to take shortcuts when possible. Instead of following the lace step-by-step,
we move backward in the lace only if we are sure to !nd an update to 𝑘 before returning to the
current node. We use the upd 𝑆 $ag in the current frame to check this: if true, we go backward,
otherwise, we take a shortcut by moving down in the log. Speci!cally, we jump directly to the
topmost frame with upd 𝑆 = true, considering it in the next step. If no such a frame exists, we jump
to the frame in position 2 of the current log (the frame in position 1 is special and is not part of the
lace). Formally, !nd_ptr (𝑘, id) is the sequence of frame ids id 1, . . . , id𝑌 where id 𝑄 = (𝑗 𝑄 , 𝑂 𝑄 ) for all
                                                                                               𝐿
𝑃 ↑ [𝑢], such that: (i) id 1 = id; (ii) for all 𝑃 ↑ [𝑢 ⇓ 1], id 𝑄 ↗prev id 𝑄+1 if 𝑠 (𝑗 𝑄 ).upd 𝑆𝑀 = true, otherwise
𝑗 𝑄+1 = 𝑗 𝑄 and 𝑂 𝑄+1 is the maximum value between 2 and the greatest index less than 𝑂 𝑄 such that
             𝐿
𝑠 (𝑗 𝑄 ).upd 𝑆𝑀 +1 = true; (iii) the frame with id id𝑌 contains the symbolic assignment ↙𝑘 ω here∝; and
(iv) all previous frames do not contain symbolic assignments to 𝑘.
   Example 4.1. We illustrate the rewinding operation with an example. Consider the fragment
of knitted-tree in Fig. 4, showing node 𝑗 and its children 𝑁 1 and 𝑁 2 . Each node displays a small
selection of the information contained within each frame. Gray numbers above the frames indicate
label positions, while numbers inside the frames represent lace positions (ordinals). The lace starts
at the frame with ordinal 1 of the root (node 𝑗), takes a local step to the frame with ordinal 2, then
moves to the left child 𝑁 1 , and so on. Suppose that the program counter in the 7th frame points to
the statement 𝑘 ω 𝑍, that dereferences pointer 𝑍. Using 7 as a shorthand for the frame (𝑁 2, 2), we
apply !nd_ptr (𝑍, 7) to !nd the sequence of frames to rewind to the most recent assignment to 𝑍. In
terms of ordinals, such sequence is 7, 6, 4, 3. In terms of frame ids we have:
                                 !nd_ptr (𝑍, (𝑁 2, 2)) = (𝑁 2, 2), (𝑗, 6), (𝑗, 4), (𝑁 1, 2) .
Notice that the sequence skips the frame with ordinal 5 because it contains upd𝑇 = false. Frames
with ordinals 8 and 9 are explained later, in Example 4.2.                                    ↭

Null pointer dereference. If the instruction located at 𝑙 .pc dereferences a pointer 𝑘, and 𝑘 is nil,
it indicates an error. Thus, if the $ag isnil 𝑆 is true in 𝑙 , we push a new frame with the symbolic
instruction )** onto the current node 𝑊 to indicate a runtime error. For the lace construction, we
assume that dereferenced pointers are not nil when the last executed instruction of 𝐿 is executed.
Encoding of p ↗ p!eld ω nil. We rewind the lace to !nd the most recent assignment to 𝑘. Let
                                                                                                       "         #
(𝑊, 𝑂) be the identi!er of 𝑙 , and 𝑂𝑆 1 = (𝑗 1, 𝑂 1 ), . . . , 𝑂𝑆𝑌 = (𝑗𝑌 , 𝑂𝑌 ) be the sequence !nd_ptr 𝑘, (𝑊, 𝑂) .
In principle, we might perform the encoding by pushing a new frame for each element of the
sequence 𝑂𝑆 1, . . . , 𝑂𝑆𝑌 , to keep a faithful record of the movements necessary to simulate the current
statement. Instead, we apply the following optimizations, whose objective is to use fewer frames:

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                                       11


                                             1       2       3            4          5   6      7
                                                     1       2            4         5    6      8
                                        𝑗                            upd𝑁 = true              *,!6

               1       2            3            4       5       6    7                   1         2     3   4   5   6   7
                       3            9                                                               7
          𝑁1       ↙𝑇 ω here∝   ↙𝑆 ω here∝                                                    pc : 𝑆 ω𝑇                       𝑁2

Fig. 4. A 3-node fragment of a kni!ed-tree with parameters 𝑄 = 2, 𝑔 = 7, 𝑞 = 0. The extra frame of position
𝑔 + 1 is not depicted. Gray numbers above the frames represent positions within the label, whereas numbers
inside the frames represent their positions in the lace.


(i) we skip the !rst id (𝑗 1, 𝑂 1 ) because it is redundant; (ii) for each of the following ids 𝑂𝑆 𝑄 in the
sequence, we only push a new frame if 𝑂𝑆 𝑄⇓1 belongs to a di"erent node than 𝑂𝑆 𝑄 . Precisely, for all
𝑃 = 2, . . . , 𝑢 ⇓ 1, if 𝑗 𝑄 ε 𝑗 𝑄⇓1 then we push a frame onto 𝑗 𝑄 with instr = *,!𝐿 𝑀 . The program counter
does not advance in these frames. Then, for the last id of the sequence, we push a frame 𝑙 onto 𝑗𝑌
with 𝑙 .pc = succ(𝑙 .pc) and 𝑙 .instr = ↙p!eld ω nil∝. The returned node is 𝑗𝑌 , i.e., 𝑗𝑌 = 𝑊.
Encoding of p ↗ p!eld ω 𝑍. The encoding process is the same as that described for p ↗ p!eld ω
nil, with one key di"erence: in the !nal frame, we set the symbolic instruction to ↙p!eld ω 𝑍∝.
Encoding of 𝑘 ω q ↗ p!eld. First, the lace moves to the node 𝑗 pointed by 𝑍 by following the
rewinding process described above for the statement p ↗ p!eld ω nil. Then, we search in 𝑗’s log
for the most recent assignment to the p!eld !eld. This operation is not done by going backward in
the lace, but rather by going backward in the log of 𝑗, since it must be recorded in 𝑗’s log per our
encoding invariant. Speci!cally, we search for the largest index 𝑂 where the frame (𝑗, 𝑂) is in use
and contains a symbolic instruction of the form ↙p!eld ! 𝑣∝, for some 𝑣. If no such index exists,
p!eld is interpreted as having its default value, which is to point at one of the children of 𝑗 in the
original input tree. We then distinguish the following cases:
[𝑣 = nil] We push a frame with isnil 𝑆 = true on 𝑗.
[𝑣 = 𝑕 , for some 𝑕 ↑ PV𝑊 ] If isnil𝑉 is true in the current frame, the lace pushes a frame with
      isnil 𝑆 = true. Otherwise, the lace moves again to the node pointed by 𝑕 , and there it pushes a
      frame with ↙𝑘 ! here∝.
[The log of 𝑗 does not contain an explicit assignment to p!eld] If p!eld is the 𝑃 th !eld in PF,
      𝑗.𝑃 ↑ 𝑀 , and 𝑗.𝑃 is active (as encoded in the $ag active_child 𝑄 ), the lace moves to 𝑗.𝑃 and pushes
      a frame with symbolic instruction ↙𝑘 ! here∝ there. Otherwise, a frame with isnil 𝑆 = true is
      pushed on 𝑗.
The last pushed frame always updates the program counter, irrespective of the executed instruction.
Encoding of 𝑘 ω 𝑍. If isnil𝑇 evaluates to true in 𝑙 , the lace pushes a new frame onto 𝑊 with isnil 𝑆
set to true. Otherwise, the lace moves to the node pointed by 𝑍 and pushes a frame with ↙𝑘 ω here∝
into it. In either case, the last frame also updates the program counter (pc).
   Example 4.2. Consider again the knitted-tree in Fig. 4. Recall that the program   "    counter
                                                                                              # in frame
(𝑁 2, 2) points to the statement 𝑘 ω 𝑍. As explained in Example 4.1, !nd_ptr 𝑍, (𝑁 2, 2) returns the
sequence of ids (𝑁 2, 2), (𝑗, 6), (𝑗, 4), (𝑁 1, 2). Due to the optimizations described above, the encoding
of the current statement adds only two frames to the lace, with ordinals 8 and 9. Frame 8 does not
advance the pc and carries the special symbolic instruction *,!6 , that keeps track of the position,
in the current log, reached by the rewinding process. Frame 9, instead, advances the pc and encodes
the actual assignment to 𝑘, in the same node where 𝑍 currently points.                                   ↭

                                                                                   , Vol. 1, No. 1, Article . Publication date: October 2024.
12                                                                                 Marco Faella and Gennaro Parlato


            Statement               Movement                        Information stored
            p ↗ p!eld ω nil         Find 𝑘 or fail                  ↙p!eld ! nil∝
            p ↗ p!eld ω 𝑍           Find 𝑘 or fail                  ↙p!eld ω 𝑍∝ or ↙p!eld ! nil∝
            𝑘 ω𝑍                    Find 𝑍                          ↙𝑘 ω here∝ or set isnil𝑆
                                    Find 𝑍 or fail, then !nd last
            𝑘 ω q ↗ p!eld                                           ↙𝑘 ω here∝ or set isnil𝑆
                                    assignment to p!eld
            p ↗ data ω exp          Find 𝑘 or fail                  Update key
           𝑆 ω p ↗ data             Find 𝑘 or fail                  Update 𝑆
                                    Move to the !rst inactive
            new 𝑘                                                   ↙𝑘 ω here∝ and set active
                                    child or fail
            free 𝑘                  Find 𝑘 or fail                  Reset active
                           Table 1. Summary of the encoding of the walking statements.



Encoding of new 𝑘. Let 𝑃 be the smallest index in [𝑄 + 1, 𝑄 + 𝑞] such that active_child 𝑄 is false. If
no such index exists, we push a frame on 𝑊 with the symbolic instruction &&., representing an
out-of-memory error. Otherwise, the lace moves to the 𝑃 th child of 𝑊 and pushes a frame 𝑙 there
with 𝑙 .pc = succ(𝑙 .pc), 𝑙 .instr = ↙𝑘 ω here∝, 𝑙 .active = true, and 𝑙 .isnil 𝑆 = false.
Encoding of free 𝑘. The lace moves to the node 𝑗 pointed by 𝑘 and pushes there a frame 𝑙 with
active = false and an updated pc. In the new frame, isnil𝑇 is set to true for every pointer 𝑍 that
currently points at 𝑗, including 𝑘. To !nd such pointers, let (𝑗, 𝑂) be the id of 𝑙 . Then, 𝑍 points at 𝑗
if the log of 𝑗 contains another frame (𝑗, 𝑃) such that: 𝑃 < 𝑂, (𝑗, 𝑃) contains ↙𝑍 ! here∝, and the
upd𝑇 $ag is false in all frames from (𝑗, 𝑃 + 1) to (𝑗, 𝑂).
   Table 1 summarizes the previous cases and includes the encodings for the statements p ↗ data ω
exp and 𝑆 ω p ↗ data, which are simple variations of the ones described above.
Encoding Boolean Conditions and Control-!ow Statements. Conditionals and loops can be
local or walking instructions, depending on the Boolean condition. Data conditions are evaluated
locally by using the values of local variables stored in the current frame 𝑙 . For heap conditions, we
may traverse the lace. Here, we only consider conditions of the form 𝑘 = 𝑍, as we can simulate
other heap conditions with extra variables. For example, we replace p ↗ p!eld = 𝑍 with 𝑕 = 𝑍 by
introducing a new pointer variable 𝑕 and assigning it the value of p ↗ p!eld.
   We handle conditions of the form 𝑘 = 𝑍 as follows. We !rst attempt to resolve the heap condition
using isnil $ags. If both pointers have their isnil $ags set to true, the condition is true; if the $ags
di"er, the condition evaluates to false. if the local resolution is inconclusive, we rewind the lace
starting from 𝑙 until !nding an assignment to either 𝑘 or 𝑍. For instance, encountering ↙𝑘 ! here∝
within frame (𝑗, 𝑂), we then search through the frames of 𝑗’s log for largest index 𝑃 < 𝑂 where frame
(𝑗, 𝑃) contains ↙𝑍 ! here∝. If no such index exists, the condition is false. If found, the condition holds
                                                                                           )
if and only if 𝑍 was not updated from (𝑗, 𝑃) to (𝑗, 𝑂), checked using the upd𝑇 $ags: ¬ 𝑌 ↑ [ 𝑄+1,𝐿 ] upd𝑌𝑇 .
Based on this evaluation, we push a new frame where we update the program counter pc based on
the condition outcome. If we !rst encounter ↙𝑍 ! here∝, the process is symmetrical.
   In the following, for a label 𝑡 and 𝑂 ↑ N, we denote by 𝑡 <𝐿 (resp., 𝑡 ↓𝐿 ) the label obtained by
setting avail to true in all frames of 𝑡 with indices greater than or equal to 𝑂 (greater than 𝑂, resp.).
   The following lemma states that each new frame in a knitted-tree depends only on local infor-
mation from the neighboring nodes, as detailed in the construction. Only the next !eld remains

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  13


unconstrained until the next frame is known. Hence, we write 𝑙1 ∞ 𝑙2 to signify that the frames 𝑙1
and 𝑙2 are equal except for their next !eld.
   L)..# 4.3 (L&/#0+"1). There exist functions Up, Down, Internal with the following properties. Let
𝑡, 𝑤1, . . . , 𝑤𝑃+𝑋 be the logs of a node 𝑗 and of its children in a knitted-tree pre!x.
     • For all steps (𝑗.𝑃, 𝑥) ↗next (𝑗, 𝑦) in the lace, it holds 𝑡 𝑍 ∞ Up(𝑤 𝑄↓𝑎 , 𝑃, 𝑡 <𝑍 ).
     • For all steps (𝑗, 𝑦) ↗next (𝑗.𝑃, 𝑥) in the lace, it holds 𝑤 𝑎𝑄 ∞ Down(𝑡 ↓𝑍 , 𝑃, 𝑤 𝑄<𝑎 ).
     • For all steps (𝑗, 𝑦) ↗next (𝑗, 𝑦 + 1) in the lace, it holds 𝑡 𝑍+1 ∞ Internal(𝑡 ↓𝑍 ).

On the choice of parameters 𝑞 and 𝑔. Parameter 𝑞 corresponds to the number of allocations made
by the program. Programs that do not create new nodes can be analyzed with 𝑞 = 0, while 𝑞 = 1 is
adequate for programs that insert a single new node. Parameter 𝑔 relates to the number of passes
and instructions executed per node. Although some terminating programs may require unbounded
labels, moderate 𝑔 values typically su#ce for common tree-like algorithms.

5     Properties of kni!ed-trees
Pre!x of a knitted-tree. An (𝑞, 𝑔)-knitted-tree is de!ned as a knitted-tree associated with an execu-
tion 𝐿 that belongs to kt (𝐿, 𝑞, 𝑔). A knitted-tree pre!x of a knitted-tree K is any data tree derived
from K by truncating its lace at some frame 𝑙 (i.e., setting the $ag 𝑙 →.avail to true for all frames 𝑙 →
that follow 𝑙 in the lace), and unconstraining 𝑙 .next so that it can take any value.

5.1    Compositionality
De"nition of the predicate formula consistent_child (𝑤, 𝑃, 𝑡). Based on the functions Up and
Down from Lemma 4.3, we de!ne the formula consistent_child (𝑤, 𝑃, 𝑡) using the underlying data
theory D. This predicate assumes that 𝑡 and 𝑤 are logs belonging to two possibly di"erent knitted-
trees and ensures that they occur in the same knitted-tree as the logs of a node and its 𝑃 th child. To
ensure this property, it checks that consecutive frames (𝑙1, 𝑙2 ) connected by the attributes next and
prev, with one frame belonging to 𝑤 and the other frame belonging to 𝑡, adhere to the functions Up
and Down accordingly. A precise de!nition of consistent_child can be found in Appendix C.4.
   The next lemma directly follows from the de!nitions of consistent_child and knitted-tree pre!x,
a#rming that consistent_child holds for all pairs of parent-child logs of a knitted-tree.
  L)..# 5.1. For all labels 𝑡, 𝑤 ↑ 𝑈(SK ) and indices 𝑃 ↑ [𝑄 + 𝑞], if there exists a knitted-tree pre!x
where 𝑡 and 𝑤 are the logs of a node and its 𝑃 th child respectively, then consistent_child (𝑤, 𝑃, 𝑡) holds.
  The following lemma establishes the key property of consistent_child relevant to our veri!cation
approach, enabling the composition of knitted-trees by combining subtrees from di"erent instances.
    L)..# 5.2 (C&.-&$+"+&(#0+"1). For 𝑂 = 1, 2, let 𝑡𝐿 ↑ 𝑈(SK ) be the log of a node 𝑊𝐿 in an (𝑞, 𝑔)-
knitted-tree pre!x K𝐿 . If consistent_child (𝑡2, 𝑃, 𝑡1 ) holds true for some 𝑃 ↑ [𝑄 + 𝑞], then there exists
an (𝑞, 𝑔)-knitted-tree pre!x K where 𝑡1 is the log of a node and 𝑡2 is the log of its 𝑃 th child. Moreover,
K can be obtained by replacing the subtree rooted at the 𝑃 th child of 𝑊 1 in K1 with the subtree rooted at
𝑊 2 in K2 .
  P*&&2. Let K be the data tree obtained by replacing the subtree rooted at the 𝑃 th child of 𝑊 1 in
K1 with the subtree rooted at 𝑊 2 in K2 . We prove that K is a knitted-tree pre!x by induction on the
number of pairs (𝑦, 𝑥) where frames 𝑡1𝑍 and 𝑡2𝑎 are adjacent in the lace, each such pair representing
an interaction between the parent’s and the child’s labels.
  When the above number is zero, there are no interactions between 𝑊 1 and its 𝑃 th child in K1 . Let
𝐿1 be an execution s.t. K1 is a pre!x of a knitted-tree representing 𝐿1 . It is direct to show that K is

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
14                                                                          Marco Faella and Gennaro Parlato


a knitted-tree pre!x for an execution 𝐿 following the same steps as 𝐿1 , starting with the input tree
of K. Since 𝐿1 never visits the 𝑃 th child of 𝑊 1 , and this subtree is the only di"erence between K1
and K, 𝐿 is a valid execution of 𝑛.
   For the inductive case, consider the last interaction (𝑦, 𝑥) between 𝑡1𝑍 and 𝑡2𝑎 . First, assume that
such interaction is a step up from the frame 𝑡2𝑎 to 𝑡1𝑍 . Let K1→ be derived from K1 by truncating its
lace to end just before 𝑡1𝑍 . Clearly, K1→ is still a knitted-tree pre!x, and the modi!ed label 𝑡1→ of 𝑊 1
is obtained from 𝑡1 by removing the frames with index at least 𝑦, by setting their avail $ags to
true. We can now apply the inductive hypothesis to the labels 𝑡1→ and 𝑡2 , because we have removed
one interaction between them. Hence, we can assume that there is a single knitted-tree pre!x
K → containing both labels as the logs of a parent and its 𝑃 th child. Next, we obtain the desired
knitted-tree pre!x K from K → by reintroducing the sequence of frames removed from K1 . We need
to prove that adding those frames respects all rules of knitted-trees. The correctness of the !rst
added frame, 𝑡1𝑍 , is ensured by consistent_child (𝑡2, 𝑃, 𝑡1 ), because it applies the function Up to all
upward interactions between 𝑡2 and 𝑡1 . In turn, Lemma 4.3 ensures that adhering to that function
is su#cient to establish the correctness of the next frame. Subsequent frames can be reintroduced
due to unchanged surroundings remain. Lemma 4.3 ensures that no other information is relevant.
   The other case to prove is when the last interaction is a step down from the parent’s frame 𝑡1𝑍 to
the child’s frame 𝑡2𝑎 . De!ne 𝑡2→ as the label obtained from 𝑡2 with the frames of indices 𝑥 and above
removed. Similar to the previous case, we apply the inductive hypothesis to the shortened label 𝑡2→
and its shortened knitted-tree pre!x K2→, resulting in a knitted-tree pre!x K →. We then reintroduce
the frames removed from K2 into K →. The correctness of the !rst reintroduced frame is ensured
by consistent_child checking the function Down on every downward interaction. The subsequent
reintroduced frames are still valid because there are no steps returning to the parent of 𝑊 2 , and their
surroundings remain unchanged from K2 .                                                                ↭

5.2    Relations with Program Executions
Retrieving the heap from its knitted-tree representation. We select the nodes where active is true in
their top frame. For a node 𝑗 and pointer !eld p!eld (assumed to be the 𝑃 th !eld in PF):
      • If p!eld has never been updated, 𝑗.p!eld points to the 𝑃 th child of 𝑗, if 𝑗.𝑃 exists and is active
        in the knitted-tree; otherwise, 𝑗.p!eld points to nil.
      • If the last update in 𝑗’s log is ↙p!eld ! nil∝, then pointer !eld is also nil.
      • Otherwise, the last update is ↙p!eld ! 𝑘∝ for some pointer variable 𝑘 (not nil). We navigate
        the lace backward using !nd_ptr until !nding a frame that reports ↙𝑘 ! here∝, say in the
        log of node 𝑁, and set 𝑗.p!eld to 𝑁.
We denote by heap(K) the heap corresponding to the knitted-tree (pre!x) K, as described above.
 From a knitted-tree, we can !nd the !nal value of each pointer variable. We denote by pv(K) the
map that assigns each 𝑘 ↑ PV𝑊 to the node of heap(K) pointed to by 𝑘 at the end of the lace of K.
Exit status of a knitted-tree. To distinguish how knitted-trees terminate, we introduce the notion of
exit statuses for individual frames and for the entire knitted-tree. Each frame 𝑙 of a knitted-tree is
assigned one of !ve statuses in ExStatus = {C, E, O, M, N}, with the following meanings:
      • Clean exit: The program counter (pc) of 𝑙 points to an exit instruction;
      • Runtime Error: 𝑙 .instr = )**, indicating a null-pointer dereference;
      • Label Over$ow: the index of 𝑙 in its label is 𝑔 + 1, indicating log over$ow;
      • Out of Memory: 𝑙 .instr = &&., indicating a failed attempt to allocate a node with the new
        statement due to the absence of inactive nodes.
      • None: Indicates that frame 𝑙 is not a terminal frame in all other cases.

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  15


A frame 𝑙 is terminal if its status is not None. Indeed, the exit statuses di"erent from N terminate
the lace, hence only the last frame in the lace may have an exit status di"erent from N. The exit
status of a knitted-tree is the status of the last frame in its lace.
   The following lemmas relate the exit status of a knitted-tree to the execution it was derived from.
  L)..# 5.3. For all executions 𝐿 and knitted-trees K ↑ kt (𝐿, 𝑞, 𝑔), if K’s exit status is not in
{O, M}, then the last con!guration of 𝐿 is (heap(K), pv(K), 𝑙.𝑆, 𝑙.pc), where 𝑙 is the last frame of
K’s lace.
   P*&&2. Let K = (𝑟, 𝑠). The proof is by induction on the length of 𝐿. The base case is when 𝐿
consists only of the initial con!guration. The thesis follows from the de!nition of the backbone 𝑟
and the base case of the labeling function 𝑠.
   For the inductive case, consider the pre!x 𝐿 of 𝐿 with one fewer step. We remove from K the
sequence of frames encoding the last step of 𝐿, by setting the avail !elds of those frames to true. The
resulting data tree is a knitted-tree K ↑ kt (𝐿, 𝑞, 𝑔). By inductive hypothesis, the last con!guration
of 𝐿 can be recovered from K. By inspecting the encoding of the various types of statements, as
described in §4.3, we can prove that the encoding in K of the last step in 𝐿 faithfully preserves the
information required to reconstruct the last con!guration in 𝐿.                                       ↭

  L)..# 5.4. Let K ↑ kt (𝐿, 𝑞, 𝑔) for some execution 𝐿 and parameters 𝑞 and 𝑔. If the exit status of
K is E, then 𝐿 ends in an error con!guration. Conversely, if 𝐿 ends in an error con!guration, then the
exit status of K is in {E, O, M}.
   P*&&2. To prove the !rst statement, assume that the exit status of K is E, occurring when the last
frame 𝑙 in K’s lace has the symbolic instruction )**. By Lemma 5.3, the last con!guration of 𝐿 can
be recovered from K as the tuple 𝑚 = (heap(K), pv(K), 𝑙.𝑆, 𝑙 .pc). By de!nition of knitted-trees, the
symbolic instruction )** arise only from a null pointer dereference, so 𝑚 is an error con!guration.
   For the second statement, assume that 𝐿 ends in an error con!guration and the exit status of K
is not O and M. We show that the exit status of K is E. By Lemma 5.3, the last con!guration of 𝐿
can be recovered from K as (heap(K), pv(K), 𝑙.𝑆, 𝑙 .pc), where 𝑙 is the last frame of the lace of K.
Since 𝐿 ends in an error con!guration, the program counter at 𝑙 points to an instruction causing a
null pointer dereference, leading to the symbolic instruction )** and hence to the exit status E. ↭

    L)..# 5.5. For all 𝑞, 𝑔, the (𝑞, 𝑔)-knitted-trees of in!nite executions have exit status O.
   P*&&2. Each step of an execution adds at least one frame to the lace of its knitted-tree. Since the
total number of nodes and frames in a knitted-tree is !nite, the lace will eventually occupy a frame
with index 𝑔 + 1 in the log hosting that frame, resulting in the exit status O.                      ↭

6     Reasoning about Kni!ed-trees through Constrained Horn Clauses
In this section, we de!ne a system of CHCs whose minimal model characterizes the set of all logs
of any (𝑞, 𝑔)-knitted-tree pre!x of a given program.

6.1    The CHC System
                                                                                              "        #
For a program 𝑛 and integer parameters 𝑄, 𝑞, and 𝑔, we introduce a CHC system called Ckt 𝑛, 𝑄, 𝑞, 𝑔 .
This system uses a single uninterpreted"relation symbol,
                                                    #     Lab(𝑡), with 𝑡 matching the data signature
SK of knitted-trees. The design of Ckt 𝑛, 𝑄, 𝑞, 𝑔 guarantees the following property:
                                                                "         #
   T3)&*). 6.1. In the minimal model of the CHC system Ckt 𝑛, 𝑄, 𝑞, 𝑔 , Lab(𝑡) is true for a label 𝑡
if and only if there exists an (𝑞, 𝑔)-knitted-tree pre!x K of 𝑛 such that 𝑡 is the label of a node in K.

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
16                                                                                 Marco Faella and Gennaro Parlato



     (I)      Lab(𝑡) ⇒ len(𝑡, 1) ⇑ !rst_frame(𝑡 1 )                      Initializing non-root nodes

     (II)     Lab(𝑡) ⇒ len(𝑡, 2) ⇑ start (𝑡)                             Initializing the root node

     (III)    Lab(𝑡) ⇒ len(𝑡, 𝑂) ⇑ Lab(𝑡 <𝐿 ) ⇑ εInternal (𝑡 <𝐿 , 𝑡 𝐿 ) An internal step

     (IV)     Lab(𝑡) ⇒ len(𝑡, 𝑂) ⇑ Lab(𝑡 <𝐿 ) ⇑ Lab(𝑤)                   A step from the 𝑃 th child to its parent
                             ⇑ consistent_child (𝑤, 𝑃, 𝑡 <𝐿 )
                             ⇑ εUp (𝑤, 𝑃, 𝑡 <𝐿 , 𝑡 𝐿 )

     (V)       Lab(𝑤) ⇒ len(𝑤, 𝑂) ⇑ Lab(𝑡) ⇑ Lab(𝑤 <𝐿 )                  A step from a node to its 𝑃 th child
                             ⇑ consistent_child (𝑤 <𝐿 , 𝑃, 𝑡)
                             ⇑ εDown (𝑡, 𝑃, 𝑤 <𝐿 , 𝑤 𝐿 )

     (VI)             ∈ ⇒ Lab(𝑡) ⇑ label_exit (𝑡, Ex)                    The lace ends with exit status in Ex

                                                 "     #
Fig. 5. CHCs (I)-(V) form the CHC system Ckt 𝑛, 𝑄, 𝑞, 𝑔 , while the CHC system Cex (I) includes all the
CHCs in the figure. Here, 𝑂 ↑ [2, 𝑔] and 𝑃 ↑ [𝑄 + 𝑞].


                                            "            #
   Our approach to de!ning CHCs in Ckt 𝑛, 𝑄, 𝑞, 𝑔 builds on the rules for constructing knitted-trees
from §4.3, with a twist. In §4.3, we extend a partial knitted-tree by adding frames to existing logs.
However, building a partial knitted-tree is impractical due to our predicate’s nature, and we must
reason about labels from all possible knitted-trees. To address this, we use the compositionality
lemma (Lemma 5.2), which states that two consistent labels imply a knitted-tree where those
labels are logs of an internal node and one of its children. Additionally, we use the locality lemma
(Lemma 4.3) to extend the lace involving these nodes. This lemma entails that constructing a
knitted-tree involves adding frames to node logs so that any two consecutive frames belong to the
same node or to neighboring backbone nodes. We use this property in the CHC system, employing
independent CHCs to simulate adding a single frame. Speci!cally, we use the functions Up for
upward movement, Down for downward movement, and Internal for expanding the lace within the
same log. To use them in the CHC system, we introduce three new predicates to constrain logs
according to these functions: εDown (𝑡, 𝑃, 𝑤 𝑄 , 𝑙 ), εUp (𝑤 𝑄 , 𝑃, 𝑡, 𝑙 ), and εInternal (𝑡, 𝑙 ), where 𝑙 represents
the frame output by the corresponding
                                    "       function.
                                               #          See the Appendix C.4 for details.
   Fig. 5 details the CHCs of Ckt 𝑛, 𝑄, 𝑞, 𝑔 . While describing each CHC, we establish the “only if”
direction of Theorem 6.1, by induction on the number of CHC applications needed to insert 𝑡 into
the minimal interpretation of Lab. The proof of the “if” direction follows the CHC descriptions.
   Before detailing the CHCs, we introduce some notation. Let 𝑡 ↑ 𝑈(SK ) and 𝑂 ↑ N. The formula
len(𝑡, 𝑂) is true if all frames with indices in [𝑂] are unavailable and all other frames are available,
                               *
i.e., len(𝑡, 𝑂) = ¬𝑡 𝐿 .avail ⇑ 𝑀+1
                                 𝑄=𝐿+1 𝑡 .avail . With an abuse of          notation, we write 𝑡 <𝐿 in a CHC as a
                def                     𝑄
                                                                         *                         *
shorthand for a fresh variable 𝑧 , together with the conjunct 𝑏 ↑ [𝐿⇓1] (𝑧 𝑏 = 𝑡 𝑏 ) ⇑ 𝑏 ↑ [𝐿,𝑀+1] 𝑧 𝑏 .avail.
   CHC I and CHC II ensure that Lab includes the labels of all knitted-trees representing an
execution of 𝑛 of length of 0. These labels form the base case for the proof of the “only if” direction
of Theorem 6.1, as both CHCs are facts. CHC I de!nes the labels of non-root nodes where all frames
except the !rst are available, and the !elds active and active_child are consistent (see Appendix C.1).
CHC II speci!es the root node labels, constraining the !rst two frames to be unavailable, with

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  17


start (𝑡) specifying the second frame of 𝑡 according to the base case of knitted-tree labels (see
§4.3.1 and Appendix C.2).
  The remaining CHCs extend each node’s log one frame at a time, following the inductive case of
the knitted-tree label de!nition. To prove the “only if” direction of Theorem 6.1, we inductively
assume that the labels in the body of each rule satisfy the claim, i.e., they label a node in a (𝑞, 𝑔)-
knitted-tree pre!x. We now show that the label in the rule’s head also satis!es the claim.
    CHC III addresses cases where 𝑡 𝐿 follows 𝑡 𝐿⇓1 in the lace, aka an internal step. In the CHC,
Lab(𝑡 <𝐿 ) ensures that 𝑡 <𝐿 labels a node in an (𝑞, 𝑔)-knitted-tree pre!x. The formula εInternal (𝑡 <𝐿 , 𝑡 𝐿 )
constrains the next frame 𝑡 𝐿 to encode the next internal step, as asserted in Lemma 4.3.
    CHC IV addresses cases where the lace extends with a new frame pushed to the parent of the pre-
vious frame, typically during a rewind phase of a walking statement. The predicate consistent_child
ensures that the labels 𝑡 <𝐿 and 𝑤 belong to the same knitted-tree pre!x, as the log of a parent and
its 𝑃 th child (Lemma 5.2). Then, the predicate εUp extends the lace by adding an extra frame to 𝑡 <𝐿 ,
following the topmost frame of 𝑤.
    CHC V addresses the opposite scenario of CHC IV, where the last step of the current lace pre!x
goes from the parent to its 𝑃 th child. This rule, thanks to εDown , ensures that 𝑤 𝑄 correctly extends
𝑤 𝑄<𝐿 with an additional frame representing the latest step in the lace.

  P*&&2. (“if” direction of Theorem 6.1). Let 𝑊 be a node in K with log 𝑡. We proceed by induction
on the length 𝛥 of the lace of K.
  Base case (𝛥 = 1): There is only one frame in the lace at the root of K. Here, either CHC I or
CHC II inserts 𝑡 into Lab, depending on whether 1 or 2 frames are unavailable in 𝑡.
  Inductive step (𝛥 > 1): Consider K𝑏⇓1 , the pre!x of K with the last frame of the lace removed. By
inductive hypothesis, the logs of K𝑏⇓1 belong to Lab. If 𝑡 is a log of K𝑏⇓1 , the claim holds. Otherwise,
𝑡 contains the last frame in the lace of K, meaning that the logs of 𝑊’s neighboring nodes (its parent
and children) are unchanged from K𝑏⇓1 . Thus, by inductive hypothesis those logs belong to Lab.
Depending on the direction taken in the last step, 𝑡 is added to Lab by one of CHC III to CHC V, as
detailed in the above description of the individual CHCs.                                              ↭

6.2   The Exit Status Problem
In this section, we propose a method to determine if a given program can lead to runtime memory
safety error via an execution that can be represented by an (𝑞, 𝑔)-knitted-tree. We achieve this
by solving a CHC system. If the system is unsatis!able, it indicates the existence of an execution
leading to a runtime error. Formally, the decision problem addressed in this section is the following.
  P*&%0). 1 (E4+" S"#"5$ P*&%0).). An instance I of the exit status problem is a tuple
(𝑛, 𝑄, 𝑞, 𝑔, Ex), where 𝑛 is a program that operates on 𝑄-ary S ω -trees with S ω = {key : D}, 𝑞, 𝑔 ↑ N,
and Ex is a set of exit statuses excluding N. The exit status problem asks whether there exists an
(𝑞, 𝑔)-knitted-tree of 𝑛 whose exit status belongs to Ex.
   We solve the exit status problem via the CHC system Cex (I): the exit status problem is positive
i" Cex (I) is unsatis!able. Fig. 5 shows the CHCs of Cex (I). The CHCs of Cex (I) are:
                       "         #
    • all CHCs of Ckt 𝑛, 𝑄, 𝑞, 𝑔 that are essential for establishing Theorem 6.1.
    • a unique query, CHC VI, to check for the existence of a log of a knitted-tree (pre!x) corre-
       sponding to a program execution with an exit status in Ex.
  The following theorem, which is the main result of this section, directly follows from Theorem 6.1
and the de!nition of CHC VI.


                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
18                                                                             Marco Faella and Gennaro Parlato


  T3)&*). 6.2. Let I be an instance of the exit-status problem. Then, I admits a positive answer if
and only if the CHC system Cex (I) is unsatis!able.
   P*&&2. Let I = (𝑛, 𝑄, 𝑞, 𝑔, Ex). We prove the theorem by establishing the equivalent statement:
I admits a negative answer if and only if the CHC system Cex (I) is satis!able.
   For the “only if” direction, if I admits a negative answer, no (𝑞, 𝑔)-knitted-tree of 𝑛 has an
exit status in Ex. Consider the interpretation for Lab containing all and only the node labels of all
       "         # pre!xes of 𝑛. By Theorem 6.1, this interpretation is in fact the minimal model
(𝑞, 𝑔)-knitted-tree
of Ckt 𝑛, 𝑄, 𝑞, 𝑔 , and as such it satis!es the CHCs I-V. Moreover, since none of those labels has an
exit status in Ex, this interpretation also satis!es the query VI, showing that Cex (I) is satis!able.
   For the “if” direction, if Cex (I) is satis!able, the interpretation of Lab in any model of Cex (I)
has" the property
              #      that no label in Lab has an exit status in Ex (CHC VI). Since Cex (I) implies
Ckt 𝑛, 𝑄, 𝑞, 𝑔 , by Theorem 6.1 such interpretation of Lab contains at least all the logs of the (𝑞, 𝑔)-
knitted-tree (pre!xes) of 𝑛. We conclude that the answer to the exit status problem is negative. ↭

7    CHC-based Verification of programs complying with precondition
This section focuses on solving the exit-status problem with preconditions, investigating how to
handle and reason about them within the CHC systems introduced in §6.
   We use S!"#s (introduced in §2.1) to specify preconditions. We denote by Apre = (S ω, S𝑁 ,𝑋,𝑋 𝑂 )
the S!"# de!ning the set of feasible input data trees for 𝑛. Apre operates on 𝑄-ary data trees over
the data signature S ω = {key : D}. Here, 𝑋 (𝑍 1, . . . , 𝑍𝑃 , key, 𝑍) is the transition constraint, and
𝑋 𝑂 (𝑍) de!nes the set of its !nal states.
   Similarly to the function heap(K) that extracts the output heap from a knitted-tree, we de!ne
in(K) to extract the input data tree from a knitted-tree K. For K = (𝑟, 𝑠), in(K) is the S ω -tree
(𝑀 , 𝑉), where 𝑀 is empty if the !rst frame of the root of 𝑟 is inactive. Otherwise, 𝑀 contains all
internal nodes of 𝑟, and for each node 𝑊 ↑ 𝑀 , 𝑉(𝑊).key = 𝑠 (𝑊).key 1 .
   We re!ne the exit status problem to comply with preconditions as follows.
  P*&%0). 2 (E4+" S"#"5$ P*&%0). ,+"3 P*)/&(!+"+&(). An instance of the exit status problem
with precondition is a pair (I, Apre ), where I = (𝑛, 𝑄, 𝑞, 𝑔, Ex) is an instance of the exit status
problem and Apre is an S!"# on 𝑄-ary S ω -trees. We say that (I, Apre ) admits a positive answer if
and only if there exists an (𝑞, 𝑔)-knitted-tree K of 𝑛 such that: K satis!es the exit status problem I
and in(K) belongs to 𝑈(Apre ).
   We reduce the exit status problem with precondition to CHC satis!ability. For an instance
(I, Apre ), we de!ne
                "      the #system Cpre (I, Apre ) as shown in Fig. 6. Besides the CHCs in the !gure, it
includes all Ckt 𝑛, 𝑄, 𝑞, 𝑔 ’s clauses. We introduce a fresh uninterpreted relation symbol Pre(𝑡, 𝑍, 𝛩),
where 𝑡 aligns with SK , 𝑍 is of type S𝑁 , and 𝛩 is Boolean. Cpre (I, Apre ) is de!ned to ensure the
following property.
  T3)&*). 7.1. Consider the minimal model of Pre and Lab that satis!es all the clauses of the CHC
system Cpre (I, Apre ) except for its query. It holds that: Pre(𝑡, 𝑍, 𝛩) holds true if and only if there exist:
  (a) a pre!x K of an (𝑞, 𝑔)-knitted-tree of 𝑛;
  (b) a node 𝑊 in K;
   (c) a run 𝑏 of Apre on the subtree of in(K) rooted at 𝑊;
such that all the following conditions hold:
  (1) 𝑡 is the log of 𝑊 in K;
  (2) 𝑍 is nil if 𝑊 is an auxiliary node of K, and 𝑏 (𝑊) otherwise;
  (3) 𝛩 is true if there exists a node in the subtree of K rooted at 𝑊 whose top frame has an exit status
       belonging to Ex.

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  19



        (i)    Pre(𝑡, 𝑍, 𝛩) ⇒ Lab(𝑡)                                               Labeling the leaves
                                ⇑ ¬(𝑡.active1 ) ⇑ ¬start (𝑡) ⇑ 𝑍 = nil
                                  "                        #
                                ⇑ 𝛩 ∋ label_exit (𝑡, Ex)

        (ii)   Pre(𝑡, 𝑍, 𝛩) ⇒ Lab(𝑡) ⇑ Pre(𝑤1, 𝑍 1, 𝛩 1 ) ⇑ . . . ⇑ Pre(𝑤𝑃+𝑋 , 𝑍𝑃+𝑋 , 𝛩𝑃+𝑋 )
                                  +
                              ⇑        consistent_child (𝑤 𝑄 , 𝑃, 𝑡)            Labeling internal nodes

                                    ,"
                                    𝑄 ↑ [𝑃+𝑋]
                                                                                 #
                                ⇑   𝑡.active1 ⇑ 𝑋 (𝑍 1, . . . , 𝑍𝑃 , 𝑡.key 1, 𝑍)
                                     "                           #                 -
                                   △ ¬𝑡.active1 ⇑ 𝑍 = nil
                                 ,      "                                            #-
                                ⇑ 𝛩 ∋ 𝛩 1 △ . . . △ 𝛩𝑃+𝑋 △ label_exit (𝑡, Ex)

       (iii)             ∈ ⇒ Pre(𝑡, 𝑍, 𝛩) ⇑ start (𝑡) ⇑ 𝛩 ⇑ 𝑋 𝑂 (𝑍)                 Checking the root


  Fig. 6. The CHC system Cpre (I, Apre ) includes the CHCs in this figure and the CHCs I-V from Fig. 5.



   We now describe the CHCs shown in Fig. 6. Simultaneously, we establish the “only if” direction
of Theorem 7.1 through induction on the number of CHC applications required to insert the triple
into the minimal interpretation of Pre. The proof of the “if” direction follows the CHC descriptions.
   Observe that in the context of Cpre (I, Apre ), Lab is independent of Pre, so the CHCs shown in
Fig. 5 retain their original meaning and properties. Speci!cally, Theorem 6.1 ensures that all labels
satisfying Lab occur as logs in some pre!x of an (𝑞, 𝑔)-knitted-tree of the program 𝑛.
    CHC (i) inserts the logs of the knitted-tree leaves into Pre, with extra information. This serves
as the base case in the inductive proof of Theorem 7.1. Leaves are nodes that are initially inactive
and do not satisfy the predicate start. In such cases, nil is inserted as the second component of the
triple. The quanti!er-free predicate label_exit (𝑡, Ex) sets the $ag 𝛩, evaluating to true if and only
if the top frame of 𝑡 corresponds to the lace tail and its exit status belongs to Ex (see Appendix C.3
for details). The constraint ¬start (𝑡) excludes the case when the input tree is empty and 𝑡 is the
root label of the knitted-tree, which is covered by CHC (ii).
   CHC (ii) propagates the state of Apre bottom-up. Inspecting its body, Lab(𝑡) ensures that 𝑡 is a
log in a knitted-tree pre!x, due to Theorem 6.1. By inductive hypothesis, for all 𝑃 ↑ [𝑄 + 𝑞] the
rest of the !rst line ensures the existence of a subtree K 𝑄 of a knitted-tree, whose root is labeled
with 𝑤 𝑄 . Moreover, 𝑍 𝑄 is the state assigned to the root of K 𝑄 by a run of Apre on in(K 𝑄 ), and 𝛩 is
true if K 𝑄 contains a log whose exit status belongs to Ex.
The second line ensures that the labels under consideration are the logs of a node and its 𝑄 + 𝑞
children in the same knitted-tree pre!x. This follows from repeatedly applying Lemma 5.2 to each
label 𝑤 𝑄 . The third line uses Apre ’s transition constraint 𝑋 to determine the new state 𝑍 in the parent
node, excluding the special case when 𝑡 labels the root of a knitted-tree with an empty input tree.
In that case, the next line assigns state nil to the root. Finally, the last line sets the parent’s exit
status $ag 𝛩 to true if any child has the same $ag set to true or if label_exit evaluates to true on 𝑡.
  CHC (iii) is the only query in the CHC system. It makes the system unsatis!able if, during the
simulation of Apre , the root of any knitted-tree (pre!x) is labeled with a !nal state of Apre and

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
20                                                                          Marco Faella and Gennaro Parlato


the parameter 𝛩 is true. This indicates that a knitted-tree satisfying the precondition contains an
end-of-lace frame with an exit status in Ex.
  It is worth clarifying how an empty input tree is handled. The precondition, Apre , may or may
not accept an empty input tree. The system of CHCs handles both cases correctly: for an empty
input tree, we get a knitted-tree with two levels of auxiliary nodes (active1 set to false). Thus,
CHC (i) labels these nodes with 𝑍 = nil, CHC (ii) puts nil also on the root, and CHC (iii) evaluates
the acceptance constraint 𝑋 𝑂 (nil), re$ecting whether Apre accepts the empty tree.

   P*&&2. (“if” direction of Theorem 7.1). Assume that K, 𝑊, and 𝑏 satisfy the assumptions of the
theorem. Let I(Pre) (resp., I(Lab)) be an interpretation of Pre (resp., Lab) corresponding to the
minimal model of Cpre (I, Apre ). We prove by structural induction that I(Pre) (𝑡, 𝑍, 𝛩) is true, where
the three components comply with items (1)-(3) of Theorem 7.1. Note that Theorem 6.1 ensures
that I(Lab)(𝑡) holds.
   The base case arises when 𝑊 is a leaf of K. Then, CHC (i) inserts the appropriate triple into I(Pre).
   The inductive step occurs when 𝑊 is an internal node of K. We show that the triple is correctly
handled by CHC (ii). Speci!cally, we assume the inductive hypothesis for all the children of 𝑊 in K,
i.e., for every 𝑃 ↑ [𝑄 + 𝑞], I(Pre) (𝑤 𝑄 , 𝑍 𝑄 , 𝛩 𝑄 ) is true, where the three components comply with items
(1)-(3) of Theorem 7.1 applied to the 𝑃 th child of 𝑊 in K. The constraints in the second line of the
body of CHC (ii) hold due to Lemma 5.1. The remaining parts of the constraint are also satis!ed as
detailed in the description of CHC (ii). Hence, with all constraints in the body of the CHC being
true, I(Pre)(𝑡, 𝑍, 𝛩) must also be true, concluding the proof.                                             ↭

  Main result of the section. We conclude the section by linking Cpre (I, Apre ) to the exit-status
problem with precondition by combining Theorem 7.1 with the properties of CHC (iii).
  T3)&*). 7.2. Let (I, Apre ) be an instance of the exit-status problem with precondition. Then,
(I, Apre ) admits a positive answer if and only if the CHC system Cpre (I, Apre ) is unsatis!able.
   P*&&2. Let I = (𝑛, 𝑄, 𝑞, 𝑔, Ex). We prove the theorem by establishing the equivalent statement:
(I, Apre ) admits a negative answer if and only if the CHC system Cpre (I, Apre ) is satis!able.
   For the “only if” direction, if (I, Apre ) admits a negative answer, by de!nition of exit-status
problem with precondition, no (𝑞, 𝑔)-knitted-tree K of 𝑛 with in(K) ↑ 𝑈(Apre ) has an exit status
in Ex. Consider an interpretation for Pre that contains all and only the triples (𝑡, 𝑍, 𝛩) complying
with items (1)-(3) of Theorem 7.1, which correspond to all the triples (K, 𝑊, 𝑏) described by the items
(a)-(c) of the same theorem. By Theorem 7.1, this interpretation satis!es all clauses of Cpre (I, Apre )
but its query. Also, it satis!es the query because the triple (𝑡, 𝑍, 𝛩), where 𝑡 is the log of the root of
any (𝑞, 𝑔)-knitted-tree, cannot satisfy both 𝛩 and 𝑋 𝑂 (𝑍), showing that Cpre (I, Apre ) is satis!able.
   For the “if” direction, assume that Cpre (I, Apre ) is satis!able. Assume by contradiction that
there exists an (𝑞, 𝑔)-knitted-tree K of 𝑛 with in(K) ↑ 𝑈(Apre ) and K has an exit status in Ex. By
applying the “if” direction of Theorem 7.1, we obtain that any interpretation of Pre that satis!es
Cpre (I, Apre ) except its query contains a triple (𝑡, 𝑍, 𝛩) where 𝑡 is the log of K’s root, 𝑍 is the state
of an accepting run of Apre on in(K), and 𝛩 = true. This triple clearly violates the query of Pre,
hence Cpre (I, Apre ) cannot be satis!able.                                                              ↭

8 Verifying memory safety
This section presents a sound algorithm for the memory safety problem (de!ned in §3). We begin
by establishing two key theorems that bridge the exit status problem to the memory safety problem,
laying the foundation for proving our method’s correctness.
   The following theorem is an immediate consequence of Lemma 5.4.

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  21


   T3)&*). 8.1. If the answer to the exit status problem (𝑛, 𝑄, 𝑞, 𝑔, {E}) is positive, then the answer
to the memory safety problem without precondition for 𝑛 is negative. The implication still holds if the
same precondition is applied to both problems.
    T3)&*). 8.2. If the answer to the exit status problem (𝑛, 𝑄, 𝑞, 𝑔, {O, M, E}) is negative, then the
answer to the memory safety problem without precondition for 𝑛 is positive. The implication still holds
if the same precondition is applied to both problems.
   P*&&2. Since no knitted-tree has exit status O, by Lemma 5.5, no execution is in!nite. Moreover,
since no knitted-tree has an exit status in {O, M, E}, by Lemma 5.4, no execution ends in an error
con!guration. It follows that all executions end in a !nal con!guration.                        ↭

   We present our algorithm to solve the memory safety problem without precondition, outlined
in Fig. 7. The input is a program 𝑛, and a natural number 𝑄 representing the arity of input data
trees. The process incorporates two parameters, 𝑞 and 𝑔, initialized to default values 𝑞 0 and 𝑔 0 ,
which are dynamically incremented during the analysis. The veri!cation process" starts by solving  #
the instance (𝑛, 𝑄, 𝑞, 𝑔, {E}) of the exit status problem, denoted by E4+"S"#"5$ 𝑛, 𝑄, 𝑞, 𝑔, {E} , to
check for null-pointer dereference errors.
   If solving this instance yields a positive answer, according to Theorem 8.1, we conclude a
negative answer
             " for the memory
                            #       safety problem for 𝑛 (indicating a memory safety violation). If the
E4+"S"#"5$ 𝑛, 𝑄, 𝑞, 𝑔, {E} does not yield a positive answer, it does not guarantee memory safety,
because the actual values of 𝑞 and 𝑔 might not capture all program executions, potentially missing
memory safety violations. To address this limitation, we proceed as follows:
                                            "              #
   (1) We solve the instance E4+"S"#"5$ 𝑛, 𝑄, 𝑞, 𝑔, {M} to check for out-of-memory failure arising
       from an unsuccessful memory allocation "    using the# new statement.
   (2) We solve the instance E4+"S"#"5$ 𝑛, 𝑄, 𝑞, 𝑔, {O} to check for label over$ow errors.
If both instances yield negative an-
swers, based on Theorem 8.2, we can                                         𝑊, 𝑃, 𝑋 0 , 𝑀 0
con!rm that 𝑛 is memory-safe. Other-
                                                                   𝑋 ⇒ 𝑋0, 𝑀 ⇒ 𝑀0
wise, we increment the corresponding
parameter value (either 𝑞 or 𝑔) to ex-
                                                                         "                  # N&
plore a broader range of program exe-                         E4+"S"#"5$ 𝑊, 𝑃, 𝑋, 𝑀, {E}          Memory-unsafe
cutions. The analysis then restarts with                                    Y)$
the updated parameter value.                 No: Increment 𝑋            "                   #
                                                              E4+"S"#"5$ 𝑊, 𝑃, 𝑋, 𝑀, {M}
   This iterative process may continue
                                                                            Y)$
inde!nitely for two reasons: either the
                                              N&: Increment 𝑀           "                   # Y)$
semi-algorithm for solving the exit sta-                      E4+"S"#"5$ 𝑊, 𝑃, 𝑋, 𝑀, {O}          Memory-safe
tus problem never returns (due to un-
decidability), or no value for (at least) Fig. 7. A sound algorithm for the memory safety problem, where
one parameter allows us to conclude 𝑛 is a program that takes a 𝑄-ary data tree as input, and 𝑞 0, 𝑔 0 ↑
the analysis when 𝑛 is memory-safe. N initialize parameters 𝑞 and 𝑔.
  T3)&*). 8.3. The procedure in Fig. 7 is a sound solution to the memory safety problem without
precondition. I.e., if the procedure terminates, it provides the correct answer to the memory safety
problem without precondition.
Coping with preconditions. We now extend the earlier veri!cation process to handle program
preconditions. The core structure remains unchanged; we replace each instance of the exit status
problem (Fig. 7) with a version that includes a precondition. This involves using the same parameters

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
22                                                                                    Marco Faella and Gennaro Parlato


along with an S!"# that speci!es the program’s precondition. The correctness of this enhanced
veri!cation process is ensured by Theorems 8.1 and 8.2, which already handle preconditions.

9    Implementation and Experiments
We have realized a proof-of-concept implementation of our approach, using the CHC solver Z3 [18]
and its Python API to build the system of CHCs described in Section 6. The experiments described
in this section were performed on an AMD Ryzen 5900X PC running Windows, equipped with
32GB of RAM. As we noticed signi!cant performance di"erences between di"erent versions of Z3,
we report the lowest running times among versions 4.12.0 and 4.12.6. Fig. 8 describes the parameters
of the case studies and the size of the corresponding CHC system, when saved in the SMT-LIB
format. Table 2 reports the experimental outcomes, discussed in this section.2
   Description of the input programs. We conducted experiments on two heap-manipulating func-
tions, each with a correct version and a memory-unsafe version. The !rst function, called “List
removal” and listed in Appendix A, searches for a given value in a singly-linked list and removes the
!rst node with that value, if any. Singly-linked lists are encoded with 𝑄 = 1, and since the function
does not allocate new nodes, we set 𝑞 = 0. The memory-unsafe version skips the initialization of
an auxiliary pointer (Line 1 in the source code). Since uninitialized pointers are considered nil, this
bug leads to a memory violation if the desired value is found in the !rst node of the list.
   The second function is the B$" insertion procedure in Fig. 1b. As it manipulates binary trees
and it allocates a new node, we set parameters 𝑄 = 2 and 𝑞 = 1. Its memory-unsafe version
consists in moving Line 3 (𝑘 ω 𝑘 →) at the end of the while-loop. In that way, at the end of
the loop both 𝑘 and 𝑘 → are nil, and a memory violation follows if Lines 12 or 13 are executed.

Experimental outcomes. Our tool can thoroughly an-                                          Size (MB)
alyze the four cases under examination, typically           Program               k   m    n=3    n=4
within a few seconds, except for two outliers that          List removal           1 0       0.7   2.0
require 45 and 51 minutes. The parameter 𝑔 (i.e.,           List removal w. bug 1 0          0.7     –
number of frames per log) is a critical performance         B$"  insertion         2   1     2.0   6.0
factor, as expected from the encoding. Indeed, some         B$" insertion w. bug 2 1         1.6     –
parts of the encoding, such as the predicates respon-
                                                         Fig. 8. Parameters and size of the CHC system
sible for the rewinding process, generate formulas
                                                         Cex (I) in SMT-LIB format.
that are quadratic or cubic in 𝑔.
   We run each experiment with increasing values of 𝑔 until either the program is proven correct,
or a memory violation is found. For the correct list removal function, 𝑔 = 4 captures all executions.
Proving the existence of a terminating execution (unsat of exit status 𝑒) takes 2 seconds, whereas
the absence of memory faults (sat of exit status 𝛬) takes 31 seconds, and proving the completeness
of the analysis (sat of exit status 𝛯) takes 48 seconds. In contrast, the memory fault in the buggy
version of list removal is detected with 𝑔 = 3 in 2 seconds (unsat of exit status 𝛬). Incidentally, the
error in the function simpli!es the range of possible executions, making 𝑔 = 3 su#cient to fully
explore all possible executions, as con!rmed by the “sat” outcome for the exit status 𝛯.
   The B$" insertion function also requires 𝑔 = 4 to be proved correct. Here, we !nd two performance
outliers: 45 minutes to prove the analysis complete and 51 minutes for the guaranteed success of
new (sat for exit status 𝛱). This can be partially explained by the fact that the system of CHCs is
three times as large as the one for the correct list removal (see Fig. 8). The error in the modi!ed
version, however, can be detected with 𝑔 = 3 in 26 seconds.
2 Our encoding uses datatypes, that are not readily supported by other CHC solvers.



, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  23


                Exit               Result                                 Exit                  Result
 Program       status             n=3             n=4    Program         status                n=3               n=4
                 O      unsat (00:05)      sat (00:48)                O      unsat (00:26)     sat (44:53)
                 C      unsat (00:01) unsat (00:02)                   C      unsat (00:12) unsat (01:00)
 List removal                                          B$" insertion
                 E         sat (00:06)     sat (00:31)                E         sat (02:48)    sat (00:17)
                 M         sat (00:01)     sat (00:01)                M         sat (00:06)    sat (50:58)
                 O         sat (00:07)              –                 O         sat (03:00)             –
 List removal C         unsat (00:01)               – B$" insertion C        unsat (00:07)              –
    w. bug       E     unsat (00:02)                –      w. bug     E     unsat (00:26)               –
                 M         sat (00:01)              –                 M         sat (00:04)             –
Table 2. Experimental results on memory safety. “sat” and “unsat” refer to the CHC system. Hence, “sat”
means that the corresponding exit status is not achieved by any program execution. Time is in mm:ss format
and does not include the time to generate the system of CHCs.



   The encoding and tool implementation are currently unoptimized. Potential optimizations are
discussed in §12 (future work).

10 Verifying Other Properties
This section presents in ascending order of complexity other program properties, besides memory
safety, that can be addressed using the framework presented in this paper. Due to space constraints,
we provide a high-level description here, with formal details to be covered in a future extension.
Checking simple contracts. When a tree data structure represents a set of elements, standard
operations include insertion, deletion, and search. It is crucial that these operations maintain the
tree’s expected properties. Speci!cally, nodes not directly involved in an operation should remain
una"ected in terms of their node allocation status and the data they store. For insertion or deletion,
the operation should add or remove the speci!ed node, respectively. We refer to these requirements
as the insertion contract and the deletion contract. Search operations should not modify the
data in any way, a property we call the read-only contract. We can address the insertion, deletion,
and read-only contracts using S!"#-based approaches. The idea is to design an S!"# that works
on knitted-trees and accepts them if they violate the property of interest. Consider the read-only
contract. Its S!"# operates bottom-up on the input knitted-tree, checking each node to ensure that
its log does not contain unavailable frames where the !eld active changes state, or the pointer !elds
or data !elds are updated. If either of these conditions is violated, the S!"# stores this information
in its state. Upon reaching the root of the knitted-tree, the S!"# accepts it if a violating node was
found. We can then intersect this S!"# with the one expressing the precondition, and simulate
them together on the set of knitted-trees, following the CHC construction in §7. A similar approach
can be designed for the other contracts, ensuring proper insertion, deletion, and search behaviors.
Checking the output tree. When dealing with tree data structures, ensuring that the program’s
execution consistently produces a valid tree is of utmost importance. Firstly, we aim to guarantee
that the heap’s underlying structure resulting from any execution is indeed a tree, referred to as
the tree-structure postcondition. To check this condition on a single knitted-tree, one could
start from the node of the output tree identi!ed by 𝑘! and recursively mark all descendants that
are active at the end of the execution as reachable. Note, however, that the children of a node in
the output tree may be di"erent from its structural children (i.e., di"erent from the children in the
knitted-tree). If a node’s log contains the symbolic instruction ↙p!eld ω 𝑘∝, it indicates that a link
of the current node was reassigned to the current value of the pointer 𝑘. The postcondition check
must then trace back the value of 𝑘, similar to the rewind operation described in §4.3. If, at any

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
24                                                                        Marco Faella and Gennaro Parlato


time, the postcondition veri!cation !nds that a node is reachable through two di"erent paths, it
will declare that the output is not a tree.
   The procedure sketched above can be simulated by a non-deterministic S!"# A¬tree that accepts
all knitted-trees whose output is not a tree. Intuitively, A¬tree would guess which nodes are
reachable and which pointers are traced along the lace, and then, in a single bottom-up pass, check
the correctness of the guesses. At that point, the CHCs in Figure 6 can be easily adapted to run
A¬tree on all knitted-trees of a given program, and so verify that all executions produce a tree.
   A similar approach can be used to check other postconditions, such as the fact that the output is a
speci!c kind of tree (e.g., a B$", a red-and-black tree, etc.). In that case, one would start by encoding
such property as an S!"#s A that checks the negated property on data trees. To run this S!"# on a
single knitted-tree, one would again start from the node that is the root of the output tree and label
it with one of the accepting states of A. Then, one would recursively visit all descendants in the
output tree, identi!ed by the same pointer-tracing procedure mentioned above, and label them with
the appropriate states of A according to its transition relation. If this process manages to build a
fully coherent accepting run of A on the output tree, it has been proved that it violates the original
property. As described above for A¬tree , this algorithm can be emulated by a non-deterministic
S!"# on knitted-trees, and then turned into a system of CHCs analogous to Figure 6.
Deductive Veri!cation. Our methodology is speci!cally tailored to establish the correctness of
procedures with a time complexity linearly proportional to the number of nodes in input lists or
trees. This limitation arises because we can only handle a bounded number of passages through
each node. While this constraint suits many common procedures in the literature that operate in
linear time, our approach can also be used in deductive veri!cation. To apply our approach in that
context, one decomposes the veri!cation process into more manageable conditions, describing
pre- and postconditions of speci!c segments of code that, in the worst case, can be executed in
linear time. Successfully proving these veri!cation conditions serves as a collective a#rmation,
establishing the overall correctness of the entire procedure under analysis.

11 Related Work
Our work is related to many works in the literature in di"erent ways. Here we focus on those that
seem to be closest to the results presented in this paper.
   Our approach uses CHC engines for backend analysis, aligning with other program veri!cation
methods [13, 22, 24, 25, 27, 29, 30, 33, 35, 39, 40, 52]. CHCs serve as an intermediate veri!cation
language, allowing focus on proof rules while solvers implement algorithms within a standard
framework. A major challenge is encoding heap-allocated mutable data structures. While array
theory is often used (e.g., [16, 41]), it can result in complex CHCs. Our approach uses simple theories
for basic data types, avoiding array theory unless necessary. Traditional heap program analysis
often uses abstractions like shape analysis [64] to scale. Re!nement types and invariants can be
used to transform complex data structures, avoiding array theory (e.g. [11, 38, 53, 63]). This method
often leads to over-approximation in CHCs, potentially causing false positives, as it replaces heap
operations with local object assertions. While this may not capture global invariants, it can enable
e#cient veri!cation for programs where local invariants su#ce. A recent proposal suggests using
an SMT-LIB theory of heaps for CHCs to standardize heap data-structure representation [21].
   Our technique intersects with tree automata, automata with auxiliary storage and bounded
tree-width graphs representing their executions. It also relates to Courcelle’s theorem proof, which
reduces analysis to tree automata emptiness [26]. Alur and Madhusudan [3] represented pushdown
automata executions with nested words, later extended for multistack and distributed automata [46].
We apply similar concepts to tree-manipulating programs, using laces as a graph representation of

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  25


program executions, where nodes are frames and edges are next and prev frame !elds. La Torre et
al. [43] proposed a tree encoding for multistack pushdown automata executions, comparable to our
lace encoding. In both cases, these graph representations of executions constitute a tree decomposi-
tion, witnessing their bounded treewidth. While [43] uses tree automata emptiness to analyze all
executions of multistack pushdown automata and solve their reachability problem, we leverage
CHC solvers. This approach allows us to employ a tree automata-like method with the added
advantage of reasoning about frame data. Similarly to [31], we use automata for program analysis.
However, whereas [31] employs counterexample-guided abstraction re!nement to iteratively re!ne
an overapproximation of a program’s error paths that is represented by an automaton, we use
precise a knitted-tree representation and leverage CHC solvers for approximation and re!nement.
   A line of work in program veri!cation focuses on developing decidable approaches for bounded-
pass heap-manipulating programs. While our work also considers bounded-pass programs, it
o"ers a broader range of veri!able properties compared to these approaches, potentially at the
cost of decidability. Mathur et al. [51] demonstrate memory safety decidability under speci!c
conditions: forest-like initial heaps and single-pass data structure traversal. Their results build on
earlier !ndings on uninterpreted coherent programs [49, 50]. While that approach handles memory
freeing, the support for more complex postconditions is left for future work. Alur and %ern& [2]
reduce assertion checking of single-pass list-processing programs to questions on data string
transducers. Its decidability stems from using a single advancing variable, limiting it compared to
Mathur et al.’s work, which supports multiple variables for pointer updates. This approach does
not directly address memory safety or heap shape changes, and is limited to reasoning about data
ordering and equality. It also does not handle explicit memory freeing.
   Heap veri!cation has been extensively studied, with research spanning decidable logics including
!rst-order logics with reachability [45], L+$%6 in the H#7&/ tool [44], and separation logic frag-
ments [8, 20, 59]. Some approaches interpret bounded treewidth data structures on trees [34, 47].
While these logics are often restricted, others with undecidable validity employ e"ective strategies
using heuristics, lemma synthesis, and programmer annotations [5–7, 9, 10, 12, 14, 15, 19, 36, 54,
56, 58, 60, 65]. In contrast, our knitted-tree encoding promotes a separation of concerns, o’oading
the algorithmic burden to the underlying CHC solver.

12 Conclusions and Future Works
Verifying programs that manipulate tree data structures often relies on intricate, manual proofs,
hindering automation and generalization. This paper introduces an automated technique to over-
come these challenges. Our core contribution lies in a uni!ed approach that leverages automata
and logics to handle various tree data structures. The foundation of our method is the knitted-tree
encoding, which ingeniously combines program inputs, outputs, and intermediate states into a
single structure. This encoding, coupled with its compositional properties, allows us to e"ectively
represent knitted trees using CHCs. By translating veri!cation into the well-studied domain of CHC
satis!ability, we bene!t from e#cient o"-the-shelf CHC solvers. We demonstrated our technique’s
applicability to the memory safety problem and discussed its potential for broader veri!cation tasks.
Our technique shows promise for automating veri!cation of linear-time procedures on tree-like
data structures, and can also assist in deductive veri!cation of higher-complexity programs.
Future work. Our primary focus will be on enhancing the practical e"ectiveness of our approach
through performance optimization. A key area for improvement is the size of the logs used in our
current implementation of knitted-trees. Our current approach follows the theoretical description
and does not optimize this parameter. We envision using summaries (see for example [28, 42]) to
compress the internal steps within the lace. This optimization could potentially reduce the log size

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
26                                                                                         Marco Faella and Gennaro Parlato


to just two frames for several procedures involving common tree data structures, which typically
navigate the input tree along a descending path. As demonstrated in our experimental results,
analyses carried out with short logs exhibit signi!cant performance improvements.
   Regarding the applicability to data structures beyond trees, we mention in the related work section
how the graphs underlying each lace associated with a knitted-tree exhibit bounded treewidth, with
the decomposition derived from the knitted-tree itself. This suggests that our technique may be
well-suited to a broader range of data structures, including doubly-linked lists and trees with parent
pointers, and generally, structures with bounded treewidth and canonical tree decompositions.
   While program logics for heap veri!cation, such as separation logics [57, 62] and related !rst-
order logics [55], are well-established, we use Symbolic Data Tree Automata as a lower-level
mechanism. Future work could explore converting properties from these higher-level logics to
equivalent S!"#s, combining the intuitive nature of established logics with the advantages of our
automata-based method.
   Another promising application of our approach is in developing a syntax-guided synthesis
(SyGuS) method [1] for procedures that manipulate tree data structures, with preconditions and
postconditions expressed by S!"#s. This method would enable the generation of code that is correct
by construction using CHCs, addressing similar challenges to those discussed in [61].

References
 [1] Rajeev Alur, Rastislav Bodík, Eric Dallal, Dana Fisman, Pranav Garg, Garvit Juniwal, Hadas Kress-Gazit, P. Madhusudan,
     Milo M. K. Martin, Mukund Raghothaman, Shambwaditya Saha, Sanjit A. Seshia, Rishabh Singh, Armando Solar-Lezama,
     Emina Torlak, and Abhishek Udupa. 2015. Syntax-Guided Synthesis. In Dependable Software Systems Engineering,
     Maximilian Irlbeck, Doron A. Peled, and Alexander Pretschner (Eds.). NATO Science for Peace and Security Series, D:
     Information and Communication Security, Vol. 40. IOS Press, 1–25. https://doi.org/10.3233/978-1-61499-495-4-1
 [2] Rajeev Alur and Pavol Cern&. 2011. Streaming transducers for algorithmic veri!cation of single-pass list-processing
     programs. In Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
     POPL 2011, Austin, TX, USA, January 26-28, 2011, Thomas Ball and Mooly Sagiv (Eds.). ACM, 599–610. https:
     //doi.org/10.1145/1926385.1926454
 [3] Rajeev Alur and P. Madhusudan. 2009. Adding nesting structure to words. J. ACM 56, 3 (2009), 16:1–16:43. https:
     //doi.org/10.1145/1516512.1516518
 [4] Emanuele De Angelis and Hari Govind V K. 2022. CHC-COMP 2022: Competition Report. Electronic Proceedings in
     Theoretical Computer Science 373 (nov 2022), 44–62. https://doi.org/10.4204/eptcs.373.5
 [5] Anindya Banerjee, Michael Barnett, and David A. Naumann. 2008. Boogie Meets Regions: A Veri!cation Experience
     Report. In Veri!ed Software: Theories, Tools, Experiments, Second International Conference, VSTTE 2008, Toronto, Canada,
     October 6-9, 2008. Proceedings (Lecture Notes in Computer Science, Vol. 5295), Natarajan Shankar and Jim Woodcock
     (Eds.). Springer, 177–191. https://doi.org/10.1007/978-3-540-87873-5_16
 [6] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. 2008. Regional Logic for Local Reasoning about Global
     Invariants. In ECOOP 2008 - Object-Oriented Programming, 22nd European Conference, Paphos, Cyprus, July 7-11, 2008,
     Proceedings (Lecture Notes in Computer Science, Vol. 5142), Jan Vitek (Ed.). Springer, 387–411. https://doi.org/10.1007/978-
     3-540-70592-5_17
 [7] Anindya Banerjee, David A. Naumann, and Stan Rosenberg. 2013. Local Reasoning for Global Invariants, Part I: Region
     Logic. J. ACM 60, 3 (2013), 18:1–18:56. https://doi.org/10.1145/2485982
 [8] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2004. A Decidable Fragment of Separation Logic. In FSTTCS
     2004: Foundations of Software Technology and Theoretical Computer Science, 24th International Conference, Chennai, India,
     December 16-18, 2004, Proceedings (Lecture Notes in Computer Science, Vol. 3328), Kamal Lodaya and Meena Mahajan
     (Eds.). Springer, 97–109. https://doi.org/10.1007/978-3-540-30538-5_9
 [9] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Smallfoot: Modular Automatic Assertion Checking
     with Separation Logic. In Formal Methods for Components and Objects, 4th International Symposium, FMCO 2005,
     Amsterdam, The Netherlands, November 1-4, 2005, Revised Lectures (Lecture Notes in Computer Science, Vol. 4111),
     Frank S. de Boer, Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever (Eds.). Springer, 115–137. https:
     //doi.org/10.1007/11804192_6
[10] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Symbolic Execution with Separation Logic. In Program-
     ming Languages and Systems, Third Asian Symposium, APLAS 2005, Tsukuba, Japan, November 2-5, 2005, Proceedings


, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                             27


     (Lecture Notes in Computer Science, Vol. 3780), Kwangkeun Yi (Ed.). Springer, 52–68. https://doi.org/10.1007/11575467_5
[11] Nikolaj S. Bjørner, Kenneth L. McMillan, and Andrey Rybalchenko. 2013. On Solving Universally Quanti!ed Horn
     Clauses. In Static Analysis - 20th International Symposium, SAS 2013, Seattle, WA, USA, June 20-22, 2013. Proceedings
     (Lecture Notes in Computer Science, Vol. 7935), Francesco Logozzo and Manuel Fähndrich (Eds.). Springer, 105–125.
     https://doi.org/10.1007/978-3-642-38856-9_8
[12] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2011. Compositional Shape Analysis by
     Means of Bi-Abduction. J. ACM 58, 6 (2011), 26:1–26:66. https://doi.org/10.1145/2049697.2049700
[13] Adrien Champion, Tomoya Chiba, Naoki Kobayashi, and Ryosuke Sato. 2020. ICE-Based Re!nement Type Discovery
     for Higher-Order Functional Programs. J. Autom. Reason. 64, 7 (2020), 1393–1418.
[14] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. 2012. Automated veri!cation of shape, size
     and bag properties via user-de!ned predicates in separation logic. Sci. Comput. Program. 77, 9 (2012), 1006–1036.
     https://doi.org/10.1016/J.SCICO.2010.07.004
[15] Duc-Hiep Chu, Joxan Ja"ar, and Minh-Thai Trinh. 2015. Automatic induction proofs of data-structures in imperative
     programs. In Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and Implementation,
     Portland, OR, USA, June 15-17, 2015, David Grove and Stephen M. Blackburn (Eds.). ACM, 457–466. https://doi.org/10.
     1145/2737924.2737984
[16] Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti. 2017. Program Veri!cation using
     Constraint Handling Rules and Array Constraint Generalizations. Fundam. Informaticae 150, 1 (2017), 73–117. https:
     //doi.org/10.3233/FI-2017-1461
[17] Emanuele De Angelis and Hari Govind V. K. 2024. CHC-COMP 2023: Competition Report. CoRR abs/2404.14923 (2024).
     https://doi.org/10.48550/ARXIV.2404.14923 arXiv:2404.14923
[18] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3: An E#cient SMT Solver. In Tools and Algorithms
     for the Construction and Analysis of Systems, 14th International Conference, TACAS 2008, Held as Part of the Joint
     European Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008.
     Proceedings (Lecture Notes in Computer Science, Vol. 4963), C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer, 337–340.
     https://doi.org/10.1007/978-3-540-78800-3_24
[19] Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2006. A Local Shape Analysis Based on Separation Logic. In
     Tools and Algorithms for the Construction and Analysis of Systems, 12th International Conference, TACAS 2006 Held as
     Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2006, Vienna, Austria, March 25 - April
     2, 2006, Proceedings (Lecture Notes in Computer Science, Vol. 3920), Holger Hermanns and Jens Palsberg (Eds.). Springer,
     287–302. https://doi.org/10.1007/11691372_19
[20] Mnacho Echenim, Radu Iosif, and Nicolas Peltier. 2021. Unifying Decidable Entailments in Separation Logic with
     Inductive De!nitions. In Automated Deduction - CADE 28 - 28th International Conference on Automated Deduction,
     Virtual Event, July 12-15, 2021, Proceedings (Lecture Notes in Computer Science, Vol. 12699), André Platzer and Geo"
     Sutcli"e (Eds.). Springer, 183–199. https://doi.org/10.1007/978-3-030-79876-5_11
[21] Zafer Esen and Philipp Rümmer. 2022. An SMT-LIB Theory of Heaps. In Proceedings of the 20th Internal Workshop
     on Satis!ability Modulo Theories co-located with the 11th International Joint Conference on Automated Reasoning
     (IJCAR 2022) part of the 8th Federated Logic Conference (FLoC 2022), Haifa, Israel, August 11-12, 2022 (CEUR Workshop
     Proceedings, Vol. 3185), David Déharbe and Antti E. J. Hyvärinen (Eds.). CEUR-WS.org, 38–53. https://ceur-ws.org/Vol-
     3185/paper1180.pdf
[22] Zafer Esen and Philipp Rümmer. 2022. Tricera: Verifying C Programs Using the Theory of Heaps. In 22nd Formal
     Methods in Computer-Aided Design, FMCAD 2022, Trento, Italy, October 17-21, 2022, Alberto Griggio and Neha Rungta
     (Eds.). IEEE, 380–391. https://doi.org/10.34727/2022/ISBN.978-3-85448-053-2_45
[23] Marco Faella and Gennaro Parlato. 2022. Reasoning About Data Trees Using CHCs. In Computer Aided Veri!cation - 34th
     International Conference, CAV 2022, Haifa, Israel, August 7-10, 2022, Proceedings, Part II (Lecture Notes in Computer Science,
     Vol. 13372), Sharon Shoham and Yakir Vizel (Eds.). Springer, 249–271. https://doi.org/10.1007/978-3-031-13188-2_13
[24] Marco Faella and Gennaro Parlato. 2023. Reachability Games Modulo Theories with a Bounded Safety Player. In
     Thirty-Seventh AAAI Conference on Arti!cial Intelligence, AAAI 2023, Thirty-Fifth Conference on Innovative Applications
     of Arti!cial Intelligence, IAAI 2023, Thirteenth Symposium on Educational Advances in Arti!cial Intelligence, EAAI
     2023, Washington, DC, USA, February 7-14, 2023, Brian Williams, Yiling Chen, and Jennifer Neville (Eds.). AAAI Press,
     6330–6337. https://doi.org/10.1609/AAAI.V37I5.25779
[25] Grigory Fedyukovich, Maaz Bin Safeer Ahmad, and Rastislav Bodík. 2017. Gradual synthesis for static parallelization of
     single-pass array-processing programs. In Proceedings of the 38th ACM SIGPLAN Conference on Programming Language
     Design and Implementation, PLDI 2017, Barcelona, Spain, June 18-23, 2017. ACM, 572–585.
[26] Jörg Flum and Martin Grohe. 2006. Parameterized Complexity Theory. Springer. https://doi.org/10.1007/3-540-29953-X
[27] Pierre-Loïc Garoche, Temesghen Kahsai, and Xavier Thirioux. 2016. Hierarchical State Machines as Modular Horn
     Clauses. In Proceedings 3rd Workshop on Horn Clauses for Veri!cation and Synthesis, HCVS@ETAPS 2016, Eindhoven, The


                                                                        , Vol. 1, No. 1, Article . Publication date: October 2024.
28                                                                                         Marco Faella and Gennaro Parlato


     Netherlands, 3rd April 2016 (EPTCS, Vol. 219). 15–28.
[28] Sergey Grebenshchikov, Nuno P. Lopes, Corneliu Popeea, and Andrey Rybalchenko. 2012. Synthesizing software
     veri!ers from proof rules. In ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI
     ’12, Beijing, China - June 11 - 16, 2012, Jan Vitek, Haibo Lin, and Frank Tip (Eds.). ACM, 405–416. https://doi.org/10.
     1145/2254064.2254112
[29] Arie Gur!nkel. 2022. Program Veri!cation with Constrained Horn Clauses (Invited Paper). In Computer Aided
     Veri!cation - 34th International Conference, CAV 2022, Haifa, Israel, August 7-10, 2022, Proceedings, Part I (Lecture Notes
     in Computer Science, Vol. 13371), Sharon Shoham and Yakir Vizel (Eds.). Springer, 19–29. https://doi.org/10.1007/978-3-
     031-13185-1_2
[30] Arie Gur!nkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A. Navas. 2015. The SeaHorn Veri!cation Framework.
     In Computer Aided Veri!cation - 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015,
     Proceedings, Part I (LNCS, Vol. 9206). Springer, 343–361.
[31] Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2013. Software Model Checking for People Who Love
     Automata. In Computer Aided Veri!cation - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July 13-19,
     2013. Proceedings (Lecture Notes in Computer Science, Vol. 8044), Natasha Sharygina and Helmut Veith (Eds.). Springer,
     36–52. https://doi.org/10.1007/978-3-642-39799-8_2
[32] Michael Hicks. [n. d.]. What is memory safety?, The Programming Languages Enthusiast. http://www.pl-enthusiast.
     net/2014/07/21/memory-safety/. Accessed: 2022-12-03.
[33] Hossein Hojjat, Filip Konecn&, Florent Garnier, Radu Iosif, Viktor Kuncak, and Philipp Rümmer. 2012. A Veri!cation
     Toolkit for Numerical Transition Systems - Tool Paper. In FM 2012: Formal Methods - 18th International Symposium,
     Paris, France, August 27-31, 2012. Proceedings (LNCS, Vol. 7436). Springer, 247–251.
[34] Radu Iosif, Adam Rogalewicz, and Jirí Simácek. 2013. The Tree Width of Separation Logic with Recursive De!nitions.
     In Automated Deduction - CADE-24 - 24th International Conference on Automated Deduction, Lake Placid, NY, USA,
     June 9-14, 2013. Proceedings (Lecture Notes in Computer Science, Vol. 7898), Maria Paola Bonacina (Ed.). Springer, 21–38.
     https://doi.org/10.1007/978-3-642-38574-2_2
[35] Shachar Itzhaky, Sharon Shoham, and Yakir Vizel. 2024. Hyperproperty Veri!cation as CHC Satis!ability. In Pro-
     gramming Languages and Systems - 33rd European Symposium on Programming, ESOP 2024, Held as Part of the
     European Joint Conferences on Theory and Practice of Software, ETAPS 2024, Luxembourg City, Luxembourg, April 6-11,
     2024, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 14577), Stephanie Weirich (Ed.). Springer, 212–241.
     https://doi.org/10.1007/978-3-031-57267-8_9
[36] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     Powerful, Sound, Predictable, Fast Veri!er for C and Java. In NASA Formal Methods - Third International Symposium, NFM
     2011, Pasadena, CA, USA, April 18-20, 2011. Proceedings (Lecture Notes in Computer Science, Vol. 6617), Mihaela Gheorghiu
     Bobaru, Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer, 41–55. https://doi.org/10.1007/978-3-
     642-20398-5_4
[37] Joxan Ja"ar and Michael J. Maher. 1994. Constraint Logic Programming: A Survey. J. Log. Program. 19/20 (1994),
     503–581.
[38] Temesghen Kahsai, Rody Kersten, Philipp Rümmer, and Martin Schäf. 2017. Quanti!ed Heap Invariants for Object-
     Oriented Programs. In LPAR-21, 21st International Conference on Logic for Programming, Arti!cial Intelligence and
     Reasoning, Maun, Botswana, May 7-12, 2017 (EPiC Series in Computing, Vol. 46), Thomas Eiter and David Sands (Eds.).
     EasyChair, 368–384. https://doi.org/10.29007/ZRCT
[39] Temesghen Kahsai, Philipp Rümmer, Huascar Sanchez, and Martin Schäf. 2016. JayHorn: A Framework for Verifying
     Java programs. In Computer Aided Veri!cation - 28th International Conference, CAV 2016, Toronto, ON, Canada, July
     17-23, 2016, Proceedings, Part I (LNCS, Vol. 9779). Springer, 352–358.
[40] Naoki Kobayashi, Ryosuke Sato, and Hiroshi Unno. 2011. Predicate abstraction and CEGAR for higher-order model
     checking. In Proceedings of the 32nd ACM SIGPLAN Conference on Programming Language Design and Implementation,
     PLDI 2011, San Jose, CA, USA, June 4-8, 2011. ACM, 222–233.
[41] Anvesh Komuravelli, Nikolaj S. Bjørner, Arie Gur!nkel, and Kenneth L. McMillan. 2015. Compositional Veri!cation
     of Procedural Programs using Horn Clauses over Integers and Arrays. In Formal Methods in Computer-Aided Design,
     FMCAD 2015, Austin, Texas, USA, September 27-30, 2015, Roope Kaivola and Thomas Wahl (Eds.). IEEE, 89–96. https:
     //doi.org/10.1109/FMCAD.2015.7542257
[42] Salvatore La Torre, Parthasarathy Madhusudan, and Gennaro Parlato. 2009. Analyzing recursive programs using
     a !xed-point calculus. In Proceedings of the 2009 ACM SIGPLAN Conference on Programming Language Design and
     Implementation, PLDI 2009, Dublin, Ireland, June 15-21, 2009, Michael Hind and Amer Diwan (Eds.). ACM, 211–222.
     https://doi.org/10.1145/1542476.1542500
[43] Salvatore La Torre, Margherita Napoli, and Gennaro Parlato. 2014. A Unifying Approach for Multistack Pushdown
     Automata. In Mathematical Foundations of Computer Science 2014 - 39th International Symposium, MFCS 2014, Budapest,


, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                         29


     Hungary, August 25-29, 2014. Proceedings, Part I (Lecture Notes in Computer Science, Vol. 8634), Erzsébet Csuhaj-Varjú,
     Martin Dietzfelbinger, and Zoltán Ésik (Eds.). Springer, 377–389. https://doi.org/10.1007/978-3-662-44522-8_32
[44] Shuvendu K. Lahiri and Shaz Qadeer. 2008. Back to the future: revisiting precise program veri!cation using SMT
     solvers. In Proceedings of the 35th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL
     2008, San Francisco, California, USA, January 7-12, 2008, George C. Necula and Philip Wadler (Eds.). ACM, 171–182.
     https://doi.org/10.1145/1328438.1328461
[45] Tal Lev-Ami, Neil Immerman, Thomas W. Reps, Mooly Sagiv, Siddharth Srivastava, and Greta Yorsh. 2009. Simulating
     reachability using !rst-order logic with applications to veri!cation of linked data structures. Log. Methods Comput. Sci.
     5, 2 (2009). http://arxiv.org/abs/0904.4902
[46] P. Madhusudan and Gennaro Parlato. 2011. The tree width of auxiliary storage. In Proceedings of the 38th ACM
     SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2011, Austin, TX, USA, January 26-28,
     2011, Thomas Ball and Mooly Sagiv (Eds.). ACM, 283–294. https://doi.org/10.1145/1926385.1926419
[47] P. Madhusudan, Gennaro Parlato, and Xiaokang Qiu. 2011. Decidable logics combining heap structures and data. In
     Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2011, Austin,
     TX, USA, January 26-28, 2011, Thomas Ball and Mooly Sagiv (Eds.). ACM, 611–622. https://doi.org/10.1145/1926385.
     1926455
[48] Zohar Manna and Calogero G. Zarba. 2002. Combining Decision Procedures. In Formal Methods at the Crossroads.
     From Panacea to Foundational Support, 10th Anniversary Colloquium of UNU/IIST, the International Institute for Software
     Technology of The United Nations University, Lisbon, Portugal, March 18-20, 2002, Revised Papers (LNCS, Vol. 2757).
     Springer, 381–422.
[49] Umang Mathur, P. Madhusudan, and Mahesh Viswanathan. 2019. Decidable veri!cation of uninterpreted programs.
     Proc. ACM Program. Lang. 3, POPL (2019), 46:1–46:29. https://doi.org/10.1145/3290359
[50] Umang Mathur, P. Madhusudan, and Mahesh Viswanathan. 2020. What’s Decidable About Program Veri!cation
     Modulo Axioms?. In Tools and Algorithms for the Construction and Analysis of Systems - 26th International Conference,
     TACAS 2020, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2020, Dublin,
     Ireland, April 25-30, 2020, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 12079), Armin Biere and David
     Parker (Eds.). Springer, 158–177. https://doi.org/10.1007/978-3-030-45237-7_10
[51] Umang Mathur, Adithya Murali, Paul Krogmeier, P. Madhusudan, and Mahesh Viswanathan. 2020. Deciding memory
     safety for single-pass heap-manipulating programs. Proc. ACM Program. Lang. 4, POPL (2020), 35:1–35:29. https:
     //doi.org/10.1145/3371103
[52] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021. RustHorn: CHC-based Veri!cation for Rust Programs.
     ACM Trans. Program. Lang. Syst. 43, 4 (2021), 15:1–15:54. https://doi.org/10.1145/3462205
[53] David Monniaux and Laure Gonnord. 2016. Cell Morphing: From Array Programs to Array-Free Horn Clauses. In Static
     Analysis - 23rd International Symposium, SAS 2016, Edinburgh, UK, September 8-10, 2016, Proceedings (Lecture Notes in
     Computer Science, Vol. 9837), Xavier Rival (Ed.). Springer, 361–382. https://doi.org/10.1007/978-3-662-53413-7_18
[54] Adithya Murali, Lucas Peña, Eion Blanchard, Christof Löding, and P. Madhusudan. 2022. Model-guided synthesis
     of inductive lemmas for FOL with least !xpoints. Proc. ACM Program. Lang. 6, OOPSLA2 (2022), 1873–1902. https:
     //doi.org/10.1145/3563354
[55] Adithya Murali, Lucas Peña, Christof Löding, and P. Madhusudan. 2020. A First-Order Logic with Frames. In Program-
     ming Languages and Systems - 29th European Symposium on Programming, ESOP 2020, Held as Part of the European Joint
     Conferences on Theory and Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings (Lecture Notes
     in Computer Science, Vol. 12075), Peter Müller (Ed.). Springer, 515–543. https://doi.org/10.1007/978-3-030-44914-8_19
[56] Huu Hai Nguyen and Wei-Ngan Chin. 2008. Enhancing Program Veri!cation with Lemmas. In Computer Aided
     Veri!cation, 20th International Conference, CAV 2008, Princeton, NJ, USA, July 7-14, 2008, Proceedings (Lecture Notes in
     Computer Science, Vol. 5123), Aarti Gupta and Sharad Malik (Eds.). Springer, 355–369. https://doi.org/10.1007/978-3-
     540-70545-1_34
[57] Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data
     Structures. In Computer Science Logic, 15th International Workshop, CSL 2001. 10th Annual Conference of the EACSL,
     Paris, France, September 10-13, 2001, Proceedings (Lecture Notes in Computer Science, Vol. 2142), Laurent Fribourg (Ed.).
     Springer, 1–19. https://doi.org/10.1007/3-540-44802-0_1
[58] Edgar Pek, Xiaokang Qiu, and P. Madhusudan. 2014. Natural proofs for data structure manipulation in C using
     separation logic. In ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI ’14,
     Edinburgh, United Kingdom - June 09 - 11, 2014, Michael F. P. O’Boyle and Keshav Pingali (Eds.). ACM, 440–451.
     https://doi.org/10.1145/2594291.2594325
[59] Ruzica Piskac, Thomas Wies, and Damien Zu"erey. 2013. Automating Separation Logic Using SMT. In Computer
     Aided Veri!cation - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013. Proceedings
     (Lecture Notes in Computer Science, Vol. 8044), Natasha Sharygina and Helmut Veith (Eds.). Springer, 773–789. https:


                                                                     , Vol. 1, No. 1, Article . Publication date: October 2024.
30                                                                                     Marco Faella and Gennaro Parlato


     //doi.org/10.1007/978-3-642-39799-8_54
[60] Ruzica Piskac, Thomas Wies, and Damien Zu"erey. 2014. Automating Separation Logic with Trees and Data. In
     Computer Aided Veri!cation - 26th International Conference, CAV 2014, Held as Part of the Vienna Summer of Logic, VSL
     2014, Vienna, Austria, July 18-22, 2014. Proceedings (Lecture Notes in Computer Science, Vol. 8559), Armin Biere and
     Roderick Bloem (Eds.). Springer, 711–728. https://doi.org/10.1007/978-3-319-08867-9_47
[61] Nadia Polikarpova and Ilya Sergey. 2019. Structuring the synthesis of heap-manipulating programs. Proc. ACM Program.
     Lang. 3, POPL (2019), 72:1–72:30. https://doi.org/10.1145/3290385
[62] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In 17th IEEE Symposium on
     Logic in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings. IEEE Computer Society,
     55–74. https://doi.org/10.1109/LICS.2002.1029817
[63] Patrick Maxim Rondon, Ming Kawaguchi, and Ranjit Jhala. 2008. Liquid types. In Proceedings of the ACM SIGPLAN
     2008 Conference on Programming Language Design and Implementation, Tucson, AZ, USA, June 7-13, 2008, Rajiv Gupta
     and Saman P. Amarasinghe (Eds.). ACM, 159–169. https://doi.org/10.1145/1375581.1375602
[64] Shmuel Sagiv, Thomas W. Reps, and Reinhard Wilhelm. 1999. Parametric Shape Analysis via 3-Valued Logic. In POPL
     ’99, Proceedings of the 26th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, San Antonio,
     TX, USA, January 20-22, 1999, Andrew W. Appel and Alex Aiken (Eds.). ACM, 105–118. https://doi.org/10.1145/292540.
     292552
[65] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2016. Automated Mutual Explicit Induction
     Proof in Separation Logic. In FM 2016: Formal Methods - 21st International Symposium, Limassol, Cyprus, November 9-11,
     2016, Proceedings (Lecture Notes in Computer Science, Vol. 9995), John S. Fitzgerald, Constance L. Heitmeyer, Stefania
     Gnesi, and Anna Philippou (Eds.). 659–676. https://doi.org/10.1007/978-3-319-48989-6_40
[66] Maarten H. van Emden and Robert A. Kowalski. 1976. The Semantics of Predicate Logic as a Programming Language.
     J. ACM 23, 4 (1976), 733–742.




, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                  31


A    List Removal Example
This appendix reports the source code of one of the case studies from Section 9. This function
removes the !rst node whose data !eld contains a value equal to key, assuming that the pointer
variable head initially points at the head of a singly linked list.

                                          pointer head, prev
                                          int key, value
                                     0 : prev ω head ;
                                      1 : while (head ε nil) do
                                     2:       value ω head ↗ data ;
                                     3:       if (key = value) then
                                     4:            head ω head ↗ next ;
                                     5:            prev ↗ next ω head ;
                                     6:            exit ;
                                              else
                                     7:            prev ω 𝛴𝛩𝑦𝑆 ;
                                     8:            head ω head ↗ next ;
                                              !;
                                          od ;
                                     9 : exit ;

B    Additional Proofs
  L)..# 5.1. For all labels 𝑡, 𝑤 ↑ 𝑈(SK ) and indices 𝑃 ↑ [𝑄 + 𝑞], if there exists a knitted-tree pre!x
where 𝑡 and 𝑤 are the logs of a node and its 𝑃-th child respectively, then consistent_child (𝑤, 𝑃, 𝑡) holds.


   P*&&2. We follow the de!nition of consistent_child presented in Appendix C.4. The
consistent_!rst_frames(𝑤, 𝑃, 𝑡) predicate holds true because it follows the de!nition of the active
and active_child !elds in the !rst frame of every node, as detailed in Sec. 4.3.1. The next two blocks
in the de!nition of consistent_child are responsible for checking that every pair of frames connected
by the prev and next !elds and belonging to di"erent labels encodes a step in the current instruction,
according to the rules detailed in §4.3. The two connected frames may represent a step downward
(!rst block) or upward (second block) in the knitted-tree.
   Consider the downward direction, as the other case is symmetrical. A downward connection
between the frames 𝑡 𝑍 and 𝑤 𝑎 is detected in two cases:
    (1) First, if 𝑡 𝑍 is occupied (i.e., not available), linked to 𝑤 𝑎 through the next !eld, and 𝑤 𝑎 is also
        occupied. Then, we apply the predicate εDown to check that the step is valid. Note that it is
        possible that in a valid knitted-tree 𝑤 𝑎 is available, even though 𝑡 𝑍 .next points to it, but only
        when 𝑡 𝑍 is the last frame of the lace.
    (2) Second, when 𝑤 𝑎 is occupied and linked to 𝑡 𝑍 via its prev !eld. In that case, 𝑡 𝑍 must be
        occupied in any valid knitted-tree, and we again check the correctness of the step using
        εDown .
                                                                                                                     ↭

                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
32                                                                                   Marco Faella and Gennaro Parlato


C Detailed Encoding
In this section, we describe in detail the predicates and functions appearing as constraints in
the CHCs that recognize knitted-trees. Consider again the system of CHCs described in Figure
5. Those CHCs are based on the predicates !rst_frame, start, consistent_child, εInternal , εDown , εUp ,
and label_exit, each described in one of the following sections.

C.1     The First Frame of Non-Root Nodes
The predicate in this section is meant to constrain the !rst frame of every non-root node of a
knitted-tree. The only property to be enforced is a relationship between the !elds active and
active_child: an auxiliary node (active = false) that is not the root must be a leaf of the knitted-tree.
Hence, no allocation of new nodes can be performed in this node. This is enforced by setting the
active_child 𝑄 $ags to true for all indices 𝑃 ↑ [𝑄 + 1, 𝑄 + 𝑞]. Vice versa, all active nodes start with 𝑞
auxiliary children with indices 𝑄 + 1, . . . , 𝑄 + 𝑞, available for allocation. We obtain the following
predicate:
                                             ,            *                                -
                                         def
                          !rst_frame(𝑙 ) = 𝑙 .active ⇑ 𝑄 ↑ [𝑃+1,𝑃+𝑋] ¬𝑙 .active_child 𝑄 △
                                             ,             *                               -
                                               ¬𝑙 .active ⇑ 𝑄 ↑ [𝑃+1,𝑃+𝑋] 𝑙 .active_child 𝑄 .

C.2     The Start of the Lace
The predicate start sets constraints on the !rst two frames at the root of any knitted-tree. These
frames must agree on the !elds active and key. The prev !eld of the second frame points to itself
through the value (→, 2). For non-empty input trees, the !rst frame must be active and the second
frame makes 𝑘! point to the root node, and active_child is non-deterministic on the !rst 𝑄 children,
constraining only the children from index 𝑄 + 1 to 𝑄 + 𝑞 as inactive. For empty input trees, the
!rst frame is inactive and the second frame sets 𝑘! to nil, and active_child requires all children to
be inactive. In both cases, pc 2 is set to the !rst program statement label, with all the other pointer
variables set to nil.


                  def
      start (𝑡) = initial(𝑡) ⇑
                        𝑡.active2 = 𝑡.active1 ⇑ 𝑡.key 2 = 𝑡.key 1 ⇑
                                         *                    2
                        𝑡.pc 2 = 0 ⇑ 𝑆 ↑PV𝐿 \{!   𝑆 } 𝑡.isnil 𝑆 ⇑
                        .,
                           𝑡.active1 ⇑ 𝑡.instr 2 = ↙!   𝑘 ω here∝ ⇑ ¬𝑡.isnil 𝑆2! ⇑      Non-empty input tree
                            *                                   -
                                                              2
                              𝑄 ↑ [𝑃+1,𝑃+𝑋] ¬𝑡.active_child 𝑄 △
                          ,
                            ¬𝑡.active1 ⇑ 𝑡.instr 2 = (&- ⇑ 𝑡.isnil 𝑆2! ⇑                Empty input tree
                            *                               -/
                                                          2
                              𝑄 ↑ [𝑃+𝑋] ¬𝑡.active_child   𝑄    ,

where the initial predicate describes the distinguishing feature of the initial frame of a lace – namely,
having itself as predecessor:

                                    initial(𝑡) = ¬𝑡.avail 2 ⇑ (𝑡.prev 2 = (→, 2)) .
                                                 def




, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                        33


C.3    Lace Termination
The function label_exit (𝑡) returns the exit status of any frame in 𝑡, assuming that at most one
frame in a label is terminal. In the following, we denote by 𝑛 (𝑂) the instruction located at program
counter 𝑂 in the program 𝑛.

                                       def
                    continues(𝑙 ) = ¬𝑙 .avail ⇑ frame_exit (𝑙 ) = 𝑖
                                      
                                       𝑒 if 𝑛 (𝑙 .pc) = exit
                                      
                                      
                                      
                                      𝛬 if 𝑙 .instr = )**
                                      
                                  def
                  frame_exit (𝑙 ) =
                                      
                                       𝛱 if 𝑙 .instr = &&.
                                      
                                      
                                       𝑖 otherwise.
                                      
                                            )         "                                 #
                                      
                                       𝑒 if 𝐿 ↑ [2,𝑀] ¬𝑡.avail𝐿 ⇑ frame_exit (𝑡 𝐿 ) = 𝑒
                                      
                                            )         "                                 #
                                      
                                      
                                      
                                      
                                      
                                        𝛬 if 𝐿 ↑ [2,𝑀] ¬𝑡.avail𝐿 ⇑ frame_exit (𝑡 𝐿 ) = 𝛬
                                                       "                                   #
                                             )
                   label_exit (𝑡) = 𝛱 if 𝐿 ↑ [2,𝑀] ¬𝑡.avail𝐿 ⇑ frame_exit (𝑡 𝐿 ) = 𝛱
                                  def

                                      
                                      
                                      
                                       𝛯 if ¬𝑡.avail𝑀+1
                                      
                                      
                                      
                                       𝑖 otherwise.
                                      
                                  def "                   #
               label_exit (𝑡, Ex) = label_exit (𝑡) ↑ Ex

C.4    Checking Parent-Child Consistency
The consistent_child (𝑤, 𝑃, 𝑡) predicate checks that the label 𝑤 of the 𝑃-th child is consistent with the
label 𝑡 of the parent. It uses the predicates consistent_!rst_frames, εDown , and εUp , de!ned later.

                                      def
       consistent _child (𝑤, 𝑃, 𝑡) = consistent_!rst_frames(𝑤, 𝑃, 𝑡) ⇑
                         Consistency of steps, when going down:
                           + ., "                                                        #
                                              ¬𝑡.avail𝑍 ⇑ 𝑡.next 𝑍 = ( 𝑃, 𝑥) ⇑ ¬𝑤 .avail𝑎 △
                                             "                               #-                              /
                          𝑂↑ [2,𝑃]
                         𝑄↑ [2,𝑃+1]
                                               ¬𝑤 .avail𝑎 ⇑ 𝑤 .prev𝑎 = (′, 𝑦) ↗ εDown (𝑡 ↓𝑍 , 𝑃, 𝑤 <𝑎 , 𝑤 𝑎 ) ⇑

                         Consistency of steps, when going up:
                           + ., "                                                        #
                                              ¬𝑤 .avail𝑍 ⇑ 𝑤 .next 𝑍 = (′, 𝑥) ⇑ ¬𝑡.avail𝑎 △
                                             "                                #-                          /
                          𝑂↑ [2,𝑃]
                         𝑄↑ [2,𝑃+1]
                                               ¬𝑡.avail𝑎 ⇑ 𝑡.prev𝑎 = ( 𝑃, 𝑦) ↗ εUp (𝑤 ↓𝑍 , 𝑃, 𝑡 <𝑎 , 𝑡 𝑎 ) .

   It is worth pointing out that di"erent child labels may be consistent with the same parent label, just
like two di"erent parent labels may be consistent with the same child label. First, consistent_child
only constrain frames that are directly involved in an interaction between parent and child, i.e.,
pairs of frames belonging to these di"erent nodes and adjacent in the lace. Now, consider a pair of
frames that are adjacent in the lace and belong to two di"erent nodes (parent and child). Here is a
description of how consistent_child constrains each !eld in those frames:
 avail: this !eld must be false, because frames involved in an interaction belong to the lace;
 active: this !eld is directly constrained only in the !rst frame of each label, where its value must
      follow the backbone rules described in Section 4.1; this is ensured by the auxiliary predicate

                                                                    , Vol. 1, No. 1, Article . Publication date: October 2024.
34                                                                               Marco Faella and Gennaro Parlato


        consistent_!rst_frames; the value in the subsequent frames of each label is only constrained
        indirectly, by the semantics of the new and free instructions;
 key: the default constraint for this !eld is to have the same value as the preceding frame in the
        same log; the only exception is the last step of the instruction p ↗ data ω exp, when the
        current value of 𝑘 has been ascertained via rewinding: in such a step the value of the key
        !eld of the new frame takes the value of the expression exp;
 pc: the program counter must be consistent with the corresponding pc on the other side of the
        interaction; i.e., the two pc’s must be equal if a rewind operation is ongoing, and otherwise
        the instruction being executed is complete and the pc advances according to the control-$ow
        graph of 𝑛;
 𝑆: the value of this !eld in the two frames of an interaction is the same, except in the last step of
        an instruction of the type 𝑆 ω p ↗ data, when the current value of 𝑘 has been ascertained
        via rewinding;
 upd 𝑆 : the auxiliary predicates ε↔ constrain these !elds to follow the rules described on page 9;
 isnil 𝑆 : this !eld generally keeps its value in an interaction, except in the last step of an assignment
        to 𝑘; speci!cally, it can switch from true to false in the last step of 𝑘 ω 𝑍 or 𝑘 ω q ↗ p!eld,
        when 𝑍 is not nil and rewinding was needed to !nd its current value; moreover, it can switch
        from false to true in the last step of 𝑘 ω q ↗ p!eld, when 𝑍 is not nil, rewinding was needed,
        and then q ↗ p!eld is found to be nil;
 instr: the symbolic instruction in the second frame of an interaction is dictated by the program
        instruction being executed and by the meaning of each symbolic instruction; for example,
        during a rewind process, the symbolic instructions *,!𝐿 and *,!𝐿,𝑆 are used; the end of a
        rewinding may be marked by a symbolic instruction of the types ↙p!eld ω 𝑘∝, ↙p!eld ω nil∝,
        or ↙𝑘 ω here∝; in some cases, the !nal symbolic instruction is simply (&-;
 next and prev: in a pair of interacting frames these !elds must connect the two frames with each
        other; i.e., the next !eld of the !rst frame points to the second frame, and the prev !eld of
        the second frame points to the !rst one.
   The following auxiliary predicates are used within consistent_child. The consistent_!rst_frames
predicate describes the initial value of the active !eld, that starts as true on all nodes of the
knitted-tree that correspond to nodes of the input tree, and false elsewhere.

                                        def "                      #  "                         #
        consistent_!rst_frames(𝑤, 𝑃, 𝑡) = initial(𝑡) △ 𝑡.active1 ⇑ 𝑤 .active1 ↗ 𝑡.active1 ⇑
                                            "                    #
                                              𝑃 > 𝑄 ↗ ¬𝑤 .active1 ⇑ 𝑡.active_child 1𝑄 = 𝑤 .active1 .
   We now present the three predicates that describe the next frame in the lace, depending on
the direction of the next step. The !rst predicate, εInternal , describes internal steps. It invokes the
general predicate step that checks a single step in a lace, passing two adjacent frames from the
same log. In addition, it makes sure that the upd 𝑆 $ags are all false after an internal step, according
to the meaning of those $ags, as described on page 9.
In the following formulas, for a label 𝑡 and a frame 𝑙 we write 𝑡 · 𝑙 to denote the label obtained by
the replacing the !rst available frame of 𝑡 with 𝑙 .

               εInternal (𝑡, 𝑙 ) = len(𝑡, 𝑦) ⇑ continues(𝑡 𝑍 ) ⇑ 𝑡.next 𝑍 = (→, 𝑦 + 1) ⇑
                                 def

                                                                                 *
                                   𝑙 .prev = (→, 𝑦) ⇑ step(𝑡, 𝑦; 𝑡 · 𝑙 , 𝑦 + 1) ⇑ 𝑆 ↑PV𝐿 ¬𝑙 .upd 𝑆 .
   The following predicates εDown and εUp describe the next frame in the lace, when the current
step involves a change of node, either from a node down to its 𝑃-th child or from a node up to its

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                      35


parent. In particular, these predicates constrain the upd $ags in the new frame to respect their
meaning, as described on page 9.
   Consider how the last two lines in εUp (𝑤, 𝑃, 𝑡, 𝑙 ) relate to the intended behavior of the upd $ags.
In that context, 𝑤 𝑍 is a frame in the 𝑃-th child of a parent node with log 𝑡, and the next frame in the
lace is 𝑙 , to be appended on top of 𝑡. Note that in this situation the previous frame in the log of
the parent (i.e., 𝑡 𝑎⇓1 ) is followed in the lace by a frame in the 𝑃-th child. Now, for every pointer
variable 𝑘 ↑ PV𝑊 , the upd 𝑆 $ag when going back to the parent is true i" 𝑘 is not nil at that time
and we observe a marker for an update to 𝑘 within the frames of the child located between the step
down and the step back up. If the update to 𝑘 was performed in one of the frames of the child, the
marker is a direct symbolic instruction of the type ↙𝑘 ω here∝. If instead the update occurs further
below in the subtree rooted in the child, the marker observed in the child is a upd 𝑆 !eld set to true,
as encoded in the last lines of εUp .




      εDown (𝑡, 𝑃, 𝑤, 𝑙 ) = len(𝑡, 𝑦) ⇑ continues(𝑡 𝑍 ) ⇑ 𝑡.next 𝑍 = ( 𝑃, 𝑥) ⇑ len(𝑤, 𝑥 ⇓ 1) ⇑
                        def


                              𝑙 .prev = (′, 𝑦) ⇑ step(𝑡, 𝑦; 𝑤 · 𝑙 , 𝑥) ⇑
                                + .                  ,
                                      𝑙.upd 𝑆 ∋ ¬𝑙.isnil 𝑆 ⇑ 𝑥 > 2 ⇑ 𝑤.next𝑎⇓1 = (′, 𝑦 →) ⇑
                              𝑆 ↑PV𝐿     ,)             "                       #   )                     --/
                                                                 𝑐                                      𝑐
                                                   →
                                             𝑐 ↑ [𝑍 ,𝑍]  𝑡.instr   = ↙𝑘 ω here∝   △        →
                                                                                     𝑐 ↑ [𝑍 +1,𝑍] 𝑡.upd 𝑆

        εUp (𝑤, 𝑃, 𝑡, 𝑙 ) = len(𝑤, 𝑦) ⇑ continues(𝑤 𝑍 ) ⇑ 𝑤 .next 𝑍 = (′, 𝑥) ⇑ len(𝑡, 𝑥 ⇓ 1) ⇑
                        def



                              𝑙 .prev = ( 𝑃, 𝑦) ⇑ step(𝑤, 𝑦; 𝑡 · 𝑙 , 𝑥) ⇑
                                + .                   ,
                                      𝑙.upd 𝑆 ∋ ¬𝑙.isnil 𝑆 ⇑ 𝑥 > 2 ⇑ 𝑡.next𝑎⇓1 = ( 𝑃, 𝑦 →) ⇑
                              𝑆 ↑PV𝐿      ,)             "                        #   )                      --/
                                                                   𝑐                                       𝑐
                                                    →
                                              𝑐 ↑ [𝑍 ,𝑍]  𝑤 .instr   = ↙𝑘 ω here∝   △        →
                                                                                       𝑐 ↑ [𝑍 +1,𝑍] 𝑤 .upd 𝑆     .




C.5    Individual Statements
The predicate step(𝑡, 𝑦; 𝑤, 𝑥) holds if 𝑤 𝑎 is the logically correct frame to follow 𝑡 𝑍 in a lace. The
structure of this predicate comprises an implication for each type of instruction in our programming
language, except for exit. The exit instruction does not produce a step, because just having the




                                                                  , Vol. 1, No. 1, Article . Publication date: October 2024.
36                                                                                                       Marco Faella and Gennaro Parlato


program counter point to it identi!es a terminating execution.



                     def
  step(𝑡, 𝑦; 𝑤, 𝑥) =
       𝑛 (𝑡.pc𝑍 ) = skip                                             ↗ step_skip(𝑡 a, 𝑤 b ) ⇑
       𝑛 (𝑡.pc𝑍 ) = (𝑘 ! nil)                                        ↗ step_assgn_nil(𝑡 a, 𝑤 b , p) ⇑
       𝑛 (𝑡.pc𝑍 ) = (𝑆 ! exp)                                        ↗ step_assgn_exp(𝑡 a, 𝑤 b , d, exp) ⇑
       𝑛 (𝑡.pc𝑍 ) = (𝑆 bool ! (𝑘 = 𝑍))                               ↗ step_assgn_cond (𝑡, a, 𝑤, b, dbool, p, q) ⇑
                𝑍
       𝑛 (𝑡.pc ) = (𝑘 ! 𝑍)                                           ↗ step_assgn_ptr (𝑡, a, 𝑤, b, p, q) ⇑
                𝑍
       𝑛 (𝑡.pc ) = (𝑘 ! q ↗ p!eld)                                   ↗ step_assgn_from_!eld (𝑡, a, 𝑤, b, p, q, p!eld) ⇑
                𝑍
       𝑛 (𝑡.pc ) = (p ↗ p!eld ω 𝑍)                                   ↗ step_assgn_to_!eld (𝑡, a, 𝑤, b, p, q, p!eld) ⇑
                𝑍
       𝑛 (𝑡.pc ) = (p ↗ data ω exp)                                  ↗ step_assgn_to_data(𝑡, a, 𝑤, b, p, exp) ⇑
                𝑍
       𝑛 (𝑡.pc ) = (𝑆 ω p ↗ data)                                    ↗ step_assgn_to_var (𝑡, 𝑦, 𝑤, 𝑥, 𝑆, 𝑘) ⇑
       𝑛 (𝑡.pc𝑍 ) = (new 𝑘)                                          ↗ step_new(𝑡 a, 𝑤 b⇓1, 𝑤 b , p) ⇑
       𝑛 (𝑡.pc𝑍 ) = (free 𝑘)                                         ↗ step_free(𝑡, a, 𝑤, b, p) ⇑
       "
         𝑛 (𝑡.pc𝑍 ) = (while 𝑘 = 𝑍) △
                                 #
         𝑛 (𝑡.pc𝑍 ) = (if 𝑘 = 𝑍)                                     ↗ step_cmp_ptr (𝑡, a, 𝑤, b, p, q, false) ⇑
       "
         𝑛 (𝑡.pc𝑍 ) = (while ¬(𝑘 = 𝑍)) △
                                        #
         𝑛 (𝑡.pc𝑍 ) = (if ¬(𝑘 = 𝑍))                                  ↗ step_cmp_ptr (𝑡, a, 𝑤, b, p, q, true) ⇑
       "
         𝑛 (𝑡.pc𝑍 ) = (while 𝑕 (exp1, . . . , exp𝑌 )) △
                                                   #
         𝑛 (𝑡.pc𝑍 ) = (if 𝑕 (exp1, . . . , exp𝑌 ))                   ↗ step_local_branch(𝑡, 𝑦, 𝑤, 𝑥, 𝑕, exp1, . . . , exp𝑌 ) .


C.5.1 Default Values. Regardless of any speci!c instruction, most !elds in any new frame of the
lace are set to their default values, as described in Section 4.3.2. The following default predicate
represents the full case, where all !elds that have default values are constrained. In the subsequent
predicates, we add subscripts to default to specify which !elds follow the default rules.



                                           def
            default (𝑙 prev , 𝑙 below , 𝑙 ) = ¬𝑙 .avail ⇑                                                       avail
                                                 𝑙 .active = 𝑙 below .active ⇑                                  active
                                                              below
                                                 𝑙 .key = 𝑙        .key ⇑                                       key
                                                 *                    prev
                                                    𝑅 ↑DV 𝐿 𝑙 .𝑆 = 𝑙       .𝑆 ⇑                                 𝑆
                                                 *                          prev
                                                    𝑆 ↑PV𝐿 𝑙 .isnil 𝑆 = 𝑙        .isnil 𝑆 ⇑                     isnil
                                                 𝑙 .instr = (&- ⇑                                               instr
                                                             prev
                                                 𝑙 .pc = 𝑙          .pc ⇑                                       pc
                                                                            prev        below
                                                 default active_child (𝑙           ,𝑙           , 𝑙 ).          active_child


, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                                   37


The default for the active_child $ags requires a little more care:
                                                           def
        default active_child (𝑙 prev , 𝑙 below , 𝑙 ) =
                                                   ,
                                𝑙 .prev = ( 𝑃, ↔) ↗ 𝑙 .active_child 𝑄 = 𝑙 prev .active ⇑
                                                    * "                           below                 #-
                                                       𝑄ε𝐿 𝑙 .active_child 𝐿 =  𝑙       .active_child 𝐿    ⇑
                                                   *           "                                           #
                                𝑙 .prev ε ( 𝑃, ↔) ↗ 𝐿 ↑ [𝑃+𝑋] 𝑙 .active_child𝐿 = 𝑙 below .active_child𝐿 .
C.5.2 Local Instructions. As our !rst type of local instruction, we describe the step_assgn_nil
predicate. As explained earlier, its encoding simply pushes a new frame 𝑙2 on the current node,
with the isnil 𝑆 $ag set to true. All the other !elds of the new frame take their default value, except
the program counter, which advances to the next instruction:
                                                  def
           step_assgn_nil(𝑙1, 𝑙2, 𝑘) = (𝑙1 .next = →) ⇑                                                                       𝑆 ω nil
                                      *
                         𝑙2 .isnil 𝑆 ⇑ 𝑇 ↑PV𝐿 \{𝑆 } (𝑙2 .isnil𝑇 = 𝑙1 .isnil𝑇 ) ⇑
                                 advance_pc(𝑙1, 𝑙2 ) ⇑ default avail,active,key,𝑅,instr,active_child (𝑙1, 𝑙1, 𝑙2 ).
The following auxiliary predicate encodes the advancement of the program counter:
                                               def "                  #
                           advance_pc(𝑙1, 𝑙2 ) = 𝑙2 .pc = succ(𝑙1 .pc) .

Next, we present the predicate that encodes the new instruction. Note that a failed new is only
justi!ed if all children of the current node with position in [𝑄 + 1, 𝑄 + 𝑞] are active (i.e., currently
allocated).
                                     def
     step_new(𝑙 , 𝑙 →, 𝑙 →→, 𝑘) =                                                                                             new 𝑆
                Case 1: Out-of-memory error
                 ,*
                       𝑄 ↑ [𝑃+1,𝑃+𝑋] 𝑙 .active_child 𝑄 ⇑ 𝑙 .next = (→, ↔) ⇑ 𝑙
                                                                                                  →→
                                                                                                       .𝑂𝑔𝛶𝑊𝑕 = &&. ⇑
                                                                                         -
                      default avail,active,key,𝑅,pc,isnil,active_child (𝑙 , 𝑙 →, 𝑙 →→)        △
                Case 2: Normal case
                 ,                  "                                 *                                                     #
                                         ¬𝑙 .active_child 𝑄 ⇑          𝐿 ↑ [𝑃+1,𝑄⇓1] 𝑙 .active_child 𝐿 ⇑ 𝑙 .next = ( 𝑃, ↔)       ⇑
                                               +
                     𝑄 ↑ [𝑃+1,𝑃+𝑋]
                                                          " →→                  #
                     ¬𝑙 →→ .isnil 𝑆 ⇑                      𝑙 .isnil𝑇 = 𝑙 .isnil𝑇 ⇑
                                           𝑇 ↑PV𝐿 \{𝑆 }
                     𝑙 .instr = ↙𝑘 ω here∝ ⇑ 𝑙 →→ .active ⇑ advance_pc(𝑙 , 𝑙 →→) ⇑
                      →→
                                                                     -
                     default avail,key,𝑅,active_child (𝑙 , 𝑙 →, 𝑙 →→) .

The following predicate handles assignments of arbitrary data expressions to data variables.
                                                                 def
                     step_assgn_exp(𝑙1, 𝑙2, 𝑆, exp) =                                                                         𝑅 ω exp
                                   "                       #
                                     𝑙1 .next = (→, ↔) ⇑ 𝑙2 .𝑆 = 𝛩𝑜𝑘 [𝑆 → ▽↗ 𝑙1 .𝑆 →]𝑅 → ↑DV 𝐿 ⇑
                                   *                         →      →
                                      𝑅 → ↑DV 𝐿 \{𝑅 } (𝑙2 .𝑆 = 𝑙1 .𝑆 ) ⇑ advance_pc(𝑙1, 𝑙2 )⇑
                                             default avail,active,key,isnil,instr,active_child (𝑙1, 𝑙1, 𝑙2 ) .

                                                                              , Vol. 1, No. 1, Article . Publication date: October 2024.
38                                                                                                 Marco Faella and Gennaro Parlato


Finally, the following is the straightforward encoding of the skip statement.

                                         def "              #
                    step_skip(𝑙1, 𝑙2, 𝑘) = 𝑙1 .next = (→, ↔) ⇑ advance_pc(𝑙1, 𝑙2 ) ⇑                                      skip

                                                    default avail,active,key,𝑅,isnil,instr,active_child (𝑙1, 𝑙1, 𝑙2 ).

C.5.3 Walking Instructions. A more complex instruction is the assignment of the form 𝑘 ω 𝑍,
which may require rewinding the lace to !nd the node currently pointed by 𝑍. In fact, the encoding
distinguishes three cases: (1) when 𝑍 is nil, (3) when 𝑍 points elsewhere, and we need to start or
keep rewinding the lace, (2) when 𝑍 points to the current node (i.e., the node with label 𝑡). The
predicates governing the rewinding operation are presented later in Section C.7.

                                                                        def
                              step_assgn_ptr (𝑡, 𝑦, 𝑤, 𝑥, 𝑘, 𝑍) =                                                         𝑆 ω𝑇
                                        Case 1: 𝑍 is nil; use the encoding for 𝑘 ω nil
                                        ,                                            -
                                         𝑡 𝑍 .isnil𝑇 ⇑ step_assgn_nil(𝑡 𝑍 , 𝑤 𝑎 , 𝑘)              △
                                        Case 2: 𝑍 points elsewhere; start or keep rewinding
                                        rewind (𝑡, a, 𝑤, b, q)        △
                                        Case 3: 𝑍 points to the current node
                                        ,                                                      -
                                            stop_rewind (𝑡, a, q) ⇑ set_ptr_here(𝑡 𝑍 , 𝑤 𝑎 , 𝑘) .

The auxiliary predicate set_ptr_here pushes a frame on the current node with ↙𝑘 ! here∝ and
updates isnil accordingly.

                                         def "              #
                 set_ptr_here(𝑙1, 𝑙2, 𝑘) = 𝑙1 .next = (→, ↔) ⇑ advance_pc(𝑙1, 𝑙2 ) ⇑
                                                     𝑙2 .instr = ↙𝑘 ! here∝ ⇑
                                                                    *           "                       #
                                                     ¬𝑙2 .isnil 𝑆 ⇑ 𝑇 ↑PV𝐿 \{𝑆 } 𝑙2 .isnil𝑇 = 𝑙1 .isnil𝑇 ⇑
                                                     default avail,active,key,𝑅,active_child (𝑙1, 𝑙1, 𝑙2 ) .

The following predicates encodes the statements of the form p ↗ p!eld ω 𝑍.

                                                                        def
             step_assgn_to_!eld (𝑡, 𝑦, 𝑤, 𝑥, 𝑘, 𝑍, p!eld) = !nd_or_fail(𝑡, 𝑦, 𝑤, 𝑥, 𝑘) △                                  p ↗ p!eld ω 𝑇
                      𝑘 points to the current node:
                       ,                           "                     #
                           stop_rewind (𝑡, a, p) ⇑ 𝑡 𝑍 .next = (→, 𝑦 + 1) ⇑ advance_pc(𝑡 𝑍 , 𝑤 𝑎 ) ⇑
                           𝑤 𝑎 .instr = ↙p!eld ! 𝑍∝ ⇑
                                                                                            -
                           default avail,active,key,𝑅,isnil,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .

   The predicate step_assgn_nil_to_!eld, corresponding to the statements of the form p ↗ p!eld ω
nil, can be obtained from step_assgn_to_!eld by replacing the symbolic instruction ↙p!eld ω 𝑍∝
with ↙p!eld ! nil∝.
   Next, we deal with the two instructions that write or read the data !eld of a node.

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                            39




                                                             def
           step_assgn_to_data(𝑡, 𝑦, 𝑤, 𝑥, 𝑘, exp) = !nd_or_fail(𝑡, 𝑦, 𝑤, 𝑥, 𝑘) △                                      p ↗ data ω exp
                   𝑘 points to the current node:
                    ,                                    "                             #
                        stop_rewind (𝑡, a, p) ⇑ 𝑡 𝑍 .next = (→, 𝑦 + 1) ⇑ advance_pc(𝑡 𝑍 , 𝑤 𝑎 ) ⇑
                                                        
                        𝑤 𝑎 .key = exp 𝑆 ▽↗ 𝑡 𝑍 .𝑆 𝑅 ↑DV 𝐿 ⇑
                                                                                           -
                        default avail,active,𝑅,isnil,instr,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .


                                                       def
           step_assgn_to_var (𝑡, 𝑦, 𝑤, 𝑥, 𝑆, 𝑘) = !nd_or_fail(𝑡, 𝑦, 𝑤, 𝑥, 𝑘) △                                        𝑅 ω p ↗ data
                   𝑘 points to the current node:
                    ,                                    "                             #
                        stop_rewind (𝑡, a, p) ⇑ 𝑡 𝑍 .next = (→, 𝑦 + 1) ⇑ advance_pc(𝑡 𝑍 , 𝑤 𝑎 ) ⇑
                                               *
                        𝑤 𝑎 .𝑆 = 𝑡 𝑍 .key ⇑ 𝑅 → ↑DV 𝐿 \{𝑅 } (𝑤 𝑎 .𝑆 → = 𝑡 𝑍 .𝑆 →) ⇑
                                                                                             -
                        default avail,active,key,isnil,instr,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .

  The following predicate handles the deallocation of the node pointed by a given pointer.


                                          def
             step_free(𝑡, 𝑦, 𝑤, 𝑥, 𝑘) = !nd_or_fail(𝑡, 𝑦, 𝑤, 𝑥, 𝑘) △                                                  free 𝑆
                        𝑘 points to the current node:
                        ,                           "                 #
                            stop_rewind (𝑡, a, p) ⇑ 𝑡 𝑍 .next = (→, ↔) ⇑ advance_pc(𝑡 𝑍 , 𝑤 𝑎 ) ⇑
                            ¬𝑤 𝑎 .active ⇑
                             + ,"                                       #
                                      points_here(𝑡, 𝑦, 𝑍) ↗ 𝑤 𝑎 .isnil𝑇 ⇑
                                     "                                                           #-
                            𝑇 ↑PV𝐿
                                      ¬points_here(𝑡, 𝑦, 𝑍) ↗ 𝑤 𝑎 .isnil𝑇 = 𝑡 𝑍 .isnil𝑇               ⇑
                                                                                      -
                            default avail,key,𝑅,instr,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .

   The following auxiliary predicates handle the search for the current value of a pointer variable
𝑘, including issuing an error if 𝑘 is nil.
                                           ,                              -
                                       def
            !nd_or_fail(𝑡, 𝑦, 𝑤, 𝑥, 𝑘) = 𝑡 𝑍 .isnil 𝑆 ⇑ error (𝑡 𝑍 , 𝑤 𝑎 ) △ rewind (𝑡, a, 𝑤, b, p)
                                               def "              #
                               error (𝑙1, 𝑙2 ) = 𝑙1 .next = (→, ↔) ⇑ (𝑙2 .instr = )**) ⇑
                                                default avail,active,key,𝑅,isnil,pc,active_child (𝑙1, 𝑙1, 𝑙2 ) .

  Next, we move to the instruction that assigns to a Boolean variable the result of the comparison
between two pointers. If at least one of the two pointers is nil, the comparison can be resolved locally.
Otherwise, a rewind operation may be necessary. The auxiliary predicates rewind2, stop_rewind2,

                                                                      , Vol. 1, No. 1, Article . Publication date: October 2024.
40                                                                                              Marco Faella and Gennaro Parlato


and are_equal_a”er_rewind are described in Sec. C.7.
                                                         def
       step_assgn_cond (𝑡, 𝑦, 𝑤, 𝑥, 𝑆 bool, 𝑘, 𝑍) =                                                                    𝑅 bool ω (𝑆 = 𝑇)
                             Case 1: at least one pointer is nil
                             ,"                            #
                               𝑡 𝑍 .isnil 𝑆 △ 𝑡 𝑍 .isnil𝑇 ⇑
                                " 𝑍                     #
                                 𝑡 .next = (→, ↔) ⇑ advance_pc(𝑡 𝑍 , 𝑤 𝑎 ) ⇑
                                             "                                 #
                               𝑤 𝑎 .𝑆 bool = 𝑡 𝑍 .isnil 𝑆 ∋ 𝑡 𝑍 .isnil𝑇 ) ⇑
                                *                      𝑎         𝑍
                                  𝑅 ↑DV 𝐿 \{𝑅 bool } (𝑤 .𝑆 = 𝑡 .𝑆) ⇑
                                                                                 "                 #-
                                default avail,active,key,isnil,instr,active_child 𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎      △

                             Case 2: start or keep rewinding
                             rewind2(𝑡, 𝑦, 𝑤, 𝑥, 𝑘, 𝑍)         △
                             Case 3: stop rewinding
                             ,                                         "                       #
                                 stop_rewind2(𝑡, 𝑦, 𝑘, 𝑍) ⇑ 𝑡 𝑍 .next = (→, ↔) ⇑ advance_pc(𝑡 𝑍 , 𝑤 𝑎 ) ⇑
                                                                                                 #
                                  𝑤 𝑎 .𝑆 bool = are_equal_a”er_rewind (𝑡, 𝑦, 𝑘, 𝑍) ⇑
                                  *                       𝑎        𝑍
                                     𝑅 ↑DV 𝐿 \{𝑅 bool } (𝑤 .𝑆 = 𝑡 .𝑆) ⇑
                                                                                                       -
                                  default avail,active,key,isnil,instr,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .

 The most complex walking instruction is the assignment of the form 𝑘 ω q ↗ p!eld, because it
may involve two consecutive rewinding phases, as explained in Section 4.
                                                                         def
             step_assgn_from_!eld (𝑡, 𝑦, 𝑤, 𝑥, 𝑘, 𝑍, p!eld) =                                                          𝑆 ω q ↗ p!eld
                       Case 1: 𝑍 is nil; null pointer dereference
                       " 𝑍                             #
                        𝑡 .isnil𝑇 ⇑ error (𝑡 𝑍 , 𝑤 𝑎 )         △
                       Case 2a: phase I; 𝑍 points elsewhere; start or keep rewinding
                       " 𝑍                                         #
                        𝑡 .instr ε *,!↔,↔ ⇑ rewind (𝑡, a, 𝑤, b, q)                   △
                       Case 2b: phase II; 𝑕 points elsewhere; start or keep rewinding
                       " 𝑍                                                   #
                        𝑡 .instr = *,!𝐿,𝑉 ⇑ rewind_special(𝑡, 𝑦, 𝑤, 𝑥, 𝑕, 𝑂)                     △
                       Case 3a: end of phase I; 𝑍 points to the current node
                       
                        𝑡 𝑍 .instr ε *,!↔,↔ ⇑ stop_rewind (𝑡, a, q) ⇑
                        ,"
                           is_p!eld_nil(𝑡, 𝑦, p!eld)△
                                                                                                 #
                            (is_p!eld_implicit (𝑡, 𝑦, p!eld) ⇑ ¬𝑡 𝑍 .active_child index (p!eld) ) ↗
                                                              -
                                step_assign_nil(𝑡 𝑍 , 𝑤 𝑎 , 𝑘) ⇑
                           ,"                                                                  #
                              is_p!eld_implicit (𝑡, 𝑦, p!eld) ⇑ 𝑡 𝑍 .active_child index (p!eld) ↗
                                " 𝑍
                                 𝑡 .next = (index (p!eld), 𝑥) ⇑ advance_pc(𝑡 𝑍 , 𝑤 𝑎 ) ⇑

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                           41


                            𝑤 𝑎 .instr = ↙𝑘 ! here∝ ⇑
                                                                                              #-
                             default avail,active,key,𝑅,isnil,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) ⇑
                         +            ,"                                                         #
                                         is_p!eld_ptr (𝑡, 𝑦, p!eld, 𝑕, 𝑂) ⇑ points_here(𝑡, 𝑂, 𝑕 ) ↗
                    𝑉 ↑PV𝐿 ,𝐿 ↑ [2,𝑀]                                  -
                                        set_ptr_here(𝑡 𝑍 , 𝑤 𝑎 , 𝑘) ⇑
                         +            ,"                                                           #
                                         is_p!eld_ptr (𝑡, 𝑦, p!eld, 𝑕, 𝑂) ⇑ ¬points_here(𝑡, 𝑂, 𝑕 ) ↗
                                                                                  
                    𝑉 ↑PV𝐿 ,𝐿 ↑ [2,𝑀]
                                                                               -
                                        rewind_special(𝑡, 𝑦, 𝑤, 𝑥, 𝑕, 𝑂)              △

                    Case 3b: end of phase II; 𝑕 points to the current node
                    ,                                                                         -
                     𝑡 𝑍 .instr = *,!𝐿,𝑉 ⇑ points_here(𝑡, 𝑂, 𝑕 ) ⇑ set_ptr_here(𝑡 𝑍 , 𝑤 𝑎 , 𝑘) .




  The following auxiliary predicates check the value of the node !eld p!eld at (𝑡, 𝑦).


              p!eld is nil at the frame (𝑡, 𝑦) of the lace:
                                           def
              is_p!eld_nil(𝑡, 𝑦, p!eld) =
                       ,                                                 +                                     -
                            𝑡 𝐿 .instr = ↙p!eld ω nil∝ ⇑                             𝑡 𝑄 .instr ε ↙p!eld ω ↔∝
                      𝐿 ↑ [2,𝑍]                                        𝑄 ↑ [𝐿+1,𝑍]

              p!eld has the same value as 𝑕 at the frame (𝑡, 𝑦) of the lace:
                                                 def
              is_p!eld_ptr (𝑡, 𝑦, p!eld, 𝑕, 𝑂) =
                                                           +
                      𝑡 𝐿 .instr = ↙p!eld ω 𝑕 ∝ ⇑                     𝑡 𝑄 .instr ε ↙p!eld ω ↔∝
                                                        𝑄 ↑ [𝐿+1,𝑍]

              p!eld has never been assigned up to the frame (𝑡, 𝑦) of the lace:
                                                  def
                                                          +
              is_p!eld_implicit (𝑡, 𝑦, p!eld) =                     𝑡 𝑄 .instr ε ↙p!eld ω ↔∝ .
                                                        𝑄 ↑ [2,𝑍]




C.6    Boolean Conditions and Control Flow Instructions
Control-$ow statements if and while have two successors, depending on the value of their Boolean
condition. To support those statements, we introduce a 3-argument version of the predicate that
advances the program counter:


                                                  def "                        #
                         advance_pc(𝑙1, 𝑙2, cond) = 𝑙2 .pc = succ(𝑙1 .pc, cond) .


                                                                       , Vol. 1, No. 1, Article . Publication date: October 2024.
42                                                                                                  Marco Faella and Gennaro Parlato


The next predicate handles the Boolean conditions of the form 𝑘 = 𝑍:
                                                            def
           step_cmp_ptr (𝑡, 𝑦, 𝑤, 𝑥, 𝑘, 𝑍, neg) =                                                                          if 𝑆 = 𝑇
                             Case 1: at least one pointer is nil
                             ,"                          #  "                     #
                               𝑡 𝑍 .isnil 𝑆 △ 𝑡 𝑍 .isnil𝑇 ⇑ 𝑡 𝑍 .next = (→, 𝑦 + 1) ⇑
                                      advance_pc(𝑡 𝑍 , 𝑤 𝑎 , xor(neg, 𝑡 𝑍 .isnil 𝑆 ∋ 𝑡 𝑍 .isnil𝑇 )) ⇑
                                                                                         "                 #-
                                      default avail,active,key,𝑅,isnil,instr,active_child 𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎    △

                             Case 2: start or keep rewinding
                             rewind2(𝑡, 𝑦, 𝑤, 𝑥, 𝑘, 𝑍)                △
                             Case 3: stop rewinding
                             ,                                         "                              #
                                 stop_rewind2(𝑡, 𝑦, 𝑘, 𝑍) ⇑ 𝑡 𝑍 .next = (→, 𝑦 + 1) ⇑
                                                "                                                          #
                                 advance_pc 𝑡 𝑍 , 𝑤 𝑎 , xor(neg, are_equal_a”er_rewind (𝑡, 𝑦, 𝑘, 𝑍)) ⇑
                                                                                                        -
                                 default avail,active,key,𝑅,isnil,instr,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .
The next predicate handles the Boolean conditions based on the content of the data variables. Those
conditions can always be resolved locally.
                                                                  def
     step_local_branch(𝑙1, 𝑙2, 𝑕, exp1, . . . , exp𝑌 ) =                                                 if
                      "                      #                                                           𝑉 (exp1 , . . . , exp𝑅 )
                        𝑙1 .next = (→, ↔) ⇑
                                     "                                                                   #
                      advance_pc 𝑙1, 𝑙2, 𝑕 (exp1 [𝑆 ▽↗ 𝑙1 .𝑆]𝑅 ↑DV 𝐿 , . . . , exp𝑌 [𝑆 ▽↗ 𝑙1 .𝑆]𝑅 ↑DV 𝐿 ) ⇑
                            default avail,active,key,𝑅,isnil,instr,active_child (𝑙1, 𝑙1, 𝑙2 ) .

C.7 Rewinding the Lace
The following predicate is true when the pointer 𝑍 is not nil at (𝑡, 𝑦) and its value cannot be
ascertained by analyzing the label 𝑡 alone. In that case, it is necessary to perform at least one
rewinding step, represented by the frame (𝑤, 𝑥).
                                                 def
                  rewind (𝑡, 𝑦, 𝑤, 𝑥, 𝑍) =
                           𝑡 𝑍 .next = (dir, 𝑥) ⇑ ¬𝑡 𝑍 .isnil𝑇 ⇑ 𝑦 → = cur_rewind_pos(𝑡, 𝑦) ⇑
                           ¬points_here(𝑡, 𝑦 →, 𝑍) ⇑ 𝑦 →→ = last_upd (𝑡, 𝑦 →, 𝑍) ⇑
                                 →→                               →
                           𝑡 𝑍 .prev = (dir, 𝑥 →) ⇑ 𝑤 𝑎 .next = (dir →, 𝑦 →→) ⇑
                           𝑥 = last_visit (𝑤, dir →, 𝑦 →) + 1 ⇑ 𝑤 𝑎 .instr = *,!𝑎 → ⇑
                           default avail,active,pc,key,𝑅,isnil,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .

   The above predicate uses several auxiliary functions and predicates. The function cur_rewind_pos(𝑡, 𝑦)
returns the position within 𝑡 of the current rewinding. If the rewinding is just starting, this position
will simply be 𝑦. Otherwise, the current instruction will be of the type *,!𝑎 , and the current
rewinding position will be 𝑥.
                                           (
                                       def  𝑥 if 𝑡 𝑍 .instr = *,!𝑎 for some 𝑥 ↑ [𝑔],
                cur_rewind_pos(𝑡, 𝑦) =
                                            𝑦 otherwise.

, Vol. 1, No. 1, Article . Publication date: October 2024.
Automated Verification of Tree-Manipulating Programs Using Constrained Horn Clauses                                                            43


                                        𝑍→→                                    𝑍→                         𝑍
                       𝑡    ...     upd𝑁 = true             ...         instr = (&-          ...    instr = *,!𝑂→      ...



                                          𝑤     ...                      ...                instr = *,!𝑄 →      ...

                                                            𝑎→                  𝑎 ⇓1               𝑎

Fig. 9. An example of the rewind (𝑡, 𝑦, 𝑤, 𝑥, 𝑍) predicate. Arrows connect a frame to its successor in the lace.



The predicate points_here(𝑡, 𝑦, 𝑍) holds when 𝑍 points to the node labeled with 𝑡 when the lace is
at (𝑡, 𝑦). This occurs when an instruction of the type ↙𝑍 ω here∝ is found in 𝑡 at position at most
𝑦, and all upd𝑇 $ags from that position to position 𝑦 are false.

                                              def
                                                       ,                          +           -
                points_here(𝑡, 𝑦, 𝑍) =                   𝑡 𝐿 .instr = ↙𝑍 ω here∝ ⇑   ¬𝑡 𝑄 .upd𝑇 .
                                                    𝐿 ↑ [2,𝑍]                                           𝑄 ↑ [𝐿+1,𝑍]


When the value of pointer 𝑍 cannot be ascertained by the current label 𝑡, we search for its most
recent assignment by identifying the latest position in 𝑡 that comes before position 𝑦 and contains
the $ag upd𝑇 = true. This is the job of the function last_upd (𝑡, 𝑦, 𝑍). If no position in 𝑡 before 𝑦
contains upd𝑇 = true, this function returns 2, because in that case the rewinding operation must go
back to the frame that lead to the !rst visit to the current node.
                           (
                       def   max{𝑂 ↑ [2, 𝑦] | 𝑡 𝐿 .upd𝑇 = true} if {𝑂 ↑ [2, 𝑦] | 𝑡 𝐿 .upd𝑇 = true} ε ⇐
    last_upd (𝑡, 𝑦, 𝑍) =
                             2                                  otherwise.

The last auxiliary function, last_visit (𝑤, dir, 𝑃), returns the position of the last frame from 𝑤 whose
next !eld is of the form (dir, 𝑚) for some 𝑚 ↓ 𝑃.

                     last_visit (𝑤, dir, 𝑃) = max{𝑂 ↑ [𝑔] | 𝑤 𝐿 .next = (dir, 𝑚), 𝑚 ↓ 𝑃 } .
                                                     def




C.7.1 Searching for Two Pointers. We describe a variant of the predicate rewind, for the instructions
that search for two di"erent pointers at the same time. In fact, this only happens in the encoding of
the Boolean condition 𝑍 1 = 𝑍 2 .

                                                                  def
                      rewind2(𝑡, 𝑦, 𝑤, 𝑥, 𝑍 1, 𝑍 2 ) =
                                  𝑡 𝑍 .next = (dir, 𝑥) ⇑ ¬𝑡 𝑍 .isnil𝑇1 ⇑ ¬𝑡 𝑍 .isnil𝑇2 ⇑
                                  𝑦 → = cur_rewind_pos(𝑡, 𝑦) ⇑
                                  ¬points_here(𝑡, 𝑦 →, 𝑍 1 ) ⇑ ¬points_here(𝑡, 𝑦 →, 𝑍 2 ) ⇑
                                            $                                                %
                                  𝑦 →→ = max last_upd (𝑡, 𝑦 →, 𝑍 1 ), last_upd (𝑡, 𝑦 →, 𝑍 2 ) ⇑
                                     →→                                             →
                                  𝑡 𝑍 .prev = (dir, 𝑥 →) ⇑ 𝑤 𝑎 .next = (dir →, 𝑦 →→) ⇑
                                  𝑥 = last_visit (𝑤, dir →, 𝑦 →) + 1 ⇑ 𝑤 𝑎 .instr = *,!𝑎 → ⇑
                                  default avail,active,pc,key,𝑅,isnil,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .


                                                                                        , Vol. 1, No. 1, Article . Publication date: October 2024.
44                                                                                              Marco Faella and Gennaro Parlato


Next, the version of rewinding used by the second phase of the statement 𝑘 ω q ↗ p!eld.
                                                                  def
                     rewind_special(𝑡, 𝑦, 𝑤, 𝑥, 𝑕, 𝑦 →) =
                                        𝑡 𝑍 .next = (dir, 𝑥) ⇑ ¬𝑡 𝑍 .isnil𝑉 ⇑
                                        ¬points_here(𝑡, 𝑦 →, 𝑕 ) ⇑ 𝑦 →→ = last_upd (𝑡, 𝑦 →, 𝑕 ) ⇑
                                           →→                               →
                                        𝑡 𝑍 .prev = (dir, 𝑥 →) ⇑ 𝑤 𝑎 .next = (dir →, 𝑦 →→) ⇑
                                        𝑥 = last_visit (𝑤, dir →, 𝑦 →) + 1 ⇑ 𝑤 𝑎 .instr = *,!𝑎 →,𝑉 ⇑
                                        default avail,active,pc,key,𝑅,isnil,active_child (𝑡 𝑍 , 𝑤 𝑎⇓1, 𝑤 𝑎 ) .
  The following predicates check whether the search for one or two pointers is !nished because
those variables point to the current node (i.e., the node with label 𝑡):
                                                      def
                       stop_rewind (𝑡, 𝑦, 𝑍) = ¬𝑡 𝑍 .isnil𝑇 ⇑ 𝑦 → = cur_rewind_pos(𝑡, 𝑦) ⇑
                                                            points_here(𝑡, 𝑦 →, 𝑍)
                                                      def
                stop_rewind2(𝑡, 𝑦, 𝑍 1, 𝑍 2 ) = stop_rewind (𝑡, 𝑦, 𝑍 1 ) △ stop_rewind (𝑡, 𝑦, 𝑍 2 ).
  The following predicate is used by the instructions that have already searched for two pointers
and want to check whether they are equal.
                                                def
are_equal_a”er_rewind (𝑡, 𝑦, 𝑘, 𝑍) =
                               𝑦 → = cur_rewind_pos(𝑡, 𝑦) ⇑ points_here(𝑡, 𝑦 →, 𝑘) ⇑ points_here(𝑡, 𝑦 →, 𝑍) .




, Vol. 1, No. 1, Article . Publication date: October 2024.
