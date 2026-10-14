                                                  Proving and Disproving Programs with
                                                          Shared Mutable Data

                                                                   Georg Schmid and Viktor Kunčak
arXiv:2103.07699v1 [cs.LO] 13 Mar 2021




                                                                       LARA, EPFL, Switzerland
                                                                {georg.schmid, viktor.kuncak}@epfl.ch



                                                 Abstract. We present a tool for verification of deterministic programs
                                                 with shared mutable references against specifications such as assertions,
                                                 preconditions, postconditions, and read/write effects. We implement our
                                                 tool by encoding programs with mutable references into annotated purely
                                                 functional recursive programs. We then rely on function unfolding and
                                                 the SMT solver Z3 to prove or disprove safety and to establish program
                                                 termination. Our tool uses a new translation of programs where frame
                                                 conditions are encoded using quantifier-free formulas in first-order logic
                                                 (instead of relying on quantifiers or separation logic). This quantifier-free
                                                 encoding enables SMT solvers to prove safety or report counterexamples
                                                 relative to the semantics of procedure specifications. Our encoding is
                                                 possible thanks to the expressive power of the extended array theory of
                                                 the Z3 SMT solver. In addition to the ability to report counterexamples,
                                                 our tool retains efficiency of reasoning about purely functional layers of
                                                 data structures, providing expressiveness for mutable data but also a
                                                 significant level of automation for purely functional aspects of software.
                                                 We illustrate our tool through examples manipulating mutable linked
                                                 structures and arrays. 1

                                                 Keywords: verification · satisfiability modulo theories · shared mutable
                                                 data structures · array theory · dynamic frames


                                         1     Introduction
                                         Formal verification of programs with shared mutable data structures is a long-
                                         standing problem. Among the most promising techniques used in today’s veri-
                                         fication tools are separation logic [15] with bi-abduction [4] implemented in the
                                         Infer tool [5] used by Facebook and dynamic frames [9] realized in tools includ-
                                         ing Dafny [10] and used to verify complex software systems at Microsoft [7].
                                         Separation logic and dynamic frames are closely related, as demonstrated by the
                                         approach in the VeriFast tool [16].
                                             This paper presents a tool for reasoning about mutable programs in a subset
                                         of the Scala programming language [14]. Like the dynamic frames approach, we
                                         use defined or constrained sets of objects to specify frame conditions. Like Dafny,
                                         1
                                             This manuscript is submitted for peer review to CAV 2021 in January 2021 and may
                                             only be used to facilitate peer review process for this conference.
2       Georg Schmid and Viktor Kunčak

our tool uses SMT solvers to establish properties instead of dedicated symbolic
execution for heap-manipulating programs in several other approaches. We also
model the heap as a function from storage locations to values.
    However, our encoding of frame conditions is different from the one in Dafny.
Unlike Dafny, which reduces programs to a guarded-command language Boogie
[2], we reduce our programs to recursive functional programs that manipulate
rich data types supported by the Z3 SMT solver [12], building on top of the pub-
licly available Stainless verification infrastructure for functional programs [6].
Whereas the encoding in Dafny makes use of universal quantifiers with triggers
to encode frame conditions (expressing that all non-modified locations remain
the same), we avoid quantifiers and instead use a generalized theory of arrays [13]
of Z3. This expressive theory of arrays comes with completeness guarantees for
satisfiability checking of quantifier-free formulas combining arrays and other the-
ories using model-based theory combination [11]. Thanks to this new encoding
and the decision procedures of Z3, our verification tool can report meaningful
counterexamples for invalid properties, even in the cases where the bodies of
methods are abstracted by their modifies clauses. In contrast, SMT solvers typi-
cally cannot report counterexamples to satisfiability for formulas with universal
quantifiers.
    The fact that our tool reduces verification conditions to functional programs
also allows users of our tool to leverage the expressive power of recursive func-
tional programming in implementation and specification. Our tool need not en-
code immutable algebraic data types using the heap nor add heap arguments to
pure functions. The result is a better verification experience on a mix of purely
functional and mutable code, compared to a more uniform encoding.
    In this paper we use a running example to outline how to use our tool to
specify and verify Scala programs that contain mutable data. We then sketch our
encoding into recursive functions via the extended array theory [13] and discuss
our experience with the tool on verifying shared mutable data structures.


2   Example

To illustrate a mix of functional and imperative programming, Figure 1 shows
a binary tree data structure whose interior nodes are immutable but whose
leaves store mutable references of generic type T. The code is accepted by the
standard Scala 2.12 compilation pipeline given appropriate library imports. Our
tool supports a fragment of Scala with functional features (such as pure first-class
functions) as well as imperative features (mutable fields) and object-oriented
features (traits and dynamic dispatch). For any class, users explicitly opt into
mutability and heap reasoning by inheriting from AnyHeapRef. Our focus is
the method def tmap(f: T ⇒ T) on the Tree class, which applies an in-place
transformation f to all leaf cells. For example, given a tree: Tree[BigInt], invoking
tree.tmap(n ⇒ n + 1) increments the values in all the leaves of tree by one.
The method recursively traverses the tree and updates all cells upon reaching
the leaves. As written, the code is sequential. That said, when all leaf cells
                         Proving and Disproving Programs with Shared Mutable Data       3


 1   case class Cell[T](var value: T) extends AnyHeapRef
 2
 3   case class Leaf[T](data: Cell[T]) extends Tree[T]
 4   case class Branch[T](left: Tree[T], right: Tree[T]) extends Tree[T]
 5   sealed abstract class Tree[T] {
 6     @ghost def repr: Set[AnyHeapRef] = this match { // all cells in the tree
 7       case Leaf(data) ⇒ Set[AnyHeapRef](data)
 8       case Branch(left, right) ⇒ left.repr ++ right.repr
 9     }
10
11       def tmap(f: T ⇒ T): Unit = { // minimal specification
12         reads(repr)
13         modifies(repr)
14         decreases(this)
15
16           this match {
17             case Leaf(data) ⇒ data.value = f(data.value)
18             case Branch(left, right) ⇒ left.tmap(f); right.tmap(f)
19           }
20       }
21   }

     Fig. 1. A tree with mutable leaves and a parallelizable in-place map, including read
     and write frame conditions and a termination measure.


     are distinct, the updates in subtrees can all proceed in parallel, without race
     conditions, resulting in logarithmic algorithm depth [3] for balanced trees.
         Figure 1 is also a minimally specified program accepted by our tool, which
     automatically verifies the conformance of tmap to its declared effects. The reads
     clause indicates that the only mutable references that tmap reads are given by the
     value returned from auxiliary function repr, which computes the set of mutable
     cells in a given tree. Similarly, modifies indicates that these are the only sets the
     method is allowed to modify, which means that all other mutable objects remain
     the same after a call to tmap. Finally, the decreases clause provides an explicit
     decreasing measure on the size of the receiver object of tmap that enables the
     system to show that the function terminates. (For the simpler function repr, the
     system automatically infers the termination measure.) The @ghost annotation
     ensures that the repr function is not accidentally executed, but can only be used
     in specifications that are erased at run time.
         If we try to omit a reads or modifies clause, or incorrectly define repr to not
     descend into subtrees, the tool reports a counterexample state detecting that
     the specification reads or modifies is violated, with a message such as
     tmap body assertion: reads of TreeImmutMapGenericExample.Tree.tmap invalid

     pointing to an undeclared effect in line 18 of Figure 1.
        Next, consider the following test method:
4       Georg Schmid and Viktor Kunčak

def test(t: Tree[Int], c: Cell[Int]) = {
  require(c.value == 0)
  reads(t.repr ++ Set[AnyHeapRef](c))
  modifies(t.repr)

  t.tmap(x ⇒ (x | 1))
} ensuring( ⇒ c.value == 0)

   If we mark tmap using the @opaque annotation to prevent function unfolding
and try to verify test, the system reports a counterexample, such as this one:
Found counter−example:
   t: Tree[Int] → Leaf[Int](HeapRef(4))
   c: HeapRef → HeapRef(4)
   heap0: Map[HeapRef, Object] → {HeapRef(4) →
         Cell(Cell[Object](SignedBitvector32(0))), ∗ → SignedBitvector32(2)}

indicating that, when tmap is approximated with its effects, the ensuring clause
can be violated when tree t contains precisely the reference c.
    To illustrate specification of stronger correctness properties, we show that
tmap behaves like map on purely functional lists. This stronger specification of
tmap is in the ensuring (postcondition) clause of the version of tmap in Figure 2
(line 21). The property is interesting because it gives us assurance of correct-
ness while being able to write code that reuses memory locations and permits
parallelization. The property is expressed by defining an abstraction function [1]
toList that maps the tree into the sequence of elements stored in its leaf cells.
(The purely functional List data type and the map function on lists are defined in
the standard library of Stainless.) To prove the ensuring clause, it is necessary to
introduce a precondition for tmap, expressed using the construct require(valid).
The valid method returns true when all subtrees store disjoint cells. The tmap
method may then only be called when this predicate holds. The assertion on
line 14 follows directly from valid and expresses disjointness of the side effects
of calls on line 15, which makes it easy for a program transformation to safely
parallelize these calls [8]. Remarkably, although it expresses separation, the valid
method in this implementation does not depend on the content of mutable cells,
but only on the identity of references. Our tool checks this independence thanks
to the absence of reads and modifies clauses in the signature of valid. Because
it does not depend on mutable state, valid trivially continues to hold after tmap
is invoked.
    In many cases our tool can automatically prove properties of interest thanks
to SMT solvers and the unfolding algorithm of Stainless. On the other hand,
showing complex properties such as functional correctness in this case may re-
quire different types of hints. If the size and the complexity of SMT formulas
overwhelm the solver the user can use auxiliary assertions, expressed using assert
and check functions in Figure 2. The system also requires guidance for induc-
tive properties when reasoning does not follow the pattern of functions that are
iteratively unfolded. In such cases, we need to introduce lemmas and prove them
using recursion to express inductive arguments, as with lemmaMapConcat defined
                     Proving and Disproving Programs with Shared Mutable Data               5


 1   def tmap(f: T ⇒ T): Unit = { // strong specification
 2     reads(repr)
 3     modifies(repr)
 4     require(valid)
 5     @ghost val oldList = toList
 6
 7     this match {
 8       case Leaf(data) ⇒
 9          data.value = f(data.value)
10          ghost { check(toList == oldList.map(f)) }
11
12       case Branch(left, right) ⇒
13         @ghost val (oldList1, oldList2) = (left.toList, right.toList)
14         assert(left.repr ∩ right.repr == ∅)
15         left.tmap(f); right.tmap(f)
16         ghost {
17            lemmaMapConcat(oldList1, oldList2, f)
18            check(toList == oldList.map(f))
19         }
20     }
21   } ensuring ( ⇒ toList == old(toList.map(f))) // main property
22
23   def valid: Boolean = // tree invariant: subtrees store disjoint cells
24     this match {
25       case Leaf(data) ⇒ true
26       case Branch(left, right) ⇒
27          left.repr ∩ right.repr == ∅ &&
28          left.valid && right.valid
29     }
30
31   def toList: List[T] = { // abstraction function
32     reads(repr)
33     this match {
34       case Leaf(data) ⇒ List(data.value)
35       case Branch(left, right) ⇒ left.toList ++ right.toList
36     }
37   }
38
39   def lemmaMapConcat[T, R](xs: List[T], ys: List[T], f: T ⇒ R): Unit = {
40     xs match {
41       case Nil() ⇒ ()
42       case Cons( , xs) ⇒ lemmaMapConcat(xs, ys, f)
43     }
44   } ensuring ( ⇒ xs.map(f) ++ ys.map(f) == (xs ++ ys).map(f))


     Fig. 2. Functional correctness of the tmap method including the abstraction function,
     the invariant, and a proven lemma about purely functional lists. We use ∩ to display
     intersection of sets &, and use ∅ for the empty set of heap references Set[AnyHeapRef]().
     The ++ symbol denotes concatenation of functional lists, as in Scala.
    6        Georg Schmid and Viktor Kunčak


1   case class HeapRef(id: BigInt)
2
3   case class CellData [T](value: T)
4
5   sealed abstract class Tree[T]
6   case class Leaf[T](dataref : HeapRef) extends Tree[T]
7   case class Branch[T](left: Tree[T], right: Tree[T]) extends Tree[T]

        Fig. 3. The data types of the running example in Section 2 after our encoding.


    in lines 39-44 and instantiated in line 17. With these specifications and hints in
    place, our tool successfully verifies the functional correctness and termination of
    tmap in a matter of seconds.


    3    Encoding
    We briefly describe our heap encoding and how it achieves framing without quan-
    tification. Our tool builds upon the existing counterexample-complete unfolding
    procedure of the Stainless verifier and exploits the additional expressive power
    afforded by combinatory array logic [13], an extended array theory available
    in Z3. This use of array combinators for framing is, to the best of our knowl-
    edge, novel. Notably, our encoding allows for a high degree of proof automation
    without giving up counterexamples.

    Heap Representation. Our tool models stateful operations by explicitly read-
    ing from and updating a global, mutable map that relates each object to its
    state. In a second transformation step such programs with local mutations are
    reduced to functional ones: We add an explicit, immutable heap parameter to
    each procedure and return a new, potentially updated heap along with the reg-
    ular outputs. Stateful operations such as reads and writes within the procedure
    are thus replaced by pure operations on a map. Given our context of Scala, a
    statically-typed language, the heap is internally modelled by a map heap of type
    Heap = Map[HeapRef, Any] where Any is the top type and HeapRef is a data
    type representing an object’s identity.

    Encoding tmap. We will explain our encoding by the example of the minimally-
    specified version of tmap on Tree (cf. Figure 1). In Figure 3 we show the data
    types after transformation. We treat heap types, i.e., descendants of AnyHeapRef,
    like Cell, differently from immutable types such as Tree. The latter are translated
    into algebraic data types in the obvious way (lines 5-7). References to heap types,
    on the other hand, are erased to the internal ADT HeapRef that is isomorphic to
    the natural numbers (line 1). For instance, the field data: Cell[T] of Leaf becomes
    dataref : HeapRef (line 6). Additionally, each heap class like Cell is translated to a
    single-constructor ADT that encapsulates an object’s state at a given time, e.g.,
    CellData (line 3).
                          Proving and Disproving Programs with Shared Mutable Data            7


 1   def tmap[T](h0: Heap, t: Tree[T], f: T ⇒ T): (Unit, Heap) = {
 2     val (rs, ms) = (repr(t), repr(t))
 3     t match {
 4       case Leaf(dataref ) ⇒
 5          assert(dataref ∈ rs, ”‘data‘ must be in reads set”)
 6          assert(dataref ∈ ms, ”‘data‘ must be in modifies set”)
 7          val data: CellData = {
 8            assume(h0(dataref ).isInstanceOf[CellData [T]])
 9            h0(dataref ).asInstanceOf[CellData [T]]
10          }
11          val data’: CellData = CellData (f(data.value))
12          ((), h0.updated(dataref , data’))
13
14           case Branch(left, right) ⇒
15             val ( , h1) = tmapshim (h0, rs, ms, left, f)
16             tmapshim (h1, rs, ms, right, f)
17       }
18   }
19
20   def tmapshim [T](h0: Heap, rd: RSet, md: RSet, t: Tree[T], f: T ⇒ T): (Unit, Heap) = {
21     val (rs, ms) = (repr(t), repr(t))
22     assert(rs ⊆ rd, ”reads set of Tree.tmap”)
23     assert(ms ⊆ md, ”modifies set of Tree.tmap”)
24     val res @ ( , h1) = tmap(h0, t, f)
25     assume(res == tmap(rs.mapMerge(h0, dummyHeap), t, f))
26     assume(h1 == ms.mapMerge(h1, h0))
27     res
28   }

     Fig. 4. The result of encoding the minimally-specified tmap method of Section 2. We
     use ⊆ to typeset subsetOf, ∈ for contains, and abbreviate Set[AnyHeapRef] by RSet.


         In Figure 4 we show the encoding of tmap itself. The method is reduced to a
     type-parametric function that takes its original argument f, the method receiver
     t and a heap parameter h0. The imperative operations in tmap are translated
     to functional operations on Heap as mentioned above, and the modified heap is
     returned along with the original return value. In particular, if the current tree t
     is a leaf, then we extract its reference to a cell dataref (line 4) and index the initial
     heap h0 at dataref (line 9). Note that since the heap map stores values of type Any
     we have to perform a downcast (lines 8-9). This is safe, since we will only verify
     well-typed Scala programs, so any such cast will be correct by construction. On
     line 11 we apply the function f to the old value of data and construct a CellData
     value reflecting the new state of data. We then return the updated heap on line
     12. In case the tree t is a Branch we simply perform two recursive calls (lines
     15-16), albeit through the newly-introduced wrapper function tmapshim .
         Our encoding achieves modular verification of heap contracts (reads and
     modifies) by injecting some additional assertions and assumptions. We bind the
8       Georg Schmid and Viktor Kunčak

reads and modifies sets (rs and ms) at the top of the function (line 2). For each
object that is read or modified we check that the object is in the respective set
(lines 5-6). For function calls we check that the callee’s reads, resp. modifies,
set is subsumed by the caller’s. We achieve this by invoking a wrapper function
tmapshim , that additionally takes as parameters the domains on which the passed
heap is defined for reads and modifications (rd and md). Within the wrapper we
bind the original function’s reads and modifies sets (line 21), check subsumption
wrt. the domains (lines 22-23) and call the original function tmap (line 24).
Finally, we also add the modular guarantees about tmap as assumptions: namely,
that the result of tmap only depends on the reads subset of the heap (line 25),
and that the heap resulting from tmap may only have changed on objects in
modifies (line 26). These two assumptions are encoded using the mapMerge
primitive, which can be seen as a ternary operator of type ∀ K V. Set[K] ⇒
Map[K,V] ⇒ Map[K,V] ⇒ Map[K,V]. Specifically, mapMerge takes a set s along
with two maps m1, m2 and produces a map m’ = s.mapMerge(m1, m2) such that
∀ k:K. (k ∈ s → m’[k] = m1[k]) ∧ (k 6∈ s → m’[k] = m2[k]).

Quantifier-Free Frame Conditions. For our encoding of frame conditions we
leverage the fact that Stainless translates both sets and maps to the theory of
(infinite, extensional) arrays in Z3. This means that reads and modifies expres-
sions of type Set[AnyHeapRef] become arrays typed HeapRef ⇒ Boolean, while
heap maps of type Map[HeapRef, Any] are translated to HeapRef ⇒ Any. We can
then use the array combinator mapf (a1 , . . . , an ) to express mapMerge efficiently.
This array combinator is part of Z3’s extended array theory [13] and axioma-
tized as ∀i. mapf (a1 , . . . , an )[i] = f (a1 [i], . . . , an [i]). While the combinator can
in practice only be used with built-in functions, this is sufficient for our purposes:
Given Stainless’ encoding of sets and maps, one can use the if-then-else function
ite of Z3, and translate s.mapMerge(m1, m2) as mapite ([s], [m1], [m2]).


4    Experience
We used our system to verify a number of benchmarks ranging in size and
complexity. Among the examples we developed are both shallowly and deeply
mutable data structures, a model of an object allocator, and a parallelization
primitive for the fork-join model. Below we discuss our experience using the tool.
Shallowly-Mutable Data Structures. We first consider “shallowly-mutable”
data structures such as Cell[T] seen in Section 2 whose mutable data is stored
directly in its fields, i.e., without any indirection. They provide a simple base-
line for our system and play an important role as building blocks for larger
data structures such as trees and arrays with fine-grained separation properties.
However, shallowly-mutable data structures are useful in their own right: For
instance, we implemented UpCounter which tracks a monotonically increasing
variable and maintains an invariant relative to the counter’s initial value. We
also implemented a simple array (SimpleArray) and stack (SimpleStack) which
essentially act as wrappers around functional data structures in that they only
               Proving and Disproving Programs with Shared Mutable Data             9

store the reference to the head of an immutable list. For instance, SimpleArray[T]
consists of a single mutable field var data: List[T]. In our examples we show safety
wrt. bounds checks and non-emptyness when popping an element off the stack.
We found that our system easily deals with this kind of mutability, in particular
since the associated operations typically require no recursion through stateful
functions, making them straightforward to verify and invalidate with counter-
examples.
Mutable Linked Lists and Queues. As an example of a more complex data
structure we implemented multiple variations of a mutable, acyclic singly-linked
list. We focussed on an append operation, which takes two valid linked lists l1
and l2 with disjoint representations and concatenates them, leaving l1 in a valid
state. This is challenging, since establishing the well-formedness of lists (e.g., the
absence of cycles) requires knowledge of heap separation and an inductive proof
that maintains the property for intermediate nodes.
     We considered several options to track a node’s representation repr. One
could express repr as a recursive function as in Section 2, or, instead, as a muta-
ble @ghost field on each node. In our benchmarks we present two variants of the
latter approach: MutList encodes the ghost field repr as List[AnyHeapRef], which
has the added benefit of allowing predicates like valid to recurse on the represen-
tation, and can be converted to a Set[AnyHeapRef] as required by our reads and
modifies clauses. MutListSetsOnly instead implements repr as Set[AnyHeapRef],
whose encoded form requires no further conversion to interact with the mapMerge
primitive we use for framing.
     We used a similar approach to implement Queue, which provides constant-
time enqueue and dequeue methods using references to the first and last nodes.
Given a valid queue we prove that enqueue and dequeue are functionally cor-
rect with respect to a serialized representation similar to toList in Section 2.
The example demonstrates how safety properties can be established even in the
presence of sharing and arbitrarily deep data structures.
Slices and Monolithic Arrays. Arrays are one of the most common data
structures found in imperative code and thus a worthwhile target for verifica-
tion. When specifying algorithms involving arrays it often pays to introduce
slices, i.e., subarrays, as a means of abstraction. By extending the SimpleArray
example we arrived at ArraySlice which provides safe indexing, update and re-
slicing operations wrt. an underlying array. In the absence of sharing, this so-
lution of encapsulating all array state in a single “monolithic” mutable heap
object (the underlying array) is the natural and practical choice. To analyze
divide-and-conquer algorithms on arrays, on the other hand, we require some
more fine-grained control, since we would like our dynamic frames to reflect the
fact that slices of an array may only access a subset of heap locations.
Cell-Based Data Structures. A more complex representation based on lists
of Cell[T]s allows us to achieve fine-grained framing of arrays and slices. In ex-
ample CellArraySimple we illustrate this approach and verify safety of accesses. A
more elaborate example, CellDataStructuresAndRepr, provides generalized infras-
tructure around splittable data structures. We provide an interface Repr that, at
     10        Georg Schmid and Viktor Kunčak


 1   abstract class Task {
 2     @ghost def readSet: Set[AnyHeapRef]
 3     @ghost def writeSet: Set[AnyHeapRef] = { ??? } ensuring ( ⊆ readSet)
 4
 5       def run(): Unit = { reads(readSet); modifies(writeSet); ??? : Unit }
 6   }
 7
 8   def parallel(task1: Task, task2: Task): Unit = {
 9     reads(task1.readSet ++ task2.readSet)
10     modifies(task1.writeSet ++ task2.writeSet)
11     require((task1.writeSet ∩ task2.readSet == ∅) &&
12              (task2.writeSet ∩ task1.readSet == ∅))
13     task1.run(); task2.run() // task1 and task2 complete before this function returns
14   }

     Fig. 5. An interface for asynchronous computations and a sequential specification for
     fork-join parallelism. The ??? denotes unimplemented code in abstract classes.




     its heart, requires implementers to provide a list of objects which make up the
     mutable representation of the data structure, and a proof of uniqueness within
     that list. Using Repr we can streamline proofs of heap separation for divide-
     and-conquer-style algorithms. In this particular example, we implemented and
     verified the functional correctness of a copy operation on cell-based array slices.


     Fork-Join Parallelism. Since dynamic frames in our system are simply given
     by read-only expressions, users may define their own imperative abstractions.
     For instance, in TaskParallel we demonstrate how one can specify a primitive
     modelling fork-join parallelism. Figure 5 shows an excerpt introducing the Task
     interface that encapsulates an asynchronous computation and declares the set
     of heap objects that may be read and modified in the process. Further below
     we define the parallel(t1, t2) construct itself, imposing a number of restrictions:
     Firstly, callers of parallel have to establish accessibility to both t1 and t2’s frames
     (lines 9-10). Secondly, we require that the read set of t1 is disjoint from t2’s write
     set and vice-versa (lines 11-12). This separation property justifies replacing our
     sequential model of parallel by a more efficient runtime implementation executing
     the two tasks concurrently. Users can define new asynchronous tasks by imple-
     menting Task. Operations such as those on cell-based data structures discussed
     above are straightforward to parallelize in this way. Our introductory example
     (Section 2) could be parallelized by defining a new class TMapTask[T](t: Tree[T],
     f: T ⇒ T) whose run method calls tmap, and replacing the recursive calls in tmap
     by parallel(TMapTask(left, f), TMapTask(right, f)).

        Based on this experience, we are confident that our tool brings substantial
     value to the practice of verification of Scala programs.
                Proving and Disproving Programs with Shared Mutable Data               11

References
 1. Abadi, M., Lamport, L.: The existence of refinement mappings. Theor. Comput.
    Sci. 82(2), 253–284 (1991). https://doi.org/10.1016/0304-3975(91)90224-P
 2. Barnett, M., Chang, B.E., DeLine, R., Jacobs, B., Leino, K.R.M.: Boogie: A
    modular reusable verifier for object-oriented programs. In: de Boer, F.S.,
    Bonsangue, M.M., Graf, S., de Roever, W.P. (eds.) Formal Methods for
    Components and Objects, 4th International Symposium, FMCO 2005,
    Amsterdam, The Netherlands, November 1-4, 2005, Revised Lectures. Lecture
    Notes in Computer Science, vol. 4111, pp. 364–387. Springer (2005).
    https://doi.org/10.1007/11804192 17
 3. Blelloch, G.E.: Programming parallel algorithms. Commun. ACM 39(3), 85–97
    (Mar 1996). https://doi.org/10.1145/227234.227246,
    https://doi.org/10.1145/227234.227246
 4. Calcagno, C., Distefano, D., O’Hearn, P.W., Yang, H.: Compositional shape
    analysis by means of bi-abduction. J. ACM 58(6), 26:1–26:66 (2011).
    https://doi.org/10.1145/2049697.2049700
 5. Distefano, D., Fähndrich, M., Logozzo, F., O’Hearn, P.W.: Scaling static analyses
    at Facebook. Commun. ACM 62(8), 62–70 (2019).
    https://doi.org/10.1145/3338112
 6. Hamza, J., Voirol, N., Kunčak, V.: System FR: Formalized foundations for the
    Stainless verifier. Proc. ACM Program. Lang OOPSLA (November 2019).
    https://doi.org/https://doi.org/10.1145/3360592
 7. Hawblitzel, C., Howell, J., Kapritsos, M., Lorch, J.R., Parno, B., Roberts, M.L.,
    Setty, S.T.V., Zill, B.: Ironfleet: proving practical distributed systems correct. In:
    Miller, E.L., Hand, S. (eds.) Proceedings of the 25th Symposium on Operating
    Systems Principles, SOSP 2015, Monterey, CA, USA, October 4-7, 2015. pp.
    1–17. ACM (2015). https://doi.org/10.1145/2815400.2815428
 8. Hendren, L.J., Nicolau, A.: Parallelizing programs with recursive data structures.
    IEEE Trans. Parallel Distributed Syst. 1(1), 35–47 (1990).
    https://doi.org/10.1109/71.80123
 9. Kassios, I.T.: Dynamic frames: Support for framing, dependencies and sharing
    without restrictions. In: Misra, J., Nipkow, T., Sekerinski, E. (eds.) FM 2006:
    Formal Methods, 14th International Symposium on Formal Methods, Hamilton,
    Canada, August 21-27, 2006, Proceedings. Lecture Notes in Computer Science,
    vol. 4085, pp. 268–283. Springer (2006). https://doi.org/10.1007/11813040 19
10. Leino, K.R.M.: Dafny: An automatic program verifier for functional correctness.
    In: Clarke, E.M., Voronkov, A. (eds.) Logic for Programming, Artificial
    Intelligence, and Reasoning - 16th International Conference, LPAR-16, Dakar,
    Senegal, April 25-May 1, 2010, Revised Selected Papers. Lecture Notes in
    Computer Science, vol. 6355, pp. 348–370. Springer (2010).
    https://doi.org/10.1007/978-3-642-17511-4 20
11. de Moura, L.M., Bjørner, N.: Model-based theory combination. Electron. Notes
    Theor. Comput. Sci. 198(2), 37–49 (2008).
    https://doi.org/10.1016/j.entcs.2008.04.079
12. de Moura, L.M., Bjørner, N.: Z3: an efficient SMT solver. In: Ramakrishnan,
    C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis of
    Systems, 14th International Conference, TACAS 2008, Held as Part of the Joint
    European Conferences on Theory and Practice of Software, ETAPS 2008,
    Budapest, Hungary, March 29-April 6, 2008. Proceedings. Lecture Notes in
12      Georg Schmid and Viktor Kunčak

    Computer Science, vol. 4963, pp. 337–340. Springer (2008).
    https://doi.org/10.1007/978-3-540-78800-3 24
13. de Moura, L.M., Bjørner, N.: Generalized, efficient array decision procedures. In:
    Proceedings of 9th International Conference on Formal Methods in
    Computer-Aided Design, FMCAD 2009, 15-18 November 2009, Austin, Texas,
    USA. pp. 45–52. IEEE (2009). https://doi.org/10.1109/FMCAD.2009.5351142,
    https://doi.org/10.1109/FMCAD.2009.5351142
14. Odersky, M., Spoon, L., Venners, B.: Programming in Scala, Fourth Edition (A
    comprehensive step-by-step guide). Artima (2019),
    https://www.artima.com/shop/programming in scala 4ed
15. O’Hearn, P.W., Reynolds, J.C., Yang, H.: Local reasoning about programs that
    alter data structures. In: Fribourg, L. (ed.) Computer Science Logic, 15th
    International Workshop, CSL 2001. 10th Annual Conference of the EACSL, Paris,
    France, September 10-13, 2001, Proceedings. Lecture Notes in Computer Science,
    vol. 2142, pp. 1–19. Springer (2001). https://doi.org/10.1007/3-540-44802-0 1
16. Smans, J., Jacobs, B., Piessens, F.: Implicit dynamic frames. ACM Trans.
    Program. Lang. Syst. 34(1), 2:1–2:58 (2012).
    https://doi.org/10.1145/2160910.2160911
