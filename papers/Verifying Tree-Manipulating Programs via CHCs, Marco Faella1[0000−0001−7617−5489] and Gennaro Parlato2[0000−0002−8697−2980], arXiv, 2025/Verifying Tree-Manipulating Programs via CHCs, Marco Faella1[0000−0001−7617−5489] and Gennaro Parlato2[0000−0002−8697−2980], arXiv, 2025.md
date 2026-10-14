                                         Verifying Tree-Manipulating Programs via CHCs

                                          Marco Faella1[0000−0001−7617−5489] and Gennaro Parlato2[0000−0002−8697−2980]
                                                               1
                                                                   University of Naples Federico II, Italy
                                                                           m.faella@unina.it
                                                                      2
                                                                        University of Molise, Italy
                                                                     gennaro.parlato@unimol.it
arXiv:2505.14092v1 [cs.PL] 20 May 2025




                                               Abstract. Programs that manipulate tree-shaped data structures of-
                                               ten require complex, specialized proofs that are difficult to generalize
                                               and automate. This paper introduces a unified, foundational approach
                                               to verifying such programs. Central to our approach is the knitted-tree
                                               encoding, modeling each program execution as a tree structure captur-
                                               ing input, output, and intermediate states. Leveraging the compositional
                                               nature of knitted-trees, we encode these structures as constrained Horn
                                               clauses (CHCs), reducing verification to CHC satisfiability task. To illus-
                                               trate our approach, we focus on memory safety and show how it naturally
                                               leads to simple, modular invariants.


                                         1   Introduction

                                         Ensuring automatic or semi-automatic verification of programs that manipulate
                                         dynamic memory (heaps) presents numerous challenges. First, heaps can grow
                                         unboundedly in size and store unbounded data, requiring expressive logics to cap-
                                         ture intricate invariants, preconditions, and postconditions. Next, dynamic shape
                                         changes complicate the maintenance of structural constraints, such as binary
                                         search tree ordering or balance. Aliasing further obscures these constraints and
                                         breaks invariants. Unbounded recursion and loops, common in tree algorithms,
                                         add complexity by making termination reasoning non-trivial. Finally, incomplete
                                         or missing specifications often force verifiers to infer properties on-the-fly, and
                                         integrating various verification techniques (e.g., SMT-solving, abstract interpre-
                                         tation, and interactive theorem proving) remains a nontrivial task.
                                             This paper presents a foundational approach for automated analysis of heap-
                                         manipulating programs, particularly those involving tree data structures. By
                                         combining automata and logic-based methods, we reduce verification to checking
                                         satisfiability of constrained Horn clauses (CHCs). This reduction allows us to
                                         capitalize on advancements in CHC solvers [16,3]. We demonstrate our approach
                                         on the memory safety problem, ensuring that no execution causes crashes (e.g.,
                                         null-pointer dereferences, use-after-free, or illegal frees) or nontermination.
                                             The core of our methodology maps an entire program execution π on an
                                         input data tree T into a single tree data structure called a knitted-tree. This
                                         structure encapsulates the input, output, and all intermediate configurations of
                                         π. Its underlying tree, or backbone, is derived from T by adding a fixed number
2       M. Faella and G. Parlato

of inactive nodes to allow dynamic node allocation. Each node is labeled by a
sequence of records, or frames, connected in a global linear sequence called the
lace, where consecutive frames may belong to the same node or adjacent nodes,
resembling a knitting tree. Each frame describes changes to the associated node
(e.g., pointer updates) and records the current program state, preserving the
backbone’s original structure while also representing the final heap that may
differ graph-wise. However, the knitted-tree’s parameters – the number of extra
nodes added to the backbone and the number of frames per node – may not
capture every possible execution, potentially excluding some from our analysis.

     pointer head, prev , cur , tmp             Example. We illustrate our encoding
     int key                                    method with a simple program shown
 0 : cur := head ;                              in Fig. 1 that manipulates a singly
 1 : while (cur ̸= nil && cur → val ̸= key) do  linked list, specifically designed to high-
 2 :       tmp := cur → next ;                  light the key features of our encoding
 3 :       cur → next := prev ;
                                                methodology. The program takes a list
 4 :       prev := cur ;
                                                of integers with head pointing to the
 5 :       cur := tmp ;
      od ;
                                                first node and a value stored in key. It
 6 : if (cur ̸= nil) then We found the key
                                                reverses the list up to and including the
 7 :       tmp := cur → next ;                  first node containing the key, then ap-
 8 :       head → next := tmp ; Rewind for head pends the remaining nodes. For exam-
 9 :       head  := cur ; Rewind for cur        ple, given the input list 1 →2 →3 →4
      else                                      →5 and key = 3, the output list is: 3
10 :       head := prev ;                       →2 →1 →4 →5. The knitted-tree corre-
      fi ;                                      sponding to this program execution is
11 : exit ;                                     shown in Fig. 2.
     Fig. 1: Running example.                       The knitted-tree’s structure matches
                                                the input list. The label of each node is
displayed next to it, with the lace being depicted by red arrows and numbers.
In our example, the lace starts at the frame with ordinal 1 of node u1 , takes
two local steps to the frames with ordinals 2 and 3, then moves to the frame
numbered 4 in node u2 , and so on. Note that consecutive frames in the lace
either belong to the same node, or to adjacent nodes. Due to space constraints,
only a selection of the information contained within each frame is displayed.
Our encoding’s main innovation is how it handles pointer fields and variables:
 1. an update to a pointer field is stored in its node;
 2. an update to a pointer variable is stored in the node it points to.
For example, the lace’s first frame includes the event ⟨head := here⟩, indicat-
ing that head initially points to the first node of the input structure. This ini-
tial assignment is implicit. The second frame corresponds to the execution of
cur := head at line 0. According to rule 2, when a pointer is dereferenced, it
may be necessary to traverse the lace backward to find its latest assignment,
a process called rewinding. In our example, the first rewinding occurs at line 8
when the current value of head is needed. In the knitted-tree, frame 15 in node
u4 reaches line 8, but since the label of u4 does not contain information about
                                    Verifying Tree-Manipulating Programs via CHCs                            3

                           1             2         3          5              6             18
          val : 1       pc : 0        pc : 1     pc : 2    pc : 4         pc : 5          pc : 9
 u1                    key : 3     ⟨cur := here⟩        ⟨next := nil⟩ ⟨prev := here⟩ ⟨next := tmp⟩
                    ⟨head := here⟩                        upd tmp                    upd tmp,cur ,prev
            1              2              3         4          5              6                  7




                          4             7         8          10              11           17       19
          val : 2      pc : 3        pc : 1     pc : 2     pc : 4          pc : 5       pc : 8    pc : 9
 u2                 ⟨tmp := here⟩ ⟨cur := here⟩        ⟨next := prev ⟩ ⟨prev := here⟩   rwd2      rwd7
                                    upd prev              upd tmp                     upd tmp,cur
            1             2              3          4          5               6             7           8




                          9             12       13     14      16       20
          val : 3      pc : 3        pc : 1     pc : 6 pc : 7 pc : 8   pc : 11
 u3                 ⟨tmp := here⟩ ⟨cur := here⟩                rwd2 ⟨head := here⟩
                                    upd prev                  upd tmp
            1             2              3          4     5        6          7



                         15
 u4       val : 4      pc : 8
                    ⟨tmp := here⟩
            1             2



 u5       val : 5
            1



Fig. 2: A knitted-tree of the program in Fig. 1 on the input list 1 →2 →3 →4
→5 and key = 3. Blue numbers below the frames represent positions within the
label, while red numbers and arrows refer to the lace.



head , rewinding is triggered. Frames 16 and 17 are then added to the lace to go
back to node u1 , where head currently points, and frame 18 in u1 reports the
effect of the instruction at line 8, consisting in the event ⟨next := tmp⟩.

    Knitted-trees enjoy compositional properties that are essential for our
CHC-based verification method. These properties allow subtree replacement: a
subtree rooted at node v in one knitted-tree can be swapped with a subtree
rooted at node v ′ in another, provided that the labels of v and v ′ satisfy a lo-
cal consistency condition expressible in a quantifier-free first-order data theory.
This replacement rule enables us to build a CHC system whose minimal model
precisely captures the set of valid node labels for the knitted-trees, allowing the
detection of any reachable error configuration during execution. If our analysis
reports no errors, we need to check whether any execution was truncated by the
current choice of parameters. With a small modification, the same CHC system
can also reveal whether that is the case; if so, we can increase the parameters
to encompass more executions. While verification is undecidable and may not
terminate, our method significantly broadens the class of programs and prop-
erties amenable to automation. In particular, executions of several well-known
programs are fully captured by knitted-trees with suitable parameters, as they
traverse nodes a bounded number of times and admit simple CHC solutions.
4       M. Faella and G. Parlato

Organization of the paper. The rest of the paper is structured as follows. Section 2
introduces notation and definitions. Section 3 defines the knitted-tree encoding,
and Section 4 details its compositionality. Section 5 describes our reduction to
the CHC satisfiability problem, presents a sound procedure to solve the mem-
ory safety problem, and analyzes the structure and complexity of the required
invariants. Section 6 reviews related work, and Section 7 concludes with future
directions. The appendices include substantial supplementary material.


2    Preliminaries
                                                               def
Let N denote the natural numbers that include 0, [i, j] = {k ∈ N | i ≤ k ≤ j},
        def
and [j] = [1, j].

Trees. A k-ary tree T is a finite, prefix-closed subset of [k]∗ , where k ∈ N. Each
element in T is a node, with the root represented by the empty string ε. The tree
edge relation is implicit: for any d ∈ [k], if both v and v .d are nodes in T , then
(v , v .d ) is an edge, making v .d the dth child of v , and v the parent of v .d .
Data signatures. A data signature S consists of pairs {id i : type i }i∈[n] , defining
field names and their types (e.g., integers, Booleans B). An evaluation ν of S
assigns each field name id a type-specific value, denoted ν.id . The language of
S, L(S), is the set of all its evaluations.
Data trees. A data tree with data signature S, or S-tree, is a pair (T, λ) where
T is a tree and λ is a labeling function λ : T → L(S) that assigns an evaluation
of S to each node t ∈ T . To simplify notation, the value of a field id at node t
can be written as t.id when λ is clear from the context.
Constrained Horn clauses. We use standard first-order logic (FOL) with equal-
ity [45] and formulas from a many-sorted, quantifier-free first-order theory D
that includes program-relevant data types like arithmetic, reals, and arrays. We
refer to D as the data theory.

Definition 1. Let R be a set of uninterpreted fixed-arity relation symbols rep-
resenting unknowns. A constrained Horn clause (CHC) is a formula of the
form H ← C ∧ B1 ∧ · · · ∧ Bn where: (i) C is a constraint, a formula of the data
theory D without symbols from R; (ii) each Bi is an application r(v1 , . . . , vk ) of
a relation symbol r ∈ R to first-order variables v1 , . . . , vk ; (iii) H (the head) is
either false, or an application r(v1 , . . . , vk ) as in Bi . A CHC is a fact if its body
is only C and a query if its head is false. A finite set C of CHCs forms a system
by conjoining all CHCs with free variables universally quantified. We assume the
constraint semantics is predefined as a structure.                                       ⊔
                                                                                         ⊓

A CHC system S with relation symbols R is satisfiable if there exists an interpre-
tation for each r ∈ R that makes all clauses in S valid. Any such interpretation
is called a solution of S. The CHC satisfiability problem is the computational
task of determining whether a given system S of CHCs is satisfiable.
                              Verifying Tree-Manipulating Programs via CHCs                 5

   Each CHC system S has a unique minimal model under subset ordering,3
computable as the fixed-point of an operator derived from its clauses [19,35]. We
use this fixed-point semantics to ensure the correctness of our reductions.


Heap-manipulating Programs. The heap is essential for dynamic memory
allocation, allowing memory blocks (nodes) to be allocated and deallocated dur-
ing execution. We assume that nodes have a single data field and one or more
pointer fields. A specific heap state is defined as follows.

Definition 2. A heap is a tuple H = (N, S, data, PF ) where

 – N is a finite set of nodes, including a unique element nil for free memory.
 – S is a data signature defining the type of data that can be stored in a node.
 – data : N \ {nil} → L(S) is a map modeling the data field of each node.
 – PF is a finite sequence of distinct pointer fields, each defined as a function
   of type (N \ {nil}) → N , representing the pointers of each node.            ⊔
                                                                                ⊓

   We define k as the number of pointer fields. For example, in Fig. 1, PF =
{next} and k = 1, while for binary trees use PF = {left, right} and k = 2.
Syntax. The syntax of
                                          def
our programming lan-           Program = decl block
                                          def
guage is shown on the                                             ∗ ∗
                                     decl = (pointer id(,id) ) (type id(,id) )
                                                                                 ∗ ∗

right. Programs begin                     def
                                    block = (pc : (ctrl_stmt | heap_stmt) ; )
                                                                                 +

with declarations of                      def
                               ctrl_stmt = d := exp | dbool := heap_cond | skip | exit
pointer and data vari-
                                              | if cond then block else block fi
ables, followed by la-                        | while cond do block od | goto pc
beled instructions. In-                   def
                              heap_stmt = new p | free p | p := nil | p := q | p := q → pfield
structions include as-
                                              | p → pfield := nil | p → pfield := q
signments, control flow,
                                              | p → dfield := exp | d := p → dfield
and heap operations.                      def
                                      exp = d | f (exp, . . . , exp)
Data assignments are
                                          def
of the form d := exp,               cond = r(exp, . . . , exp) | (¬)? heap_cond
where d is a data vari-                   def
                              heap_cond = p = q | p = nil | p → pfield = q | p → pfield = nil
able set to the value of
the data expression exp. Data expressions are built from data variables and com-
bined using function symbols of the data theory D. Control flow instructions in-
clude skip, exit, if-then-else statements, and while loops. Boolean conditions
(cond ) are exclusively either data conditions or heap conditions. Heap conditions
can be assigned to a Boolean variable with dbool := heap_cond , integrating them
into Boolean theory. Heap operations include new p (creates a new node, ini-
tializes its fields to undefined or nil, and assigns it to p) and free p (deallocates
the node pointed by p and sets all pointers pointing to the node to nil). We
also allow assignment and retrieval of pointer fields (i.e., pfield ∈ PF ) and data
fields (i.e., dfield ∈ S). Programs are valid if they are well-formed, type-correct,
3
    See [19] for logic programs and [35, Prop. 4.1] for constr. logic programs (or CHCs).
6         M. Faella and G. Parlato

uniquely labeled, and terminate with exit. Fig. 1 shows an example of a pro-
gram.4 For a program P , PC P , PV P , and DV P represent program counters,
pointer variables, and data variables, respectively. The function succ defines the
successor(s) of a program counter. Statements can have from 0 to 2 successors:
most statements have a single successor, denoted by succ(pc); the exit state-
ment has no successor; if-then-else and while have two successors based on
a Boolean condition: succ(pc, true) and succ(pc, false). The language does not
support function calls directly: non-recursive calls are inlined, and limited re-
cursion, typical in tree-based algorithms, can be simulated (see Appendix A for
details).
Semantics. A program P operates on a specialized heap called a P -heap, that
includes all its pointers and data. A configuration of P is a tuple (H, νp , νd , pc)
consisting of a P -heap, an evaluation of the pointer variables, an evaluation of
the data variables, and next instruction label. Focusing on tree-based programs,
a configuration c is initial if it meets the following conditions:

    – H is isomorphic to a data tree T via a bijection ρ that maps each node in
      H to a node in T , such that for all nodes x, y in H and i ∈ |PF |, y = pfi (x)
      iff ρ(y) = ρ(x).i, where pfi is the i-th pointer field in PF . We refer to T as
      the data tree of c, and may use T in place of H.
    – νp maps the first pointer variable declared in P , conventionally denoted by
      pb, to the H node corresponding to the root of T and maps the other pointer
      variables to nil.
    – νd assigns each variable a non-deterministic value.
    – pc is the label of the first statement in P .

    A transition c →P c′ in P occurs by executing the instruction at pc using
standard semantics unless noted otherwise. If pc is an exit statement, c becomes
a final configuration with no further transitions. Attempting to dereference or
deallocate a nil pointer makes c an error configuration. An execution π of P
is a (possibly infinite) sequence of configurations c0 c1 . . . where: (i) c0 is initial,
and (ii) ci−1 →P ci for each i ∈ N. A finite π that ends in a final or error
configuration is a terminating or buggy execution, respectively. We aim to solve
the following (undecidable) problem:

Problem 1. A program P is memory safe if all its executions terminate without
reaching an error configuration. The memory safety problem asks whether a
given program is memory safe.


3      Knitted-Trees: Representing Executions as Data Trees

Our approach to solving the memory safety problem uses the knitted-tree encod-
ing, which models a program execution as a single data tree capturing inputs,
outputs, and intermediate configurations.
4
    The while condition goes beyond our syntax but is easily translatable into it.
                                   Verifying Tree-Manipulating Programs via CHCs              7

    We first fix notation and assumptions. The encoding uses two parameters
m, n ∈ N, explained later. For simplicity, we assume that heap nodes have a
single data field val of an arbitrary type D. We consider a fixed program P and
omit it from most notations and statements. Let π be an execution of P starting
from an initial configuration c0 , where T = (T, λ) is a k-ary data tree of c0 with
signature S Σ = {val : D}, and pb points to the root of T . The encoding maps
π to a set of data trees kt(π, m, n), called the (m, n)-knitted-trees of π. We now
describe a generic knitted-tree K = (K, µ) from the set kt(π, m, n).


The backbone. The backbone K of K is the smallest tree such that: (i) the
input tree T is a subset of K (T ⊂ K), (ii) all nodes from T are internal nodes
in K, (iii) each internal node of K has degree k + m, and (iv) K has at least one
internal node. Note that, in the special case where T is empty, the backbone K
is a full tree of height 2, consisting of a root and its k + m children.
    Each node of K represents a distinct heap node. Initially, all nodes in T are
active, and the rest are inactive; freeing an active node makes it inactive.


The node signature. The backbone of a knitted-tree depends only on the
input data tree and parameters m, n, independent of the execution it represents.
Each backbone node is labeled with a sequence of frames (a log) tracking changes
along π. Frames form a doubly linked list called lace, to maintain chronological
order and enable bidirectional navigation. When consecutive operations involve
different nodes, frames are inserted along the backbone path connecting them.
The data signature SK of an (m, n)-knitted-tree is the following:
       n
SK =       avail i : B,                 Is this frame available?
           active i : B,                Is this node allocated?
           val i : D,                   Current value of this node’s data field
           pc i : PC P ,                Program counter
             i
           {d : Dd }d∈DVP ,             Current value of the data variables
           {upd ip : B}p∈PVP ,          Has p been updated since the frame i − 1?
           {isnil ip : B}p∈PVP ,        Is p nil?
                 i
           event : Event,               A pointer update, rewind, or error
                           i   k+m
           active_child : B             Is each child allocated?
           next i : Dir × [2, n + 1],   Link to the next frame                      o
           prev i : Dir × [2, n]        Link to the previous frame                                ,
                                                                                        i∈[n+1]


where Dir = {−, ↑} ∪ [k + m] encodes the position of an adjacent frame relative
to the reference frame. Each node’s label, or log, has n+1 indexed frames in time
order. Once a frame f in a log σ is named, its fields are referenced without the
index (e.g., f.pc instead of σ.pc i ). The last frame of a log handles label overflow
(if more than n frames are needed), via the (n + 1)th frame. The prev field holds
8       M. Faella and G. Parlato

a value from Dir × [n], since a frame with index n + 1 has no successor. The
event field holds an event taken from:
          
Event = ⟨pfield := p⟩, ⟨pfield := nil⟩, ⟨p := here⟩ | pfield ∈ PF , p ∈ PV P
                                                              
          ∪ rwdi | i ∈ [n] ∪ rwdi,p | i ∈ [n], p ∈ PV P ∪ nop, err, oom .
The first group represents updates to pointer fields and variables. rwdi and
rwdi,p represent lace rewinding events. Other symbols denote the empty event
(nop), null-pointer dereference (err), and out-of-memory error (oom) caused
by excessive use of the statement new.

3.1   The Labeling Function
The labeling function µ of K is defined inductively on the length of π.

Base case. π consists of an initial configuration, say (T , νp , νd , pc). We encode
the input tree T = (T, λ) into the backbone by setting the first frame of each
node t ∈ K as follows:
                                                                 (
           1                                                1       true if t ∈ T
µ(t).avail = false,                            µ(t).active =
                                                                    false otherwise
               (                                                 (
                λ(t).val    if t ∈ T                                true if t.j ∈ T
  µ(t).val 1 =                           µ(t).active_child 1j =
                unspecified otherwise                               false otherwise.
All other fields of the first frame are unspecified. The root’s second frame stores
π’s initial configuration: µ(ε).avail 2 = false, µ(ε).prev 2 = (−, 2) (a self-loop),
µ(ε).pc 2 is the first statement’s label in P , and µ(ε).isnil 2q = true for all pointer
variables q different from pb. If T is not empty, µ(ε).event 2 = ⟨b    p := here⟩ and
µ(ε).isnil 2pb = false; otherwise, µ(ε).event 2 = nop and µ(ε).isnil 2pb = true. All
other frames are marked as available. The root’s second frame also copies active,
val , and active_child from the first frame.

Inductive case. We start with an overview of the encoding method, its prop-
erties, and the required notation. Let π = πc, where c is a configuration and π is
a non-empty execution. Assume that K = (K, µ) is a knitted-tree in kt(π, m, n).
We define the labeling µ for π by extending the lace of K based on the last
instruction executed in π. To aid understanding, we list some invariants for all
knitted-trees, providing an informal explanation for brevity.
The lace. Besides individual node logs, we maintain a chronological order of all
frames across all nodes. All the unavailable frames in the knitted-tree with index
greater than 1 form a doubly linked list called the lace using the next and prev
fields of the frames. The first frame in the lace is the root’s second frame. Each
frame is identified by a pair (u, i), where u is a node and i ∈ [n + 1] is the frame’s
index. A frame (v, j) is the lace successor of frame (u, i), denoted (u, i) →next
(v, j) (and (u, i) is the lace predecessor of (v, j), written (v, j) →prev (u, i)) if
i, j > 1 and one of the following holds:
                            Verifying Tree-Manipulating Programs via CHCs            9

 – u = v, j = i + 1, µ(u).next i = (−, j), and µ(v).prev j = (−, i);
 – v is the lth child of u, µ(u).next i = (l, j), and µ(v).prev j = (↑, i);
 – u is the lth child of v, µ(u).next i = (↑, j), and µ(v).prev j = (l, i).
Available frames’ unspecified fields contribute to kt(π, m, n)’s non-determinism.
Properties of the frame fields. In our inductive definition, we obtain the knitted-
tree for π by extending that of π by appending frames for π’s final step. This
helps us assign meanings to fields like upd p , isnil p , d, val , pc, and active_child
for the unavailable frames. The upd p flag tracks changes to the pointer p outside
the current node: it is set to true in frame (u, i) (for i > 1) if p was assigned a
non-nil value in the part of the lace between frames (u, i−1) and (u, i) (excluding
these frames). Thus, if frames (u, i − 1) and (u, i) are adjacent in the lace (i.e.,
(u, i − 1) →next (u, i), aka an internal step), all upd p flags in (u, i) are false.
The isnil p flag is true in a frame if p = nil at that point in the execution. The
active_child flags help track the allocation of the child nodes of the backbone.
Other fields preserve their usual meanings.
Pushing a frame. Appending a frame to a log involves: (1) finding the smallest
index i with avail i is true, and (2) adding the new frame at position i. Hence,
a log behaves like a stack, with the bottom frame at index 1 and the top frame
being the highest-index frame where avail is false.
Default values for a frame. Any frame pushed onto a log assumes default values
unless specified otherwise. When pushing a frame f on a node u, default values
come from the preceding frame in the lace, f prev , or the frame below f in u’s
log, f below . Note that f prev and f below can be the same. The default values for
the fields of f are as follows: for all p ∈ PV P and d ∈ DV P ,
 – avail = false, event = nop, and upd p = false;
 – active and val are copied from f below ;
 – isnil p , d, and pc are copied from f prev ;
 – active_child j is copied from f prev .active if f prev belongs to the j th child of
   u; otherwise, it is copied from f below .active_child j ;
 – prev points to f prev ;
 – next is unspecified and can take any value in different knitted-trees for the
   same execution.
Moreover, f prev .next is updated to point to f , eliminating the non-determinism
of the next field of the previous frame.
    Despite the non-determinism in the next field, identifying the last frame f
in a lace can be done by checking f and its lace successor f ′ . Specifically, f is
the last frame of the lace if f ′ is available or f ′ precedes f in the lace, which
happens when field of f ′ .prev does not point to f .
    Henceforth, assume that f is the final lace last frame in K, located as the
top frame of node t. We first present the encoding of the statements that push
a single new frame f on the current node t. The fields of f are set to default
values, except for those specified below.
Encoding of p := nil: f.pc = succ(f .pc) and f.isnil p = true.
10        M. Faella and G. Parlato

Encoding of d := exp: f.pc = succ(f .pc) and f.d is set to the value of exp,
with variables in DV P evaluated using their values from f .
Encoding of skip: f.pc = succ(f .pc).
    The other statements may operate on different nodes in addition to t. The
main reasons to move to another node are to dereference a pointer or identify
the node a pointer field refers to. To get this information, we rewind the lace
by moving backward to find the most recent assignment to the relevant pointer.
For example, to identify the node a pointer variable p points to, we rewind the
lace until we find a frame with the event ⟨p := here⟩.
Lace rewinding function. To enable rewinding, we define the auxiliary function
find_ptr (p, id ), which takes a pointer p ∈ PV P and a frame ID and returns a
sequence of frame IDs by traversing the lace backward from id , until the most
recent assignment to p. The sequence uses shortcuts, including only the IDs
where the lace moves between nodes and where such moves are relevant to track
p, as indicated by the upd p flags. For example, in Fig. 2, rewinding from frame
15 to resolve head gives the following: 5
                                                                                
find_ptr (head , (u4 , 2)) = find_ptr (head , 15) = (u3 , 2), (u2 , 2), (u1 , 2) = (9, 4, 1).

Frames 9 and 4 have a predecessor that belongs to another node; moreover, they
represent the earliest occurrence of their node in the lace. Contrast this with
frame 12, which also follows a frame in another node, but is not in the sequence
because 12 is not the first visit to u3 , and upd head is false in 12. Frame 1 is
included as the value of head in frame 15 was established in frame 1. Thus,
rewinding from 15 adds frames 16, 17 and 18 for these IDs.
Null pointer dereference. If the instruction located at f .pc dereferences a pointer
p, and p is nil, it indicates an error. Thus, if the flag isnil p is true in f , we push
a new frame with the event err onto the current node t to indicate a runtime
error. We now present the encoding for the other types of statement.
Encoding of p → pfield := nil. We rewind the lace to find the latest assignment
to p. Let (t, i) be the identifier    of f , and id1 = (u1 , i1 ), . . . , idl = (ul , il ) be
the sequence find _ptr p, (t, i) . We push a new frame for each element of the
sequence id1 , . . . , idl , to keep a faithful record of the movements necessary to
simulate the current statement: for each j ∈ [l − 1], we push a frame onto uj
with the event rwdij , without advancing the program counter. Finally, we push
a frame f onto ul with f.pc = succ(f .pc) and f.event = ⟨pfield := nil⟩.
Encoding of p → pfield := q. Same as the encoding for p → pfield := nil, but
the final frame’s event is set to ⟨pfield := q⟩.
Encoding of p := q. If isnil q evaluates to true in f , we push a new frame onto
t with isnil p set to true. Otherwise, a rewinding operation takes the lace to the
node pointed by q, where we push a frame with ⟨p := here⟩. In either case, the
last frame also updates the program counter.
5
     Using the global lace positions as frame IDs (red numbers in Fig. 2).
                            Verifying Tree-Manipulating Programs via CHCs            11

Encoding of new p. Let j be the smallest index in [k + 1, k + m] such that
active_child j is false. If no such index exists, we push a frame on t with the
event oom, representing an out-of-memory error. Otherwise, the lace moves to
the j th child of t and pushes a frame f there with f.pc = succ(f .pc), f.event =
⟨p := here⟩, f.active = true, and f.isnil p = false.
Encoding of free p. A rewinding operation takes the lace to the node u pointed
by p, where we push a frame f with active = false and an updated pc. In the
new frame, isnil q is set to true for every pointer q that currently points at u,
including p. To find such pointers, let (u, i) be the id of f . Then, q points at
u if the log of u contains another frame (u, j) such that: j < i, (u, j) contains
⟨q := here⟩, and the upd q flag is false in all frames from (u, j + 1) to (u, i).
Encoding of p := q → pfield . First, the lace moves to the node u pointed by
q through a rewinding process. Then, we search in u’s log for the most recent
assignment to pfield . We look for the largest index i s.t. the frame (u, i) is in
use and contains an event of the form ⟨pfield := α⟩, for some α. If no such index
exists, pfield is interpreted as having its default value pointing to a child in the
original input tree. We then distinguish the following cases:
[α = nil] We push a frame with isnil p = true on u.
[α = r, for some r ∈ PV P ] If isnil r is true in the current frame, the lace pushes
    a frame with isnil p = true. Otherwise, the lace moves again to the node
    pointed by r, and there it pushes a frame with ⟨p := here⟩.
[The log of u does not contain an explicit assignment to pfield ] If pfield
    is the j th field in PF , u.j ∈ T , and u.j is active (as encoded in the flag
    active_child j ), the lace moves to u.j and pushes a frame with event ⟨p := here⟩
    there. Otherwise, a frame with isnil p = true is pushed on u.
The last pushed frame always updates the program counter.
Encoding Boolean conditions and control-flow statements. Data con-
ditions are evaluated locally using variable values in the current frame f . For
heap conditions, we may need to traverse the lace. We focus on conditions of
the form p = q, since others (e.g., p → pfield = q) can be reduced to this form
using auxiliary variables. To evaluate p = q, we first check the isnil flags: if both
pointers have their isnil flags set to true, the condition is true; if the flags differ,
it is false. If this is inconclusive, we rewind the lace to find an assignment to p
or q. For example, upon finding ⟨p := here⟩ in frame (u, i), we search in u’s log
for the largest index j < i where frame (u, j) has ⟨q := here⟩. If none exists,
the condition is false. If found,Wthe condition holds if q was unchanged between
(u, j) and (u, i), verified via ¬ l∈[j+1,i] upd lq . A new frame is then pushed, up-
dating the program counter accordingly. The process is symmetric if ⟨q := here⟩
is found first.

On the choice of parameters m and n. Parameter m bounds the number of
allocations: m = 0 for programs without allocations, while m = 1 is adequate
for programs that insert a single new node. The parameter n limits the passes
and instructions executed per node; while some programs need unbounded labels,
typical tree-like algorithms work with moderate n (usually ≤ 10).
12         M. Faella and G. Parlato

     Statement           Movement                     Information stored
     p → pfield := nil   Find p or fail               ⟨pfield := nil⟩
     p → pfield := q     Find p or fail               ⟨pfield := q⟩ or ⟨pfield := nil⟩
     p := q              Find q                       ⟨p := here⟩ or set isnil p
                         Find q or fail, then find
     p := q → pfield                                  ⟨p := here⟩ or set isnil p
                         last assignment to pfield
     p → val := exp      Find p or fail               Update val
     d := p → val        Find p or fail               Update d
                         Move to the first inactive
     new p                                            ⟨p := here⟩ and set active
                         child or fail
     free p              Find p or fail               Reset active

                         Table 1: Summary of the encodings.



3.2      Relations with Program Executions

Our first result establishes that knitted-trees provide an accurate and faithful
representation of program executions.
Theorem 1. Given a program P and parameters m, n, kt(·, m, n) is computable.
Moreover, there is a computable function exec such that, for any data tree K that
is a knitted-tree of P , exec(K) is an execution π of P s.t. K ∈ kt(π, m, n).
    Notice that the relation between executions π and knitted-trees K defined
by K ∈ kt(π, m, n) is neither injective nor functional. It is not functional due
to the non-determinism in the encoding. It is not injective because a knitted-
tree ending in a label overflow represents only a prefix of an execution and thus
relates to all executions sharing that prefix.
Exit status of a knitted-tree. To distinguish how knitted-trees terminate, we
introduce the notion of exit status for individual frames and for the entire
knitted-tree. Each frame f of a knitted-tree is assigned one of five statuses in
ExStatus = {C, E, O, M, N}, with the following meanings:

 – Clean exit: The program counter (pc) of f points to an exit instruction.
 – Runtime Error: f.event = err, indicating a null-pointer dereference.
 – Label Overflow: The index of f in its label is n + 1, indicating log overflow.
 – Out of Memory: f.event = oom, indicating a failed attempt to allocate a
   node with the new statement due to the absence of inactive nodes.
 – None: Indicates that frame f is not a terminal frame.

A frame f is terminal if its status is not None. Indeed, the exit statuses different
from N terminate the lace, hence only the last frame in the lace may have an
exit status different from N. The exit status of a knitted-tree K, denoted exit(K),
is the status of the last frame in its lace. The theorem below links knitted-tree’s
exit status to its corresponding executions.
                             Verifying Tree-Manipulating Programs via CHCs             13

Theorem 2. For all executions π and K ∈ kt(π, m, n), the following hold:
1. If exit(K) = E, then π ends in an error configuration.
2. If π ends in an error configuration, then exit(K) ∈ {E, O, M}.
3. If π is infinite, then exit(K) = O.


4    Properties of Knitted-Trees
Prefix of a knitted-tree. An (m, n)-knitted-tree is a knitted-tree associated with
an execution π in kt(π, m, n). A prefix of a knitted-tree K is a data tree ob-
tained from K by truncating its lace at a frame f , setting f ′.avail to true for all
subsequent frames, and leaving f.next unconstrained.
Locality. For a label σ and i ∈ N, we define σ <i (resp., σ ≤i ) as the label obtained
by setting avail to true in all frames of σ with indices ≥ i (resp., > i).
   The following lemma states that each new frame in a knitted-tree depends
only on local information from neighboring nodes. We use f1 ≡ f2 to indicate
that frames f1 and f2 differ only in their next field.
Lemma 1 (Locality). There exist functions Up, Down, Internal such that for
logs σ, τ1 , . . . , τk+m of a node u and of its children in a knitted-tree prefix:
 – For all steps (u.j, b) →next (u, a) in the lace, it holds σ a ≡ Up(τj≤b , j, σ <a ).
 – For all steps (u, a) →next (u.j, b) in the lace, it holds τjb ≡ Down(σ ≤a , j, τj<b ).
 – For all steps (u, a) →next (u, a+1) in the lace, it holds σ a+1 ≡ Internal (σ ≤a ).
Compositionality. Using the functions Up and Down from Lemma 1, we define
the predicate consistent_child (τ, j, σ). This predicate is meant to check whether
two logs σ and τ may belong to the same knitted-tree as the logs of a node and
its j th child. Specifically, it verifies that all pairs of consecutive frames, linked by
next and prev , with one frame belonging to τ and the other frame belonging to σ,
adhere to the functions Up and Down. A detailed definition of consistent_child
is in Appendix C.4.
    From consistent_child and knitted-tree prefix definitions, the next lemma
follows, ensuring that consistent_child holds on all parent-child log pairs.

Lemma 2. For all labels σ, τ ∈ L(SK ) and indices j ∈ [k + m], if there ex-
ists a knitted-tree prefix where σ and τ are the logs of a node and its j th child
respectively, then consistent_child (τ, j, σ) holds.

    The following lemma establishes a key property of consistent_child for our
verification approach, enabling knitted-tree composition from different subtrees.

Lemma 3 (Compositionality). Let σ1 , σ2 ∈ L(SK ) be the logs of nodes t1 , t2
in (m, n)-knitted-tree prefixes K1 , K2 . If consistent_child (σ2 , j, σ1 ) holds true for
some j ∈ [k + m], then there is an (m, n)-knitted-tree prefix K where σ1 is the log
of a node and σ2 is the log of its j th child. Moreover, K is obtained by replacing
the j th subtree of t1 in K1 with the subtree rooted at t2 in K2 .
14      M. Faella and G. Parlato

Proof. Let K be the data tree obtained by replacing the subtree rooted at the
j th child of t1 in K1 with the subtree rooted at t2 in K2 . We prove that K is
a knitted-tree prefix by induction on the number of pairs (a, b) where frames
σ1a and σ2b are adjacent in the lace, each such pair representing an interaction
between the parent’s and the child’s labels.
     When the above number is zero, there are no interactions between t1 and
its j th child in K1 . Let π1 be an execution s.t. K1 is a prefix of a knitted-
tree representing π1 . It is direct to show that K is a knitted-tree prefix for an
execution π following the same steps as π1 , starting with the input tree of K.
Since π1 never visits the j th child of t1 , and this subtree is the only difference
between K1 and K, π is a valid execution of P .
     For the inductive case, consider the last interaction (a, b) between σ1a and σ2b .
First, assume that such interaction is a step up from frame σ2b to σ1a . Let K1′
be derived from K1 by truncating its lace to end just before σ1a . Clearly, K1′ is
still a knitted-tree prefix, and the modified label σ1′ of t1 is obtained from σ1 by
removing the frames with index at least a, by setting their avail flags to true.
We can now apply the inductive hypothesis to the labels σ1′ and σ2 , because we
have removed one interaction between them. Hence, we can assume that there
is a single knitted-tree prefix K′ containing both labels as the logs of a parent
and its j th child. We then obtain the desired knitted-tree prefix K from K′ by
reintroducing the sequence of frames removed from K1 . We need to prove that
adding those frames respects all rules of knitted-trees. The correctness of the first
added frame, σ1a , is ensured by consistent_child (σ2 , j, σ1 ), because it applies the
function Up to all upward interactions between σ2 and σ1 . In turn, Lemma 1
ensures that adhering to that function is sufficient to establish the correctness
of the next frame. Subsequent frames can be reintroduced due to the unchanged
surroundings. Lemma 1 ensures that no other information is relevant.
     The other case to prove is when the last interaction is a step down from
the parent’s frame σ1a to the child’s frame σ2b . Define σ2′ as the label obtained
from σ2 with the frames of indices b and above removed. Similar to the previ-
ous case, we apply the inductive hypothesis to the shortened label σ2′ and its
shortened knitted-tree prefix K2′ , resulting in a knitted-tree prefix K′ . We then
reintroduce the frames removed from K2 into K′ . The correctness of the first rein-
troduced frame is ensured by consistent_child checking the function Down on
every downward interaction. The subsequent reintroduced frames are still valid
because there are no steps returning to the parent of t2 , and their surroundings
remain unchanged from K2 .                                                            ⊔
                                                                                      ⊓

Example 1. Consider the knitted-tree in Fig. 2, with node labels σ1 , . . . , σ5 , and
another knitted-tree of the same program on the input list 7 →8 →9 →3 →10
→11 →12 and key = 3. Let v4 be the node of the second knitted-tree with value
3, and let τ4 be its label. By inspecting the second knitted-tree, one can observe
that the occupied frames of τ4 (i.e., those with avail = false) contain the same
information as the occupied frames of σ3 . Therefore, consistent_child (τ4 , 1, σ2 )
holds, and by Lemma 3, the two knitted-trees can be composed at nodes u2 -v4
to construct a knitted-tree for the input list 1 →2 →3 →10 →11 →12.
                              Verifying Tree-Manipulating Programs via CHCs                 15



     (I)    Lab(σ) ← len(σ, 1) ∧ first_frame(σ 1 )            Initializing non-root nodes

    (II)    Lab(σ) ← len(σ, 2) ∧ start(σ)                     Initializing the root node

    (III)   Lab(σ) ← len(σ, i) ∧ Lab(σ ) ∧ ΨInternal (σ <i , σ i )
                                              <i
                                                                            Internal step

            A step from the j th child to its parent
    (IV)    Lab(σ) ← len(σ, i) ∧ Lab(σ <i ) ∧ Lab(τ )
                          ∧ consistent_child (τ, j, σ <i ) ∧ ΨUp (τ, j, σ <i , σ i )
            A step from a node to its j th child
    (V)     Lab(τ ) ← len(τ, i) ∧ Lab(σ) ∧ Lab(τ <i )
                          ∧ consistent_child (τ <i , j, σ) ∧ ΨDown (σ, j, τ <i , τ i )

    (VI)           ⊥ ← Lab(σ) ∧ label _exit(σ, Ex )           Lace ends with status in Ex

                                                         
Fig. 3: CHCs (I)-(V) form the CHC system Ckt P, m, n , while the CHC system
Cex (I) includes all the CHCs in the figure. Here, i ∈ [2, n] and j ∈ [k + m].

5     Reasoning about Knitted-Trees with CHCs
                                                    
We introduce a CHC system Ckt P, m, n for a program P with parameters
m, n ∈ N. It employs a single uninterpreted relation symbol, Lab(σ), where σ
matches the data signature SK of knitted-trees, ensuring the following:
                                                             
Theorem 3. In the minimal model of Ckt P, m, n , Lab(σ) holds for a label σ
iff σ labels a node in some (m, n)-knitted-tree prefix K of P .
                            
    We define Ckt P, m, n using the knitted-tree rules constructing constructing
partial knitted-trees (impractical for enumerating all knitted-trees). Instead, we
rely on the compositionality lemma (Lemma 3), which states that two consistent
labels imply the existence of a knitted-tree where those labels are logs of an
internal node and one of its children, and the locality lemma (Lemma 1) to
extend the lace involving these nodes. This lemma entails that constructing a
knitted-tree involves adding frames to node logs so that any two consecutive
frames belong to the same node or to neighboring backbone nodes. We use this
property in the CHC system, employing independent CHCs to simulate adding
a single frame. In the CHC system, we simulate adding a single frame via Up
(upward), Down (downward), and Internal (within the same log). We define
predicates ΨDown (σ, j, τj , f ), ΨUp (τj , j, σ, f ), and ΨInternal (σ, f ) to constrain logs
accordingly, with f as the resulting frame. 
    Figure 3 details the CHCs of Ckt P, m, n . While describing each CHC, we
establish the “only if” direction of Theorem 3, by induction on the number of
CHC applications needed to insert σ into the minimal interpretation of Lab. For
completeness, the proof of the “if” direction appears in Appendix B.3.
16      M. Faella and G. Parlato

    Before detailing the CHCs, we introduce some notation. Let σ ∈ L(SK ) and
i ∈ N. The formula len(σ, i) is true if all frames with indices in [i] are unavailable
                                                     def            Vn+1
and all other frames are available, i.e., len(σ, i) = ¬σ i .avail ∧ j=i+1 σ j .avail .
                                           <i
With an abuse of notation, we write σV         in a CHC as a shorthand      for a fresh
variable θ, together with the conjunct ℓ∈[i−1] (θℓ = σ ℓ ) ∧ ℓ∈[i,n+1] θℓ .avail .
                                                               V

    CHCs I and II ensure that Lab includes labels of all knitted-trees of 0-length
executions of P , forming the base case for the “only if” direction of Theorem 3,
since both are facts. CHC I defines non-root labels with all but the first frame
available, and consistent active/active_child , while CHC II defines root labels
by disabling the first two frames and using start(σ) for the second frame, as per
the base-case labeling (Section 3.1).
    The remaining CHCs extend each node’s log frame by frame, following the
inductive knitted-tree label definition. For Theorem 3 (“only if” direction), we
assume inductively that the body labels satisfy the claim, i.e., they label a node
in a (m, n)-knitted-tree prefix, and show that the head label does too.
    CHC III handles internal steps, where σ i follows σ i−1 in the lace. Here,
Lab(σ <i ) ensures that σ <i labels a node in an (m, n)-knitted-tree prefix, while
ΨInternal (σ <i , σ i ) constrains σ i to encode the next internal step, as per Lemma 1.
    CHC IV handles cases where the lace extends with a new frame pushed to
the parent of the previous frame, typically during a rewind phase. The predicate
consistent_child ensures that σ <i and τ belong to the same knitted-tree prefix,
as the log of a parent and its j th child (Lemma 3). Then, ΨUp extends the lace
by adding a frame to σ <i , following the topmost frame of τ .
    CHC V handles the reverse of CHC IV, where the current lace extends from
a parent to its j th child. Using ΨDown , it ensures that τj correctly extends τj<i
with a new frame for the latest step.


The Exit Status Problem. We present a method to check whether a program
can lead to a memory safety error via an execution that can be represented by
an (m, n)-knitted-tree. This reduces to solving a CHC system: if unsatisfiable,
such an execution exists. We formalize this as the following decision problem.

Problem 2. An instance of the exit status problem is a tuple (P, m, n, Ex ),
where P is a program, m, n ∈ N, and Ex is a set of exit statuses excluding N.
The exit status problem asks whether there exists an (m, n)-knitted-tree of P
whose exit status is in Ex .

    We solve the exit status problem using the CHC system Cex (I) (Figure 3),
which includes (i) all CHCs from Ckt P, m, n , crucial for Theorem 3, and (ii)
a single query, CHC VI, to check for a knitted-tree corresponding to a program
execution with an exit status in Ex . Combining Theorem 3 with the definition
of CHC VI yields the main result of this section.

Theorem 4. Let I be an instance of the exit-status problem. Then, I admits a
positive answer if and only if the CHC system Cex (I) is unsatisfiable.
                          Verifying Tree-Manipulating Programs via CHCs        17

5.1   Verifying Memory Safety
We begin by establishing two key theorems linking the exit status problem to
memory safety, forming the basis for our method’s correctness.
Theorem 5. If the answer to the exit status problem (P, m, n, {E}) is positive,
then the answer to the memory safety for P is negative.

Theorem 6. If the answer to the exit status problem (P, m, n, {O, M, E}) is
negative, then the answer to the memory safety problem for P is positive.
Algorithm MemSafety: We                               P, m0 , n0
outline our algorithm on the                 m ← m0 , n ← n0
right. We are given a program
P and initial values m0 and n0                                    Yes Memory
for the two parameters m and             ExitStatus P, m, n, {E}
                                                                       unsafe
n of knitted-trees. Verification                      No
starts by solving the problem
                            
                                 Yes
                                        ExitStatus P, m, n, {M}
                                                                 

ExitStatus P, m, n, {E}          m ++
                                                      No
to detect null-pointer derefer-  Yes                              No Memory
                                         ExitStatus P, m, n, {O}
ence errors. If the answer is    n ++                                  safe
positive, by Theorem 5 P vi-
olates memory safety. Otherwise, memory safety is not guaranteed, as the cur-
rent values of m and n may not cover all executions. To address this, we solve
ExitStatus P, m, n, X with:
1. X = {M} to detect out-of-memory failure from new allocations, and
2. X = {O} to detect label overflow errors.
If both instances are negative, Theorem 6 ensures that P is memory-safe. Oth-
erwise, we increment m or n to broaden coverage and restart. This may continue
indefinitely if the semi-algorithm never terminates (due to undecidability) or no
parameter values suffice to establish memory safety.
Theorem 7. Algorithm MemSafety is a sound solution to the memory safety
problem, i.e., if it terminates, it yields the correct answer.

5.2   Invariant Structure
In this section, we examine the essential properties that a solution to the CHC
system presented in Fig. 3 must satisfy, with particular emphasis on the structure
and complexity of the required invariants. To ground the discussion, we refer to
the running example introduced in Section 1 and shown in Fig. 1, representative
of a broad class of procedures manipulating tree data structures. This example
highlights both the challenges and the recurring structural patterns encountered
in the synthesis of suitable invariants for CHC systems.
    The minimal model of Lab for logs of knitted trees (from lists containing the
key value) results in labels that can be classified as follows:
18      M. Faella and G. Parlato

Initial Node: the first node of the lists is shaped as u1 (see Fig. 2).
Intermediate Nodes: one or more nodes like u2 (depending on the length of
    the input list).
Target Node: the node containing the special value, u3 .
Post-Target Node: the node immediately following the special value, u4 .
Subsequent Nodes: remaining nodes, similar to u5 .

    Labels associated with nodes of the same category differ only in their data
fields (val and key), while all other fields (e.g., program counters) are equal
across nodes (for instance, nodes like u2 consistently exhibit program counter 3
in the second frame). Only the data fields val and key depend on the input list,
and their constraints are simple:

 – In each node, both val and key retain the same value across all frames.
 – In an intermediate node, val ̸= key;
 – In the target node (u3 ), val = key.

Input lists that do not contain the key induce additional node types, subject
to analogous constraints. In Section 7, we briefly outline how the regularities
discussed above could be exploited in an implementation of our framework.


6    Related Work

Our work is related to many works in the literature in different ways. Here we
focus on those that seem to be the closest to the results presented in this paper.
    Our approach uses CHC engines for backend analysis, similar to other verifi-
cation methods [12,25,27,29,31,37,38,49,28,23,21,33,24]. CHCs serve as an inter-
mediate language, allowing us to focus on proof rules while solvers implement
algorithms within a standard framework. A primary challenge is encoding heap-
allocated mutable data structures. While array theory is often used (e.g., [39,15]),
it can result in complex CHCs. Our approach uses simple theories for basic data
types, avoiding array theory unless necessary. Traditional heap program analysis
often relies on abstractions like shape analysis [58] to scale. Refinement types
and invariants can be used to transform complex data structures, avoiding ar-
ray theory (e.g. [57,10,50,36]). This can lead to over-approximation in CHCs
and false positive by replacing heap operations with local object assertions, po-
tentially missing global invariants but enabling efficient verification when local
invariants suffice. A recent proposal suggests using an SMT-LIB theory of heaps
for CHCs to standardize heap data-structure representation [20].
    Our technique relates to tree automata, automata with auxiliary storage, and
bounded tree-width graphs representing their executions. It also relates to Cour-
celle’s theorem (proof), which reduces analysis to tree automata emptiness [26].
Inspired by Alur and Madhusudan’s nested words to represent pushdown au-
tomata executions [2], and their extensions for multistack and distributed au-
tomata by Madhusudan and Parlato [43], we represent tree-manipulating pro-
gram executions as knitted-trees, where nodes are frames and edges are next and
                          Verifying Tree-Manipulating Programs via CHCs        19

prev frame fields. Similar to La Torre et al. [40] for multistack pushdown au-
tomata, our approach provides tree decompositions with a bounded tree width.
Instead of using tree automata emptiness for reachability analysis, we leverage
CHC solvers to enable a tree automata-like method with enhanced data rea-
soning. Additionally, like Heizmann et al. [30], we use automata for program
analysis but replace counterexample-guided abstraction refinement with precise
knitted-tree representations and CHC solvers for approximation and refinement.
     Our work extends decidable methods for bounded-pass heap-manipulating
programs by supporting a broader range of properties, potentially at the cost of
undecidability. Mathur et al. [48] achieve decidable memory safety for forest-like
initial heaps and single-pass traversals, building on uninterpreted coherent pro-
grams [46,47]. They handle memory freeing but leave support for more complex
postconditions for future work. Alur and Černý [1] reduce assertion checking
of single-pass list-processing programs to data string transducers, achieving de-
cidability with a single advancing variable. This approach is less flexible than
Mathur et al.’s, as it doesn’t address memory safety or heap shape changes and is
limited to data ordering and equality without handling explicit memory freeing.
     Heap verification has been extensively studied using decidable logics such
as first-order logic with reachability [42], Lisbq in the Havoc tool [41], and
fragments of separation logic [7,54,18]. Some approaches interpret bounded tree
width data structures on trees [32,44]. While these logics are often restric-
tive, others methods handle undecidable cases using heuristics, lemma synthe-
sis, and programmer annotations [4,6,5,9,8,11,13,14,17,34,51,52,53,55,59]. In con-
trast, our knitted-tree encoding promotes a separation of concerns, offloading the
algorithmic burden to the underlying CHC solver.

7   Conclusions and Directions for Future Research
We presented a foundational, compositional approach to verifying programs that
manipulate tree data structures. By modeling executions as knitted-trees and
encoding them as CHCs, verification reduces to CHC satisfiability. This enables
modular reasoning and supports simple invariants. Overall, our method offers a
uniform and scalable framework for automating the verification of a broad class
of tree-manipulating programs.
Future Work. Our approach opens multiple research directions.
Efficient Implementation. Labels are currently handled by a single predicate,
Lab. Performance can be improved via case splitting—encoding enumerated
fields into predicate names—to simplify invariants (see Section 5.2). Moreover,
precomputing all possible configurations of the enumerated fields arising in ev-
ery possible frame of the program, together with (an overapproximation of) the
within-node and across-neighbor adjacency relations between frames would pro-
duce a larger set of significantly simplified CHCs that enforce consistency of the
data with the enumerated structure of the knitted tree.
Beyond Memory Safety. Full correctness requires verifying structural and func-
tional properties. Using symbolic data-tree automata (Sdtas), which integrate
20     M. Faella and G. Parlato

well with CHC-based verification [22], we can formally specify pre/postconditions–
e.g., that inputs form a red-black tree and outputs a sorted list. Preconditions
are easy to encode as they involve only the first frame of each node in the
knitted-tree, while postconditions require more effort due to the complexity of
encoding the output heap within the knitted-tree structure. For set-like trees, it
is also important to verify that operations such as insertion, deletion, and search
preserve key invariants, which can be checked via knitted-tree logs. Termination
can be verified by ensuring that labels do not overflow.

Deductive Verification. Our methodology is particularly suited for deductive ver-
ification of procedures with linear-time complexity—i.e., those that traverse each
node a bounded number of times. We aim to develop a verification framework
where program correctness is established by breaking down verification condi-
tions into preconditions and postconditions for code segments, with each segment
provably executable in linear time. This would bridge the gap between our ap-
proach and classical deductive verification techniques.

More Structures. Our approach naturally extends to programs manipulating
multiple data structures, especially those with bounded treewidth. While there
is no general method for all combinations, many can be handled with suitable
encodings. For example, a program that traverses a red-black tree in-order and
inserts values into a singly linked list can be modeled using knitted trees with
bounded labels; our method can then verify that the output list contains the
input values in non-increasing order. Some scenarios require more inventive en-
codings. For instance, checking equality of two lists via separate dummy roots
leads to unbounded log growth. Instead, modeling both as a single list of paired
elements keeps the log size bounded and tractable.
    As noted in the previous section, the graphs induced by knitted-trees have
bounded treewidth, suggesting applicability to a broad range of structures, in-
cluding arrays, doubly-linked lists, trees with parent pointers, and, more gener-
ally, any structure with bounded treewidth and a canonical tree decomposition.

Program Synthesis. We also plan to explore syntax-guided synthesis (SyGuS) of
tree-manipulating code. By expressing correctness properties as Sdtas and re-
ducing synthesis to CHC solving, we aim to generate correct-by-construction pro-
cedures, extending extending recent work on synthesis from specifications [56].



Acknowledgements We sincerely thank the anonymous reviewers for their
insightful feedback and constructive suggestions, which significantly improved
the quality of this paper. This work was partially supported by INdAM-GNCS
Project 2025 - CUP: E53C24001950001, and the MUR projects SOP (Securing
sOftware Platforms, CUP: H73C22000890001) as part of the SERICS project
(n. PE00000014 - CUP: B43C22000750006), and MUR project FAIR (Future AI
Research, CUP: E63C220 02150007).
                            Verifying Tree-Manipulating Programs via CHCs             21

References
 1. Alur, R., Cerný, P.: Streaming transducers for algorithmic verification of single-
    pass list-processing programs. In: Ball, T., Sagiv, M. (eds.) Proceedings of the 38th
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    POPL 2011, Austin, TX, USA, January 26-28, 2011. pp. 599–610. ACM (2011).
    https://doi.org/10.1145/1926385.1926454
 2. Alur, R., Madhusudan, P.: Adding nesting structure to words. J. ACM 56(3),
    16:1–16:43 (2009). https://doi.org/10.1145/1516512.1516518
 3. Angelis, E.D., K, H.G.V.: CHC-COMP 2022: Competition report. Elec-
    tronic Proceedings in Theoretical Computer Science 373, 44–62 (nov 2022).
    https://doi.org/10.4204/eptcs.373.5
 4. Banerjee, A., Barnett, M., Naumann, D.A.: Boogie meets regions: A verification
    experience report. In: Shankar, N., Woodcock, J. (eds.) Verified Software: Theo-
    ries, Tools, Experiments, Second International Conference, VSTTE 2008, Toronto,
    Canada, October 6-9, 2008. Proceedings. Lecture Notes in Computer Science,
    vol. 5295, pp. 177–191. Springer (2008). https://doi.org/10.1007/978-3-540-87873-
    5_16
 5. Banerjee, A., Naumann, D.A., Rosenberg, S.: Regional logic for local reasoning
    about global invariants. In: Vitek, J. (ed.) ECOOP 2008 - Object-Oriented Pro-
    gramming, 22nd European Conference, Paphos, Cyprus, July 7-11, 2008, Proceed-
    ings. Lecture Notes in Computer Science, vol. 5142, pp. 387–411. Springer (2008).
    https://doi.org/10.1007/978-3-540-70592-5_17
 6. Banerjee, A., Naumann, D.A., Rosenberg, S.: Local reasoning for global
    invariants, part I: region logic. J. ACM 60(3), 18:1–18:56 (2013).
    https://doi.org/10.1145/2485982
 7. Berdine, J., Calcagno, C., O’Hearn, P.W.: A decidable fragment of separation logic.
    In: Lodaya, K., Mahajan, M. (eds.) FSTTCS 2004: Foundations of Software Tech-
    nology and Theoretical Computer Science, 24th International Conference, Chen-
    nai, India, December 16-18, 2004, Proceedings. Lecture Notes in Computer Science,
    vol. 3328, pp. 97–109. Springer (2004). https://doi.org/10.1007/978-3-540-30538-
    5_9
 8. Berdine, J., Calcagno, C., O’Hearn, P.W.: Smallfoot: Modular automatic asser-
    tion checking with separation logic. In: de Boer, F.S., Bonsangue, M.M., Graf, S.,
    de Roever, W.P. (eds.) Formal Methods for Components and Objects, 4th Inter-
    national Symposium, FMCO 2005, Amsterdam, The Netherlands, November 1-4,
    2005, Revised Lectures. Lecture Notes in Computer Science, vol. 4111, pp. 115–137.
    Springer (2005). https://doi.org/10.1007/11804192_6
 9. Berdine, J., Calcagno, C., O’Hearn, P.W.: Symbolic execution with separa-
    tion logic. In: Yi, K. (ed.) Programming Languages and Systems, Third Asian
    Symposium, APLAS 2005, Tsukuba, Japan, November 2-5, 2005, Proceedings.
    Lecture Notes in Computer Science, vol. 3780, pp. 52–68. Springer (2005).
    https://doi.org/10.1007/11575467_5
10. Bjørner, N.S., McMillan, K.L., Rybalchenko, A.: On solving universally quantified
    horn clauses. In: Logozzo, F., Fähndrich, M. (eds.) Static Analysis - 20th Inter-
    national Symposium, SAS 2013, Seattle, WA, USA, June 20-22, 2013. Proceed-
    ings. Lecture Notes in Computer Science, vol. 7935, pp. 105–125. Springer (2013).
    https://doi.org/10.1007/978-3-642-38856-9_8
11. Calcagno, C., Distefano, D., O’Hearn, P.W., Yang, H.: Compositional shape
    analysis by means of bi-abduction. J. ACM 58(6), 26:1–26:66 (2011).
    https://doi.org/10.1145/2049697.2049700
22      M. Faella and G. Parlato

12. Champion, A., Chiba, T., Kobayashi, N., Sato, R.: Ice-based refinement type dis-
    covery for higher-order functional programs. J. Autom. Reason. 64(7), 1393–1418
    (2020)
13. Chin, W., David, C., Nguyen, H.H., Qin, S.: Automated verification of shape, size
    and bag properties via user-defined predicates in separation logic. Sci. Comput.
    Program. 77(9), 1006–1036 (2012). https://doi.org/10.1016/J.SCICO.2010.07.004
14. Chu, D., Jaffar, J., Trinh, M.: Automatic induction proofs of data-structures in
    imperative programs. In: Grove, D., Blackburn, S.M. (eds.) Proceedings of the
    36th ACM SIGPLAN Conference on Programming Language Design and Im-
    plementation, Portland, OR, USA, June 15-17, 2015. pp. 457–466. ACM (2015).
    https://doi.org/10.1145/2737924.2737984
15. De Angelis, E., Fioravanti, F., Pettorossi, A., Proietti, M.: Program verification
    using constraint handling rules and array constraint generalizations. Fundam. In-
    formaticae 150(1), 73–117 (2017). https://doi.org/10.3233/FI-2017-1461
16. De Angelis, E., K., H.G.V.: CHC-COMP 2023: Competition report. CoRR
    abs/2404.14923 (2024). https://doi.org/10.48550/ARXIV.2404.14923
17. Distefano, D., O’Hearn, P.W., Yang, H.: A local shape analysis based on separa-
    tion logic. In: Hermanns, H., Palsberg, J. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems, 12th International Conference, TACAS
    2006 Held as Part of the Joint European Conferences on Theory and Practice
    of Software, ETAPS 2006, Vienna, Austria, March 25 - April 2, 2006, Proceed-
    ings. Lecture Notes in Computer Science, vol. 3920, pp. 287–302. Springer (2006).
    https://doi.org/10.1007/11691372_19
18. Echenim, M., Iosif, R., Peltier, N.: Unifying decidable entailments in separation
    logic with inductive definitions. In: Platzer, A., Sutcliffe, G. (eds.) Automated
    Deduction - CADE 28 - 28th International Conference on Automated Deduction,
    Virtual Event, July 12-15, 2021, Proceedings. Lecture Notes in Computer Science,
    vol. 12699, pp. 183–199. Springer (2021). https://doi.org/10.1007/978-3-030-79876-
    5_11
19. van Emden, M.H., Kowalski, R.A.: The semantics of predicate logic as a program-
    ming language. J. ACM 23(4), 733–742 (1976)
20. Esen, Z., Rümmer, P.: An SMT-LIB theory of heaps. In: Déharbe, D., Hyvärinen,
    A.E.J. (eds.) Proceedings of the 20th Internal Workshop on Satisfiability Modulo
    Theories co-located with the 11th International Joint Conference on Automated
    Reasoning (IJCAR 2022) part of the 8th Federated Logic Conference (FLoC 2022),
    Haifa, Israel, August 11-12, 2022. CEUR Workshop Proceedings, vol. 3185, pp. 38–
    53. CEUR-WS.org (2022)
21. Esen, Z., Rümmer, P.: Tricera: Verifying C programs using the theory of heaps.
    In: Griggio, A., Rungta, N. (eds.) 22nd Formal Methods in Computer-Aided De-
    sign, FMCAD 2022, Trento, Italy, October 17-21, 2022. pp. 380–391. IEEE (2022).
    https://doi.org/10.34727/2022/ISBN.978-3-85448-053-2_45
22. Faella, M., Parlato, G.: Reasoning about data trees using chcs. In: Shoham,
    S., Vizel, Y. (eds.) Computer Aided Verification - 34th International Confer-
    ence, CAV 2022, Haifa, Israel, August 7-10, 2022, Proceedings, Part II. Lec-
    ture Notes in Computer Science, vol. 13372, pp. 249–271. Springer (2022).
    https://doi.org/10.1007/978-3-031-13188-2_13
23. Faella, M., Parlato, G.: Reachability games modulo theories with a bounded
    safety player. In: Williams, B., Chen, Y., Neville, J. (eds.) Thirty-Seventh AAAI
    Conference on Artificial Intelligence, AAAI 2023, Thirty-Fifth Conference on
    Innovative Applications of Artificial Intelligence, IAAI 2023, Thirteenth Sym-
                            Verifying Tree-Manipulating Programs via CHCs            23

    posium on Educational Advances in Artificial Intelligence, EAAI 2023, Wash-
    ington, DC, USA, February 7-14, 2023. pp. 6330–6337. AAAI Press (2023).
    https://doi.org/10.1609/AAAI.V37I5.25779
24. Faella, M., Parlato, G.: A unified automata-theoretic approach to ltlf modulo theo-
    ries. In: Endriss, U., Melo, F.S., Bach, K., Diz, A.J.B., Alonso-Moral, J.M., Barro,
    S., Heintz, F. (eds.) ECAI 2024 - 27th European Conference on Artificial Intelli-
    gence, 19-24 October 2024, Santiago de Compostela, Spain - Including 13th Con-
    ference on Prestigious Applications of Intelligent Systems (PAIS 2024). Frontiers in
    Artificial Intelligence and Applications, vol. 392, pp. 1254–1261. IOS Press (2024).
    https://doi.org/10.3233/FAIA240622
25. Fedyukovich, G., Ahmad, M.B.S., Bodík, R.: Gradual synthesis for static paral-
    lelization of single-pass array-processing programs. In: Proceedings of the 38th
    ACM SIGPLAN Conference on Programming Language Design and Implementa-
    tion, PLDI 2017, Barcelona, Spain, June 18-23, 2017. pp. 572–585. ACM (2017)
26. Flum, J., Grohe, M.: Parameterized Complexity Theory. Texts in Theoretical Com-
    puter Science. An EATCS Series, Springer (2006). https://doi.org/10.1007/3-540-
    29953-X
27. Garoche, P., Kahsai, T., Thirioux, X.: Hierarchical state machines as modular horn
    clauses. In: Proceedings 3rd Workshop on Horn Clauses for Verification and Syn-
    thesis, HCVS@ETAPS 2016, Eindhoven, The Netherlands, 3rd April 2016. EPTCS,
    vol. 219, pp. 15–28 (2016)
28. Gurfinkel, A.: Program verification with constrained horn clauses (invited pa-
    per). In: Shoham, S., Vizel, Y. (eds.) Computer Aided Verification - 34th Inter-
    national Conference, CAV 2022, Haifa, Israel, August 7-10, 2022, Proceedings,
    Part I. Lecture Notes in Computer Science, vol. 13371, pp. 19–29. Springer (2022).
    https://doi.org/10.1007/978-3-031-13185-1_2
29. Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The seahorn verification
    framework. In: Computer Aided Verification - 27th International Conference, CAV
    2015, San Francisco, CA, USA, July 18-24, 2015, Proceedings, Part I. LNCS,
    vol. 9206, pp. 343–361. Springer (2015)
30. Heizmann, M., Hoenicke, J., Podelski, A.: Software model checking for people who
    love automata. In: Sharygina, N., Veith, H. (eds.) Computer Aided Verification
    - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July 13-
    19, 2013. Proceedings. Lecture Notes in Computer Science, vol. 8044, pp. 36–52.
    Springer (2013). https://doi.org/10.1007/978-3-642-39799-8_2
31. Hojjat, H., Konecný, F., Garnier, F., Iosif, R., Kuncak, V., Rümmer, P.: A verifi-
    cation toolkit for numerical transition systems - tool paper. In: FM 2012: Formal
    Methods - 18th International Symposium, Paris, France, August 27-31, 2012. Pro-
    ceedings. LNCS, vol. 7436, pp. 247–251. Springer (2012)
32. Iosif, R., Rogalewicz, A., Simácek, J.: The tree width of separation logic with
    recursive definitions. In: Bonacina, M.P. (ed.) Automated Deduction - CADE-24 -
    24th International Conference on Automated Deduction, Lake Placid, NY, USA,
    June 9-14, 2013. Proceedings. Lecture Notes in Computer Science, vol. 7898, pp.
    21–38. Springer (2013). https://doi.org/10.1007/978-3-642-38574-2_2
33. Itzhaky, S., Shoham, S., Vizel, Y.: Hyperproperty verification as CHC satisfiabil-
    ity. In: Weirich, S. (ed.) Programming Languages and Systems - 33rd European
    Symposium on Programming, ESOP 2024, Held as Part of the European Joint
    Conferences on Theory and Practice of Software, ETAPS 2024, Luxembourg City,
    Luxembourg, April 6-11, 2024, Proceedings, Part II. Lecture Notes in Computer
24      M. Faella and G. Parlato

    Science, vol. 14577, pp. 212–241. Springer (2024). https://doi.org/10.1007/978-3-
    031-57267-8_9
34. Jacobs, B., Smans, J., Philippaerts, P., Vogels, F., Penninckx, W., Piessens, F.: Ver-
    ifast: A powerful, sound, predictable, fast verifier for C and java. In: Bobaru, M.G.,
    Havelund, K., Holzmann, G.J., Joshi, R. (eds.) NASA Formal Methods - Third In-
    ternational Symposium, NFM 2011, Pasadena, CA, USA, April 18-20, 2011. Pro-
    ceedings. Lecture Notes in Computer Science, vol. 6617, pp. 41–55. Springer (2011).
    https://doi.org/10.1007/978-3-642-20398-5_4
35. Jaffar, J., Maher, M.J.: Constraint logic programming: A survey. J. Log. Program.
    19/20, 503–581 (1994)
36. Kahsai, T., Kersten, R., Rümmer, P., Schäf, M.: Quantified heap invariants for
    object-oriented programs. In: Eiter, T., Sands, D. (eds.) LPAR-21, 21st Interna-
    tional Conference on Logic for Programming, Artificial Intelligence and Reasoning,
    Maun, Botswana, May 7-12, 2017. EPiC Series in Computing, vol. 46, pp. 368–384.
    EasyChair (2017). https://doi.org/10.29007/ZRCT
37. Kahsai, T., Rümmer, P., Sanchez, H., Schäf, M.: Jayhorn: A framework for verifying
    java programs. In: Computer Aided Verification - 28th International Conference,
    CAV 2016, Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part I. LNCS,
    vol. 9779, pp. 352–358. Springer (2016)
38. Kobayashi, N., Sato, R., Unno, H.: Predicate abstraction and CEGAR for higher-
    order model checking. In: Proceedings of the 32nd ACM SIGPLAN Conference on
    Programming Language Design and Implementation, PLDI 2011, San Jose, CA,
    USA, June 4-8, 2011. pp. 222–233. ACM (2011)
39. Komuravelli, A., Bjørner, N.S., Gurfinkel, A., McMillan, K.L.: Compositional ver-
    ification of procedural programs using horn clauses over integers and arrays. In:
    Kaivola, R., Wahl, T. (eds.) Formal Methods in Computer-Aided Design, FM-
    CAD 2015, Austin, Texas, USA, September 27-30, 2015. pp. 89–96. IEEE (2015).
    https://doi.org/10.1109/FMCAD.2015.7542257
40. La Torre, S., Napoli, M., Parlato, G.: A unifying approach for multistack push-
    down automata. In: Csuhaj-Varjú, E., Dietzfelbinger, M., Ésik, Z. (eds.) Math-
    ematical Foundations of Computer Science 2014 - 39th International Sympo-
    sium, MFCS 2014, Budapest, Hungary, August 25-29, 2014. Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 8634, pp. 377–389. Springer (2014).
    https://doi.org/10.1007/978-3-662-44522-8_32
41. Lahiri, S.K., Qadeer, S.: Back to the future: revisiting precise program verification
    using SMT solvers. In: Necula, G.C., Wadler, P. (eds.) Proceedings of the 35th
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    POPL 2008, San Francisco, California, USA, January 7-12, 2008. pp. 171–182.
    ACM (2008). https://doi.org/10.1145/1328438.1328461
42. Lev-Ami, T., Immerman, N., Reps, T.W., Sagiv, M., Srivastava, S., Yorsh, G.:
    Simulating reachability using first-order logic with applications to verification of
    linked data structures. Log. Methods Comput. Sci. 5(2) (2009)
43. Madhusudan, P., Parlato, G.: The tree width of auxiliary storage. In: Ball, T.,
    Sagiv, M. (eds.) Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium
    on Principles of Programming Languages, POPL 2011, Austin, TX, USA, January
    26-28, 2011. pp. 283–294. ACM (2011). https://doi.org/10.1145/1926385.1926419
44. Madhusudan, P., Parlato, G., Qiu, X.: Decidable logics combining heap struc-
    tures and data. In: Ball, T., Sagiv, M. (eds.) Proceedings of the 38th ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL
    2011, Austin, TX, USA, January 26-28, 2011. pp. 611–622. ACM (2011).
    https://doi.org/10.1145/1926385.1926455
                            Verifying Tree-Manipulating Programs via CHCs            25

45. Manna, Z., Zarba, C.G.: Combining decision procedures. In: Formal Methods at the
    Crossroads. From Panacea to Foundational Support, 10th Anniversary Colloquium
    of UNU/IIST, the International Institute for Software Technology of The United
    Nations University, Lisbon, Portugal, March 18-20, 2002, Revised Papers. LNCS,
    vol. 2757, pp. 381–422. Springer (2002)
46. Mathur, U., Madhusudan, P., Viswanathan, M.: Decidable verification of unin-
    terpreted programs. Proc. ACM Program. Lang. 3(POPL), 46:1–46:29 (2019).
    https://doi.org/10.1145/3290359
47. Mathur, U., Madhusudan, P., Viswanathan, M.: What’s decidable about program
    verification modulo axioms? In: Biere, A., Parker, D. (eds.) Tools and Algorithms
    for the Construction and Analysis of Systems - 26th International Conference,
    TACAS 2020, Held as Part of the European Joint Conferences on Theory and
    Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings,
    Part II. Lecture Notes in Computer Science, vol. 12079, pp. 158–177. Springer
    (2020). https://doi.org/10.1007/978-3-030-45237-7_10
48. Mathur, U., Murali, A., Krogmeier, P., Madhusudan, P., Viswanathan, M.: Decid-
    ing memory safety for single-pass heap-manipulating programs. Proc. ACM Pro-
    gram. Lang. 4(POPL), 35:1–35:29 (2020). https://doi.org/10.1145/3371103
49. Matsushita, Y., Tsukada, T., Kobayashi, N.: Rusthorn: Chc-based verification
    for rust programs. ACM Trans. Program. Lang. Syst. 43(4), 15:1–15:54 (2021).
    https://doi.org/10.1145/3462205
50. Monniaux, D., Gonnord, L.: Cell morphing: From array programs to array-
    free horn clauses. In: Rival, X. (ed.) Static Analysis - 23rd International Sym-
    posium, SAS 2016, Edinburgh, UK, September 8-10, 2016, Proceedings. Lec-
    ture Notes in Computer Science, vol. 9837, pp. 361–382. Springer (2016).
    https://doi.org/10.1007/978-3-662-53413-7_18
51. Murali, A., Peña, L., Blanchard, E., Löding, C., Madhusudan, P.: Model-guided
    synthesis of inductive lemmas for FOL with least fixpoints. Proc. ACM Program.
    Lang. 6(OOPSLA2), 1873–1902 (2022). https://doi.org/10.1145/3563354
52. Nguyen, H.H., Chin, W.: Enhancing program verification with lemmas. In:
    Gupta, A., Malik, S. (eds.) Computer Aided Verification, 20th International
    Conference, CAV 2008, Princeton, NJ, USA, July 7-14, 2008, Proceedings.
    Lecture Notes in Computer Science, vol. 5123, pp. 355–369. Springer (2008).
    https://doi.org/10.1007/978-3-540-70545-1_34
53. Pek, E., Qiu, X., Madhusudan, P.: Natural proofs for data structure manipulation
    in C using separation logic. In: O’Boyle, M.F.P., Pingali, K. (eds.) ACM SIG-
    PLAN Conference on Programming Language Design and Implementation, PLDI
    ’14, Edinburgh, United Kingdom - June 09 - 11, 2014. pp. 440–451. ACM (2014).
    https://doi.org/10.1145/2594291.2594325
54. Piskac, R., Wies, T., Zufferey, D.: Automating separation logic using SMT. In:
    Sharygina, N., Veith, H. (eds.) Computer Aided Verification - 25th International
    Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013. Proceedings.
    Lecture Notes in Computer Science, vol. 8044, pp. 773–789. Springer (2013).
    https://doi.org/10.1007/978-3-642-39799-8_54
55. Piskac, R., Wies, T., Zufferey, D.: Automating separation logic with trees and data.
    In: Biere, A., Bloem, R. (eds.) Computer Aided Verification - 26th International
    Conference, CAV 2014, Held as Part of the Vienna Summer of Logic, VSL 2014, Vi-
    enna, Austria, July 18-22, 2014. Proceedings. Lecture Notes in Computer Science,
    vol. 8559, pp. 711–728. Springer (2014). https://doi.org/10.1007/978-3-319-08867-
    9_47
26      M. Faella and G. Parlato

56. Polikarpova, N., Sergey, I.: Structuring the synthesis of heap-manipulating
    programs. Proc. ACM Program. Lang. 3(POPL), 72:1–72:30 (2019).
    https://doi.org/10.1145/3290385
57. Rondon, P.M., Kawaguchi, M., Jhala, R.: Liquid types. In: Gupta, R., Amaras-
    inghe, S.P. (eds.) Proceedings of the ACM SIGPLAN 2008 Conference on Pro-
    gramming Language Design and Implementation, Tucson, AZ, USA, June 7-13,
    2008. pp. 159–169. ACM (2008). https://doi.org/10.1145/1375581.1375602
58. Sagiv, S., Reps, T.W., Wilhelm, R.: Parametric shape analysis via 3-valued
    logic. In: Appel, A.W., Aiken, A. (eds.) POPL ’99, Proceedings of the 26th
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    San Antonio, TX, USA, January 20-22, 1999. pp. 105–118. ACM (1999).
    https://doi.org/10.1145/292540.292552
59. Ta, Q., Le, T.C., Khoo, S., Chin, W.: Automated mutual explicit induction proof
    in separation logic. In: Fitzgerald, J.S., Heitmeyer, C.L., Gnesi, S., Philippou,
    A. (eds.) FM 2016: Formal Methods - 21st International Symposium, Limassol,
    Cyprus, November 9-11, 2016, Proceedings. Lecture Notes in Computer Science,
    vol. 9995, pp. 659–676 (2016). https://doi.org/10.1007/978-3-319-48989-6_40
                            Verifying Tree-Manipulating Programs via CHCs           27

A    Encoding Restricted Recursion Mechanisms in the
     Programming Language
In Section 2, we introduced a simple programming language for heap-manipulating
programs that does not directly support procedure calls. For non-recursive pro-
cedures, we can handle calls by inlining their code at each call site. In this section,
we describe an approach to simulating a specific form of recursive procedures,
commonly used in procedures that manipulate tree data structures, as found in
the literature.
    We focus on procedures where the first parameter (later denoted by first) is
a pointer. The corresponding argument that is passed at runtime must satisfy
the following conditions:
 1. It references a node that has not been previously used for invocation.
 2. It corresponds to a pointer field of the current node (i.e., the node on which
    the procedure was last invoked).
 3. Its value is unchanged from its original value at the beginning of the program.
The remaining parameters can be any data values or pointer variables. Addi-
tionally, if the procedure is invoked with a nil pointer as the first parameter, it
must not call another procedure before returning. The code handling this case
must be guarded by an if statement that checks whether the first argument of
the function is equal to or different from nil. These constraints are typically sat-
isfied by functions that manipulate Binary Search Trees (Bsts), red-black trees,
AVL trees, and similar structures.
     We assume that procedures do not return data or pointer values; instead, any
return values are managed via global variables. We also assume that the main
(i.e., outmost) procedure is never called.
     Under these constraints, recursive programs can be transformed into a pro-
gram without procedures by extending the input tree’s structure to include addi-
tional fields for local data and pointer variables used within the procedures. We
also include additional fields to orchestrate the simulation of the control flow
during calls and returns, thereby eliminating the need for a system stack. To
formalize this approach, we define an extended heap as follows:
Definition 3. An extended heap is a tuple Hext = (N, S, data, PF , Sext ,
dataext , PF ext ) where (N, S, data, PF ) and (N, Sext , dataext , PF ext ) are heaps.
The extended data signature Sext includes:
Local Variable Fields: Fields for the distinct local variables of the procedures
   (including the procedure arguments). The types of these fields match the
   types of the corresponding local variables.
Program Counter: A field named return_lab to keep track of the next state-
   ment to execute within a procedure after returning from the last ongoing
   procedure call.
Parent Field: A pointer field that points to the parent node in the input tree,
   facilitating the return control. This field is initialized accordingly and is never
   modified in the translated code.
28       M. Faella and G. Parlato

A.1     Code to Code Translation
Here, we outline a method to rewrite the code and entirely eliminate recursive
procedures, resulting in a program that behaves equivalently to the original.

Initialize the local variables of the root: We add a fresh assignment to set
the local variables related the main procedure to point at pb. This establishes the
property that the first argument of the procedure refers to the node on which it
is invoked. For other nodes, this assignment is performed before the simulation
starts.

Local variable replacement: Within a procedure’s body, replace all occur-
rences of local variables as follows. If loc is a local variable, replace it with
first → loc. This modification is applied throughout the procedure code except
for the code block executed when the procedure is called with nil as the first
parameter. This ensures that local variables correctly reference the appropriate
heap node.

Consolidate into a single procedure: Combine all existing functions into a
single procedure by removing individual function declarations. We assume that
all statement labels, variable names, and function parameter names are distinct
to avoid naming conflicts.

Replace procedure calls: This process is divided into four phases. Consider
a procedure call statement, and assume that the first parameter of the calling
procedure is first, whereas the arguments of this call are arg 1 , . . . , arg ℓ . Recall
that, according to Condition 2 at the beginning of this section, arg 1 = first →
pfield , for some pointer field pfield . We then perform the following steps, that
add new statements in place of the procedure call.

Phase 1 – Argument Assignment: Assign the values of the arguments of the
called procedure to the corresponding fields of the node referenced by arg 1 .
Specifically, let param 1 , . . . , param ℓ be the list of parameters of the callee, for
each i ∈ [ℓ], add an assignment of the form:
                               arg 1 → param i := arg i .

Phase 2 – Set Return Label Assignment: Assign the label of the statement im-
mediately following the current function call to arg 1 → return_lab. This sets
up the point to which the program should jump after the simulated procedure
execution corresponding to the current call:
      arg 1 → return_lab := ⟨label of the next statement in the orginal code⟩

Phase 3 – Jump to the First Statement of the Called Procedure: Transfer control
in the monolithic program to the first statement of the called procedure via a
goto statement:

             goto ⟨label of the first statement of the called function⟩.
                          Verifying Tree-Manipulating Programs via CHCs          29

Phase 4 – Jump Back to the Caller Procedure: Replace return statements in the
original code with a goto statement that uses the label stored in the auxiliary
field of the current node set at the time of procedure invocation, namely:

                            goto first → return_lab.

    This systematic transformation effectively simulates recursive procedure calls
without using actual function calls or a system stack. By extending the heap with
additional fields to store local variables, return addresses, and parent pointers,
the program maintains the necessary state to manage control flow and variable
references during execution.


B     Additional Proofs
B.1   Proofs for Section 3
Theorem 1. Given a program P and parameters m, n, kt(·, m, n) is computable.
Moreover, there is a computable function exec such that, for any data tree K that
is a knitted-tree of P , exec(K) is an execution π of P s.t. K ∈ kt(π, m, n).

Proof. The first part of the statement (i.e., the computability of kt) can be
shown by inspecting the encoding described in Section 3, with further details in
Appendix C. One can clearly see that the definition of knitted-tree is entirely
constructive. In fact, the content of each new frame in the lace can be computed
from the program and the log of the current node and of the neighboring nodes.
    The second part of the statement requires a function exec that maps knitted-
trees back to executions. To this aim, we first prove two supporting claims.
    Claim 1: We can retrieve the state of the heap from any knitted-tree prefix.
We show that we can recover the state of the heap at each point of the lace
of a knitted-tree. We select the nodes where active is true in their top frame.
We then examine the logs of the selected nodes to determine the values of their
fields. For any node u, the current value of its data field val is the value of the
val field in the topmost frame of the log. The current value of a pointer field
pfield (assumed to be the j th field in PF ) can be recovered as follows:
 – If pfield has never been updated, u.pfield points to the j th child of u, if u.j
   exists and is active in the knitted-tree; otherwise, u.pfield points to nil.
 – If the last update in u’s log is ⟨pfield := nil⟩, then that pointer field is also
   nil.
 – Otherwise, the last update is ⟨pfield := p⟩ for some pointer variable p. We
   navigate the lace backward using find _ptr until finding a frame that reports
   ⟨p := here⟩, say in the log of node v, and set u.pfield to v.
We denote by heap(K) the heap corresponding to the knitted-tree (prefix) K, as
described above.
    Claim 2: We can retrieve the value of all pointer variables from any knitted-
tree prefix. The isnil fields in the last frame of the knitted-tree prefix indicate
30        M. Faella and G. Parlato

which pointer variables are nil. We can find the current value of the other pointer
variables p ∈ PV P , by retracing the lace backward until the most recent assign-
ment to it (i.e., ⟨p := here⟩). We denote by pv (K) the map that assigns each
p ∈ PV P to the node of heap(K) pointed to by p at the end of the lace of K.
    We can now prove the second part of the statement. Let K = (K, µ) be a
data tree that is the knitted-tree of some execution. To define exec(K), we start
by recovering the initial program configuration c0 = (H0 , νp , νd , pc 0 ), where the
initial heap H0 can be obtained from Claim 1 above, and the initial value of the
pointer variables νp from Claim 2. The initial value of the program counter is
simply the label of the first line in the program, and the initial value for the
data variables νd can be read from the d fields in the second frame of the root of
K. To obtain each subsequent program configuration, it is sufficient to scan the
lace chronologically, iteratively identify the frame f that marks the end of each
statement6 , and at that point build a new program configuration using Claims 1
and 2 above, and reading the current value of the data variables and program
counter from f .                                                                     ⊔
                                                                                     ⊓

Theorem 2. For all executions π and K ∈ kt(π, m, n), the following hold:

1. If exit(K) = E, then π ends in an error configuration.
2. If π ends in an error configuration, then exit(K) ∈ {E, O, M}.
3. If π is infinite, then exit(K) = O.

Proof. Claim 1. To prove the first statement, assume that K has exit status E,
occurring when the last frame f in K’s lace has the event err. By Thm 1, the last
configuration of π can be recovered from K via the exec function. By definition
of knitted-trees, the event err arises only from a null pointer dereference, so c
is an error configuration.
    Claim 2. For the second statement, assume that π ends in an error configu-
ration and the exit status of K is neither O nor M. We show that the exit status
of K is E. By Thm 1, the last configuration of π can be recovered from K via
the exec function. Since π ends in an error configuration, the program counter
in the last frame of the lace of K points to an instruction causing a null pointer
dereference, leading to the event err and hence to the exit status E.
    Claim 3. Each step of an execution adds at least one frame to the lace of
its knitted-tree. Since the total number of nodes and frames in a knitted-tree is
finite, the lace will eventually occupy a frame with index n + 1 in the log hosting
that frame, resulting in the exit status O.                                       ⊔
                                                                                  ⊓


B.2      Proofs for Section 4

Lemma 2. For all labels σ, τ ∈ L(SK ) and indices j ∈ [k + m], if there ex-
ists a knitted-tree prefix where σ and τ are the logs of a node and its j th child
respectively, then consistent_child (τ, j, σ) holds.
6
     Recall that the execution of a statement may require multiple frames in the lace,
     especially if a rewind is involved.
                           Verifying Tree-Manipulating Programs via CHCs          31

Proof. We follow the definition of consistent_child presented in Appendix C.4.
The consistent_first_frames(τ, j, σ) predicate holds true because it follows the
definition of the active and active_child fields in the first frame of every node, as
detailed in Sec. 3.1. The next two blocks in the definition of consistent_child are
responsible for checking that every pair of frames connected by the prev and next
fields and belonging to different labels encodes a step in the current instruction,
according to the rules detailed in §3.1. The two connected frames may represent
a step downward (first block) or upward (second block) in the knitted-tree.
    Consider the downward direction, as the other case is symmetrical. A down-
ward connection between the frames σ a and τ b is detected in two cases:
 1. First, if σ a is occupied (i.e., not available), linked to τ b through the next
    field, and τ b is also occupied. Then, we apply the predicate ΨDown to check
    that the step is valid. Note that it is possible that in a valid knitted-tree τ b
    is available, even though σ a .next points to it, but only when σ a is the last
    frame of the lace.
 2. Second, when τ b is occupied and linked to σ a via its prev field. In that
    case, σ a must be occupied in any valid knitted-tree, and we again check the
    correctness of the step using ΨDown .                                          ⊔
                                                                                   ⊓

B.3    Proofs for Section 5
                                                     
Theorem 3. In the minimal model of Ckt P, m, n , Lab(σ) holds for a label σ
iff σ labels a node in some (m, n)-knitted-tree prefix K of P .

Proof. We present only the “if” direction of the theorem; the “only if” direction
is provided in Section 5.
    Let t be a node in K with log σ. We proceed by induction on the length ℓ of
the lace of K.
    Base case (ℓ = 1): The root of K has one frame in the lace. CHC I or CHC II
inserts σ into Lab, depending on whether 1 or 2 frames are unavailable in σ.
    Inductive step (ℓ > 1): Let Kℓ−1 be K with its the last frame of the lace
removed. By inductive hypothesis, its logs are in Lab. If σ is a log of Kℓ−1 , the
claim holds. Otherwise, σ includes the last frame in the lace of K, meaning that
the logs of t’s neighboring nodes (its parent and children) remain unchanged
from Kℓ−1 . By inductive hypothesis those logs belong to Lab. Depending on the
direction taken in the last step, σ is added to Lab via CHC III or CHC V, as
detailed in the above description of the individual CHCs.                        ⊔
                                                                                 ⊓

Theorem 4. Let I be an instance of the exit-status problem. Then, I admits a
positive answer if and only if the CHC system Cex (I) is unsatisfiable.

Proof. Let I = (P, k, m, n, Ex ). We prove the theorem by establishing the equiv-
alent statement: I admits a negative answer if and only if Cex (I) is satisfiable.
    For the “only if” direction, if I has a negative answer, no (m, n)-knitted-tree
of P has an exit status in Ex . Consider the interpretation of Lab containing
exactly the node labels from all (m, n)-knitted-tree prefixes of P . By Theorem 3,
32      M. Faella and G. Parlato
                                              
this is the minimal model of Ckt P, m, n and satisfies CHCs I-V. Since none of
these labels have an exit status in Ex , the interpretation also satisfies the query
VI, proving that Cex (I) is satisfiable.
    For the “if” direction, if Cex (I) is satisfiable, the interpretation of Lab in any
model of Cex (I) has the property that no label    in Lab has an exit status in Ex
(CHC VI). Since Cex (I) implies Ckt P, m, n , by Theorem 3 such interpretation
of Lab contains at least all the logs of the (m, n)-knitted-tree (prefixes) of P .
We conclude that the answer to the exit status problem is negative.                   ⊔
                                                                                      ⊓


B.4    Proofs for Section 5.1

Theorem 5 is an immediate consequence of Claim 1 of Theorem 2.

Theorem 6. If the answer to the exit status problem (P, m, n, {O, M, E}) is
negative, then the answer to the memory safety problem for P is positive.

Proof. Since no knitted-tree has exit status O, Claim 3 of Theorem 2 ensures
that no execution is infinite. Similarly, since no knitted-tree has an exit status
in {O, M, E}, Claim 2 guarantees no execution ends in an error. Thus, all exe-
cutions reach a final configuration.                                             ⊔
                                                                                 ⊓


C     Detailed Encoding

In this section, we describe in detail the predicates and functions appearing as
constraints in the CHCs that recognize knitted-trees.
    Consider again the system of CHCs described in Figure 3. Those CHCs are
based on the predicates first_frame, start, consistent_child , ΨInternal , ΨDown ,
ΨUp , and label _exit, each described in one of the following sections.


C.1    The First Frame of Non-Root Nodes

The predicate in this section is meant to constrain the first frame of every non-
root node of a knitted-tree. The only property to be enforced is a relationship
between the fields active and active_child : an auxiliary node (active = false)
that is not the root must be a leaf of the knitted-tree. Hence, no allocation
of new nodes can be performed in this node. This is enforced by setting the
active_child j flags to true for all indices j ∈ [k + 1, k + m]. Vice versa, all active
nodes start with m auxiliary children with indices k + 1, . . . , k + m, available for
allocation. We obtain the following predicate:
                                                                         
                           def             V
         first_frame(f ) = f.active ∧ j∈[k+1,k+m] ¬f.active_child j ∨
                                           V                             
                                 ¬f.active ∧ j∈[k+1,k+m] f.active_child j .
                              Verifying Tree-Manipulating Programs via CHCs        33

C.2    The Start of the Lace



The predicate start sets constraints on the first two frames at the root of any
knitted-tree. These frames must agree on the fields active and val . The prev
field of the second frame points to itself through the value (−, 2). For non-
empty input trees, the first frame must be active and the second frame makes
pb point to the root node, and active_child is non-deterministic on the first k
children, constraining only the children from index k + 1 to k + m as inactive.
For empty input trees, the first frame is inactive and the second frame sets pb to
nil, and active_child requires all children to be inactive. In both cases, pc 2 is set
to the first program statement label, with all the other pointer variables set to
nil.



         def
start(σ) = initial (σ) ∧
               σ.active 2 = σ.active 1 ∧ σ.val 2 = σ.val 1 ∧
               σ.pc 2 = 0 ∧ p∈PVP \{bp} σ.isnil 2p ∧
                             V
               h
                                            p := here⟩ ∧ ¬σ.isnil 2pb ∧ Non-empty input tree
                  σ.active 1 ∧ σ.event 2 = ⟨b
                                                    
                  V                               2
                    j∈[k+1,k+m] ¬σ.active_child   j   ∨
                
                  ¬σ.active 1 ∧ σ.event 2 = nop ∧ σ.isnil 2pb ∧         Empty input tree
                                               i
                  V                         2
                    j∈[k+m] ¬σ.active_child j     ,


where the initial predicate describes the distinguishing feature of the initial
frame of a lace – namely, having itself as predecessor:


                      initial (σ) = ¬σ.avail 2 ∧ (σ.prev 2 = (−, 2)) .
                                 def




C.3    Lace Termination



The function label _exit(σ) returns the exit status of any frame in σ, assuming
that at most one frame in a label is terminal. In the following, we denote by P (i)
the instruction located at program counter i in the program P .
34       M. Faella and G. Parlato



                        def
           continues(f ) = ¬f.avail ∧ frame_exit(f ) = N
                             
                             
                              C if P (f.pc) = exit
                             
                             E if f.event = err
                         def
        frame_exit(f ) =
                             M if f.event = oom
                             
                             
                               N otherwise.
                             
                             
                               C if i∈[2,n] ¬σ.avail i ∧ frame_exit(σ i ) = C
                                    W                                         
                             
                             
                                                      i
                                                                              
                             E if W                                  i
                                       i∈[2,n] ¬σ.avail ∧ frame_exit(σ ) = E
                             
                             
                             
                         def
          label _exit(σ) = M if i∈[2,n] ¬σ.avail i ∧ frame_exit(σ i ) = M
                                    W                                          
                             
                               O if ¬σ.avail n+1
                             
                             
                             
                             
                             
                               N otherwise.
                             
                         def                    
     label _exit(σ, Ex ) = label _exit(σ) ∈ Ex


C.4     Checking Parent-Child Consistency

The consistent_child (τ, j, σ) predicate checks that the label τ of the j-th child is
consistent with the label σ of the parent. It uses the predicates consistent_first_frames,
ΨDown , and ΨUp , defined later.

                         def
consistent_child (τ, j, σ) = consistent_first_frames(τ, j, σ) ∧
                Consistency of steps, when going down:
                  ^ h
                            ¬σ.avail a ∧ σ.next a = (j, b) ∧ ¬τ.avail b ∨
                                                                       
                  a∈[2,n]
                 b∈[2,n+1]                                                                   i
                               ¬τ.avail b ∧ τ.prev b = (↑, a)   → ΨDown (σ ≤a , j, τ <b , τ b ) ∧

                Consistency of steps, when going up:
                  ^ h
                            ¬τ.avail a ∧ τ.next a = (↑, b) ∧ ¬σ.avail b ∨
                                                                       
                  a∈[2,n]
                 b∈[2,n+1]                                                                      i
                               ¬σ.avail b ∧ σ.prev b = (j, a)        → ΨUp (τ ≤a , j, σ <b , σ b ) .

    It is worth pointing out that different child labels may be consistent with
the same parent label, just like two different parent labels may be consistent
with the same child label. First, consistent_child only constrains frames that are
directly involved in an interaction between parent and child, i.e., pairs of frames
belonging to these different nodes and adjacent in the lace. Now, consider a pair
of frames that are adjacent in the lace and belong to two different nodes (parent
and child). Here is a description of how consistent_child constrains each field in
those frames:

 avail : this field must be false, because frames involved in an interaction belong
   to the lace;
                           Verifying Tree-Manipulating Programs via CHCs            35

 active: this field is directly constrained only in the first frame of each label,
    where its value must follow the backbone rules described in Section 3.1; this
    is ensured by the auxiliary predicate consistent_first_frames; the value in
    the subsequent frames of each label is only constrained indirectly, by the
    semantics of the new and free instructions;
 val : the default constraint for this field is to have the same value as the preceding
    frame in the same log; the only exception is the last step of the instruction
    p → data := exp, when the current value of p has been ascertained via
    rewinding: in such a step the value of the val field of the new frame takes
    the value of the expression exp;
 pc: the program counter must be consistent with the corresponding pc on the
    other side of the interaction; i.e., the two pc’s must be equal if a rewind op-
    eration is ongoing, and otherwise the instruction being executed is complete
    and the pc advances according to the control-flow graph of P ;
 d: the value of this field in the two frames of an interaction is the same, except
    in the last step of an instruction of the type d := p → data, when the current
    value of p has been ascertained via rewinding;
 upd p : the auxiliary predicates Ψ∗ constrain these fields to follow the rules de-
    scribed on page 9;
 isnil p : this field generally keeps its value in an interaction, except in the last
    step of an assignment to p; specifically, it can switch from true to false in
    the last step of p := q or p := q → pfield , when q is not nil and rewinding was
    needed to find its current value; moreover, it can switch from false to true
    in the last step of p := q → pfield , when q is not nil, rewinding was needed,
    and then q → pfield is found to be nil;
 event: the event in the second frame of an interaction is dictated by the program
    instruction being executed and by the meaning of each event; for example,
    during a rewind process, the events rwdi and rwdi,p are used; the end of a
    rewinding may be marked by a event of the types ⟨pfield := p⟩, ⟨pfield := nil⟩,
    or ⟨p := here⟩; in some cases, the final event is simply nop;
 next and prev : in a pair of interacting frames these fields must connect the two
    frames with each other; i.e., the next field of the first frame points to the
    second frame, and the prev field of the second frame points to the first one.

   The following auxiliary predicates are used within consistent_child . The
consistent_first_frames predicate describes the initial value of the active field,
that starts as true on all nodes of the knitted-tree that correspond to nodes of
the input tree, and false elsewhere.

                                 def
consistent_first_frames(τ, j, σ) = initial (σ) ∨ σ.active 1 ∧ τ.active 1 → σ.active 1 ∧
                                                                                    

                                     j > k → ¬τ.active 1 ∧ σ.active_child 1j = τ.active 1 .
                                                         


    We now present the three predicates that describe the next frame in the
lace, depending on the direction of the next step. The first predicate, ΨInternal ,
describes internal steps. It invokes the general predicate step that checks a single
36      M. Faella and G. Parlato

step in a lace, passing two adjacent frames from the same log. In addition, it
makes sure that the upd p flags are all false after an internal step, according to
the meaning of those flags, as described on page 9.
In the following formulas, for a label σ and a frame f we write σ · f to denote
the label obtained by the replacing the first available frame of σ with f .


                   def
  ΨInternal (σ, f ) = len(σ, a) ∧ continues(σ a ) ∧ σ.next a = (−, a + 1) ∧
                                                                  V
                      f.prev = (−, a) ∧ step(σ, a; σ · f, a + 1) ∧ p∈PVP ¬f.upd p .

    The following predicates ΨDown and ΨUp describe the next frame in the lace,
when the current step involves a change of node, either from a node down to
its j-th child or from a node up to its parent. In particular, these predicates
constrain the upd flags in the new frame to respect their meaning, as described
on page 9.
    Consider how the last two lines in ΨUp (τ, j, σ, f ) relate to the intended be-
havior of the upd flags. In that context, τ a is a frame in the j-th child of a parent
node with log σ, and the next frame in the lace is f , to be appended on top of
σ. Note that in this situation the previous frame in the log of the parent (i.e.,
σ b−1 ) is followed in the lace by a frame in the j-th child. Now, for every pointer
variable p ∈ PV P , the upd p flag when going back to the parent is true iff p is not
nil at that time and we observe a marker for an update to p within the frames of
the child located between the step down and the step back up. If the update to
p was performed in one of the frames of the child, the marker is a direct event of
the type ⟨p := here⟩. If instead the update occurs further below in the subtree
rooted in the child, the marker observed in the child is a upd p field set to true,
as encoded in the last lines of ΨUp .
    Finally, note that ΨUp is also responsible for synchronizing the active_child
field in the parent with the active field in the child; these fields may become
out-of-sync after a free operation performed on the child.


                 def
ΨDown (σ, j, τ, f ) = len(σ, a) ∧ continues(σ a ) ∧ σ.next a = (j, b) ∧ len(τ, b − 1) ∧
                      f.prev = (↑, a) ∧ step(σ, a; τ · f, b) ∧
                         ^ h               
                               f.upd p ↔ ¬f.isnil p ∧ b > 2 ∧ τ.next b−1 = (↑, a′ ) ∧
                       p∈PVP                                                             i
                                                  c
                                                          := here⟩ ∨ c∈[a′ +1,a] σ.upd cp
                               W                                    W
                                 c∈[a′ ,a] σ.event = ⟨p

                 def
  ΨUp (τ, j, σ, f ) = len(τ, a) ∧ continues(τ a ) ∧ τ.next a = (↑, b) ∧ len(σ, b − 1) ∧
                       f.prev = (j, a) ∧ step(τ, a; σ · f, b) ∧ f.active_child = τ.active a ∧
                         ^ h               
                               f.upd p ↔ ¬f.isnil p ∧ b > 2 ∧ σ.next b−1 = (j, a′ ) ∧
                       p∈PVP                                                               i
                                                  c
                                                           := here⟩ ∨ c∈[a′ +1,a] τ.upd cp
                               W                                     W
                                 c∈[a′ ,a] τ.event = ⟨p                                        .
                                 Verifying Tree-Manipulating Programs via CHCs                           37

C.5     Individual Statements

The predicate step(σ, a; τ, b) holds if τ b is the logically correct frame to follow
σ a in a lace. The structure of this predicate comprises an implication for each
type of instruction in our programming language, except for exit. The exit
instruction does not produce a step, because just having the program counter
point to it identifies a terminating execution.
                def
step(σ, a; τ, b) =
    P (σ.pc a ) = skip                                      → step_skip(σ a , τ b ) ∧
    P (σ.pc a ) = (p := nil)                                → step_assgn_nil (σ a , τ b , p) ∧
    P (σ.pc a ) = (d := exp)                                → step_assgn_exp(σ a , τ b , d , exp) ∧
    P (σ.pc a ) = (dbool := (p = q))                        → step_assgn_cond (σ, a, τ, b, dbool , p, q) ∧
    P (σ.pc a ) = (p := q)                                  → step_assgn_ptr (σ, a, τ, b, p, q) ∧
    P (σ.pc a ) = (p := q → pfield )                        → step_assgn_from_field (σ, a, τ, b, p, q, pfield ) ∧
    P (σ.pc a ) = (p → pfield := q)                         → step_assgn_to_field (σ, a, τ, b, p, q, pfield ) ∧
    P (σ.pc a ) = (p → val := exp)                          → step_assgn_to_data(σ, a, τ, b, p, exp) ∧
    P (σ.pc a ) = (d := p → val )                           → step_assgn_to_var (σ, a, τ, b, d, p) ∧
    P (σ.pc a ) = (new p)                                   → step_new (σ a , τ b−1 , τ b , p) ∧
    P (σ.pc a ) = (free p)                                  → step_free(σ, a, τ, b, p) ∧
     P (σ.pc a ) = (while p = q) ∨
     P (σ.pc a ) = (if p = q)
                              
                                                            → step_cmp_ptr (σ, a, τ, b, p, q, false) ∧
     P (σ.pc a ) = (while ¬(p = q)) ∨
     P (σ.pc a ) = (if ¬(p = q))
                                     
                                                            → step_cmp_ptr (σ, a, τ, b, p, q, true) ∧
     P (σ.pc a ) = (while r(exp 1 , . . . , exp l )) ∨
     P (σ.pc a ) = (if r(exp 1 , . . . , exp l ))
                                                  
                                                            → step_local _branch(σ, a, τ, b, r, exp 1 , . . . , exp l ) .


Default values. Regardless of any specific instruction, most fields in any new
frame of the lace are set to their default values, as described in Section 3.1. The
following default predicate represents the full case, where all fields that have
default values are constrained. In the subsequent predicates, we add subscripts
to default to specify which fields follow the default rules.
                                  def
   default(f prev , f below , f ) = ¬f.avail ∧                                          avail
                                                         below
                                        f.active = f             .active ∧              active
                                                    below
                                        f.val = f     .val ∧                            val
                                        V                prev
                                          d∈DVP f.d = f       .d ∧                      d
                                        V                      prev
                                          p∈PVP f.isnil p = f       .isnil p ∧          isnil
                                        f.event = nop ∧                                 event
                                        f.pc = f prev .pc ∧                             pc
                                        default active_child (f prev , f below , f ).   active_child
38       M. Faella and G. Parlato

The default for the active_child flags requires a little more care:
                                                 def
default active_child (f prev , f below , f ) =
                                             
                     f.prev = (j, ∗) → f.active_child j = f prev .active ∧
                                             V                           below
                                                                                              
                                               j̸=i f.active_child i = f       .active_child i ∧
                     f.prev ̸= (j, ∗) → i∈[k+m] f.active_child i = f below .active_child i .
                                             V                                                   



Internal instructions. Internal instructions push a single new frame on the
current node of the knitted-tree. As our first type of internal instruction, we
describe the step_assgn_nil predicate. As explained earlier, its encoding simply
pushes a new frame f2 on the current node, with the isnil p flag set to true. All
the other fields of the new frame take their default value, except the program
counter, which advances to the next instruction:
                                                  def
          step_assgn_nil (f1 , f2 , p) = (f1 .next = −) ∧                                              p := nil
                                        V
                         f2 .isnil p ∧ q∈PVP \{p} (f2 .isnil q = f1 .isnil q ) ∧
                                     advance_pc(f1 , f2 )∧
                                     default avail,active,val,d,event,active_child (f1 , f1 , f2 ).

The following auxiliary predicate encodes the advancement of the program counter:
                                               def                    
                          advance_pc(f1 , f2 ) = f2 .pc = succ(f1 .pc) .

Next, we present the predicate that encodes the new instruction. Note that a
failed new is only justified if all children of the current node with position in
[k + 1, k + m] are active (i.e., currently allocated).

step_new (f, f ′ , f ′′ , p) =
                               def
                                                                                                       new p
            Case 1: Out-of-memory error
            V
                                                                                   ′′
                 j∈[k+1,k+m] f.active_child j ∧ f.next = (−, ∗) ∧ f                   .instr = oom ∧
                                                                                 
                default avail,active,val,d,pc,isnil,active_child (f, f ′ , f ′′ )   ∨
            Case 2: Normal case
                         _                                       ^                                     
                                     ¬f.active_child j ∧              f.active_child i ∧ f.next = (j, ∗) ∧
                j∈[k+1,k+m]                                   i∈[k+1,j−1]
                                          ^
                     ′′                                  ′′
                                                                              
             ¬f .isnil p ∧                              f .isnil q = f.isnil q ∧
                                     q∈PVP \{p}

             f .event = ⟨p := here⟩ ∧ f ′′ .active ∧ advance_pc(f, f ′′ ) ∧
                ′′
                                                              
             default avail,val,d,active_child (f, f ′ , f ′′ ) .
                              Verifying Tree-Manipulating Programs via CHCs                         39

The following predicate handles assignments of arbitrary data expressions to
data variables.

                                            def
     step_assgn_exp(f1 , f2 , d, exp) =                                                             d := exp
                                                                      ′          ′
                                                  
                          f1 .next = (−, ∗) ∧ f2 .d = exp[d 7→ f1 .d ]d′ ∈DVP ∧
                         V                    ′       ′
                           d′ ∈DVP \{d} (f2 .d = f1 .d ) ∧ advance_pc(f1 , f2 )∧
                         default avail,active,val,isnil,event,active_child (f1 , f1 , f2 ) .

Finally, the following is the straightforward encoding of the skip statement.

                          def                
   step_skip(f1 , f2 , p) = f1 .next = (−, ∗) ∧ advance_pc(f1 , f2 ) ∧                              skip
                             default avail,active,val,d,isnil,event,active_child (f1 , f1 , f2 ).



Walking instructions. The following walking instructions may add multiple
frames to different nodes of the knitted-tree. The first such instruction is the
assignment of the form p := q, which may require rewinding the lace to find
the node currently pointed by q. In fact, the encoding distinguishes three cases:
(1) when q is nil, (3) when q points elsewhere, and we need to start or keep
rewinding the lace, (2) when q points to the current node (i.e., the node with
label σ). The predicates governing the rewinding operation are presented later
in Section C.7.

                                                      def
           step_assgn_ptr (σ, a, τ, b, p, q) =                                                      p := q
                  Case 1: q is nil; use the encoding for p := nil
                                                                     
                      σ a .isnil q ∧ step_assgn_nil (σ a , τ b , p)        ∨
                  Case 2: q points elsewhere; start or keep rewinding
                  rewind (σ, a, τ, b, q) ∨
                  Case 3: q points to the current node
                                                                         
                      stop_rewind (σ, a, q) ∧ set_ptr _here(σ a , τ b , p) .


The auxiliary predicate set_ptr _here pushes a frame on the current node with
⟨p := here⟩ and updates isnil accordingly.

                             def                
  set_ptr _here(f1 , f2 , p) = f1 .next = (−, ∗) ∧ advance_pc(f1 , f2 ) ∧
                                 f2 .event = ⟨p := here⟩ ∧
                                               V                                    
                                 ¬f2 .isnil p ∧ q∈PVP \{p} f2 .isnil q = f1 .isnil q ∧
                                 default avail,active,val,d,active_child (f1 , f1 , f2 ) .
40      M. Faella and G. Parlato

The following predicate encodes the statements of the form p → pfield := q.

                                                       def
 step_assgn_to_field (σ, a, τ, b, p, q, pfield ) = find _or _fail (σ, a, τ, b, p) ∨   p → pfield := q
        p points to the current node:

           stop_rewind (σ, a, p) ∧ σ a .next = (−, a + 1) ∧ advance_pc(σ a , τ b ) ∧
           
               ¬σ a .isnil q ∧ τ b .event = ⟨pfield := q⟩ ∨
                                                          

                                                          
               σ a .isnil q ∧ τ b .event = ⟨pfield := nil⟩ ∧
                                                                              !
                                                             a    b−1     b
           default avail,active,val,d,isnil,active_child (σ , τ         ,τ ) .



   The predicate step_assgn_nil _to_field , corresponding to the statements of
the form p → pfield := nil, is a simple variant of the above, that only sets the
event ⟨pfield := nil⟩.
   Next, we deal with the two instructions that write or read the data field of a
node.



                                                 def
step_assgn_to_data(σ, a, τ, b, p, exp) = find _or _fail (σ, a, τ, b, p) ∨             p → val := exp
       p points to the current node:
       
        stop_rewind (σ, a, p) ∧ σ a .next = (−, a + 1) ∧ advance_pc(σ a , τ b ) ∧
                                                                   

        τ b .val = exp d 7→ σ a .d d∈DV ∧
                                   
                                            P
                                                                            
        default avail,active,d,isnil,event,active_child (σ a , τ b−1 , τ b ) .




                                           def
step_assgn_to_var (σ, a, τ, b, d, p) = find _or _fail (σ, a, τ, b, p) ∨               d := p → val
       p points to the current node:
       
        stop_rewind (σ, a, p) ∧ σ a .next = (−, a + 1) ∧ advance_pc(σ a , τ b ) ∧
                                                                    

        τ b .d = σ a .val ∧ d′ ∈DVP \{d} (τ b .d′ = σ a .d′ ) ∧
                            V
                                                                              
        default avail,active,val,isnil,event,active_child (σ a , τ b−1 , τ b ) .


    The following predicate handles the deallocation of the node pointed by a
given pointer.
                                   Verifying Tree-Manipulating Programs via CHCs                        41



                                 def
  step_free(σ, a, τ, b, p) = find _or _fail (σ, a, τ, b, p) ∨                                            free p
            p points to the current node:
            
                stop_rewind (σ, a, p) ∧ σ a .next = (−, ∗) ∧ advance_pc(σ a , τ b ) ∧
                                                          

             ¬τ b .active ∧
               ^ 
                         points_here(σ, a, q) → τ b .isnil q ∧
                                                            

                q∈PVP
                                                                                    
                      ¬points_here(σ, a, q) → τ b .isnil q = σ a .isnil q                ∧
                                                                        
             default avail,val,d,event,active_child (σ a , τ b−1 , τ b ) .

    The following auxiliary predicates handle the search for the current value of
a pointer variable p, including issuing an error if p is nil.
                                                                  
                                def
 find _or _fail (σ, a, τ, b, p) = σ a .isnil p ∧ error (σ a , τ b ) ∨ rewind (σ, a, τ, b, p)
                                    def                      
                   error (f1 , f2 ) = f1 .next = (−, ∗) ∧ (f2 .event = err) ∧
                                        default avail,active,val,d,isnil,pc,active_child (f1 , f1 , f2 ) .

    Next, we move to the instruction that assigns to a Boolean variable the
result of the comparison between two pointers. If at least one of the two point-
ers is nil, the comparison can be resolved locally. Otherwise, a rewind opera-
tion may be necessary. The auxiliary predicates rewind2 , stop_rewind2 , and
are_equal _after _rewind are described in Sec. C.7.
                                                    def
step_assgn_cond (σ, a, τ, b, dbool , p, q) =                                                             dbool := (p = q)
        Case 1: at least one pointer is nil
        
             σ a .isnil p ∨ σ a .isnil q ∧
                                        

             σ a .next = (−, ∗) ∧ advance_pc(σ a , τ b ) ∧
                                    

            τ b .dbool = σ a .isnil p ↔ σ a .isnil q ) ∧
                                                      
            V                       b      a
               d∈DVP \{dbool } (τ .d = σ .d) ∧
                                                                                  
            default avail,active,val,isnil,event,active_child σ a , τ b−1 , τ b          ∨

        Case 2: start or keep rewinding
        rewind2 (σ, a, τ, b, p, q) ∨
        Case 3: stop rewinding
        
            stop_rewind2 (σ, a, p, q) ∧ σ a .next = (−, ∗) ∧ advance_pc(σ a , τ b ) ∧
                                                             

             τ b .dbool = are_equal _after _rewind (σ, a, p, q) ∧
                                                               
             V                    b      a
                d∈DVP \{dbool } (τ .d = σ .d) ∧
42        M. Faella and G. Parlato
                                                                                    
              default avail,active,val,isnil,event,active_child (σ a , τ b−1 , τ b ) .

   The most complex walking instruction is the assignment of the form p :=
q → pfield , because it may involve two consecutive rewinding phases.
                                                              def
step_assgn_from_field (σ, a, τ, b, p, q, pfield ) =                                         p := q → pfield
          Case 1: q is nil; null pointer dereference
           σ a .isnil q ∧ error (σ a , τ b ) ∨
                                            

          Case 2a: phase I; q points elsewhere; start or keep rewinding
           σ a .event ̸= rwd∗,∗ ∧ rewind (σ, a, τ, b, q) ∨
                                                        

          Case 2b: phase II; r points elsewhere; start or keep rewinding
           σ a .event = rwdi,r ∧ rewind _special (σ, a, τ, b, r, i)
                                                                              
                                                                                   ∨
          Case 3a: end of phase I; q points to the current node

           σ a .event ̸= rwd∗,∗ ∧ stop_rewind (σ, a, q) ∧
           
              is_pfield _nil (σ, a, pfield )∨
            (is_pfield _implicit(σ, a, pfield ) ∧ ¬σ a .active_child index (pfield) ) →
                                                                                     
                                             
              step_assign_nil (σ a , τ b , p) ∧
           
             is_pfield _implicit(σ, a, pfield ) ∧ σ a .active_child index (pfield) →
                                                                                  

                  σ a .next = (index (pfield ), b) ∧ advance_pc(σ a , τ b ) ∧
                  τ b .event = ⟨p := here⟩ ∧
                                                                                 
               default avail,active,val,d,isnil,active_child (σ a , τ b−1 , τ b ) ∧
              ^                                                                       
                            is_pfield _ptr (σ, a, pfield , r, i) ∧ points_here(σ, i, r) →
          r∈PVP ,i∈[2,n]                               
                         set_ptr _here(σ a , τ b , p) ∧
              ^                                                                         
                            is_pfield _ptr (σ, a, pfield , r, i) ∧ ¬points_here(σ, i, r) →
          r∈PVP ,i∈[2,n]                                       !
                                                             
                         rewind _special (σ, a, τ, b, r, i)           ∨

          Case 3b: end of phase II; r points to the current node
                                                                                      
              σ a .event = rwdi,r ∧ points_here(σ, i, r) ∧ set_ptr _here(σ a , τ b , p) .

The following auxiliary predicates check the value of the node field pfield at
(σ, a).

     pfield is nil at the frame (σ, a) of the lace:
                                       def
     is_pfield _nil (σ, a, pfield ) =
                                   Verifying Tree-Manipulating Programs via CHCs                               43

             _                                                        ^                                   
                         σ i .event = ⟨pfield := nil⟩ ∧                      σ j .event ̸= ⟨pfield := ∗⟩
           i∈[2,a]                                               j∈[i+1,a]

  pfield has the same value as r at the frame (σ, a) of the lace:
                                             def
  is_pfield _ptr (σ, a, pfield , r, i) =
                                                      ^
           σ i .event = ⟨pfield := r⟩ ∧                        σ j .event ̸= ⟨pfield := ∗⟩
                                                   j∈[i+1,a]

  pfield has never been assigned up to the frame (σ, a) of the lace:
                                              def
                                                      ^
  is_pfield _implicit(σ, a, pfield ) =                         σ j .event ̸= ⟨pfield := ∗⟩ .
                                                     j∈[2,a]


C.6    Boolean Conditions and Control-Flow Instructions
Control-flow statements if and while have two successors, depending on the
value of their Boolean condition. To support those statements, we introduce a
3-argument version of the predicate that advances the program counter:
                                        def                           
            advance_pc(f1 , f2 , cond ) = f2 .pc = succ(f1 .pc, cond ) .

The next predicate handles the Boolean conditions of the form p = q:
                                               def
step_cmp_ptr (σ, a, τ, b, p, q, neg) =                                                                         if p = q
                     Case 1: at least one pointer is nil
                     
                          σ a .isnil p ∨ σ a .isnil q ∧ σ a .next = (−, a + 1) ∧
                                                                             

                         advance_pc(σ a , τ b , xor(neg, σ a .isnil p ↔ σ a .isnil q )) ∧
                                                                                                 
                         default avail,active,val,d,isnil,event,active_child σ a , τ b−1 , τ b         ∨

                     Case 2: start or keep rewinding
                     rewind2 (σ, a, τ, b, p, q) ∨
                     Case 3: stop rewinding
                     
                         stop_rewind2 (σ, a, p, q) ∧ σ a .next = (−, a + 1) ∧
                                                                           

                      advance_pc σ a , τ b , xor(neg, are_equal _after _rewind (σ, a, p, q)) ∧
                                                                                                 
                                                                                              
                      default avail,active,val,d,isnil,event,active_child (σ a , τ b−1 , τ b ) .

The next predicate handles the Boolean conditions based on the content of the
data variables. Those conditions can always be resolved locally.
                                                                 def
step_local _branch(f1 , f2 , r, exp 1 , . . . , exp l ) =                                                      if r(exp 1 , . . . , exp l )
                         
       f1 .next = (−, ∗) ∧
                                                                                          
        advance_pc f1 , f2 , r(exp 1 [d 7→ f1 .d]d∈DVP , . . . , exp l [d 7→ f1 .d]d∈DVP ) ∧
        default avail,active,val,d,isnil,event,active_child (f1 , f1 , f2 ) .
44       M. Faella and G. Parlato

C.7     Rewinding the Lace

The following predicate is true when the pointer q is not nil at (σ, a) and its
value cannot be ascertained by analyzing the label σ alone. In that case, it is
necessary to perform at least one rewinding step, represented by the frame (τ, b).
                                     def
      rewind (σ, a, τ, b, q) =
             σ a .next = (dir , b) ∧ ¬σ a .isnil q ∧ a′ = cur _rewind _pos(σ, a) ∧
             ¬points_here(σ, a′ , q) ∧ a′′ = last_upd (σ, a′ , q) ∧
                   ′′                                ′
             σ a .prev = (dir , b′ ) ∧ τ b .next = (dir ′ , a′′ ) ∧
             b = last_visit(τ, dir ′ , a′ ) + 1 ∧ τ b .event = rwdb′ ∧
             default avail,active,pc,val,d,isnil,active_child (σ a , τ b−1 , τ b ) .




                               a′′                             a′                        a
        σ    ...        upd q = true           ...   event = nop          ...   event = rwda′         ...



                           τ         ...                 ...              event = rwdb′         ...

                                                b′                  b−1         b


Fig. 4: An example of the rewind (σ, a, τ, b, q) predicate. Arrows connect a frame
to its successor in the lace.


    The above predicate uses several auxiliary functions and predicates. The func-
tion cur _rewind _pos(σ, a) returns the position within σ of the current rewind-
ing. If the rewinding is just starting, this position will simply be a. Otherwise, the
current instruction will be of the type rwdb , and the current rewinding position
will be b.
                                     (
                                 def  b if σ a .event = rwdb for some b ∈ [n],
        cur _rewind _pos(σ, a) =
                                       a otherwise.

The predicate points_here(σ, a, q) holds when q points to the node labeled with σ
when the lace is at (σ, a). This occurs when an instruction of the type ⟨q := here⟩
is found in σ at position at most a, and all upd q flags from that position to
position a are false.
                           def
                               _                               ^            
     points_here(σ, a, q) =          σ i .event = ⟨q := here⟩ ∧   ¬σ j .upd q .
                                           i∈[2,a]                                  j∈[i+1,a]
                                     Verifying Tree-Manipulating Programs via CHCs                     45

When the value of pointer q cannot be ascertained by the current label σ, we
search for its most recent assignment by identifying the latest position in σ that
comes before position a and contains the flag upd q = true. This is the job of the
function last_upd (σ, a, q). If no position in σ before a contains upd q = true, this
function returns 2, because in that case the rewinding operation must go back
to the frame that led to the first visit to the current node.
                     (
                  def max{i ∈ [2, a] | σ i .upd q = true}              if {i ∈ [2, a] | σ i .upd q = true} =
                                                                                                           ̸ ∅
last_upd (σ, a, q) =
                      2                                                otherwise.

 The last auxiliary function, last_visit(τ, dir , j), returns the position of the last
frame from τ whose next field is of the form (dir , c) for some c ≤ j.
                                        def
          last_visit(τ, dir , j) = max{i ∈ [n] | τ i .next = (dir , c), c ≤ j} .

Searching for two pointers. We describe a variant of the predicate rewind ,
for the instructions that search for two different pointers at the same time. In
fact, this only happens in the encoding of the Boolean condition q1 = q2 .
                                                 def
           rewind2 (σ, a, τ, b, q1 , q2 ) =
                   σ a .next = (dir , b) ∧ ¬σ a .isnil q1 ∧ ¬σ a .isnil q2 ∧
                   a′ = cur _rewind _pos(σ, a) ∧
                   ¬points_here(σ, a′ , q1 ) ∧ ¬points_here(σ, a′ , q2 ) ∧
                   a′′ = max last_upd (σ, a′ , q1 ), last_upd (σ, a′ , q2 ) ∧
                                 
                           ′′                                ′
                        σ a .prev = (dir , b′ ) ∧ τ b .next = (dir ′ , a′′ ) ∧
                        b = last_visit(τ, dir ′ , a′ ) + 1 ∧ τ b .event = rwdb′ ∧
                        default avail,active,pc,val,d,isnil,active_child (σ a , τ b−1 , τ b ) .
Next, the version of rewinding used by the second phase of the statement p :=
q → pfield .
      rewind _special (σ, a, τ, b, r, a′ ) =
                                                       def



                            σ a .next = (dir , b) ∧ ¬σ a .isnil r ∧
                            ¬points_here(σ, a′ , r) ∧ a′′ = last_upd (σ, a′ , r) ∧
                                ′′                               ′
                            σ a .prev = (dir , b′ ) ∧ τ b .next = (dir ′ , a′′ ) ∧
                            b = last_visit(τ, dir ′ , a′ ) + 1 ∧ τ b .event = rwdb′ ,r ∧
                            default avail,active,pc,val,d,isnil,active_child (σ a , τ b−1 , τ b ) .
    The following predicates check whether the search for one or two pointers is
finished because those variables point to the current node (i.e., the node with
label σ):

         stop_rewind (σ, a, q) = ¬σ a .isnil q ∧ a′ = cur _rewind _pos(σ, a) ∧
                                        def



                                              points_here(σ, a′ , q)
                                        def
   stop_rewind2 (σ, a, q1 , q2 ) = stop_rewind (σ, a, q1 ) ∨ stop_rewind (σ, a, q2 ).
46        M. Faella and G. Parlato

    The following predicate is used by the instructions that have already searched
for two pointers and want to check whether they are equal.
                                          def
     are_equal _after _rewind (σ, a, p, q) =
      a′ = cur _rewind _pos(σ, a) ∧ points_here(σ, a′ , p) ∧ points_here(σ, a′ , q) .
